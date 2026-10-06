# Phase 4: Evaluation Tooling

---

## Status

**Current Status:** 🟡 In Progress (0% — 0/12)
**Started:** 2026-10-06
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
fresh `claude -p` sessions; description tuning; and blind comparison, which Phase 0 kept
as an option for when the benchmark does not separate two versions.

---

## Overview

### Why This Phase Matters
A skill that triggers shows that Claude found it, not that it helps. The official
documentation asks for two separate measures against a baseline: whether Claude invokes
the skill when it should, and whether the output is what was intended. The roadmap
evals and Phase 3's runs have already shown several traps:
- an installed copy shadows the skill under test;
- a run that can read `evals/` sees the assertions, even when its prompt forbids the
  folder;
- an agent's verdict varies from run to run;
- runs take the session's effort, which makes them costly when it is `max`.

### What It Enables
Any skill, the new one included, can show that it beats its baseline. Phase 5 moves the
roadmap evals onto this tooling.

### Out of Scope
`claude plugin eval` and its format; `.skill` packaging.

---

## Tasks

### Design
- [ ] Write the design — `evals.json` with output, pressure and trigger cases, workspace layout, run prompts, grading and benchmark schemas, review — in the phase's `## Design`, citing a decision record where the section is not enough, and get the user's approval
  Proof: review — the design, each part tied to the Phase 0 matrix rows it carries and to this phase's constraints, approved before any script is written
- [ ] Measure what a nested `claude -p` session loads — hooks, skills, `CLAUDE.md`, and that no plugin is left — and how to keep it from biasing a trigger eval
  Proof: probe — one `claude -p` session started from a temporary directory as the trigger eval will start it, its transcript listing the hooks that ran, this setup's SessionStart line and the review domain's Stop hook among them, the skills listed and the files loaded; a second session, with what the design keeps out removed, as the control

### Output Evals
- [ ] Test and implement the count of a run's tokens and cost from its transcripts: one usage per message id, the price of each model, the effort recorded, and the output tokens estimated and marked as such where a subagent's transcript does not hold them
  Proof: test — transcript excerpts with known usages, a message id repeated and a subagent's stream-start records, red before the code; then Phase 3's sessions counted again and compared with `docs/decisions/2026-10-06-token-costs.md`, to the cent where `cost-state` holds the totals, before their transcripts are deleted 30 days after their last write
- [ ] Test and implement the workspace preparation, under the repository's `[skills] workspace` in a `skills/<skill-name>/` subfolder so that evaluated agents can share the folder later: a copy of the skill without `evals/`, a snapshot of the baseline version, one directory per case and configuration, `eval_metadata.json`
  Proof: test — a sample skill holding `evals/`: its copy lacks `evals/`, the snapshot matches the baseline version given, one directory per case and configuration, `eval_metadata.json` written, all under `skills/<skill-name>/` of the workspace
- [ ] Write the run procedure: with-skill and baseline subagents launched in the same turn, at an effort and a model the procedure sets rather than the session's, the Skill tool forbidden, and from each transcript the path the run read, the model and the effort it actually used; tokens, cost and duration saved for each run
  Proof: eval — one case run with and without the skill by a fresh agent, first without the procedure, then with it; expected before the runs: with it, both runs at the effort and model it sets, neither reaching `evals/` in its transcript, and each run's path, model, effort, tokens, cost and duration recorded
- [ ] Write the grader agent: it grades each assertion with evidence, flags an assertion that a wrong output would also pass, and writes `grading.json`
  Proof: eval — three outputs graded by a fresh agent without the grader's definition, then by the grader: one that passes, one that fails, one with an assertion a wrong output also passes; their grades written before the runs, each judgment run as many times as the design sets
- [ ] Test and implement the grading entry point: the skill's own `evals/grade.py` when it exists, the grader agent otherwise
  Proof: test — a skill with its own `evals/grade.py` graded by it, one without handed to the grader, and a `grade.py` that fails stopping the grading with its message
- [ ] Test and implement the benchmark: pass rate, time, tokens and cost per configuration, with mean, standard deviation and delta, and the model and effort of its runs
  Proof: test — grading files whose pass rates, times, tokens and costs were computed by hand: mean, standard deviation and delta per configuration, model and effort reported, and a run whose output tokens are unknown marked rather than counted as zero
- [ ] Measure the same output evals at `max` and at `xhigh`, pass rates and costs, and set from the result the effort the runs take, as `docs/decisions/2026-10-06-token-costs.md` asks
  Proof: probe — Phase 3's three skill-writing tasks run with the skill at `max` and at `xhigh`, same model and prompts, as many runs as the design sets, their count and estimated cost announced before they start; the pass rates and costs compared in the report set the effort
- [ ] Adapt the skill-creator review viewer, from its copy in `study/skill/create-skill/skills/skill-creator/eval-viewer/`, to the workspace layout, keeping its Apache 2.0 notice, and list it in `NOTICE`
  Proof: check — the adapted viewer's `--static` export on the sample skill's workspace writes a page holding each output, its grades and the benchmark, and `NOTICE` names the adapted files, their origin and their license

### Trigger Evals
- [ ] Test and implement the trigger eval: each query run several times in a fresh `claude -p` session, with the skill in a temporary directory passed with `--add-dir`, never in the project's `.claude/`
  Proof: test — a stub standing for `claude`: each query run the set number of times, the rate per query computed, the skill passed with `--add-dir` from a temporary directory, nothing written under the project's `.claude/`, and the count of sessions printed before the first starts
