# Phase 0: Framing

---

## Status

**Current Status:** 🟡 In Progress (71% — 5/7)
**Started:** 2026-10-14
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, before any change to `authoring-skills`, which directions of the two feedback
notes the update takes, how a failure and an auditor point are classified, and the
criterion a skill's validation ends on, from measures of the instruments' spread on a
fixed version rather than from the notes alone.

---

## Overview

### Why This Phase Matters
The two notes propose twelve directions, D1 to D7 and E1 to E5, none decided. Their
figures rest on one grading per run and on auditor passes over changing text: no
measure yet says how often the grader or the auditor changes its answer on the same
output. A criterion chosen without that measure would be a second guess the next skill
works around.

### What It Enables
Phases 1 to 3 build a design the user approved, each change traced to the problem it
answers.

### Out of Scope
Changes to the skill, its scripts and its agents: they start in Phase 1.

---

## Design

Approved by the user on 2026-10-14, the runs and the next uses to tell whether its
reading holds (What Is Left Open). It rests on the report's map of
V1 to V6 and R1 to R6 to their lines, on its list of what the two skills carry, and on
its measures; paths are from `domains/skill-tooling/skills/authoring-skills/`, the
agents' from `domains/skill-tooling/agents/`.

### What The Measures Settle

- **The auditor's verdict is reproducible; its inputs are not held.** No verdict changed
  across 26 passes on a text and request held fixed, and every change on 2026-10-13 came
  with a change of the text, the request, or both. The request is free text the caller
  writes: on the same text, the bare request of `references/audit.md` failed six times
  in six and the 2026-10-13 request passed six times in six. What varies from pass to
  pass is the list of points, an open search. The agent runs at `medium`, an effort no
  file sets.
- **The grader is stable.** One verdict in 54 changed over four readings, on an
  assertion carrying a premise (V6). One grading per run, with the failed assertions
  graded a second time, is enough to tell a grader's error from an output's.
- **So the update fixes the instruments' inputs and judgments rather than adding
  passes**, and the criterion counts failures by their class rather than by their
  number.

### The Directions

| Direction | Decision | Changes | Phase |
|---|---|---|---|
| D1, a declared world | Kept, the hook run for real: see A Case's World | `evals.json`'s `hooks`, `run.py`, `workspace.py`, `references/evaluate.md`, `references/eval-files.md` | 1 |
| E1, the grader sees the world | Kept: each session's starting context rendered and kept whole | `scripts/harness.py` (`render`), `scripts/run.py`, `scripts/grade.py`, `skill-grader.md` | 1 |
| E2, several sessions | Changed: the fixture form alone, a sequence of sessions dropped | `references/evaluate.md` | 1 |
| E3, exact figures | Kept, the agents' output read as `usage.session` reads it | `scripts/harness.py`, `scripts/run.py`, `scripts/benchmark.py` | 1 |
| D2 and E5, a failure classified | Kept, with a sixth class for the tool: see A Failure's Class | `scripts/grade.py` (`--again`), `scripts/benchmark.py`, `references/evaluate.md`, `references/eval-files.md` | 2 |
| D3, a criterion in rates | Kept: see The Criterion | `scripts/benchmark.py`, `references/evaluate.md` | 2 |
| D4, no premise in an assertion | Kept, unchanged | `references/evaluate.md`, the skill's `evals/grade.py` | 2 |
| E4, kinds of assertion | Kept: guard, check, measure | `evals.json`'s `assertions`, `scripts/workspace.py`, `scripts/grade.py`, `scripts/benchmark.py`, `skill-grader.md` | 2 |
| D5, the auditor weighed by the evals | Kept, with a fixed request and effort: see The Auditor's Verdict | `references/audit.md`, `skill-auditor.md` | 2 |
| D6, sources apart | Kept, in `evals/sources.md`: see Sources | `references/writing-guide.md`, `skill-auditor.md` | 3 |
| D7 and R6, failures seen in use | Kept: see Failures Seen In Use | `evals.json`'s `failures_in_use`, `scripts/workspace.py`, `references/writing-guide.md`, `references/create-and-edit.md`, `skill-auditor.md` | 3 |

### A Case's World

- `evals.json` gains `hooks`, beside `agents`: the `hooks.json` of the skill's domain and
  the hook files it names. Each arm's runs get their version, installed in the run's
  folder as project hooks, `{{HOOKS_DIR}}` resolved to the copy; the arm without the
  skill gets none, as a repository without the domain. The harness keeps the project's
  hooks (`scripts/harness.py:9-11`); Phase 1 probes that a project SessionStart hook's
  output reaches a `claude -p` session before relying on it.
