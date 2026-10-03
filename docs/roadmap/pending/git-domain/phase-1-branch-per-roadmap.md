# Phase 1: Branch Per Roadmap

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
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

Keep `phase-1-branch-per-roadmap-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Build `branch = "roadmap"`: a branch per roadmap, made when its first phase opens and
integrated, or kept, when it closes.

---

## Overview

### Why This Phase Matters
It is the `[git]` table's one value roadmap `roadmap-execution` refuses until this
phase builds it.

### What It Enables
Two roadmaps advanced at once, each in a worktree the harness makes, or a roadmap
reviewed before its merge.

### Out of Scope
Worktrees: the harness makes and removes them; Phase 2 covers the rest.

---

## Tasks

### Conventions
- [ ] Make `conventions.py` accept `branch = "roadmap"` — failing tests first — and refresh the copies with `make shared`

### Rituals
- [ ] Make `open-phase.md` create `roadmap/<folder-name>` from the default branch when a roadmap's first phase opens, and record its base
- [ ] Make `close-roadmap.md` propose, after its own commit, the base fast-forwarded and the branch deleted, or the branch kept; check the user's uncommitted files before any switch of branch; send a refused fast-forward to the user

### Evals
- [ ] Add the scenarios of a roadmap closed on its branch and of a refused fast-forward, run them against the previous release, and compare

---

## Technical Details

### Files to Modify
```
shared/conventions/conventions.py
shared/conventions/tests/test_conventions.py
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
domains/roadmap/skills/roadmap/evals/evals.json
```

### Dependencies
Phase 0's designs.

### Constraints
Fast-forward only. A push, of a branch or a tag, waits for the user's request.

---

## Acceptance Criteria

- [ ] A roadmap under `branch = "roadmap"` opens on its branch and closes with the integration the user confirms
- [ ] `make check` passes
