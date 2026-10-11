# Token Costs Of Phase 5 Of `skill-tooling` — 2026-10-11

Measured on 2026-10-11, at the user's request, after Phase 5 of roadmap `skill-tooling`
closed, to give roadmap `token-usage` a third count by hand. Phase 5 ran in fourteen
sessions, most of them short and many spent watching eval runs started in the background,
and it paid for 248 `claude -p` sessions. The method is that of
`docs/decisions/2026-10-06-token-costs.md`, as `docs/decisions/2026-10-09-phase-4-token-costs.md`
applied it, counted with `shared/usage/usage.py`. No decision was taken on the figures:
What They Suggest lists what they bear on.

The transcripts these figures come from are deleted after 30 days, from 2026-11-08, so
this record is their source once they are gone.

## Method

- **Sources.**
  - The main transcripts of this repository from `585d56e6` (2026-10-09 00:34) to
    `e235aebc` (2026-10-11 14:17), which closed the phase, and the subagent files of
    `8f80c90c` and `e235aebc`. `23f69b8f` opened Phase 5 at 00:30 and stays counted in
    Phase 4. `585d56e6` measured Phase 4 and is counted here, as Phase 4's record counted
    the session that measured Phase 3. Two sessions of that span are left out and given
    apart: `8af16381`, which worked on roadmap `roadmap-dependencies`, and `be775c66`,
    which closed the roadmap after the phase.
  - The transcripts of the `claude -p` sessions whose first record falls in that span:
    folders under `~/.claude/projects/` named `-tmp-skill-run-`, `-tmp-skill-judge-` and
    `-tmp-skill-trigger-`. No probe left a transcript in a scratchpad.
- **Counting.** `usage.calls()`, each message id once. `a556427b` continues `c3561bb8`
  in a new process from 11:27 and copies the history they share, which is counted in
  `c3561bb8`. A `claude -p` session is given to the main session whose span holds its
  first record. None of their calls lacks its final usage, so none is estimated.
- **Sessions to tasks.** Each main session is matched to the tasks of its commits.
- **Checks.**
  - Fourteen of the fifteen main sessions have a `cost-state` record. Twelve equal the
    count to the cent. In `585d56e6` and `2e908d55`, `cost-state` holds $0.10 and $0.04
    more: calls on Claude Opus 5.5 that no transcript holds, each with a few output
    tokens and about 180,000 tokens of cache read. `e235aebc` had written no record on
    2026-10-11.
  - The 96 `claude -p` sessions that left a json result under `.eval-runs/` match it to
    the cent on Claude Sonnet 5.5, except one roadmap run, whose result is $0.012 higher.
    The results add $1.01 of Claude Haiku 4.5 calls that no transcript holds. The 144
    trigger sessions match the json of `triggers.py` to the cent.
  - The subagents of `8f80c90c`: 43 of their 52 calls lack their final usage. The
    estimate in `usage.py`, 5,400 output tokens a call, gives $3.73 where `cost-state`
    gives $1.50. Their calls averaged about 640 output tokens.
- **Prices.** Those of `usage.py`, read 2026-10-06. The main sessions ran on Claude Code
  2.1.293 to 2.1.296 in the VS Code extension, the `claude -p` sessions on 2.1.292.
  Claude Code's own calls in the main sessions now use Claude Haiku 5.5, which the table
  lacks. Its `cost-state` records fit $0.10 input and $0.50 output per million, plus
  $0.01 a web search. Every figure is an API price; the user's subscription meters its
  own way.
- **Estimates, marked ≈.**
  - The subagents of `e235aebc`, 9 calls, all without their final usage, are priced at
    640 output tokens a call, the figure measured in `8f80c90c`.
  - Documents read and tool reviews are priced as in the 2026-10-06 record: 3.5
    characters per token, each injected token one one-hour cache write plus a read by
    every later call.
  - A review runs from the Stop hook's request to the end of its turn. Where the turn
    goes on after `record.py` because a background notification arrived, the review
    ends at the call after `record.py`.
