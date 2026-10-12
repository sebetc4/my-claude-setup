# Token Usage — 2026-10-12

Decided with the user on 2026-10-11 and 2026-10-12, in Phase 0 of roadmap `token-usage`:
**the review domain measures what this setup's tools and a stretch of work cost, in
dollars per model and effort, so as to conclude what to change.** A figure no decision
reads is not computed. This record and the design, both approved by the user on
2026-10-12, stand together: the design is the `## Design` section of
[the phase file](../roadmap/pending/token-usage/phase-0-framing.md); this record keeps
what it decided, the figures it rests on, and how the domain's four open defects are
fixed.

## Decisions

- **Two uses.** The return on each tool: each tool review carries the slice's cost by
  model and effort and the tool's own cost, beside what the tool brought and whether it
  served (`full`, `partial`, `none`); `make reviews` flags a tool whose new version costs
  more, or that costs without serving. A review of several sessions: the skill
  `reviewing-token-usage`, run by hand at the end of a phase, a roadmap or a stretch of
  work, in the repository it reviews, never started by a phase closure.
- **Three reviews, three questions.** `tool-review` asks what one of this setup's tools
  brings for its cost; `session-review`, which roadmap `session-review` brings in, asks
  it of a repository's own tools; `reviewing-token-usage` asks where a stretch of work's
  tokens went and how the work should run. Whether the first two become one tool review
  with two catalogs is roadmap `session-review`'s to decide.
- **The tools reviewed are chosen.** A review serves only a tool someone means to
  improve. A `[review]` table of `.agent-conventions.toml` lists them where they are
  improved: this setup's in this repository's file, read by its path from every project;
  a repository's own in its file. Without the table, no review.
- **Reviews are processed, then archived.** Gone through with the user in this
  repository, each finding carried into a roadmap or set aside, then archived; the
  findings and the saturation count only the reviews not archived. A tool version holding
  ten complete reviews whose last five raised nothing new is left out until a new version
  or an archive. Budget: a median of $0.25 a review.
- **The transcripts stay at Claude Code's 30 days.** Each measure is recorded when it is
  taken; a window's record, kept in this repository's `reviews/windows/`, serves a longer
  window, and a window older than the transcripts kept is warned of.
- **Three ways of going on after a stop are compared:** a hand-over note and a new
  session, the same session once its cache is lost, and a compaction, not tried yet.
- **One reader.** `shared/usage/` extended, `shared/sessions/` new for a window: prices
  with their date and source, every subagent, a run's last output from the Agent tool's
  result, a shared message id given to the transcript whose last record comes first,
  each call of a window counted by its time.

## Figures

From the three counts by hand (`2026-10-06-token-costs.md`,
`2026-10-09-phase-4-token-costs.md`, `2026-10-11-phase-5-token-costs.md`) and Phase 0's
probes:

| | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|
| Phase, all counted | ≈ $176.38 | ≈ $186.62 | ≈ $158.54 |
| `claude -p` sessions | — | 218, $69.32 | 248, $103.57 |
| Tool reviews | ≈ $2.45 | 18, ≈ $6.09, $0.34 each | 15, ≈ $3.52, $0.23 each |
| Cache rebuilds | 3, ≈ $8.50 | 4, ≈ $6.50 | 4, ≈ $2.74 |
| Runs lost | — | $17.26 | $10.52 |
| A session's opening | — | ≈ $1.27 | ≈ $0.55 |

- A subagent's output, estimated at 5,400 tokens a call for every agent, was eight times
  too high for `skill-auditor`, about 640.
- A window between two commits, each call counted by its time, found the main sessions
  of Phases 4 and 5 that the counts by hand had, but for a few calls at the bounds. The
  `claude -p` sessions whose first record falls in the window were 218 and 248, the
  records' figures; the `.eval-runs/` results alone missed 43 and 8. Giving a shared
  message id to the transcript that starts first gave a continuation all 102 calls it
  shared with the conversation it continued.
