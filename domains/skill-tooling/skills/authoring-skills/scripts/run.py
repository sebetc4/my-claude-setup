#!/usr/bin/env python3
"""Start the runs of an iteration that workspace.py prepared, as unattended agent sessions.

Usage: run.py <iteration> [--start] [--jobs N] [--timeout MINUTES] [--case NAME ...] | --status

Lists the runs to start — each case, configuration and number not yet complete — with
their count and estimated cost: the mean cost of the skill's complete runs at the
iteration's model and effort, or $2.50 a run when there is none. Starts nothing without
--start; with it, starts them --jobs at a time and prints one line per run as it starts
and as it ends. A run the subscription's usage limit stops leaves the runs not yet
started unstarted, since each would stop at once. --status prints where each run
stands, a running one with its calls, its cost so far and its last call, read from its
transcript as it is written; it starts nothing. --case limits the runs listed and started
to the cases named.

Each run works in a temporary folder outside any repository: work/, where the session
starts, holds the repository without the skill's folder and with the arm's version put
back at its path, the case's fixture, or an empty folder, with the case's files, made a
git repository; a skill's arm adds skill/<skill-name>/, the copy the prompt names. The
session takes the iteration's model, effort and ceiling, the evals' env, and guard.py,
which refuses any call naming the real repository or the real configuration folder.
The prompt is a preamble, a line `---`, then the case's prompt.

Into the run's folder go prompt.md, result.json, response.md, transcript.jsonl and
transcript.md, outputs/ (the files the run added or changed, at their paths),
changes.json, and run.json: status, claude version, models and efforts read from the
transcript, tokens, cost, duration, refusals, the files of the skill's copy the run
named and any path of the real repository it named. A run stopped by its ceiling, a
limit or an error is marked stopped; the next --start starts it again from a fresh
folder, and skips the complete runs. While a run goes, its folder holds running.json: its
session id, start and the pid of run.py.
"""

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
import tempfile
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402  (same directory, not an installed package)
import usage  # noqa: E402

GUARD = Path(__file__).resolve().parent / "guard.py"
JOBS = 4
TIMEOUT = 120
DEFAULT_COST = 2.50
PREAMBLE = ("Work on the request below, in this folder. Nobody can answer a question during this "
            "session: where you would ask one, take the most reasonable assumption, say which, and "
            f"go on. Do not start a `{harness.COMMAND}` session. End with an account of what you did.")
SKILL_LINE = "Use the skill `{name}`, whose copy is at `{path}`: read its `SKILL.md` and follow it."
GIT_ENV = {"GIT_AUTHOR_NAME": "eval", "GIT_AUTHOR_EMAIL": "eval@localhost",
           "GIT_COMMITTER_NAME": "eval", "GIT_COMMITTER_EMAIL": "eval@localhost"}
# git's empty tree, to compare against when a fixture brings a repository without a commit.
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
PATH_END = r"[^\s'\"`;|&()<>]*"


class Refused(Exception):
    pass