- A case turns a hook off through its fixture's configuration, as an installed
  repository would: for `close-session`, `start_notes = 0`.
- `references/evaluate.md`'s The Cases gains the check: each hook, setting or tool the
  skill relies on is provided by the case or turned off by it, never left to the
  harness's defaults.
- The grader reads what each session started with: `render` writes each `attachment`
  record of a session's start (instruction files, a hook's context) as a `## Context`
  entry naming its type, path and size, and the content whole under the run's
  `context/` and each agent's; `skill-grader.md` names `context/` for a claim about what
  a session had loaded.
- A workflow's later step is tested by a case whose fixture holds the state the earlier
  step leaves, built by `evals/fixtures.py`, from a recorded run's outputs when one
  exists; the earlier step's output has its own case. A sequence of sessions in one case
  waits until a hand-off fails in use while both cases pass.
- A run with agents gets its wall duration from `started` and `ended`; each agent's
  output where its Agent result records it, as `usage.session` reads a session's runs,
  and marked `settled` where it is shared by call count; the benchmark's footnote reads
  `output_source`; the effort note applies to the main session's calls, each agent's
  effort shown beside it.

### A Failure's Class

Each failed assertion of the skill's arm gets one class, with its evidence, before any
change; `grade.py --again <iteration>` grades the failed assertions alone in a new grader
session, one per run, and records the second reading beside the first.

| Class | When | What changes |
|---|---|---|
| `skill` | The output is wrong on what the assertion checks, and the skill's text leads there or leaves it open | The skill |
| `variance` | The output is wrong, the skill's text asks for the right thing plainly, and other runs of the version pass | Nothing; it counts against the criterion's rate |
| `grader` | The output is right: the second reading passes it, and the files bear it out | Nothing; the upheld reading stands |
| `assertion` | The assertion asks what the skill does not, carries a premise, or holds an item without substance | The assertion, then every run of the version graded again on it, both arms |
| `world` | The case's world is not one the installed skill meets | The case, then its runs again |
| `tool` | The validation itself misleads: a script, the grader's view, a figure, the auditor | Reported for the tool's repository; set aside from the criterion with its record |

The classes are written to the iteration's `classes.json`, each with the run, the
assertion, the class and its evidence; the benchmark reads the criterion only once every
failure has its class. Only `skill` sends a fix to the skill. For the other five,
`references/evaluate.md` says where the fix goes and that the skill stays as it is:
this is the step taken when an instrument is suspected.

### The Criterion

Read per assertion over the skill's arm, the runs of one snapshot pooled across
iterations, once every failure is classed and the `assertion`, `world`, `grader` and
`tool` failures are fixed or set aside:

- **a guard**, what must hold in every run (no stack command, no file left in `/tmp`):
  no failure classed `skill` or `variance`; never told to discriminate, never named weak;
- **a check**, the default: no failure classed `skill`, and a pass rate of 80% or more
  over five runs or more;
- **a measure**, an assertion over a list: each item graded and read as a check, the
  benchmark giving the count per configuration.

With three runs, one `variance` failure calls for two more on the same snapshot
(`workspace.py --extend`); one in five meets the criterion. Why 80% over five: the
grader changed one verdict in 54, and `close-session`'s Parquet failure came once in
fifteen graded runs; one such failure in five runs passes, two do not. A roadmap's proof
for a skill task cites this criterion, `audit.py` clean and the auditor's verdict below.

### The Auditor's Verdict

- **One request, held by files.** `references/audit.md` gives the request word for word:
  the skill's folder, the writing guide's path, the templates' folder and the static
  audit's output, nothing else. What the auditor must know beyond the skill's runtime
  files is in the skill's `evals/`: the copies it holds and their source, in
  `evals/sources.md` (Sources below).
- **One effort**: `skill-auditor.md` sets `effort: medium`, the effort every pass of
  2026-10-13 and of this phase ran at, 28 passes, 112 calls.
- **Two passes, started together**: the verdict is PASS when both pass. A FAIL whose
  lines are all answered never counts: the fixed text gets two new passes.
- **A point that changes behavior counts once the evals ran on its fix.** When they show
  a regression, the fix is reverted and the regression recorded under the case's
  `failures_with_skill`, quoting the point; `skill-auditor.md` does not raise a point the
  evals record as contradicted. One it raises anyway, or a point no judgment covers, or
  a line past the file's end, is a defect of the auditor, classed `tool` and fixed in
  the auditor with a fixture under `evals/auditor/`, never by rewording the skill.
