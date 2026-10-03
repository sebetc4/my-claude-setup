# Phase 3: Release And Turn-Off

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
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

Release the `working-method` domain, then turn the superpowers plugin off by the plan of
the study's decision record.

---

## Overview

### Why This Phase Matters
With the two skills and roadmap `roadmap-execution` installed, every kept capability of
the plugin has its receiver, and the plugin's ~1,650 tokens per session buy nothing more.

### What It Enables
Sessions without the plugin in every repository, and the plugin's uninstall.

### Out of Scope
The git domain: roadmap `git-domain`, which the turn-off does not wait for.

---

## Tasks

### Release
- [ ] Make `working-method` a domain — `VERSION`, `CHANGELOG.md`, `tests/` — add its skills to `domains/review/hooks/tools.json` and to `CLAUDE.md`, install it with the user's go-ahead, and tag it after the merge

### Turn Off
- [ ] Check the go-ahead conditions of the plan in the study's decision record, then, with the user's go-ahead, set the plugin off in the user settings and in scriptorium's and forma-rust's local settings, and remove the deny rule on `writing-skills`
- [ ] Check a new session in each repository: no `superpowers:` line in the skill listing, no injection
- [ ] Read `.superpowers/` for anything to keep, then remove it and its line in `CLAUDE.md`
- [ ] Two weeks after the turn-off, read the tool reviews of the replacements, then, with the user's go-ahead, uninstall the plugin at every scope and remove its cache

---

## Technical Details

### Files to Modify
```
domains/working-method/VERSION              new
domains/working-method/CHANGELOG.md         new
domains/review/hooks/tools.json
CLAUDE.md
~/.claude/settings.json                     with the user's go-ahead
<repository>/.claude/settings.local.json    scriptorium, forma-rust, with the user's go-ahead
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
