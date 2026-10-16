# Phase 0: Measure And Design

---

## Status

**Current Status:** 🟡 In Progress (100% — 4/4)
**Started:** 2026-10-15
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-measure-and-design-report.md` current as the work happens — after each
significant step, and before every commit, pause, or end of session.

---

## Objective

Measure where the current workflow's time and tokens go, decide what each tool and each
waiting roadmap keeps, and set the figures Phases 1 to 3 are judged on.

---

## Overview

### Why This Phase Matters
Until now the workflow's weight was answered by additions; a measure says what to remove.

### What It Enables
Phases 1 and 2 cut from a design and against targets, not from impressions.

### Out of Scope
Changing any tool: Phases 1 and 2.

---

## Tasks

### Measure
- [x] Measure from the transcripts since 2026-09-28, with `shared/sessions/`: each roadmap's cost and days from its opening to its tool installed, the working sessions' share, the words per phase report and per task, the user's yeses per eval iteration
  Proof: check — each figure in the report with the command that gives it
- [x] List the steps and rules each tool imposes — the roadmap skill and `roadmap-auditor`, `authoring-skills` and its agents, the review domain's requests, `CLAUDE.md`'s conventions, the agent's memories — each with what it caught in the reports and reviews, and what it cost
  Proof: review — the list read by the user

### Decide
- [x] Decide with the user, for each waiting roadmap — `roadmap-dependencies`, `roadmap-execution`, `working-method`, `git-domain`, `session-review` — and for `token-usage`'s remaining tasks: keep, merge into this roadmap, or cut
  Proof: review — the user's decision for each, in the report and in `docs/roadmap/README.md`
- [x] Write the design in this file's `## Design`: what is removed, what changes, the targets of Phases 1 to 3; then the decision record
  Proof: review — the design approved by the user

---

## Design

From tasks 1 to 3; the figures are the report's, 2026-10-15 and 2026-10-16.

The checks that cost least caught most, and no script check is cut. What weighs is what
the rules ask of a session — eval iterations at 2.4 yeses each, reports at 726 words per
task — and tools that serve little: `roadmap-auditor` passed 26 closures of 26, its one
FAIL since on a report section's wording; working sessions since 2026-09-28 started
`compare.py` twice and `tuning.py` once, and saved one feedback in 34 benchmarks.

One rule bounds the cuts, from the user: a failure that would be silent keeps its check;
one that shows can wait for use, since nobody reports a check that does not exist.

### Phase 1: `authoring-skills`

- **Removed:** `viewer.py`, `compare.py` with `skill-comparator`, `tuning.py` with
  `assets/description-rewrite.md`, their tests, keys, files and sections, the viewer's line
  in `NOTICE`. A description missing its triggers is rewritten by hand and measured again
  with `triggers.py`.
- **Changed:** `references/eval-files.md` keeps the files the agent writes, `evals.json`
  and `classes.json`; a script says its output in its `--help`. `references/evaluate.md`
  leads with the default regime, the full regime adding the rest. One yes per iteration
  covers its runs, its gradings and the instrument fixes proposed with it.
- **Kept:** `audit.py` and its hook, `skill-auditor`, `skill-grader`, `workspace.py`,
  `run.py`, `grade.py`, `benchmark.py`, `triggers.py`; the From Use task.

### Phase 2: The Roadmap Skill

- **Removed:** Under `versioning = "git"`, the report's `## Files Changed`, which git gives from the Start
  Commit, and the closure's ordering around it. The README's `## Changelog`,
  `**Version:**` and `**Last Updated:**`, with the Changelog invariant: the reports and git
  hold the history. The phase template's sections that repeat the skill or another
  section: Before Starting, While Working, Why It Matters, What It Enables, Acceptance
  Criteria — each task's `Proof:` line stands for them. The opening's search for a second
  🟡, which `progress_guard.py` makes. `references/old-contract.md`. A roadmap closure's
  audit: its points show when they fail.
