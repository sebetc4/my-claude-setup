#!/usr/bin/env python3
"""Run the static checks on every skill in this repository.

Usage: python3 tests/check.py [SKILLS_DIR]

Skills are found under domains/*/skills/, or directly under SKILLS_DIR when it
is given. Every skill gets the checks in tests/skills.py. A skill also gets the
checks in its own evals/checks.py when that file exists, and its
evals/test_*.py unit tests are run. The unit tests in tests/test_*.py and domains/*/tests/test_*.py are run as well.
Every domain under domains/ gets the checks in tests/domains.py.
Each problem is printed as path:line: message, and the exit status is 1 when any problem is found.
"""

import importlib.util
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


def main():
    if len(sys.argv) > 1:
        found = Path(sys.argv[1]).resolve().glob("*/SKILL.md")
    else:
        found = ROOT.glob("domains/*/skills/*/SKILL.md")
    skills = sorted(p.parent for p in found)
    if not skills:
        print("no skill found under " + (sys.argv[1] if len(sys.argv) > 1 else f"{ROOT}/domains/*/skills"))
        return 1
    common = load(TESTS / "skills.py")
    problems = []
    for skill in skills:
        suites = [common]
        specific = skill / "evals" / "checks.py"
        if specific.is_file():
            suites.append(load(specific))
        for suite in suites:
            problems.extend(suite.run(skill))
    if len(sys.argv) == 1:
        domain_checks = load(TESTS / "domains.py")
        for domain in sorted(p for p in ROOT.glob("domains/*") if p.is_dir() and not p.name.startswith((".", "__"))):
            problems.extend(domain_checks.run(domain))
    unit_tests = sorted(TESTS.glob("test_*.py")) + sorted(ROOT.glob("domains/*/tests/test_*.py"))
    for skill in skills:
        unit_tests.extend(sorted((skill / "evals").glob("test_*.py")))
    for test in unit_tests:
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", str(test)],
                                capture_output=True, text=True, cwd=test.parent)
        if result.returncode:
            problems.append((test, 1, "unit tests failed\n" + result.stderr.strip()))
    for path, line, message in problems:
        print(f"{shown(path)}:{line}: {message}")
    print(f"{len(skills)} skill(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
