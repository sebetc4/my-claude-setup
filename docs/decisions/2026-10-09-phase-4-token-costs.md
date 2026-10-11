# Token Costs Of Phase 4 Of `skill-tooling` — 2026-10-09

Measured on 2026-10-09, at the user's request, after Phase 4 of roadmap `skill-tooling`
ran in sixteen short sessions instead of Phase 3's five long ones, the user managing the
context and the sessions to spend less. The method is that of
`docs/decisions/2026-10-06-token-costs.md`, counted with `shared/usage/usage.py`. No
decision was taken on the figures the day they were recorded: What They Suggest lists
what they bear on.

The transcripts these figures come from are deleted after 30 days, from 2026-11-05, so
this record is their source once they are gone.

## Method

- **Sources.**
  - The main transcripts of this repository from `8a3f412b` (2026-10-06 21:14) to
    `23f69b8f` (2026-10-09 00:30), and the subagent files of `23f69b8f`, the only
    session with subagents. `ed7dbe88` opened Phase 4 at 21:08 and stays counted in
    Phase 3. `7af1242d` made no call.
  - The transcripts of the `claude -p` sessions whose first record falls in that span:
    folders under `~/.claude/projects/` named `-tmp-skill-run-`, `-tmp-skill-grade-`,
    `-tmp-skill-judge-`, `-tmp-skill-trigger-` and `-tmp-skill-rewrite-`, and the
    probes under the scratchpads of `fc3bbbd2` and `28575edf`.
- **Counting.** `usage.calls()`, each message id once. A `claude -p` session is given to
  the main session whose span holds its first record. None of their calls lacks its
  final usage, so nothing is estimated.
- **Checks.**
  - Thirteen main sessions have a `cost-state` record, and each equals the count to the
    cent. `3e3cb8b0`, `abe452df` and `23f69b8f` had written none on 2026-10-09.
  - The 128 `claude -p` sessions that left a json result under `.eval-runs/` match it
    to the cent on Claude Sonnet 5.5. The results add $1.20 of Claude Haiku 4.5 calls
    that no transcript holds.
- **Prices.** Those of `usage.py`, read 2026-10-06. Claude Code 2.1.289 to 2.1.293. Every
  figure is an API price; the user's subscription meters its own way.
- **Estimates, marked ≈.** Documents read and tool reviews are priced as in the
  2026-10-06 record: 3.5 characters per token, each injected token one one-hour cache
  write plus a read by every later call. A review runs from the Stop hook's request to
  the user's next prompt. The Read tool's line numbers make the documents' figures a
  little high.
- **Tools.** One-off scripts, run in the session's scratchpad and not kept.

## Figures

### By session

Times in UTC+2. "Calls" are the main thread's API calls, all on Claude Opus 5.5 at
`xhigh`; the context is the input of one call, cached and fresh. The last column is the
`claude -p` sessions each one started.

| Session | Span | Work | Calls | Context, mean / peak | Main thread | `claude -p` |
|---|---|---|---|---|---|---|
| `8a3f412b` | 10-06 21:14 → 22:35 | Phase 3's cost measure | 95 | 219k / 357k | $10.19 | — |
| `b7d2f2a7` | 10-06 22:38 → 23:02 | task 1 | 43 | 185k / 266k | $5.22 | — |
| `fc3bbbd2` | 10-06 23:06 → 23:40 | tasks 2, 3 | 96 | 174k / 277k | $7.96 | $1.39 |
| `e5c48457` | 10-06 23:40 → 10-07 00:10 | tasks 4, 5 | 70 | 167k / 256k | $6.85 | $0.11 |
| `4700fd1c` | 10-07 00:10 → 00:37 | tasks 6, 7 | 66 | 179k / 256k | $6.24 | $0.73 |
| `dc7d5399` | 10-07 00:38 → 00:53 | task 8 | 35 | 142k / 190k | $3.48 | — |
| `3d474511` | 10-07 12:40 → 19:58 | task 9 | 123 | 210k / 310k | $15.18 | $38.47 |
| `d9a8d9a0` | 10-08 09:05 → 11:35 | task 9 | 80 | 127k / 174k | $5.13 | $17.88 |
| `8b22a5a0` | 10-08 13:07 → 14:50 | task 9 | 88 | 198k / 308k | $8.14 | — |
| `871b9d72` | 10-08 14:56 → 16:08 | task 10 | 102 | 230k / 327k | $9.10 | $3.15 |
| `28575edf` | 10-08 16:10 → 17:13 | tasks 10, 11 | 84 | 176k / 288k | $7.11 | $0.61 |
| `6a93eb54` | 10-08 17:16 → 17:53 | task 12 | 53 | 188k / 252k | $5.69 | $0.03 |
| `80964ead` | 10-08 17:54 → 18:47 | task 13 | 68 | 221k / 293k | $7.24 | $0.83 |
| `3e3cb8b0` | 10-08 19:59 → 21:09 | task 13 | 74 | 176k / 238k | $5.15 | $0.58 |
| `abe452df` | 10-08 20:47 → 21:15 | task 14 | 73 | 203k / 289k | $6.71 | $0.56 |
| `23f69b8f` | 10-08 23:30 → 10-09 00:30 | task 14, closure | 83 | 189k / 260k | $6.09 | $4.97 |
| **Phase 4** | | | **1,233** | **190k / 357k** | **$115.47** | **$69.32** |

