# Phase 2 Report: Reviews And Reports

**Phase:** [phase-2-reviews-and-reports.md](phase-2-reviews-and-reports.md)
**Start Commit:** 2c2081e

---

## Work Log

### 2026-10-12

Phase opened in a new session, as Phase 1's closure planned. Read `phase-1-usage-reader.md`
and `phase-1-usage-reader-report.md` in full. Phase 1's report holds no restructuring
pending approval; no other phase is in progress; `Blocked By` is empty. The Start Commit
is Phase 1's closing commit.

Carried into this phase:
- The measured block of task 1 reads the slice through `usage.calls()`, already copied
  beside `transcript.py` in `tool-review`, a call's time being its first record's; the
  slice count of `transcript.py` still keeps each message's first record, whose output is
  the stream's first figure.
- `reviewing-token-usage` takes its window from `sessions.window()`. `tools/shared.py
  <skill>` copies every shared module into a new skill, which the audit then refuses as
  unread: `usage`, `sessions` and `reviewfile` are copied by hand, and `make shared`
  keeps them.
- Phase 1's decisions bind the counts: prices and estimates are data in `usage.toml`; a
  run's output is estimated by agent type and effort and marked; a compaction's call is
  derived and marked; a text is priced at 2.6 characters a token; a call held by several
  transcripts goes to the one whose record of it comes first; a repository's working
  sessions are its project folder's transcripts a person prompted; a span runs from a
  session's first call to its last record.
- Left to the review of several sessions, beside `cost-state`: `general-purpose` runs on
  the default estimate, 5,400 a call, wrong both ways; a web search's $0.01, not counted;
  the probe `927b9ad1`'s record at twice the table's price.
- Skill-tooling 0.1.2 and review 0.3.0 are open, `— unreleased`: each change to the
  review domain adds to 0.3.0's changelog entry, each change to `shared/usage/` to
  0.1.2's, and each transcript field newly read goes to `docs/claude-code-coupling.md`.
- The transcripts the checks on real data read are deleted: Phase 4's from about
  2026-11-05, Phase 5's and the continued pair's from about 2026-11-08, `bbaa7e41` about
  2026-11-11.

Task 1, the measured block, before its test. Read Phase 0's `## Design` and
`docs/decisions/2026-10-12-token-usage.md`, then `transcript.py`, `measure.py`,
`record.py`, the Stop hook, `reviewfile.py` and their tests. Calibrated on this session's
first review, `3936fdd7`, read through `shared/usage/`: its slice holds 12 calls of
Claude Opus 5.5 at `xhigh`, $0.757; the review's own turn, from the Stop to the call after
`record.py`, 5 calls, $0.192, within the $0.25 budget; the roadmap skill's load, 6,799
characters, 2,615 tokens, $0.026 over the 11 calls after it. `usage.session()` reads the
largest transcripts kept, 23 MB and 2,854 lines, in 0.03 to 0.06 s: the Stop hook can
afford it. Main threads hold their final usage: 5 of 5,616 calls in this repository's
transcripts lack it.

Put to the user, the block's shape: `cost` with the prices' date, the slice's dollars and
the estimated part, `main` and `subagents` by model then effort; `derived.tool_cost`, each
tool's tokens and dollars with its rule; `review`, the review's own turn, written by the
Stop hook. And the choices under it: calls counted by their time; `tokens`, `turns` and
the peak read through `usage.calls()`, a call without its final usage adding no output to
`tokens`; a tool's text read until the next compaction; the median over the same tool
version's earlier reviews, three at least; `served` beside `brought` in the draft;
decimals in the review format; `usage.Run` carrying its `toolUseId`. The user asked for
the effort of every model that uses one: over the transcripts kept, Claude Haiku 4.5's 239
calls carry none, Claude Opus 5 has 228 without among its efforts. So every breakdown,
the agent's cost and the review's turn included, goes by model then effort; a model whose
calls carry no effort takes its figures directly, and a call without one beside calls
with one goes under `none`.

Task 1, tests first. In `shared/reviewfile/tests/test_reviewfile.py`, decimals read back
in flow and block style, written without an exponent, a string of digits kept a string, a
number not finite refused; in `shared/usage/tests/test_usage.py`, a run carrying the
Agent call that started it. Red: 3 errors. Then `reviewfile.py` writes and reads decimals,
`usage.Run` gains `tool_use` from the `.meta.json`'s `toolUseId`; `make shared`.

