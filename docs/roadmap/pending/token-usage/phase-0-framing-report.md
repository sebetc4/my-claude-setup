# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** be6f381

---

## Work Log

### 2026-10-11

Phase opened. Roadmap `skill-tooling` closed on 2026-10-11, so the phase's
`Blocked By` is cleared. First phase of the roadmap: no previous report to read,
no restructuring to settle.

Task 1, the inputs. Read the three records, `shared/usage/usage.py`, the review
domain's `transcript.py`, `measure.py`, `record.py`, `reviewfile.py`, `review.py`,
`tools.json`, `tools/reviews.py` and the output of `make reviews` (86 reviews,
2026-09-27 → 2026-10-11). Checked three points on the transcripts of `e235aebc`,
`ead9c2d4`, `197b64c4` and `585d56e6`. The list, put to the user:

**What the reader measures today** (`shared/usage/usage.py`, copied into
`authoring-skills`, whose `run.py`, `grade.py`, `benchmark.py`, `triggers.py` and
`tuning.py` call `count`, `as_json`, `price_of` and `ESTIMATED_OUTPUT`):
- R1. One call per message id, its last record kept, `<synthetic>` left out
  (`usage.py:132`).
- R2. A price table of five models read 2026-10-06, without Haiku 5.5
  (`usage.py:33`); cache writes split five-minute and one-hour, at 1.25 and 2 times
  the input price, one-hour when the split is missing (`usage.py:43`, `usage.py:116`);
  a model the table lacks costs `None`, never zero (`usage.py:149`).
- R3. The output of a call without `stop_reason` replaced by 5,400 tokens and marked
  estimated, one figure for every agent (`usage.py:48`, `usage.py:124`).
- R4. `count(paths)`: several transcripts, each message id once, the first
  transcript keeping it; totals per model and calls per effort (`usage.py:88`,
  `usage.py:159`).
- R5. Not done: finding a session's subagents or the `claude -p` sessions it
  started, selecting a phase's sessions, cache rebuilds, the `cost-state` records,
  the Agent tool's result.

**What the review domain measures today:**
- T1. A slice's tokens: `fresh` adds input and cache writes, so a slice cannot be
  priced; `cache_read`; `output`; turns, context peak, active minutes, tool counts,
  tool errors, interruptions (`transcript.py:322`). No model, no effort, no dollar,
  no mark of an estimate. Main transcript only: a subagent not in the catalog is not
  counted at all.
- T2. Per tool under review: a skill's loads and characters, its files read through
  the Read tool, its scripts run through Bash (`transcript.py:263`); an agent's runs,
  fresh and cached tokens and seconds, no output and no model (`transcript.py:285`);
  a hook's runs, injected characters, blocks and errors (`transcript.py:188`).
- T3. The Stop hook asks for a review once per tool and session; the slice runs from
  the end of the previous one to this Stop (`review.py:51`). The review's own turn,
  from `to` to `closed`, falls in no slice: `next_start` starts the next slice at
  `closed` (`reviewfile.py:323`), seen in `e235aebc` and `ead9c2d4`. After the last
  review, the rest of the session falls in no slice either: reviews do not add up to
  a session.
- T4. `measure.py` prints the block from the requested review's slice
  (`measure.py:100`); `record.py` measures it again when it writes the review
  (`record.py:145`).
- T5. `make reviews` gives each tool's median of loaded characters, fresh tokens and
  seconds of a run, or injected characters (`tools/reviews.py:62`): no dollar.

**What the records' method adds:**
- M1. Sources: a session's subagent files and its `cost-state` records (2026-10-06,
  Method). A transcript holds several `cost-state` records, each the running total of
  the session by model, with `costUSD`, the last one covering the session up to its
  write (seen in `197b64c4`).
- M2. Prices checked against `cost-state` and the json results of `claude -p`; cache
  writes five-minute for subagents and one-hour for main sessions (2026-10-06,
  Recount); Haiku 5.5 fitted at $0.10 and $0.50 (2026-10-11, Method); `claude -p`
  sessions writing one-hour entries too (2026-10-11, Where it went).
