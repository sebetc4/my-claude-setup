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

## Design

Approved by the user on 2026-10-05, as proposed. It answers the failures of the
baseline, B1 to B13 at the end of this section, and carries the rows of the
[2026-09-28 matrix](../../../decisions/2026-09-28-skill-tooling.md) that are writing
capabilities: rows S16, S18 to S23, S25 to S31 and S34 are Phase 4's evaluation tooling,
S32 and S33 Phase 2's audit, and the dropped rows carry nothing.

### Operations

| Request | Operation | Reads |
|---|---|---|
| Write a new skill, or turn a workflow of the conversation into one | create | `references/create-and-edit.md`, which sends to `references/writing-guide.md`, to `references/discipline.md` for a skill that enforces a rule, and to one template of `assets/templates/` |
| Change a skill: its behavior, description, facts, scripts or wording | edit | the Edit section of `references/create-and-edit.md`, and the parts of the writing guide the change touches |
| Audit, review or check a skill | audit | `references/audit.md` |
| Write or fix the `[skills]` table | — | `references/conventions.md`, unchanged |
| Anything else | — | nothing |

Phase 4 adds a fourth operation, evaluate, with its own reference.

`SKILL.md` holds, in this order: what the skill covers, in one line; the conventions,
read with `scripts/conventions.py skills` before a create or an edit; three rules that
hold for every operation, kept there so that they outlive compaction; the routing table;
the two scripts. The three rules:

1. Guidance answers an observed failure: nothing goes into a skill before a run without
   it has shown the gap, to the extent the Testing rule sets for the change.
2. The size of the work follows the size of the request: the deliverable is what was
   asked; a hook, a script, a new domain or tests beyond the skill's evals are proposed
   with their cost, and built on the user's yes.
3. After any write to a skill, whatever tool made it, `scripts/audit.py <skill-dir>`
   runs and its errors are fixed: a file written through Bash escapes the audit hook.

### References

**`references/create-and-edit.md`**, about 3,000 tokens, the procedure:

1. Scope: the deliverable sized to the request (B11).
2. Intent: the four questions, answered from the conversation first, then edge cases,
   formats, success criteria and dependencies; the rule or behavior restated as the user
   gave it, a stricter or broader version being a question (B8). Rows S2, S4, S5.
3. Whether a skill answers it: a one-off does not; a rule that a script, a hook or a
   permission rule can enforce gets that guard first, and the skill only what the guard
   cannot do; a global skill or a repository skill. Row W4.
4. The kind, which sets the template and the proof: a reference, whose facts are proved
   by an agent finding and applying them, never by a test that reads the text back
   (B2); a task, by output evals; a discipline skill, by pressure scenarios. Rows W3, W5.
5. The place: one of the conventions' `dirs`, given with its reason; evals in `evals`,
   runs in `workspace`. Rows W6, S14.
6. Research: the repository first; the harness's documentation linked, and taken only as
   far as the skill uses it; nothing outside the repository — other projects, session
   transcripts — without the user's agreement (B7, B13).
7. Observe before writing: the scenarios first, then each run without the skill — or
   with its previous version for an edit — by a fresh agent given a copy without
   `evals/` and no skill tool; failures quoted; `evals/evals.json` written from them,
   with assertions a reader can check. When no run is possible, the scenarios still come
   first, the skill holds only what the request states, and the gap is recorded (B1).
   Rows W1, S1, S13, S15, S17.
8. Write the minimum that answers the observed failures, from the template, by the
   writing guide.
9. Audit, rule 3 (B12).
10. Compare: the same scenarios with the skill, each failure gone or recorded; one skill
    at a time. Rows W26, S1.

Its Edit section: the name kept (S37); the proof each kind of change needs — the Testing
rule as a table, unit tests first for a script, the trigger queries first for a
description, a wording micro-test when a wording decides behavior (W2, W22) — plus one
line this design adds to that rule: a change that alters no instruction, a typo or a
link, needs the audit alone; improving from feedback — generalize, keep the text lean,
read the runs' transcripts, bundle a script every run rewrote (S24); a `SKILL.md` change
applies live in a session, a new skills folder needs a reload. A table of
rationalizations against skipping step 7 (W18) is added only if the Verification runs
still skip it with the skill.

