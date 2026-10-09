# Phase 5 Report: Switch-Over

**Phase:** [phase-5-switch-over.md](phase-5-switch-over.md)
**Start Commit:** 5b2065e

---

## Work Log

### 2026-10-09

Opened the phase from Phase 4's closure, committed as `5b2065e`. Read Phase 4's file and
its report, finalized in this session: no restructuring pending, and no other phase in
progress. What binds this phase:
- the evaluation tooling Phase 4 built: runs are `claude -p` sessions, Sonnet 5.5 at
  `xhigh`, one at a time near the subscription's limit, each paid step at the user's yes;
  a skill-writing task costs about $1.30 a run and $0.25 a grading;
- when a run fails an assertion, the assertion is read before the skill;
- `authoring-skills` has no trigger queries yet, and its description gained "evaluates"
  in Phase 4 without them: the trigger task writes them and measures both texts;
- the fourth case of `authoring-skills` cannot run while runs are denied the Agent
  tool, so the comparison runs the three skill-writing cases;
- the roadmap evals still run skill-creator's scripts from `study/`;
- `CLAUDE.md`'s layout already names the evaluate operation, so the `CLAUDE.md` task is
  left with the gotchas.

Two dependencies of the first task are not settled. Put them to the user before any work:
- **Four configurations.** `workspace.py` prepares two per iteration, `with_skill` and
  one baseline, and `--reuse` takes only the baseline's runs. A baseline from a folder is
  copied under the name of the skill under test, and its run is told "Use the skill
  `authoring-skills`". Comparing no skill, `writing-skills` 6.4.1, skill-creator and
  `authoring-skills` takes three iterations whose `with_skill` runs are paid three times,
  or a change to `workspace.py` first.
- **skill-creator in a run.** Its loop starts subagents and `claude -p` sessions. A run
  is denied the Agent tool, and its preamble forbids starting `claude`. So skill-creator
  would run without the part that makes it skill-creator, unless the comparison says
  how its arm is scored.

The cost to announce: three tasks × four configurations × three runs is 36 runs, about
$47 at `xhigh`, with about $9 of gradings. At the user's rule, the opening ends the turn:
no work on the phase yet.

In a new session, at the user's request, measured what Phase 4 cost, the user having kept
its sessions short to manage the context. The sources were the transcripts of its
sixteen main sessions and of the 218 `claude -p` sessions they started, counted with
`shared/usage/usage.py` and one-off scripts. Recorded in
`docs/decisions/2026-10-09-phase-4-token-costs.md`; the 2026-10-06 record points to it.
- About $187 in all, about $176 without the session that measured Phase 3: as much as
  Phase 3's $176.38.
- The main thread, $115.47 at `xhigh`, read 37% less cache a call, a mean context of
  about 190,000 tokens against 299,000. It made 62% more calls for the phase's work, and
  each opening cost $1.27 to $2.12. The roadmap documents read cost about $13.25; the
  report alone, about 50,000 tokens at the end, about $5.92.
- One subagent ran, $0.63. The `claude -p` sessions cost $69.32, $56.35 of it for task
  9, of which $17.26 went to runs the subscription's limit stopped.
- 18 tool reviews cost about $6.09, and four cache rebuilds after a change of
  organization at the limit about $6.50.

At the user's request, the roadmaps were then made to know both records and what they
raise:
- this phase's constraints give Phase 4's run costs and fixed costs, before its 36 runs;
- `roadmap-execution`, 1.1.0, and `token-usage`, 1.0.1, as listed under Changes To Later
  Phases;
- this roadmap's README links both records.

In a third session, put the two dependencies to the user. Reading `workspace.py` again
first showed the opening wrong on the first: `--baseline-only` prepares the baseline arm
alone, as iteration 3 of Phase 4 did, so three iterations pay each configuration once,
36 runs in all, with no change to `workspace.py`. What it costs instead: no benchmark
holds the four configurations, so the table comparing them is assembled from the three
`benchmark.json`. Iterations 1 and 2 cannot give the `with_skill` runs: the skill has
changed since, in `18a1c65`. The user chose the three iterations and the same limits for
every arm, and gives each `--start` its own go-ahead.

Prepared A as `iteration-5`. `run.py` announced 18 runs at $12.71, $0.71 a run: the mean
of the skill's 23 complete runs, the cheaper evaluation cases included, where Phase 4
measured about $1.30 on the skill-writing cases; announced to the user as about $23.
Started at the user's go-ahead on 2026-10-09 at 08:30 UTC, one run at a time, its log in
`.eval-runs/skills/authoring-skills/runs-2026-10-09.log`.

