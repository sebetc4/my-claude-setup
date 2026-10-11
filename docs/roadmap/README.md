# Roadmaps

Temporary: written by hand on 2026-10-10, until `scripts/roadmaps.py` from Phase 2 of
roadmap `roadmap-dependencies` generates this file. Each roadmap's README remains the
source of its state and of what it waits for.

---

## In Progress

None.

---

## Up Next

In order of priority.

| # | Roadmap | What it does | Waits for |
|---|---|---|---|
| 1 | `token-usage` | The dollar cost of tools, sessions, phases and roadmaps, kept beyond the transcripts | `skill-tooling` |
| 2 | `roadmap-dependencies` | Dependencies between roadmaps, enforced by the skill, and this overview generated | — |
| 3 | `roadmap-execution` | Phase execution in the roadmap skill: a design per phase, a proof per task, the `[git]` table | `roadmap-dependencies` |
| 4 | `working-method` | The `shaping-work` and `finding-root-causes` skills, from superpowers' design and debugging | `skill-tooling`, `roadmap-execution` |
| 5 | `git-domain` | Branch per roadmap and worktrees, built once a repository asks for them | `roadmap-execution`, and a repository asking |

---

## Completed

| Roadmap | What it did | Completed |
|---|---|---|
| `superpowers-study` | What to keep of the superpowers plugin, and where each kept part goes | 2026-10-03 |
| `skill-tooling` | One tool that creates, audits and evaluates skills, replacing writing-skills and skill-creator | 2026-10-11 |
