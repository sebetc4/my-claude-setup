# Phase 3: Git

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/3)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-proof.md` and `phase-2-proof-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-git-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Rule on `using-git-worktrees` and `finishing-a-development-branch`, and design the
`[git]` table of `.agent-conventions.toml` that the roadmap skill's commit steps read.

---

## Overview

### Why This Phase Matters
The roadmap skill commits "per the repository's convention", which nothing defines:
skill-tooling's Phase 1 closed in one commit of 36 files, the phase's work mixed with
its closure. The agent's view, given on 2026-10-01: a commit per task or coherent group
of tasks, then a closure commit holding the closure documents only, since the Start
Commit and Files Changed logic already works at any granularity; a branch per roadmap
only when roadmaps advance in parallel in the same area or a pull request is wanted,
which the work-in-progress rule makes rare; a worktree only for agent sessions working
in parallel.

### What It Enables
The roadmap skill and a future git domain read one convention.

### Out of Scope
The git domain itself: a follow-up roadmap.

---

## Tasks

### Matrix
- [ ] Rule on every capability of `using-git-worktrees` and `finishing-a-development-branch`

### Conventions
- [ ] Survey how this repository, scriptorium and forma-rust commit today — granularity, messages, branches — from their histories
- [ ] Design the `[git]` table — branching, commit granularity, message format, worktrees, and what the roadmap skill's commit steps read — and get the user's approval

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
Phase 1's execution model and Phase 2's proof per task.

### Constraints
Every verdict cites its evidence. No code in this phase. The `[git]` table of
`.agent-conventions.toml` decides, per repository, whether work stays on `main` or goes
to branches, and when the execution operation commits — at each task's end or at the
closure (rows EP9 and WP4, decision 3 of Phase 1). Row RC10, replies in a forge's
review threads through `gh`, is ruled with the pull-request capabilities of
`finishing-a-development-branch`.

---

## Acceptance Criteria

- [ ] Both skills have their verdicts with their reasons
- [ ] The `[git]` table is designed and approved by the user