- M3. Calls no transcript holds: Claude Code's own Haiku calls and a few Opus calls,
  counted by `cost-state` and by the json results (2026-10-06, Recount; 2026-10-09
  and 2026-10-11, Checks).
- M4. Subagent output: one estimate eight times too high for `skill-auditor`, about
  640 tokens a call against 5,400 (2026-10-11, Checks). The Agent tool's result,
  `toolUseResult`, holds `usage` with the final output of the subagent's last call,
  `resolvedModel`, `totalTokens` and `totalDurationMs` (seen in `e235aebc`).
- M5. Cache rebuilds: the whole context written again after a pause past the hour or
  a change of organization recorded as `credential_org`, sized in tokens (2026-10-06
  and 2026-10-09, Where it went).
- M6. Effort per call, from the record's `effort` (2026-10-06, Effort).
- M7. A phase's sessions: main transcripts between the opening session and the
  closing one, by time span (2026-10-09, Method), then matched to tasks by their
  commits, a session working on another roadmap set apart (2026-10-11, Method).
  `claude -p` sessions found by their folders' prefixes, `-tmp-skill-run-`,
  `-grade-`, `-judge-`, `-trigger-`, `-rewrite-`, and scratchpad probes, each given to
  the main session whose span holds its first record. A conversation continued in a
  new process copies the history it shares, given to the first session by message id.
