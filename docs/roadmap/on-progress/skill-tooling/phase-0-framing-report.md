# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** 2f47fe7

---

## Work Log

### 2026-09-28

Opened the phase. `references/open-phase.md` names two README fields to change, but the
progress block also had to change: `progress.py --check` expects the Phase 0 line at 🟡
with one filled cell, per the Progress bar invariant. Replaced the line with the script's
output. Also found that nothing will bring this phase back in a new session: the roadmap
stays under `pending/` until Phase 0 closes, and `session_resume.py` scans only
`on-progress/`. Both are recorded under Problems And Deviations.

Checked that the local copies under `pending/skill/` are identical to the installed
superpowers 6.4.1 and skill-creator (cache `fa59bc903774`), then read `writing-skills`
and its companion files in full, and skill-creator's SKILL.md, agents and scripts.
Fetched the Claude Code skills page, the Agent Skills specification and the live best
practices as Markdown, into the session's scratchpad.

Findings that shaped the matrix: the best-practices file bundled with `writing-skills` is
an edited copy — "Claude" rewritten to "agent" — and stale; skill-creator's
`run_eval.py` counts only the first tool call of a trigger run; the docs confirm that a
local skill attaches the files its `@` references name, and ask bodies to "state what to
do rather than narrating how or why", against skill-creator's "explain the why".

Ran `tests/skills.py` on each source through a small runner in the scratchpad: 20
problems in `writing-skills`, 11 in skill-creator, none in this repository's skills.
Most resource problems are false positives — example paths, `python -m` module names,
imports — and two wording hits come from this repository's convention applied to foreign
skills. Also found that `tests/skills.py`, `tests/domains.py` and
`domains/review/tests/test_reviewfile.py` import PyYAML, against the standard-library-only
convention.

Wrote the capability matrix (30 rows for `writing-skills`, 38 for skill-creator), the
platform facts with the phase encoding each, and the classified check results into the
draft `docs/decisions/2026-09-28-skill-tooling.md`. Ticked the inventory tasks except the
skill-creator one: rows S26 and S30 wait on the open questions about blind comparison and
description tuning.

Before reading the draft, the user set three principles, recorded under Decisions, and
announced the repository will be renamed `my-agent-setup`. Wrote them into `CLAUDE.md`
under `## Principles`, adjusted two Phase 2 tasks, and recorded the README statements they
contradict as pending approval. Revised the draft record to match: W29 and W30 now read the
agent-neutral wording of `writing-skills` as the right direction, and the record now
presents the documentation's facts and the checks' results as evidence to weigh. A grep
found a single use of "Claude" outside "Claude Code" in `domains/`, in a test docstring:
the existing tools already address the agent.

The user reviewed the matrix. W3 was wrong: superpowers stays installed, and only
`writing-skills` is retired — the README's "the plugin" means skill-creator. W15 needs a
measurement rather than a drop, Node and Graphviz being acceptable. Several rows reasoned
from Claude Code alone (W17, W28, S18, S32), and the platform facts needed a scope.
Revised W3, W4, W9, W15, W17, W25, W28, W29, W30, S14, S18 and S32, and gave the platform
facts a scope column, standard or Claude Code. Added two tasks to this phase at the
user's request: the flowchart measurement, and `docs/claude-code-coupling.md` listing
every tie to Claude Code.

For the testing rule, read `local-review/2026-09-27-5f2a65d1-tool-review-build.md`:
`test-driven-development` added little where the plan already ordered every step RED →
GREEN, while the headless probes run before designing overturned two assumptions. The
live best practices, § Build evaluations first, prescribe test-first for skills: run the
tasks without the skill, build three scenarios on the gaps, measure the baseline, then
write the minimum.

The user answered the open questions and approved the three README changes, now applied.
Ticked the skill-creator inventory, whose rows S26 and S30 now have verdicts, and the four
open questions; row W15 waits on its own measurement task. Adjusted Phases 1, 4 and 5 to
the answers. While checking Phase 5, found that the skills page says `skillOverrides`
does not reach plugin skills, against the memory read from the 2.1.268 binary, and that
no settings file on this machine sets `skillOverrides`: the overrides decided on
2026-09-18 are not in place, and this session lists every superpowers skill.

