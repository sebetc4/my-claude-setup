# Phase 5 Report: Switch-Over

**Phase:** [phase-5-switch-over.md](phase-5-switch-over.md)
**Start Commit:** 5b2065e

---

## Work Log

### 2026-10-09

Opened the phase from Phase 4's closure, committed as `5b2065e`. Read Phase 4's file and
its report, finalized in this session: no restructuring pending, and no other phase in
progress. What binds this phase:
- the evaluation tooling Phase 4 built: runs are `claude -p` sessions, Sonnet 5.5 at
  `xhigh`, one at a time near the subscription's limit, each paid step at the user's yes;
  a skill-writing task costs about $1.30 a run and $0.25 a grading;
- when a run fails an assertion, the assertion is read before the skill;
- `authoring-skills` has no trigger queries yet, and its description gained "evaluates"
  in Phase 4 without them: the trigger task writes them and measures both texts;
- the fourth case of `authoring-skills` cannot run while runs are denied the Agent
  tool, so the comparison runs the three skill-writing cases;
- the roadmap evals still run skill-creator's scripts from `study/`;
- `CLAUDE.md`'s layout already names the evaluate operation, so the `CLAUDE.md` task is
  left with the gotchas.

Two dependencies of the first task are not settled. Put them to the user before any work:
- **Four configurations.** `workspace.py` prepares two per iteration, `with_skill` and
  one baseline, and `--reuse` takes only the baseline's runs. A baseline from a folder is
  copied under the name of the skill under test, and its run is told "Use the skill
  `authoring-skills`". Comparing no skill, `writing-skills` 6.4.1, skill-creator and
  `authoring-skills` takes three iterations whose `with_skill` runs are paid three times,
  or a change to `workspace.py` first.
- **skill-creator in a run.** Its loop starts subagents and `claude -p` sessions. A run
  is denied the Agent tool, and its preamble forbids starting `claude`. So skill-creator
  would run without the part that makes it skill-creator, unless the comparison says
  how its arm is scored.

The cost to announce: three tasks × four configurations × three runs is 36 runs, about
$47 at `xhigh`, with about $9 of gradings. At the user's rule, the opening ends the turn:
no work on the phase yet.

In a new session, at the user's request, measured what Phase 4 cost, the user having kept
its sessions short to manage the context. The sources were the transcripts of its
sixteen main sessions and of the 218 `claude -p` sessions they started, counted with
`shared/usage/usage.py` and one-off scripts. Recorded in
`docs/decisions/2026-10-09-phase-4-token-costs.md`; the 2026-10-06 record points to it.
- About $187 in all, about $176 without the session that measured Phase 3: as much as
  Phase 3's $176.38.
- The main thread, $115.47 at `xhigh`, read 37% less cache a call, a mean context of
  about 190,000 tokens against 299,000. It made 62% more calls for the phase's work, and
  each opening cost $1.27 to $2.12. The roadmap documents read cost about $13.25; the
  report alone, about 50,000 tokens at the end, about $5.92.
- One subagent ran, $0.63. The `claude -p` sessions cost $69.32, $56.35 of it for task
  9, of which $17.26 went to runs the subscription's limit stopped.
- 18 tool reviews cost about $6.09, and four cache rebuilds after a change of
  organization at the limit about $6.50.

At the user's request, the roadmaps were then made to know both records and what they
raise:
- this phase's constraints give Phase 4's run costs and fixed costs, before its 36 runs;
- `roadmap-execution`, 1.1.0, and `token-usage`, 1.0.1, as listed under Changes To Later
  Phases;
- this roadmap's README links both records.

In a third session, put the two dependencies to the user. Reading `workspace.py` again
first showed the opening wrong on the first: `--baseline-only` prepares the baseline arm
alone, as iteration 3 of Phase 4 did, so three iterations pay each configuration once,
36 runs in all, with no change to `workspace.py`. What it costs instead: no benchmark
holds the four configurations, so the table comparing them is assembled from the three
`benchmark.json`. Iterations 1 and 2 cannot give the `with_skill` runs: the skill has
changed since, in `18a1c65`. The user chose the three iterations and the same limits for
every arm, and gives each `--start` its own go-ahead.