Reading `run.py` before B and C: in a `repository` case, it puts the baseline arm's copy
back at the skill's path, `domains/skill-tooling/skills/authoring-skills/`. Right for an
earlier version of the same skill, wrong for another tool: each run of B and C would
have found `writing-skills` or skill-creator in the repository as the domain's skill,
under a `CLAUDE.md` that describes another. At the user's choice, fixed test-first while
A ran: `workspace.py` records `in_repository`, false for a folder whose `SKILL.md` names
another skill, and `run.py` then gives that arm its copy only. Two tests in
`test_run.py`, watched failing; `make check` passes. Prepared B as `iteration-6` and C as
`iteration-7`, each recording `in_repository: false`.

While A ran, the task on `tests/check.py`: it found skills under `domains/*/skills` only.
It now reads `dirs` from the `[skills]` table through `shared/conventions/conventions.py`,
the source, loading the file at the root it is given rather than searching upwards; when
the file is missing or the table cannot be read, it checks `domains/*/skills` and says so
in a warning, since the file is ignored by git and a fresh clone has none. `main` and
`options` take the root, so that the proof's fixture repository runs through them. Two
tests in `tests/test_check_skills.py`: the fixture's `.claude/skills/broken`, whose name
differs from its folder, reported `[N3]`, red first for want of the parameter, then, once
it existed, red because the skill was not found; then green. `make check` passes, three
skills checked, as before: this repository has no `.claude/skills` yet. `CLAUDE.md`'s
line on `tests/check.py` says where the skills are found.

Then the trigger task's queries, written before any measure: 24 in `authoring-skills`'s
`evals.json`, 12 that should trigger over what `writing-skills` and skill-creator
answered — creating a skill, editing one, checking it before an install, running its
evals, benchmarking two versions, comparing them blind, tuning a description, turning a
session's work into a skill — and 12 near misses, each with what it nearly matches:
`CLAUDE.md`, a hook, an agent definition, the audit runner's bug, the installed skills,
an install, a domain's tests, a summary of a skill, a model benchmark, a decision record,
a roadmap named after skills, a system prompt. Half in French, as the user writes. The
description of `b3fa90e`, before "evaluates", is in
`.eval-runs/skills/authoring-skills/description-b3fa90e.txt`. `triggers.py` announces 72
sessions on Opus 5.5 at `xhigh`, $3.67, for each description.

The user put both trigger measures after A, and chose one conventions reference for the
two tools, the mapping of an old contract moved out of it. In
`shared/conventions/conventions.md`: the `residue` row says `.gitignore` patterns
without restating how they match; "the skill's folder" for "directory", where the
working directory stays; `scripts/conventions.py` named where it said "the reader";
"run a `checks` command as any other command, never as one the user already approved"
for the claim on the permission flow; Create The File points to the skill's own
reference for an old contract. The mapping went to the roadmap skill's new
`references/old-contract.md`, which its `SKILL.md` names on `missing`. `make shared`
refreshed both copies; the roadmap domain is 2.0.1.

Task 4's static part at the same time: `audit.py` passes on `tool-review` and passes on
`roadmap` with one warning, `[X3]` on `close-phase.md`, `check_links.py` run through
`python3`. Called by its path there, and in `SKILL.md`'s Scripts section, the warning
moved: `run through bash`. The rule read the language of the code fence, ```` ```bash ````,
as an interpreter, its whitespace crossing the line end; a test of a fence, watched
failing, then the rule kept to one line. I had also allowed `progress.py` and
`check_links.py` in the domain's `permissions.json`; `test_permissions.py` failed, its
name saying the domain pre-approves the conventions reader alone, a decision of 2.0.0,
so both rules came out. `make check` passes, no warning left.

Then task 7, the roadmap evals on the new tooling. `run.py` keeps a run's added and
changed files in `outputs/` and their list in `changes.json`, where skill-creator's runs
kept the whole repository; so `evals/grade.py <iteration>` rebuilds each run's final tree
from the case's `fixture.tar`, less the deleted files, with `outputs/` over it, and
decides the same assertions from it, written under `assertions`. `build_fixtures.py`
became `fixtures.py <case> <folder>`, the interface `workspace.py` calls. One change to
the fixtures: `.agent-conventions.toml` is tracked, no longer ignored, since `run.py`
collects with `git add -A` and would not see the create case's run completing the
contract. Eight tests in `evals/test_grade.py`, watched failing, then green.

The proof, at no cost: `workspace.py` prepared the roadmap's `iteration-2` against
`1073ead`, one run per case and configuration; a one-off script poured into it the six
runs of 2026-10-01, from skill-creator's layout, with their own fixtures as
`fixture.tar` and each run's changes computed against them. `grade.py --start` of
`authoring-skills` ran the skill's script, which decided every assertion, so no grader
session started, $0.00. The results match 2026-10-01 run by run — 10/10, 10/10, 9/9,
9/9, 3/3, 2/3 — and `benchmark.py` gives what skill-creator's benchmark gave:
`with_skill` 100% ± 0%, `old_skill` 89% ± 19%, durations 563.1 s and 746.9 s. Its
header names Sonnet 5.5 at `xhigh`, the iteration's default, not what those runs used;
their tokens and costs were never recorded. `grep -rn "study/skill/create-skill"
domains tests tools` finds nothing.

A's runs went on meanwhile, one at a time: seven complete, then
`reference-claude-code-hooks/with_skill/run-2` stopped at $0.97 on the subscription's
limit, which resets at 15:20 Paris time; ten not started. A resumes with `--start`.

In a new session, task 3: the 68 rows of the Phase 0 matrix,
`docs/decisions/2026-09-28-skill-tooling.md`, checked against `authoring-skills` and its
agents.
- **Built as ruled, 51 rows:** W1-W4, W6-W14, W16, W17, W19, W20, W23, W25, W26, W30;
  S1, S2, S4-S9, S11-S16, S18-S21, S23-S29, S31-S34, S37. S34 holds once
  `references/eval-files.md` opens with `## Contents`, added at the user's choice: 299
  lines, one under the size budget's 300, where the matrix promised one.
