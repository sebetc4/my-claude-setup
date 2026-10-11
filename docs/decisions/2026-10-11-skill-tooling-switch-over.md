# Skill Tooling Switch-Over — 2026-10-11

Decision, taken by the user on 2026-10-11: **`authoring-skills`, with its agents
`skill-auditor`, `skill-grader` and `skill-comparator`, is this setup's one tool for
skills. It is installed, and the roadmap evals run on its scripts. Neither
`writing-skills` nor skill-creator comes back. The skill stays as it is until real use
shows one of the three points to watch below.**

Recorded by Phase 5 of roadmap `skill-tooling`, from the runs, measures and audits of
its report, `docs/roadmap/completed/skill-tooling/phase-5-switch-over-report.md`.

## What It Replaces

`2026-09-18-superpowers-plugin-audit.md` decided two things about the old tools:
- leave `writing-skills` out of any vendoring;
- keep the skill-creator plugin enabled, because the roadmap evals ran its benchmark
  script and its review viewer.

`2026-09-28-skill-tooling.md` chose the replacement and turned both sources off.
`2026-10-04-plugins-removed.md` uninstalled every plugin, and kept the sources under
`study/` for the roadmaps. This record closes the matter. The new tool did the old
tools' work at least as well in the comparison below. Nothing in this repository
depends on the copies under `study/skill/` any more:
`grep -rn "study/skill/create-skill" domains tests tools` finds nothing.

## The Benchmark

The three skill-writing cases of `authoring-skills`'s evals:
- `task-release-domain`;
- `reference-claude-code-hooks`;
- `discipline-real-claude-dir`.

Four arms ran them in three iterations under `.eval-runs/skills/authoring-skills/`:
- iteration 5: no skill, and `authoring-skills`;
- iteration 6: `writing-skills` 6.4.1;
- iteration 7: skill-creator `fa59bc903774`.

Each arm had three runs per case, on Sonnet 5.5 at `xhigh`, from 2026-10-09 to
2026-10-10. Each pass rate is the mean of the runs' rates, as `benchmark.py` gives it.

| Case | No skill | `writing-skills` | skill-creator | `authoring-skills` |
|---|---|---|---|---|
| task-release-domain | 43% | 52% | 43% | 76% |
| reference-claude-code-hooks | 78% | 67% | 72% | 89% |
| discipline-real-claude-dir | 39% | 61% | 33% | 94% |
| All | 53% ± 20% | 60% ± 9% | 49% ± 20% | 87% ± 16% |
| Cost a run | $1.73 | $1.51 | $1.96 | $1.39 |
| Duration a run | 545 s | 446 s | 536 s | 433 s |

**Without the audit assertions.** Each case closes on "the audit reports no error".
That needs `audit.py`, which only the `authoring-skills` arm holds, so the three other
arms fail it in all 27 of their runs. Without those three assertions, the pooled counts
are:
- no skill: 30/48, 63%;
- `writing-skills`: 34/48, 71%;
- skill-creator: 28/48, 58%;
- `authoring-skills`: 40/48, 83%.

By case, `authoring-skills` keeps the lead on two of the three:
- task-release-domain: 72%, against 50% to 61%;
- discipline-real-claude-dir: 93%, against 40% to 73%.

On reference-claude-code-hooks it reads 87%. That ties skill-creator, beats
`writing-skills`'s 80%, and sits one assertion under the no-skill arm's 93% over three
runs.

**What it does not measure.** Every arm ran under the same limits: no Agent tool and no
`claude -p` session. So two things went unmeasured: skill-creator's test loop and its
description optimization, and `writing-skills`'s pressure tests with subagents.
`authoring-skills` has these loops as `run.py`, `grade.py`, `triggers.py` and
`tuning.py`, which the comparison did not run either.

**What each old tool brought.** `writing-skills` wrote the prohibition with its
condition in all three discipline runs. skill-creator wrote a total ban in all three.
Neither wrote pressure scenarios before the rules.

**Failures of `authoring-skills`.** It failed eight assertions in its arm, and each one
is a rule the skill states and the run had read. The skill was left unchanged. The three
that recur are the points to watch below.

**Cost.** The 36 runs cost $59.23 and their gradings $9.14. A further $9.55 went to
runs lost without a result: one when the editor's window was closed, six to the
subscription's session limit.

## Trigger Rates

`authoring-skills`'s `evals.json` holds 24 queries, half of them in French:
- 12 that should trigger: what `writing-skills` and skill-creator answered — creating,
  editing, checking, evaluating, benchmarking or comparing a skill, tuning its
  description, turning a session's work into one;
- 12 near misses, each with what it nearly matches.

Measured by `triggers.py` on 2026-10-10: three sessions per query, Opus 5.5 at `xhigh`,
Claude Code 2.1.292.

| Description | Should trigger | Near misses | Cost |
|---|---|---|---|
| current, with "evaluates" | 12/12, each 3 of 3, at the first call | 0 of 12 triggered | $8.35 |
| `b3fa90e`, before "evaluates" | 12/12, each 3 of 3, at the first call | 0 of 12 triggered | $8.37 |

No query failed, so the description was not tuned. The current one stays because it
states what the skill does.

The set cannot tell the two descriptions apart. Every query that should trigger names a
skill, and this is the only skill given that writes skills. A set that could tell them
apart would hold a request about evaluation that names no skill, with other skills that
could answer it in the same listing.

## The Capability Matrix

