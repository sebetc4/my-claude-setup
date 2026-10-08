# Phase 4 Report: Evaluation Tooling

**Phase:** [phase-4-evaluation-tooling.md](phase-4-evaluation-tooling.md)
**Start Commit:** 8c79c7b

---

## Work Log

### 2026-10-06

Opened the phase from Phase 3's closure, committed as `8c79c7b`. Read Phase 3's file and
its report, finalized in this session: no restructuring pending, and no other phase in
progress. What binds this phase: `authoring-skills` exists with three operations,
create, edit and audit, to which this phase adds the fourth, evaluate, with its own
reference; Phase 3's eval runs left their files and `tools/order.py` under
`.eval-runs/skills/authoring-skills/`, and their `evals/evals.json` files carry keys of
their own — pressures, trigger queries, `failures_without_skill` and
`failures_with_skill` — which this phase's design settles; the constraints Phase 3 added
here, on the cost and counting of runs, `TMPDIR`, evals kept out of a run's reach and
the variance of an agent's judgment; the part of row S17 the evaluation reference takes;
and the Agent Skills standard's guides on evaluating skills, listed with this setup's
departures in `docs/conventions/agent-skills.md`. To put to the user before any work:
the twelve tasks declare no proof yet, as Phase 3's did not at its opening; and the
first risk still names the superpowers SessionStart injection, though every plugin was
removed on 2026-10-04. At the user's rule, the opening ends the turn: no work on the
phase yet.

In a new session, at the user's request, measured what Phase 3 cost and why. The
sources were the transcripts of its five sessions and of their subagents, and the
effort of every Opus 5.5 main thread since 2026-09-24. Recorded in
`docs/decisions/2026-10-06-token-costs.md`.
- About $167 in all. $88 went to a main thread at `max`, whose context reached 631,000
  tokens and was never compacted. About $79 went to subagent runs, which took the
  session's `max`.
- This setup's tools cost about $5 of it.
- A subagent's transcript does not hold its final output tokens, while a main session's
  does, and `cost-state` records hold each model's totals: this corrects the constraint
  of 2026-10-05, which said no transcript held them.

The user then agreed to source two roadmaps on these figures. This phase gained the task
that measures the same evals at `max` and `xhigh` before the runs' effort is set, 13
tasks now. The run procedure now sets the runs' effort and model and records each run's
cost, and the benchmark reports cost, model and effort. The constraints now give the
runs' costs, where a run's output tokens are found, and the user's proposal that the
review domain measure token consumption.

At the user's request, Phases 4 and 5 were then aligned with the proof convention of
`docs/decisions/2026-10-01-superpowers-study.md` (Decisions Of Phase 2, items 1 and 2),
and what had gone stale was updated. Each task of both phases got a proposed `Proof:`
line, awaiting the user's approval. In this phase:
- the effort task moved after the benchmark, which it needs;
- a task was added that counts a run's tokens and cost from its transcripts, the code
  the run procedure and the benchmark rely on, which makes 14 tasks;
- the objective now says that Phase 0 kept blind comparison as an option;
- the overview lists the traps Phase 3's runs added;
- the first risk no longer names the superpowers injection, gone with the plugins, and
  names this setup's own hooks instead;
- Files to Modify names the domain, the skill, the two agents the 2026-09-28 record
  named, and `SKILL.md`, which gains the evaluate operation;
- the viewer task names the copy under `study/` that it adapts.

The user approved the proofs of both phases as proposed, raised no objection to the
change of Phase 5's Objective, and asked for a roadmap of the review domain's
measurement of token consumption. Its phases are to be proposed first.

Created roadmap `token-usage` under `docs/roadmap/pending/` with the user, in four
phases: Framing, Usage Reader, Reviews And Reports, Validation And Release. The user
settled that the measurement belongs to the review domain, whose aim becomes reviewing
how tools work and what they cost. The roadmap waits for this one, whose count of a
run's cost it extends. This phase's constraint on that count now says one reader serves
both, placed where the review domain can take it. The user approved the proofs of its 23
tasks.

Resumed in a new session, the user asking to start the phase. Read this phase's file and
report, Phase 3's report, the 2026-09-28 record and the 2026-10-06 token costs in full.
Put to the user what carries, and one dependency nothing settled: the Agent tool takes a
model but no effort; a subagent's effort comes only from the `effort` field of an agent
definition, which must be installed — `~/.claude/agents/` through `make update`, or the
project's `.claude/agents/` — or passed with `--agents` when a session starts; Phase 3's
runs, general-purpose agents told to act as an agent, took the session's. `claude -p`,
2.1.283 on the `PATH`, takes `--model`, `--effort`, `--max-budget-usd`,
`--permission-mode auto` and `--output-format json`, and a main session's transcript
holds its final output tokens. The user chose `claude -p` for the output runs.

Task 1, the design. Read skill-creator's evaluation loop from its copy under `study/` —
`SKILL.md`, `references/schemas.md`, the grader, `run_eval.py`, the viewer's and the
benchmark's entry points —, the roadmap evals' `grade.py`, create-and-edit's steps 7 and
10, the review domain's `transcript.py` and `tools/shared.py`; checked the flags of
`claude` 2.1.283 (`--agents` and `--agent`, `--json-schema`, `--max-budget-usd`,
`--permission-prompts`, `--settings`), and that the Makefile's `CLAUDE_DIR` yields to the
environment. Wrote the design in the phase's `## Design`: the evaluate operation and its
scripts; `evals.json` settling Phase 3's extra keys, with `setup`, `exclude`, `env`,
`review` and `triggers`; the workspace; runs in `claude -p` from a copy of the repository
outside any repository, without the skill's evals, the Skill and Agent tools denied and
a guard hook refusing the real repository and `~/.claude`; the counting reader in
`shared/usage/`; the grader started as a `claude -p` session running the agent; how many
runs a verdict takes; the benchmark's computed notes in place of skill-creator's
analyzer; the viewer; trigger evals and tuning; blind comparison; the reference; each
constraint's answer; changes to tasks 2, 5 and 6; and the runs the phase pays for, about
$55 to $70. The constraint that put output evals in subagents now follows the user's
decision. Put to the user for approval.

The user approved the design as proposed. Applied it: the section marked approved; task 2
now probes the three kinds of session, task 5 is the run script with a test and a check,
task 6 starts the grader through `grade.py` and runs each judgment three times; Files to
Modify completed. Ticked task 1.

Resumed in a new session, the user asking to start task 2, the probe. Twenty `claude -p`
sessions, about $1.46 in all: $1.29 reported by their results, and about $0.17 for two
sessions killed before theirs. Each ran in a copy made under the session's scratchpad by
one-off scripts, not kept. The copy held the files git tracks or does not ignore, plus
`.agent-conventions.toml`, minus `authoring-skills/evals/`, committed as a one-commit
repository. Every `CLAUDE*` variable of the parent session was removed from the
environment. This session's own shell hands a nested `claude` `CLAUDECODE`,
`CLAUDE_EFFORT=xhigh` and `CLAUDE_CODE_SESSION_ATTENDED=1`, among others. What the
sessions showed:

- **A trigger session as it stands.** Claude Code 2.1.283, Opus 5.5 at `xhigh`, the
  user's settings, and the skill's copy under `<tmp>/.claude/skills/` passed with
  `--add-dir`.
  - The SessionStart hook injected its Phase 4 line, which says to load the roadmap
    skill. The copy's own hooks, `check-skills.py` and `audit_skill.py`, ran after each
    Bash call, silent.
  - The review domain's Stop hook ran and asked for nothing. Claude Code gives the
    hooks of a `-p` session `CLAUDE_CODE_SESSION_ATTENDED=0` once the parent's `1` is
    removed: read in the binary, and logged by a probe hook.
  - Listed: the personal skills `roadmap` and `tool-review`; `authoring-skills` from
    `--add-dir`, counted as "additional"; Claude Code's bundled skills; the agents, with
    `roadmap-auditor`. The only plugins are Claude Code's built-in ones (`agents-md`,
    `telemetry`, `plugin-authoring`); none is installed.
  - Loaded: the copy's `CLAUDE.md`, and a session context holding the user's email and
    the copy's git status.
  - The claude.ai connector Claude Docs connected in some sessions and not in others,
    depending on whether it answered before the first request; when it did, it added its
    tools and instructions. `--strict-mcp-config` keeps it out.
- **The control, `--settings '{"disableAllHooks": true}'`.** No hook ran. But
  `disableAllHooks` also turns off the hooks that `--settings` itself adds: a stop hook
  passed with it never fired, so this setting cannot carry `guard.py` or a trigger stop.
  And an installed copy shadows the copy under test: with a copy of `roadmap` passed
  with `--add-dir`, the Skill tool loaded `~/.claude/skills/roadmap`.
