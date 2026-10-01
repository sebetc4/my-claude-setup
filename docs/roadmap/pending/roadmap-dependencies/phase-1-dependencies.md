# Phase 1: Dependencies

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/8)
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

Keep `phase-1-dependencies-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Make the roadmap skill read, enforce and clear dependencies between roadmaps, per the
Phase 0 design.

---

## Overview

### Why This Phase Matters
Today `Blocked By` is free text that nothing checks: a phase can open while its roadmap
waits, and a closing roadmap does not tell the roadmaps waiting for it.

### What It Enables
Phase 2's overview reads the same field, and the work-in-progress rule holds without
the user policing it.

### Out of Scope
The overview script and the session hook: Phase 2.

---

## Tasks

### Checks
- [ ] Write the failing tests of the dependency checks of `progress.py --check`: a `Blocked By` that names no roadmap under `root`, and a 🟡 phase in a roadmap that waits for one not yet completed
- [ ] Implement those checks

### Skill
- [ ] Make `references/create.md` list the roadmaps in `pending/` and `on-progress/` before the phase breakdown, and ask whether the new roadmap waits for one of them or holds one back
- [ ] Make `references/open-phase.md` refuse to open a phase that waits, itself or through its roadmap, for a roadmap not yet in `completed/`, and name that roadmap
- [ ] Apply the work-in-progress rule in `references/create.md` and `references/open-phase.md`
- [ ] Make `references/close-roadmap.md` find the roadmaps that wait for the one it closes, clear their `Blocked By` and their ⏸️, and tell the user which can resume
- [ ] Make a phase that a closure unblocked start by reading the blocking roadmap's `summary.md`, in `references/open-phase.md`
- [ ] Rewrite the Statuses invariant of `SKILL.md` for the ⏸️ the skill now sets, and move a roadmap to `on-progress/` when its first phase opens, per Phase 0

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/skills/roadmap/references/create.md
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/close-phase.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
domains/roadmap/skills/roadmap/scripts/progress.py
domains/roadmap/skills/roadmap/evals/test_scripts.py
```

### Dependencies
Phase 0's design.

### Constraints
Python standard library only; failing tests first.

---

## Acceptance Criteria

- [ ] `progress.py --check` flags a `Blocked By` that names no roadmap, and a phase open while its roadmap waits
- [ ] A phase that waits cannot be opened, and closing the roadmap it waits for unblocks it