The user approved the description rule, now in the record's Settled Rules, and asked to
turn off skill-creator and `writing-skills` at once, since three skills doing the same job
would bias every test. Probed first with headless `claude -p` runs on Haiku, their settings
passed with `--settings`, reading the skills listed in the init event: `skillOverrides`
keyed `superpowers:writing-skills` or `writing-skills` left the plugin skill listed, while
the same setting on `roadmap` removed it, which validated the probe; a
`Skill(superpowers:writing-skills)` deny rule refused the call with "Skill execution
blocked by permission rules". Six runs, about $0.12. Then disabled the skill-creator
plugin and added the deny rule in user settings. A fresh session lists 37 skills, without
skill-creator; `writing-skills` stays listed but cannot run; the plugin cache stays, so
`grade.py` still finds its scripts. Moved the Phase 5 turn-off task here, ticked.

Proposed the tone rule. Before deciding, the user asked to turn the whole superpowers
plugin off while the new tool is built. Turned it off in this repository's
`.claude/settings.local.json` only, so other projects keep it for the usage study, and
found that this same file had kept skill-creator enabled here over the user settings: the
earlier check had run from the scratchpad, outside the repository. Disabled it there too.
Two fresh sessions confirm: started in the repository, 23 skills, no superpowers skill,
no skill-creator; started elsewhere, 37 skills with the 15 superpowers ones.

Stopped here, at the user's request, until a new session. The tone rule waits in the
record under Settled Rules, "Tone — proposed", on two decisions: emphatic wording as a
last resort or banned, and a one-clause reason when a rule needs judgment, always, or
never. Remaining after it: the testing, size and script rules, the flowchart
measurement, the LICENSE, the coupling page and the record's completion.

The user asked to finish the phase in the same session. Ran the flowchart measurement as
wording micro-tests: fresh headless sessions on Haiku, the guidance as the whole system
prompt, no tools, no settings. The first two tests, forced choices among four described
options, did not discriminate: the control scored 24/24, the options giving the answer
away. The third, a one-word answer, did: without guidance the model chose to fix an
unrecorded failing check 6 times out of 6, and each form — flowchart, table, list — made
it stop 6 times out of 6; the flowchart cost about 255 input tokens against 100 and 90,
and two of its six reasons drifted to "must be fixed". Row W15 is now a drop. Probed
`allowed-tools` for the script rule: the skill that declared it needed an approval to be
invoked, and once invoked, its script was refused, with `${CLAUDE_SKILL_DIR}` and with a
literal path. Added the Apache 2.0 `LICENSE` from apache.org, and the licensing rules to
the record. Wrote `docs/claude-code-coupling.md` from a grep of the tracked files, and
the rule that keeps it current in `CLAUDE.md`. Measured the skills: `roadmap` ~1,800
tokens, `tool-review` ~1,000, `writing-skills` ~6,700 and skill-creator ~8,300 — the
latter under 500 lines yet over the 5,000 tokens kept after compaction; five of our
references run between 100 and 300 lines without a table of contents.

The user approved the testing rule and the size budgets, with the table of contents from
300 lines, both now in the record. Still open: the two tone points, which the user asked
to see developed with examples, and the script rule, on which the user asked what serves
several repositories and several agents best; the user also asked whether a TDD skill,
as in superpowers, would fit better than a testing rule inside the new skill.

Developed the tone points with examples and answered both questions; the user settled
the tone rule — emphatic wording as a last resort, a one-clause reason when a rule needs
judgment — approved the script rule, and chose no separate TDD skill. Wrote the three
into the record, gave it its decision line and a When To Revisit section, and ticked the
last tasks. Adjusted Phase 1 — the reader runs as a step, not through a `!` command, and
the two roadmap defects found at opening join its migration tasks — and Phase 2, whose
`[skills]` checks now flag the harness features a repository excludes. Then started the
closure: `make check` passed.

---

## Decisions

