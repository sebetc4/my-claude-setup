# Phase 4 Report: Evaluation Tooling

**Phase:** [phase-4-evaluation-tooling.md](phase-4-evaluation-tooling.md)
**Start Commit:** 8c79c7b

---

## Work Log

### 2026-10-06

Opened the phase from Phase 3's closure, committed as `8c79c7b`. Read Phase 3's file and
its report, finalized in this session: no restructuring pending, and no other phase in
progress. What binds this phase: `authoring-skills` exists with three operations,
create, edit and audit, to which this phase adds the fourth, evaluate, with its own
reference; Phase 3's eval runs left their files and `tools/order.py` under
`.eval-runs/skills/authoring-skills/`, and their `evals/evals.json` files carry keys of
their own — pressures, trigger queries, `failures_without_skill` and
`failures_with_skill` — which this phase's design settles; the constraints Phase 3 added
here, on the cost and counting of runs, `TMPDIR`, evals kept out of a run's reach and
the variance of an agent's judgment; the part of row S17 the evaluation reference takes;
and the Agent Skills standard's guides on evaluating skills, listed with this setup's
departures in `docs/conventions/agent-skills.md`. To put to the user before any work:
the twelve tasks declare no proof yet, as Phase 3's did not at its opening; and the
first risk still names the superpowers SessionStart injection, though every plugin was
removed on 2026-10-04. At the user's rule, the opening ends the turn: no work on the
phase yet.

In a new session, at the user's request, measured what Phase 3 cost and why. The
sources were the transcripts of its five sessions and of their subagents, and the
effort of every Opus 5.5 main thread since 2026-09-24. Recorded in
`docs/decisions/2026-10-06-token-costs.md`.
- About $167 in all. $88 went to a main thread at `max`, whose context reached 631,000
  tokens and was never compacted. About $79 went to subagent runs, which took the
  session's `max`.
- This setup's tools cost about $5 of it.
- A subagent's transcript does not hold its final output tokens, while a main session's
  does, and `cost-state` records hold each model's totals: this corrects the constraint
  of 2026-10-05, which said no transcript held them.

The user then agreed to source two roadmaps on these figures. This phase gained the task
that measures the same evals at `max` and `xhigh` before the runs' effort is set, 13
tasks now. The run procedure now sets the runs' effort and model and records each run's
cost, and the benchmark reports cost, model and effort. The constraints now give the
runs' costs, where a run's output tokens are found, and the user's proposal that the
review domain measure token consumption.

At the user's request, Phases 4 and 5 were then aligned with the proof convention of
`docs/decisions/2026-10-01-superpowers-study.md` (Decisions Of Phase 2, items 1 and 2),
and what had gone stale was updated. Each task of both phases got a proposed `Proof:`
line, awaiting the user's approval. In this phase:
- the effort task moved after the benchmark, which it needs;
- a task was added that counts a run's tokens and cost from its transcripts, the code
  the run procedure and the benchmark rely on, which makes 14 tasks;
- the objective now says that Phase 0 kept blind comparison as an option;
- the overview lists the traps Phase 3's runs added;
- the first risk no longer names the superpowers injection, gone with the plugins, and
  names this setup's own hooks instead;
- Files to Modify names the domain, the skill, the two agents the 2026-09-28 record
  named, and `SKILL.md`, which gains the evaluate operation;
- the viewer task names the copy under `study/` that it adapts.

The user approved the proofs of both phases as proposed, raised no objection to the
change of Phase 5's Objective, and asked for a roadmap of the review domain's
measurement of token consumption. Its phases are to be proposed first.

Created roadmap `token-usage` under `docs/roadmap/pending/` with the user, in four
phases: Framing, Usage Reader, Reviews And Reports, Validation And Release. The user
settled that the measurement belongs to the review domain, whose aim becomes reviewing
how tools work and what they cost. The roadmap waits for this one, whose count of a
run's cost it extends. This phase's constraint on that count now says one reader serves
both, placed where the review domain can take it. The user approved the proofs of its 23
tasks.

---

## Decisions

- **A run's effort and model are set by the run procedure, never left to the
  session.** Phase 3's runs took the session's `max`, where thinking made 84% of their
  output. A benchmark left to the session's effort compares runs made under different
  conditions. Which effort the runs take is this phase's measure of `max` against
  `xhigh` to decide.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

- `docs/roadmap/pending/roadmap-execution/phase-0-framing.md`, roadmap
  `roadmap-execution`, at the user's request on 2026-10-06:
  - added the task that settles when `execute-phase` hands over to a new session,
    whether at a phase's end, at a task's end, or past a context threshold declared in
    `[roadmap]`;
  - added a constraint giving the figures of `docs/decisions/2026-10-06-token-costs.md`;
  - the phase holds 7 tasks now. Its opening decision, one phase per conversation, may
    change there.
- `phase-5-switch-over.md`, at the user's request on 2026-10-06 to update what the
  removal of every plugin made stale:
  - The Objective no longer turns `superpowers:writing-skills` and skill-creator off,
    done on 2026-10-04, and names the install and the decision record. This change is
    a restructuring, made at the user's request in those words.
  - Why This Phase Matters and Out of Scope follow the Objective.
  - The section Proof becomes Comparison With The Old Tools, so that it is not confused
    with the `Proof:` lines, and Turn Off becomes Install And Release.
  - The first task gives the old tools to the runs from their copies under
    `study/skill/`.
  - `tests/check.py` and `.claude/settings.json` join Files to Modify.
  - Each of the 12 tasks has a `Proof:` line, approved by the user on 2026-10-06.

---

## Assessment
