#!/usr/bin/env python3
"""Build the repository a case of the close-session skill's evals starts in.

Usage: fixtures.py <case> <folder>

The workspace.py of the authoring-skills skill runs it once per case when it prepares an
iteration. Each case is a small service, stock-sync, in a git repository whose
.agent-conventions.toml declares a roadmap root and a [session] table, with roadmap
resilient-sync open at its Phase 1. The case's prompt gives the session to close; the
repository is in the state that session left. CLAUDE.md declares the agent's memory as the
tracked folder .agent-memory/, so that a run writing to it shows in its changes.json, the
runs' own memory being off.

  step-stopped-midway            Phase 1's task 2 half done: the backoff written in
                                 src/retry.py and its tests in tests/test_backoff.py,
                                 neither committed
  phase-every-task-ticked        Phase 1's tasks 1 to 3 done and committed; task 4's
                                 docs/retry-policy.md and its tick uncommitted, beside
                                 config/local.toml, modified before the session
  outside-roadmap-note-taken-up  a clean tree with two resume notes under notes/sessions/,
                                 2026-10-10-export-formats.md not taken up yet
"""

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

RD = "docs/roadmap/on-progress/resilient-sync"
# A fixed date keeps the commits' hashes, and the start commit the report names, the same
# from one build to the next, so that workspace.py's fixture digest holds across iterations
GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com",
           "GIT_AUTHOR_DATE": "2026-10-10T18:00:00+02:00", "GIT_COMMITTER_DATE": "2026-10-10T18:00:00+02:00"}

CLAUDE_MD = """# Stock Sync

A small service that pushes the shop's stock levels to the warehouse's API.

Run the tests with `PYTHONPATH=src python3 -m unittest discover -s tests`.

## Agent Memory

`.agent-memory/` is the agent's memory across sessions, loaded at the start of each one:
one fact per file, indexed by one line in `.agent-memory/MEMORY.md`. Save there what the
user tells you about how to work — corrections, preferences, rules — so that later
sessions follow it.
"""
CONVENTIONS = """language   = "english"
versioning = "git"

[roadmap]
root = "docs/roadmap"

[session]
notes = "notes/sessions"
"""
MEMORY_INDEX = "- [Reply in French](reply-in-french.md) — every reply in French; files stay in English\n"
MEMORY_FACT = """---
name: reply-in-french
description: every reply in French; files stay in English
---

The user writes in French: reply in French, and keep code, commits and documents in English.
"""
SOURCES = {
    "src/sync.py": "from retry import RetryQueue\nfrom warehouse import push\n\n\ndef sync(levels, queue: RetryQueue):\n"
                   "    for sku, count in levels.items():\n        if not push(sku, count):\n            queue.add(sku, count)\n",
    "src/warehouse.py": "import csv\n\n\ndef push(sku, count):\n    return True\n\n\ndef import_export(path):\n"
                        "    with open(path, newline=\"\") as f:\n        return list(csv.DictReader(f))\n",
    "src/log.py": "import os\nimport sys\n\n\ndef log(line):\n    print(line, file=sys.stderr)\n"
                  "    if os.environ.get(\"SYNC_DEBUG\") == \"1\":\n        print(line, file=sys.stderr)\n",
    "tests/test_sync.py": "import unittest\n\nfrom retry import RetryQueue\nfrom sync import sync\n\n\nclass Sync(unittest.TestCase):\n"
                          "    def test_nothing_queued_when_pushes_succeed(self):\n        q = RetryQueue(\":memory:\")\n"
                          "        sync({\"A1\": 3}, q)\n        self.assertEqual(q.db.execute(\"select count(*) from queue\").fetchone()[0], 0)\n",
    "config/local.toml": "warehouse_url = \"https://warehouse.example.com/api\"\n",
}
RETRY = ("import sqlite3\n\n\nclass RetryQueue:\n    \"\"\"Failed pushes, kept in SQLite so that a restart loses none.\"\"\"\n\n"
         "    def __init__(self, path):\n        self.db = sqlite3.connect(path)\n"
         "        self.db.execute(\"create table if not exists queue (sku text, count integer, failures integer default 0)\")\n\n"
         "    def add(self, sku, count):\n        self.db.execute(\"insert into queue (sku, count) values (?, ?)\", (sku, count))\n")
