# Roadmap: working-method

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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 1  Shaping Work               🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/3)
Phase 2  Finding Root Causes        🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/3)
Phase 3  Release And Turn-Off       🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/15)
```

**Current Phase:** —
**Blocked By:** roadmaps `skill-tooling` and `roadmap-execution`
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

The superpowers plugin carried design and debugging into the user's work in every
project: `brainstorming` was its most called skill, 13 of its 38 calls from 2026-09-04 to
2026-10-03, and `systematic-debugging` found the cause of a timeout by measure before any
fix. Roadmap `superpowers-study` kept their useful rows, and turns the plugin off once
every kept row has its place in this setup.

This roadmap writes the two skills that receive them, `shaping-work` and
`finding-root-causes`, in a domain of their own, then turns the plugin off by the plan of
the study's decision record.

---

## Decisions Taken At Opening

Taken with the user from 2026-10-01 to 2026-10-03, in roadmap `superpowers-study`:

- One domain, `working-method`, holds both skills.
- `shaping-work` takes the kept rows of `brainstorming`. Its exit follows the path: a
  recommendation for a spike; for bounded work, a design approved in the chat, its proof
  stated, then the implementation; for architectural work, a roadmap or the `## Design`
  of the phase under way.
- `finding-root-causes` takes the kept rows of `systematic-debugging`: no fix before its
  root cause, a failing test before the fix, a fourth fix waiting for the user.
- Neither trigger overlaps the other or the roadmap skill, which trigger evals check,
  written from the 38 prompts saved on 2026-10-03.
- Both skills are written and evaluated with roadmap `skill-tooling`'s tools, with
  superpowers' MIT notice wherever its text is adapted.
- The plugin goes off when the plan's go-ahead conditions hold, with the user's
  go-ahead.

---

## Deliberately Out Of Scope

- The roadmap skill's changes: roadmap `roadmap-execution`.
- The git domain: roadmap `git-domain`, which the turn-off does not wait for.
- A SessionStart line naming the two skills, unless their trigger evals fail.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 4 | 🔴 Not Started |
| 1 | [Shaping Work](phase-1-shaping-work.md) | 3 | 🔴 Not Started |
| 2 | [Finding Root Causes](phase-2-finding-root-causes.md) | 3 | 🔴 Not Started |
| 3 | [Release And Turn-Off](phase-3-release-and-turn-off.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `skill-tooling`: `authoring-skills` and its eval tooling.
- Roadmap `roadmap-execution`: the proof reference and the `## Design` section the two
  skills hand over to.
- `study/superpowers-recount/call-prompts.md`, which `.gitignore` keeps out of the
  repository: the prompts of the trigger evals.

---

## Related Documentation

- [Superpowers study, 2026-10-01](../../../decisions/2026-10-01-superpowers-study.md) — the verdicts, the target architecture and the plan that turns the plugin off.
- [superpowers](https://github.com/obra/superpowers) — version 6.4.1, MIT.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/working-method/`
**Version:** 1.0.0
**Created:** 2026-10-03
**Last Updated:** 2026-10-03

---

## Changelog

### 1.0.0 (2026-10-03)

- Roadmap created by Phase 4 of roadmap `superpowers-study`, with four phases: Phase 0
  Framing, Phase 1 Shaping Work, Phase 2 Finding Root Causes, Phase 3 Release And
  Turn-Off. It waits for roadmaps `skill-tooling` and `roadmap-execution`.
