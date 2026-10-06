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

Put the figures where the reviews and the user read them:
- each review's measured block;
- `make reviews`;
- a command that reports a session, a phase or a roadmap;
- a store that outlives the transcripts.

Fix the domain's four open defects along the way.

---

## Overview

### Why This Phase Matters
A review judges how a tool worked: with its cost beside it, the judgment weighs what the
tool costs against what it brings.

### What It Enables
Decisions on effort, sessions and eval runs that rest on measures taken as the work
happens, rather than on a one-off analysis.

### Out of Scope
Writing a phase's cost into its report at closure: the roadmap skill's, proposed to
roadmap `roadmap-execution` once the command exists.

---

## Tasks

### Reviews
- [ ] Test and implement the measured block the design chose: the slice's cost per model, its subagents, its effort and its cache rebuilds, beside the token counts it carries today
  Proof: test — `measure.py` on a fixture session with a subagent and a rebuild prints the block, red before the change
- [ ] Test and implement `make reviews` reporting each tool's median cost in dollars beside its current measures
  Proof: test — `tools/reviews.py` on fixture reviews with known costs prints each tool's median in dollars, red before the change

### Usage Command
- [ ] Test and implement the command that reports the cost of a session, a phase or a roadmap: per model, main thread and subagents, effort and rebuilds, estimates marked
  Proof: test — a fixture repository and its transcripts, the session, phase and roadmap totals computed by hand, red before the code
- [ ] Test and implement keeping the measures beyond the transcripts' 30 days, as the design chose
  Proof: test — a session's measures kept, its transcript removed, the command still reporting the session, red before the code

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
domains/review/hooks/review.py                         if the design keeps measures from the Stop hook
tools/reviews.py
tools/<usage command>.py                               new, as the design names it
Makefile
domains/review/tests/test_*.py
tests/test_reviews.py
docs/claude-code-coupling.md
```

### Dependencies
Phase 1: the extended reader.

### Constraints
Standard library only; test first. The Stop hook runs at every stop of every session:
whatever it gains is timed on a long transcript before it ships. The reviews already
written keep their measured block as recorded; `make reviews` reads both shapes.

---

## Acceptance Criteria

- [ ] A review written in a session with subagents carries its cost in dollars per model
- [ ] The command reports the cost of a closed phase of this repository
- [ ] Each of the four defects has a passing test