BACKOFF = ("\n\ndef backoff(failures):\n    \"\"\"Seconds before the next retry: 1 s doubled at each failure, capped at 5 minutes.\"\"\"\n"
           "    return min(2 ** failures, 300)\n")
JITTER = "\n\ndef jittered(failures, draw):\n    return backoff(failures) * (0.5 + draw / 2)\n"
ALERT = "\n\ndef must_alert(failures):\n    return failures >= 5\n"
REPLAY = ("\n\ndef replay(queue, push=push, alert=print, draw=lambda: 0.5, wait=lambda seconds: None):\n"
          "    \"\"\"Push each queued item again after its jittered delay; alert from its fifth failure.\"\"\"\n"
          "    for rowid, sku, count, failures in queue.db.execute(\"select rowid, sku, count, failures from queue\").fetchall():\n"
          "        wait(jittered(failures, draw()))\n        if push(sku, count):\n"
          "            queue.db.execute(\"delete from queue where rowid = ?\", (rowid,))\n        else:\n"
          "            queue.db.execute(\"update queue set failures = failures + 1 where rowid = ?\", (rowid,))\n"
          "            if must_alert(failures + 1):\n                alert(sku)\n")
TEST_REPLAY = ("\n\nclass Replay(unittest.TestCase):\n    def test_a_push_refused_ten_times_still_reaches_the_warehouse(self):\n"
               "        from sync import replay\n        q = RetryQueue(\":memory:\")\n        q.add(\"A1\", 3)\n"
               "        answers, alerts = [False] * 10 + [True], []\n        for _ in range(11):\n"
               "            replay(q, push=lambda sku, count: answers.pop(0), alert=alerts.append)\n"
               "        self.assertEqual(q.db.execute(\"select count(*) from queue\").fetchone()[0], 0)\n"
               "        self.assertEqual(alerts, [\"A1\"] * 6)\n")
TEST_RETRY = ("import unittest\n\nfrom retry import RetryQueue\n\n\nclass Queue(unittest.TestCase):\n"
              "    def test_a_failed_push_is_kept(self):\n        q = RetryQueue(\":memory:\")\n        q.add(\"A1\", 3)\n"
              "        self.assertEqual(q.db.execute(\"select count(*) from queue\").fetchone()[0], 1)\n")
TEST_BACKOFF = ("import unittest\n\nimport retry\n\n\nclass Backoff(unittest.TestCase):\n"
                "    def test_first_delay_is_one_second(self):\n        self.assertEqual(retry.backoff(0), 1)\n\n"
                "    def test_delay_doubles(self):\n        self.assertEqual(retry.backoff(3), 8)\n\n"
                "    def test_delay_is_capped_at_five_minutes(self):\n        self.assertEqual(retry.backoff(20), 300)\n\n"
                "    def test_jitter_stays_within_half_the_delay(self):\n        self.assertEqual(retry.jittered(3, 0), 4)\n\n"
                "    def test_jitter_reaches_the_full_delay(self):\n        self.assertEqual(retry.jittered(3, 1), 8)\n")
RETRY_POLICY = """# Retry Policy

A push the warehouse refuses goes to the retry queue, kept in SQLite (`src/retry.py`).

- **Delay:** 1 s before the first retry, doubled at each failure, capped at 5 minutes.
- **Jitter:** each delay is drawn between half of it and all of it, so that the queue's
  retries do not hit the warehouse together.
- **Alert:** after five failed retries of the same item, the service raises an alert.
"""
TASKS = ["Persist failed pushes in a retry queue", "Retry with exponential backoff and jitter",
         "Alert after five failed retries", "Document the retry policy"]
