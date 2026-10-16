# Phase 2 Report: Adoption And Release

**Phase:** [phase-2-adoption-and-release.md](phase-2-adoption-and-release.md)
**Start Commit:** 9afe4d4

---

## Work Log

### 2026-10-15

Phase opened at Phase 1's closure, in the same session, after reading
`phase-1-skill-and-hooks.md` and its report in full; no restructuring was pending.

Task 1, on the user's go-ahead. `make enable D=session` under a temporary `CLAUDE_DIR`:
five files installed — the hook `hooks/session/resume_note.py`, the skill's `SKILL.md`,
its two references and `scripts/conventions.py`, no `evals/` —, the SessionStart hook
and the allow rule merged into `settings.json`. The install on `~/.claude` was refused
by Claude Code's auto mode classifier as a self-modification, and so was a read of
`.agent-conventions.toml` right after: both waited for the user.

The user authorized both. `make enable D=session` on `~/.claude`: five files, and
`make list` shows `session on 0.1.0`; `review` and `roadmap` show `outdated`, changed in
the repository since their install, among other things by the copies of
`shared/conventions/` Phase 1's task 1 refreshed: their update waits for the user. This
repository's `[session]` table holds `notes = "notes/sessions"`, the `sessions/`
subfolder of the `notes/` folder it keeps, as `references/conventions.md` says;
`language` comes from the shared key, `start_notes` is not declared. Every installed
reader accepts the file — `close-session`'s, `authoring-skills`', and the roadmap skill's
and `tool-review`'s older copies —, and the installed hook, run on this repository, says
nothing, no note existing yet. Task 1 done.

On the user's yes, `make update` of `roadmap` and `review`, 18 and 12 files: `make list`
shows every domain `on`, and both updated readers accept the `[session]` table. The user
then asked to record the session and to resume in a new one: this entry is written by
`close-session`, its first close of a real session, the one task 2 asks for.

**Where the next session starts:**
1. Task 2's proof: show the user this entry, this close's commit and the next session's
   own first answer, for their approval; read this close's answer, the last of session
   `316bc624` before its tool review, for a sentence on what the next start will or will
   not show.
2. Task 3: with the user's go-ahead in another repository, write its `[session]` table,
   close a session there outside any roadmap, and start the next one from the
   SessionStart line.
- No question is waiting for the user.
- Nothing uncommitted after this record's commit; the `[session]` table lives in the
  ignored `.agent-conventions.toml`.

Resumed in a new session from the user's "continue phase 2": the roadmap hook named the
open phase, `resume_note.py` named nothing, as no note exists inside a roadmap, and the
resume point led to task 2's proof with no other word from the user. The close's answer,
the last of session `316bc624`, says nothing of what the next start will or will not show:
the noise to monitor is absent; it gives the user the words to resume with. The resume
point's "before its tool review" was wrong, harmless: no review followed the close. The
user approved the entry, commit `89b4f67` and this session's first answer. Task 2 done;
task 3 goes to ai-ctl, on the user's word.

Task 3, in ai-ctl. Its `[session]` table was already there, `notes = "notes/sessions"`,
written at 18:02 with `/notes` in its `.gitignore` by no agent session the transcripts
hold; `close-session`'s reader accepts it. An earlier close there, session `35772463`,
was inside roadmap `review-skill`: its record went to the phase report, its answer silent
on the next start too. The user then held a discussion outside the roadmap, a GNOME Shell
extension, and closed it with `/close-session` (session `44d4439d`): the note
`notes/sessions/2026-10-15-gnome-extension.md`, every section filled, no commit since
`notes/` is ignored, and an answer giving the words to resume with, nothing on what the
next start will show. The next session, `ec84f208`, started with two lines, the note's and
the roadmap's; to the user's vague "where were we?" it read the phase file and the note,
answered on the roadmap and ended with the note's question, as a question left from the
previous session. The user approved the note, the line and that first answer. Task 3
done. The note's `**Taken up:**` stays `—` until `ec84f208` closes: checked then.

