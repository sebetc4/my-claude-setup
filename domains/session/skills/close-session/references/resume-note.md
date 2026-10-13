# The Resume Note

Outside a roadmap, the session's record is a resume note, in the folder the repository
declares.

## Its Folder

Run `scripts/conventions.py session` by its path from the skill's folder. On `ok`, the
folder is `notes`, relative to the root, and the prose is in `language`, or in the
conversation's when `language` is on the `# not declared` line.

On any other status, follow `references/conventions.md`. For `notes`, propose a folder of
the notes' own — `sessions/` under a notes folder the repository already keeps, else
`notes/sessions` — and say whether git ignores it: the folder is not meant to be
versioned. Write the table once the user agrees, then the note. When no one can answer,
write no note: give the resume point in the answer, and say the table is missing.

## Its Name And Form

`<notes>/YYYY-MM-DD-<slug>.md`, today's date and a slug of its subject. Headings in
English, prose in the folder's language:

```markdown
# SUBJECT

**Date:** YYYY-MM-DD
**Taken up:** —

## Where The Next Session Starts

1. WHAT_THE_NEXT_SESSION_DOES_FIRST
2. WHAT_FOLLOWS

## Done

## Decided

## Observed

## Questions For The User

## Files
```

Where The Next Session Starts ends with what is pending: runs, uncommitted files, a
download. Files lists the files the session wrote. A section with nothing to hold says so
in one line.

## Taken Up

`**Taken up:**` stays `—` until a later close takes the note up. A session takes up a note
when it read it and worked on its subject, whatever course the work then took. After
writing its own note, the close sets the earlier note's `**Taken up:**` to one of:

- today's date and the new note's file name, `2026-10-13, 2026-10-13-export-storage.md`,
  when the new note carries the work on;
- today's date and `finished`, `2026-10-13, finished`, when the work is done and no new
  note carries it on.

Change nothing else in the earlier note. A note the session did not read stays open.
