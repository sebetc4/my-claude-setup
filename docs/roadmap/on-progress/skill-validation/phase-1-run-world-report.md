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

---

## Changes To Later Phases

---

## Assessment
