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
