# Phase 1: Shaping Work

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/3)
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

Keep `phase-1-shaping-work-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Write `shaping-work` from the kept rows of `brainstorming`, and show that it does at least
as well as `superpowers:brainstorming`.

---

## Overview

### Why This Phase Matters
Design was the plugin's most called skill: 13 of its 38 calls in both periods.

### What It Enables
Design work in any project without the plugin, ending where this setup keeps designs.

### Out of Scope
The visual companion and its server, dropped by the study (rows BR18 and BR19).

---

## Tasks

### Skill
- [ ] Write `shaping-work` with `authoring-skills`, from Phase 0's design, reading the proof reference copied by `tools/shared.py`, with superpowers' MIT notice

### Evals
- [ ] Run its output evals — a spike, a bounded change, an architectural design ending in a roadmap — against no skill and against `superpowers:brainstorming`, and record the benchmark
- [ ] Run its trigger evals and tune the description until it fires where it should and nowhere the roadmap skill should

---

## Technical Details

### Files to Modify
```
domains/working-method/skills/shaping-work/SKILL.md               new
domains/working-method/skills/shaping-work/references/proof.md    copy
domains/working-method/skills/shaping-work/evals/
```

### Dependencies
Phase 0's design and eval set.

### Constraints
The skill is written and evaluated with roadmap `skill-tooling`'s tools.

---

## Acceptance Criteria

- [ ] `shaping-work` matches or beats `superpowers:brainstorming` on every output scenario, and beats no skill
- [ ] Its trigger evals pass
