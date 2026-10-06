#!/usr/bin/env python3
"""Prepare an iteration of a skill's evals under the repository's eval workspace.

Usage: workspace.py <skill-dir> [--baseline <git revision or folder>] [--baseline-only]
                    [--reuse <iteration>] [--runs N] [--model ID] [--effort LEVEL]
                    [--budget USD] [--case NAME ...]

Validates the skill's evals.json, refusing an unknown key, a missing one or a wrong type
by name, then writes <workspace>/skills/<skill-name>/iteration-N/, the workspace being the
[skills] table's of .agent-conventions.toml:

  iteration.json            the cases, configurations, runs each, model, effort, budget,
                            and the evals folder, where grade.py finds the skill's own
  with_skill/<skill-name>/  the skill without its evals folder
  old_skill/<skill-name>/   with --baseline, that version without its evals folder
  base.tar                  for a `repository` case: the files git tracks or does not
                            ignore, and .agent-conventions.toml, without the skill's folder
                            or the workspace; each run puts its own version of the skill back
  <case>/eval_metadata.json the case, and the digest of what its runs receive
  <case>/files/             the case's files, at their paths in the evals folder, or in
                            the skill for a file outside it
  <case>/fixture.tar        for a `fixture` case, what evals/fixtures.py <case> <folder> built
  <case>/<configuration>/run-N/

The configurations are with_skill and without_skill, or with_skill and old_skill with
--baseline; --baseline-only prepares the second alone, as before a skill is written.
--reuse takes the baseline's runs from an earlier iteration for each case whose digest,
model, effort and baseline are the same, without their grading.json.
Prints the iteration's folder, then one line per case. Exits 1 on a refusal, one problem
per line.
"""

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conventions  # noqa: E402  (same directory, not an installed package)

EVALS = "evals"
MODEL = "claude-sonnet-5-5"
EFFORT = "xhigh"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
RUNS = 3
BUDGET = 5.0
KINDS = ("reference", "task", "discipline")
SETUPS = ("repository", "empty", "fixture")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CACHES = ("__pycache__",)

# key: (type, required). A type is "string", "strings", "integer", "boolean", "env",
# or a tuple of allowed strings.
TOP = {"skill_name": ("string", True), "env": ("env", False), "evals": ("cases", True),
       "triggers": ("triggers", False)}
CASE = {"id": ("integer", True), "name": ("string", True), "kind": (KINDS, True), "setup": (SETUPS, True),
        "exclude": ("strings", False), "prompt": ("string", True), "files": ("strings", False),
        "expected_output": ("string", True), "assertions": ("strings", False), "review": ("strings", False),
        "pressures": ("strings", False), "failures_without_skill": ("strings", False),
        "failures_with_skill": ("strings", False), "pending": ("string", False)}
TRIGGER = {"query": ("string", True), "should_trigger": ("boolean", True), "near": ("string", False)}
METADATA = ("id", "name", "kind", "setup", "prompt", "expected_output", "assertions", "review", "pressures",
            "files", "exclude")


class Refused(Exception):
    def __init__(self, *problems):
        super().__init__("\n".join(problems))
        self.problems = list(problems)


def type_problem(value, kind):
    """What is wrong with value for kind, or None."""
    if kind == "string" and not isinstance(value, str):
        return "expected a string"
    if kind == "strings" and not (isinstance(value, list) and all(isinstance(v, str) for v in value)):
        return "expected a list of strings"
    if kind == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        return "expected an integer"
    if kind == "boolean" and not isinstance(value, bool):
        return "expected a boolean"
    if isinstance(kind, tuple) and value not in kind:
        return f"expected one of {', '.join(kind)}, got {json.dumps(value)}"
    return None


def check_keys(item, schema, where):
    """Problems of one object against schema: unknown keys, missing keys, wrong types."""
    if not isinstance(item, dict):
        return [f"{where}: expected an object"]
    problems = [f"{where}: unknown key `{key}`" for key in item if key not in schema]
    problems += [f"{where}: missing key `{key}`" for key, (_, required) in schema.items()
                 if required and key not in item]
    for key, (kind, _) in schema.items():
        if key in item and kind not in ("cases", "triggers", "env"):
            problem = type_problem(item[key], kind)
            if problem:
                problems.append(f"{where}.{key}: {problem}".lstrip("."))
    return problems


