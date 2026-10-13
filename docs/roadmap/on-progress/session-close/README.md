# Roadmap: session-close

---

## Status Indicators

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Done
- ⏸️ Blocked
- ⚠️ Needs Review

---

## Overall Progress

```
Phase 0  Framing                    🟢 ████████████████████ 100%  (5/5)
Phase 1  Skill And Hooks            🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 2  Adoption And Release       🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  ███████░░░░░░░░░░░░░  36%  (5/14)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** Phase 1 — Skill And Hooks

---

## Why This Roadmap Exists

At the end of nearly every session, the user types the same request by hand: record what
the session did, decided and observed that is not recorded yet, often commit, and resume
in a fresh session, sometimes naming where it starts. From 2026-10-05 to 2026-10-13, 63
such requests came in six repositories — this one, ai-ctl, open-work-projects,
rust-projects/ai-ctl, open-design and cowork —, often at 89 to 93% of the plan's
five-hour usage window, the user watching the figure to leave room for the close.

Inside a roadmap, the records go into the phase report, where this repository's sessions
grew a "Where the next session starts" block of their own, and `session_resume.py` names
the open phase at the next start. Outside one, each session chose its own place —
`study/hermes-openclaw/_notes-reprise.md` in open-work-projects,
`session/note-ouverte-runtimes.md` in open-design, the agent's memory — and nothing reads
it back at the next start.

This roadmap writes the skill `close-session`, called by `/close-session` with where the
next session starts, or by the user's usual words. It:
- records what the session did, decided and observed that is not recorded yet, each
  where it belongs: the phase report inside a roadmap, a resume note in a folder the
  repository declares outside one, a decision record, the agent's memory;
- proposes closing the phase through the roadmap skill when every task is ticked;
- commits the session's changes;
- says where the next session starts, which a SessionStart hook names at that start.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-13:
- A skill `close-session`, in a new domain `session`; the name is checked in Phase 0
  against `docs/claude-code-builtins.md`, where `recap` and `resume` are built-in
  commands.
- It is called by `/close-session` and by the user's own words; its trigger evals are
  written from the requests found in the transcripts.
- It serves three ends of session: after a roadmap step, at a phase's end, outside any
  roadmap.
- Outside a roadmap, it writes a dated resume note in a folder each repository declares
  in `.agent-conventions.toml`, and a SessionStart hook names the note at the next start,
  as the roadmap hook names an open phase.
- A Stop hook suggests the close past a context threshold declared in the same table.
  Dropped on 2026-10-13: see Deliberately Out Of Scope.
- It never closes a phase without the user's word: the closure stays the roadmap skill's.
- A roadmap of its own, pending, roadmap `token-usage` staying the one in progress.

---

## Deliberately Out Of Scope

- Closing a phase or a roadmap: the roadmap skill's `close-phase.md` and
  `close-roadmap.md`, which `close-session` hands over to.
- What a session cost: roadmap `token-usage`, and roadmap `session-review`.
- The commit convention: the `[git]` table's `commit` key, roadmap `roadmap-execution`;
  `close-session` follows it once it exists.
- Pushing, of a branch or a tag.
- Compacting a session.
- A hook that warns the agent before the plan's usage limit cuts the session, or past a
  context threshold: the usage figure reaches only Claude Code's status line, for claude.ai
  Pro and Max subscribers, and 2 closes in 69 were cut by the limit from 2026-09-10 to
  2026-10-13. Session management stays the user's judgment; the subject comes back if
  sessions cut before they were recorded recur, counted from the transcripts' quota
  records, as Phase 0's decision record will say.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🟢 Done |
| 1 | [Skill And Hooks](phase-1-skill-and-hooks.md) | 4 | 🔴 Not Started |
| 2 | [Adoption And Release](phase-2-adoption-and-release.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `roadmap-execution`: its Phase 0 hand-over task, which decides what a session
  resuming a phase reads, and its `[git]` table's `commit` key. Neither blocks this
  roadmap; Phase 0 carries its design into the first.
- Roadmap `skill-tooling`: `authoring-skills` and its eval scripts.

---

## Related Documentation

- [Claude Code built-ins](../../../claude-code-builtins.md) — the skill and command names already taken.
- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — the cost of a hand-over to a new session.

---

## Metadata

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/on-progress/session-close/`
**Version:** 1.2.0
**Created:** 2026-10-13
**Last Updated:** 2026-10-13

---

## Changelog

### 1.2.0 (2026-10-13)

- Phase 0 Framing closed. Delivered: the 112 messages matching the requests to close a
  session, saved from every project's transcripts into the ignored `study/session-close/`
  with their context, records, commits and the next session's first message; their sort,
  69 closes in six kinds and 43 others, the near misses of Phase 1's trigger evals among
  them; the list of what the setup already asks at a session's end; the design of
  `close-session`, approved, in the phase file's `## Design`; and the decision record
  `docs/decisions/2026-10-13-session-close.md`, carried into roadmap `roadmap-execution`'s
  Phase 0. Found: the figure watched at a session's end is the plan's usage, which no hook
  reads, so the Stop hook left the roadmap (1.1.0). Nothing moved. The folder moves from
  `pending/` to `on-progress/`.

### 1.1.0 (2026-10-13)

- The Stop hook that suggested the close past a context threshold is dropped, with the
  user's approval: the figure the user watches at a session's end is the plan's usage
  window, not the context, as Phase 0's first task found, and only the status line
  receives it, for claude.ai subscribers. Phase 1 loses its Stop hook task, 5 tasks to 4,
  and its dependency on roadmap `token-usage`'s `shared/usage/`; Phase 0's objective and
  design task lose the threshold. The requests since 2026-10-05 are 63, not about 45.

### 1.0.0 (2026-10-13)

- Roadmap created with three phases: Phase 0 Framing, which saves the requests to close
  a session from the transcripts and settles the design; Phase 1 Skill And Hooks, the
  domain `session`, its SessionStart and Stop hooks and the skill `close-session`; Phase
  2 Adoption And Release.
