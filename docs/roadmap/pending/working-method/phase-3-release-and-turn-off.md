# Phase 3: Release And Turn-Off

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/2)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-finding-root-causes.md` and `phase-2-finding-root-causes-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-release-and-turn-off-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Release the `working-method` domain, and clear what the superpowers plugin left in this
repository: the plugin itself was uninstalled everywhere on 2026-10-04, ahead of the
study's plan.

---

## Overview

### Why This Phase Matters
With the two skills and roadmap `roadmap-execution` installed, every kept capability of
the plugin, uninstalled on 2026-10-04, has its receiver again.

### What It Enables
The plugin's kept capabilities back in every repository, in this setup's own tools.

### Out of Scope
The git domain: roadmap `git-domain`, which the turn-off does not wait for.

---

## Tasks

### Release
- [ ] Make `working-method` a domain — `VERSION`, `CHANGELOG.md`, `tests/` — add its skills to `domains/review/hooks/tools.json` and to `CLAUDE.md`, install it with the user's go-ahead, and tag it after the merge

### Turn Off
- [ ] Read `.superpowers/` for anything to keep, then remove it and its line in `CLAUDE.md`

---

## Technical Details

### Files to Modify
```
domains/working-method/VERSION              new
domains/working-method/CHANGELOG.md         new
domains/review/hooks/tools.json
CLAUDE.md
```

### Dependencies
Phases 1 and 2; roadmap `roadmap-execution`, installed.

### Constraints
Nothing is changed in the user's settings, and nothing installed, without the user's
go-ahead.

---

## Acceptance Criteria

- [ ] A new session in each repository lists no superpowers skill and receives no injection
- [ ] The `working-method` domain is released and installed