- M8. Documents and tool texts priced at 3.5 characters a token, each injected token
  one one-hour write plus a read by every later call (2026-10-06, This setup's tools).
- M9. A review's cost: from the Stop hook's request to the end of its turn, or to
  the call after `record.py` when a background notification goes on in that turn
  (2026-10-11, Method); ≈ $0.34 a review in Phase 4, ≈ $0.23 in Phase 5.
- M10. Two open review findings ask for the same thing: a measure over a set of
  sessions (`shared/usage/usage.py`, tooling-gap) and a cross-session reader
  (`transcript.py`, tooling-gap).

**The four open defects:**
- D1. `session_resume.py` measured at zero runs although the hook served: 50
  findings on `transcript.py`. Cause: `session_start` takes the first timestamped
  record (`transcript.py:219`), a `queue-operation` at 11:36:02.745 in `e235aebc`,
  while the SessionStart `hook_success` attachment is dated 11:35:52.579, ten seconds
  earlier, so `measure` leaves it out (`transcript.py:332`); `uses`, called without
  bounds by the Stop hook (`review.py:55`), finds it, so the hook is under review and
  counted at zero. Touches T1, T2, T3.
- D2. A skill's files read through Bash, `cat` or `sed`, missing from `files_read`
  (reviews of `b9be3716`, `1cee558e`, `f2b80cf5`): `count_skill_files` looks at Read
  paths and Bash script runs only (`transcript.py:263`). Touches T2.
- D3. The message "run make update D=review in it" (`measure.py:94`,
  `record.py:125`): an instruction the agent must not follow without the user's
  agreement (Phase 3 report of `skill-tooling`). Touches T4.
- D4. Agent runs without output tokens (`transcript.py:285`), and `make reviews`
  ranks agents by fresh tokens only (`tools/reviews.py:69`). M4 gives the final usage
  of the last call. Touches T2, T5.

The user approved the list. Task 1 ticked.

Task 2, the probe of persistence, prepared. `~/.claude/projects/` holds 881 MB for
the 30 days kept, transcripts written from 2026-09-10 to 2026-10-11, about 29 MB a
day; `cleanupPeriodDays` is not set. The probe hook, in the session's scratchpad,
appends one line per event: the event, the session, `reason`, the input's keys, the
transcript's size. Registering it in `.claude/settings.local.json` was refused by the
agent's permission classifier as a change to its own configuration: the user decides
how it is registered.

The user then reframed the phase. On scope: every project is measured, since
`make reviews` runs from this repository and the work happens in others. On
persistence: the `SessionEnd` and Stop hooks are judged unreliable, and
`cleanupPeriodDays` raised is chosen, so the hook probe is not run. On purpose: the
question to start from is why the cost is measured, not when. The three counts by
hand served to manage subagents, context and the resumption of sessions; they led the
user to shorten sessions and to start subagents and runs against the credit left, so
as to lose fewer runs. A measure must lead to conclusions that improve a workflow,
not only give figures. Two uses come first: the consumption of this setup's tools,
to find a tool that costs too much or one that costs without serving, a return on
each tool, reviewed automatically; and a summary over several sessions, a phase of a
roadmap or a stretch of coding, of what was used where and when, and of what did
harm. The user pointed to `study/session-review/`, a skill that reviews the tools a
repository provides, at the repository's scale, run by hand at the end of a session.

Read `study/session-review/`: `SKILL.md`, `session-ledger.sh`, the headers of
`metrics.py` and `aggregate.py`. What it does that the review domain does not:
- each measure beside the median of earlier reviews of the same skill, with the
  ratio, and a mark past 1.5 times;
- obligations printed by the script: explain the three largest costs, five without a
  baseline; explain each measure past 1.5 times its median; a finding or a reason for
  each waste or friction counter;
- one review per task, its slice starting where the previous review stopped;
- the review tooling's own turns left out of the measure;
- a ledger of session-level figures for every session, reviewed or not, written by a
  SessionStart sweep of the earlier sessions, one session late, the live one skipped:
  `SessionEnd` was left out because it does not fire for a session that crashed or
  was killed;
- `aggregate.py`, the corpus read across reviews: what a kind of task costs, which
  target keeps coming back, findings never carried, and the work nobody reviewed.
What it does not do: price anything, its measures being tokens.

The user approved the reframing, and the roadmap became 1.1.0: README, Phase 0's
Objective and tasks 2 and 4, Phases 1 to 3 (below, Changes To Later Phases). The hook
probe is dropped, the probe hook left unregistered in the scratchpad. The user also
wishes to bring `study/session-review/` into this repository as a standard tool, to
review the tools any repository builds for itself, growing with the findings of the
tool reviews: not this roadmap's work, written in its Out Of Scope as a roadmap to be
created.

Committed as `82497dc`. At the user's request, roadmap `session-review` was created
while the context held it: three phases, Framing, Standard Skill, Adoption And Release;
its Phase 1 is blocked by this roadmap's Phase 1, whose reader it uses. The roadmaps'
overview, `docs/roadmap/README.md`, shows this roadmap in progress and `session-review`
fifth in line. The session ends here, at the user's word.

**Where the next session starts:**
1. Task 2: read Claude Code's documentation on `cleanupPeriodDays`, cite it with its
   date, and put the value and the way to set it to the user, with the disk at about
   29 MB a day. Transcripts written from 2026-09-10 are deleted day by day until it is
   set; Phase 4 of `skill-tooling`'s from 2026-11-05, which task 3 probes.
2. Task 3: the probe of a phase's sessions, on Phases 4 and 5 of `skill-tooling`.
3. Task 4, the design, from the two uses and the Decisions above; it keeps
   `study/session-review/` in view, whose roadmap shares this one's reader, and avoids
   the name `usage`, a Claude Code command.

Session resumed. Task 2, `cleanupPeriodDays`. Read on 2026-10-11, Claude Code 2.1.292
(CLI) and 2.1.296 (VS Code extension):
- `settings-reference.md#cleanupperioddays`: days Claude Code keeps session
  transcripts and other application data, deleted by a background sweep after a
  session starts, without a message. Any settings file; a whole number, minimum 1,
  default 30; `0` fails validation, "pick a large value such as `3650` for long
  retention".
- `claude-directory.md#cleaned-up-automatically`: the sweep deletes, past the period,
  `projects/<project>/<session>.jsonl` with its `subagents/` and `tool-results/`,
  `file-history/`, `plans/`, `debug/`, `tasks/` and others, and a session's scratchpad
  with its transcript. Auto memory is kept. `--bare` skips the sweep; a sweep is paused
  when the period cannot be safely determined.
- `monitoring-usage.md#retention-sweep-event`: at most one sweep per session, delayed
  10 minutes when one ran on the machine in the last 24 hours. Paused with
  `user_source_disabled` when user settings are excluded, by `--setting-sources` for
  instance, and no enabled source sets `cleanupPeriodDays`. So the `claude -p` sessions
  of `harness.py`, started with `--setting-sources project,local` and a `--settings`
  without the key, never sweep: the key set in the user's settings is not undone by
  the eval runs.
- `settings-reference.md`, precedence: the value comes from the highest source that
  sets it. A project's `.claude/settings.json` setting a lower value would make every
  session in that project sweep every project's transcripts with it. None of this
  repository's settings files sets it.

Measured on 2026-10-11: `~/.claude/projects/` 883 MB, transcripts from 2026-09-10,
about 29 MB a day over the 30 days and 43 MB a day over the last seven (301 MB);
420 MB of it in 363 `-tmp-*` folders of `claude -p` sessions. `file-history/` 30 MB.
`/home` has 1.8 TB free. A year at 43 MB a day is about 16 GB. The transcripts are
plaintext and hold whatever a tool read, secrets included: a longer period keeps them
longer. `cleanupPeriodDays` is set in no settings file; the installer merges only
hooks and permission rules into `settings.json` (`tools/claude_setup.py:286`).

Put to the user: 365 days, about 16 GB a year, recommended over 3650 and 180; set by
hand at once and carried by the installer in Phase 2. The user chose 365 days through
the installer only, then asked what raising the period gains at all, since a tool
review measures in its session and a review of several sessions runs at the end of
a phase. Checked against the roadmaps: phases lasted 0 to 3 days, the longest roadmap,
`skill-tooling`, 14 days (2026-09-28 to 2026-10-11). What a longer period buys is
only the edge cases: a review run late, a phase past a month, a roadmap with a long
pause reviewed whole, an old window recounted with a better reader. What it costs: a
new kind of merge in the installer, a scalar key with its conflicts, state, removal,
tests and coupling entry, for one setting; a year of plaintext transcripts. Proposed
instead, and approved by the user: keep the 30 days, have the review of several
sessions write a record that a longer window reads, and warn when a window starts
before the oldest transcript kept. Task 2 ticked; the roadmap becomes 1.2.0 (below,
Changes To Later Phases), and roadmap `session-review`, which named `token-usage` as
the one setting `cleanupPeriodDays`, becomes 1.0.1. Committed as `0589e5e`.

Task 3, the probe of a phase's sessions, on Phases 4 and 5 of `skill-tooling`, and on
its Phase 2 for the shared session `2f2e66de`. A one-off script in the session's
scratchpad, not kept: the window runs from the phase's opening commit to its closing
commit, by commit time; it takes the main transcripts of the repository's folder with
calls in the window, each message id given to one transcript; each commit goes to the
main session whose span holds it; and the transcripts of other project folders whose
first record falls in the window are compared with the session ids of the `.eval-runs/`
json results. Found:
- Phase 4, `ae210e8` (2026-10-06 21:08) to `5b2065e` (2026-10-09 00:29): 16 main
  sessions inside, the record's 16 exactly; `7af1242d`, without a call, is absent. Two
  straddle a bound: `ed7dbe88`, Phase 3's closer, with 7 of its 58 calls after the
  opening commit, and `23f69b8f`, with 13 of 83 after the closing commit, where it
  opened Phase 5. The record gave each whole to the phase holding most of its calls.
- Phase 5, `0c1e7a0` (2026-10-09 00:30) to `fefa592` (2026-10-11 14:17): 15 main
  sessions inside, and `e235aebc` straddling with 5 of 76 calls after the closing
  commit. The record's 15 are these 16 without `8af16381`, whose one commit, `f21c767`,
  is on roadmap `roadmap-dependencies` and the roadmaps' overview. `be775c66`, which
  closed the roadmap, falls after the window, as the record has it. The first run
  missed `c3561bb8`: `a556427b` continues it and its copied records start 52 seconds
  earlier, so giving a shared message id to the transcript that starts first gave
  `a556427b` all 102 shared calls. Giving it to the transcript that ends first gives
  them back.
- Phase 2, `da8f005` to `4945b24`: `2f2e66de`, one session from 2026-10-03 01:51 to
  2026-10-04 19:33, has 179 calls in the window and 99 before the opening commit, where
  it closed roadmap `superpowers-study`. Each call counted by its time, the other
  roadmap's part falls out; the session given whole, by its majority, keeps it.
- So a window between commits, each call counted by its time, matches both records but
  for a few calls at the bounds, a closing session's tail that opens the next phase
  (7 and 13 calls), and it separates `2f2e66de`'s two roadmaps. A session that works
  wholly on another roadmap inside the window, `8af16381`, shows only through its
  commits. A session without a commit, four in Phase 4 (`3d474511`, `d9a8d9a0`,
  `871b9d72`, `80964ead`), shows only through its time.
- Every commit of the three windows falls in one main session's span, except where a
  continued conversation's two transcripts overlap (`a556427b`, `c3561bb8`). The bounds
  are at hand: a report's Start Commit is the HEAD at opening, the previous phase's
  closing commit, and Phase 5's, `5b2065e`, is the commit that closed Phase 4. Phase 4's
  Start Commit, `8c79c7b`, precedes its opening commit by 47 seconds.
- `claude -p` sessions whose first record falls in the window: 218 in Phase 4 and 248
  in Phase 5, the records' figures exactly. Phase 4: `-tmp-skill-run-` 67, `-grade-` 64,
  `-judge-` 56, `-trigger-` 6, `-rewrite-` 1, and 24 in scratchpad folders. Phase 5:
  run 68, judge 36, trigger 144. The `.eval-runs/` json results name 175 of Phase 4's
  (grade 46 of 64, run 63 of 67, scratchpad 3 of 24) and 240 of Phase 5's (run 60 of
  68): a run lost to the session limit or stopped, and a probe, leave no result, so
  the results alone miss 43 and 8 sessions.
