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

---

## Acceptance Criteria

- [ ] The designs of the operation, the template, the proof reference and the two agents are approved by the user
- [ ] The decision record is committed