Prepared A as `iteration-5`. `run.py` announced 18 runs at $12.71, $0.71 a run: the mean
of the skill's 23 complete runs, the cheaper evaluation cases included, where Phase 4
measured about $1.30 on the skill-writing cases; announced to the user as about $23.
Started at the user's go-ahead on 2026-10-09 at 08:30 UTC, one run at a time, its log in
`.eval-runs/skills/authoring-skills/runs-2026-10-09.log`.

Reading `run.py` before B and C: in a `repository` case, it puts the baseline arm's copy
back at the skill's path, `domains/skill-tooling/skills/authoring-skills/`. Right for an
earlier version of the same skill, wrong for another tool: each run of B and C would
have found `writing-skills` or skill-creator in the repository as the domain's skill,
under a `CLAUDE.md` that describes another. At the user's choice, fixed test-first while
A ran: `workspace.py` records `in_repository`, false for a folder whose `SKILL.md` names
another skill, and `run.py` then gives that arm its copy only. Two tests in
`test_run.py`, watched failing; `make check` passes. Prepared B as `iteration-6` and C as
`iteration-7`, each recording `in_repository: false`.

While A ran, the task on `tests/check.py`: it found skills under `domains/*/skills` only.
It now reads `dirs` from the `[skills]` table through `shared/conventions/conventions.py`,
the source, loading the file at the root it is given rather than searching upwards; when
the file is missing or the table cannot be read, it checks `domains/*/skills` and says so
in a warning, since the file is ignored by git and a fresh clone has none. `main` and
`options` take the root, so that the proof's fixture repository runs through them. Two
tests in `tests/test_check_skills.py`: the fixture's `.claude/skills/broken`, whose name
differs from its folder, reported `[N3]`, red first for want of the parameter, then, once
it existed, red because the skill was not found; then green. `make check` passes, three
skills checked, as before: this repository has no `.claude/skills` yet. `CLAUDE.md`'s
line on `tests/check.py` says where the skills are found.

Then the trigger task's queries, written before any measure: 24 in `authoring-skills`'s
`evals.json`, 12 that should trigger over what `writing-skills` and skill-creator
answered — creating a skill, editing one, checking it before an install, running its
evals, benchmarking two versions, comparing them blind, tuning a description, turning a
session's work into a skill — and 12 near misses, each with what it nearly matches:
`CLAUDE.md`, a hook, an agent definition, the audit runner's bug, the installed skills,
an install, a domain's tests, a summary of a skill, a model benchmark, a decision record,
a roadmap named after skills, a system prompt. Half in French, as the user writes. The
description of `b3fa90e`, before "evaluates", is in
`.eval-runs/skills/authoring-skills/description-b3fa90e.txt`. `triggers.py` announces 72
sessions on Opus 5.5 at `xhigh`, $3.67, for each description.

The user put both trigger measures after A, and chose one conventions reference for the
two tools, the mapping of an old contract moved out of it. In
`shared/conventions/conventions.md`: the `residue` row says `.gitignore` patterns
without restating how they match; "the skill's folder" for "directory", where the
working directory stays; `scripts/conventions.py` named where it said "the reader";
"run a `checks` command as any other command, never as one the user already approved"
for the claim on the permission flow; Create The File points to the skill's own
reference for an old contract. The mapping went to the roadmap skill's new
`references/old-contract.md`, which its `SKILL.md` names on `missing`. `make shared`
refreshed both copies; the roadmap domain is 2.0.1.