- No record of a `claude -p` session names the session that started it (`entrypoint`
  `sdk-cli`, `cwd` `/tmp/skill-run-…/work`). A scratchpad folder carries the main
  session's id in its name, 24 in Phase 4. The others go by time: 192 and 240 to one
  main session's span, 2 and 8 to two spans that overlap (`3e3cb8b0` and `abe452df`;
  the continued `a556427b` and `c3561bb8`).
- Other projects' working sessions start in the windows too, 7 and 15, each with a
  human prompt and none from the eval tooling: a phase's sessions are the
  repository's main transcripts plus the sessions without a human prompt.
- `run.py` writes each run's `run.json`, with its session id, its tokens, its cost per
  model and its effort, and copies the run's transcript into `.eval-runs/`: 149
  `run.json` and 264 transcripts there, out of the sweep's reach.

Task 3 ticked, committed as `9248176`. The session ends here, at the user's word.

**Where the next session starts:**
1. Task 4, the design, from the two uses, the Decisions below and the inputs' list
   (R, T, M, D above). From task 3, it settles: a window given by two commits, the
   report's Start Commit and the phase's closing commit, each call counted by its time
   rather than each session whole; a session whose commits touch only another roadmap,
   as `8af16381`, set apart or kept, and how the agent is told; the `claude -p`
   sessions taken as the transcripts without a human prompt whose first record falls
   in the window, never from the `.eval-runs/` results alone, and linked to a main
   session by the scratchpad folder's name or by time; whether `run.json` serves as
   the record of a run. From task 2: the record the review of several sessions writes
   and its warning on a window older than the transcripts kept. It keeps
   `study/session-review/` in view and avoids the name `usage`.
