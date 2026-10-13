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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 1  Skill And Hooks            🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Adoption And Release       🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/15)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

At the end of nearly every session, the user types the same request by hand: record what
the session did, decided and observed that is not recorded yet, often commit, and resume
in a fresh session, sometimes naming where it starts. From 2026-10-05 to 2026-10-13,
about 45 such requests came in six repositories — this one, ai-ctl, open-work-projects,
rust-projects/ai-ctl, open-design and cowork —, often at 89 to 93% of the context, the
user watching the figure to leave room for the close.

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

A Stop hook suggests the close past a context threshold the repository declares.

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

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🔴 Not Started |
| 1 | [Skill And Hooks](phase-1-skill-and-hooks.md) | 5 | 🔴 Not Started |
| 2 | [Adoption And Release](phase-2-adoption-and-release.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `token-usage`, Phase 1: `shared/usage/`, which reads a call's tokens from a
  transcript, for the context's size at a request and in the Stop hook.
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

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/session-close/`
**Version:** 1.0.0
**Created:** 2026-10-13
**Last Updated:** 2026-10-13

---

## Changelog

### 1.0.0 (2026-10-13)

- Roadmap created with three phases: Phase 0 Framing, which saves the requests to close
  a session from the transcripts and settles the design; Phase 1 Skill And Hooks, the
  domain `session`, its SessionStart and Stop hooks and the skill `close-session`; Phase
  2 Adoption And Release.
