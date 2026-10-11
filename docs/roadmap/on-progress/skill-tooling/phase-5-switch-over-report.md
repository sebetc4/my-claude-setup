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

### 2026-10-10

In a new session, resumed from that point: no `run.py` running, no `stop.json`, no work
folder under `/tmp`. `run.py` announced $2.43 for each iteration's two runs, $1.22 a run,
the mean of 55 complete runs; the case's runs so far cost $1.46 to $2.81, so $6 to $11
for the four. The user chose two at a time: B's and C's
`discipline-real-claude-dir/old_skill/run-2`, each started alone by `one_run.sh` as a
background command, logs `runs-2026-10-10-iteration-6.log` and
`runs-2026-10-10-iteration-7.log`; run 3 of each waits for the next yes.

C's run 2: $2.03 in 9.3 minutes, two refusals — a probe of its own hook in a
`mktemp -d` folder whose payloads name `.claude`, and a Python heredoc editing
`docs/claude-code-coupling.md`, both the families met before. C stands at 8 of 9.

B's run 2: $2.27 in 10.9 minutes, three refusals — a probe of the guard on a decoy
`Makefile` in a `mktemp -d` folder, run with `CLAUDE_DIR=$HOME/.claude`, and two Python
heredocs, one editing `CLAUDE.md`, one the guard's hook and its test. B stands at 8 of 9.
The pair cost $4.30. No `stop.json` is left and no work folder under `/tmp`; the last
two runs, B's and C's run 3, wait for the user's yes. At the user's word, the session
stops here, to go on in a new one. Where the iterations stand:

| Iteration | Complete | Left |
|---|---|---|
| A, `iteration-5` | 18 of 18, $28.04 | — |
| B, `iteration-6` | 8 of 9, $11.75 | `discipline-real-claude-dir/old_skill/run-3` |
| C, `iteration-7` | 8 of 9, $15.19 | `discipline-real-claude-dir/old_skill/run-3` |

