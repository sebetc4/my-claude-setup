# Phase 1: Proof And Template

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-proof-and-template-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Give each task of a phase its declared proof, and each phase its design: the proof
reference, the template's `## Design` and `Proof:` line, and the rules that write them.

---

## Overview

### Why This Phase Matters
`execute-phase` runs what a task declares: without the declaration it has nothing to run
before ticking a task.

### What It Enables
Phase 3's operation reads phases that say what proves each task.

### Out of Scope
The operation itself: Phase 3.

---

## Tasks

### Proof Reference
- [ ] Write `shared/proof/proof.md` — the five kinds, each with its object and its rules, from Decisions Of Phase 2 and the proof rows of the record — with superpowers' MIT notice, and copy it into the roadmap skill with `tools/shared.py`

### Template
- [ ] Add the `## Design` section and the indented `Proof:` line to `assets/templates/phase.md`
- [ ] Check with failing tests that `progress.py` and the progress guard count a task and its `Proof:` line as one task, and fix them if they do not

### Rituals
- [ ] Write into `references/create.md` and `references/open-phase.md` the rules the record keeps: one roadmap per effort, right-sized tasks without placeholders, each task's proof proposed and approved with the phase, the self-review before the hand-over, the `## Design` approved when the phase opens
- [ ] Write into `references/report.md` the rulings with their cost if wrong, which replace the ledger

---

## Technical Details

### Files to Modify
```
shared/proof/proof.md                                 new
domains/roadmap/skills/roadmap/references/proof.md    copy
domains/roadmap/skills/roadmap/assets/templates/phase.md
domains/roadmap/skills/roadmap/references/create.md
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/report.md
domains/roadmap/skills/roadmap/scripts/progress.py
domains/roadmap/skills/roadmap/evals/test_scripts.py
```

### Dependencies
Phase 0's designs.

### Constraints
Python standard library only; scripts test-first. The proof reference is edited in
`shared/`, never in a copy.

---

## Acceptance Criteria

- [ ] Every kind of proof is defined once, in `shared/proof/`
- [ ] A phase written from the template carries a `## Design` section and room for a `Proof:` line under each task
- [ ] `make check` passes
