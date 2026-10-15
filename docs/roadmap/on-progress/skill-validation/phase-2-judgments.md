# Phase 2: Judgments

---

## Status

**Current Status:** 🟡 In Progress (86% — 6/7)
**Started:** 2026-10-15
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
Phase 3 releases the new judgments, and the two paused skills resume on a criterion
they can meet without bending.

### Out of Scope
Which failures count as evidence for a line of a skill: Phase 3. Where its sources go:
dropped on 2026-10-15 (`docs/decisions/2026-10-15-validation-weight.md`).

---

## Tasks

### Failures
- [x] Classify each failed assertion before any change by Phase 0's design, No Failure Stands and A Failure's Class — `skill` by default, `variance`, `grader`, `assertion`, `world`, `tool` —, an instrument's class only on the evidence its row lists and the user's yes, with a second grading of the failed assertions alone (`grade.py --again`), in the iteration's `classes.json`; the benchmark shows per iteration the share of instrument classes; only `skill` sends the fix to the skill
  Proof: test — the second grading, the recorded class and a class without its evidence refused, red before the code; eval — `references/evaluate.md`'s step, with the previous version and the new one
- [x] Add to `references/evaluate.md` the step taken when an instrument is suspected — the case's world, an assertion, the grader, the auditor, a figure —, stated as the classes' conditions and nothing more general: the fix goes to the instrument, then the skill's runs are judged again on it; Reading A Benchmark loses "check the assertion before the skill"
  Proof: eval — a case where a failure comes from the assertion, with the previous version and the new one

### Assertions
- [x] Give assertions their kinds — a guard, which must pass in every run; a discriminating check; a measure, which counts — in `evals/evals.json`, `benchmark.py` reading each kind its own way and never telling a guard to discriminate
  Proof: test — a benchmark over each kind, red before the code
- [x] Check an assertion over a list item by item, or as a count, so that one item's wording leaves the others' results standing
  Proof: test — a grading over a list with one item failing, red before the code
- [x] Keep premises out of assertions: `references/evaluate.md` puts a premise in the case's setup or prompt, and a scripted check in the skill's `evals/grade.py` where a path, a heading or a count settles the assertion
  Proof: eval — a case whose assertion carried a premise, with the previous version and the new one

### Criterion
- [x] Compute the pass criterion in rates, per assertion across the runs of one version, iterations sharing its snapshot pooled, and say in the benchmark whether it is met
  Proof: test — pooled iterations, a rate at the threshold and one below, red before the code

### Auditor
- [ ] Make `skill-auditor`'s verdict reproducible by Phase 0's design, The Auditor's Verdict: the request `references/audit.md` fixes word for word, `effort: medium` in its frontmatter, two passes started together, each point answered by the skill first and counting once the evals ran on a behavior-changing fix, the auditor at fault only on the evidence listed and the user's yes, line numbers from a numbered read of the one file
  Proof: check — two passes started together on `65ca91f`, and two on `authoring-skills` at its text of `5d7228a`, on the fixed request, each pair agreeing; the fixtures of `evals/auditor/` still getting their verdicts

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
Phase 1's report: the two `skill-auditor` passes of 2026-10-15 on `authoring-skills`, PASS
and FAIL on one text and one request, four of the FAIL's six lines past the end of their
file — evidence for the Auditor task.

### Constraints
Scripts test-first. The rule that a FAIL whose lines are answered never counts stands:
the auditor's verdict is made reproducible, not relaxed.

---

## Acceptance Criteria

- [ ] No step of the procedure sends a fix to the skill for a failure not classified as its defect
- [ ] The benchmark reads guards, discriminating checks and measures each its own way, and states whether the criterion is met
- [ ] The auditor's spread on a fixed version is within the design's threshold
