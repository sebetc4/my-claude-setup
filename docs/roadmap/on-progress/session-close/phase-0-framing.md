# Phase 0: Framing

---

## Status

**Current Status:** 🟢 Done (100% — 5/5)
**Started:** 2026-10-13
**Completed:** 2026-10-13
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, before any code, what `close-session` does at each kind of session end, from the
requests the user typed and what the agent did after each: where its records go, the
resume note and its folder, the line the next session starts with, and what it leaves to
the roadmap skill and to roadmap `roadmap-execution`.

---

## Overview

### Why This Phase Matters
The requests vary in their words and in what followed them: a report entry, a memory
file, a note in a folder made up for it, a commit or none. A skill written from one
session's habit would serve one kind of session end.

### What It Enables
Phase 1 builds a design the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Design

Approved by the user on 2026-10-13, with four answers the report records: no commit while
a step is unfinished; no decision record at the close; the agent's memory for preferences
and rules only; the notes in a subfolder of `notes/`, not versioned. It rests on the 69
requests to close a
session that `study/session-close/kinds.md` sorts, cited by their number in
`close-requests.md`, and on the list of what this setup already asks,
`study/session-close/existing.md`, cited as E1 to E9. One rule comes first: the close runs
when the user is leaving, often near the plan's usage limit, which cut requests 54 and 68;
it asks nothing it can record instead, reads little, and writes the resume point first.

### Name And Trigger

- **`close-session`**, verb first as the writing guide asks; no built-in skill or command
  takes it, the nearest being the commands `recap`, `resume`, `compact` and `clear`
  (`docs/claude-code-builtins.md`). Compacting a session stays out of scope.
- **Called by `/close-session [where the next session starts]`** and by the user's words.
  The argument, free text, opens the resume point verbatim, as the user gave it in 63, 79,
  88, 97 and 105 ("par le téléchargement de l'image", "pour la vérification des clients").
