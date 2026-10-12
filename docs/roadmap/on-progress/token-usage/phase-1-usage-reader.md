# Phase 1: Usage Reader

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/6)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-usage-reader-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Extend the reader that Phase 4 of `skill-tooling` wrote, so that it counts what the
tool reviews and the review of several sessions need:
- each model's cost;
- every subagent;
- the effort, the cache rebuilds and the compactions;
- a window of sessions, a phase's among them;
- sessions resumed from one another, counted once.

---

## Overview

### Why This Phase Matters
Every figure of Phase 2 comes from this reader: a count wrong here is wrong in every
review and every report.

### What It Enables
Phase 2's measured block, the tools `make reviews` flags, and the review of several
sessions.

### Out of Scope
Showing the figures, the conclusions drawn from them and the transcripts kept: Phase 2.

---

## Tasks

### Probe
- [ ] Probe how a compacted session is recorded: a session compacted by hand, its transcript read for the records the compaction writes, the compaction's call and the context the next call holds
  Proof: probe — the records cited from the transcript with the Claude Code version and the date, and the fields the count will read, put in the report before the count's test

### Reader
- [ ] Test and implement the price table the design chose: each model's input, output, cache-read and cache-write prices, each with its date and its source, published or fitted, and a model the table lacks reported as unknown rather than priced at zero
  Proof: test — a usage of each model in the table priced by hand, and a model the table lacks reported as unknown, red before the code
- [ ] Test and implement the count of a session with all its subagents: cost per model and effort, the subagents' output tokens estimated per agent type and marked as such, a run's last call taking its output from the Agent tool's result, each cache rebuild with its size, cost and cause, each compaction, and the rule that prices a tool's text
  Proof: test — transcript excerpts holding a main session, two subagents, a run whose last call's output comes from the Agent tool's result, a rebuild after a pause, a compaction as the probe recorded it and calls at two efforts, every figure computed by hand, red before the code
- [ ] Test and implement the deduplication of resumed sessions: a message id counted once, given to the transcript whose last record comes first
  Proof: test — two transcripts sharing messages, as a resumed session writes them, the continuation's copied records starting earlier, counted once in all and the shared calls given to the first conversation, red before the code
- [ ] Test and implement the selection of a window of sessions as the design decided, a phase's among them: each call counted by its time, the `claude -p` sessions given to a main session by their scratchpad folder or their time and marked shared in two spans, each commit given to its session
  Proof: test — a fixture repository with a phase's opening and closing commits, transcripts inside, outside and across the window, and `claude -p` sessions started from the phase in project folders of their own, one in a scratchpad folder, the phase's sessions found, red before the code

### Shared Code
- [ ] Bring the extended reader to the review domain as the design decided: `shared/usage/` extended and `shared/sessions/` new, copied into `tool-review`, whose scripts, Stop hook and `tools/reviews.py` use them; `reviewfile.py` moved to `shared/reviewfile/`; the copies into `reviewing-token-usage` come with the skill in Phase 2
  Proof: check — `make shared`, then `make check`, which fails on a copy that differs from its source

---

## Technical Details

### Files to Modify
```
shared/usage/                                         the reader, extended
shared/sessions/                                      new, a window's sessions
shared/reviewfile/                                    moved from tool-review's scripts
domains/review/skills/tool-review/scripts/*.py        its copies and its callers
domains/review/tests/test_*.py
docs/claude-code-coupling.md
```

### Dependencies
Phase 0: the design and the decision record. Roadmap `skill-tooling`: the reader of its
Phase 4.

### Constraints
Standard library only; test first. An estimated figure stays marked in every structure
that carries it, and no total adds it to counted figures without saying so. Each field
of Claude Code's transcripts the reader starts to depend on is added to
`docs/claude-code-coupling.md` in the same commit, as `CLAUDE.md` asks.

Claude Code's own Haiku calls appear in no transcript: a main session's `cost-state`
counts them, and a `claude -p` session's json result. Over Phase 4 of `skill-tooling`'s
128 results, they added $1.20, up to $0.29 in one run
(`docs/decisions/2026-10-09-phase-4-token-costs.md`). The `cost-state` records name
Claude Haiku 5.5 from 2026-10-08, a model the price table of `usage.py` lacks.

Phase 5 of `skill-tooling` adds (`docs/decisions/2026-10-11-phase-5-token-costs.md`):
- The estimate of a subagent's output, one figure for every agent, 5,400 tokens a call
  taken from Phase 3's runs, was eight times too high for `skill-auditor`, whose calls
  averaged about 640: $3.73 estimated where `cost-state` counted $1.50. The Agent tool's
  result holds the usage of the subagent's last call, final output included.
- Claude Haiku 5.5's `cost-state` records fit $0.10 input and $0.50 output per million,
  plus $0.01 a web search; no published price was read. `claude -p` sessions still call
  Claude Haiku 4.5: $1.01 over Phase 5's 96 json results.
- Two main sessions' `cost-state` records hold $0.10 and $0.04 of Opus 5.5 calls that no
  transcript holds, so a main thread counted from its transcript can fall a little short
  of its record.

---

## Acceptance Criteria

- [ ] Every function the design names is covered by unit tests that pass under `make check`
- [ ] No estimated figure reaches a total without its mark
