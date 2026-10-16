# Roadmap: lean-workflow

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
Phase 0  Measure And Design         🟢 ████████████████████ 100%  (4/4)
Phase 1  Authoring Skills           🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/6)
Phase 2  Roadmap And Conventions    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/7)
Phase 3  Use And Measure            🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
TOTAL                                  ████░░░░░░░░░░░░░░░░  19%  (4/21)
```

**Current Phase:** —
**Blocked By:** roadmap `session-close`, finished first: its Phase 2's tasks 4 and 7
**Next Milestone:** Phase 1 — Authoring Skills

---

## Why This Roadmap Exists

The setup's tools give every piece of work the same proof, the heaviest, whatever its
risk, and each problem met so far was answered with one more rule or tool. Measured on
2026-10-15 (`docs/decisions/2026-10-15-validation-weight.md`): `close-session` was useful
at its second iteration and took nine more; `skill-validation`, meant to fix the
validation, made its references heavier; the working sessions make two thirds or more of
the cost; the tool reviews' most recurrent finding waits behind a roadmap's end; the
reports are long and hard to read.

This roadmap revises in depth `authoring-skills`, the roadmap skill, `CLAUDE.md`'s
conventions, the agent's memories and the review domain, so that a tool goes from the
request to real use in about a day and improves through its use, without losing what the
current tools catch.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-15:
- A roadmap of its own, after `skill-validation` and `session-close`, which finish
  first under the default regime; `token-usage` stays waiting.
- Remove before adding: each phase removes more text and rules than it adds.
- Judged on figures measured from the transcripts in Phase 0, before any change.
- No regression: the existing evals of the roadmap skill and `authoring-skills` are
  guards, not targets; the rest is proven in real use.
- The waiting roadmaps and `token-usage`'s remaining tasks wait for Phase 0, which
  decides for each: keep, merge into this roadmap, or cut.
- Short records, this roadmap's own included.

---

## Deliberately Out Of Scope

- The domain `session`: roadmap `session-close`.
- New tools, unless Phase 0's design shows one replaces more than it adds.
- The other repositories' own tools, such as ai-ctl's review skill: they follow the
  released workflow.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Measure And Design](phase-0-measure-and-design.md) | 4 | 🟢 Done |
| 1 | [Authoring Skills](phase-1-authoring-skills.md) | 6 | 🔴 Not Started |
| 2 | [Roadmap And Conventions](phase-2-roadmap-and-conventions.md) | 7 | 🔴 Not Started |
| 3 | [Use And Measure](phase-3-use-and-measure.md) | 4 | 🔴 Not Started |

---

## Dependencies

- Roadmap `skill-validation`: its release of `skill-tooling`; its three Regimes tasks
  moved to Phase 1.
- Roadmap `session-close`: finished, its use a first measure for Phase 0.

---

## Related Documentation

- [Lean workflow, 2026-10-16](../../../decisions/2026-10-16-lean-workflow.md) — Phase 0's decision, its figures and targets.
- [Validation weight, 2026-10-15](../../../decisions/2026-10-15-validation-weight.md) — the figures and regimes this roadmap starts from.
- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — how a session's cost is counted.

---

## Metadata

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/pending/lean-workflow/`
**Version:** 1.2.0
**Created:** 2026-10-15
**Last Updated:** 2026-10-16

---

## Changelog

### 1.2.0 (2026-10-16)

- Phase 0 closed: the workflow measured from the transcripts, the waiting roadmaps
  decided, the design approved with its seven targets and recorded in
  `docs/decisions/2026-10-16-lean-workflow.md`. The user kept `roadmap-auditor` on two
  points of judgment and approved the README's Changelog cut, both for Phase 2. Phase 3's
  Judge task also judges the auditor from its reviews. Phase 1 waits for `session-close`.

### 1.1.0 (2026-10-16)

- Phase 0's task 3 decided the waiting roadmaps with the user: `roadmap-dependencies`,
  `roadmap-execution`, `working-method` and `session-review` cut, `git-domain` kept after
  this roadmap, `token-usage` closed. Phase 2 gains three tasks — the roadmap skill's
  fixes from `roadmap-dependencies`, two measure fixes from `token-usage`, the measure's
  scripts brought in — and its release names review 0.3.0 and roadmap 2.0.4; Phase 3's
  first task proposes a skill of `working-method`.
- The Roadmap Status set to 🟡, missed when Phase 0 opened.

### 1.0.2 (2026-10-15)

- Phase 1 gains a From Use task, handed over by roadmap `session-close`'s Phase 2: the
  eval scripts' cost announced as a limit without a measured session, an estimate per
  case and configuration with its ceiling from ai-ctl's proposal `notes/2026-10-13-run-estimate-per-case.md`, and
  `workspace.py`'s `--reuse` and `--extend` fixed; Phase 0's design may cut it.

### 1.0.1 (2026-10-15)

- Phase 1's first Regimes task: the default regime's `audit.py` clean means no error and
  no warning, a warning the skill could only drop by bending fixed in `audit.py`, as T1
  on `legacy` was from ai-ctl's feedback, in `skill-tooling` 0.1.3.

### 1.0.0 (2026-10-15)

- Roadmap created with four phases: Phase 0 Measure And Design, Phase 1 Authoring
  Skills, Phase 2 Roadmap And Conventions, Phase 3 Use And Measure. Phase 1 receives the
  three Regimes tasks of roadmap `skill-validation`'s Phase 3.
