#!/usr/bin/env python3
"""Run the static checks on every skill in this repository.

Usage: python3 tests/check.py [--skip-skills] [--brief] [SKILLS_DIR]

--skip-skills leaves out the checks of the skills themselves, which the skill audit
hook makes at each edit; --brief reports each failing unit test on one line, its id and
the first line of its failure, instead of unittest's whole output.

Skills are found under each folder that `dirs` names in the [skills] table of the
repository's .agent-conventions.toml, or under domains/*/skills/ with a warning when the
table cannot be read, or directly under SKILLS_DIR when it is given. Every skill gets the
checks in tests/skills.py. A skill also gets the checks in its own evals/checks.py when
that file exists, and its evals/test_*.py unit tests are run. The unit tests in tests/test_*.py, domains/*/tests/test_*.py and shared/*/tests/test_*.py are run as well.
Every domain under domains/ gets the checks in tests/domains.py.
Every copy of a shared module must equal its source under shared/ (tools/shared.py).
A domain's release on main without its tag is a warning (tools/tags.py).
Each problem is printed as path:line: message, and the exit status is 1 when any problem is found.
"""

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
DEFAULT_DIRS = ["domains/*/skills"]


def shown(path):
    return path.relative_to(ROOT) if path.is_relative_to(ROOT) else path


def load(path):
    spec = importlib.util.spec_from_file_location(f"checks_{path.parent.parent.name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BLOCK_RE = re.compile(r"^(FAIL|ERROR): (\S+) \(([^)]*)\)\n-+\n(.*?)(?=^=+$|^-+\nRan |\Z)", re.M | re.S)
EXCEPTION_RE = re.compile(r"^[A-Za-z_][\w.]*(?:Error|Exception|Exit|Interrupt)\b.*$", re.M)


def brief(stderr):
    """One line per failing test of unittest's stderr: its kind, name and id, then the first
    line of its exception — the last one for a module that could not load."""
    lines = []
    for kind, name, where, body in BLOCK_RE.findall(stderr):
        found = EXCEPTION_RE.findall(body)
        cause = (found[-1] if "_FailedTest" in where else found[0]) if found else body.strip().splitlines()[-1]
        lines.append(f"{kind} {name} ({where}): {cause.strip()}")
    if not lines:
        found = EXCEPTION_RE.findall(stderr)
        lines.append(found[-1].strip() if found else (stderr.strip().splitlines() or ["no output"])[-1])
    return lines


def skill_dirs(root):
    """The folders [skills] names in root's conventions; DEFAULT_DIRS and a warning when
    the table cannot be read."""
    conventions = load(ROOT / "shared" / "conventions" / "conventions.py")
    path = root / conventions.FILE
    result = conventions.load("skills", root, path) if path.is_file() else None
    if result and result.status == "ok":
        return result.values["dirs"], []
    cause = "; ".join(result.problems) if result else "no file"
    return DEFAULT_DIRS, [(path, 1, f"[skills] not read ({cause}): checking {', '.join(DEFAULT_DIRS)}")]


def options(argv, root=ROOT):
    parser = argparse.ArgumentParser(description="Run the static checks and unit tests of this repository.")
    parser.add_argument("--skip-skills", action="store_true", help="leave out the checks of the skills themselves")
    parser.add_argument("--brief", action="store_true", help="one line per failing unit test")
    parser.add_argument("skills_dir", nargs="?", type=Path)
    args = parser.parse_args(argv)
    base = args.skills_dir.resolve() if args.skills_dir else None
    if base:
        args.searched, args.notes = [base], []
        found = base.glob("*/SKILL.md")
    else:
        dirs, args.notes = skill_dirs(root)
        args.searched = [root / d for d in dirs]
        found = (p for d in dirs for p in root.glob(f"{d}/*/SKILL.md"))
    args.all_skills = sorted({p.parent for p in found})
    args.skills = [] if args.skip_skills else args.all_skills
    return args


def main(argv=None, root=ROOT):
    args = options(sys.argv[1:] if argv is None else argv, root)
    skills = args.skills
    if not args.all_skills:
        print("no skill found under " + ", ".join(map(str, args.searched)))
        return 1
    common = load(TESTS / "skills.py")
    problems, warnings = [], list(args.notes)
    for skill in skills:
        suites = [common]
        specific = skill / "evals" / "checks.py"
        if specific.is_file():
            suites.append(load(specific))
        for suite in suites:
            problems.extend(suite.run(skill))
        warnings.extend(common.warnings(skill))
    if args.skills_dir is None:
        domain_checks = load(TESTS / "domains.py")
        for domain in sorted(p for p in root.glob("domains/*") if p.is_dir() and not p.name.startswith((".", "__"))):
            problems.extend(domain_checks.run(domain))
        problems.extend(load(ROOT / "tools" / "shared.py").stale(root))
        warnings.extend(load(ROOT / "tools" / "tags.py").warnings(root))
    unit_tests = (sorted((root / "tests").glob("test_*.py")) + sorted(root.glob("domains/*/tests/test_*.py"))
                  + sorted(root.glob("shared/*/tests/test_*.py")))
    for skill in args.all_skills:
        unit_tests.extend(sorted((skill / "evals").glob("test_*.py")))
    for test in unit_tests:
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", str(test)],
                                capture_output=True, text=True, cwd=test.parent)
        if result.returncode and args.brief:
            problems.extend((test, 1, line) for line in brief(result.stderr))
        elif result.returncode:
            problems.append((test, 1, "unit tests failed\n" + result.stderr.strip()))
    for path, line, message in problems + warnings:
        print(f"{shown(path)}:{line}: {message}")
    tail = f", {len(warnings)} warning(s)" if warnings else ""
    print(f"{len(skills)} skill(s) checked, {len(problems)} problem(s){tail}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
