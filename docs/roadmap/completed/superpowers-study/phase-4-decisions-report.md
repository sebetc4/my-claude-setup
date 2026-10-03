# Phase 4 Report: Decisions

**Phase:** [phase-4-decisions.md](phase-4-decisions.md)
**Start Commit:** ae3f52f

---

## Work Log

### 2026-10-02

Opened the phase from Phase 3's closure, committed as `ae3f52f`. Read Phase 3's file and
its report, written in this session: no restructuring pending, and no other phase in
progress. What binds this phase: the decisions of Phases 1 to 3 in the draft record,
which its constraints carry into the follow-up roadmaps — `shaping-work`, the execution
operation, the reviewer and implementer agents, the `Proof:` line and its reference, a
debugging skill, the `[git]` table and a git domain to name —; the recount by
2026-10-18 at the latest; and nothing changed in the user's settings without the
user's go-ahead. At the user's rule, the opening ends the turn: no work on the phase
yet.

### 2026-10-03

The user asked to work the phase and close the roadmap. Wrote the recount script,
`study/superpowers-recount/recount.py`, by the Phase 0 method, and ran it first on the
baseline period: it reproduced the baseline exactly, 32 working conversations in 41
transcripts, 11 calling superpowers, 29 calls with the same split. Then on the window,
2026-09-19 to 2026-10-03, up to the day rather than on 2026-10-18, since the user wants
the roadmap finished: 36 working conversations, 4 calling superpowers, 11 % against
34 %, 9 calls, six of them in the one chain of 2026-09-26 and 2026-09-27; 92 % of the
conversations called a skill of some kind, the roadmap skill, `tool-review` and
scriptorium's own skills taking the work. Established what `attributionSkill` covers —
the turn a skill starts, up to the next human message — so the cost per call stays the
`SKILL.md` size; measured the fixed cost as delivered in scriptorium, ~1,650 tokens.
Wrote the Recount section of the record.

Read `using-superpowers`, its Claude Code note, the hook and `diagnosing-superpowers`
with its companions; found the plugin's state in the user's settings — on at user scope
and in scriptorium's and forma-rust's local settings, off here, three local installs
pointing at folders no longer on disk — and, in passing, skill-creator still on in
scriptorium's local settings. Ruled the three parts in the record's Plugin section: 25
rows, all dropped, the recount's 4 of 36 against the injection's ~934 tokens per start
deciding HK1 and US3.

Grouped the 142 kept and improved rows of the matrix by their "Goes to" column, and drew
from them the target architecture: nine receivers, each with its rows and the roadmap
that builds it. Put to the user the four choices left to this phase — the names of the
operation and of the two agents, the name of the debugging skill, the domain of the two
method skills, the split and order of the follow-up roadmaps —; the user took the
recommended option of each. Before writing the turn-off plan, saw that the baseline
period's transcripts start going tomorrow: saved the human prompt before each of the 38
superpowers calls of both periods to `study/superpowers-recount/call-prompts.md`, the
material of `working-method`'s trigger evals. Wrote the Decision — the architecture
table, checked by a script to cover every kept and improved row exactly once per
receiver —, the plan that turns the plugin off with its go-ahead conditions, and When
To Revisit; the record is no longer a draft. `make check` passed; committed as
`6fb9d7d`, the recount, the plugin rows and the decision together, all three in the one
file.

Created the three follow-up roadmaps in `pending/` from the skill's templates:
`roadmap-execution`, five phases and 25 tasks, waiting for `roadmap-dependencies`;
`working-method`, four phases and 15 tasks, waiting for `skill-tooling` and
`roadmap-execution`, its last phase carrying the turn-off plan step by step;
`git-domain`, four phases and 14 tasks, waiting for `roadmap-execution` and for a
repository's request. Each Framing phase settles its designs with the user before any
change, as `roadmap-dependencies` does. No `Proof:` line yet: the decision has the user
approve each proof with its phase, at its opening. `progress.py --check` passed on all
three, and the links resolve. Committed as `6ffc133`.

