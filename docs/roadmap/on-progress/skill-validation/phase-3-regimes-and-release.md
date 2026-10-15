# Phase 3: Regimes And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-judgments.md` and `phase-2-judgments-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-regimes-and-release-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Write the validation's two regimes, its stop rule and the fix from use into
`authoring-skills`, release the domain `skill-tooling`, and hand the two paused skills
back to their roadmaps, as `docs/decisions/2026-10-15-validation-weight.md` decided.

---

## Overview

### Why This Phase Matters
The validation had one size, the heaviest, whatever the tool's risk: two skills useful
from their second iteration waited days behind it, and fixes seen in real use waited
behind them.

### What It Enables
`close-session` installed and used; ai-ctl's review run on real code; later tools built
in about a day and improved from their use.

### Out of Scope
Dropped on 2026-10-15, to revisit as the decision record says: the sources' place (V4),
the replay of both skills' recorded evidence, the re-evaluation of `authoring-skills` on
all its evals.

---

## Tasks

### Regimes
- [ ] Write the default regime, the full regime with its three criteria and its cap of three iterations, and the stop rule into `references/evaluate.md`, routed from `SKILL.md`; the default regime's single auditor pass and the full regime's two into `references/audit.md`
  Proof: eval — one iteration against the previous version, a case asking to validate a change to a skill that no criterion of the full regime covers
- [ ] Add the fix from use to `references/create-and-edit.md`'s Edit section, and the key `failures_in_use` to `evals/evals.json`, each entry with its transcript or study, validated by `workspace.py` and given in `references/eval-files.md`
  Proof: test — an entry with its reference accepted and one without refused, red before the code; eval — in the same iteration, a case fixing a skill from a quoted real-session failure
- [ ] Accept a failure seen in real use as grounds for a prohibition, in the writing guide's The Form Follows The Failure and in `skill-auditor`'s form judgment
  Proof: check — two fixtures under `evals/auditor/`, a prohibition grounded in a real-use failure alone passing, one grounded in nothing failing

### Release
- [ ] Fix at their source the points of the `skill-auditor` FAIL of 2026-10-15 on `authoring-skills` that Phase 1's report left to later phases, then audit `authoring-skills` and the changed agents
  Proof: check — `audit.py` clean; `skill-auditor`'s two passes `VERDICT: PASS` on each, the full regime
- [ ] Release the domain `skill-tooling`: `VERSION`, its `CHANGELOG.md` entry dated, installed with `make update D=skill-tooling` on the user's yes, its tag on `main` after the merge with `make tags`
  Proof: check — `make check` passing, `make list` showing the installed version equal to the repository's, `git tag --points-at` naming the tag

### Hand-Over
- [ ] Write the hand-over in `notes/design-feedback/`, for this repository and for ai-ctl: the regimes, the lines each skill carries because of the validation that it may revert, from Phase 0's list, and each one's next step — `close-session` installed as it stands, ai-ctl's `review-skill` to its Phase 4
  Proof: review — the note read by the user
- [ ] Tell the user the tool is released, so that they lift the ⏸️ of `session-close`'s Phase 1 and resume ai-ctl's roadmap; update `docs/roadmap/README.md`
  Proof: check — `docs/roadmap/README.md` no longer naming this roadmap as a blocker

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/SKILL.md
domains/skill-tooling/skills/authoring-skills/references/evaluate.md
domains/skill-tooling/skills/authoring-skills/references/audit.md
domains/skill-tooling/skills/authoring-skills/references/create-and-edit.md
domains/skill-tooling/skills/authoring-skills/references/eval-files.md
domains/skill-tooling/skills/authoring-skills/references/writing-guide.md
domains/skill-tooling/skills/authoring-skills/scripts/workspace.py
domains/skill-tooling/agents/skill-auditor.md
domains/skill-tooling/skills/authoring-skills/evals/
domains/skill-tooling/tests/test_*.py
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

### Constraints
Scripts test-first. `authoring-skills` falls under the full regime: three iterations at
most. Every eval session is announced with its count and cost and started on the user's
yes. `make update` on the real `~/.claude` only on the user's yes. Nothing is pushed.

---

## Acceptance Criteria

- [ ] `authoring-skills` states the two regimes, the stop rule and the fix from use, and its iteration beats the previous version
- [ ] The auditor passes `authoring-skills` and the changed agents
- [ ] The domain `skill-tooling` is released, installed and tagged
- [ ] The hand-over note is written and the user told
