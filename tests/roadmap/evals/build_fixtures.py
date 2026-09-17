#!/usr/bin/env python3
"""Build the fixture repositories and the run directories for the roadmap evaluations.

Usage: python3 tests/roadmap/evals/build_fixtures.py WORKSPACE

Creates WORKSPACE/fixtures/<scenario>/, a git repository per scenario, then one
fresh copy per version to compare:
WORKSPACE/iteration-1/eval-<scenario>/{new_skill,old_skill}/run-1/outputs/repo.
See grade.py for the whole evaluation procedure.
"""

import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RD = "docs/roadmap/on-progress/search-index"
PHASES = [("framing", "Framing"), ("tokenizer", "Tokenizer"), ("indexer", "Indexer"), ("results-page", "Results Page")]
TASKS = {0: ["Inventory current search queries", "Define index scope", "Choose storage format", "Write acceptance targets"],
         1: ["Rewrite the tokenizer for accented text", "Add tokenizer unit tests", "Batch index commits", "Extract text utilities"],
         2: ["Build the inverted index", "Add incremental updates", "Benchmark index build time", "Document the index format"],
         3: ["Render paginated results", "Highlight matched terms", "Add empty-state message", "Wire results to the index"]}
CONTRACT_FULL = "## Roadmaps\n\nRoot       : docs/roadmap/{pending,on-progress,completed}/\nLanguage   : english\nVersioning : git\n"
CONTRACT_NO_VERSIONING = "## Roadmaps\n\nRoot     : docs/roadmap/{pending,on-progress,completed}/\nLanguage : english\n"
GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True, env=GIT_ENV).stdout.strip()


def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(text)


def bar(done, total, started):
    filled = int(done / total * 20 + 0.5)
    if started and done < total:
        filled = max(filled, 1)
    if done < total:
        filled = min(filled, 19)
    return "█" * filled + "░" * (20 - filled)


def phase_file(n, status, started, completed):
    slug, name = PHASES[n]
    emoji, label = {"done": ("🟢", "Done"), "progress": ("🟡", "In Progress"), "todo": ("🔴", "Not Started")}[status]
    done = 4 if status == "done" else 0
    ticked = "x" if status != "todo" else " "
    before = "" if n == 0 else (
        f"## Before Starting This Phase\n\nRead `phase-{n-1}-{PHASES[n-1][0]}.md` and `phase-{n-1}-{PHASES[n-1][0]}-report.md` in full before\n"
        "touching anything here: the decisions already taken, the problems and\ndeviations recorded, and the changes made to this phase.\n\n---\n\n")
    tasks = "\n".join(f"- [{ticked}] {t}" for t in TASKS[n])
    return (f"# Phase {n}: {name}\n\n---\n\n## Status\n\n**Current Status:** {emoji} {label} ({100 if done else 0}% — {done}/4)\n"
            f"**Started:** {started}\n**Completed:** {completed}\n**Blocked By:** —\n\n---\n\n{before}"
            f"## While Working\n\nKeep `phase-{n}-{slug}-report.md` current as the work happens — after each significant\n"
            "step, and before every commit, pause, or end of session.\n\n---\n\n"
            f"## Objective\n\nDeliver the {name.lower()} stage of the search index.\n\n---\n\n## Overview\n\n"
            "### Why This Phase Matters\nSearch depends on it.\n\n### What It Enables\nThe next phase.\n\n### Out of Scope\nRanking.\n\n---\n\n"
            f"## Tasks\n\n### Work\n{tasks}\n\n---\n\n## Technical Details\n\n### Files to Modify\n```\nsrc/\n```\n\n"
            "### Dependencies\nNone.\n\n### Constraints\nNone.\n\n---\n\n"
            f"## Acceptance Criteria\n\n- [{ticked}] The {name.lower()} stage works end to end\n")


