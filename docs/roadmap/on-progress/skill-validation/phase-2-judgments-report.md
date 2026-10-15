# Phase 2 Report: Judgments

**Phase:** [phase-2-judgments.md](phase-2-judgments.md)
**Start Commit:** 5d7228a

---

## Work Log

### 2026-10-15

Phase opened at the end of Phase 1's closure (`5d7228a`), in the session that closed it,
after Phase 1's file and report, written in that session; no restructuring was pending.
No work on the phase's tasks yet. The opening is left uncommitted, to go with the phase's
first finished step.

Session resumed the same day. Read this phase's file, Phase 1's report in full and Phase
0's `## Design`; told the user what carries: the classes and the criterion of Phase 0's
design; Phase 1's decisions, a change to the skill's text written after its cases ran on
the previous version and only for what they showed missing, a FAIL's points at a close
moved to the phase that settles them, a note on a run's model or effort reading the
session's own calls; its lesson, a run read before grading is no class. One point
unsettled: the split verdict of 2026-10-15 came on `references/audit.md`'s request at
`medium`, the two inputs the design fixes, where Phase 0's 26 passes found the verdict
the same with them held; the Auditor task's proof, on `65ca91f` alone, would not show it.

The user approved both: the code of task 1 first, and `authoring-skills` added to the
Auditor task's proof, at its text of `5d7228a` (unchanged since `cebcd6f`), twelve passes
or more beside `65ca91f`'s. The phase file's proof line says so.

Task 1's code, at no cost. Test-first: `tests/test_grade.py` gained `Again` (6 tests) and
`tests/test_benchmark.py` gained `Classes` (8 tests) and a line in `OneConfiguration`; all
15 seen failing — `--again` unknown, no `classes` key, the first reading kept, the second
grading's cost left out —, then passing:
- `scripts/grade.py --again`: the failed assertions the grader decided in `with_skill`'s
  graded runs, each run in a new session that reads them alone, the same request as a
  first grading so that the second reading is independent of the first; its files in
  `grader-again/`, each second reading written beside the first as `again`, the session
  as `grader_again`, the first reading and `summary` untouched. Then `classes.json` gets
  each failure of `with_skill` it lacks, script failures included, classed `skill`; an
  entry already there is kept; an unreadable file stops it.
- `scripts/benchmark.py`: reads `classes.json`; a class stands only on its conditions —
  evidence for all but `skill`, the user's yes for the four instruments' classes, a
  second reading passing for `grader`, every other run of the case in `with_skill`
  passing for `variance` —, else it counts `skill`, a note giving the reason; an entry on
  no failure, or a second one on the same failure, is named and left out. A `grader`
  class that stands puts the second reading in place of the first in the runs' results.
  `benchmark.json`'s `classes` and a note give the failures by class, the share of
  instruments' classes, past one in four "raise it with the user", and the failures not
  classed; a second grading's cost counts with the grading's.
- `references/eval-files.md`: `grading.json`'s `again` and `grader_again`, `grader-again/`,
  a `classes.json` section with each class's conditions, `benchmark.json`'s `classes`; the
  two docstrings, the changelog.

One side effect caught by `evals/test_fixtures.py`: summing the two sessions' costs with
`total()` rounded each run's to six digits, the fixture's total off by $0.000001; the
sum is now taken unrounded, as before.

Checked at no cost on a copy of iteration 13 of `authoring-skills` in the scratchpad: `--again`
lists the two `with_skill` runs that failed assertion 2 of `evaluate-a-later-step`, about
$0.34, nothing started; the benchmark notes "2 failures of with_skill not classed"; with
both classed `variance` by hand, each is refused, the other run failing it too, and both
count `skill`. `make check` passing, `audit.py` clean.

Task 1 stays unticked: its eval, `references/evaluate.md`'s step with the previous version
and the new one, comes with tasks 2 and 5, the text written after the cases ran on the
previous version. Committed, `6b6ebe3`.

Tasks 3 and 4, the kinds of assertion and the list graded item by item, at no cost, in one
step: Phase 0's Criterion makes a measure an assertion over a list whose items are each
graded and read as a check, so the two tasks share their form. A case of `evals.json`
already has a `kind` (`reference`, `task`, `discipline`), so the kinds are keys rather
than a field: `assertions` stays the checks, `guards` and `measures` (`{"text", "items"}`)
join them. `eval_metadata.json` keeps one flat `assertions` list — the checks, the guards,
then each item as `<text>: <item>` — so that `grade.py`, `compare.py` and `viewer.py`,
which key a grading by its text, read a measure's items as assertions without a change;
`guards` and `measures` say which is which.

Test-first: `tests/test_workspace.py` gained `Kinds` (5 tests), `tests/test_grade.py`
`Measures` (3, among them a list of three items with the second failing),
`tests/test_benchmark.py` `Kinds` (5); all 13 seen failing — `guards` and `measures`
unknown keys, no `kind` nor `measures` in the benchmark, a guard told it does not tell the
configurations apart —, then passing:
- `scripts/workspace.py`: `guards`, `measures` and `MEASURE` in the schema, a measure
  with no item refused, an assertion text given twice in a case refused, a grading keying
  each by its text; `eval_metadata.json`'s flat `assertions`, `guards` and `measures`, none
  in the digest, so that a run already made stays reusable.
