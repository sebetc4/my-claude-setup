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
Phase 0  Measure And Design         🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 1  Authoring Skills           🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Roadmap And Conventions    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 3  Use And Measure            🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/17)
```

**Current Phase:** —
**Blocked By:** roadmaps `skill-validation` and `session-close`, finished first
**Next Milestone:** Phase 0 — Measure And Design

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
| 0 | [Measure And Design](phase-0-measure-and-design.md) | 4 | 🔴 Not Started |
| 1 | [Authoring Skills](phase-1-authoring-skills.md) | 5 | 🔴 Not Started |
| 2 | [Roadmap And Conventions](phase-2-roadmap-and-conventions.md) | 4 | 🔴 Not Started |
| 3 | [Use And Measure](phase-3-use-and-measure.md) | 4 | 🔴 Not Started |

---

## Dependencies

- Roadmap `skill-validation`: its release of `skill-tooling`; its three Regimes tasks
  moved to Phase 1.
- Roadmap `session-close`: finished, its use a first measure for Phase 0.

---

## Related Documentation

- [Validation weight, 2026-10-15](../../../decisions/2026-10-15-validation-weight.md) — the figures and regimes this roadmap starts from.
- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — how a session's cost is counted.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/lean-workflow/`
**Version:** 1.0.0
**Created:** 2026-10-15
**Last Updated:** 2026-10-15

---

## Changelog

### 1.0.0 (2026-10-15)

- Roadmap created with four phases: Phase 0 Measure And Design, Phase 1 Authoring
  Skills, Phase 2 Roadmap And Conventions, Phase 3 Use And Measure. Phase 1 receives the
  three Regimes tasks of roadmap `skill-validation`'s Phase 3.
