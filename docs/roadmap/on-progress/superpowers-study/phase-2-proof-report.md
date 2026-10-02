# Phase 2 Report: Proof

**Phase:** [phase-2-proof.md](phase-2-proof.md)
**Start Commit:** d3c5420

---

## Work Log

### 2026-10-02

Opened the phase from Phase 1's closure, committed as `d3c5420`. Read Phase 1's file and
its report in full: no restructuring pending, and no other phase in progress. What binds
this phase: the matrix format and the five rules of evidence of the draft record; the
constraint Phase 1 added, a proof a task declares being one the execution operation can
run and record before ticking the task (EP18), and the reviewer agent taking the parts of
`code-reviewer.md` this phase keeps; the method question of `study/methods.md` (WP9). At
the user's rule, the opening ends the turn: no work on the phase yet.

The user started the work. Read the five skills and their companion files in full, and
their changes since 6.3.0: the whole-suite paragraph of `test-driven-development`, the
"vision document" and "Declined to judge" sections of `code-reviewer.md`. Found in the
transcripts, counted once per `tool_use` id, four distinct calls in all: three to
`test-driven-development`, one to `systematic-debugging`, none to the other three skills.
Read what followed each. The two own calls to `test-driven-development` enforced the RED
step — a stub turned errors into failures, and a test that passed at once was rewritten
until it reproduced the real case — and one of them mutated its code with `sed` to show
that its tests caught the change, a practice of the companion file that nobody read: no
call opened a companion file. The `systematic-debugging` call set aside two plausible
causes on evidence and measured the real one before any change; the bug fixed earlier in
the same session without a skill had its test written after the fix. The third
`test-driven-development` call, the cascade of 2026-09-27, added nothing to a plan that
already ordered RED and GREEN (review 09-27).

For the review skills, read the final reviewer runs in the subagent transcripts: four ran
to their end, and each found one to three issues to fix before the merge, three of them
after every task had passed its own review; two were cut by a limit. Read the four tool
reviews of `roadmap-auditor`: four PASS, no defect found, a median of 77,910 fresh tokens.
The release notes hold the plugin's own measures — the rebuttals of
`test-driven-development` holding test-first at 8/10 against 5/10 without them, sessions
running only the named test file in 11 of 12 probes — cited as measured by the plugin.

Wrote the five matrices into the draft record under Proof, with a table of the four calls
and one of the final reviews so that the evidence outlives the transcripts: 79 rows, 21
kept, 36 improved, 20 dropped, 2 open. TD13, the rationalization table, waits for task 4,
which can measure it under pressure; RC10 goes to Phase 3. Every destination of
`test-driven-development`, `verification-before-completion` and `systematic-debugging`
stays `open` until task 5 places the proof; the review rows go to the reviewer agent and
the execution operation that Phase 1 decided. Checked the cited release-note lines before
moving on: one pointed at the wrong bullet, and one observation claimed a whole-suite run
for a call where none was seen; both fixed.

Designed task 4's micro-tests by the method of row W22, as the flowcharts were measured
on 2026-09-28: one headless session per sample, no tools, no settings, no skills, from an
empty directory, the system prompt a role line plus one form of guidance; the agent lists
the actions it would take, and every answer is read and classified. Four forms: none;
plain, this repository's "write a failing test, watch it fail, then the code"; catalogue,
the five proof kinds defined and the agent choosing one; declared, the same definitions
and the task's own `Proof:` line. Five scenarios, one per kind, each built on a real case
of this setup — a script's exit code (test), the closure's silence on uncommitted work
(eval), `allowed-tools` taken on the documentation's word (probe), a `.gitignore` line
(check), the naming of two agents (review) — and a sixth, the code task under the user's
haste, where a fifth form adds three rows of TD13's rationalizations, so the measure
also rules on TD13. 24 cells, 6 samples each: 144 sessions on Claude Haiku 4.5, the
script in the session's scratchpad, printing the count before it starts. Not run yet: it
waits for the user's go-ahead.

The user chose to run it on Claude Haiku 4.5 and on Claude Sonnet 5.5: 288 sessions,
started once the script had printed their count, no error, $1.06 and $3.34. The first six
answers checked the harness before the rest ran: Haiku had run, isolated. A defect of the
script was fixed on the way — a sample saved in error would have been kept on a rerun
instead of retried; no sample erred. In the Sonnet runs, Haiku answered one side call of
the harness, ~16 output tokens a session, so the plans are Sonnet's. Read and labelled
every answer: the labels for the platform, configuration and naming scenarios had to be
refined on the first answers, since plans rarely say whether a run is a real headless
session and the naming answers had shapes the rubric had not foreseen; the record says
how.