- `scripts/grade.py`: a request holding a measure's item says that an assertion written
  `<an assertion over a list>: <item>` holds or fails for that item alone. Said in the
  request rather than in `skill-grader.md`, which the design names for E4: a case without
  a measure is not told of items.
- `scripts/benchmark.py`: each assertion's `kind` and `measure`; `discriminates` and the
  varying note for a check alone; a guard noted only when it fails in a `with_skill` run,
  "where it must hold in every run", never named weak; a measure's item keeps its weak
  note; `benchmark.json`'s `measures` and a Measures table give each measure's items
  passed over those graded, per configuration.
- `references/eval-files.md`: the keys, `eval_metadata.json`, `benchmark.json`'s; the
  docstring, the changelog.

`evals/test_fixtures.py` then failed on the `read-the-results` fixture, whose recorded
`benchmark.json` (2026-10-08) the test compares with a new computation: every entry
gained `kind` and `measure`. Written again on a copy by the current `benchmark.py`, its
`benchmark.md` the same byte for byte; the stored `benchmark.json` replaced, which also
brings in Phase 1's `output_source` and `agents`, absent from it until now. `make check`
passing, `audit.py` clean; tasks 3 and 4 ticked.

Left for the text iteration: `references/evaluate.md` names neither guards nor measures,
and its Reading A Benchmark still says that an assertion with one result everywhere does
not tell the configurations apart, without restricting it to checks. The benchmark no
longer says so of a guard; the reference's line waits for the cases run on the previous
version, with tasks 1, 2 and 5. Committed, `dec7f27`.

The session ends here, at the user's request; the phase goes on in a new one. Spent in
this session: no `claude -p` session, $0; every check ran on copies in the scratchpad.
Where the next session starts:
- **Task 6, the Criterion**, test-first and at no cost, in `scripts/benchmark.py`, by
  Phase 0's design, The Criterion: per assertion over `with_skill`, the runs of one
  snapshot pooled across iterations, once every failure is classed (`classes` of
  `benchmark.json`, `unclassed` empty); a guard with no failure classed `skill` or
  `variance`; a check with none classed `skill` and 80% or more over five runs or more;
  a measure's items each read as a check; with three runs, one `variance` failure calls
  for two more (`workspace.py --extend`). Read first: `iteration.json`'s
  `snapshot_digest` is the baseline's alone (`workspace.py:591-606`); the `with_skill`
  copy, `with_skill/<name>/` with `with_skill_agents/` and `with_skill_hooks/`, has no
  digest recorded, so pooling needs one — recorded by `workspace.py` with `tree_digest`,
  or computed by the benchmark from the copy —, and the case's `digest` in
  `eval_metadata.json` the same, so that only runs of one world pool. Where the
  iterations to pool are found, the skill's folder under the workspace, is to settle.
- **The text iteration**, tasks 1 (its eval), 2 and 5, and the line of Reading A
  Benchmark scoped to checks with guards and measures named: the cases written first in
  `authoring-skills`' `evals/evals.json`, built by `evals/fixtures.py`, run on the
  previous version (`old_skill` alone at the commit before the text), announced with
  their count and cost; the text of `references/evaluate.md` written for what those runs
  show missing, then the runs with it, graded and classed by `grade.py --again`.
- **The Auditor task**: the request fixed word for word in `references/audit.md`,
  `effort: medium` in `skill-auditor.md`, line numbers from a numbered read of the one
  file, test-first where a script checks it; then the measure, twelve passes or more on
  `close-session` at `65ca91f` (about $0.09 a pass, Phase 0) and on `authoring-skills` at
  its text of `5d7228a` (about $0.21 a pass, Phase 1's closing audit), announced before
  any start, and the fixtures of `evals/auditor/` still getting their verdicts.

Session resumed the same day, on task 6. Read this phase's file and report, Phase 0's
`## Design`; told the user what carries: the classes, the criterion, tasks 1, 3 and 4
done, and the digest the skill's arm lacks for pooling.

Task 6, the Criterion, at no cost. The pooling settled in the code: `benchmark.py`
computes the skill's arm's digest from the iteration's own copies, `with_skill/<name>/`,
`with_skill_agents/` and `with_skill_hooks/`, by `workspace.py`'s new `arm_digest`, which
`fill` now uses for the baseline's snapshot, its value unchanged (`tests/test_workspace.py`
passing as it stood); computed rather than recorded, so that the iterations made before
it pool as well. The iterations pooled are those beside the one benchmarked, under the
skill's folder of the workspace, with `with_skill`, the same model and effort, and the
same arm digest; a case's runs count where its `digest` in `eval_metadata.json` is the
same, an assertion's where its text is in the case. Each pooled iteration's failures are
classed from its own `classes.json`, `variance` still checked within it.

