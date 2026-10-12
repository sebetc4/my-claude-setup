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
ticked.

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

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
