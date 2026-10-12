# Roadmap: token-usage

---

## Status Indicators

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Done
- ⏸️ Blocked
- ⚠️ Needs Review

---

## Overall Progress

```
Phase 0  Framing                    🟢 ████████████████████ 100%  (5/5)
Phase 1  Usage Reader               🟡 ███████░░░░░░░░░░░░░  33%  (2/6)
Phase 2  Reviews And Reports        🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/11)
Phase 3  Validation And Release     🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  █████░░░░░░░░░░░░░░░  26%  (7/27)
```

**Current Phase:** Phase 1 — Usage Reader
**Blocked By:** —
**Next Milestone:** Phase 2 — Reviews And Reports

---

## Why This Roadmap Exists

The review domain asks a session that used a tool of this setup for a review, and
measures the slice it reviews: fresh and cached tokens, output, turns, and the tools that
served. It gives no cost in dollars. It counts no subagent but the agents of its catalog,
and those without their output. It records neither the model nor the effort.

So the cost of a session, a phase or a tool was known on 2026-10-06 only through a
one-off analysis of the transcripts (`docs/decisions/2026-10-06-token-costs.md`). That
analysis found about $167 for Phase 3 of roadmap `skill-tooling`, nearly half of it in
eval runs that no review measured; recounted with `cost-state`, $176.38. A second one, on
2026-10-09 (`docs/decisions/2026-10-09-phase-4-token-costs.md`), found about $187 for
Phase 4. $69 of it went to 218 `claude -p` sessions that the phase's scripts started,
each transcript in a project folder of its own: five one-off scripts gathered them and
gave each to the session that started it. A third, on 2026-10-11
(`docs/decisions/2026-10-11-phase-5-token-costs.md`), found about $159 for Phase 5, two
thirds of it in 248 `claude -p` sessions, and a subagent's output estimated eight times
too high for a read-only agent. The transcripts are deleted after 30 days, so a cost not
measured within that time is lost.

Those counts served because they ended in conclusions. They led to shorter sessions, and
to subagents and runs started against the credit left, so as to lose fewer runs. A
measure is there to improve a workflow, not only to give a figure. This roadmap has the
review domain review how the tools are used on both counts, how they work and what they
cost, for two uses:
- **The return on each tool.** Each tool review carries the slice's cost in dollars per
  model and effort, subagents included, and the tool's own cost, beside what the tool
  brought. The tools reviewed are those the user means to improve, listed in
  `.agent-conventions.toml`. `make reviews` gives each tool's cost, and flags a tool that
  costs too much or costs without serving; once the user has gone through them, the
  reviews are archived.
- **A review of several sessions.** `reviewing-token-usage`, a skill run by hand at the
  end of a phase, a roadmap or a stretch of work, measures its sessions, the `claude -p`
  sessions they started included. It shows what served where and when, compares the
  ways of going on after a stop, flags what did harm, and has the agent conclude on what
  to change.

The transcripts stay at Claude Code's 30 days. Each measure is recorded when it is
taken: a tool review in its session, a review of several sessions at the end of its
window, whose record a longer window reads.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-06:

- Measuring token consumption belongs to the review domain. The domain's aim becomes to
  review how this setup's tools are used: how they work and what they cost.
  `CLAUDE.md`, which calls the domain temporary, follows at the release.
- One reader counts tokens and cost: the one Phase 4 of `skill-tooling` writes for eval
  runs, extended here rather than written a second time.
- Costs are API prices per model, counted as `docs/decisions/2026-10-06-token-costs.md`
  counts them.
- An estimate is marked as one. A subagent's output tokens, which its transcript does
  not hold, are estimated and labelled, never mixed with counted figures.

---

## Deliberately Out Of Scope

- Counting the eval runs: Phase 4 of roadmap `skill-tooling`, whose reader this roadmap
  extends.
- When a phase hands over to a new session: Phase 0 of roadmap `roadmap-execution`,
  which these measures inform.
- A phase closure that starts the review of several sessions or writes a phase's cost
  into its report: the roadmap and review domains stay independent, and the review is
  started by hand.
- Bringing `study/session-review/` into this repository as a standard tool that reviews
  the tools a repository builds for itself: a roadmap of its own, to be created, which
  can share this roadmap's reader.
- Whether `session-review` and `tool-review` become one tool review with two catalogs,
  a repository's tools and this setup's: Phase 0 of roadmap `session-review`.
- A subscription's quota and its limits: costs stay API prices.
- Agents other than Claude Code: the transcripts and their `cost-state` records are
  Claude Code's, listed in `docs/claude-code-coupling.md`.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🟢 Done |