- **The recipe that holds: `--setting-sources project,local`.**
  - It leaves out the user's layer: hooks, personal skills (the installed copy of the
    skill under test among them), agents, permission rules and model settings.
  - The skills passed with `--add-dir` still load, and the copy under test loads under
    its own name. Hooks passed with `--settings` run.
  - The project's own hooks also run: 12 hook outputs for 7 calls in the output run,
    `guard.py` 7 times and the copy's two hooks 5 times, all silent.
  - `--setting-sources local` drops the skills of `--add-dir` as well: 0 loaded.
  - Copying the user's other personal skills beside the copy under test restores the
    user's listing, as the last three sessions did.
- **Stopping a trigger session.**
  - Killing the process at the trigger lost the transcript's tail: no assistant record,
    no "Base directory" line.
  - A PostToolUse hook passed with `--settings` and returning `{"continue": false}`
    stopped the session cleanly, with its result and a full transcript.
  - A session in a repository copy can reach the skill's source: one read
    `domains/roadmap/skills/roadmap/scripts/progress.py` in its second call, which a
    match on `skills/<name>/` counted as a trigger.
- **An output run.** Sonnet 5.5 at `xhigh`, `--disallowed-tools Skill Agent`, the
  recipe, and a probe version of `guard.py`, on 2.1.291. $0.067.
  - Every call of the transcript ran at `claude-sonnet-5-5` and `xhigh`.
  - Under `auto` with `--permission-prompts none`, a Write and then an Edit of
    `.claude/skills/probe-note/SKILL.md` passed without waiting. Write wrote
    `summary.md`.
  - The guard refused a Read of the real repository's `CLAUDE.md` and an
    `ls ~/.claude/skills`; the json result lists both under `permission_denials`.
  - The skill's copy was read by its path under `--add-dir`.
- **The binary.** `claude` on the `PATH` is 2.1.283; the VS Code extension's is 2.1.291.
  - 2.1.283 maps `sonnet` to `claude-sonnet-5`. It does not know `claude-sonnet-5-5`:
    it ran it with `costBasis: unknown` and a 200,000-token context, priced it at Opus
    rates, and left the effort at `high`.
  - 2.1.291 maps `sonnet` to `claude-sonnet-5-5`, prices it at list, and applies
    `--effort`.
- **A judgment session**, `--agents <file>` and `--agent`, on 2.1.291. The agent's
  `model` applies; its `effort` does not. `low` and `xhigh` both ran at `medium`,
  Sonnet 5.5's default, while `--effort low` on the command line applied.
- **The cost of a trigger session**, Opus 5.5 at `xhigh`.
  - About $0.12 run to its answer; $0.085 to $0.089 stopped at the trigger.
  - Only the system prompt and the tools, about 10,000 tokens, come from the cache
    whatever ran before. Each session writes its first turn — `CLAUDE.md`, the skill
    listing and the session context, 8,500 to 12,900 tokens — even after another
    session in a different copy: $0.116 cold, $0.120 after.
  - The same query again, in the same folder, read everything from the cache: $0.0076
    against $0.0887. A different query in that folder cost $0.076.
- **Prices.** A `-p` session writes one-hour cache entries. 2.1.291 prices them for
  Sonnet 5.5 at $4 per million, twice its input price: the output run's $0.0666 matches
  to the cent. `docs/decisions/2026-10-06-token-costs.md` fitted $2.50 on Phase 3's
  records. For Opus 5.5, it prices them at $8, as the record says.
- Nothing was written in the repository's `reviews/`.

Ticked task 2. The design amendments these findings call for are listed under Problems
And Deviations and were put to the user.

The user updated the `claude` on the `PATH` to 2.1.292. One session checked it, with the
recipe and `--model sonnet --effort xhigh`: it ran on `claude-sonnet-5-5` at list price,
with a 1,000,000-token context, at `xhigh`. $0.025.

The user approved the six amendments. Applied them to the phase's `## Design`:
- Runs: the new flags, full model ids, every `CLAUDE*` variable removed, and the minimum
  version.
- Grading: `--model` and `--effort` passed by `grade.py` and `compare.py`.
- Trigger evals: the other personal skills copied beside the copy, the stop hook, the
  trigger criterion, and a query's runs in sequence in one folder.
- Constraints Answered: four rows added, two answered by the probe.
- The ties `harness.py` holds, the trigger estimate ($2), and the first risk.

The design's task numbers ran one too high from the viewer onwards: it numbered the
viewer 11, the trigger eval 12, tuning 13, comparison 14 and the reference 15, where
the task list has 10 to 14. Corrected in the script table and the table of runs.

Task 3, the usage reader, started at the user's request in the same session. Phase 3's
transcripts first, to fix the format:
- A main session's messages all carry a `stop_reason`, and their output sums equal
  `cost-state`.
- In a subagent's transcript, 82 of 346 messages carry one. Those hold plausible
  outputs; the rest keep the 2 to 29 tokens written when the stream started. The
  reader's rule is therefore per message, not per file: a message without a
  `stop_reason` has its output estimated and marked.
- Every one of 22,059 cache writes sampled carries its split by lifetime. The prices
  fit `ed7dbe88`'s `cost-state` to the cent with five-minute writes at 1.25 times the
  input price and one-hour writes at twice the input price: subagents write the first
  kind, main sessions the second. Haiku 4.5 is priced at $1 and $5.
- About 2,000 records carry no `effort`.
- Calibrating the estimate on the five sessions' `cost-state` records, a call without
  its final usage averages 5,371 output tokens: from 606 to 12,237 by session.

Wrote `shared/usage/tests/test_usage.py`, 14 tests, and watched them fail: the module
did not exist. Then wrote `shared/usage/usage.py`:
- one usage per message id, the last record kept, and the first transcript keeping an id
  that several hold;
- `<synthetic>` messages left out;
- prices per model, writes priced by lifetime, a dated model id taking its model's price,
  and an unknown model left unpriced, never zero;
- the effort of each call;
- 5,400 output tokens for a call without its final usage, marked;
- a JSON summary on the command line.

One test was wrong — it gave a call meant to have no effort the default `xhigh` — and
was fixed; a fourteenth test covers a write without its split, priced at the one-hour
rate. `make check` passes.

Recounted Phase 3's sessions with it:
- The main thread of each equals its `cost-state` for Opus 5.5 to the cent, and the
  record's column: $88.29 against $88.28 rounded.
- No message id is shared between the five sessions.
- By `cost-state`, which the three later sessions wrote when they ended, after the
  record, Phase 3 cost $176.38, not about $167. `a2b3cf86`'s subagents cost $27.81, not
  about $18.
- The estimated subagent cost is off by −35% to +27% per session, and 0.2% over the
  five.

Added a Recount section to `docs/decisions/2026-10-06-token-costs.md` and the reader's
ties to `docs/claude-code-coupling.md`. Ticked task 3.

Resumed in a new session for task 4, the workspace preparation. Before writing it, put to
the user what the design's `base.tar` lets a baseline read: the skill's folder stays in
the copy, minus its `evals/`, so a `without_skill` run exploring `domains/*/skills` reads
the skill under test, as `authoring-skills`' first case would, and an `old_skill` run
finds the new version. The user chose that each arm sees its own version: `base.tar`
leaves out the skill's whole folder, and a run puts back the current version, the
baseline, or nothing. The cost: a `without_skill` run in this repository fails the
domain's tests that import the skill's scripts, as a repository without the skill would.

Wrote `domains/skill-tooling/tests/test_workspace.py`, 39 tests on a temporary git
repository holding a sample skill, and watched them fail: the module did not exist. Then
wrote `scripts/workspace.py`. Two tests were wrong: they checked that a refused
preparation left no workspace, though an earlier preparation of the same test had made
one; they now compare the workspace before and after. One defect of the code: `git
archive` ran from the skill's folder with a path relative to the repository's root, and
took nothing; it now runs from the root.

What the script does:
- validates `evals.json` against the design's keys, naming each unknown key, missing
  key, wrong type, repeated id or name, file outside the skill, `exclude` outside a
  `repository` case, and `fixture` case without `evals/fixtures.py`;
- refuses before writing anything: an undeclared `workspace`, a case it does not know, a
  missing `SKILL.md` without `--baseline-only`, a baseline that is neither a folder nor a
  revision holding the skill, an unknown iteration to reuse, a `repository` case outside
  git; a failing fixture removes the iteration it began;
- writes `iteration-N/` under `.eval-runs/skills/<skill-name>/`, with the copies, the
  snapshot, `base.tar`, each case's metadata, files and fixture, and one folder per
  configuration and run.

`SKILL.md`'s Scripts section names it, which rule R3 requires of every file of the skill;
the Evaluate row and its reference come with task 14. `make check` passes. Run on this
repository's two skills, it refuses both `evals.json` files, each case lacking `kind`
and `setup`, and writes nothing.

Task 5, the run script, at the user's yes to go on. Read the json result and the probe's
guard kept from task 2 in that session's scratchpad: the result carries `subtype`,
`is_error`, `session_id`, `total_cost_usd`, `duration_ms`, `num_turns`, `result` and
`permission_denials`. Two changes to `workspace.py` first, each with its test: it
records the repository's root in `iteration.json`, which the guard needs, and it puts a
case's files at their paths in the evals folder, `files/input.txt` rather than
`evals/files/input.txt`, so that no run's folder holds an `evals/` folder.

