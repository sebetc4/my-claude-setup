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

Tasks 3 and 4, the measures, announced together and started on the user's yes, about
$2.40 expected:

- `skill-auditor`: six passes on `close-session`, whose tree is unchanged since `65ca91f`,
  as are the writing guide and the agent since the fourteen passes of 2026-10-13. Each
  pass started as a subagent, as `references/audit.md` starts it and as those fourteen
  ran, all six at once, with the same request: the skill's folder, the installed writing
  guide's path, and `audit.py`'s output, "0 errors, 0 warnings". Announced at $0.11 a
  pass, the cost measured on 2026-10-13, about $0.66, with no ceiling: a subagent takes
  none. The agent's frontmatter sets Sonnet and no effort.
- `skill-grader`: six runs graded again three times each, eighteen sessions at Sonnet
  `xhigh` by `grade.py`: the two failed runs, iteration 10's run 3 and iteration 11's
  run 1 of case 3, and four passed runs, run 1 of each case in iteration 10 and run 2 of
  case 3 in iteration 11. Three copies of both iterations under the ignored
  `.eval-runs/skills/close-session/spread/grader-1` to `grader-3`, each with the sampled
  runs' `grading.json` removed, the originals untouched. Announced at $1.74, $0.10 a
  session, the mean of these iterations' gradings, under `grade.py`'s ceiling of $1 a
  session, $18 at most.

The six auditor passes all answered `VERDICT: FAIL`, and every point but one fell on
`references/conventions.md`, the copy of `shared/conventions/`. Points by the number of
passes that raised them:

| Point | Judgment | Passes |
|---|---|---|
| The Keys and Where To Look tables carry the keys of other tools' tables | content | 6 of 6 |
| The old contract's candidate "mapped key by key by the skill's own reference" names a reference close-session lacks | content | 3 of 6 |
| "never as one the user already approved", for `checks`, answers no failure | form | 2 of 6 |
| "tool" and "skill" both name the table's owner | terminology | 2 of 6 |
| `start_notes`' default and "Python older than 3.11" stated without a source | content | 1 of 6 |
| `references/resume-note.md`: "resume notes' folder", "the folder" and "`notes`" for one thing | terminology | 1 of 6 |

Two passes cite lines past the end of the 95-line file (`:103` to `:176`). Each pass made
4 calls, all on Sonnet at `medium`: the effort the harness gives a subagent whose
frontmatter sets none, where the session runs at `xhigh`. Their cost, read as
`shared/usage/usage.py`'s `session` reads a session's runs, each run's last call completed
from the Agent result's usage: $0.10, $0.08, $0.05, $0.09, $0.07 and $0.10, $0.50 in all,
of which at most $0.014 a pass is estimated output. A first reading with `usage.calls` on
each transcript alone gave $1.26, counting every call without a final usage at 5,400
tokens of output; it is not the figure.

The six passes ran on the request `references/audit.md` gives, not on the one the passes
of 2026-10-13 had. That session's transcript holds sixteen calls of `skill-auditor` on
close-session, where the note counts fourteen. From the second on, the request added a
section "Context the files do not hold". It said that `references/conventions.md` is a
shared copy whose other keys cannot be cut, asking to "judge whether the skill needs the
page, not its content beyond the skill's use". It also gave the source of the
`## Steps` and `## Result` headings, what "my-agent-setup `<path>`" means, and where the
runs lie. The two passes that approved `65ca91f` had that request. So the measure does
not compare with them: on the same text, the bare request fails on what the context had
set aside. What the caller adds to the request is an input of the verdict, not
recorded anywhere but in the session's transcript.

On the user's yes, a second series: six passes with the request of the last pair of
2026-10-13, word for word, $0.66 announced. All six answered `VERDICT: PASS`, with no
point; 3 or 4 calls each on Sonnet at `medium`, $0.08, $0.09, $0.09, $0.10, $0.08 and
$0.09, $0.53 in all. Two passes say they did not open the runs the request offers.