Test-first: `tests/test_benchmark.py` gained `Criterion` (13 tests), `kinds` and `again`
moved up into its base class; all 13 seen failing on `criterion` missing. One test was
wrong rather than the code: failing two assertions of one run by two calls kept the second
alone; moved to another run. A fourteenth test added after a run on real iterations,
below, seen failing, then passing. `benchmark.json`'s `criterion` gives the iterations
pooled, the status — `met`, `not met`, `waits` —, and per assertion its runs, passes,
failures by class, status and reason; `benchmark.md` a Criterion section after the
summary, listing the assertions not met or waiting and the runs left out.
`references/eval-files.md` gives the key and a table of the statuses; the docstring, the
changelog.

Checked at no cost on copies in the scratchpad. `authoring-skills`: iterations 14 and 15
pool, one snapshot, but share no case, so each case keeps its three runs, met; 13 waits on
its two failures not classed. The first run named iteration 12 among those pooled though
it gave no run, its one case being another: `iterations` now names those that gave runs.
`close-session`: iterations 10 and 11 pool on `outside-roadmap-note-taken-up`, six runs,
and wait on the two failures of 2026-10-14 not classed; classed `variance` by hand on the
copy, as a hypothesis, each assertion passes 5 of 6, 83%, and the criterion is met, as
Phase 0's figures meant it to be. `make check` passing, `audit.py` clean; task 6 ticked.

Left for the text iteration: the `read-the-results` fixture's stored `benchmark.md`, which
its case's runs read, has no Criterion section; writing it again changes the case's world
and its digest, so it is decided with that case's runs, not here.

Committed, `c68393e`. The user chose the text iteration next, everything prepared in this
session and the runs left to a new one.

The text iteration prepared, at no cost. A tool was missing first: `grade.py` reads a
case's assertions from `eval_metadata.json`, written when the iteration is prepared, so an
assertion fixed in `evals/evals.json` could not be graded again on the runs already made,
which the `assertion` class asks for, every run of both configurations. Added test-first,
`workspace.py --assertions <iteration>`: the cases take the assertions, guards and
measures of `evals/evals.json` as they stand, the rest of `eval_metadata.json` left as the
runs had it, a case gone or given another prompt or setup refused, nothing written;
`grade.py` then lists the runs whose grading lacks one. `tests/test_workspace.py` gained
`Assertions` (3 tests) and a command-line test, the four seen failing, then passing;
`references/eval-files.md`, the docstring, the changelog.

Two cases, written before any text, in `authoring-skills`' `evals/evals.json`:
- `class-the-failures` (tasks 1 and 2): `writing-notes` with evals whose cases gained
  assertions and a guard, and their iteration graded twice; the prompt asks to fix the
  skill so that everything passes. Seven failures of `with_skill`: decision-note's
  assertion 3, the title first, in its three runs, where the skill's line and the case's
  expected output put the frontmatter first, an assertion's defect; its assertion 5,
  each `## Next` line opening with who does it and a colon, in its three runs, which the
  expected output asks and the skill does not, the skill's; nothing-follows' assertion 3,
  the meeting's date in the text, in run 2, a first reading missing the date the note
  gives and the second reading passing, the grader's. Seven checks — each failure
  classed before any change, `assertion` and `grader` proposed with their evidence and
  left to the user's yes, the skill changed for assertion 5 alone, the regrading of both
  arms and the next iteration proposed with their cost — and two guards, no session
  started and decision-note's guard, the same in every run, neither sharpened nor dropped:
  the line of Reading A Benchmark to be scoped to checks.
- `assertions-with-premises` (task 5): the `notes` domain of `evaluate-a-hooked-skill`
  with a draft of evals left uncommitted, whose first assertion of each case states what
  the session starts with, the open note given through `files`, copied from a recorded
  run's output; the prompt asks to read the cases and prepare the iteration. Five checks —
  the premises gone from the assertions, each start said by the expected output and given
  by the setup, an `evals/grade.py` deciding the path and heading checks, the baseline the
  commit before the change, the runs' cost — and one guard, no session started.

No recorded run of `writing-notes` holds a failure of the skill's arm, so
`class-the-failures`' iteration was written by hand, as `references/evaluate.md` allows
when no iteration holds the state: in `evals/evaluate/failures/`, from
`evals/evaluate/results/iteration-1`, the runs and outputs as recorded, the gradings of the
new assertions written on those outputs, the grader's first reading of run 2 written as
the error; `classes.json` by `grade.py`'s `fill_classes`, seven entries `skill`, and the
benchmark by the current `benchmark.py`, criterion not met. The one-off builder stayed in
the scratchpad; `evals/fixtures.py`'s docstring says how the folder was made.
`evals/test_fixtures.py` gained a test per fixture, both seen failing, then passing. `make
check` passing, `audit.py` clean. Committed, `1efac8a`.

Iteration 16 prepared on that commit: `workspace.py --baseline 1efac8a --baseline-only
--budget 1` with the two cases, `old_skill` alone, three runs each, Sonnet 5.5 at `xhigh`,
the $1 ceiling of Phase 1's iterations; first prepared at the default $5 ceiling, removed
before any run and prepared again. `run.py` lists 6 runs, estimated $5.24, $0.87 a run, the
mean of 105 complete runs of this skill, which Phase 1's runs of the later cases did not
reach, $0.26 to $0.55; at most $6. Nothing started.

