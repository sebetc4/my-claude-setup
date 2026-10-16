# Phase 1 Report: Usage Reader

**Phase:** [phase-1-usage-reader.md](phase-1-usage-reader.md)
**Start Commit:** 9859dd4

---

## Work Log

### 2026-10-12

Phase opened. Read `phase-0-framing.md`, its `## Design` included, and
`phase-0-framing-report.md` in full, then `docs/decisions/2026-10-12-repository-move.md`.
Phase 0's report holds no restructuring pending approval; no other phase is in progress;
`Blocked By` is empty.

The move and rename of this repository, which Phase 0's Assessment put before this
phase, are done: moved to `/code/ai/my-agent-setup` (`6ba2a7e`), content renamed
`my-agent-setup` (`34acf5b`), recorded (`9859dd4`). The Start Commit follows both, as the
move's record asked.

Carried into this phase:
- The design binds every task: prices with their date and source, Claude Haiku 5.5
  fitted at $0.10 and $0.50; subagent output estimated per agent type, `skill-auditor`
  640 tokens, any other 5,400, a run's last output from `toolUseResult.usage`; effort per
  call; cache rebuilds with their cause; a shared message id given to the transcript
  whose last record comes first; a window's calls counted by their time, `claude -p`
  sessions found by their first record, never by `.eval-runs/` alone.
- Left open by Phase 0 and named in both records' When To Revisit: this repository's
  sessions from before the move sit in the renamed project folder
  `-code-ai-my-agent-setup`, but their records keep `cwd` `/code/claude/my-claude-setup`;
  19 folders of `claude -p` runs keep their old names. The window's selection, task 5,
  takes it up: a repository's sessions found by project folder, not by `cwd` alone.
- No kept transcript holds a compaction: task 1 probes one before the count's test.

Task 1, the probe of a compaction. The user had compacted by hand, with `/compact`, the
session that closed Phase 0, `bbaa7e41`, before the move: one compaction, at
2026-10-12 11:14:17 UTC, written by the VS Code extension's Claude Code 2.1.296.
`compact_boundary` and `isCompactSummary` searched under `~/.claude/projects/`: this
transcript alone holds them (two others name them in text). What it records, in order:
- Line 745, `type` `system`, `subtype` `compact_boundary`, `content` "Conversation
  compacted", `parentUuid` null and `logicalParentUuid` the last record before it, the
  previous turn's `stop_hook_summary`. `compactMetadata`: `trigger` `manual`, `preTokens`
  291,810, `postTokens` 11,535, `cumulativeDroppedTokens` 280,275, `durationMs` 73,003,
  and `preservedSegment` / `preservedMessages`, the uuids of the last turn's answer kept
  after the summary.
- Line 746, a `user` record with `isCompactSummary` true and `isVisibleInTranscriptOnly`
  true, the summary as a string of 16,768 characters, dated 12 ms before the boundary.
- Lines 747 to 749, the command as the user typed it: `<local-command-caveat>`,
  `<command-name>/compact</command-name>`, `<local-command-stdout>Compacted`, the first
  two dated 11:13:04.625, when the command started, 73 s before the boundary.
- Lines 750 to 756, attachments that rebuild the context: `compact_file_reference` (the
  report), `file` (the decision record, 9,028 characters), `invoked_skills` (10,911),
  `deferred_tools_delta`, `agent_listing_delta`, `environment`, `model`.
- No `assistant` record for the compaction's call: the transcript does not hold it.

The compaction's call found through `cost-state`. The session's count by
`shared/usage/usage.py`, its transcript up to the `cost-state` record at line 908 and its
one subagent, against that record, for Claude Opus 5.5: 2,066 input, 8,542 output,
287,337 cache-read and 63 cache-write tokens missing from the transcript, $0.2368864 in
the record. The same tokens priced, the write at five minutes, give $0.2368864 exactly.
The 287,337 tokens read equal the cache read of the last call before the compaction
(line 737), nine minutes earlier, so the cache still held. From line 908 to the next
record, line 987, transcript and record grow by the same tokens: nothing else is hidden.
The context it leaves: the first call after the boundary, at 11:18:54, reads 24,279
tokens and writes 23,265, a context of 47,546 against 287,473 for the last call before.

The fields the count will read:
- the boundary: `subtype` `compact_boundary`, its `timestamp`, `compactMetadata`'s
  `trigger`, `preTokens`, `postTokens` and `durationMs`;
- the call: absent, so derived. Its cache read is the previous call's context, written
  again when the pause passed the hour; its output is unknown and must be estimated and
  marked, one compaction giving 8,542 tokens for a context of about 290,000; the gap with
  `cost-state` checks it when a record covers the session;
- the context left: the first `assistant` call after the boundary, its cache read and
  cache write.

Seen in passing, for task 3: the session's `roadmap-auditor` run, Claude Sonnet 5.5, two
calls. Its Agent tool result, `toolUseResult.usage`, gives the last call's 688 output
tokens; `cost-state` counts 1,085 for both, so the first call wrote 397. The reader
estimates 5,400 a call, 10,800 for the run: the design's table, `skill-auditor` 640 and
any other 5,400, prices `roadmap-auditor` like a writing agent.