- **Its description** names the words of the 69 requests: record the session ("consigne
  la session", "tout consigner"), resume in a new session ("nouvelle session", "session
  fresh", "session neuve", "nouvelle discussion"), "fin de session", "clôturer la session".
  It excludes the near misses of `kinds.md`: a phase or a roadmap to close with the session
  going on (3, 4, 9, 16, 17, 85), which is the roadmap skill's; a fact, a rule or a
  direction to record mid-session (6, 12, 35, 49, 58, 76, 84, 96); the word `consignes`.
  "Clôturer" alone is ambiguous (51, then 52: "non cloturer la session je voulais dire"):
  with every task of the open phase ticked and no word of a new session, it is the phase's.
- **Trigger evals, Phase 1:** the close requests and near misses of `close-requests.md`,
  split into training and held-out queries by `triggers.py`; the held-out close requests
  trigger at a rate of 0.9 or more, the near misses at 0.1 or less.

### The Procedure By Kind Of End

| Kind (`kinds.md`) | Where the records go | Then |
|---|---|---|
| A roadmap step finished (30) | One entry in the open phase's report, per `report.md` (E1) | Commit the step's work and the entry |
| A step stopped midway (19) | The same entry, with the state of what is pending: runs started, a task half done, what is uncommitted | No commit: the entry and the work wait for the step's end, as the resume point says |
| Every task of the open phase ticked (9) | Hand over to the roadmap skill's `close-phase.md` (E2) when the user's words ask for the closure (19, 102); otherwise say every task is ticked and propose it. Never close a phase on its own (51) | The closure's commit; then record only what the closure did not |
| A roadmap or a study created (4) | Its own files hold the work; anything they do not goes to a resume note | Commit per the repository |
| Outside any roadmap, a study, a discussion (7) | A resume note in the `[session]` table's folder | Commit if the folder is tracked |

The work belongs where its subject lives: a session on a phase of roadmap `x` records in
that phase's report even when another phase is open too, as with `token-usage` and
`session-close` today; a session whose work fits no open phase, as the 2026-10-13 session
that created this roadmap, writes a resume note rather than an entry in an unrelated
report. A user who will not answer (22, 23, 33: "n'attend pas de retour de moi") gets no
question: the close waits for the work running to end, then records, and every question
goes into the resume point, to be put at the next opening (77: "les questions devront y
être posées à l'ouverture").

### What Goes Where

- **Only what is not recorded yet** (104: "qui ne l'ont pas été"): before writing, the
  close reads the report's last Work Log entry and the previous resume point, not the
  whole report.
- **The phase report or the resume note** holds what the session did, decided and
  observed, dead ends included, and the resume point.
- **The resume point** is the entry's last block, `**Where the next session starts:**`, as
  the sessions wrote it 38 times since 2026-10-05 (E3): a numbered list of what the next
  session does first, the argument's words opening it, then the questions still put to
  the user, then what is pending — runs, uncommitted files, a download (88). It is what the
  user pasted into the next session 14 times (`kinds.md`); written there, nothing needs
  pasting.
- **The agent's memory** receives only a preference or a rule the user gave in the session
  and no memory holds yet (96: commit once a step is recorded); never the session's state,
  which every later session would load (66 and 41 put a study's state there), and which an
  agent of another provider, with another memory or none, could not read.
- **A decision record** is not written at the close: a lasting decision the session took
  goes into the report or the note, and the resume point lists the record to write. No
  close in the 69 wrote one; they came at a step (34) or at a roadmap's end (85).

### The `[session]` Table

```toml
[session]
notes = "notes/sessions"
```

`notes`, the folder of the resume notes, relative to the repository's root, read through a
copy of `shared/conventions/`; `language` comes from the shared keys, as for `[roadmap]`.
A close inside a roadmap needs no table. Outside one, a missing table makes the close
propose a folder of the notes' own: a subfolder when the repository keeps a notes folder
for other kinds of notes, so that they do not mix — `notes/sessions/` here, where `notes/`
also takes the notes another repository sends for a change —, else `notes/sessions/`.
The folder is not meant to be versioned, and the close says whether git ignores it; it
writes the table once the user agrees, then the note. In a run without a user, it writes
nothing outside a roadmap and says so.

### The Resume Note

`<notes>/YYYY-MM-DD-<slug>.md`, headings in English, prose in the table's language:

```markdown
# <Subject>

**Date:** 2026-10-13
**Taken up:** —

## Where The Next Session Starts
## Done
## Decided
## Observed
## Questions For The User
## Files
```

**Taken up** stays `—` until a later close continues the work: that close writes its own
note, then sets the old one's `**Taken up:**` to its date and the new note's name, or to
its date and `finished` when the work is done. A session cut before its close leaves the
old note open, which still says where to start.

### The SessionStart Line

A hook of the domain, `resume_note.py`, reads the `[session]` table and names each note
not taken up, latest first, three at most, one line each:

> Resume note notes/sessions/2026-10-13-open-design-runtimes.md (2026-10-13), not taken
> up: <the first item of its resume point>. If the request continues that work, read the
> note before working; otherwise, ignore this line.

Nothing when the table is missing, its folder empty, or every note taken up. Inside a
roadmap, the roadmap's `session_resume.py` (E7) keeps naming the open phase; this hook adds
nothing there.

### The Commit

Until roadmap `roadmap-execution`'s `[git]` table has its `commit` key (E4):

- Under the shared `versioning = "git"`, the close commits once a step is finished and
  recorded, unless the user said not to; a session that stops a step midway commits
  nothing, and its resume point says what waits uncommitted (the user, 2026-10-12, 96, and
  2026-10-13). It stages by path only the files the session wrote, since
  the working tree may hold files left uncommitted on purpose (26: "l'aide d'audit.py, qui
  reste non commitée exprès"; 55, a phase's opening kept for its own commit), and leaves
  out a file holding unfinished work, which the resume point names. The message follows the repository's own
  form: its instruction file's rule, else its last commits' (`(docs) …` here, `docs: …`
  in ai-ctl).
- Under `versioning = "none"`, or outside a git repository, no commit is made or promised.

### Cost And Order

The close reads the report's last entry, `git status --short` and `git diff --stat`, and
nothing it already holds in its context; no subagent. It writes in this order, so that a
session cut midway loses the least: the report entry or the note, resume point included,
in one write; the memory; the old note marked taken up; the commit; the answer.

### The Answer

A few lines, since the user checks the close (48, 55, 101: "tout est consigné ?"): what
was recorded and where, the commit, what stays uncommitted and why, and how to resume —
"nous pouvons reprendre la phase 2", or nothing to type when the SessionStart line will
name the note.

### Left To Others

- **The roadmap skill:** closing a phase or a roadmap (E2), the report's format (E1), and
  how an open phase is resumed (E8).
- **Roadmap `roadmap-execution`** (E9): when a phase hands over to a new session — the
  user's judgment, as no hook watches the plan's usage or the context (see Decisions in
  the report) —, whether a resuming session reads the whole report or the resume point
  this close writes last, and the `[git]` table's `commit` key, which replaces the rule
  above.

---

## Tasks

### Inputs
- [x] Save the requests to close a session from every project's transcripts into `study/session-close/close-requests.md`, each with its date, its repository, its words, the context's size when it was typed, and what the agent then wrote, committed and answered, before the oldest transcripts pass Claude Code's 30 days
  Proof: check — the search's pattern and date at the file's head, and the 67 messages that `consign|clôtur|fin de session|nouvelle session|session fresh|prochaine session` found on 2026-10-13 found again
- [x] Sort the requests into kinds of session end — a roadmap step finished, a step stopped midway, a phase finished, outside any roadmap, a study — with, for each, where the records went, whether a commit followed, what the next session read first, and the context's size at the request
  Proof: review — the table, each row tied to a request of the file, approved by the user
- [x] List what this setup already asks at a session's end and at the next start: the roadmap skill's `references/report.md`, `session_resume.py`, the "Where the next session starts" blocks of roadmap `token-usage`'s reports, the Stop hook of the review domain, roadmap `roadmap-execution`'s Phase 0 hand-over task and `[git]` table, the agent's memory
  Proof: review — the list, each item tied to a file and a line, approved by the user

### Design
- [x] Write the design and get the user's approval: the skill's name, checked against `docs/claude-code-builtins.md`; its procedure for each kind of session end; what goes to the phase report, to a resume note, to `docs/decisions/` and to the agent's memory; the `[session]` table of `.agent-conventions.toml` — the notes' folder — and what the skill proposes when the table is missing; the resume note's format and when the next session counts it taken up; the SessionStart line; the commit, until the `[git]` table's `commit` key exists; what the close reads and writes, at a cost that leaves it room under the plan's usage limit, and in what order — the records first, the commit last — so that a session cut by the limit loses the least; its trigger, and the argument naming where the next session starts
  Proof: review — the design, each part tied to the sorted requests, approved by the user before any code
- [x] Write the decision record under `docs/decisions/` — with the decision that no hook watches the plan's usage or the context, session management staying the user's judgment, and when to revisit it —, and carry into roadmap `roadmap-execution`'s Phase 0 what it settles for that roadmap's hand-over task, with a changelog entry there
  Proof: review — the record and the change to `roadmap-execution`, approved by the user with its date

---

## Technical Details

### Files to Modify
```
study/session-close/close-requests.md            new, ignored by git
docs/decisions/<date>-session-close.md           new
docs/roadmap/pending/roadmap-execution/          its Phase 0 and README changelog
```

### Dependencies
None to start.

### Constraints
No domain changes in this phase. The transcripts are read in place under
`~/.claude/projects/`; the user's words are copied only into `study/`, which git ignores,
since most requests come from other repositories. Claude Code deletes a transcript after
30 days: the oldest request found on 2026-10-13 dates from 2026-09-10. A request's
context size is the last call's before it, read with roadmap `token-usage`'s reader,
`shared/usage/`.

---

## Acceptance Criteria

- [x] The requests are saved before their transcripts are deleted
- [x] The design is approved by the user
- [x] The decision record is committed
