# Eval Files

The files of a skill's evals: `evals/evals.json`, which the agent writes, then the files
the scripts write under the workspace, which the agent and the review page read. Each
section names the script that writes the file; the scripts' `--help` gives their options.
Every time is UTC, in ISO 8601; every cost is in dollars, `null` when unknown, never 0.

## Contents

- `evals/evals.json`: the cases and the trigger queries
- The Workspace: the folders the scripts write
- `iteration.json`, `eval_metadata.json`: an iteration and each of its cases
- A Run's Folder, `stop.json`: what a run leaves, and how to stop the runs
- `grading.json`, `benchmark.json` and `benchmark.md`, `feedback.json`: the grades, their
  sum, the user's feedback
- A Trigger Eval's File, `tuning.json`: trigger rates and the tuning of a description
- A Comparison's Files: a blind comparison of two versions

## `evals/evals.json`

Written by the agent, validated by `scripts/workspace.py`, which refuses an unknown key,
a missing one or a wrong type by name.

```json
{
  "skill_name": "releasing-domains",
  "env": {"CLAUDE_DIR": "{tmp}/claude"},
  "agents": ["agents/release-checker.md"],
  "hooks": "domains/release/hooks.json",
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

| Key | Required | Holds |
|---|---|---|
| `skill_name` | yes | The skill's folder name |
| `env` | no | Variables set for every run; `{tmp}` stands for the run's temporary folder |
| `agents` | no | The files of the agents the skill starts, as paths from the repository's root, each file name once: each arm's runs get their version of them, the arm without the skill none, and every run may use the Agent tool, in both arms; the baseline is then a git revision, never a folder |
| `hooks` | no | The hooks file of the skill's domain, as a path from the repository's root: a JSON object mapping each event to its hook groups, as Claude Code's settings hold them, whose commands name the folder `hooks/` beside it as `{{HOOKS_DIR}}`, no other placeholder. Each arm's runs get their version, the hook files copied beside the skill's copy as an install puts them, the arm without the skill none; the baseline is then a git revision, never a folder. A case turns a hook off as an installed repository would, through its fixture's configuration |
| `starts_agents` | no | `true` for a skill that starts agents whose files are not written yet, as before its first runs: every run may use the Agent tool; a non-empty `agents` implies it |
| `evals` | yes | One case or more |
| `id`, `name` | yes | Unique; `name` in lowercase letters, digits and hyphens, the case's folder name |
| `kind` | yes | `reference`, `task` or `discipline`, the kinds of `references/create-and-edit.md` |
| `setup` | yes | Where a run works: `repository`, a copy of the repository; `empty`, an empty folder; `fixture`, the folder `evals/fixtures.py <name> <folder>` builds |
| `exclude` | no | For a `repository` case: paths left out of the copy, such as documents that hold the expected results |
| `prompt` | yes | The request, worded as a user would word it |
| `files` | no | Paths in the skill, copied into the run's folder at their paths in the evals folder |
| `expected_output` | yes | What the run should produce, for the grader and the reader |
| `assertions` | no | Checks a reader settles from the output and the transcript, each carrying the measure of what it checks |
| `review` | no | What only a person can judge, shown beside the output and never graded |
| `pressures` | no | A discipline case's combined pressures |
| `failures_without_skill`, `failures_with_skill` | no | Failures quoted from runs, each with its run and date |
| `pending` | no | What no run has shown yet, and why |
| `triggers` | no | Queries for the trigger eval: `query`, `should_trigger`, and for a near miss `near`, what it nearly matches |

## The Workspace

Under the `[skills]` table's `workspace`, written by `scripts/workspace.py`, then filled
by `scripts/run.py`, `scripts/grade.py`, `scripts/benchmark.py` and `scripts/viewer.py`:

```
<workspace>/skills/<skill-name>/iteration-N/
  iteration.json
  base.tar                      for a repository case
  with_skill/<skill-name>/      the skill without its evals folder
  old_skill/<skill-name>/       with --baseline, that version without its evals folder
  with_skill_agents/            for a skill with agents: their files at their paths from the root
  old_skill_agents/             with --baseline, their files at that revision, an agent it lacks left out
  with_skill_hooks/             for a skill with hooks: its hooks file and the folder hooks/ beside it, at their paths
  old_skill_hooks/              with --baseline, the same at that revision, empty when it lacks the hooks file
  stop.json                     while a stop is asked
  benchmark.json, benchmark.md
  feedback.json
  <case>/
    eval_metadata.json
    files/                      the case's files
    fixture.tar                 for a fixture case
    <configuration>/run-N/      a run's folder
