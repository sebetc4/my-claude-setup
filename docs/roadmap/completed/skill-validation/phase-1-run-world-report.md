# Phase 1 Report: Run World

**Phase:** [phase-1-run-world.md](phase-1-run-world.md)
**Start Commit:** 1c83afe

---

## Work Log

### 2026-10-14

Phase opened at the end of Phase 0's closure (`1c83afe`), in the session that closed it,
after Phase 0's file and report, written in that session; no restructuring was pending.
No work on the phase's tasks: the user starts it in a new session. The opening is left
uncommitted, to go with the phase's first finished step.

Where the next session starts: read Phase 0's file, its `## Design` above all, and its
report in full, then this phase's file. The first step is the probe the `hooks` key rests
on: whether a project SessionStart hook's output reaches a `claude -p` session under the
harness's flags (`--setting-sources project,local`, `--strict-mcp-config`, the guard
through `--settings`), on the installed Claude Code, dated; announce its sessions and
cost before starting them. Then the design's A Case's World, section by section, scripts
test-first, the map in Phase 0's Work Log giving each change's starting line, and
`docs/claude-code-coupling.md` updated with each new dependency on Claude Code.

Session resumed the same day. Read Phase 0's file and report in full, then this phase's;
told the user what carries: the design's A Case's World, E2 reduced to the fixture form,
and the probe still unsettled.