Task 4's static part at the same time: `audit.py` passes on `tool-review` and passes on
`roadmap` with one warning, `[X3]` on `close-phase.md`, `check_links.py` run through
`python3`. Called by its path there, and in `SKILL.md`'s Scripts section, the warning
moved: `run through bash`. The rule read the language of the code fence, ```` ```bash ````,
as an interpreter, its whitespace crossing the line end; a test of a fence, watched
failing, then the rule kept to one line. I had also allowed `progress.py` and
`check_links.py` in the domain's `permissions.json`; `test_permissions.py` failed, its
name saying the domain pre-approves the conventions reader alone, a decision of 2.0.0,
so both rules came out. `make check` passes, no warning left.

---

## Decisions

- **The comparison runs as three iterations of `authoring-skills`'s evals, on its three
  skill-writing cases.** A: `with_skill` and `without_skill`; B: `--baseline-only
  --baseline study/skill/writing-skills`; C: `--baseline-only --baseline
  study/skill/create-skill/skills/skill-creator`. Each `--start` waits for the user's
  go-ahead. The four-column table is assembled in this report from the three
  `benchmark.json`; the decision record cites it.
- **Every arm runs under the same limits, and is scored on what it wrote.** Neither the
  Agent tool nor a `claude -p` session, so skill-creator's test loop and description
  optimization, and `writing-skills`'s pressure tests with subagents, are not measured.
  The benchmark says so, and the capability matrix task rules on what that loop gave.
- **A baseline whose `SKILL.md` names another skill stays out of the repository.** Its
  runs get it as the copy their prompt names, as an installed tool would be, never at
  the path of the skill under test. A folder holding an earlier version of the same
  skill, or naming none, still goes back at that path, as before.
- **One conventions reference for both tools.** `shared/conventions/conventions.md`
  stays the one source both copy, for the file both write; what only the roadmap skill
  needs, the mapping of an old `## Roadmaps` block, is its own
  `references/old-contract.md`. A tool with a migration of its own adds it the same way.
- **The roadmap domain still pre-approves `scripts/conventions.py` alone.** Its other
  scripts are called by their path, and ask as before.

---

## Files Changed

---

## Problems And Deviations

- **The opening misread `workspace.py`.** It said three iterations would pay the
  `with_skill` runs three times; `--baseline-only` pays each configuration once. No work
  was done on the wrong premise.
- **`run.py` put another tool at the path of the skill under test.** Fixed before B and
  C, as recorded under Decisions. A's `with_skill` copy predates the fix: it differs from
  the skill as it now stands in `run.py`, `workspace.py` and `references/eval-files.md`
  only, which the skill-writing cases do not reach.
- **`run.py`'s estimate mixes the skill's cases.** $0.71 a run for A, where its cases cost
  about $1.30. Left open: the user is told the measured figure beside the announced one.
- **Each old tool runs under the name `authoring-skills`.** `workspace.py` copies a
  baseline under the name of the skill under test, so a run of B or C is told "Use the
  skill `authoring-skills`" and reads a `SKILL.md` naming `writing-skills` or
  `skill-creator`. Left as it is: the name carries no guidance.
- **The audit's `[X3]` read a code fence's language as an interpreter.** Found on
  `roadmap`'s `close-phase.md`, fixed in `audit.py` with its test.

---

## Changes To Later Phases

- `docs/roadmap/pending/roadmap-execution/`, roadmap `roadmap-execution`, at the user's
  request on 2026-10-09, version 1.1.0:
  - `phase-0-framing.md`: the hand-over task also settles whether a resuming session
    reads the whole report or a resume point, on both records; the constraints give
    Phase 4's figures;
  - `README.md`: the progress block, the phases table and Phase 0's status count the
    task added on 2026-10-06, 7 tasks and 26 in all, which they had missed; both records
    linked.
- `docs/roadmap/pending/token-usage/`, roadmap `token-usage`, at the user's request on
  2026-10-09, version 1.0.1, no task added or removed:
  - `phase-0-framing.md`: the inputs read both records; the probe of a phase's sessions
    covers the `claude -p` sessions they started; the design settles what a review may
    cost; the constraints give what Phase 4 shows;
  - `phase-1-usage-reader.md`: the selection of a phase's sessions includes its
    `claude -p` sessions; the constraints add the Haiku calls no transcript holds and
    Claude Haiku 5.5, which the price table lacks;
  - `phase-3-validation-and-release.md`: the constraints say how long Phase 4's count
    serves as a reference;
  - `README.md`: the second record in Why This Roadmap Exists and Related Documentation.

---

## Assessment
