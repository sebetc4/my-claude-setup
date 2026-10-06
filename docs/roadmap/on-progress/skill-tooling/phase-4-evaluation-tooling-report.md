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
- **The design's `base.tar` let a baseline read the skill under test.** It kept the
  skill's folder minus `evals/`. Changed at the user's choice, above; the design's
  Workspace and Runs sections now say so.
- **This repository's two `evals.json` files are refused by `workspace.py`:** no case
  has `kind` or `setup`. `authoring-skills`' gain them with task 9, which runs its three
  skill-writing cases; the roadmap's with Phase 5, which moves its evals onto this
  tooling. `authoring-skills`' fourth case also cites a path of Phase 3's workspace in
  its prompt, which a run's copy will not hold.
- **`references/eval-files.md` is not written yet.** The design puts every file's schema
  there; it is written once `run.json`, `grading.json` and `benchmark.json` exist, so
  that it describes the formats the scripts write rather than plans for them.
  `workspace.py`'s docstring and refusals name the keys meanwhile.

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
