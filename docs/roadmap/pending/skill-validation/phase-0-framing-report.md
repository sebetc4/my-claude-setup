# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** 039a804

---

## Work Log

### 2026-10-14

Phase opened. Read before working: the roadmap's README and this phase's file. The two
feedback notes the phase starts from are in place in the ignored
`notes/design-feedback/`: `2026-10-14-close-session-validation.md` and
`2026-10-14-reviewing-delivered-code-validation.md`.

Task 1, with the user's leave to read ai-ctl's `review-skill`: read both notes in full,
ai-ctl's Phase 3 report in full and its Phase 2 report where it cuts blocks and passes the
auditor. The repository's `domains/skill-tooling/` differs from the installed 0.1.2 only in
`references/conventions.md` and `scripts/conventions.py`, so the notes' line numbers hold
for the source; each was checked there. The map below gives each problem the lines that
cause it, the skill's paths from `domains/skill-tooling/skills/authoring-skills/`, the
agents' from `domains/skill-tooling/agents/`:

- **V1, a case's world the installed skill never meets.** `scripts/harness.py:124` starts
  every run with `--setting-sources project,local`, which leaves out the user's hooks and
  keeps the project's (`harness.py:9-11`); `scripts/run.py:209-232` (`build_work`) puts in
  the run's folder the skill's copy and its agents, never a hook of its domain. Nothing
  asks for that world to be declared: `references/eval-files.md:60-72` gives a case no key
  for the context a hook would inject or for a hook declared off, and
  `references/evaluate.md:29-55`, The Cases, has no step that checks the hooks, settings
  and tools a skill relies on. Found beyond the note: since the project's hooks stay, a
  fixture can already provide a hook in its own `.claude/settings.json`; no text says so.
- **V2, zero failures read through one grading per run.** `scripts/grade.py:118-135`
  grades a run only while its `grading.json` lacks an assertion, so each run gets one
  grading and a second needs the file deleted; `references/evaluate.md:64-67` asks three
  sessions per pair for a blind comparison because "a judgment varies from one session to
  the next", but nothing of the kind for a grading. `evaluate.md:93-94` sets no pass
  criterion, `evaluate.md:99-100` checks the assertion before the skill without classing
  the failure, and `evaluate.md:104-105` gives the grader's spread a rule for a weak flag
  only.
- **V3, the auditor's verdict changing on the same text.** `agents/skill-auditor.md:24-25`
  asks for every problem an open reading finds, and `:50-51` fails on any one;
  `:27-45`, the five judgments, never weigh a point against the evals' results;
  `references/audit.md:35-47` reports the verdict and turns a fix into an edit, with no
  rule for a point a second pass does not raise. Found beyond the note: the auditor's
  frontmatter sets no `effort` (`skill-auditor.md:1-6`), where `skill-grader` sets
  `xhigh`; the measures of task 3 are to fix it.
- **V4, the sourcing rule putting repository paths in a portable skill.**
  `references/writing-guide.md:80-82` asks a source for every fact, the repository's
  included, and `agents/skill-auditor.md:35-38` fails a fact without one; neither sets
  apart a source the running agent never opens, nor a fact it observes in its own
  context. `scripts/audit.py:428`, rule R2 of the catalogue, warns on a citation outside
  the skill, which turned `close-session`'s citation of the roadmap skill's file into the
  "my-agent-setup `<path>`" form.
- **V5, failures seen in real sessions counting for nothing.**
  `agents/skill-auditor.md:31-32` fails a prohibition that answers no failure "in the
  evals", and `references/eval-files.md:71` holds only "failures quoted from runs";
  `references/writing-guide.md:69-70` and `references/create-and-edit.md:93-95` tell to
  write only what the runs without the skill showed, or the request states.
- **V6, a premise inside an assertion.** `references/evaluate.md:36-39` and
  `references/eval-files.md:68` say what an assertion measures, nothing of a premise it
  must not carry; `agents/skill-grader.md:22-25` grades on what the files show, so a
  grader checks the premise against the fixture's files.
- **R1, the grader blind to the context each session started with.**
  `scripts/harness.py:288-308` (`render`) keeps only the `user` and `assistant` records
  (`:293`), so the `attachment` records, instruction files and hook context, are lost;
  `scripts/grade.py:324-334` copies the rendered files, and `agents/skill-grader.md:14-18`
  names `transcript.md` as the run's account.
- **R2, a workflow of several sessions.** A case holds one `prompt`
  (`references/eval-files.md:65`), and `scripts/run.py:323` (`execute`) starts one session
  per run under one ceiling; `references/evaluate.md:34-35` speaks of requests only, with
  no word on testing a later step from a fixture holding the state before it.
