#!/usr/bin/env python3
"""Build the folder a fixture case of authoring-skills' evals starts in.

Usage: fixtures.py <case> <folder>

scripts/workspace.py runs it once per fixture case when it prepares an iteration. Each
case starts in a repository of the sample skill, writing-notes (sample/):

  evaluate-an-edit   two commits: the skill without its `## Next` section, then the
                     commit that adds it; the skill has no evals yet
  read-the-results   the skill with its evals and ten trigger queries, and under the
                     ignored workspace an iteration run, graded and benchmarked, and a
                     trigger eval: evaluate/results/, copied
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "evaluate/results"
NEXT = "\nClose the note with a `## Next` section"

_spec = importlib.util.spec_from_file_location("sample_build", HERE / "sample/build.py")
sample = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sample)


def git(folder, *args):
    subprocess.run(["git", *args], cwd=folder, check=True, capture_output=True, env=sample.GIT_ENV)


def evaluate_an_edit(folder):
    skill = folder / "skills" / sample.NAME
    skill.mkdir(parents=True)
    (folder / ".agent-conventions.toml").write_text(sample.CONVENTIONS, encoding="utf-8")
    (folder / ".gitignore").write_text("/.eval-runs/\n", encoding="utf-8")
    text = (HERE / "sample/skill.md").read_text(encoding="utf-8")
    (skill / "SKILL.md").write_text(text.split(NEXT)[0].rstrip() + "\n", encoding="utf-8")
    git(folder, "init", "-q")
    git(folder, "add", "-A")
    git(folder, "commit", "-q", "-m", "Add the writing-notes skill")
    (skill / "SKILL.md").write_text(text, encoding="utf-8")
    git(folder, "commit", "-q", "-am", "Close each note with a Next section")


def read_the_results(folder):
    skill = sample.build(folder)
    found = json.loads(next((RESULTS / "triggers").glob("*.json")).read_text(encoding="utf-8"))
    evals = json.loads((skill / "evals/evals.json").read_text(encoding="utf-8"))
    evals["triggers"] = [{k: q[k] for k in ("query", "should_trigger", "near") if k in q}
                         for q in found["queries"]]
    (skill / "evals/evals.json").write_text(json.dumps(evals, indent=2) + "\n", encoding="utf-8")
    git(folder, "commit", "-q", "--amend", "--no-edit", "-a")
    shutil.copytree(RESULTS, folder / ".eval-runs/skills" / sample.NAME)


CASES = {"evaluate-an-edit": evaluate_an_edit, "read-the-results": read_the_results}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__.splitlines()[2])
    if sys.argv[1] not in CASES:
        sys.exit(f"no fixture named {sys.argv[1]}: {', '.join(CASES)}")
    CASES[sys.argv[1]](Path(sys.argv[2]).resolve())
