# Summary — superpowers-study

---

## Where We Started

On 2026-10-01 the superpowers plugin, 6.4.1, was the user's working method in most
projects: design, plans, execution through subagents, test-driven development, branch
finishing. It ran a SessionStart hook in every session and brought its own conventions,
and the decision of 2026-09-18 had postponed vendoring it on a baseline of 51 calls and
"8 % of sessions" calling any skill. The user wanted it off for good, keeping every part
that serves, rewritten for this setup. Two roadmaps waited for the study, `skill-tooling`
from its Phase 2 and `roadmap-dependencies`, and three questions of the user rode with
it: whether a task should choose its engineering method, how git work is organized, and
how a plan is executed.

---

## Where We Landed

The decision record `docs/decisions/2026-10-01-superpowers-study.md` rules on every part
of the plugin but `writing-skills`: 220 rows, each with its evidence — 57 kept, 85
improved, 78 dropped, none left open — and a target architecture that gives each kept
row a receiver. The plugin goes off everywhere, and nothing of it is vendored.

The three questions have their answers. No method is chosen from a catalogue: each task
declares its proof — `test`, `eval`, `probe`, `check` or `review` — naming its object, on
a `Proof:` line the execution runs and records before ticking the task. Git work follows
a `[git]` table per repository — `branch`, `commit`, `message` — this repository and
scriptorium committing per task on their default branch, pull requests dropped for now.
A phase is executed inline by an operation of the roadmap skill, `execute-phase`, one
phase per run, with a reviewer agent only when the phase changes code or scripts and a
delegated task only when the phase says so.

Three roadmaps wait in `pending/` to build it: `roadmap-execution` for the roadmap
skill, its proof reference, its `[git]` table and its two agents; `working-method` for
`shaping-work` and `finding-root-causes`, after which it turns the plugin off under three
go-ahead conditions; `git-domain`, until a repository asks for branches or worktrees.
`skill-tooling` and `roadmap-dependencies` no longer wait, and this repository's
`CLAUDE.md` scopes test-first to code and scripts.

---

## What Each Phase Delivered

- **Phase 0 Framing** — the inventory of 6.4.1, its hand-overs, the conventions it
  imposes and its ties to Claude Code, and the method every later verdict followed: the
  matrix with a `Goes to` column, five rules of evidence, a recount by working sessions.
  It found that the baseline had measured 6.3.0 and counted eval runs, and that the
  evidence goes with the transcripts, after 30 days.
- **Phase 1 Design And Planning** — 90 rows on the five skills that turn an idea into
  executed work, and the decisions taken with the user: a design skill of this setup's
  own, `shaping-work`; a phase's design in its `## Design` section; the plan as the
  phase's tasks; an execution operation that runs one phase inline. It corrected the
  baseline to 29 calls in 32 working conversations, resumed sessions having copied their
  history.
- **Phase 2 Proof** — 79 rows on the five skills that prove work done, and the proof
  each task declares, decided on 288 micro-test sessions on two models: a plain
  test-first instruction works for code and does harm elsewhere, where a declared proof
  naming its object brings each artifact its method. Debugging got a skill of its own.
- **Phase 3 Git** — 26 rows on the two git skills, settling the four rows earlier phases
  had left open, and the `[git]` table designed with the user: every finish observed had
  moved the base forward and none had made a pull request.
- **Phase 4 Decisions** — the recount, 4 of 36 working conversations calling the plugin
  against 11 of 32 in the baseline; 25 rows dropping the plugin's entry point and its
  diagnosis skill; the decision, the turn-off plan and when to revisit; the three
  follow-up roadmaps, and the two waiting roadmaps unblocked.

---

## What We Learned

- **Transcripts are perishable, and they over-count.** Claude Code deletes them after 30
  days; resumed sessions copy their history into new transcripts; eval runs and stubs
  outnumbered working transcripts ten to one in the baseline period. A count over them groups conversations by assistant
  message id, counts calls once per `tool_use` id and keeps the conversations a person
  spoke in — and a measure that waits loses its baseline, so the evidence a decision
  rests on goes into the record before it goes.
- **A recount starts by reproducing its baseline.** The 2026-09-18 figures held 22 copies
  among 51 calls and counted runs in their 8 %; the script of Phase 4 reproduced the
  corrected baseline exactly before it counted the window, which is what makes the two
  comparable.
- **Guidance that names its object does better than a general rule.** A plain test-first
  instruction made the stronger model test text and configuration; the same model given
  a declared proof chose the right method, and a `check` without its command drifted to
  the suite. Where a rule must hold across artifacts, the declaration says what is run.
- **An injected "always use a skill" rule did not bring its skills.** Injected in every
  session, it preceded a superpowers call in 4 conversations of 36; in this repository,
  without it, every working conversation called the skill its work needed. What brings a
  skill to the work is its description, which trigger evals can check.
- **One review at the end found what per-task reviews let through.** Every final review
  that ran to its end found something to fix, three of them after every task had passed
  its own review.
- **Conventions come from observed practice, then go where a tool reads them.** The
  plugin's finishing menu was bypassed or reworded four times out of five and its pull
  request never chosen; this setup records what each repository actually does in its
  `[git]` table instead of offering a menu.

---

## What We Are Leaving Open

- **Everything decided is still to build,** in `roadmap-execution`, `working-method` and
  `git-domain`. Until `working-method`'s last phase, the plugin stays on at user scope
  and in scriptorium and forma-rust, and nothing reads `Proof:` lines or the `[git]`
  table.
- **The user's row-by-row review of the matrix stopped at EP1,** in Phase 1. The later
  rows stand as the agent's verdicts on the decisions taken with the user; each
  follow-up roadmap's Framing phase lists the rows it builds and gets its designs
  approved before any change.
- **Some verdicts rest on no observed use or on plans:** the worktree rows, no worktree
  having served as a workspace; the proof design, measured on what agents said they would
  do rather than on what they did, which the evals of `execute-phase` will measure.
- **The trigger evals' 38 prompts live only in `study/`,** outside git.
- **What `attributionSkill` measures is a turn's work, not a skill's carried cost,** so the
  cost per call stays the size of its `SKILL.md`.
- **The When To Revisit list of the record:** a failing go-ahead condition, proof
  declarations going wrong in use, a month of `phase-reviewer` runs, a repository asking
  for branches or worktrees, and two weeks after the plugin is off.
