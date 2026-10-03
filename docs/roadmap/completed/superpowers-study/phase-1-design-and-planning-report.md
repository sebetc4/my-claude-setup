# Phase 1 Report: Design And Planning

**Phase:** [phase-1-design-and-planning.md](phase-1-design-and-planning.md)
**Start Commit:** 7c95fb0

---

## Work Log

### 2026-10-01

Opened the phase from Phase 0's closure, committed as `7c95fb0`. Read Phase 0's file and
its report in full: no restructuring pending, and no other phase in progress. What binds
this phase: the matrix format of the draft record — five columns with `Goes to`, row ids
BR, WP, EP, SD and DP for its five skills — and the five rules of evidence; the deadline
on the plugin's 2026-09 sessions, which go from about 2026-10-10; and the two mapping
tasks, which need the user's approval. The `.gitignore` change of the user, predating
Phase 0, is still uncommitted.

At the user's request, committed everything left: the `.gitignore` change on its own,
then this opening.

Started on `brainstorming` with the transcripts, as the deadline asks. Summarizing each
call showed one request in six transcripts with identical figures: a resumed or forked
session copies the history it continues, under a new `sessionId`, often with new `uuid`s,
sometimes with new timestamps; only the `tool_use` ids and the assistant `message.id`s
survive. Counted once per `tool_use` id, the baseline's 51 calls are 29 — `brainstorming`
10, not 16. Grouped into conversations by shared `message.id`, Phase 0's baseline becomes
32 working conversations, not 41 sessions: 11 (34 %) with a superpowers call, 24 (75 %)
with a call to any skill. Corrected the draft record's method and baseline, this phase's
overview and constraint, and the agent's memory; Phase 0's report and the README's 1.1.0
entry keep the figures they were written with.

Read what followed each of the 13 distinct `brainstorming` calls, and the user's review of
2026-09-27, which followed a whole 6.4.1 chain. Two outcomes the first summary missed came
from Bash heredocs: the 2026-09-10 EPUB spec, the only one in the default
`docs/superpowers/specs/`, and the scriptorium session-review roadmap. Five designs ended
in a roadmap, six in `writing-plans`, two in direct implementation; the class was
announced in 9 calls; the visual companion was never offered. Wrote the `brainstorming`
matrix, 20 rows, with a table of the 13 calls so that the evidence outlives the
transcripts: 9 kept, 5 improved, 6 dropped, every destination `open` until task 4. A
first draft credited the write-back of understanding with the corrections that review
09-27 credits to one question at a time; fixed before moving on.

For `writing-plans` and `executing-plans`, read the 9 distinct calls and set them against
the roadmap skill's phase template and report. The 2026-09-04 forma-rust call used
`executing-plans` to run a roadmap's phases one after another, closing each: in the
user's practice a plan is already a phase's task list. Review 09-27 gave both sides of
complete code in a plan: a transcription at execution, but the implementation written
twice. Wrote both matrices, 16 and 23 rows; checked that `task-brief` cuts a plan at its
`Task N` headings before saying so.

For `subagent-driven-development`, measured the four runs from their subagent
transcripts: the tiers asked are the tiers that ran, re-reviews came to about one for
every two tasks and stopped at round 2, no subagent called the Skill tool, and the
subagents alone cost 4.5 to 8.1 M fresh tokens a session against 146,559 for the inline
run of 2026-09-27. A first draft said fix rounds followed half the tasks; re-reviews count
rounds, not tasks, and the wording was fixed. Wrote the matrices of
`subagent-driven-development`, 26 rows, and `dispatching-parallel-agents`, 5 rows: the
latter goes as a skill, never invoked, its integration rule kept. The prose contract "no
subagents of your own" can become a worker's tool list, as `roadmap-auditor` has.

The three matrix tasks are done; tasks 4 and 5 go to the user as proposals.