<workspace>/skills/<skill-name>/triggers/
  <date-time>.json              one trigger eval, written by scripts/triggers.py
<workspace>/skills/<skill-name>/tuning-N/
  tuning.json                   one tuning of the description, written by scripts/tuning.py
  proposals/N.txt               a rewrite, to measure with triggers.py --description
  proposals/N-request.md, N-answer.md   what the rewriting session received and answered
<workspace>/skills/<skill-name>/comparison-N/
  comparison.json, comparison.md        one blind comparison of two versions, written by scripts/compare.py
  <case>/run-N/session-M/       a comparator session's files and session.json
```

The configurations are `with_skill` and `without_skill` for a new skill, `with_skill`
and `old_skill` for an edit; an iteration prepared with `--skill-only` or
`--baseline-only` holds one.

## `iteration.json`

Written by `workspace.py`; read by every other script.

| Key | Holds |
|---|---|
| `skill_name`, `skill`, `skill_path` | The skill's name, its folder, and its path from `root` |
| `root` | The repository's root, which a run's guard refuses |
| `evals` | The evals folder's name, where `grade.py` finds the skill's own `grade.py` |
| `created` | When the iteration was prepared |
| `cases`, `configurations` | Their names, in order; the first configuration is the skill's |
| `runs` | Runs per case and configuration |
| `model`, `effort`, `budget_usd` | Every run's model by its full id, effort, and ceiling |
| `baseline` | `{"folder": …, "in_repository": …}` or `{"revision": …, "commit": …}`; `null` without `--baseline`. `in_repository` is false for a folder whose `SKILL.md` names another skill: another tool, which a `repository` case's runs get as their copy only, never at the skill's path |
| `agents` | The evals' `agents`, `[]` without |
| `hooks` | The evals' `hooks`, `null` without |
| `starts_agents` | Whether the runs have the Agent tool: the evals' `starts_agents`, or `agents` listed |
| `snapshot_digest` | The digest of `old_skill/`'s copy, with `old_skill_agents/` and `old_skill_hooks/` for a skill with agents or hooks, or `null` |
| `base_digest` | The digest of `base.tar`, or `null` |
| `env` | The evals' `env` |
| `reused` | `{case: iteration}` for each case whose baseline runs came from an earlier iteration |
| `extended` | Present after `--extend`: `[{"from", "to", "at"}]` |

## `eval_metadata.json`

Written by `workspace.py`, one per case: the case's `id`, `name`, `kind`, `setup`,
`prompt`, `expected_output`, `assertions`, `review`, `pressures`, `files` and `exclude`,
an absent list given as `[]`, and `digest`, over what its runs receive — prompt, setup,
`exclude`, `env`, files, base, fixture and, when the runs have it, the Agent tool, never the
agents' files, which the arm without the skill does not receive, nor the assertions —,
which decides `--reuse`.

## A Run's Folder

Written by `run.py`. It is emptied when the run starts again.

| File | Holds |
|---|---|
| `running.json` | While the run goes: `session_id`, `started`, and `pid`, run.py's |
| `prompt.md` | What the session received: the preamble, a line `---`, the case's prompt |
| `result.json` | The session's json result; `stdout.txt` in its place when none could be read |
| `stderr.txt` | The session's error output, when there was any |
| `response.md` | The run's closing account |
| `transcript.jsonl` | The session's transcript, copied: it outlives the harness's own retention |
| `transcript.md` | The prompt, then the agent's texts, its calls and their results, in order, each past 2,000 characters cut short, naming the file of `whole/` that holds it; at its head, the agents the run started, when it started any |
| `subagents/` | The transcripts of the agents the run started, `agent-<id>.jsonl` with its `.meta.json`, copied |
| `agents/` | Each agent's run as `transcript.md` renders the session, `<agent type>-<id>.md` |
| `context/` | What the sessions were given beyond the prompt — instruction files, a hook's context or blocking error —, each whole, numbered in the order it came, an agent's in `context/<agent type>-<id>/`; `transcript.md` and each agent's file name each one where it came, with its path and size |
| `whole/` | Each text, call input or result that `transcript.md` cuts short, whole, numbered in the order it came — `NN-prompt.txt`, `NN-agent.txt`, `NN-call-<tool>.json`, `NN-result.txt` —, an agent's in `whole/<agent type>-<id>/`, its closing answer among them, a text or the input of the call that hands it back |
| `outputs/` | The files the run added or changed, at their paths in its folder |
| `changes.json` | `added`, `modified` and `deleted`: paths in the run's folder |
| `run.json` | Below |

`run.json`:

| Key | Holds |
|---|---|
| `case`, `configuration`, `run` | Which run |
| `status`, `reason` | `complete` with `null`, or `stopped` with what stopped it: `timeout`, `no result, exit code …`, an API error with its message, the json result's subtype, `transcript not found`, `error: …` |
| `claude_version` | The harness's version for this run |
| `model`, `effort`, `budget_usd` | As the iteration set them |
| `started`, `ended` | Times |
| `hooks` | The events of the hooks the session started with, from the arm's hooks file; `[]` without |
| `session_id` | The session's id |
| `reported_cost_usd` | The cost the json result reports, a cross-check |
| `duration_s` | The session's wall time, from its start to its end, the time it waits on its agents included |
| `reported_duration_s`, `turns` | From the json result, whose duration leaves out the time a session waits on agents in the background |
| `refusals` | The calls the guard refused, the agents' included, each with `tool_name`, `tool_use_id` and `tool_input` |
| `models`, `efforts` | Calls per model and per effort, read from the transcripts, the agents' included; `none` counts calls without a recorded effort |
| `calls`, `estimated_calls` | Calls counted, and those whose own output their transcript lacks, as most of an agent's |
| `tokens` | `input`, `output`, `cache_read`, `write_5m`, `write_1h` |
| `output_source` | Where the output of `estimated_calls` comes from: `transcript`, none lacking; `reported`, the json result's total per model, shared among them by their estimates, the total exact; `estimated`, `usage.py`'s estimates by agent type and effort |
| `cost_usd` | Counted from the transcripts at `usage.py`'s prices; `null` for a model the table lacks |
| `agents` | `{agent type: {"runs", "calls", "estimated_calls", "models", "efforts", "tokens", "cost_usd", "output_source"}}` for the agents the run started; `{}` without. An agent's `output_source`: `transcript`, every call's final output read, from its transcript or its Agent result; `settled`, its share of the reported total, set by its calls' estimates, so that its output and cost are not measured; `estimated` |
| `prices` | The date of `usage.py`'s price table |
| `skill_reads` | The paths under the skill's copy the calls named, the agents' included, `.` for the copy itself; `[]` in the arm without the skill |
| `repository_paths` | The paths under the real repository the calls named, the agents' included; should be `[]` |

The keys read from the transcript are absent when it was not found.

## `stop.json`

Written by `run.py --stop` in the iteration's folder: `{"asked": time}`. The `run.py`
going starts no new run while it is there; the next `--start` removes it.

## `grading.json`

Written in a run's folder by `grade.py`, or first by the skill's own `evals/grade.py`,
which writes `{"assertions": [{"text", "passed", "evidence"}]}` for the assertions it
decides, each `text` exactly as the case gives it.

| Key | Holds |
|---|---|
| `assertions` | In the case's order: `text`, `passed`, `evidence`, and `by`, `script` or `grader` |
| `summary` | `passed`, `failed`, `total`, and `pass_rate` to two decimals |
| `weak` | `[{"text", "reason"}]`: the assertions the grader found a wrong output would also pass |
| `claims` | `[{"claim", "verified", "evidence"}]`: the run's claims checked against its files |
| `grader` | The grader session: `agent`, `status`, `model` and `effort` from the agent's frontmatter, the session's figures as in `run.json`; `null` when the script decided every assertion |

A run's `grader/` holds the grader session's `prompt.md`, `result.json`, `response.md`,
`transcript.jsonl`, `transcript.md`, and `session.json`, its record with `passed` and
`total`. A session stopped, or an answer that cannot be read, leaves the run ungraded,
its `grading.json` holding at most the script's assertions; `session.json` gives the
reason.

## `benchmark.json` And `benchmark.md`

Written by `benchmark.py` in the iteration's folder; `benchmark.md` shows the same
figures as tables, then the notes. A run counts when it is complete and graded on every
assertion of its case.

| Key | Holds |
|---|---|
| `skill_name`, `iteration`, `created`, `model`, `effort`, `cases`, `configurations` | As the iteration gives them |
| `runs_per_configuration` | The iteration's `runs` |
| `summary` | Per configuration: `runs`, `estimated_runs` (those whose `output_source` is `estimated`), `models`, `efforts`, and for each metric — `pass_rate`, `duration_s`, `input`, `cache_read`, `cache_write`, `output`, `cost_usd` — its `n`, `mean`, `stddev`, `min` and `max` |
| `delta_of`, `delta` | With two configurations: their names, the skill's first, and per metric the first's mean less the second's; `null` otherwise |
| `by_case` | Per case: the pass rate's statistics per configuration, and `delta` |
| `assertions` | Per case and assertion: `number`, `text`, `results` per configuration (`passed`, `runs`), `discriminates`, `varies_in`, `weak` (how many gradings named it), `weak_reason`, `runs` |
| `runs` | Each counted run: case, configuration, run, `passed`, `total` and the metrics, `estimated_calls`, `output_source`, `models`, `efforts`, `agents` (each agent type's `calls`, `models`, `efforts`, `output_source`), `claude_version` |
| `left_out` | `[{"run", "reason"}]`: `not started`, `not complete: …`, `not graded` |
| `cost_usd` | `runs` and `grading`, the counted runs' totals |
| `notes` | Sentences computed from the above |

A metric's `n` is the number of runs that give it: a figure a run lacks is left out, and
`stddev` is the sample's, `null` for a single value. `discriminates` is `false` when an
assertion has one result in every run of both configurations, `null` with a single
configuration.

## `feedback.json`

Written in the iteration's folder by `viewer.py` as the user types, or downloaded by a
page written with `--static`, for the user to put there. The viewer reads it back, and
an iteration's viewer shows it beside each run with `--previous`.

```json
{
  "reviews": [
    {"run": "release-a-minor-change/with_skill/run-1", "feedback": "…", "at": "…"}
  ],
  "status": "complete"
}
```

`run` names a run as `<case>/<configuration>/run-N`. While the user types, `status` is
`in_progress` and `reviews` holds the runs with feedback; on submit, it is `complete` and
`reviews` holds every run shown, an empty `feedback` meaning that the user found nothing
to say.

## A Trigger Eval's File

Written by `triggers.py` under the skill's `triggers/`, one per run of the script, named
by the time it ended.

| Key | Holds |
|---|---|
| `skill_name`, `description` | The skill, and the description its copy carried: the skill's own, or the text of `--description` |
| `description_file` | That file's path, or `null` |
| `model`, `effort`, `runs`, `budget_usd` | Every session's model by its full id, effort, sessions per query, and ceiling |
| `threshold` | 0.5: a query that should trigger passes at that rate or more, one that should not below it |
| `claude_version`, `started`, `ended` | The harness's version and the times |
| `summary` | `queries`, `passed`, `failed`, `not_measured`; `should_trigger` and `should_not_trigger`, each `queries` and `passed`; `sessions` counted, `not_started`, `source_reads`, and `cost_usd` over every session started |
| `queries` | Per query, in the order of `evals.json`: `query`, `should_trigger`, `near` when given, `triggered` and `counted` sessions, `rate` (`null` when none counted), `passed`, and `sessions` |

A session holds `run`, its number in the query, the first reading the query's context
into the cache; `session_id`, `status`, `reason`, `claude_version`, `reported_cost_usd`,
`duration_s`, `reported_duration_s`, `turns` and `refusals`, as in `run.json`; `counted`, `false` for a session
stopped by a timeout, an API error or the subscription's limit; `triggered`, and
`trigger_call`, the number of the call that used the skill among the first three, or
`null`; `calls`, each `[tool, input in a few words]`; `source_reads`, the paths of the
skill's source in the repository that the calls named, recorded and not counted; and,
read from the transcript, `models`, `efforts` and `cost_usd`.

## `tuning.json`

Written by `tuning.py` in `tuning-N/` under the skill's workspace: `split` creates it,
`score` and `propose` add to it.

| Key | Holds |
|---|---|
| `skill_name`, `skill_path`, `created` | The skill, its folder, and when the split was made |
| `seed`, `held_out_share` | The split's seed and the share of each class held out, 0.4 |
| `description` | The skill's own description at the split, which `score` names `skill` |
| `train`, `held_out` | The two sets, each query as in `evals.json`: `query`, `should_trigger`, `near` when given |
| `descriptions` | Each description scored, in order: `number`, `origin` (`skill`, `proposal N` or `given`), `description`, `characters`, `results` (the `triggers.py` file it was scored from), `model`, `effort`, `runs`, `train` and `held_out` (each `passed` and `queries`), and `queries`, each with its `set`, `should_trigger`, `triggered`, `counted`, `rate` and `passed` |
| `best` | The number of the best description on the held-out queries, a tie going to the shorter, then the earlier |
| `proposals` | Each rewriting session: `number`; `rewrote`, the description it started from; `status`, `proposed`, `refused` (no description, too long, or a repeat) or `stopped`, with `reason`; `description` and `file`, `proposals/N.txt`, when proposed; `notes`, whether notes were given; `model`, `effort`, `budget_usd`, `claude_version`, `session_id`, `duration_s`, `reported_cost_usd`, `started`; and, read from the transcript, `models`, `efforts` and `cost_usd` |

`proposals/N-request.md` holds what the session received, `proposals/N-answer.md` what
it answered.

## A Comparison's Files

Written by `compare.py` in `comparison-N/` under the skill's workspace, one folder per
pair of versions: a later `--start` on the same two versions fills the same folder. A
version is named `<iteration>/<configuration>`, such as `iteration-2/with_skill`.

`comparison.json`:

| Key | Holds |
|---|---|
| `skill_name`, `updated` | The skill, and when the file was last written |
| `versions` | The two versions, each `name`, `iteration` (its folder) and `configuration` |
| `agent` | The comparator's `name`, `model` and `effort`, from its frontmatter |
| `sessions_per_pair` | 3 |
| `pairs` | Per pair: `case`, `run`; `labels`, each session's `{"A": version, "B": version}`, drawn before any session; `sessions`, each `session`, `status` (`complete`, `stopped` or `not started`), `reason`, `winner` (a version, `tie`, or `null` when not complete) and `cost_usd`; `verdict`, the version or `tie` that two sessions agree on, `split` when every session is complete and none agree, `null` while sessions are missing; `agreeing`, how many sessions gave the verdict |
| `left_out` | `[{"name", "reason"}]`: a case one version lacks, a case whose prompts differ, a pair whose runs are not both complete |
| `summary` | `pairs`; `verdicts`, the pairs per version, `tie`, `split` and `pending`; `sessions`, per status; `label_wins`, the complete sessions won by the output shown as `A`, as `B`, or tied, which shows a preference for a place; `scores`, per version the mean of each criterion, `correctness`, `completeness` and `form`, 1 to 5; `assertions`, per version `passed` of `checked`; `cost_usd`, over the sessions started |

A session's folder holds `prompt.md`, `result.json`, `response.md`, `transcript.jsonl`,
`transcript.md` and `session.json`: the session's figures as in a grading's `grader`
record, plus `case`, `run`, `session`, `labels`, `winner`, `shown_winner` (`A`, `B` or
`tie`, as answered), and `answer`, unblinded: `winner`, `reason` as written, `scores`,
`strengths` and `weaknesses` keyed by version, and `assertions`, each `text`, `passed`
keyed by version and `evidence`. `comparison.md` shows the verdicts, the scores per
version, and each session's reason under its labels.