The sixteen passes of 2026-10-13 then read again from that session's transcript and
its subagents', each with its request:

| Time (UTC) | Request | Verdicts | Points |
|---|---|---|---|
| 18:33 | 1 | FAIL | 3 |
| 18:48 | 2 | FAIL | 4 |
| 19:08, pair | 3 | FAIL, FAIL | 3 and 6, none shared |
| 19:15, pair | 4 | FAIL, FAIL | 1 and 1, not the same |
| 19:23, pair | 4 | PASS, PASS | — |
| 19:31, pair | 5 | FAIL, FAIL | 2, and 2 or more, none shared |
| 19:38, pair | 6 | FAIL, FAIL | 2 and 1, one shared |
| 19:42, pair | 6 | FAIL, FAIL | 1 and 1, the same: the Result's condition without a source |
| 19:44, pair | 7 | PASS, PASS | — |

Seven requests for sixteen passes; between pairs the text changed too. Two passes
started together, on one request and one text, always gave the same verdict, and every
change of verdict came with a change of the request, of the text, or both. With the
twelve passes of this phase, no verdict changed across 26 passes on a text and request
held fixed. What changes from one pass to the next is the list of points: on the bare
request, one point in all six passes and five raised by one to three; on 2026-10-13, two
FAIL of one point each, not the same point. V3, read again: the verdict follows the text
and the request, which no file holds, and an open search draws different points on each
pass.

The eighteen gradings, all `complete`, cost $1.78, $0.08 to $0.12 a session. Over the six
runs, each assertion now has four readings, the first grading and three again:

| Run | Passed, four readings | Assertions whose verdict changed |
|---|---|---|
| Iteration 10, case 1, run 1 | 9, 9, 9, 9 of 9 | none |
| Iteration 10, case 2, run 1 | 9, 9, 9, 9 of 9 | none |
| Iteration 10, case 3, run 1 | 9, 9, 9, 9 of 9 | none |
| Iteration 10, case 3, run 3 | 8, 8, 8, 8 of 9 | none: assertion 4, Parquet under Decided, failed four times |
| Iteration 11, case 3, run 1 | 8, 8, 8, 9 of 9 | assertion 9: failed, failed, failed, passed |
| Iteration 11, case 3, run 2 | 9, 9, 9, 9 of 9 | none |

One verdict in 54 changed: assertion 9, on "Pour reprendre, il suffit de dire « … »".
Three readings failed it, each re-deriving the premise from the absent `start_notes`, as
V6 says; the fourth passed it as "a borderline pass", reading the words as what the user
types. Weak flags: one reading of 24 named four assertions weak, all four absences in
case 1 (no `git commit`, task 2 unticked, nothing under `.agent-memory/` or `notes/`), as
a run that wrote nothing would pass them; the three other readings of that run named
none. These are R4's guards, which a reading flags or not.

Tasks 3 and 4 ticked. The measures cost $2.81: the auditor's twelve passes $1.03, the
grader's eighteen sessions $1.78, against $3.06 announced in two steps.

Task 5: read the four later phase files, their tasks and proofs, and the session
domain's `hooks.json`, then wrote the design in the phase file's `## Design`, proposed
for the user's approval. Checked while writing: the sixteen passes of 2026-10-13 also
ran at `medium`, 64 calls for $1.55, so every measured pass did.

The user approved the design as written, "the runs and the next uses will tell whether
the reading is right"; task 5 ticked.

Task 6: proposed the memory's new application line. Asked what "a FAIL whose lines are
all answered never counts" means, explained the rule of 2026-10-13: answering a FAIL's
points is no PASS, a new pass must answer PASS. The user then set two points: asking for
a PASS at any cost was not the answer and degraded the tool, but no FAIL is legitimate —
it is a defect of the skill audited or of the validator, never accepted; and writing
that the validator can be wrong risks a fragile rule and a way out, so the agent must
first answer the problem in the skill before declaring an instrument at fault. Proposed
and approved: no failure or point stands, each ending in a fix and a run or pass that
succeeds; `skill` as the default class, an instrument's class only on the evidence its
row lists, produced by the tools, and on the user's yes; fixing an instrument never
validating the skill; for an auditor's point, a wording of the skill first, the evals
run on it, the auditor at fault only on a regression they show; the procedure stating
the classes as conditions, with nothing more general about the instruments, the reasons
in the decision record; the share of instrument classes shown per iteration, raised with
the user past one in four. The design amended accordingly: No Failure Stands, A
Failure's Class, The Auditor's Verdict, What Is Left Open; the `tool` class, which set a
failure aside, now fixes the tool and judges the runs again.

