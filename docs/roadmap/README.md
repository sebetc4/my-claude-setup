# Roadmaps

Temporary: written by hand on 2026-10-10, until a script generates this file. Each
roadmap's README remains the source of its state and of what it waits for.

---

## Next Steps

In order of priority, as of 2026-10-15:

1. `session-close`, Phase 2 — the install, a session closed inside and outside a
   roadmap, the start line's noise measured, the changes waiting handed over, the
   release.
2. ai-ctl's `review-skill`, in ai-ctl — its Phase 4, the first review of real code, by
   `notes/design-feedback/2026-10-15-skill-validation-hand-over.md`.
3. `lean-workflow`, Phase 0 — the workflow measured, each waiting roadmap kept, merged or
   cut, the design and its targets.

---

## In Progress

| Roadmap | What it does | State |
|---|---|---|
| `session-close` | The `close-session` skill, which records a session's work not yet recorded and where the next one starts | Phase 2, Adoption And Release, open, 0/7 |
| `token-usage` | What this setup's tools and a set of sessions cost, read so as to conclude what to change | Phase 2, Reviews And Reports, open and waiting; its remaining tasks decided by `lean-workflow`'s Phase 0 |

---

## Up Next

| Roadmap | What it does | Waits for |
|---|---|---|
| `lean-workflow` | The workflow revised in depth — `authoring-skills`, the roadmap skill, the conventions, the memories, the reviews — so that a tool reaches real use in about a day and improves through it | `session-close` |

---

## Waiting For lean-workflow

Frozen on 2026-10-15: each is kept, merged into `lean-workflow` or cut by its Phase 0.

| Roadmap | What it does |
|---|---|
| `roadmap-dependencies` | Dependencies between roadmaps, enforced by the skill, and this overview generated |
| `roadmap-execution` | Phase execution in the roadmap skill: a design per phase, a proof per task, the `[git]` table |
| `working-method` | The `shaping-work` and `finding-root-causes` skills, from superpowers' design and debugging |
| `git-domain` | Branch per roadmap and worktrees, built once a repository asks for them |
| `session-review` | scriptorium's `session-review` made a standard tool, with which any repository reviews the tools it builds for itself |

---

## Completed

| Roadmap | What it did | Completed |
|---|---|---|
| `superpowers-study` | What to keep of the superpowers plugin, and where each kept part goes | 2026-10-03 |
| `skill-tooling` | One tool that creates, audits and evaluates skills, replacing writing-skills and skill-creator | 2026-10-11 |
| `skill-validation` | The validation of `authoring-skills` updated, so that it tells a skill's quality apart from its instruments' errors | 2026-10-15 |
