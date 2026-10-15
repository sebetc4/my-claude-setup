# Evaluating A Skill

Measure whether a skill, or a change to it, does better than its baseline. An output eval
runs the skill's cases, realistic requests, with the skill and without it, or with its
previous version, and grades what each run produced; a trigger eval runs queries to
measure whether the agent picks the skill from its description. The scripts hold the mechanics, each one's `--help` gives its
options, and `references/eval-files.md` gives `evals/evals.json` and every file they
write. The Agent Skills standard describes the same loop in its guides,
https://agentskills.io/skill-creation/evaluating-skills and
https://agentskills.io/skill-creation/optimizing-descriptions.

An evaluation runs the skill; an audit reads it. A request to evaluate, test, measure or
benchmark a skill or a change to it goes through the steps below, from the cases to the
announcement, even when no session can follow.

## What The Change Calls For

| Change | Evaluation | Baseline |
|---|---|---|
| A new skill | Output cases, and trigger queries | No skill: `without_skill`, `workspace.py`'s default |
| A change meant to alter behavior | Output cases whose result depends on the change | The previous version: `--baseline` with the commit before the change, or a copy made before it |
| The description | A trigger eval before and after, then tuning if it fails | The current description |
| Wording meant to keep behavior | The existing cases again | The previous version |
| A script, a typo, a link | No eval: unit tests, or the static audit alone | — |

The agent picks a skill from its name and description alone (specification § Progressive
disclosure): a change that leaves both as they were needs no trigger eval.

## The Cases

Write `evals/evals.json` first, or complete it for the change, and the skill's
`evals/grade.py` with it when an assertion below calls for one: both are the skill's
evals, written as part of the request, not a script proposed apart. Writing them,
preparing an iteration and listing its runs start no session and need no yes; only the
sessions do.

- Two or three output cases: realistic requests worded as users word them, each with its
  expected output; for a change, requests whose result depends on what changed.
- An assertion checks what its case sets out to measure, by the measure the skill's rule
  gives — a path, a heading, a value, a count, the writing guide's token budget —, never
  by a bare word such as "short" or "clear", which each grader reads its own way
  (my-agent-setup, roadmap `skill-tooling`: `phase-4-evaluation-tooling-report.md`,
  2026-10-08).
- An assertion settled by a path, a heading or a count is decided by the skill's
  `evals/grade.py`, which `grade.py --start` runs first, as `evals/grade.py <iteration>`
  from the repository's root: it writes into each complete run's `grading.json` the
  assertions it decides (`references/eval-files.md`, `grading.json`), and the grader
  gets the rest.
- An assertion, a guard included, checks what the run did, never what the session
  starts with: a file present, a note open, a line a hook prints is given by the case's
  setup, `files` or prompt, and no assertion states it. A grader re-deriving a premise
  from the run's files can read it wrongly and fail a run that did right (my-agent-setup,
  roadmap `skill-validation`: `phase-0-framing-report.md`, 2026-10-14).
- What only a person can judge — tone, whether the output reads as the user meant — goes
  under `review`: the review page shows it beside each output, and no grader judges it.
- The assertions come from the failures the runs without the skill showed
  (`references/create-and-edit.md`, step 7); before those runs, the expected output says
  what a good result is.
- A skill whose operation starts agents of its own lists their files under `agents`:
  each arm's runs get their version of them, the arm without the skill none, and every
  run may then use the Agent tool, in both arms, so that the baseline has the tools the
  skill's arm has; the baseline of an edit is then a git revision. Before the agents'
  files exist, as for the first runs of a new skill, `starts_agents: true` gives the runs
  the Agent tool alone. The grader reads each agent's run in the run's `agents/`
  (my-agent-setup, `docs/decisions/2026-10-13-eval-runs-with-agents.md`).
- A skill that relies on what its session starts with, such as the line a hook of its
  domain prints, has a case for each start the change depends on, one where nothing is
  printed among them, and each expected output says which start its run gets: the line,
  or none (my-agent-setup, roadmap `skill-validation`: `phase-1-run-world-report.md`,
  2026-10-14).
- A step a later session takes on what an earlier one left starts its case from that
  state as the earlier step really leaves it: the outputs of a recorded run of that step,
  copied by `evals/fixtures.py`, rather than files written for the case. Look for that
  run first, in the `outputs/` of the skill's iterations under the workspace
  (`references/eval-files.md`, The Workspace), in each case whose prompt takes that
  step. Only when no iteration holds one does the case write the state by hand, as the
  step leaves it, so that the first iteration runs every case (my-agent-setup,
  roadmap `skill-validation`: `phase-1-run-world-report.md`, 2026-10-14).
