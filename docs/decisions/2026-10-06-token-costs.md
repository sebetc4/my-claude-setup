# Token Costs Of Sessions And Eval Runs — 2026-10-06

Measured on 2026-10-06, at the user's request, after Phase 3 of roadmap `skill-tooling`
cost about $167 over five sessions. Decided with the user the same day: **the figures
go to two roadmaps as constraints and tasks, and the designs are settled there.** Phase 4
of `skill-tooling` runs its evals at an effort and a model it fixes and counts each
run's cost; Phase 0 of `roadmap-execution` settles when `execute-phase` hands over to a
new session. The user also proposed that the review domain measure token consumption.

The transcripts these figures come from are deleted after 30 days, so this record is
their source once they are gone.

## Method

- **Sources.** The transcripts under `~/.claude/projects/`: each session's own file, its
  subagents' files under `<session>/subagents/`, and the `cost-state` records Claude
  Code writes into a session's file when it is resumed or ends, which hold its totals
  per model, subagents included, with a `costUSD`.
- **Counting.** One usage per assistant `message.id`, the last record kept. A resumed
  session copies the history it continues into a new file, so sessions sharing message
  ids are counted once, each message given to the first session that holds it.
- **Prices.** Claude Opus 5.5: $4 per million input tokens, $20 output, $0.20 cache read,
  $8 cache write with the one-hour lifetime Claude Code uses. Claude Sonnet 5.5: $2, $10,
  $0.20, and $2.50 for a cache write, the price Claude Code applies to it. Claude Opus 5:
  $5, $25, $0.50, $10. The input and output prices come from the `claude-api` skill
  bundled with Claude Code 2.1.289 (table cached 2026-09-25). The cache prices are fitted
  to the `cost-state` records, which Opus 5.5's three sessions and Sonnet 5.5's ten
  records match to the cent. Opus 5's cache prices are taken as 0.1 and 2 times its
  input price, without a record to check them against. Every figure is an API price;
  the user's subscription meters its own way.
- **Output tokens.** A main session's transcript holds its final output counts. Its sum
  equals `cost-state` in each of the three cases checked. A subagent's transcript does
  not: most of its records keep the count written when the message started streaming.
  In the first half of session `f2b80cf5`, they hold 88,681 output tokens where
  `cost-state` counts 804,047. Where no `cost-state` covers the subagents, their output
  is estimated at 3,700 tokens per call, the mean of the three measured cases, and the
  figure is marked ≈.
- **Tools.** One-off scripts, run in the session's scratchpad and not kept. Phase 4
  builds the counted version.

## Figures

### Phase 3 of `skill-tooling`, by session

Times in UTC+2. "Calls" are the main thread's API calls; the context is the input of one
call, cached and fresh.

| Session | Span | Effort | Calls | Context, mean / peak | Main thread, Opus 5.5 | Subagents and other models | Total |
|---|---|---|---|---|---|---|---|
| `1cee558e` | 10-04 19:41 → 10-05 09:07 | max | 124 | 274k / 448k | $16.87 | $20.64 | $37.50 |
| `10444f3f` | 10-05 11:58 → 13:50 | max | 108 | 242k / 407k | $12.68 | $14.43 | $27.11 |
| `f2b80cf5` | 10-05 19:22 → 10-06 09:15 | max | 189 | 294k / 506k | $23.23 | ≈ $26 | ≈ $49 |
| `a2b3cf86` | 10-06 12:59 → 17:09 | max | 225 | 392k / 631k | $32.32 | ≈ $18 | ≈ $50 |
| `ed7dbe88` | 10-06 20:46 → 21:09 | xhigh | 58 | 118k / 158k | $3.19 | ≈ $0.3 | ≈ $3.5 |
| **Phase 3** | | | **704** | | **$88.28** | **≈ $79** | **≈ $167** |

Phase 2 ran in one session, `2f2e66de`, which also closed roadmap `superpowers-study`:
$54, $3 of it in subagents.

### Where it went

