# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle the design of `shaping-work` and `finding-root-causes`, and the trigger evals
that must pass before the plugin goes off.

---

## Overview

### Why This Phase Matters
The trigger evals are a go-ahead condition of the plugin's turn-off: written first, they
say what each description must catch before any description is written.

### What It Enables
Phases 1 and 2 write two skills against approved designs and a fixed eval set.

### Out of Scope
Writing the skills: Phases 1 and 2.

---

## Tasks

### Inputs
- [ ] Read the decision record `docs/decisions/2026-10-01-superpowers-study.md` and the summaries of roadmaps `skill-tooling` and `roadmap-execution`, and list what each row the record gives the two skills asks

### Evals
- [ ] Write the trigger eval set from `study/superpowers-recount/call-prompts.md` — queries that should and should not trigger each skill, and queries for the roadmap skill — rewriting any prompt that holds what should not be published, and get the user's approval

### Design
- [ ] Write the design of `shaping-work` — its three paths and their exits, its steps, the proof stated in a bounded design, its hand-over to the roadmap skill — and get the user's approval
- [ ] Write the design of `finding-root-causes` — its steps, the failing test before the fix, the fourth fix waiting for the user — and get the user's approval

---

## Technical Details

### Files to Modify
```
domains/working-method/skills/shaping-work/evals/evals.json           new
domains/working-method/skills/finding-root-causes/evals/evals.json    new
```

### Dependencies
Roadmaps `skill-tooling` and `roadmap-execution`, completed.

### Constraints
No skill text in this phase. The eval set holds no private content from the transcripts.

---

## Acceptance Criteria

- [ ] The trigger eval set and both designs are approved by the user