def report_file(n, start, closed):
    slug, name = PHASES[n]
    if closed:
        tail = ("\n---\n\n## Files Changed\n\n**Modified**\n- `src/search.py`\n\n---\n\n## Problems And Deviations\n\nNone.\n\n---\n\n"
                "## Changes To Later Phases\n\nNone.\n\n---\n\n## Assessment\n\nThe stage is complete and nothing is left open.\n")
    else:
        tail = "\n---\n\n## Files Changed\n\n\n---\n\n## Problems And Deviations\n\n\n---\n\n## Changes To Later Phases\n\n\n---\n\n## Assessment\n\n"
    return (f"# Phase {n} Report: {name}\n\n**Phase:** [phase-{n}-{slug}.md](phase-{n}-{slug}.md)\n**Start Commit:** {start}\n\n---\n\n"
            f"## Work Log\n\n### 2026-09-0{n + 1}\n\nWorked through the {name.lower()} stage in the order the code required.\n\n---\n\n"
            f"## Decisions\n\n- **Keep the stage self-contained.** It keeps the next phase independent.\n{tail}")


def readme(statuses, current, blocked, milestone, version):
    lines, done_total = [], 0
    for n, (slug, name) in enumerate(PHASES):
        done = 4 if statuses[n] == "done" else 0
        done_total += done
        emoji = {"done": "🟢", "progress": "🟡", "todo": "🔴"}[statuses[n]]
        lines.append(f"Phase {n}  {name:<27}{emoji} {bar(done, 4, statuses[n] != 'todo')} {int(done / 4 * 100 + 0.5):>3}%  ({done}/4)")
    lines.append(f"TOTAL{'':<34}{bar(done_total, 16, done_total > 0)} {int(done_total / 16 * 100 + 0.5):>3}%  ({done_total}/16)")
    phases = "\n".join(f"- {({'done': '🟢', 'progress': '🟡', 'todo': '🔴'}[statuses[n]])} [Phase {n}: {name}](phase-{n}-{slug}.md)"
                       for n, (slug, name) in enumerate(PHASES))
    return ("# Roadmap: Search Index\n\n---\n\n## Status Indicators\n\n- 🔴 Not Started\n- 🟡 In Progress\n- 🟢 Done\n- ⏸️ Blocked\n- ⚠️ Needs Review\n\n---\n\n"
            "## Overall Progress\n\n```\n" + "\n".join(lines) + f"\n```\n\n**Current Phase:** {current}\n**Blocked By:** {blocked}\n"
            f"**Next Milestone:** {milestone}\n\n---\n\n## Why This Roadmap Exists\n\nFull-text search replaces the current substring match.\n\n---\n\n"
            "## Decisions Taken At Opening\n\nThe index lives in the application database.\n\n---\n\n"
            "## Deliberately Out Of Scope\n\nRelevance ranking.\n\n---\n\n## Phases\n\n" + phases + "\n\n---\n\n"
            f"## Metadata\n\n**Roadmap Status:** 🟡 In Progress\n**Location:** `{RD}/`\n**Version:** {version}\n"
            f"**Created:** 2026-09-01\n**Last Updated:** 2026-09-10\n\n---\n\n## Changelog\n\n### {version} (2026-09-10)\n\nLatest phase closed.\n\n"
            "### 1.0.0 (2026-09-01)\n\nRoadmap created with four phases.\n")


def base_repo(path, contract):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    git(path, "init", "-q", "-b", "main")
    write(path / "CLAUDE.md", "# Search App\n\nA small web app with a search feature.\n\n" + contract)
    for name, text in {"src/search.py": "def search(q):\n    return []\n", "src/tokenizer.py": "def tokenize(s):\n    return s.split()\n",
                       "src/util.py": "def clean(s):\n    return s.strip()\n", "src/legacy_index.py": "INDEX = {}\n"}.items():
        write(path / name, text)


