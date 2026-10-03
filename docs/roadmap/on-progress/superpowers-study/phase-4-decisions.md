# Phase 4: Decisions

---

## Status

**Current Status:** 🟡 In Progress (50% — 4/8)
**Started:** 2026-10-02
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-git.md` and `phase-3-git-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-decisions-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Turn the verdicts into decisions: what is kept and where it goes, the follow-up
roadmaps, and the plugin turned off everywhere.

---

## Overview

### Why This Phase Matters
Nothing gets built from a study that ends on verdicts: the follow-up roadmaps, and the
lift of the two roadmaps waiting for this one, are what make it act.

### What It Enables
The follow-up roadmaps start, and roadmaps `skill-tooling` and `roadmap-dependencies`
resume.

### Out of Scope
Building the replacements: the follow-up roadmaps.

---

## Tasks

### Recount
- [x] Recount the plugin's usage with the Phase 0 method — the 2026-10-18 recount if it is due, otherwise up to the day — and compare it with the baseline

### Plugin
- [x] Rule on `using-superpowers`, `diagnosing-superpowers` and the SessionStart hook

### Decisions
- [x] Write the decision record: the matrix, the target architecture — which domain, skill, agent, convention or roadmap-skill operation receives each kept capability — and when to revisit
- [x] Create the follow-up roadmaps in `pending/`, each with the roadmaps it waits for
- [ ] Propose the change to skill-tooling's Phase 5, which turns superpowers back on in this repository, as a restructuring for the user's approval
- [ ] Write the plan that turns the plugin off in the user's settings once the replacements exist, with its go-ahead conditions
- [ ] Clear the `Blocked By` of roadmaps `skill-tooling` and `roadmap-dependencies`
- [ ] Scope this repository's `CLAUDE.md` line "TDD (failing test first)" to the artifacts it
  fits, since Phase 2's micro-tests found that plain instruction harmful outside code

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
Phases 1 to 3.

### Constraints
Nothing is changed in the user's settings without the user's go-ahead. The recount runs
by 2026-10-18 at the latest: its window opens on 2026-09-19, and Claude Code deletes
transcripts older than 30 days. The follow-up roadmaps carry Phase 1's decisions: the
skill `shaping-work`, whose trigger overlaps neither the roadmap skill nor the skills to
come, as trigger evals check; the roadmap skill's execution operation, which runs one
phase and never chains the next; a reviewer agent run only when a phase changes code or
scripts, its value weighed by the tool reviews; an implementer agent for the delegation
a phase writes down. They also carry Phase 2's decisions: the `Proof:` line in the
roadmap skill's phase template, one proof reference read by the execution operation and
`shaping-work`, the reviewer agent's criteria from rows RQ12 to RQ18, and a debugging
skill, named here with the operation and the agents.
They also carry Phase 3's decisions: the `[git]` table — `branch`, `commit`,
`message` — read through `conventions.py` by the execution operation, `close-phase` and
`close-roadmap`; `commit = "task"` and `branch = "none"` in this repository and
scriptorium, `branch = "roadmap"` built only when a repository asks for it; this
repository's `CLAUDE.md` line on commit messages replaced once a tool reads the key; and
a git domain, named here, for the kept rows of `using-git-worktrees` and
`finishing-a-development-branch`.

---

## Acceptance Criteria

- [ ] The decision record is committed
- [ ] The follow-up roadmaps exist, and roadmaps `skill-tooling` and `roadmap-dependencies` are no longer blocked
