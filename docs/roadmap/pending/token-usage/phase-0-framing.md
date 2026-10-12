# Phase 0: Framing

---

## Status

**Current Status:** 🟡 In Progress (100% — 5/5)
**Started:** 2026-10-11
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle what the measures are for, before any code: the return on each tool of this
setup, and a review of several sessions run by hand. From these uses, settle what the
review domain measures, from which prices, how a window of sessions is found, how long
the transcripts are kept, and how the domain's four open defects are fixed.

---

## Overview

### Why This Phase Matters
The analysis of 2026-10-06 made these choices by hand, once. A tool makes them in every
review, so a wrong price or a wrong window for a phase would be repeated in all of them.
The three counts by hand served because they ended in conclusions: shorter sessions,
runs started against the credit left. A figure no decision reads costs and gives
nothing.

### What It Enables
Phases 1 and 2 build designs the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Design

Approved by the user on 2026-10-12, after five rounds the report records: every cost by
model and effort; the three ways of going on after a stop compared; `served`; the
reviews processed and archived; the name `reviewing-token-usage`; the window's record
kept here; the boundaries with `session-review`; the tools reviewed chosen by a list.
It rests on the inputs' list of the report,
R1 to R5, T1 to T5, M1 to M10 and D1 to D4, and on the results of tasks 2 and 3. One rule
comes first: each figure is kept for the decision it informs (the user, 2026-10-11), and
a figure no decision reads is not computed, nor printed, since printing it costs context.

### What Each Measure Serves

| Measure | Where | The decision it informs |
|---|---|---|
| Cost per model, in dollars | Tool review, review of several sessions | Whether a tool, a phase or a kind of work is worth its cost |
| Every subagent and `claude -p` session | Both; a tool review has no `claude -p` session | Runs started against the credit left; what a run costs (M7, R5) |
| A tool's own cost | Tool review, `make reviews` | The return on the tool, beside what its reviews say it brought |
| Model and effort of each call, with its price | Both, every cost broken down by model and effort | The model and effort of sessions, agents and runs (2026-10-06, Effort) |
| How the work went on after a stop: a new session, a rebuilt cache, a compaction | Review of several sessions | Which way to go on at the end of a roadmap step: a hand-over note and a new session, the same session, or a compaction (M5) |
| Openings, documents read, sessions past break-even | Review of several sessions | When a phase hands over to a new session (roadmap `roadmap-execution`), how large a report may grow |
| Runs lost | Review of several sessions | Runs started together or against the credit left (P4 $17.26, P5 $10.52) |
| A review's own cost | Tool review, `make reviews` | How often a review is asked for |
| The gap with `cost-state` | Review of several sessions | The price table and the estimates (M2, M3) |

### Boundaries

Three reviews, told apart by the question each answers (the user, 2026-10-12):

| | `tool-review` | `session-review`, roadmap `session-review` | `reviewing-token-usage` |
|---|---|---|---|
| Question | What one of this setup's tools brings for its cost | What one of a repository's own tools brings for its cost | Where a stretch of work's tokens went, and how the work should run |
| Unit | A tool, in a session's slice | A tool, in a task | A window of sessions |
| Started | By the Stop hook | By hand, at the end of a task | By hand, at the end of a phase, a roadmap or a stretch of work |
| Concludes on | The tool: its text, its trigger, its noise, its model and effort | The same, for the repository's tools | The way of working: hand-overs, model and effort of sessions and runs, runs lost, the reviews' budget |
| Records | This repository's `reviews/` | The repository it reviews | This repository's `reviews/windows/` |

`tool-review` and `session-review` ask one question of two catalogs: whether they
become one tool review with two catalogs is roadmap `session-review`'s Phase 0 to decide.
`reviewing-token-usage` judges no tool's return: it counts spending by kind, main thread,
subagent type, `claude -p` folder and reviews; when a tool stands among the largest
costs, its conclusion points to that tool's reviews, or asks for one.