def close_phase_uncommitted_work(p):
    """Phase 1 finished: some work committed, some modified, renamed, deleted or never added."""
    base_repo(p, CONTRACT_FULL)
    statuses = ["done", "progress", "todo", "todo"]
    write(p / RD / "README.md", readme(statuses, "Phase 1: Tokenizer", "—", "Phase 1: Tokenizer", "1.1.0"))
    for n in range(4):
        s = statuses[n]
        write(p / RD / f"phase-{n}-{PHASES[n][0]}.md",
              phase_file(n, s, "2026-09-01" if s != "todo" else "{{START_DATE}}", "2026-09-05" if s == "done" else "{{COMPLETION_DATE}}"))
    write(p / RD / "phase-0-framing-report.md", report_file(0, "0000000", closed=True))
    git(p, "add", "-A")
    git(p, "commit", "-q", "-m", "Open phase 1")
    start = git(p, "rev-parse", "--short", "HEAD")
    write(p / RD / "phase-1-tokenizer-report.md", report_file(1, start, closed=False))
    write(p / "src/tokenizer.py", "import unicodedata\n\ndef tokenize(s):\n    return unicodedata.normalize('NFC', s).split()\n")
    write(p / "src/indexer.py", "def build(docs):\n    return {}\n")
    write(p / "tests/test_tokenizer.py", "from tokenizer import tokenize\n\ndef test_accented():\n    assert tokenize('café crème') == ['café', 'crème']\n")
    git(p, "add", "-A")
    git(p, "commit", "-q", "-m", "Rewrite tokenizer, add its tests, start indexer")
    write(p / "src/search.py", "from tokenizer import tokenize\n\ndef search(q):\n    return tokenize(q)\n")
    git(p, "mv", "src/util.py", "src/text_utils.py")
    (p / "src/legacy_index.py").unlink()
    write(p / "src/batch.py", "BATCH_SIZE = 500\n")


def close_whole_roadmap(p):
    """Every phase closed, stale Blocked By and Next Milestone left in the README."""
    base_repo(p, CONTRACT_FULL)
    write(p / RD / "README.md", readme(["done"] * 4, "Phase 3: Results Page", "Pending design sign-off", "Phase 3: Results Page", "1.4.0"))
    for n in range(4):
        write(p / RD / f"phase-{n}-{PHASES[n][0]}.md", phase_file(n, "done", f"2026-09-0{n + 1}", f"2026-09-0{n + 2}"))
        write(p / RD / f"phase-{n}-{PHASES[n][0]}-report.md", report_file(n, "0000000", closed=True))
    git(p, "add", "-A")
    git(p, "commit", "-q", "-m", "Close phase 3")


def create_with_incomplete_contract(p):
    """A contract without Versioning, and no roadmap yet."""
    base_repo(p, CONTRACT_NO_VERSIONING)
    (p / "docs/roadmap").mkdir(parents=True)
    git(p, "add", "-A")
    git(p, "commit", "-q", "-m", "Initial app")


BUILDERS = {"close-phase-uncommitted-work": close_phase_uncommitted_work,
            "close-whole-roadmap": close_whole_roadmap,
            "create-with-incomplete-contract": create_with_incomplete_contract}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    workspace = Path(sys.argv[1]).resolve()
    evals = json.load(open(HERE / "evals.json", encoding="utf-8"))["evals"]
    for e in evals:
        fixture = workspace / "fixtures" / e["name"]
        BUILDERS[e["name"]](fixture)
        run_root = workspace / "iteration-1" / f"eval-{e['name']}"
        for version in ("new_skill", "old_skill"):
            outputs = run_root / version / "run-1" / "outputs"
            if outputs.exists():
                shutil.rmtree(outputs)
            outputs.mkdir(parents=True)
            shutil.copytree(fixture, outputs / "repo", symlinks=True)
        json.dump({"eval_id": e["id"], "eval_name": e["name"], "prompt": e["prompt"], "assertions": e["assertions"]},
                  open(run_root / "eval_metadata.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"{len(evals)} scenario(s) ready under {workspace / 'iteration-1'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