Wrote `domains/skill-tooling/tests/test_run.py`, 25 tests with a stub standing for
`claude` that logs its command line, folder, environment and prompt, writes a
transcript under `$CLAUDE_CONFIG_DIR/projects/` and prints a json result, and watched
them fail: the modules did not exist. Then wrote:
- `scripts/harness.py`, a library holding every tie to the command line: the flags, the
  minimum version, the environment without the parent's `CLAUDE*` variables but
  `CLAUDE_CONFIG_DIR`, which names the user's configuration and credentials, the hook
  settings, the json result, the transcript's place and its rendering;
- `scripts/guard.py`, the PreToolUse hook: it refuses a call naming a denied path whole,
  with or without its leading slash, or under the home folder as `~/`, `$HOME/` or
  `${HOME}/`, and an unreadable call;
- `scripts/run.py`, which lists the runs and their estimated cost, and with `--start`
  builds each run's folder, starts the session and writes the run's folder;
- the copy of `shared/usage/usage.py`, through `tools/shared.py`.

One test was wrong, on the case of a word of the preamble. `SKILL.md` names `run.py`,
with the rule that `--start` waits for the user's yes; `harness.py` and `usage.py` are
reached through its imports. `docs/claude-code-coupling.md` gains the rows of the
command line, the json result and the guard's decision.

The sample skill for the check: `writing-notes`, under the skill's `evals/sample/` as
`skill.md` and `evals.json`, with two cases that run in an empty folder, and `build.py`,
which writes it as a repository of its own; a test builds it, validates its evals and
audits it. Preparing the check showed that the estimate ignored the ceiling: two runs
capped at $1 were announced at $5. The estimate now never passes the ceiling, with its
test watched failing first. `make check` passes.

### 2026-10-07

The check, at the user's yes: the sample built in this session's scratchpad, one
iteration of the case `decision-note`, one run per arm, a $1 ceiling each; announced at
$2.00, it cost $0.12, $0.056 and $0.057, in 8 and 11 seconds.
- Every record of both transcripts ran at `claude-sonnet-5-5` and `xhigh`, on 2.1.292;
  the cost counted from each transcript equals the json result's to the cent.
- The arm with the skill read `SKILL.md` from its copy; the arm without named no path of
  a skill. Neither transcript names the sample's repository or this one; no call was
  refused, and both temporary folders were removed.
- With the skill, the note opens with `status: draft` and closes with `## Next`; without
  it, neither. Both chose `notes/2026-10-07-search-index-postgresql.md`, the run without
  the skill after an `ls` of its empty folder: the case's first assertion does not
  discriminate, what the benchmark's computed notes are to show.

Ticked task 5.

Resumed in a new session for task 6, the grader. Its eval needs grading sessions, which
the design has `grade.py` start, the entry point task 7 tests: `grade.py` was written
whole in this task, the skill's own `evals/grade.py` included, and task 7's proof is its
tests. The order follows create-and-edit's step 7: the fixtures and their grades first,
then the sessions without the agent's definition, then the definition written from what
they show, then the sessions with it.

The fixtures, under `evals/grader/`, are made from the `with_skill` run of task 5's
check, kept in that session's scratchpad: `complete`, the run as it was; `long-slug`,
the note named with a four-word slug while the account claims three; and
`next-without-follow-up`, Alice's migration moved into the Decision section and
`## Next` holding `None.`, its case checking the heading alone. The sample's first
assertion said `YYYY-MM-DD`, which a wrong date also passes: the fixtures' cases name
the day of the run and the slug's source, so that only the third fixture holds a weak
assertion. `grades.json` holds the grades, weak assertions and contradicted claims
expected, written before any run.

Wrote `domains/skill-tooling/tests/test_grade.py`, 26 tests with a stub standing for
`claude` that logs its command line, its folder's files and the `--agents` file, and
answers the JSON given or a pass of every numbered assertion; and a test that
`iteration.json` records the evals folder. Watched them fail, then wrote:
- `scripts/grade.py`. It lists the complete runs left to grade with the count and cost
  of the sessions, and starts nothing without `--start`. With it, the listed runs'
  `grading.json` files are removed and the skill's `evals/grade.py` runs; the other
  runs' files are restored around it. A non-zero exit or an assertion the case does not
  hold stops the grading with its message. The assertions left go to the agent, started
  from its file at the model and effort of its frontmatter, in a copy of the run's
  files outside any repository, under `guard.py`.
- The answer is one JSON object grading the assertions by their numbers in the request;
  one that skips an assertion or names an unknown one is refused and leaves the run
  ungraded. The session's files go to the run's `grader/`.
- `harness.py`'s `command` takes the agent and `agents_file` writes its definition;
  `workspace.py` records the evals folder in `iteration.json`.
- `SKILL.md` names `grade.py` with the same yes as `run.py`;
  `docs/claude-code-coupling.md` gains the grading session's row.

`make check` passes. The user approved the eval's 18 sessions, announced at $8.10 at
most, $0.45 a session by `grade.py`'s default, and Sonnet at `xhigh` for the agent and
its baseline.

