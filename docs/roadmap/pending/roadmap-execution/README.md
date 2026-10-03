# Roadmap: roadmap-execution

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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/6)
Phase 1  Proof And Template         🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Git Table                  🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 3  Execute Phase              🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/6)
Phase 4  Validation And Release     🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/25)
```

**Current Phase:** —
**Blocked By:** roadmap `roadmap-dependencies`
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

Roadmap `superpowers-study` decided how this setup designs, executes, proves, reviews
and commits the work of a phase, keeping 142 of the 220 rows of its capability matrix of
the superpowers plugin. Most of them go to the roadmap skill, which opens and closes
phases but executes none: a task declares no proof, nothing reviews a phase's diff, and
commits follow no convention a tool reads.

This roadmap gives the roadmap skill its execution operation, `execute-phase`; a phase's
`## Design` section and each task's `Proof:` line; the proof reference, shared with
`shaping-work`; the `[git]` table; and two agents, `phase-reviewer` and
`task-implementer`.

---

## Decisions Taken At Opening

Taken with the user from 2026-10-01 to 2026-10-03, in roadmap `superpowers-study`:

- `execute-phase` runs one phase in the main conversation, task by task in order, with
  no pause but its four stops; closing a phase and opening the next ends the turn.
- Each task declares its proof — `test`, `eval`, `probe`, `check` or `review`, naming
  its object — on an indented `Proof:` line, proposed by the agent writing the phase and
  approved by the user with it. `execute-phase` runs it and records it in the Work Log
  before ticking the task; no default key, no `task-done` script.
- The five kinds are defined once, in `shared/proof/proof.md`, copied into the roadmap
  skill and into `shaping-work`.
- A phase's design lives in its `## Design` section, approved when the phase opens; the
  plan is its tasks, and the words "spec" and "plan" leave the tools.
- `phase-reviewer` reviews a phase's diff before its closure only when the phase changes
  code or scripts; a task goes to `task-implementer` only when the phase says so; one fix
  round, then back to the user. Neither agent holds the Agent tool, and the implementer
  holds no Skill tool.
- The `[git]` table holds `branch`, `commit` and `message`; this repository and
  scriptorium take `none`, `task` and their own format; `branch = "roadmap"` is roadmap
  `git-domain`'s.

---

## Deliberately Out Of Scope

- `shaping-work` and `finding-root-causes`, and turning the superpowers plugin off:
  roadmap `working-method`.
- `branch = "roadmap"`, worktrees and the git domain: roadmap `git-domain`.
- The dependency model between roadmaps: roadmap `roadmap-dependencies`.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 6 | 🔴 Not Started |
| 1 | [Proof And Template](phase-1-proof-and-template.md) | 5 | 🔴 Not Started |
| 2 | [Git Table](phase-2-git-table.md) | 4 | 🔴 Not Started |
| 3 | [Execute Phase](phase-3-execute-phase.md) | 6 | 🔴 Not Started |
| 4 | [Validation And Release](phase-4-validation-and-release.md) | 4 | 🔴 Not Started |

---

## Dependencies

- Roadmap `roadmap-dependencies`: both change the roadmap skill, and this one builds on
  its release.

---

## Related Documentation

- [Superpowers study, 2026-10-01](../../../decisions/2026-10-01-superpowers-study.md) — the verdicts, the target architecture and the decisions this roadmap applies.
- [superpowers](https://github.com/obra/superpowers) — version 6.4.1, MIT.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/roadmap-execution/`
**Version:** 1.0.0
**Created:** 2026-10-03
**Last Updated:** 2026-10-03

---

## Changelog

### 1.0.0 (2026-10-03)

- Roadmap created by Phase 4 of roadmap `superpowers-study`, with five phases: Phase 0
  Framing, Phase 1 Proof And Template, Phase 2 Git Table, Phase 3 Execute Phase, Phase 4
  Validation And Release. It waits for roadmap `roadmap-dependencies`.