The review domain's test world, `review_world.py`, writes what 2.1.296 writes: a reply
with its model, effort and `stop_reason`; a run's calls on Claude Sonnet 5.5 with the
stream's first usage, its Agent result holding the last call's final usage; a
compaction's boundary; a hook's block with its reason. The existing 68 tests pass on it.
The figures of the new tests are worked out in the tests from the table's rates, never
from `usage.cost()`, so that a repricing changes no test. Tests: in `test_transcript.py`,
the slice's cost by model and effort, main thread and subagents apart, two runs at
`medium` and `max`; a model without effort, and a call without one beside `xhigh` under
`none`; a model the table lacks named and left out of the dollars; the token counts from
each call's final usage, a streamed call and an interrupted one; a compaction's call in
the cost alone, estimated; each tool's own cost, a hook's text held by six calls, a
skill's load, a file read and a script's output, an agent's runs; a text read until the
next compaction, a block's reason as a text; the review's own turn up to the call after
`record.py`, a failed `record.py` passed over, or to `closed`. In `test_measure.py`,
`measure.py` on a session with two subagents at two efforts and six earlier reviews:
each tool's cost, its median over the three of its version, a review of another version
and a skipped one left out, the ratio and the explanation owed. In `test_record.py`, a
draft without `served`, with a string for a tool, a wrong `served`, an empty `brought`,
an unknown key. In `test_hook.py`, a complete review given its own turn, four calls, the
conversation's next call left out; a skipped review given none. Red: 9 in
`test_transcript.py` (output 4 counted where the final usage says 50, `cost` and
`review_turn` missing), the line of costs in `test_measure.py`, every valid draft refused
in `test_record.py`, `review` missing in `test_hook.py`.

Then `transcript.py`: `measure()` reads the slice through `usage.session()`, each call by
its time, `tokens`, `turns` and the peak from the main thread's recorded calls, `cost`
from `slice_cost()`, `derived.tool_cost` from each tool's texts, priced by `text_cost()`
on the calls that hold them up to a compaction, and an agent's runs matched by
`toolUseId`; `review_turn()`. `measure.py` reads the earlier reviews' `tool_cost`, prints
each tool's cost on its line under "tools under review" with its median from three
reviews of its version, and owes an explanation past 1.5 times; `record.py` checks
`brought` and `served`; the Stop hook writes `measured.review` when it closes a complete
review. One old expectation changed: the tool's line now carries its cost. 80 tests of
the domain pass, and `make check`.

Checked on this session's first review, `3936fdd7`, its slice measured again: 30 lines of
block, $0.7566 for 12 calls at `xhigh`, the roadmap skill's own cost 4,612 tokens and
$0.0455 (its load and its scripts' output, the first `conventions.py` command holding a
`cat` of `open-phase.md`), and the review's turn 5 calls for $0.1919, the figures of the
calibration. Timed on the longest transcripts kept: `measure()` 0.15 s on 7 MB with three
tools, `review_turn()` 0.07 s, which the Stop hook adds once per complete review. The
rule printed with `tool_cost` was cut from four lines to two.

`SKILL.md` of `tool-review` changed with `authoring-skills`: the draft's tool entry holds
`brought` and `served`, `served` defined, measure.py's output naming the tools' cost; the
audit gives no error and no warning. `references/format.md` documents `served`, `cost`,
`derived.tool_cost` and `review`, its example read back by `reviewfile.py`.
`docs/claude-code-coupling.md`'s review row names what `transcript.py` now reads; review
0.3.0's and skill-tooling 0.1.2's changelogs the change. Task 1 ticked.

---

## Decisions

- **Every cost of a review is broken down by model, then by effort where the model uses
  one** (the user, 2026-10-12): the slice's main thread and subagents, an agent's own cost
  and the review's turn. A model whose calls carry no effort, as Claude Haiku 4.5, takes
  its figures without an effort level; a call without an effort beside calls with one goes
  under `none`.
- **A slice's calls are counted by their time; an agent's own cost by its runs**
  (2026-10-12): `cost` takes each call of the main thread and the subagents whose time
  falls in the slice, as `sessions.window()` does; `tool_cost` takes every call of the
  runs started by an Agent call of the slice, a background run's later calls included.
- **A tool's text is read until the next compaction** (2026-10-12), whose summary
  replaces it: the compaction's derived call is the last to read it. A hook's block
  reason is a text it gave, priced with its injected text.
- **A tool's cost is set beside the median of its version's earlier reviews, from three**
  (2026-10-12): the explanation owed past 1.5 times asks about this session, not the
  version, whose change in cost `make reviews` flags (task 5).
- **`tokens`, `turns` and the context peak take each call's final usage**: the measured
  block of the reviews written before kept the stream's first output, smaller. Their
  `tokens.output` is not compared with the new ones; `make reviews` reads the dollars of
  the new block only.

---

## Files Changed

---

## Problems And Deviations

- **`tool-review`'s `SKILL.md` changed without an eval run**: the skill has no evals, and
  the change only states what `record.py` now checks, whose test is the task's proof; the
  audit is clean. The first review written with the installed new version, after
  `make update`, shows whether the agent fills `served`.

---

## Changes To Later Phases

---

## Assessment