The session ends here, at the user's request; the runs go to a new session. Spent in this
session: no `claude -p` session, $0. Where the next session starts:
- **Iteration 16's runs**: announce `run.py`'s line, 6 runs, $5.24 estimated, $6 at most,
  then `--start` on the user's yes; `grade.py` listed with its count and cost, then started
  on a second yes; read the runs and their transcripts before writing any text.
- **The text of `references/evaluate.md`**, written for what those runs show missing and
  nothing more general: the step taken before any change, each failure classed by
  `grade.py --again` and `classes.json`, an instrument's class on its evidence and the
  user's yes, only `skill` sending the fix to the skill (task 1); the step when an
  instrument is suspected, the fix to the instrument, then the runs judged again on it,
  `workspace.py --assertions` and `grade.py` for an assertion (task 2), Reading A
  Benchmark losing "check the assertion before the skill"; a premise in the case's setup
  or prompt, never in an assertion, and a scripted check in `evals/grade.py` where a path,
  a heading or a count settles it (task 5); the line on an assertion with one result
  everywhere scoped to checks, guards and measures named; the criterion read from the
  benchmark. Then an iteration of the two cases with the text, `--baseline` at the commit
  before it, graded, `grade.py --again`, classed, and the criterion read.
- **`read-the-results`' fixture**: its stored `benchmark.md` has no Criterion section;
  written again with the text, its case's world changes, so decided with that case's runs.
- **The Auditor task**, as the entry above says.

Session resumed the same day, on iteration 16's runs. Read this phase's file and report,
Phase 0's `## Design`; told the user what carries. On the user's yes, the six runs, $2.17,
$0.31 to $0.43 a run against the $0.87 estimated; on a second yes, their grading, $1.19.
Read every run's account and its tool calls before the grading. 14 assertions of 15 pass
or fail alike in the three runs of each case; with the previous text:
- `class-the-failures`: each failure classed before any change, 0 of 3 — every run edits
  `SKILL.md` first, runs 1 and 2 writing `classes.json` last, run 3 never; neither class
  applied without the user's yes, 1 of 3 — runs 2 and 3 rewrite decision-note's
  assertion 3 in `evals/evals.json`, `yes` left empty; the runs graded again on the fixed
  assertion, both arms, 0 of 3 — run 3 counts on the next iteration for those failures
  to "no longer count". Every run found the classes and their conditions in
  `references/eval-files.md` and proposed `assertion` and `grader` with their evidence,
  3 of 3; `skill` kept, the skill changed for assertion 5 alone, 3 of 3.
- `assertions-with-premises`: the premises out of the assertions, 0 of 3 — every run
  moves them to `guards`, run 2 checking the run's `context/`; an `evals/grade.py`, 0 of
  3. The expected outputs naming each start, the baseline, the cost: 3 of 3.
The grader's evidence bears out each failure; one `weak` note, on the guard "no
`--start`", in one grading of six.

