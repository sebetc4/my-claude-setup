# Roadmap: git-domain

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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 1  Branch Per Roadmap         🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 2  Git Skill                  🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 3  Release                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/2)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/14)
```

**Current Phase:** —
**Blocked By:** roadmap `lean-workflow`
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

Roadmap `superpowers-study` kept 14 rows of `using-git-worktrees` and
`finishing-a-development-branch` for the day a repository works on a branch per roadmap
or in worktrees: a linked worktree detected, integration by fast-forward only, a discard
only on request, never a removal with `--force`. On 2026-10-03 no repository needs them —
this repository and scriptorium commit on `main`, forma-rust has no git — so this
roadmap waits for one that asks.

On 2026-10-16, roadmap `lean-workflow`'s Phase 0 kept it on the user's word: the need is
there though no repository asks for it — commits pile up without a convention, and no
branch strategy is set. It no longer waits for a request, and it takes over the `[git]`
table's `commit` and `message` keys from roadmap `roadmap-execution`, cut that day. Its
Phase 0 reframes the phases.

---

## Decisions Taken At Opening

Taken with the user from 2026-10-02 to 2026-10-03, in roadmap `superpowers-study`:

- The domain is named `git`.
- It is built only when a repository asks for `branch = "roadmap"`, a worktree as a
  workspace, or pull requests.
- Under `branch = "roadmap"`, a branch `roadmap/<folder-name>` is made from the default
  branch when the roadmap's first phase opens, its base recorded; `close-roadmap`
  proposes the base fast-forwarded and the branch deleted, or the branch kept.
- Worktrees are the harness's: the skill names its worktree tools first, and removes only
  a worktree it made with git, never with `--force`.
- A push, of a branch or a tag, waits for the user's request; a force-push needs the
  user's explicit request.

---

## Deliberately Out Of Scope

- Pull requests and review-thread replies, unless the request that starts this roadmap
  names them.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 4 | 🔴 Not Started |
| 1 | [Branch Per Roadmap](phase-1-branch-per-roadmap.md) | 4 | 🔴 Not Started |
| 2 | [Git Skill](phase-2-git-skill.md) | 4 | 🔴 Not Started |
| 3 | [Release](phase-3-release.md) | 2 | 🔴 Not Started |

---

## Dependencies

- Roadmap `lean-workflow`: the workflow this roadmap is built with.

---

## Related Documentation

- [Superpowers study, 2026-10-01](../../../decisions/2026-10-01-superpowers-study.md) — the git rows and the `[git]` table.
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) — Claude Code's own worktrees.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/git-domain/`
**Version:** 1.1.0
**Created:** 2026-10-03
**Last Updated:** 2026-10-16

---

## Changelog

### 1.1.0 (2026-10-16)

- Kept by roadmap `lean-workflow`'s Phase 0, which it now waits for, rather than for a
  repository's request; the `[git]` table's `commit` and `message` keys come in from
  roadmap `roadmap-execution`, cut.

### 1.0.0 (2026-10-03)

- Roadmap created by Phase 4 of roadmap `superpowers-study`, with four phases: Phase 0
  Framing, Phase 1 Branch Per Roadmap, Phase 2 Git Skill, Phase 3 Release. It waits for
  roadmap `roadmap-execution` and for a repository's request.