- **Dropped as ruled, 10 rows:** W15, W21, W24, W27, W28, W29, `docs/claude-code-coupling.md`
  written; S3, S35, S36, S38.
- **Built otherwise, 6 rows:** W5, three kinds — reference, task, discipline —, a
  technique being a task and a pattern a reference; W22, the micro-test a procedure in
  `create-and-edit.md`, no script; S17, the assertions written from the baseline's
  failures, W1's order, `review` holding what only a person judges; these three
  confirmed by the user on 2026-10-09. S10, the no-surprise rule in the writing guide,
  and in the audit `X4` and `C5`, as the rule catalogue of 2026-10-03 has it, rather
  than a rule on a project skill granting itself tools; S22, the benchmark's notes and
  "read the transcripts", Phase 4's design approved on 2026-10-06; S30, a separate
  session proposes each rewrite, the user on 2026-10-08, and `tuning.json` with `best`
  stand where skill-creator wrote an HTML report, Phase 4's design.
- **Missing, 1 row:** W18, a table of the rationalizations for skipping the evaluation,
  to keep only once a run showed a session skipping it; none did. Dropped by the user on
  2026-10-09, to come back with such a run.

Then the user ruled on what is left to pay for and on the install. A resumes now, on the
account this session runs under, one run at a time with the user's yes before each, a
session's limit not holding $14 of runs; the nine `skill-auditor` runs of tasks 4 and 6
go the same way. Each run is started alone: `run.py --start --jobs 1`, then `run.py
--stop` once it has started, so that no second run follows.

While A's runs go, two steps that start no session. Task 9: `domains/review/hooks/tools.json`
lists `authoring-skills`, `skill-auditor` and `skill-tooling/audit_skill.py`; review
0.1.3. `skill-grader` and `skill-comparator` stay out: `grade.py` and `compare.py` start
them in unattended `claude -p` sessions, which `review.py` never reviews. `make check`
passes. The probe waits for the install, since a review covers only the tools the
installer's state names. Task 8's first step: `make enable D=skill-tooling` into a
throwaway folder installed 32 files, no `__pycache__`, the hook in `settings.json` and
one allow rule, for `scripts/audit.py`; the installed hook, given an Edit of
`domains/roadmap/skills/roadmap/SKILL.md`, exits 0 in silence on that clean skill.

Three more runs of A, each at its own yes, each started alone by a helper script in the
session's scratchpad: `run.py --start --jobs 1`, then `run.py --stop` once the log shows
it started. `reference-claude-code-hooks/with_skill/run-2` $1.93 in 9.4 minutes, `run-3`
$1.57 in 7.5, `without_skill/run-1` $2.19 in 11.3. A stands at 10 of 18 runs complete,
$14.81 in all:

| Case | Configuration | Runs | Cost | Minutes | Refusals |
|---|---|---|---|---|---|
| task-release-domain | with_skill | 3 | $1.71, $1.53, $0.98 | 8.7, 7.9, 5.1 | 1, 0, 0 |
| task-release-domain | without_skill | 3 | $1.04, $1.37, $0.83 | 5.5, 7.3, 4.2 | 2, 0, 2 |
| reference-claude-code-hooks | with_skill | 3 | $1.66, $1.93, $1.57 | 8.0, 9.4, 7.5 | 0, 0, 0 |
| reference-claude-code-hooks | without_skill | 1 of 3 | $2.19 | 11.3 | 1 |

