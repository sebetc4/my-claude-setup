# Phase 3 Report: Writing Method

**Phase:** [phase-3-writing-method.md](phase-3-writing-method.md)
**Start Commit:** 4945b24

---

## Work Log

### 2026-10-04

Opened the phase from Phase 2's closure, committed as `4945b24`. Read Phase 2's file and
its report, written in this session: no restructuring pending, and no other phase in
progress. What binds this phase: the rule catalogue of
`docs/decisions/2026-10-03-skill-audit-rules.md` and its audit, which the writing guide
and the `skill-auditor` build on, the agent taking the judgment the rules leave out;
`authoring-skills` already exists, its `SKILL.md` limited to the audit and to be
rewritten, with `audit.py`, `frontmatter.py`, `conventions.py` and
`references/conventions.md`; the design goes in the phase's `## Design`, citing a
decision record where needed; the template rules are the roadmap skill's own checks;
each task declares its proof, approved with the phase, and commits go task by task, by
hand until roadmap `roadmap-execution`. At the user's rule, the opening ends the turn:
no work on the phase yet, the user continuing in a new session.

Resumed in a new session. Read this phase's file, Phase 2's report, the 2026-09-28
record and the proof decisions of the 2026-10-01 record. Found that the twelve tasks
declare no proof and the file has no `## Design` section yet. Put to the user a `Proof:`
line per task, with two changes of order: the baseline before the design, so that the
design answers observed failures (row W1), and the agent before the audit reference,
whose proof calls it. Raised two dependencies nothing settles yet: the repository's
audit hook may fire on the baseline subagents' edits, and the proof reference of roadmap
`roadmap-execution`, which will define the five kinds, comes after this phase.

The proofs still waiting, the user asked to remove every plugin for good, with its cache:
none serves here any more, they pollute contexts and tests, and the other repositories
wait for this repository's roadmaps. Measured first with `claude plugin details`: an
always-on listing of about 840 tokens for superpowers, plus its start-up injection, 110
for skill-creator, 140 for claude-code-setup, 180 for claude-md-management. Every source
the roadmaps still need is copied under `study/`, which git ignores; only step 6 of
`grade.py` read the plugin cache. Uninstalled the five plugins at user scope and locally
here, in scriptorium and in forma-rust with `claude plugin uninstall`; removed the
official marketplace, which also uninstalled the records left for the three projects
whose folders are gone; deleted the plugin cache. The auto mode classifier refused the
script that removed the remaining entries from the settings files, as a change to the
agent's own settings: left to the user are the `diagram-design` marketplace declared in
the user settings and in scriptorium's committed `.claude/settings.json`, its entry in
forma-rust's local settings, and the deny rule on `writing-skills`.

### 2026-10-05

The user approved the twelve proofs and both changes of order, with two remarks: session
reviews will later measure which parts of the skill are really used (task 3), which
Phase 5's task adding the new tools to `domains/review/hooks/tools.json` provides; and
once the loopholes are closed, the whole set runs again so that no fix broke another
(task 11), which the task and its proof now say. Wrote a `Proof:` line under each task
and reordered them: the baseline before the design, the agent before the audit
reference, which moved under its own `### Audit` heading. Reworded Phase 4's design
task, which still named `.superpowers/specs/`.

---

## Decisions

- **Each task declares its proof** (the user, 2026-10-05), on an indented `Proof:` line,
  with two changes of order: the baseline runs before the design, so that the design
  answers observed failures rather than expected ones (row W1 of the 2026-09-28
  record); the agent comes before the audit reference, whose proof calls it. Task 11
  runs the whole set again once the loopholes are closed.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

- `phase-4-evaluation-tooling.md`: its design task writes the design in the phase's
  `## Design`, citing a decision record where the section is not enough, rather than in
  `.superpowers/specs/`, which the superpowers study set aside, as Phase 3's design task
  already reads.

---

## Assessment