- **R3, misleading figures for a run with agents.** `scripts/harness.py:206-208` takes
  `duration_s` from the result's `duration_ms`. `scripts/run.py:285-312` (`counted`)
  settles the reported output over the agents' calls with `usage.settle`
  (`shared/usage/usage.py:683-703`), which shares it by the calls' equal estimates and
  keeps each call marked estimated; `run.json`'s `agents` carries no mark of it.
  `scripts/benchmark.py:142` counts a run with estimated calls and `:330-333` writes the
  footnote of estimated output without reading `output_source`; `:237-241` reports every
  effort other than the iteration's as a deviation, the efforts a skill gives its agents
  included.
- **R4, every assertion told to discriminate.** `references/evaluate.md:101-102` and
  `scripts/benchmark.py:216-218`, which notes an assertion with one result everywhere,
  a guard included, and groups failures of different causes as one.
- **R5, an assertion over a list failing whole.** An assertion is a sentence
  (`references/eval-files.md:68`) and its result a boolean (`eval-files.md:199`,
  `agents/skill-grader.md:22-25`): no count, no item-by-item result, and no step that
  classes a failure (V2's lines).
- **R6, a rule from a study with no place as evidence.** The lines of V5, which the
  auditor's first pass on ai-ctl's skill applied to the verifier's "Do not invent a
  defense", cut since.

The user read the map and approved it; task 1 ticked.

Task 2: the lines both skills carry because of the validation, the cases Phase 4 replays,
from both notes' lists and their problems' sections, each found in the skill's files.
`close-session`, in `domains/session/skills/close-session/`, unchanged since `65ca91f`:

1. `SKILL.md:97-98`, the Result's last sentence, "When none does, say nothing of what the
   next start will show": V1, written for a world only the harness produces.
2. `SKILL.md:95-97`, the Result's condition, "or nothing when a line at the top of this
   session's context names open resume notes", reworded across iterations 3 to 10 (V1),
   and its citation of `docs/decisions/2026-10-13-session-close.md` (V4).
3. `SKILL.md:9`, the opening's citation of the same decision record: V4.
4. `SKILL.md:21`, step 1's citation of the roadmap skill's `references/report.md`: V4, and
   `audit.py`'s rule R2 refusing a skill-local path to another skill's file.
5. Three cuts. The prohibition on `git add -A`, `git add .` and `git commit -a`, and
   "Write no decision record", cut by `4dc28ce` though the study of real transcripts
   called for both: V5. The commit message's form, cut by `65ca91f` under the auditor's
   content judgment, though case 2 keeps its assertion (`evals/evals.json:42`): V3, a
   point no judgment weighed against the evals.
6. Case 3's four `failures_with_skill` entries (`evals/evals.json:88-91`), written partly
   so that the auditor reads why the Result explains no hook: V1 and V3.
7. Case 3's ninth assertion (`evals/evals.json:78`), "The answer claims nothing of what
   the next session's start will show … no line at this session's start named an open
   note", added after iteration 2: V1, it penalizes trusting the configuration, and V6,
   its premise re-derived wrongly by two graders.

`reviewing-delivered-code`, in ai-ctl's `.claude/skills/reviewing-delivered-code/`. The
note found its changes uncommitted; ai-ctl has committed them since, `7445f39` and
`243717f`, and its tree is clean:

1. "Claims hold"'s clause on the files the harness loads, in both cases: R1. Already
   reverted at `243717f`, as ai-ctl's Phase 3 report records; Phase 4 replays the
   assertion as it stood before.
2. Three citations of ai-ctl's phase reports in `SKILL.md`, which the fixture keeps out
   of every run: step 3's mutants probe (`:52-54`), step 4's rates (`:88-93`) and step 4's
   $20 window (`:95-97`): V4 and R6.
3. Step 4's rates (`SKILL.md:81-93`), recalibrated from per-agent costs whose output share
   is set by call count: R3; to measure again once the figures are exact.
4. The v2 case's partial observation and its manual continuation, the first decision of
   ai-ctl's Phase 3 report: R2.
5. Three cuts drawn from the study of review plugins rather than from runs: the verifier's
   "Do not invent a defense", on the auditor's first pass, and the report's list of
   refuted findings and the reviewers started in one message, by the rule of what the runs
   showed. Made before the skill's first commit, they survive only in ai-ctl's Phase 2
   report (`phase-2-skill-build-report.md:102-117`): R6 and V5.

Left off the list, as both notes say they stand on failures in use: ai-ctl's merge of
findings before verification and `review-tests`' step 4, and the rewording of ai-ctl's
defect 8, an assertion defect fixed in the assertion alone.

The user read the list and approved it; task 2 ticked.

---

## Decisions

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