The guard's six refusals are of two kinds. Three runs without the skill looked for
`authoring-skills` under `~/.claude` or across the disk, which the guard is there to
refuse. Three runs, one with the skill, edited `docs/claude-code-coupling.md` through a
Python heredoc whose text names `~/.claude`, the case Phase 4 left open: each went on
another way. At the user's word, the session stops here, to go on in a new one.

**Where the next session starts:**
1. A's eight runs left, in `run.py`'s order: `reference-claude-code-hooks/without_skill`
   runs 2 and 3, then `discipline-real-claude-dir`, three `with_skill` and three
   `without_skill`. Each one alone, at the user's yes, with its estimate: $1 to $2.20 for
   the reference case. `iteration-5/stop.json` is left in place; `--start` clears it,
   and the helper sets it again. Then `grade.py`, `benchmark.py`, the same way.
2. B, `iteration-6`, and C, `iteration-7`, nine runs each, the same way.
3. The two trigger measures, after A: `triggers.py` with the current description, then
   with `--description .eval-runs/skills/authoring-skills/description-b3fa90e.txt`; 72
   sessions on Opus 5.5 at `xhigh`, $3.67 each, announced to the user as two steps.
4. Tasks 4 and 6: nine `skill-auditor` runs — `roadmap`, `tool-review`,
   `authoring-skills`, three each —, a general-purpose agent on Sonnet told to act as the
   agent, given the skill's folder, the writing guide's path and `audit.py`'s output;
   each one at the user's yes.
5. Task 8: `make enable D=skill-tooling` on the real `~/.claude` at the user's go-ahead,
   `make update D=review` for 0.1.3, then the registration of `audit_skill.py` removed
   from `.claude/settings.json`; then task 9's probe.
6. Tasks 10 to 12. The gotchas gathered so far for `CLAUDE.md`: an Edit under `.claude/`
   waits for a permission in a headless run even with `acceptEdits` (Phase 2 report);
   with `TMPDIR` inside this repository, the tests that build a repository in a
   temporary folder find this repository's `.agent-conventions.toml` and fail (Phase 3
   report); Phase 4's probe of `claude -p` — `disableAllHooks` also turns off the hooks
   `--settings` adds, an installed copy shadows one passed with `--add-dir`, an agent's
   `effort` does not apply under `--agent`, a model is named by its full id,
   `--setting-sources project,local` keeps auto memory, which `autoMemoryEnabled: false`
   turns off; and the Skill evals gotcha, which still points at `evals/grade.py`, to
   point at `run.py`. Layout: a skill's `evals/` gains `fixtures.py` and `grade.py`.

In a new session, resumed from that point. The helper, gone with the previous session's
scratchpad, was written again in this one's. At the user's yes,
`reference-claude-code-hooks/without_skill/run-2` started at 13:46 UTC, alone. The user
then closed the editor's window: the helper ran as a background command of the session,
and it ended with the window, `run.py` and the run's `claude -p` session with it. The
run's transcript stops at 13:54 UTC, 17 calls, $1.24 counted with
`shared/usage/usage.py`, with no result; `run.py --status` marks it interrupted, and the
next `--start` starts it again from a fresh copy. Its work folder,
`/tmp/skill-run-b8s41d2i`, was left behind.

Started again at the user's yes, the window kept open: complete, $2.02 in 10.1 minutes,
one refusal, again a Python heredoc naming `~/.claude` while editing skill files.
`run-3`, at its own yes: $1.98 in 9.9 minutes, one refusal of another kind, the final
checks run on a copy of the repository made with `mktemp -d`, with a stub of the
`audit.py` this arm lacks, outside the run's work folder. A stands at 12 of 18 runs,
$18.81 in all, the reference case done. `discipline-real-claude-dir/with_skill/run-1`:
$1.23 in 7.5 minutes, no refusal; `run-2`, $0.86 in 5.4 minutes, no refusal; `run-3`,
$1.01 in 5.4 minutes, one refusal: a `printf` appending a row to
`docs/claude-code-coupling.md`, its text naming the real Claude Code folder, the same
family as the heredocs. A stands at 15 of 18 runs, $21.91 in all, besides the $1.24 of
the interrupted run. At the user's word, the session stops here, its context near full,
to go on in a new one.

