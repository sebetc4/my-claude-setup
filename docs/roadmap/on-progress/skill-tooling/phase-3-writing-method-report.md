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
task, which still named `.superpowers/specs/`. Committed as `1d74460`.

Found the plugin cleanup partly done on the user's side: the `diagram-design` marketplace
and every install record gone, its declaration out of the user settings. Left: the deny
rule on `writing-skills`, and `diagram-design` in scriptorium's committed
`.claude/settings.json` and in forma-rust's local settings. A fresh headless session
started from a scratch folder listed no plugin skill: only the builtin plugins
`agents-md` and `telemetry`, and 21 skills — 19 bundled with Claude Code, `roadmap` and
`tool-review`.

Probed, before the baseline relies on it, whether the repository's audit hook fires on a
subagent's write: a Haiku subagent wrote a skill with a `tools` field under
`.eval-runs/probe-hook/`, and the hook blocked with "[F6] unknown field `tools`" and
"[C1] `probe-skill` is outside the skill folders domains/*/skills, .claude/skills". The
hook thus runs in both arms of every eval, as `CLAUDE.md` does, which the subagent's
context also held; and C1 would report every skill an eval run writes in the workspace,
pushing the run to move it. Removed the probe's folder.

At the user's request, wrote a script for the user to run that removes the three
entries left, a dry run unless given `--apply`: the first script had refused every file,
since scriptorium's settings escape non-ASCII characters, a format its check did not
expect; the new one keeps each file's own format. Tested on copies of the three files:
the dry run writes nothing, the apply removes only the entries, a second run finds
nothing, and a file in an unknown format is left untouched. Listed the skills that ship
with Claude Code: a fresh headless session lists 15 of them to the model, and its init
event names 8 more that only the user can invoke.

At the user's request, wrote `docs/claude-code-builtins.md`, cited from `CLAUDE.md`:
what Claude Code 2.1.283 ships — skills, agents, tools, commands, plugins, the claude.ai
sync and the settings that control them — and where each overlaps this setup, so that no
tool of ours takes a built-in's name or duplicates one unsaid. Taken from the headless
init event, the skill listing the model sees, and the definitions inside the executable.
Two findings bear on this phase: `run-skill-generator`, a bundled skill the user invokes,
writes one kind of skill, so `authoring-skills`' trigger evals take its requests as near
misses; and the sessions here have no `Grep` or `Glob` tool, which `roadmap-auditor`
still declares. The skill that wrote skills the user remembered turning off was the copy
of `skill-creator` among the 8 skills synced from claude.ai, off since 2026-09-18. At the
user's request, the auditor's fix became a task of roadmap `roadmap-dependencies`'
Phase 3, whose README moved to 1.0.2.

The user approved the three baseline tasks with what a good result holds, the run
conditions — prompts in French, since the user speaks French in conversations — and
C1's change. C1 first, a fix the baseline needs: a test written first, a skill under the
workspace of a repository declaring `workspace = ".eval-runs"`, failed because C1
reported it, while a skill outside both still gets C1; then C1 left the workspace out,
and the 67 tests of the audit and `make check` passed. The record's C1 row and the
domain's changelog say so.

---

## Decisions

- **Each task declares its proof** (the user, 2026-10-05), on an indented `Proof:` line,
  with two changes of order: the baseline runs before the design, so that the design
  answers observed failures rather than expected ones (row W1 of the 2026-09-28
  record); the agent comes before the audit reference, whose proof calls it. Task 11
  runs the whole set again once the loopholes are closed.
- **The baseline runs under fixed conditions** (the user, 2026-10-05): three tasks, one
  per kind of skill, their expected results in `authoring-skills/evals/evals.json`;
  Sonnet, one run per task, the same model for the runs with the skill; prompts in
  French, as the user speaks in conversations, after a preamble in English; the audit
  hook and `CLAUDE.md` in both arms, so that the comparison measures what the skill adds
  to the audit.
- **C1 leaves the eval workspace out** (the user, 2026-10-05): the audit hook also fires
  on a subagent's edits, and eval runs write their outputs under `.eval-runs/`. Phase 4's
  runs rely on it.

---

## Files Changed

---

## Problems And Deviations

- **Rule C1 reported every skill an eval run writes in the workspace,** and the audit hook
  fires on a subagent's edits: found by a probe before the baseline. Fixed, with the
  user's approval, by a change to the catalogue approved on 2026-10-04.

---

## Changes To Later Phases

- `phase-4-evaluation-tooling.md`: its design task writes the design in the phase's
  `## Design`, citing a decision record where the section is not enough, rather than in
  `.superpowers/specs/`, which the superpowers study set aside, as Phase 3's design task
  already reads.

---

## Assessment
