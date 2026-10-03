# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, on the request that starts this roadmap, what the git domain and
`branch = "roadmap"` must do, before any change.

---

## Overview

### Why This Phase Matters
The study kept these rows for a need no repository had on 2026-10-03: the request that
starts the roadmap says which of them it needs, and may add pull requests.

### What It Enables
Phases 1 and 2 build what the request needs, on approved designs.

### Out of Scope
Changes to the skills: they start in Phase 1.

---

## Tasks

### Inputs
- [ ] Record the request that starts this roadmap — the repository, what it asks — and read the git rows of the study's decision record against it

### Design
- [ ] Write the design of `branch = "roadmap"` in `open-phase` and `close-roadmap` — the branch made, its base recorded, the integration proposed, the branch kept — and get the user's approval
- [ ] Write the design of the git skill — its name, its description, its steps for a linked worktree, a removal, an integration and a discard — and, when the request names pull requests, of the phase that adds them, and get the user's approval

### Record
- [ ] Write the decision record under `docs/decisions/`

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-git-domain.md    new
```

### Dependencies
Roadmap `roadmap-execution`, completed; a repository's request.

### Constraints
No change to the skills in this phase.

---

## Acceptance Criteria

- [ ] The designs are approved by the user
- [ ] The decision record is committed
