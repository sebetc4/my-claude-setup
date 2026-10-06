# Phase 4: Evaluation Tooling

---

## Status

**Current Status:** 🟡 In Progress (0% — 0/12)
**Started:** 2026-10-06
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-writing-method.md` and `phase-3-writing-method-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-evaluation-tooling-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Give the skill the evaluation loop of skill-creator, improved: output evals with and
without the skill in subagents, grading, benchmark and human review; trigger evals in
fresh `claude -p` sessions; description tuning; and blind comparison, which Phase 0 kept
as an option for when the benchmark does not separate two versions.

---

## Overview

### Why This Phase Matters
A skill that triggers shows that Claude found it, not that it helps. The official
documentation asks for two separate measures against a baseline: whether Claude invokes
the skill when it should, and whether the output is what was intended. The roadmap
evals and Phase 3's runs have already shown several traps:
- an installed copy shadows the skill under test;
- a run that can read `evals/` sees the assertions, even when its prompt forbids the
  folder;
- an agent's verdict varies from run to run;
- runs take the session's effort, which makes them costly when it is `max`.

### What It Enables
Any skill, the new one included, can show that it beats its baseline. Phase 5 moves the
roadmap evals onto this tooling.

### Out of Scope
`claude plugin eval` and its format; `.skill` packaging.

---

## Design

Approved by the user on 2026-10-06, as proposed, and amended the same day with the user's
approval after task 2's probe: the session flags of Runs, the grader's model and effort,
the trigger sessions, the constraints answered and the trigger estimate. It carries the rows of the
[2026-09-28 matrix](../../../decisions/2026-09-28-skill-tooling.md) that Phase 3 left to
this phase — S13 to S16, S18 to S23, S25 to S31 and S34 —, the remainder of S17, W5's map
of case types and W23's pressure scenarios, and it answers each constraint of this phase
(Constraints Answered). One decision comes first: output runs start `claude -p`
sessions, not subagents (the user, 2026-10-06). The Agent tool sets no effort, a
definition that does must be installed first, and a subagent's transcript does not hold
its output tokens; `claude -p` takes the model, the effort and a cost ceiling as flags,
and a main session's transcript holds its output.

### The Operation

`SKILL.md` gains a fourth row, Evaluate — run a skill's evals, measure its triggering,
tune its description, compare two versions — which reads `references/evaluate.md`.
create-and-edit's step 7 (observe before writing), its step 10 (compare) and the Edit
table's proofs that run scenarios or trigger queries send to it. The reference holds the
procedure; scripts hold the mechanics, so that a run's conditions never depend on an
agent following prose:

| Script | Does | Task |
|---|---|---|
| `scripts/usage.py` | A session's tokens, cost, models and effort from its transcript; the copy of `shared/usage/usage.py` | 3 |
| `scripts/workspace.py` | Prepares an iteration | 4 |
| `scripts/harness.py` | Builds, starts and reads `claude -p` sessions; imported by the others, the one script that knows the harness's command line | 5 |
| `scripts/run.py` | Lists an iteration's runs with their count and estimated cost; starts them with `--start` | 5 |
| `scripts/guard.py` | The hook that keeps a run inside its copy | 5 |
| `scripts/grade.py` | Grades an iteration: the skill's `evals/grade.py`, then `skill-grader` | 7 |
| `scripts/benchmark.py` | `benchmark.json` and `benchmark.md` | 8 |
| `scripts/viewer.py`, `assets/viewer.html` | The review page, adapted from skill-creator | 10 |
| `scripts/triggers.py` | Trigger rates per query | 11 |
| `scripts/tuning.py` | Splits the queries, scores descriptions, picks the best | 12 |
| `scripts/compare.py` | Blind pairs, `skill-comparator` sessions, unblinding | 13 |

Every script that starts sessions prints first how many and their estimated cost, and
starts nothing without `--start`: the agent shows that line to the user and waits for a
yes.

### `evals/evals.json`

```json
{
  "skill_name": "releasing-domains",
  "env": {"CLAUDE_DIR": "{tmp}/claude"},
  "evals": [
    {
      "id": 1,
      "name": "release-a-minor-change",
      "kind": "task",
      "setup": "repository",
      "exclude": ["docs/roadmap/"],
      "prompt": "…",
      "files": [],
      "expected_output": "…",
      "assertions": ["…"],
      "review": ["…"],
      "pressures": [],
      "failures_without_skill": ["… (run of 2026-10-06)"],
      "failures_with_skill": [],
      "pending": "…"
    }
  ],
  "triggers": [
    {"query": "…", "should_trigger": true},
    {"query": "…", "should_trigger": false, "near": "…"}
  ]
}
```