- **Main thread, $88.28.** Cache reads $41.50, cache writes $24.74, output $22.04. The
  output is 1.10 million tokens, 704,000 of them thinking (64%).
- **Cache rebuilds.** The whole context was written again three times, about $8.50 in
  all:
  - twice after a night's pause, which outlived the cache's hour: 177,000 and 373,000
    tokens;
  - once, 514,000 tokens, at 15:35 on 2026-10-06. Twenty minutes earlier, the
    subscription's session limit had stopped `a2b3cf86` ("You've hit your session
    limit"). The session resumed under an organization credential the transcript
    records (`credential_org`), and the cache did not survive the change.
- **Subagents, about $79.** Most of it is runs, from the baseline to the reruns after a
  fix:

  | Kind | Runs | Cost |
  |---|---|---|
  | Full-task runs: baseline, guide, procedure, Verification, reruns | 23 | ≈ $57.50, ≈ $2.50 each |
  | `skill-auditor` runs: fixtures, rounds, final audits | 45 | ≈ $20.10, ≈ $0.45 each |
  | Routing evals | 10 | ≈ $0.90 |
  | `roadmap-auditor` | 1 | ≈ $0.30 |
  | Probes, on Haiku | 3 | ≈ $0.10 |

  Thinking makes 84% of the subagents' output where `cost-state` measures it: 1.86
  million of 2.21 million tokens.
- **Effort of the runs.** The general-purpose agents that ran the evals took the
  session's effort. In the four sessions at `max`, 2,586 of their calls ran at `max`, 19
  at `medium`, all in three reruns of `f2b80cf5`, and 16 recorded none. No run set its
  own effort. `roadmap-auditor`, whose definition declares no effort, ran at `medium` in
  a session at `xhigh`.

### Effort

Opus 5.5 main threads of every project, 2026-09-24 to 2026-10-06, 5,808 calls once
deduplicated. Output tokens per call:

| Effort | Calls | Output per call | Of which thinking |
|---|---|---|---|
| max | 3,020 | 1,942 | 1,211 (62%) |
| xhigh | 1,537 | 1,366 | 676 (49%) |
| high | 908 | 959 | 325 (34%) |
| medium | 333 | 858 | 276 (32%) |

The comparison is not controlled: different tasks ran at each level, and no measure says
what `max` adds to quality. The thinking stays in the context: in `a2b3cf86`, it is
179,000 of the final 631,000 tokens. The `claude-api` skill names `xhigh` the best setting
for most coding and agentic work on the models it lists, and Claude Code's default. On
cost, it advises raising effort to `max` only when a measure shows headroom at the level
below.

### Long sessions

- No main context shrank: no compaction ran, and every call read the whole history
  again.
- **Reorientation.** A session that started on a phase took 9 to 17 calls and $0.57 to
  $1.16 to read the skill, the phase file and the report. It reached a context of 62,000
  to 108,000 tokens before its first edit.
- **Break-even.** Continuing costs, at each call, a read of the context a fresh session
  would not hold: about (context − 100,000) × $0.20 per million. That is $0.04 a call at
  300,000 tokens and $0.08 at 500,000. A reorientation of about $1 pays back after
  roughly 25 calls at 300,000 tokens, and 12 at 500,000.
- **Simulation.** A Phase 3 task took about 59 main calls: 704 calls for 12 tasks. A new
  session every 60 calls, each paying its session's measured reorientation, gives nine
  hand-overs. They save $20.23 of reads for $7.81 of reorientation, $12.42 net, 14% of
  the main thread. Fresh sessions after the pauses would also avoid most of the $8.50 of
  rebuilds.

### This setup's tools

Phase 3's main threads. Costs are estimated at 3.5 characters per token, each injected
token priced as one cache write plus a read by every later call.

| Tool | Cost |
|---|---|
| Roadmap documents read: phase files, reports, about 47,000 tokens | ≈ $2.30 |
| `tool-review` at the Stop hook: 23 calls, and its text kept in context | ≈ $2.45 |
| The roadmap skill's body, about 2,000 tokens per session | ≈ $0.35 |
| Every hook: `audit_skill.py`, `check-skills.py`, `session_resume.py`, `progress_guard.py`, the review's Stop hook | ≈ $0.16 |
| **Total** | **≈ $5.25, 6% of the main thread** |