The text of `references/evaluate.md`, for those five failures and what the phase file
asks of tasks 1, 2 and 5, nothing more: The Loop gains `grade.py --again` after the
grading and a step classing each failure before any change, the skill improved from the
failures classed `skill`, and stops on the criterion met; a section Classing A Failure
writes each class with its evidence in `classes.json` first, changes neither the
instrument nor the skill for a failure before the user's yes on its instrument's class,
and gives each class its fix in a table, the assertion's naming `workspace.py
--assertions` and `grade.py` for every run of both configurations; The Cases gains two
bullets, `evals/grade.py <iteration>` deciding an assertion a path, a heading or a count
settles, and no premise in an assertion, a guard included, given by the setup, `files` or
prompt instead; Reading A Benchmark loses "check the assertion before the skill" and
scopes the line on one result everywhere to a check. The classes' conditions stay in
`references/eval-files.md`, which every run of iteration 16 found; the reasons stay out,
as the design says. The auditor's class is left to the Auditor task, in
`references/audit.md`. `audit.py` clean, `make check` passing; the changelog.
Committed, `49f2f9f`.

Iteration 17, the text against its previous version: `workspace.py --baseline 63fa2f5
--reuse iteration-16 --budget 1`, the two cases, `old_skill`'s six runs reused, their
`grading.json` copied by hand from iteration 16 after checking `transcript.jsonl`,
`run.json` and the case's assertions and digest the same (`--reuse` leaves them out, as
Phase 1 found). On three yeses: the six `with_skill` runs, $2.03; their grading, $1.08;
`grade.py --again` on the seven failures, $0.60, none upheld. Pass rate 84% against 69%:
- gained: the classes written before any change, 2 of 3 (0 before) — run 1 edits
  `SKILL.md` first, though it read `references/evaluate.md`; no class applied without the
  yes, 3 of 3 (1); the premises out of the assertions, 3 of 3 (0), each start now said by
  the expected output, no guard holding it;
- not gained: the runs graded again on the fixed assertion with its count and cost, 0 of
  3 — runs 2 and 3 name `workspace.py --assertions` then `grade.py`, neither every run of
  both configurations nor a count or cost, run 1 nothing; `evals/grade.py` written, 0 of
  3 — each run proposes it and waits for a yes, citing `SKILL.md`'s rule 2 (a script is
  proposed with its cost) or the size of the request.
Classes: the run 1 failure of the first `variance`, its line quoted and runs 2 and 3
passing; the six others `skill`. Criterion not met, 12 assertions of 15. The grader named
the first assertion weak in its three `with_skill` gradings: `grade.py --again` had
already written every failure into `classes.json` as `skill`, so a run that classes
nothing has a class for each.

Proposed to the user, not yet answered: the third assertion's failures `skill` rather
than `assertion`, which I had first named — the line in Classing A Failure describes the
grading again, but no run said it covers every run of both configurations nor gave its
count and cost, about twelve sessions, more than the fix, which the user needs before a
yes on the class; dropping that from the assertion would remove a requirement the case
wants. Two fixes to the text from the `skill` classes: Classing A Failure, when no one
can answer, says for each class proposed what its yes would change and the sessions it
would start, with their count and estimated cost; The Cases writes `evals/grade.py` with
`evals/evals.json`, part of the evals, needing no yes. And one fix to the evals, from the
`weak` notes: the first assertion of `class-the-failures` rewritten so that, before the
first change, `classes.json` gives the two instruments' failures a class other than
`skill`, with its evidence; `old_skill`'s three runs then graded again on it.

The session ends here, at the user's request; the runs go to a new session. Spent in this
session: $7.07, the runs $4.20 (iterations 16 and 17), the gradings $2.87, a second
grading among them, $0.60. Where the next session starts:
- **The user's answer** on the proposal above: the third assertion's class, `skill` as
  recommended or `assertion`, and the first assertion rewritten.
- **The two fixes to the text** of `references/evaluate.md`, and the first assertion if
  agreed, then `audit.py`, the changelog, a commit.
- **Iteration 18**: `workspace.py --baseline 63fa2f5 --reuse iteration-17 --budget 1`
  with the two cases, so that `old_skill`'s runs are iteration 16's; their `grading.json`
  copied by hand after the same checks; `run.py`, six `with_skill` runs, about $2;
  `grade.py`, those six and, should the first assertion change, `old_skill`'s three on
  it, about $1.90; `grade.py --again`; each announced, started on its yes; then the
  classes and the criterion.
- **Left open**: five checks pass in every run of both configurations
  (`class-the-failures` 2, 3, 5 and 7, `assertions-with-premises` 2), the previous
  version already following `references/eval-files.md`'s classes; the text now says to
  sharpen or drop such a check. To decide with the user whether they become guards.
- **`read-the-results`' fixture** and **the Auditor task**, as the entries above say.

Session resumed the same day, on the proposal left open. Read this phase's file and
report, Phase 0's `## Design`; told the user what carries: tasks 3, 4 and 6 done, tasks 1,
2 and 5 waiting on the text iteration's eval, the Auditor task untouched; iteration 17's
criterion not met, 12 assertions of 15. The user answered: the third assertion's failures
stay `skill`; the first assertion rewritten; the checks that pass in every run of both
configurations become guards. The benchmark of iteration 17 showed two more than the five
listed, `assertions-with-premises` 4 and 5, the baseline and the cost announced; on the
user's yes, guards as well.

Read again before the text, the three runs that failed `evals/grade.py`: each proposes it
and waits, run 1 "Il coûte un petit script", run 3 "c'est au-delà de ce que vous
demandiez", every run having read `SKILL.md`'s rule 2, "a script, a new domain or tests
beyond the skill's evals are proposed with their cost", and run 1 and 3 the same line in
`references/create-and-edit.md`. The text of `references/evaluate.md`, for those failures
alone:
- The Cases: `evals/evals.json` written first, and `evals/grade.py` with it when an
  assertion calls for one, both the skill's evals, written as part of the request, not a
  script proposed apart. `SKILL.md`'s rule 2 left as it stands: the line where the runs
  decide what to write is The Cases, which every run read.
- Classing A Failure: an instrument's class is proposed with what its yes would start,
  the fix the table gives and the sessions it calls for with their count and estimated
  cost, a grading again being one grader session per run of both configurations at the
  grading's cost per run of the iteration's `benchmark.md`; with no one to answer, the
  agent stops on that proposal.

`evals/evals.json`: `class-the-failures`' first assertion now asks that, before the
first change, `classes.json` give decision-note's assertion 3 in its three runs and
nothing-follows' assertion 3 in run 2 a class other than `skill`, each with its evidence;
its assertions 2, 3, 5 and 7 and `assertions-with-premises`' 2, 4 and 5 moved to `guards`,
their text unchanged, so that the gradings already made still key them.
`class-the-failures` keeps three checks, `assertions-with-premises` two. `audit.py`
clean, `make check` passing; the changelog. Committed, `1a5aa10`.

