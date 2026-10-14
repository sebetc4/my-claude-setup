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
Phase 0  Framing                    🟡 ███░░░░░░░░░░░░░░░░░  14%  (1/7)
Phase 1  Run World                  🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Judgments                  🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/7)
Phase 3  Evidence And Sources       🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 4  Validation And Release     🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/6)
TOTAL                                  █░░░░░░░░░░░░░░░░░░░   3%  (1/29)
```

**Current Phase:** Phase 0 — Framing
**Blocked By:** —
**Next Milestone:** Phase 0 — Framing

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

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 7 | 🟡 In Progress |
| 1 | [Run World](phase-1-run-world.md) | 5 | 🔴 Not Started |
| 2 | [Judgments](phase-2-judgments.md) | 7 | 🔴 Not Started |
| 3 | [Evidence And Sources](phase-3-evidence-and-sources.md) | 4 | 🔴 Not Started |
| 4 | [Validation And Release](phase-4-validation-and-release.md) | 6 | 🔴 Not Started |

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

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/pending/skill-validation/`
**Version:** 1.0.0
**Created:** 2026-10-14
**Last Updated:** 2026-10-14

---

## Changelog

### 1.0.0 (2026-10-14)

- Roadmap created with five phases: Phase 0 Framing, which measures the auditor's and the
  grader's spread and settles the design from the two feedback notes; Phase 1 Run World,
  the case's declared world, the grader's view of each session's starting context, a
  workflow's later step, exact figures; Phase 2 Judgments, failures classified, kinds of
  assertion, a criterion in rates, a reproducible auditor; Phase 3 Evidence And Sources,
  real-use failures as evidence, sources out of the runtime text; Phase 4 Validation And
  Release, the recorded evidence of both skills judged again, the domain released, the
  hand-over.