- **Changed:** `roadmap-auditor` audits a phase closure on its two points of judgment —
  each ticked task's proof in the report, by its `Proof:` kind, and each moved task present
  in its later phase —, with watch points in `domains/review/hooks/tools.json` for Phase 3
  to judge it; the two mechanical points left, sections not empty and the
  `**Completed:**` date, go to `progress.py --check`. Four report sections — Work Log, Decisions, Deviations (Problems And
  Deviations and Changes To Later Phases, `**Pending approval**` kept), Assessment. An
  entry says what changed, the figures, the decisions; the report keeps the latest
  hand-over only. A resume reads the phase file, the Decisions, the Deviations and the last
  hand-over. The
  first opening moves the folder to `on-progress/` and sets the Roadmap Status.
  `progress.py --write` writes the block. The closure: checks, tasks done or moved, phase
  file and report, README, residue under `none`, `--check` and links, the auditor, commit,
  next phase.
- **Kept:** the contract, the other invariants, `Proof:` per task, `## Design` in a phase
  that designs, the two hooks.

### Phase 2: Conventions, Memories, Reviews, Measure

- `CLAUDE.md`: one line per folder in the Layout, a module's detail in its docstring;
  `.superpowers/`, gone from disk, leaves it.
- Memories: each whose rule a tool or `CLAUDE.md` then carries goes — the auditor's
  verdict, the cost limit, short records, records in the report, commit per step,
  coupling names, cite by name, superpowers' two. Kept: French replies, transcripts, skill
  settings.
- Review domain: kept, no longer temporary, its requests unchanged: it is the default
  regime's watch in real use, at $0.19 a review. Saturation at 5 reviews instead of 10
  would have asked 101 of the 175 reviews instead of 138, about $7 saved, and lost 5 more
  of 69 targets raised. Its own defects, 97 of 272 findings, are fixed, the SessionStart
  count first.
- The measure: `baseline.py` and `tools.py` in one `tools/measure.py`, beside
  `tools/reviews.py`.

### Findings Of 2026-10-16

Each is fixed in its phase, unless its target is cut — moot: `roadmap-auditor`'s search of
the old path, the move now at the opening, `report.md`'s rename threshold and a waiting phase's Files Changed — or it asks for a tool
that replaces nothing — set aside: a `probe.py`.

### Plugins Removed

`docs/decisions/2026-10-04-plugins-removed.md` waited for `working-method` and
`roadmap-execution`, both cut. Planning comes back through the roadmap skill's
`## Design` and `Proof:`, design or debugging through Phase 3's first tool; a capability
missed in use is a request for a tool under the default regime.

### Targets

| Measure | Phase 0 | Target | Judged |
|---|---|---|---|
| A tool, request to install | `session-close` 2.3 days, $94; `skill-validation` 1.2, $127 | ≤ 1 day, ≤ $50 | Phase 3 |
| The user's yeses per eval iteration | 2.4 | 1 | Phases 1, 3 |
| `authoring-skills`: words, agents | 13,052, 3 | ≤ 9,000, 2 | Phase 1 |
| Roadmap skill: words; auditor's words | 8,333; 467 | ≤ 6,000; ≤ 250 | Phase 2 |
| `CLAUDE.md` words, memories | 1,960, 12 | ≤ 1,000, 3 | Phase 2 |
| Report words per task | 726 | ≤ 300 | Phase 3 |
| Review findings on the review domain | 36% | ≤ 10% | Phase 3 |

The existing evals stay guards; a guard checking a cut step goes with it.

---

## Technical Details

### Files to Modify
```
docs/roadmap/pending/lean-workflow/phase-0-measure-and-design.md
docs/roadmap/README.md
docs/decisions/<date>-lean-workflow.md    new
```

### Dependencies
`docs/decisions/2026-10-15-validation-weight.md`: its figures and regimes are the
starting point, not measured again.

### Constraints
Remove before adding. The design adds a tool only when it replaces more than it adds.

---

## Acceptance Criteria

- [ ] The baseline figures are recorded with their commands
- [ ] Each waiting roadmap has the user's decision
- [ ] The design and its targets are approved