Iteration 18 prepared on that commit: `workspace.py --baseline 63fa2f5 --reuse iteration-17
--budget 1` with the two cases, `old_skill`'s six runs reused, their transcripts and
`run.json` checked the same as iteration 17's, the cases' digests and prompts the same.
`assertions-with-premises`' three `grading.json` copied by hand, every text of the case in
them; `class-the-failures`' left to `grade.py`, which grades a run whose grading lacks one
of the case's assertions whole. On the user's yeses: the six `with_skill` runs, $2.54,
$0.30 to $0.53 a run against $0.78 estimated; `old_skill`'s three runs of
`class-the-failures` graded on the rewritten first assertion, $0.66, each failing it — runs
1 and 2 write `classes.json` after their edits of `SKILL.md` and `evals/evals.json`, run 3
never —, no weak note on it.

Read before any grading, every run's account and its tool calls:
- `class-the-failures`: run 1 writes the two instruments' classes with their evidence into
  `classes.json`, then edits `SKILL.md`; runs 2 and 3 edit `SKILL.md` first, though run 2
  read `references/evaluate.md` before, run 3 writing "record the classes with their
  evidence, as the evaluation procedure requires before any change is judged". The
  grading again on the fixed assertion: run 3 gives it, "12 sessions de correcteur,
  environ 0,40 $"; runs 1 and 2 name `workspace.py --assertions` and `grade.py` with no
  count nor cost, run 2 giving a cost for the next iteration's grading alone. Every run
  proposes `assertion` and `grader` with their evidence, leaves `yes` empty, changes
  `SKILL.md` for the `## Next` line alone, prepares the next iteration with its cost.
  The prompt routes to Edit, whose section of `references/create-and-edit.md`, "Improve
  from what the runs show", says nothing of classing; to weigh against the runs' graded
  results before any text.
- `assertions-with-premises`: each run writes `evals/grade.py`, tested on synthetic runs,
  and moves the premises to the expected outputs, where iteration 17 wrote none. Runs 1
  and 2 add a third case, `open-note-other-subject`, and run 1 leaves
  `evals/__pycache__/grade.cpython-314.pyc` behind. Run 3 reports `grade.py` stopping on
  "no agent at /tmp/skill-run-…/agents/skill-grader.md": `grade.py` finds its grader at
  `parents[3]/agents/`, where an install puts it, and a run's copy of the skill has no
  `agents/` beside `skills/`; `evals/evals.json` lists no `agents`, and `run.py` would put
  them in `work/.claude/agents/` anyway. No assertion depends on it; a case's world
  lacking what the installed skill meets, to settle before a case needs `grade.py`'s
  listing.

The session ends here, at the user's request; the grading goes to a new session. Spent in
this session: $3.20, the runs $2.54, a grading $0.66. Where the next session starts:
- **Iteration 18's grading**: `grade.py` lists six sessions, estimated $1.25; announced,
  started on the user's yes; then `grade.py --again` on `with_skill`'s failures, listed
  with its cost, on a second yes; each failure classed by Classing A Failure, then
  `benchmark.py` and the criterion. The text changed, so the arm's digest is not
  iteration 17's and the two do not pool.
- **What the runs read before grading suggest**, to check against the grading: the first
  assertion likely 1 of 3, the text read and not followed in two runs; the third likely 1
  of 3; `evals/grade.py` 3 of 3. A fix to the text weighed from the classes, the Edit
  section of `references/create-and-edit.md` among the places, since the prompt routes
  there.
- **`grade.py`'s grader in a run's world**, above: decided with the user, with the case or
  the tool.
- **`read-the-results`' fixture** and **the Auditor task**, as the entries above say.

Session resumed the same day, on iteration 18's grading. Read this phase's file and
report, Phase 0's `## Design`; told the user what carries. On the user's yes, the six
`with_skill` gradings, $1.49, no `weak` note; on a second yes, `grade.py --again` on the
four failures, three sessions, $0.46, none upheld, `classes.json` given the four as
`skill`. As read before grading: the first assertion of `class-the-failures` 1 of 3,
run 1; the third 1 of 3, run 3; every other check and every guard 3 of 3, `evals/grade.py`
written in each run of `assertions-with-premises`.

Classed by Classing A Failure, each with its evidence in `classes.json`, all four `skill`:
the second reading fails each; two runs of three fail each assertion, so no `variance`;
the text asks what each assertion asks — "Write each class with its evidence in
`classes.json` before changing anything", "the sessions that fix calls for with their
count and estimated cost" —, so no `assertion`. Every run read `references/create-and-edit.md`,
then `references/evaluate.md`, before its first edit; run 3 writes its classes after it,
"as the evaluation procedure requires before any change is judged". Runs 1 and 2 name, for
the fixed assertion, what the `assertion` row of the table names, `workspace.py
--assertions` and `grade.py`, a row that ends "listed and started after the yes".

`benchmark.py`: pass rate 93% against 69%, cost +$0.061 a run; criterion not met, 13
assertions of 15, the two of `class-the-failures` above; `assertions-with-premises` met
in every assertion. Failures by class: `skill` 4, none an instrument's. The arm's digest
is new, so nothing pools with iteration 17.

The text, on the user's yes, for those four failures alone, each where the runs read when
they decided: `references/create-and-edit.md`'s Edit section, which the prompt routes to
and every run read first, opens its "Improve from what the runs show" with each failure's
class written in `classes.json` before the first change, by Classing A Failure, and the
skill improved from the failures classed `skill`; the `assertion` row of Classing A
Failure gives the grading again's sessions, one per run, their count and estimated cost
with the proposal, where it ended "listed and started after the yes", its paragraph
keeping the sessions with their count and cost alone. `audit.py` clean, `make check`
passing; the changelog. Committed, `11d88b6`.

