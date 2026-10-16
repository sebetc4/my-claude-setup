# Summary — token-usage

---

## Where We Started

On 2026-10-06 a tool review measured tokens and turns but no dollars, no model, no
effort, and no subagent outside its catalog. A session's, a phase's or a tool's cost was
known only through one-off analyses of the transcripts, three of them from 2026-10-06 to
2026-10-11, each with scripts written for the occasion, while the transcripts are deleted
after 30 days.

---

## Where We Landed

One reader of cost, `shared/usage/`, with its prices and estimates as data, and
`shared/sessions/`, which gives a window's working sessions, the `claude -p` sessions
given to them and its commits. Every tool review now carries its slice's cost by model and
effort, subagents and its own turn included, each tool's cost beside its median, and
whether the tool served. The tools reviewed are chosen by the `[review]` table, a
saturated tool version is left out, and processed reviews are archived. Review 0.3.0 and
roadmap 2.0.4 are installed but unreleased; their release is roadmap `lean-workflow`'s.
The review of several sessions was not built: `lean-workflow`'s Phase 0 measured the
workflow with the reader directly, and cut it.

---

## What Each Phase Delivered

- **Phase 0, Framing**: a design and `docs/decisions/2026-10-12-token-usage.md`, after
  five rounds with the user; the measures tied to two uses, the return on each tool and
  the review of several sessions; the transcripts kept at 30 days, each measure recorded
  when taken.
- **Phase 1, Usage Reader**: `shared/usage/` and `shared/sessions/`, checked against the
  records of `skill-tooling`'s Phases 4 and 5 and against `cost-state`, within a cent.
- **Phase 2, Reviews And Reports**: 4 of its 12 tasks, those on the tool reviews. It
  waited from 2026-10-13 behind `session-close`; its remaining tasks were moved to
  `lean-workflow` or cut on 2026-10-16, with Phase 3.

---

## What We Learned

- A measure is kept for the decision it informs; the reader served `lean-workflow`'s
  baseline within a day, where the skill planned around it never got built.
- Measured figures move a design: a token holds 2.6 characters, not 3.5; a run's output
  depends on its effort more than on its agent type; copies of a conversation need a
  rule to count each call once.
- Prices and estimates belong in data, so that a model or a price is one entry, not a
  code change.
- A phase that waits behind other roadmaps loses its reason: by its return, the
  questions it was answering had moved.

---

## What We Are Leaving Open

- Claude Sonnet 5.5's cache-read price: $0.10 a million in Claude Code's
  `total_cost_usd`, $0.20 in `usage.toml`.
- A copied compaction counted once on an assumption, until a continued compacted
  conversation is seen.
- `general-purpose` runs on the default output estimate, wrong both ways.
- `git-domain`'s Phase 3 still adds its tools to `tools.json`'s lists, which the
  `[review]` table replaced: for its Phase 0.
