# Close A Phase

The closing ritual: a phase is finished, and the repository has to say so
from top to bottom.

Work top-down, in the order below. Each step leaves the documents consistent
with the ones above it, so an interrupted closure stops at a known point
instead of leaving the roadmap half-written.

The order has one deliberate inversion: `## Files Changed` is written last,
once every file this closure moves or creates has moved. It is the one
section derived mechanically from the repository, and anything written after
it would make it wrong. For the same reason the next phase is opened after
the commit, and not before it.

## Run The Contract Checks First

Run every command the contract declares under `Checks`, before touching any
file. With no `Checks` declared, skip this step without comment.

**A red command stops the ritual.** A phase is not closable while a
repository invariant is broken: report which command failed, with its
output, and wait. Do not close around the failure, and do not weaken the
check to get past it.

One nuance, and it is the reason this step reads as well as runs: a check
can legitimately fail while a known, recorded defect is still open. Before
treating a red check as a blocker, read `## Problems And Deviations` in the
phase's report. If the failure is the defect already recorded there, it is
not news — name the entry, say so in the report to the user, and continue.
If it is anything else, stop.

## Every Task Done Or Moved

Tick every task actually done — `- [ ]` → `- [x]`. **A phase closes with no
unticked task.** Each task still unticked is moved, before anything else is
written:

- **A later phase exists:** move the task into a named later phase — an
  adjustment, per `references/report.md`, made without asking. Name it under
  `## Problems And Deviations` in the phase's report, with the phase it went
  to, and record the move under `## Changes To Later Phases`.
- **No later phase exists:** the closure stops. Name every unticked task and
  wait: the user finishes it, or approves adding a phase to receive it — a
  restructuring, per `references/report.md`, applied through
  `references/create.md`.

A task is never ticked to get past this step, and never deleted from the
roadmap without the user's approval.

## The Ritual

### 1. The Phase File And Its Report

- Tick the acceptance criteria that hold, and name the ones that do not.
- `**Current Status:**` → 🟢, labeled in the contract's `Language`, with the
  count written as `(100% — N/N)`: every remaining task is ticked.
- `**Completed:**` → today's date, per the Dates invariant.

Then finalize the phase's report, per `references/report.md`, except for
`## Files Changed`:

- make sure every task moved to a later phase and every acceptance criterion
  that does not hold is recorded under `## Problems And Deviations`;
- complete `## Changes To Later Phases`, with every restructuring marked
  `**Pending approval**`;
- write `## Assessment`.

These are the sections only a reader of the phase can write, and they are
written first on purpose, so that an interrupted closure leaves the account
of the phase behind. `## Files Changed` is the one section a command
produces; it waits for step 7, when nothing is left to move.

The report is the point of the whole ritual. Everything else here is
bookkeeping a careful reader could reconstruct from the documents
themselves; the report cannot be reconstructed from anything. It is what
`open-phase.md` makes the next phase read before it starts, and it is the
difference between a next phase that builds on the decisions this one took
and one that re-opens them and lands somewhere else. When this closure
ends, the report is frozen, per the Reports invariant.

### 2. The Roadmap README

- Progress block and `TOTAL` line: replace the whole block with the output
  of `scripts/progress.py` run on the roadmap folder, rather than trusting
  the figures already written — the Progress bar and Totals invariants
  apply, and a phase that added or removed tasks along the way has already
  invalidated them.
- Phase list: the closed phase's emoji → 🟢.
- `**Blocked By:**` and `**Next Milestone:**` → repointed at the next phase.
- `**Current Phase:**` → `—`. The next phase is opened at the end of this
  ritual, after the commit, and that step writes this field and the next
  phase's emoji itself — set them once, there, rather than twice here.
  Between the commit and that step the README names no current phase, which
  is the state the ritual intends: no phase is running.
- `## Metadata`: bump `**Version:**` — a minor bump for a closed phase —
  set `**Last Updated:**`, and set `**Roadmap Status:**` if the roadmap as a
  whole changed state.
- `## Changelog`: a new entry **at the top**, written in the contract's
  `Language`, under the new version. It says what was delivered, what was
  found, and what moved. Per the Changelog invariant, no past entry is
  touched.

Every edit here goes through the Editing invariant.

### 3. The Roadmap Folder

Move the folder only when the roadmap still sits under `pending` and a phase
follows this one: opening that phase at the end of this ritual makes the
roadmap active, so the folder moves with this closure — `pending` →
`on-progress`. Most closures move nothing.

**This step owns the `pending` → `on-progress` transition only.** The move to
`completed` happens when the whole roadmap closes, in
`references/close-roadmap.md`.

**The folder name never changes**, per the Folder name invariant in
`SKILL.md`. Only the state segment of the path moves.

After a move, repair every reference to the old path:

```bash
grep -rln '<Root>/pending/<name>' --include='*.md' .
```

Fix each hit per the Editing invariant, and quote every path. The list is
short and never obvious from memory: a parent roadmap, `CLAUDE.md`, sibling
phase files, a sub-roadmap README pointing back up.

### 4. The Parent Roadmap

Only if the contract declares `Parent`, and only if this phase advances one
of that roadmap's own phases. When it does, the parent gets the same
treatment as step 2 — bar, total, and a changelog entry at the top naming
what moved and where it came from.

A single phase of a sub-roadmap usually does not advance the parent. Closing
the sub-roadmap as a whole always does, and that closure belongs to
`references/close-roadmap.md`.

### 5. `CLAUDE.md`

