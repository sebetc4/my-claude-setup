# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** c56896a

---

## Work Log

### 2026-10-13

Phase opened at the user's request, as an urgent need: roadmap `token-usage` waits, its
Phase 2 still open, until this roadmap is finished; its Phase 2 report and
`docs/roadmap/README.md` say so. Read before working: the roadmap's README and its three
phase files, and the last entry of `token-usage`'s Phase 2 report, which left this
roadmap's rank and the transcripts' deadline to put to the user. `cleanupPeriodDays` is
not set in `~/.claude/settings.json`, so Claude Code's 30 days apply; the oldest
transcripts, from 2026-09-10, were still there at 33 days, and task 1 came first.

Task 1. A script, `study/session-close/close_requests.py`, reads every main transcript
under `~/.claude/projects/*/*.jsonl` and keeps the human messages (`origin.kind` `human`,
the IDE's and harness's blocks left out) that match the pattern; for each, the context's
size at the last main-thread call before it and at the turn's end, the files the agent
wrote or edited until the next human message, its commit titles, the skills it loaded, its
last answer, and the first message of the next transcript started in the same project
folder — which only the transcripts hold, and task 2 needs for what the next session read
first. It wrote `study/session-close/close-requests.md`, 112 messages from 2026-09-10 to
2026-10-13 with an index, and `close-requests.json` beside it, the same data for task 2
and Phase 1's trigger evals. A first run matched 96 messages, not 67: the earlier search,
read back in session `6719e16a`'s transcript, used a wider pattern than the one the phase
file quotes — `clotur` unaccented, which the user mostly types, and `fin de (la )?session`
— and another filter, every `user` record under 600 characters, distinct by text. With
its pattern, 112; with its filter run again, the same 67 before 08:40, 64 of them in the
file, the other 3 trigger-eval queries of 2026-09-16 in transcripts without a human origin.
Three fixes along the way: one message copied by a resumed session's transcript merged
into one entry, commit titles read from the message's first line (the first regex cut them
at an apostrophe and missed `fix(doctor):`), and only real `git commit` commands counted,
not a Python string or a grep pattern holding the words.

The context's size at the requests: 80,606 to 885,859 tokens, median 239,731, on
`claude-opus-5` and `claude-opus-5-5`. The percentages the user typed are not the
context's: "nous sommes à 92%" came at 290,985 tokens and "89% de la session" at 89,650,
and a pasted answer of 2026-10-09 reads "Utilisation de la session : vous avez vu 85 %
utilisés", the plan's usage window. The README's "often at 89 to 93% of the context" was
that window's figure.

---

## Decisions

---

## Files Changed

---

## Problems And Deviations

- **The pattern the phase file quotes is narrower than the search it cites.** The search of
  2026-10-13 used `consign|clotur|clôtur|fin de (la )?session|nouvelle session|session
  fresh|prochaine session`; the file uses that one. 3 of the 67 messages are trigger-eval
  queries, not the user's, and are left out; the head of `close-requests.md` names them.
- **The figure the user watches at a session's end is the plan's usage, not the context.**
  The README's "often at 89 to 93% of the context" and the Stop hook "past a context
  threshold" rest on a misreading: at those requests, the context held 90k to 291k tokens.
  Left open for the design, task 4: which figure the Stop hook reads — the context's size,
  the plan's usage window, or both — and whether a hook can read the second.

---

## Changes To Later Phases

---

## Assessment
