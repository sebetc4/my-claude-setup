# Phase 2: Judgments

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-run-world.md` and `phase-1-run-world-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-judgments-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Change a skill only for a failure classified, with its evidence, as a defect of the
skill, and end a validation on a criterion that the instruments' measured spread does not
fail by chance, as the design decided.

---

## Overview

### Why This Phase Matters
`close-session` passed 106 assertions of 108, and its proof asked for all: the two
failures read as a grader's reading and a run's variance, yet the procedure offered no
step to say so, only a change to the skill (V2). Ten of fourteen auditor passes failed,
mostly on points other passes had let through on the same text, and one point the evals
later contradicted made the skill worse (V3). Graders re-derived an assertion's premise
wrongly (V6); guards were told to discriminate (R4); one item's wording failed a list of
eleven (R5).

### What It Enables
Phase 4 replays the recorded failures through the new judgments, and the two paused
skills resume on a criterion they can meet without bending.

### Out of Scope
Which failures count as evidence for a line of a skill, and where its sources go:
Phase 3.

---

## Tasks

### Failures
- [ ] Classify each failed assertion before any change — a defect of the skill, a run's variance, a grader's error, a defect of the assertion —, with its evidence and a second grading of the failed assertions alone, recorded where the design says; only a defect of the skill sends the fix to the skill
  Proof: test — the second grading and the recorded class, red before the code; eval — `references/evaluate.md`'s step, with the previous version and the new one
- [ ] Add to `references/evaluate.md` the step taken when an instrument is suspected — the case's world, an assertion, the grader, the auditor, a figure —: the fix goes to the validation and is recorded, the skill left as it is
  Proof: eval — a case where a failure comes from the assertion, with the previous version and the new one

### Assertions
- [ ] Give assertions their kinds — a guard, which must pass in every run; a discriminating check; a measure, which counts — in `evals/evals.json`, `benchmark.py` reading each kind its own way and never telling a guard to discriminate
  Proof: test — a benchmark over each kind, red before the code
- [ ] Check an assertion over a list item by item, or as a count, so that one item's wording leaves the others' results standing
  Proof: test — a grading over a list with one item failing, red before the code
- [ ] Keep premises out of assertions: `references/evaluate.md` puts a premise in the case's setup or prompt, and a scripted check in the skill's `evals/grade.py` where a path, a heading or a count settles the assertion
  Proof: eval — a case whose assertion carried a premise, with the previous version and the new one

### Criterion
- [ ] Compute the pass criterion in rates, per assertion across the runs of one version, iterations sharing its snapshot pooled, and say in the benchmark whether it is met
  Proof: test — pooled iterations, a rate at the threshold and one below, red before the code

### Auditor
- [ ] Make `skill-auditor`'s verdict reproducible by the design's rule, a point whose fix changes behavior counting once the evals ran on it
  Proof: check — Phase 0's measure repeated on the same fixed version, its spread within the design's threshold; the fixtures of `evals/auditor/` still getting their verdicts

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/scripts/grade.py
domains/skill-tooling/skills/authoring-skills/scripts/benchmark.py
domains/skill-tooling/skills/authoring-skills/scripts/workspace.py
domains/skill-tooling/skills/authoring-skills/references/evaluate.md
domains/skill-tooling/skills/authoring-skills/references/eval-files.md
domains/skill-tooling/skills/authoring-skills/references/create-and-edit.md
domains/skill-tooling/agents/skill-grader.md
domains/skill-tooling/agents/skill-auditor.md
domains/skill-tooling/skills/authoring-skills/evals/
domains/skill-tooling/tests/test_*.py
domains/skill-tooling/CHANGELOG.md
```

### Dependencies
Phase 1: the runs judged here hold their world and their starting context.

### Constraints
Scripts test-first. The rule that a FAIL whose lines are answered never counts stands:
the auditor's verdict is made reproducible, not relaxed.

---

## Acceptance Criteria

- [ ] No step of the procedure sends a fix to the skill for a failure not classified as its defect
- [ ] The benchmark reads guards, discriminating checks and measures each its own way, and states whether the criterion is met
- [ ] The auditor's spread on a fixed version is within the design's threshold