**`references/writing-guide.md`**, about 4,000 tokens and under 300 lines, the rules of
form, which `skill-auditor` also judges against:

- Description: Description rules 1 to 7; the listing facts — cut at 1,536 characters,
  1% of the context, the least used dropped first, `disable-model-invocation`; keyword
  coverage (B3, B4, B5). Rows W9, W10, S6.
- What goes in: what an agent without the skill got wrong or cannot know, nothing else; a
  fact with its source; the official page linked, found through the `llms.txt` indexes,
  not copied; no narration, no history (B6, B7). Row W30.
- Form follows the failure: the Tone rules — the form-to-failure table, emphasis as a
  last resort, no nuance or exemption clause, a reason in one clause, imperative and
  positive, no persuasion. Rows W19, S11, S12.
- Degrees of freedom: free, a template or a parameterized script, or an exact script, by
  fragility (Tone rule 6).
- Structure: progressive disclosure, references one level deep, a table of contents from
  300 lines, one reference per variant, the instructions for the whole task first since
  compaction keeps 5,000 tokens, detail behind `--help`, cross-references over
  repetition. Rows W7, W12, W13, S7, S8, S9; the Size Budgets.
- Scripts and permissions: the Scripts rule; no surprise, the skill doing what its
  description says. Rows W17, S10.
- Terminology: one term per thing, in every file.
- Examples and templates: one runnable example; output templates; input and output
  examples; no version per language. Rows W16, W25.
- Names and citations: verb-first or gerund names, clear of the harness's built-ins;
  other skills cited by name, never by `@`. Rows W11, W14.
- Harness features, each marked as Claude Code's: `context: fork`, `paths`,
  `disallowed-tools`, `hooks`, substitutions, `ultrathink`; the conventions' `exclude`
  says which a repository refuses. The Platform Facts marked Phase 3.

The frontmatter facts of row W8 stay with the audit, which checks them.

**`references/discipline.md`**, about 2,000 tokens, for a skill that enforces a rule:

- A mechanical guard considered first; the user's condition kept as given (B8).
- Pressure scenarios before any rule, each combining three pressures or more and ending
  on a forced choice among concrete options, run without the skill (B9). Row W23.
- The rule in plain form: prohibition, condition, safe path (Tone rule 3).
- The rationalization table, the red flags and the description's symptoms quoted from
  the runs, never invented (B5, B10; Description rule 7). Row W20.
- Runs again with the skill, loopholes closed one at a time, the meta-test; emphasis
  only after plain wording failed in a run (Tone rule 4); a micro-test for a decisive
  wording (W22).

**`assets/templates/reference.md`, `task.md`, `discipline.md`**, about 300 tokens each:
`SKILL.md` skeletons with UPPER_SNAKE_CASE placeholders and no HTML comment. The
description slot takes the "what", then the "when" (B3, B5); a reference's facts each
with a source slot; a task's numbered steps each with its check; a discipline skill's
rule, condition and safe path, and a rationalization table whose rows come from runs
(B10). Rows W7, W16, S11. `evals/checks.py` loads the roadmap skill's `check_templates`
from that skill's `evals/checks.py`, so that one source holds the template rules; evals
stay in this repository, so the import never ships.

**`references/audit.md`**, about 800 tokens: `scripts/audit.py <skill-dir>`, then
`skill-auditor` given the skill's folder, the writing guide's path, the audit's output
and the skill's evals; one report, the audit's errors and warnings and then the agent's
problems, each with its fix; nothing fixed unless asked, a fix then being an edit. Where
no agent can be started, the agent running the audit applies the judgments itself and
says so. In Claude Code, `/skill-doctor` shows the skill's context cost and use, for the
user to run. Row S10.

Each tie to Claude Code that a file adds gets its row in `docs/claude-code-coupling.md`
in the same commit.

