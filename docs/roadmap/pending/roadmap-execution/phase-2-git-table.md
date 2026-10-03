# Phase 2: Git Table

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-proof-and-template.md` and `phase-1-proof-and-template-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-git-table-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Read the `[git]` table and commit by it: `commit`, `message` and `branch = "none"` built,
`branch = "roadmap"` refused with its reason until roadmap `git-domain` builds it.

---

## Overview

### Why This Phase Matters
Phase 3 of the study decided commits per task in this repository and scriptorium, and
the `message` key as the format's only written source; nothing reads either yet.

### What It Enables
Phase 3's operation commits each task, and this repository's `CLAUDE.md` loses its
commit-message line.

### Out of Scope
`branch = "roadmap"`, worktrees and the git domain: roadmap `git-domain`.

---

## Tasks

### Conventions
- [ ] Add the `[git]` table to `shared/conventions/conventions.py` — its three keys and their values, validated, present when the contract says `versioning = "git"`, its values proposed from `git log` when it is missing — failing tests first, then refresh the copies with `make shared`
- [ ] Write the `[git]` table into this repository's and scriptorium's `.agent-conventions.toml`, with the user's agreement

### Rituals
- [ ] Make `close-phase.md` and `close-roadmap.md` commit by the table: under `task`, the closure commit holds the closure documents only; under `closure`, the phase's work and its closure in one commit; the subject in the `message` format
- [ ] Replace this repository's `CLAUDE.md` line on commit messages with a pointer to the key, and record the harness's commit trailer in `docs/claude-code-coupling.md`

---

## Technical Details

### Files to Modify
```
shared/conventions/conventions.py
shared/conventions/conventions.md
shared/conventions/tests/test_conventions.py
domains/roadmap/skills/roadmap/scripts/conventions.py    copy
domains/roadmap/skills/roadmap/references/close-phase.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
CLAUDE.md
docs/claude-code-coupling.md
```

### Dependencies
Phase 0's designs.

### Constraints
Python standard library only; failing tests first. `.agent-conventions.toml` is written
only with the user's agreement.

---

## Acceptance Criteria

- [ ] `conventions.py` reads and validates the `[git]` table, and refuses `branch = "roadmap"` with its reason
- [ ] A closure in this repository commits by the table
- [ ] `make check` passes