README = """# Roadmap: resilient-sync

---

## Overall Progress

```
Phase 0  Framing                    🟢 ████████████████████ 100%  (3/3)
Phase 1  Retry Queue                🟡 █░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 2  Monitoring                 🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/3)
TOTAL                                  ██████░░░░░░░░░░░░░░  30%  (3/10)
```

**Current Phase:** Phase 1 — Retry Queue
**Blocked By:** —
**Next Milestone:** Phase 2 — Monitoring

---

## Why This Roadmap Exists

A push the warehouse refuses is lost today: the stock levels drift until someone notices.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 3 | 🟢 Done |
| 1 | [Retry Queue](phase-1-retry-queue.md) | 4 | 🟡 In Progress |
| 2 | [Monitoring](phase-2-monitoring.md) | 3 | 🔴 Not Started |

---

## Metadata

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/on-progress/resilient-sync/`
**Version:** 1.1.0
**Created:** 2026-10-06
**Last Updated:** 2026-10-07

---

## Changelog

### 1.1.0 (2026-10-07)

- Phase 0 Framing closed.

### 1.0.0 (2026-10-06)

- Roadmap created with three phases.
"""
PHASE_0 = """# Phase 0: Framing

---

## Status

**Current Status:** 🟢 Done (100% — 3/3)
**Started:** 2026-10-06
**Completed:** 2026-10-07
**Blocked By:** —

---

## Objective

Decide where failed pushes wait and how they are retried.

---

## Tasks

- [x] List the pushes the warehouse refused last month
- [x] Choose where the retry queue lives
- [x] Set the retry policy's figures

---

## Acceptance Criteria

- [x] The retry policy is approved
"""
REPORT_0 = """# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** 0000000

---

## Work Log

### 2026-10-06

Listed the 212 pushes the warehouse refused in September: 190 came back on a retry within
ten minutes.

---

## Decisions

- **Failed pushes wait in SQLite**, beside the shop's database.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/resilient-sync/`

---

## Problems And Deviations

None.

---

## Changes To Later Phases

None.

---

## Assessment

The policy is set; Phase 1 builds the queue.
"""
PHASE_2 = """# Phase 2: Monitoring

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/3)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Tasks

- [ ] Count the queue's items per hour
- [ ] Graph the count on the team's dashboard
- [ ] Page the on-call after an hour above 100 items
"""
ENTRIES = {
    1: ("2026-10-08", "Opened the phase. Task 1: failed pushes go to a queue kept in SQLite, `src/retry.py`,\n"
                      "so that a restart loses none; `tests/test_retry.py` covers it. Task 1 done.",
        "1. Task 2, the exponential backoff and its jitter in `src/retry.py`."),
    2: ("2026-10-09", "Task 2: `backoff()` and `jittered()` in `src/retry.py`, five tests in\n"
                      "`tests/test_backoff.py`. Task 2 done.",
        "1. Task 3, the alert after five failed retries."),
    3: ("2026-10-10", "Task 3: `must_alert()` in `src/retry.py`, called by `replay()` in `src/sync.py`, which\n"
                      "pushes each queued item again after its jittered delay; `tests/test_sync.py` drives it\n"
                      "through ten refusals. Task 3 done.",
        "1. Task 4, the retry policy documented in `docs/retry-policy.md`, each figure taken from\n"
        "   `src/retry.py`."),
}
EXPORT_NOTE = """# Export Formats

**Date:** 2026-10-10
**Taken up:** —

## Where The Next Session Starts

1. Benchmark Parquet writes on `data/orders-2025.csv` against the current CSV export: the
   file's size and the time to write it.
2. Then decide between the two formats for the nightly export to the warehouse.

## Done

- Read how the nightly export is written: one CSV of every order, 41 MB for 2025.

## Decided

- Only the export's format is in question; its schedule stays.

## Observed

- The export takes 4 minutes, most of it writing the file.

## Questions For The User

- None.

## Files

- None written.
"""
WAREHOUSE_NOTE = """# Warehouse API

**Date:** 2026-10-02
**Taken up:** 2026-10-05, finished

## Where The Next Session Starts

1. Check that the warehouse's API accepts a batch of 500 stock levels.

## Done

- Read the API's documentation.

## Decided

- Pushes go one item at a time until a batch is tested.

## Observed

- The API answers 429 above 20 calls a second.

## Questions For The User

- None.

## Files

- None written.
"""


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True, env=GIT_ENV).stdout.strip()


def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(text)


def phase_1(done):
    ticks = "\n".join(f"- [{'x' if n < done else ' '}] {task}" for n, task in enumerate(TASKS))
    return f"""# Phase 1: Retry Queue

---

## Status

**Current Status:** 🟡 In Progress ({round(done / 4 * 100)}% — {done}/4)
**Started:** 2026-10-08
**Completed:** {{{{COMPLETION_DATE}}}}
**Blocked By:** —

---

## While Working

Keep `phase-1-retry-queue-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Keep every push the warehouse refuses, and retry it until it goes through.

---

## Tasks

{ticks}

---

## Acceptance Criteria

- [ ] A push refused ten times in a row still reaches the warehouse
"""


