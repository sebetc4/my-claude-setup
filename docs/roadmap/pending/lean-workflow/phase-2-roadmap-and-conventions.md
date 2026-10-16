# Phase 2: Roadmap And Conventions

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
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
- [ ] Apply the fixes the design keeps from roadmap `roadmap-dependencies`' Phase 3, cut on 2026-10-16 (its list at `9a10c5e`), the most recurrent in the reviews first: the first phase's opening setting the roadmap's status (10×), a 🟡 phase capped at 19 cells (9×), `progress.py --write` (3×), a roadmap's files cited by its name, which retires the memory asking for it; and, from roadmap `roadmap-execution`, cut, the phase template's `Proof:` line and `## Design` section if the design keeps them
  Proof: test — each script fix red before the code; eval — the cases of the Roadmap task above

### Conventions
- [ ] Rewrite `CLAUDE.md`'s conventions and prune the agent's memories as the design says
  Proof: review — the diff read by the user

### Reviews
- [ ] Change the review domain's requests as the design says
  Proof: test — red before the code
- [ ] Test and implement two measure fixes from roadmap `token-usage`'s Phase 2: a skill's files read through a Bash `cat` or `sed` counted as through Read; a session's subagent output settled from its `cost-state` record, and `usage.py --session` counting a main transcript with its `subagents/`
  Proof: test — a fixture session reading a reference with `cat`, and one with a `cost-state` record and a subagent lacking its final usage; red before the change

### Measure
- [ ] Bring Phase 0's measure, `notes/lean-workflow/baseline.py` and `tools.py`, into the repository where the design says, on `shared/sessions/`, for Phase 3 to run again
  Proof: test — a fixture window whose figures are computed by hand, red before the move

### Release
- [ ] Release the domains changed, review 0.3.0 and roadmap 2.0.4 among them, installed unreleased since roadmap `token-usage`: `VERSION`, `CHANGELOG.md`, installed on the user's yes, tagged with `make tags`
  Proof: check — `make check` passing, `make list` showing each installed version equal to the repository's

---

## Technical Details

### Files to Modify
```
domains/roadmap/
domains/review/
shared/usage/
notes/lean-workflow/baseline.py, tools.py    moved where the design says
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