- `kind`: `reference`, `task` or `discipline`, create-and-edit's kinds (row W5).
- `setup`: where a run works. `repository`, a copy of the repository the skill is
  evaluated in; `empty`, an empty folder holding `files`; `fixture`, a folder the skill's
  `evals/fixtures.py <name> <folder>` builds, as the roadmap evals build theirs.
- `exclude`: paths left out of a `repository` copy besides the skill's `evals/`, which is
  always left out: documents that would give the answer away, such as a roadmap that
  records the expected results.
- `env`: variables set for every run, `{tmp}` being the run's temporary folder: here
  `CLAUDE_DIR`, which the Makefile reads (`CLAUDE_DIR ?= $(HOME)/.claude`), so that a run
  that installs writes into its own folder.
- `assertions`: checks a reader settles from the output and the transcript, each named
  after what it checks (S17). `review`: what only a person can judge — a description's
  tone, whether a rule reads as the user meant it —, shown beside the output in the
  viewer and never graded (S17's remainder).
- `pressures`: a discipline case's combined pressures (W23); its forced choice is in the
  prompt.
- `failures_without_skill`, `failures_with_skill`: failures quoted from runs, each with
  its run and date, the evidence create-and-edit's step 7 asks for and `skill-auditor`
  reads; `pending`, what no run has shown yet and why. These settle the keys Phase 3's
  runs added on their own.
- `triggers`: about twenty queries, half that should trigger and half near misses that
  should not, `near` naming what a near miss nearly matches (S27, S31, the standard's
  guide on optimizing descriptions); reviewed in the file, not through a browser
  download (S28).

`workspace.py` validates the file and refuses an unknown key or a wrong type, naming it.
The other files' schemas — `iteration.json`, `run.json`, `grading.json`,
`benchmark.json`, `tuning.json` — go in `references/eval-files.md`, the contract between
the scripts and the viewer (S34).

### Workspace

Under the `[skills]` table's `workspace`, in `skills/<skill-name>/` (S14), one folder
per iteration (S25):

```
<workspace>/skills/<skill-name>/
  iteration-1/
    iteration.json              cases, configurations, runs each, model, effort, budget, digests
    base.tar                    the repository copy, for setup `repository`
    with_skill/<skill-name>/    the skill without evals/
    old_skill/<skill-name>/     the previous version without evals/, for an edit
    <case-name>/
      eval_metadata.json        id, name, prompt, assertions, review (S16), digest
      files/                    the case's files, at their paths in the skill
      fixture.tar               for setup `fixture`, what `evals/fixtures.py` built
      with_skill/run-1/
        outputs/                files the run added or changed, at their paths; response.md
        changes.json            added, modified, deleted
        run.json                session, status, claude version, models and effort used, tokens, cost, duration, refusals
        transcript.jsonl        the session's transcript, copied: it outlives Claude Code's 30 days
        transcript.md           the calls in order, for the grader and the viewer
        grading.json
      without_skill/run-1/ …
    benchmark.json, benchmark.md, feedback.json
  triggers/<date-time>.json
  tuning/
```

- Configurations: `with_skill` and `without_skill` for a new skill; `with_skill` and
  `old_skill` for an edit, from `--baseline <git revision or folder>` (S15). A
  `without_skill` baseline does not change between iterations: `--reuse <iteration>`
  takes its runs instead of paying for them again.
- `base.tar`: the repository's tracked files and untracked files that git does not
  ignore, as they are on disk, plus `.agent-conventions.toml`, minus the skill's whole
  folder and the workspace. An archive, so that the iteration's base stays fixed and no
  session loads the `CLAUDE.md` inside it. A run leaves out the case's `exclude` when it
  extracts the archive, and puts its arm's version of the skill back at its path: the
  current one for `with_skill`, the baseline for `old_skill`, none for `without_skill`,
  so that no baseline reads the version under test (the user, 2026-10-06, task 4).
- A case's fixture is built once, when the iteration is prepared, and each run extracts
  it. The claude version goes in each `run.json`, not in `iteration.json`: the binary
  can change between the runs of one iteration, as it did on 2026-10-06.
- `--reuse` takes a baseline run when the case's digest — its prompt, setup, `exclude`,
  `env`, files, base and fixture, not its assertions — the model, the effort and the
  baseline's snapshot are the same; its `grading.json` is left behind.

### Runs

`run.py <iteration>` lists the runs to start — case, configuration, number — with their
count and estimated cost; with `--start`, it starts them, `--jobs` at a time (4 by
default), and prints one line per run as it ends. Each run:

1. A temporary folder outside any repository — `run.py` never sets `TMPDIR`, and refuses
   a temporary folder with `.git` or `.agent-conventions.toml` among its ancestors —
   holding `work/`, extracted from `base.tar` with the arm's version of the skill put
   back, extracted from the case's `fixture.tar`, or empty with the case's `files`, then
   made a git repository of one commit; and, for a skill's arm, `skill/<skill-name>/`.
2. `claude -p` started in `work/` with:
   - `--model` and `--effort` from `iteration.json`, the model named by its full id
     (`claude-sonnet-5-5`), since an alias follows the binary's version;
   - `--max-budget-usd`, the per-run ceiling;
   - `--disallowed-tools Skill Agent`, so that no installed skill answers in place of
     the copy and no run starts others;
   - `--add-dir` for the skill's copy;
   - `--permission-mode auto` and `--permission-prompts none`, so that a call that would
     wait for a person is refused instead;
   - `--setting-sources project,local`, which leaves out the user's layer — hooks,
     personal skills, agents, permission rules, model settings — while the project's
     own hooks still run, as part of the repository the skill serves; `disableAllHooks`
     cannot serve, since it also turns off the hooks `--settings` adds;
   - `--strict-mcp-config`, which keeps out the claude.ai connectors, loaded in some
     sessions and not in others;
   - `--settings` adding `guard.py`, below;
   - `--output-format json`;
   - the file's `env`, without any `CLAUDE*` variable of the session that starts it but
     `CLAUDE_CONFIG_DIR`, which names the user's configuration and credentials:
     `CLAUDECODE` refuses a nested session, `CLAUDE_EFFORT` carries its effort, and
     `CLAUDE_CODE_SESSION_ATTENDED=1` would make the run's hooks act as in an attended
     session.

   `harness.py` refuses a `claude` older than 2.1.291, the version task 2's probe
   validated: 2.1.283 did not know `claude-sonnet-5-5`, priced it as unknown and ignored
   the effort.
3. The prompt, from a file: a preamble, `---`, then the case's prompt. The preamble keeps
   Phase 3's limits that no flag enforces: the user cannot answer, so questions are
   written with the assumption taken; no `claude` session is started; the run ends on an
   account of what it did. A skill's arm adds "Use the skill `<name>`, whose copy is at
   `<path>`: read its `SKILL.md` and follow it." Phase 3's lines on where to write and
   what not to read go: the copy enforces both.
4. At the end: the json result, the transcript copied and rendered, the outputs and
   changes against the base, `run.json`. A run stopped by its budget, the subscription's
   limit or an error is marked so; the next `--start` starts it again from a fresh copy
   and skips the complete runs. Phase 3's runs stopped on the limit four times.

`guard.py`, a PreToolUse hook given to runs only, refuses a call that names the real
repository's root or the real `~/.claude`, with "outside the test's limits", and
`run.json` keeps each refusal. It puts the skill's evals out of reach beyond the copy,
where Phase 3's runs found them through `grep`, and the real `~/.claude` out of reach of
a baseline run that would install, the discipline case's subject.

Model and effort until task 9 sets them: Sonnet 5.5, the model of Phase 3's runs, at
half Opus 5.5's prices, and `xhigh`, Claude Code's default and the setting the
`claude-api` skill names best for agentic work. Both are stored in `iteration.json`, and
`run.json` records the model and effort of every call read back from the transcript, a
session being able to run on another model than the one asked. The estimated cost is the
mean of the same skill's complete runs at that model and effort; with none, $2.50 a full
task, Phase 3's mean at `max`, said as such. The default ceiling is $5 a run.

### Counting

`shared/usage/usage.py`, copied into `authoring-skills/scripts/` by `make shared`, where
roadmap `token-usage` extends it for the review domain (its Phase 1). It counts one usage
per `message.id`, the last record kept; prices each model from a table dated as
`docs/decisions/2026-10-06-token-costs.md` gives it, a model the table lacks being priced
as unknown, never zero, and each cache write by its lifetime; reads each call's model and
effort; and counts the output of a call whose last record carries a `stop_reason`, as
every call of a main session does, while a call without one, as most of a subagent's,
is estimated and marked (task 3). A run is a main session,
so its output is counted; `run.json` also keeps the cost the json result reports, as a
cross-check (S18: the transcript first, the harness's own figure as the fallback).

### Grading

`grade.py <iteration>`, for each run without a `grading.json`:

1. The skill's `evals/grade.py <iteration>`, when it exists (S20), writes the assertions
   it decides and may leave others out. A non-zero exit stops the grading with its
   message.
2. `skill-grader` grades the assertions left, from the case's assertions, the run's
   `outputs/`, `transcript.md` and `response.md`. A pass needs evidence of real
   completion; the grader checks the claims of the run's closing account against the
   files, and names each assertion a wrong output would also pass (S19). Read-only,
   `tools: Read, Bash`, `model: sonnet`, its `effort` in its file.
3. `grading.json`: `assertions`, each with its text, `passed`, `evidence` and `by`,
   `script` or `grader`; `summary`; `weak`; `claims`. One term, "assertions", from
   `evals.json` to the viewer, where skill-creator's files say "expectations".

The grader stays an agent, installed with the domain like `skill-auditor`. `grade.py`
starts it as a `claude -p` session running that agent (`--agents`, `--agent`), with the
flags of a run, so that its model, effort and cost are set and counted like a run's,
whether or not the domain is installed. It passes `--model` and `--effort` read from the
agent's frontmatter: a session started with `--agent` takes the agent's model but not
its effort (task 2), and `compare.py` does the same for `skill-comparator`. It finds the agent's file at `../../agents/` from the skill's folder, true
in the repository and once installed.

### How Many Runs

An agent's verdict varies between runs: on an unchanged file, `skill-auditor` reported
one problem, then three, then four. So:

- A verdict that decides alone — a blind comparison, a proof's grading — takes three
  runs; it counts when two agree, and the split is reported.
- In a benchmark, each run is graded once: three runs per case and configuration
  already sample the spread (S21's deviation needs several), and an assertion graded
  differently across runs shows in its pass rate.
- Observing a baseline before writing takes one run per case (create-and-edit's step 7):
  its failures are quoted, not averaged.
- A trigger query takes three runs, its rate set against 0.5, as the standard's guide
  does.

### Benchmark

`benchmark.py <iteration>` writes `benchmark.json` and `benchmark.md` (S21): per
configuration, the pass rate, duration, fresh input, cache reads and writes, output and
cost, each with mean, standard deviation, minimum and maximum, and the delta between
configurations; the model and effort of each run. A run whose output is estimated is
marked, never counted as zero. Its notes are computed rather than left to an analyst
agent (S22): assertions with the same result in every run of both configurations, which
do not discriminate; assertions whose result varies within a configuration; and the cost
delta beside the pass-rate delta.

### Review

`viewer.py <iteration> [--previous <iteration>] [--static <file>]`, adapted from
skill-creator's `eval-viewer/` (S23), its Apache 2.0 notice kept and the adapted files
listed in `NOTICE`. The Outputs tab shows each run's prompt, outputs, response and
grades, with the case's `review` items beside the feedback box; the Benchmark tab adds
cost, model and effort; feedback goes to the iteration's `feedback.json`, which the next
iteration reads (S25).

### Trigger Evals And Description Tuning

`triggers.py <skill-dir> [--description <file>] [--start]`, from the `triggers` of
`evals.json` (S29):

- The skill is copied into a temporary folder as `.claude/skills/<name>/`, with the given
  description when there is one, and passed with `--add-dir`, never written into the
  project's `.claude/`. The user's other personal skills are copied beside it, so that
  the listing stays the user's while the installed copy of the skill under test, which
  would shadow the copy, stays out.
- Each session starts in a copy of the repository, as an output run does: a query about
  "this repository" finds one, and nothing is written into the real one. It takes a
  run's flags but `--disallowed-tools`: `--setting-sources project,local` leaves out
  the user's hooks, this setup's SessionStart line among them, and the personal skills;
  the project's own hooks stay.
- `--settings` adds a PostToolUse hook that records each call and returns
  `{"continue": false}` once the session triggered or at its third call; the session
  otherwise ends with its first turn. Killing the process instead loses the transcript's
  tail (task 2).
- A session counts as triggered when it calls the Skill tool on the skill or reads a
  file under the copy's path within its first three tool calls, where S29 counted the
  first only. A read of the skill's source in the repository copy, which a session can
  reach, is recorded beside the rate, not counted.
- Model and effort: those of the sessions the skill serves, Opus 5.5 at `xhigh` by
  default, recorded with the results.
- The count, queries × runs, and the estimated cost are printed first. A query's runs
  follow one another in one folder, so that the second and third read the first's
  context from the cache, $0.008 against $0.09 on Opus 5.5 (task 2); different queries
  share only the system prompt and the tools, and run in parallel in their own folders.

`tuning.py` (S30, as Phase 0 decided): `split` divides the queries 60/40 with a fixed
seed, both classes in each set; `score` records a description's rates on both sets in
`tuning.json`; `best` returns the best on the held-out set, a tie going to the shorter.
The session proposes each rewrite from the training failures only, the held-out queries
kept from it so that the rewrite cannot fit them; five rewrites at most, fewer when two
in a row gain nothing.

### Blind Comparison

`compare.py <iteration-a> <iteration-b> [--case <name>]` (S26), for when the benchmark
does not separate two versions: it pairs each case's outputs of the two versions, labels
them A and B at random, keeps the key outside what the comparator reads, and starts
`skill-comparator` three times per pair. The comparator, given the prompt, the expected
output, the assertions and both outputs, names the better one, scores both against the
assertions and on correctness, completeness and form, and says why; after unblinding,
its reasons are mapped to the versions. skill-creator's analyzer is not kept as an
agent: its benchmark part is the computed notes, and its reading of transcripts is the
reference's "read the transcripts, not only the outputs" (S24).

### The Reference

`references/evaluate.md`: when to evaluate, by the Testing rule and the Edit table; how
many cases, two or three output cases and about twenty trigger queries; which baseline,
none for a new skill and the previous version for an edit; the announcement, the
script's count and cost shown before `--start`; model and effort, set and never the
session's; the loop — prepare, start, grade, benchmark, review, improve, next
iteration — and its stops: the user is satisfied, the feedback is empty, or an iteration
gains nothing (S25); how to read a benchmark and trigger rates; which checks stay
assertions and which go to `review` (S17); blind comparison when the benchmark does not
separate two versions. Fixtures: a small sample skill under `evals/sample/`, its files
named other than `SKILL.md` so that the audit does not take them for a skill, whose cases
work in an empty folder and cost little; the tests and the acceptance criteria run on
it.

### Constraints Answered

| Constraint | Answer |
|---|---|
| Standard library only | Every script; the tests use a stub standing for `claude` |
| Count and cost before any session starts | Printed by every script that starts sessions, nothing started without `--start` |
| Write refuses report-named files in a subagent | Runs are main sessions; task 2 wrote `summary.md` with Write |
| An Edit under `.claude/` waits in a headless run | Under `auto` with `--permission-prompts none`, task 2 wrote and edited a file under `.claude/skills/` without waiting |
| `TMPDIR` inside the repository breaks five tests | The scripts leave `TMPDIR` alone and refuse a temporary folder inside a repository |
| 48 to 107 calls and about $2.50 a full run | The announcement, the ceiling per run, baseline runs reused across iterations |
| Cost from the transcript, never `total_tokens` | `usage.py` |
| A subagent's transcript lacks its output tokens | Runs and judgments are main sessions; a subagent's output is estimated and marked |
| A run takes the session's effort | `--model` and `--effort` per session |
| One reader for the runs and the reviews | `shared/usage/` |
| Runs reach the skill's evals | A copy without `evals/`, outside the repository, and `guard.py` |
| An agent's judgment varies | How Many Runs |
| Nested sessions load hooks, skills and `CLAUDE.md` | `--setting-sources project,local` and `--strict-mcp-config` for every session, the parent's `CLAUDE*` variables removed; the project's hooks and `CLAUDE.md` stay (task 2) |
| An installed copy shadows the skill under test | The user's layer left out; the other personal skills copied beside the copy for trigger sessions |
| An agent's `effort` is ignored under `--agent` | `grade.py` and `compare.py` pass `--model` and `--effort` |
| The `claude` on the `PATH` can lag behind the models | Full model ids; `harness.py` refuses a version older than 2.1.291 |
| A session can run on another model | Model and effort read from every call |

`harness.py` and `usage.py` hold every tie to Claude Code — the `claude -p` flags, the
json result, the stream-json events, the transcripts' fields, `--agents` and `--agent`,
`--setting-sources` and `--strict-mcp-config`, a PostToolUse hook's `continue`, the
`CLAUDE*` variables, the minimum version —, each with its row in
`docs/claude-code-coupling.md` in the commit that adds it; another agent needs another
`harness.py`. The scripts get their allow rules in `domains/skill-tooling/permissions.json`.

### Changes To The Tasks

Proposed with the design, since the proofs were approved before `claude -p` was chosen:

- Task 2 probes the three kinds of session: a trigger session as it stands, then with
  what `--settings` removes, as its proof says; an output run — `--model` and `--effort`
  applied to every call, `auto` with prompts refused, a write to `.claude/skills/`, a
  write of `summary.md`, `guard.py` refusing a path of the real repository; a judgment
  session started with `--agents` and `--agent`, the agent's model and effort applied;
  and one trigger session's cost, alone and after another has cached the prefix.
- Task 5 becomes "Test and implement the run script: the count and estimated cost
  printed, nothing started without `--start`, each run in a copy outside any repository
  at the model, effort and ceiling of the iteration, the Skill and Agent tools denied,
  `guard.py` given; a stopped run started again, a complete one skipped". Proof: test —
  a stub standing for `claude`: the command carries model, effort, ceiling, denied
  tools, hook and folder; the folder lies outside any repository and holds no `evals/`;
  nothing starts without `--start`; a stopped run starts again and a complete one does
  not; `run.json` is written from the stub's transcript, red before the code; then a
  check — one case of the sample skill run for real with and without the skill, each
  transcript showing the set model and effort, the skill's copy read in the skill's arm
  only, and no path of the real repository.
- Task 6: the grader is started by `grade.py`'s session; its proof is unchanged, each
  judgment run three times.

### Runs This Phase Pays For

Estimated now, on Sonnet 5.5 at `xhigh` unless stated, and announced again by each
script before it starts:

| Task | Sessions | Estimate |
|---|---|---|
| 2, probe | about 10 short ones | $2 |
| 5, check | 2 runs of the sample skill | $1 |
| 6, grader | 3 outputs × 2 graders × 3 | $8 |
| 9, effort | Phase 3's 3 tasks × 2 efforts × 2 runs, a third per task when the pass rates differ | $25 to $38 |
| 11 and acceptance, triggers | 20 queries × 3, on Opus 5.5: 20 first runs at $0.09, 40 repeats at $0.008 (task 2) | $2 |
| 13, comparison | 2 versions × 2 runs, then 2 comparators × 3 | $6 |
| 14, reference | 2 runs of a fresh agent | $4 |
| Acceptance, full iteration | the sample skill, 2 cases × 2 configurations × 3 runs, graded | $5 |
| **Total** | | **about $55 to $70** |

Task 9 takes two runs per task and effort rather than three: Phase 3's three tasks lost
every recorded failure with the skill, so the pass rates should sit near their ceiling
and the cost should decide; a third run is added where they differ.

---

## Tasks

### Design
- [x] Write the design — `evals.json` with output, pressure and trigger cases, workspace layout, run prompts, grading and benchmark schemas, review — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval
  Proof: review — the design, each part tied to the Phase 0 matrix rows it carries and to this phase's constraints, approved before any script is written
- [x] Measure what the design's three kinds of `claude -p` session load and obey — hooks, skills, `CLAUDE.md`, that no plugin is left, the flags and settings the design relies on — and how to keep a trigger eval from being biased
  Proof: probe — one `claude -p` session started from a temporary directory as the trigger eval will start it, its transcript listing the hooks that ran, this setup's SessionStart line and the review domain's Stop hook among them, the skills listed and the files loaded; a second session, with what `--settings` keeps out removed, as the control; an output run with `--model` and `--effort` applied to every call, `auto` with prompts refused, a write to `.claude/skills/`, a write of `summary.md` and `guard.py` refusing a path of the real repository; a judgment session started with `--agents` and `--agent`, the agent's model and effort applied; and one trigger session's cost, alone and after another has cached the prefix

### Output Evals
- [x] Test and implement the count of a run's tokens and cost from its transcripts: one usage per message id, the price of each model, the effort recorded, and the output tokens estimated and marked as such where a subagent's transcript does not hold them
  Proof: test — transcript excerpts with known usages, a message id repeated and a subagent's stream-start records, red before the code; then Phase 3's sessions counted again and compared with `docs/decisions/2026-10-06-token-costs.md`, to the cent where `cost-state` holds the totals, before their transcripts are deleted 30 days after their last write
- [x] Test and implement the workspace preparation, under the repository's `[skills] workspace` in a `skills/<skill-name>/` subfolder so that evaluated agents can share the folder later: a copy of the skill without `evals/`, a snapshot of the baseline version, one directory per case and configuration, `eval_metadata.json`
  Proof: test — a sample skill holding `evals/`: its copy lacks `evals/`, the snapshot matches the baseline version given, one directory per case and configuration, `eval_metadata.json` written, all under `skills/<skill-name>/` of the workspace
- [x] Test and implement the run script: the count and estimated cost printed, nothing started without `--start`, each run in a copy outside any repository at the model, effort and ceiling of the iteration, the Skill and Agent tools denied, `guard.py` given; from each transcript the path the run read, the model and the effort it actually used, and its tokens, cost and duration saved; a stopped run started again, a complete one skipped
  Proof: test — a stub standing for `claude`: the command carries model, effort, ceiling, denied tools, hook and folder; the folder lies outside any repository and holds no `evals/`; nothing starts without `--start`; a stopped run starts again and a complete one does not; `run.json` is written from the stub's transcript, red before the code; then a check — one case of the sample skill run for real with and without the skill, each transcript showing the set model and effort, the skill's copy read in the skill's arm only, and no path of the real repository
- [ ] Write the grader agent: it grades each assertion with evidence, flags an assertion that a wrong output would also pass, and its answer becomes `grading.json`; `grade.py` starts it as a `claude -p` session running the agent
  Proof: eval — three outputs graded by a fresh agent without the grader's definition, then by the grader: one that passes, one that fails, one with an assertion a wrong output also passes; their grades written before the runs, each judgment run three times, as the design sets
- [ ] Test and implement the grading entry point: the skill's own `evals/grade.py` when it exists, the grader agent otherwise
  Proof: test — a skill with its own `evals/grade.py` graded by it, one without handed to the grader, and a `grade.py` that fails stopping the grading with its message
- [ ] Test and implement the benchmark: pass rate, time, tokens and cost per configuration, with mean, standard deviation and delta, and the model and effort of its runs
  Proof: test — grading files whose pass rates, times, tokens and costs were computed by hand: mean, standard deviation and delta per configuration, model and effort reported, and a run whose output tokens are unknown marked rather than counted as zero
- [ ] Measure the same output evals at `max` and at `xhigh`, pass rates and costs, and set from the result the effort the runs take, as `docs/decisions/2026-10-06-token-costs.md` asks
  Proof: probe — Phase 3's three skill-writing tasks run with the skill at `max` and at `xhigh`, same model and prompts, as many runs as the design sets, their count and estimated cost announced before they start; the pass rates and costs compared in the report set the effort
- [ ] Adapt the skill-creator review viewer, from its copy in `study/skill/create-skill/skills/skill-creator/eval-viewer/`, to the workspace layout, keeping its Apache 2.0 notice, and list it in `NOTICE`
  Proof: check — the adapted viewer's `--static` export on the sample skill's workspace writes a page holding each output, its grades and the benchmark, and `NOTICE` names the adapted files, their origin and their license

### Trigger Evals
- [ ] Test and implement the trigger eval: each query run several times in a fresh `claude -p` session, with the skill in a temporary directory passed with `--add-dir`, never in the project's `.claude/`
  Proof: test — a stub standing for `claude`: each query run the set number of times, the rate per query computed, the skill passed with `--add-dir` from a temporary directory, nothing written under the project's `.claude/`, and the count of sessions printed before the first starts
- [ ] Implement description tuning as Phase 0 decided: the session proposes each rewrite, a script measures it on training and held-out queries, and the best on held-out queries wins
  Proof: test — fixed trigger results standing for the runs: the split into training and held-out queries, each rewrite scored on both, and the best on held-out queries chosen even when another wins on training
- [ ] Implement blind comparison between two versions of a skill, the option Phase 0 kept for when the benchmark does not separate them
  Proof: eval — two versions of a skill whose better one is known, their outputs compared with the labels hidden, by a fresh agent without the comparator's definition, then by the comparator; expected before the runs: the comparator names the better one and says why

### Reference
- [ ] Write the evaluation reference: when to evaluate, how many cases, which baseline, how to read the benchmark and the trigger rates, and which checks stay assertions and which go to a person's review (row S17, left from Phase 3)
  Proof: eval — a fresh agent asked to evaluate a sample skill, without the reference, then with it; expected before the runs: with it, the cases and the baseline chosen, the count and cost of runs announced, the effort and model set, the benchmark and trigger rates read, and S17's assertions and reviews kept apart

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/SKILL.md                   the fourth operation, evaluate
domains/skill-tooling/skills/authoring-skills/scripts/*.py               new, usage.py a copy of shared/usage/
domains/skill-tooling/skills/authoring-skills/scripts/viewer.py          new, adapted from skill-creator
domains/skill-tooling/skills/authoring-skills/assets/viewer.html         new, adapted from skill-creator
domains/skill-tooling/skills/authoring-skills/references/evaluate.md     new
domains/skill-tooling/skills/authoring-skills/references/eval-files.md   new, the schemas
domains/skill-tooling/skills/authoring-skills/references/create-and-edit.md  steps 7 and 10 and the Edit table send to evaluate
domains/skill-tooling/skills/authoring-skills/evals/sample/              new, the sample skill
domains/skill-tooling/agents/skill-grader.md                             new
domains/skill-tooling/agents/skill-comparator.md                         new
domains/skill-tooling/permissions.json                                   the scripts' allow rules
domains/skill-tooling/tests/test_*.py                                    new
domains/skill-tooling/CHANGELOG.md
shared/usage/usage.py                                                    new, with shared/usage/tests/
docs/claude-code-coupling.md                                             harness.py's and usage.py's ties
NOTICE                                                                   new
```

### Dependencies
Phase 3: the skill. Phase 0: the decisions on description tuning and blind comparison.
The Agent Skills standard's guides on evaluating skills and optimizing descriptions
describe the same loop as skill-creator, for any agent; `docs/conventions/agent-skills.md`
lists them and where this setup departs from them, a cost counted from `total_tokens`
and a workspace beside the skill among them. `docs/decisions/2026-10-06-token-costs.md`
gives Phase 3's costs, the method that counted them and the effort its runs took.

### Constraints
Standard library only. Output runs and trigger runs start `claude -p` sessions, as the
user decided on 2026-10-06 against the opening decision that output evals run in
subagents, and a script says how many it will start before it starts them.
In a subagent, Claude Code's Write tool refuses any file whose name matches
`^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$`, case-insensitive (seen in 2.1.286): a skill
that produces such a file, as the roadmap closure produces `summary.md`, makes its run
agents fall back on a Bash heredoc. The design says whether those runs move to
`claude -p` or their prompt warns of it. In a headless run, an Edit under `.claude/`
waits for a permission even with `--permission-mode acceptEdits` (seen in 2.1.283): a
scenario's skill sits elsewhere, as Phase 2's hook probe put it under `skills/`, or the
run grants that permission. The repository's tests assume a temporary folder outside any
repository that holds `.agent-conventions.toml`: with `TMPDIR` inside this repository,
five of them fail, two of the audit's and three of the conventions reader's (seen on
2026-10-05), so the tooling leaves `TMPDIR` alone or makes those tests independent of
it first. A realistic skill-writing run, in Phase 3's baseline on Sonnet, took 48 to 107
API calls and 22 to 45 minutes, read 7.6 to 26.1 million tokens from cache, and ended on
a context of 250,000 to 410,000 tokens: the design says how many runs a benchmark
starts, and the script announces it, with its estimated cost, before starting them.
Phase 3's 23 full-task runs cost about $57.50, $2.50 each, and its 45 runs of
`skill-auditor` about $20, $0.45 each: 77 of the phase's 167 dollars
(`docs/decisions/2026-10-06-token-costs.md`). A run's cost is counted from its
transcript, fresh input and cache reads, one usage per message id, never from the
`total_tokens` of the Agent tool's result, which is the size of the last context and
which skill-creator records as the cost. A subagent's transcript does not hold its final
output tokens: most of its records keep the usage written when the message started
streaming (seen on 2026-10-05, 221 recorded for about 2,500 tokens of visible text; on
2026-10-06, 88,681 recorded for 804,047). A main session's transcript holds them. The
`cost-state` record Claude Code writes into a session's file when the session is resumed
or ends holds each model's totals, subagents included, but no run's. So the design
takes a run's output from a source that holds it, or estimates it and says so, as the
record does. A run takes the effort of the session that starts it: in Phase 3, 2,586 of
the runs' 2,621 calls in sessions at `max` ran at `max`, and thinking made 84% of their
output. A benchmark whose effort is left to the session compares runs made under
different conditions and pays for the highest setting: the run procedure sets the
effort, as it sets the model. One reader counts tokens and cost for the runs and for the
review domain, as roadmap `token-usage` decided at its opening on 2026-10-06. This phase
writes it for the runs, and `token-usage` extends it to the reviews: the design places
it where the review domain can take it, as `shared/` holds code several tools use. A run working in this repository reaches
the skill's own evals with one `grep`, as two of Phase 3's Verification runs did
despite a prompt that forbade the skill's folder: the run procedure keeps the evals out
of the run's reach rather than out of its instructions. An agent's judgment varies from
run to run: on a file left unchanged between them, `authoring-skills`' copy of the
shared conventions reference, three runs of `skill-auditor` reported one problem, then
three, then four, two of them new and one of the earlier ones missing (seen on
2026-10-06), so the design says how many runs a judgment takes before its verdict
counts.

---

## Acceptance Criteria

- [ ] One full iteration runs end to end on a sample skill: workspace, runs, grading, benchmark, review
- [ ] A trigger eval reports a rate per query and writes nothing into the project's `.claude/`
- [ ] Every evaluation capability marked keep or improve in the Phase 0 matrix is implemented
- [ ] Every script is covered by unit tests that pass under `make check`

---

## Risk & Mitigation

- A nested `claude -p` session loads the user's hooks, skills and `CLAUDE.md`, which can
  bias triggering. Among them is this setup's own SessionStart line. The review domain's
  Stop hook can also ask each session for a tool review. No plugin is left since
  2026-10-04 (`docs/decisions/2026-10-04-plugins-removed.md`). Task 2 measured what
  loads: the design leaves out the user's layer with `--setting-sources project,local`.
- A subagent can run on another model than the one requested, as two reviewers did on
  2026-09-27: the run procedure reads the model from each transcript, and the benchmark
  reports it.
- Trigger evals are costly — twenty queries run three times make sixty sessions per
  description — so the scripts print the count before starting and accept a smaller
  sample.
