---
name: authoring-skills
description: Creates, edits and audits skills — a `SKILL.md` with its references, scripts, templates and evals — by the repository's conventions. Use when asked to write, create, change, fix, improve, review, audit or check a skill or its description, or to turn a workflow of the session into a skill.
---

# Authoring Skills

Create, edit and audit skills — a skill's `SKILL.md` and every file it cites — in any
repository, by that repository's conventions.

## The Conventions

Before creating or editing a skill, run `scripts/conventions.py skills`. On
`status: ok`, it prints the repository's `[skills]` table: the folders that hold skills,
the folder of a skill's evals, the workspace where eval runs write, and the features the
repository excludes, which the audit checks. On any other status, follow
`references/conventions.md` before going further.

## Rules For Every Operation

1. Guidance answers an observed failure. For a new skill or a change meant to alter
   behavior, first run the scenarios without it — for an edit, with the previous
   version —, then write only what answers the failures the runs show; when no run is
   possible, write only what the request states. Any other change takes the proof that
   `references/create-and-edit.md` lists for its kind.
2. The size of the work follows the size of the request: deliver what was asked. A hook,
   a script, a new domain or tests beyond the skill's evals are proposed with their
   cost, and built only on the user's yes.
3. After any write to a skill, whatever tool made it, run `scripts/audit.py <skill-dir>`
   and fix its errors: a file written through a shell command escapes an audit hook that
   matches the editing tools (https://code.claude.com/docs/en/hooks, § Matcher patterns).

## Routing

| Request | Operation | Read |
|---|---|---|
| Write a new skill, or turn a workflow of the session into one | Create | `references/create-and-edit.md`, which sends to `references/writing-guide.md`, to `references/discipline.md` for a skill that enforces a rule, and to a template under `assets/templates/` |
| Change a skill: its behavior, description, facts, scripts or wording | Edit | The Edit section of `references/create-and-edit.md`, then the parts of `references/writing-guide.md` the change touches |
| Audit, review or check a skill | Audit | `references/audit.md` |
| Write or fix the repository's `[skills]` table | — | `references/conventions.md` |
| Anything else | — | Nothing from this skill |

## Scripts

Run each as a command, by its path in this skill's folder and with no interpreter in
front: permission rules name the scripts and match the whole command
(https://code.claude.com/docs/en/permissions, § Bash). Run them rather than read their
code: the audit names each problem with its rule when it runs, after the writes.

- `scripts/audit.py <skill-dir>` audits a skill against the Agent Skills standard, the
  harness's rules and the repository's conventions, and exits 1 on an error; `--help`
  gives its options.
- `scripts/conventions.py skills` prints the repository's `[skills]` table, or what is
  wrong with the conventions file.
- `scripts/workspace.py <skill-dir>` validates the skill's `evals/evals.json`, naming
  each wrong key, and prepares the next iteration of its evals under the workspace;
  `--help` gives its options.
- `scripts/run.py <iteration>` lists the iteration's runs with their count and estimated
  cost; `--start` starts them as unattended sessions, each in a copy outside the
  repository, `--status` shows where each run stands, and `--stop` lets the runs going
  end and starts no other. Runs cost money: show the user that count and cost, and add
  `--start` only after their yes.
- `scripts/grade.py <iteration>` lists the iteration's complete runs left to grade, with
  the count and estimated cost of the grader sessions; `--start` runs the skill's own
  `evals/grade.py` first, when it exists, then grades the assertions left with the agent
  `skill-grader`. Its sessions cost money as the runs do: the same yes first.
- `scripts/benchmark.py <iteration>` sums up the graded runs per configuration — pass
  rate, duration, tokens and cost, with their deltas — and notes the assertions that do
  not tell the configurations apart or that vary, in the iteration's `benchmark.json`
  and `benchmark.md`; it starts no session.
- `scripts/viewer.py <iteration>` serves the review page — each run's prompt, output and
  grades, the case's review items, the benchmark — and saves the user's feedback to the
  iteration's `feedback.json`; it runs until stopped, so start it in the background and
  give the user its address. `--static <file>` writes the page instead, `--previous
  <iteration>` adds the earlier iteration's outputs and feedback.
- `scripts/triggers.py <skill-dir>` lists the trigger queries of `evals/evals.json` with
  the count and estimated cost of their sessions; `--start` runs each query in fresh
  unattended sessions, the skill's copy beside the user's other skills and never in the
  project's `.claude/`, and writes each query's trigger rate under the workspace;
  `--description <file>` measures another description. The same yes first.
- `scripts/tuning.py split <skill-dir>` divides the trigger queries into a training and a
  held-out set; `score` records the rates of a description that `triggers.py` measured;
  `propose` has a session without tools rewrite the description from the training
  results alone, the user's intent and feedback passed with `--notes` and no held-out
  query; `best` names the description to keep. `propose` starts a session: the same yes
  first, then measure its rewrite with `triggers.py --description`.
- `scripts/compare.py <iteration> [<other-iteration>]` compares blind the outputs of two
  versions — an iteration's two configurations, or the skill's arm of two iterations —
  for when the benchmark does not separate them: the agent `skill-comparator` judges
  each pair of runs three times, the outputs shown as A and B, and the verdicts are
  unblinded in the comparison's `comparison.md`. It lists the count and estimated cost of
  its sessions; `--start` starts them, after the same yes.

`references/eval-files.md` gives the keys of `evals/evals.json` and of every file these
scripts write: read it before writing a skill's evals, and to read a run, a grading or a
benchmark.