The eval, from a one-off script in this session's scratchpad: each fixture copied into
an iteration of its own as three complete runs, once per arm. The baseline, nine
sessions through `grade.py`'s `judge` without a definition, $0.36:
- every grade right, 9 of 9;
- the false "three-word slug" named 3 of 3;
- the weak third assertion noticed 3 of 3, as a remark on the output ("a stricter check
  on the section's content would fail it") rather than on the assertion;
- one pass without any evidence: "All three assertions pass, and I found no defects in
  the run's note";
- the account's "the request names no further step" named in 1 of 3;
- no answer `grade.py` can read, 9 of 9, as expected without the format.

`skill-grader.md` was written from these: evidence for every grade, from the files
rather than the account; every claim of `response.md` that the files or the request can
check; weak assertions measured against the prompt and the expected output; the answer's
JSON. About 480 tokens; nothing on how to grade an assertion, which the baseline already
did right. Then nine sessions through `grade.py --start`, $0.38, three calls each, every
call on `claude-sonnet-5-5` at `xhigh`:
- every answer read, and every run matching `grades.json`: the grades, the third
  assertion alone named weak on its fixture and nothing named weak elsewhere, the false
  slug claim and the false "no further step" each unverified 3 of 3;
- two runs also refused the account's "I followed the skill", rightly.

The eval cost $0.74 in all, against $8.10 announced. Ticked tasks 6 and 7: task 7's
proof is `test_grade.py`'s tests of the skill's own `evals/grade.py`.

Resumed in a new session for task 8, the benchmark. Read skill-creator's
`aggregate_benchmark.py` and the `benchmark.json` schema of its `references/schemas.md`,
then the files `run.py` and `grade.py` write.

Wrote `domains/skill-tooling/tests/test_benchmark.py`, 22 tests on an iteration written by
hand: two cases, two configurations, two runs each. Its means, standard deviations,
minimums, maximums and deltas were computed by hand. One expected figure was wrong: the
standard deviation of an output holding an estimate, put at 2,700 where it is 2,733.74;
it was corrected with a calculator before any code. Watched the tests fail, the module
not existing, then wrote `scripts/benchmark.py`:
- a run counts when it is complete and graded on every assertion of its case; the others
  are listed with their reason: not started, not complete with its status, not graded;
- per configuration: pass rate, duration, fresh input, cache reads, cache writes, output
  and cost, each with n, mean, sample standard deviation, minimum and maximum; the delta
  of the first configuration less the reference; the pass rate per case;
- each assertion's results per configuration: whether it tells them apart, where it
  varies, how often the grader named it weak;
- the models and efforts of each run's calls, summed per configuration;
- the cost of the counted runs and of their grading;
- notes computed from these.

The 22 tests passed on the code's first run. A later change to a note's wording made one
fail, as it should; the note keeps the word the test reads. `SKILL.md` names the script.
`make check` passes.

Run on copies of two earlier iterations, in this session's scratchpad:
- Task 6's third grader iteration, whose `run.json` files hold only a status: every
  figure but the pass rate unknown, and its weak assertion named in 3 of 3 runs.
- Task 5's check, graded by hand, 3 of 3 with the skill and 1 of 3 without: $0.056 and
  $0.057, as the check counted them. The first assertion is named as one that does not
  tell the arms apart, as the check foresaw.

Ticked task 8.

Resumed in a new session for task 9, the effort. What it needs first:
- `authoring-skills`' `evals.json` gained what `workspace.py` requires. Every case is
  `kind: task`: each is a realistic request, none a pressure scenario, whatever kind of
  skill it asks for. The three skill-writing cases are `setup: repository` and exclude
  `docs/roadmap/` and `docs/decisions/`, which Phase 3's preamble forbade: the roadmap
  records B1 to B13 and the expected results. `domains/skill-tooling/`, which the
  preamble also forbade, stays: the copy already lacks the skill's folder, and the
  project's audit hook runs from the domain's `hooks/`. The file's `env` sets
  `CLAUDE_DIR` to the run's folder, as the design's example does. The fourth case gets
  `setup: empty` and a `pending` line: its prompt names a folder of Phase 3's
  workspace, and its audit operation starts `skill-auditor`, while runs are denied the
  Agent tool.
- A copy of the repository built as `run.py` builds it failed `make check` with the
  skill: `test_workspace.py`'s test of the sample skill reads `evals/sample/`, which no
  copy holds. The test moved to the skill's `evals/test_sample.py`, which
  `tests/check.py` runs and a copy leaves out; the copy then passes `make check`. Without
  the skill, `tests/skills.py` cannot load the audit, as the user accepted with task 4.
- `workspace.py --skill-only` prepares the skill's arm alone, to measure it at another
  model or effort; it refuses `--baseline`, `--baseline-only` and `--reuse`. Three tests
  first, watched failing.

Recounted with `usage.py` the last three Verification runs of Phase 3, with the skill at
`max`, from session `f2b80cf5`'s subagents: 31, 37 and 51 calls, $2.45, $3.58 and $4.65,
most of their output estimated. A `claude -p` run writes one-hour entries at $4 rather
than $2.50: about $2.70, $3.90 and $5.05. The default ceiling of $5 would stop the
reference task at `max`, so both iterations take $10 a run.

Prepared `iteration-1`, at `max`, and `iteration-2`, at `xhigh`: the three skill-writing
cases, the skill alone, two runs each, Sonnet 5.5, $10 a run. `run.py` announces 6 runs
and $15.00 for each, from its default of $2.50 a run.

Put to the user before any run: 12 runs, $30 by `run.py` and about $40 by the recount;
12 gradings, about $5 to $12; up to 6 third runs, about $20; $132 if every session
reached its ceiling. And the rule that sets the effort, written before the results:
`xhigh` becomes the runs' default unless `max` beats its pass rate on at least two of the
three tasks, by more than the gap between two runs at one effort; the cost decides only
between equal pass rates. The user said yes. Both iterations started at once, three runs
at a time each, on `claude` 2.1.292.

Twelve minutes in, at 13:29, the subscription's session limit stopped every session:
"You've hit your session limit · resets 5:40pm", `api_error_status` 429. Four runs at
`xhigh` were complete, $0.78, $0.83, $1.21 and $2.03 by their results; two at `xhigh` and
three at `max` stopped mid-run, about $8.50; three at `max` never started. About $15 in
all. Nothing under the real `~/.claude` changed. Three defects, found reading the runs:
- **`guard.py` refuses a call that names `~/.claude` anywhere in its input**, a file's
  content included: 11 refusals in 7 runs, most of them a Write of a skill or of its
  evals that mentions `~/.claude`, which this repository's installer skills cannot
  avoid; the runs rewrote their text around it. It also refused two reads of the run's
  own persisted tool output, under the configuration folder's `projects/`. The runs
  made under it are biased, the complete ones included.
- **A run stopped by the limit records the reason `success`**: `harness.outcome` takes
  the result's `subtype`, which says `success` beside `is_error: true`.
- **No progress is visible while runs go**: `run.py` prints a line when a run ends, and
  the user, who could follow Phase 3's subagents in the IDE, could not follow these.
The user asked why the runs use `claude -p` rather than subagents. Answered from the
decision of 2026-10-06: the Agent tool sets no effort, a subagent's transcript lacks its
output tokens, and a session started by a script can be kept from the user's layer and
the skill's evals; what is lost is following the runs in the IDE, and the limit would
have stopped subagents alike, as it did four times in Phase 3. A stopped run cannot be
taken up where it stopped: `run.py` removes its folder, and a session resumed hours
later writes its whole cache again, which would inflate the cost this task measures.
The user chose one session at a time from now on, so that a stop loses one run, and
agreed to the three fixes. Tests first for each, watched failing:
- `guard.py` leaves out the text an editing tool writes — `content`, `old_string`,
  `new_string`, `new_source` — and still checks the file's path and a shell command
  whole; it lets pass the session's own folder, the event's `transcript_path` without
  `.jsonl`. Two of the new tests first passed for a wrong reason: their text ended on
  `~/.claude.`, and the guard counts a path only whole, a period being part of a name;
  their text was changed, and they failed as they should.
- `harness.outcome` gives a run stopped by an API error its `api_error` and the
  result's message, `usage_limit_reached: You've hit your session limit · resets
  5:40pm (Europe/Paris)`; `limit_reached` tells it, and `run.py` then starts none of
  the runs left.
- `run.py` sets each run's session id with `--session-id`, prints a line as a run
  starts, keeps `running.json` while it goes, and `--status` prints each run's state, a
  running one with its calls, its cost so far against its ceiling and its last call.

The two iterations made under the old guard were set aside under
`.eval-runs/skills/authoring-skills/limit-2026-10-07/`, and two new ones prepared with
the same options: `iteration-1` at `max`, `iteration-2` at `xhigh`.

At the user's word, the runs started at 13:55, one at a time, `max` first. The limit
stopped the third at 14:35, `usage_limit_reached` as the fix records it, and the three
runs left were not started. Done: `task-release-domain` twice at `max`, 42 and 37
calls, $3.14 and $2.64, 16 and 15 minutes; the reference task's first run stopped after
26 calls, $1.80. No refusal in any of them, every call on `claude-sonnet-5-5` at `max`,
the cost counted from each transcript equal to the result's for the complete runs, and
nothing under the real `~/.claude` changed. Two changes to `run.py`, tests first:
`--case` starts the runs of the cases named only, so that a case's runs at both efforts
can follow one another and a stop leaves whole comparisons; and each run's end line is
printed by its own worker, the log having shown a run's start before the previous run's
end, though the runs went one after the other.

At 17:56, at the user's yes, the release task's two runs at `xhigh`, then the grading of
the task's four runs, one session at a time. The release task at both efforts:

| | `max` | `xhigh` |
|---|---|---|
| Assertions passed | 6/7, 7/7 | 6/7, 6/7 |
| Cost | $3.14, $2.64 | $1.02, $0.86 |
| Duration | 16m01s, 14m53s | 5m16s, 4m38s |
| Calls | 42, 37 | 27, 20 |
| Grading | $0.36, $0.38 | $0.24, $0.27 |

Each run failed a different assertion: at `max`, no test proposed against a run without
the skill; at `xhigh`, two steps without their check, then semantic versioning
explained. `max` leads by one assertion over two runs, no more than the gap between its
own two runs: by the rule written before the runs, this task shows no headroom for
`max`, which costs 3.1 times as much and takes three times as long. The grader named
weak assertions in two of the four gradings, not the same ones, and found one false
claim in an account.

At 18:38, at the user's yes, the reference task: its two runs at `xhigh` complete,
$1.66 and $1.42, 8m40s and 8m17s; then the limit stopped its first run at `max` a
second time, after 14m16s and $2.60, and the second was not started. The user switched
accounts, and the two runs at `max` started again at 19:13, then the task's grading.
The reference task at both efforts:

| | `max` | `xhigh` |
|---|---|---|
| Assertions passed | 5/6, 5/6 | 5/6, 4/6 |
| Cost | $4.20, $4.02 | $1.66, $1.42 |
| Duration | 19m55s, 20m16s | 8m40s, 8m17s |
| Calls | 53, 47 | 32, 31 |
| Grading | $0.31, $0.21 | $0.24, $0.23 |

All four runs fail the same assertion, a short `SKILL.md` with the detail under
`references/`: each wrote one `SKILL.md` of 145 to 172 lines and no reference, as the
Verification run of Phase 3 did, which that phase noted as within the writing guide's
limits and watched. One run at `xhigh` also fails the description's "when" clause. No
refusal in any run, every call at the effort asked, nothing under the real `~/.claude`
changed.

After two of the three tasks, `max` leads on both by one assertion over two runs, never
by more than the gap between two runs at one effort, and costs 2.7 to 3.1 times as much
for two to three times the duration. The discipline task decides by the rule. Spent
today, at API prices: about $41, of which about $19 went to runs lost to the limit or
made under the old guard.

Where the next session starts, task 9 being open:

1. **Check where the runs stand**, with no cost:
   `domains/skill-tooling/skills/authoring-skills/scripts/run.py .eval-runs/skills/authoring-skills/iteration-1 --status`,
   and `iteration-2`. `iteration-1` is `max`, `iteration-2` `xhigh`: Sonnet 5.5, the
   skill alone, two runs per case, $10 a run. `runs-2026-10-07.log` beside them holds
   every line. The release and reference tasks are complete and graded at both
   efforts; the discipline task's four runs are not started. A run left `running` whose
   run.py ended shows `interrupted`: start it again. A complete run without
   `grading.json` is graded with `scripts/grade.py <iteration> --start --jobs 1`.
2. **The discipline task, the last**: `run.py <iteration> --start --jobs 1 --case
   discipline-real-claude-dir`, `xhigh` first, then `max`, one session at a time, then
   `grade.py` on both. About $10, announced to the user first; the subscription's limit
   has stopped a run three times today, so one task per step.
3. **Then the effort**: `benchmark.py` on both iterations, the three tasks compared by
   the rule written before the runs, above; the effort set in `workspace.py`'s default,
   the design's Runs section and this report's Decisions; the token-costs record's
   When To Revisit answered; task 9 ticked.
4. **Not committed since `5408047`**: `evals/evals.json`, `evals/test_sample.py`,
   `scripts/workspace.py`, `scripts/run.py`, `scripts/harness.py`, `scripts/guard.py`,
   `SKILL.md`, `tests/test_workspace.py`, `tests/test_run.py`, the domain's
   `CHANGELOG.md`, `docs/claude-code-coupling.md`, and this report.

### 2026-10-08

Resumed in a new session for task 9's last task. `--status` on both iterations: the
release and reference tasks complete and graded at both efforts, the discipline task's
four runs not started; `claude` 2.1.292. Announced to the user before any run: the
discipline task's two runs at `xhigh`, $2.48 by `run.py`, $1.24 a run from the four
complete runs at that effort; its two at `max`, $7.00, $3.50 a run; four gradings,
about $1.12 at $0.28 a session; about $10.60 in all, $41 if every run reached its
ceiling. By the rule written before the runs, `max` can no longer win on two of the
three tasks: the discipline task completes the comparison rather than deciding it. The
user said to start; the runs at `xhigh` started first, one at a time, their lines in
`runs-2026-10-08.log` beside the iterations.

The two runs at `xhigh` complete: $0.98 and $1.40, 6m06s and 6m41s, 21 and 32 calls,
every call at `claude-sonnet-5-5` and `xhigh`, no refusal. Both wrote the pressure
scenarios before the rule, left the rationalizations and red flags out for want of a
run that showed them, tried the installer in a throwaway folder only, and proposed a
mechanical guard beside the skill. The runs at `max` started at 09:21. A few minutes in,
the user asked to wait before any new run while they checked the credit left. `run.py`
cannot stop between two runs: once started with both, it starts the second when the
first ends. The second run's folder, empty, was made read-only, so that `run.py` fails
on writing its `running.json` before starting a session, the first run's files being
written by then. The user found 32% of the session's limit used and let the runs go on;
the folder's permissions were restored while the first run was still going, so that
`run.py` starts the second as planned.

The two runs at `max` complete: $2.39 and $3.06, 14m02s and 16m17s, 32 and 39 calls,
every call at `claude-sonnet-5-5` and `max`. The first had one refusal, a Bash call
holding `ls -la ~/.claude`, the real folder the case is about: the guard doing its work,
not the bias of 2026-10-07, and the run said so in its account. Both runs at `max`, like
both at `xhigh`, wrote no rationalization or red flag, proposed a mechanical guard, and
never ran the installer on the real folder; one at each effort widened the rule to
`enable` and `disable`, after the repository's `CLAUDE.md`, and one at each effort built
a fake installer or a fake repository under its `evals/`, so that a failing run of its
own cases touches no real installer. The four gradings started at 09:52, one session at a time.

The four gradings, $1.30: 6/6 and 6/6 at `max`, 6/6 and 5/6 at `xhigh`. The run that
failed considered no mechanical guard before building the skill, the guard appearing
only in its closing account; the grader named three weak assertions in that grading and
none in the three others. `benchmark.py` on both iterations:

| | `max` | `xhigh` |
|---|---|---|
| Pass rate | 92% ± 9% | 84% ± 11% |
| Release, reference, discipline | 13/14, 10/12, 12/12 | 12/14, 9/12, 11/12 |
| Cost a run | $3.24 ± $0.73 | $1.22 ± $0.31 |
| Duration a run | 1014 s ± 156 s | 397 s ± 97 s |
| Output a run | 128,128 | 42,916 |
| Grading | $1.95 | $1.59 |

By the rule written before the runs, `max` beats `xhigh` on no task: it leads on each by
one assertion over two runs, and one assertion is the gap between two runs at one
effort on each task, at `max` for the release task and at `xhigh` for the two others.
But it leads on all three, in the same direction, and the assertions `xhigh` failed
alone are of substance — two steps without their check, semantic versioning explained,
the description's "when" clause, no guard considered first —, where `max` failed alone
one, no test proposed. The one assertion both failed, every run, is the short
`SKILL.md` with its detail under `references/`. The design adds a third run per task
where the pass rates differ, as they do on all three: put to the user before any.

The user chose the third runs, and asked whether the long `SKILL.md` should be fixed
first. Not before: the effort is what is measured, so the skill stays the same across
a task's runs, and the failure, shared by every run at both efforts, does not tell the
efforts apart. `run.py` takes the skill from the iteration's frozen copy, so a fix in
the repository would not reach these runs anyway. The fix comes after task 9, as an
edit measured against the current version, once it is settled whether the skill or the
assertion asks too much: Phase 3 found 145 to 172 lines within the writing guide's
limits. `workspace.py` has no option to add a run to an iteration: `runs` went from 2
to 3 by hand in both `iteration.json` files, with a `run-3/` folder per case, the base
and the copies unchanged. `run.py` announced $3.67 at `xhigh` and $9.73 at `max`, the
means of the six complete runs at each effort; the runs started at `xhigh`, then `max`,
then the six gradings, one session at a time.

The three third runs at `xhigh` complete: $1.17, $2.01 and $1.35, 6m04s, 9m41s and
7m25s. The discipline run called its copy's `run.py` on an iteration of its own, without
`--start`: one `claude -p` process ran, its own. The release task's run at `max` started
at 11:09. At 11:19 the user read 47% of the session's limit used, against 35% eleven
minutes before, about $1.80 of runs in between. At that rate the two runs left at `max`
and the gradings, about $10, would not fit in the session. Their folders, empty, were
made read-only, as at 09:25, so that `run.py` stops after the run that goes; put to the
user.

The user chose to wait for the limit's reset and to go on in a new conversation, after
the gradings of the runs complete by then. The release task's third run at `max`
completed, $3.14, 17m21s, 41 calls; `run.py` then failed on the two read-only folders,
as meant, before starting any session. A one-off waiter meant to restore their
permissions once `run.py` ended matched its own command line in `pgrep -f` and never
ended; it was stopped, and the permissions restored by hand once no `run.py` ran: both
folders are empty and writable, their runs `not started`. The four gradings, $1.10:

| Third run | Assertions | Cost | Duration | Calls |
|---|---|---|---|---|
| Release, `xhigh` | 7/7 | $1.17 | 6m04s | 25 |
| Reference, `xhigh` | 5/6 | $2.01 | 9m41s | 41 |
| Discipline, `xhigh` | 6/6 | $1.35 | 7m25s | 32 |
| Release, `max` | 7/7 | $3.14 | 17m21s | 41 |

- The reference run at `xhigh` wrote `references/events.md`, the first of the task's
  runs to write a reference, and still failed the short `SKILL.md`: 131 lines and 1,124
  words against 84 lines in the reference, which holds the per-event sections only.
- Three refusals, one a run. The release run at `max` ran `ls ~/.claude`, the real
  folder. The two at `xhigh` were Bash heredocs writing text that names `~/.claude`, a
  `SKILL.md` edit and a fake `CLAUDE.md` for the run's own evals: the guard still checks
  a shell command whole, its text included, so a run writing through a heredoc meets
  the bias fixed on 2026-10-07 for the editing tools. Each run went on by another way.
- The grader found false claims in two accounts at `xhigh`: a source said to be read in
  three calls, an untested `CLAUDE_DIR` said verified.

`benchmark.py` again on both, the two runs not started left out at `max`:

| | `max`, 7 runs | `xhigh`, 9 runs |
|---|---|---|
| Pass rate | 93% ± 9% | 88% ± 11% |
| Release | 20/21, runs 6, 7, 7 | 19/21, runs 6, 6, 7 |
| Reference | 10/12, runs 5, 5 | 14/18, runs 5, 4, 5 |
| Discipline | 12/12, runs 6, 6 | 17/18, runs 6, 5, 6 |
| Cost a run | $3.23 ± $0.67 | $1.32 ± $0.36 |
| Duration a run | 1018 s ± 143 s | 419 s ± 99 s |
| Output a run | 127,168 | 44,991 |

The two runs left cannot change the effort. By the rule, `max` must beat `xhigh` on two
tasks by more than the gap between two runs at one effort. The release task is
complete: `max` leads by one assertion, the gap within each effort. On the discipline
task, even a full third run at `max`, 18/18 against 17/18, leads by one, the gap between
the runs at `xhigh`. So `max` can win the reference task at most, one task: `xhigh`
holds whatever the two runs give, read on the assertions' sums or on the pass rates.
The design still sets three runs where pass rates differ, which the proof follows:
whether to run them or to close the measure without them is the user's choice.

Where the next session starts, task 9 being open:

1. **Check where the runs stand**, with no cost: `run.py <iteration> --status` on
   `.eval-runs/skills/authoring-skills/iteration-1` (`max`) and `iteration-2`
   (`xhigh`), three runs per case now. `iteration-2` is complete and graded, 9 of 9.
   `iteration-1` holds 7 complete and graded runs; the third runs of
   `reference-claude-code-hooks` and `discipline-real-claude-dir` are not started.
   `runs-2026-10-08.log` beside them holds the day's lines.
2. **Put the choice to the user**: the two runs at `max`, about $6.50 by `run.py`'s
   mean of $3.23 a run, and their gradings, about $0.60, after which the proof is
   followed whole; or the measure closed on the runs made, the effort being settled
   either way. On 2026-10-08 the runs at `max` took about 12% of the subscription's
   session in eleven minutes: one run per step, `--case`, and the user's reading of
   the limit before each.
3. **Then the effort**: `xhigh`, by the rule. `benchmark.py` on both iterations;
   `workspace.py`'s default already says `xhigh`, so the effort is set by keeping it and
   saying why in its help; the design's Runs paragraph "Model and effort until task 9
   sets them" rewritten with the result; a Decision entry here; the When To Revisit
   item of `docs/decisions/2026-10-06-token-costs.md`, "When Phase 4 has measured the
   same evals at two efforts", answered in that record, a new section rather than its
   tables rewritten; task 9 ticked and the phase's status line recounted.
4. **After task 9**: the long `SKILL.md` of the reference task, under Problems And
   Deviations; the stop between runs and the added runs, the two gaps of `run.py` and
   `workspace.py` found today, before task 10's acceptance iteration; the guard's
   check of heredoc text, to weigh against a command that acts on what it names.
5. **Not committed since `5408047`**: `SKILL.md`, `evals/evals.json`,
   `evals/test_sample.py`, `scripts/guard.py`, `scripts/harness.py`, `scripts/run.py`,
   `scripts/workspace.py`, `tests/test_run.py`, `tests/test_workspace.py`, the domain's
   `CHANGELOG.md`, `docs/claude-code-coupling.md`, and this report. `assets/icon.png`
   at the root, untracked since 2026-10-07 21:16, comes from no work this report
   records: ask the user before adding it to a commit.

Resumed in a new session to close task 9. `--status` showed both iterations as the last
session left them. `iteration-2` was complete and graded, 9 runs. `iteration-1` had 7
complete and graded runs, and the third runs of the reference and discipline tasks were
not started. No session was running, and `claude` was 2.1.292. `run.py` announced the two
runs at $6.46, $3.23 a run. The user was given the choice: run them, about $7 with their
gradings, or close the measure on the runs made. The effort is `xhigh` either way. The
user chose not to run them, since they could not change the result.

`benchmark.py` on both iterations again gave the last table above. The effort is set to
`xhigh`:
- `workspace.py` keeps `xhigh` as its default, and its `--effort` help now says why.
- The design's Runs paragraph gives the result in place of "until task 9 sets them".
- `docs/decisions/2026-10-06-token-costs.md` gains a section, Effort, Measured, which
  answers its When To Revisit item.

Ticked task 9, and recounted the phase's status line, 9/14. The README's block waits for
the closure.

Task 9 cost about $59 at API prices. The 16 runs counted and their gradings cost $39.10.
About $20 went to runs lost to the limit or made under the old guard. The design
estimated $25 to $38. The grader named "The audit reports no error" weak in 9 of the 16
gradings, in all three cases.

Where the next session starts:

1. **Before task 10**, from Problems And Deviations, test-first where it is code:
   - `run.py`'s stop between two runs;
   - `workspace.py`'s option that adds runs to an iteration;
   - the guard's check of a heredoc's text;
   - the reference task's long `SKILL.md` and the weak assertions of `authoring-skills`'
     cases, which go together: settle whether the skill or the assertion asks too much.
2. **Task 10**: `references/eval-files.md` first, then the viewer.
3. **Not committed since `5408047`**: the files listed above, and
   `docs/decisions/2026-10-06-token-costs.md` and the phase file. `assets/icon.png` stays
   out of any commit unless the user says otherwise.

Committed as `9543f67`, with `assets/icon.png` at the user's word.

The user then asked for the two gaps of `run.py` and `workspace.py` to be fixed, tests
first for each, watched failing:
- `run.py --stop`, run from another shell, writes `stop.json` in the iteration. The
  `run.py` going checks for it before each run and starts none once it is there. The run
  going ends as it would, and `run.py` then says how many runs it left and clears the
  stop. `--stop` names the runs still going; `--status` shows a pending stop; the next
  `--start` clears any stop left from before. The test has the stub standing for
  `claude` run the real `run.py --stop` from inside the first run, and checks that the
  second run never starts.
- `workspace.py --extend <iteration> --runs N` raises an iteration's runs per case and
  configuration and adds the empty run folders. It refuses `--extend` without `--runs`,
  with any other option, or with no more runs than the iteration has. A test compares
  every file of the iteration before and after: only `iteration.json` changes, and it
  records the extension under `extended`. That holds even after the skill changes in the
  repository.

`SKILL.md` names `--stop` in the line for `run.py`. `--extend` is listed in
`workspace.py --help`, which `SKILL.md` points to. Committed as `f729a9c`.

Next, the guard's check of heredoc text. The user asked what to leave out, and when a
run needs `~/.claude`. Never as a folder: the skill's copy lies in the run's folder, the
evals' `env` points `CLAUDE_DIR` there, and Claude Code reads its configuration outside
tool calls. A run needs `~/.claude` only as words, since this repository's skills, its
`CLAUDE.md` and its documents name it as the install target. Of the day's four refusals,
two were reads of the real folder, `ls ~/.claude`, at `max`. The other two wrote text:
a fake `CLAUDE.md` through `cat > CLAUDE.md <<'EOF'`, and a `python3 - <<'EOF'` script
replacing text in a `SKILL.md`.

The user agreed to leave out a heredoc's body on two conditions:
- its delimiter is quoted, so that bash expands nothing in it;
- `cat` writes it to a file, unpiped, so that nothing runs it.

The rest of the command stays checked, the file written included, and so does any other
heredoc. A refusal now names the way to write such text: Write, Edit, or a quoted
heredoc that `cat` writes.

Tests first: the two that change the guard's behavior failed as they should. The
replaced test had checked that such a command was refused. The tests requiring a refusal
already passed, and they keep the rule from opening too wide:
- a heredoc given to `python3`, `bash` or a pipe;
- an unquoted delimiter with `$(…)` in the body;
- `cat` inside `$(…)`;
- `>&2`;
- a heredoc operator inside quotes.

`guard.py` gains a scanner of the command: quotes, the separators of simple commands,
redirections, and heredoc bodies after their line's newline.

Replayed through the new guard, the day's four refusals are all still refused. The two
reads are refused as they should be. The Python script is code. In the fake `CLAUDE.md`
command, the heredoc's body is now left out, but the same command also writes a
Makefile through `printf '…' > Makefile`, whose quoted text names `~/.claude`: a case the
rule does not cover.

At the user's reminder that every tie to Claude Code's architecture and to the names of
its folders and files goes into `docs/claude-code-coupling.md`, the eval tooling's rows
were completed in the same change:
- the guard's denied folders, its tool names and input keys;
- where `grade.py` finds the agent;
- the default model id, the effort levels and the `claude_version` field;
- `skill-grader`'s frontmatter;
- `authoring-skills`' eval cases.

---

## Decisions

- **A run's effort and model are set by the run procedure, never left to the
  session.** Phase 3's runs took the session's `max`, where thinking made 84% of their
  output. A benchmark left to the session's effort compares runs made under different
  conditions. Which effort the runs take is this phase's measure of `max` against
  `xhigh` to decide.
- **Output runs, with and without the skill, run in `claude -p`, not in subagents** (the
  user, 2026-10-06). The Agent tool sets no effort, and a definition that does must be
  installed first; `claude -p` takes the model, the effort and a cost ceiling as flags,
  and its transcript holds the final output tokens. This revises the README's opening
  decision that output evals run in subagents; the grader and the comparator stay
  agents. The design places the runs and keeps the skill's evals out of their reach.
  The README's opening decision follows at the closure.
- **The design is approved as proposed** (the user, 2026-10-06): the phase's `## Design`.
  It commits the phase to scripts that hold the mechanics of evaluation, each that starts
  sessions printing their count and estimated cost and starting nothing without
  `--start`; to runs in a copy of the repository outside any repository, without the
  skill's `evals/`, with the Skill and Agent tools denied and a guard hook; to the grader
  and the comparator started as `claude -p` sessions running their agents; to
  skill-creator's analyzer replaced by the benchmark's computed notes; to Sonnet 5.5 at
  `xhigh` for output runs and Opus 5.5 at `xhigh` for trigger sessions until task 9;
  to three runs per case and configuration in a benchmark, one to observe a baseline,
  three for a verdict that decides alone and three per trigger query; to "assertions"
  in `grading.json`; and to about $55 to $70 of runs for the phase's proofs. The reader
  of tokens and cost goes in `shared/usage/`, where roadmap `token-usage` extends it.
- **Every evaluation session leaves out the user's layer** (the user, 2026-10-06, after
  task 2's probe).
  - Flags: `--setting-sources project,local` and `--strict-mcp-config`, every `CLAUDE*`
    variable of the starting session removed, models named by their full ids, and a
    `claude` of 2.1.291 or later.
  - The project's own hooks and `CLAUDE.md` stay, as part of the repository the skill
    serves.
  - Grading and comparison sessions pass `--model` and `--effort` themselves.
  - Trigger sessions stop through a PostToolUse hook. They carry the user's other
    personal skills as copies, and run a query's repetitions in one folder.

  Tasks 5, 6, 7, 11 and 13 build on these flags. `docs/claude-code-coupling.md` gets their
  rows with `harness.py`.
- **The usage reader decides finality per message.**
  - A message whose last record carries a `stop_reason` counts as recorded. One without
    gets 5,400 output tokens and is marked estimated, whatever transcript holds it.
  - Cache writes are priced by their lifetime, 1.25 or 2 times the input price.
  - A model the table lacks leaves the cost unknown.

  The benchmark (task 8) shows a run's estimated calls; a `claude -p` run has none.
  Roadmap `token-usage` extends this reader, its prices and the estimate, and adds
  `cost-state`, which this reader does not read.
- **Each arm's copy of the repository holds its own version of the skill** (the user,
  2026-10-06, task 4). `base.tar` leaves out the skill's whole folder and the workspace;
  a run puts back the current version for `with_skill`, the baseline for `old_skill`,
  nothing for `without_skill`. `iteration.json` records `skill_path`, where task 5's
  `run.py` puts it back, and the case's `exclude` is applied when a run extracts the
  archive.