@dataclass
class Run:
    case: str
    configuration: str
    number: int
    folder: Path

    @property
    def name(self):
        return f"{self.case}/{self.configuration}/run-{self.number}"

    def recorded(self):
        path = self.folder / "run.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def status(self):
        return (self.recorded() or {}).get("status")

    def running(self):
        try:
            return json.loads((self.folder / "running.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def plan(iteration, recorded):
    return [Run(case, configuration, number, iteration / case / configuration / f"run-{number}")
            for case in recorded["cases"] for configuration in recorded["configurations"]
            for number in range(1, recorded["runs"] + 1)]


def estimate(iteration, recorded):
    """(cost per run, what it rests on)."""
    model, effort = recorded["model"], recorded["effort"]
    costs = []
    for path in iteration.parent.glob("iteration-*/*/*/run-*/run.json"):
        try:
            run = read_json(path)
        except (OSError, ValueError):
            continue
        if ((run.get("status"), run.get("model"), run.get("effort")) == ("complete", model, effort)
                and run.get("cost_usd") is not None):
            costs.append(run["cost_usd"])
    if costs:
        cost = statistics.mean(costs)
        basis = f"${cost:.2f} a run, the mean of {len(costs)} complete runs of this skill at {model} and {effort}"
    else:
        cost = DEFAULT_COST
        basis = (f"$2.50 a run, the mean of a full skill-writing task measured on 2026-10-06, since no run of this "
                 f"skill at {model} and {effort} is complete")
    ceiling = recorded["budget_usd"]
    if cost > ceiling:
        return ceiling, f"the run's ceiling, ${ceiling:.2f}, below {basis}"
    return cost, basis


def check_outside(folder):
    """Refuse a temporary folder that lies inside a repository."""
    for place in (folder, *folder.parents):
        for marker in (".git", ".agent-conventions.toml"):
            if (place / marker).exists():
                raise Refused(f"the temporary folder {folder} lies inside a repository ({place / marker}): "
                              "point TMPDIR outside any repository, or leave it unset")


def git(work, *args):
    return subprocess.run(["git", "-C", str(work), *args], capture_output=True, text=True,
                          env={**os.environ, **GIT_ENV})


def extract(archive, target, left_out=()):
    """Extract archive into target, without the paths left out."""
    left_out = [p.rstrip("/") for p in left_out]
    with tarfile.open(archive) as tar:
        members = [m for m in tar.getmembers()
                   if not any(m.name == p or m.name.startswith(p + "/") for p in left_out)]
        tar.extractall(target, members=members, filter="data")


def arm_copy(iteration, recorded, configuration):
    """The arm's version of the skill in the iteration, or None for the arm without it."""
    if configuration == "without_skill":
        return None
    return iteration / configuration / recorded["skill_name"]


def build_work(run, iteration, recorded, metadata, tmp):
    """The run's work/ folder, a git repository; its starting commit."""
    work = tmp / "work"
    work.mkdir()
    case_folder = iteration / run.case
    if metadata["setup"] == "repository":
        extract(iteration / "base.tar", work, metadata.get("exclude", []))
        source = arm_copy(iteration, recorded, run.configuration)
        if source:
            shutil.copytree(source, work / recorded["skill_path"], symlinks=True)
    elif metadata["setup"] == "fixture":
        extract(case_folder / "fixture.tar", work)
    if (case_folder / "files").is_dir():
        shutil.copytree(case_folder / "files", work, symlinks=True, dirs_exist_ok=True)
    if not (work / ".git").exists():
        for args in (("init", "-q"), ("add", "-A", "-f"), ("commit", "-q", "--allow-empty", "-m", "base")):
            done = git(work, *args)
            if done.returncode != 0:
                raise Refused(f"git {args[0]} in the run's folder failed: {done.stderr.strip()}")
    head = git(work, "rev-parse", "HEAD")
    return work, head.stdout.strip() if head.returncode == 0 else None


def prompt_of(metadata, name, copy):
    head = [PREAMBLE] + ([SKILL_LINE.format(name=name, path=copy)] if copy else [])
    return "\n\n".join(head) + "\n\n---\n\n" + metadata["prompt"].strip() + "\n"


def collect(work, start, outputs):
    """Copy the files the run added or changed into outputs; {added, modified, deleted}."""
    git(work, "add", "-A")
    listed = git(work, "diff", "--cached", "--name-status", "--no-renames", "-z", start or EMPTY_TREE)
    fields = [f for f in listed.stdout.split("\0") if f]
    changes = {"added": [], "modified": [], "deleted": []}
    for letter, path in zip(fields[::2], fields[1::2]):
        key = {"A": "added", "D": "deleted"}.get(letter[0], "modified")
        changes[key].append(path)
        if key != "deleted" and (work / path).is_file():
            target = outputs / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(work / path, target)
    return {key: sorted(paths) for key, paths in changes.items()}


def named(calls, folder):
    """The paths under folder that the calls name, relative to it."""
    found = re.compile(re.escape(str(folder)) + r"(?:/(" + PATH_END + "))?")
    paths = set()
    for _, given in calls:
        for text in harness.strings(given):
            for match in found.finditer(text):
                paths.add(match.group(1) or ".")
    return sorted(paths)


def denied_paths(recorded):
    paths = [Path(recorded["root"]), harness.config_dir()]
    home_config = Path.home() / ".claude"
    if home_config not in paths:
        paths.append(home_config)
    return paths


def execute(run, iteration, recorded, metadata, binary, version, timeout, limit=None):
    """Start one run and write its folder; its run.json. limit, a threading.Event, is set
    when the subscription's usage limit stopped the run."""
    for child in list(run.folder.iterdir()) if run.folder.exists() else []:
        shutil.rmtree(child) if child.is_dir() and not child.is_symlink() else child.unlink()
    run.folder.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    session_id = str(uuid.uuid4())
    (run.folder / "running.json").write_text(json.dumps({"session_id": session_id, "started": started,
                                                         "pid": os.getpid()}) + "\n", encoding="utf-8")
    record = {"case": run.case, "configuration": run.configuration, "run": run.number, "status": "stopped",
              "reason": None, "claude_version": version, "model": recorded["model"], "effort": recorded["effort"],
              "budget_usd": recorded["budget_usd"], "started": started}
    tmp = Path(tempfile.mkdtemp(prefix="skill-run-")).resolve()
    try:
        check_outside(tmp)
        work, start = build_work(run, iteration, recorded, metadata, tmp)
        source = arm_copy(iteration, recorded, run.configuration)
        copy = None
        if source:
            copy = tmp / "skill" / recorded["skill_name"]
            shutil.copytree(source, copy, symlinks=True)
        env = harness.environment(os.environ, {k: v.replace("{tmp}", str(tmp))
                                               for k, v in recorded.get("env", {}).items()})
        settings = harness.hook_settings("PreToolUse", harness.guard_command(GUARD, denied_paths(recorded)))
        line = harness.command(binary, recorded["model"], recorded["effort"], recorded["budget_usd"], settings,
                               add_dirs=[copy] if copy else [], session_id=session_id)
        prompt = prompt_of(metadata, recorded["skill_name"], copy)
        (run.folder / "prompt.md").write_text(prompt, encoding="utf-8")
        session = harness.start(line, work, prompt, env, timeout)
        result = harness.result_of(session.stdout)
        if result is not None:
            (run.folder / "result.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        else:
            (run.folder / "stdout.txt").write_text(session.stdout, encoding="utf-8")
        if session.stderr.strip():
            (run.folder / "stderr.txt").write_text(session.stderr, encoding="utf-8")
        record["status"], record["reason"] = harness.outcome(session, result)
        if limit is not None and harness.limit_reached(result):
            limit.set()
        figures = harness.figures(result)
        (run.folder / "response.md").write_text(figures.pop("response").strip() + "\n", encoding="utf-8")
        record.update(figures)
        record["session_id"] = record["session_id"] or session_id
        if record["duration_s"] is None:
            record["duration_s"] = round(session.seconds, 1)
        transcript = harness.transcript_of(record["session_id"])
        calls = []
        if transcript:
            shutil.copy2(transcript, run.folder / "transcript.jsonl")
            (run.folder / "transcript.md").write_text(harness.render(transcript), encoding="utf-8")
            counted = usage.as_json(usage.count([transcript]))
            record.update({"models": {m: t["calls"] for m, t in counted["models"].items()},
                           "efforts": counted["efforts"], "calls": counted["calls"],
                           "estimated_calls": counted["estimated"], "tokens": counted["tokens"],
                           "cost_usd": counted["cost"], "prices": counted["prices"]})
            calls = harness.tool_calls(transcript)
        elif record["status"] == "complete":
            record["status"], record["reason"] = "stopped", "transcript not found"
        changes = collect(work, start, run.folder / "outputs")
        (run.folder / "changes.json").write_text(json.dumps(changes, indent=1) + "\n", encoding="utf-8")
        record["skill_reads"] = named(calls, copy) if copy else []
        record["repository_paths"] = named(calls, recorded["root"])
    except Exception as error:  # a run that fails is recorded and started again by the next --start
        record["status"], record["reason"] = "stopped", f"error: {error}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        (run.folder / "running.json").unlink(missing_ok=True)
        record["ended"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        (run.folder / "run.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def line_of(run, record):
    text = f"{run.name}: {record['status']}"
    if record.get("reason"):
        text += f" ({record['reason']})"
    if record.get("cost_usd") is not None:
        text += f", ${record['cost_usd']:.2f}"
    if record.get("duration_s") is not None:
        minutes, seconds = divmod(int(record["duration_s"]), 60)
        text += f", {minutes}m{seconds:02d}s"
    return text


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (PermissionError, TypeError, ValueError, OverflowError):
        return isinstance(pid, int)
    return True


def short(given, width=80):
    """A call's input in a few words: its command or path, else its JSON."""
    text = next((given[k] for k in ("command", "file_path", "path", "pattern", "url", "query")
                 if isinstance(given.get(k), str)), None) if isinstance(given, dict) else None
    text = " ".join((text if text is not None else json.dumps(given)).split())
    return text if len(text) <= width else text[:width - 1] + "…"


def progress(run, recorded):
    """(state, where the run stands in one line)."""
    running = run.running()
    if running:
        if not alive(running.get("pid")):
            return "interrupted", (f"{run.name}: interrupted, started {running.get('started')}: run.py ended "
                                   "before the run")
        text = f"{run.name}: running since {running.get('started')}"
        transcript = harness.transcript_of(running.get("session_id"))
        if not transcript:
            return "running", text + ", no call yet"
        counted = usage.as_json(usage.count([transcript]))
        cost = "an unknown cost" if counted["cost"] is None else f"${counted['cost']:.2f}"
        text += f", {plural(counted['calls'], 'call')}, {cost} of ${recorded['budget_usd']:.2f}"
        calls = harness.tool_calls(transcript)
        if calls:
            text += f", last: {calls[-1][0]} {short(calls[-1][1])}"
        return "running", text
    record = run.recorded()
    return (record["status"], line_of(run, record)) if record else ("not started", f"{run.name}: not started")


def show_status(iteration, recorded):
    runs = plan(iteration, recorded)
    found = [progress(run, recorded) for run in runs]
    for _, line in found:
        print(line)
    states = [state for state, _ in found]
    counts = {state: states.count(state) for state in dict.fromkeys(states)}
    print(", ".join(f"{count} {state}" for state, count in counts.items()) + f", of {plural(len(runs), 'run')}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Start the runs of an iteration that workspace.py prepared.")
    parser.add_argument("iteration", type=Path, help="the iteration's folder")
    parser.add_argument("--start", action="store_true", help="start the runs; without it, only list them")
    parser.add_argument("--jobs", type=int, default=JOBS, help=f"runs at a time ({JOBS})")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help=f"minutes before a run is stopped ({TIMEOUT})")
    parser.add_argument("--status", action="store_true", help="print where each run stands, and start nothing")
    parser.add_argument("--case", dest="cases", action="append", help="a case whose runs to list or start; every "
                        "case by default")
    args = parser.parse_args(argv)
    iteration = args.iteration.resolve()
    try:
        recorded = read_json(iteration / "iteration.json")
    except (OSError, ValueError) as error:
        print(f"no iteration at {iteration}: {error}", file=sys.stderr)
        return 1
    if args.status:
        show_status(iteration, recorded)
        return 0
    unknown = [name for name in args.cases or [] if name not in recorded["cases"]]
    if unknown:
        for name in unknown:
            print(f"no case named `{name}` in the iteration", file=sys.stderr)
        return 1
    runs = [r for r in plan(iteration, recorded) if not args.cases or r.case in args.cases]
    todo = [r for r in runs if r.status() != "complete"]
    per_run, basis = estimate(iteration, recorded)
    for run in todo:
        status = run.status()
        print(run.name + (f" (again, {status})" if status else ""))
    print(f"{plural(len(todo), 'run')} to start, estimated ${len(todo) * per_run:.2f}: {basis}; "
          f"{plural(len(runs) - len(todo), 'complete run')} skipped.")
    if not args.start:
        print("Nothing started: run again with --start to start them.")
        return 0
    if not todo:
        return 0
    try:
        binary = harness.binary()
        version = harness.version(binary)
        check_outside(Path(tempfile.gettempdir()).resolve())
    except (harness.HarnessError, Refused) as error:
        print(error, file=sys.stderr)
        return 1
    lock, limit = threading.Lock(), threading.Event()

    def go(run):
        if limit.is_set():
            return None
        with lock:
            print(f"{run.name}: started", flush=True)
        record = execute(run, iteration, recorded, read_json(iteration / run.case / "eval_metadata.json"),
                         binary, version, args.timeout * 60, limit)
        with lock:
            print(line_of(run, record), flush=True)
        return record

    with ThreadPoolExecutor(max_workers=max(args.jobs, 1)) as pool:
        records = list(pool.map(go, todo))
    left = records.count(None)
    if left:
        print(f"{plural(left, 'run')} not started: the subscription's limit was reached; run again with --start "
              "once it resets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
