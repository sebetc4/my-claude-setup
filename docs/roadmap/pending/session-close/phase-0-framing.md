# Phase 0: Framing

---

## Status

**Current Status:** 🟡 In Progress (60% — 3/5)
**Started:** 2026-10-13
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, before any code, what `close-session` does at each kind of session end, from the
requests the user typed and what the agent did after each: where its records go, the
resume note and its folder, the line the next session starts with, and what it leaves to
the roadmap skill and to roadmap `roadmap-execution`.

---

## Overview

### Why This Phase Matters
The requests vary in their words and in what followed them: a report entry, a memory
file, a note in a folder made up for it, a commit or none. A skill written from one
session's habit would serve one kind of session end.

### What It Enables
Phase 1 builds a design the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Tasks

### Inputs
- [x] Save the requests to close a session from every project's transcripts into `study/session-close/close-requests.md`, each with its date, its repository, its words, the context's size when it was typed, and what the agent then wrote, committed and answered, before the oldest transcripts pass Claude Code's 30 days
  Proof: check — the search's pattern and date at the file's head, and the 67 messages that `consign|clôtur|fin de session|nouvelle session|session fresh|prochaine session` found on 2026-10-13 found again
- [x] Sort the requests into kinds of session end — a roadmap step finished, a step stopped midway, a phase finished, outside any roadmap, a study — with, for each, where the records went, whether a commit followed, what the next session read first, and the context's size at the request
  Proof: review — the table, each row tied to a request of the file, approved by the user
- [x] List what this setup already asks at a session's end and at the next start: the roadmap skill's `references/report.md`, `session_resume.py`, the "Where the next session starts" blocks of roadmap `token-usage`'s reports, the Stop hook of the review domain, roadmap `roadmap-execution`'s Phase 0 hand-over task and `[git]` table, the agent's memory
  Proof: review — the list, each item tied to a file and a line, approved by the user

### Design
- [ ] Write the design and get the user's approval: the skill's name, checked against `docs/claude-code-builtins.md`; its procedure for each kind of session end; what goes to the phase report, to a resume note, to `docs/decisions/` and to the agent's memory; the `[session]` table of `.agent-conventions.toml` — the notes' folder — and what the skill proposes when the table is missing; the resume note's format and when the next session counts it taken up; the SessionStart line; the commit, until the `[git]` table's `commit` key exists; what the close reads and writes, at a cost that leaves it room under the plan's usage limit, and in what order — the records first, the commit last — so that a session cut by the limit loses the least; its trigger, and the argument naming where the next session starts
  Proof: review — the design, each part tied to the sorted requests, approved by the user before any code
- [ ] Write the decision record under `docs/decisions/` — with the decision that no hook watches the plan's usage or the context, session management staying the user's judgment, and when to revisit it —, and carry into roadmap `roadmap-execution`'s Phase 0 what it settles for that roadmap's hand-over task, with a changelog entry there
  Proof: review — the record and the change to `roadmap-execution`, approved by the user with its date

---

## Technical Details

### Files to Modify
```
study/session-close/close-requests.md            new, ignored by git
docs/decisions/<date>-session-close.md           new
docs/roadmap/pending/roadmap-execution/          its Phase 0 and README changelog
```

### Dependencies
None to start.

### Constraints
No domain changes in this phase. The transcripts are read in place under
`~/.claude/projects/`; the user's words are copied only into `study/`, which git ignores,
since most requests come from other repositories. Claude Code deletes a transcript after
30 days: the oldest request found on 2026-10-13 dates from 2026-09-10. A request's
context size is the last call's before it, read with roadmap `token-usage`'s reader,
`shared/usage/`.

---

## Acceptance Criteria

- [ ] The requests are saved before their transcripts are deleted
- [ ] The design is approved by the user
- [ ] The decision record is committed
