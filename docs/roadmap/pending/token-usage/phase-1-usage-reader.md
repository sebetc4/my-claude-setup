# Phase 1: Usage Reader

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
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
reviews and the cost command need:
- each model's cost;
- every subagent;
- the effort and the cache rebuilds;
- a phase's sessions;
- sessions resumed from one another, counted once.

---

## Overview

### Why This Phase Matters
Every figure of Phase 2 comes from this reader: a count wrong here is wrong in every
review and every report.

### What It Enables
Phase 2's measured block, `make reviews` in dollars, and the cost command.

### Out of Scope
Showing the figures and keeping them: Phase 2.

---

## Tasks

### Reader
- [ ] Test and implement the price table the design chose: each model's input, output, cache-read and cache-write prices, the date they were read, and a model the table lacks reported as unknown rather than priced at zero
  Proof: test — a usage of each model in the table priced by hand, and a model the table lacks reported as unknown, red before the code
- [ ] Test and implement the count of a session with all its subagents: cost per model, the subagents' output tokens estimated and marked as such, the effort of each call, and each cache rebuild with its size
  Proof: test — transcript excerpts holding a main session, two subagents, a rebuild after a pause and calls at two efforts, every figure computed by hand, red before the code
- [ ] Test and implement the deduplication of resumed sessions: a message id counted once, given to the first session that holds it
  Proof: test — two transcripts sharing messages, as a resumed session writes them, counted once in all, red before the code
- [ ] Test and implement the selection of a phase's sessions as the design decided
  Proof: test — a fixture repository with a phase's opening and closing commits and transcripts inside and outside the window, the phase's sessions found, red before the code

### Shared Code
- [ ] Bring the extended reader to the review domain as the design decided, so that the tool-review scripts, the Stop hook and `tools/reviews.py` use one copy of it
  Proof: check — `make shared`, then `make check`, which fails on a copy that differs from its source

---

## Technical Details

### Files to Modify
```
shared/<module>/                                      the reader, as the design places it
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

---

## Acceptance Criteria

- [ ] Every function the design names is covered by unit tests that pass under `make check`
- [ ] No estimated figure reaches a total without its mark
