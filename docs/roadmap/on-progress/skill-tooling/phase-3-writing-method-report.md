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
domain's changelog say so. Committed as `58e5eb0`, after `6ce08ad`, which holds
`docs/claude-code-builtins.md` and the task added to `roadmap-dependencies`.

Task 1, the baseline. Wrote the three tasks and what a good result holds into
`authoring-skills/evals/evals.json`, as approved, then gave each to a fresh subagent on
Sonnet, `claude-sonnet-5-5`, in parallel, the user's prompt in French after this
preamble, `<NAME>` being the eval's name:

```
You are working in the repository /code/claude/my-claude-setup. The user's request is at the end, after the line ---.

Work as in a real session, within these limits, which come from the test setup and not from the user:
- Write every file you create under `/code/claude/my-claude-setup/.eval-runs/skills/authoring-skills/baseline/<NAME>/`, and nowhere else: not elsewhere in the repository, not under `~/.claude`. In your final answer, say where the skill would live in the repository, and why.
- Do not use the Skill tool.
- Do not start other agents or `claude -p` sessions: describe any test you would run instead of running it.
- Do not read `docs/decisions/`, `docs/roadmap/` or `domains/skill-tooling/`.
- The user cannot answer during the task: where you would ask a question, write the question and the assumption you take, then go on.
- End with a short account: what you wrote and where, what you checked, the questions and assumptions, what you would do next.

---
```

The runs cost 250,138, 408,786 and 406,811 tokens, in 22, 37 and 45 minutes; none
called the Skill tool. Judged against the files, the audit and each transcript's order
of calls, not against the runs' own accounts. All three skills audit without an error.

**Task, `release-domain`** (`SKILL.md` 122 lines, 6 scenarios). Met: it read the
repository first, 31 calls before its first write, and wrote six questions with the
assumption taken; it placed the skill in `.claude/skills/`, since the skill serves only
here; its steps come in order with their checks, the tag on `main` after the merge; no
emphasis; the audit hook caught F3 and N7 on the way. Failed:

- The description lists the steps: "Picks the X.Y.Z version, writes the CHANGELOG.md
  entry, sets VERSION, runs the checks, commits, tags it on main with a name like
  roadmap-v2.0.0, and pushes when asked."
- The body explains semantic versioning and git: "Major: someone who uses the domain has
  to change something, because a contract or a file format moved, or a skill, agent, hook
  or command was renamed or removed"; "The two numbers are the commits only origin has,
  then the commits only `main` has."
- Its evals came after the skill, `SKILL.md` at call 37 and `evals.json` at call 45, from
  imagined scenarios, and the comparison only after them: "Lancer ensuite chaque scénario
  deux fois, avec le skill (copie sans `evals/`) et sans lui".

Outside the expected results: an exclusion that no false trigger called for, "Not for
installing a domain (make update), and never on the agent's own initiative, since a
release commits and tags."

**Reference, `claude-code-hooks`** (`SKILL.md` 88 lines, three references, an asset, task
and trigger evals). Met: every specific of the repository, `{{HOOKS_DIR}}`, the
installer's merge, the scripts found by walking ancestors, the stdin tests, the pitfalls
of `CLAUDE.md` and the coupling page; a short `SKILL.md` that says which reference to read
when; the description's what and when; evals of an agent's use proposed; no audit error,
one warning, N8, for `claude` in the name, the hook having caught N7, R1, C2 and C4 on
the way. Partly met:

- Sources: each fact is marked seen or documented, and the official page is linked
  once, `references/events.md:187`, but the same file restates that page for events the
  repository does not use.
- Its own text tested first: `evals/test_checks.py` and `evals/checks.py`, 19 tests that
  its examples parse and its cited paths exist, came before `SKILL.md` (calls 70 and 73
  against 76); the evals of an agent's use came after (call 91).

Outside the expected results: three exclusions that no false trigger called for, "Not
for other settings.json changes such as permissions or environment variables, not for
plugin mods written as function hooks, and not for git hooks."; it read session
transcripts outside the repository, one command refused by the classifier as personal
data.

**Discipline, `installing-the-setup`** (`SKILL.md` 65 lines, 7 scenarios, a hook). Met:
a mechanical guard considered first, "Un skill seul ne peut pas « empêcher » … Ce qui
empêche, c'est un hook PreToolUse qui refuse la commande"; the safe path through
`CLAUDE_DIR`; no emphasis; no audit error. Failed:

