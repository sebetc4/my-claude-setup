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
  evaluate-a-hooked-skill
                     the skill in a domain, domains/notes/, beside its hooks.json and
                     hooks/open_notes.py, a SessionStart hook naming the notes still in
                     draft; two commits: the skill, then the one that has it add to an
                     open note; no evals yet
  evaluate-a-later-step
                     the skill with its evals, and under the ignored workspace the
                     iteration of evaluate/results/, each run's note in its outputs/;
                     two commits: the skill, then the one that adds the closing
                     of a note, a later session's step
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
DOMAIN_CONVENTIONS = '[skills]\ndirs = ["domains/*/skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
OPEN_NOTE = """
When a line at this session's start names an open note — a note still in `status: draft` —
on the subject of the request, add to that note rather than write a new one: a dated
paragraph before its `## Next` section, and its `## Next` brought up to date.
"""
HOOKS = {"SessionStart": [{"hooks": [{"type": "command", "command": 'python3 "{{HOOKS_DIR}}/open_notes.py"'}]}]}
OPEN_NOTES = '''#!/usr/bin/env python3
"""SessionStart hook: name the notes of the session's folder still in draft, one line."""
import json
import sys
from pathlib import Path

event = json.load(sys.stdin)
folder = Path(event.get("cwd") or ".") / "notes"
found = sorted(p for p in folder.glob("*.md") if "\\nstatus: draft\\n" in p.read_text(encoding="utf-8"))
if found:
    names = ", ".join(p.relative_to(folder.parent).as_posix() for p in found)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                             "additionalContext": f"Open notes, still in draft: {names}."}}))
'''
DOMAIN_README = """# notes

The skill `writing-notes` and its hook. Installed into the agent's configuration with the
repository's installer, `hooks.json` runs `hooks/open_notes.py` at every session's start:
it names the notes of the session's folder still in `status: draft`.
"""
CLOSING = """
## Closing A Note

When asked to close a note, in a session after the one that wrote it: set its `status` to
`done`, and append each line of its `## Next` section but `None.` to `notes/next.md`,
prefixed with the note's file name and a colon.
"""

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


def evaluate_a_hooked_skill(folder):
    domain = folder / "domains/notes"
    skill = domain / "skills" / sample.NAME
    skill.mkdir(parents=True)
    (domain / "hooks").mkdir()
    (folder / ".agent-conventions.toml").write_text(DOMAIN_CONVENTIONS, encoding="utf-8")
    (folder / ".gitignore").write_text("/.eval-runs/\n", encoding="utf-8")
    (domain / "README.md").write_text(DOMAIN_README, encoding="utf-8")
    (domain / "hooks.json").write_text(json.dumps(HOOKS, indent=2) + "\n", encoding="utf-8")
    (domain / "hooks/open_notes.py").write_text(OPEN_NOTES, encoding="utf-8")
    text = (HERE / "sample/skill.md").read_text(encoding="utf-8")
    (skill / "SKILL.md").write_text(text, encoding="utf-8")
    git(folder, "init", "-q")
    git(folder, "add", "-A")
    git(folder, "commit", "-q", "-m", "Add the notes domain")
    (skill / "SKILL.md").write_text(text + OPEN_NOTE, encoding="utf-8")
    git(folder, "commit", "-q", "-am", "Add to an open note rather than write a new one")


def evaluate_a_later_step(folder):
    skill = sample.build(folder)
    shutil.copytree(RESULTS / "iteration-1", folder / ".eval-runs/skills" / sample.NAME / "iteration-1")
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    (skill / "SKILL.md").write_text(text + CLOSING, encoding="utf-8")
    git(folder, "commit", "-q", "-am", "Close a note in a later session")


def read_the_results(folder):
    skill = sample.build(folder)
    found = json.loads(next((RESULTS / "triggers").glob("*.json")).read_text(encoding="utf-8"))
    evals = json.loads((skill / "evals/evals.json").read_text(encoding="utf-8"))
    evals["triggers"] = [{k: q[k] for k in ("query", "should_trigger", "near") if k in q}
                         for q in found["queries"]]
    (skill / "evals/evals.json").write_text(json.dumps(evals, indent=2) + "\n", encoding="utf-8")
    git(folder, "commit", "-q", "--amend", "--no-edit", "-a")
    shutil.copytree(RESULTS, folder / ".eval-runs/skills" / sample.NAME)


CASES = {"evaluate-an-edit": evaluate_an_edit, "read-the-results": read_the_results,
         "evaluate-a-hooked-skill": evaluate_a_hooked_skill, "evaluate-a-later-step": evaluate_a_later_step}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__.splitlines()[2])
    if sys.argv[1] not in CASES:
        sys.exit(f"no fixture named {sys.argv[1]}: {', '.join(CASES)}")
    CASES[sys.argv[1]](Path(sys.argv[2]).resolve())
