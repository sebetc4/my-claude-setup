# Phase 3: Evidence And Sources

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-2-judgments.md` and `phase-2-judgments-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-3-evidence-and-sources-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Let a line of a skill rest on the evidence that justified it, from runs, real sessions or
a study, and keep each source where the auditor and the next editor read it rather than
in the text loaded at every use, as the design decided.

---

## Overview

### Why This Phase Matters
`close-session` lost two prohibitions drawn from real transcripts because no baseline
reproduced them (V5), and `reviewing-delivered-code` lost three blocks drawn from a study
of nine plugins (R6). Both skills now cite this repository's or ai-ctl's paths that no
run opens and every run pays for, put there for the auditor (V4).

### What It Enables
Phase 4 revalidates the two skills with their real-use evidence admitted and their
sources out of their runtime text.

### Out of Scope
The judgments of failures and the criterion: Phase 2.

---

## Tasks

### Evidence
- [ ] Record failures seen in real use in `evals/evals.json`, by the key the design gives, each with its transcript or study reference; `workspace.py` validates it and `references/eval-files.md` gives it
  Proof: test — a valid entry and an entry without its reference refused, red before the code
- [ ] Accept a failure seen in real use as grounds for a prohibition, in the writing guide's The Form Follows The Failure and in `skill-auditor`'s form judgment
  Proof: check — two fixtures under `evals/auditor/`, a prohibition grounded in a real-use failure alone passing and one grounded in nothing failing, each run three times

### Sources
- [ ] Keep a source the agent never opens out of the skill's runtime text, in the place the design gave it, and need no source for a fact the agent observes in its own context, in the writing guide's What Goes In and in `skill-auditor`'s content judgment
  Proof: check — fixtures under `evals/auditor/`, a source in its place passing and a runtime citation of a repository path failing, each run three times
- [ ] Make `audit.py` accept the sources' place: the rule that every file of a skill but `evals/` is reached from `SKILL.md`, and the rule refusing a skill-local path to another skill's file, as the design settles them
  Proof: test — a skill with its sources in their place, audited clean, red before the code; or the audit's tests unchanged when the place needs no rule changed

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/references/writing-guide.md
domains/skill-tooling/skills/authoring-skills/references/create-and-edit.md
domains/skill-tooling/skills/authoring-skills/references/eval-files.md
domains/skill-tooling/skills/authoring-skills/scripts/workspace.py
domains/skill-tooling/skills/authoring-skills/scripts/audit.py
domains/skill-tooling/agents/skill-auditor.md
domains/skill-tooling/skills/authoring-skills/evals/auditor/
domains/skill-tooling/tests/test_*.py
domains/skill-tooling/CHANGELOG.md
docs/decisions/2026-10-03-skill-audit-rules.md
```

### Dependencies
Phase 2's auditor: the fixtures added here run against its new verdict rule.

### Constraints
Scripts test-first. A change to an audit rule updates the rule catalogue it comes from.

---

## Acceptance Criteria

- [ ] A failure seen in real use, with its reference, grounds a prohibition the auditor accepts
- [ ] A skill's sources sit outside its runtime text, and the audit and the auditor accept them there