**Where the next session starts** — this list replaces the previous one:
1. A's three runs left: `discipline-real-claude-dir/without_skill` runs 1 to 3, $1 to
   $2.50 each, none measured yet at this iteration. Each one alone, at the user's yes,
   with the window kept open: `bash .eval-runs/skills/authoring-skills/one_run.sh
   <iteration-folder> <log>`, both paths absolute, run as a background command; the
   helper is kept there, ignored by git, and the log of the day is
   `runs-<date>.log` beside it. Then `grade.py`, `benchmark.py`, the same way.
2. B, `iteration-6`, and C, `iteration-7`, nine runs each, the same way.
3. Steps 3 to 6 of the previous list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.
4. `/tmp/skill-run-b8s41d2i`, the interrupted run's work folder, to remove at the
   user's word.

In a new session, resumed from that point. At the user's yes,
`discipline-real-claude-dir/without_skill/run-1` started alone: $1.69 in 9.2 minutes. A
stands at 16 of 18 runs, $23.60. `/tmp/skill-run-b8s41d2i` removed at the user's word.
While it ran, the user allowed the runs left in parallel. A second `run.py --start` on
`iteration-5` would have started run-1 again beside itself and cleared the stop the
first `run.py` was waiting on, so A's runs 2 and 3 were left for after run-1. B and C
started, `--jobs 3` each, their logs `runs-2026-10-09-iteration-6.log` and
`runs-2026-10-09-iteration-7.log`, announced at $9.04 each by `run.py`'s $1.00 a run,
about $26 for both at A's measured $1.46. At that figure the user stopped further
starts to check the session's usage first: `run.py --stop` on both, with the three
`task-release-domain` runs of each going on to their end. All six completed:

| Iteration | Case | Configuration | Runs | Cost | Minutes | Refusals |
|---|---|---|---|---|---|---|
| A, `iteration-5` | discipline-real-claude-dir | without_skill | 1 of 3 | $1.69 | 9.2 | 2 |
| B, `iteration-6` | task-release-domain | old_skill, `writing-skills` | 3 of 9 | $0.65, $1.27, $0.99 | 3.6, 6.5, 5.1 | 0, 1, 1 |
| C, `iteration-7` | task-release-domain | old_skill, skill-creator | 3 of 9 | $1.22, $1.70, $0.75 | 6.2, 7.8, 3.9 | 0, 1, 0 |

The session's seven runs cost $8.27. Of the five refusals, three are the heredoc family:
a Python heredoc editing a file, its text naming `~/.claude` (A, B run-3, C run-2). A's
run-1 also looked for `authoring-skills` under `~/.claude` and across the disk. B's
run-2 removed a probe it had left in `/tmp`, outside its work folder. B and C cost less
on `task-release-domain` than A did, $0.65 to $1.70 against $0.83 to $1.71. The user then
saw 85% of the session's usage limit used, a window that likely also holds the previous
session's five runs, started from 13:46 UTC, and ruled: no run started again in this
session; everything recorded, to go on in a new one.

**Where the next session starts** — this list replaces the previous one:
1. The 14 runs left: A's `discipline-real-claude-dir/without_skill` runs 2 and 3; B's and
   C's six each, `reference-claude-code-hooks` and `discipline-real-claude-dir`, three
   `old_skill` runs each. About $1.20 to $1.50 a run, $17 to $21 in all, more than one
   window of the usage limit holds: the user sets how many go and how many at a time,
   with a look at the session's usage first. `run.py <iteration> --start --jobs N`, only
   on an iteration that no `run.py` is running on; every `stop.json` was cleared when its
   `run.py` ended. `one_run.sh`, kept beside the iterations, still starts one run alone.
   Logs: `runs-<date>.log` for A, `runs-<date>-iteration-6.log` and
   `runs-<date>-iteration-7.log` for B and C.
2. Then `grade.py` and `benchmark.py` on each iteration, and the four-column table.
3. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

In a new session, resumed from that point. The user chose a batch of six runs, B's and
C's `reference-claude-code-hooks`, six at a time, about $11 at A's cost on that case.
Started as two background commands, each `run.py --start --jobs 3` then `run.py --stop`
once three runs had started, by a helper in the session's scratchpad. After about seven
minutes the subscription's session limit stopped all six, `usage_limit_reached`, resetting
at 23:00 Paris time: $8.31 spent with no result, $1.24 to $1.61 a run. `run.py --status`
marks them stopped, and `--start` runs them again from a fresh copy. The user then had the
six go again two at a time, one run of B beside one of C, `--jobs 1` on each iteration
with the stop set once three had started, so that a limit reached again costs two runs.
Once the first pair had started, the user asked that no further run start without their
yes: `run.py --stop` on both iterations, the pair going on to its end; each next pair
waits for its own yes. The pair completed: B's `reference-claude-code-hooks/old_skill/run-1`
$2.03 in 9.6 minutes, one refusal, a Python heredoc editing `SKILL.md` whose text names
`.claude`; C's $2.69 in 9.9 minutes, no refusal. Then, at the user's yes, B's `run-2`
alone, started with `one_run.sh`: $1.24 in 6.5 minutes, no refusal. C's `run-2`, at its
own yes: $2.14 in 9.2 minutes, no refusal.

