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
folder with a draft note and a done one. `make check` passing.

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
- **Whatever the grader's view cuts is written whole beside it, and the cut names the
  file**: `context/` for what a session was given, `whole/` for what its rendering cuts,
  each with an agent's sub-folder. A later change that shortens anything in the view
  keeps that rule.

---

## Files Changed

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

---

## Changes To Later Phases

---

## Assessment