- On 2026-10-12, 90 reviews since 2026-09-27: `session_resume.py` in 69, `roadmap` in
  64. The transcripts took 883 MB, about 29 MB a day over 30 days and 43 MB over the last
  seven.

## The Four Defects

Each fixed in Phase 2 of the roadmap, test first, the test red before the fix.

- **D1, `session_resume.py` counted at zero runs although it served.** 41 of the 55
  defect findings on `transcript.py` by 2026-10-12, grouped by their fix's wording.
  `session_start` takes the first timestamped record, while the SessionStart hook writes
  its records earlier: in `bbaa7e41`, two `queue-operation` records at 09:18:53 come
  first and the hook's `hook_success`, at 09:17:19, third, so the first slice leaves it
  out while the Stop hook, reading without bounds, puts the hook under review.
  - Fix: `session_start` returns the earliest timestamp of the transcript. A hook's run
    is also counted for each block and each error, so that its runs never fall below
    what it did (2 findings).
  - Test: a fixture transcript opening as `bbaa7e41` does: the first review's slice
    starts at the hook's time and its block counts one run of `session_resume.py` and
    its characters; a hook that blocks twice counts two runs and two blocks.
- **D2, a skill's files read through Bash not counted.** 12 findings. `count_skill_files`
  reads the Read tool's paths and the scripts Bash runs, nothing else.
  - Fix: a Bash command naming a file of a skill's folder, other than a script it runs,
    counts once as a read of that file, by its path in the skill, whether written in
    full or under `~/.claude` or `$HOME/.claude`; a folder or a glob is not counted.
  - Test: a fixture session whose Bash runs `cat` on `references/report.md`, `sed` on
    `SKILL.md` under `~/.claude`, and a script: `files_read` names the two files once
    each, and the script stays under `scripts`.
- **D3, the `make update` message.** `measure.py` and `record.py` answer "run make
  update D=review in it" when the domain does not know its repository: an instruction
  the agent must not follow without the user (Phase 3 of `skill-tooling`).
  - Fix: both scripts state the fact, the path the installer's state names or none, and
    that the user decides whether the domain is installed again; they name no command.
  - Test: a state naming a repository that does not exist, then none: both scripts exit
    1, their message names the path and the user, and holds no `make`.
- **D4, agent runs without their output.** `agent_runs` adds fresh and cached tokens
  only, and `make reviews` ranks agents by fresh tokens.
  - Fix: a run is counted by the shared reader: each call's output where its record
    holds the final usage, else estimated per agent type and marked; the last call's
    output from the Agent tool's result, `toolUseResult.usage`, matched by the run's
    `toolUseId`; the run carries its model, effort, output, estimated calls and cost.
    `make reviews` ranks an agent by its median cost in dollars.
  - Test: a fixture subagent whose records keep the stream's first usage, and a main
    transcript holding its Agent result: the run's output is the result's for its last
    call and the estimate for the others, marked estimated, and its cost is priced.

## What It Changes

- **Roadmap `token-usage` 1.3.0.** Phase 1 builds the reader, a probe of compactions
  first, 6 tasks; Phase 2 the reviews, the list of tools reviewed, the saturation, the
  archive, `reviewing-token-usage` and the four fixes, 11 tasks; Phase 3 recounts and
  releases the review domain as 0.3.0.
- **Roadmap `session-review` 1.0.2.** Its Phase 0 reads the boundaries and decides on one
  tool review with two catalogs.
- **`domains/review/hooks/tools.json`** keeps only the points to watch; the list of tools
  moves to the `[review]` table.

## When To Revisit

- **When a compaction is first recorded:** Phase 1's probe; the comparison of the three
  ways of going on starts with it.
- **When the median review passes $0.25 despite the saturation:** the Stop hook asks
  less often.
- **When roadmap `session-review` decides on one tool review:** the boundaries above
  follow.
- **When a published price is read for Claude Haiku 5.5:** it replaces the fitted one.
- **When this repository moves:** the reader finds a moved repository's earlier sessions,
  whose transcripts keep the old path.