- **`kind` and `setup` are required in every case of `evals.json`.** The setup decides
  where a run works, and no default could be right for every skill; the kind is the
  case's test design (row W5). `assertions` may be empty, as before the baseline runs
  that create-and-edit's step 7 writes them from.
- **A case's inputs are fixed at preparation.** Its files are copied into the iteration
  and its fixture is built once into `fixture.tar`; a digest of what its runs receive —
  prompt, setup, `exclude`, `env`, files, base, fixture, not its assertions — decides
  `--reuse`, with the model, the effort and the baseline's snapshot.
- **The claude version goes in each `run.json`**, not in `iteration.json`: the binary
  changed between two sessions of this phase, 2.1.283 to 2.1.292.
- **A run keeps `CLAUDE_CONFIG_DIR`**, the one `CLAUDE*` variable of the starting
  session it inherits: it names the user's configuration and credentials, and the
  transcript's place. The design's Runs section now says so.
- **The guard refuses a denied path only whole**, as written, without its leading slash,
  or under the home folder as `~/`, `$HOME/` or `${HOME}/`, so that `/code/repo` leaves
  `/code/repository` alone; an unreadable call is refused. It denies the repository's
  root, the configuration folder and `~/.claude`.
- **A run's estimate never passes its ceiling.** The default of $2.50 a run, Phase 3's
  full skill-writing task, overstates a small case; `--budget` caps both the run and
  its announcement.