| 1 | [Usage Reader](phase-1-usage-reader.md) | 6 | 🟡 In Progress |
| 2 | [Reviews And Reports](phase-2-reviews-and-reports.md) | 11 | 🔴 Not Started |
| 3 | [Validation And Release](phase-3-validation-and-release.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `skill-tooling`: the reader its Phase 4 writes to count a run's tokens and
  cost from its transcripts, which this roadmap extends.

---

## Related Documentation

- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — the method, the figures and the prices this roadmap starts from.
- [Token costs of Phase 4, 2026-10-09](../../../decisions/2026-10-09-phase-4-token-costs.md) — the same method applied to a phase run in sixteen sessions and 218 `claude -p` sessions, and what it took by hand.
- [Token costs of Phase 5, 2026-10-11](../../../decisions/2026-10-11-phase-5-token-costs.md) — the same method on a phase of fifteen sessions with small contexts and 248 `claude -p` sessions, with what the reader's estimates and price table missed.

---

## Metadata

**Roadmap Status:** 🟡 In Progress
**Location:** `docs/roadmap/on-progress/token-usage/`
**Version:** 1.4.0
**Created:** 2026-10-06
**Last Updated:** 2026-10-12

---

## Changelog

### 1.4.0 (2026-10-12)

- Phase 0 closed. Delivered: the design, approved by the user, and the decision record
  `docs/decisions/2026-10-12-token-usage.md`, with one fix and one test for each of the
  review domain's four defects. Found: a window between two commits, each call counted
  by its time, finds a phase's sessions as the counts by hand did; the `claude -p`
  sessions are found by their first record; no kept transcript holds a compaction; the
  transcripts keep the path their session ran in. Moved: no task. The roadmap moves to
  `on-progress`; Phase 1 opens once the user has settled the move and rename of this
  repository.

### 1.3.0 (2026-10-12)

- Phase 0's design approved by the user on 2026-10-12. Every cost is broken down by
  model and effort. A tool review carries the tool's own cost and whether it served; the
  tools reviewed are the ones a `[review]` list names, a tool version saturated with
  reviews is left out, and the reviews, once processed with the user, are archived. The
  cache rebuilds move to the review of several sessions, the skill
  `reviewing-token-usage`, which compares a hand-over note and a new session with a
  session whose cache was lost and with a compaction.
- Phase 1 gains a probe of how a compaction is recorded, 5 tasks to 6. Its tasks follow
  the design: prices with their source, a run's last output from the Agent tool's result,
  a shared message id given to the transcript whose last record comes first, a window's
  calls counted by their time, `reviewfile.py` shared. Its Objective adds the compactions.
- Phase 2 gains three tasks, the list of tools reviewed, the saturation and the archive,
  8 tasks to 11. Its Objective, its measured block, `make reviews`, script and skill
  tasks, its files, constraints and acceptance criteria follow.
- Out of scope: whether `session-review` and `tool-review` become one tool review,
  decided in roadmap `session-review`, whose Phase 0 gains the boundaries.

### 1.2.0 (2026-10-11)

- The transcripts stay at Claude Code's 30 days, as the user decided on 2026-10-11,
  replacing the `cleanupPeriodDays` raised of 1.1.0: a tool review measures in its
  session, a review of several sessions at the end of a phase, and phases last 0 to 3
  days, the longest roadmap 14. A longer window reads the records of the reviews it
  spans. Phase 0's task 2 ends on that decision; its design task covers the record and
  the warning on a window older than the transcripts kept. Phase 2's Objective drops
  the transcripts kept past 30 days and its script task gains the record and the
  warning; the task setting `cleanupPeriodDays` is removed, 9 tasks to 8.

### 1.1.0 (2026-10-11)

- Phase 0 opened. The roadmap is recentred on what the measures are for, as the user
  decided on 2026-10-11: a measure leads to a conclusion that improves a workflow. Two
  uses replace the four outcomes: the return on each tool, read by `make reviews`, which
  flags a tool that costs too much or costs without serving; and a review of several
  sessions, a skill of the review domain run by hand, never by a phase closure. The cost
  command becomes that review's script.
- The transcripts are kept through `cleanupPeriodDays` raised, the `SessionEnd` and Stop
  hooks being judged unreliable for it: Phase 0's probe of the hooks becomes a check of
  `cleanupPeriodDays`, and Phase 2's task on keeping the measures becomes setting it.
  Every project is measured.
- Phase 0's Objective and its design task follow the two uses. Phase 1 counts a window
  of sessions, a phase's among them. Phase 2's Objective, its `make reviews` task and its
  Out of Scope change; it gains the task that writes the skill, 8 tasks to 9. Phase 3
  recounts with the review's script and sets its conclusions beside a record's.
- Out of scope: bringing `study/session-review/` into this repository, a roadmap of its
  own to be created.

### 1.0.4 (2026-10-11)

- Phase 3 releases the review domain as 0.3.0, tagged `review-v0.3.0`: the domain
  reached 0.2.0 and 0.2.1 during Phase 5 of roadmap `skill-tooling`, so the 0.2.0 this
  roadmap targeted is already taken. The task, its proof and the acceptance criterion
  follow. No task added or removed.

### 1.0.3 (2026-10-11)

- The third count by hand, `docs/decisions/2026-10-11-phase-5-token-costs.md`, joins the
  first two: Phase 0 reads it, and its constraints add how Phase 5's sessions were found
  and what its reviews cost. Phase 1's constraints add the subagent output estimate eight
  times too high for `skill-auditor`, Claude Haiku 5.5's fitted price and the Opus calls
  no transcript holds. Phase 3's constraints add Phase 5's count as a second reference,
  its transcripts deleted from 2026-11-08. No task added or removed.

### 1.0.2 (2026-10-11)

- Unblocked: roadmap `skill-tooling` closed on 2026-10-11, its Phase 4 having delivered
  `shared/usage/`, the reader this roadmap extends. `Blocked By` is cleared; nothing else
  changes.

### 1.0.1 (2026-10-09)

- The second count by hand, `docs/decisions/2026-10-09-phase-4-token-costs.md`, joins
  the first: Phase 0 reads both, and its probe and Phase 1's selection of a phase's
  sessions include the `claude -p` sessions a phase starts. Phase 0's design also settles
  what a review may cost, one review a session having cost about $0.34 in Phase 4 of
  `skill-tooling`. Phase 1's constraints add the Haiku calls no transcript holds and the
  model the price table lacks; Phase 3's, how long Phase 4's count serves as a reference.
  No task added or removed.

### 1.0.0 (2026-10-06)

- Roadmap created with four phases: Phase 0 Framing, Phase 1 Usage Reader, Phase 2
  Reviews And Reports, Phase 3 Validation And Release. It waits for roadmap
  `skill-tooling`, whose Phase 4 writes the reader it extends. Each task declares its
  proof, approved by the user.
