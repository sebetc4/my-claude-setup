# Phase 3: Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/2)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-git-skill.md` and `phase-2-git-skill-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-release-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Release the `git` domain and the roadmap skill's `branch = "roadmap"`, and install them.

---

## Overview

### Why This Phase Matters
The request that started the roadmap is served only once both are installed.

### What It Enables
The requesting repository sets its `[git]` table's `branch`.

### Out of Scope
Changing the `[git]` table of a repository that did not ask.

---

## Tasks

### Release
- [ ] Make `git` a domain — `VERSION`, `CHANGELOG.md`, `tests/` — add its skill to `domains/review/hooks/tools.json` and to `CLAUDE.md`, install it with the user's go-ahead, and tag it after the merge
- [ ] Release the roadmap domain with `branch = "roadmap"`, install it with the user's go-ahead, and tag it after the merge

---

## Technical Details

### Files to Modify
```
domains/git/VERSION         new
domains/git/CHANGELOG.md    new
domains/roadmap/VERSION
domains/roadmap/CHANGELOG.md
domains/review/hooks/tools.json
CLAUDE.md
```

### Dependencies
Phases 1 and 2.

### Constraints
Nothing is installed into `~/.claude` without the user's go-ahead.

---

## Acceptance Criteria

- [ ] The `git` domain and the roadmap domain are released and installed