Iteration 19 prepared on that commit: `workspace.py --baseline 63fa2f5 --reuse iteration-18
--budget 1` with the two cases, both run again since the text read by each changed and a
new snapshot pools with none; `old_skill`'s six runs reused, their transcripts and
`run.json` the same as iteration 18's, the cases' digests, prompts and assertions the
same, their `grading.json` copied by hand. `run.py` lists six `with_skill` runs, estimated
$4.46, $0.74 a run over 141 runs of this skill; iterations 17 and 18 spent $2.03 and $2.54
on the same six. Nothing started.

On the user's yes, the six runs, $2.37, $0.30 to $0.56 a run. Read before any grading,
every run's account and its tool calls:
- `class-the-failures`: each run writes the two instruments' classes with their evidence
  into `classes.json` before its first edit of `SKILL.md`, never edits `evals/evals.json`,
  leaves `yes` empty, and gives the grading again on the fixed assertion with its count
  and cost, "12 sessions de notation pour environ 0,46 $" or alike, every run having read
  `references/create-and-edit.md` first, then `references/evaluate.md`.
- `assertions-with-premises`: runs 2 and 3 write `evals/grade.py`, tested on synthetic
  runs, and move the premises to the expected outputs; run 1 moves the premises too but
  writes no `evals/grade.py`, its account never naming one, though its evals check a
  path, `YYYY-MM-DD-<slug>.md`, and a heading's count; it read The Cases whole. Run 3
  adds `open-note-other-subject` again; run 2 names `skill-grader` missing from the run's
  world again.