### The Agent

`domains/skill-tooling/agents/skill-auditor.md`, about 1,500 tokens, `tools: Read, Bash`
since the sessions have no `Grep` or `Glob`, `model: sonnet`. It changes nothing: its
commands list and read files. Given the skill's folder, the writing guide's path and the
static audit's output, it judges against the guide what no rule can: the description —
a workflow, an exclusion or a symptom no run showed, no "what"; the form of the guidance
against the failure it targets — emphasis or a prohibition that no failure in the
skill's evals calls for; content an agent does not need — what the model knows, a copied
source; terminology — two terms for one thing; degrees of freedom — a fragile step left
free, a free one over-constrained. It answers `VERDICT: PASS` or `VERDICT: FAIL`, then
one line per problem, `path:line: [judgment] problem — fix`, and leaves out what the
static audit reported. Its fixtures, a clean skill and one copy per planted problem, are
kept under `evals/` with other names than `SKILL.md`, so that the audit does not take
them for skills, and are copied into the workspace as skills for each run.

### Budget

`SKILL.md`: 1,500 tokens for its body by Z1's estimate, characters divided by four, and
under 100 lines; Z1's 5,000 stays the limit. The heaviest load, creating a discipline
skill — `SKILL.md`, create-and-edit, the writing guide, discipline, a template — comes to
about 11,000 tokens, each file read when its step comes, against 6,700 for
writing-skills' `SKILL.md` alone and 8,300 for skill-creator's; an audit, about 2,300.

### Order Of The Tasks

Written first, as planned, `SKILL.md` would cite references that do not exist yet: rule
R1 would fail `make check` at every commit until they do. A reference that `SKILL.md`
does not cite yet is unreached, rule R3. So each reference adds its row to the current
`SKILL.md` as it lands, and the `SKILL.md` task moves after the audit reference, where it
rewrites the file in full and runs its routing eval on the final table. The writing
guide comes first, since create-and-edit cites it. The order becomes: writing guide,
create-and-edit, discipline, templates, agent, audit reference, `SKILL.md`, then the
three Verification tasks.

### Evaluation And Its Cost

Every run on Sonnet with the baseline's preamble, its cost counted from its transcript:
calls, fresh input, cache reads, output.

- A reference is run on its own step: for the writing guide, each baseline task with its
  research handed over and only the `SKILL.md` asked for (B3 to B7); for create-and-edit,
  the three tasks, stopped once `SKILL.md` is written and audited (B1, B2, B8, B11, B12);
  for discipline, the discipline task alone (B5, B8 to B10).
- `SKILL.md`: one fresh agent per request, given `SKILL.md` alone and no tool.
- The agent: one run per fixture.
- Verification: the three tasks in full, once; each failing task again after its fix,
  then the three.

Measured besides each failure, on the full runs: the calls, cache reads and output
against the baseline's 48, 107 and 87 calls, and every deliverable that went past the
request without a question.

### Baseline Failures

| # | Failure | Run | Answered by |
|---|---|---|---|
| B1 | No failure observed before writing; evals written after the skill, from imagined scenarios | all three | create-and-edit, step 7; rule 1 |
| B2 | The skill's own text tested — examples parse, paths exist — in place of a check on an agent's use | reference | create-and-edit, step 4 |
| B3 | The description lists the steps | task, discipline | writing guide; templates; agent |
| B4 | Exclusions that no false trigger called for | task, reference | writing guide; agent |
| B5 | A description with no "what", and symptoms no run showed | discipline | writing guide; discipline; templates |
| B6 | The body explains what the model knows: semantic versioning, git | task | writing guide; agent |
| B7 | The official page restated for events the repository does not use | reference | writing guide; create-and-edit, step 6 |
| B8 | The rule asked for made stricter: no install even after a yes | discipline | create-and-edit, step 2; discipline |
| B9 | Pressure scenarios after the rules, two of seven carrying pressure | discipline | discipline |
| B10 | Rationalizations invented, no scenario run | discipline | discipline; templates |
| B11 | Work far past the request: a domain with a 646-line hook, 52 tests and fuzzing for one line | discipline | rule 2; create-and-edit, step 1 |
| B12 | Files written through Bash, unseen by the audit hook | discipline | rule 3 |
| B13 | Session transcripts read outside the repository, one command refused as personal data | reference | create-and-edit, step 6 |

