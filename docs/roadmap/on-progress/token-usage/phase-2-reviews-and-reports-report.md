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
0.3.0's and skill-tooling 0.1.2's changelogs the change. Task 1 ticked, committed with the
phase's opening as `5a8d77e`.

Put to the user and left open: installing the change, `make update D=review` and
`D=skill-tooling`, whose copy of `usage.py` changed too, so that the next reviews are the
first to carry dollars and `served`. Not done: the installed copies under `~/.claude`
are still review 0.2.2 and skill-tooling 0.1.1, whose `record.py` takes a tool's
`brought` as a string. The session ends here, at the user's word, to resume in a new one.

**Where the next session starts:**
1. Ask the user first whether to run `make update D=review` and `make update
   D=skill-tooling` on the real `~/.claude`, never run without the user's word. Until it
   runs, every review keeps the old block: no `cost`, no `tool_cost`, no `served`, so
   `measure.py`'s medians stay empty and task 5 has no dollars to read.
2. Task 2, the tools reviewed chosen by the `[review]` table of the setup repository's
   `.agent-conventions.toml`, read by its path, the repository the installer's state
   names, never by climbing from the session's directory; `tools.json` keeps only the
   points to watch. The table's copy of `shared/conventions/` goes into `tool-review`'s
   `scripts/` by hand, as Phase 1's task 7 did, so that the audit finds a reader for it.
3. Tasks 3 and 4, the saturation and the archive, then task 5, `make reviews`: it reads a
   tool's dollars from `measured.derived.tool_cost.value.<tool id>.dollars`, a review's
   own from `measured.review.dollars`, `served` from each tool entry; the reviews written
   before have none of them and stay readable.
4. Tasks 6 and 7, `reviewing-token-usage`: its script on the copies of `shared/usage/`,
   `shared/sessions/` and `shared/reviewfile/`; `transcript.py`'s `part()`,
   `by_model()` and `slice_cost()` give the breakdown by model then effort it can take
   up or move to `shared/usage/`.
5. The defects, tasks 8 to 11. D1: `session_start()` still takes the first timestamped
   record. D2: a file read through `cat` or `sed` adds to `files_read` and, through
   `texts_of` in `measure()`, to the skill's `tool_cost`. D3: the `make update` message,
   still in `measure.py` and `record.py`. D4: an agent's `setup` runs still lack their
   output; its `tool_cost` already prices its runs, the output estimated.
- The review domain's tests end a slice at the world's clock with `request_at_clock()`:
  the world's records run an hour behind the real time the Stop hook stamps.
- Each change to the review domain adds to review 0.3.0's changelog entry, each to
  `shared/usage/` to skill-tooling 0.1.2's, each transcript field newly read to
  `docs/claude-code-coupling.md`.

### 2026-10-13

Resumed in a new session. Read the phase file and this report in full, then Phase 0's
design of the `[review]` table. Put to the user the two choices the last session left:
installing now, and what the table lists. The user chose to install now, an update after
each change to the hook, and the table as today, `tools = ["roadmap", "skill-tooling"]`.
`make enable` of both domains into a temporary Claude directory, then `make update
D=review` and `D=skill-tooling` on `~/.claude`: `make list` shows review 0.3.0 and
skill-tooling 0.1.2 installed, so the next reviews carry dollars and `served`.

Task 2, the tools reviewed by choice. The reader of the table is `shared/conventions/`,
the one source for `.agent-conventions.toml`: `[review]` joins its tables, with one key,
`tools`, required, a list of strings. Tests first: in `test_conventions.py`, the table
resolved, `tools = []` valid, the table without `tools` and `tools = [1]` refused, and the
procedure's test then wanting `tools` documented; red, 4. In the review domain, the test
world writes the repository's `.agent-conventions.toml` with its `[review]` table, a
`tools.json` holding `watch` alone, and a second domain installed, skill-tooling's skill,
agent and hook. In `test_transcript.py`, the installed tools every domain's but the review
domain's; an entry naming a tool id or a domain; the table read from the repository, `[]`
for a file missing, a table missing, empty, misnamed, of the wrong type or not TOML; a tool
the table does not list ignored; `tool-review` never under review, even listed. In
`test_hook.py`, a table naming `roadmap` and `agent:skill-auditor` in a session that used
four tools: the request names those two; no request without the table or with `tools =
[]`; the project's own `.agent-conventions.toml` never read, the repository's read at the
next Stop; a review requested measured whole at its skip after its tool left the table;
the error logged now from a broken install state, since the hook no longer reads
`tools.json`. In `test_measure.py`, `measure.py` measuring a requested review whole after
its tool left the table. In `test_tools_json.py`, `watch` alone, each watched tool a
skill, agent or hook of a domain. Red across the domain.