2. Task 5, the four defects D1 to D4, then the decision record under `docs/decisions/`.

### 2026-10-12

Session resumed on task 4. Read again `shared/usage/usage.py`, the review domain's
`transcript.py`, `measure.py`, `record.py`, `reviewfile.py`, `review.py` and
`tools/reviews.py`, `study/session-review/` (`SKILL.md`, `references/findings.md`, the
headers of `metrics.py`, `aggregate.py` and `session-ledger.sh`), the three records'
Where It Went and What They Suggest, and Phase 0 of roadmap `session-review`.
Checked two points:
- A `cost-state` record carries no timestamp (`bff058db`, two records): it can check a
  whole session's count, not a window's.
- Claude Code's commands include `usage`, `insights` and `recap`
  (`docs/claude-code-builtins.md`); `session-review` is taken by roadmap
  `session-review`.
`make reviews` gave 90 reviews, 69 holding `session_resume.py` and 64 `roadmap`.

Design written as a `## Design` section of the phase file, proposed and put to the user:
what each measure serves, the reader, tool reviews, `make reviews`, a review's budget,
the review of several sessions as skill `work-review`, what is taken from
`study/session-review/`, shared code, and changes to the tasks.

The user answered the four choices. Every cost broken down by model and effort, with
its price, so that conclusions can be drawn. `make reviews` runs from this repository,
the setup's central one; the review of several sessions runs in the repository whose
work it reviews, this one included. The name `work-review` declined; `setup-review`
weighed against `study/claude-code-setup/`, which reviews setup files, not costs, and
`usage-setup-tools-review` as the clearest. Rebuilds out of the tool reviews, measured
against a clean hand-over and a new session's opening. `served` approved. The budget's
lever approved, on one condition: the counters start again once the reviews are
processed, examined in this repository and archived, or the reviews pile up and nothing
is drawn from them. The design follows: cost per model and effort everywhere, `make
reviews` without a deadline since a review holds its measures, a section Processing The
Reviews with `tools/reviews.py --archive`, the saturation counting the reviews not
archived, each rebuild beside the window's median opening, the record kept in this
repository, and the name `reviewing-session-usage` proposed, verb first as the writing
guide asks, since the skill reviews the sessions' consumption, the setup's tools among
it, while the return on each tool stays with the tool reviews. Phase 2 would go from 8
tasks to 10.

