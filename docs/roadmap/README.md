# Roadmaps

Temporary: written by hand on 2026-10-10, until `scripts/roadmaps.py` from Phase 2 of
roadmap `roadmap-dependencies` generates this file. Each roadmap's README remains the
source of its state and of what it waits for.

---

## In Progress

| Roadmap | What it does | Phase |
|---|---|---|
| `token-usage` | What this setup's tools and a set of sessions cost, read so as to conclude what to change: the return on each tool, and a review of several sessions run by hand | Phase 0, Framing |

---

## Up Next

In order of priority.

| # | Roadmap | What it does | Waits for |
|---|---|---|---|
| 1 | `roadmap-dependencies` | Dependencies between roadmaps, enforced by the skill, and this overview generated | — |
| 2 | `roadmap-execution` | Phase execution in the roadmap skill: a design per phase, a proof per task, the `[git]` table | `roadmap-dependencies` |
| 3 | `working-method` | The `shaping-work` and `finding-root-causes` skills, from superpowers' design and debugging | `roadmap-execution` |
| 4 | `git-domain` | Branch per roadmap and worktrees, built once a repository asks for them | `roadmap-execution`, and a repository asking |
| 5 | `session-review` | scriptorium's `session-review` made a standard tool, with which any repository reviews the tools it builds for itself | Phase 1: `token-usage`'s Phase 1 |

---

## Completed

| Roadmap | What it did | Completed |
|---|---|---|
| `superpowers-study` | What to keep of the superpowers plugin, and where each kept part goes | 2026-10-03 |
| `skill-tooling` | One tool that creates, audits and evaluates skills, replacing writing-skills and skill-creator | 2026-10-11 |