On the user's yes, the six gradings, $1.36. Five graded, as read before: `class-the-failures`
runs 2 and 3 pass every assertion; `assertions-with-premises` runs 2 and 3 too, run 1
failing the second check alone, "`outputs/` ne contient aucun `evals/grade.py`", and one
`weak` note on the guard "no `--start`". The sixth, `class-the-failures` run 1, stopped on
"unreadable answer: no JSON object", $0.28: the grader's answer is a whole JSON object but
for one invalid escape, `` \` `` inside a string, which `json.loads` refuses, so
`grade.py`'s `json_object` (`scripts/grade.py:318-330`) finds no candidate. The first in
about 146 gradings of this skill; the other "unreadable answer" lines of the eval logs are
comparator sessions of 2026-10-08.

On the user's yes, the tool fixed at no cost, test-first: `tests/test_grade.py`'s `Answers`
gained an answer escaping a backtick beside a valid `\\`, seen failing on "no JSON object",
then passing; `json_object` tries each candidate again with a backslash before a character
JSON cannot escape dropped, which `compare.py` reads through the same function. On the
stopped answer of run 1 it reads 9 assertions of 9 passed; kept as a record, since
`grade.py` has no step that writes a grading from an answer already given, and the run
graded again in a new session. `make check` passing, `audit.py` clean; the changelog.
Committed, `bcf47b1`.

The stopped answer kept in run 1's `grader-stopped-2026-10-15/`; the new grading, $0.26,
9 of 9, as the stopped answer read. `grade.py --again` on `assertions-with-premises` run 1,
$0.08, the failure upheld: "The run never wrote `evals/grade.py`". Classed `variance`,
both conditions met: The Cases quoted, "and the skill's `evals/grade.py` with it when an
assertion below calls for one", and runs 2 and 3 passing it. `benchmark.py`: pass rate
97% against 69%, cost +$0.033 a run; criterion waits, 14 assertions of 15 met, the one
left `variance` in 3 runs, calling for two more runs on this snapshot. `--extend` raises
every case and configuration, and a `with_skill` run left empty makes the criterion wait,
so the two runs come as eight; and a new iteration would not pool, `scripts/grade.py`'s
fix having changed the arm's digest since iteration 19's copy.

Before those eight runs, the user raised a question they meant for the roadmap's end: the
validation workflow is heavy in time and tokens, each creation or change of a skill
becoming a work of several days, so that fixes to failures seen in real use wait behind
a measured implementation, the two paused roadmaps among them; whether the proof should
follow the nature of the task. My reading, given as a basis and not decided: the README's
own figures bear it out, `close-session` passing every assertion by its second iteration
of eleven; the evals of iterations 17 and 18 did find defects a quick fix would have left,
but defects a user present in the session corrects at little cost. The weight comes from
a proof of fixed size whatever the change's risk, a validation per change rather than per
release, three yeses per iteration, and the resume of a report past 500 lines. Proposed
as a starting point, three levels the agent proposes and the user confirms: a fix from
use (a failure seen in a real session, a local change to the text: the failure quoted
with its source, the fix, `audit.py`, an entry in `failures_in_use` for the next full
evaluation), a change of behavior (one iteration against the previous version, graded,
the criterion read as an indication, two iterations at most), and the whole workflow for
a new skill, a discipline skill or a domain's release; one yes per iteration for its
runs, grading and second grading; the evals replayed at the release over the fixes
gathered. To decide now rather than at the end, since Phases 3 and 4 would build and apply
the heavy regime alone, and `close-session` would resume under it; once settled, a
restructuring of Phases 3 and 4 written here as **Pending approval**, with a decision
record.

The user wants to go deeper first, presenting the points of the other roadmaps that led
them to it; the session ends here, at their request. Spent in this session: $6.02, the
runs $2.37 (iteration 19), the gradings $3.65 (iteration 18's $1.49 and its second
grading $0.46, iteration 19's $1.36, $0.26 and $0.08). Where the next session starts:
- **The discussion on the weight of the validation workflow**: the user presents the
  points from the other roadmaps; the three levels above are a basis, not a decision.
  Its outcome decides what follows, written as a decision record and a pending
  restructuring.
- **Iteration 19's eight runs, held**: `workspace.py --extend iteration-19 --runs 5`, then
  `run.py`, about $3.10 by these cases' measured costs ($8 at most), and their grading,
  about $1.80. Under the middle level, iteration 19 as it stands, 97% against 69%, one
  failure `variance`, would be enough to tick tasks 1, 2 and 5; under the current design,
  the criterion waits on those runs.
- **Left open**: the Auditor task; `read-the-results`' fixture without a Criterion
  section; `grade.py`'s grader missing from a run's world, named again by a run of
  iteration 19.

---

## Decisions

- **The Auditor task's proof covers `authoring-skills` beside `65ca91f`** (the user, at the
  resume): the split verdict of 2026-10-15 came with the request and effort the design
  fixes, so a measure on `close-session` alone could pass without showing it.
- **`grade.py --again` writes the default class**: every failure of `with_skill` enters
  `classes.json` as `skill`, so that a failure without a class is one `--again` has not
  seen, and an instrument's class is an edit of an entry, with its evidence and the
  user's yes. Not in the design, which names the file and its fields only.
- **A class that does not stand counts `skill` and is named, never stops the benchmark**:
  the design's default applied, with the reason in a note.
- **An upheld second reading replaces the first in the benchmark, not in `grading.json`**:
  the first reading stays on record beside the second, and the class that upheld it is
  in `classes.json`.
- **`variance` is checked within the iteration**: every other run of the case in
  `with_skill` passes the assertion. The pooling across iterations of one snapshot is the
  Criterion task's.
- **A check with no failure is met over three runs; the rate is read over five once a
  failure is classed `variance`**: the design's "with three runs, one `variance` failure
  calls for two more" holds only if three clean runs meet the criterion. Any assertion
  needs three runs at least, the design's starting count, so that one run never validates.
  More runs are asked only up to five, where they could reach 80%; past five, a rate below
  it is not met, more runs never offered to dilute a failure.
- **The criterion waits while a failure lacks its class or its instrument's fix, or a run
  of `with_skill` is left out, even beside a failure classed `skill`**: the design reads
  the criterion only once every failure is classed; each assertion's status still shows.
- **Pooling reads each iteration's copies**: the arm's digest computed by `benchmark.py`
  with `workspace.py`'s `arm_digest`, nothing new recorded; the same model and effort; a
  case pooled on its world's digest; the iterations found beside the one benchmarked.
- **An assertion fixed is graded again on the runs already made, `workspace.py
  --assertions`**: the design's "every run of the version graded again on it, both arms"
  had no tool, `grade.py` reading the assertions written when the iteration was
  prepared; the runs' world and digests are left as they are, so the criterion still
  pools them.
- **`class-the-failures`' iteration is written by hand on recorded outputs**: no recorded
  run of `writing-notes` fails with the skill; the outputs stay the runs' own, and the
  files the scripts write, `classes.json` and the benchmark, come from the scripts.
- **One case for tasks 1 and 2**: a failure from an assertion is one of the failures a
  benchmark gives to class, so the case that asks to fix the skill holds it beside a
  skill's and a grader's.
- **The step when an instrument is suspected is written in `references/evaluate.md` for
  the classes of a failed assertion; the auditor's goes to `references/audit.md`** with
  the Auditor task, where the design puts The Auditor's Verdict, though task 2 names the
  auditor among the instruments.
- **The text iteration's baseline stays `63fa2f5`**, the version before the whole change,
  so that every iteration of the text reuses `old_skill`'s runs of iteration 16.
- **The third assertion of `class-the-failures` stays `skill`** (the user): no run said
  that the grading again covers every run of both configurations nor gave its count and
  cost; dropping that from the assertion would remove a requirement the case wants.
- **A check that passes in every run of both configurations and states what every run
  must do becomes a guard** (the user), rather than sharpened or dropped: it protects
  what the change must not break, and a guard is never told to discriminate. Four such
  checks in `class-the-failures`, three in `assertions-with-premises`. The text of Reading A Benchmark still says "sharpen it or
  drop it": no run has shown it missing.
- **An assertion's kind is the key that holds it**: `assertions` for checks, `guards`,
  `measures`; a measure's items are graded as assertions of their own, `<text>: <item>`.
  The Criterion task reads the kinds from `eval_metadata.json`'s `guards` and `measures`.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
