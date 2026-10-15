# Phase 2: Adoption And Release

---

## Status

**Current Status:** 🟡 In Progress (29% — 2/7)
**Started:** 2026-10-15
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-skill-and-hooks.md` and `phase-1-skill-and-hooks-report.md` in full
before touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-adoption-and-release-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Install the domain `session`, close real sessions with it inside a roadmap and outside
one, start the next sessions from what it recorded, and release it.

---

## Overview

### Why This Phase Matters
The evals run on fixture repositories; only a real session's end shows whether the
records let the next session start without the user's words.

### What It Enables
The user ends a session with `/close-session`, in any repository whose conventions name
the notes' folder.

### Out of Scope
Changes to the roadmap skill beyond what the design asked in Phase 0.

---

## Tasks

### Adoption
- [x] With the user's go-ahead, install the domain on `~/.claude` and write this repository's `[session]` table
  Proof: check — the install first under `CLAUDE_DIR=$(mktemp -d)`, then on `~/.claude` with the go-ahead, and `make list` showing the version installed
- [x] Close a session of a roadmap of this repository with `close-session`, and start the next one from what it recorded
  Proof: review — the report's entry, the commit and the next session's first answer, approved by the user; the close's answer read for a sentence on what the next start will or will not show, the noise Phase 1's report left to monitor
- [ ] With the user's go-ahead in another repository, write its `[session]` table, close a session outside any roadmap, and start the next one from the SessionStart line
  Proof: review — the resume note, the line at the next start and the next session's first answer, approved by the user; the close's answer read for a sentence on what the next start will or will not show, the noise Phase 1's report left to monitor
- [ ] Measure the SessionStart line's noise from the transcripts of every session started since the install in a repository with a `[session]` table: per start, the notes the line named and whether the session read each; too noisy when a note is named at five starts without being read, or when more than half the starts with a line read none of the notes it named, and then a rule proposed to the user before the release
  Proof: check — the figures, with the count of starts they rest on, approved by the user

### Release
- [ ] List `session` in this repository's `[review]` table, give `close-session` its watch points in `domains/review/hooks/tools.json` — the failures Phase 1 left, of its output cases and of its trigger queries, and the Result's condition passed on to the user —, and update `CLAUDE.md`: the domain under Layout, the `[session]` table beside the other tables of `.agent-conventions.toml`
  Proof: review — the lines changed, approved by the user
- [ ] Hand over the changes to the setup that waited for this roadmap's end, each to the roadmap that owns its tool or to a new one, as the user decides: the eval scripts' cost announcements — with no measured session of the skill, a limit, with the source of its figure, never an expected cost, as Phase 1's report says —, with ai-ctl's proposal `notes/2026-10-13-run-estimate-per-case.md`: an estimate per case and configuration, the ceiling beside it, and for roadmap `token-usage` the output estimate of `usage.py`; `workspace.py --reuse` naming why it takes no run, as it took none silently on a fixture whose digest had changed, and `workspace.py --extend` taking `--case`; and the tool review's count of 0 runs for a SessionStart hook
  Proof: review — each change and where it went, approved by the user
- [ ] Release the domain: `VERSION`, its `CHANGELOG.md` entry naming the failures Phase 1 left with their class, and its tag on `main` after the merge, with `make tags`
  Proof: check — `make check`, whose `tests/domains.py` compares `VERSION` with the changelog's first entry, then `git tag --points-at` on `main`'s merge commit naming the tag

---

## Technical Details

### Files to Modify
```
CLAUDE.md
domains/session/VERSION
domains/session/CHANGELOG.md
```

### Dependencies
Phase 1: the domain, its hooks and its skill.

### Constraints
`make enable` and `make update` touch the real `~/.claude`, and every change in another
repository is made in that repository: each waits for the user's go-ahead. Once
installed, the hooks fire in every open conversation, as `CLAUDE.md`'s Gotchas say.
`.agent-conventions.toml` is ignored by git here: the `[session]` table is written on the
machine, not committed.

---

## Acceptance Criteria

- [ ] The domain is installed and `make list` shows its version
- [ ] A session in a roadmap and a session outside one were each closed with the skill and resumed from its records
- [ ] The domain's release is tagged on `main`