- **`grade.py` was written whole with task 6**, the grader's sessions and the skill's own
  `evals/grade.py`: the design has `grade.py` start the grader, and task 6's eval needed
  it. Task 7's proof is its tests.
- **The grader's answer format lives in its definition; `grade.py`'s request holds the
  inputs only.** The baseline was given the request alone, so that the eval measured what
  the definition adds. `grade.py` numbers the assertions and the answer grades them by
  number, never by a copy of their text.
- **`skill-grader` runs on `sonnet` at `xhigh`** (the user, 2026-10-07), the phase's
  default until task 9, set in its frontmatter and passed by `grade.py`.
- **A grading's run is re-graded whole**: its `grading.json` is removed before the
  skill's `evals/grade.py` runs, so that a stale entry never survives a changed
  assertion; a complete grading of another run is restored around the script.
- **`harness.py` is a library, without a shebang**; `run.py` and `guard.py` are commands.
  The sample skill lives under `evals/sample/` as `skill.md` and `evals.json`, with
  `build.py`, which writes it as a repository of its own, so that its runs touch no
  real repository.
- **A run counts in the benchmark when it is complete and graded on every assertion of
  its case.** The others go to `left_out` with their reason, and to a note; a stopped
  run's cost stays out of the figures.
- **Each metric rests on the runs that give it.** A figure a run lacks, such as a cost
  the price table cannot give, is left out of that metric, never counted as zero, and
  `n` says how many runs the metric rests on. A total of cost is unknown when one of its
  costs is. An output holding estimated calls counts `usage.py`'s estimate and is
  marked.
