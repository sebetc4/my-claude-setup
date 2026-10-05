# Creating And Editing A Skill

The procedure for a new skill, then for a change to an existing one. Enter at the step
the user has reached — an intent already settled, scenarios already written, a draft to
test — and do first the earlier steps that are missing. Evaluation is skipped only when
the user chooses it, and that choice is recorded in the skill's evals.

## Creating A Skill

### 1. Size The Work To The Request

The deliverable is what the request asks for: a skill, with the evals that prove it.
Anything more — a hook, a script, a new domain, tests beyond the skill's evals — is a
proposal, given with what it would cost and built only on the user's yes. When the user
cannot answer, write the proposal down and deliver the smaller result.

### 2. Capture The Intent

Draw the answers from the conversation first, since a workflow just done in the session
is the most common source of a skill, then ask for what is missing:

- what the skill should let the agent do;
- when it should apply, in the words users would use;
- what a good result is: the output, its format, its success criteria;
- the edge cases, inputs and dependencies that matter.

Restate the rule or the behavior exactly as the user gave it, with its condition. A
stricter, broader or narrower version is a question for the user, never a choice made in
the skill: a skill that forbids what the user wanted asked about has changed the user's
rule.

### 3. Decide Whether A Skill Is The Answer

- A one-off task needs no skill: do the task.
- A rule that a script, a hook or a permission rule can enforce gets that guard, proposed
  under step 1; the skill holds only what the guard cannot decide.
- A convention or a procedure of one repository makes a repository skill; one that
  serves every project makes a global skill.

### 4. Choose The Kind

The kind sets the proof:

| Kind | Holds | Proof |
|---|---|---|
| Reference | Facts and conventions the agent applies to its work | An agent on a realistic task finds each key fact and applies it; never a test that reads the skill's own text back |
| Task | A procedure for one action, in steps | Output evals: realistic requests, run without the skill and with it |
| Discipline | A rule that must hold under pressure | Pressure scenarios, run without the skill first |

A technique, a concrete method with steps, is a task; a pattern, a way of thinking
applied to the work, is a reference.

### 5. Place It

Run `scripts/conventions.py skills` by its path in this skill's directory; on any status
but `ok`, follow `references/conventions.md`. `dirs` lists the folders that hold skills:
choose one and say why — a skill that serves only this repository goes where the
repository keeps its own skills, one meant for every project where its installable skills
live. The skill's evals go in its `evals` folder, and runs write under `workspace`.

### 6. Research

Read the repository first: its instruction file, the files the skill will act on, and
the skills it will sit beside. For a fact about a harness or a tool, read its official
documentation, link the page in the skill, and take only what the skill uses. Read
nothing outside the repository — other projects, session transcripts, home
directories — without the user's agreement.

### 7. Observe Before Writing

1. Write the scenarios first, in the skill's `evals/evals.json`: two or three realistic
   requests, worded as users would word them, each with the result it should produce.
2. Run each one without the skill — for an edit, with the previous version — by a fresh
   agent given a copy of the skill's folder without `evals/`, so that it cannot read the
   assertions, and no tool that loads skills, so that an installed copy cannot answer in
   place of the one under test.
3. Quote each failure as the run shows it, then write the assertions from the failures:
   each one a check that a reader settles from the output, named after what it checks.

When no run is possible — no agent can be started, or the user declines the runs — write
the scenarios first all the same, put in the skill only what the request states, and
record in the evals that no failure was observed yet.

### 8. Write The Minimum

Write only what answers the observed failures and what the request states, by
`references/writing-guide.md`. A failure that one line fixes gets one line.

### 9. Audit

Run `scripts/audit.py <skill-dir>` once the files are written, whatever wrote them: a
file written through a shell command escapes any audit hook. Fix each error and weigh
each warning.

### 10. Compare

Run the same scenarios with the skill, by fresh agents given its copy. Each failure is
gone, or recorded with the reason it stays. Run a scenario again after each fix, then
the whole set once all pass, so that no fix broke another. Finish one skill before the
next.

## Editing A Skill

Keep the skill's name: a rename breaks its invocations and every permission rule or file
that names it. Copy the previous version before the change: it is the baseline.

Each kind of change takes its proof:

| Change | Proof |
|---|---|
| New behavior, or a change meant to alter behavior | The target scenarios with the previous version, then with the new one |
| A script | Unit tests first, watched failing |
| The description | Queries that should and should not trigger the skill, written first, run before and after |
| Wording meant to keep behavior | The existing evals again, and a wording micro-test when the wording decides behavior |
| A fact in a reference | An agent finds the fact and applies it |
| A discipline skill | Pressure scenarios |
| A harness mechanism — permissions, injected commands, hooks | A probe before relying on it |
| No instruction changed: a typo, a link, formatting | The audit alone |

A wording micro-test compares wordings of one instruction: one fresh sample per call, a
control without the instruction, five samples or more per wording, and every flagged
match read; the spread between samples is a result too.

Improve from what the runs show:

- generalize from the feedback rather than fitting one example;
- cut what the runs did not need;
- read the runs' transcripts, not only their outputs;
- when every run wrote the same helper, bundle it in `scripts/`.

In Claude Code, a change to `SKILL.md` applies in the running session; a new top-level
skills folder needs `/reload-skills` before its skills appear.