### The Reader

Phase 1 extends `shared/usage/usage.py` (one reader, decided at opening) and adds
`shared/sessions/sessions.py`, which selects a window's sessions and imports the first.
The module keeps its name: the skill is what a user calls, and its name avoids `usage`.

- **Prices.** Each model's input, output and cache-read price, with its own date and
  source: published, as read from the `claude-api` skill of a named Claude Code version,
  or fitted to `cost-state` records, marked fitted. Claude Haiku 5.5 enters fitted, $0.10
  and $0.50 (M2), until a published price is read. Cache writes stay five-minute and
  one-hour, at 1.25 and 2 times the input price; a model the table lacks costs `None`
  (R2). The table is kept current by the review of several sessions, which compares
  every session a `cost-state` record covers whole with its `costUSD` per model, and
  flags a gap (below); a price changes with its date and its test.
- **Subagents.** Every subagent under `<session>/subagents/`, not only the catalog's
  (T1). A call without its final usage takes an output estimated per agent type, from a
  table: `skill-auditor` 640 tokens, any other 5,400 (M4, R3), marked estimated. The last
  call of a run takes its final output from the Agent tool's result,
  `toolUseResult.usage`, counted (M4).
- **Effort** of each call, from the record's `effort` (M6).
- **Cache rebuilds.** A call that writes again most of the context the previous call
  read: its size, its cost over a read of the same tokens, and its cause, a pause past
  the hour, a `credential_org` change, or none known (M5).
- **Compactions.** A compaction's call and the context it leaves. No transcript kept on
  2026-10-12 holds one, as none did in the three counts by hand: Phase 1 probes how a
  compacted session is recorded before it tests the count.
- **A conversation continued in a new process.** A message id held by several
  transcripts goes to the transcript whose last record comes first, the one the history
  was copied from. Task 3 showed the rule of R4, the first transcript to start, give
  `a556427b` all 102 calls it shared with `c3561bb8`.
