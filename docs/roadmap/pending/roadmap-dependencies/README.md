# Roadmap: roadmap-dependencies

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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 1  Dependencies               🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/8)
Phase 2  Overview And Hook          🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 3  Fixes                      🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 4  Validation And Release     🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/26)
```

**Current Phase:** —
**Blocked By:** roadmap `superpowers-study`
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

Sub-roadmaps and parent roadmaps left the roadmap skill in 2.0.0: every roadmap of a
repository lives under `root`, side by side, as scriptorium's already do. What replaces
the nesting is a dependency — a roadmap, or one of its phases, waiting for another
roadmap — and the skill does not know about it yet. `Blocked By` is free text that
nothing checks, a phase can open while its roadmap waits, and a closing roadmap does not
tell the roadmaps waiting for it.

This roadmap gives the skill that model, a computed overview of every roadmap, and the
fixes of the defects found along the way.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-01:

- Every roadmap lives under `root`: no sub-roadmaps and no parent roadmaps, as roadmap
  2.0.0 already does, and no `blocked/` state folder — blocking is a relation, often
  partial, and moving a folder breaks the paths that point into it.
- A dependency names the roadmap it waits for by its folder name, which never changes,
  rather than by a link, which breaks when either roadmap changes state.
- A phase or a roadmap waits for a whole roadmap, never for a phase of another one.
- An open roadmap is finished first, unless a new roadmap blocks it: one roadmap
  advances at a time, with the intermediate roadmaps it waits for — Kanban's
  work-in-progress limit, in the terms of `study/methods.md`.
- The skill sets and clears ⏸️ along with `Blocked By`, so that every roadmap's state
  stays current together.
- A roadmap moves to `on-progress/` when its first phase opens.
- Left open for Phase 0: what a phase closure does with the user's uncommitted work.

---

## Deliberately Out Of Scope

- Moving forma-rust's roadmaps under its `root`: done from a session in that repository.
- The study of superpowers, the proof each task declares and the git conventions:
  roadmap `superpowers-study` decides them, and this roadmap applies what concerns the
  roadmap skill.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🔴 Not Started |
| 1 | [Dependencies](phase-1-dependencies.md) | 8 | 🔴 Not Started |
| 2 | [Overview And Hook](phase-2-overview-and-hook.md) | 4 | 🔴 Not Started |
| 3 | [Fixes](phase-3-fixes.md) | 5 | 🔴 Not Started |
| 4 | [Validation And Release](phase-4-validation-and-release.md) | 4 | 🔴 Not Started |

---

## Dependencies

- Roadmap `superpowers-study`: its decisions on how a phase is executed, on the proof each
  task declares and on git shape Phases 0 and 1.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/roadmap-dependencies/`
**Version:** 1.0.0
**Created:** 2026-10-01
**Last Updated:** 2026-10-01

---

## Changelog

### 1.0.0 (2026-10-01)

- Roadmap created with five phases: Phase 0 Framing, Phase 1 Dependencies, Phase 2
  Overview And Hook, Phase 3 Fixes, Phase 4 Validation And Release. It waits for roadmap
  `superpowers-study`.