def report_1(start, entries):
    log = "\n\n".join(f"### {ENTRIES[n][0]}\n\n{ENTRIES[n][1]}\n\n**Where the next session starts:**\n{ENTRIES[n][2]}"
                      for n in range(1, entries + 1))
    return f"""# Phase 1 Report: Retry Queue

**Phase:** [phase-1-retry-queue.md](phase-1-retry-queue.md)
**Start Commit:** {start}

---

## Work Log

{log}

---

## Decisions

- **The retry queue lives in SQLite**, beside the shop's database: a restart loses no failed
  push. Task 3 reads its counts from it.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
"""


def base(path):
    """The service with roadmap resilient-sync's Phase 1 opened, committed; its start commit."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    git(path, "init", "-q", "-b", "main")
    for name, text in {"CLAUDE.md": CLAUDE_MD, ".agent-conventions.toml": CONVENTIONS, ".gitignore": "__pycache__/\ndata/\n",
                       ".agent-memory/MEMORY.md": MEMORY_INDEX, ".agent-memory/reply-in-french.md": MEMORY_FACT,
                       f"{RD}/README.md": README, f"{RD}/phase-0-framing.md": PHASE_0,
                       f"{RD}/phase-0-framing-report.md": REPORT_0, f"{RD}/phase-1-retry-queue.md": phase_1(0),
                       f"{RD}/phase-2-monitoring.md": PHASE_2, **SOURCES}.items():
        write(path / name, text)
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "feat(roadmap): open resilient-sync phase 1")
    return git(path, "rev-parse", "--short", "HEAD")


def task(path, start, n, files, message):
    for name, text in files.items():
        write(path / name, text)
    write(path / RD / "phase-1-retry-queue.md", phase_1(n))
    write(path / RD / "phase-1-retry-queue-report.md", report_1(start, n))
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", message)


def task_1(path):
    start = base(path)
    task(path, start, 1, {"src/retry.py": RETRY, "tests/test_retry.py": TEST_RETRY},
         "feat(retry): keep failed pushes in a SQLite queue")
    return start


def step_stopped_midway(path):
    """Task 2 half done: the backoff written, its jitter not, nothing committed."""
    task_1(path)
    write(path / "src/retry.py", RETRY + BACKOFF)
    write(path / "tests/test_backoff.py", TEST_BACKOFF)


def phase_every_task_ticked(path):
    """Tasks 1 to 3 committed; task 4's document and tick left for the close."""
    start = task_1(path)
    task(path, start, 2, {"src/retry.py": RETRY + BACKOFF + JITTER, "tests/test_backoff.py": TEST_BACKOFF},
         "feat(retry): back off exponentially, with jitter")
    task(path, start, 3, {"src/retry.py": RETRY + BACKOFF + JITTER + ALERT,
                          "src/sync.py": SOURCES["src/sync.py"].replace("from retry import RetryQueue",
                                                                        "from retry import RetryQueue, jittered, must_alert") + REPLAY,
                          "tests/test_sync.py": SOURCES["tests/test_sync.py"] + TEST_REPLAY},
         "feat(retry): replay the queue, alert after five failed retries")
    write(path / "docs/retry-policy.md", RETRY_POLICY)
    write(path / RD / "phase-1-retry-queue.md", phase_1(4))
    write(path / "config/local.toml", SOURCES["config/local.toml"] + "warehouse_token = \"dev-only\"\n")


def outside_roadmap_note_taken_up(path):
    """A clean tree, task 1 of the roadmap done, and an open resume note on another subject."""
    task_1(path)
    write(path / "notes/sessions/2026-10-02-warehouse-api.md", WAREHOUSE_NOTE)
    write(path / "notes/sessions/2026-10-10-export-formats.md", EXPORT_NOTE)
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "docs(notes): record the export formats study")


BUILDERS = {"step-stopped-midway": step_stopped_midway,
            "phase-every-task-ticked": phase_every_task_ticked,
            "outside-roadmap-note-taken-up": outside_roadmap_note_taken_up}


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    name, folder = argv
    if name not in BUILDERS:
        print(f"no case named `{name}`: {', '.join(BUILDERS)}", file=sys.stderr)
        return 1
    BUILDERS[name](Path(folder).resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
