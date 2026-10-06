---
name: writing-notes
description: Writes meeting and decision notes in the team's format. Use when asked to write, take or record a note.
---

# Writing Notes

Write each note as `notes/YYYY-MM-DD-<slug>.md`: today's date, and a slug of three words
at most from the note's subject, lowercase, joined by hyphens.

Open the note with this frontmatter, then write the note:

```markdown
---
status: draft
---
```

Close the note with a `## Next` section: what follows from it, one line each, with who
does it when the request says; `None.` when nothing follows.
