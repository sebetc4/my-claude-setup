# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/6)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, on the decisions of roadmap `superpowers-study`, the design of what this roadmap
adds to the roadmap skill, before any change to it.

---

## Overview

### Why This Phase Matters
The study decided what each kept capability does, not the text that does it: the steps
of `execute-phase`, the shape of the `Proof:` line, the agents' inputs and answers.
Settling them first keeps Phases 1 to 3 from arguing each point again.

### What It Enables
Phases 1 to 3 build designs the user approved.

### Out of Scope
Changes to the skill: they start in Phase 1.

---

## Tasks

### Inputs
- [ ] Read the decision record `docs/decisions/2026-10-01-superpowers-study.md` and the summary of roadmap `roadmap-dependencies`, and list what each row the record gives the roadmap skill, the proof reference, the `[git]` table and the two agents asks of each file

### Design
- [ ] Write the design of `execute-phase` — its steps, the four stops and the fourth fix, the proof run and recorded before a task is ticked, the review's findings ruled in one fix pass, the delegation a phase writes down, the commit per the `[git]` table — and get the user's approval
- [ ] Write the design of the phase template's `## Design` section and `Proof:` line, of the proof reference, and of what `create.md`, `open-phase.md` and `report.md` gain, and get the user's approval
- [ ] Write the design of `phase-reviewer`, `task-implementer` and the `review-package` script — inputs, tool lists, model tier, answer — and get the user's approval
- [ ] Settle with the user when `execute-phase` hands over to a new session — at the end of a phase, at the end of a task, or at the first task ticked past a context threshold declared in `[roadmap]` and overridable by a roadmap — what the new session reads to resume, and whether `progress_guard.py` can read the context's size from the transcript when a task is ticked, on the figures of `docs/decisions/2026-10-06-token-costs.md`
- [ ] Choose with the user the eval scenarios that prove the operation in Phase 4

### Record
- [ ] Write the decision record under `docs/decisions/`

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-roadmap-execution.md    new
```

### Dependencies
Roadmap `roadmap-dependencies`, completed.

### Constraints
No change to the skill in this phase. The designs carry the record's verdicts; a
verdict changed here is recorded with its reason.

The opening decision that `execute-phase` runs one phase in the main conversation was
taken before any cost was measured. Phase 3 of roadmap `skill-tooling` then ran its main
thread in five sessions, four of which reached a context of 407,000 to 631,000 tokens,
never compacted. A
session that started on a phase took 9 to 17 calls and $0.57 to $1.16 to read the skill,
the phase file and the report, against a read of about (context − 100,000) × $0.20 per
million at each call of a continued session. A new session every 60 calls, about one
task, would have saved $12.42 net of the phase's $88.28 of main thread, 14%
(`docs/decisions/2026-10-06-token-costs.md`). The report a resumed session reads in full
grows through the phase: Phase 3's ended at about 30,000 tokens. The 60 calls are a
mean over the phase's 12 tasks, not a measure of each one: a fixed rule of one session
per task would pay a full reorientation even for a task of a few calls.

---

## Acceptance Criteria

- [ ] The designs of the operation, the template, the proof reference and the two agents are approved by the user
- [ ] The decision record is committed