- [ ] Implement description tuning as Phase 0 decided: the session proposes each rewrite, a script measures it on training and held-out queries, and the best on held-out queries wins
  Proof: test — fixed trigger results standing for the runs: the split into training and held-out queries, each rewrite scored on both, and the best on held-out queries chosen even when another wins on training
- [ ] Implement blind comparison between two versions of a skill, the option Phase 0 kept for when the benchmark does not separate them
  Proof: eval — two versions of a skill whose better one is known, their outputs compared with the labels hidden, by a fresh agent without the comparator's definition, then by the comparator; expected before the runs: the comparator names the better one and says why

### Reference
- [ ] Write the evaluation reference: when to evaluate, how many cases, which baseline, how to read the benchmark and the trigger rates, and which checks stay assertions and which go to a person's review (row S17, left from Phase 3)
  Proof: eval — a fresh agent asked to evaluate a sample skill, without the reference, then with it; expected before the runs: with it, the cases and the baseline chosen, the count and cost of runs announced, the effort and model set, the benchmark and trigger rates read, and S17's assertions and reviews kept apart

---

## Technical Details

### Files to Modify
```
domains/skill-tooling/skills/authoring-skills/SKILL.md                   the fourth operation, evaluate
domains/skill-tooling/skills/authoring-skills/scripts/*.py               new
domains/skill-tooling/skills/authoring-skills/assets/viewer/             new, adapted from skill-creator
domains/skill-tooling/skills/authoring-skills/references/evaluate.md     new
domains/skill-tooling/agents/skill-grader.md                             new
domains/skill-tooling/agents/skill-comparator.md                         new
domains/skill-tooling/tests/test_*.py                                    new
NOTICE                                                                   new
```

### Dependencies
Phase 3: the skill. Phase 0: the decisions on description tuning and blind comparison.
The Agent Skills standard's guides on evaluating skills and optimizing descriptions
describe the same loop as skill-creator, for any agent; `docs/conventions/agent-skills.md`
lists them and where this setup departs from them, a cost counted from `total_tokens`
and a workspace beside the skill among them. `docs/decisions/2026-10-06-token-costs.md`
gives Phase 3's costs, the method that counted them and the effort its runs took.

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
starts, and the script announces it, with its estimated cost, before starting them.
Phase 3's 23 full-task runs cost about $57.50, $2.50 each, and its 45 runs of
`skill-auditor` about $20, $0.45 each: 77 of the phase's 167 dollars
(`docs/decisions/2026-10-06-token-costs.md`). A run's cost is counted from its
transcript, fresh input and cache reads, one usage per message id, never from the
`total_tokens` of the Agent tool's result, which is the size of the last context and
which skill-creator records as the cost. A subagent's transcript does not hold its final
output tokens: most of its records keep the usage written when the message started
streaming (seen on 2026-10-05, 221 recorded for about 2,500 tokens of visible text; on
2026-10-06, 88,681 recorded for 804,047). A main session's transcript holds them. The
`cost-state` record Claude Code writes into a session's file when the session is resumed
or ends holds each model's totals, subagents included, but no run's. So the design
takes a run's output from a source that holds it, or estimates it and says so, as the
record does. A run takes the effort of the session that starts it: in Phase 3, 2,586 of
the runs' 2,621 calls in sessions at `max` ran at `max`, and thinking made 84% of their
output. A benchmark whose effort is left to the session compares runs made under
different conditions and pays for the highest setting: the run procedure sets the
effort, as it sets the model. One reader counts tokens and cost for the runs and for the
review domain, as roadmap `token-usage` decided at its opening on 2026-10-06. This phase
writes it for the runs, and `token-usage` extends it to the reviews: the design places
it where the review domain can take it, as `shared/` holds code several tools use. A run working in this repository reaches
the skill's own evals with one `grep`, as two of Phase 3's Verification runs did
despite a prompt that forbade the skill's folder: the run procedure keeps the evals out
of the run's reach rather than out of its instructions. An agent's judgment varies from
run to run: on a file left unchanged between them, `authoring-skills`' copy of the
shared conventions reference, three runs of `skill-auditor` reported one problem, then
three, then four, two of them new and one of the earlier ones missing (seen on
2026-10-06), so the design says how many runs a judgment takes before its verdict
counts.

---

## Acceptance Criteria

- [ ] One full iteration runs end to end on a sample skill: workspace, runs, grading, benchmark, review
- [ ] A trigger eval reports a rate per query and writes nothing into the project's `.claude/`
- [ ] Every evaluation capability marked keep or improve in the Phase 0 matrix is implemented
- [ ] Every script is covered by unit tests that pass under `make check`

---

## Risk & Mitigation

- A nested `claude -p` session loads the user's hooks, skills and `CLAUDE.md`, which can
  bias triggering. Among them is this setup's own SessionStart line. The review domain's
  Stop hook can also ask each session for a tool review. No plugin is left since
  2026-10-04 (`docs/decisions/2026-10-04-plugins-removed.md`). The second design task
  measures what loads before the trigger eval is written.
- A subagent can run on another model than the one requested, as two reviewers did on
  2026-09-27: the run procedure reads the model from each transcript, and the benchmark
  reports it.
- Trigger evals are costly — twenty queries run three times make sixty sessions per
  description — so the scripts print the count before starting and accept a smaller
  sample.
