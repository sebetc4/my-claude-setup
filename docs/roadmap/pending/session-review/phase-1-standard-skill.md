# Phase 1: Standard Skill

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** roadmap `token-usage`, Phase 1

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-standard-skill-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Port `session-review` into the domain the design chose, as a skill any repository runs
on its own tools: its settings read from the repository's conventions, its transcript
reading shared as the design decided, nothing of scriptorium left in it.

---

## Overview

### Why This Phase Matters
A review tool that only one repository can run reviews only that repository's tools.
Shared with `tool-review`, it moves forward with the findings of the tool reviews.

### What It Enables
Phase 2 installs it and moves scriptorium on to it.

### Out of Scope
Installing it, and scriptorium's move: Phase 2.

---

## Tasks

### Measure
- [ ] Test and implement the measure of a task's slice on the shared reader, as the design decided: tokens, subagents, turns, tools, friction, the skills loaded, and the review tooling's own turns left out
  Proof: test — fixture transcripts with a subagent, a loaded skill and a run of the review tooling, every figure computed by hand, red before the code
- [ ] Test and implement the settings read from `.agent-conventions.toml`: the reviews folder, the repository's skills, and what the design adds
  Proof: test — a fixture repository with its conventions file, and one without, for which the skill proposes values as `references/conventions.md` says, red before the code

### Corpus
- [ ] Test and implement the corpus as the design decided: reviews read and checked, each measure beside its median, the obligations printed, and the aggregate read across reviews
  Proof: test — fixture reviews, the medians and the obligations computed by hand, red before the code
- [ ] Apply the design's decision on the ledger: kept with its hook, changed, or dropped
  Proof: test — when kept, a sweep over fixture transcripts writes one entry per session and skips the live one, red before the code; when dropped, no file of the domain names it

### Skill
- [ ] Write `SKILL.md` and its references with `authoring-skills`, from scriptorium's, with nothing of scriptorium left in them
  Proof: eval — a case that reviews a finished task of a fixture repository, its assertions passing; `audit.py` clean, and `skill-auditor`'s verdict PASS

---

## Technical Details

### Files to Modify
```
domains/<domain>/skills/<name>/                the skill, as the design names it
domains/<domain>/skills/<name>/evals/
domains/<domain>/hooks/ and hooks.json         if the ledger is kept
domains/<domain>/permissions.json
domains/<domain>/tests/test_*.py
shared/<module>/                               what the design shares
docs/claude-code-coupling.md
```

### Dependencies
Phase 0: the design and the decision record. Roadmap `token-usage`, Phase 1: the
extended reader, which this phase uses rather than write a second one.

### Constraints
Standard library only; `unittest`; test first. scriptorium's pytest tests are rewritten
under `unittest`, not run as they are. Each Claude Code tie the skill adds goes to
`docs/claude-code-coupling.md` in the same commit, as `CLAUDE.md` asks.

---

## Acceptance Criteria

- [ ] Every function the design names is covered by unit tests that pass under `make check`
- [ ] The skill passes `audit.py` and its evals