Beside these: `roadmap-auditor` in `23f69b8f`, 5 calls, $0.63; the Haiku calls of the
`claude -p` results, $1.20; Claude Code's own calls in the main sessions, under a cent
each. **Phase 4 cost ≈ $186.62**, and ≈ $176.43 without `8a3f412b`, which measured
Phase 3.

### Against Phase 3

| | Phase 3 | Phase 4 |
|---|---|---|
| Sessions | 5 | 16 |
| Main thread's effort | `max` in four, `xhigh` in one | `xhigh` |
| Main thread's calls | 704 | 1,233 |
| Calls a task, `8a3f412b` left out | 59 | 81 |
| Context, mean / peak | ≈ 299k / 631k | ≈ 190k / 357k |
| Main thread | $88.29 | $115.47 |
| A call: cache reads, writes, output | $0.059, $0.035, $0.031 | $0.037, $0.031, $0.025 |
| Thinking, of the main thread's output | 64% | 51% |
| Subagents, `claude -p` sessions, other models | $88.10 | ≈ $71.15 |
| **Total** | **$176.38** | **≈ $186.62** |

Phase 3's mean context is its five sessions' means weighted by their calls. Phase 4's
thinking share comes from the thirteen `cost-state` records: 699,492 of 1,381,747 output
tokens.

- **What the shorter sessions bought.** A call reads 37% less cache. At Phase 3's mean
  context, Phase 4's 1,233 calls would have read about $27 more.
- **What took it back.** 62% more main calls for the phase's work, 1,138 against 704,
  task 9's measure, and the fixed costs of sixteen openings, below.

### Where it went

- **Main thread, $115.47.** Cache reads $45.84, 229.2 million tokens. Cache writes
  $38.37, 4.80 million tokens, all one-hour. Output $31.26, 1.56 million tokens.
- **By stage.**

  | Stage | Sessions | Calls | Main thread | `claude -p` | Total |
  |---|---|---|---|---|---|
  | Phase 3's cost measure | 1 | 95 | $10.19 | — | $10.19 |
  | Tasks 1–3: design, probes, usage reader | 2 | 139 | $13.18 | $1.39 | $14.57 |
  | Tasks 4–8: workspace, runs, grader, grading, benchmark | 3 | 171 | $16.57 | $0.84 | $17.41 |
  | Task 9: effort measured | 3 | 291 | $28.45 | $56.35 | $84.80 |
  | Tasks 10–13: viewer, triggers, tuning, comparison | 5 | 381 | $34.29 | $5.20 | $39.49 |
  | Task 14 and closure | 2 | 156 | $12.80, and $0.63 of subagent | $5.53 | $18.96 |

- **`claude -p` sessions, $69.32.** One subagent ran in the whole phase. What the user
  saw as subagents were 218 `claude -p` sessions:

  | Kind | Sessions | Calls | Cost |
  |---|---|---|---|
  | Runs, Sonnet 5.5: 597 calls at `xhigh`, 435 at `max` | 67 | 1,032 | $56.32 |
  | Grading, Sonnet 5.5 | 64 | 366 | $8.44 |
  | Judgment (`-tmp-skill-judge-`), Sonnet 5.5 | 56 | 176 | $2.89 |
  | Probes in scratchpads | 24 | 47 | $1.45 |
  | Triggers, Opus 5.5 | 6 | 6 | $0.19 |
  | Description rewrite, Opus 5.5 | 1 | 1 | $0.03 |

