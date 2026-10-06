# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** roadmap `skill-tooling`

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle what the review domain measures, from which prices, how it finds a phase's
sessions, how its measures outlive the transcripts, and how its four open defects are
fixed, before any code.

---

## Overview

### Why This Phase Matters
The analysis of 2026-10-06 made these choices by hand, once. A tool makes them in every
review, so a wrong price or a wrong window for a phase would be repeated in all of them.

### What It Enables
Phases 1 and 2 build designs the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Tasks

### Inputs
- [ ] Read `docs/decisions/2026-10-06-token-costs.md`, the reader Phase 4 of `skill-tooling` delivered, and the review domain's `transcript.py`, `measure.py`, `record.py` and `tools/reviews.py`, and list what each measures today, what the record's method adds, and which open defect each touches
  Proof: review — the list, each item tied to a section of the record or a line of the code, approved by the user before the design

### Probes
- [ ] Probe how measures can outlive the transcripts' 30 days: a `SessionEnd` hook, the Stop hook writing a session's usage at each stop, and `cleanupPeriodDays` raised, with the disk each one takes
  Proof: probe — a minimal hook that writes a file, registered in this repository's local settings and removed after, in a session ended by `/exit` in the CLI and in one closed from the VS Code panel; the file written or not in each, the Stop hook as the control
- [ ] Probe how a phase's sessions are found: the window from the phase's opening commit to its closing commit, applied to the two latest closed phases whose transcripts remain
  Proof: probe — each window computed from `git log`, the transcripts whose calls fall in it, compared with the sessions the phase's report names in its Work Log; a session shared with another roadmap, as `2f2e66de` was, counted as the design must then decide

### Design
- [ ] Write the design — what a review's measured block holds (cost per model, subagents, effort, cache rebuilds, estimates marked), the price table and how it is kept current, the command that reports a session, a phase or a roadmap, and how measures are kept — and get the user's approval
  Proof: review — the design, each part tied to the inputs' list and to the probes' results, approved before any code
- [ ] Settle how the four open defects are fixed: `session_resume.py` not counted in a session it opened, a skill's files read through Bash not counted, the `make update` message of `measure.py:92` and `record.py:125`, and agent runs reported without their output tokens; then write the decision record under `docs/decisions/`
  Proof: review — one fix per defect, each with the test that will show it, then the record, approved by the user with its date

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-token-usage.md    new
```

### Dependencies
Roadmap `skill-tooling`, completed: the reader its Phase 4 wrote to count a run's tokens
and cost from its transcripts.

### Constraints
No change to the domain in this phase. A probe that registers a hook does it in this
repository's local settings and removes it afterwards. Transcripts are deleted 30 days
after their last write: a probe that reads a session's transcript runs within that time.
The defects come from two tool reviews of 2026-10-06 and from Phase 3 of `skill-tooling`.
`measure.py` reported no run of `session_resume.py` in a session that had started with
its line. It reported no file read where the session had read the roadmap skill's
references with `cat`. Agent runs carry fresh and cached tokens but no output. Phase 3's
report left the `make update` message open, as an instruction the agent must not follow
without the user's agreement.

---

## Acceptance Criteria

- [ ] The design and the fixes of the four defects are approved by the user
- [ ] The decision record is committed