What came out: for code, a plain test-first instruction and a declared `test` do the same,
and both hold under the user's haste, where Sonnet without guidance wrote all six tests
after the fix. Elsewhere the plain instruction turned every non-code task of Sonnet into a
new test, mostly of text, and halved its real tries of the platform. A declared proof
brought the right method for `eval`, `test` and `review` on both models, `probe` on
Sonnet only, and `check` drifted to `make check` when no command was named. The catalogue
was enough for Sonnet but for the naming decision, which it took itself; Haiku, choosing,
took the cheapest proof. `review` came after the files were written. Wrote the measure
into the draft record under Proof Per Task, and ruled TD13: dropped, the three rows
adding nothing to a declared proof under haste.

Drew task 5's design from the measure and put it to the user: the five kinds, each
declaration naming its object — the behavior, the scenario, the mechanism, the command,
the decision — since `check` without its command drifted; `probe` tried before the change
with a control, and `review` asked before the work it decides, since both came late
otherwise; the declaration on an indented `Proof:` line under its task; no
`.agent-conventions.toml` key for now, a default kind without its object being what
drifted; the `test` proof running the contract's `checks` as its suite; no `task-done`
script, three kinds of five not being commands.

The user approved the design as proposed: the indented `Proof:` line, no default key,
the `CLAUDE.md` line "TDD (failing test first)" left to Phase 4, the rest as written.
Asked where the kept rows of `systematic-debugging` go, since both observed bugs came in
the chat, outside any roadmap: the user chose a skill of its own. Wrote the decisions
into the draft record, filled the destinations — a proof reference, the reviewer agent,
the execution operation, the debugging skill — and dropped TD1 and VC1, whose
descriptions the declared proof makes moot. Settled the four rows of Phase 1 that waited
for this phase: WP9, EP12, EP17 and EP18. Carried a task and a constraint into Phase 4
and a constraint into Phase 3. Copied the micro-test script, its answers and labels from
the session's scratchpad to `study/proof-micro-tests/`, which git ignores, so that the
measure outlives the session. The user asked to close the phase; `make check` passed.

---

## Decisions

- **A task declares its proof, and the declaration names its object** (the user,
  2026-10-02): `test: <the behavior>`, `eval: <the scenario>`, `probe: <the mechanism>`,
  `check: <the command>`, `review: <the decision>`, each defined in the draft record.
  The object is required because `check` without its command drifted to the repository's
  suite in the micro-tests; `probe` and `review` say "before" because both came late
  otherwise. The roadmap skill's phase template and its execution operation carry them.
- **The declaration is an indented `Proof:` line under each task,** proposed by the agent
  writing the phase and approved by the user with the phase (the user, 2026-10-02).
  Bounded work outside a roadmap states its proof in the design `shaping-work` gets
  approved.
- **The execution operation runs the declared proof, records it in the Work Log, then
  ticks the task; no `task-done` script** (the user, 2026-10-02): three kinds of five are
  not commands. The reviewer agent checks that each proof ran and proves its claim.
- **No key in `.agent-conventions.toml` for now** (the user, 2026-10-02): a default kind
  carries no object; the `test` proof's suite is the contract's `checks`. To revisit if
  declarations go wrong in use.
- **No method chosen from a catalogue** (the user, 2026-10-02): the methods of
  `study/methods.md` land as proofs — test-driven development as `test`, acceptance and
  behavior scenarios as `eval`, a spike as `probe` — which settles row WP9 but for its
  commit granularity, Phase 3's.
- **Debugging goes to a skill of its own** (the user, 2026-10-02), from the kept rows of
  `systematic-debugging`; Phase 4 names it with the operation and the agents.
- **The `CLAUDE.md` line "TDD (failing test first)" is scoped by Phase 4** (the user,
  2026-10-02): the micro-tests found that plain instruction harmful outside code.
- **TD13, the rationalization table, is dropped** on the measure: under the user's haste,
  a declared `test` held 12 times out of 12, and three of its rows added nothing. An
  explicit "tests after" from the user is the user's to give.