The memory `skill-auditor-pass-required` rewritten in the same sense: its Why gains the
measures and the user's words of the day, its How to apply the fixed request and two
passes, a wording of the skill first, the auditor at fault only on the evidence listed
and the user's yes, never a rewording of the skill to satisfy a point the evals
contradict. The user read it and approved it; task 6 ticked.

Task 7: wrote `docs/decisions/2026-10-14-skill-validation.md`, after the form of
`2026-10-13-eval-runs-with-agents.md`: the problems by family, the measures, the
decisions with their reasons — among them why the procedure names the instruments'
defects only as conditions —, what is not done, and when to revisit. `make check`
passing; task 7 ticked, every task of the phase done.

---

## Decisions

- **The update fixes the instruments' inputs and judgments rather than adding passes.**
  The auditor gave the same verdict across 26 passes on a text and request held fixed,
  and the grader changed one verdict in 54; what moved the verdicts was the request, the
  text, and premises inside assertions. Phases 1 to 3 build the design of
  `phase-0-framing.md`, approved by the user on 2026-10-14.
- **A case's world comes from the domain's real hooks**, installed as project hooks in
  the run's folder by a `hooks` key, and turned off by a fixture's configuration. Phase 1
  probes that a project SessionStart hook reaches a `claude -p` session first.
- **A workflow's later step is tested from a fixture holding its intermediate state**;
  a sequence of sessions in one case waits for a hand-off that fails in use.
- **No failure and no auditor point stands** (the user, amending the design): each is a
  defect of the skill or of an instrument and ends in a fix, then a run or pass that
  succeeds; fixing an instrument never validates the skill.
- **Each failure of the skill's arm gets one of six classes** — `skill` and `variance`,
  the skill's; `grader`, `assertion`, `world` and `tool`, an instrument's — in the
  iteration's `classes.json`, with a second grading of the failed assertions alone.
  `skill` is the default; an instrument's class needs the evidence its row lists,
  produced by the tools, and the user's yes. The procedure states the classes as these
  conditions and nothing more general about the instruments; the share of instrument
  classes is shown per iteration and raised with the user past one in four. Phase 2
  builds it, and Phase 4 classes the two skills' recorded failures with it.
- **The criterion**: a guard with no failure classed `skill` or `variance`; a check with
  none classed `skill` and 80% or more over five runs or more of one snapshot; a list
  read item by item. Revisited after Phase 4.
- **The auditor's verdict**: a request fixed word for word, its context in the skill's
  `evals/`; `effort: medium` in its frontmatter; two passes started together, PASS when
  both pass; each point answered by a wording of the skill first, the auditor at fault
  only on a regression the evals show, then fixed in the auditor on the user's yes. The
  user's rule stands: a FAIL whose lines are answered never counts.
- **Sources go to `evals/sources.md`**; a fact the agent observes in its own context
  needs none. **Failures seen in use go to `failures_in_use`**, with their source, and
  ground a prohibition; a study's practice that answers no failure does not.

---

## Files Changed

**Added**

- `docs/decisions/2026-10-14-skill-validation.md`
- `docs/roadmap/on-progress/skill-validation/phase-0-framing-report.md`
- `docs/roadmap/on-progress/skill-validation/phase-0-framing.md` — the phase file, moved
  with the folder and grown by its `## Design`: git pairs no rename with it, and lists
  its old path under Deleted

**Modified**

- `docs/roadmap/README.md`

**Deleted**

