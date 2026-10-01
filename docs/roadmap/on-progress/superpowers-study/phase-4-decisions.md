# Phase 4: Decisions

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-git.md` and `phase-3-git-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-decisions-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Turn the verdicts into decisions: what is kept and where it goes, the follow-up
roadmaps, and the plugin turned off everywhere.

---

## Overview

### Why This Phase Matters
Nothing gets built from a study that ends on verdicts: the follow-up roadmaps, and the
lift of the two roadmaps waiting for this one, are what make it act.

### What It Enables
The follow-up roadmaps start, and roadmaps `skill-tooling` and `roadmap-dependencies`
resume.

### Out of Scope
Building the replacements: the follow-up roadmaps.

---

## Tasks

### Recount
- [ ] Recount the plugin's usage with the Phase 0 method — the 2026-10-18 recount if it is due, otherwise up to the day — and compare it with the baseline

### Plugin
- [ ] Rule on `using-superpowers`, `diagnosing-superpowers` and the SessionStart hook

### Decisions
- [ ] Write the decision record: the matrix, the target architecture — which domain, skill, agent, convention or roadmap-skill operation receives each kept capability — and when to revisit
- [ ] Create the follow-up roadmaps in `pending/`, each with the roadmaps it waits for
- [ ] Propose the change to skill-tooling's Phase 5, which turns superpowers back on in this repository, as a restructuring for the user's approval
- [ ] Write the plan that turns the plugin off in the user's settings once the replacements exist, with its go-ahead conditions
- [ ] Clear the `Blocked By` of roadmaps `skill-tooling` and `roadmap-dependencies`

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
Phases 1 to 3.

### Constraints
Nothing is changed in the user's settings without the user's go-ahead. The recount runs
by 2026-10-18 at the latest: its window opens on 2026-09-19, and Claude Code deletes
transcripts older than 30 days.

---

## Acceptance Criteria

- [ ] The decision record is committed
- [ ] The follow-up roadmaps exist, and roadmaps `skill-tooling` and `roadmap-dependencies` are no longer blocked
