# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, on the decisions of roadmap `superpowers-study`, the design of what this roadmap
adds to the roadmap skill, before any change to it.

---

## Overview

### Why This Phase Matters
The study decided what each kept capability does, not the text that does it: the steps
of `execute-phase`, the shape of the `Proof:` line, the agents' inputs and answers.
Settling them first keeps Phases 1 to 3 from arguing each point again.

### What It Enables
Phases 1 to 3 build designs the user approved.

### Out of Scope
Changes to the skill: they start in Phase 1.

---

## Tasks

### Inputs
- [ ] Read the decision record `docs/decisions/2026-10-01-superpowers-study.md` and the summary of roadmap `roadmap-dependencies`, and list what each row the record gives the roadmap skill, the proof reference, the `[git]` table and the two agents asks of each file

### Design
- [ ] Write the design of `execute-phase` — its steps, the four stops and the fourth fix, the proof run and recorded before a task is ticked, the review's findings ruled in one fix pass, the delegation a phase writes down, the commit per the `[git]` table — and get the user's approval
- [ ] Write the design of the phase template's `## Design` section and `Proof:` line, of the proof reference, and of what `create.md`, `open-phase.md` and `report.md` gain, and get the user's approval
- [ ] Write the design of `phase-reviewer`, `task-implementer` and the `review-package` script — inputs, tool lists, model tier, answer — and get the user's approval
- [ ] Settle with the user when `execute-phase` hands over to a new session — at the end of a phase, at the end of a task, or at the first task ticked past a context threshold declared in `[roadmap]` and overridable by a roadmap, knowing that the user ends sessions by watching the plan's usage window, which no hook reads, and closes them with `close-session` — what the new session reads to resume — the whole report, as `report.md` asks today, or the resume point `close-session` writes as the last block of a report entry —, and whether `progress_guard.py` can read the context's size from the transcript when a task is ticked, on the figures of `docs/decisions/2026-10-06-token-costs.md`, `docs/decisions/2026-10-09-phase-4-token-costs.md` and `docs/decisions/2026-10-13-session-close.md`
- [ ] Choose with the user the eval scenarios that prove the operation in Phase 4

### Record
- [ ] Write the decision record under `docs/decisions/`

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-roadmap-execution.md    new
```

### Dependencies
Roadmap `roadmap-dependencies`, completed.

### Constraints
No change to the skill in this phase. The designs carry the record's verdicts; a
verdict changed here is recorded with its reason.

The opening decision that `execute-phase` runs one phase in the main conversation was
taken before any cost was measured. Phase 3 of roadmap `skill-tooling` then ran its main
thread in five sessions, four of which reached a context of 407,000 to 631,000 tokens,
never compacted. A
session that started on a phase took 9 to 17 calls and $0.57 to $1.16 to read the skill,
the phase file and the report, against a read of about (context − 100,000) × $0.20 per
million at each call of a continued session. A new session every 60 calls, about one
task, would have saved $12.42 net of the phase's $88.28 of main thread, 14%
(`docs/decisions/2026-10-06-token-costs.md`). The report a resumed session reads in full
grows through the phase: Phase 3's ended at about 30,000 tokens. The 60 calls are a
mean over the phase's 12 tasks, not a measure of each one: a fixed rule of one session
per task would pay a full reorientation even for a task of a few calls.

Phase 4 of `skill-tooling` then ran in sixteen sessions, the user handing over by hand
(`docs/decisions/2026-10-09-phase-4-token-costs.md`). The fifteen that worked on the
phase made 35 to 123 calls, 76 on average, and no context passed 357,000 tokens. A call
read 37% less cache than in Phase 3, about $27 over the phase, yet the phase's main
thread cost $105.28 against Phase 3's $88.29: 62% more calls, and a dearer opening.
- A session spent $1.27 to $2.12 before its first edit, and reached about 150,000 tokens.
- The roadmap documents read cost about $13.25, against about $2.30 in Phase 3. The
  report, which ended at about 50,000 tokens, was read 39 times, about $5.92, and the
  phase file 26 times, about $3.81.
- Each session also paid one tool review, about $0.34, and four cache rebuilds, when a
  session went on under another organization after the subscription's limit, cost about
  $6.50.

At that opening, a hand-over pays back after 65 to 105 calls, where Phase 3's paid back
after about 25 at 300,000 tokens. Phase 4's sessions sat near that point, so handing over
more often would have saved little: what a resuming session reads moves the break-even
as much as when it starts.

---

## Acceptance Criteria

- [ ] The designs of the operation, the template, the proof reference and the two agents are approved by the user
- [ ] The decision record is committed