The user approved a design skill of its own, in this setup's skill architecture, and
inline execution with delegation only on request; asked what the skill would add, what
`## Design` and the Review Focus are for, and where the figures 4.5 to 8 M against
147,000 came from. Answered with the sources and the limits: different plans, sizes and
pauses make it an order of magnitude, not a controlled measure. The user then approved
`## Design` in the phase file, citing a decision record when needed. Wrote the three
decisions into the draft record and filled its "Goes to" column, 71 rows: three stay
open, WP4 and WP9 for Phases 2 and 3, WP11 for the user's answer on the Review Focus.
EP7 and SD2 became improve and SD26 drop, as the decisions settle them. Ticked tasks 4 and
5, and wrote a review sheet in French for the user, outside the repository's tracked
files; at the user's request, detailed it row by row, each row linked to its line.

### 2026-10-02

The user reviewed the rows down to EP1: BR1 to BR5, BR7, BR9 and BR12 approved, BR8
confirmed as the point where this setup's tools take over; WP4 goes to the future git
convention, WP9 back to the method question of `study/methods.md` (Phase 2), WP11 becomes
conditional, written only when the need is really felt. The user asked for a clearer
name than `brainstorming`, its exact trigger, the types of approaches, whether an
architecture skill is needed, a definition of plan, spec and roadmap, and how execution
relates to opening a phase. Recorded WP4, WP9 and WP11 in the draft record; the other
points went back to the user as proposals.

The user then settled most of them: the skill's name comes from shaping, to avoid UI
design skills, and its trigger must not overlap the roadmap skill or the skills to come;
"spec" and "plan" leave this setup's vocabulary; the execution operation runs one phase,
closing a phase and opening the next ending the turn, never chaining phases, with commits
per the git convention; the review is conditional, the tool reviews weighing its value;
delegation stays light and is written into the roadmap; SD26 and DP1 are dropped. Asked
to settle the ledger scripts: EP15 `task-start` dropped, EP18 `task-done` kept as the rule
"a task is ticked only once its declared proof passed", its script waiting for Phase 2's
proof format; `task-brief` dropped, `review-package` kept. Amended 11 rows and the three
decisions in the draft record, and the French sheet to match.

The user named the skill `shaping-work`, and chose to close the phase with the row review
stopped at EP1, the record staying a draft until Phase 4. During the closure, the user
corrected a wording: the git convention is not "less strict" on branches, it follows the
repository's `[git]` table, everything on `main` or branches; fixed in row EP9 and in the
sheet. `make check` passed; carried Phase 1's decisions into Phases 2, 3 and 4 as
constraints.

---

## Decisions

- **Calls count once per `tool_use` id, and transcripts that share an assistant
  `message.id` form one conversation.** Copies carried 22 of the baseline's 51 calls.
  Phase 4's recount and every usage figure of this study follow the rule.
- **Design work goes to a skill of its own, built in this setup's skill architecture**
  (the user, 2026-10-01). The user added that any kept capability may become a new
  skill, agent or hook, and any of them may be reworded: the aim is this setup's own
  architecture and workflow.
- **A phase's design lives in a `## Design` section of its phase file, which cites a
  decision record when the section is not enough** (the user, 2026-10-01: the two
  complement each other). A roadmap's design stays in its README, the plan is the phase's
  tasks with detail per task when the phase calls for it, lasting decisions go to
  `docs/decisions/`, bounded work stays in the chat. A Review Focus section in the phase
  file is written only when the need is really felt (the user, 2026-10-02).
- **The roadmap skill gains an operation that executes a phase inline, task by task in
  order; delegation only on request** (the user, 2026-10-01: tasks are meant to run in
  chronological order, so delegation by default does not fit).
- **The execution operation runs one phase and stops at its boundary** (the user,
  2026-10-02): closing a phase and opening the next ends the turn, with no phase chained;
  commits come at each task's end or at the closure, and work stays on `main` or goes to
  branches, as the repository's `[git]` convention says (Phase 3). The reviewer agent is conditional; delegation stays light — one implementer, one
  reviewer, one fix round — and a phase that needs it says so in the roadmap.