- **A window.** Two times, `from` and `to`; each call is counted by its time, so a
  session that straddles a bound is split (task 3: 7 and 13 calls of a closing session;
  `2f2e66de`'s two roadmaps):
  - main sessions: the transcripts of the project folders whose sessions ran in the
    repository, with calls in the window;
  - `claude -p` sessions: the transcripts of any project folder without a human prompt
    whose first record falls in the window, each given to a main session by its
    scratchpad folder's name, else by the main session whose span holds its first
    record; in no span of the repository's sessions, left out as another project's; in
    two spans, given to the first and marked shared (task 3: 2 and 8 sessions). Never
    from `.eval-runs/` alone, whose results miss a run lost or stopped (task 3: 43 and 8);
  - each commit of the repository in the window, given to the session whose span holds
    it, so that a session working on something else shows (`8af16381`).
- **Calls no transcript holds**, Claude Code's own (M3): not counted; they show as part
  of the gap with `cost-state`.

### Tool Reviews

The measured block gains, beside its token counts (Phase 2):
- `cost`: the slice's calls and cost per model and effort, main thread and subagents
  apart, every subagent of the slice included; the part resting on estimates; the
  prices' date; the models the table lacks;
- a `cost` per tool under review, derived and marked as such, its rule printed beside
  it: a skill's loaded characters, the files of it read through Read or Bash (D2) and
  its scripts' output, and a hook's injected characters, as tokens at 3.5 characters,
  each priced as one one-hour write and a read by every later call of the slice (M8); an
  agent's runs at their own cost per model, output estimated and marked as the reader
  does (D4), with their model and effort;
- `review`: the review's own turn, from `slice.to` to the first call after `record.py`
  has answered, or to `closed` when that comes first (T3, M9). The Stop hook writes it
  when it closes the turn; the review never measures itself.

Cache rebuilds stay out of the tool review: a rebuild follows from a pause or a change
of organization, not from a tool, and no decision on a tool reads it. The review of
several sessions shows them.

`measure.py` prints each tool's cost beside the median of the tool's earlier reviews,
with the ratio, and owes an explanation past 1.5 times (taken from
`study/session-review/`). The draft gives each tool a `served` beside what it brought:
`full`, `partial` or `none`, checked by `record.py`; a review written before reads as
unknown.

### `make reviews`

It runs from this repository, the setup's central one, where the domain writes every
tool review from every project. A review holds its measures, so `make reviews` has no
deadline: the 30 days bound only the review of several sessions, which reads transcripts.

- Each tool's median cost in dollars over its current version's reviews, beside today's
  measures (T5); a review written before the change counts in no median of dollars.
- Two flags, each from three reviews: a tool whose current version's median cost passes
  1.5 times its earlier versions', and a tool whose current version's reviews say
  `served: none` in a third of them or more, with what those reviews cost.
- One line for the reviews themselves: their median and total cost over the last 30
  days, flagged past the budget below.
- One line per window that the review of several sessions recorded: its date, its
  repository, its bounds, its cost and its flags.

### Which Tools Are Reviewed

A review serves only a tool someone means to improve; otherwise it is noise in the
workflow (the user, 2026-10-12). So the tools reviewed are chosen, in a `[review]` table
of `.agent-conventions.toml`, the same key in every repository:

```toml
[review]
tools = ["roadmap", "agent:skill-auditor"]
```

- An entry is a tool id, `agent:skill-auditor`, or in this repository a whole domain of
  the setup, `roadmap`.
- The list lives where its tools are improved. This repository's lists this setup's
  tools, whatever project uses them: the Stop hook reads it by its path, the repository
  the installer's state names, as it already writes the reviews into its `reviews/` from
  every project, and never climbs from the session's working directory. A repository's
  own tools, scriptorium's `pdf-reviewer` for one, go in that repository's file, for
  roadmap `session-review` to read.
- Read at each Stop, so that a change applies without `make update`; a table missing or
  empty asks for no review, and `make reviews` says so. `tools.json` keeps only the
  points to watch, which belong to each tool.
- `make reviews` proposes, never decides: dropping a tool on which the reviews of the
  last two archives raised no finding, and watching again a tool not reviewed that has a
  new version.
- A tool no longer reviewed still costs tokens: the review of several sessions keeps
  counting it, so a stable tool whose cost drifts shows among a window's largest costs.
- `.agent-conventions.toml` is ignored by git here: the list is working state, like the
  roadmaps' root, and a new clone reviews nothing until it is written.

### What A Tool Review May Cost

A review cost about $0.34 in Phase 4 of `skill-tooling` and $0.23 in Phase 5 (M9). The
budget: a median of $0.25 a review. The lever: the Stop hook leaves out of its request a
tool version that holds ten complete reviews not archived, whose last five raised no kind
and target the earlier ones had not; when every tool the session used is left out, it
asks for no review. A new version, or the archive below, starts the reviews again. On
2026-10-12, `session_resume.py` held 69 of the 90 reviews and `roadmap` 64, over three
versions each: they serve first in every roadmap session.

### Processing The Reviews

Reviews that pile up teach nothing (the user, 2026-10-12). In this repository, at a
moment the user chooses, the agent goes through `make reviews` with the user: its flags,
and its findings by recurrence, each carried into a roadmap or set aside on the user's
word. Then `tools/reviews.py --archive` moves the reviews it read into
`reviews/archive/<date>/`. The findings and the saturation count only the reviews not
archived, so their counters start again from zero; the medians of cost read the archive
too, so that a tool keeps its baseline. `make reviews` says how many reviews wait since
the last archive.

### The Review Of Several Sessions

A skill of the review domain, `reviewing-token-usage`, run by hand (the user,
2026-10-11) in the repository whose work it reviews, this one included, within 30 days of
its window's start. It reviews how the sessions of a stretch of work consumed, the
setup's tools among them; the return on each tool stays with the tool reviews. Its name
says what it measures, the tokens spent wherever they go, main threads, subagents and
`claude -p` sessions, rather than one session's (the user, 2026-10-12); it follows the
writing guide, verb first, and takes none of Claude Code's (`usage`,
`insights`, `recap`, `docs/claude-code-builtins.md`) nor `session-review`, which roadmap
`session-review` brings in.