- **Tools.** One-off scripts, run in the session's scratchpad and not kept.

## Figures

### By session

Times in UTC+2. "Calls" are the main thread's API calls, all on Claude Opus 5.5 at
`xhigh`; the context is the input of one call, cached and fresh. The last column is the
`claude -p` sessions each one started.

| Session | Span | Work | Calls | Context, mean / peak | Main thread | `claude -p` |
|---|---|---|---|---|---|---|
| `585d56e6` | 10-09 00:34 → 00:55 | Phase 4's cost measure | 72 | 132k / 214k | $5.28 | — |
| `c3561bb8` | 10-09 10:24 → 11:24 | task 1 started; task 5, the trigger queries, the roadmap evals moved | 102 | 134k / 245k | $6.47 | $10.10 |
| `a556427b` | 10-09 11:27 → 12:33 | task 1; tasks 3, 9 | 61 | 227k / 255k | $5.38 | $5.69 |
| `1e1f7ebf` | 10-09 15:43 → 17:39 | task 1's runs | 59 | 75k / 92k | $1.86 | $8.34 |
| `b8e9ac00` | 10-09 17:41 → 17:58 | task 1's runs | 34 | 71k / 90k | $1.42 | $8.27 |
| `197b64c4` | 10-09 18:32 → 22:53 | task 1's runs | 49 | 79k / 98k | $2.59 | $16.41 |
| `a2151727` | 10-09 23:03 → 23:38 | task 1's runs | 42 | 74k / 92k | $1.57 | $12.40 |
| `6a1b5603` | 10-10 09:16 → 09:32 | task 1's runs | 27 | 70k / 83k | $1.12 | $4.30 |
| `8c8726fe` | 10-10 10:15 → 10:34 | task 1's runs and gradings | 39 | 78k / 98k | $1.55 | $8.76 |
| `a5814d4f` | 10-10 13:10 → 14:06 | task 1's gradings and benchmark; tasks 10, 11 | 73 | 130k / 203k | $4.56 | $4.62 |
| `e228b6e1` | 10-10 15:38 → 15:56 | task 2 | 42 | 88k / 110k | $2.41 | $16.72 |
| `8f80c90c` | 10-10 21:29 → 22:12 | tasks 4, 6 | 77 | 143k / 212k | $5.04 | — |
| `2e908d55` | 10-11 09:14 → 10:26 | task 7 | 84 | 153k / 202k | $5.21 | $6.08 |
| `ead9c2d4` | 10-11 10:50 → 11:16 | tasks 7, 8 | 55 | 112k / 151k | $2.86 | $1.87 |
| `e235aebc` | 10-11 13:36 → 14:17 | tasks 9, 12 to 14, closure | 76 | 142k / 200k | $4.71 | — |
| **Phase 5** | | | **892** | **123k / 255k** | **$52.04** | **$103.57** |

`a556427b`'s context carries the history of `c3561bb8`.

Beside these:
- the subagents: $1.50 in `8f80c90c`, nine `skill-auditor` runs on Sonnet 5.5 at
  `medium`, and ≈ $0.28 in `e235aebc`, one `skill-auditor` and one `roadmap-auditor`;
- the Haiku 4.5 calls of the `claude -p` results, $1.01;
- the Opus 5.5 calls outside the transcripts, $0.14;
- Claude Code's own Haiku 5.5 calls in the main sessions, under a cent each.

**Phase 5 cost ≈ $158.54**, and ≈ $153.16 without `585d56e6`, which measured Phase 4.

Apart from the phase: `8af16381`, 24 calls, $2.25; `be775c66`, the roadmap's closure, 69
calls at a mean context of 260k, $7.25 and ≈ $0.06 of `roadmap-auditor`.

### Against Phases 3 and 4

| | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|
| Sessions | 5 | 16 | 15 |
| Main thread's effort | `max` in four, `xhigh` in one | `xhigh` | `xhigh` |
| Main thread's calls | 704 | 1,233 | 892 |
| Calls a task, the cost measure left out | 59 | 81 | 59 |
| Context, mean / peak | ≈ 299k / 631k | ≈ 190k / 357k | ≈ 123k / 255k |
| Main thread | $88.29 | $115.47 | $52.04 |
| A call | $0.125 | $0.094 | $0.058 |
| A call: cache reads, writes, output | $0.059, $0.035, $0.031 | $0.037, $0.031, $0.025 | $0.024, $0.020, $0.015 |
| Thinking, of the main thread's output | 64% | 51% | 42% |
| Subagents, `claude -p` sessions, other models | $88.10 | ≈ $71.15 | ≈ $106.50 |
| **Total** | **$176.38** | **≈ $186.62** | **≈ $158.54** |

Phase 5's thinking share comes from the fourteen `cost-state` records: 247,182 of 592,696
output tokens.

- **A smaller context.** A call cost 38% less than in Phase 4 and 53% less than in
  Phase 3. The mean context fell 35% from Phase 4, and with it cache reads by 35%, cache
  writes by 37% and output by 42%. The output fell with the thinking, but the work
  differs between phases, so the comparison is not controlled.
- **Sessions that watched runs.** The six sessions that only moved task 1's runs on,
  `1e1f7ebf` to `8c8726fe`, never passed 98k. Each read the phase file and the report,
  started runs in the background and recorded their results. Their main thread cost
  $10.11, 17% of the $58.48 of runs and gradings they watched. Phase 4's task 9 watched
  $56.35 of runs for $28.45, 50%.
- **What grew.** The `claude -p` sessions: $103.57 against $69.32 in Phase 4, two thirds
  of the phase.

### Where it went

- **Main thread, $52.04.** Cache reads $21.53, 107.6 million tokens. Cache writes $17.50,
  2.19 million tokens, all one-hour. Output $13.00, 650,197 tokens.
- **By stage.**

  | Stage | Sessions | Calls | Main thread | Subagents, `claude -p` | Total |
  |---|---|---|---|---|---|
  | Phase 4's cost measure | 1 | 72 | $5.28 | — | $5.28 |
  | Task 1, with tasks 3, 5, 9 to 11 between its runs | 9 | 486 | $26.52 | $78.89 | $105.41 |
  | Task 2: triggers | 1 | 42 | $2.41 | $16.72 | $19.13 |
  | Tasks 4 and 6: `skill-auditor` | 1 | 77 | $5.04 | $1.50 | $6.54 |
  | Tasks 7 and 8: roadmap evals, install | 2 | 139 | $8.07 | $7.95 | $16.02 |
  | Tasks 9, 12 to 14, closure | 1 | 76 | $4.71 | ≈ $0.28 | ≈ $4.99 |

- **`claude -p` sessions, $103.57.**

  | Kind | Sessions | Calls | Cost |
  |---|---|---|---|
  | Task 1's runs, Sonnet 5.5 at `xhigh`, complete | 36 | 1,073 | $59.24 |
  | Task 1's runs stopped before their result | 8 | 173 | $10.52 |
  | Task 1's gradings, Sonnet 5.5 | 36 | 315 | $9.14 |
  | Task 2's triggers, Opus 5.5 at `xhigh` | 144 | 279 | $16.72 |
  | Task 7's roadmap runs, Sonnet 5.5 | 24 | 362 | $7.95 |

