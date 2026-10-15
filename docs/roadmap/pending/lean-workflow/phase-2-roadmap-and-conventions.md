# Phase 2: Roadmap And Conventions

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-authoring-skills.md` and `phase-1-authoring-skills-report.md` in full
before touching anything here: the decisions already taken, the problems and deviations
recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-roadmap-and-conventions-report.md` current as the work happens — after
each significant step, and before every commit, pause, or end of session.

---

## Objective

Remove from the roadmap skill, `CLAUDE.md`'s conventions, the agent's memories and the
review domain what Phase 0's design cuts, and give the records a short form.

---

## Overview

### Why This Phase Matters
The rituals and the records weigh on every session of every roadmap: the working sessions
make two thirds or more of the cost.

### What It Enables
Phases run and resumed at less cost, with reports a person reads.

### Out of Scope
`authoring-skills`: Phase 1.

---

## Tasks

### Roadmap
- [ ] Remove from the roadmap skill and `roadmap-auditor` what the design cuts — opening, closure, report sections, the resume's reading — and give a report entry its short form
  Proof: eval — the roadmap skill's existing cases as guards; a report's words against Phase 0's target

### Conventions
- [ ] Rewrite `CLAUDE.md`'s conventions and prune the agent's memories as the design says
  Proof: review — the diff read by the user

### Reviews
- [ ] Change the review domain's requests as the design says
  Proof: test — red before the code

### Release
- [ ] Release the domains changed: `VERSION`, `CHANGELOG.md`, installed on the user's yes, tagged with `make tags`
  Proof: check — `make check` passing, `make list` showing each installed version equal to the repository's

---

## Technical Details

### Files to Modify
```
domains/roadmap/
domains/review/
CLAUDE.md
~/.claude/projects/-code-ai-my-agent-setup/memory/
```

### Dependencies
Phase 0's design and targets.

### Constraints
Remove before adding. Scripts test-first.

---

## Acceptance Criteria

- [ ] The roadmap skill's existing cases still pass, and its reports meet Phase 0's target
- [ ] The conventions and memories are rewritten as the design says
- [ ] The changed domains are released and installed
