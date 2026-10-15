# Phase 3 Report: Release

**Phase:** [phase-3-release.md](phase-3-release.md)
**Start Commit:** fde4222

---

## Work Log

### 2026-10-15

Phase opened at the end of Phase 2's closure (`fde4222`), in the session that closed it,
after Phase 2's file and report; no restructuring pending. The opening is left
uncommitted, to go with the phase's first finished step.

A figure of Phase 2's report, unsettled: its auditor measure's $3.00 is `usage.py` run on
each pass's transcript, $2.11 of it estimated; `tool-review`'s `measure.py` counts the
same eleven passes at $1.04. The gap lies in the estimate of the subagents' output.

`skill-auditor`'s text of `669a6b1` copied again to `.claude/agents/`, uncommitted, so
that the next session loads it; removed before this phase closes, the install then
bringing it.

**Where the next session starts:**
1. Task 1: the points of Phase 1's FAIL and of Phase 2's two FAILs, in this phase's
   Dependencies, each checked against `authoring-skills`' current text, then fixed at
   its source, `shared/conventions/conventions.md` for the shared copy; `audit.py`; two
   passes of `skill-auditor` on `authoring-skills` and on the changed agents, announced
   with their cost.
2. Tasks 2 to 4: the release, the hand-over note, the overview.

Session resumed, task 1. The FAILs' lines read from the passes' transcripts, each
checked against the current text and fixed at its source, cutting where the guide
allowed:
- `shared/conventions/conventions.md` (`make shared`: roadmap, tool-review,
  close-session, authoring-skills): `:14`'s causes cut, the `problem:` line saying why;
  `:16`'s `checks` sentence and `:87`'s `residue` clause cut, no failure grounding them;
  `:21-24` down to its conditional, report and stop; `:45`'s block deleted on the
  user's yes, the lines removed shown.
- `references/audit.md:4`: "unless the user asks" cut, The Report already making a fix
  asked for an edit. `references/create-and-edit.md`: the baseline's step,
  `workspace.py --baseline`; the micro-test sourced (writing-skills); the cost clause
  cut. `references/discipline.md`: the pressures sourced (writing-skills).
- `references/evaluate.md`: its opening names an output eval's cases and a trigger
  eval's queries; the roadmap reports cited by the roadmap's name and the file's, the
  user correcting a first fix by paths, the repository's convention; the writing guide
  gives that form. "The static audit" for `audit.py`'s in `SKILL.md`,
  `create-and-edit.md` and `evaluate.md`.

A line in the unreleased changelogs of `skill-tooling`, `roadmap`, `review` and
`session`. `audit.py` clean on the four skills, `make check` passing.

The changed agents: no `skill-auditor` pass, the user choosing the proof already
recorded — the auditor's seven fixtures holding (Phase 2), `skill-grader`'s `context/`
and `whole/` by Phase 1's tests and gradings; `skill-auditor` judges a skill.

Iteration 1 of the full regime's three, on the user's yes: FAIL and FAIL, $0.98 by
`usage.py` ($0.59 estimated). Seven points, none a repeat but `conventions.md`'s block
removal, each fixed: the removal's offer cut from `shared/conventions/`;
`references/audit.md`'s two prohibitions stated as the procedure, a fix reverted checked
by `git diff`; `SKILL.md`'s unsourced clause on where `triggers.py` puts the copy cut;
`references/evaluate.md`'s "a check" made "an assertion under `assertions`", the judgment
varying sourced to roadmap `skill-tooling`: `phase-3-writing-method-report.md`, the
"costs cents" clause cut. `audit.py` clean on the four skills, `make check` passing.

Iteration 2, on the user's yes: FAIL and FAIL, $1.10 by `usage.py` ($0.59 estimated).
Five points, one a repeat — the revert, now `git checkout` with `git diff` as its check —
and four sources: The Keys' source named, `scripts/conventions.py`, `start_notes`'
default cut, left to its hook; `references/eval-files.md` links the hooks page, sources
the json result's duration to roadmap `skill-validation`: `phase-1-run-world-report.md`,
drops the retention clause. Fourteen points over four passes, two repeats: each pass
samples a 12,600-word skill anew, Phase 2's open search. `audit.py` clean on the four
skills, `make check` passing.

Iteration 3, the full regime's last, on the user's yes: FAIL and FAIL, one point each,
$0.86 by `usage.py` ($0.43 estimated): `references/audit.md` calling the auditor's
findings "points" and "problems", now "problems"; `references/writing-guide.md`'s 500
lines unsourced, now the specification's § Progressive disclosure. Both fixed, `audit.py`
clean, `make check` passing. Points per iteration 7, 5, 2. Task 1 ticked at the cap, no
point left open. The auditor's three iterations cost $2.94.

**Where the next session starts:** task 2, the release: `CHANGELOG.md`'s 0.1.2 dated,
`make update D=skill-tooling` on the user's yes, `.claude/agents/`'s copy removed, `make
tags`; then the hand-over note and the overview.

---

## Decisions

- **The changed agents keep the proof already recorded** (the user): `skill-auditor`'s
  seven fixtures holding (Phase 2), `skill-grader`'s `context/` and `whole/` by Phase 1;
  `skill-auditor` judges a skill, never an agent's file.
- **A roadmap's file is cited by the roadmap's name and the file's, never by a path** (the
  user, the repository's convention): `references/writing-guide.md` gives it as a
  source's form, so that the auditor judges by it.
- **Task 1 ticked at the full regime's cap**: three iterations, no PASS, each point fixed
  at its source and none left open, as Phase 2 ticked its tasks at the same cap.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
