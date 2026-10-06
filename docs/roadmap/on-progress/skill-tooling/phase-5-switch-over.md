# Phase 5: Switch-Over

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/12)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-4-evaluation-tooling.md` and `phase-4-evaluation-tooling-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-5-switch-over-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Move this setup onto the new tool: prove it with its own tooling against the old tools
and the no-skill baseline, run the roadmap evals on it, audit the existing skills with
it, install it, and record the decision that replaces the 2026-09-18 one.
`superpowers:writing-skills` and the skill-creator plugin are already off: every plugin
was removed on 2026-10-04 (`docs/decisions/2026-10-04-plugins-removed.md`).

---

## Overview

### Why This Phase Matters
The old tools are gone, but nothing yet shows that the new one does their work as well.
The roadmap evals still run skill-creator's scripts from the copy under `study/`, and
the 2026-09-18 decision still says to keep skill-creator.

### What It Enables
One tool for skills in this setup, and a recorded decision in place of the 2026-09-18 one.

### Out of Scope
The other superpowers skills: roadmap `superpowers-study` ruled on them, and roadmaps
`roadmap-execution` and `working-method` build what it kept.

---

## Tasks

### Comparison With The Old Tools
- [ ] Evaluate the new skill against the no-skill baseline and against the two old tools, given to the runs from their copies under `study/skill/`, on the same skill-writing tasks, and record the benchmark
  Proof: eval — Phase 3's three skill-writing tasks run with no skill, with `writing-skills` 6.4.1, with skill-creator and with `authoring-skills`, through Phase 4's benchmark at the effort and model Phase 4 set; expected before the runs: the new skill matches or beats each old tool on every task and beats the baseline
- [ ] Run trigger evals on the queries where `writing-skills` or skill-creator should trigger, and tune the description until the new skill triggers on them
  Proof: eval — the queries run through Phase 4's trigger eval with the description before tuning, then with the tuned one, the rate per query recorded each time
- [ ] Check every row of the Phase 0 capability matrix against what was built, and record each gap as a decision
  Proof: review — each row of the Phase 0 matrix marked built, built otherwise or missing, and the decision on each gap taken by the user, with its date

### Existing Skills
- [ ] Audit `roadmap` and `tool-review` with the static audit and the `skill-auditor`, and fix or record each problem
  Proof: check — `audit.py` on `domains/roadmap/skills/roadmap` and on `domains/review/skills/tool-review` passes; then `skill-auditor` on each, as many runs as Phase 4 sets for a judgment, every problem fixed or ruled by the user
- [ ] Make `tests/check.py` audit every folder that the `[skills]` conventions name in `dirs`, `.claude/skills` included, and not only `domains/*/skills`
  Proof: test — a fixture repository whose `[skills] dirs` names `.claude/skills`, holding there a skill with an error that `tests/check.py` reports, red before the change
- [ ] Settle the problems `skill-auditor` found in Phase 3 in `shared/conventions/conventions.md`, which `authoring-skills` and `roadmap` both copy: the `residue` row restating how `.gitignore` patterns match; the section mapping an old contract, which only the roadmap skill uses; "directory" where the skills say "folder"; "the reader" for `scripts/conventions.py`; and the claim, with no source, that a `checks` command runs through the normal permission flow. Decide first whether each tool gets its own conventions reference; then refresh the copies with `make shared`, and give the roadmap domain its patch version
  Proof: review — whether each tool gets its own conventions reference, decided by the user before any edit; then `skill-auditor` on `authoring-skills` and `roadmap` reports none of the five problems over the runs Phase 4 sets for a judgment, and `make check` passes after `make shared`
- [ ] Move `domains/roadmap/skills/roadmap/evals/grade.py` from the copy of skill-creator under `study/` to the new benchmark and viewer
  Proof: check — the roadmap evals' last recorded runs graded again through the new benchmark, with the pass rates recorded before, and `grep -rn "study/skill/create-skill" domains tests tools` finding nothing

### Install And Release
- [ ] With the user's go-ahead, install the new domain with `make enable`, and remove from `.claude/settings.json` the registration of `domains/skill-tooling/hooks/audit_skill.py` that Phase 2 added until the install, or the audit hook runs twice here
  Proof: check — `make enable D=skill-tooling CLAUDE_DIR=$(mktemp -d)` first, then `make enable D=skill-tooling` with the user's go-ahead; once the registration is removed, one edit of a skill file gives one audit report, not two
- [ ] Add the new tools to `domains/review/hooks/tools.json` so that tool reviews cover them
  Proof: probe — a session that loads `authoring-skills` and starts `skill-auditor` gets the Stop hook's review request naming both, and a session that uses neither, as the control, gets none for them
- [ ] Update `CLAUDE.md`: the new domain in the layout, and the gotchas the phases revealed
  Proof: review — the lines added to Layout and Gotchas, each gotcha with the report that found it, approved by the user
- [ ] Write the decision record that replaces the 2026-09-18 decision on writing-skills and skill-creator
  Proof: review — the record, citing this phase's benchmark, trigger rates and matrix gaps, approved by the user with its date
- [ ] Release the domain: `VERSION`, its `CHANGELOG.md` entry, and the `<domain>-vX.Y.Z` tag after the merge
  Proof: check — `make check`, whose `tests/domains.py` compares `VERSION` with the changelog's first entry, then `git tag --points-at` on `main`'s merge commit naming `skill-tooling-vX.Y.Z`

---

## Technical Details

### Files to Modify
```
domains/roadmap/skills/roadmap/evals/grade.py
shared/conventions/conventions.md                     and its copies
tests/check.py
.claude/settings.json                                 the audit hook's registration removed
domains/review/hooks/tools.json
domains/<domain>/VERSION
domains/<domain>/CHANGELOG.md
CLAUDE.md
docs/decisions/<date>-skill-tooling-switch-over.md    new
```

### Dependencies
Phases 2, 3 and 4.

### Constraints
`make enable` and `make update` touch the real `~/.claude`: each waits for the user's
go-ahead. Installing the domain turns its audit hook on in every project: on 2026-10-04
it would report 85 errors in scriptorium, 55 of them on test files that a `[skills]`
table with `evals = "tests"` sets aside; before the install, the user decides whether
those repositories get the table or their fixes first.

---

## Acceptance Criteria

- [ ] The new skill matches or beats the two old tools on every benchmark task, and beats the no-skill baseline
- [ ] The new skill triggers on the queries where the old tools triggered
- [ ] `roadmap` and `tool-review` pass the static audit
- [ ] No file of this repository refers to the skill-creator plugin's directory
- [ ] A new session lists neither `superpowers:writing-skills` nor the skill-creator plugin's skill
