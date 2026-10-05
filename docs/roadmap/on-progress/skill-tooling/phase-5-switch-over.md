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
The other superpowers skills: roadmap `superpowers-study` ruled on them, and roadmap
`working-method` turns the plugin off.

---

## Tasks

### Proof
- [ ] Evaluate the new skill against the no-skill baseline and against the two old tools on the same skill-writing tasks, and record the benchmark
- [ ] Run trigger evals on the queries where `writing-skills` or skill-creator should trigger, and tune the description until the new skill triggers on them
- [ ] Check every row of the Phase 0 capability matrix against what was built, and record each gap as a decision

### Existing Skills
- [ ] Audit `roadmap` and `tool-review` with the static audit and the `skill-auditor`, and fix or record each problem
- [ ] Make `tests/check.py` audit every folder that the `[skills]` conventions name in `dirs`, `.claude/skills` included, and not only `domains/*/skills`
- [ ] Move `domains/roadmap/skills/roadmap/evals/grade.py` from the copy of skill-creator under `study/` to the new benchmark and viewer

### Turn Off
- [ ] With the user's go-ahead, install the new domain with `make enable`, and remove from `.claude/settings.json` the registration of `domains/skill-tooling/hooks/audit_skill.py` that Phase 2 added until the install, or the audit hook runs twice here
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
```

### Dependencies
Phases 2, 3 and 4.

### Constraints
`make enable` and `make update` touch the real `~/.claude`: each waits for the user's
go-ahead. Installing the domain turns its audit hook on in every project: on 2026-10-04
it would report 85 errors in scriptorium, 55 of them on test files that a `[skills]`
table with `evals = "tests"` sets aside; before the install, the user decides whether
those repositories get the table or their fixes first.

---

## Acceptance Criteria

- [ ] The new skill matches or beats the two old tools on every benchmark task, and beats the no-skill baseline
- [ ] The new skill triggers on the queries where the old tools triggered
- [ ] `roadmap` and `tool-review` pass the static audit
- [ ] No file of this repository refers to the skill-creator plugin's directory
- [ ] A new session lists neither `superpowers:writing-skills` nor the skill-creator plugin's skill
