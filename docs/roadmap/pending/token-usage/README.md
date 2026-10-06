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
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 1  Usage Reader               🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Reviews And Reports        🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/8)
Phase 3  Validation And Release     🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/23)
```

**Current Phase:** —
**Blocked By:** roadmap `skill-tooling`
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

The review domain asks a session that used a tool of this setup for a review, and
measures the slice it reviews: fresh and cached tokens, output, turns, and the tools that
served. It gives no cost in dollars. It counts no subagent but the agents of its catalog,
and those without their output. It records neither the model nor the effort.

So the cost of a session, a phase or a tool was known on 2026-10-06 only through a
one-off analysis of the transcripts (`docs/decisions/2026-10-06-token-costs.md`). That
analysis found about $167 for Phase 3 of roadmap `skill-tooling`, nearly half of it in
eval runs that no review measured. The transcripts are deleted after 30 days, so a cost
not measured within that time is lost.

This roadmap has the review domain review how the tools are used on both counts: how
they work, and what they cost.
- Each review carries the slice's cost in dollars per model, subagents included, with
  the effort and the cache rebuilds.
- `make reviews` gives each tool's cost in dollars.
- A command gives the cost of a session, a phase or a roadmap.
- The measures outlive the transcripts.

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
- Writing a phase's cost into its report at closure: the roadmap skill's, proposed to
  roadmap `roadmap-execution` once the command exists.
- A subscription's quota and its limits: costs stay API prices.
- Agents other than Claude Code: the transcripts and their `cost-state` records are
  Claude Code's, listed in `docs/claude-code-coupling.md`.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 5 | 🔴 Not Started |
| 1 | [Usage Reader](phase-1-usage-reader.md) | 5 | 🔴 Not Started |
| 2 | [Reviews And Reports](phase-2-reviews-and-reports.md) | 8 | 🔴 Not Started |
| 3 | [Validation And Release](phase-3-validation-and-release.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `skill-tooling`: the reader its Phase 4 writes to count a run's tokens and
  cost from its transcripts, which this roadmap extends.

---

## Related Documentation

- [Token costs, 2026-10-06](../../../decisions/2026-10-06-token-costs.md) — the method, the figures and the prices this roadmap starts from.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/token-usage/`
**Version:** 1.0.0
**Created:** 2026-10-06
**Last Updated:** 2026-10-06

---

## Changelog

### 1.0.0 (2026-10-06)

- Roadmap created with four phases: Phase 0 Framing, Phase 1 Usage Reader, Phase 2
  Reviews And Reports, Phase 3 Validation And Release. It waits for roadmap
  `skill-tooling`, whose Phase 4 writes the reader it extends. Each task declares its
  proof, approved by the user.
