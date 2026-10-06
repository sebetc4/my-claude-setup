# Phase 3: Validation And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-reviews-and-reports.md` and `phase-2-reviews-and-reports-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-validation-and-release-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Show that the counts match Claude Code's own, recount a real phase, and release the
review domain.

---

## Overview

### Why This Phase Matters
A cost tool that is wrong is worse than none: decisions would rest on it. Claude Code's
`cost-state` records give, for whole sessions, a total to compare with.

### What It Enables
Every roadmap after this one is measured as it is built.

### Out of Scope
New measures: a gap the validation finds is fixed or recorded, not extended.

---

## Tasks

### Validation
- [ ] Recount every session of this repository that holds a `cost-state` record covering it whole, and compare each model's cost with the record's `costUSD`
  Proof: check — the command run on each such session, every model within a cent of `costUSD`, each gap explained in the report
- [ ] Recount the last closed phase of a roadmap and compare with a count by hand of its sessions, made with the method of `docs/decisions/2026-10-06-token-costs.md`
  Proof: review — the two counts side by side, each gap explained, approved by the user

### Documentation
- [ ] Update `CLAUDE.md`: the review domain described as reviewing how tools work and what they cost, no longer as temporary, and the new command under Commands
  Proof: review — the lines changed, approved by the user

### Release
- [ ] Release the review domain: `VERSION` 0.2.0, its `CHANGELOG.md` entry, and the `review-v0.2.0` tag on `main` after the merge
  Proof: check — `make check`, whose `tests/domains.py` compares `VERSION` with the changelog's first entry, then `git tag --points-at` on `main`'s merge commit naming `review-v0.2.0`
- [ ] With the user's go-ahead, install the release with `make update D=review`
  Proof: check — `make update D=review CLAUDE_DIR=$(mktemp -d)` first, then on `~/.claude` with the go-ahead, and `make list` showing review 0.2.0 installed

---

## Technical Details

### Files to Modify
```
CLAUDE.md
domains/review/VERSION
domains/review/CHANGELOG.md
```

### Dependencies
Phases 1 and 2.

### Constraints
`make update` touches the real `~/.claude`: it waits for the user's go-ahead. A
`cost-state` record written when a session was resumed covers only the session's part
before the resume: only a record that covers the whole session is a reference.

---

## Acceptance Criteria

- [ ] Every session with a `cost-state` record covering it whole is recounted within a cent per model
- [ ] Review 0.2.0 is tagged and installed