- **Check and test scripts raise alerts; they do not define the rules.** Set by the user
  on 2026-09-28: `tests/skills.py` and the other checks were written from one of the two
  sources this roadmap replaces, and the new tool redefines the rules. Later phases
  re-justify each current rule instead of preserving it.
- **The official documentation informs; it does not cap.** Set by the user on
  2026-09-28: a tool may go past a documented limit or recommendation when its evaluations
  show it does better. The arbitration of this phase and the rule catalogue of Phase 2
  settle each rule on evidence, the documentation being one source among others.
- **Tools address the agent, never Claude.** Set by the user on 2026-09-28: the setup is
  meant to serve other agents later, and only the install target — `~/.claude`,
  `settings.json`, the hooks format — stays Claude Code's for now, because the tools are
  built and tested with it. Every tool written from Phase 1 on says "the agent", and
  Phase 2 checks it as a `[skills]` convention. Recorded in `CLAUDE.md` under
  `## Principles`.
- **superpowers stays installed; only `writing-skills` is retired.** Set by the user on
  2026-09-28: the other superpowers skills keep being studied for what serves, when and
  why, as `local-review/2026-09-27-5f2a65d1-tool-review-build.md` began. Phase 5 was to
  turn off `writing-skills` and the skill-creator plugin only; both went off during this
  phase, as the entries below record.
- **The new tools stay under tool review for a while after Phase 5,** like the review
  domain's current tools. Set by the user on 2026-09-28; it changes nothing in how the
  skill is written.
- **The new tool writes two kinds of skill:** global skills, like this setup's, used
  across repositories, and repository skills, bound to one repository's conventions and
  context. Agreed by the user on 2026-09-28 (row W4).
- **A description carries no step-by-step workflow; a short mention of what the skill
  does is allowed.** Set by the user on 2026-09-28 (row W9); the description rule builds
  on it.
- **A shared module owns `.agent-conventions.toml`:** one source, copied into each tool
  that reads the file. Chosen by the user on 2026-09-28 from the trade-offs, without the
  planned measurement. Phase 1 decides whether the installer copies it or each domain
  keeps a checked copy.
- **Description tuning: the session proposes each rewrite, a script only measures it,**
  on training and held-out queries. Chosen by the user on 2026-09-28; Phase 4 builds it.
- **Blind comparison is kept as an option,** run only when the benchmark does not
  separate two versions. Chosen by the user on 2026-09-28; Phase 4 builds it.
- **Names.** The skill is `authoring-skills`, chosen by the user on 2026-09-28, who may
  rename it `writing-skills` once superpowers' skill of that name is gone. The domain
  `skill-tooling` and the agents `skill-auditor` and `skill-grader` stand as proposed,
  uncontested; `skill-comparator` was added for the blind comparison kept above.
- **The description rule is settled,** with `when_to_use` excluded and exclusions added
  only after an observed false trigger. Approved by the user on 2026-09-28; the record's
  Settled Rules hold it with its evidence, and Phase 4's trigger evals test it.
- **skill-creator and `writing-skills` are off from now on, not from Phase 5.** Asked by
  the user on 2026-09-28, so that they cannot compete with the new tool in its tests. The
  plugin is disabled; `writing-skills` is refused by a deny rule and stays listed, since
  no setting hides a single plugin skill. Its listing is a known bias for Phase 4's
  trigger evals, which control their settings per run.
- **superpowers is off in this repository until the new tool is built.** Asked by the
  user on 2026-09-28. Turned off in `.claude/settings.local.json`, so other projects keep
  it and its usage study continues there; Phase 5 turns it back on with the user's
  go-ahead. The 2026-10-18 recount has to leave this repository's period out.
- **Flowcharts are dropped** (rows W15 and W25): in the one micro-test that
  discriminated, a table and a numbered list fixed the failure as well as a flowchart,
  for about 40% of its tokens and with steadier reasons.
- **The tone rule is settled:** emphatic wording only as a last resort, after an observed
  discipline failure that plain wording and the discipline form did not fix; a reason in
  one clause when a rule needs judgment. Set by the user on 2026-09-28.
