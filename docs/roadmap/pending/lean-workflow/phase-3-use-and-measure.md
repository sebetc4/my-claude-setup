# Phase 3: Use And Measure

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-roadmap-and-conventions.md` and `phase-2-roadmap-and-conventions-report.md`
in full before touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-use-and-measure-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Use the released tools on real work and judge them against Phase 0's targets.

---

## Overview

### Why This Phase Matters
Only real use proves a lighter workflow keeps what the heavier one caught.

### What It Enables
The next roadmaps run on a workflow measured in use.

### Out of Scope
New tools beyond the one the user picks for the first task.

---

## Tasks

### Use
- [ ] Build or change a tool the user picks under the default regime, from the request to its install — proposed first: `finding-root-causes` or `shaping-work`, from roadmap `working-method`, cut, its decisions in `docs/decisions/2026-10-01-superpowers-study.md`
  Proof: check — its cost, days and yeses against Phase 0's targets
- [ ] Run a phase of a roadmap with the released roadmap skill
  Proof: check — its report's words and its steps against Phase 0's targets
- [ ] Fix what both show by the fix from use
  Proof: check — each fix released as a patch

### Judge
- [ ] Review the targets with the user — met, or what changes next —, and `roadmap-auditor`'s two points from their reviews, kept or cut; update the decision record's When To Revisit
  Proof: review — the user's verdict in the report

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-lean-workflow.md
```

### Dependencies
Phases 1 and 2 released.

### Constraints
The fixes follow the default regime unless the full regime's criteria hold.

---

## Acceptance Criteria

- [ ] A tool and a roadmap phase ran on the released workflow, measured against the targets
- [ ] The user's verdict on the targets is recorded
