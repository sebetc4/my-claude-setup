# Roadmap closure ordering — 2026-09-19

Decision: **reorder `close-phase.md` so that the closure is committed before the next
phase is opened, and `## Files Changed` is computed after every file has moved.** Three
of the four audit failures observed close on their own; the fourth becomes an
instruction. Revisit after the next full roadmap closes elsewhere, or if a closure fails
its audit again on `## Files Changed`.

## What was observed

The `session-review` roadmap ran four phases to closure in `scriptorium` on 2026-09-18,
each handed to `roadmap-auditor` before being reported, as `close-phase.md` requires.

| Phase | First verdict | What the auditor reported |
|---|---|---|
| 0 | FAIL | `## Files Changed` named 3 files under their pre-move path and omitted 5 others |
| 1 | FAIL | omitted the 2 files that opening the next phase always changes |
| 2 | FAIL | listed 10 paths of 16; the recorded start commit was one phase behind |
| 3 | FAIL | omitted a file touched by a repair commit that landed inside the phase's span |
| 4 | PASS | — |

Four failures, one section. Phase 4 passed because by then the closure was being done
against rules written by hand in the roadmap's own reports, not against the ritual.

Three repair commits exist in that repository for no other reason than these failures:
`584c06f`, `c833b3a`, `76e968e`.

## Why the ritual produces this

### 1. `## Files Changed` is computed before the steps that invalidate it

`close-phase.md` step 1 finalizes the report, which per `report.md` computes
`## Files Changed` from `git diff -M --name-status <Start Commit>`. Step 3 then opens the
next phase, which **adds** two files — that phase's file is modified and its report is
created. Step 4 then moves the roadmap folder `pending/` → `on-progress/`, which
**renames every file in the list just computed**.

The ritual asks for a git-derived list and then performs two operations that make it
wrong. Phases 0 and 1 above are the two halves of this defect.

### 2. The start commit is one phase behind, by construction

`report.md` defines `{{START_COMMIT}}` as `git rev-parse --short HEAD` at the moment the
phase opens. `close-phase.md` opens the next phase at step 3 and commits at step 8. A
phase is therefore always opened **before** the closure that opened it is committed, so
`HEAD` at that instant is the commit before the closure — one phase behind.

The consequence is invisible until the audit: the diff from that commit sweeps in the
whole of the previous phase's work. Phase 2 above failed on eight paths for this single
reason, and the cause was found only on the third closure.

### 3. A repair to an earlier phase falls inside the current phase's span

`76e968e` corrected phase 2's report after phase 3's start commit had been cut, so
`git diff` from that commit reports it and check 4 of the auditor requires it listed.
This one is **not a defect**. `## Files Changed` is defined as the diff, which is what
makes it auditable at all; the alternative — "what this phase changed" — is a judgement
no agent can check. What is missing is the instruction to list such a path with its
reason, which both closures ended up inventing on the spot.

### 4. The audit runs after the commit

`## Audit` sits after step 8. Every `FAIL` therefore costs a second commit whose only
content is a correction to a report. The auditor reads `git diff` and
`git ls-files --others`, both of which work on the working tree: it has no need of the
commit.

## The proposed order

Steps 1 and 2 of `close-phase.md` are unchanged. Inside `## The Ritual`:

| | Now | Proposed |
|---|---|---|
| 1 | Phase file and its report, `## Files Changed` included | Phase file: criteria, status 🟢, `**Completed:**` |
| 2 | Roadmap README | Roadmap README |
| 3 | **The next phase** | The roadmap folder |
| 4 | The roadmap folder | Parent roadmap, `CLAUDE.md`, residue |
| 5-7 | Parent, `CLAUDE.md`, residue | **The report, finalized — `## Files Changed` computed here** |
| 8 | Commit | Final verification, then **the audit** |
| — | Final verification, audit, report | **Commit**, then **the next phase**, then report |

Two properties fall out of it:

- `## Files Changed` is computed when nothing else will move, so it is right the first
  time. Defect 1 closes.
- A phase is opened when `HEAD` **is** the commit that closed the phase before it, so
  `report.md`'s definition of `{{START_COMMIT}}` becomes correct as written, with no new
  rule to remember. Defect 2 closes, and the repository-side workaround that
  `scriptorium` had to write down becomes unnecessary.

One line is added to `report.md`, under `### Files Changed`: a path the diff reports that
belongs to earlier work is listed with a one-line reason. Defect 3 becomes an
instruction rather than an improvisation.

The audit moves before the commit. Defect 4 closes, and a clean closure becomes one
commit.

## What this costs

The narrative sections of the report — `## Assessment`, `## Problems And Deviations`,
`## Decisions` — stay in step 1. `close-phase.md` puts the report first deliberately
("The report is the point of the whole ritual"), so that an interrupted closure leaves it
written. Only `## Files Changed`, the one mechanically derived section, moves late. That
reason is worth keeping in the file, or the next reader will move it back.

Between the closure commit and the opening of the next phase, the README names no current
phase. That window is inside one session, and `progress_guard.py` allows it: it forbids a
second 🟡, not the absence of one.

## To verify before changing anything

- `domains/roadmap/skills/roadmap/evals/` — `evals.json` and `checks.py` may assert the
  current step order or the current report shape.
- `close-roadmap.md` — it has its own commit step and its own audit, and the same two
  questions apply to it.
- `roadmap-auditor.md` check 4 is unchanged by all of this: it keeps comparing against
  `git diff`. Nothing here weakens what the audit enforces; it changes when the ritual
  gives it something correct to check.
