# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle the dependency model and the rules this roadmap implements, on the decisions of
roadmap `superpowers-study`, before any change to the roadmap skill.

---

## Overview

### Why This Phase Matters
The model changes an invariant — who sets ⏸️ — the moment a roadmap leaves `pending/`,
and what a closure does with work it did not make. Deciding them in writing keeps
Phases 1 to 3 from arguing each point again, and the study may reshape how a phase is
executed, which this roadmap builds on.

### What It Enables
Phase 1 implements a settled model, and Phase 3 applies a settled closure rule.

### Out of Scope
Changes to the skill: they start in Phase 1.

---

## Tasks

### Inputs
- [ ] Read the decision record of roadmap `superpowers-study`, and list what its decisions on plan execution, on the proof each task declares and on git conventions change in this roadmap's phases

### Design
- [ ] Write the design of the dependency model — `Blocked By` naming a roadmap by its folder name, at roadmap or phase level; a wait on a whole roadmap only; what stays free text, for a blocker that is not a roadmap; the work-in-progress rule; ⏸️ set and cleared by the skill — and get the user's approval
- [ ] Settle what a phase closure does with the user's uncommitted work, from the two eval runs of skill-tooling's Phase 1 that diverged on it
- [ ] Settle the move to `on-progress/` when a roadmap's first phase opens, and what it changes in `open-phase.md`, `close-phase.md` and the session hook

### Record
- [ ] Write the decision record under `docs/decisions/`

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-roadmap-dependencies.md    new
```

### Dependencies
Roadmap `superpowers-study`, completed.

### Constraints
No change to the skill in this phase.

---

## Acceptance Criteria

- [ ] The dependency model, the work-in-progress rule, the ⏸️ rule, the opening move and the closure rule for uncommitted work are settled and approved by the user
- [ ] The decision record is committed