- `skill-auditor.md` asks for each line number as a numbered read of that one file
  shows it.
- Phase 2's proof: the measure of this phase repeated on `65ca91f`, twelve passes or
  more on the fixed request, every verdict the same.

### Sources

- A skill's `evals/sources.md` holds the source of each fact its text states — a page, a
  dated probe, a file named with its repository —, and the copies the skill holds with
  their source. `evals/` is never installed nor loaded at runtime, and the audit's rule
  that every file is reached from `SKILL.md` already leaves it out: `audit.py` needs no
  rule changed.
- The runtime text keeps only what the agent opens while it works: a page to read, a
  file to run. A fact the agent observes in its own context, such as a line at its
  session's start, needs no source.
- `references/writing-guide.md`'s What Goes In and the auditor's content judgment
  follow: a fact without a source in the skill's text or in `evals/sources.md` fails, a
  citation in the runtime text that the agent never opens fails, and a declared copy is
  judged on whether the skill needs it, not on its content beyond the skill's use.

### Failures Seen In Use

- `evals.json` gains `failures_in_use`, at its top: each failure quoted, with its source,
  a transcript by its path and session, or a study by its file and section;
  `workspace.py` refuses an entry without its source.
- The writing guide's The Form Follows The Failure, `references/create-and-edit.md`'s
  Write The Minimum and the auditor's form judgment accept such a failure as they accept
  a run's: a prohibition answering one stands.
- A failure in use that a fixture can reproduce gets a case; one that cannot stays
  recorded, and the line it grounds is named under `pending` as not yet evaluated.
- A practice a study recommends, with no failure it answers, is no evidence: it stays
  out unless the user states it.

### What Is Left Open

- Out of scope as the README says: V7, trigger evals, the two skills' rework.
- To revisit after Phase 4's replay and the first two skills validated with the update:
  the 80% rate and the five runs; the `medium` effort, should Phase 2's fixtures show
  points missed; a sequence of sessions in one case.

---

## Tasks

### Inputs
- [x] Map each problem of the two notes, V1 to V6 and R1 to R6, to the file and line of `authoring-skills`, its scripts or its agents that causes it, reading ai-ctl's `review-skill` reports and runs only with the user's leave
  Proof: review — the map in the report, each problem with its file and line, read by the user
- [x] List the lines `close-session` and `reviewing-delivered-code` carry because of the validation, from both notes, as the cases Phase 4 replays
  Proof: review — the list in the report, each line with the problem it answers

### Measures
- [x] Measure `skill-auditor`'s spread: five passes or more on `close-session` at `65ca91f`, the same text each time; count the verdicts and each point by the number of passes that raised it, the cost announced first
  Proof: check — the counts in the report, with each pass's cost
- [x] Measure `skill-grader`'s spread: grade again, three times each, the two failed runs of `close-session`'s iterations 10 and 11 and a sample of their passed runs; count how often an assertion's verdict changes on the same output, the cost announced first
  Proof: check — the counts in the report, with the gradings' cost

### Design
- [x] Write the design in this file's `## Design`: each direction D1 to D7 and E1 to E5 kept, changed or dropped, with the file it changes and the phase that builds it; the classes of a failure and the step that classifies one; the step that sends a fix to the validation when an instrument is suspected; the pass criterion in rates; the auditor's verdict rule, the rule that a FAIL whose lines are answered never counts standing; where a skill's sources go; how a failure seen in real use enters the evals; get the user's approval
  Proof: review — the user's approval, recorded in the report
- [ ] Rewrite the application line of the agent's memory `skill-auditor-pass-required`, which tells the agent to answer an auditor point it disagrees with by a wording that satisfies the auditor, to the design's rule for a point the evals or the classification contradict
  Proof: review — the new line read by the user

### Record
- [ ] Write the decision record `docs/decisions/<date>-skill-validation.md`: the problems, the measures, the design's decisions and when to revisit them
  Proof: check — the record committed, `make check` passing

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-skill-validation.md    new
```

### Dependencies
Roadmap `skill-tooling`, completed: `authoring-skills` as installed at 0.1.2. The two
notes, in the ignored `notes/design-feedback/`:
`2026-10-14-close-session-validation.md` and
`2026-10-14-reviewing-delivered-code-validation.md`.

### Constraints
No change to `authoring-skills`, its scripts or its agents in this phase. Every session
the measures start is announced with its count and cost, and started on the user's yes.

---

## Acceptance Criteria

- [ ] The auditor's and the grader's spread are measured on fixed versions
- [ ] The design is approved by the user, each direction of both notes settled
- [ ] The decision record is committed
