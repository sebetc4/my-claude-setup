# Roadmap: skill-tooling

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
Phase 0  Framing                    🟢 ████████████████████ 100%  (18/18)
Phase 1  Agent Conventions          🟢 ████████████████████ 100%  (19/19)
Phase 2  Static Audit               🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/13)
Phase 3  Writing Method             🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/12)
Phase 4  Evaluation Tooling         🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/12)
Phase 5  Switch-Over                🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/11)
TOTAL                                  █████████░░░░░░░░░░░  44%  (37/85)
```

**Current Phase:** —
**Blocked By:** roadmap `superpowers-study`
**Next Milestone:** Phase 2 — Static Audit

---

## Why This Roadmap Exists

Skills are written and checked today with two external tools that overlap and contradict
each other. `superpowers:writing-skills` (superpowers 6.4.1) brings a method — watch an
agent fail before writing, match the form of the guidance to the failure — and no
tooling. The skill-creator plugin brings tooling — evals with and without the skill,
grading, benchmark, review viewer, description tuning — and thinner writing guidance.
Neither audits an existing skill, neither follows its own rules, and both drift from the
official Claude Code documentation on descriptions, frontmatter fields and size limits.
The only automated audit, this repository's `tests/skills.py`, runs only on `domains/`.

This roadmap replaces both with one tool of our own — a skill, agents and a hook — that
creates, edits, audits and evaluates skills in any repository, builds on the official
documentation and the best practices without being capped by them, and adapts to each
repository's conventions, declared in a `.agent-conventions.toml` file at its root.

---

## Decisions Taken At Opening

- One tool replaces `superpowers:writing-skills` and the skill-creator plugin: a synthesis
  rewritten from both, not a copy.
- The whole repository becomes open source under Apache 2.0. Code adapted from
  skill-creator (Apache 2.0) or superpowers (MIT) keeps its license notice.
- Skills can be created in any repository, and each takes the format of the repository it
  lives in.
- A repository's conventions live in `.agent-conventions.toml` at its root, in TOML read
  with the standard library's `tomllib`: shared keys at the top, one table per tool. There
  are no default values, and the lookup never goes above the repository root; the root of
  a personal skill is `~/.claude`. The file is added to `.gitignore` when it is created.
- Contracts leave `CLAUDE.md`: a tool reads its table only when it runs, so sessions no
  longer carry them. The roadmap contract moves first.
- When the file is missing or malformed, the agent in conversation proposes values
  detected in the repository, asks, and writes only after the user agrees; it never
  rewrites silently. Hooks, subagents and `claude -p` runs never guess: they stay silent,
  or stop and name what is missing.
- The file is untrusted data: keys and types are validated, and `checks` commands run
  through the normal permission flow, never pre-approved.
- The official documentation and the Agent Skills standard inform every rule without
  capping any: a tool may go past a documented limit when its evaluations show it does
  better. Conventions apply only where the file declares them.
- `tests/skills.py` becomes a client of the domain's audit, so the rules have one source.
- Output evals run in subagents; trigger evals run in fresh `claude -p` sessions, the only
  way to see whether Claude picks a skill from its description.
- The skill-creator review viewer is kept.
- Once the new tool is in place, the roadmap evals stop depending on the skill-creator
  plugin, and `superpowers:writing-skills` and the plugin are turned off, which revises
  the decision of 2026-09-18.

---

## Deliberately Out Of Scope

- The `[docs]` and `[git]` tables and their tools: the file is designed to hold them, but
  they come with their own domains.
- The other superpowers skills: whether to vendor them is decided at the recount of
  2026-10-18.
- The `claude plugin eval` format.
- `.skill` packaging and the instructions specific to claude.ai and Cowork: syncing skills
  from claude.ai is turned off.
- Installing for agents other than Claude Code: every tool is written for the agent,
  never for Claude, but installs into `~/.claude` and is tested with Claude Code only.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 18 | 🟢 Done |
| 1 | [Agent Conventions](phase-1-agent-conventions.md) | 19 | 🟢 Done |
| 2 | [Static Audit](phase-2-static-audit.md) | 13 | 🔴 Not Started |
| 3 | [Writing Method](phase-3-writing-method.md) | 12 | 🔴 Not Started |
| 4 | [Evaluation Tooling](phase-4-evaluation-tooling.md) | 12 | 🔴 Not Started |
| 5 | [Switch-Over](phase-5-switch-over.md) | 11 | 🔴 Not Started |

---

## Dependencies

- Python 3.11 or later wherever the tools run, for `tomllib`.
- The skill-creator plugin's files stay in the plugin cache until Phase 5, although the
  plugin is disabled since 2026-09-28: `domains/roadmap/skills/roadmap/evals/grade.py`
  uses its benchmark script and its review viewer.

---

## Related Documentation

- [Superpowers plugin audit, 2026-09-18](../../../decisions/2026-09-18-superpowers-plugin-audit.md) — the decision this roadmap revises.
- [Extend Claude with skills](https://code.claude.com/docs/en/skills) — the official Claude Code documentation.
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Agent Skills specification](https://agentskills.io/specification)
- [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) — Apache 2.0.
- [superpowers](https://github.com/obra/superpowers) — `skills/writing-skills`, version 6.4.1, MIT.

---

## Metadata

**Roadmap Status:** ⏸️ Blocked
**Location:** `docs/roadmap/on-progress/skill-tooling/`
**Version:** 1.2.1
**Created:** 2026-09-28
**Last Updated:** 2026-10-01

---

## Changelog

### 1.2.1 (2026-10-01)

- Paused before Phase 2, at the user's request: the roadmap waits for roadmap
  `superpowers-study`, whose decisions on design, plans, execution, proof and git shape
  the phases left. Phase 2 had been opened by Phase 1's closure, with nothing done and
  nothing committed; that opening was undone, so that Phase 2 opens later on a current
  start commit.

### 1.2.0 (2026-10-01)

- Phase 1 Agent Conventions closed. Delivered `.agent-conventions.toml`: its reader and
  writer in `shared/conventions/`, copied into skills by `tools/shared.py`, the procedure
  that fills or fixes the file, and roadmap 2.0.0, which reads its contract there — skill,
  hook and evals — installed. This repository, scriptorium and forma-rust carry the file,
  and their `CLAUDE.md` no longer carries a contract.
- Found: the session hook put a Work Log excerpt into every session, now one conditional
  line; forma-rust's workspaces keep legitimate `Cargo.lock` files, so `residue` entries
  became `.gitignore` patterns; in a subagent, Claude Code's Write refuses files named
  like reports.
- Changed: at the user's request, sub-roadmaps and parent roadmaps are gone and every
  roadmap lives under `root`; the dependency mechanics go to a separate roadmap for the
  roadmap skill. Phase 1 grew to 19 tasks; Phases 2 and 4 gained checks and a constraint
  on the eval workspace and on report-named files.
- Two acceptance criteria stay open: the final text was not run after that removal, and
  the fill-or-fix conversation has no eval.

### 1.1.0 (2026-09-28)

- Phase 0 Framing closed. Delivered `docs/decisions/2026-09-28-skill-tooling.md` — the
  capability matrix of both sources, the description, tone, testing, size and script
  rules, the open questions answered, the names (`authoring-skills`), a flowchart
  measurement — plus the Apache 2.0 `LICENSE`, `docs/claude-code-coupling.md` and the
  Principles section of `CLAUDE.md`.
- Found: `allowed-tools` grants nothing in headless runs, `skillOverrides` cannot hide a
  plugin skill, and two defects of the roadmap skill — the opening leaves the progress
  block stale, and a first phase under `pending/` is never resumed — now Phase 1 tasks.
- Moved: the turn-off of `superpowers:writing-skills` and the skill-creator plugin came
  forward from Phase 5 and is done, so the "turned off once the new tool is in place" of
  the opening decisions happened at the start, and Phase 5's Objective holds that part as
  met. superpowers is off in this repository until Phase 5, which gained the task that
  turns it back on. Three statements of this README follow the user's principles, as
  approved; Phase 0 grew to 18 tasks and Phase 1 to 16.
- The folder moves from `pending/` to `on-progress/`: Phase 1 opens next.

### 1.0.0 (2026-09-28)

- Roadmap created with six phases: Phase 0 Framing, Phase 1 Agent Conventions, Phase 2
  Static Audit, Phase 3 Writing Method, Phase 4 Evaluation Tooling, Phase 5 Switch-Over.