The user approved the breakdown by model and effort, the processing of the reviews and
the answers on where each tool runs. On rebuilds, the user asked for the comparison the
hand-over decision needs: a hand-over note and a new session, against the same session
once its cache is lost, past the hour or on a change of account, and against a
compaction at the end of a roadmap step, continued in the same session, a way not tried
yet. No kept transcript holds a compaction (`compact_boundary` and `isCompactSummary`
searched under `~/.claude/projects/`, none found), so Phase 1 gains a probe of how one is
recorded, 5 tasks to 6. The user preferred `reviewing-token-usage`, since the skill
measures tokens wherever they are spent, not in one session; the design follows. The
user asked what a window's record is.

Explained the window, two bounds given as commits or times, and its record, the
figures and conclusions a longer window, the comparison with earlier windows and the
ways of going on read. The user approved the design and the records kept in this
repository's `reviews/windows/`, then raised the boundary with roadmap
`session-review`'s skill, which reviews the tools a working repository builds for
itself, scriptorium's for instance, where costs and models matter as much: the line
between the three reviews looked thin. Put to the user: a split by the question each
answers, and the overlap of `tool-review` and `session-review`, the same question on
two catalogs.

The user approved both changes: a Boundaries section in the design, written, with the
rule that prices a tool's text moved into `shared/usage/` for any catalog; and the
boundary and the merge question added to roadmap `session-review`'s Phase 0, held until
the next point is settled since it bears on it. The user then proposed watching tools
by choice: a list, in `.agent-conventions.toml` or a configuration file, of the tools
being improved, since a review only serves a target someone means to improve, and is
noise otherwise (`roadmap` once stable, scriptorium's `pdf-reviewer` alike). Today the
list is `domains/review/hooks/tools.json`, installed by copy, which also holds the
points to watch.

Proposed a `[review]` table of `.agent-conventions.toml`, the same key in every
repository, read at each Stop, nothing reviewed without it; `tools.json` keeping the
points to watch; `make reviews` proposing to drop or watch again; the review of several
sessions as the net for a tool no longer reviewed. The user found it coherent and asked
where this setup's list lives, its tools serving in other repositories: a file here,
Claude Code's configuration, or each repository listing every tool. Answered: here, in
this repository's file, read by its path, the repository the installer's state names,
as the Stop hook already writes every project's reviews into this repository's
`reviews/`; a list under `~/.claude` is a copy that `make update` overwrites and a hand
edit turns into a conflict; a list in each repository repeats the setup's decision in
every project. Each list lives where its tools are improved.

The design marked approved and task 4 ticked. Applied in roadmap 1.3.0: Phase 1, 5 tasks
to 6, Phase 2, 8 to 11, the README's uses, scope and changelog; roadmap `session-review`
becomes 1.0.2. `progress.py --check` passes.

---

## Decisions

- **Every project is measured** (the user, 2026-10-11). `make reviews` runs from this
  repository, and the work it reports on happens in others.
- **The transcripts stay at Claude Code's 30 days** (the user, 2026-10-11, replacing
  the `cleanupPeriodDays` raised chosen earlier that day). The `SessionEnd` and Stop
  hooks are judged unreliable, and no hook keeps the measures. Each measure is
  recorded when it is taken: a tool review in its session, a review of several
  sessions at the end of its window. A longer window, a roadmap's, reads the records
  of the reviews it spans, and a window that starts before the oldest transcript kept
  is warned of, never counted short in silence. The design settles both.