**Where the next session starts** — this list replaces the previous one:
1. The 2 runs left: B's and C's `discipline-real-claude-dir/old_skill/run-3`, about
   $2 to $2.80 each, the case's last four runs having cost $1.46 to $2.81. Two at a time,
   at the user's yes, each with `bash .eval-runs/skills/authoring-skills/one_run.sh
   <iteration-folder> <log>`, both paths absolute, as a background command, the window
   kept open; or `run.py <iteration> --start --jobs 1`, which finishes the iteration. The
   log must exist before `one_run.sh` starts, or it asks the stop before any run starts:
   `runs-<date>-iteration-6.log` and `runs-<date>-iteration-7.log`, created with `touch`.
2. Then `grade.py` on each iteration, each at the user's yes: A's 18 runs, $4.08
   announced, then B's and C's nine each; then `benchmark.py` on each, and the
   four-column table. The gradings are read beside the refusals: on the discipline case,
   every iteration met the heredoc refusals, and the guard refused the safe trial install
   or a probe in a `mktemp -d` folder in A's `without_skill` arm, in B and in C.
3. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

In a new session, resumed from that point: no `run.py` running, no `stop.json`, no work
folder under `/tmp`. The user had the last two runs go in parallel: B's and C's
`discipline-real-claude-dir/old_skill/run-3`, each started at 08:16 UTC by `run.py
<iteration> --start --jobs 1` as a background command, since one run left finishes the
iteration; logs `runs-2026-10-10-iteration-6.log` and `runs-2026-10-10-iteration-7.log`.
`run.py` announced $1.25 a run, the mean of 57 complete runs; the case cost $1.46 to
$2.81 so far. Both completed, $4.25:

| Iteration | Case | Configuration | Run | Cost | Minutes | Refusals |
|---|---|---|---|---|---|---|
| B, `iteration-6` | discipline-real-claude-dir | old_skill | 3 | $1.82 | 9.0 | 2 |
| C, `iteration-7` | discipline-real-claude-dir | old_skill | 3 | $2.43 | 11.5 | 4 |

B's two refusals are Python heredocs editing its guard's test, one going on to a trial
install with `make enable CLAUDE_DIR=$(mktemp -d)`. C's four: a `grep` whose pattern
names `~/.claude`, a probe of its guard written to `/tmp` and run in a `mktemp -d` folder,
a Python heredoc editing the guard's hook, and a live test of the guard with `make
update` on an unset `CLAUDE_DIR`. All families met before.

The comparison's 36 runs are complete. No `run.py` running, no `stop.json`, no work
folder under `/tmp`:

| Iteration | Complete | Cost |
|---|---|---|
| A, `iteration-5` | 18 of 18 | $28.04 |
| B, `iteration-6` | 9 of 9 | $13.57 |
| C, `iteration-7` | 9 of 9 | $17.62 |

`grade.py` without `--start` announces 18 grader sessions at most for A, $4.08, and 9 for
each of B and C, $2.04 each, $0.23 a session, the mean of 28 complete gradings.

**Where the next session starts** — this list replaces the previous one:
1. `grade.py <iteration> --start` on each iteration, each at the user's yes: A, $4.08
   announced, then B and C, $2.04 each; then `benchmark.py` on each, and the four-column
   table. The gradings are read beside the refusals: on the discipline case, every
   iteration met the heredoc refusals, and the guard refused the safe trial install or a
   probe in a `mktemp -d` folder in A's `without_skill` arm, in B and in C.
2. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

At the user's yes, `grade.py --start` on A, as a background command, its output in
`grades-2026-10-10-iteration-5.log`; it runs four grader sessions at a time, its default.
All 18 graded, $4.52 where $4.08 was announced, $0.16 to $0.32 a session:

| Case | with_skill | without_skill |
|---|---|---|
| task-release-domain | 4/7, 6/7, 6/7 — 16/21 | 3/7, 3/7, 3/7 — 9/21 |
| reference-claude-code-hooks | 6/6, 4/6, 6/6 — 16/18 | 5/6, 4/6, 5/6 — 14/18 |
| discipline-real-claude-dir | 5/6, 6/6, 6/6 — 17/18 | 3/6, 2/6, 2/6 — 7/18 |
| All | 49/57, 86% | 30/57, 53% |

The `with_skill` arm's eight failures, each assertion read with its evidence before the
skill:
- `task-release-domain`: the body defines the semantic versioning levels, runs 1 and 3,
  though tied to the domain's changelog, which the grader calls borderline; steps without
  a check command, and the `VERSION`-changelog match left to `make check`, runs 1 and 2;
  a description whose first clause chains the steps, run 1, borderline too by the
  grader's word, since the writing guide allows a clause naming operations.
- `reference-claude-code-hooks` run 2: facts on Stop's `stop_hook_active` and
  SessionStart's sources with no source, which the run admits it never read; a
  description missing "a hook that does not fire" and "exit code 2".
- `discipline-real-claude-dir` run 1: the mechanical guard considered after the skill
  and its scenarios were written, not before.

Each assertion holds as written, and each evidence quotes the run's own files; whether
the skill teaches what each failure misses is read once the four columns stand. The
`without_skill` arm fails what only the method gives: the test proposed before writing,
the pressure scenarios, the audit, and on the discipline case the prohibition with its
condition.

The session's paid steps cost $8.77: the two runs, $4.25, and A's gradings, $4.52. At the
user's word, the session stops here, to go on in a new one; no `run.py` or `grade.py` is
running, no `stop.json` is left, and no work folder under `/tmp`.

**Where the next session starts** — this list replaces the previous one:
1. `grade.py <iteration> --start` on B, `iteration-6`, then on C, `iteration-7`, each at
   the user's yes: 9 grader sessions each, $2.04 announced, about $2.30 at A's measured
   $0.25 a session; as a background command, its output in
   `grades-<date>-iteration-N.log`. The failures read with their evidence, as for A.
2. `benchmark.py` on each of the three iterations, then the four-column table — no
   skill, `writing-skills`, skill-creator, `authoring-skills` — assembled here from the
   three `benchmark.json`. Then, for each failure of the `authoring-skills` arm, whether
   the skill teaches what it misses. The gradings are read beside the refusals: on the
   discipline case, every iteration met the heredoc refusals, and the guard refused the
   safe trial install or a probe in a `mktemp -d` folder in A's `without_skill` arm, in
   B and in C.
3. Steps 3 to 6 of the first list, unchanged: the two trigger measures, the nine
   `skill-auditor` runs, the install, tasks 10 to 12.

In a new session, resumed from that point: no `run.py` or `grade.py` running, no
`stop.json`, no work folder under `/tmp`. `grade.py` announced 9 grader sessions for each
of B and C, $2.13 each, $0.24 a session, the mean of 46 complete gradings. The user had
both go in parallel: `grade.py <iteration> --start` on `iteration-6` and `iteration-7` as
two background commands, four grader sessions at a time each, their output in
`grades-2026-10-10-iteration-6.log` and `grades-2026-10-10-iteration-7.log`.

All 18 graded: B $2.36, C $2.26, $0.19 to $0.31 a session. `benchmark.py` then ran on
each of the three iterations. The four columns, each pass rate the mean of the runs' rates
as `benchmark.py` gives it, so A's `with_skill` reads 87% where the pooled count gave 86%:

| Case | No skill | `writing-skills` | skill-creator | `authoring-skills` |
|---|---|---|---|---|
| task-release-domain | 43% | 52% | 43% | 76% |
| reference-claude-code-hooks | 78% | 67% | 72% | 89% |
| discipline-real-claude-dir | 39% | 61% | 33% | 94% |
| All | 53% ± 20% | 60% ± 9% | 49% ± 20% | 87% ± 16% |
| Cost a run | $1.73 | $1.51 | $1.96 | $1.39 |
| Duration a run | 545 s | 446 s | 536 s | 433 s |

Per assertion, three runs each:

| Case | # | Assertion, short | No skill | `writing-skills` | skill-creator | `authoring-skills` |
|---|---|---|---|---|---|---|
| task-release-domain | 1 | reads how releases are done | 3 | 3 | 3 | 3 |
| | 2 | says where the skill belongs | 3 | 3 | 3 | 3 |
| | 3 | description: one clause, then when | 0 | 1 | 0 | 2 |
| | 4 | steps in order, each with its check | 3 | 2 | 2 | 1 |
| | 5 | no git or semver explained | 0 | 1 | 0 | 1 |
| | 6 | proposes a test, run first without the skill | 0 | 1 | 1 | 3 |
| | 7 | audit clean, no emphatic wording | 0 | 0 | 0 | 3 |
| reference-claude-code-hooks | 1 | each fact sourced | 2 | 2 | 2 | 2 |
| | 2 | covers what is specific here | 3 | 3 | 3 | 3 |
| | 3 | under 5,000 tokens, references cited | 3 | 3 | 3 | 3 |
| | 4 | description: what, then when | 3 | 1 | 2 | 2 |
| | 5 | proposes a behavioral check | 3 | 3 | 3 | 3 |
| | 6 | audit clean | 0 | 0 | 0 | 3 |
| discipline-real-claude-dir | 1 | considers a mechanical guard first | 3 | 3 | 3 | 2 |
| | 2 | pressure scenarios before the rules | 0 | 0 | 0 | 3 |
| | 3 | prohibition with its condition | 0 | 3 | 0 | 3 |
| | 4 | symptoms only from a scenario | 1 | 2 | 0 | 3 |
| | 5 | no capitals or CRITICAL | 3 | 3 | 3 | 3 |
| | 6 | audit clean | 0 | 0 | 0 | 3 |

The three audit assertions fail in every run of the three other arms, for one cause the
evidence gives each time: `audit.py` lives in `authoring-skills`, which their copy of the
repository lacks, so `make check` fails on the missing file and the runs fell back on
skill-creator's `quick_validate.py`, a stub or a hand check. Without those three
assertions, pooled counts: no skill 30/48, 63%; `writing-skills` 34/48, 71%;
skill-creator 28/48, 58%; `authoring-skills` 40/48, 83%. By case, `authoring-skills`
still leads on task-release-domain, 72% against 50% to 61%, and on
discipline-real-claude-dir, 93% against 40% to 73%; on reference-claude-code-hooks it
reads 87%, as skill-creator, above `writing-skills`'s 80%, under no skill's 93%, one
assertion apart over three runs.

What the evidence says of the old tools under the comparison's limits: `writing-skills`
holds the prohibition with its condition in all three discipline runs, where skill-creator
writes a total ban in all three; neither writes pressure scenarios before the rules, and
B's run 3 says it could not run agents without the skill, the loop the Decisions put out
of the measure. Semantic versioning is explained in the body by every arm, all but one run
of `writing-skills` and one of `authoring-skills`.

The task's expectation holds in both views: `authoring-skills` matches or beats each old
tool on every case — on reference-claude-code-hooks without the audit, 87% as
skill-creator — and beats the no-skill arm overall, 87% against 53%, 83% against 63%.
Task 1 ticked.

Then, at the user's word, each of the `authoring-skills` arm's eight failures read
against the skill, from the copy A ran, which differs from the skill now only in
`conventions.md`, `eval-files.md` and three scripts the writing does not reach. Every
failing run read, before writing, the file that covers its failure:

| Failure | Runs | Where the skill teaches it | Other arms |
|---|---|---|---|
| Description's first clause chains the steps, "by setting `VERSION`, writing its entry, committing both and tagging" | release 1 | writing guide, The Description: one clause naming the operations, no sequence of steps | none 3, B 2, C 3 fail |
| A step without its check; `VERSION` against the changelog left to `make check` | release 1, 2 | the task template's `Check:` slot on every step; Degrees Of Freedom: "a step that can fail gets its check" | none 0, B 1, C 1 fail |
| The body defines major, minor and patch | release 1, 3 | What Goes In names semantic versioning, and says to cut a line "even when it restates a convention through an example of this repository" | none 3, B 2, C 3 fail |
| Facts on Stop and SessionStart with no source, the section never read | hooks 2 | create-and-edit step 6, and What Goes In: each fact its source | 1 each fails |
| Description without "a hook that does not fire" or "exit code 2" | hooks 2 | The Description: symptoms and error messages in the users' words; the request named none | none 0, B 2, C 1 fail |
| The guard weighed after the skill and its scenarios were written | discipline 1 | create-and-edit step 3, before step 7; discipline.md, Before The Rule | none fail |

No failure points at something the skill does not teach: each is a rule the run read and
did not apply. Two weigh more than one run:
- semantic versioning, two runs of three, though the line names that very case; every
  other arm fails it as often or more, so the skill does not cure what the model does
  unasked;
- the check on each step, two runs of three, where the no-skill arm passes all three. The
  assertion reads two ways, a check on each step or the three checks it names, and the
  grader called it weak: a body naming the three in prose passes, as the no-skill runs
  did. "A step that can fail" also lets a run judge a step safe and leave its check out.
Three assertions put `authoring-skills` under the no-skill arm: the checks on each step by
two runs, the hooks description and the guard first by one run each.

The user left the skill unchanged, the failures to real use through the tool reviews, as
recorded under Decisions. Since a review sees friction — a correction, an error, a missed
trigger — more than a fault that slips silently into the skill a session writes, task 11's
proof now asks the decision record for the points to watch in real use, each with the
condition to revisit it: the body explaining a convention the model knows, a step without
its check, the guard weighed after the skill. Assertion 4's two readings are recorded
under Problems And Deviations, to split at the next run of the evals.

The user then raised two points. The skills `authoring-skills` writes must fit the review
domain's skill and hook, for the real-use reviews to reach them. And the reviews under
`reviews/`, 70 from 2026-09-27, were made on the installed versions, not the repository's:
`tools/reviews.py` prints "not seen since 2.0.1" on every roadmap finding because the
repository's `VERSION` is above the last version reviewed, while `make list` shows roadmap
2.0.0 installed, so no session ran 2.0.1.

On the first point the user chose points to watch per tool: `tools.json` gives, for each
tool, what a review must check, and `measure.py` adds them to what the review must
explain, so that the review of a session that used `authoring-skills` judges the skill it
wrote on them. Not chosen: a test requiring every tool of `domains/` to be listed in
`tools.json` or set aside with its reason. The second point waits for the user, who asked
for the proposal in more detail.

Explained, the user held it necessary, so that the reviews do not mislead. Two tasks added
to Install And Release, after task 9: `tools/reviews.py` telling a version no session
has used from one whose reviews no longer raise a finding, and the points to watch per
tool. The first done test-first: in `tests/test_reviews.py`, the test of "not seen since"
became one expecting `1.2.0 not reviewed yet`, and a second expects `absent from 2 reviews
of 1.2.0` from two complete reviews of 1.2.0 and a skipped one; both watched failing on
"not seen since 1.2.0". `finding_groups` now counts the complete reviews of each domain's
version, and `left_behind` words the result. `make check` passes. `make reviews` now
prints `2.0.1 not reviewed yet` on each roadmap finding where it printed "not seen since
2.0.1". The review period on the repository's versions starts with task 8's install.

Then the points to watch, test-first. `tools.json` keeps its three lists, which the hook
and the catalog read unchanged, and gains `watch`, the points by tool id; `transcript.py`'s
`load_config` reads the installed file for both the catalog and `measure.py`, whose
`owed` prints `- point to watch for <tool>: <point>; a finding when the slice shows it`
after what the tool brought. Two tests in `test_measure.py`: a slice that used the
roadmap skill finds its two points and not those of the auditor it did not start, red
first on their absence; a slice whose tools carry no point finds none. In
`test_tools_json.py`, `watch` is a known key, `unlisted_watches` refuses a point on a tool
the lists do not name, tried on a fixture, and each point is a sentence; these hold the
file and were green before it changed. `authoring-skills`'s three points written in
`tools.json`. Review 0.2.0; `CLAUDE.md`'s layout line names `watch`. `make check` passes.
The points reach the reviews once `make update D=review` installs 0.2.0, with task 8.

The session's paid steps cost $4.62, B's and C's gradings; the rest started no session.
The phase stands at 6 of 14 tasks: 1, 3, 5, 7 and the two added, 10 and 11. Tasks after
9 moved down by two, so the decision record, task 11 earlier in this entry, is now task
13. At the user's word, the session stops here, to go on in a new one; no `run.py` or
`grade.py` is running, no `stop.json` is left, and no work folder under `/tmp`.

**Where the next session starts** — this list replaces the previous one:
1. Task 2, the two trigger measures, each at the user's yes: `triggers.py` on
   `authoring-skills` with the current description, then with `--description
   .eval-runs/skills/authoring-skills/description-b3fa90e.txt`; 72 sessions on Opus 5.5 at
   `xhigh`, $3.67 announced each. Then the tuning, if a query that should trigger does
   not.
2. Tasks 4 and 6: nine `skill-auditor` runs — `roadmap`, `tool-review`,
   `authoring-skills`, three each —, a general-purpose agent on Sonnet told to act as the
   agent, given the skill's folder, the writing guide's path and `audit.py`'s output; each
   at the user's yes.
3. Task 8: `make enable D=skill-tooling` on the real `~/.claude` at the user's go-ahead,
   `make update D=review` for 0.2.0 and `make update D=roadmap` for 2.0.1, then the
   registration of `audit_skill.py` removed from `.claude/settings.json`; then task 9's
   probe. The review period on the repository's versions starts there.
4. Tasks 12 to 14. `CLAUDE.md`: the gotchas of the first list, and the layout's
   `fixtures.py` and `grade.py` under a skill's `evals/`. The decision record: the
   benchmark in its two views, the trigger rates, the matrix gaps, and the three points to
   watch with the condition to revisit each. Assertion 4 of `task-release-domain` is split
   at the next run of `authoring-skills`'s evals.

In a new session, resumed from that point: no `run.py`, `grade.py` or `triggers.py`
running. `triggers.py` without `--start` announced, for each description, 72 sessions on
Opus 5.5 at `xhigh`, four queries at a time, $0.50 the ceiling of a session, $3.67 from
the defaults measured on 2026-10-06 and 2026-10-08, the skill having no trigger session
of its own yet. At the user's yes, the measure with the current description started as a
background command, its output in `triggers-2026-10-10-current.log`.

It ran from 13:40 to 13:45 UTC on Claude Code 2.1.292, every session counted, written to
`triggers/2026-10-10T134515Z.json`: the 12 queries that should trigger did so in 3 of 3
sessions, each at its first call through the Skill tool; the 12 near misses triggered in
none. No query fails, so the description needs no tuning on these queries. The cost was
$8.35 where $3.67 was announced:
- the queries that should trigger cost $1.19, $0.080 a first session and $0.009 a repeat,
  as the defaults said;
- the near misses cost $7.16, $0.238 a first session and $0.179 a repeat, where the
  defaults said $0.120 and $0.040. Each session gets copies of the user's other personal
  skills, and four queries load one of them: the hook query `update-config`, whose three
  sessions passed the $0.50 ceiling, $0.71 to $0.78, stopped as `error_max_budget_usd`
  after the Skill call and one Bash; the system prompt query and the model comparison
  `claude-api`, $0.41 to $0.49 and $0.36 to $0.42 a session; the roadmap update
  `roadmap`, $0.07 to $0.11. Those three queries alone cost $4.69.

`triggers.py` now estimates from this skill's own sessions: $8.35 for the measure of the
description of `b3fa90e`. Started at the user's yes as a background command, its output
in `triggers-2026-10-10-b3fa90e.log`; the user restated the rule, each paid step at its
own confirmation.

It ran from about 13:48 to 13:53 UTC, written to `triggers/2026-10-10T135348Z.json`, $8.37:
the same result as the current description, query by query — the 12 that should trigger
in 3 of 3 sessions, each at its first call, the 12 near misses in none; the hook query's
sessions stopped again on the ceiling, four sessions in all. So "evaluates" changes
nothing on these queries: the five on evaluating a skill — evals against no skill, a
benchmark against the previous commit, a discipline check, a blind comparison, a trigger
rate — triggered the skill under the description that does not name evaluation. Every
query that should trigger names a skill, and this skill is the only one given that
writes skills, so the set cannot tell the two descriptions apart; the current one stays,
since it states what the skill does. Task 2 ticked, with no tuning: no query failed.
The two measures cost $16.72.

Then tasks 4 and 6, their part that starts no session: `audit.py` passes on `roadmap`,
`tool-review` and `authoring-skills`, no error and no warning, and `make check` passes.
The nine `skill-auditor` runs follow, each at the user's confirmation, about $0.45 each,
the mean of Phase 3's 45 runs: a general-purpose agent on Sonnet told to act as the
agent, the domain not being installed.

The session's paid steps cost $16.72, the two trigger measures. At the user's word, the
session stops here, before the first `skill-auditor` run, to go on in a new one; no
`run.py`, `grade.py` or `triggers.py` is running. The phase stands at 7 of 14 tasks.

**Where the next session starts** — this list replaces the previous one:
1. Tasks 4 and 6: nine `skill-auditor` runs — `roadmap`, `tool-review`,
   `authoring-skills`, three each —, each at the user's confirmation, about $0.45 a run.
   A general-purpose agent on Sonnet, told to act as the agent of
   `domains/skill-tooling/agents/skill-auditor.md`, given the skill's folder, the writing
   guide's path, `domains/skill-tooling/skills/authoring-skills/references/writing-guide.md`,
   and `audit.py`'s output, clean on all three on 2026-10-10. The runs on `roadmap` and
   `authoring-skills` also show whether any of task 6's five conventions problems is
   left. Every problem fixed or ruled by the user.
2. Task 8: `make enable D=skill-tooling` on the real `~/.claude` at the user's go-ahead,
   `make update D=review` for 0.2.0 and `make update D=roadmap` for 2.0.1, then the
   registration of `audit_skill.py` removed from `.claude/settings.json`; then task 9's
   probe. The review period on the repository's versions starts there.
3. Tasks 12 to 14. `CLAUDE.md`: the gotchas of the first list, and the layout's
   `fixtures.py` and `grade.py` under a skill's `evals/`. The decision record: the
   benchmark in its two views, the trigger rates of both descriptions and why the set
   cannot tell them apart, the matrix gaps, and the three points to watch with the
   condition to revisit each. Assertion 4 of `task-release-domain` is split at the next
   run of `authoring-skills`'s evals.

In a new session, resumed from that point: no `run.py`, `grade.py` or `triggers.py`
running, the tree clean, `audit.py` clean on the three skills. Task 6's edits stand since
`bada0e8`, roadmap 2.0.1, so the nine `skill-auditor` runs are what tasks 4 and 6 have
left. Announced at about $0.45 a run, $4 for the nine; the user allowed the nine in one
yes, three at a time, one skill after the other: a general-purpose agent on Sonnet told to
act as the agent, read-only, denied the Skill tool and the installed copy under
`~/.claude`.

The nine ran, $3.74 counted from their transcripts by `shared/usage/usage.py`, output
undercounted as in any subagent: `roadmap` $0.66, $0.53, $0.37; `tool-review` $0.23,
$0.24, $0.24; `authoring-skills` $0.51, $0.40, $0.57. All nine answered `VERDICT: FAIL`.
Their problems, merged across runs, each read in the files, with the number of runs that
raised it; a line number a run gave wrong is given here from the file:

| Skill | # | Problem | Runs |
|---|---|---|---|
| roadmap | R1 | description: the "Not for …" exclusion, with no false trigger recorded — the evals hold three output cases and no trigger query, and the sentence predates the domain | 3 |
| | R2 | form: bold sentences with no eval where plain wording failed — "A red command stops the ritual" (`SKILL.md:43`, `close-phase.md:22`), "Only one phase may be 🟡 at a time" (`SKILL.md:60`), "A phase closes with no unticked task" (`close-phase.md:36`), "Any phase not at 🟢 stops the closure" (`close-roadmap.md:20`), `report.md:61` and `:121` | 3 |
| | R3 | form: `close-phase.md:27`, "One nuance, and it is the reason …", a nuance clause around a real conditional | 3 |
| | R4 | form: persuasion and narration, `close-phase.md:75` "The report is the point of the whole ritual …" and `open-phase.md:24` "This is the continuity between sessions …" | 3 |
| | R5 | content: `close-phase.md`'s Traps tell past sessions and restate the Editing and Changelog invariants | 3 |
| | R6 | content: `old-contract.md:3`, "Before `.agent-conventions.toml`, this skill read …", the skill's history | 3 |
| | R7 | terminology: the skill's folder is "this skill's directory" (`SKILL.md:12`), "this skill's base directory" (`SKILL.md:71`, `close-phase.md:195`), `<skill-dir>`, "the skill's folder" (`conventions.md:5`) | 3 |
| | R8 | terminology: "Repository Contract" against "Repository Conventions"; `SKILL.md:12` defines the contract as the `[roadmap]` table of the conventions file, so the two names may name two things | 3 |
| | R9 | freedom: `close-phase.md:146`, Residue, a deletion under `versioning = "none"` left as prose, with no listing command and no check | 3 |
| | R10 | content: `create.md:91` "1 to 4 hours" and `:103` "700 lines", with no source | 2 |
| | R11–R14 | the description's breadth unmeasured; `create.md`'s Good and Bad examples; the glob paragraph of `close-phase.md:197`; "ritual", "closure" and "closing operation" | 1 each |
| tool-review | T1 | description: "Never on its own initiative, never to review code, and never in a subagent", with no eval | 3 |
| | T2 | content: `SKILL.md:14-16`, "the permission rules name that path, and `~` or `$HOME` would prompt" and "a project may refuse `python3`", with no source; `CHANGELOG.md` 0.1.1 holds the second's origin | 3 |
| | T3 | form and content: "What this skill never does" repeats the description and the procedure | 3 |
| | T4 | form: "Say nothing about the review", "No subagent, no other read, and no fix", prohibitions with no eval; `CHANGELOG.md` 0.1.2 records the behavior chosen, not a failure | 2 |
| | T5–T6 | "Your part", "the session's part" and "the draft"; "A session grading itself gives itself a good mark" with no run behind it | 1 each |
| authoring-skills | A1 | terminology: "scenarios" (`SKILL.md:22`, `create-and-edit.md`, `discipline.md`) against "cases" (`evaluate.md`, `eval-files.md`, the keys of `evals.json`) | 2 |
| | A2 | content: `evaluate.md:62`, "a small skill's run costs cents", with no source; Phase 4's report holds the measure | 2 |
| | A3–A7 | the 0.5 threshold of `evaluate.md:104`, defined in `eval-files.md:253`; `conventions.md:16`'s rule on `checks` read as a prohibition with no failure; `create-and-edit.md:116`'s copy of the previous version left as prose; `discipline.md:19` and `:61`, writing-skills' method without its source; `create-and-edit.md:87`, "playing them yourself", with no failure in the evals | 1 each |

`tool-review` has no `evals/`, so every judgment resting on an eval fires on it.

Task 6's five problems, over the six runs on `roadmap` and `authoring-skills`: none
raised in `shared/conventions/conventions.md` — the `residue` row, the old contract's
mapping, "directory", "the reader", and the `checks` claim, which one run of
`authoring-skills` read as a prohibition with no failure (A4), not as a fact with no
source. Two remain outside that file, in `roadmap`'s `SKILL.md`, where task 6 did not
reach: "directory" for the skill's folder (R7), and "the reader" at `SKILL.md:36`,
which no run raised.

The user asked what the problems meant, since both skills work and pass the static
audit; explained as departures from the writing guide, which both skills predate, none
breaking a skill, R9 the only one on a step hard to undo. The user then followed the
recommendation, as recorded under Decisions. Fixed:
- `roadmap` 2.0.2: R2, R3, R4, R5, R6, R7, R9, R10 and "the reader". The bold of R2
  goes from every rule sentence, two more found in `close-phase.md` and
  `close-roadmap.md`, the paragraph labels of `report.md` kept. R5 also removes
  `close-roadmap.md`'s Traps section, which only pointed to `close-phase.md`'s. R9's
  `find` commands tried on a scratch tree: nested `__pycache__/` folders, `*.log` at any
  depth, `data/*.tmp` from the root, and a file named `__pycache__` left out by `-type d`.
  R10 removes the phase-file length with its sentence, sub-phases existing nowhere else
  in the skill.
- `review` 0.2.1: T2, the sources named; T3, the section removed, what only it said moved
  into the procedure. `domains/review/tests/test_skill.py` read the removed line; its
  test now reads the rule where it moved, in step 4.
- `authoring-skills`: A1, "case" everywhere, "pressure scenario" defined in
  `discipline.md` as the case of a discipline skill, and `skill-auditor.md` following;
  A2, the measure cited as "(my-claude-setup, 2026-10-09)", Phase 4's.

`audit.py` passes on the three skills, no error and no warning, and `make check` passes.
Tasks 4 and 6 ticked: every problem is fixed or ruled, and none of task 6's five is left
in the shared reference or in `roadmap`. The phase stands at 9 of 14 tasks. The proof
`authoring-skills` asks for a wording change, the existing evals again, and for R9's
change of behavior, a case of its own, is not run: two of `roadmap`'s three cases
close under `versioning = "git"` and the third stops for want of `versioning`
(`evals/fixtures.py`), so none reaches the Residue step.

The session's paid steps cost $3.74, the nine `skill-auditor` runs. At the user's word,
the session stops here, to go on in a new one, with the questions below put at its
opening; the work is committed. No `run.py`, `grade.py` or `triggers.py` is running, and
no agent.

**Where the next session starts** — this list replaces the previous one.

Put these questions to the user at the opening, before any work, each answered before
the step it decides:
1. The proofs this session left for its edits: run `roadmap`'s three cases again on
   2.0.2, `with_skill` against `old_skill` at the commit before them, the proof
   `authoring-skills` gives for wording meant to keep behavior? The runs' cost was never
   recorded; `run.py` announces it without `--start`, from its mean of about $1.25 a
   run, so about $7.50 for one run per case and configuration, about $22 for three, the
   grading by `evals/grade.py` alone, $0. And write a fourth case, under
   `versioning = "none"`, for the Residue step that 2.0.2 changed, which no case reaches?
   It needs a fixture in `evals/fixtures.py` and its assertions, then its runs.
2. The go-ahead for task 8 on the real `~/.claude`: `make enable D=skill-tooling`,
   `make update D=review` for 0.2.1 and `make update D=roadmap` for 2.0.2, the trial
   first with `CLAUDE_DIR=$(mktemp -d)`. If the user wants question 1's proofs first,
   the install waits for them, since it puts 2.0.2 in every project.

Then, in order:
1. Question 1's proofs, if chosen, each paid step at its own yes.
2. Task 8: the trial install, then the three commands at the go-ahead, then the
   registration of `audit_skill.py` removed from `.claude/settings.json`, so that one
   edit of a skill file gives one audit report; then task 9's probe. The review period
   on the repository's versions starts there.
3. Tasks 12 to 14. `CLAUDE.md`: the gotchas of the first list, and the layout's
   `fixtures.py` and `grade.py` under a skill's `evals/`. The decision record: the
   benchmark in its two views, the trigger rates of both descriptions and why the set
   cannot tell them apart, the matrix gaps, the three points to watch with the condition
   to revisit each, and the rulings on `skill-auditor`'s problems. Assertion 4 of
   `task-release-domain` is split at the next run of `authoring-skills`'s evals.

### 2026-10-11

In a new session, resumed from that point: no `run.py`, `grade.py` or `triggers.py`
running, the tree clean at `fe99852`; `make list` shows review 0.1.2 and roadmap 2.0.0
installed, skill-tooling off. The user answered the opening's questions: `roadmap`'s
cases again on 2.0.2 against the commit before it, three runs each; a fourth case for the
Residue step; task 8 after those proofs.

The fourth case first, test-first. `close-phase-no-versioning`: phase 1 of the
search-index roadmap finished under `versioning = "none"` and `residue = ["__pycache__/",
"*.log", "data/*.tmp"]`, no `.git` in the fixture, the phase's report keeping its Files
Changed by hand and no Start Commit. Its residue sits at several depths:
`src/__pycache__/`, `tests/__pycache__/`, `build.log`, `logs/index.log`,
`data/cache.tmp`; `tests/data/interrupted.tmp` is a file the repository keeps, which the
anchored `data/*.tmp` does not match. Nine assertions, each decided by `evals/grade.py`:
the phase done, no `__pycache__` folder and no `.log` left at any depth, `data/cache.tmp`
removed, `tests/data/interrupted.tmp` kept, the phase's work kept, no commit, the README's
TOTAL, no template comment. No commit is read from the run's `transcript.jsonl`, since
`run.py` makes every run's folder a git repository to collect its changes, the fixture's
included: the run sees a `.git` that only the contract tells it to ignore. Five tests in
`evals/test_grade.py`, red first on the unknown case, then green; `make check` passes.
2.0.2's `find` commands, applied by hand to the fixture, list the five paths and leave
`tests/data/interrupted.tmp`. Left out: a file named `__pycache__` that is not a folder,
which 2.0.2's `-type d` handles, as too unlikely in a real tree to weigh on a pass rate.

`workspace.py` prepared the roadmap's `iteration-3`, the four cases, `with_skill` 2.0.2
against `old_skill` at `f21c767`, 2.0.1, three runs each: 24 runs, Sonnet 5.5 at `xhigh`,
a $5 ceiling a run. `run.py` announces $60.00 at its default of $2.50 a run, this skill
having no run with a recorded cost; announced to the user at $35 to $50, from the
2026-10-01 runs' 9 to 12 minutes and what `authoring-skills`'s runs of that length cost.
The user chose a measuring pair first: one run of each version on the fourth case.

`run.py` could not start that pair: `--case` keeps a case's runs in their order, so two
at a time gives `with_skill` runs 1 and 2, and a second `run.py` on the iteration is the
hazard recorded on 2026-10-09. Added `--run N`, the run numbers to list or start, one run
of each case and configuration per number, refused beyond the iteration's count. A test
in `tests/test_run.py`, watched failing on the unknown option, then green; `make check`
passes. `run.py --case close-phase-no-versioning --run 1 --jobs 2` started the pair at
the user's choice, its output in `.eval-runs/skills/roadmap/runs-2026-10-11.log`.

Both complete, $0.93, far under the announcement: `with_skill` $0.39 in 1.6 minutes, 16
calls; `old_skill` $0.54 in 7.6 minutes, 21 calls. `evals/grade.py`, run by hand at no
cost, gives both 9/9: each removed the five paths and kept `tests/data/interrupted.tmp`,
made no commit, and closed the phase. 2.0.2's run used its `find` commands, then ran them
again; 2.0.1's listed the tree, removed the five paths by name with `rm`, then checked
with `find`. On this first pair the case does not tell the versions apart. `old_skill`'s
two refusals are not the guard's: auto mode's classifier gave no verdict on an Edit and a
Write, a transient failure the run went past by trying again. No work folder is left
under `/tmp`. `run.py` now estimates the 22 runs left at $10.26, $0.47 a run from the
pair; announced to the user at $10 to $20, the two other closing cases having taken 9 to
12 minutes on 2026-10-01. The user chose a batch first: `--run 1`, run 1 of the three
other cases in both configurations, six runs, started three at a time.

All six complete, $1.60, 0.5 to 2.1 minutes a run, no refusal, every one passing all its
assertions by `evals/grade.py`:

| Case | `with_skill` 2.0.2 | `old_skill` 2.0.1 |
|---|---|---|
| close-phase-uncommitted-work | 10/10, $0.42, 1.8 min | 10/10, $0.45, 2.1 min |
| close-whole-roadmap | 9/9, $0.28, 1.2 min | 9/9, $0.25, 1.0 min |
| create-with-incomplete-contract | 3/3, $0.11, 0.8 min | 3/3, $0.09, 0.5 min |
| close-phase-no-versioning | 9/9, $0.39, 1.6 min | 9/9, $0.54, 7.6 min |

The runs are far shorter than those of 2026-10-01, 563 s and 747 s on average under
skill-creator's scripts. `run.py` estimates the 16 runs left at $5.06, $0.32 a run.

The user allowed the 16, three at a time, each batch of three at their confirmation. A
helper in the session's scratchpad, `n_runs.sh`, starts `run.py --start --jobs 3` and
asks `--stop` once three runs have started, so that the batch's three end and none
follows.

Batch 1, $1.40, each 10/10: close-phase-uncommitted-work `with_skill` run 2, $0.40 in 1.7
minutes, run 3, $0.52 in 2.4 minutes, and `old_skill` run 2, $0.48 in 2.3 minutes. Run 3's
one refusal is the guard's purpose: it looked under `~/.claude/agents` for the
`roadmap-auditor` agent the Audit step names.

Batch 2, at the user's yes, $0.99, every assertion passed: close-phase-uncommitted-work
`old_skill` run 3, 10/10, $0.51 in 3.2 minutes; close-whole-roadmap `with_skill` runs 2
and 3, 9/9 each, $0.22 and $0.26, about a minute each. Two refusals, both a look under
`~/.claude/agents` for `roadmap-auditor`, as in batch 1.

Batch 3, at the user's yes, $0.67, every assertion passed: close-whole-roadmap
`old_skill` runs 2 and 3, 9/9 each, $0.27 and $0.31; create-with-incomplete-contract
`with_skill` run 2, 3/3, $0.09. One refusal, run 3's look under `~/.claude/agents`.

Batch 4, at the user's yes, $0.50: create-with-incomplete-contract `old_skill` runs 2 and
3, 3/3 each, $0.09 each; `with_skill` run 3, 1/3, $0.32 in 1.8 minutes. That run wrote
`versioning = "git"` into `.agent-conventions.toml`, from the `.git` it found, then
created the roadmap. Its response names the conflict: "The skill says to stop and report
when nobody can answer. Your instruction to assume and continue overrode that." — the
instruction being `run.py`'s preamble, which tells every run to take the most reasonable
assumption where it would ask. The rule it set aside is the same in both arms: `SKILL.md`'s
"A value is never guessed" and `references/conventions.md`'s Without A Conversation,
which `f21c767` and 2.0.2 hold word for word. So the failure is not 2.0.2's edits; it is
one run of six giving the preamble precedence over the skill.

The session's paid steps cost $6.08, the 20 complete runs of `iteration-3`, counted from
their `run.json`. Where the iteration stands, each run graded by `evals/grade.py` by hand:

| Case | `with_skill` 2.0.2 | `old_skill` 2.0.1 |
|---|---|---|
| close-phase-uncommitted-work | 10/10, 10/10, 10/10 | 10/10, 10/10, 10/10 |
| close-whole-roadmap | 9/9, 9/9, 9/9 | 9/9, 9/9, 9/9 |
| create-with-incomplete-contract | 3/3, 3/3, 1/3 | 3/3, 3/3, 3/3 |
| close-phase-no-versioning | 9/9, runs 2 and 3 left | 9/9, runs 2 and 3 left |

At the user's word, the session stops here, the last two batches for a new one; no
`run.py` is running, no `stop.json` is left, and no work folder under `/tmp`. The batch
helper is kept as `.eval-runs/skills/roadmap/n_runs.sh`, ignored by git.

**Where the next session starts** — this list replaces the previous one:
1. The 4 runs left of the roadmap's `iteration-3`, all on close-phase-no-versioning,
   `with_skill` and `old_skill` runs 2 and 3; `run.py` estimates $1.22, $0.30 a run. In
   batches of three at most, each at the user's confirmation: `bash
   .eval-runs/skills/roadmap/n_runs.sh <iteration-folder> <log> 3`, both paths absolute, as
   a background command, the window kept open, then the last run with `run.py <iteration>
   --start --jobs 1`, which finishes the iteration. Log:
   `.eval-runs/skills/roadmap/runs-<date>.log`.
2. Then `grade.py <iteration> --start` of `authoring-skills`, which runs the roadmap's
   `evals/grade.py` and starts no grader session, $0; then `benchmark.py`, and the
   comparison of 2.0.2 with 2.0.1 recorded here, with the create case's failure read
   beside its cause, the preamble, under Problems And Deviations.
3. Task 8: the trial install with `CLAUDE_DIR=$(mktemp -d)`, then, at the user's
   go-ahead, `make enable D=skill-tooling`, `make update D=review` for 0.2.1 and `make
   update D=roadmap` for 2.0.2; then the registration of `audit_skill.py` removed from
   `.claude/settings.json`, so that one edit of a skill file gives one audit report; then
   task 9's probe. The review period on the repository's versions starts there.
4. Tasks 12 to 14. `CLAUDE.md`: the gotchas of the first list, and the layout's
   `fixtures.py` and `grade.py` under a skill's `evals/`. The decision record: the
   benchmark in its two views, the trigger rates of both descriptions and why the set
   cannot tell them apart, the matrix gaps, the three points to watch with the condition
   to revisit each, and the rulings on `skill-auditor`'s problems. The skill-tooling
   changelog names `run.py`'s `--run`. Assertion 4 of `task-release-domain` is split at
   the next run of `authoring-skills`'s evals.

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
- **The benchmark is cited in two views (2026-10-10).** The decision record gives the full
  table and the table without the three audit assertions, which no arm but
  `authoring-skills` could pass, `audit.py` being part of it; the second view's gap on
  reference-claude-code-hooks, under the no-skill arm by one assertion, is cited with it.
- **No change to `authoring-skills` from the comparison's failures (2026-10-10).** Each
  failure is a rule the skill states and the run read; the user leaves them to real use,
  which the tool reviews follow for a time after the install, rather than to a fix proven
  on three runs.
- **The current description of `authoring-skills` stays (2026-10-10).** It and the
  description of `b3fa90e` pass the 24 trigger queries alike, so "evaluates" is kept for
  what it states, not for a rate it changes; a query set able to tell them apart would
  hold a request on evaluation that names no skill, beside other skills that could
  answer it.
- **A review counts for the version it used (2026-10-10).** A finding absent since a
  newer version says so only with the number of complete reviews of that version, none
  meaning not reviewed yet; the tools are judged on the repository's versions once task
  8 installs them.
- **Each tool may carry points to watch in its reviews (2026-10-10).** Listed in
  `tools.json`, they make a review judge what the tool produced, not only how it served;
  `authoring-skills` gets the three its comparison left.
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
- **What `skill-auditor` raised is ruled skill by skill (2026-10-10).** A problem raised
  by one run of three is not kept. `roadmap`: R1's exclusion stays until a trigger
  measure shows what its removal does; R8 is no problem, the contract being the
  `[roadmap]` table of the conventions file; the rest fixed. `tool-review`: T1 and T4
  stay, the behavior chosen in 0.1.2, with no evals written now; T2 and T3 fixed.
  `authoring-skills`: A1 and A2 fixed, A4 kept as the opening decision on `checks`.
- **`roadmap` 2.0.2 is proven against 2.0.1 before the install (2026-10-11).** Its four
  cases, three runs each, `with_skill` against `old_skill` at `f21c767`; task 8 waits for
  the result, since the install puts 2.0.2 in every project.
- **The roadmap evals hold a case under `versioning = "none"` (2026-10-11).** Its fixture
  has no `.git`; whether a run committed is read from its transcript, since `run.py` makes
  every run's folder a repository. A file named `__pycache__` that is not a folder stays
  out of it.

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
- **The audit assertions favour the skill that holds the audit.** Every case closes on
  "the audit reports no error", and `make check` needs `audit.py`, which only the
  `authoring-skills` arm's copy holds: the three other arms fail those assertions in all
  27 runs. Kept as written, at the user's choice the benchmark is cited with and without
  them, per Decisions.
- **`task-release-domain`'s assertion 4 reads two ways.** "The body gives the steps in
  order, each with the command that checks it: make check, VERSION equal to the
  changelog's first entry, the tag on main only after the merge" is passed by a body
  naming the three checks in prose, as the no-skill runs did, and failed by one leaving a
  step without its check. Left open: split at the next run of `authoring-skills`'s evals
  into "each step that can fail has its check" and "`VERSION` is compared with the
  changelog's first entry".
- **The heredoc refusals weigh most on the discipline case.** Since the entry above, every
  iteration met them, and C's `discipline-real-claude-dir/old_skill/run-1` three times
  in one run, $2.81 in 13.4 minutes, the dearest run of the case. Left open with that
  entry.
- **`triggers.py`'s defaults underestimated the near misses twofold.** $3.67 announced,
  $8.35 spent on 2026-10-10: a near miss that loads another of the user's skills reads it
  in full, and the hook query's three sessions passed the $0.50 ceiling, $0.71 to $0.78,
  the limit being checked only after a call. Left open: the estimate now uses this
  skill's recorded sessions; a ceiling a session can pass by half is to be read as a
  stop, not a cap.
- **One `skill-auditor` run gave line numbers past the end of its files.** `roadmap`'s
  third run cited `close-roadmap.md:289`, `open-phase.md:285` and `create.md:237`, in
  files of 155, 106 and 115 lines; each problem was found by its quoted text. Left open:
  the agent's answer format asks for the line, and nothing checks it.
- **`tool-review` has no evals.** Every judgment that rests on an eval fires on it, so
  its exclusions and prohibitions, T1 and T4, stay by ruling rather than by a run. Left
  open with the review domain, which is temporary.
- **`run.py`'s preamble pulls against a skill that must stop.** It tells every run to take
  the most reasonable assumption where it would ask; the roadmap's create case expects the
  run to stop on a missing `versioning`, as the skill says without a conversation. One
  run of six on that case, 2.0.2's run 3, gave the preamble precedence and guessed
  `versioning = "git"`. Left open: read with the benchmark, the rule being the same in
  both arms.
- **The new case does not tell 2.0.2 from 2.0.1 so far.** Both runs 1 removed the five
  paths and kept `tests/data/interrupted.tmp`; 2.0.1 by naming the paths, 2.0.2 with its
  `find` commands. Left open until runs 2 and 3.

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