- **Task 9, $84.80, 46% of the phase.** Its runs cost $56.35, and $17.26 of it went to
  runs the measure could not use: the twelve set aside under
  `.eval-runs/skills/authoring-skills/limit-2026-10-07/`, $12.86, and two runs at `max`
  stopped by the subscription's limit before their result, $4.40. The phase's report
  gave about $20 from the json results, which add Haiku.

### Openings and fixed costs

Fifteen sessions worked on the phase, `8a3f412b` left out: 35 to 123 calls, 76 on
average.

- **Opening.** A session's first call held 35,000 to 37,000 tokens. Before its first
  edit in the repository outside `docs/roadmap/`, a session made 8 to 56 calls, reached
  87,000 to 253,000 tokens, 153,000 on average, and spent $0.70 to $4.50: $31.73 in
  all, 30% of the fifteen sessions' $105.28. That bound is high, since it holds design
  and probes. The calls up to each session's last read of a roadmap document, a closer
  bound, cost $19.11, $1.27 a session.
- **Roadmap documents read.**

  | Document | Reads | Tokens | Cost |
  |---|---|---|---|
  | Phase 4's report | 39 | ≈ 271k | ≈ $5.92 |
  | Phase 4's phase file | 26 | ≈ 170k | ≈ $3.81 |
  | Decision records | 29 | ≈ 53k | ≈ $1.02 |
  | Other roadmap documents | 24 | ≈ 45k | ≈ $0.89 |
  | The roadmap skill | 35 | ≈ 38k | ≈ $0.82 |
  | Phase 3's report | 11 | ≈ 43k | ≈ $0.80 |
  | **Total** | | **≈ 620k** | **≈ $13.25** |

  Phase 3's documents cost about $2.30. Phase 4's report ended at 175,249 characters,
  about 50,000 tokens; Phase 3's at 103,289.
- **Tool reviews.** The Stop hook asked for 18, one in each session and two in
  `8a3f412b` and `23f69b8f`: 93 calls, $5.43, and about $0.66 for the context they left
  to later calls, ≈ $6.09. Phase 3's 23 calls cost about $2.45.
- **Cache rebuilds.** Four, each where the session went on under another organization
  after the subscription's session limit, as the `credential_org` record shows:
  `3d474511` at 13:35, 17:51 and 19:12, 165,000, 250,000 and 279,000 tokens, and
  `d9a8d9a0` at 10:46, 118,000 tokens. The gaps before them were 17, 236, 15 and 41
  minutes, so the change, not the cache's hour, lost three of them. 812,000 tokens,
  ≈ $6.50. Phase 3 had three, ≈ $8.50.
- **Break-even.** At 250,000 tokens, continuing reads about 100,000 tokens a call that a
  session opened at about 150,000 would not, $0.02 a call. An opening at $1.27 to $2.12
  pays back after 65 to 105 calls. Phase 4's sessions ran 76 calls on average, near that
  point: shorter sessions would have saved little, and the opening is what costs.

## What They Suggest

Nothing was decided on 2026-10-09. The same day, at the user's request, the roadmaps
below were given these figures as inputs and constraints, and Phase 5 of `skill-tooling`
its run costs; the decisions stay with their tasks. The figures bear on:

- **Roadmap `roadmap-execution`, Phase 0.** Its hand-over task rests on Phase 3's
  simulation, a new session every 60 calls saving 14%. Phase 4 ran close to that rule
  and its sessions sat near break-even, because an opening costs $1.27 to $2.12 and the
  report it reads grew to about 50,000 tokens. A resume point read in place of the whole
  report lowers the opening, and with it the length a session needs to pay back.
- **The review domain.** One review per session cost about $6.09 over sixteen sessions.
- **Roadmap `token-usage`.** This count took five one-off scripts around `usage.calls()`
  to find the phase's sessions and the `claude -p` sessions they started, and to give
  each to its session. Its last phase recounts a closed phase against a count by hand:
  this record is one.
- **Eval runs.** $17.26 went to runs lost to the subscription's limit. `run.py` stops on
  `limit_reached` since task 9.

## When To Revisit

- **When Phase 0 of `roadmap-execution` settles hand-overs:** these figures stand beside
  Phase 3's.
- **When a tool counts a phase's costs:** its count of Phase 4 is checked against this
  record, ≈ $186.62. Phase 5 was counted the same way on 2026-10-11:
  `2026-10-11-phase-5-token-costs.md`.
- **When prices or the `cost-state` record change:** the method's prices follow, as in
  the 2026-10-06 record.
