# The Phase Report

The record of what actually happened during one phase. The phase file is the
plan — what was meant to happen; the report is the account of what did.
`open-phase.md` creates the report, the work on the phase keeps it,
`close-phase.md` finalizes it, and `close-roadmap.md` reads it.

## Name And Place

Per the Reports invariant in `SKILL.md`: one report per opened phase, beside
its phase file, named after it with a `-report` suffix. The phase file
`phase-3-search-index.md` has the report `phase-3-search-index-report.md`.

## Lifecycle

**Created when the phase opens.** `open-phase.md` writes it from
`assets/templates/report.md`:

- `{{PHASE_NUMBER}}` and `{{PHASE_NAME}}` — as in the phase file;
- `{{PHASE_FILE}}` — the phase file's name, such as `phase-3-search-index.md`;
- `{{START_COMMIT}}` — the output of `git rev-parse --short HEAD` when the
  contract says `Versioning: git`. Under `Versioning: none`, the
  `**Start Commit:**` line is left out. When the phase is opened from a
  closure, that closure is already committed — `close-phase.md` opens the
  next phase last for this reason — so `HEAD` is the commit that closed the
  previous phase, and this phase's diff will hold its own work only.

All six section headings are present, and their bodies start empty.

**Kept while the work happens.** Write into the report as things happen:
after each significant step, and always before a commit, a pause, or the end
of a session. The report is never reconstructed at the end of the phase — by
then the early steps survive only as a summary of a summary.

**Finalized at closure** by `close-phase.md`, then frozen per the Reports
invariant.

## Resuming An Open Phase

Before any work on a phase that is already open, read its phase file and its
report in full. The last Work Log entries say where the work stopped, and the
Decisions say what is already settled.

## Sections

### Work Log

The work as it actually unfolded, in chronological order. Entries are grouped
under date headings, `### YYYY-MM-DD` per the Dates invariant. Each entry says
what was done, what was found, and where it led — dead ends and backtracking
included.

**The Work Log is never organized by the phase's task list.** It follows the
order in which the work was really done: a log shaped like the plan records
the plan a second time and loses what only the log can hold.

### Decisions

Every decision taken during the phase, one entry each: the decision, the
reason for it, and what it commits later phases to. This is the section the
next phase reads so that it builds on what is settled instead of reopening
it.

### Files Changed

Four groups, each left out when empty: **Added**, **Modified**, **Deleted**,
and **Renamed** (`old → new`).

- Under `Versioning: git`, the list is computed at closure, never kept from
  memory. Compare the working tree with the start commit, so that work not
  yet committed is counted, then list the files git does not track yet:

  ```bash
  git diff -M --name-status <Start Commit>
  git ls-files --others --exclude-standard
  ```

  From the first command, `A` goes under Added, `M` under Modified, `D` under
  Deleted, and any `R` under Renamed; every file from the second goes under
  Added.

  The list is the diff, entirely: a path the diff reports that belongs to
  earlier work — a repair to a previous phase's documents, say, landed after
  this phase started — is listed like any other, with a one-line reason
  beside it. Leaving it out makes the section unauditable, since the auditor
  has only the diff to compare against.
- Under `Versioning: none`, the list is kept by hand during the work.

The section is written at the very end of the closure, after the roadmap
folder has moved and before anything else is created, per
`references/close-phase.md`. Computed earlier, it names files under paths
that no longer exist and misses the ones the rest of the ritual adds.

### Problems And Deviations

Everything that did not go as planned: tasks not done, tasks done
differently, premises that proved false, defects discovered. Each entry
states its consequence and where it went — fixed, moved to a named later
phase, or left open.

### Changes To Later Phases

Every change made to a later phase's file: which file, what changed, and
why. A restructuring is written here, its entry opening with the marker
`**Pending approval**`, and is not applied — see below.

### Assessment

Written at closure: the overall account of the phase, ending with what the
next phase needs to know first.

**At closure, `## Problems And Deviations` and `## Changes To Later Phases`
are never left empty.** When there is nothing to record, one line says so:
an empty section cannot be told apart from a forgotten one.

The group labels and the `**Pending approval**` marker are written exactly as
shown, in English, whatever the contract's `Language`.

## Example

An excerpt of a report in progress, for a roadmap whose contract declares
`Language: english`:

```markdown
## Work Log

### 2026-03-04

Started with the tokenizer, since the indexer depends on it. The existing
tokenizer drops accented characters; replaced it rather than patching it.

### 2026-03-05

Built the indexer on the new tokenizer. Index builds ran three times slower
than the target; profiling pointed at one commit per document. Switched to
batched commits, which met the target.

## Decisions

- **Index commits are batched, 500 documents per batch.** One commit per
  document missed the build-time target threefold. Phase 3 inherits the batch
  size as a tuning parameter.

## Problems And Deviations

- **Task "Add stemming" not done.** The tokenizer rewrite consumed the time
  planned for it. Moved to phase 3.

## Changes To Later Phases

- `phase-3-ranking.md`: added the task "Add stemming", moved from this phase.
- **Pending approval** — `phase-4-results-page.md`: merge it into phase 3.
  The results page is now a single component, too small to stand as a phase.
```

## Adjusting And Restructuring Later Phases

**Adjust — done without asking, and recorded under Changes To Later
Phases:**

- move an unfinished task into a named later phase — required at closure, per
  `references/close-phase.md`;
- add, reword, or split a task in a later phase;
- add a dependency, a constraint, or a `**Blocked By:**` entry to a later
  phase.

**Restructure — recorded with `**Pending approval**`, never applied without
the user's approval:**

- add, remove, merge, split, or reorder phases;
- change a later phase's `## Objective` or `### Out of Scope`;
- change the roadmap's scope as its README states it;
- remove a task from the roadmap without moving it to a later phase.

An adjustment that changes a phase's task count is absorbed when the totals
are recomputed at closure, per the Totals invariant.

A restructuring stays pending in the report that recorded it, and that
report is frozen at closure. The decision is taken before the roadmap moves
on: `open-phase.md` raises it before the next phase opens, and
`close-roadmap.md` raises it when no phase follows.
