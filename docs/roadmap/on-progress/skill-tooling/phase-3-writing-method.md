# Phase 3: Writing Method

---

## Status

**Current Status:** 🟡 In Progress (0% — 0/12)
**Started:** 2026-10-04
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-static-audit.md` and `phase-2-static-audit-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-writing-method-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Write the skill that creates, edits and audits skills — a SKILL.md that routes to the
right operation, and references that merge the method of writing-skills, the best
practices and the official documentation — and the `skill-auditor` agent, which judges
what the static audit cannot.

---

## Overview

### Why This Phase Matters
This is the replacement proper: the method of writing-skills — watch the failure before
writing, match the form of the guidance to the failure — joined with the facts of the
platform, in one skill that follows its own rules.

### What It Enables
Skills are written and reviewed with one tool. Phase 4 adds the evaluation loop to it.

### Out of Scope
Evaluation tooling, in Phase 4.

---

## Tasks

### Design
- [ ] Write the design of the skill — operations, routing table, what each reference holds, token budget of SKILL.md — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval

### Baseline
- [ ] Give three realistic skill-writing tasks to fresh subagents without the skill, and record their failures verbatim

### Skill
- [ ] Write SKILL.md: when each operation applies, the conventions read through the Phase 1 reader, and the routing table, within the Phase 0 budget
- [ ] Write the create-and-edit reference: capture the intent, choose the kind of skill, place it per the repository's conventions, write the description and the body
- [ ] Write the writing-guide reference: the description rule, the form-to-failure table, degrees of freedom, progressive disclosure, scripts and permissions, terminology, examples
- [ ] Write the discipline reference: pressure scenarios, rationalization tables and red flags, for skills that enforce a rule
- [ ] Write the SKILL.md templates for each kind of skill — reference, task, discipline — under `assets/templates/`
- [ ] Write the audit reference: run the static audit, then the `skill-auditor` agent, then report the findings

### Agent
- [ ] Write the `skill-auditor` agent: read-only, it judges the description, the form of the guidance against the failure it targets, content the model already knows, terminology and degrees of freedom, and answers `VERDICT: PASS` or `VERDICT: FAIL` with one line per problem

### Verification
- [ ] Run the three baseline tasks with the skill and compare with the recorded failures
- [ ] Close the loopholes the runs revealed, then run the failing tasks again
- [ ] Pass the skill and the agent through the static audit and the `skill-auditor`

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/SKILL.md                 rewritten
domains/skill-tooling/skills/authoring-skills/references/*.md          new
domains/skill-tooling/skills/authoring-skills/assets/templates/*.md    new
domains/skill-tooling/agents/skill-auditor.md                          new
domains/skill-tooling/CHANGELOG.md
```

### Dependencies
Phase 0: the settled rules and the names. Phase 1: the reader. Phase 2: the static audit.

### Constraints
Skill files in English. References one level deep from SKILL.md, and no file under
`references/`, `assets/` or `scripts/` left uncited. Templates carry no HTML comment and
only UPPER_SNAKE_CASE placeholders: since Phase 2 these rules are the roadmap skill's own
`evals/checks.py`, so `authoring-skills` checks its templates the same way or by hand.
The skill already exists: Phase 2 wrote a short `SKILL.md` on the audit alone, with
`scripts/audit.py`, `frontmatter.py`, `conventions.py` and `references/conventions.md`;
this phase rewrites `SKILL.md`, the audit becoming one of its operations.

---

## Acceptance Criteria

- [ ] The skill and the agent pass the static audit and the `skill-auditor` with no problem
- [ ] SKILL.md fits the Phase 0 budget in lines and in tokens
- [ ] With the skill, the three baseline tasks no longer show the failures recorded without it
- [ ] Every writing capability marked keep or improve in the Phase 0 matrix is present in a reference
