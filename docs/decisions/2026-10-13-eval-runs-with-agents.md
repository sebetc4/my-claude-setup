# Eval Runs With Agents — 2026-10-13

Decided with the user on 2026-10-13, from a proposal written by ai-ctl (roadmap
`review-skill`, Phase 0), whose skill `reviewing-delivered-code` runs one agent per review
axis: **a skill's evals may list the agents the skill starts; their runs then get each
arm's version of those agents and the Agent tool, in both arms, and a run's record counts
and renders what its agents did.** It settles the point left open by the Phase 4 report
of roadmap `skill-tooling` and by `docs/decisions/2026-10-11-skill-tooling-switch-over.md`
(Left Open, When To Revisit: "A run needing subagents").

## Decisions

- **A skill-level `agents` key in `evals/evals.json`**, the agents' files as paths from
  the repository's root. The agents belong to the version compared: a case that needs
  none simply does not start them.
- **The Agent tool in both arms, for a skill with agents only.** The baseline measures
  what an agent does without the skill with the same tools; denying Agent in the
  baseline alone would credit the skill with what the tool does. A skill without agents
  keeps `--disallowed-tools Skill Agent`, and its digests, so that its earlier iterations
  and `--reuse` stay valid. Skill stays denied in every run: an installed copy must not
  answer for the copy under test (Phase 4, unchanged).
- **Each arm's version.** `workspace.py` snapshots the agents per arm, as it does the
  skill: `with_skill` the current files, `old_skill` the baseline revision's, an agent it
  lacks left out, `without_skill` none; it leaves them out of `base.tar`. A folder
  baseline is refused for a skill with agents, since nothing says which version of them
  goes with it.
- **The digests.** The agents enter each case's digest, and the baseline's agents its
  snapshot digest, so that `--reuse` never takes a baseline run made with Agent denied
  for an iteration where it is allowed.
- **Where a run finds them.** In `work/.claude/agents/`, copied as they are, and in a
  `repository` case also back at their paths. Probe 1 showed `--agents` works too; the
  folder needs no translation of the frontmatter into JSON.
- **The record of a run.** `<session>/subagents/` is copied into the run's folder, each
  agent's run rendered as `agents/<type>-<id>.md` and listed at the head of
  `transcript.md`; the grader gets `agents/` and reads what its assertions need. The
  figures count the agents' calls, and `run.json` gives them by agent type; the paths a
  run named include its agents', so that `repository_paths` shows an agent's leak.
- **The output their transcripts lack**, most of an agent's, comes from the json
  result's `modelUsage`, each model's output, the agents' included, shared among the
  estimated calls by their estimates (`usage.settle()`): the total is exact, its split
  between agents estimated. The cost stays counted at `usage.toml`'s prices, as every
  other figure of this repository; `reported_cost_usd` stays beside it. Without
  `modelUsage`, the estimates stand, and `output_source` says which.
- **The estimate before any run** of a skill with agents is the run's ceiling, which the
  agents' spend counts toward.
- **Not done:** no `--append-subagent-system-prompt`: an agent has no user to ask, and a
  nested `claude` is refused by `CLAUDECODE` in the session's environment; no default for
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, Claude Code's being what a skill meets in real
  use, the ceiling bounding the cost, and the evals' `env` able to set it.
- **The proposal's S2** (a case run as one agent, to evaluate a brief alone) stays a
  complement for later; S3 and S4 are set aside.

## The Probes

Five `claude -p` sessions on Claude Code 2.1.292, at the harness's flags (`--setting-sources
project,local`, `--strict-mcp-config`, the guard through `--settings`), on
`claude-sonnet-5-5`, each in a git folder outside any repository; $0.28 in all.

| Probe | Setting | Result |
|---|---|---|
| 1a | `work/.claude/agents/probe-echo.md`, `effort: low`, session at `--effort high` | Offered beside the built-in agents (`claude`, `Explore`, `general-purpose`, `Plan`, `statusline-setup`), none of the user's; started, its secret word returned; its call at `low`, the main thread's at `high` |
| 1b | The same agent in an `--agents` file | The same |
| 2 | `--disallowed-tools Skill`, a project skill in `work/.claude/skills/`, a `general-purpose` agent asked to call it | The agent's tools hold no Skill |
| 2c | Control: no tool denied | The agent has Skill and reads the skill's secret |
| 3 | The agent asked to Read the real repository's `CLAUDE.md`, a path it builds itself | The guard refuses the Read, and the agent's report naming the path; both refusals in the result's `permission_denials` |
| 4 | Folded into 1a and 1b | The agent's frontmatter effort applies under `--effort`; a `general-purpose` agent takes the session's (probes 2, 3, 5) |
| 5 | Two `general-purpose` agents in parallel | See below |

In all five sessions, the input, cache-read and cache-write tokens of the transcripts
equal `modelUsage`'s, and so does the output where no call is estimated (1a, 1b, 5). In
2 and 2c, the estimate for an agent type `usage.toml` lacks, 5,400 tokens a call, put
the output at 6,741 and 12,009 tokens where `modelUsage` gives 1,745 and 1,970, and the
count at $0.111 and $0.188 where Claude Code reports $0.058 and $0.083.

Claude Code's `total_cost_usd` differs from `usage.toml`'s pricing by one rate: fitted
on the five sessions, it prices Claude Sonnet 5.5's cache reads at $0.10 a million,
where `usage.toml` gives $0.20, 0.1 times the input; input, output and both cache
writes match (for probe 5: 10 × $2 + 2,895 × $10 + 33,353 × $0.10 + 16,164 × $2.50 +
5,934 × $4 = $0.0964513, the reported figure to the last digit). Which of the two is
right is left to roadmap `token-usage`, which owns the table.

## When To Revisit

- **The first runs of ai-ctl's `reviewing-delivered-code`:** the share of the agents in a
  run's cost, whether the grader reads `agents/` affordably, and whether the ceiling
  makes a sane announcement before any run is measured.
- **A skill whose cases need different agents:** then a case-level key.
- **The fourth case of `authoring-skills`,** which starts `skill-auditor`: its evals can
  now list it; the case still waits for a prompt that names no folder of Phase 3's
  workspace.
- **Claude Code changing** how it finds a project's agents, or `--disallowed-tools` or a
  settings hook no longer reaching subagents: probes 1 to 3 again.
