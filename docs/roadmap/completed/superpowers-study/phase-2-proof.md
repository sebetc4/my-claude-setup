# Phase 2: Proof

---

## Status

**Current Status:** 🟢 Done (100% — 5/5)
**Started:** 2026-10-02
**Completed:** 2026-10-02
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-design-and-planning.md` and `phase-1-design-and-planning-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-proof-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Rule on the skills that prove work done — `test-driven-development`,
`verification-before-completion`, `systematic-debugging`, `requesting-code-review`,
`receiving-code-review` — and settle how a task declares the proof that will say it is
done.

---

## Overview

### Why This Phase Matters
The user asked whether a task or a roadmap should choose its engineering method among
those of `study/methods.md`, and whether practices other than test-driven development
bring real value. This repository's record answers part of it, as the agent put it on
2026-10-01:

- Test first, for scripts and hooks, paid: in skill-tooling's Phase 1 the tests fixed
  the conventions reader's contract to the character. But a review of 2026-09-27 found
  that the test-driven-development skill added nothing where the plan already ordered
  test first: the practice counts, not the skill.
- Eval first, for skills — the task run without the skill, then with it — paid most:
  skill-tooling's Phase 1 evals found what no unit test would, a snapshot writing a whole
  roadmap on an incomplete contract, Claude Code refusing report-named files to
  subagents, and the closure's silence on uncommitted work.
- Probes, when the platform is uncertain, paid best for their cost: they overturned
  `allowed-tools` and `skillOverrides` in skill-tooling's Phase 0, and reading the
  binary explained the Write refusal.
- Acceptance-test-driven and behaviour-driven development are already practiced without
  the ceremony: `evals.json` scenarios are given a repository, when this is asked, then
  these assertions hold, and a phase's acceptance criteria are acceptance tests.
- Domain-driven design, pair programming and design by contract weigh little at this
  scale: no rich business domain, and the user already pairs with the agent.

The hypothesis this phase tests: rather than a method chosen from a catalogue, which
risks being a label the agent applies without changing the outcome, each task, or group
of tasks, declares before it starts the proof that will say it is done — `test` (a
failing test first), `eval` (a baseline without the skill, then with it), `probe` (the
real platform tried before designing), `check` (an existing check passes) or `review`
(the user decides, as for a design). The method then follows from the kind of artifact,
and a repository sets its defaults in `.agent-conventions.toml`.

### What It Enables
The roadmap skill's phase template and Phase 1's execution model carry the proof each
task declares.

### Out of Scope
Project-management methods: the roadmap skill is this setup's method, and the
work-in-progress rule of roadmap `roadmap-dependencies` brings in the best of Kanban.

---

## Tasks

### Matrix
- [x] Rule on every capability of `test-driven-development` and its testing anti-patterns file
- [x] Rule on every capability of `verification-before-completion` and `systematic-debugging`, with its companion files
- [x] Rule on every capability of `requesting-code-review` and `receiving-code-review`, with the code-reviewer prompt, against `roadmap-auditor` and the agents skill-tooling plans

### Proof Per Task
- [x] Measure the proof-per-task hypothesis with wording micro-tests, as skill-tooling's Phase 0 measured flowcharts: does a declared proof change what an agent does, against a plain test-first instruction and against no guidance
- [x] Design the proof a task declares — its values, where a phase file writes it, the defaults of `.agent-conventions.toml` — and get the user's approval

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
Phase 1's execution model.

### Constraints
Every verdict cites its evidence; the micro-tests run headless, and a script says how
many sessions it starts before it starts them. The proof a task declares is one the
roadmap skill's execution operation can run and record before it ticks the task (row
EP18 of the draft record), and the reviewer agent of Phase 1's decision 3 takes the parts
of `code-reviewer.md` this phase keeps (rows EP19, SD16, SD17).

---

## Acceptance Criteria

- [x] Every capability of the five skills has a verdict with its reason
- [x] The proof per task is measured, then decided with the user