Then the code. `transcript.py` loses `load_catalog()` and `catalog()` for three functions:
`installed(state)`, every tool this repository installed, from the installer's state, the
review domain's left out; `reviewed(repo)`, the table's tools, read by its path through
the copy of `conventions.py`, `[]` unless it reads `ok`; `chosen(catalog, entries)`, the
tools an entry names by id or by domain. The Stop hook measures with `installed()` and
asks with `chosen(installed(), reviewed(repo))`; `measure.py` and `record.py` measure
with `installed()`. `tools.json` keeps `watch`. `shared/conventions/conventions.md`
documents `tools` under The Keys and Where To Look. `make shared` refreshed the copies in
`roadmap` and `authoring-skills`; `tool-review` took `scripts/conventions.py` and
`references/conventions.md` by hand, both files, since `tools/shared.py` checks every file
of a module a skill holds. The audit then refused `references/conventions.md` as reached
by no file: `SKILL.md` of `tool-review`, edited with `authoring-skills`, names both in The
Scripts, as the hook's reader of the table, read by no review; a citation, so the audit
alone is its proof, clean. 85 tests of the domain pass, 55 of `shared/conventions/`, and
`make check`. Two of the new tests were wrong first, not the code: the measured block
writes a tool's setup in flow style, and `tools = [1]` sits on line 12.

Timed: the table read and the catalog, 0.07 ms a Stop on the real install state; the
selection over this session's transcript, 1.3 MB, 3 ms. Wrote the table into this
repository's `.agent-conventions.toml`, `conventions.py review` printing `status: ok`: it
chooses nine tools, the two agents `skill-grader` and `skill-comparator` among them, which
`tools.json` did not list. `make update D=review` and `D=skill-tooling` again, tried
first in a temporary directory: the installed hook reads the table from the next Stop.

The copy of `conventions.py` changed in the roadmap domain, released and tagged at 2.0.3:
`VERSION` 2.0.4 with a `— unreleased` entry, not installed, `make list` showing it
`outdated`. Review 0.3.0's and skill-tooling 0.1.2's changelogs say the change;
`docs/claude-code-coupling.md`'s row on the install state says the review domain reads
the tools it installed there, `installed` beside `load_state`; `CLAUDE.md`'s lines on
`shared/conventions/`, `.agent-conventions.toml` and the review domain name the table in
place of `tools.json`'s lists. Task 2 ticked, committed as `be8c614`.

Task 3, the saturation, on the user's word after task 2. Timed first: reading the 105
reviews of `reviews/` takes 10 ms, so the Stop hook can read them all, and only once it
has tools to ask for. The rule goes into `shared/reviewfile/`, beside the reader of the
fields it uses, so that `tools/reviews.py` can take it up through `tool-review`'s copy.
Tests first, in `test_reviewfile.py`: ten complete reviews whose last five raised only
pairs seen before, or none; nine not enough; a new target or a new kind in the last five;
the earlier ones every review before the last five, twelve given; the last five by their
slices whatever the order given; only the complete reviews of that tool version, a review
of another version, of another tool, skipped or requested not counted; `listed()`, the
readable reviews directly under the folder, neither under `archive/` nor a draft nor an
unreadable file. In `test_hook.py`: ten past reviews of `skill:roadmap` at the installed
version leave it out of a request that keeps `session_resume.py`; with no other tool, no
request; the next version, the same ten under `reviews/archive/2026-10-13/`, or nine
reviews, each asked for again. Red: `listed` and `saturated` missing, and the hook asking
for the saturated version; the three cases asked for again passed already, as guards.

Then `reviewfile.py` gives `listed()` and `saturated()`, with `SATURATION = 10` and
`RECENT = 5`; the Stop hook drops a saturated tool from the tools it would ask for.
`make shared` refreshed `tool-review`'s copy. 26 tests of `shared/reviewfile/` pass, the
review domain's, and `make check`. On the real reviews, no version is saturated:
`skill:roadmap` 2.0.3 holds 8 complete reviews, its last five raising 5 findings, and the
2.0.0 versions, 57 reviews of `session_resume.py`, are no longer installed; the rule over
every version takes 0.6 ms beside the 10 ms of reading. Task 3 ticked, committed as
`0dca000`; `make update D=review`, tried first in a temporary directory.

Task 4, the archive, on the user's word. The findings of `make reviews` and the saturation
already read only the files directly under `reviews/`; what was missing was the move, and
the medians reading the archive. Chosen before the tests: `--archive` prints the same
report, then moves the reviews it read, so that what is archived is what was printed;
only the closed ones, since a review not closed yet belongs to a session whose Stop hook
still looks for it directly under `reviews/`; drafts, unreadable files and `errors.log`
stay. Tests first. In `tests/test_reviews.py`: two closed reviews moved into
`reviews/archive/<today>/`, a requested one and a complete one not closed kept, with the
draft, the unreadable file and the log; nothing to archive, no folder made; ten closed
reviews saturating a version, archived, then one more: no finding left, no saturation,
the tool's row counting one review and its median over the eleven. In `test_measure.py`,
the median over three reviews of a version, two of them archived. Red: `--archive`
unknown, the median over one review.

