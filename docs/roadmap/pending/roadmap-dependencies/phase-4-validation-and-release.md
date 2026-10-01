# Phase 4: Validation And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-fixes.md` and `phase-3-fixes-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-validation-and-release-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Show that the new skill does at least as well as roadmap 2.0.0 on every scenario, then
release and install it.

---

## Overview

### Why This Phase Matters
The dependency model touches creation, opening and both closures: every ritual the evals
cover.

### What It Enables
The release of roadmap 3.0.0, and the work-in-progress rule in every repository.

### Out of Scope
Moving forma-rust's roadmaps under its `root`.

---

## Tasks

### Evals
- [ ] Add two scenarios to `evals/`: opening a phase that waits for an open roadmap, and closing a roadmap that another one waits for
- [ ] Run every scenario on the new skill and on a snapshot of 2.0.0 — which also measures the 2.0.0 text left unrun in skill-tooling's Phase 1 — and compare

### Release
- [ ] Bump the roadmap domain to 3.0.0 with its `CHANGELOG.md` entry, and install it with the user's go-ahead
- [ ] Check the `Blocked By` entries of this repository's and scriptorium's roadmaps against the new form, and rewrite those that name a roadmap

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/evals/evals.json
domains/roadmap/skills/roadmap/evals/build_fixtures.py
domains/roadmap/skills/roadmap/evals/grade.py
domains/roadmap/VERSION
domains/roadmap/CHANGELOG.md
```

### Dependencies
Phases 1 to 3.

### Constraints
Nothing is installed into `~/.claude` without the user's go-ahead.

---

## Acceptance Criteria

- [ ] The new skill passes at least as many assertions as 2.0.0, and both new scenarios
- [ ] Roadmap 3.0.0 is installed
