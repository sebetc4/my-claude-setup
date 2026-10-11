# Phase 2: Adoption And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-standard-skill.md` and `phase-1-standard-skill-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-adoption-and-release-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Install the standard skill, move scriptorium on to it, try it in a second repository,
and release the domain.

---

## Overview

### Why This Phase Matters
A standard tool is shown standard by a second repository: scriptorium alone would prove
only the port.

### What It Enables
Any repository reviews the tools it builds for itself, and the findings of both review
tools are read side by side.

### Out of Scope
New measures: a gap the adoption finds is fixed or recorded, not extended.

---

## Tasks

### Adoption
- [ ] With the user's go-ahead, install the domain on `~/.claude`
  Proof: check — the install first under `CLAUDE_DIR=$(mktemp -d)`, then on `~/.claude` with the go-ahead, and `make list` showing the version installed
- [ ] With the user's go-ahead in scriptorium, move it on to the installed skill: its conventions written, its project copy and its ledger hook removed as the design said
  Proof: check — a review written in scriptorium with the installed skill, and its earlier reviews read by the aggregate
- [ ] Try the skill in a second repository that builds tools for itself
  Proof: review — one review written at the end of a real task, and what it showed, approved by the user

### Release
- [ ] Update `CLAUDE.md`: the skill under Layout, and how a repository adopts it
  Proof: review — the lines changed, approved by the user
- [ ] Release the domain: `VERSION`, its `CHANGELOG.md` entry, and its tag on `main` after the merge, with `make tags`
  Proof: check — `make check`, whose `tests/domains.py` compares `VERSION` with the changelog's first entry, then `git tag --points-at` on `main`'s merge commit naming the tag

---

## Technical Details

### Files to Modify
```
CLAUDE.md
domains/<domain>/VERSION
domains/<domain>/CHANGELOG.md
```

### Dependencies
Phase 1: the standard skill.

### Constraints
`make update` touches the real `~/.claude`, and every change in scriptorium is made in
that repository: each waits for the user's go-ahead. scriptorium's earlier reviews keep
their format; the aggregate reads them, or the design says why not. If the design puts
the skill in the review domain, its release comes after the review 0.3.0 of roadmap
`token-usage`.

---

## Acceptance Criteria

- [ ] A review is written with the installed skill in scriptorium and in a second repository
- [ ] The release is tagged and installed
