# Superpowers plugin audit — 2026-09-18

Decision: **do not vendor the superpowers skills into `domains/` yet. Recount usage on
2026-10-18 and decide then.**

## Why wait

Usage of the plugin started on 2026-09-04, and 50 of the 51 recorded calls fall in the
two weeks before this audit. The figures measure adoption, not habit. Freezing a
vendoring perimeter on them would arbitrate on noise.

## What was measured

Skills invoked through the Skill tool, counted from the `tool_use` blocks named `Skill`
in `~/.claude/projects/*/*.jsonl`, field `input.skill`, over 479 sessions between
2026-08-21 and 2026-09-18.

| Skill | Calls | Sessions | Projects | SKILL.md |
|---|---:|---:|---:|---:|
| brainstorming | 16 | 13 | 6 | 3864 tk |
| writing-plans | 11 | 8 | 4 | 1763 tk |
| subagent-driven-development | 9 | 8 | 4 | 8085 tk |
| finishing-a-development-branch | 7 | 5 | 3 | 1945 tk |
| executing-plans | 4 | 4 | 2 | 576 tk |
| test-driven-development | 2 | 2 | 2 | 2254 tk |
| systematic-debugging | 1 | 1 | 1 | 2366 tk |
| writing-skills | 1 | 1 | 1 | 6590 tk |

Never invoked: `dispatching-parallel-agents`, `receiving-code-review`,
`requesting-code-review`, `using-git-worktrees`, `verification-before-completion`,
`using-superpowers`.

Only 8 % of sessions invoke any skill at all.

## Context cost

Fixed, paid by every session: **~1400 tokens**. About 840 come from the SessionStart
hook, which reads `skills/using-superpowers/SKILL.md` whole and injects it through
`additionalContext`; the remaining ~600 are the 14 descriptions in the skill listing.
The hook matches `startup|clear|compact`, so the injection survives every compaction.

Loaded on demand over the period: **~183k tokens**, 73 % of it
`subagent-driven-development` and `brainstorming`. Reference files are cited in prose,
never force-loaded with `@`, so they cost nothing until read.

## Conformity with this repository's checks

`python3 tests/check.py <plugin>/skills` reports 35 problems over the 14 skills.
Eight skills pass clean. The rest:

| Skill | Problems |
|---|---|
| writing-skills | 16 — 679 lines against the 500 limit, 12 cited scripts that do not exist, compatibility wording |
| subagent-driven-development | 5 — 569 lines, 3 uncited scripts |
| brainstorming | 5 — 5 scripts not cited from SKILL.md |
| receiving-code-review | 5 — compatibility wording |
| using-superpowers | 2 |
| requesting-code-review | 1 |

## Decisions taken

- **Vendor nothing before the recount.** Set the never-used skills to
  `"user-invocable-only"` in `skillOverrides` instead: they leave the model's listing
  but stay typable as `/name`, so a missing one surfaces as a need rather than staying
  invisible. `using-superpowers` is exempt — the hook injects it directly, and
  `skillOverrides` has no effect on a hook.
- **Leave `writing-skills` out of any future vendoring.** One call, the worst check
  results of the set, and it overlaps `tests/skills.py`, which already encodes these
  conventions as executable checks rather than prose.
- **Keep the `skill-creator` plugin enabled.**
  `domains/roadmap/skills/roadmap/evals/grade.py` depends on its
  `scripts/aggregate_benchmark.py` and `eval-viewer/generate_review.py`. Its step 6 now
  resolves the plugin directory through a glob, because the cache path carries a
  version hash that changes with every release.
- **First candidates if vendoring goes ahead:** `writing-plans`, which passes the checks
  and copies directly, then `brainstorming`, which needs its 5 scripts cited from
  SKILL.md.
- **Vendoring trades automatic updates for reviewed ones,** not for no updates: the
  plugin is a git clone of `github.com/obra/superpowers` pinned on a tag, and upstream
  has 34 releases. A vendored domain needs an `UPSTREAM` file recording repo, tag and
  commit, or the divergence becomes untraceable.

## Related change

`syncClaudeAiSkills: false` was set in user settings the same day: the 8 skills synced
from claude.ai cost ~1300 tokens per session for 2 calls in a month, and one of them
duplicated `skill-creator`. That setting lives outside this repository.
