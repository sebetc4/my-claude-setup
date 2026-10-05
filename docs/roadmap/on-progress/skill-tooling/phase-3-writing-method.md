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

### Baseline
- [ ] Choose three realistic skill-writing tasks, one per kind of skill — reference, task, discipline — with what a good result holds, get the user's approval, then give them to fresh subagents without the skill and record their failures verbatim
  Proof: eval — the without-skill half: the three tasks and what a good result holds, approved before the runs; each run by a fresh subagent with no skill and no Skill tool; its failures quoted in the report

### Design
- [ ] Write the design of the skill — operations, routing table, what each reference holds against the baseline's failures and the Phase 0 matrix, token budget of SKILL.md — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval
  Proof: review — the design, each reference tied to the baseline failures it answers and the matrix rows it carries, approved before any part of the skill is written

### Skill
- [ ] Write SKILL.md: when each operation applies, the conventions read through the Phase 1 reader, and the routing table, within the Phase 0 budget
  Proof: eval — one request per operation and one that is not about a skill, given to a fresh agent with SKILL.md alone, which names the reference it would read or none; Z1 reports no excess
- [ ] Write the create-and-edit reference: capture the intent, choose the kind of skill, place it per the repository's conventions, write the description and the body
  Proof: eval — the baseline failures it targets, named in the report before it is written, run again on that step with the skill, each gone
- [ ] Write the writing-guide reference: the description rule, the form-to-failure table, degrees of freedom, progressive disclosure, scripts and permissions, terminology, examples
  Proof: eval — the baseline failures it targets, named in the report before it is written, run again on that step with the skill, each gone
- [ ] Write the discipline reference: pressure scenarios, rationalization tables and red flags, for skills that enforce a rule
  Proof: eval — the discipline task's baseline failures, named in the report before it is written, run again with the skill, each gone
- [ ] Write the SKILL.md templates for each kind of skill — reference, task, discipline — under `assets/templates/`
  Proof: check — the roadmap skill's template rules run on `assets/templates/`, red on a template that breaks one, green on the three

### Agent
- [ ] Write the `skill-auditor` agent: read-only, it judges the description, the form of the guidance against the failure it targets, content the model already knows, terminology and degrees of freedom, and answers `VERDICT: PASS` or `VERDICT: FAIL` with one line per problem
  Proof: eval — the agent on a clean skill and on copies with planted problems, one per judgment it owns — a workflow in the description, emphasis with no observed failure, content the model knows, two terms for one thing, a fragile step left free —, its verdicts written before the runs

### Audit
- [ ] Write the audit reference: run the static audit, then the `skill-auditor` agent, then report the findings
  Proof: eval — a fresh agent asked to audit a skill holding one problem the rules catch and one only judgment catches runs the audit, then `skill-auditor`, and reports both

### Verification
- [ ] Run the three baseline tasks with the skill and compare with the recorded failures
  Proof: eval — the three baseline tasks with the skill, same prompts and model as the baseline, each recorded failure marked gone or still there
- [ ] Close the loopholes the runs revealed, run the failing tasks again, then the whole set once they pass
  Proof: eval — each task that still failed run again after its fix, until its failure is gone or the user rules on it, then the three tasks run again so that no fix broke another
- [ ] Pass the skill and the agent through the static audit and the `skill-auditor`
  Proof: check — `audit.py` on the skill and `make check` pass, then `skill-auditor` answers `VERDICT: PASS` on the skill and on the agent

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
