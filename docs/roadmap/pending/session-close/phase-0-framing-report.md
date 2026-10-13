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

Task 2. `study/session-close/kinds.py` sorts the 112 messages by a kind given by hand to
each, from its words, its commit titles, the agent's answer and the next session's first
words, and writes `kinds.md`: a table by kind, then one row per request. 69 are requests
to close a session: 30 after a roadmap step finished, 19 with a step stopped midway, 9 at
a phase's or a roadmap's end, 4 after creating a roadmap, 5 in a study, 2 outside any
roadmap or study. The other 43: 11 next-session starts pasting the previous session's last
answer, 6 phase closures with the session going on and 8 facts to record mid-session —
the near misses of Phase 1's trigger evals —, and 18 that only share a word, `consignes`
first. Inside a roadmap, the records went to the phase report and a commit followed 28
times in 30 after a finished step, 9 in 19 after a step stopped midway; in a study, to
notes and the agent's memory, never committed. The next session named the phase or task
in most cases, but pasted the last answer 14 times from 2026-10-05 to 2026-10-12, though
`session_resume.py` names the open phase since 2026-09-17. Two requests went unanswered,
the session stopping on them, and one "cloturer" was read as the phase, the user
correcting it: "non cloturer la session je voulais dire". Awaiting the user's review.

Task 3. `study/session-close/existing.md` lists nine things this setup already asks at a
session's end and at the next start, each tied to a file and a line: the report kept
before the end of a session (`report.md:30-33`), the phase closure (`close-phase.md`),
the "Where the next session starts" blocks — a habit of the sessions since 2026-10-05,
38 of them, which the skill does not ask for —, the commit rules, the review domain's Stop
hook and its `stop_hook_active` guard, the agent's memory and open-design's own hand-over
rule (`session/journal-<date>.md` and `session/reprise-*.md`), `session_resume.py`, the
resume of an open phase that reads the whole report, and `roadmap-execution`'s hand-over
task, which asks the same three questions as this roadmap's threshold, resume note and
Stop hook. Awaiting the user's review.

The user answered the finding on the percentages: the plan's usage is the figure to watch,
so that the close runs before the limit cuts the session, leaving it unrecorded and its
cache to rebuild. The transcripts bear it out: the two requests left unanswered were cut
by the limit — request 54 by the five-hour one ("You've hit your session limit"), request
68 by the weekly one ("You've hit your weekly limit") —, and 118 rate-limit records sit in
60 transcripts. Whether a hook can read that figure: the transcripts record the quota only
once it is hit (`quotaLimits`, status `rejected`, with `rateLimitType` and `resetsAt`); no
hook input carries it, Stop's being `stop_hook_active`, `last_assistant_message`,
`background_tasks` and `session_crons` besides the common fields; only the status line
receives it, as `rate_limits.five_hour` and `rate_limits.seven_day`, each with
`used_percentage` and `resets_at`, for Pro and Max subscribers after the session's first
response (code.claude.com/docs/en/statusline and /hooks, read on 2026-10-13). No status
line is configured in `~/.claude/settings.json`, and whether the VS Code extension the
user works in runs one is not known.

The agent proposed a status line script writing the figures to a file for the Stop hook,
after a probe of the VS Code extension. The user added that VS Code already shows the
usage alerts to the user, so the hook would warn the agent, against a user's inattention,
and proposed setting the feature aside if it proved too complex, since it depends
entirely on the agent's provider. The agent agreed: the figure exists only for claude.ai
Pro and Max subscribers and only in the status line, the bridge needs a status line, a
hook and an installer setting a single `statusLine` key, none of it certain to run in VS
Code, for 2 closes cut in 69; and a warned agent could rush a close mid-task. The user
approved dropping it, with the changes to the roadmap below, and approved tasks 2 and 3
as they stand.

Task 4. The design's draft is written in the phase file's `## Design`, each part tied to
the requests of `close-requests.md` and to the list of `existing.md`: the name and the
trigger, with its near misses and the rates of Phase 1's trigger evals; the procedure by
kind of end; what goes where, the resume point being the entry's last block; the
`[session]` table, its one key `notes`; the resume note and when it counts taken up; the
SessionStart line of a hook `resume_note.py`; the commit until the `[git]` table's
`commit` key; the cost and the order of the writes; the answer; and what is left to the
roadmap skill and to roadmap `roadmap-execution`. Two claims were checked before
writing and one corrected: requests 22 and 23 came from one session, its working folder
changed, not from two sessions closing the same report, so the reason to stage files by
path became the files left uncommitted on purpose (26, 55); the reports hold 38 resume
blocks, not 39, the 39th being this report's mention. Awaiting the user's review.