- **The window.** `--repo`, the working directory by default; `--from`, a commit or a
  time; `--to`, a commit, a time, or now by default; a commit stands for its time. For a
  phase of a roadmap, the skill says to give its report's Start Commit and the commit
  that closed it; the script reads no roadmap file, so that the two domains stay
  independent. `--exclude <session>` sets a session apart, named in the record.
- **What it prints**, 80 lines at most, the sessions' table cut to the costliest:
  - the window, its sources, and any warning;
  - the cost per model and effort, split into main thread, subagents, `claude -p`
    sessions by kind of folder, and tool reviews, with the calls and the output of a
    call; the estimated part; the models the table lacks;
  - per session: calls, peak context, cost, opening, the call past break-even, commits;
  - the continuations below, by way;
  - the comparison with the repository's earlier windows: medians, ratio, a mark past
    1.5 times (taken from `study/session-review/`);
  - the flags and the obligations below.
- **How the work went on after a stop** (the user, 2026-10-12), the comparison the
  hand-over decision rests on. Three ways, each found in the transcripts:
  - a new session, opened from the hand-over note the report keeps: its opening, the
    calls up to its first edit, subagent or question;
  - the same session after its cache was lost, past the hour or on a change of
    organization, which rebuilds it alike: the rebuild, then the reads of the context
    carried beyond what a new session's opening holds, up to the same point;
  - the same session after a compaction, not tried yet: the compaction's call, then the
    calls up to the same point, on the summary's context.

  For each way, the times it happened, the median cost up to that point, and the cost of
  a later call, which the context carried sets. A way the window lacks is said, and the
  records of earlier windows supply it: the comparison builds up from phase to phase.
- **What it flags as having done harm**, each seen in the counts by hand:
  - runs lost: `claude -p` sessions that ended without their answer, a session limit or
    a stop, with their cost;
  - cache rebuilds, with their cause and cost (Phases 3 to 5: $8.50, $6.50, $2.74),
    each beside what a new session's opening cost in the window;
  - sessions past break-even: the reads of the context beyond the opening's passed the
    opening's cost and a review's, at a named call, with what a hand-over there would
    have saved;
  - a gap with `cost-state` past a cent and 1% for a model, in a session a record covers
    whole: the price table or an estimate is off;
  - a model the price table lacks;
  - tool reviews past their budget.
- **What it makes the agent conclude on**, printed as obligations (taken from
  `study/session-review/`): what the three largest costs bought, five without an earlier
  window; a finding or a reason for each flag; an explanation for each measure past 1.5
  times its median; what to change, as findings with a target and a fix in the tool
  reviews' kinds, the high ones put to the user and carried into a roadmap only on the
  user's word. No section for what went well.
- **The record.** In this repository, beside the tool reviews, whatever repository the
  window covers: `reviews/windows/<date>-<repo>-<name>.md`, in the tool reviews'
  format: the window, its sources and exclusions, the figures in a form a longer window
  adds up (per model, part, session, effort, rebuild and lost run), the findings, and
  prose of 300 words at most. Its script writes it from the agent's draft, measuring
  again as `record.py` does (T4).
- **A longer window.** The records of the same repository whose windows lie inside it
  are read in place of transcripts; the transcripts count the rest; `--recount` ignores
  the records. When a part counted from transcripts starts before the oldest transcript
  kept, the script says which part may be counted short, never in silence.

### From `study/session-review/`