- **A measure is there to lead to a conclusion** (the user, 2026-10-11). The design
  starts from the uses the measures serve, a return on each tool and a review of
  several sessions, and each figure it keeps is tied to the decision it informs.
- **The review of several sessions is run by hand** (the user, 2026-10-11), at a
  moment that makes it worth it, the end of a phase or of a roadmap. A phase closure
  does not start it: that would tie the roadmap domain to the review domain, which
  have no reason to depend on each other.
- **The roadmap is recentred on two uses** (the user, 2026-10-11): the return on each
  tool, and the review of several sessions as a skill of the review domain. The cost
  command becomes that skill's script. Phases 1 to 3 follow, below.
- **`study/session-review/` comes into this repository through a roadmap of its own**
  (the user, 2026-10-11), to be created; this roadmap's design keeps it in view so that
  the two share the reader rather than build two.
- **The design is approved** (the user, 2026-10-12), as the phase file's `## Design`
  holds it. Phases 1 and 2 build it; what follows binds them.
- **Every cost by model and effort, with its price** (the user, 2026-10-12): the
  conclusions on models and effort rest on it.
- **The review of several sessions compares the ways of going on after a stop** (the
  user, 2026-10-12): a hand-over note and a new session, the same session once its
  cache is lost, a compaction. The cache rebuilds leave the tool reviews for it. A way
  the window lacks is said, and earlier windows' records supply it.
- **The skill is named `reviewing-token-usage`** (the user, 2026-10-12): it measures
  tokens wherever they are spent, not one session's.
- **A window's record is kept in this repository's `reviews/windows/`** (the user,
  2026-10-12), whatever repository the window covers; the review runs in that
  repository, within 30 days of its window's start.
- **The tools reviewed are chosen** (the user, 2026-10-12): a review serves only a tool
  someone means to improve. A `[review]` table of `.agent-conventions.toml` lists them,
  where they are improved: this setup's in this repository's file, read by its path from
  every project; a repository's own in its file. Without the table, no review.
