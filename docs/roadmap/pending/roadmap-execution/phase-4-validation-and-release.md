# Phase 4: Validation And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-execute-phase.md` and `phase-3-execute-phase-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-validation-and-release-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Show that the skill with `execute-phase` does at least as well as its previous release
on every scenario, then release and install it.

---

## Overview

### Why This Phase Matters
The operation changes how every phase of every roadmap runs.

### What It Enables
Roadmap `working-method` starts, and phases run with declared proofs and commits per
task in every repository that declares them.

### Out of Scope
Turning the plugin off: roadmap `working-method`.

---

## Tasks

### Evals
- [ ] Add the scenarios chosen in Phase 0 to `evals/`
- [ ] Run every scenario on the new skill and on a snapshot of its previous release, and compare

### Release
- [ ] Bump the roadmap domain with its `CHANGELOG.md` entry, install it with the user's go-ahead, and tag it after the merge
- [ ] Update `CLAUDE.md`: the proof reference in `shared/`, the operation and the two agents

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/evals/evals.json
domains/roadmap/skills/roadmap/evals/build_fixtures.py
domains/roadmap/VERSION
domains/roadmap/CHANGELOG.md
CLAUDE.md
```

### Dependencies
Phases 1 to 3.

### Constraints
Nothing is installed into `~/.claude` without the user's go-ahead.

---

## Acceptance Criteria

- [ ] The new skill matches or beats its previous release on every scenario
- [ ] The roadmap domain is released and installed