- `docs/roadmap/pending/skill-validation/phase-0-framing.md` — the same file's old path,
  see Added

**Renamed**

- `docs/roadmap/pending/skill-validation/README.md` → `docs/roadmap/on-progress/skill-validation/README.md`
- `docs/roadmap/pending/skill-validation/phase-1-run-world.md` → `docs/roadmap/on-progress/skill-validation/phase-1-run-world.md`
- `docs/roadmap/pending/skill-validation/phase-2-judgments.md` → `docs/roadmap/on-progress/skill-validation/phase-2-judgments.md`
- `docs/roadmap/pending/skill-validation/phase-3-evidence-and-sources.md` → `docs/roadmap/on-progress/skill-validation/phase-3-evidence-and-sources.md`
- `docs/roadmap/pending/skill-validation/phase-4-validation-and-release.md` → `docs/roadmap/on-progress/skill-validation/phase-4-validation-and-release.md`

---

## Problems And Deviations

- **The first auditor series ran on another request than the passes it was to check.**
  It followed `references/audit.md` to the letter, where the passes of 2026-10-13 had a
  free-text context; found after its six FAIL. Consequence: a second series of six on
  the earlier request, announced and approved, $0.53; the two series together showed
  the request to be an input of the verdict, now in the design.
- **A cost first misread.** The first series' cost was computed with `usage.calls` on
  each subagent's transcript alone, $1.26, every call without a final usage counted at
  5,400 tokens of output; read again as `usage.session` reads a session's runs, $0.50.
  Corrected in the Work Log before the commit.
- **The feedback notes' figures differ from the transcripts in two places**: the
  2026-10-13 session holds sixteen auditor passes where the close-session note counts
  fourteen, twelve FAIL and four PASS; and ai-ctl committed the changes its note calls
  uncommitted (`7445f39`, `243717f`), the "Claims hold" clause already reverted. Both
  recorded where they were found; the notes, ignored and written by their sessions,
  are left as they are.
- No task moved, every acceptance criterion holds.

---

## Changes To Later Phases

- `phase-1-run-world.md`, Cases: the first task names the `hooks` key the design chose,
  the domain's hooks installed as project hooks, in place of "the context a hook would
  inject"; its proof names a case with a SessionStart hook and the probe of a project
  SessionStart hook under the harness's flags.
- `phase-2-judgments.md`, Failures: the first task names the six classes, `skill` by
  default, an instrument's class on its evidence and the user's yes, `grade.py --again`,
  `classes.json` and the share of instrument classes per iteration, its proof a class
  without its evidence refused; the second states the step as the classes' conditions
  and drops "check the assertion before the skill" from Reading A Benchmark.
- `phase-2-judgments.md`, Auditor: the task names the fixed request, `effort: medium`,
  two passes, the skill answering a point first, the auditor at fault only on the
  evidence listed and the user's yes, and line numbers from a numbered read; its proof
  sets the threshold, twelve passes or more on `65ca91f`, every verdict the same.
- No restructuring.

---

## Assessment

The phase settled the update from measures rather than from the notes alone, and the
measures changed the reading of the problems. The instruments are stable at fixed
inputs: no auditor verdict changed across 26 passes on a text and request held fixed,
and the grader changed one verdict in 54, on an assertion carrying a premise. What
moved the validation was what no file held: the request the caller writes, the world a
run meets, the premises inside assertions, the effort the auditor runs at. The design
fixes those inputs, and, after the user's two points, makes every failure end in a fix,
the skill's by default, an instrument blamed only on evidence the tools produce and
the user's yes. `docs/decisions/2026-10-14-skill-validation.md` holds the reasons, which
the procedure itself will not state.

What Phase 1 needs first: the probe that a project SessionStart hook's output reaches a
`claude -p` session under the harness's flags (`--setting-sources project,local`, the
guard through `--settings`), since the `hooks` key rests on it; then the design's A
Case's World, section by section. The paths of the map in this report's Work Log give
each change's starting line. Nothing in `close-session` or ai-ctl changes before Phase
4.
