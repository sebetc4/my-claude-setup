# Phase 0: Framing

---

## Status

**Current Status:** 🟡 In Progress (40% — 2/5)
**Started:** 2026-10-11
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle what the measures are for, before any code: the return on each tool of this
setup, and a review of several sessions run by hand. From these uses, settle what the
review domain measures, from which prices, how a window of sessions is found, how long
the transcripts are kept, and how the domain's four open defects are fixed.

---

## Overview

### Why This Phase Matters
The analysis of 2026-10-06 made these choices by hand, once. A tool makes them in every
review, so a wrong price or a wrong window for a phase would be repeated in all of them.
The three counts by hand served because they ended in conclusions: shorter sessions,
runs started against the credit left. A figure no decision reads costs and gives
nothing.

### What It Enables
Phases 1 and 2 build designs the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Tasks

### Inputs
- [x] Read `docs/decisions/2026-10-06-token-costs.md`, `docs/decisions/2026-10-09-phase-4-token-costs.md` and `docs/decisions/2026-10-11-phase-5-token-costs.md`, the reader Phase 4 of `skill-tooling` delivered, and the review domain's `transcript.py`, `measure.py`, `record.py` and `tools/reviews.py`, and list what each measures today, what the records' method adds, and which open defect each touches
  Proof: review — the list, each item tied to a section of a record or a line of the code, approved by the user before the design

### Probes
- [x] Check how `cleanupPeriodDays` keeps the transcripts past 30 days: what Claude Code's documentation says it does, the value to set, the disk it takes at the present rate, and how it is set, the installer merging only hooks and permission rules into `settings.json`
  Proof: probe — the documentation read and cited with its date, the disk of `~/.claude/projects/` measured, about 29 MB a day on 2026-10-11, and the value and the way to set it put to the user
- [ ] Probe how a phase's sessions are found: the window from the phase's opening commit to its closing commit, applied to the two latest closed phases whose transcripts remain, and the `claude -p` sessions those sessions started, whose transcripts sit in project folders of their own
  Proof: probe — each window computed from `git log`, the transcripts whose calls fall in it, compared with the sessions the phase's report names in its Work Log; a session shared with another roadmap, as `2f2e66de` was, counted as the design must then decide; the `claude -p` sessions found compared with those the phase's scripts recorded

### Design
- [ ] Write the design from the two uses the measures serve, each measure kept tied to the decision it informs. The return on each tool: what a review's measured block holds (cost per model, subagents, effort, cache rebuilds, estimates marked, the review's own turn), and the tools `make reviews` flags, one costing past its median or costing while its reviews say it brought nothing. The review of several sessions: a skill of the review domain run by hand at the end of a phase, a roadmap or a stretch of work, how its window is given, what it flags as having done harm, and what it makes the agent conclude on. Also the price table and how it is kept current, the record the review of several sessions writes so that a longer window, a roadmap's, reads its phases' records rather than transcripts past 30 days, its warning when a window starts before the oldest transcript kept, what is taken from `study/session-review/`, and what a tool review itself may cost. Then get the user's approval
  Proof: review — the design, each part tied to the inputs' list and to the probes' results, approved before any code
- [ ] Settle how the four open defects are fixed: `session_resume.py` not counted in a session it opened, a skill's files read through Bash not counted, the `make update` message of `measure.py:94` and `record.py:125`, and agent runs reported without their output tokens; then write the decision record under `docs/decisions/`
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
No change to the domain in this phase. No hook keeps the measures: the user judged
`SessionEnd` and Stop unreliable for it on 2026-10-11. The transcripts stay at Claude
Code's 30 days (the user, 2026-10-11): each measure is recorded when it is taken.
The review of several sessions is started by hand, never by a phase closure, so that
the roadmap and review domains stay independent. Transcripts are deleted 30 days
after their last write: a probe that reads a session's transcript runs within that time.
The defects come from two tool reviews of 2026-10-06 and from Phase 3 of `skill-tooling`.
`measure.py` reported no run of `session_resume.py` in a session that had started with
its line. It reported no file read where the session had read the roadmap skill's
references with `cat`. Agent runs carry fresh and cached tokens but no output. Phase 3's
report left the `make update` message open, as an instruction the agent must not follow
without the user's agreement.

Phase 4 of `skill-tooling` shows what the probe and the design meet
(`docs/decisions/2026-10-09-phase-4-token-costs.md`):
- Its sixteen main sessions started 218 `claude -p` sessions, $69.32 of the phase's
  ≈ $186.62. Their transcripts sit under `~/.claude/projects/` in folders named after
  the copy each ran in, `-tmp-skill-run-…`, `-tmp-skill-grade-…` and the like, not under
  the repository's folder. A phase's window on the repository's folder misses them.
- The Stop hook asked for 18 reviews in those sixteen sessions: 93 calls, about $6.09,
  against about $2.45 in Phase 3's five sessions. A review is asked once per tool and
  session, so its cost follows the number of sessions.

Phase 5 of `skill-tooling` adds (`docs/decisions/2026-10-11-phase-5-token-costs.md`):
- Its fourteen main sessions started 248 `claude -p` sessions, $103.57 of the phase's
  ≈ $158.54, in folders named `-tmp-skill-run-…`, `-tmp-skill-judge-…` and
  `-tmp-skill-trigger-…`. Its main sessions were matched to the phase by the commits
  each made.
- A conversation went on in a new process, under another session id, and copied the
  history it shared with the first: counting each message id once gave the shared part
  to the first session.
- The Stop hook asked for 15 reviews in fourteen sessions, ≈ $3.52, about $0.23 each: a
  second one in a session where a tool first served after the first review. A session
  waiting on background runs goes on in the review's turn once the review is recorded,
  so the end of the turn does not bound a review's slice.

---

## Acceptance Criteria

- [ ] The design and the fixes of the four defects are approved by the user
- [ ] The decision record is committed