- **Task 1, $78.90 of `claude -p` sessions, half the phase.** Its constraints announced
  about $47 for 36 runs and about $9 for their gradings.

  | Configuration | Runs | Cost | A run |
  |---|---|---|---|
  | `authoring-skills`, iteration A | 9 | $12.48 | $1.39 |
  | No skill, iteration A | 9 | $15.58 | $1.73 |
  | `writing-skills` 6.4.1, iteration B | 9 | $13.56 | $1.51 |
  | skill-creator, iteration C | 9 | $17.62 | $1.96 |

  - A complete run cost $1.65 on average, against $1.30 announced. `run.py` announced
    A's 18 runs at $0.71 each: the mean of the skill's earlier complete runs, all
    cases mixed.
  - A grading cost $0.25.
  - The runs stopped before their result cost $10.52:
    - $9.28 to the subscription's limit, which stopped one run that ran alone and six
      started together;
    - $1.24 to a run started from a session as a background command, which ended when
      the user closed the editor's window.

    Phase 4 lost $17.26 to the limit.
- **Task 2, $16.72, for two measures announced at $3.67 each.**
  - The measures cost $8.35 and $8.37, each 24 queries of three sessions.
  - The 12 near misses make 86% of it. A session that should not trigger answers the
    query in full: $0.24 for a query's first session and $0.18 for each repeat. The
    defaults in `triggers.py`, from Phase 4, give $0.12 and $0.04.
  - A query that should trigger cost what the defaults give: $0.08 and $0.009.
- **One-hour cache writes in `claude -p` sessions.**
  - Every `claude -p` session wrote one-hour cache entries, at twice the input price.
    A run lasts about ten minutes, and a trigger session a few seconds.
  - Writes make 33% of the runs' cost, 57% of the gradings' and 79% of the triggers'.
  - At the five-minute price, 1.25 times the input price, the 248 sessions would have
    cost $16.70 less, 16%. No probe has checked whether a `claude -p` session can ask
    for five-minute entries.

### Openings and fixed costs

Thirteen sessions opened on the phase. `585d56e6`, which measured Phase 4, and
`a556427b`, which continued `c3561bb8`, are left out.

- **Opening.**
  - A session's first call held 35,000 to 37,000 tokens, as in Phase 4.
  - Each opening read the phase file and the report in full. The report grew from
    5,259 characters in `c3561bb8` to 99,113 in `e235aebc`.
  - Up to its first question to the user, or before its first edit or subagent, a
    session made 5 to 13 calls. It reached 58,000 to 99,000 tokens, 72,000 on average,
    and spent $0.43 to $0.89.
  - That is $7.10 in all, $0.55 a session, 17% of these sessions' $41.38 of main
    thread.
  - Phase 4's closer bound, the calls up to each session's last read of a roadmap
    document, gave $1.27 a session.
- **Roadmap documents read**, in the fourteen sessions.

  | Document | Reads | Tokens | Cost |
  |---|---|---|---|
  | Phase 5's report | 18 | ≈ 158k | ≈ $3.10 |
  | The roadmap skill: its body loaded 14 times, its files read 22 times | 36 | ≈ 60k | ≈ $1.09 |
  | Phase 5's phase file | 9 | ≈ 25k | ≈ $0.50 |
  | Other roadmap documents | 9 | ≈ 6k | ≈ $0.08 |
  | Decision records | 3 | ≈ 6k | ≈ $0.07 |
  | Phase 4's file and report | 6 | ≈ 2k | ≈ $0.04 |
  | **Total** | | **≈ 257k** | **≈ $4.88** |

  Phase 4's documents cost about $13.25, its report alone about $5.92. Phase 5's report
  ended at 105,685 characters, about 30,000 tokens; Phase 4's at 175,249.
- **Tool reviews.**
  - The Stop hook asked for 15: one in each of the fourteen sessions, and a second in
    `ead9c2d4` and `e235aebc`, where a tool first served after the first review.
  - They took 69 calls and $2.88, and about $0.64 for the context they left to later
    calls: ≈ $3.52, ≈ $0.23 a review. Phase 4's 18 cost about $6.09, $0.34 each.
  - `585d56e6` had two more, ≈ $0.65.
