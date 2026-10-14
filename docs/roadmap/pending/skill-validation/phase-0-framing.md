# Phase 0: Framing

---

## Status

**Current Status:** 🟡 In Progress (57% — 4/7)
**Started:** 2026-10-14
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, before any change to `authoring-skills`, which directions of the two feedback
notes the update takes, how a failure and an auditor point are classified, and the
criterion a skill's validation ends on, from measures of the instruments' spread on a
fixed version rather than from the notes alone.

---

## Overview

### Why This Phase Matters
The two notes propose twelve directions, D1 to D7 and E1 to E5, none decided. Their
figures rest on one grading per run and on auditor passes over changing text: no
measure yet says how often the grader or the auditor changes its answer on the same
output. A criterion chosen without that measure would be a second guess the next skill
works around.

### What It Enables
Phases 1 to 3 build a design the user approved, each change traced to the problem it
answers.

### Out of Scope
Changes to the skill, its scripts and its agents: they start in Phase 1.

---

## Tasks

### Inputs
- [x] Map each problem of the two notes, V1 to V6 and R1 to R6, to the file and line of `authoring-skills`, its scripts or its agents that causes it, reading ai-ctl's `review-skill` reports and runs only with the user's leave
  Proof: review — the map in the report, each problem with its file and line, read by the user
- [x] List the lines `close-session` and `reviewing-delivered-code` carry because of the validation, from both notes, as the cases Phase 4 replays
  Proof: review — the list in the report, each line with the problem it answers

### Measures
- [x] Measure `skill-auditor`'s spread: five passes or more on `close-session` at `65ca91f`, the same text each time; count the verdicts and each point by the number of passes that raised it, the cost announced first
  Proof: check — the counts in the report, with each pass's cost
- [x] Measure `skill-grader`'s spread: grade again, three times each, the two failed runs of `close-session`'s iterations 10 and 11 and a sample of their passed runs; count how often an assertion's verdict changes on the same output, the cost announced first
  Proof: check — the counts in the report, with the gradings' cost

### Design
- [ ] Write the design in this file's `## Design`: each direction D1 to D7 and E1 to E5 kept, changed or dropped, with the file it changes and the phase that builds it; the classes of a failure and the step that classifies one; the step that sends a fix to the validation when an instrument is suspected; the pass criterion in rates; the auditor's verdict rule, the rule that a FAIL whose lines are answered never counts standing; where a skill's sources go; how a failure seen in real use enters the evals; get the user's approval
  Proof: review — the user's approval, recorded in the report
- [ ] Rewrite the application line of the agent's memory `skill-auditor-pass-required`, which tells the agent to answer an auditor point it disagrees with by a wording that satisfies the auditor, to the design's rule for a point the evals or the classification contradict
  Proof: review — the new line read by the user

### Record
- [ ] Write the decision record `docs/decisions/<date>-skill-validation.md`: the problems, the measures, the design's decisions and when to revisit them
  Proof: check — the record committed, `make check` passing

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-skill-validation.md    new
```

### Dependencies
Roadmap `skill-tooling`, completed: `authoring-skills` as installed at 0.1.2. The two
notes, in the ignored `notes/design-feedback/`:
`2026-10-14-close-session-validation.md` and
`2026-10-14-reviewing-delivered-code-validation.md`.

### Constraints
No change to `authoring-skills`, its scripts or its agents in this phase. Every session
the measures start is announced with its count and cost, and started on the user's yes.

---

## Acceptance Criteria

- [ ] The auditor's and the grader's spread are measured on fixed versions
- [ ] The design is approved by the user, each direction of both notes settled
- [ ] The decision record is committed
