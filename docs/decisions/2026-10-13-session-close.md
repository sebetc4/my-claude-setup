# Session Close — 2026-10-13

Decided with the user on 2026-10-13, in Phase 0 of roadmap `session-close`: **a skill
`close-session` records, at the end of a session, what the session did, decided and
observed that is not recorded yet, and where the next session starts; outside a roadmap,
in a resume note that a SessionStart hook names at the next start. No hook decides when a
session ends: that stays the user's judgment.** This record and the design, both approved
by the user on 2026-10-13, stand together: the design is the `## Design` section of
[the phase file](../roadmap/on-progress/session-close/phase-0-framing.md); this record keeps
what it decided, the figures it rests on, and when to revisit it.

## Decisions

- **One skill, in a new domain `session`.** `close-session`, called by
  `/close-session [where the next session starts]` and by the user's own words; the
  argument opens the resume point verbatim. It never closes a phase or a roadmap on its
  own: with the user's word, it hands over to the roadmap skill's `close-phase.md`.
- **The records go where their subject lives.** Inside a roadmap, one entry in the phase
  report the session worked on; outside one, a resume note. The entry or the note holds
  only what is not recorded yet, and ends with the resume point, `**Where the next session
  starts:**`: what the next session does first, the questions to put to the user, and what
  is pending.
- **The agent's memory takes only preferences and rules the user gave**, never a
  session's state, so that the records serve an agent of another provider, whose memory
  differs or is missing.
- **No decision record at the close.** A lasting decision goes into the entry or the note,
  and the resume point lists the record to write.
- **Resume notes stay out of version control**, in a folder the `[session]` table of
  `.agent-conventions.toml` declares (`notes`), a subfolder when the repository's notes
  folder holds other kinds of notes: `notes/sessions/` in this repository. A note counts as
  taken up when a later close continues its work and marks it; the hook `resume_note.py`
  names the notes not taken up, three at most.
- **A commit only when a step is finished and recorded**, staging by path the files the
  session wrote; a session that stops a step midway commits nothing, and its resume point
  says what waits. The repository's own message form applies until roadmap
  `roadmap-execution`'s `[git]` table has its `commit` key.
- **The close is cheap and ordered**: it reads the report's last entry and the git status,
  writes the entry or the note in one write, resume point included, and commits last, so
  that a session cut by the plan's usage limit loses the least.
- **No hook watches the plan's usage or the context.** The figure the user watches at a
  session's end is the plan's usage window, which only Claude Code's status line receives;
  bridging it to a hook would tie the domain to one provider, for few sessions cut. VS Code
  already shows the user the usage alerts.

## Figures

From every project's transcripts, searched on 2026-10-13 by a study script kept in the
ignored `study/session-close/`:

- **112 messages** matched `consign|clotur|clôtur|fin de (la )?session|nouvelle
  session|session fresh|prochaine session`, from 2026-09-10 to 2026-10-13; **69 are
  requests to close a session**, 63 of them since 2026-10-05, in six repositories.
- **The kinds of end:** 30 after a roadmap step finished, 19 with a step stopped midway, 9
  at a phase's or a roadmap's end, 4 after creating a roadmap, 5 in a study, 2 outside any
  roadmap or study. The other 43: 11 next-session starts, 6 phase closures with the session
  going on, 8 facts to record mid-session, 18 sharing a word only.
- **A commit followed** 28 closes in 30 after a finished step, 9 in 19 after a step
  stopped midway; in a study, never.
- **The context at a request:** 80,606 to 885,859 tokens, median 239,731. The percentages
  the user typed are the plan's five-hour usage: "92%" came at 290,985 tokens of context,
  "89% de la session" at 89,650.
- **The previous session's last answer was pasted** into the next one 14 times, from
  2026-10-05 to 2026-10-12, though `session_resume.py` names the open phase since
  2026-09-17. The reports of `skill-tooling` and `token-usage` hold 38 resume blocks
  since 2026-10-05, a habit the roadmap skill does not ask for.
- **2 closes were cut by the plan's limit**, request 54 by the five-hour window and 68 by
  the weekly one; 118 rate-limit records sit in 60 transcripts.
- **Where the usage figure is:** the status line receives `rate_limits.five_hour` and
  `rate_limits.seven_day`, each with `used_percentage` and `resets_at`, for claude.ai Pro
  and Max subscribers after a session's first response; no hook input carries it; a
  transcript records the quota only once it is hit (`quotaLimits`, status `rejected`)
  (code.claude.com/docs/en/statusline and /hooks, read on 2026-10-13).

## What It Changes

- **Roadmap `roadmap-execution`, Phase 0:** its hand-over task learns that the user ends
  sessions by watching the plan's usage, which no hook reads, and that `close-session`
  writes a resume point as the last block of a report entry, which a resuming session may
  read in place of the whole report. Its `[git]` table's `commit` key will replace the
  close's commit rule.
- **The roadmap skill:** nothing. `report.md` asks for the report to be written before the
  end of a session; `close-session` is how it is done.
- **`docs/claude-code-coupling.md`:** Phase 1 adds the SessionStart event, the
  `/close-session` command and the memory folder.

## When To Revisit

- **When sessions cut by the plan's limit before they were recorded recur:** a rate-limit
  record (`quotaLimits`, status `rejected`) in a working session whose work since its last
  close was not recorded; 2 in 69 closes from 2026-09-10 to 2026-10-13. Past three in a
  month, a hook warning the agent comes back, the status line bridging the figure first.
- **When a hook input carries the plan's usage:** the bridge is no longer needed, and the
  warning costs one hook.
- **When roadmap `roadmap-execution`'s `[git]` table has its `commit` key:** the close
  follows it.
- **When another agent runs this setup:** the SessionStart event, the command and the
  memory folder each need that agent's equivalent.