- **The script rule is settled:** the skill stays portable — scripts cited by their path
  relative to the skill's directory, no `allowed-tools`, no permission syntax, a `!`
  command only with a fallback step — and whatever depends on an agent, permissions
  first, is set at install. Approved by the user on 2026-09-28. Phase 1 builds its reader
  under this rule.
- **No separate TDD skill:** the new tool carries its own testing rule, centered on what
  each change needs. Set by the user on 2026-09-28; a general TDD skill for code belongs
  to the superpowers recount.

---

## Files Changed

**Added**
- `LICENSE`
- `docs/claude-code-coupling.md`
- `docs/decisions/2026-09-28-skill-tooling.md`
- `docs/roadmap/on-progress/skill-tooling/phase-0-framing-report.md`

**Modified**
- `CLAUDE.md`

**Renamed**
- `docs/roadmap/pending/skill-tooling/README.md` → `docs/roadmap/on-progress/skill-tooling/README.md` — also modified
- `docs/roadmap/pending/skill-tooling/phase-0-framing.md` → `docs/roadmap/on-progress/skill-tooling/phase-0-framing.md` — also modified
- `docs/roadmap/pending/skill-tooling/phase-1-agent-conventions.md` → `docs/roadmap/on-progress/skill-tooling/phase-1-agent-conventions.md` — also modified
- `docs/roadmap/pending/skill-tooling/phase-2-static-audit.md` → `docs/roadmap/on-progress/skill-tooling/phase-2-static-audit.md` — also modified
- `docs/roadmap/pending/skill-tooling/phase-3-writing-method.md` → `docs/roadmap/on-progress/skill-tooling/phase-3-writing-method.md`
- `docs/roadmap/pending/skill-tooling/phase-4-evaluation-tooling.md` → `docs/roadmap/on-progress/skill-tooling/phase-4-evaluation-tooling.md` — also modified
- `docs/roadmap/pending/skill-tooling/phase-5-switch-over.md` → `docs/roadmap/on-progress/skill-tooling/phase-5-switch-over.md` — also modified

Outside the diff, not tracked by this repository: `~/.claude/settings.json` (skill-creator
disabled, `writing-skills` denied) and this repository's gitignored
`.claude/settings.local.json` (superpowers and skill-creator off).

---

## Problems And Deviations

- **The roadmap skill's opening leaves the progress block stale.** `open-phase.md` lists
  the phase list and `**Current Phase:**` as the README fields to change, while
  `progress.py --check` requires the opened phase's progress line at 🟡 with one filled
  cell. Fixed here by hand; the reference itself is fixed in Phase 1, which gained the
  task.
- **No session will resume this phase automatically.** The folder moves from `pending/`
  to `on-progress/` only when Phase 0 closes (`close-phase.md`, step 3), and
  `domains/roadmap/hooks/session_resume.py` reads only `<Root>/on-progress/`. Moved to
  Phase 1, whose `session_resume.py` task now covers `pending/`.
- **The phase grew from 15 tasks to 18.** The flowchart measurement and
  `docs/claude-code-coupling.md` were added at the user's request, and the turn-off task
  came forward from Phase 5; all three are done.
- **Two of the three flowchart micro-tests could not discriminate.** Forced choices among
  described options gave the answer away, and the control never failed. The drop of row
  W15 rests on the third test alone, on one small model; the record says when to revisit
  it.
- **The task measuring the ways to own `.agent-conventions.toml` was settled without its
  measurement.** The user chose the shared module from the trade-offs; the decision
  record gives the reasoning, and no figure backs it.
- **How to turn off `writing-skills` was unverified.** The skills page (§ Override skill
  visibility from settings) says `skillOverrides` does not affect plugin skills, while the
  memory read from the 2.1.268 binary said a qualified `plugin:skill` key works. Probed
  the same day on 2.1.283: the page is right, and a deny rule is the only way to stop a
  single plugin skill, which stays listed. Fixed; the memory is corrected. Also, no
  settings file on this machine set `skillOverrides`, so the overrides decided on
  2026-09-18 were never in place; reported to the user.
