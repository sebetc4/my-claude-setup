# Changelog — session

## 0.1.0 — unreleased

- The domain `session`, for a session's close and the next session's start. `skills/close-session/scripts/conventions.py` and `references/conventions.md`, copied from `shared/conventions/`, read the `[session]` table of a repository's `.agent-conventions.toml`: `notes`, required, the folder of the resume notes, relative to the root; `language`, from the shared keys, optional. `permissions.json` lets the reader run by its path without a prompt.
- Hook `resume_note.py`, at SessionStart: one line per resume note of the `[session]` folder not taken up yet, latest first by its `**Date:**` then its last change, three at most — the note, its date, the first item of its resume point cut past 200 characters, and an instruction to read the note when the request continues that work. A note is a `.md` file directly in the folder with a `**Taken up:**` field, open while it holds `—`. Nothing without the table, with an invalid one, or with no open note.