The largest document is the phase's report, which grows through the phase and which a
session resuming the phase reads in full. Phase 3's report ended at 103,289
characters, about 30,000 tokens.

### Other projects

The costliest main threads still on disk, deduplicated:

| Date | Repository | Model | Calls | Peak context | Main thread |
|---|---|---|---|---|---|
| 2026-09-18 | scriptorium | Opus 5 | 562 | 898k | $191.90 |
| 2026-09-10 | pdf-creator | Opus 5 | 259 | 718k | $102.13 |
| 2026-09-18 | forma-rust | Opus 5.5, mostly | 438 | 927k | $81.84 |
| 2026-10-02 | my-claude-setup, Phase 2 | Opus 5.5 | 278 | 852k | $50.71 |

Long sessions with contexts past 600,000 tokens are the rule in every repository, not a
trait of Phase 3. What set Phase 3 apart is its runs.

## What It Changes

- **Roadmap `skill-tooling`, Phase 4.**
  - Its constraints say where a run's output tokens are found.
  - Runs take a fixed effort and model.
  - The benchmark counts cost.
  - A design task measures the same evals at two efforts before the runs' effort is
    set.
- **Roadmap `roadmap-execution`, Phase 0.** A design task settles when `execute-phase`
  hands over to a new session, on the figures of Long sessions. Its opening decision has
  one phase run in one conversation, so this task may change that verdict.
- **The review domain.** The user proposed on 2026-10-06 that `domains/review` measure
  token consumption too. Its `transcript.py` already reads a session's slice: fresh
  input, cache reads and output. No roadmap holds the work yet.

## Recount

Run on 2026-10-06 with `shared/usage/usage.py`, the reader Phase 4 of `skill-tooling`
wrote, over the same transcripts. Three sessions, `f2b80cf5`, `a2b3cf86` and `ed7dbe88`,
wrote their `cost-state` records when they ended, after this record, so every session
now has one.

- **Main threads.** The count equals each session's `cost-state` for Opus 5.5 to the
  cent: $16.87, $12.68, $23.23, $32.33 and $3.19, $88.29 in all. The table above gives
  $88.28 from rounded figures.
- **Sessions.** By `cost-state`, Phase 3 cost **$176.38**: $37.50, $27.11, $48.26,
  $60.13 and $3.38. Subagents and Claude Code's own Haiku calls make $88.10 of it, not
  about $79; `a2b3cf86`'s subagents alone cost $27.81, not about $18.
- **Cache-write prices.** A cache write costs 1.25 times the input price for a
  five-minute entry and twice the input price for a one-hour entry. Subagents write
  five-minute entries and main sessions one-hour entries. Sonnet 5.5's $2.50 above is its
  five-minute price; its one-hour price is $4, as the results of `claude -p` sessions on
  2.1.291 show. Haiku 4.5's $1 input and $5 output match a `cost-state` record.
- **Subagent output.** A call lacks its final usage when its last record carries no
  `stop_reason`. Over Phase 3's 711 such calls on Sonnet 5.5, the `cost-state` records
  give a mean of 5,371 output tokens each. The method above estimated 3,700 tokens per
  call of any kind. `usage.py` estimates 5,400 for each such call and marks it. Per
  session, the estimated cost is off by −35% to +27%; over the five sessions, by 0.2%.
- **Calls outside the transcripts.** Claude Code's own Haiku calls appear in
  `cost-state` and in no transcript: $0.10, $0.06 and $0.002 in three sessions.

## When To Revisit

- **When Phase 4 has measured the same evals at two efforts:** its result replaces the
  uncontrolled effort table.
- **When prices or the `cost-state` record change:** the method's prices and its
  correction of subagent output follow.
- **When a tool counts costs:** Phase 4 or the review domain. Its first count of a
  phase is checked against this record's method.
