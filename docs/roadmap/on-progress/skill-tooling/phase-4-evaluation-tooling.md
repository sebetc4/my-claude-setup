# Phase 4: Evaluation Tooling

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/12)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-3-writing-method.md` and `phase-3-writing-method-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-4-evaluation-tooling-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Give the skill the evaluation loop of skill-creator, improved: output evals with and
without the skill in subagents, grading, benchmark and human review; trigger evals in
fresh `claude -p` sessions; description tuning; and blind comparison if Phase 0 keeps it.

---

## Overview

### Why This Phase Matters
A skill that triggers shows that Claude found it, not that it helps. The official
documentation asks for two separate measures against a baseline: whether Claude invokes
the skill when it should, and whether the output is what was intended. The roadmap evals
have already shown two traps: an installed copy shadows the skill under test, and a run
that can read `evals/` sees the assertions.

### What It Enables
Any skill, the new one included, can show that it beats its baseline. Phase 5 moves the
roadmap evals onto this tooling.

### Out of Scope
`claude plugin eval` and its format; `.skill` packaging.

---

## Tasks

### Design
- [ ] Write the design — `evals.json` with output, pressure and trigger cases, workspace layout, run prompts, grading and benchmark schemas, review — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval
- [ ] Measure what a nested `claude -p` session loads — plugins, hooks, skills, `CLAUDE.md` — and how to keep it from biasing a trigger eval

### Output Evals
- [ ] Test and implement the workspace preparation, under the repository's `[skills] workspace` in a `skills/<skill-name>/` subfolder so that evaluated agents can share the folder later: a copy of the skill without `evals/`, a snapshot of the baseline version, one directory per case and configuration, `eval_metadata.json`
- [ ] Write the run procedure: with-skill and baseline subagents launched in the same turn, the Skill tool forbidden, and from each transcript the path the run read and the model it actually used; tokens and duration saved from each notification
- [ ] Write the grader agent: it grades each assertion with evidence, flags an assertion that a wrong output would also pass, and writes `grading.json`
- [ ] Test and implement the grading entry point: the skill's own `evals/grade.py` when it exists, the grader agent otherwise
- [ ] Test and implement the benchmark: pass rate, time and tokens per configuration, with mean, standard deviation and delta
- [ ] Adapt the skill-creator review viewer to the workspace layout, keeping its Apache 2.0 notice, and list it in `NOTICE`

### Trigger Evals
- [ ] Test and implement the trigger eval: each query run several times in a fresh `claude -p` session, with the skill in a temporary directory passed with `--add-dir`, never in the project's `.claude/`
- [ ] Implement description tuning as Phase 0 decided: the session proposes each rewrite, a script measures it on training and held-out queries, and the best on held-out queries wins
- [ ] Implement blind comparison between two versions of a skill, the option Phase 0 kept for when the benchmark does not separate them

### Reference
- [ ] Write the evaluation reference: when to evaluate, how many cases, which baseline, how to read the benchmark and the trigger rates, and which checks stay assertions and which go to a person's review (row S17, left from Phase 3)

---

## Technical Details

### Files to Modify
```
domains/<domain>/skills/<skill>/scripts/*.py               new
domains/<domain>/skills/<skill>/assets/viewer/             new, adapted from skill-creator
domains/<domain>/skills/<skill>/references/evaluate.md     new
domains/<domain>/agents/<grader>.md                        new
domains/<domain>/tests/test_*.py                           new
NOTICE                                                     new
```

### Dependencies
Phase 3: the skill. Phase 0: the decisions on description tuning and blind comparison.
The Agent Skills standard's guides on evaluating skills and optimizing descriptions
describe the same loop as skill-creator, for any agent; `docs/conventions/agent-skills.md`
lists them and where this setup departs from them, a cost counted from `total_tokens`
and a workspace beside the skill among them.

### Constraints
Standard library only. Output evals run in subagents; only trigger evals start
`claude -p` sessions, and a script says how many it will start before it starts them.
In a subagent, Claude Code's Write tool refuses any file whose name matches
`^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$`, case-insensitive (seen in 2.1.286): a skill
that produces such a file, as the roadmap closure produces `summary.md`, makes its run
agents fall back on a Bash heredoc. The design says whether those runs move to
`claude -p` or their prompt warns of it. In a headless run, an Edit under `.claude/`
waits for a permission even with `--permission-mode acceptEdits` (seen in 2.1.283): a
scenario's skill sits elsewhere, as Phase 2's hook probe put it under `skills/`, or the
run grants that permission. The repository's tests assume a temporary folder outside any
repository that holds `.agent-conventions.toml`: with `TMPDIR` inside this repository,
five of them fail, two of the audit's and three of the conventions reader's (seen on
2026-10-05), so the tooling leaves `TMPDIR` alone or makes those tests independent of
it first. A realistic skill-writing run, in Phase 3's baseline on Sonnet, took 48 to 107
API calls and 22 to 45 minutes, read 7.6 to 26.1 million tokens from cache, and ended on
a context of 250,000 to 410,000 tokens: the design says how many runs a benchmark
starts, and the script announces it before starting them. A run's cost is counted from
its transcript, fresh input and cache reads, one usage per message id, never from the
`total_tokens` of the Agent tool's result, which is the size of the last context and
which skill-creator records as the cost. The transcript's output tokens are not final:
most assistant records keep the usage written when the message started streaming (seen
on 2026-10-05, 221 recorded for about 2,500 tokens of visible text), so the design finds
the output elsewhere or reports it as unknown. A run working in this repository reaches
the skill's own evals with one `grep`, as two of Phase 3's Verification runs did
despite a prompt that forbade the skill's folder: the run procedure keeps the evals out
of the run's reach rather than out of its instructions.

---

## Acceptance Criteria

- [ ] One full iteration runs end to end on a sample skill: workspace, runs, grading, benchmark, review
- [ ] A trigger eval reports a rate per query and writes nothing into the project's `.claude/`
- [ ] Every evaluation capability marked keep or improve in the Phase 0 matrix is implemented
- [ ] Every script is covered by unit tests that pass under `make check`

---

## Risk & Mitigation

- A nested `claude -p` session loads the user's plugins and hooks — the superpowers
  SessionStart injection among them — which can bias triggering: the second design task
  measures it before the trigger eval is written.
- A subagent can run on another model than the one requested, as two reviewers did on
  2026-09-27: the run procedure reads the model from each transcript, and the benchmark
  reports it.
- Trigger evals are costly — twenty queries run three times make sixty sessions per
  description — so the scripts print the count before starting and accept a smaller
  sample.
