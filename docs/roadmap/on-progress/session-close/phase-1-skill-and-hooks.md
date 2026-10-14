# Phase 1: Skill And Hooks

---

## Status

**Current Status:** ⏸️ Blocked (50% — 2/4)
**Started:** 2026-10-13
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** roadmap `skill-validation`, the update of the validation tool, `authoring-skills` with its agents `skill-grader` and `skill-auditor`, decided by the user on 2026-10-14 — see `notes/design-feedback/2026-10-14-close-session-validation.md` and the report's Decisions

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-skill-and-hooks-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Build the domain `session` as the design decided: the `[session]` table read, the
SessionStart line naming a resume note not yet taken up, and the skill `close-session`,
evaluated on the three kinds of session end and on the user's own words.

---

## Overview

### Why This Phase Matters
The skill writes into reports, notes and commits at the very end of a session, when no
context is left to repair a mistake: what it records has to be right the first time.

### What It Enables
Phase 2 installs a tested domain and tries it at the end of real sessions.

### Out of Scope
The install on `~/.claude` and the release: Phase 2.

---

## Tasks

### Domain
- [x] Create the domain `session` — `VERSION` at `0.1.0`, its `CHANGELOG.md` entry `— unreleased`, `hooks.json`, `permissions.json` — and read the `[session]` table through a copy of `shared/conventions/`, as the design decided
  Proof: test — a fixture repository with the table, one without, one with an invalid value, red before the code; `tests/domains.py` passing on the domain

### Hooks
- [x] Test and implement the SessionStart hook: one line per resume note not yet taken up, latest first, as many as the `[session]` table's `start_notes`, three when not declared, `0` turning the hook off, nothing when there is none or the table is missing
  Proof: test — fixture notes folders, taken up and not, with more than three notes open, and `start_notes` at 1 and 0, red before the code

### Skill
- [ ] Write `SKILL.md` and its references with `authoring-skills`
  Proof: eval — three cases on a fixture repository: a roadmap step stopped midway, where the user asked during the session to finish the roadmap before any other change, which the close records in the phase report and neither in a note nor in the agent's memory, a phase with every task ticked, a session outside any roadmap that took up an earlier note on another course than its resume point said, the note marked taken up, their assertions passing; `audit.py` clean, and `skill-auditor`'s verdict PASS
- [ ] Evaluate the skill's trigger on the requests of `study/session-close/close-requests.md` and on near misses: a phase closed with the session going on, a fact to record mid-session
  Proof: eval — `triggers.py`, at the rate the design sets

---

## Technical Details

### Files to Modify
```
domains/session/VERSION
domains/session/CHANGELOG.md
domains/session/hooks.json
domains/session/permissions.json
domains/session/hooks/                       the SessionStart hook
domains/session/skills/close-session/        the skill, with its evals/
domains/session/tests/test_*.py
docs/claude-code-coupling.md
```

### Dependencies
Phase 0: the design and the decision record. `authoring-skills` and its eval scripts.

### Constraints
Standard library only; `unittest`; test first. Each tie to Claude Code goes to
`docs/claude-code-coupling.md` in the same commit, as `CLAUDE.md` asks: the SessionStart
event, the `/close-session` command, the memory folder. The skill, its hook and their
messages address the agent, never Claude. The eval scripts
start sessions only with `--start`, after announcing their count and cost.

---

## Acceptance Criteria

- [ ] The domain's tests and `make check` pass
- [ ] The three cases' assertions pass, the audit is clean, and `skill-auditor` answers PASS
- [ ] The trigger evals reach the rate the design sets
