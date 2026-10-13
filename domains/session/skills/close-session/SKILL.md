---
name: close-session
description: Records at a session's end what the session did, decided and observed that is not recorded yet — in the open phase's report inside a roadmap, in a resume note outside one —, commits a finished step, and says where the next session starts. Use when the user is leaving and asks to record the session or everything, to continue or resume in a new, fresh session or discussion, says the session is ending, or types /close-session with where the next session starts, in whatever language the user writes.
---

# Close Session

The record the next session starts from, written when the user leaves, often near the
plan's usage limit: ask nothing that can be recorded instead, read little, and write the
record before anything else.

`/close-session TEXT` names where the next session starts: `TEXT` opens the resume point,
in the user's words.

## Steps

1. **Find where the record goes.**
   - Inside a roadmap — the session worked on a phase: one entry in that phase's report,
     `phase-N-<slug>-report.md` beside its phase file, even when another roadmap has a
     phase open. No resume note.
   - Outside a roadmap — a discussion, a study, work that fits no open phase, or a
     roadmap just created whose files do not hold all the session did: a resume note, by
     `references/resume-note.md`, in the folder of the repository's `[session]` table;
     `references/conventions.md` says what to do when the table is missing or invalid.
   - Every task of the phase ticked: when the user's words ask for the phase's closure,
     hand over to the roadmap skill's phase closure, then record only what it did not.
     Otherwise close nothing: say every task is ticked and propose the closure, in the
     answer and as the resume point's first item.

2. **Read only what the record needs:** the report from its last Work Log entry, or the
   note the session took up; `git status --short` and `git diff --stat`. Record only what
   neither these nor earlier records hold.

3. **Let running work end.** Wait for the runs or downloads the session started before
   writing. Ask the user nothing: each open question goes into the resume point.

4. **Write the record, in one write.** Outside a roadmap, write the note. Inside one,
   append to the report's Work Log, under today's `### YYYY-MM-DD` heading — after the
   last entry, or under it when it is already today's:
   - what the session did, decided and observed, dead ends included; for a step stopped
     midway, its state: runs started, what is half done, what is uncommitted;
   - the user's requests that bind the work still to do, such as finishing the roadmap
     before any other change;
   - last, the resume point:

     ```markdown
     **Where the next session starts:**
     1. WHAT_THE_NEXT_SESSION_DOES_FIRST
     2. WHAT_FOLLOWS
     - QUESTIONS_STILL_PUT_TO_THE_USER
     - WHAT_IS_PENDING: runs, uncommitted files, a download
     ```

   A decision that binds later work goes to the report's Decisions too, a defect found to
   Problems And Deviations. Change nothing else: the earlier entries stay as written,
   their resume points included, since the log is a record; Files Changed, the
   Assessment, the phase's ticks and status, and the roadmap's README belong to the
   phase's closure. Write no decision record: the resume point names the one to write.

   Check: the record ends with its resume point, and `git diff` shows no line removed from
   an earlier entry. If it does, restore the line.

5. **Write to the agent's memory** only a preference or a rule the user gave in the
   session, that no memory holds yet, and that still holds once the work in progress is
   done. A request that ends with the work — "finish this roadmap before any other
   change" — goes to the record. The session's state never goes there: every later
   session would load it, and an agent of another provider could not read it.

6. **Mark the note the session took up**, outside a roadmap, by
   `references/resume-note.md`, Taken Up.

7. **Commit**, in a git repository whose `.agent-conventions.toml` does not declare
   `versioning = "none"`. The close request is the user's word: commit without waiting
   for the word "commit", unless the user said not to.
   - A step finished: commit its work and its record.
   - A step stopped midway: commit nothing; the resume point names what waits
     uncommitted.
   - Outside a roadmap: commit the notes when git tracks their folder.

   Stage by path the files the session wrote, never `git add -A`, `git add .` or
   `git commit -a`: the tree may hold files left uncommitted on purpose. Leave out a file
   holding unfinished work, which the resume point names. The message takes the form the
   repository's instruction file sets, else the form of its last commits.

   Check: `git status --short` lists only the files left out on purpose. If another
   shows, commit it or name it in the answer.

## Result

A few lines, since the user checks the close: what was recorded and where; the commit, or
why none; what stays uncommitted and why; and how to resume — the words to type, such as
"we can resume phase 2", or nothing when this session's own start named open notes.
When it named none, say nothing of what the next start will show.