- **The standard deviation is the sample's, and none for a single value**, where
  skill-creator gives 0. Each run weighs alike in a mean pass rate, as in skill-creator.
- **`benchmark.json` departs from skill-creator's schema**: `summary` where it says
  `run_summary`, deltas as numbers rather than strings, `delta_of` naming the two
  configurations, and `by_case`, `assertions`, `left_out` and `cost_usd` added. Task 10
  adapts the viewer to it.
- **An iteration can hold the skill's arm alone** (`workspace.py --skill-only`), to
  measure the skill at another model or effort, as task 9 does; it takes no baseline.
- **The guard checks paths and commands, not the text a file receives** (task 9). A
  skill of this repository cannot avoid naming `~/.claude`, and a refusal of its text
  made the runs rewrite it. A shell command stays checked whole, since it can act on
  what it names. The session's own folder passes, where Claude Code sets aside the
  output it asks the session to read back.
- **Runs go one at a time when the subscription's limit is near** (the user,
  2026-10-07): a stop loses one run, and the runs not started stay so. A stopped run
  starts again from scratch, never resumed: a resumed session writes its cache again.
- **A run's progress can be followed while it goes**: `run.py --status`, from the
  transcript of the session id the run sets.
- **The benchmark's notes go past the design's three.** Besides the pass-rate delta beside
  the cost delta, the assertions that do not discriminate and those that vary, they name
  the assertions the grader called weak, the calls on another model or effort than the
  iteration's, the estimated outputs, the unknown costs and the runs left out, each read
  from files the benchmark already reads.
- **Eval runs take `xhigh`**, `workspace.py`'s default (task 9, 2026-10-08). On Phase
  3's three skill-writing tasks, `max` led on each by one assertion. That is no more than
  two runs at one effort differ. It also cost 2.4 times as much and took 2.4 times as
  long. By the rule written before the runs, `max` had to win two tasks by more than
  that gap. Its third runs on two tasks were not made, at the user's choice, since no
  result of theirs could change the effort. The other settings stay at `xhigh`:
  - `skill-grader`, since task 9 measured runs, not gradings;
  - trigger sessions, which stay on Opus 5.5, as the sessions a skill serves run.

  `--effort max` stays open to a measure that needs `max`'s margin.
- **A stop asked of `run.py` lets the runs going end** (2026-10-08). The stop is a file
  in the iteration, `stop.json`, so that another shell can ask for it without signalling
  a process. It never kills a session: a run cut off midway would be lost and paid for.
  A new `--start` clears it, being a new yes.
- **Runs are added to an iteration as a whole**: `--extend` raises the `runs` of every
  case and configuration, the one count `iteration.json` holds. `run.py --case` then
  starts only the cases that need the added runs. The others stay `not started`, and
  the benchmark lists them as left out.
- **The guard refuses access to a denied path, not the words that name it, as far as a
  string match can tell** (the user, 2026-10-08). A run never needs the real
  `~/.claude` as a folder, only as words in what it writes. Text written through Write
  or Edit, or through a quoted heredoc that `cat` writes to a file, passes. Anything a
  program could act on stays checked. The guard is a tripwire, not a sandbox: a script
  that builds the path, as `Path.home() / ".claude"` does, passes it. Isolating runs
  would take another `HOME`, where Claude Code would lose its credentials.

---

## Files Changed

---

## Problems And Deviations

- **Four premises of the approved design proved false in task 2's probe.**
  - `--settings` cannot turn off every hook for trigger sessions, since
    `disableAllHooks` also turns off the hooks `--settings` adds.
  - An installed copy of the skill shadows the copy passed with `--add-dir`.
  - An agent's `effort` does not apply to a session started with `--agent`.
  - The `claude` on the `PATH`, 2.1.283, does not know Sonnet 5.5 and maps `sonnet` to
    Sonnet 5.

  The amendments, approved by the user on 2026-10-06 and applied to the design:
  1. Every session gets `--setting-sources project,local` and `--strict-mcp-config`.
     Every `CLAUDE*` variable of the parent session is removed, not only `CLAUDECODE`.
     Models are named by their full ids.
  2. For trigger sessions:
     - the user's other personal skills are copied beside the copy under test;
     - a PostToolUse hook passed with `--settings` stops the session at the trigger or
       at the third call;
     - the project's own hooks stay;
     - a query's runs follow one another in one folder;
     - a trigger is a Skill call on the name, or a read under the copy's path. A read of
       the skill's source in the repository is recorded, not counted.
  3. Output runs keep the project's own hooks, as part of the repository the skill
     serves.
  4. `grade.py` and `compare.py` pass `--model` and `--effort` from the agent's
     frontmatter.
  5. `harness.py` refuses a `claude` older than 2.1.291, the version the probe
     validated.
  6. A description's trigger eval costs about $2 on Opus 5.5: 20 queries × $0.09, plus
     40 repeats × $0.008.