Task 5. `session` joins the `[review]` table, read at every Stop. `close-session` gets four
watch points in `domains/review/hooks/tools.json`, one per failure Phase 1 left or the
Result's condition: the answer speaking of the next start, the Result's rule told to the
user among them (iteration 11's run 1 and the condition); a decision filed under Done
(iteration 10's run 3); a phase closed without the skill loaded (request 102); the skill
loaded on a session's first message (request 78). The two observations of task 3 stay out,
each point weighing on every review; a line in `review`'s 0.3.0 changelog. `CLAUDE.md`:
`domains/session/` under Layout, `[session]` beside the other tables, `close-session`
among the copies of `shared/conventions/`. The user approved the lines; `make update
D=review` on their yes. The user saw no review asked for `close-session`: it was not
listed. The installed selection, run on `44d4439d`'s transcript without writing, now
picks `skill:close-session`, and on `ec84f208`'s `hook:session/resume_note.py`, which a
start without a note line does not count as used.

Task 6, each change to the roadmap owning its tool, as the agent proposed and the user
approved. To `lean-workflow`'s Phase 1, a From Use task: the eval scripts' cost announced
as a limit without a measured session, E1 and E2 of ai-ctl's proposal `notes/2026-10-13-run-estimate-per-case.md`,
`workspace.py --reuse` naming why it takes no run and `--extend` taking `--case`
(roadmap 1.0.2). To `token-usage`'s Phase 2 Defects: a task for U1 and U3 of the same
proposal, the output settled from `cost-state` and `usage.py --session`; and its
SessionStart task widened to `resume_note.py`, measured at 0 runs on `ec84f208` though
its line opened the session (roadmap 1.5.1). `lean-workflow`'s Phase 0 still decides
`token-usage`'s remaining tasks and may cut the new one.

### 2026-10-16

From `lean-workflow`'s Phase 0: U1 and U3 went to its Phase 2, the SessionStart task was
cut with `token-usage`, closed. The tool reviews gone through there bring two findings
here: for task 4, `resume_note.py` injecting a note beside an open phase's line, or after
a session that did not take it up (2×); for the release, `close-session`'s Result saying
nothing when an unrelated resume note is named at the start (1×).

Task 4, measured by a script over `~/.claude/projects/`. A SessionStart hook's output is
recorded only when it prints, so starts without a line are counted from the sessions' first
records. Since the install, 2026-10-15 15:55 UTC, 17 starts in the two repositories with a
`[session]` table: 7 here, where no note was ever written, every session being inside a
roadmap; 10 in ai-ctl, the first 4 before its first note, 6 with a line.

| Note | Named | Read | Not read |
|---|---|---|---|
| `2026-10-15-gnome-extension.md` | 6 | 2 | 4 |
| `2026-10-16-v2-review-gpu-pass.md` | 1 | 1 | 0 |
| `2026-10-16-v2-review-pass-5-done.md` | 1 | 1 | 0 |

Starts reading none of the notes named: 2 of 6 (`d93c8ff9`, `10bbfffc`), both resuming
roadmap `review-skill`. Neither threshold is crossed. `gnome-extension` reaches five unread
starts at ai-ctl's next one: read at `ec84f208` (and `a2d577c1`, a duplicate start
interrupted at once) on a vague "where were we?", its question to the user never answered,
its subject never worked on. `pass-5-done` is taken up by `5546bb5d`, still running, which
carries its work into `review-skill`'s Phase 5: `close-session` marks a note only outside
a roadmap (step 5, `references/resume-note.md` Taken Up), so that close will leave it
open, named at every start beside the phase's line, the noise both reviews describe.

The user placed the defect upstream: `close-session` is not meant to write a note for a
roadmap's work. Both `v2-review` notes were written between `review-skill`'s Phases 4 and
5: `10bbfffc` closed Phase 4 (`ef05b42`), then planned pass 5, and its close answered
"Aucune phase n'est ouverte : la phase 4 est close" before writing `gpu-pass`;
`2cd24729` ran pass 5 and wrote `pass-5-done`. Both followed step 1's "work that fits no
open phase", from Phase 0's design. Fixed from use, on the user's "both": step 1 gives a
roadmap with no phase open, a roadmap just created included, no resume note, the close
proposing the phase the work belongs to and recording in its report once opened on the
user's word; the roadmap skill's side, asking for that phase before the work starts, goes
to `lean-workflow`'s Phase 2 as a Roadmap task (roadmap 1.2.1). With it, the Result's fix
from `d93c8ff9`'s review: the resume words left out only when the record is a resume note
and a line names open notes. `audit.py` clean. The user found a rule in the hook appealing
but premature, one note observed; `gnome-extension` closed by hand in ai-ctl on their
word, `**Taken up:** 2026-10-16, dropped`; `pass-5-done` too, its work carried on in
`review-skill`'s Phase 5 report. The user approved the figures and the diff. Task 4 done.

---

## Decisions

- **No resume note for a roadmap's work.** Between two phases or on a roadmap just created,
  the close proposes the phase the work belongs to and records in its report once opened;
  a note holds only work outside any roadmap. Reverses Phase 0's design on "work that fits
  no open phase"; the roadmap skill asks for that phase upstream, in `lean-workflow`'s
  Phase 2.
- **No rule in `resume_note.py` yet.** Neither threshold crossed on 6 starts; a cap on
  unread starts waits for more than one note observed.

---

## Files Changed

---

## Problems And Deviations

- **A resume point's item read alone at the start.** The note's first item ends "from the
  Observed section below", which the start line quotes out of the note; harmless, the line
  asking to read the note. Left open, to watch.
- **`conventions.py` run from the skill's folder.** `44d4439d`'s close ran it first from
  `~/.claude/skills/close-session`, then again from the repository: one wasted call. Left
  open, to watch.

---

## Changes To Later Phases

---

## Assessment
