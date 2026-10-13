# Phase 3: Fixes

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/16)
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
- [ ] Define the Progress bar invariant's "not finished" as a phase that is not 🟢, and make `progress.py` cap a 🟡 phase at 19 cells even with every task ticked, failing tests first (tool reviews, 9×)
- [ ] Add `progress.py --write`, which replaces the README's progress block in place, so that an opening or a closure needs no replacement of the block by hand, failing tests first (tool reviews, 3×)

### Hooks
- [ ] Make `hooks/session_resume.py`, when the SessionStart `source` is `resume`, inject the state line alone, without the instruction to load the skill and read the phase file and its report, which the resumed conversation holds already, failing tests first (tool reviews, 13×)

### Rituals
- [ ] Apply in `references/close-phase.md` the rule for the user's uncommitted work settled in Phase 0
- [ ] Make `references/report.md`'s Resuming An Open Phase read the phase file, the report's Decisions and its last "where the next session starts" entry, and the rest of the report only where that entry points (tool reviews, 12×)
- [ ] Make `references/open-phase.md`, when the phase opened is the roadmap's first, also set the README's `**Roadmap Status:**` to 🟡 and `**Last Updated:**` to today (tool reviews, 10×)
- [ ] Make `references/create.md` propose for confirmation the answers to Name, Purpose, Scope and Phase breakdown that the conversation already gives, instead of asking the four questions afresh (tool reviews, 5×)
- [ ] Say in the Links invariant of `SKILL.md` that a document git ignores is cited with a backtick and the note that it is untracked, as a missing file is, since a link to it breaks in every other clone (tool reviews, 5×)
- [ ] Make `references/close-phase.md` update the Tasks column of the README's phase list from `progress.py`'s counts, or make `--check` compare that column
- [ ] Make a report cite a roadmap's files by the roadmap's name, not by their path — roadmap `<name>`: `<file>`, a move naming the state left and the one reached — in `references/report.md`'s Files Changed and in `agents/roadmap-auditor.md`'s comparison with `git diff`, so that a citation holds when the folder moves; the path repair of `references/close-phase.md` and `references/close-roadmap.md` then covers the `**Location:**` field and the files outside the reports (the user, 2026-10-11, at the closure of roadmap `skill-tooling`)

### Agent
- [ ] Make `agents/roadmap-auditor.md`, when the closure moved the roadmap's folder, search the old path in the repository's `*.md` files and its instruction file, and fail on a hit outside the records (tool reviews, 5×)
- [ ] Make `agents/roadmap-auditor.md`, for a roadmap target, list each check it ran before its verdict, so that a PASS shows what it covered (tool reviews, 4×)
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
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/create.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
domains/roadmap/skills/roadmap/references/report.md
domains/roadmap/agents/roadmap-auditor.md
domains/roadmap/hooks/session_resume.py
domains/roadmap/tests/test_hooks.py
```

### Dependencies
Phase 0's closure rule for uncommitted work.

### Constraints
Python standard library only; failing tests first.

---

## Acceptance Criteria

- [ ] None of the defects these tasks fix shows up again in Phase 4's runs