- **Cache rebuilds.** Four. In each, the session went on under another organization, as
  its `credential_org` records show:
  - `a556427b` at 11:27, 171,000 tokens, three minutes after `c3561bb8`'s last call;
  - `197b64c4` at 18:39, 46,000 tokens, after 7 minutes, and at 22:18, 53,000 tokens,
    after 217 minutes, past the cache's hour;
  - `e228b6e1` at 15:54, 81,000 tokens, with no pause.

  351,000 tokens, ≈ $2.74. Phase 4 had four, 812,000 tokens, ≈ $6.50; Phase 3 three,
  ≈ $8.50.
- **Break-even.**
  - A new session pays an opening, about $0.55, and a tool review, about $0.23. It
    starts its work at about 72,000 tokens.
  - Continuing reads, at each call, the context past that point. That costs $0.010 a
    call at Phase 5's mean of 123,000 tokens, so a new session pays back after about 76
    calls. At 200,000 tokens it costs $0.026 a call and pays back after 30; at the peak
    of 255,000, $0.037 and 21.
  - Phase 5's work sessions ran 59 calls on average, below break-even.
  - One session in place of the six that watched task 1's runs would have saved five
    openings and five reviews, $3.20. It would have read $2.68 more cache, as its
    context grew to about 236,000 tokens.
  - That leaves $0.52 saved, before the rebuild after the night between `a2151727` and
    `6a1b5603`, about $1.20 at 150,000 tokens.
  - Openings and reviews together cost ≈ $10.62, 23% of the fourteen sessions' main
    thread.

## What They Suggest

Nothing was decided on 2026-10-11. The figures bear on:

- **Roadmap `token-usage`.**
  - The reader's estimate of a subagent's output. One figure for every agent, 5,400
    tokens a call from Phase 3's runs, is eight times too high for `skill-auditor`,
    about 640. An estimate per agent would come closer. So would the Agent tool's
    result, which holds the usage of the subagent's last call. Where a `cost-state`
    record exists, it remains the reference.
  - The price table lacks Claude Haiku 5.5, used by Claude Code's own calls in the main
    sessions; `claude -p` sessions still call Haiku 4.5.
  - Selection. A conversation continued in a new process copies the history it shares,
    which counting by message id handles. A phase's main sessions were still found by
    their commits, and 248 `claude -p` sessions by their first record, with one-off
    scripts.
  - A review's slice. It ends with its turn. A session waiting on background runs
    carries on in that same turn after the review.
  - What a review may cost, Phase 0's question: ≈ $0.23 in Phase 5, two in a session
    when a tool first serves after the first.
  - Its last phase recounts a closed phase against a count by hand: this record is the
    third, ≈ $158.54, the per-session table holding once the transcripts are gone.
- **Roadmap `roadmap-execution`, Phase 0.**
  - Phase 5's sessions sat below break-even. One session for the six that watched runs
    would have saved about $0.52 before a night's rebuild.
  - What lowered the main thread was a context that stayed small, with an opening at
    about $0.55, not the number of sessions.
- **The eval scripts of `authoring-skills`.**
  - `triggers.py`'s defaults for a near miss are two to four times under what this
    skill's near misses cost. Its next estimate for this skill rests on the recorded
    sessions; a new skill still gets the defaults.
  - `run.py` estimates from the mean over all of a skill's cases. It announced $0.71 a
    run for runs that cost $1.39 to $1.96.
  - The one-hour cache writes of `claude -p` sessions: $16.70 of $103.57 at five-minute
    prices, if a session can ask for them.
  - Runs started together share the subscription's limit: six stopped at once cost
    $8.31.

## When To Revisit

- **When Phase 0 of `roadmap-execution` settles hand-overs:** these figures stand
  beside those of Phases 3 and 4.
- **When a tool counts a phase's costs:** its count of Phase 5 is checked against this
  record, ≈ $158.54.
- **When prices or the `cost-state` record change:** the method's prices follow, as in
  the 2026-10-06 record, and Claude Haiku 5.5's price enters the table.
