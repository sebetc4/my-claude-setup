# Plugins Removed — 2026-10-04

Decision, taken by the user on 2026-10-04: **every plugin is uninstalled at every scope,
with its cache and its marketplace.** None serves this setup any more, and each one
pollutes the contexts of sessions and the conditions of tests. The other repositories
wait for this repository's roadmaps rather than keep superpowers until its replacements
exist.

This replaces the turn-off plan of `2026-10-01-superpowers-study.md` and its three
go-ahead conditions, and goes past `2026-09-28-skill-tooling.md`, which only disabled
`superpowers:writing-skills` and the skill-creator plugin.

## Figures

Projected by `claude plugin details` on 2026-10-04, Claude Code 2.1.283:

| Plugin | Listing in every session | Largest skill when invoked | Where it was on |
|---|---|---|---|
| superpowers | ~840 tokens, plus its start-up injection of `using-superpowers` | `subagent-driven-development`, ~11,800 | user, scriptorium, forma-rust |
| skill-creator | ~114 | `skill-creator`, ~10,900 | scriptorium |
| claude-code-setup | ~141 | `claude-automation-recommender`, ~4,100 | user, here, scriptorium |
| claude-md-management | ~177 | `claude-md-improver`, ~2,200 | here, scriptorium |
| diagram-design | not measured | — | scriptorium, forma-rust |

On disk: about 22 MB of plugin cache, five versions of skill-creator among them, and
35 MB of marketplace clones.

## What Was Done

- `claude plugin uninstall` at user scope, and at local scope here, in scriptorium and
  in forma-rust. `claude plugin marketplace remove` for both marketplaces, which also
  uninstalled the records left by three projects whose folders are gone: pdf-creator,
  my-claude and `~/Bookmarks/projects/scriptorium`.
- The plugin cache deleted, and with it a stray clone left by an earlier install.
- The last settings entries — the deny rule on `superpowers:writing-skills`,
  `diagram-design` in scriptorium's committed `.claude/settings.json` and in forma-rust's
  local settings — removed by the user with a script written for it: Claude Code's auto
  mode refused the agent's own edit of these files as a change to its configuration.
  Scriptorium's change is its commit `3dcd3ff`; scriptorium draws its diagrams with its
  own system.
- Verified on 2026-10-05: a fresh headless session lists no plugin skill, only the two
  builtin plugins `agents-md` and `telemetry`.

## What Is Kept

Copies of the sources, under `study/`, which git ignores: `writing-skills` 6.4.1 and
skill-creator `fa59bc903774` in `study/skill/`, superpowers 6.3.0 and 6.4.1,
claude-code-setup 1.0.0 and claude-md-management 1.0.0. The roadmaps read them, and
`domains/roadmap/skills/roadmap/evals/grade.py` runs skill-creator's benchmark script
and review viewer from them until Phase 5 of roadmap `skill-tooling` replaces both.

## What It Changes

- In the other repositories, superpowers' design, debugging, test-first and planning
  skills are gone until roadmaps `working-method` and `roadmap-execution` deliver their
  replacements.
- Roadmap `skill-tooling`: Phase 5 loses its task that turned skill-creator off in
  scriptorium.
- Roadmap `working-method`: its last phase loses the three tasks that turned the plugin
  off, checked a new session and uninstalled it.
- `docs/claude-code-coupling.md` no longer lists the plugin cache as a dependency.

## When To Revisit

- **Before installing any plugin again:** check `docs/claude-code-builtins.md` and this
  setup's tools for the capability first, and install at project scope only.
- **When `working-method` and `roadmap-execution` close:** check that every capability
  the study kept is back in the repositories that used superpowers.
