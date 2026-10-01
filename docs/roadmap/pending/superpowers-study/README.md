# Roadmap: superpowers-study

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
Phase 1  Design And Planning        🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Proof                      🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 3  Git                        🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/3)
Phase 4  Decisions                  🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/7)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/25)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

The superpowers plugin (6.4.1) is the user's working method in most projects —
brainstorming, plans, execution through subagents, test-driven development, branch
finishing — and it costs about 1,400 tokens per session before any use, runs a
SessionStart hook, and brings its own conventions (`docs/superpowers/`, then
`.superpowers/` in this repository). The user wants it off for good, keeping every part
that serves, rewritten for this setup: one tool per job, conventions read from
`.agent-conventions.toml`, the agent addressed rather than a model, roadmaps as the
frame of long work.

This roadmap studies each part — how it works, what it brings, what it costs — and
decides where each kept capability goes, before anything is built. It also answers three
questions the user raised on 2026-10-01, each of which the plugin already touches:
whether a task should choose its engineering method (`study/methods.md`), against
`test-driven-development` and `verification-before-completion`; how git work is
organized, against `using-git-worktrees` and `finishing-a-development-branch`; and how a
plan is executed, against `writing-plans`, `executing-plans` and
`subagent-driven-development`.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-01:

- The goal is to turn the plugin off everywhere, not to vendor it: each capability is
  kept, improved or dropped on its content, and a kept one is rewritten for this setup,
  with superpowers' MIT notice wherever its text is adapted.
- The study comes first: roadmap `skill-tooling`, from its Phase 2, and roadmap
  `roadmap-dependencies` wait for it, because its decisions shape how a phase is
  planned, executed, proven and committed.
- `writing-skills` is out: skill-tooling's Phase 0 already ruled on it, row by row.
- The usage recount planned for 2026-10-18 informs Phase 4 when it is available, without
  blocking it, and leaves out this repository's sessions since 2026-09-28, where the
  plugin is off.
- `.superpowers/` is not kept: the study decides where specs and plans go instead.

---

## Deliberately Out Of Scope

- Building the replacements: the follow-up roadmaps created in Phase 4.
- `writing-skills` and the skill-creator plugin: roadmap `skill-tooling` replaces them.
- The other plugins copied under `study/`.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🔴 Not Started |
| 1 | [Design And Planning](phase-1-design-and-planning.md) | 5 | 🔴 Not Started |
| 2 | [Proof](phase-2-proof.md) | 5 | 🔴 Not Started |
| 3 | [Git](phase-3-git.md) | 3 | 🔴 Not Started |
| 4 | [Decisions](phase-4-decisions.md) | 7 | 🔴 Not Started |

---

## Dependencies

- The plugin's copy under `study/superpowers/6.4.1/`, which `.gitignore` keeps out of the
  repository, and the installed plugin.
- The session transcripts under `~/.claude/projects/`, for the recount.

---

## Related Documentation

- [Superpowers plugin audit, 2026-09-18](../../../decisions/2026-09-18-superpowers-plugin-audit.md) — the usage baseline and the decision to postpone vendoring.
- [Skill tooling, 2026-09-28](../../../decisions/2026-09-28-skill-tooling.md) — the matrix format, and the verdicts on `writing-skills`.
- [superpowers](https://github.com/obra/superpowers) — version 6.4.1, MIT.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/superpowers-study/`
**Version:** 1.0.0
**Created:** 2026-10-01
**Last Updated:** 2026-10-01

---

## Changelog

### 1.0.0 (2026-10-01)

- Roadmap created with five phases: Phase 0 Framing, Phase 1 Design And Planning, Phase
  2 Proof, Phase 3 Git, Phase 4 Decisions. Roadmaps `skill-tooling` and
  `roadmap-dependencies` wait for it.
