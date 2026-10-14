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
for the Grader's View task.

---

## Decisions

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
