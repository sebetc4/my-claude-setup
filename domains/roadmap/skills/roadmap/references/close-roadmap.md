# Close A Roadmap

The closing ritual for an entire roadmap: every phase already closed, and the
repository has to fold the roadmap itself into `completed/`. `close-phase.md`
hands over to this file when a closed phase has no successor to open — at its
last step, so that phase's closure is already committed and audited when this
ritual starts. What follows is this ritual's own commit.

## Run The Contract Checks First

Run the contract's `Checks` exactly as `close-phase.md` describes, before
touching any file. A red command stops this ritual the same way, and the same
exception applies to a defect already recorded in the last phase's report.

## Prerequisite: Every Phase Is Green

Scan every phase file in the roadmap for its `**Current Status:**` field.
Closing the roadmap requires every one of them at 🟢.

**Any phase not at 🟢 stops the closure.** Name the phase and its status,
and wait. Do not close the roadmap around an unfinished phase, and do not
reinterpret its status to get past this check.

## Prerequisite: Nothing Left Pending

Read the last phase's report. If its `## Changes To Later Phases` holds
entries marked `**Pending approval**`, present each one to the user and wait
for every answer. An approved restructuring that adds a phase means the
roadmap is not finished: add the phase per `references/create.md` and stop
here. Apply any other approved restructuring per the Editing invariant, and
record every answer in the changelog entry written in step 2.

## The Ritual

### 1. The Summary

Write `summary.md` from `assets/templates/summary.md`, into the roadmap's own
folder and before the folder move in step 3, so the move carries it along with
everything else. What sets this document apart from everything else the
ritual touches: it is written **after** the fact, from every phase's report
read in full, and it is a narrative, not a metrics table — the bar, the
totals, and the per-phase counts already live in the README and need no
restating here.

It answers six questions: where the roadmap started, where it arrived, what
each phase actually delivered, what was learned that outlives this one
roadmap, what is deliberately left open, and — when the contract declares a
`Parent` — what this roadmap rolls up to the parent's own account. Without a
`Parent`, omit that last section with its heading. The most valuable section
is `## What We Learned`: what holds beyond this one roadmap, not what happened
in it. As with every produced document, the summary carries only the
template's headings and the written answers — no explanatory notes.

`## What Each Phase Delivered` draws on the reports' `## Assessment`
sections; `## What We Learned` draws on their `## Decisions` and
`## Problems And Deviations`.

### 2. The Roadmap README

The roadmap's own README is finalized before the folder moves — step 2 of
`close-phase.md`, at roadmap scope:

- `## Metadata`: `**Roadmap Status:**` → 🟢 with its label, per the Statuses
  invariant; bump `**Version:**` — a major bump for a closed roadmap — and
  set `**Last Updated:**`.
- `**Current Phase:**`, `**Blocked By:**`, and `**Next Milestone:**` →
  cleared to `—`. A completed roadmap that still points at a phase or a
  milestone reads as though work were still running.
- `## Changelog`: a new entry **at the top**, written in the contract's
  `Language`, under the new version. It names the closure, what
  `summary.md` records, where the folder now lives, and the answer to any
  restructuring settled before the ritual. Per the Changelog invariant, no
  past entry is touched.

Every edit here goes through the Editing invariant. The bar, the totals, and
the phase emoji were brought to their final figures by the last phase's
closure — `scripts/progress.py --check` says whether they still agree with
the per-phase counts; replace the block with its output only if they do not.
`**Location:**` still names the old path at this point; step 3 repairs it
with every other reference to that path.

### 3. The Roadmap Folder

Move `<Root>/on-progress/<name>/` to `<Root>/completed/<name>/`. **The folder
name never changes**, per the Folder name invariant in `SKILL.md` — only the
state segment of the path moves.

**This step owns the `on-progress` → `completed` transition.** The earlier
move out of `pending` belongs to `close-phase.md`.

After the move, repair every reference to the old path:

```bash
grep -rln '<Root>/on-progress/<name>' --include='*.md' .
```

Fix each hit per the Editing invariant, and quote every path. The list is
rarely limited to the roadmap's own README: a parent roadmap, `CLAUDE.md`,
and any sibling document that linked into this roadmap while it was active
can all carry the old path.

### 4. The Parent Roadmap

Only if the contract declares `Parent`. Where a single phase's closure only
sometimes reaches the parent, closing the whole sub-roadmap **always**
does — the parent gets the same treatment `close-phase.md` gives it for a
phase: replace its progress block with the output of `scripts/progress.py`,
set the corresponding phase's emoji to 🟢, and add a changelog entry at the
top naming what closed and where it now lives.

### 5. `CLAUDE.md`

Only if the roadmap's closure changed something `CLAUDE.md` documents: the
current state, the entry point, a convention, an invariant. Do not touch it
otherwise — a closure is not an occasion to tidy it.

## Traps

The traps listed in `close-phase.md` apply to this ritual unchanged.

## Final Verification

Re-run the contract's `Checks`, then run `scripts/progress.py --check` and
`scripts/check_links.py` as `close-phase.md`'s own Final Verification section
describes, including its rule for building the globs from the contract.

## Audit

Hand the closure to the `roadmap-auditor` agent before committing it. Give it
the roadmap folder, now under `completed/`, `roadmap` as the target, and the
contract's `Versioning`. As in `close-phase.md`, the auditor reads the working
tree: auditing before the commit keeps a closure it sends back from costing a
second commit. Its answer opens with `VERDICT: PASS` or
`VERDICT: FAIL`, followed by one line per problem.

- `VERDICT: PASS` — continue to the commit.
- `VERDICT: FAIL` — fix every problem it lists, run the Final Verification
  again, then run the audit again.
- `VERDICT: FAIL` a second time — stop. Present the remaining problems to the
  user, and do not report the roadmap as closed.

When the `roadmap-auditor` agent is not available, continue, and say in the
report to the user that the audit did not run and that `make enable
D=roadmap`, run in the my-claude-setup repository, installs it.

## Commit

Only when the contract says `Versioning: git`. Commit per the repository's
own convention — message format, scope, trailers — staging the files this
ritual touched: `summary.md`, the README, the folder move, and whatever step
4 and step 5 reached.

Under `Versioning: none`, no commit is made and none is promised.

## Report To The User

Keep it short — the documents carry the detail:

- that the roadmap is closed, and where it now lives;
- the figures the checks and the two scripts returned;
- the audit verdict, or that the audit did not run;
- what the roadmap accomplished, in a line or two, drawn from `summary.md`;
- whether the parent roadmap was updated, and what changed there.
