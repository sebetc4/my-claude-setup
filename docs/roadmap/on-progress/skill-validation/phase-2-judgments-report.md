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
version, with tasks 1, 2 and 5.

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
