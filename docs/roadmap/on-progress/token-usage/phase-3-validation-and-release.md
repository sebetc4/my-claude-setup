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
  Proof: check — the script of the review of several sessions run on each such session, every model within a cent of `costUSD`, each gap explained in the report
- [ ] Recount the last closed phase of a roadmap and compare with a count by hand of its sessions, made with the method of `docs/decisions/2026-10-06-token-costs.md`
  Proof: review — the two counts side by side, each gap explained, and the review's conclusions set beside the record's What They Suggest, approved by the user

### Documentation
- [ ] Update `CLAUDE.md`: the review domain described as reviewing how tools work and what they cost, no longer as temporary, with the review of several sessions under Layout
  Proof: review — the lines changed, approved by the user

### Release
- [ ] Release the review domain, `VERSION` 0.3.0, and the skill-tooling domain, 0.1.2, whose copy of `shared/usage/` Phase 1 changed: each `CHANGELOG.md` entry dated, and the `review-v0.3.0` and `skill-tooling-v0.1.2` tags on `main` after the merge
  Proof: check — `make check`, whose `tests/domains.py` compares each `VERSION` with its changelog's first entry, then `git tag --points-at` on `main`'s merge commit naming `review-v0.3.0` and `skill-tooling-v0.1.2`
- [ ] With the user's go-ahead, install the releases with `make update D=review` and `make update D=skill-tooling`
  Proof: check — each `make update` with `CLAUDE_DIR=$(mktemp -d)` first, then on `~/.claude` with the go-ahead, and `make list` showing review 0.3.0 and skill-tooling 0.1.2 installed

---

## Technical Details

### Files to Modify
```
CLAUDE.md
domains/review/VERSION
domains/review/CHANGELOG.md
domains/skill-tooling/CHANGELOG.md
```

### Dependencies
Phases 1 and 2.

### Constraints
`make update` touches the real `~/.claude`: it waits for the user's go-ahead. A
`cost-state` record written when a session was resumed covers only the session's part
before the resume: only a record that covers the whole session is a reference.

Counts by hand exist for two phases of `skill-tooling`. Phase 4,
`docs/decisions/2026-10-09-phase-4-token-costs.md`: ≈ $186.62, sixteen main sessions and
218 `claude -p` sessions, its transcripts deleted from 2026-11-05. Phase 5,
`docs/decisions/2026-10-11-phase-5-token-costs.md`: ≈ $158.54, fifteen main sessions and
248 `claude -p` sessions, its transcripts deleted from 2026-11-08. Each serves as the
reference only while its transcripts remain; past those dates, the count by hand is made
on a phase closed less than 30 days before.

---

## Acceptance Criteria

- [ ] Every session with a `cost-state` record covering it whole is recounted within a cent per model
- [ ] Review 0.3.0 and skill-tooling 0.1.2 are tagged and installed