Taken: the median of earlier reviews, the ratio and its mark past 1.5 times; obligations
printed by the script, the three largest costs, five without a baseline; the review's
own turns measured apart; high findings carried into a roadmap on the user's word; no
section for what went well; a budget for the review. Left: the ledger, since no hook
keeps the measures; one review per task, roadmap `session-review`'s; tokens alone, since
costs are API prices here (Decisions Taken At Opening).

### Shared Code

`shared/usage/` extended and `shared/sessions/` new; `reviewfile.py` moves to
`shared/reviewfile/`, since both skills write the format. The rule that prices a tool's
text, its characters carried as one one-hour write and a read by each later call, lives
in `shared/usage/` and takes the text of any tool, so that `session-review` prices a
repository's tools as `tool-review` prices this setup's; each review keeps finding its
own tools in the transcript. `make shared` copies `usage.py`
into `tool-review`, whose scripts and Stop hook read it, and `usage.py`, `sessions.py`
and `reviewfile.py` into `reviewing-token-usage`; `authoring-skills` keeps its `usage.py`;
`tools/reviews.py` imports from `tool-review`'s copies, as it does today. Each field of
the transcripts the reader starts to read — `subagents/`, `toolUseResult`,
`origin.kind`, `credential_org`, `cost-state` — gets its row in
`docs/claude-code-coupling.md` in the commit that adds it.

### Changes To The Tasks

Proposed with the design:
- The README's two uses: the cache rebuilds move from each tool review to the review
  of several sessions, which compares the three ways of going on after a stop (the user,
  2026-10-12); the reviews are processed and archived; the skill is named
  `reviewing-token-usage`.
- Phase 1, task 3: the message id goes to the transcript whose last record comes first,
  not to the first session that holds it. Task 2's proof adds a run whose last call's
  output comes from the Agent tool's result, and its excerpts a compaction. A task added
  before it: probe how a compacted session is recorded, 5 tasks to 6. The shared-code
  task follows Shared Code.
- Phase 2, task 1: no rebuilds; cost per model and effort, the tool's cost, the
  review's own turn written by the Stop hook, and `served`. Task 2 adds the line on the
  reviews' cost, the windows, the reviews waiting since the last archive and the
  proposals on the list. Three tasks added: the Stop hook reviews the tools the
  `[review]` table lists; it leaves out a tool version saturated with reviews;
  `--archive` moves the processed reviews and starts the counters again. 8 tasks to 11.
- Roadmap `session-review`, Phase 0: the boundaries above among its inputs; its design
  task decides whether `session-review` becomes the repository's side of one tool
  review, and reads the repository's tools from the same `[review]` key.

---

## Tasks

### Inputs
- [x] Read `docs/decisions/2026-10-06-token-costs.md`, `docs/decisions/2026-10-09-phase-4-token-costs.md` and `docs/decisions/2026-10-11-phase-5-token-costs.md`, the reader Phase 4 of `skill-tooling` delivered, and the review domain's `transcript.py`, `measure.py`, `record.py` and `tools/reviews.py`, and list what each measures today, what the records' method adds, and which open defect each touches
  Proof: review — the list, each item tied to a section of a record or a line of the code, approved by the user before the design

### Probes
- [x] Check how `cleanupPeriodDays` keeps the transcripts past 30 days: what Claude Code's documentation says it does, the value to set, the disk it takes at the present rate, and how it is set, the installer merging only hooks and permission rules into `settings.json`
  Proof: probe — the documentation read and cited with its date, the disk of `~/.claude/projects/` measured, about 29 MB a day on 2026-10-11, and the value and the way to set it put to the user
- [x] Probe how a phase's sessions are found: the window from the phase's opening commit to its closing commit, applied to the two latest closed phases whose transcripts remain, and the `claude -p` sessions those sessions started, whose transcripts sit in project folders of their own
  Proof: probe — each window computed from `git log`, the transcripts whose calls fall in it, compared with the sessions the phase's report names in its Work Log; a session shared with another roadmap, as `2f2e66de` was, counted as the design must then decide; the `claude -p` sessions found compared with those the phase's scripts recorded

