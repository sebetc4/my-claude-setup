# Phase 1: Design And Planning

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-design-and-planning-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Rule on the skills that turn an idea into a design, a plan and executed work —
`brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`,
`dispatching-parallel-agents` — and map each kept capability onto this setup, the
roadmap skill first.

---

## Overview

### Why This Phase Matters
These are the plugin's most used skills — 36 of the 51 calls of the 2026-09-18
baseline: `brainstorming` 16, `writing-plans` 11, `subagent-driven-development` 9 — and
its most expensive, about 8,100 tokens per call of `subagent-driven-development` and
3,900 of `brainstorming`. They also overlap the roadmap skill: a plan is a phase's task
list, executing it is working a phase, and `brainstorming` is the design step every phase
of this setup already starts with by hand (write the design, get the user's approval).

### What It Enables
Roadmap `roadmap-dependencies` and the follow-up roadmaps build on a settled execution
model.

### Out of Scope
Proof practices (Phase 2) and git (Phase 3), although these skills call them.

---

## Tasks

### Matrix
- [ ] Rule on every capability of `brainstorming`, with its scripts and its visual companion
- [ ] Rule on every capability of `writing-plans` and `executing-plans`, against what the roadmap skill's phase files and reports already carry
- [ ] Rule on every capability of `subagent-driven-development` and `dispatching-parallel-agents`, with their prompts, against this setup's agents and the subagent facts found in skill-tooling: Write refuses report-named files in a subagent, and run agents work without the Skill tool

### Mapping
- [ ] Decide where design work happens — a step of the roadmap skill, a skill of its own, or a phase's first task — and where specs and plans live once `.superpowers/` is gone; get the user's approval
- [ ] Decide whether the roadmap skill gains an operation that executes a phase's tasks, and how it delegates to subagents; get the user's approval

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
Phase 0's inventory and method.

### Constraints
Every verdict cites its evidence. No code in this phase.

---

## Acceptance Criteria

- [ ] Every capability of the five skills has a verdict with its reason
- [ ] The design step, the location of specs and plans, and the execution model are decided with the user