def validate(data, skill, evals):
    """The problems of evals.json's data for the skill whose evals folder is evals."""
    if not isinstance(data, dict):
        return ["expected an object"]
    problems = [p.replace(": unknown", "unknown", 1) if p.startswith(": ") else p
                for p in check_keys(data, TOP, "")]
    if isinstance(data.get("skill_name"), str) and data["skill_name"] != skill.name:
        problems.append(f"skill_name: `{data['skill_name']}` is not the skill's folder name `{skill.name}`")
    env = data.get("env", {})
    if not isinstance(env, dict):
        problems.append("env: expected an object of strings")
    else:
        problems += [f"env.{key}: expected a string" for key, value in env.items() if not isinstance(value, str)]
    cases = data.get("evals", [])
    if not isinstance(cases, list) or not cases:
        problems.append("evals: expected a list of one case or more")
        cases = []
    ids, names = set(), set()
    for i, case in enumerate(cases):
        where = f"evals[{i}]"
        problems += check_keys(case, CASE, where)
        if not isinstance(case, dict):
            continue
        if isinstance(case.get("id"), int):
            if case["id"] in ids:
                problems.append(f"{where}.id: {case['id']} is already used")
            ids.add(case["id"])
        name = case.get("name")
        if isinstance(name, str):
            if not NAME_RE.match(name):
                problems.append(f"{where}.name: expected lowercase letters, digits and hyphens, got `{name}`")
            if name in names:
                problems.append(f"{where}.name: `{name}` is already used")
            names.add(name)
        if "exclude" in case and case.get("setup") != "repository":
            problems.append(f"{where}.exclude: only a `repository` case excludes paths")
        if case.get("setup") == "fixture" and not (skill / evals / "fixtures.py").is_file():
            problems.append(f"{where}.setup: a `fixture` case needs `{evals}/fixtures.py`")
        if type_problem(case.get("files", []), "strings") is None:
            for path in case.get("files", []):
                target = Path(os.path.normpath(skill / path))
                if Path(path).is_absolute() or not target.is_relative_to(skill):
                    problems.append(f"{where}.files: `{path}` lies outside the skill")
                elif not target.is_file():
                    problems.append(f"{where}.files: `{path}` does not exist")
    triggers = data.get("triggers", [])
    if not isinstance(triggers, list):
        problems.append("triggers: expected a list")
        triggers = []
    for i, trigger in enumerate(triggers):
        problems += check_keys(trigger, TRIGGER, f"triggers[{i}]")
    return problems


def load(skill, evals=EVALS):
    """evals.json of the skill, validated; Refused with every problem otherwise."""
    shown = f"{evals}/evals.json"
    path = skill / evals / "evals.json"
    if not path.is_file():
        raise Refused(f"no `{shown}` in {skill}: write the skill's evals first")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refused(f"{shown} is not valid JSON: {error}")
    problems = validate(data, skill, evals)
    if problems:
        raise Refused(*(f"{shown}: {p}" for p in problems))
    return data


def read_conventions(skill):
    """(root, workspace, evals folder) from the repository's [skills] table."""
    result = conventions.read("skills", start=skill)
    if result.status != "ok":
        raise Refused(f"the conventions file is {result.status}: follow references/conventions.md",
                      *result.problems)
    if "workspace" not in result.values:
        raise Refused(f"`workspace` is not declared in the [skills] table of {result.file}: declare it, "
                      "following references/conventions.md")
    return result.root, result.root / result.values["workspace"], result.values.get("evals", EVALS)


def git(folder, *args, binary=False):
    result = subprocess.run(["git", "-C", str(folder), *args], capture_output=True, text=not binary)
    return result.returncode, result.stdout


