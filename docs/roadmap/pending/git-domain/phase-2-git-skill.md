# Phase 2: Git Skill

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-branch-per-roadmap.md` and `phase-1-branch-per-roadmap-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-git-skill-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Write the git skill from the kept rows of `using-git-worktrees` and
`finishing-a-development-branch`.

---

## Overview

### Why This Phase Matters
A session started in a linked worktree, a worktree to remove, a branch to integrate or
discard: each has a step the study kept and nothing of this setup holds.

### What It Enables
Worktrees and branches handled the same way in every repository.

### Out of Scope
Making, placing and removing the harness's own worktrees: the harness does it.

---

## Tasks

### Skill
- [ ] Write the git skill with `authoring-skills`, from Phase 0's design, with superpowers' MIT notice
- [ ] Run its output evals — a session started in a linked worktree, a removal refused over untracked files, a discard asked for — against no skill and against the two superpowers skills, and record the benchmark
- [ ] Run its trigger evals and tune the description

### Coupling
- [ ] Record in `docs/claude-code-coupling.md` the harness's worktree tools the skill names

---

## Technical Details

### Files to Modify
```
domains/git/skills/<name>/SKILL.md    new
domains/git/skills/<name>/evals/      new
docs/claude-code-coupling.md
```

### Dependencies
Phase 0's design.

### Constraints
Never `--force` on a removal, never a force-push without the user's explicit request.

---

## Acceptance Criteria

- [ ] The git skill matches or beats the two superpowers skills on every output scenario
- [ ] Its trigger evals pass