Put to the user: how the count takes the compaction's call, absent from the transcript,
and `roadmap-auditor` added to the table of output estimates, measured in task 3 over the
sessions kept. The user approved the first; the second waits for task 3. The user also
asked that each step be committed once finished and recorded, the opening with it. Task 1
ticked, committed as `2d6663e`.

Task 2, the price table. Read the pricing of the `claude-api` skill bundled with Claude
Code 2.1.296, this session's: its models table, cached 2026-10-06, its migration guide and
`shared/prompt-caching.md`. Every price the reader needs is published there:
- Claude Haiku 5.5 at $0.10 and $0.50, the figures Phase 5 of `skill-tooling` had fitted,
  so it enters published, not fitted as the design planned; it has two rate cards, $0.50
  and $2.50 for a prompt past 100,000 tokens, cache reads at a tenth of the input price;
- cache reads, which the table had fitted: Claude Opus 5.5 and Claude Sonnet 5.5 $0.20,
  Claude Fable 5.1 and Claude Mythos 5.1 $0.25, "every other model at 0.1x" the input
  price; Claude Opus 5's $0.50 confirmed by Claude Fable 5.1's rate, half of it;
- cache writes at 1.25 and 2 times the input price, as the table had them.

Tests first, in `shared/usage/tests/test_usage.py`: every model of the table priced by hand
on one usage, the table's models checked against that list; each price's source, date and
origin; Claude Haiku 5.5 on its long-prompt rates past 100,000 prompt tokens, at the bound
and one token past it, and Claude Opus 5.5 on one rate card at 200,000; each model's price
source in the count's json, `null` for a model the table lacks. Watched failing, 1 failure
and 9 errors, then `usage.py`: a `Price` per model, with its source, `published` or
`fitted`, the date read and where, and an optional second rate card; thirteen models, all
published, read 2026-10-12. `PRICES_READ` stays the table's date, which `run.py` of
`authoring-skills` records in each `run.json`. 18 tests pass; `make shared` refreshed
`authoring-skills`' copy, and `make check` passes.

The copy is installed with skill-tooling, so that domain opens 0.1.2, `— unreleased`, its
changelog naming the change; Phase 3 releases it with the review domain (below, Changes To
Later Phases). `docs/claude-code-coupling.md`'s row on token usage names the prices'
source, the `claude-api` skill bundled with Claude Code, and Claude Haiku 5.5's two rate
cards. Task 2 ticked, committed as `bc875dd`.

Proposed for task 3: measure each agent type's output per call over the sessions kept, as
the gap in output between transcript and `cost-state` for the agents' model, divided by
the calls without a final usage, in sessions where one agent type ran. Not yet answered:
the session ends here, at the user's word, to resume in a new one.

**Where the next session starts:**
1. Task 3, the count of a session with all its subagents. Put the measure above to the
   user first: `roadmap-auditor` is estimated at 5,400 output tokens a call where
   `bbaa7e41`'s run wrote 397, and the design's table knows only `skill-auditor`, 640.
   The fixture follows the task's proof: a main session, two subagents, a run whose last
   call's output comes from `toolUseResult.usage`, a rebuild after a pause, calls at two
   efforts, and a compaction shaped as task 1 recorded it, `compact_boundary` with its
   `compactMetadata`, the `isCompactSummary` record, no `assistant` record for its call,
   which is rebuilt as the Decisions below say. The rule that prices a tool's text is the
   design's: its characters at 3.5 a token, one one-hour write and a read by every later
   call. `bbaa7e41`'s transcript, the probe's source, is kept until about 2026-11-11.