def file_digest(path):
    if path.is_symlink():
        return "link:" + os.readlink(path)
    mode = "x" if path.stat().st_mode & 0o100 else "-"
    return mode + hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(folder, skip=()):
    """One digest over the files under folder, by path, content, link target and executable bit."""
    digest = hashlib.sha256()
    for path in sorted(p for p in folder.rglob("*") if p.is_file() or p.is_symlink()):
        relative = path.relative_to(folder)
        if relative.parts[0] in skip:
            continue
        digest.update(f"{relative.as_posix()}\0{file_digest(path)}\0".encode())
    return digest.hexdigest()


def copy_skill(source, target, evals):
    """Copy a skill's folder without its evals folder or caches."""
    def ignore(folder, names):
        left = [n for n in names if n in CACHES]
        if Path(folder).resolve() == (source / evals).parent.resolve():
            left += [n for n in names if n == Path(evals).name]
        return left
    shutil.copytree(source, target, symlinks=True, ignore=ignore)


def resolve_baseline(argument, skill):
    """(record, folder or None, commit or None) for --baseline: a folder, else a git revision."""
    folder = Path(argument).expanduser()
    if folder.is_dir():
        return {"folder": str(folder.resolve())}, folder.resolve(), None
    code, commit = git(skill, "rev-parse", "--verify", "--quiet", f"{argument}^{{commit}}")
    if code != 0:
        raise Refused(f"--baseline `{argument}` is neither a folder nor a git revision")
    commit = commit.strip()
    _, top = git(skill, "rev-parse", "--show-toplevel")
    top = Path(top.strip()).resolve()
    relative = skill.relative_to(top).as_posix()
    code, _ = git(top, "cat-file", "-e", f"{commit}:{relative}")
    if code != 0:
        raise Refused(f"revision `{argument}` holds no `{relative}`")
    return {"revision": argument, "commit": commit}, None, (top, commit, relative)


def snapshot_revision(top, commit, relative, target, evals):
    """Extract the skill's folder at commit into target, without its evals folder or caches."""
    code, data = git(top, "archive", "--format=tar", commit, "--", relative, binary=True)
    if code != 0:
        raise Refused(f"git archive of `{relative}` at {commit} failed")
    prefix = relative + "/"
    target.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        members = []
        for member in tar.getmembers():
            if not member.name.startswith(prefix):
                continue
            member.name = member.name[len(prefix):]
            parts = Path(member.name).parts
            if (member.name.startswith(evals.rstrip("/") + "/") or member.name == evals.rstrip("/")
                    or any(p in CACHES for p in parts)):
                continue
            members.append(member)
        tar.extractall(target, members=members, filter="data")


def base_files(root, skill, workspace):
    """The repository's files a run's copy holds: tracked or not ignored, the conventions
    file, never the skill's folder or the workspace."""
    code, top = git(root, "rev-parse", "--show-toplevel")
    if code != 0:
        raise Refused(f"a `repository` case needs a git repository: {root} is not one")
    _, listed = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    paths = {p for p in listed.split("\0") if p}
    if (root / conventions.FILE).is_file():
        paths.add(conventions.FILE)
    left_out = [skill.relative_to(root)]
    if workspace.is_relative_to(root):
        left_out.append(workspace.relative_to(root))
    kept = []
    for path in sorted(paths):
        full = root / path
        if any(Path(path).is_relative_to(out) for out in left_out):
            continue
        if full.is_symlink() or full.is_file():
            kept.append(path)
    return kept


def write_base(root, paths, target):
    """base.tar from paths under root; its digest."""
    digest = hashlib.sha256()
    with tarfile.open(target, "w") as tar:
        for path in paths:
            tar.add(root / path, arcname=path, recursive=False)
            digest.update(f"{path}\0{file_digest(root / path)}\0".encode())
    return digest.hexdigest()