Put to the user the restructuring of skill-tooling — its Phase 5's task that turned
superpowers back on here removed, a task added that turns skill-creator off in
scriptorium's local settings, the recount of 2026-10-18 no longer named in its Phase 5
and README — and the line of roadmap-dependencies' README that had it apply the study's
decisions, now roadmap-execution's. The user approved both; applied them, cleared both
`Blocked By`, set skill-tooling back from ⏸️ to 🟡, its pause having been for this
roadmap, and gave each roadmap a changelog entry. Then scoped `CLAUDE.md`'s "TDD (failing
test first)" to code and scripts, naming the proof that fits the other artifacts.
`make check` passed.

---

## Decisions

- **The recount ran up to the day, on 2026-10-03, not on 2026-10-18.** The phase file
  allowed it, and the user asked to finish the roadmap; the window, fifteen days, is as
  long as the baseline's period. Nothing is left for 2026-10-18.
- **Every row of `using-superpowers`, `diagnosing-superpowers` and the hook is dropped.**
  The injection brought a superpowers call in 4 of 36 conversations; each skill of this
  setup is brought by its own description, which trigger evals tune.
- **Names** (the user, 2026-10-03): `execute-phase` for the roadmap skill's execution
  operation, `phase-reviewer` and `task-implementer` for the two agents,
  `finding-root-causes` for the debugging skill, `git` for the git domain.
- **One domain, `working-method`, holds `shaping-work` and `finding-root-causes`** (the
  user, 2026-10-03); the proof reference lives in `shared/proof/`, copied into the
  roadmap skill and `shaping-work`.
- **Three follow-up roadmaps, `roadmap-dependencies` before `roadmap-execution`** (the
  user, 2026-10-03): `roadmap-execution` waits for `roadmap-dependencies`;
  `working-method` waits for `skill-tooling` and `roadmap-execution`, and turns the
  plugin off in its last phase; `git-domain` waits for a repository asking for
  `branch = "roadmap"` or pull requests. The order means `roadmap-dependencies` runs
  under the roadmap skill as it is, its phases' proofs and commits applied by hand.
