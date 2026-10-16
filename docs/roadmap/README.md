# Roadmaps

Temporary: written by hand on 2026-10-10, until a script generates this file. Each
roadmap's README remains the source of its state and of what it waits for.

---

## Next Steps

In order of priority, as of 2026-10-16:

1. `session-close`, Phase 2 — the start line's noise measured, the release.
2. ai-ctl's `review-skill`, in ai-ctl — its Phase 4, the first review of real code, by
   `notes/design-feedback/2026-10-15-skill-validation-hand-over.md`.
3. `lean-workflow`, Phase 0 — `token-usage` closed as decided, then the design and its
   targets.

---

## In Progress

| Roadmap | What it does | State |
|---|---|---|
| `session-close` | The `close-session` skill, which records a session's work not yet recorded and where the next one starts | Phase 2, Adoption And Release, open, 5/7 |
| `token-usage` | What this setup's tools and a set of sessions cost, read so as to conclude what to change | Phase 2, Reviews And Reports, open; its remaining tasks merged into `lean-workflow` or cut on 2026-10-16, the roadmap to close |
| `lean-workflow` | The workflow revised in depth — `authoring-skills`, the roadmap skill, the conventions, the memories, the reviews — so that a tool reaches real use in about a day and improves through it | Phase 0, Measure And Design, open, 3/4; Phase 1 waits for `session-close` |

---

## Up Next

| Roadmap | What it does | Waits for |
|---|---|---|
| `git-domain` | Commit conventions and a branch strategy for the repositories, with worktrees | `lean-workflow` |

---

## Cut

Cut on 2026-10-16 by `lean-workflow`'s Phase 0, with the user; their files at commit
`9a10c5e`.

| Roadmap | What it was | Where its parts went |
|---|---|---|
| `roadmap-dependencies` | Dependencies between roadmaps, enforced by the skill, and this overview generated | The fixes of its Phase 3 the design keeps: `lean-workflow`'s Phase 2 |
| `roadmap-execution` | Phase execution in the roadmap skill: a design per phase, a proof per task, the `[git]` table | The `[git]` table: `git-domain`; `Proof:` and `## Design`: `lean-workflow`'s Phase 2 if the design keeps them |
| `working-method` | The `shaping-work` and `finding-root-causes` skills, from superpowers' design and debugging | One of the two skills proposed for `lean-workflow`'s Phase 3 |
| `session-review` | scriptorium's `session-review` made a standard tool | None: scriptorium keeps its own |

---

## Completed

| Roadmap | What it did | Completed |
|---|---|---|
| `superpowers-study` | What to keep of the superpowers plugin, and where each kept part goes | 2026-10-03 |
| `skill-tooling` | One tool that creates, audits and evaluates skills, replacing writing-skills and skill-creator | 2026-10-11 |
| `skill-validation` | The validation of `authoring-skills` updated, so that it tells a skill's quality apart from its instruments' errors | 2026-10-15 |
