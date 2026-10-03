# Phase 2: Finding Root Causes

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/3)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-shaping-work.md` and `phase-1-shaping-work-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-finding-root-causes-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Write `finding-root-causes` from the kept rows of `systematic-debugging`, and show that it
does at least as well as `superpowers:systematic-debugging`.

---

## Overview

### Why This Phase Matters
Both bugs observed on 2026-09-17 were reported in the chat, outside any roadmap, where
only a skill of its own reaches.

### What It Enables
Debugging without the plugin, the failing test before the fix.

### Out of Scope
`find-polluter.sh` and the condition-based waiting example, dropped by the study (rows
SY14 and SY15).

---

## Tasks

### Skill
- [ ] Write `finding-root-causes` with `authoring-skills`, from Phase 0's design, with superpowers' MIT notice

### Evals
- [ ] Run its output evals — a timeout whose cause is measured, a bug given its failing test before the fix, a fourth fix that waits for the user — against no skill and against `superpowers:systematic-debugging`, and record the benchmark
- [ ] Run its trigger evals and tune the description

---

## Technical Details

### Files to Modify
```
domains/working-method/skills/finding-root-causes/SKILL.md    new
domains/working-method/skills/finding-root-causes/evals/
```

### Dependencies
Phase 0's design and eval set.

### Constraints
The skill is written and evaluated with roadmap `skill-tooling`'s tools.

---

## Acceptance Criteria

- [ ] `finding-root-causes` matches or beats `superpowers:systematic-debugging` on every output scenario, and beats no skill
- [ ] Its trigger evals pass
