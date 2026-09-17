#!/usr/bin/env python3
"""Run the static checks on every skill in this repository.

Usage: python3 tests/check.py [SKILLS_DIR]

Every skill gets the checks in tests/skills/checks.py. A skill named NAME also
gets tests/NAME/checks.py when that file exists. Each problem is printed as
path:line: message, and the exit status is 1 when any problem is found.
"""

import importlib.util
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location(f"checks_{path.parent.name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    skills_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else TESTS.parent / "skills"
    skills = sorted(p.parent for p in skills_dir.glob("*/SKILL.md"))
    if not skills:
        print(f"no skill found under {skills_dir}")
        return 1
    common = load(TESTS / "skills" / "checks.py")
    problems = []
    for skill in skills:
        suites = [common]
        specific = TESTS / skill.name / "checks.py"
        if specific.is_file():
            suites.append(load(specific))
        for suite in suites:
            problems.extend(suite.run(skill))
    for path, line, message in problems:
        print(f"{path.relative_to(skills_dir.parent)}:{line}: {message}")
    print(f"{len(skills)} skill(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
