# Phase 3: Release

---

## Status

**Current Status:** 🟢 Done (100% — 4/4)
**Started:** 2026-10-15
**Completed:** 2026-10-15
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-judgments.md` and `phase-2-judgments-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-release-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Release the domain `skill-tooling` with Phases 1 and 2, and hand the two paused skills
back to their roadmaps under the default regime of
`docs/decisions/2026-10-15-validation-weight.md`.

---

## Overview

### Why This Phase Matters
Two skills useful from their second iteration have waited since 2026-10-14 for the
validation's update.

### What It Enables
`close-session` finished and installed; ai-ctl's review run on real code; roadmap
`lean-workflow`.

### Out of Scope
Moved on 2026-10-15 to roadmap `lean-workflow`'s Phase 1: the regimes, the fix from use,
real-use failures as grounds for a prohibition. Dropped the same day, to revisit as the
decision record says: the sources' place (V4), the replay of both skills' recorded
evidence, the re-evaluation of `authoring-skills` on all its evals.

---

## Tasks

### Release
- [x] Fix at their source the points of the `skill-auditor` FAILs of 2026-10-15 on `authoring-skills`, those Phase 1's report left to later phases and those of Phase 2's measure, then audit `authoring-skills` and the changed agents
  Proof: check — `audit.py` clean; `skill-auditor`'s two passes `VERDICT: PASS` on each, the full regime
- [x] Release the domain `skill-tooling`: `VERSION`, its `CHANGELOG.md` entry dated, installed with `make update D=skill-tooling` on the user's yes, its tag on `main` after the merge with `make tags`
  Proof: check — `make check` passing, `make list` showing the installed version equal to the repository's, `git tag --points-at` naming the tag

### Hand-Over
- [x] Write the hand-over in `notes/design-feedback/`, for this repository and for ai-ctl: the default regime each resumes under, the lines each skill carries because of the validation that it may revert, from Phase 0's list, and each one's next step — `close-session` installed as it stands, ai-ctl's `review-skill` to its Phase 4
  Proof: review — the note read by the user
- [x] Tell the user the tool is released, so that they lift the ⏸️ of `session-close`'s Phase 1 and resume ai-ctl's roadmap; update `docs/roadmap/README.md`
  Proof: check — `docs/roadmap/README.md` no longer naming this roadmap as a blocker

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/references/
domains/skill-tooling/agents/skill-auditor.md
domains/skill-tooling/VERSION
domains/skill-tooling/CHANGELOG.md
docs/roadmap/README.md
notes/design-feedback/<date>-skill-validation-hand-over.md    new, ignored
```

### Dependencies
Phase 2: the classes, the criterion, the auditor's fixed request.
Phase 1's report: the points of the `skill-auditor` FAIL of 2026-10-15 left to later
phases — the sources of `references/discipline.md`'s three pressures and of
`references/create-and-edit.md`'s five samples; the shared `references/conventions.md`'s
"never as one the user already approved"; the previous version copied before an edit;
the old block's removal offered with no edit nor check; the words eval, case and query
across `references/evaluate.md` and `references/create-and-edit.md`.
Phase 2's report: the points of its two FAIL passes on `authoring-skills` at `5d7228a`,
each checked against the current text first — `references/conventions.md:14`, `:16`,
`:21-24` and `:87`, whose source is `shared/conventions/conventions.md`;
`references/audit.md:4`; `references/create-and-edit.md:85-89`; `references/evaluate.md`
citing roadmap reports as sources; the static audit, the conventions file and the
instruction file each named two ways. `skill-auditor`'s text of `669a6b1` reaches a
session once installed, or copied to `.claude/agents/` before the session starts.

### Constraints
Every eval session is announced with its count and cost and started on the user's
yes. `make update` on the real `~/.claude` only on the user's yes. Nothing is pushed.

---

## Acceptance Criteria

- [ ] The auditor passes `authoring-skills` and the changed agents
- [x] The domain `skill-tooling` is released, installed and tagged
- [x] The hand-over note is written and the user told