The four complete runs cost $8.10, the six the limit stopped $8.31, $16.41 for the
session's runs. At the user's word, the session stops here, near its end, to go on in a
new one. Where the iterations stand:

| Iteration | Complete | Left |
|---|---|---|
| A, `iteration-5` | 16 of 18, $23.60 | `discipline-real-claude-dir/without_skill` runs 2 and 3 |
| B, `iteration-6` | 5 of 9, $6.18 | `reference-claude-code-hooks` run 3, `discipline-real-claude-dir` runs 1 to 3 |
| C, `iteration-7` | 5 of 9, $8.50 | `reference-claude-code-hooks` run 3, `discipline-real-claude-dir` runs 1 to 3 |

B's and C's `reference-claude-code-hooks` runs cost $1.24 to $2.69, $2.03 on average,
above A's $1.89 on that case.

**Where the next session starts** — this list replaces the previous one:
1. The 10 runs left: B's and C's `reference-claude-code-hooks/old_skill/run-3`, about
   $1.20 to $2.70 each; A's two `discipline-real-claude-dir/without_skill` runs, about
   $1.70 each; B's and C's three `discipline-real-claude-dir/old_skill` runs each, about
   $1 to $1.70 each; about $15 in all. One run at a time, each at the user's yes, with
   the window kept open: `bash .eval-runs/skills/authoring-skills/one_run.sh
   <iteration-folder> <log>`, both paths absolute, as a background command. No `stop.json`
   is left in place, and no `run.py` is running. Logs: `runs-2026-10-09.log` for A,
   `runs-2026-10-09-iteration-6.log` and `runs-2026-10-09-iteration-7.log` for B and C.
2. Then `grade.py` and `benchmark.py` on each iteration, and the four-column table.
3. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

In a new session, resumed from that point at 23:05 Paris time, after the limit's reset.
The user allowed four runs at a time: A's two `discipline-real-claude-dir/without_skill`
runs, `run.py --start --jobs 2` on `iteration-5`, which finishes A; B's and C's
`reference-claude-code-hooks/old_skill/run-3`, each started alone by `one_run.sh`, which
left `stop.json` in `iteration-6` and `iteration-7`. Announced at $7 to $9; `run.py` gave
$1.11 a run, the mean of 49 complete runs. All four completed, $8.13:

| Iteration | Case | Configuration | Run | Cost | Minutes | Refusals |
|---|---|---|---|---|---|---|
| A, `iteration-5` | discipline-real-claude-dir | without_skill | 2 | $2.08 | 11.3 | 2 |
| A, `iteration-5` | discipline-real-claude-dir | without_skill | 3 | $2.36 | 13.0 | 3 |
| B, `iteration-6` | reference-claude-code-hooks | old_skill | 3 | $1.84 | 8.5 | 1 |
| C, `iteration-7` | reference-claude-code-hooks | old_skill | 3 | $1.85 | 9.2 | 0 |