- **The plugin goes off once `roadmap-execution` and `working-method` are installed,**
  the trigger evals pass on the 38 saved prompts, and the user agrees; `git-domain` is
  not waited for, both repositories running `branch = "none"`.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/superpowers-study/phase-4-decisions-report.md` — created at
  the opening, committed with it in `1480cc2`
- `docs/roadmap/pending/git-domain/README.md`
- `docs/roadmap/pending/git-domain/phase-0-framing.md`
- `docs/roadmap/pending/git-domain/phase-1-branch-per-roadmap.md`
- `docs/roadmap/pending/git-domain/phase-2-git-skill.md`
- `docs/roadmap/pending/git-domain/phase-3-release.md`
- `docs/roadmap/pending/roadmap-execution/README.md`
- `docs/roadmap/pending/roadmap-execution/phase-0-framing.md`
- `docs/roadmap/pending/roadmap-execution/phase-1-proof-and-template.md`
- `docs/roadmap/pending/roadmap-execution/phase-2-git-table.md`
- `docs/roadmap/pending/roadmap-execution/phase-3-execute-phase.md`
- `docs/roadmap/pending/roadmap-execution/phase-4-validation-and-release.md`
- `docs/roadmap/pending/working-method/README.md`
- `docs/roadmap/pending/working-method/phase-0-framing.md`
- `docs/roadmap/pending/working-method/phase-1-shaping-work.md`
- `docs/roadmap/pending/working-method/phase-2-finding-root-causes.md`
- `docs/roadmap/pending/working-method/phase-3-release-and-turn-off.md`

**Modified**
- `CLAUDE.md`
- `docs/decisions/2026-10-01-superpowers-study.md`
- `docs/roadmap/on-progress/skill-tooling/README.md`
- `docs/roadmap/on-progress/skill-tooling/phase-5-switch-over.md`
- `docs/roadmap/on-progress/superpowers-study/README.md` — the opening's edits,
  committed in `1480cc2`, then this closure's
- `docs/roadmap/on-progress/superpowers-study/phase-4-decisions.md` — the opening's
  status, committed in `1480cc2`, then the work and the closure
- `docs/roadmap/pending/roadmap-dependencies/README.md`

---

## Problems And Deviations

- **The recount covers fifteen days, not thirty.** Run on 2026-10-03 rather than
  2026-10-18, its window matches the baseline's period in length, and nothing is left to
  recount; the window's transcripts go from about 2026-10-19.
- **The window leans on one repository:** 30 of its 36 working conversations are
  scriptorium's, where the user's own skills took much of the work, and this
  repository's count stops on 2026-09-28. Left as a limit of the recount, written in the
  record's Recount section.
- **Commits per task, applied by hand and only in part.** The recount, the plugin rows
  and the decision all edit the decision record and went into one commit; the restructuring
  and the unblocking of the two roadmaps went into another. No tool reads the `[git]`
  table yet.
- **skill-tooling's ⏸️ was cleared by this phase,** where the roadmap skill leaves ⏸️ to a
  person: its pause, on 2026-10-01, was for this roadmap, and clearing its `Blocked By`
  was a task the user asked to finish.
- **skill-creator was found still on in scriptorium's local settings,** although
  skill-tooling's Phase 0 turned it off at user scope, a local value overriding the
  user's. Moved, with the user's approval, to a task of skill-tooling's Phase 5.
- **The turn-off plan names no command for the uninstall,** only Claude Code's plugin
  commands: not probed here, it is left to `working-method`'s Phase 3.
- **The trigger evals' prompts live only in `study/`,** which git ignores: a new clone
  does not have them. `working-method`'s README names the file among its dependencies.
- **The follow-up roadmaps carry no `Proof:` line,** the user approving each proof with
  its phase, at its opening (Decisions Of Phase 2, item 2).

---

## Changes To Later Phases

- No phase of this roadmap follows Phase 4.
- Approved by the user on 2026-10-03 and applied, in roadmap `skill-tooling`:
  `phase-5-switch-over.md` lost the task that turned superpowers back on in this
  repository, gained the task that turns skill-creator off in scriptorium's local
  settings, and its Out of Scope and its Files to Modify follow; the README's Out Of
  Scope no longer leaves the other superpowers skills to the recount of 2026-10-18.
- Approved by the user on 2026-10-03 and applied, in roadmap `roadmap-dependencies`: the
  README's Out Of Scope leaves the study's decisions on execution, proof and git to
  roadmap `roadmap-execution`.
- The `Blocked By` of both roadmaps cleared, as the phase's task; each roadmap's
  changelog records it.

---

## Assessment

The phase turned the verdicts of Phases 1 to 3 into a decision. The recount, run up to
the day, found the plugin called in 4 of 36 working conversations where it stayed on,
against 11 of 32 in the baseline, while 92 % called a skill of some kind: the roadmap
skill, `tool-review` and scriptorium's own skills had taken the work. The plugin's entry
point and its diagnosis skill went whole, 25 rows dropped. The record now holds 220 rows
— 57 kept, 85 improved, 78 dropped, none open —, a target architecture that gives each
of the 142 kept rows its receiver, the plan that turns the plugin off with its three
go-ahead conditions, and when to revisit. Three roadmaps carry it — `roadmap-execution`,
`working-method`, `git-domain` — and `skill-tooling` and `roadmap-dependencies` resume.

What comes next needs to know first: `skill-tooling` resumes at its Phase 2, then the
order is `roadmap-dependencies`, `roadmap-execution`, `working-method`, with `git-domain`
waiting for a request. Until `roadmap-execution` is installed, nothing reads `Proof:`
lines or the `[git]` table: a phase that applies those decisions before then does it by
hand, as this one did for its commits. The 38 prompts of the trigger
evals are saved outside git, and the baseline period's transcripts start going on
2026-10-04.
