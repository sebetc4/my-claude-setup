#!/usr/bin/env python3
"""Run the static checks on every skill in this repository.

Usage: python3 tests/check.py [--skip-skills] [--brief] [SKILLS_DIR]

--skip-skills leaves out the checks of the skills themselves, which the skill audit
hook makes at each edit; --brief reports each failing unit test on one line, its id and
the first line of its failure, instead of unittest's whole output.

Skills are found under domains/*/skills/, or directly under SKILLS_DIR when it
is given. Every skill gets the checks in tests/skills.py. A skill also gets the
checks in its own evals/checks.py when that file exists, and its
evals/test_*.py unit tests are run. The unit tests in tests/test_*.py, domains/*/tests/test_*.py and shared/*/tests/test_*.py are run as well.
Every domain under domains/ gets the checks in tests/domains.py.
Every copy of a shared module must equal its source under shared/ (tools/shared.py).
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


def options(argv):
    parser = argparse.ArgumentParser(description="Run the static checks and unit tests of this repository.")
    parser.add_argument("--skip-skills", action="store_true", help="leave out the checks of the skills themselves")
    parser.add_argument("--brief", action="store_true", help="one line per failing unit test")
    parser.add_argument("skills_dir", nargs="?", type=Path)
    args = parser.parse_args(argv)
    base = args.skills_dir.resolve() if args.skills_dir else None
    found = base.glob("*/SKILL.md") if base else ROOT.glob("domains/*/skills/*/SKILL.md")
    args.all_skills = sorted(p.parent for p in found)
    args.skills = [] if args.skip_skills else args.all_skills
    return args


def main(argv=None):
    args = options(sys.argv[1:] if argv is None else argv)
    skills = args.skills
    if not args.all_skills:
        print("no skill found under " + (str(args.skills_dir) if args.skills_dir else f"{ROOT}/domains/*/skills"))
        return 1
    common = load(TESTS / "skills.py")
    problems, warnings = [], []
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
        for domain in sorted(p for p in ROOT.glob("domains/*") if p.is_dir() and not p.name.startswith((".", "__"))):
            problems.extend(domain_checks.run(domain))
        problems.extend(load(ROOT / "tools" / "shared.py").stale(ROOT))
    unit_tests = (sorted(TESTS.glob("test_*.py")) + sorted(ROOT.glob("domains/*/tests/test_*.py"))
                  + sorted(ROOT.glob("shared/*/tests/test_*.py")))
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