def build_fixture(skill, evals, name, target):
    """Run evals/fixtures.py <name> <folder> in a fresh folder, archive what it built into
    target; the digest of its files, git's own folder left out."""
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "fixture"
        folder.mkdir()
        result = subprocess.run([sys.executable, str(skill / evals / "fixtures.py"), name, str(folder)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            message = (result.stderr or result.stdout).strip() or f"exit code {result.returncode}"
            raise Refused(f"`{evals}/fixtures.py {name}` failed: {message}")
        with tarfile.open(target, "w") as tar:
            for child in sorted(folder.iterdir()):
                tar.add(child, arcname=child.name)
        return tree_digest(folder, skip=(".git",))


def in_evals(path, evals):
    """A case file's path in a run's folder: relative to the evals folder when it lies
    there, so that no run's folder holds an evals folder; relative to the skill otherwise."""
    path = Path(os.path.normpath(path))
    return path.relative_to(evals) if path.is_relative_to(evals) else path


def case_digest(case, env, files, base, fixture):
    """The digest of what a run of case receives; assertions and review items left out."""
    record = {"prompt": case["prompt"], "setup": case["setup"], "exclude": case.get("exclude", []),
              "env": env, "files": files, "base": base, "fixture": fixture}
    return hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()


def find_iteration(skills_dir, name):
    folder = Path(name)
    folder = folder if folder.is_absolute() else skills_dir / folder
    if not (folder / "iteration.json").is_file():
        raise Refused(f"no iteration `{name}` under {skills_dir}")
    return folder


def next_iteration(skills_dir):
    numbers = [int(m.group(1)) for p in skills_dir.glob("iteration-*")
               if (m := re.fullmatch(r"iteration-(\d+)", p.name))]
    return skills_dir / f"iteration-{max(numbers, default=0) + 1}"


def prepare(skill, baseline=None, baseline_only=False, reuse=None, runs=RUNS, model=MODEL, effort=EFFORT,
            budget=BUDGET, cases=None):
    """Write the next iteration of the skill's evals; its folder. Refused before anything is
    written when the evals, the conventions or the options are wrong."""
    skill = Path(skill).resolve()
    root, workspace, evals = read_conventions(skill)
    data = load(skill, evals)
    chosen = data["evals"]
    if cases:
        known = {c["name"] for c in chosen}
        unknown = [f"no case named `{name}` in {evals}/evals.json" for name in cases if name not in known]
        if unknown:
            raise Refused(*unknown)
        chosen = [c for c in chosen if c["name"] in cases]
    if not baseline_only and not (skill / "SKILL.md").is_file():
        raise Refused("the skill has no `SKILL.md` yet: prepare its baseline alone with --baseline-only")
    record, folder, revision = resolve_baseline(baseline, skill) if baseline else (None, None, None)
    reference = "old_skill" if baseline else "without_skill"
    configurations = ([] if baseline_only else ["with_skill"]) + [reference]
    skills_dir = workspace / "skills" / skill.name
    previous = find_iteration(skills_dir, reuse) if reuse else None
    paths = base_files(root, skill, workspace) if any(c["setup"] == "repository" for c in chosen) else None

    iteration = next_iteration(skills_dir)
    iteration.mkdir(parents=True)
    try:
        return fill(iteration, skill, root, evals, data, chosen, configurations, record, folder, revision,
                    previous, paths, runs, model, effort, budget)
    except BaseException:
        shutil.rmtree(iteration, ignore_errors=True)
        raise


def fill(iteration, skill, root, evals, data, chosen, configurations, record, folder, revision, previous,
         paths, runs, model, effort, budget):
    name = skill.name
    if "with_skill" in configurations:
        copy_skill(skill, iteration / "with_skill" / name, evals)
    snapshot = None
    if "old_skill" in configurations:
        target = iteration / "old_skill" / name
        if folder:
            copy_skill(folder, target, evals)
        else:
            snapshot_revision(*revision, target, evals)
        snapshot = tree_digest(target)
    base = write_base(root, paths, iteration / "base.tar") if paths is not None else None
    env = data.get("env", {})
    earlier = json.loads((previous / "iteration.json").read_text(encoding="utf-8")) if previous else None
    reference = configurations[-1]
    reused = {}
    for case in chosen:
        folder_ = iteration / case["name"]
        folder_.mkdir()
        files = {}
        for path in case.get("files", []):
            target = folder_ / "files" / in_evals(path, evals)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill / path, target)
            files[path] = file_digest(target)
        fixture = None
        if case["setup"] == "fixture":
            fixture = build_fixture(skill, evals, case["name"], folder_ / "fixture.tar")
        digest = case_digest(case, env, files, base if case["setup"] == "repository" else None, fixture)
        metadata = {key: case.get(key, []) for key in METADATA} | {"digest": digest}
        (folder_ / "eval_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        for configuration in configurations:
            for number in range(1, runs + 1):
                (folder_ / configuration / f"run-{number}").mkdir(parents=True)
        if earlier and reusable(previous, earlier, case["name"], digest, reference, model, effort, snapshot):
            take_runs(previous / case["name"] / reference, folder_ / reference, runs)
            reused[case["name"]] = previous.name
    recorded = {
        "skill_name": name, "root": str(root), "skill": str(skill),
        "skill_path": skill.relative_to(root).as_posix(), "evals": evals,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cases": [c["name"] for c in chosen], "configurations": configurations, "runs": runs,
        "model": model, "effort": effort, "budget_usd": budget, "baseline": record,
        "snapshot_digest": snapshot, "base_digest": base, "env": env, "reused": reused,
    }
    (iteration / "iteration.json").write_text(json.dumps(recorded, indent=2) + "\n", encoding="utf-8")
    return iteration


def reusable(previous, earlier, name, digest, reference, model, effort, snapshot):
    """Whether the earlier iteration's baseline runs of case name stand for this one's."""
    path = previous / name / "eval_metadata.json"
    if not path.is_file() or reference not in earlier["configurations"]:
        return False
    same = json.loads(path.read_text(encoding="utf-8")).get("digest") == digest
    return (same and (earlier["model"], earlier["effort"]) == (model, effort)
            and earlier.get("snapshot_digest") == snapshot)


def take_runs(source, target, runs):
    """Copy the earlier runs into the new iteration's empty run folders, grades left out."""
    for number in range(1, runs + 1):
        run = source / f"run-{number}"
        if run.is_dir():
            destination = target / f"run-{number}"
            shutil.rmtree(destination)
            shutil.copytree(run, destination, symlinks=True, ignore=shutil.ignore_patterns("grading.json"))


def summary(iteration):
    recorded = json.loads((iteration / "iteration.json").read_text(encoding="utf-8"))
    runs = recorded["runs"]
    count = f"{runs} run" + ("" if runs == 1 else "s")
    lines = [str(iteration)]
    for name in recorded["cases"]:
        parts = []
        for configuration in recorded["configurations"]:
            part = f"{configuration} {count}"
            if name in recorded["reused"] and configuration == recorded["configurations"][-1]:
                part += f" reused from {recorded['reused'][name]}"
            parts.append(part)
        lines.append(f"{name}: {', '.join(parts)}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepare an iteration of a skill's evals under the "
                                     "repository's eval workspace.")
    parser.add_argument("skill", type=Path, help="the skill's folder")
    parser.add_argument("--baseline", help="the previous version, a git revision or a folder, for an edit")
    parser.add_argument("--baseline-only", action="store_true", help="prepare the baseline alone")
    parser.add_argument("--reuse", help="an earlier iteration whose baseline runs this one takes")
    parser.add_argument("--runs", type=int, default=RUNS, help=f"runs per case and configuration ({RUNS})")
    parser.add_argument("--model", default=MODEL, help=f"the runs' model, by its full id ({MODEL})")
    parser.add_argument("--effort", default=EFFORT, choices=EFFORTS, help=f"the runs' effort ({EFFORT})")
    parser.add_argument("--budget", type=float, default=BUDGET, help=f"the ceiling per run, in dollars ({BUDGET})")
    parser.add_argument("--case", dest="cases", action="append", help="a case to prepare; every case by default")
    args = parser.parse_args(argv)
    if args.runs < 1 or args.budget <= 0:
        parser.error("--runs and --budget must be positive")
    try:
        iteration = prepare(args.skill, baseline=args.baseline, baseline_only=args.baseline_only,
                            reuse=args.reuse, runs=args.runs, model=args.model, effort=args.effort,
                            budget=args.budget, cases=args.cases)
    except Refused as refusal:
        for problem in refusal.problems:
            print(problem, file=sys.stderr)
        return 1
    print(summary(iteration))
    return 0


if __name__ == "__main__":
    sys.exit(main())