- About twenty trigger queries, half that should trigger and half near misses, each with
  `near`, what it nearly matches, all detailed as users write them: a simple one-step
  request may trigger no skill, the agent handling it alone, and an unrelated negative
  tests nothing (the standard's guide on optimizing descriptions).

## Model, Effort And Runs

- Each script sets its sessions' model and effort, by default the ones its `--help`
  names, never the session's own; name them to the user with the cost. Keep the default
  effort: the highest led by one assertion a task at most, within the spread between two
  runs, for 2.4 times the cost (my-agent-setup, `docs/decisions/2026-10-06-token-costs.md`
  § Effort, Measured). Raise it with `--effort` only for a measure that needs that margin.
- Three runs per case and configuration in a benchmark; one per case to observe the
  baseline before the skill is written; three sessions per trigger query; three per pair
  in a blind comparison, whose verdict counts when two agree. A judgment varies from one
  session to the next (my-agent-setup, roadmap `skill-tooling`:
  `phase-3-writing-method-report.md`, 2026-10-06).
- With no run of the skill recorded, `run.py` estimates each run at a full skill-writing
  task's cost, and a skill with agents at the run's ceiling, its agents' spend included:
  cap the runs and their estimate with `workspace.py --budget`.

## The Announcement

`run.py`, `grade.py`, `triggers.py`, `tuning.py propose` and `compare.py` each list the
sessions they would start, with their count and estimated cost, and start nothing
without `--start`. Show that line to the user with the model and effort, and add
`--start` after their yes, one step per yes. When no one can answer, stop there: say what
is prepared and what the yes would start. `run.py --stop` lets the run going end and
starts no other.

## The Loop

1. `workspace.py <skill-dir>` prepares the next iteration: `--baseline` for an edit,
   `--reuse <iteration>` to take the baseline's runs when its cases did not change.
2. `run.py`, then `grade.py`, then `grade.py --again`, each listed, then started after
   the yes: `--again` grades `with_skill`'s failed assertions a second time and enters
   each failure in the iteration's `classes.json` as `skill`.
3. Class each failure, by Classing A Failure below, before any change to the skill or
   to its evals.
4. `benchmark.py`.
5. `viewer.py`, with `--previous` from the second iteration on: the user reads the
   outputs beside their review items and writes feedback.
6. Improve the skill from the failures classed `skill`, the benchmark's notes and the
   feedback, by the Edit section of `references/create-and-edit.md`, then prepare the
   next iteration.

Stop when the benchmark's criterion is met and the user is satisfied, or when an
iteration gains nothing on the one before.

## Classing A Failure

A failure of `with_skill` keeps the class `skill` unless the evidence of another class,
as `references/eval-files.md` gives it under `classes.json`, is in the runs' files. Write
each class with its evidence in `classes.json` before changing anything. Propose an
instrument's class — `grader`, `assertion`, `world`, `tool` — to the user with its
evidence and what its yes would start: the fix the table below gives, and the sessions
that fix calls for, with their count and estimated cost. Write their yes in its `yes`; until that yes, change
neither the instrument nor the skill for that failure, and when no one can answer, stop
there with that proposal.

Each class then sends its fix:

| Class | Fix |
|---|---|
| `skill` | The skill, by step 6 of The Loop |
| `variance` | None at once: the criterion counts it, and asks for more runs on the same snapshot when it needs them (`workspace.py --extend`) |
| `grader` | None: the benchmark reads the second reading in place of the first |
| `assertion` | The assertion in `evals/evals.json`; then `workspace.py --assertions <iteration>` and `grade.py <iteration>` grade every run of both configurations again on it: one grader session per run, their count and estimated cost given with the proposal, at the grading's cost per run of the iteration's `benchmark.md`; started after the yes |
| `world` | The case's setup, `files` or fixture; then the case's runs again, in the next iteration |
| `tool` | The script or the agent, in its repository; then the runs judged again by it |

## Reading A Benchmark

- Set the pass-rate delta beside the cost delta.
- An assertion under `assertions` with one result in every run of both configurations
  does not tell them apart: sharpen it or drop it. An assertion whose result varies within a
  configuration: read those runs' transcripts, not only their outputs.
- An assertion the grader named weak in most gradings gets its measure; a flag in one
  grading of several is the grader's own spread.
- When the benchmark does not separate two versions, compare them blind:
  `compare.py <iteration>` for an edit's two configurations, `compare.py <iteration>
  <other-iteration>` for two iterations, then read `comparison.md`.

## Reading Trigger Rates

- A query passes at a rate of 0.5 or more when it should trigger, below 0.5 when it
  should not; one session in three either way sits at the threshold.
- Missed queries that should trigger widen the description's situations, in the users'
  words; a near miss that triggers calls for a more specific description first, then an
  exclusion (`references/writing-guide.md`, The Description).
- Change the description by measure, with `tuning.py`: `split` once; `score` each
  description from a `triggers.py` results file, the current one first; `propose` a
  rewrite, with `--notes` carrying the user's intent and feedback and never a query;
  measure it with `triggers.py --description` on every query, then `score` it; `best`
  names the description to keep, the best on the held-out queries. With far fewer than
  twenty queries the held-out set is too small to choose by: write more first.