Then `reviewfile.py` gives `archived()`, the readable reviews under `archive/*/`, beside
`listed()`, both through `readable()`; `measure.py`'s `earlier_costs()` reads both;
`tools/reviews.py` gains `archive()` and `--archive`, and `tool_rows()` counts the
reviews not archived and takes its median over both. Reading the code back, a review
already in the archive under the same name would have been counted among the reviews not
closed: a test for it, red, then the line names it apart and leaves the review in place.
20 tests of `tests/test_reviews.py` pass, the domain's, and `make check`; `make reviews`
prints as before on the 106 real reviews. None archived: the design archives them once
gone through with the user. `CLAUDE.md` names `reviews/archive/<date>/` and the command;
review 0.3.0's changelog the change. Task 4 ticked, committed as `ce8469a`;
`make update D=review`, tried first in a temporary directory.

The session ends here, at the user's word, to resume in a new one. Installed on
`~/.claude`: review 0.3.0 and skill-tooling 0.1.2 as of `ce8469a`, the Stop hook reading
the `[review]` table and leaving saturated versions out; roadmap still 2.0.3, its 2.0.4
copy of `shared/conventions/` waiting for the user's word. This session's tool review,
`reviews/2026-10-13-0f584561-session-resume.md`, raised one finding: the dev hook
`.claude/hooks/check-skills.py` repeats the same failure list after every command of a
red step.

**Where the next session starts:**
1. Go through the reviews with the user, as the design's Processing The Reviews says:
   `make reviews`, its findings by recurrence, each carried into a roadmap or set aside
   on the user's word, then `python3 tools/reviews.py --archive`. `make reviews` still
   prints task 4's columns: the median in characters, no dollars, no flag, which task 5
   brings.
2. Hear the user's feedback on `authoring-skills`, announced at this session's end and
   not yet given.
3. Then task 5, `make reviews` in dollars: a tool's dollars from
   `measured.derived.tool_cost.value.<tool id>.dollars`, a review's own from
   `measured.review.dollars`, `served` from each tool entry, the reviews written before
   0.3.0 holding none of them; the medians read `reviewfile.archived()` too; the
   `[review]` table reported missing, empty or invalid with its problems, through the
   copy of `conventions.py`; the reviews waiting since the last archive.
- Still put to the user and unanswered: installing roadmap 2.0.4 with `make update
  D=roadmap`; rewording the tasks of `roadmap-execution`, `git-domain` and
  `working-method` that add tools to `tools.json`'s lists.
- Each change to the review domain adds to review 0.3.0's changelog entry, and is
  installed with `make update D=review` after a try in a temporary directory, the user
  having agreed on 2026-10-13 to an update after each change to the hook.

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
- **The tools measured are every tool installed; the `[review]` table chooses only what
  the Stop hook asks for** (2026-10-13): a review requested is measured whole after its
  tool leaves the table, a review the user asks for with `/tool-review` covers every
  installed tool, and the review domain's own tools are never reviewed, listed or not.
- **The `[review]` table is a table of `shared/conventions/`** (2026-10-13), its key
  `tools` required: one reader validates the whole file. Every skill holding a copy
  changes with it, the roadmap domain's included, 2.0.4.
- **A table missing, empty or invalid asks for no review and logs nothing** (2026-10-13):
  it is no error of the hook's; `make reviews` says so, with the problems (task 5).
- **Saturation reads every finding of a review, whatever tool it targets** (2026-10-13):
  a finding is a kind and a target, a file, which names no tool; a review of two tools
  whose other tool raises new findings keeps both asked for, the cautious side. The
  reviews not archived are those directly under `reviews/`, ordered by their slices'
  ends; task 4's archive moves them under `reviews/archive/<date>/`, which
  `reviewfile.listed()` does not read.

---

## Files Changed

---

## Problems And Deviations

- **`tool-review`'s `SKILL.md` changed without an eval run**: the skill has no evals, and
  the change only states what `record.py` now checks, whose test is the task's proof; the
  audit is clean. The first review written with the installed new version, after
  `make update`, shows whether the agent fills `served`.
- **The roadmap domain changes in this phase**, unplanned: its copy of
  `shared/conventions/` gains the `[review]` table. `VERSION` 2.0.4, unreleased; its
  release and install join Phase 3's tasks.
- **Two agents come under review that `tools.json` did not list**, `skill-grader` and
  `skill-comparator`, since the table names the skill-tooling domain whole. Started by
  `claude -p` sessions, which the hook leaves unattended, they are seldom asked for.
- **Three pending roadmaps name `tools.json`'s lists in a task**: `roadmap-execution`'s
  Phase 3, `git-domain`'s Phase 3 and `working-method`'s Phase 3 add their tools to
  `domains/review/hooks/tools.json`. Left as they are, other roadmaps' files, and put to
  the user: with the table, a new domain is reviewed once its name is added to the
  `[review]` table, and a new tool of a listed domain without any change.

---

## Changes To Later Phases

- `phase-3-validation-and-release.md`: the release task adds the roadmap domain, 2.0.4,
  and its tag `roadmap-v2.0.4`; the install task adds `make update D=roadmap`. The roadmap
  domain's copy of `shared/conventions/` changed in task 2.
- `phase-2-reviews-and-reports.md`, this phase's task 5: `make reviews` also reports the
  `[review]` table missing, empty or invalid, with its problems, as the design says.

---

## Assessment
