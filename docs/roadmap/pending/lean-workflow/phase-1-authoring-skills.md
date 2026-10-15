# Phase 1: Authoring Skills

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-measure-and-design.md` and `phase-0-measure-and-design-report.md` in full
before touching anything here: the decisions already taken, the problems and deviations
recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-authoring-skills-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Give `authoring-skills` the default and full regimes, the stop rule and the fix from
use, and remove from its procedures, references, scripts and agents what Phase 0's
design cuts.

---

## Overview

### Why This Phase Matters
The skill gives every change the heaviest proof; a useful skill waited days behind it.

### What It Enables
A tool built in about a day under the default regime, then improved from its use.

### Out of Scope
The roadmap skill, the conventions, the memories and the reviews: Phase 2.

---

## Tasks

### Regimes
Moved from roadmap `skill-validation`'s Phase 3 on 2026-10-15.
- [ ] Write the default regime, the full regime with its three criteria and its cap of three iterations, and the stop rule into `references/evaluate.md`, routed from `SKILL.md`; the default regime's single auditor pass and the full regime's two into `references/audit.md`
  Proof: eval — a case in the Cut task's iteration, asking to validate a change no criterion of the full regime covers
- [ ] Add the fix from use to `references/create-and-edit.md`'s Edit section, and the key `failures_in_use` to `evals/evals.json`, each entry with its transcript or study, validated by `workspace.py` and given in `references/eval-files.md`
  Proof: test — an entry with its reference accepted and one without refused, red before the code; eval — a case in the Cut task's iteration, fixing a skill from a quoted real-session failure
- [ ] Accept a failure seen in real use as grounds for a prohibition, in the writing guide's The Form Follows The Failure and in `skill-auditor`'s form judgment
  Proof: check — two fixtures under `evals/auditor/`, a prohibition grounded in a real-use failure alone passing, one grounded in nothing failing

### Cut
- [ ] Remove from `authoring-skills`' references, scripts and agents what Phase 0's design cuts, one yes per iteration covering its runs and gradings among them
  Proof: eval — one iteration against the previous version, the existing cases as guards; the references' words against Phase 0's target

### Release
- [ ] Release the domain `skill-tooling`: `VERSION`, its `CHANGELOG.md` entry dated, installed with `make update D=skill-tooling` on the user's yes, its tag with `make tags`
  Proof: check — `make check` passing, `make list` showing the installed version equal to the repository's

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/
domains/skill-tooling/agents/
domains/skill-tooling/tests/
domains/skill-tooling/VERSION
domains/skill-tooling/CHANGELOG.md
```

### Dependencies
Phase 0's design and targets. Roadmap `skill-validation` released.

### Constraints
`authoring-skills` falls under the full regime: three iterations at most. Remove before
adding. Scripts test-first.

---

## Acceptance Criteria

- [ ] `authoring-skills` states the two regimes, the stop rule and the fix from use
- [ ] Its existing cases still pass, and its references meet Phase 0's target
- [ ] The domain is released and installed
