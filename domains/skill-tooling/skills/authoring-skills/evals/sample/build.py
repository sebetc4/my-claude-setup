#!/usr/bin/env python3
"""Build the sample skill's repository, on which the evaluation scripts are checked.

Usage: build.py <folder>

Writes <folder> as a git repository of one commit holding .agent-conventions.toml, whose
[skills] table puts the workspace in .eval-runs/, and skills/writing-notes/, its SKILL.md
from skill.md and its evals/evals.json from evals.json. Prints the skill's folder. The
sample's cases work in an empty folder: a run costs little.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "writing-notes"
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "sample", "GIT_AUTHOR_EMAIL": "sample@localhost",
           "GIT_COMMITTER_NAME": "sample", "GIT_COMMITTER_EMAIL": "sample@localhost"}


def build(folder):
    folder = Path(folder).resolve()
    skill = folder / "skills" / NAME
    (skill / "evals").mkdir(parents=True)
    (folder / ".agent-conventions.toml").write_text(CONVENTIONS, encoding="utf-8")
    (folder / ".gitignore").write_text("/.eval-runs/\n", encoding="utf-8")
    shutil.copy(HERE / "skill.md", skill / "SKILL.md")
    shutil.copy(HERE / "evals.json", skill / "evals" / "evals.json")
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "sample")):
        subprocess.run(["git", *args], cwd=folder, check=True, capture_output=True, env=GIT_ENV)
    return skill


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__.splitlines()[2])
    print(build(sys.argv[1]))
