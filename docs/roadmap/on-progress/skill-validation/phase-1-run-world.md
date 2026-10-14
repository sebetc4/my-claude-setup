# Phase 1: Run World

---

## Status

**Current Status:** 🟡 In Progress (20% — 1/5)
**Started:** 2026-10-14
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-run-world-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Run each case in the world the skill meets once installed, and show the grader what each
of the run's sessions had in context, as the design decided.

---

## Overview

### Why This Phase Matters
`close-session`'s case 3 ran without the hook its configuration declared, so eight
rewordings answered a world only the harness produces (V1). `harness.render` drops every
record but the turns, so the grader graded a true claim of `reviewing-delivered-code`
false (R1). A case is one session, so a workflow's last pass cannot be evaluated (R2).
A run with agents reports a duration and per-agent costs that are not what they seem
(R3), and ai-ctl recalibrated its estimate on them.

### What It Enables
Phase 2 judges outputs produced in a faithful world and read whole.

### Out of Scope
How a failure is classified and the pass criterion: Phase 2.

---

## Tasks

### Cases
- [x] Let a case declare its world, by the `hooks` key Phase 0's design gives `evals/evals.json`: the domain's `hooks.json` and hook files, installed in the run's folder as project hooks, each arm its version, the arm without the skill none; a hook turned off by the fixture's configuration; `workspace.py` validates the key and `run.py` installs the hooks
  Proof: test — a case with a SessionStart hook, its run's transcript holding the hook's line, and an invalid `hooks` refused, red before the code; a probe that a project SessionStart hook's output reaches a `claude -p` session under the harness's flags, dated, before relying on it
- [ ] Add to `references/evaluate.md` the check that a case's world is one the skill can meet: each hook, setting or tool the skill relies on, provided by the case or declared absent
  Proof: eval — a case of `authoring-skills`' own evals whose skill relies on a hook, with the previous version and the new one

### Grader's View
- [ ] Render each attachment a session starts with — instruction files, a hook's context — with its path and size, write it whole beside the run's files, and tell `skill-grader` where to read it
  Proof: test — a transcript fixture holding an `instructions` attachment and a hook's context, red before the code; then, with the user's leave, ai-ctl's iteration 2 run graded again on "Claims hold" as Phase 1 of `review-skill` wrote it

### Several Sessions
- [ ] Evaluate a workflow's later step, by the form the design chose: a case of several sessions in sequence over one working folder, each with its prompt and ceiling, graded once at the end, or a fixture holding the intermediate state, with `references/evaluate.md` saying how
  Proof: test — a case of two sessions, the second reading the first's output, red before the code; or eval, for the fixture form alone

### Figures
- [ ] Give a run with agents its exact figures: the wall duration from its start and end; each agent's output marked when it is shared by call count; `benchmark.py`'s footnote reading `output_source`; the effort note accepting the efforts the skill passes to its agents
  Proof: test — a `run.json` with agents and a benchmark over it, red before the code

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/scripts/harness.py
domains/skill-tooling/skills/authoring-skills/scripts/workspace.py
domains/skill-tooling/skills/authoring-skills/scripts/run.py
domains/skill-tooling/skills/authoring-skills/scripts/grade.py
domains/skill-tooling/skills/authoring-skills/scripts/benchmark.py
domains/skill-tooling/skills/authoring-skills/references/evaluate.md
domains/skill-tooling/skills/authoring-skills/references/eval-files.md
domains/skill-tooling/agents/skill-grader.md
domains/skill-tooling/skills/authoring-skills/evals/
domains/skill-tooling/tests/test_*.py
domains/skill-tooling/CHANGELOG.md
docs/claude-code-coupling.md
```

### Dependencies
Phase 0's design.

### Constraints
Scripts test-first. A change that adds a dependency on Claude Code — a transcript record,
a flag — updates `docs/claude-code-coupling.md` in the same commit.

---

## Acceptance Criteria

- [ ] A case can declare the context its skill relies on, and its runs hold it
- [ ] The grader reads each session's starting context
- [ ] A workflow's later step can be evaluated
- [ ] A run with agents reports its wall duration, and marks every figure that is estimated