- **The five kinds are defined once, in a proof reference** read by the execution
  operation and by `shaping-work`. Phase 4 places it; `shared/` is how this repository
  gives two skills one source.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/superpowers-study/phase-2-proof-report.md` — created at the
  opening, committed with it in `d2471be`

**Modified**
- `docs/decisions/2026-10-01-superpowers-study.md`
- `docs/roadmap/on-progress/superpowers-study/README.md` — the opening's edits, committed
  in `d2471be`, then this closure's
- `docs/roadmap/on-progress/superpowers-study/phase-2-proof.md` — the opening's status,
  committed in `d2471be`, then the work and the closure
- `docs/roadmap/on-progress/superpowers-study/phase-3-git.md`
- `docs/roadmap/on-progress/superpowers-study/phase-4-decisions.md`

Outside the diff: `study/proof-micro-tests/`, the micro-test script with its 288 answers
and their labels, which git ignores.

---

## Problems And Deviations

- **The micro-tests measure plans, not actions.** The agents said what they would do;
  what they do with tools may differ. The plugin's own measure of the rationalization
  table came from runs. Left as a limit of the record; an eval of the execution operation,
  once built, measures the actions.
- **The labels were refined on the first answers** of three scenarios, where the rubric
  fixed beforehand could not classify them: platform runs whose real or simulated nature
  plans rarely state, configuration checks that split git from re-reading and the suite,
  naming answers that asked leave to explore or handed over after writing. The record
  states each refinement.
- **The naming scenario was weak on Haiku:** set in a Python repository, it was read as
  Python classes, and two to four answers per form only asked leave to explore. Its
  Sonnet answers carry the finding.
- **Task 4 ran on two models instead of one,** at the user's choice: 288 sessions and
  $4.40 rather than the 144 and about $0.60 first proposed. A defect of the script — a
  sample saved in error would have been kept on a rerun — was fixed before any sample
  erred.
- **The hypothesis held with two exceptions,** which shaped the design rather than
  sinking it: a declared `probe` did not make Haiku try the mechanism first, and a
  declared `check` without its command drifted to the repository's suite.
- **The first count of verdicts changed:** 21 kept, 36 improved, 20 dropped and 2 open
  became 21, 34, 23 and 1 once task 4 dropped TD13 and task 5 dropped TD1 and VC1. Four
  rows of Phase 1 — WP9, EP12, EP17, EP18 — were settled by this phase's decisions.
- **The phase file's "testing anti-patterns file"** is `writing-good-tests.md`, its name
  since `testing-anti-patterns.md` was rebuilt (`RELEASE-NOTES.md:114`); ruled as such.

---

## Changes To Later Phases

- `phase-3-git.md`: added a constraint — row RC10, replies in a forge's review threads, is
  ruled with the pull-request capabilities of `finishing-a-development-branch`.
- `phase-4-decisions.md`: added the task "Scope this repository's `CLAUDE.md` line 'TDD
  (failing test first)' to the artifacts it fits", at the user's decision of 2026-10-02.
- `phase-4-decisions.md`: added a constraint — the follow-up roadmaps carry Phase 2's
  decisions: the `Proof:` line in the phase template, one proof reference, the reviewer
  agent's criteria from rows RQ12 to RQ18, and a debugging skill named in Phase 4.

No restructuring is pending.

---

## Assessment

The phase ruled on the five skills that prove work done — 79 rows in the draft record,
21 kept, 34 improved, 23 dropped, 1 left to Phase 3 — and replaced their method with
one decided with the user: each task declares its proof, naming its object, among five
kinds, on a `Proof:` line the execution operation runs and records before ticking.

Its strongest evidence came from 288 micro-test sessions on two models. A plain
test-first instruction works for code and does harm elsewhere: on Sonnet it turned every
skill, platform, configuration and naming task into a new test, mostly of text. A
declared proof brought each artifact its method, provided it names what it runs. The
transcripts showed the skills serving only when the agent called them itself, their
companion files never read, and every final review that ran to its end finding something
to fix — three of them after per-task reviews had passed.

What Phase 3 needs to know first: a task's commit, if the `[git]` table commits per
task, comes after its declared proof passed and was recorded; row RC10 waits for its
pull-request rows; and the micro-test script of this phase is kept, with its prompts,
answers and labels, in `study/proof-micro-tests/`, for any wording Phase 3 measures.