Kept from the baseline and watched for regressions: the repository read before writing,
the place given with its reason, questions written with the assumption taken, a
mechanical guard considered first, a short `SKILL.md` over references, no emphasis.

---

## Tasks

### Baseline
- [x] Choose three realistic skill-writing tasks, one per kind of skill — reference, task, discipline — with what a good result holds, get the user's approval, then give them to fresh subagents without the skill and record their failures verbatim
  Proof: eval — the without-skill half: the three tasks and what a good result holds, approved before the runs; each run by a fresh subagent with no skill and no Skill tool; its failures quoted in the report

### Design
- [x] Write the design of the skill — operations, routing table, what each reference holds against the baseline's failures and the Phase 0 matrix, token budget of SKILL.md — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval
  Proof: review — the design, each reference tied to the baseline failures it answers and the matrix rows it carries, approved before any part of the skill is written

### Skill
- [x] Write the writing-guide reference: the description rule, the form-to-failure table, degrees of freedom, progressive disclosure, scripts and permissions, terminology, examples; cite it from the current `SKILL.md`
  Proof: eval — the baseline failures it targets, named in the report before it is written, run again on that step with the skill, each gone
- [x] Write the create-and-edit reference: capture the intent, choose the kind of skill, place it per the repository's conventions, write the description and the body; cite it from the current `SKILL.md`
  Proof: eval — the baseline failures it targets, named in the report before it is written, run again on that step with the skill, each gone
- [ ] Write the discipline reference: pressure scenarios, rationalization tables and red flags, for skills that enforce a rule; cite it from create-and-edit and the current `SKILL.md`
  Proof: eval — the discipline task's baseline failures, named in the report before it is written, run again with the skill, each gone
- [ ] Write the SKILL.md templates for each kind of skill — reference, task, discipline — under `assets/templates/`; cite them from create-and-edit
  Proof: check — the roadmap skill's template rules run on `assets/templates/`, red on a template that breaks one, green on the three

### Agent
- [ ] Write the `skill-auditor` agent: read-only, it judges the description, the form of the guidance against the failure it targets, content the model already knows, terminology and degrees of freedom, and answers `VERDICT: PASS` or `VERDICT: FAIL` with one line per problem
  Proof: eval — the agent on a clean skill and on copies with planted problems, one per judgment it owns — a workflow in the description, emphasis with no observed failure, content the model knows, two terms for one thing, a fragile step left free —, its verdicts written before the runs

### Audit
- [ ] Write the audit reference: run the static audit, then the `skill-auditor` agent, then report the findings; it replaces the audit section of the current `SKILL.md`
  Proof: eval — a fresh agent asked to audit a skill holding one problem the rules catch and one only judgment catches runs the audit, then `skill-auditor`, and reports both

### Routing
- [ ] Rewrite SKILL.md in full: when each operation applies, the conventions read through the Phase 1 reader, the three rules of the design, and the routing table, within the design's budget
  Proof: eval — one request per operation and one that is not about a skill, given to a fresh agent with SKILL.md alone, which names the reference it would read or none; Z1 reports no excess, and the body stays within 1,500 tokens

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
domains/skill-tooling/skills/authoring-skills/evals/evals.json         extended
domains/skill-tooling/skills/authoring-skills/evals/checks.py          new
domains/skill-tooling/skills/authoring-skills/evals/auditor/           new, the agent's fixtures
domains/skill-tooling/agents/skill-auditor.md                          new
domains/skill-tooling/CHANGELOG.md
docs/claude-code-coupling.md
docs/decisions/2026-09-28-skill-tooling.md                             one line of the Testing rule
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