The user approved the design with four answers: no commit while a step is unfinished,
where the draft committed the entry and the finished work; no decision record at the
close; the agent's memory for preferences and rules only, in view of other providers;
and the notes not versioned, as intended, but in a subfolder, `notes/sessions/` here, so
that `notes/` keeps other kinds of notes apart, such as one another repository sends for
a change. The design's header, its table of kinds, the memory, the `[session]` table and
the commit carry the answers. Task 4 done.

Task 5. The decision record, `docs/decisions/2026-10-13-session-close.md`: the decisions,
the figures of tasks 1 and 2 and of the usage probe, what it changes for roadmap
`roadmap-execution`, the roadmap skill and the coupling document, and when to revisit —
the agent proposing three sessions cut unrecorded in a month as the mark for the usage
warning. Roadmap `roadmap-execution`, version 1.2.0: its Phase 0 hand-over task now names
the user's own judgment over the plan's usage, `close-session`'s resume point as what a
resuming session may read, and this record among its figures; a changelog entry says so.
The user approved both, the threshold of three sessions cut in a month included, and
asked to close the phase and the session, Phase 1 to open in a new session. Task 5 done.

---

## Decisions

- **The figure watched at a session's end is the plan's usage, not the context's size.**
  The user, on 2026-10-13: the close must run before the limit cuts the session,
  unrecorded, its cache to rebuild. A Stop hook watching it was first meant to follow;
  the next decision drops it.
- **No hook watches the plan's usage or the context: session management stays the user's
  judgment.** The user, on 2026-10-13, on the agent's advice. The usage figure reaches only
  Claude Code's status line, for claude.ai Pro and Max subscribers; the bridge to a hook
  would tie the domain to one provider and to a status line the VS Code extension may not
  run, for 2 closes cut in 69 from 2026-09-10 to 2026-10-13; VS Code already shows the
  user the usage alerts. Two things carry into the design instead: the close writes the
  records first and commits last, so that a cut loses the least, and it stays cheap, so
  that it needs little room under the limit. Revisit when sessions cut by the limit before
  they were recorded recur, counted from the transcripts' `quotaLimits` records beside the
  close requests: the decision record, task 5, says how. Phase 1 loses its Stop hook.
- **The design of `close-session` is approved** (the phase file's `## Design`), the user's
  four answers on 2026-10-13 settling it: a session that stops a step midway commits
  nothing, its resume point saying what waits; the close writes no decision record, the
  resume point listing the one to write; the agent's memory takes only preferences and
  rules the user gave, never a session's state, so that the records serve an agent of
  another provider; the resume notes go to a subfolder of the repository's notes folder,
  `notes/sessions/` here, unversioned. Phase 1 builds this design.

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
  The user confirmed the usage window is the figure; the Stop hook was then dropped (see
  Decisions).
- **The context's size was summed by the study script, not read with `shared/usage/`**, as
  the phase file's constraint asks: the four usage fields of the last main-thread call, the
  same figure as the reader's prompt and output for one call. No consequence.

---

## Changes To Later Phases

- Approved by the user on 2026-10-13, before being written: the Stop hook dropped, per
  the second decision above.
  - `README.md`, version 1.1.0: the Stop hook leaves "Why This Roadmap Exists" and goes to
    "Deliberately Out Of Scope" with its reason and when to revisit; the decision taken at
    opening says it was dropped; the dependency on roadmap `token-usage`'s `shared/usage/`
    goes; "89 to 93% of the context" becomes the plan's usage window, and "about 45"
    requests since 2026-10-05 become 63, as task 2 counted them.
  - `phase-0-framing.md`: the objective loses the context threshold; the design task loses
    the threshold, the Stop hook and "about 90% of the context", and gains what the close
    reads and writes at a cost that leaves it room under the usage limit, records first and
    commit last; the decision record's task names the decision and when to revisit it.
  - `phase-1-skill-and-hooks.md`: the Stop hook task removed, 5 tasks to 4; the objective,
    the files, the dependencies and the constraints lose the Stop hook, the transcript's
    usage fields and `shared/usage/`.

---

## Assessment
