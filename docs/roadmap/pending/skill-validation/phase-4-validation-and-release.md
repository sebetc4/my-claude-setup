# Phase 4: Validation And Release

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/6)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-evidence-and-sources.md` and `phase-3-evidence-and-sources-report.md` in
full before touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-validation-and-release-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Prove the update on the evidence that showed its gaps, release the domain
`skill-tooling`, and hand the two paused skills back to their roadmaps with what each can
revert.

---

## Overview

### Why This Phase Matters
The update answers failures recorded on two real skills. Its proof is that the same
evidence, judged again, no longer asks for a change to either skill where none was due,
while the failures the evals rightly caught still show.

### What It Enables
Phase 1 of roadmap `session-close` and Phase 3 of ai-ctl's roadmap `review-skill`
resume on the updated tool.

### Out of Scope
Reworking `close-session` and `reviewing-delivered-code`, reverting the lines they carry
because of the validation included: their own roadmaps.

---

## Tasks

### Replay
- [ ] Judge `close-session`'s recorded evidence with the updated tool: iterations 10 and 11's two failures classified, the criterion read over their twelve runs, and iteration 2's baselines still failing where they failed
  Proof: review — the classes and the criterion's result in the report, no failure of the skill's arm classified as its defect without evidence, read by the user
- [ ] Judge `reviewing-delivered-code`'s iteration 2 with the updated tool, with the user's leave in ai-ctl: "Claims hold" in its original wording with the agents' starting context in view, the guards read as guards, the run's figures exact
  Proof: review — the new gradings and figures in the report, read by the user

### Authoring-Skills
- [ ] Evaluate `authoring-skills` on its own evals with the updated tool, then audit it and the changed agents
  Proof: eval — its cases meeting the new criterion; `audit.py` clean; `skill-auditor`'s `VERDICT: PASS` on the skill and on each changed agent

### Release
- [ ] Release the domain `skill-tooling`: `VERSION`, its `CHANGELOG.md` entry dated, installed with `make update D=skill-tooling` on the user's yes, its tag on `main` after the merge with `make tags`
  Proof: check — `make check` passing, `make list` showing the installed version equal to the repository's, `git tag --points-at` naming the tag

### Hand-Over
- [ ] Write the hand-over in `notes/design-feedback/`, for this repository and for ai-ctl: what the updated tool changes, and which lines each skill carries because of the validation it may now revert, from Phase 0's list
  Proof: review — the note read by the user
- [ ] Tell the user the tool is released, so that they lift the ⏸️ of `session-close`'s Phase 1 and resume ai-ctl's Phase 3; update `docs/roadmap/README.md`
  Proof: check — `docs/roadmap/README.md` no longer naming this roadmap as a blocker

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/VERSION
domains/skill-tooling/CHANGELOG.md
docs/roadmap/README.md
notes/design-feedback/<date>-skill-validation-hand-over.md    new, ignored
```

### Dependencies
Phases 1 to 3.

### Constraints
Every eval session is announced with its count and cost and started on the user's yes.
`make update` on the real `~/.claude` only on the user's yes. Nothing is pushed.

---

## Acceptance Criteria

- [ ] The recorded evidence of both skills, judged again, asks for no change to either skill where the classification finds no defect of it
- [ ] `authoring-skills` passes its own evals by the new criterion, and the auditor passes it
- [ ] The domain `skill-tooling` is released, installed and tagged
- [ ] The hand-over note is written and the user told
