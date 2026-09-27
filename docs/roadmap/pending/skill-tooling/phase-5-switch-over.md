# Phase 5: Switch-Over

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/11)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-4-evaluation-tooling.md` and `phase-4-evaluation-tooling-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-5-switch-over-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Move this setup onto the new tool: prove it with its own tooling, run the roadmap evals
on it, audit the existing skills with it, and turn off `superpowers:writing-skills` and
the skill-creator plugin.

---

## Overview

### Why This Phase Matters
As long as the old tools stay on, they keep triggering and compete with the new one, and
the 2026-09-18 decision still says to keep skill-creator.

### What It Enables
One tool for skills in this setup, and a recorded decision in place of the 2026-09-18 one.

### Out of Scope
Vendoring the other superpowers skills, decided at the recount of 2026-10-18.

---

## Tasks

### Proof
- [ ] Evaluate the new skill against the no-skill baseline and against the two old tools on the same skill-writing tasks, and record the benchmark
- [ ] Run trigger evals on the queries where `writing-skills` or skill-creator should trigger, and tune the description until the new skill triggers on them
- [ ] Check every row of the Phase 0 capability matrix against what was built, and record each gap as a decision

### Existing Skills
- [ ] Audit `roadmap` and `tool-review` with the static audit and the `skill-auditor`, and fix or record each problem
- [ ] Move `domains/roadmap/skills/roadmap/evals/grade.py` from the skill-creator plugin to the new benchmark and viewer

### Turn Off
- [ ] With the user's go-ahead, install the new domain with `make enable`
- [ ] With the user's go-ahead, set `superpowers:writing-skills` to `"off"` in `skillOverrides` and disable the skill-creator plugin
- [ ] Add the new tools to `domains/review/hooks/tools.json` so that tool reviews cover them
- [ ] Update `CLAUDE.md`: the new domain in the layout, and the gotchas the phases revealed
- [ ] Write the decision record that replaces the 2026-09-18 decision on writing-skills and skill-creator
- [ ] Release the domain: `VERSION`, its `CHANGELOG.md` entry, and the `<domain>-vX.Y.Z` tag after the merge

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/evals/grade.py
domains/review/hooks/tools.json
domains/<domain>/VERSION
domains/<domain>/CHANGELOG.md
CLAUDE.md
docs/decisions/<date>-skill-tooling-switch-over.md    new
~/.claude/settings.json                               skillOverrides and plugins, with the user's go-ahead
```

### Dependencies
Phases 2, 3 and 4.

### Constraints
`make enable`, `make update`, `skillOverrides` and plugin changes touch the real
`~/.claude`: each waits for the user's go-ahead.

---

## Acceptance Criteria

- [ ] The new skill matches or beats the two old tools on every benchmark task, and beats the no-skill baseline
- [ ] The new skill triggers on the queries where the old tools triggered
- [ ] `roadmap` and `tool-review` pass the static audit
- [ ] No file of this repository refers to the skill-creator plugin's directory
- [ ] A new session lists neither `superpowers:writing-skills` nor the skill-creator plugin's skill
