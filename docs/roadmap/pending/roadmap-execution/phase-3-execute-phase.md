# Phase 3: Execute Phase

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/6)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-git-table.md` and `phase-2-git-table-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-execute-phase-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Add the `execute-phase` operation to the roadmap skill, with the two agents and the
`review-package` script it calls.

---

## Overview

### Why This Phase Matters
The roadmap skill opens and closes phases but executes none: the study gives it the
execution `executing-plans` and `subagent-driven-development` did, inline by default and
one phase at a time.

### What It Enables
A phase executed task by task, each proof recorded, reviewed when it changes code or
scripts, and committed per the `[git]` table.

### Out of Scope
Subagents by default, a review per task and more than one fix round: dropped by the
study.

---

## Tasks

### Operation
- [ ] Write `references/execute-phase.md` from Phase 0's design, and route it from `SKILL.md`
- [ ] Rewrite the roadmap skill's description by the Description rule of 2026-09-28 so that it covers the execution, and run its trigger evals
- [ ] Write `scripts/review_package.py` — the log, the stat and the diff of a range in one file — failing tests first, with superpowers' MIT notice

### Agents
- [ ] Write `agents/phase-reviewer.md`: read-only on the checkout, without the Agent tool, its criteria from rows RQ12 to RQ18 and TD20 to TD23, its verdict first
- [ ] Write `agents/task-implementer.md`: without the Skill and Agent tools, the declared proof, four statuses, its report in a file
- [ ] Record the two agents' format and tool lists in `docs/claude-code-coupling.md`, and add the operation and the agents to `domains/review/hooks/tools.json`

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/references/execute-phase.md    new
domains/roadmap/skills/roadmap/scripts/review_package.py      new
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/skills/roadmap/evals/test_scripts.py
domains/roadmap/agents/phase-reviewer.md                      new
domains/roadmap/agents/task-implementer.md                    new
domains/review/hooks/tools.json
docs/claude-code-coupling.md
```

### Dependencies
Phases 1 and 2.

### Constraints
One phase per run: closing a phase and opening the next ends the turn. Superpowers'
MIT notice wherever its text is adapted. Python standard library only; scripts
test-first.

---

## Acceptance Criteria

- [ ] `execute-phase` runs a phase inline, records each proof before ticking its task, and stops at the four stops
- [ ] Neither agent holds the Agent tool, and `task-implementer` holds no Skill tool
- [ ] `make check` passes
