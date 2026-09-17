# Open A Phase

Starting work on a phase: the moment a roadmap moves from planned to active.
A phase is opened either directly or from `close-phase.md`, when the previous
phase closes.

## Read The Previous Phase First

Before anything else — before touching a status field, before checking
whether the roadmap is free to open this phase — read the previous phase
file and its report in full: the decisions already taken, the problems and
deviations recorded, the changes made to later phases, and the tasks and
acceptance criteria left unmet.

This is the continuity between sessions, and it is the step that gets
skipped. A phase opened without it does not build on the decisions the
previous phase already took — it re-litigates them, often arriving at a
different answer than the one the repository is already committed to. The
previous report exists for exactly this reason: it is where a finished phase
records what happened so the next one does not have to rediscover it.

The roadmap's first phase has no predecessor. Skip this step only then.

## Settle Pending Restructurings

If the previous report's `## Changes To Later Phases` holds entries marked
`**Pending approval**`, present each one to the user and wait for every
answer. Write nothing until all of them are decided: a phase does not open
onto a roadmap whose shape is still in question.

Then apply the approved ones, per the Editing invariant. A restructuring that
adds a phase follows the procedure for adding a phase in
`references/create.md`; any restructuring that changes the set of phases
replaces the README's progress block with the output of
`scripts/progress.py`, per the Totals and Progress bar invariants. When the result changes which phase comes next, open that phase
rather than the one first intended. The answers are recorded in this phase's
report, below.

The roadmap's first phase has no predecessor and nothing to settle.

## Confirm No Other Phase Is In Progress

Before writing anything, scan every phase file in the roadmap for its
`**Current Status:**` field. Per the Statuses invariant in `SKILL.md`,
confirm no other phase is already 🟡 before writing.

Two situations produce that state, and both need a decision from the user
rather than a silent workaround:

- the previous phase was never actually closed — run `close-phase.md` on it
  first, or confirm it should stay open and this phase waits;
- two phases are genuinely meant to advance in parallel — a real but rare
  case that the one-🟡 rule does not accommodate as written, so ask before
  overriding it.

Do not proceed with either condition unresolved.

## Update The Phase File

In the phase file's `## Status` block, three fields change:

- `**Current Status:**` → 🟡, labeled in the contract's `Language`, with the
  count written as `(0% — 0/N)`, where `N` is the phase's total task count.
- `**Started:**` → today's date, per the Dates invariant.
- `**Blocked By:**` → emptied if the dependency it named is now resolved.
  If it is not resolved, leave the field as it stands and flag it to the
  user when reporting the result — a phase should never open into a block
  it has quietly forgotten to mention.

Apply per the Editing invariant.

## Update The Roadmap README

Two fields in the roadmap's `README.md` change to match:

- the phase's status emoji in the phase list → 🟡;
- `**Current Phase:**` → repointed to the phase just opened.

Same editing discipline as above.

## Create The Report

Create this phase's report from `assets/templates/report.md`, per
`references/report.md`. If restructurings were settled above, record each
answer under `## Decisions` — approved or rejected, and what it changed.

## Resulting State

A phase file with `**Current Status:**` at 🟡 and a `**Started:**` date, a
README whose `**Current Phase:**` points to it, and a report beside the phase
file with its header filled. This is the entry state `close-phase.md` assumes
when it later closes this same phase.