- **Reviews are processed, then archived** (the user, 2026-10-12): gone through with the
  user in this repository, then `--archive` starts the counters again; a tool version
  saturated with reviews is left out until then or until a new version. Budget: a median
  of $0.25 a review.
- **Each tool review says whether the tool served**, `full`, `partial` or `none` (the
  user, 2026-10-12), which `make reviews` reads to flag a tool that costs without
  serving.
- **Three reviews, three questions** (the user, 2026-10-12): `tool-review` and
  `session-review` ask what a tool brings for its cost, of this setup's tools and of a
  repository's; `reviewing-token-usage` where a stretch of work's tokens went. Whether
  the first two merge is roadmap `session-review`'s to decide.

---

## Files Changed

---

## Problems And Deviations

- **Task 3's proof compares with sessions the phase reports do not name.** Phase 5's
  report names no session, Phase 4's three, for other reasons. The windows were
  compared with the sessions the two records list instead, the counts by hand. The
  design does not count on a report naming its sessions.

---

## Changes To Later Phases

Restructurings approved by the user on 2026-10-11 and applied in roadmap 1.1.0:
- `phase-1-usage-reader.md`: the Objective counts for the tool reviews and the review of
  several sessions, and a window of sessions, a phase's among them; What It Enables, Out
  of Scope and the selection and shared-code tasks follow.
- `phase-2-reviews-and-reports.md`: the Objective puts the figures where they lead to a
  conclusion; Out of Scope keeps phase closures from starting the review; the
  `make reviews` task flags tools; Usage Command becomes Review Of Several Sessions, its
  command task the skill's script, a task added to write the skill, and keeping the
  measures becomes setting `cleanupPeriodDays`, 8 tasks to 9; the files, constraints and
  an acceptance criterion follow.
- `phase-3-validation-and-release.md`: the recount runs the review's script and sets its
  conclusions beside a record's; `CLAUDE.md` describes the skill under Layout.

Restructuring approved by the user on 2026-10-11 and applied in roadmap 1.2.0:
- `phase-2-reviews-and-reports.md`: the Objective drops the transcripts kept past 30
  days and the review of several sessions records what a longer window reads; the
  script task gains the record and the warning on a window older than the transcripts
  kept, with their proof; the task setting `cleanupPeriodDays` is removed, 9 tasks to
  8; the constraint on who sets it becomes the 30 days kept.
- `README.md`: Why This Roadmap Exists keeps the transcripts at 30 days, each measure
  recorded when it is taken.

Restructuring approved by the user on 2026-10-12 with the design, applied in roadmap
1.3.0:
- `phase-1-usage-reader.md`: the Objective adds the compactions; a task added, the probe
  of how a compaction is recorded, 5 tasks to 6; the price, count, deduplication,
  window and shared-code tasks and their proofs follow the design; the files name
  `shared/usage/`, `shared/sessions/` and `shared/reviewfile/`.
- `phase-2-reviews-and-reports.md`: the Objective adds the reviews processed and
  archived, the tools reviewed chosen by a list, the budget and the ways of going on
  after a stop, and names `reviewing-token-usage`; three tasks added, the list of tools
  reviewed, the saturation and the archive, 8 tasks to 11; the measured block,
  `make reviews`, script and skill tasks rewritten; the files, a constraint on reading
  the `[review]` table and an acceptance criterion follow.
- `README.md`: the two uses, Out Of Scope and the phases' counts.

Adjustment of another roadmap, approved by the user on 2026-10-12:
- Roadmap `session-review`, `phase-0-framing.md`: its comparison task reads this
  design's Boundaries and the list of tools reviewed; its design task decides whether
  `session-review` becomes the repository's side of one tool review, reading the
  repository's tools from the `[review]` key; its Dependencies say what the approved
  design settles. Its README becomes 1.0.2.

---

## Assessment