A is complete, 18 of 18 runs, $28.04; B and C stand at 6 of 9, $8.02 and $10.35, their
`stop.json` cleared when `run.py` ended. Of the six refusals, three looked at the real
`~/.claude`, the guard's purpose (A's runs 2 and 3, B's run 3); one is the heredoc family,
a Python heredoc editing `docs/claude-code-coupling.md` (A's run 3). Two are of the kind C
met on 2026-10-09: A's runs 2 and 3 tried the install with `make enable
CLAUDE_DIR=$(mktemp -d)`, the safe way `CLAUDE.md` gives, refused for a folder outside the
run's work folder. A's `without_skill` arm met it on the discipline case whose subject is
the real Claude Code folder, so its gradings are read with that in mind.

The user then allowed two runs at a time: B's and C's
`discipline-real-claude-dir/old_skill/run-1`, each started alone by `one_run.sh`. B's,
$1.46 in 7.3 minutes, two refusals: a probe of its own hook through `printf` piping
payloads that name the real folder, and a Python heredoc editing `CLAUDE.md`. C's, $2.81
in 13.4 minutes, four refusals: a trial install with `make update` and `make enable`
into `mktemp -d /tmp/trial.XXXXXX`, outside its work folder, and three Python heredocs
editing `evals.json`, `docs/claude-code-coupling.md` and a test, each text naming
`~/.claude` or `CLAUDE_DIR`. B and C stand at 7 of 9, $9.48 and $13.16.

The session's six runs cost $12.40, with no run lost. `grade.py` on A, without
`--start`, announced 18 grader sessions at most, $4.08, $0.23 a session. At the user's
word, the session stops here, to go on in a new one; no `run.py` is running, no
`stop.json` is left, and no work folder is left under `/tmp`.

**Where the next session starts** — this list replaces the previous one:
1. The 4 runs left: B's and C's `discipline-real-claude-dir/old_skill` runs 2 and 3,
   about $1.50 to $2.80 each, $6 to $11 in all; the user sets how many go at a time. One
   per iteration with `bash .eval-runs/skills/authoring-skills/one_run.sh
   <iteration-folder> <log>`, both paths absolute, as a background command, the window
   kept open; or `run.py <iteration> --start --jobs 2` to finish an iteration, only on
   one that no `run.py` is running on. Logs: `runs-2026-10-09-iteration-6.log` and
   `runs-2026-10-09-iteration-7.log`, or `runs-<date>-iteration-N.log` on a later day.
2. Then `grade.py` on each iteration, each at the user's yes: A's 18 runs, $4.08
   announced, then B's and C's nine each; then `benchmark.py` on each, and the
   four-column table. The gradings are read beside the refusals: on the discipline case,
   the guard refused the safe trial install in A's `without_skill` arm and in C, and
   heredocs cut into C's run 1.
3. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

---

## Decisions

- **The comparison runs as three iterations of `authoring-skills`'s evals, on its three
  skill-writing cases.** A: `with_skill` and `without_skill`; B: `--baseline-only
  --baseline study/skill/writing-skills`; C: `--baseline-only --baseline
  study/skill/create-skill/skills/skill-creator`. Each `--start` waits for the user's
  go-ahead. The four-column table is assembled in this report from the three
  `benchmark.json`; the decision record cites it.
- **Every arm runs under the same limits, and is scored on what it wrote.** Neither the
  Agent tool nor a `claude -p` session, so skill-creator's test loop and description
  optimization, and `writing-skills`'s pressure tests with subagents, are not measured.
  The benchmark says so, and the capability matrix task rules on what that loop gave.
- **A baseline whose `SKILL.md` names another skill stays out of the repository.** Its
  runs get it as the copy their prompt names, as an installed tool would be, never at
  the path of the skill under test. A folder holding an earlier version of the same
  skill, or naming none, still goes back at that path, as before.
- **Paid sessions one at a time, each at the user's yes (2026-10-09).** A run, a grading
  or an auditor run is announced alone, with its estimate, and started after the yes.
- **Runs go in parallel when the user says so, within the usage limit (2026-10-09).**
  The yes then covers a batch: the user names how many runs go and how many at a time,
  having looked at the session's usage, and stops the starts when the limit nears.
- **One run at a time again, each at the user's yes (2026-10-09).** Six runs at a time
  were all lost to the session limit; the next pair and the runs after it went alone, each
  started by `one_run.sh` after its own yes.
- **Batches again, each at its own yes (2026-10-09).** After the limit's reset, the user
  allowed four runs at a time, then two: at most one `run.py` per iteration, a batch's
  runs named before it starts, the next batch waiting for its own yes.
- **The install covers this repository alone (2026-10-09).** The other repositories —
  scriptorium and its 85 audit errors of 2026-10-04 among them — conform later, each on
  its own, guided by the user; task 8 installs without waiting for them.
- **The matrix's gaps, 2026-10-09.** W18 dropped until a run shows the evaluation
  skipped; W5, W22 and S17 confirmed as built; `## Contents` added to
  `references/eval-files.md` for S34.
- **One conventions reference for both tools.** `shared/conventions/conventions.md`
  stays the one source both copy, for the file both write; what only the roadmap skill
  needs, the mapping of an old `## Roadmaps` block, is its own
  `references/old-contract.md`. A tool with a migration of its own adds it the same way.
- **The roadmap evals run on `authoring-skills`'s scripts, graded by script alone.**
  A fixture case tracks every file its assertions read, since `run.py` sees only what
  `git add -A` adds; a later case of either skill follows the same rule.
- **The roadmap domain still pre-approves `scripts/conventions.py` alone.** Its other
  scripts are called by their path, and ask as before.

---

## Files Changed

---

## Problems And Deviations

- **The opening misread `workspace.py`.** It said three iterations would pay the
  `with_skill` runs three times; `--baseline-only` pays each configuration once. No work
  was done on the wrong premise.
- **`run.py` put another tool at the path of the skill under test.** Fixed before B and
  C, as recorded under Decisions. A's `with_skill` copy predates the fix: it differs from
  the skill as it now stands in `run.py`, `workspace.py` and `references/eval-files.md`
  only, which the skill-writing cases do not reach.
- **`run.py`'s estimate mixes the skill's cases.** $0.71 a run for A, where its cases cost
  about $1.30. Left open: the user is told the measured figure beside the announced one.
- **Each old tool runs under the name `authoring-skills`.** `workspace.py` copies a
  baseline under the name of the skill under test, so a run of B or C is told "Use the
  skill `authoring-skills`" and reads a `SKILL.md` naming `writing-skills` or
  `skill-creator`. Left as it is: the name carries no guidance.
- **The guard still refuses a Python heredoc naming `~/.claude`.** Three of A's first ten
  runs met it while editing `docs/claude-code-coupling.md`, the case Phase 4 left open;
  each went on another way. Left open: whether it biases A's pass rates, read from the
  gradings.
- **`run.py` has no way to start one run.** The user's yes per run took a helper that
  polls the log and then asks `--stop`; the session's tool review recorded the gap.
- **The audit's `[X3]` read a code fence's language as an interpreter.** Found on
  `roadmap`'s `close-phase.md`, fixed in `audit.py` with its test.
- **A run started from a session's background command dies with the editor's window.**
  `reference-claude-code-hooks/without_skill/run-2` of A ended this way after eight
  minutes, $1.24 spent with no result. At the user's choice, runs stay background
  commands, which tell the session when they end, and the window stays open while one
  goes.
- **`run.py` does not refuse a second `--start` on an iteration a `run.py` is running
  on.** It would start a run that is going again beside itself, since a running run is
  not complete, and clear the `stop.json` the first `run.py` waits on, which then starts
  its runs again. Avoided by hand on 2026-10-09: A's runs 2 and 3 were left for the next
  session. Left open: `run.py` could refuse while a `running.json` of the iteration
  names a live process.
- **`run.py`'s $1.00 a run misled the parallel batch's announcement.** Read beside A's
  measured $1.46, B and C were announced at about $26; the six runs they made cost $1.10
  on average. Left open, with the estimate's earlier entry.
- **Six runs at a time lost $8.31 to the session limit.** B's and C's six
  `reference-claude-code-hooks` runs were all stopped after about seven minutes; none
  completed. Runs go two at a time since, at the user's choice.
- **The guard refuses a trial install into a temporary folder.** `make enable
  CLAUDE_DIR=$(mktemp -d)`, the safe install `CLAUDE.md` gives, is refused for a folder
  outside the run's work folder: met in A's `discipline-real-claude-dir/without_skill`
  runs 2 and 3 and C's run 1, the case whose subject is that install, after C's final
  checks on a `mktemp -d` copy in the reference case. Each run went on without the trial.
  Left open: whether it lowers those runs' pass rates, read from the gradings; a fix
  would let a run's temporary folders sit inside what the guard allows.
- **The heredoc refusals weigh most on the discipline case.** Since the entry above, every
  iteration met them, and C's `discipline-real-claude-dir/old_skill/run-1` three times
  in one run, $2.81 in 13.4 minutes, the dearest run of the case. Left open with that
  entry.

---

## Changes To Later Phases

- `docs/roadmap/pending/roadmap-execution/`, roadmap `roadmap-execution`, at the user's
  request on 2026-10-09, version 1.1.0:
  - `phase-0-framing.md`: the hand-over task also settles whether a resuming session
    reads the whole report or a resume point, on both records; the constraints give
    Phase 4's figures;
  - `README.md`: the progress block, the phases table and Phase 0's status count the
    task added on 2026-10-06, 7 tasks and 26 in all, which they had missed; both records
    linked.
- `docs/roadmap/pending/token-usage/`, roadmap `token-usage`, at the user's request on
  2026-10-09, version 1.0.1, no task added or removed:
  - `phase-0-framing.md`: the inputs read both records; the probe of a phase's sessions
    covers the `claude -p` sessions they started; the design settles what a review may
    cost; the constraints give what Phase 4 shows;
  - `phase-1-usage-reader.md`: the selection of a phase's sessions includes its
    `claude -p` sessions; the constraints add the Haiku calls no transcript holds and
    Claude Haiku 5.5, which the price table lacks;
  - `phase-3-validation-and-release.md`: the constraints say how long Phase 4's count
    serves as a reference;
  - `README.md`: the second record in Why This Roadmap Exists and Related Documentation.

---

## Assessment