Only if the phase changed something `CLAUDE.md` documents: the current
state, the entry point, a convention, an invariant. Do not touch it
otherwise — a closure is not an occasion to tidy it.

### 6. Residue

Only when the contract says `Versioning: none`. Without git, whatever a
command wrote stays, and nothing will flag it later. Before declaring the
phase closed, look for `__pycache__/`, `target/`, a stray `Cargo.lock`, and
run artifacts, and remove them.

Under `Versioning: git`, skip this step: the commit surfaces stray files on
its own.

### 7. `## Files Changed`

Every file this closure moves or creates has now moved. Compute
`## Files Changed` in the phase's report, per `references/report.md`, and
write it there.

Nothing below this step writes a file the report has to name: the commit
records what is already on disk, and the next phase is opened after it.

## Traps

How the Editing and Changelog invariants in `SKILL.md` get broken in practice:

- **Verify the exact string before replacing**, per the Editing invariant.
  A phase list item and a progress bar line wrote the same phase name
  differently; the pattern loose enough to match both corrupted one of them.
- **Never rewrite a past changelog entry**, per the Changelog invariant. If
  names or paths have changed since — step 3 is the usual cause — the old
  entry keeps the old ones and the new entry explains the change.
- **Never mass-substitute across the repository**, per the Editing
  invariant. A sweep over every `.md` file rewrote a read-only reference
  document and a paragraph where an ordinary word happened to read like an
  identifier, and reported success for both.
- **Quote every path**, per the Editing invariant. A roadmap folder named
  for a release candidate — spaces and parentheses in the name — split into
  three arguments mid-ritual and the command ran against the wrong tree.

## Final Verification

Re-run the contract's `Checks`, then run `scripts/progress.py --check` on
the roadmap folder — and on the parent's folder when step 4 touched it —
then verify that relative links still resolve with `scripts/check_links.py`:

```bash
python3 "<skill-dir>/scripts/check_links.py" '<Root>/*/*/*.md' '<Sub-roadmaps>/*/*/*.md' 'CLAUDE.md'
```

`<skill-dir>` is this skill's base directory.

The globs are arguments, built from the contract. Per the `Root` convention
in `SKILL.md`, a contract path stops one level short of the state segment, so
every glob is built by **appending** — never by collapsing a segment inside
the path. Append `*/` for the state, then a `<roadmap-name>/*.md` tail: a
wildcard for the roadmap's name, then its phase files. `CLAUDE.md` is added
as-is. With the complete contract example from `SKILL.md`: `Root`
(`docs/roadmap`) plus the state wildcard plus the tail gives
`docs/roadmap/*/*/*.md`; `Sub-roadmaps` (`packages/*/roadmap/`), built the
same way, gives `packages/*/roadmap/*/*/*.md`. The arguments then read
`'docs/roadmap/*/*/*.md' 'packages/*/roadmap/*/*/*.md' 'CLAUDE.md'`. Quote
each one so the shell leaves the expansion to the script.

`Sub-roadmaps` is optional: when the contract does not declare it, drop that
argument entirely rather than passing a glob that matches nothing.

Expected output is `0 progress problem(s)`, then a count and `0 broken`. Anything else names the file and
the link, and is fixed before the closure is reported as done.

## Audit

Hand the closure to the `roadmap-auditor` agent before committing it. Give
it the roadmap folder, the phase file just closed, the contract's
`Versioning`, and the `**Start Commit:**` from the phase's report. The
auditor reads the working tree, so it needs no commit; auditing first means a
closure it sends back is repaired in place instead of costing a second commit
whose only content is a correction. Its answer opens with
`VERDICT: PASS` or `VERDICT: FAIL`, followed by one line per problem.

- `VERDICT: PASS` — continue to the commit.
- `VERDICT: FAIL` — fix every problem it lists, run the Final Verification
  again, then run the audit again.
- `VERDICT: FAIL` a second time — stop. Present the remaining problems to the
  user, and do not report the phase as closed.

When the `roadmap-auditor` agent is not available, continue, and say in the
report to the user that the audit did not run and that `make enable
D=roadmap`, run in the my-claude-setup repository, installs it.

## Commit

Only when the contract says `Versioning: git`. Commit per the repository's
own convention — message format, scope, trailers — staging the files this
closure touched rather than the whole tree, since a repository usually has
unrelated work in progress.

A closure that passed its audit is one commit. Nothing that follows belongs
to it: the next phase opens onto a repository whose last commit is the
closure of the phase before it.

Under `Versioning: none`, no commit is made and none is promised.

## The Next Phase

Open it by following `references/open-phase.md`, which starts by reading the
report this ritual has just finalized.

This is the last step for a reason. Under `Versioning: git`, `open-phase.md`
records the new phase's `**Start Commit:**` as `HEAD`, and `HEAD` is now the
commit that closed the phase before it — so that phase's own diff, at its
closure, holds its work and nothing else. Opening the phase any earlier
records a commit one phase behind, and the whole of the previous phase's work
is swept into the next report's `## Files Changed`.

If no phase follows, this one was the last: the roadmap itself is finished,
and `references/close-roadmap.md` takes over from here.

## Report To The User

Keep it short — the documents carry the detail:

- what was delivered, and every unfinished task by name with the phase it moved to;
- the figures the checks and the two scripts returned;
- the audit verdict, or that the audit did not run;
- what the phase found, in a line or two, drawn from the report's
  `## Assessment`;
- every restructuring the report marks `**Pending approval**`, one by one,
  since the next phase will not open until each is decided;
- which phase is current now, or that the roadmap is ready to close.
