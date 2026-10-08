# Eval Files

The files of a skill's evals: `evals/evals.json`, which the agent writes, then the files
the scripts write under the workspace, which the agent and the review page read. Each
section names the script that writes the file; the scripts' `--help` gives their options.
Every time is UTC, in ISO 8601; every cost is in dollars, `null` when unknown, never 0.

## `evals/evals.json`

Written by the agent, validated by `scripts/workspace.py`, which refuses an unknown key,
a missing one or a wrong type by name.

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

| Key | Required | Holds |
|---|---|---|
| `skill_name` | yes | The skill's folder name |
| `env` | no | Variables set for every run; `{tmp}` stands for the run's temporary folder |
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
| `baseline` | `{"folder": …}` or `{"revision": …, "commit": …}`; `null` without `--baseline` |
| `snapshot_digest` | The digest of `old_skill/`'s copy, or `null` |
| `base_digest` | The digest of `base.tar`, or `null` |
| `env` | The evals' `env` |
| `reused` | `{case: iteration}` for each case whose baseline runs came from an earlier iteration |
| `extended` | Present after `--extend`: `[{"from", "to", "at"}]` |

## `eval_metadata.json`

Written by `workspace.py`, one per case: the case's `id`, `name`, `kind`, `setup`,
`prompt`, `expected_output`, `assertions`, `review`, `pressures`, `files` and `exclude`,
an absent list given as `[]`, and `digest`, over what its runs receive — prompt, setup,
`exclude`, `env`, files, base and fixture, never the assertions —, which decides
`--reuse`.

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
| `transcript.md` | The prompt, then the agent's texts, its calls and their results, in order, each shortened |
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
| `session_id` | The session's id |
| `reported_cost_usd` | The cost the json result reports, a cross-check |
| `duration_s`, `turns` | From the json result |
| `refusals` | The calls the guard refused, each with `tool_name`, `tool_use_id` and `tool_input` |
| `models`, `efforts` | Calls per model and per effort, read from the transcript; `none` counts calls without a recorded effort |
| `calls`, `estimated_calls` | Calls counted, and those whose output is estimated |
| `tokens` | `input`, `output`, `cache_read`, `write_5m`, `write_1h` |
| `cost_usd` | Counted from the transcript at `usage.py`'s prices; `null` for a model the table lacks |
| `prices` | The date of `usage.py`'s price table |
| `skill_reads` | The paths under the skill's copy the calls named, `.` for the copy itself; `[]` in the arm without the skill |
| `repository_paths` | The paths under the real repository the calls named; should be `[]` |

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
| `summary` | Per configuration: `runs`, `estimated_runs`, `models`, `efforts`, and for each metric — `pass_rate`, `duration_s`, `input`, `cache_read`, `cache_write`, `output`, `cost_usd` — its `n`, `mean`, `stddev`, `min` and `max` |
| `delta_of`, `delta` | With two configurations: their names, the skill's first, and per metric the first's mean less the second's; `null` otherwise |
| `by_case` | Per case: the pass rate's statistics per configuration, and `delta` |
| `assertions` | Per case and assertion: `number`, `text`, `results` per configuration (`passed`, `runs`), `discriminates`, `varies_in`, `weak` (how many gradings named it), `weak_reason`, `runs` |
| `runs` | Each counted run: case, configuration, run, `passed`, `total` and the metrics, `estimated_calls`, `models`, `efforts`, `claude_version` |
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
`duration_s`, `turns` and `refusals`, as in `run.json`; `counted`, `false` for a session
stopped by a timeout, an API error or the subscription's limit; `triggered`, and
`trigger_call`, the number of the call that used the skill among the first three, or
`null`; `calls`, each `[tool, input in a few words]`; `source_reads`, the paths of the
skill's source in the repository that the calls named, recorded and not counted; and,
read from the transcript, `models`, `efforts` and `cost_usd`.