2. Task 4, a shared message id given to the transcript whose last record comes first
   (`a556427b` and `c3561bb8`, Phase 0's task 3).
3. Task 5, the window's selection: this repository's sessions before the move sit in
   `-code-ai-my-agent-setup` with `cwd` `/code/claude/my-claude-setup`, and 19 folders of
   `claude -p` runs keep the old name; found by project folder, not by `cwd` alone.
4. Task 6, the shared code. Each change to `shared/usage/usage.py` adds to skill-tooling
   0.1.2's changelog entry, still `— unreleased`.

A new session resumed the phase. Before task 3, the user raised a point: the models
measured today will change and other providers may come, so the models' configuration
must let one be added or changed without starting over. What made it costly: the table
is Python code, a `published(...)` call per model; `test_usage.py` pins every model of
the shipped table, so a new model breaks the test without testing anything new; the
cache writes are Anthropic's multipliers, global (`WRITE_5M`, `WRITE_1H`), and the
dated-id rule Anthropic's; the estimates are constants in the code. Proposed: the prices
and estimates in a data file read with `tomllib`, a rate per kind of token, a kind
without a rate leaving the call unpriced, rate cards and aliases generic, the tests on a
table of their own and the shipped one checked by `make check`; another agent's
transcripts not read yet, `calls()` staying the one part tied to Claude Code. The user
agreed and kept the multipliers: Anthropic's writes are always 1.25 and 2 times the
input, its reads 0.1 times but for three models, so they stay as a provider's defaults,
which a model's own value overrides. Added as task 3, before the count, 6 tasks to 7; the
data file is named `usage.toml`, since it holds the estimates beside the prices.

Task 3, the data file. Tests first. In `tests/test_shared.py`, a `.toml` source copied
into a skill's `scripts/`, beside the script that reads it: red on a `KeyError`, then
`tools/shared.py` maps `.toml` to `scripts/`. In `shared/usage/tests/test_usage.py`, the
tests price on a table of their own, patched over the shipped one, the figures of the
earlier tests kept; the test that pinned every shipped model is gone, its place taken by
tests of the mechanism: a provider's multiple and a model's own rate over it, a kind
without a rate leaving the call unpriced and its model listed unknown, an alias, the
source taken from the provider or the model, a rate card on the multiples of its own
input, the estimates read with their measure, sixteen malformed entries each refused by
its place, two problems named at once, an unreadable file named, and the shipped table
loaded, the check `make check` runs. Red on `usage.table` missing, then `usage.py`:
`table()` and `load()`, a `Price` as rate cards of rates by kind, `cost()` refusing a
kind without a rate, `PRICES_READ` the latest date of the table, `ESTIMATED_OUTPUT` read
from `[estimates.output] default`; `WRITE_5M`, `WRITE_1H` and `published()` gone. The
table loads at import and a malformed one stops every script that reads it, naming the
file and each problem. `usage.toml` holds the provider `anthropic` and the thirteen
models, ten of them on the provider's cache-read multiple, three with their own.

Checked against the table of `bc875dd`, out of the repository: the thirteen models priced
on four usages each, the long-prompt bound included, differ by 7e-18 dollars at most;
`PRICES_READ` and `ESTIMATED_OUTPUT` unchanged. 25 tests pass, `make shared` copied
`usage.py` and `usage.toml` into `authoring-skills`, whose audit gives no error and no
warning, and `make check` passes. `docs/claude-code-coupling.md`'s row on token usage
names `calls()` as the one reader of Claude Code's format and the data file, and
skill-tooling 0.1.2's changelog the change. Task 3 ticked. The tasks of the hand-over
above are now numbered one higher: the count is task 4, the deduplication 5, the window
6, the shared code 7.

Task 4, before its test: the measure of each agent type's output per call, which the
user started ("nous pouvons lancer les sessions de la tâche 4"). One-off scripts in the
session's scratchpad, not kept, read the 55 main sessions under `~/.claude/projects/`
that hold a `subagents/` folder. For each, the calls before its last `cost-state`
record: the main thread and the runs whose Agent call comes before it, each run's agent
type from its `agent-<id>.meta.json`, `agentType`. On each model a run used, where the
transcripts' input, cache-read and cache-write tokens equal the record's, the record's
output tokens less the final outputs and the runs' last outputs is the output of the
calls without a final usage. 34 pairs of a session and a model equal their record.
Where one agent type ran at one effort:

| Agent type, model, effort | Calls | Output a call | By session |
|---|---|---|---|
| `roadmap-auditor`, Sonnet 5.5, `medium` | 20 | 346 | 190 to 584, 8 sessions, 2.1.287 to 2.1.296 |
| `roadmap-auditor`, Sonnet 5.5, `max` | 29 | 2,280 | 2,231 and 2,408 |
| `roadmap-auditor`, Sonnet 5, `high` | 45 | 877 | 818 to 940, 4 sessions |
| `roadmap-auditor`, Sonnet 5, `max` | 30 | 2,517 | 1,827 to 4,997, 3 sessions |
| `skill-auditor` as `general-purpose`, Sonnet 5.5, `medium` | 34 | 325 | `8f80c90c` alone |
| `general-purpose`, Sonnet 5.5, `max` | 398 | 5,948 | 2,422 to 12,807, 3 sessions of eval runs |

What it shows:
- The effort decides more than the agent type: the same `roadmap-auditor` writes 346
  tokens a call at `medium` and 2,280 at `max`. An estimate per agent type alone, as the
  design has it, misses by a factor of six whichever effort it takes. `roadmap-auditor`
  declares no effort; its calls carry the one they ran at.
- The 640 the design gives `skill-auditor` is `8f80c90c`'s mean with the runs' last
  calls, which wrote the reports, 658 to 3,719 tokens; the other calls wrote 325.
- The default of 5,400 holds for writing agents at `max`, 5,948 over 398 calls.
- A run in the background has no `usage` in its Agent result. Its last call's output is
  found in the `<task-notification>` Claude Code queues when the run ends, a
  `queue-operation` record whose `content` holds `<usage><subagent_tokens>`: those tokens
  less the last call's input, cache reads and cache writes. In `8f80c90c` (2.1.296), the
  nine runs' last outputs so taken, 658 to 3,719, leave 325 a call to the 34 others, near
  the 346 of runs in the foreground at `medium`. The figure is not exact: in the 92 runs
  whose last record carries its final usage, 2.1.267 to 2.1.289, it equals that record's
  input, cache and output in 9, and differs by a few hundred tokens in the others, either
  way. A foreground result's `totalTokens` equals its `usage`'s sum in all 135 results.
- Up to 2.1.280, the runs' records carry their final usage; from 2.1.281 most calls lack
  it, 9 of the 74 calls of runs on 2.1.296 excepted, so nearly every subagent call but a
  run's last is now estimated.

Put to the user before the test: the estimates of `usage.toml` keyed by agent type and
effort, `roadmap-auditor` 350 at `medium` and 2,300 at `max`, `skill-auditor` 330 at
`medium`, a pair the table lacks taking the default, 5,400; and a background run's last
output taken from its notification, marked estimated. Committed as `d5b0753`; the user
agreed to both ("oui").

Task 4, the count. Two more figures read from the transcripts before the test:
- The characters of a token, which the design priced at 3.5 from the 2026-10-06 record,
  where it was assumed, not measured: 755 tool results past 6,000 characters against the
  cache write of the call after them, the previous call's output taken off, in this
  repository's and scriptorium's main sessions on Claude Opus 5.5 and 5. Median 2.55 for
  Bash (615), 2.59 for Read (125), 2.62 for Artifact (15); 90 skill loads, 2.76. The
  table takes 2.6: a text costs a third more than the design's rule said.
- The cache rebuilds: over every main transcript kept, 136 pairs of calls where the
  second reads back less than the first left in the cache. 128 lose half of it or more:
  92 after a pause past the hour, 10 on a change of `credential_org`, 2 at a compaction,
  one on a change of model, 23 without a known cause. Below half, 8, and below 1,000
  tokens, 12. "Most of the context", the design's words, is half or more. A
  `credential_org` record is an `attachment` with `organizationUuid`; a change is a uuid
  other than the one in force at the previous call.

Tests first, in `shared/usage/tests/test_usage.py`, on a session shaped as 2.1.296 writes
it, every figure by hand: a main thread on Claude Opus 5.5 at `xhigh` then `max`; a
`roadmap-auditor` run in the foreground and a `general-purpose` run in the background, on
Claude Sonnet 5.5 at `medium`; an Agent result, a notification; a rebuild after a pause
and one on a change of organization; a compaction as task 1 found it. Checked: each run
counted with its agent type; outputs estimated at 350 and 5,400; the foreground run's last
output, 900, counted from the result; the background run's, 800, taken from its
notification and estimated; cost per model and effort; the estimated part, $0.2475924, in
every total; main thread and runs apart; the two rebuilds, 21,500 tokens for $0.1677 and
24,000 for $0.1872; the compaction's call, 33,002 read, 2,998 input, 8,000 output, and the
13,003 tokens it left. Apart: a compaction past the hour writing its context again,
rebuilds by a change of model and of no known cause, a thread on five-minute entries
losing them past five minutes, the text rule, the estimates' lookup and their malformed
entries. Red on the table refusing the estimates by effort, then on `session`,
`rebuilds`, `estimate` and `text_cost` missing.

Then `usage.py`: `session()`, `rebuilds()`, `text_cost()`, `estimate()`, `tally()`; a
`Call` with its time, agent type and `derived` mark; totals with `estimated_cost` and by
model and effort. `usage.toml`'s estimates: `[estimates.output]` by agent type and effort,
`[estimates.compaction]` 8,500, `[estimates.text]` 2.6 characters a token, each with its
date and origin. 43 tests pass; `make shared` refreshed `authoring-skills`' copies;
`make check` passes.

Checked on the kept sessions, each main transcript cut at its last `cost-state` record
with the runs started before it: 569 of 625 pairs of a session and a model hold the
record's input, cache-read and cache-write tokens. Where they do:
- this setup's auditors at `medium` come within 703 output tokens and 3 cents of the
  record, 9 pairs; at `max`, within 1,446 tokens and 2 cents, 3 pairs;
- `bbaa7e41`'s compaction, derived: Claude Opus 5.5 at $11.2038 against $11.1959, its
  call $0.2448 against $0.2369;
- `general-purpose` runs on the default, 5,400 a call, miss by $0.12 to $7.63, both ways,
  on runs that wrote 325 to 12,807 a call; `8f80c90c`'s `skill-auditor` runs, typed
  `general-purpose`, take the default, $1.91 over its $1.50;
- other projects' agents, which the table lacks, miss both ways; scriptorium's are its
  own to measure;
- one probe of 2.1.283, `927b9ad1`, two calls with nothing estimated, holds a record of
  $0.0215 for $0.0110 at the table's prices: not explained, a lone case.

`docs/claude-code-coupling.md`'s row on token usage names what `session()` reads, and
skill-tooling 0.1.2's changelog the count. Task 4 ticked, its text following the
decisions below, committed as `05ceb3f`. The session ends here, at the user's word, to
resume in a new one; this block replaces the hand-over above.

**Where the next session starts:**
1. Put to the user first, if not answered: the characters of a token at 2.6, not the
   design's 3.5 (Problems And Deviations). Changing it back is one entry of `usage.toml`.
2. Task 5, the deduplication: a message id held by several transcripts goes to the
   transcript whose last record comes first, not to the first given, as `count()` and
   `tally()` do today. The pair Phase 0's task 3 found, `c3561bb8` and `a556427b`, 102
   calls shared, is kept until about 2026-11-08. The rule applies to whole sessions,
   runs with them, since Phase 2 counts a window of `session()`s.
3. Task 6, the window, in `shared/sessions/` (new): this repository's sessions before the
   move sit in `-code-ai-my-agent-setup` with `cwd` `/code/claude/my-claude-setup`, and 19
   folders of `claude -p` runs keep the old name; found by project folder, not by `cwd`
   alone. A `claude -p` session is found by its first record, never by `.eval-runs/`
   alone.
4. Task 7, the shared code, then the phase's closure.
- Each change to `shared/usage/` adds to skill-tooling 0.1.2's changelog, still
  `— unreleased`, and each transcript field newly read to `docs/claude-code-coupling.md`.
- Seen and left for Phase 2, whose review of several sessions reads `cost-state`: a web
  search costs $0.01 in the records and the reader does not count it; the probe
  `927b9ad1` holds a record twice the table's price, unexplained.

A new session resumed the phase. Put to the user first, the characters of a token: the
user kept the measured 2.6.

Task 5, before its test: how a continued conversation writes the calls it copies. One-off
scripts in the session's scratchpad, not kept, read the 1,065 main transcripts under
`~/.claude/projects/` and their runs. 12 groups of two or three transcripts share message
ids, 25 to 290 calls a group, 1,354 calls without Claude Code's own messages, in this
repository, scriptorium, `-code-claude-my-claude` and `-code-rust-projects-ai-ctl`, on
2.1.274 to 2.1.295. What they show:
- No run's call is held twice: a continuation's `subagents/` holds its own runs only. The
  rule applies to the main threads; the runs stay with their session.
- A shared call's usage is the same in every transcript that holds it, 1,371 of 1,371
  with Claude Code's own messages.
- A copied record keeps its `timestamp` and its message id; its `uuid` and `sessionId`
  are the continuation's. In `c3561bb8` and `a556427b`, the 102 shared calls run from
  08:24:53 to 09:01:22 in both.
- A call's last record can differ: the copy may lack the last content block
  (`f57dee82` and `f1d16520`, 2.1.295), or write it at the resumption, hours later
  (`msg_011CfSEjfwTvBFZpVU8gZuEp`: its text block at 14:51:03 in `264525a3`, at 17:39:18
  in its two continuations). Its first record's time is the same in every transcript for
  1,235 calls; it differs for 3, each earlier in the transcript that ends first, and for
  116 held by a teleported transcript.
- `348d400d`, `-code-claude-my-claude`, 2026-09-16, holds a `teleported-from` record
  (`remoteSessionId`, `messageCount` 483) and every record dated at the teleport, from
  18:20:01.342 to 18:20:01.823, a millisecond apart, `version` `1.0`. Its 116 calls are
  all held by `046e9700` and `f240c07b`, which date them from 2026-09-11. It ends before
  both, so the design's rule gives it the 116 calls, dated at the teleport. Four other
  teleported transcripts share no call: three hold none, `60d1fe46` 12 of its own.

Put to the user: a shared call goes to the transcript whose record of it comes first, at
equal times to the one whose last record comes first; the design's rule alone, or the
design's rule with a teleported transcript yielding its shared calls, read from its
`teleported-from` record. The user chose the first.

Tests first, in `shared/usage/tests/test_usage.py`: a call's time from its first record; a
`Continued` case shaped as 2.1.294 wrote `c3561bb8` and `a556427b`, the continuation's
records copied with their times under its own uuids and session id, its first record
earlier, one text block written again at the resumption. Checked: a session's end; the
shared calls given to the original whatever the order given, by `count()` and by
`distinct()`; a teleported copy yielding its calls; a chain of three; a copied compaction,
its derived call and a rebuild counted once; a continuation's runs kept. The test that
gave a shared call to the first transcript given is gone. Red: 1 failure and 6 errors, on
`distinct` and `Session.ended` missing and the time taken from the last record.

Then `usage.py`: `transcript()` gives a transcript's calls and the time of its latest
record, `calls()` its calls; a call's time is its first record's; `Session.ended`;
`owners()` gives each message id to its transcript by the rule, `distinct()` keeps each
session's own calls with their compactions and rebuilds, and `count()` takes the same
rule. A compaction's derived call is named after the call before it, not after its
boundary's `uuid`, which a copy changes: a copied compaction keeps the same id. 49 tests
pass; `make shared` refreshed `authoring-skills`' copy; `make check` passes.

Checked on the 1,065 main transcripts kept: every one read by `session()`; in the nine
groups of continued conversations their main threads form, each call kept once, and every
call where the design's rule puts it but the 116 of `348d400d`, kept by `046e9700`.
`c3561bb8` keeps its 102 calls, `a556427b` 61; `count()` gives 163 calls and $11.8513 in
either order. `docs/claude-code-coupling.md`'s row on token usage names the times read
and what `distinct()` relies on, a copy keeping message ids and times; skill-tooling
0.1.2's changelog the change. Task 5 ticked, committed as `6e553d9`.

Task 6, the window, before its test. Of the 400 project folders kept, one is this
repository's, `-code-ai-my-agent-setup`: 60 transcripts, 59 prompted by a person, 56 of
them with `cwd` `/code/claude/my-claude-setup`. No folder holds a subdirectory's or a
worktree's sessions. The sessions no person prompted, by folder: `-tmp-skill-*` 442,
scratchpad folders 373 (40 under this repository's old name, 333 under another project's),
`-home-seb` 99 (trigger runs of 2026-09-16), one in this repository's folder.

Tests first, in `shared/sessions/tests/test_sessions.py`: a fixture repository whose phase
opens at 09:00 and closes at 15:00, a commit before, two inside, one after; in the
repository's folder, sessions inside, across the closing and before the window, a
continuation and a probe no person prompted, one session's prompt under an old `cwd`; in
folders of their own, `claude -p` sessions inside, before and after the window, in two
spans, in none, in a scratchpad folder naming a working session and in one naming another
project's; another project's working session. Checked: a folder's name from its path; the
bounds by commits or times; the working sessions by their folder; each call by its time
and once; the spans; each `claude -p` session's owner, way and mark; each commit's owner;
the end now by default. Red: the module missing, and `Session.started`. Then
`shared/sessions/sessions.py`, `window()`, and `usage.py`'s `Session.started`: 9 and 49
tests pass.

Checked on Phases 4 and 5 of `skill-tooling`, from their Start Commits to their closing
commits, against Phase 0's counts by hand and the decision records:
- Phase 4: 218 `claude -p` sessions, `run` 67, `grade` 64, `judge` 56, scratchpad 24,
  `trigger` 6, `rewrite` 1, two of them in two spans (`3e3cb8b0` and `abe452df`), $69.32;
  17 working sessions, the 13 calls of Phase 3's closing session among them; 26 commits,
  each in one span.
- Phase 5, first run: 245 sessions, 3 runs missing. `c3561bb8`'s last call, at 09:01:12,
  had started an evaluation whose three runs went on in the background from 09:05 to
  09:23, and its transcript ends at 09:24:40: a span closed at the session's last call
  left them out. A span now runs from the session's own first call to its last record, a
  fixture's run after its last call added, red, then the code.
- Phase 5 again: 248 sessions, `trigger` 144, `run` 68, `judge` 36, none in two spans
  where Phase 0's count found 8, the overlap of `c3561bb8` and `a556427b`'s copied
  history; $103.57, the decision record's figure; 27 commits, each in one span.

`docs/claude-code-coupling.md` gains a row for what `sessions.py` reads, `CLAUDE.md` names
the module, and skill-tooling 0.1.2's changelog `Session.started`. `make check` passes.
Task 6 ticked, committed as `20c318d`.

Task 7, the shared code. The design copies `usage.py` into `tool-review` and `sessions.py`
into `reviewing-token-usage` only, and the skill audit refuses a file no script imports
(R3): a copy needs a reader. `transcript.py` counts a slice's tokens from each message's
first record, and an agent's runs the same way; the slice's count becomes the measured
block of Phase 2's task 1, which changes its figures. The runs' fresh and cached tokens
stand in every record, so `agent_runs()` reads its calls through `usage.calls()`, its
figures unchanged: its test passes as it was, and on the 69 pairs of a session and an
agent type kept, the old and the new `agent_runs()` give the same runs.

`reviewfile.py` moved to `shared/reviewfile/` with its test, `tool-review`'s copy put back
beside its scripts, and `usage.py` and `usage.toml` copied there; `tools/shared.py --check`
finds every copy equal, `tools/reviews.py` reads `tool-review`'s copy as before. The review
domain opens 0.3.0, `— unreleased`, the version Phase 3 releases, its changelog naming
both copies; `CLAUDE.md` names `shared/reviewfile/` and the copies. `make check` passes,
the audit of `tool-review` clean. Task 7 ticked; every task of the phase is done,
committed as `dc7057c`.

The user asked to close the phase, and to open Phase 2 in a new session. `make check`
passes; the three acceptance criteria hold.

---

## Decisions

- **A compaction's call is rebuilt from the transcript** (the user, 2026-10-12): its cache
  read is the previous call's context, a write instead when the pause since that call
  passed the hour; its fresh input the rest of `preTokens`; its output estimated, 8,500
  tokens from the one compaction probed, and marked estimated. When a `cost-state` record
  covers the session, the gap checks it. Task 3 counts it so, and the review of several
  sessions flags the gap.
- **A step is committed once finished and recorded** (the user, 2026-10-12): the phase's
  opening goes with task 1.
- **Every price is published, read from the `claude-api` skill bundled with Claude Code**
  (2026-10-12, Claude Code 2.1.296): the table covers the thirteen models it prices, and a
  price becomes `fitted` only when no published one exists. Claude Haiku 5.5 enters
  published, its two rate cards with it. The review of several sessions keeps checking the
  table against `cost-state` (Phase 2).
- **Skill-tooling 0.1.2 is open, `— unreleased`**, for `authoring-skills`' copy of
  `shared/usage/`, which every task of this phase changes; Phase 3 releases it.
- **Prices and estimates are data, in `shared/usage/usage.toml`** (the user, 2026-10-12):
  a model or a provider is added or repriced by an entry alone. A rate is given in
  dollars per million tokens or as a multiple of its card's input price; a provider holds
  defaults, rates and source, that a model's own value overrides, Anthropic's cache
  writes at 1.25 and 2 times the input and its reads at 0.1 times; a rate card past a
  prompt length takes the multiples of its own input; a kind of token with tokens and no
  rate leaves the call unpriced, never priced at zero. The tests price on a table of
  their own; the shipped table is checked by `make check`. Only `calls()` reads Claude
  Code's format: another agent's transcripts would need their own reader, not built
  until one is used. Task 3's estimates per agent type go in the same file.
- **A run's output is estimated by agent type and effort** (the user, 2026-10-12): the
  measure of task 4 found the same agent writing six times more at `max` than at
  `medium`. `[estimates.output]` holds a figure per agent type and effort, or one for
  every effort; a pair the table lacks takes the default. A run's last call takes the
  Agent result's final output; a run in the background, whose result has none, takes its
  notification's tokens less the call's prompt, marked estimated.
- **Every estimate is data** (2026-10-12): the compaction's output and the characters of
  a token join the subagents' output in `usage.toml`, each by model with a default.
- **A text is priced at 2.6 characters a token** (the user, 2026-10-12), the figure
  measured in task 4, not the design's 3.5. Phase 2's measured block and its review of
  several sessions price a tool's text so.
- **A call held by several transcripts goes to the one whose record of it comes first, at
  equal times to the one whose last record comes first** (the user, 2026-10-12). It is the
  design's rule on every continued conversation kept, and gives a teleported copy's calls
  back to the transcript that holds them with their own times. A call's time is its first
  record's, the same in every copy. Phase 2 counts a window of sessions through
  `distinct()`; task 6 counts each call by that time.
- **A repository's working sessions are the transcripts of its project folder that a
  person prompted** (2026-10-12): the folder Claude Code names after the repository's
  path, whatever the sessions' `cwd`, and a record of `origin.kind` `human`. No other
  folder is searched: none holds a subdirectory's or a worktree's sessions.
- **A working session's span runs from its own first call to its last record**
  (2026-10-12): its own calls, after `distinct()`, so a continuation's copied history
  does not widen it; its last record, so the runs it started in the background before
  stopping stay with it. A `claude -p` session and a commit go to the first span that
  holds them, marked shared in two; a `claude -p` session whose scratchpad folder names a
  session the repository does not hold is left out. Commits are read on every local
  branch, at their committer's time.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/token-usage/phase-1-usage-reader-report.md`
- `domains/review/skills/tool-review/scripts/usage.py`
- `domains/review/skills/tool-review/scripts/usage.toml`
- `domains/skill-tooling/skills/authoring-skills/scripts/usage.toml`
- `shared/reviewfile/reviewfile.py` — the source of `tool-review`'s `scripts/reviewfile.py`, which stays, unchanged
- `shared/sessions/sessions.py`
- `shared/sessions/tests/test_sessions.py`
- `shared/usage/usage.toml`

**Modified**
- `CLAUDE.md`
- `docs/claude-code-coupling.md`
- `docs/roadmap/README.md` — the roadmaps' overview, at the opening and the closure
- `docs/roadmap/on-progress/token-usage/README.md`
- `docs/roadmap/on-progress/token-usage/phase-1-usage-reader.md`
- `docs/roadmap/on-progress/token-usage/phase-2-reviews-and-reports.md`
- `docs/roadmap/on-progress/token-usage/phase-3-validation-and-release.md`
- `domains/review/CHANGELOG.md`
- `domains/review/VERSION`
- `domains/review/skills/tool-review/scripts/transcript.py`
- `domains/skill-tooling/CHANGELOG.md`
- `domains/skill-tooling/VERSION`
- `domains/skill-tooling/skills/authoring-skills/scripts/usage.py`
- `shared/usage/tests/test_usage.py`
- `shared/usage/usage.py`
- `tests/test_shared.py`
- `tools/shared.py`

**Renamed**
- `domains/review/tests/test_reviewfile.py → shared/reviewfile/tests/test_reviewfile.py`

---

## Problems And Deviations

- **A text is priced at 2.6 characters a token, not the design's 3.5.** The 3.5 of the
  2026-10-06 record was assumed; measured on 755 tool results and 90 skill loads, a token
  holds 2.55 to 2.76 characters. A tool's text costs a third more than Phase 0's design
  and the decision records of Phases 3 to 5 of `skill-tooling` counted it. The user kept
  2.6; the figure is one entry of `usage.toml`.
- **Task 4's text changed with the decisions**: "estimated per agent type" became "per
  agent type and effort", and the background run's notification was added. No task added
  or removed.
- **Task 5's rule differs from the design's**: a teleported transcript dates its copies
  at the teleport and ends before the original, so the design's rule gave `348d400d` 116
  calls at false times. Task 5's text now says the rule the user chose. No task added or
  removed.
- **A copied compaction is counted once on an assumption**: no transcript kept holds a
  copy of a compacted conversation, so its derived call is named after the call before
  it, which a copy keeps, rather than its boundary's `uuid`, which a copy changes. Left
  open until a continued compacted conversation is seen.
- **Task 7's text changed**: it copied `shared/sessions/` into `tool-review`, where no
  script reads it and the audit would refuse it; the design copies it into
  `reviewing-token-usage` only, which Phase 2 writes. `tool-review` receives `usage.py`,
  read by `agent_runs()`; its slice count stays for Phase 2's task 1. No task added or
  removed.
- **Review 0.3.0 is open, `— unreleased`**, for `tool-review`'s copies of
  `shared/reviewfile/` and `shared/usage/`; Phase 3 releases it, as its task already says.
- **`general-purpose` runs stay on the default**, 5,400 a call, which misses their
  output both ways: they wrote 325 to 12,807 a call by what they did. The review of
  several sessions flags the gap with `cost-state` (Phase 2).
- **Task added: the prices and the estimates moved into a data file**, 6 tasks to 7, at
  the user's request before the count: a model added to the code-held table took a code
  change and a test change. Done as task 3, before the count, whose estimates it holds.
- **Claude Haiku 5.5 entered published, not fitted.** The design took it as fitted until a
  published price was read; the `claude-api` skill of Claude Code 2.1.296 publishes it, at
  the fitted figures, with a second rate card past 100,000 prompt tokens that the design
  did not know. The table has it. The record's When To Revisit on that price is met.

---

## Changes To Later Phases

- `phase-3-validation-and-release.md`: the release task also releases skill-tooling 0.1.2,
  whose copy of `shared/usage/` this phase changes, tagged `skill-tooling-v0.1.2`; the
  install task, its files and the acceptance criterion on the release follow. No task
  added or removed; the Objective, which names the review domain, unchanged.
- `phase-2-reviews-and-reports.md`: the task of `reviewing-token-usage`'s script names
  the copies of `shared/usage/`, `shared/sessions/` and `shared/reviewfile/` it works on,
  and its window taken through `sessions.window()`, which Phase 1's task 6 wrote. No task
  added or removed.

---

## Assessment

Phase 1 delivered the reader the design asked for, in seven tasks, one of them added at
the user's request. `shared/usage/` counts a session with all its runs: each call priced
per model and effort from `usage.toml`, a data table whose every price is published; a
run's output estimated by agent type and effort and marked, its last output taken from
the Agent result or, in the background, its notification; a compaction's call derived and
marked; each cache rebuild with its size, cost and cause; a text priced at 2.6 characters
a token; a call held by several transcripts counted once. `shared/sessions/` gives a
window's working sessions, the `claude -p` sessions given to them and its commits.
Checked on the transcripts kept: Phases 4 and 5 of `skill-tooling` recounted to their
records' figures, 218 and 248 `claude -p` sessions for $69.32 and $103.57; `bbaa7e41`'s
compaction within a cent of `cost-state`.

Measured, the design moved in five places: a run's output depends on its effort more
than on its agent type; a token holds 2.6 characters, not 3.5; Claude Haiku 5.5 is
published; a shared call goes to the transcript that recorded it first, which a teleported
copy needed; a span runs to its session's last record, which background runs needed.

What Phase 2 needs to know first:
- `transcript.py`'s slice count still keeps each message's first record, whose output is
  the stream's first figure: the measured block of task 1 reads the slice through
  `usage.calls()`, already beside it in `tool-review`, a call's time being its first
  record's.
- `reviewing-token-usage` takes its window from `sessions.window()`. `tools/shared.py
  <skill>` copies every shared module into a new skill, `conventions` and `frontmatter`
  included, which the audit then refuses as unread: copy `usage`, `sessions` and
  `reviewfile` by hand, as task 7 did, and `make shared` keeps them.
- Left to the review of several sessions, beside `cost-state`: `general-purpose` runs on
  the default estimate, wrong both ways; a web search's $0.01, not counted; `927b9ad1`'s
  record at twice the table's price.
- Skill-tooling 0.1.2 and review 0.3.0 are open, `— unreleased`, for Phase 3 to release.
- The transcripts the checks on real data read are deleted: Phase 4's from about
  2026-11-05, Phase 5's and the continued pair's from about 2026-11-08, `bbaa7e41` about
  2026-11-11.
