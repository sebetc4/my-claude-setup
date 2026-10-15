# Roadmap: skill-validation

---

## Status Indicators

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Done
- ⏸️ Blocked
- ⚠️ Needs Review

---

## Overall Progress

```
Phase 0  Framing                    🟢 ████████████████████ 100%  (7/7)
Phase 1  Run World                  🟢 ████████████████████ 100%  (6/6)
Phase 2  Judgments                  🟢 ████████████████████ 100%  (7/7)
Phase 3  Release                    🟢 ████████████████████ 100%  (4/4)
TOTAL                                  ████████████████████ 100%  (24/24)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** —

---

## Why This Roadmap Exists

Two skills built with `authoring-skills` reached the same point on 2026-10-14: the work
bent the skill under construction around the gaps of the tool that validates it. In this
repository, `close-session` took eleven iterations and 81 runs, about $10.60 of runs,
$4.05 of grading and 14 `skill-auditor` passes; by iteration 2, every assertion passed
with the skill against 57% without it, and most of what followed answered the
validation. In ai-ctl, `reviewing-delivered-code` rewrote an assertion so that the grader
would look around the harness's rendering, and could not evaluate its last pass. Both
roadmaps are paused at the user's request, and each wrote its problems down:
`notes/design-feedback/2026-10-14-close-session-validation.md` (V1 to V7, directions D1
to D7) and `notes/design-feedback/2026-10-14-reviewing-delivered-code-validation.md`
(R1 to R6, directions E1 to E5), in the ignored `notes/`.

The common cause: the validation has five instruments — the run's world, the grader's
view, the assertions, the auditor, the figures —, while its procedure offers one lever,
the skill, and a proof that asks for every check to pass. When an instrument is wrong, no
step lets the agent name it and fix it, so the agent changes the skill until the
instrument passes. The instruments' defects fall into three families:
- the instrument does not see the world the skill meets once installed: a case run
  without the hook its configuration declares (V1), a grader that never sees the context
  a session starts with, `harness.render` keeping only the turns (R1), a workflow of
  several sessions with no case for it (R2), figures of runs with agents that mislead
  (R3);
- a judgment's spread is counted as a signal: one grading per run under a zero-failure
  proof (V2), an auditor that fails as soon as an open search finds anything and finds
  something else at each pass, as roadmap `skill-tooling` already saw in its Phase 3
  (V3), premises inside assertions (V6), guards told to discriminate (R4), a list
  failing whole on one item (R5);
- the rules of evidence sit in the wrong place: sources that only the editor reads,
  loaded at every use (V4), and failures seen in real sessions or in a study counting for
  nothing (V5, R6).

This roadmap updates `authoring-skills`, its scripts and its agents `skill-grader` and
`skill-auditor`, so that the validation tells a skill's quality apart from its own
instruments' errors, and a skill under construction is never changed to satisfy an
instrument.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-14:
- The update has a roadmap of its own, `skill-validation`: roadmap `skill-tooling`, which
  built the tool, is completed, and no pending roadmap covers it.
- Phase 1 of roadmap `session-close` and Phase 3 of ai-ctl's roadmap `review-skill` wait
  for it; it comes before any other roadmap of this repository.
- In scope: the problems V1 to V6 and R1 to R6 of the two notes, and a step that sends a
  fix to the validation when an instrument is suspected.
- The user's rule stands: a `skill-auditor` FAIL whose lines are all fixed or answered is
  no proof. The auditor's verdict is made reproducible instead, and a point of the
  auditor that the evals contradict is fixed in the auditor, not in the skill: the
  application line of the agent's memory `skill-auditor-pass-required`, which says to
  satisfy the auditor by a wording, changes with the design.
- Phase 0 measures the auditor's and the grader's spread on fixed versions before the
  design chooses a criterion.
- The update is proven by replaying the evidence the two skills recorded; the skills
  themselves resume in their own roadmaps.

---

## Deliberately Out Of Scope

- V7, the cost estimates of the eval scripts before any measured run and
  `workspace.py --reuse` taking no run without a word, with `workspace.py --extend`
  taking no `--case`: the hand-over task of roadmap `session-close`'s Phase 2, with
  ai-ctl's proposal `notes/2026-10-13-run-estimate-per-case.md`. They cost money or time
  and push no change to a skill.
- Resuming `close-session` and `reviewing-delivered-code`, and reverting the lines they
  carry because of the validation: roadmap `session-close`, Phase 1, and ai-ctl's
  roadmap `review-skill`, Phase 3. This roadmap hands them the list.
- The proofs other roadmaps write for a skill task: they cite the new criterion once it
  exists; how a roadmap phase declares a task's proof is roadmap `roadmap-execution`'s.
- Trigger evals and description tuning, `triggers.py` and `tuning.py`: no note raises a
  problem with them, and ai-ctl's trigger eval passed its 22 queries.
- Dropped on 2026-10-15 with the validation's weight
  (`docs/decisions/2026-10-15-validation-weight.md`): the sources' place (V4), the replay
  of both skills' recorded evidence, the re-evaluation of `authoring-skills` on all its
  evals.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 7 | 🟢 Done |
| 1 | [Run World](phase-1-run-world.md) | 6 | 🟢 Done |
| 2 | [Judgments](phase-2-judgments.md) | 7 | 🟢 Done |
| 3 | [Release](phase-3-release.md) | 4 | 🟢 Done |

---

## Dependencies

- Roadmap `skill-tooling`, completed: `authoring-skills`, its eval scripts and its agents,
  installed at 0.1.2.
- Waiting for this roadmap: Phase 1 of roadmap `session-close`, and through it roadmap
  `token-usage`'s Phase 2; Phase 3 of ai-ctl's roadmap `review-skill`.

---

## Related Documentation

- [Roadmap skill-tooling](../../completed/skill-tooling/README.md) — the roadmap that built the tool.
- [Skill audit rules, 2026-10-03](../../../decisions/2026-10-03-skill-audit-rules.md) — the rule catalogue `audit.py` checks.
- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — the effort and the spread between runs the evaluation's defaults rest on.
- [Eval runs with agents, 2026-10-13](../../../decisions/2026-10-13-eval-runs-with-agents.md) — how a run of a skill that starts agents is set up and counted.

---

## Metadata

**Roadmap Status:** 🟢 Done
**Location:** `docs/roadmap/completed/skill-validation/`
**Version:** 2.0.0
**Created:** 2026-10-14
**Last Updated:** 2026-10-15

---

## Changelog

### 2.0.0 (2026-10-15)

- Roadmap closed, 24 of 24 tasks over four phases. `summary.md` records where it started,
  what each phase delivered, what holds beyond it — fix an instrument's inputs before
  counting passes, a run read before grading is no evidence, a proof sized to the
  tool's risk — and what it leaves open: V4, the regimes and real-use evidence for
  `lean-workflow`, the auditor's list of points not converging. The folder moves from
  `on-progress/` to `completed/`.

### 1.6.0 (2026-10-15)

- Phase 3 Release closed, 4 of 4 tasks. Delivered: the points of every auditor FAIL on
  `authoring-skills` fixed at their source, mostly by cuts, the shared conventions
  reference among them; `skill-tooling` 0.1.2 released, installed and tagged
  `skill-tooling-v0.1.2`; the hand-over note to `close-session` and ai-ctl's review
  skill; `session-close` unblocked.
- Found: three auditor iterations at the full regime's cap, FAIL and FAIL each, 7, 5 and
  2 points; the verdict reproduces, its list of points does not.
- Moved: nothing; the last phase.

### 1.5.0 (2026-10-15)

- Phase 2 Judgments closed, 7 of 7 tasks. Delivered: each failure classed before any
  change (`grade.py --again`, `classes.json`); guards, checks and measures graded item by
  item; the criterion in rates, iterations of one snapshot pooled; the text of
  `references/evaluate.md`, 97% against 69% on `authoring-skills`' own cases; the
  auditor's request and `medium` effort fixed.
- Found: each pair of auditor passes agrees on its verdict, `close-session` PASS and
  PASS, `authoring-skills` at `5d7228a` FAIL and FAIL, the seven fixtures holding; the
  points still vary between passes.
- Moved: no task; the FAIL's points to Phase 3's first task.

### 1.4.0 (2026-10-15)

- Phase 3's three Regimes tasks move to roadmap `lean-workflow`'s Phase 1, created the
  same day with the user to revise the workflow in depth; Phase 3 becomes Release, 4
  tasks, 27 to 24 in all.

### 1.3.0 (2026-10-15)

- Restructured with the user's approval, from the discussion on the validation's weight
  (`docs/decisions/2026-10-15-validation-weight.md`): Phases 3 and 4 merge into Phase 3
  Regimes And Release — the default and full regimes, the stop rule, the fix from use,
  real-use failures as evidence, the release and the hand-over. Dropped: the sources'
  place, the replay of both skills' evidence, the re-evaluation of `authoring-skills`.
  Five phases to four, 30 tasks to 27. Phase 2's tasks 1, 2 and 5 met on iteration 19,
  its Auditor task's proof cut from 24 passes to four.

### 1.2.0 (2026-10-15)

- Phase 1 Run World closed, 6 of 6 tasks. Delivered: a case's `hooks` key, its domain's
  hooks run in each arm through `--settings`, the skill and its hooks laid out as an
  install lays them; the grader's view with each session's starting context in
  `context/` and whatever it cuts whole in `whole/`; a workflow's later step evaluated
  from a fixture holding a recorded run's state; a run's wall duration and each agent's
  estimated or settled figures; two bullets of `references/evaluate.md`'s The Cases,
  each proven on `authoring-skills`' own evals (+17 and +28 points against the previous
  version).
- Found: two sentences took four wordings and eight iterations, readings before grading
  undone twice by the grading; a defect of the `hooks` key's own code, found by a run;
  the closing audit split, PASS and FAIL on one text and request, four of the FAIL's
  lines past their file's end.
- Moved: no task. The FAIL's points named in the dependencies of Phases 2, 3 and 4, a
  task added to Phase 1 along the way (the grader's view kept whole).


- Phase 0 Framing closed, 7 of 7 tasks. Delivered: the map of V1 to V6 and R1 to R6 to
  the lines that cause them; the list of what `close-session` and
  `reviewing-delivered-code` carry because of the validation; the measures of the
  auditor's and the grader's spread, $2.81; the design, approved then amended with the
  user; the memory `skill-auditor-pass-required` rewritten; the decision record
  `docs/decisions/2026-10-14-skill-validation.md`.
- Found: the auditor's verdict held across 26 passes on a text and request held fixed,
  and the grader changed one verdict in 54; what moved the validation was its inputs —
  the caller's request, the run's world, premises in assertions, the auditor's unset
  effort. No failure stands: each ends in a fix, the skill's by default.
- Moved: no task; Phase 1's first task and two of Phase 2's reworded to the design.
- The roadmap moves from `pending/` to `on-progress/`, Phase 1 following.

### 1.0.0 (2026-10-14)

- Roadmap created with five phases: Phase 0 Framing, which measures the auditor's and the
  grader's spread and settles the design from the two feedback notes; Phase 1 Run World,
  the case's declared world, the grader's view of each session's starting context, a
  workflow's later step, exact figures; Phase 2 Judgments, failures classified, kinds of
  assertion, a criterion in rates, a reproducible auditor; Phase 3 Evidence And Sources,
  real-use failures as evidence, sources out of the runtime text; Phase 4 Validation And
  Release, the recorded evidence of both skills judged again, the domain released, the
  hand-over.