- **The design skill is named `shaping-work`** (the user, 2026-10-02), on the model of
  `authoring-skills`, clear of UI design skills; the operation and the agents are named
  in Phase 4.
- **The ledger scripts are settled** (asked of the agent by the user, 2026-10-02):
  `task-start` and `task-brief` go; `task-done` survives as a rule, a task ticked only once
  its declared proof passed, with a script only if Phase 2's proof format allows it;
  `review-package` stays for the reviewer.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/superpowers-study/phase-1-design-and-planning-report.md` —
  created at the opening, committed with it in `1edc3fe`

**Modified**
- `.gitignore` — the user's change of before Phase 0, committed on its own during this
  phase in `4fbaa5b`, at the user's request
- `docs/decisions/2026-10-01-superpowers-study.md`
- `docs/roadmap/on-progress/superpowers-study/README.md`
- `docs/roadmap/on-progress/superpowers-study/phase-1-design-and-planning.md`
- `docs/roadmap/on-progress/superpowers-study/phase-2-proof.md`
- `docs/roadmap/on-progress/superpowers-study/phase-3-git.md`
- `docs/roadmap/on-progress/superpowers-study/phase-4-decisions.md`

Outside the diff: the French review sheet
`local-review/2026-10-01-superpowers-study-relecture.md`, which git ignores, and the
agent's memory, outside the repository, corrected on the copies in transcripts.

---

## Problems And Deviations

- **Phase 0's baseline counted copies.** Its 41 sessions and 41 % counted transcripts, and
  the 2026-09-18 record's 51 calls include 22 copies. Fixed in the draft record, this
  phase's file and the memory; Phase 0's frozen report and the README's 1.1.0 changelog
  entry keep the old figures, which this phase's changelog entry corrects.
- **The user's review of the matrix stopped at EP1.** The later rows stand as the agent's
  verdicts; the user chose to close all the same (2026-10-02), the record staying a draft
  until Phase 4 reads the whole matrix again.
- **Two first drafts misread their evidence**: BR2 took the credit review 09-27 gives to
  one question at a time, and the fix rounds were counted per task; both fixed before
  the user read them.
- **Three verdicts changed with the decisions**: EP7 and SD2 from open to improve, SD26 to
  drop; EP15 to drop and EP18, SD18 and WP11 to improve with the user's answers.

---

## Changes To Later Phases

- `phase-2-proof.md`: added a constraint — the proof a task declares is one the execution
  operation can run and record before ticking the task (EP18), and the reviewer agent
  takes the parts of `code-reviewer.md` Phase 2 keeps (EP19, SD16, SD17).
- `phase-3-git.md`: added a constraint — the `[git]` table decides, per repository, `main`
  or branches, and when the execution operation commits (EP9, WP4).
- `phase-4-decisions.md`: added a constraint — the follow-up roadmaps carry
  `shaping-work`, the execution operation, the conditional reviewer agent and the
  implementer agent, with the trigger and phase-boundary rules.

---

## Assessment

The phase ruled on the five skills that turn an idea into executed work — 90 rows in the
draft record, each with its evidence, 33 kept, 37 improved, 18 dropped, 2 left to Phases 2
and 3 — and settled with the user where they go: a design skill of this setup's own,
`shaping-work`; a phase's design in a `## Design` section; the plan as the phase's tasks;
and an operation of the roadmap skill that executes one phase inline, never chaining the
next, with a conditional reviewer and light delegation written into the roadmap.

Its evidence came mostly from the transcripts and review 09-27, read before they go, and
it corrected Phase 0: resumed sessions copy their history, so the baseline is 29 calls in
32 conversations, not 51 calls in 41 sessions.

What Phase 2 needs to know first: the proof a task declares must be runnable by the
execution operation, which ticks a task only once its proof passed (EP18), and the
method question of `study/methods.md` returns there (WP9); the reviewer agent waits for
Phase 2's verdict on `code-reviewer.md`.