The probe, announced at $0.50 at most (one session under a ceiling of $0.50, about $0.10
expected from Phase 0's auditor passes) and started on the user's yes, on Claude Code
2.1.296: one session built by `harness.command` itself, Sonnet 5.5 at `low`, in a folder
outside any repository holding a project `.claude/settings.json` with a SessionStart hook
that prints `additionalContext` with a random marker and a PreToolUse hook that logs each
call, a `CLAUDE.md` with its own marker, and `--settings` carrying the harness's guard and
a second PreToolUse logger. Result, $0.04, 2 turns, complete:
- the session quoted both markers: a project SessionStart hook's context reaches a
  `claude -p` session under `--setting-sources project,local`, `--strict-mcp-config` and
  the `--settings` hooks; the hook got `source: startup` on its input;
- the transcript holds three `attachment` records of the session's start:
  `hook_success` (`hookName` `SessionStart:startup`, `command`, `stdout`, `exitCode`),
  `hook_additional_context` (`content`, a list of the context's strings, `hookEvent`
  `SessionStart`) and `instructions` (`files`, each with `path`, `type` `Project` and
  `content`);
- the project's PreToolUse hook and the one `--settings` adds each fired once on the
  session's single call: a case's hooks and the guard coexist.

The `hooks` key can rest on project hooks. The three records are what `render` will read
for the Grader's View task. Committed with the phase's opening, `2cfee0e`.

Task 1, the `hooks` key. Writing a case's hooks into the run's folder raised a problem the
design had not seen: `close-session`'s fixtures are git repositories, so a hook merged
into a fixture's `.claude/settings.json` would show in the run's `outputs/` and
`changes.json` as a change the run made. Two more probes, each a session on a model that
does not exist, so that it stops at its first API call after the SessionStart hooks ran,
$0 each, on 2.1.296: a SessionStart hook of `.claude/settings.local.json` runs and is
recorded as the project's was; so does one given through `--settings` beside the guard,
with nothing written into the run's folder. The case's hooks go through `--settings`,
which is also where an install puts them: in the user's settings, not in the project
the agent reads.

Reading the session domain's two SessionStart hooks showed a second condition: each
finds its skill's scripts by walking up from its own folder to `skills/<name>/scripts/`,
as `~/.claude/hooks/<domain>/` sits beside `~/.claude/skills/`. A run's copy of the skill
lay in `skill/<name>/`, where such a hook finds nothing and prints nothing, without an
error. The copy moves to `skills/<name>/`, and the hook files go to `hooks/<folder>/`
beside it, `<folder>` the hooks file's own (`session` for `domains/session/hooks.json`).

Test-first: `tests/test_workspace.py` gained `Hooks` (9 tests) and `tests/test_run.py`
gained `Hooks` (6 tests), its stub running the SessionStart hooks `--settings` carries and
writing their context into the transcript as Claude Code does, and the copy's path
`skills/demo`; all 16 seen failing — unknown key `hooks`, no hook context, the copy under
`skill/demo` —, then passing with the code:
- `scripts/workspace.py`: `hooks`, a string, checked by `hook_problems` — a JSON file of
  the repository mapping each event to a list of hook groups, naming no placeholder but
  `{{HOOKS_DIR}}`, with the folder `hooks/` beside it when it names that one;
  `with_skill_hooks/` and `old_skill_hooks/`, the baseline's at its revision through
  `git show` and `git archive`, caches left out; both left out of `base.tar`; the old
  arm's hooks in the snapshot digest, not in a case's digest, since the arm without the
  skill never receives them; a folder baseline refused; `iteration.json`'s `hooks`.
- `scripts/run.py`: `arm_hooks`, `session_hooks` (copy into `hooks/<folder>/`,
  `{{HOOKS_DIR}}` resolved, JSON-escaped as the installer does), the hooks back at their
  paths in a repository case, `run.json`'s `hooks`, the events the session started with.
- `scripts/harness.py`: `session_settings` takes `groups` beside the (event, command)
  pairs; its docstring records the probes of the day.
- `references/eval-files.md`: the key, the two folders, `iteration.json`'s and
  `run.json`'s `hooks`, and a hook turned off through the fixture's configuration;
  `docs/claude-code-coupling.md`: one row for the hooks given through `--settings`, the
  hooks format and the install layout; the domain's changelog, under 0.1.2, unreleased.

A check at no cost of the real hook: `domains/session/hooks/` copied to
`hooks/session/` and `close-session` without its evals to `skills/close-session/`, a work
folder with a `[session]` table and one open note; `resume_note.py`, given the work
folder as its event's `cwd`, printed the note's line, and printed nothing once
`start_notes = 0` was added: the hook runs in a run's layout, and a fixture turns it off.
`audit.py` clean on `authoring-skills`, `make check` passing; task 1 ticked.

Task 3, the grader's view. An inventory of the `attachment` records of 211 transcripts —
this repository's eval runs and sessions — gave the four that carry a context a session
was given beyond its prompt: `instructions` (each file's `path`, `type`, `content`),
`nested_memory` (an instruction file loaded when the session reads in its folder),
`hook_additional_context` and `hook_blocking_error`, the last seen in eval runs already,
from a project's PostToolUse hook, and lost by `render`. Each record also holds
`rendered`, the text as the model received it; left unused, since the fields give each
file's path and size and add no further tie to Claude Code.

Test-first: `tests/test_run.py` gained `Render` (4 tests, a transcript fixture of the
four records shaped as 2.1.296 writes them) and two tests in `Hooks` (the run's
`context/`, an agent's `context/<type>-<id>/`, the stub given a head for its agent's
transcript); `tests/test_grade.py` gained `Context`; all 7 seen failing, then passing:
- `scripts/harness.py`: `CONTEXT_KINDS`, `contexts()`, and `render(path, context,
  shown_as)`, which writes a `## Context: instructions` or `## Context: hook <name>` entry
  where the record came, with the path and type and the size in characters, and, given a
  folder, the content whole as `NN-<name>`;
- `scripts/run.py`: the run's `context/`, each agent's beside it;
- `scripts/grade.py`: `context/` copied for the grader and named in its request;
- `agents/skill-grader.md`: an assertion or claim about what a session had loaded or was
  told is settled from `context/`;
- `references/eval-files.md`, the coupling row of the transcript's records, the
  changelog.

`make check` passing. The task's second proof waits for the user's leave: ai-ctl's
iteration 2 run graded again on "Claims hold" as Phase 1 of `review-skill` wrote it.
Committed, `268abbf`.

With the user's leave to read ai-ctl, announced at $1 at most (one grader session under
`grade.py`'s ceiling): ai-ctl's `iteration-2/post-session-review/with_skill/run-1`
copied, ai-ctl's files only read, into this repository's ignored
`.eval-runs/skills/reviewing-delivered-code/claims-regrade/iteration-2`, its case holding
"Claims hold" alone, the text graded on 2026-10-13 ("every file the report or the
closing account says was read was opened by a call of the run or of its agents, in full
where it says in full"), its `grading.json` left out; `transcript.md` and `agents/`
rendered again from the transcript and `subagents/` by the current `render` and
`render_agents`. Eleven `context/` files came out, `CLAUDE.md` whole at the start of the
main session and of each of the ten agents, `review-structure`'s among them, the entry
placed after each agent's prompt, where its transcript records it.

`grade.py --start`: 1/1 passed, $0.60, Sonnet `xhigh`, 2.1.296. On `review-structure`'s
`CLAUDE.md`, failed on 2026-10-13 for a `sed -n 35,60p`, the grader writes: "Its
CLAUDE.md was only partly printed by call (`sed -n 35,60p`), but the instruction file was
loaded whole in its context (`context/review-structure-…/01-CLAUDE.md`)." The true claim
R1 names is now graded true, the assertion as written. The grader also notes: "The
handbacks are truncated in the agent files, so the structure agent's `build_store.rs
(138-290)` range could not be checked": `render` shortens every text and result past
2,000 characters (`SHOWN`), an agent's closing answer included. Task 3 ticked.

Raised with the user, who added it to this phase: a task under Grader's View keeps whole
each text and result `render` shortens, an agent's closing answer first, its proof a
transcript fixture red before the code. The phase holds six tasks, two done; the README's
progress block is recomputed at the closure.

The session ends here, at the user's request; the phase goes on in a new one. Spent in
this session: $0.64, the probe $0.04 and the regrade $0.60, the two other probes $0.
Where the next session starts:
- **Task 5, Figures**, test-first and at no cost, from R3 of ai-ctl's note, each point
  with its line: `harness.figures` takes `duration_s` from the result's `duration_ms`
  (`harness.py:216-219`), which misses the wall time of a session waiting on background
  agents — the design takes it from `started` and `ended`; `run.py`'s `counted` shares
  the reported output among the agents' estimated calls with `usage.settle`, equal per
  call, and `run.json`'s `agents` does not mark it — each agent's output is to be marked
  `settled` where it is shared; `benchmark.py`'s footnote (`:330-333`, `estimated_runs`
  at `:142`) speaks of calls estimated at 5,400 tokens without reading `output_source`;
  its effort note (`:236-241`) reports the efforts a skill gives its agents as a
  deviation — the design applies it to the main session's calls, each agent's effort
  shown beside it. Tests in `tests/test_run.py` (the stub's `STUB_SUBAGENT`) and
  `tests/test_benchmark.py`.
- **The new task, whole texts**, test-first and at no cost: `harness.shorten` and
  `SHOWN` (`harness.py:58`, `:290`), used by `render` for texts and results.
- **Tasks 2 and 4**, both in `references/evaluate.md` — the check that a case's world is
  one the skill can meet, and a workflow's later step tested from a fixture holding the
  state before it — each proven by an eval of `authoring-skills`' own evals: one
  iteration for both, its runs announced with their count and cost before any start.
- The regrade's copy stays in the ignored
  `.eval-runs/skills/reviewing-delivered-code/claims-regrade/`; ai-ctl's tree is
  untouched.

Session resumed the same day. Read this phase's file and report and Phase 0's in full;
told the user what carries: the two decisions above, tasks 1 and 3 done, the order the
previous session left, no dependency unsettled.

Task 5, the figures, at no cost. Read first: `usage.session` already takes a run's last
output from its Agent result, so the design's "each agent's output where its Agent result
records it" held; what R3 names was left: the duration, the per-agent mark, the footnote,
the effort note. The note's per-model figure has the same defect as its effort: an agent
whose frontmatter sets another model is noted as a deviation; both treated alike.

Test-first: `tests/test_run.py` gained four tests in `Agents` — the duration with a stub
sleeping one second and reporting 100 ms, each agent's `output_source` `settled`,
`estimated` and `transcript` (the last on `counted` directly, the stub's agent always
lacking one output), its `models` and `efforts` — and `Command`'s check of the result's
duration moved to `reported_duration_s`; `tests/test_benchmark.py` gained three — the
agents' models and efforts shown beside and never noted, a session's own call at another
effort noted beside its agents, the footnote reading `output_source`. All eight seen
failing, two of them on R3's very notes ("2 of 5 calls at high, where the iteration sets
xhigh"), then passing:
- `scripts/harness.py`: `figures(result, seconds)` gives `duration_s`, the session's wall
  time `harness.start` measures, and `reported_duration_s`, the result's `duration_ms`;
  `run.py`, `grade.py`, `triggers.py` and `tuning.py` pass it, their fallback on
  `session.seconds` gone. `Status`'s test of a run's line now sets its `duration_s`, the
  stub's wall time being under a second.
- `scripts/run.py`: `counted` gives each agent type `estimated_calls`, `models`,
  `efforts` and `output_source` — `transcript`, `settled` where the run's source is
  `reported`, else `estimated`.
- `scripts/benchmark.py`: each run's `output_source` (from its estimated calls for a
  `run.json` older than the key) and `agents`; `estimated_runs` and the `*` only for
  `estimated`, the footnote naming `usage.py`'s estimate by agent type and effort (5,400
  tokens is only its default); one note for the runs whose output comes from the reported
  total; the model and effort notes on the session's own calls, the run's counts less its
  agents'; the Runs table's Models and Efforts the session's, then each agent's.
- `references/eval-files.md`, the two docstrings, the changelog. No new tie to Claude
  Code: `duration_ms` is still read, as `reported_duration_s`.

Checked at no cost on ai-ctl's run copied for the regrade, its transcript and
`subagents/` laid out as a session's: `counted` gives the same cost, $8.313, and each of
the six agent types the same as `run.json` recorded ($0.32 to $0.88 a reviewer, $2.43 for
the five verifiers), now each marked `settled`; the 128 calls at `high` are the agents'
alone (15 + 19 + 8 + 7 + 11 + 68), so the effort note finds the session's 35 calls at
`xhigh` and says nothing. The session's wall time there: 812 s between `run.json`'s
`started` and `ended`, its transcript from 19:49:08 to 20:02:38, against the 120.6 s the
result reports. `audit.py` clean on `authoring-skills`, `make check` passing; task 5
ticked. Committed, `766fdb8`.

The whole-texts task, at no cost. `render` cut each text, call input and result past
2,000 characters (`SHOWN`); call inputs taken in with texts and results, `shorten`
cutting all three alike.

Test-first: `tests/test_run.py` gained `Whole` (4 tests, a transcript fixture of an
agent's run holding a tool result and a closing answer past 2,000 characters) and, in
`Hooks`, an agent's closing answer kept whole by a run, the stub's agent given a long
final text; `tests/test_grade.py`'s `Context` gained the request naming `whole/`. Seen
failing — no `whole/`, the cut naming no file, the request silent —, then passing:
- `scripts/harness.py`: `render(path, kept, under)` takes the run's folder and, for an
  agent, its `<type>-<id>`; each context goes to `context/` as before, and each cut
  item whole to `whole/`, numbered in the order the cuts come, `NN-prompt.txt`,
  `NN-agent.txt`, `NN-call-<tool>.json` or `NN-result.txt`, the cut ending
  "… (N more characters, whole in `whole/…`)"; `shorten(text, whole)`, `Kept`. Without
  a folder, a cut is counted alone, as before.
- `scripts/run.py`: both `render` calls pass the run's folder.
- `scripts/grade.py`: `whole/` copied for the grader and named in the request;
  `agents/skill-grader.md`: an assertion or claim that turns on what a cut leaves out is
  settled from the file it names.
- `references/eval-files.md`, `run.py`'s docstring, the changelog. No new tie to Claude
  Code.

Checked at no cost on ai-ctl's run copied for the regrade, rendered again into the
scratchpad: 22 cuts of the main transcript and 97 of the ten agents written whole. The
agents of 2.1.296 do not end on a text: each hands its answer back by a
`SubagentHandback` call, `{"message": …}`, so the closing answer is a call's input, and
the structure agent's `build_store.rs (138-290)`, which the regrade could not check, is
whole in `whole/review-structure-a92d46447158c324e/13-call-SubagentHandback.json`. Had
the task kept texts and results only, as its wording says, the closing answer would
have stayed cut. `Whole`'s fixture rewritten to that form, the handback a call, and seen
failing again on the previous `harness.py` before the commit; the run-level test keeps
an agent that ends on a text. `make check` passing, `audit.py` clean; the task ticked.
Committed, `4f345fb`.

Tasks 2 and 4, both in `references/evaluate.md`, proven by one iteration of
`authoring-skills`' own evals. Its Edit section asks the target cases with the previous
version first, then with the new one: the cases written before any word of
`evaluate.md`, the old version run on them, and the text written for the failures they
show. Two cases, each on the sample skill `writing-notes` edited by its last commit, as
`evaluate-an-edit` is:
- `evaluate-a-hooked-skill` (task 2): the skill in a domain, `domains/notes/`, beside
  `hooks.json` and `hooks/open_notes.py`, a SessionStart hook naming the notes still in
  draft; the change has the skill add to an open note the session's start names. Its
  assertions: `hooks` declared as the domain's file, a case starting with an open note
  and one with none, each expected output saying which line the session starts with.
- `evaluate-a-later-step` (task 4): the change adds the closing of a note in a session
  after the one that wrote it; the ignored workspace holds the iteration of
  `evaluate/results/`, each run's note in its `outputs/`. Its assertions: a closing case
  starting from a draft note, not one session writing then closing; that note taken
  from a recorded run's outputs; the writing cases kept.
- Both: assertions by their measure, the baseline the commit before the change, the
  runs announced and none started, as `evaluate-an-edit` asks.

`evals/fixtures.py` builds both, test-first: two tests in `evals/test_fixtures.py`, seen
failing on an unknown case, then passing; the hook's line checked by running it on a
folder with a draft note and a done one. `make check` passing. Committed, `e6ad590`.

Iteration 8 of `authoring-skills`' evals, the two cases, `old_skill` alone at `e6ad590`,
three runs each, Sonnet 5.5 at `xhigh` under a $1 ceiling, announced at $6 at most and
about $1.50 from `evaluate-an-edit`'s runs, started on the user's yes: six runs
complete, $2.58, $0.36 to $0.46 a run. Read before any grading, at no cost:
- `evaluate-a-hooked-skill`: all three declare `hooks` as `domains/notes/hooks.json`,
  each with a case starting on an open note and one or two without; the previous version,
  whose `eval-files.md` gives the key since task 1, already provides the hook. All three
  then stopped in `workspace.py --baseline HEAD~1`: `snapshot_hooks` fails with
  `ValueError: 'domains' is not in the subpath of 'domains/notes'`, since `git archive`
  lists the folders above a nested hooks file as entries of their own. Run 1 reported
  it and stopped; runs 2 and 3 patched a copy of `workspace.py` to go on. A defect of
  task 1's code, which its tests missed, their hooks file one folder deep.
- `evaluate-a-later-step`: all three test the closing from a draft note already in
  `notes/`, given by `files` or built by `evals/fixtures.py`, none asking one session to
  write then close, the writing cases kept. None takes the note a recorded run left: run
  1 read the recorded outputs and wrote variants, runs 2 and 3 wrote their own. That is
  the one point the design's text for task 4 would answer.

The defect fixed test-first: `tests/test_workspace.py`'s `Hooks` gained a hooks file in
`domains/notes/`, snapshotted at a revision, seen failing on the runs' very error, then
passing once `snapshot_hooks` leaves out the members above the hooks folder. `make
check` passing, `audit.py` clean. Case 7's runs ran on the broken tool: by the design's
`tool` class, they are run again on the fixed one. Committed, `c4c47a2`.

Iteration 9, the same two cases at `c4c47a2`, `old_skill` alone, announced at $6 at most
and about $2.60 from iteration 8, started on the user's yes: the three runs of
`evaluate-a-hooked-skill` and the first of `evaluate-a-later-step` complete, $0.26 to
$0.34; the two others stopped by the subscription's limit, $0.63, to start again once
it resets (20:20). Read at no cost:
- `evaluate-a-hooked-skill`: the three declare `hooks` as `domains/notes/hooks.json`,
  each with a case on an open note and one without, and prepare the iteration on the
  fixed `workspace.py`, none stopping. Six runs in six across iterations 8 and 9 provide
  the hook: what V1 lacked, the key itself, is in the previous version since task 1.
- `evaluate-a-later-step`, run 1: a closing case from draft notes written by hand under
  `evals/notes/`; the recorded outputs not read. Four runs in four test the later step
  from a fixture holding the state before it; none in four takes a recorded run's note.

Raised with the user, who chose on this evidence: task 2 without any text, the case kept
in the evals as a guard, the task ticked on the six runs; task 4 by one sentence, the
part the runs lack. `references/evaluate.md`'s The Cases gained it: a step a later
session takes on what an earlier one left starts its case from that state as the earlier
step really leaves it, a recorded run's outputs copied by `evals/fixtures.py` when one
exists. `audit.py` clean. Task 4 waits for its runs with the new version, once the
limit resets. Committed, `96f3798`.

Iteration 10 prepared at no cost: `evaluate-a-later-step` alone, `--baseline c4c47a2
--reuse iteration-9`, `with_skill` at `96f3798`; `run.py` lists five runs, the three of
`with_skill` and iteration 9's two stopped `old_skill` runs again, its first reused,
$5 at most under the $1 ceiling, about $2 from this case's measured runs.

The session ends here, at the user's request; the five runs go to a new session. Spent
in this session: $4.41, iteration 8 $2.58 and iteration 9 $1.83 so far; no grading yet.
Iteration 8 stays ungraded, an observation made on the broken `workspace.py`. Where the
next session starts:
- **Iteration 10's runs**: `scripts/run.py .eval-runs/skills/authoring-skills/iteration-10`,
  announced with its count and cost, started on the user's yes, once the
  subscription's limit of 2026-10-14 (20:20) has reset.
- **The gradings**, each announced: `grade.py` on iteration 10 (six runs of
  `evaluate-a-later-step`) and on iteration 9 (the three of `evaluate-a-hooked-skill`,
  the guard of task 2), then `benchmark.py` on iteration 10. Task 4 is proven when the
  new version's runs start the closing case from a recorded run's note where the
  previous version's never did (none in four read so far), the other assertions holding.
- **Two passes of `skill-auditor`** on `authoring-skills`, started together, by
  `references/audit.md`, announced at about $0.10 each; the skill is done only when both
  answer `VERDICT: PASS`.
- **Then the phase's closure**, every task done, by the roadmap skill's `close-phase.md`.

Session resumed the same day, at 17:45, before the limit's announced reset. Read this
phase's file and report in full; told the user what carries: the decisions above, task 4
waiting for its runs, no dependency unsettled. Iteration 10's five runs announced at $5
at most, about $2, the limit possibly still in force; started on the user's yes. The limit
had lifted: five runs complete, $1.98, $0.29 to $0.55 a run. Read before any grading, at
no cost:
- `with_skill`, three in three: each adds an `evals/fixtures.py` that copies into the
  closing case's folder a note a recorded run of the writing step left, kept under
  `evals/recorded/` or `evals/fixtures/`; each such note is byte for byte the one in
  `decision-note/with_skill/run-1/outputs/` or `nothing-follows/with_skill/run-1/outputs/`
  under the fixture's `iteration-1/`. The writing cases kept, the baseline `HEAD~1` or the
  commit before the change.
- `old_skill`, runs 2 and 3 of iteration 9 run again: draft notes written by hand, under
  `evals/notes/` or built by a `fixtures.py` that copies nothing recorded. With iteration
  8's three and iteration 9's first, none in six takes a recorded run's note.

The sentence of `96f3798` gives what the previous version lacked; the gradings decide the
other assertions.

The gradings, announced at $9 at most, about $2.17, nine sessions, started on the user's
yes. Iteration 9's `evaluate-a-later-step/old_skill/run-1` is the run iteration 10
reused, its transcript and `run.json` the same byte for byte and the evals unchanged
between `c4c47a2` and `96f3798`: graded once in iteration 10, its `grading.json` and
`grader/` copied into iteration 9, which then listed three runs.
- Iteration 10, $1.09: `with_skill` 6/6 in each run, `old_skill` 5/6 in each, the one
  assertion failed the recorded run's note, the grader finding each `old_skill` note
  written by hand. `benchmark.py`: pass rate 100% against 83%, +17 points, cost +$0.088 a
  run. Assertions 1, 3, 4, 5 and 6 pass in both arms. Task 4 is proven.
- Iteration 9, `evaluate-a-hooked-skill`, $0.45: 5/6, 4/6, 4/6. Assertion 1, the `hooks`
  key, passes in all three. Failed: "each case's expected output says whether the session
  starts with a line naming an open note, and which one", in all three; "at least one
  [case] starts with no open note", in runs 2 and 3, whose `fixtures.py` gives every case
  the same draft. Checked against the runs' files, the grader holds. Iteration 8's three,
  read at no cost: one in three says in each expected output what the session starts
  with, one has no case without an open note. The previous session's reading, "a case on
  an open note and one without", took a case with no open note on its subject for one
  with none.

The decision on task 2 rested on that reading: the previous version provides the hook,
six in six, but in one run in six says what each case's session starts with, which is
the "declared" half of the design's check. Raised with the user, who chose to write the
missing text. Task 4 ticked, task 2 unticked. `references/evaluate.md`'s The Cases gained
one bullet: a skill that relies on what its session starts with, such as a hook's line,
has a case for each start the change depends on, one where nothing is printed among
them, each expected output saying which start its run gets. `audit.py` clean, `make
check` passing. Committed, `252f76f`.

Iteration 11, `evaluate-a-hooked-skill` alone, `--baseline c4c47a2 --reuse iteration-9`,
`with_skill` at `252f76f`, three runs, $3 at most, the cost given in the option the user
chose: complete, $0.97. Iteration 9's gradings copied into the reused runs, the same
files byte for byte, then three grader sessions, $0.49. `benchmark.py`: 94% against 72%,
+22 points, cost +$0.036 a run.
- The start declared in each expected output: three in three, against none in three;
  the hook's line quoted or "no line" with its reason.
- A case where the hook prints nothing: three in three (an empty folder, or a note
  closed), against one in three.
- Run 2 still fails assertion 2, on its other half: its two cases on an open note build
  it from `evals/recorded/postgres-note/`, which does not exist yet, so that the
  iteration prepares `nothing-open` alone, its plan recording that case's note first and
  copying it in. The later-step bullet of `96f3798`, "a recorded run's outputs … when one
  exists", read as asking for a recording before any case starts from a note: the state
  a writing step leaves taken for a later step's, and "when one exists" for "once one
  exists". None of the six `old_skill` runs did so.

Task 2 ticked on iteration 11. Raised with the user, who chose to settle the case with no
recorded run: the later-step bullet now says that, with no run of that step recorded
yet, the case writes the state by hand, as the step leaves it, so that the first
iteration runs every case; "when one exists" gone. `audit.py` clean, `make check`
passing. Committed, `9fc7717`. `workspace.py`'s `--reuse` takes one iteration, so two at
`9fc7717`, the first prepared with both cases deleted before any run: iteration 12,
`evaluate-a-hooked-skill` reusing iteration 11's `old_skill` runs, and iteration 13,
`evaluate-a-later-step` reusing iteration 10's; six runs, $6 at most, the cost given in
the option the user chose, started. Six runs complete: iteration 12 $0.86, iteration 13
$1.13. Read before any grading, at no cost:
- Iteration 12, `evaluate-a-hooked-skill`: the three write the open note by hand, each
  `fixtures.py` saying no run of the skill is recorded yet. What run 2 of iteration 11
  missed is answered, three in three.
- Iteration 13, `evaluate-a-later-step`: run 3 copies the recorded notes from the
  fixture's `iteration-1/`, as the three of iteration 10 did; run 1 writes them by hand,
  its `fixtures.py` saying no run of the writing step is recorded yet, where the fixture
  holds the iteration of `evaluate/results/`; run 2 writes them by hand under
  `evals/notes/`. One in three against three in three before: the clause "with no run of
  that step recorded yet" read as leave to write by hand without looking for one. Task 4
unticked: the text that proved it on iteration 10 is no longer the skill's.

The session ends here, at the user's request, the window's end near. Spent in this
session: $6.97, the runs $4.94 (iterations 10, 11, 12, 13), the gradings $2.03.
Where the next session starts:
- **The gradings**, announced together: `grade.py` on iteration 12 and on iteration 13,
  three `with_skill` runs each, the reused `old_skill` runs' `grading.json` and `grader/`
  first copied from iterations 11 and 10 after checking `transcript.jsonl` and
  `run.json` the same; about $1.10, $6 at most; then `benchmark.py` on both.
- **The later-step bullet**, if the gradings confirm the reading above: a wording that
  keeps both, the recorded run looked for first under the eval workspace and copied, the
  state written by hand only when none is there, decided with the user on the gradings;
  then one more iteration on both cases, `with_skill` alone, the `old_skill` runs reused.
- **Two passes of `skill-auditor`** on `authoring-skills`, once its text is settled,
  started together, by `references/audit.md`, about $0.10 each; done only on two
  `VERDICT: PASS`.
- **Then the phase's closure**, every task ticked, by the roadmap skill's
  `close-phase.md`. Iterations 12 and 13 stay ungraded until then.

### 2026-10-15

Session resumed. Read this phase's file and report in full; told the user what carries:
the decisions above, task 4 reopened on the clause of `9fc7717`, iteration 12 ungraded,
no dependency unsettled. The reused `old_skill` runs of iterations 12 and 13 checked
against iterations 11 and 10: `transcript.jsonl`, `run.json` and the case's
`eval_metadata.json` the same byte for byte, `grader/` already carried by `--reuse`;
their `grading.json` copied. `grade.py` listed six grader sessions, about $1.34, $6 at
most, started on the user's yes: $0.96.
- Iteration 12, `evaluate-a-hooked-skill`: `with_skill` 6/6 in each run, `old_skill`
  5/6, 4/6, 4/6; `benchmark.py` 100% against 72%, +28 points, cost -$0.001 a run. Task 2
  holds on the current text.
- Iteration 13, `evaluate-a-later-step`: `with_skill` 5/6, 5/6, 6/6, `old_skill` 5/6 in
  each; 89% against 83%, +6 points, against +17 on iteration 10. Runs 1 and 2 fail the
  recorded run's note alone. The grader finds `iteration-1` holding the writing cases'
  runs in both: run 1 listed it once and never opened their `outputs/`, its
  `fixtures.py` saying no run of the writing step is recorded; run 2 wrote its notes,
  then listed `iteration-1` and read its benchmark, and still wrote that none is
  recorded. The reading of the previous session holds: "with no run of that step
  recorded yet" is taken for a finding the run may state, not a search it must make.

Raised with the user, who chose the wording that has the run looked for first: the
later-step bullet of `references/evaluate.md` now says to look for that run first, in
the `outputs/` of the skill's iterations under the workspace, in each case whose prompt
takes that step, and to write the state by hand only when no iteration holds one. The
changelog's line follows. `audit.py` clean, `make check` passing. Committed, `cebcd6f`.

Two iterations at `cebcd6f`, `--baseline c4c47a2`, `with_skill` alone: iteration 14,
`evaluate-a-hooked-skill` reusing iteration 12's `old_skill` runs, and iteration 15,
`evaluate-a-later-step` reusing iteration 13's. Six runs announced at $6 at most, about
$2 from iterations 12 and 13 (`run.py`'s $5.40 being the mean of all the skill's runs),
started on the user's yes: six complete, $2.51. Read before any grading, at no cost:
- Iteration 15: three in three start the closing cases from the notes the writing
  cases' runs left under the fixture's `iteration-1/`, against one in three in
  iteration 13. Runs 1 and 3 copy them through `evals/fixtures.py`, run 3 choosing each
  writing case's first complete `with_skill` run with no failed assertion; run 2 wrote
  notes by hand first, found `iteration-1` afterwards, `ls -R` having hidden the dotted
  `.eval-runs`, and replaced them. Only the earlier line of `next.md` is written by
  hand, no closing run being recorded.
- Iteration 14: three in three write the open note by hand, no iteration being in that
  fixture; each says so.
The reused `old_skill` runs checked against iterations 12 and 13, the same byte for
byte, their `grading.json` copied; six grader sessions announced at about $1.28, $6 at
most, started on the user's yes: $0.98, every `with_skill` run 6/6.
- Iteration 15, `evaluate-a-later-step`: 100% against 83%, +17 points, as on iteration
  10; the recorded run's note passes three in three, against none in three for
  `old_skill`. Task 4 proven again, on the text the skill now holds.
- Iteration 14, `evaluate-a-hooked-skill`: 100% against 72%, +28 points, as on
  iteration 12. The new wording costs task 2 nothing.
- The search costs: +$0.128 and +51 s a run on the later-step case against
  `old_skill` (+$0.032 and +9 s on iteration 13), +$0.079 and +42 s on the hooked case
  (-$0.001 and -3 s on iteration 12), the runs now looking through the workspace before
  writing their fixtures.

Task 4 ticked; the six tasks done. `progress.py --check` finds the phase file's count
updated and the README's block lagging, recomputed at the closure. Committed, `47d1974`.

Two passes of `skill-auditor` on `authoring-skills`, started together on the user's yes,
the request `references/audit.md` gives (the skill's folder, the writing guide's path,
`audit.py`'s output, clean): $0.42, Sonnet 5.5 at `medium`. One answered `VERDICT: PASS`;
the other `VERDICT: FAIL`, six lines, none on a line this phase changed:
- four cite a line past the end of their file, the passage they quote standing
  elsewhere in it: `references/discipline.md:261` for line 20 of 74, the three
  pressures without a source; `references/create-and-edit.md:229` and `:211` for lines
  133 and 116 of 146, the five samples without a source and the previous version copied
  as the baseline with no exact step; `references/evaluate.md:327` for lines 3 to 5 of
  134, eval, case and query used for one thing;
- two cite their line: `references/conventions.md:16`, a prohibition ("never as one the
  user already approved") no failure grounds, and `:45`, the old block's removal offered
  with no edit nor check; that file is the copy of `shared/conventions/conventions.md`,
  shared with the roadmap and tool-review skills.
The same text and request, PASS and FAIL: V3, which Phase 2's Auditor task answers, a
line past the file's end being one of the evidences Phase 0's design gives for an
auditor's defect. Raised with the user with three ways — the points answered now, the
auditor fixed first, or the phase closed with the points moved —, who chose the last:
the FAIL not counted as a PASS, the split verdict given to Phase 2's Auditor task as
evidence, the sources and the prohibition to Phase 3, the three others to Phase 4's
audit of `authoring-skills`, which asks for two PASS already.

Spent in this session: $4.87, the gradings $1.94 (iterations 12 to 15), the runs $2.51
(iterations 14 and 15), the auditor $0.42. Phase closed the same day.

---

## Decisions

- **A case's hooks reach its runs through `--settings`, not the run's folder.** Written
  into the folder, they would show among a fixture repository's changes; through
  `--settings`, probed on 2.1.296, a SessionStart hook runs and its context is recorded
  as a project's, and the agent finds in the project what an installed repository holds.
  The grader's view (Grader's View task) reads them from the transcript's attachment
  records, not from the folder.
- **A run lays the skill's copy and its hook files out as an install does**:
  `skills/<name>/` and `hooks/<folder>/` side by side, so that a hook that finds its
  skill's scripts from its own place finds them. Every later change to a run's layout
  keeps that correspondence.
- **A session's duration is its wall time, as `harness.start` measures it, in every
  session the scripts start**: a run in both arms, a grading, a trigger session, a
  tuning proposal; the result's `duration_ms` kept beside as `reported_duration_s`. Both
  arms measured alike, the benchmark's duration delta compares like with like.
- **A note on a run's model or effort reads the session's own calls**; an agent's model
  and effort are the skill's to set, shown beside them. Phase 2's notes on a run keep
  that split.
- **A change to `authoring-skills`' text is written after its cases ran on the previous
  version, and only for what they showed missing** (the user, on tasks 2 and 4): the
  design names what to look at, the runs decide what is written.
- **Whatever the grader's view cuts is written whole beside it, and the cut names the
  file**: `context/` for what a session was given, `whole/` for what its rendering cuts,
  each with an agent's sub-folder. A later change that shortens anything in the view
  keeps that rule.
- **A later step's case looks for a recorded run of the earlier step before writing its
  state by hand** (the user, on iterations 12 and 13): the third wording of the
  later-step bullet, the two before it read as leave to write by hand without looking.
- **Until the auditor's verdict is reproducible, a FAIL's points at a phase's close go to
  the phase that settles them** (the user, on the split verdict of 2026-10-15): the FAIL
  never counts as a PASS, and `authoring-skills`' two PASS stay required at Phase 4.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/skill-validation/phase-1-run-world-report.md`

**Modified**
- `docs/claude-code-coupling.md`
- `docs/roadmap/README.md`
- `docs/roadmap/on-progress/skill-validation/README.md`
- `docs/roadmap/on-progress/skill-validation/phase-1-run-world.md`
- `docs/roadmap/on-progress/skill-validation/phase-2-judgments.md`
- `docs/roadmap/on-progress/skill-validation/phase-3-evidence-and-sources.md`
- `docs/roadmap/on-progress/skill-validation/phase-4-validation-and-release.md`
- `domains/skill-tooling/CHANGELOG.md`
- `domains/skill-tooling/agents/skill-grader.md`
- `domains/skill-tooling/skills/authoring-skills/evals/evals.json`
- `domains/skill-tooling/skills/authoring-skills/evals/fixtures.py`
- `domains/skill-tooling/skills/authoring-skills/evals/test_fixtures.py`
- `domains/skill-tooling/skills/authoring-skills/references/eval-files.md`
- `domains/skill-tooling/skills/authoring-skills/references/evaluate.md`
- `domains/skill-tooling/skills/authoring-skills/scripts/benchmark.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/grade.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/harness.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/run.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/triggers.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/tuning.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/workspace.py`
- `domains/skill-tooling/tests/test_benchmark.py`
- `domains/skill-tooling/tests/test_grade.py`
- `domains/skill-tooling/tests/test_run.py`
- `domains/skill-tooling/tests/test_workspace.py`

---

## Problems And Deviations

- **The design's "installed in the run's folder as project hooks" done otherwise.** The
  hooks go through `--settings`, since a fixture repository would list a merged settings
  file among the run's changes; the probes show the same start for the session. The
  design's intent, the domain's real hooks run for real in each arm, stands.
- **A run's copy of the skill moved from `skill/<name>/` to `skills/<name>/`.** Not in the
  design: found when a domain hook's way of finding its skill met the run's layout. The
  prompt names the copy by its path, so nothing reads the old one.
- **The grader's view still cuts long texts.** `render` shortens each text and result
  past 2,000 characters, so an agent's closing answer, the one its caller relies on, is
  cut; the regrade of ai-ctl's run could not check one range for that. Added to this
  phase as a task of its own, under Grader's View, on the user's yes.
- **The wall duration taken from the session's own start and end, not from `run.json`'s
  `started` and `ended`** as the design says: those two also hold the run's folder being
  built and its outputs collected. The design's intent, a duration with the time spent
  waiting on agents, stands.
- **The figures task done a little beyond its wording**: the model note, which read an
  agent's model as a deviation as the effort note read its effort, follows the same
  rule; and the change reaches the grading, trigger and tuning sessions, which share
  `harness.figures`.
- **The whole-texts task done beyond its wording, calls' inputs kept whole too**: on
  2.1.296 an agent's closing answer is the input of its `SubagentHandback` call, so the
  task's first aim needed it.
- **Task 1's `workspace.py` broke on a nested hooks file at a revision baseline**, found
  by iteration 8's runs, every one of case 7's three; fixed with its test. Its runs are
  started again on the fixed tool.
- **Task 2 first ticked without text on a misread, then reopened.** The previous version
  provides the skill's hook in six runs in six, through the `hooks` key task 1 added; the
  reading before grading took that for the whole check, and a case without an open note
  on its subject for one without any. The grading showed the other half missing: each
  case's start declared in its expected output in one run in six. Unticked, and The
  Cases gained one bullet for that half alone, not the design's whole check.
- **Task 4 by one sentence, not the design's paragraph**: the previous version already
  tests a later step from a fixture holding the state before it, four runs in four; only
  the state's source, a recorded run's outputs, was missing, none in four.
- **Task 4's sentence reworded, and not settled at this session's end.** "When one
  exists" led one run in three of the hooked case to wait for a recording; the clause
  added for that case, "with no run of that step recorded yet", led two runs in three of
  the later-step case to write the state by hand beside a recorded run, on a reading not
  yet graded. Left for the next session.
- **Task 4 settled on a third wording**, the recorded run looked for first: three runs in
  three take it on iteration 15, as on iteration 10, and task 2 holds on iteration 14.
  The search costs: +$0.128 and +51 s a run against the previous version on the
  later-step case, +$0.079 and +42 s on the hooked case.
- **`authoring-skills`' audit not passed at the closure**: two passes, PASS and FAIL on
  one text and request, none of the FAIL's six points on this phase's text, four of them
  on a line past the end of their file. On the user's choice, not counted as a PASS; its
  points moved: the split verdict to Phase 2's Auditor task as evidence, the two
  sources and the prohibition of the shared `conventions.md` to Phase 3, the baseline's
  copy, the old block's removal and the words eval, case and query to Phase 4's audit.
- **Each reused run's `grading.json` copied by hand**, in iterations 9, 12, 13, 14 and 15,
  after checking its transcript, `run.json` and case unchanged: `workspace.py --reuse`
  carries `grader/` but not the grading. Left open: the README puts `--reuse`'s defects,
  V7, out of this roadmap's scope.

---

## Changes To Later Phases

- `phase-2-judgments.md`, Dependencies: the two `skill-auditor` passes of 2026-10-15,
  PASS and FAIL, four of the FAIL's lines past their file's end, named as evidence for
  the Auditor task.
- `phase-3-evidence-and-sources.md`, Dependencies: the FAIL's three points this phase's
  rules decide — the sources of `references/discipline.md`'s three pressures and of
  `references/create-and-edit.md`'s five samples, the prohibition of the shared
  `references/conventions.md` that no failure grounds.
- `phase-4-validation-and-release.md`, Dependencies: the FAIL's three other points, left
  to the Authoring-Skills task's audit — the previous version copied before an edit, the
  old block's removal offered with no edit nor check, the words eval, case and query.
- No restructuring: nothing pending approval.

---

## Assessment

The phase delivered what its objective asked: a case runs in the world the skill meets
once installed, its domain's hooks given through `--settings` and laid out as an install
lays them; the grader reads each session's starting context and, whole, whatever the
view cuts; a workflow's later step is evaluated from a fixture holding a recorded run's
state; a run with agents reports its wall time and marks each agent's estimated or
settled figures. Every script change went test-first, and three probes on 2.1.296 settled
the ties to Claude Code before the code relied on them.

What took the phase longest was its two text tasks, not its scripts: four wordings and
eight iterations (8 to 15) for two sentences of `references/evaluate.md`. Each wording
was read one way by some runs and another by others, and two decisions taken on a
reading before the grading (task 2 ticked on six runs, then the clause "with no run of
that step recorded yet") were undone by the grading. Iteration 8 also found a defect of
task 1's own code, which its tests had missed.

What Phase 2 needs first: the split verdict of the closing audit, PASS and FAIL on one
text and request, four of the FAIL's lines past their file's end — the reproducibility
its Auditor task answers; and the lesson of the text tasks for its Failures tasks: a run
read before grading is no class, the grading decides.