The Phase 0 matrix in `2026-09-28-skill-tooling.md` has 68 rows. Each was checked
against what was built, on 2026-10-09:

| Verdict | Rows |
|---|---|
| Built as ruled | 51 |
| Dropped as ruled | 10 |
| Built otherwise | 6 — W5, W22 and S17, confirmed by the user on 2026-10-09; S10, S22 and S30, as Phase 2 and Phase 4 designed them |
| Missing | 1 — W18 |

W18 is a table of the excuses for skipping the evaluation. The user dropped it on
2026-10-09 until a run shows a session skipping the evaluation. For S34,
`references/eval-files.md` gained a `## Contents` section.

## The Existing Skills

`audit.py` passes on `roadmap`, `tool-review` and `authoring-skills`, with no error and
no warning. On 2026-10-10, `skill-auditor` ran three times on each of the three skills.
The user ruled:

- **Not kept:** a problem raised by only one run of three.
- **`roadmap`:**
  - R1, the "Not for …" exclusion of the description, stays until a trigger measure
    shows what removing it does.
  - R8 is not a problem.
  - The rest was fixed in 2.0.2.
- **`tool-review`:**
  - T1 and T4 stay as the behavior chosen in 0.1.2, with no evals written now.
  - T2 and T3 were fixed in review 0.2.1.
- **`authoring-skills`:**
  - A1 and A2 were fixed.
  - A4 stays as the opening decision on `checks`.

On 2026-10-11, a tenth run on `tool-review` raised no problem that these rulings leave
open.

## Roadmap Evals On The New Tooling

`domains/roadmap/skills/roadmap/evals/grade.py` now runs on `authoring-skills`'s
scripts. To prove the move, the six runs of 2026-10-01 were graded again. The results
were the same run by run: 10/10, 10/10, 9/9, 9/9, 3/3 and 2/3. That gives `with_skill`
100% and `old_skill` 89% ± 19%, the figures skill-creator's benchmark gave.

Roadmap 2.0.2 holds the `skill-auditor` fixes. It was proven against 2.0.1 on
2026-10-11, in `.eval-runs/skills/roadmap/iteration-3`:
- four cases, one of them new and run under `versioning = "none"`;
- three runs of each version per case, 24 runs, $7.96;
- 94% ± 19% for 2.0.2, against 100% for 2.0.1.

The one gap is a single run of the create case. That run followed `run.py`'s preamble,
which says to assume rather than ask, and wrote `versioning = "git"` where the skill
says to stop. Both versions state that rule word for word.

## The Install

Installed on 2026-10-11:
- skill-tooling 0.1.0;
- review 0.2.1;
- roadmap 2.0.2.

The repository's own registration of `audit_skill.py` was removed, so one edit gives
one audit report.

`domains/review/hooks/tools.json` lists:
- `authoring-skills`;
- `skill-auditor`;
- `skill-tooling/audit_skill.py`.

The Stop hook's review request named the skill and the agent in a session that used
them, and neither in a session that did not.

From this install on, `make reviews` judges each tool on the repository's version.

## Points To Watch In Real Use

A tool review sees friction, such as a correction, an error or a missed trigger. It
sees less of a fault that slips silently into a skill the session writes. So
`tools.json` gives `authoring-skills` three points, and every review of a session that
used the skill must check them.

| Point | In the benchmark | Revisit when |
|---|---|---|
| A skill it wrote explains a convention the model already knows, such as semantic versioning or git usage | failed in 2 runs of 3, and as often or more by every other arm | two reviews raise it: change What Goes In in the writing guide, proven on task-release-domain, where 3 runs of 3 must not explain the convention |
| A step of a skill it wrote that can fail has no check | failed in 2 runs of 3; the no-skill arm passed 3 of 3 on an assertion that reads two ways | two reviews raise it: split assertion 4 of task-release-domain first, then change the task template or Degrees Of Freedom, proven on the split assertion in 3 runs of 3 |
| A skill it wrote to enforce a rule came before a mechanical guard was weighed | failed in 1 run of 3 | one review raises it, since such a skill guards a step that is hard to undo: change step 3 of `create-and-edit.md` or `discipline.md`, proven on discipline-real-claude-dir's first assertion in 3 runs of 3 |

When no review raises any of the three over ten reviews of sessions in which
`authoring-skills` wrote a skill, the three points leave `tools.json`.

## Left Open

These are recorded under Problems And Deviations in the Phase 5 report:
- `run.py` estimates a run's cost from the mean over all of the skill's cases.
- `run.py` does not refuse a second `--start` on an iteration already running.
- The guard refuses Python heredocs that name `~/.claude`, and trial installs into
  `mktemp -d`.
- `triggers.py`'s budget ceiling can be passed by half.
- `grade.py` announces grader sessions that the skill's own script makes needless.
- The fourth case of `authoring-skills` cannot run while runs are denied the Agent tool.

## When To Revisit

- **A point to watch:** at the condition its row gives.
- **Assertion 4 of task-release-domain:** split it at the next run of `authoring-skills`'s
  evals.
- **R1, `roadmap`'s exclusion:** at the first trigger measure of `roadmap`.
- **A run needing subagents:** when the runs may use the Agent tool. Then run the fourth
  case and measure the test loops the comparison left out.
- **Another repository adopting the tool:** when one adopts the `[skills]` table,
  scriptorium first. Read its first reviews of `authoring-skills` and `audit_skill.py`
  before calling the switch-over done there.
