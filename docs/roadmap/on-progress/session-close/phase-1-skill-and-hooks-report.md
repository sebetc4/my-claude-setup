# Phase 1 Report: Skill And Hooks

**Phase:** [phase-1-skill-and-hooks.md](phase-1-skill-and-hooks.md)
**Start Commit:** 1d55bc7

---

## Work Log

### 2026-10-13

Phase opened at the user's request, in a new session as Phase 0's closure planned. Read
before working: the roadmap's README, `phase-0-framing.md` with its `## Design`, and
`phase-0-framing-report.md` in full. No restructuring was pending in Phase 0's
`## Changes To Later Phases`, its one entry approved and applied in version 1.1.0, and no
other phase of the roadmap was in progress. `docs/roadmap/README.md` now shows Phase 1 in
progress.

One gap between the plan and the design, raised with the user: the hook task names "the
latest resume note not yet taken up", where the approved design names each note not taken
up, latest first, three at most.

The user asked how notes could pile up when the next session takes a note up. It does not
necessarily: a note counts as taken up only when a later close continues its work, and the
next session may work on something else. Phase 0's requests show it twice: in open-design
on 2026-10-08, request 38 wrote `session/reprise-rapport-domaines.md` and the next
session, on another strand of the same study, closed an hour later with
`session/note-ouverte-runtimes.md` (41), two strands open at once; in open-work-projects on
2026-10-10, two sessions ran side by side in `hermes/repo` and `openclaw/repo` and closed
eight minutes apart (66, 67), both writing `_notes-reprise.md`. Three of the five study
closes (41, 48, 67) have no next session in the transcripts, so their notes would have
stayed open. The cap of three is the agent's, not a figure of the data, which never shows
more than two at once; it keeps a dropped note from being named forever once newer ones
exist. The user kept the design and asked to measure that the line does not bring too much
noise: the hook task now follows the design, and Phase 2 measures the noise.

Seen on the way: this session's tool review measured `session_resume.py` at 0 runs and 0
characters injected, though the transcript holds its `hook_success` record and its
`hook_additional_context`, before the session's first message. Phase 2's measure reads the
transcripts itself rather than the reviews' measured block; the cause is not looked into.

The user approved Phase 2's two thresholds, and turned down a precision the agent
proposed, that a close marks a note taken up only when the session did what the note's
resume point asked: a session that takes a note up closes it, even when the user has
changed their mind on the way forward meanwhile; otherwise such a note would never be
closed. The skill task's case outside a roadmap now starts from an earlier note.

Task 1. The `[session]` table joins `shared/conventions/`: `TOOLS` gains `session`, with
`notes`, a required path, and `language` from the shared keys, optional; `conventions.md`
gains the key and where to look for it — a `sessions/` subfolder of a notes folder the
repository keeps, else `notes/sessions`. Tests first, watched failing: three in the
module's own tests (the table resolved, no language needed, `notes` missing), four in
`domains/session/tests/test_conventions.py` through the skill's copy — the table read, no
file, a file without the table, a folder outside the root —, two in `test_permissions.py`.
Then the domain: `VERSION` 0.1.0, `CHANGELOG.md` `— unreleased`, `hooks.json` empty until
task 2, `permissions.json` allowing `skills/close-session/scripts/conventions.py` by its
path; the copy and its reference under `skills/close-session/`, ahead of the skill's
`SKILL.md`. `make shared` refreshed the copies in `roadmap`, `authoring-skills` and
`tool-review`, whose unreleased changelog entries say so. `make check` passes, 3 skills
checked, `tests/domains.py` running on the new domain. No tie to Claude Code added:
`docs/claude-code-coupling.md` already covers `domains/*/permissions.json` and the
reader's personal directory. Task 1 done.

The user asked to finish this roadmap before any other change to the setup: the defects
seen on the way, such as the review's count of SessionStart hooks above, wait for it.

Task 2. `domains/session/tests/test_hooks.py` first, 17 tests run as Claude Code runs a
hook, all red without the hook: one conditional line per open note, latest first, three at
most, notes of the same day by their last change, a note taken up left out, a file without
the `**Taken up:**` field not counted as a note, a resume point's first item joined over
its lines and cut past 200 characters, a note without a resume point still named, the
table read from a subfolder, a folder with spaces, and silence without the file, without
the table, with an invalid table, without the folder, with every note taken up, and on
invalid JSON. Then `domains/session/hooks/resume_note.py`: it finds the skill's
`scripts/conventions.py` above it, as `session_resume.py` finds the roadmap skill's, in the
repository or installed, reads `[session]`, and names the open notes; the latest is the
latest `**Date:**`, then the latest change, since a note holds no time. `hooks.json`
registers it at SessionStart under `python3 -B`, so that importing the reader leaves no
`__pycache__` in the installed skill. Tried under `make enable D=session
CLAUDE_DIR=$(mktemp -d)`: the hook, the skill's copy and the allow rule installed, the
installed hook silent on this repository, which has no `[session]` table, and naming a
fixture repository's open note. `docs/claude-code-coupling.md` names the domain's
`hooks.json` and the hook in its rows on events and stdin. `make check` passes. Task 2
done.

