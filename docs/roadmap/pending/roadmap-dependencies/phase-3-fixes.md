# Phase 3: Fixes

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/6)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-overview-and-hook.md` and `phase-2-overview-and-hook-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-fixes-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Fix the roadmap-skill defects that skill-tooling's Phase 1 and the tool reviews left
open.

---

## Overview

### Why This Phase Matters
Each one recurs in the tool reviews or diverged in an eval run, and each one sits in a
file this roadmap changes anyway.

### What It Enables
Phase 4's runs measure a skill without its known defects.

### Out of Scope
Defects of other domains.

---

## Tasks

### Scripts
- [ ] Find why `progress.py` prints file names where forma-rust's block carries phase titles, and fix it, failing tests first
- [ ] Say in `SKILL.md` that `progress.py --check` agrees only right after an opening or a closure, the README block lagging the ticked tasks by design

### Rituals
- [ ] Apply in `references/close-phase.md` the rule for the user's uncommitted work settled in Phase 0
- [ ] Make `references/close-phase.md` update the Tasks column of the README's phase list from `progress.py`'s counts, or make `--check` compare that column

### Agent
- [ ] Let `agents/roadmap-auditor.md` run read-only inspection commands such as `git status`, `wc` and `sort`, and take the scripts' path from its caller
- [ ] Take `Grep` and `Glob` out of `agents/roadmap-auditor.md`'s `tools`: the sessions of Claude Code 2.1.283 have neither (`docs/claude-code-builtins.md`), and the agent's command list leaves it no other way to search, so let it search with `grep` and `find` through `Bash`

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/scripts/progress.py
domains/roadmap/skills/roadmap/evals/test_scripts.py
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/skills/roadmap/references/close-phase.md
domains/roadmap/agents/roadmap-auditor.md
```

### Dependencies
Phase 0's closure rule for uncommitted work.

### Constraints
Python standard library only; failing tests first.

---

## Acceptance Criteria

- [ ] None of the five defects shows up again in Phase 4's runs