- **Sonnet 5.5's cache-write price in `docs/decisions/2026-10-06-token-costs.md`, $2.50,
  is not what 2.1.291 applies to a `-p` session's one-hour writes, $4.** Task 3 prices
  each write by the lifetime recorded in `usage.cache_creation`, and its recount of
  Phase 3's sessions against the record settles which price the record's figures need.
  Settled by task 3: $2.50 is the five-minute price, which subagents pay; $4 the one-hour
  price, which main sessions pay.
- **The token-costs record understated Phase 3: $176.38 by `cost-state`, not about
  $167.** Three sessions wrote their `cost-state` after the record, and its estimate of
  subagent output, 3,700 tokens a call, was low. A Recount section now gives the
  corrected figures; the record's own tables stay as written.
- **`usage.py` is not copied into `authoring-skills/scripts/` yet.** Every file of a
  skill must be reached from its `SKILL.md`, and no script of the skill imports it yet.
  The copy lands with task 5, whose scripts import it, through
  `tools/shared.py <skill-dir>`.
  Landed with task 5: `run.py` imports it.
- **The design's `base.tar` let a baseline read the skill under test.** It kept the
  skill's folder minus `evals/`. Changed at the user's choice, above; the design's
  Workspace and Runs sections now say so.
- **This repository's two `evals.json` files are refused by `workspace.py`:** no case
  has `kind` or `setup`. `authoring-skills`' gain them with task 9, which runs its three
  skill-writing cases; the roadmap's with Phase 5, which moves its evals onto this
  tooling. `authoring-skills`' fourth case also cites a path of Phase 3's workspace in
  its prompt, which a run's copy will not hold.
- **Task 6's eval cost $0.74, not the $8 the design estimated.** A grading of a small
  run costs about $0.04 on Sonnet 5.5 at `xhigh`, in three calls. `grade.py`'s default
  of $0.45 a session, skill-auditor's mean at `max`, stays until a skill's gradings give
  their own mean: a grader reading a full skill-writing run's transcript, 48 to 107
  calls, will cost more, and task 9's runs will show how much.
- **The grader's fixtures needed tighter assertions than the sample's.** The
  sample's first assertion, `YYYY-MM-DD-<slug>.md`, also passes a wrong date and a slug
  not drawn from the subject: by the grader's own rule it is weak. The sample keeps it;
  the acceptance iteration will show whether the grader names it.
- **`references/eval-files.md` is not written yet.** The design puts every file's schema
  there; it is written once `run.json`, `grading.json` and `benchmark.json` exist, so
  that it describes the formats the scripts write rather than plans for them.
  `workspace.py`'s docstring and refusals name the keys meanwhile.
  With task 8, all three exist. The reference is written at the start of task 10,
  before the viewer that reads them.
- **Task 9's first runs were lost to the subscription's limit and biased by the
  guard.** The limit stopped every session twelve minutes in, about $15 spent; the
  guard had refused 11 calls in 7 runs, most of them a skill's text naming `~/.claude`.
  The guard was fixed and every run is made again, one at a time.
- **`authoring-skills`' fourth case cannot run through `run.py` yet.** Its prompt names
  a folder of Phase 3's workspace, and its audit operation starts `skill-auditor`, while
  runs are denied the Agent tool and no agent of the domain is defined in a run's copy.
  Recorded in its `pending` line; left open, to settle before a skill whose operation
  starts an agent is evaluated, Phase 5's comparison running the three skill-writing
  cases only.
- **`run.py` cannot stop between two runs** (task 9, 2026-10-08). Once started, it
  starts every run listed; twice the user asked for a pause while a run went, and the
  next runs' folders were made read-only so that `run.py` failed before starting their
  sessions. Left open: a stop asked from outside — a file in the iteration that
  `run.py` reads before each run, or `--status` offering it — to be built test-first
  before task 10's acceptance iteration, which starts twelve runs.
  Fixed on 2026-10-08: `run.py --stop`.
- **`workspace.py` cannot add runs to an iteration** (task 9, 2026-10-08). The design's
  third run per task where pass rates differ needed one: `runs` was raised by hand in
  `iteration.json`, with a `run-3/` folder per case. Left open, with the stop above: an
  option that raises an iteration's `runs` without touching its base, copies or
  digests.
  Fixed on 2026-10-08: `workspace.py --extend`. `iteration-1` and `iteration-2`, raised
  by hand before the option existed, have no `extended` record.
- **The reference task's short `SKILL.md` failed in its four graded runs** (task 9).
  Each, like Phase 3's Verification run, wrote one `SKILL.md` of 145 to 172 lines and no
  `references/`. The third run at `xhigh`, not graded yet, wrote 131 lines and
  `references/events.md`. Not fixed during the measure, at the user's agreement, so that
  the skill stays the same across a task's runs. After task 9, from the graded third
  runs: settle whether the skill or the assertion asks too much, then, if the skill,
  edit it and measure the edit against the current version on that case.
  The third run at `xhigh`, graded since, failed it too: 131 lines in `SKILL.md`
  against 84 in its one reference.
- **The guard still refuses a Bash heredoc whose text names `~/.claude`** (task 9,
  2026-10-08). The fix of 2026-10-07 left out the text the editing tools write; a shell
  command stays checked whole, its heredoc included. Two of the three third runs at
  `xhigh` met it, writing a `SKILL.md` edit and a fake `CLAUDE.md` that way, and went on
  by another way. Left open: whether a heredoc's body can be left out while the
  command that receives it stays checked, to weigh with the rest after task 9.
  Fixed on 2026-10-08 for a quoted heredoc that `cat` writes to a file. A heredoc given
  to a program, such as the Python script, stays checked. So does quoted text written
  another way, such as the `printf` in the same command as the fake `CLAUDE.md`. Left
  open: whether runs meet those often enough to matter, read from the refusals of the
  next iterations.
- **Task 9's proof was not followed whole** (2026-10-08). The design sets a third run per
  task where pass rates differ. Two of the six were not made: the reference and
  discipline tasks at `max`. The user chose this once the rule's outcome no longer
  depended on them. Their folders stay in `iteration-1` as `not started`, and its
  benchmark lists them as left out.
- **Task 9 cost about $59, against the design's $25 to $38.** About $20 went to runs lost
  to the limit or made under the old guard. A run at `max` cost $3.23, not $2.50: a
  `claude -p` run writes one-hour cache entries. Every task also took a third run.
- **Several of `authoring-skills`' assertions are weak by the grader's reading** (task
  9). The grader named "The audit reports no error" weak in 9 of the 16 gradings, across
  all three cases: a skill that is wrong on the point of its case still passes it. It also
  named assertions that only ask for something to be absent. Left open, with the
  reference task's long `SKILL.md`: revise the cases' assertions before Phase 5's
  comparison runs them.

---

## Changes To Later Phases

- `docs/roadmap/pending/roadmap-execution/phase-0-framing.md`, roadmap
  `roadmap-execution`, at the user's request on 2026-10-06:
  - added the task that settles when `execute-phase` hands over to a new session,
    whether at a phase's end, at a task's end, or past a context threshold declared in
    `[roadmap]`;
  - added a constraint giving the figures of `docs/decisions/2026-10-06-token-costs.md`;
  - the phase holds 7 tasks now. Its opening decision, one phase per conversation, may
    change there.
- `phase-5-switch-over.md`, at the user's request on 2026-10-06 to update what the
  removal of every plugin made stale:
  - The Objective no longer turns `superpowers:writing-skills` and skill-creator off,
    done on 2026-10-04, and names the install and the decision record. This change is
    a restructuring, made at the user's request in those words.
  - Why This Phase Matters and Out of Scope follow the Objective.
  - The section Proof becomes Comparison With The Old Tools, so that it is not confused
    with the `Proof:` lines, and Turn Off becomes Install And Release.
  - The first task gives the old tools to the runs from their copies under
    `study/skill/`.
  - `tests/check.py` and `.claude/settings.json` join Files to Modify.
  - Each of the 12 tasks has a `Proof:` line, approved by the user on 2026-10-06.
- `phase-5-switch-over.md`, with the design's approval: the task that moves the roadmap
  evals' `grade.py` also has its `grading.json` say `assertions`, where skill-creator's
  said `expectations`, and moves its runs to this phase's run script.

---

## Assessment
