# Phase 2: Reviews And Reports

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/8)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-usage-reader.md` and `phase-1-usage-reader-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-reviews-and-reports-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Put the figures where they lead to a conclusion:
- each tool review's measured block, the tool's cost beside what it brought;
- `make reviews`, each tool's cost and the tools it flags;
- a skill of the review domain, run by hand, that reviews several sessions, a phase, a
  roadmap or a stretch of work, and has the agent conclude on what served and what did
  harm, and records its figures and conclusions so that a longer window reads them.

Fix the domain's four open defects along the way.

---

## Overview

### Why This Phase Matters
A review judges how a tool worked: with its cost beside it, the judgment weighs what the
tool costs against what it brings. The review of several sessions does with a tool what
the three counts by hand did, ending in what to change.

### What It Enables
Decisions on effort, sessions and eval runs that rest on measures taken as the work
happens, rather than on a one-off analysis.

### Out of Scope
A phase closure that starts the review of several sessions or writes a phase's cost into
its report: the roadmap and review domains stay independent (the user, 2026-10-11).

---

## Tasks

### Reviews
- [ ] Test and implement the measured block the design chose: the slice's cost per model, its subagents, its effort and its cache rebuilds, beside the token counts it carries today, and the review's own turn as the design decided
  Proof: test — `measure.py` on a fixture session with a subagent and a rebuild prints the block, red before the change
- [ ] Test and implement `make reviews` reporting each tool's median cost in dollars beside its current measures, and flagging the tools the design names: one costing past its median, one costing while its reviews say it brought nothing
  Proof: test — `tools/reviews.py` on fixture reviews with known costs prints each tool's median in dollars and flags the two fixture tools built to be flagged, red before the change

### Review Of Several Sessions
- [ ] Test and implement the script of the review of several sessions: a window given as the design decided, per model, main thread, subagents and `claude -p` sessions, effort and rebuilds, estimates marked, what served where and when, what the design flags as having done harm, and what the agent must conclude on; the record it writes, read by a longer window in place of transcripts past 30 days, and its warning when a window starts before the oldest transcript kept
  Proof: test — a fixture repository and its transcripts, the window's totals computed by hand and each flagged pattern built into the fixture; a window made of recorded phases read from their records; a window older than the fixture's oldest transcript warned; red before the code
- [ ] Write the skill, run by hand, that runs the script and draws the conclusions, with `authoring-skills`
  Proof: eval — a case on a fixture window whose conclusions are known, its assertions passing, and `audit.py` clean on the skill

### Defects
- [ ] Count the run of `session_resume.py` in a session it opened
  Proof: test — a fixture session that opens with the hook's line: the measured block counts one run and its characters, red before the fix
- [ ] Count a skill's files read through a Bash `cat` or `sed` as through the Read tool
  Proof: test — a fixture session reading a reference with `cat`: `files_read` names it, red before the fix
- [ ] Replace the `make update` message of `measure.py` and `record.py` as the design settled
  Proof: test — a domain that does not know its repository: neither script tells the agent to run `make update`, red before the change
- [ ] Count each agent run's output tokens, estimated and marked as the reader does, beside its fresh and cached tokens
  Proof: test — a fixture subagent whose records keep the stream's first usage: its run carries an output estimate marked as such, red before the change

---

## Technical Details

### Files to Modify
```
domains/review/skills/tool-review/scripts/transcript.py
domains/review/skills/tool-review/scripts/measure.py
domains/review/skills/tool-review/scripts/record.py
domains/review/skills/tool-review/references/format.md
domains/review/hooks/review.py                         if the design changes the slices
domains/review/skills/<name>/                          new, the review of several sessions, as the design names it
domains/review/permissions.json
tools/reviews.py
domains/review/tests/test_*.py
tests/test_reviews.py
docs/claude-code-coupling.md
```

### Dependencies
Phase 1: the extended reader.

### Constraints
Standard library only; test first. The Stop hook runs at every stop of every session:
whatever it gains is timed on a long transcript before it ships. The reviews already
written keep their measured block as recorded; `make reviews` reads both shapes. The
review of several sessions is started by hand only. The transcripts stay at Claude
Code's 30 days (the user, 2026-10-11): a window is reviewed within that time, and a
longer one reads the records of the reviews it spans.

---

## Acceptance Criteria

- [ ] A review written in a session with subagents carries its cost in dollars per model
- [ ] The review of several sessions, run on a closed phase of this repository, gives its cost and its conclusions
- [ ] Each of the four defects has a passing test
