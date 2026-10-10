# Phase 2: Overview And Hook

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/7)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-dependencies.md` and `phase-1-dependencies-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-overview-and-hook-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

`scripts/roadmaps.py` writes `<Root>/README.md`, the overview of every roadmap of a
repository — the one in progress, the ones waiting in the user's order of priority, the
completed ones by date —, the rituals keep it current, and the session hook says when an
open roadmap waits.

---

## Overview

### Why This Phase Matters
With every roadmap side by side and linked by dependencies, the order of the work is
spread over several READMEs; a `blocked/` folder was turned down for a view computed
from them. Dependencies give only a partial order: which of two roadmaps ready comes
first is the user's choice, recorded nowhere. On 2026-10-10 the user asked for the view
as a file at the root, written by a script so that it duplicates no source.

### What It Enables
The user and the agent see at once which roadmap to work on next, and `close-roadmap`
names it.

### Out of Scope
Any part of `<Root>/README.md` written by hand: the script writes it whole, from each
roadmap's README and the order the user gives.

---

## Tasks

### Overview
- [ ] Write the failing tests of `scripts/roadmaps.py <root>`, per Phase 0's design: every roadmap with its state, its phase in progress, its progress, the roadmaps it waits for, its one-line description and its completion date; `<Root>/README.md` written from them, keeping the user's order and changing it only on command; `--check` naming every disagreement, a roadmap ranked before one it waits for included
- [ ] Implement `scripts/roadmaps.py` and cite it from `SKILL.md`

### Rituals
- [ ] Add the one-line description under the title of `assets/templates/roadmap-readme.md`, and make `references/create.md` have the agent creating a roadmap write it, ask the user where the roadmap ranks, and run `scripts/roadmaps.py`
- [ ] Make `references/open-phase.md`, `references/close-phase.md` and `references/close-roadmap.md` rewrite `<Root>/README.md` with `scripts/roadmaps.py` and check it in their verification, and make `close-roadmap.md` name the next roadmap ready in the user's order
- [ ] Replace the temporary `docs/roadmap/README.md`, written by hand on 2026-10-10: each description moves under its roadmap's title, the order goes to the script, and the file is generated

### Hook
- [ ] Make `hooks/session_resume.py` name, in its line, the roadmap an open roadmap waits for — failing tests first
- [ ] Decide under the work-in-progress rule whether the hook still names a roadmap that waits, and apply the decision

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/scripts/roadmaps.py    new
domains/roadmap/skills/roadmap/evals/test_scripts.py
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/skills/roadmap/assets/templates/roadmap-readme.md
domains/roadmap/skills/roadmap/references/create.md
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/close-phase.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
domains/roadmap/hooks/session_resume.py
domains/roadmap/tests/test_hooks.py
docs/roadmap/README.md
docs/roadmap/*/*/README.md
```

### Dependencies
Phase 1's `Blocked By` form; Phase 0's design of `<Root>/README.md`.

### Constraints
Python standard library only; failing tests first. The hook stays one line per roadmap.
`<Root>/README.md` is written only by `scripts/roadmaps.py`. The link check's glob,
`<Root>/*/*/*.md`, does not reach it: a link it holds is checked too, or it names each
roadmap by its folder name, as `Blocked By` does.

---

## Acceptance Criteria

- [ ] `scripts/roadmaps.py` lists every roadmap of this repository and of scriptorium with its state and what it waits for
- [ ] This repository's `docs/roadmap/README.md` is generated, `--check` agrees with it, and no part of it but the roadmaps' descriptions was written by hand
- [ ] The session hook names the roadmap an open one waits for, in one line
