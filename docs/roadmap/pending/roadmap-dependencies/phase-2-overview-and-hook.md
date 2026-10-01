# Phase 2: Overview And Hook

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-dependencies.md` and `phase-1-dependencies-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-overview-and-hook-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

One command shows every roadmap of a repository — its state, its phase in progress, its
progress and what it waits for — and the session hook says when an open roadmap waits.

---

## Overview

### Why This Phase Matters
With every roadmap side by side and linked by dependencies, the order of the work is
spread over several READMEs; a `blocked/` folder was turned down for a view computed
from them.

### What It Enables
The user and the agent see at once which roadmap to work on next.

### Out of Scope
A maintained index file: the view is computed, never stored.

---

## Tasks

### Overview
- [ ] Write the failing tests of `scripts/roadmaps.py <root>`: every roadmap with its state, its phase in progress, its progress and the roadmap it waits for
- [ ] Implement `scripts/roadmaps.py` and cite it from `SKILL.md`

### Hook
- [ ] Make `hooks/session_resume.py` name, in its line, the roadmap an open roadmap waits for — failing tests first
- [ ] Decide under the work-in-progress rule whether the hook still names a roadmap that waits, and apply the decision

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/scripts/roadmaps.py    new
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/hooks/session_resume.py
domains/roadmap/tests/test_hooks.py
```

### Dependencies
Phase 1's `Blocked By` form.

### Constraints
Python standard library only; failing tests first. The hook stays one line per roadmap.

---

## Acceptance Criteria

- [ ] `scripts/roadmaps.py` lists every roadmap of this repository and of scriptorium with its state and what it waits for
- [ ] The session hook names the roadmap an open one waits for, in one line
