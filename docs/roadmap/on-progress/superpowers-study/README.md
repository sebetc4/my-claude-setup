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
Phase 0  Framing                    🟢 ████████████████████ 100%  (5/5)
Phase 1  Design And Planning        🟢 ████████████████████ 100%  (5/5)
Phase 2  Proof                      🟢 ████████████████████ 100%  (5/5)
Phase 3  Git                        🟢 ████████████████████ 100%  (3/3)
Phase 4  Decisions                  🟢 ████████████████████ 100%  (8/8)
TOTAL                                  ████████████████████ 100%  (26/26)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** —

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
| 0 | [Framing](phase-0-framing.md) | 5 | 🟢 Done |
| 1 | [Design And Planning](phase-1-design-and-planning.md) | 5 | 🟢 Done |
| 2 | [Proof](phase-2-proof.md) | 5 | 🟢 Done |
| 3 | [Git](phase-3-git.md) | 3 | 🟢 Done |
| 4 | [Decisions](phase-4-decisions.md) | 8 | 🟢 Done |

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

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/on-progress/superpowers-study/`
**Version:** 1.5.0
**Created:** 2026-10-01
**Last Updated:** 2026-10-03

---

## Changelog

### 1.5.0 (2026-10-03)

- Phase 4 Decisions closed. The decision record
  `docs/decisions/2026-10-01-superpowers-study.md` is final: 220 rows, 57 kept, 85
  improved, 78 dropped, none open; a target architecture placing every kept row; the
  plan that turns the plugin off with its go-ahead conditions; when to revisit. Decided
  with the user: the names `execute-phase`, `phase-reviewer`, `task-implementer` and
  `finding-root-causes`, the domains `working-method` and `git`, and three follow-up
  roadmaps created in `pending/` — `roadmap-execution`, `working-method`, `git-domain`.
- Found: the recount, run up to the day over 2026-09-19 to 2026-10-03, has the plugin
  called in 4 of 36 working conversations, 11 % against the baseline's 34 %, while 92 %
  called a skill; `using-superpowers`, `diagnosing-superpowers` and the hook are dropped
  whole. skill-creator is still on in scriptorium's local settings.
- Changed: roadmaps `skill-tooling` and `roadmap-dependencies` are no longer blocked;
  with the user's approval, skill-tooling's Phase 5 no longer turns superpowers back on
  here, and roadmap-dependencies leaves the study's decisions to `roadmap-execution`.
  This repository's `CLAUDE.md` scopes test-first to code and scripts.

### 1.4.0 (2026-10-02)

- Phase 3 Git closed. The draft record rules on `using-git-worktrees` and
  `finishing-a-development-branch`, 26 rows with their evidence, settles WP4, EP9, RC10
  and RQ18, and holds the `[git]` table decided with the user: `branch`, `none` or
  `roadmap`, `commit`, `task` or `closure`, and `message`, the format's only written
  source; this repository and scriptorium take `none` and `task`. Pull requests and
  review-thread replies are dropped for now, a push waits for the user's request, and
  worktrees are the harness's.
- Found: every one of the five finishes ended in the base moved forward, never in a pull
  request, and the menu was bypassed or reworded four times out of five; no worktree
  ever served as a workspace; branches lived only under the plugin's executors, merged
  the same day.
- Changed: Phase 4 gained a constraint carrying Phase 3's decisions and a git domain to
  name.

### 1.3.0 (2026-10-02)

- Phase 2 Proof closed. The draft record rules on `test-driven-development`,
  `verification-before-completion`, `systematic-debugging`, `requesting-code-review` and
  `receiving-code-review`, 79 rows with their evidence, and holds the decisions taken with
  the user: each task declares its proof — `test`, `eval`, `probe`, `check` or `review` —
  naming its object, on an indented `Proof:` line that the execution operation runs and
  records before ticking the task; no default key in `.agent-conventions.toml` and no
  `task-done` script; no method chosen from a catalogue; debugging as a skill of its own.
- Found: 288 micro-test sessions on Claude Haiku 4.5 and Claude Sonnet 5.5 showed a plain
  test-first instruction working for code and harmful elsewhere, where a declared proof
  brought each artifact its method, provided it names what it runs. Every final review
  of the plugin's executors that ran to its end found something to fix.
- Changed: Phase 3 gained a constraint, row RC10; Phase 4 a constraint carrying Phase 2's
  decisions, and a task that scopes this repository's `CLAUDE.md` line "TDD (failing test
  first)".

### 1.2.0 (2026-10-02)

- Phase 1 Design And Planning closed. The draft record rules on `brainstorming`,
  `writing-plans`, `executing-plans`, `subagent-driven-development` and
  `dispatching-parallel-agents`, 90 rows with their evidence, and holds the decisions taken
  with the user: a design skill of this setup's own, `shaping-work`; a phase's design in a
  `## Design` section citing a decision record when needed; the plan as the phase's tasks;
  an operation of the roadmap skill that executes one phase inline and never chains the
  next, with a conditional reviewer agent and light delegation written into the roadmap.
- Found: resumed sessions copy their history into new transcripts, so the baseline of
  2026-09-18 counted copies. Corrected: 29 distinct calls, not 51, in 32 working
  conversations, not the 41 sessions entry 1.1.0 gave; 34 % of them, not 41 %, called
  superpowers.
- Changed: Phases 2, 3 and 4 each gained a constraint carrying Phase 1's decisions.

### 1.1.0 (2026-10-01)

- Phase 0 Framing closed. Delivered the draft record
  `docs/decisions/2026-10-01-superpowers-study.md`: the inventory of superpowers 6.4.1 —
  fifteen skills, the prompts, the hook, the scripts, the tests — with the hand-overs
  between skills, the conventions the plugin imposes and its ties to Claude Code; the
  matrix format Phases 1 to 3 rule in; and the recount method.
- Found: the 2026-09-18 baseline measured 6.3.0, and its 479 sessions and 8 % counted
  eval runs; by working sessions, the baseline is 41 sessions, 41 % of them calling
  superpowers. Transcripts go after 30 days: the user chose to run the roadmap ahead of
  that rather than raise `cleanupPeriodDays`.
- Changed: Phase 1 gained a constraint, to read before about 2026-10-10 the plugin
  sessions its verdicts cite, and Phase 4 another, to recount by 2026-10-18.
- The folder moves from `pending/` to `on-progress/`: Phase 1 opens next.

### 1.0.0 (2026-10-01)

- Roadmap created with five phases: Phase 0 Framing, Phase 1 Design And Planning, Phase
  2 Proof, Phase 3 Git, Phase 4 Decisions. Roadmaps `skill-tooling` and
  `roadmap-dependencies` wait for it.