- **skill-creator stayed enabled in this repository after it was disabled.** This
  repository's `.claude/settings.local.json` set it to `true`, and local settings win
  over user settings; the first check ran outside the repository and missed it. Fixed
  the same day, and checked from inside the repository.

---

## Changes To Later Phases

- `phase-2-static-audit.md`: the `[skills]` checks now include who the files address —
  the agent, never a named model — per the decision above.
- `phase-2-static-audit.md`: the task moving `tests/skills.py` into the audit re-justifies
  each rule in the catalogue instead of requiring the same `make check` output.
- `phase-1-agent-conventions.md`: the packaging task names the shared module chosen
  here, and leaves to Phase 1 whether the installer copies it or each domain keeps a
  checked copy.
- `phase-4-evaluation-tooling.md`: the description tuning task states the method chosen
  here, and the blind comparison task states it is the option kept for when the
  benchmark does not separate two versions.
- `phase-5-switch-over.md`: the turn-off task no longer assumes `skillOverrides` reaches
  a plugin skill, and starts with a probe.
- `phase-5-switch-over.md`: the turn-off task moved to this phase, done at the user's
  request; `~/.claude/settings.json` and `skillOverrides` left its Technical Details. The
  "turn off" part of its Objective is now met, and the README's opening decision on the
  turn-off happened earlier than it says: the closure changelog records both.
- `README.md`, Dependencies: the skill-creator plugin is disabled, and only its cached
  files stay for `grade.py` until Phase 5.
- `phase-5-switch-over.md`: added the task that turns superpowers back on in this
  repository, with the user's go-ahead, and its file in Technical Details.
- `phase-1-agent-conventions.md`: the reader runs as a step of each skill's procedure, not
  through a `!` command, in its task and its Risk & Mitigation, per the script rule; the
  `session_resume.py` task now also looks under `pending/`; a new task makes
  `open-phase.md` refresh the progress block; `open-phase.md` joins Files to Modify, and
  the reader's source is now the shared module chosen here.
- `phase-2-static-audit.md`: the `[skills]` checks also flag the harness features a
  repository excludes, such as `allowed-tools` and `!` commands.
- **Approved by the user on 2026-09-28, applied** — `README.md`: align three statements
  with the principles above.
  - Why This Roadmap Exists: the tool "follows the official documentation and the best
    practices" becomes "builds on the official documentation and the best practices
    without being capped by them".
  - Decisions Taken At Opening: "Platform rules — the official documentation and the
    Agent Skills standard — apply everywhere; conventions apply only where the file
    declares them." becomes "The official documentation and the Agent Skills standard
    inform every rule without capping any: a tool may go past a documented limit when its
    evaluations show it does better. Conventions apply only where the file declares
    them."
  - Deliberately Out Of Scope: "Agents other than Claude Code: the file name is
    agent-neutral, but only Claude Code tools read it." becomes "Installing for agents
    other than Claude Code: every tool is written for the agent, never for Claude, but
    installs into `~/.claude` and is tested with Claude Code only."

---

## Assessment

The phase turned the two sources and the documentation into one decision record: 68
capabilities ruled keep, improve or drop, five rules settled — description, tone,
testing, sizes, scripts — the open questions answered, the names chosen, a license, and
a map of every tie to Claude Code. The rules rest on the sources, the documentation and
measures; where none existed, the record says so and when to revisit.

Three things moved the ground under the later phases. The user set principles that
reframe every rule: this repository's checks and the documentation are evidence, not
limits, and every tool addresses the agent, never Claude, with Claude Code only as
today's install target. Probes contradicted two premises of the plan: `allowed-tools`
grants nothing headless, and `skillOverrides` cannot hide a plugin skill. And both
sources were turned off at the start instead of at Phase 5 — superpowers entirely in this
repository — so the new tool is built and tested without them.

Phase 1 needs to know first: the reader of `.agent-conventions.toml` is a shared module
that skills run as an ordinary step — no `!` command, no `allowed-tools` — with its
permission from the installer's allow rules, and it addresses the agent. Its `[skills]`
table must hold what Phase 2 checks: where skills and evals live, their language, who
they address, and the harness features the repository excludes. It also owns the two
roadmap defects this phase found.