### Design
- [x] Write the design from the two uses the measures serve, each measure kept tied to the decision it informs. The return on each tool: what a review's measured block holds (cost per model, subagents, effort, cache rebuilds, estimates marked, the review's own turn), and the tools `make reviews` flags, one costing past its median or costing while its reviews say it brought nothing. The review of several sessions: a skill of the review domain run by hand at the end of a phase, a roadmap or a stretch of work, how its window is given, what it flags as having done harm, and what it makes the agent conclude on. Also the price table and how it is kept current, the record the review of several sessions writes so that a longer window, a roadmap's, reads its phases' records rather than transcripts past 30 days, its warning when a window starts before the oldest transcript kept, what is taken from `study/session-review/`, and what a tool review itself may cost. Then get the user's approval
  Proof: review — the design, each part tied to the inputs' list and to the probes' results, approved before any code
- [x] Settle how the four open defects are fixed: `session_resume.py` not counted in a session it opened, a skill's files read through Bash not counted, the `make update` message of `measure.py:94` and `record.py:125`, and agent runs reported without their output tokens; then write the decision record under `docs/decisions/`
  Proof: review — one fix per defect, each with the test that will show it, then the record, approved by the user with its date

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-token-usage.md    new
```

### Dependencies
Roadmap `skill-tooling`, completed: the reader its Phase 4 wrote to count a run's tokens
and cost from its transcripts.

### Constraints
No change to the domain in this phase. No hook keeps the measures: the user judged
`SessionEnd` and Stop unreliable for it on 2026-10-11. The transcripts stay at Claude
Code's 30 days (the user, 2026-10-11): each measure is recorded when it is taken.
The review of several sessions is started by hand, never by a phase closure, so that
the roadmap and review domains stay independent. Transcripts are deleted 30 days
after their last write: a probe that reads a session's transcript runs within that time.
The defects come from two tool reviews of 2026-10-06 and from Phase 3 of `skill-tooling`.
`measure.py` reported no run of `session_resume.py` in a session that had started with
its line. It reported no file read where the session had read the roadmap skill's
references with `cat`. Agent runs carry fresh and cached tokens but no output. Phase 3's
report left the `make update` message open, as an instruction the agent must not follow
without the user's agreement.

Phase 4 of `skill-tooling` shows what the probe and the design meet
(`docs/decisions/2026-10-09-phase-4-token-costs.md`):
- Its sixteen main sessions started 218 `claude -p` sessions, $69.32 of the phase's
  ≈ $186.62. Their transcripts sit under `~/.claude/projects/` in folders named after
  the copy each ran in, `-tmp-skill-run-…`, `-tmp-skill-grade-…` and the like, not under
  the repository's folder. A phase's window on the repository's folder misses them.
- The Stop hook asked for 18 reviews in those sixteen sessions: 93 calls, about $6.09,
  against about $2.45 in Phase 3's five sessions. A review is asked once per tool and
  session, so its cost follows the number of sessions.

Phase 5 of `skill-tooling` adds (`docs/decisions/2026-10-11-phase-5-token-costs.md`):
- Its fourteen main sessions started 248 `claude -p` sessions, $103.57 of the phase's
  ≈ $158.54, in folders named `-tmp-skill-run-…`, `-tmp-skill-judge-…` and
  `-tmp-skill-trigger-…`. Its main sessions were matched to the phase by the commits
  each made.
- A conversation went on in a new process, under another session id, and copied the
  history it shared with the first: counting each message id once gave the shared part
  to the first session.
- The Stop hook asked for 15 reviews in fourteen sessions, ≈ $3.52, about $0.23 each: a
  second one in a session where a tool first served after the first review. A session
  waiting on background runs goes on in the review's turn once the review is recorded,
  so the end of the turn does not bound a review's slice.

---

## Acceptance Criteria

- [ ] The design and the fixes of the four defects are approved by the user
- [ ] The decision record is committed
