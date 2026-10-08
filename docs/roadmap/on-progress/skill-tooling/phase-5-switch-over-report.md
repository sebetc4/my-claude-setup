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

---

## Decisions

---

## Files Changed

---

## Problems And Deviations

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
