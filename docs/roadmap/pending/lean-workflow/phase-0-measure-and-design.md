# Phase 0: Measure And Design

---

## Status

**Current Status:** 🟡 In Progress (25% — 1/4)
**Started:** 2026-10-15
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-measure-and-design-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Measure where the current workflow's time and tokens go, decide what each tool and each
waiting roadmap keeps, and set the figures Phases 1 to 3 are judged on.

---

## Overview

### Why This Phase Matters
Until now the workflow's weight was answered by additions; a measure says what to remove.

### What It Enables
Phases 1 and 2 cut from a design and against targets, not from impressions.

### Out of Scope
Changing any tool: Phases 1 and 2.

---

## Tasks

### Measure
- [x] Measure from the transcripts since 2026-09-28, with `shared/sessions/`: each roadmap's cost and days from its opening to its tool installed, the working sessions' share, the words per phase report and per task, the user's yeses per eval iteration
  Proof: check — each figure in the report with the command that gives it
- [ ] List the steps and rules each tool imposes — the roadmap skill and `roadmap-auditor`, `authoring-skills` and its agents, the review domain's requests, `CLAUDE.md`'s conventions, the agent's memories — each with what it caught in the reports and reviews, and what it cost
  Proof: review — the list read by the user

### Decide
- [ ] Decide with the user, for each waiting roadmap — `roadmap-dependencies`, `roadmap-execution`, `working-method`, `git-domain`, `session-review` — and for `token-usage`'s remaining tasks: keep, merge into this roadmap, or cut
  Proof: review — the user's decision for each, in the report and in `docs/roadmap/README.md`
- [ ] Write the design in this file's `## Design`: what is removed, what changes, the targets of Phases 1 to 3; then the decision record
  Proof: review — the design approved by the user

---

## Technical Details

### Files to Modify
```
docs/roadmap/pending/lean-workflow/phase-0-measure-and-design.md
docs/roadmap/README.md
docs/decisions/<date>-lean-workflow.md    new
```

### Dependencies
`docs/decisions/2026-10-15-validation-weight.md`: its figures and regimes are the
starting point, not measured again.

### Constraints
Remove before adding. The design adds a tool only when it replaces more than it adds.

---

## Acceptance Criteria

- [ ] The baseline figures are recorded with their commands
- [ ] Each waiting roadmap has the user's decision
- [ ] The design and its targets are approved