- The scenarios came after the rules, `SKILL.md` at call 59 and `evals.json` at call 62,
  and two of the seven carry pressure.
- The condition changed: the user's rule asks before an install, the skill forbids one
  even after a yes, "So the agent never runs these commands against the real directory:
  whoever asked, however small the update looks".
- The rationalizations are invented, no scenario having run: under "What does not change
  the rule", "\"The user said to go ahead\"", "\"It is only an update of a domain that is
  already installed\"", "\"Another route gets there\"", "\"A trial is not the real
  thing\"".
- The description opens on "Use before" with no "what", carries symptoms no run showed,
  and ends on the workflow: "when an installed copy looks stale, when a change should be
  tried live, or when a tool's message says to run make update. Only the user changes the
  real ~/.claude. The agent looks with make list, tries in a throwaway directory and hands
  the exact command over."

Outside the expected results: a new domain, `install-guard`, for a one-line request — a
hook of 646 lines, 52 tests in 398, 17 mutations, 240,000 fuzzed inputs; and files
written through Bash, which the audit hook does not see, only `SKILL.md` going through
Write.

What the three share: none watched a failure before writing, each wrote its skill and
then evals from imagined scenarios; their descriptions break the 2026-09-28 rule three
ways, listed steps, exclusions or symptoms nothing showed, no "what"; and all three read
the repository first, gave a reason for their placement, and fixed what the audit hook
reported. Checked a claim of the task run: with `TMPDIR` inside this repository, five
tests fail, two of the audit's and three of the conventions reader's, since they assume
a temporary folder outside any repository with `.agent-conventions.toml`. Ticked task 1.
Committed as `f9c9191`.

The user had run the script: the three settings entries are gone. Committed
scriptorium's `.claude/settings.json` alone, as `3dcd3ff`, its 20 files of work in
progress untouched. Then the plugin removal reached this repository: the decision
record `docs/decisions/2026-10-04-plugins-removed.md`, with the plugins' figures; a note
in the 2026-10-01 record that its turn-off plan is superseded; step 6 of
`grade.py` reading skill-creator's scripts from `study/`; `CLAUDE.md`'s gotcha on plugins;
the coupling page, which loses the plugin cache; this roadmap's README dependency and
Phase 5; and roadmap `working-method`, whose last phase loses its three turn-off tasks,
its README moving to 1.0.1.

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
- **Every plugin is uninstalled, with its cache and marketplace** (the user, 2026-10-04):
  none serves this setup any more, and each pollutes contexts and tests; the other
  repositories wait for this repository's roadmaps. The sources stay under `study/`, and
  the record `docs/decisions/2026-10-04-plugins-removed.md` replaces the turn-off plan of
  2026-10-01. The runs of Phases 3 to 5 start without any plugin.
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
- **The repository's tests depend on where `TMPDIR` points:** with it inside this
  repository, five fail, two of the audit's and three of the conventions reader's,
  because the conventions lookup climbs to this repository's `.agent-conventions.toml`.
  Found by the task run of the baseline, checked here. Moved to Phase 4, whose runs may
  set it, as a constraint.
- **The baseline cost about 1.07 million tokens and up to 45 minutes a run,** far above
  what a skill-writing request costs in conversation: each run tested its commands in
  throwaway repositories, and the discipline run built a whole domain. The runs with the
  skill keep the same preamble, so that the comparison holds; the cost goes to Phase 4's
  constraints.

---

## Changes To Later Phases

- `phase-4-evaluation-tooling.md`: its design task writes the design in the phase's
  `## Design`, citing a decision record where the section is not enough, rather than in
  `.superpowers/specs/`, which the superpowers study set aside, as Phase 3's design task
  already reads.
- `phase-5-switch-over.md`, as the user approved on 2026-10-04: the task that turned
  skill-creator off in scriptorium's local settings is removed, with its line under Files
  to Modify, since every plugin is gone; the task that moves `grade.py` now moves it
  from the copy of skill-creator under `study/`. Phase 5 counts 10 tasks.
- `phase-4-evaluation-tooling.md`: two constraints from the baseline — the tests that
  fail with `TMPDIR` inside the repository, and the cost of a realistic run, 250,000 to
  410,000 tokens and 22 to 45 minutes on Sonnet, so that its design says how many runs a
  benchmark starts.

---

## Assessment