The user proposed two keys in `[session]`, one turning the hook on or off and one setting
how many notes it names; the agent proposed a single one, since two can contradict
(`enabled = true` with 0 notes), and the user agreed: `start_notes`, a whole number, 3 when
not declared, `0` turning the hook off while the close still writes its notes. Task 2
reopened for it, tests first, five red: in `shared/conventions/`, the key read, and
refused when negative, a boolean, a string or a float, through a new kind `count`; in the
hook's tests, `start_notes = 1` naming the latest note alone and `0` keeping the hook
silent. `make shared` refreshed the three skills' copies; the copy under
`skills/close-session/` was copied by hand, as the problem below says. The task's text and
proof name the key. `make check` passes.

The user asked to record the session and to go on in a new one. Everything above is
committed, the last commit `41eebaa`; the README's progress block still reads 0/4, as it
is recomputed at the phase's closure only.

At that close, the agent also wrote the user's request to finish this roadmap first into
its memory, as a rule the user gave; the user pointed out that the tool being built keeps
such things out of memory. The agent agreed and deleted it: the request holds until this
roadmap ends, so it is the project's state, not a rule — a memory that must be deleted at
a date is the state the design keeps out —; this report and `docs/roadmap/README.md`
already hold it; and an agent need not hold the user to their own request. The design's
"a preference or a rule the user gave" let it through: the skill needs a test, whether
it still holds once the work in progress is done; if not, it goes to the report or the
note.

**Where the next session starts:**
1. Task 3, `SKILL.md` and its references, written with the `authoring-skills` skill,
   loaded first. They build `phase-0-framing.md`'s `## Design` with this report's
   Decisions: a note is taken up by the session that takes it up, whatever it then does;
   `start_notes`; `language` optional; and the memory's test above, a request that holds
   only until the work in progress ends going to the report or the note, never to memory,
   also a near miss for the evals. The skill folder already holds the copy of
   `shared/conventions/`, `scripts/conventions.py` and `references/conventions.md`;
   once `SKILL.md` exists, check that `make check` compares the copy with its source and
   that `make shared` refreshes it (see Problems And Deviations).
2. Task 3's evals: three cases on a fixture repository, `evals/fixtures.py` — a roadmap
   step stopped midway, a phase with every task ticked, a session outside any roadmap
   that took up an earlier note on another course than its resume point said, the note
   marked taken up —, then `audit.py` and `skill-auditor`. The eval scripts start
   `claude -p` sessions only with `--start`, after announcing their count and cost to the
   user.
3. Task 4, the trigger evals: the close requests of `study/session-close/close-requests.json`
   and the near misses `kinds.md` sorts as `near-phase` and `near-fact`, through
   `triggers.py`, at the rates of the design: 0.9 or more on the held-out close requests,
   0.1 or less on the near misses.
- No question is waiting for the user. Nothing is uncommitted.
- Waiting for this roadmap's end, at the user's request: any other change to the setup,
  among them the review's count of 0 runs for `session_resume.py` seen above.

---

## Decisions

- **The SessionStart hook names each resume note not taken up, latest first, three at
  most**, as the approved design says. The user, on 2026-10-13, over naming the latest note
  only, with or without a count of the others: two strands of work can be open at once in
  one repository, and the agent then matches the request to the right note from the line.
  The cost to watch is noise, which Phase 2 measures before the release, with the two
  thresholds the user approved: a note named at five starts without being read, or more
  than half the starts with a line reading none of the notes it named.
- **A note is taken up by the session that takes it up**, whatever that session then does:
  its close sets the note's `**Taken up:**`, to its date and the new note's name, or to its
  date and `finished`. The user, on 2026-10-13, against the agent's proposal to mark it only
  when the session did what the note's resume point asked: a user who changes their mind
  on the way forward would leave the note open forever. A note the line named and the
  session did not read stays open, and a session cut before its close leaves the note it
  read open, as the design says. The skill and its eval case outside a roadmap carry it.
- **`[session]` needs `notes` only; `language` is optional.** The agent's choice, task 1:
  the design's own example table holds `notes` alone, and would be invalid in a repository
  whose file declares no shared `language`, the hook then naming nothing. Without it, the
  `# not declared` line names `language`, and the close writes the note's prose in the
  conversation's language.
- **`start_notes` sets how many notes the SessionStart line names, 3 when not declared,
  `0` turning the hook off.** The user, on 2026-10-13, who proposed a key to turn the hook
  off and one for the count; one key, on the agent's advice, so that no two values
  contradict. It is also the first lever if Phase 2's measure finds the line too noisy in
  a repository.

---

## Files Changed

---

## Problems And Deviations

- **The copy of `shared/conventions/` in `skills/close-session/` is not checked yet.**
  `tools/shared.py` finds a skill by its `SKILL.md`, which task 3 writes: until then,
  `make check` does not compare the copy with its source, and `make shared` does not
  refresh it. A change to `shared/conventions/` before task 3 is copied by hand.

---

## Changes To Later Phases

- `phase-2-adoption-and-release.md`: a task added under Adoption, at the user's request on
  2026-10-13 — measure the SessionStart line's noise from the transcripts of the sessions
  started since the install, too noisy when a note is named at five starts without being
  read, or when more than half the starts with a line read none of the notes it named; a
  rule then goes to the user before the release. 5 tasks to 6; the README's block and table
  follow.

---

## Assessment
