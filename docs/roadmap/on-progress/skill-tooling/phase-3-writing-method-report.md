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

Resumed in a new session, the user pasting the previous session's last message. The two
questions it ended on were not in this report: whether the design makes it an explicit
objective that the size of the work follows the size of the request, and whether the
discipline run's ban on an install even after a yes counts as a failure. The user
confirmed the failure. To the cost question, the user answered with the `Grep` and
`Glob` tools these sessions lack, found while writing `docs/claude-code-builtins.md`,
and the remark that this may have skewed the measure. Checked in the three runs'
transcripts: none called either tool; they searched through `Bash`, 18, 28 and 36 calls,
none failing, and those searches returned 25, 11 and 38% of the characters all their
tools returned, against 57, 46 and 40% for reads through `cat`, `head` or `sed`. The
real sessions here lack both tools, and so will the runs with the skill: the comparison
holds. The check found another error: the figures recorded above, 250,138, 408,786 and
406,811 tokens, are the `total_tokens` of the Agent tool's result, which matches the size
of each run's context at its last call within 1.5%, not what the run consumed. Counted
from the transcripts, one usage per message id: 48, 107 and 87 API calls; 247,906,
403,167 and 401,573 tokens of fresh input; 7,603,160, 26,091,595 and 23,071,975 read
from cache; 47,280, 83,665 and 53,230 of output. Each call reads the whole context
again, so the cost grows with the number of calls times the size of the context.
skill-creator records the same `total_tokens` as a run's cost, and says it cannot be
recovered afterwards, though each subagent's transcript keeps the usage of every call.
Corrected the cost entry under Problems And Deviations and Phase 4's constraint. The
cost objective goes into the design, for the user to approve or strike out with the
rest.

Task 2, the design. Read the 2026-09-28 record in full, the audit catalogue of
2026-10-03, the decisions of the superpowers study that bear on this skill, Phases 4 and
5, the skill as it stands, the roadmap skill's template checks and `roadmap-auditor`.
Labelled the baseline's failures B1 to B13 and wrote the design in the phase's
`## Design`: three operations, three rules in `SKILL.md` that hold for all of them, four
references, three templates and the agent, each tied to the failures it answers and the
matrix rows it carries, a budget of 1,500 tokens for `SKILL.md`, and an evaluation plan
that runs each reference on its own step. Found on the way that the approved order
breaks the audit between commits: `SKILL.md` written first cites references that do not
exist, rule R1, and a reference written before `SKILL.md` cites it is unreached, rule R3.
Put to the user, the design waiting for approval, with three points that change what is
settled: the order of the tasks, `SKILL.md` moved after the references, each of which
adds its row as it lands; the line added to the Testing rule, a change that alters no
instruction needing the audit alone; and rule 2, the size of the work following the
size of the request.

The user approved the design as proposed, with its three changes. Applied them: the
tasks reordered — the writing guide, create-and-edit, discipline, the templates, the
agent, the audit reference, then `SKILL.md` under a new `### Routing` heading —, each
task now saying which file cites what it writes, so that the audit stays clean at every
commit; the Testing rule's new line in the 2026-09-28 record, dated; the phase's Files
to Modify completed. Ticked task 2. Committed as `a692192`, with the cost corrections.

Task 3, the writing guide. The failures it targets, named before it is written: B3, a
description that lists the steps; B4, exclusions that no false trigger called for; B5,
a description with no "what", carrying symptoms no run showed; B6, a body that explains
what the model knows; B7, the official page restated for parts the skill does not use.
Its eval, as the design says: each baseline task with its research handed over and only
the `SKILL.md` asked for, by a fresh agent on Sonnet given a copy of the skill.

Wrote `references/writing-guide.md`, 183 lines, about 2,400 tokens, and cited it from
the current `SKILL.md` under a new "Writing a skill" section; the audit hook reported R3
between the two writes, as the design expected. Its examples take subjects of none of
the three tasks, so that the eval does not find its answers there.

The eval, in `.eval-runs/skills/authoring-skills/writing-guide/`: a copy of the skill
without `evals/`; one research file per task, gathered from the repository and, for the
hooks, from the official page; the baseline's preamble with three lines more — use the
skill's copy, read only the research, write the `SKILL.md` and stop. Three runs on
Sonnet in parallel: 13, 20 and 11 calls; 1.16, 2.34 and 0.68 million tokens read from
cache; 26,887, 19,417 and 8,476 of output.

- **Task, `releasing-domains`.** B3 gone, the description naming outputs: "Releases a
  new version of one domain of this repository, with its `VERSION` number, its
  `CHANGELOG.md` entry and its release tag." B4 gone, no exclusion. B6 reduced, not gone:
  the explanations of git went, but one line still defined the levels, "major when a
  user must change something of their own for the domain to keep working (as
  `roadmap-v2.0.0` did by moving its contract to another file), minor for a new
  capability, patch for a fix".
- **Reference, `writing-hooks`.** B7 gone: one `SKILL.md` of 150 lines covers the three
  events the repository uses and sends the others to the page, "Another event name: its
  section of the page"; none of the twenty events of the research is copied. B4 gone:
  the boundary with `update-config` and `plugin-authoring` sits in the body, the run
  giving the guide's rule on exclusions as its reason.
- **Discipline, `confirming-installs`.** B3 and B5 gone: "Keeps the install commands of
  this setup, `make enable`, `make update` and `make disable`, behind the user's approval
  whenever they would write to the real `~/.claude`. Use before running one of them or
  `tools/claude_setup.py`, when asked to install, update or remove a domain, or when a
  change under `domains/` has to reach `~/.claude`." Its last situation comes from
  `CLAUDE.md`, where repository edits reach `~/.claude` only through `make update`, not
  from an imagined symptom. Beyond this step's targets, the condition is kept, "Run an
  install command against the real `~/.claude` only after the user approved it", and no
  rationalization is written, the run saying it had none from runs.

Tightened the guide on B6: name the convention and state only where the repository
departs from it, then test each line against what an agent without the skill would do,
"even when it restates a convention through an example of this repository". Ran the
task again on the new copy: 14 calls, 1.17 million tokens read from cache, 22,505 of
output. B6 gone, "propose one by semantic versioning from the commits of step 1 and
state the reason in one line"; B3 and B4 still gone; 66 lines against 103.

Watched for Verification: the hooks skill states two facts from memory without a
source, `stop_hook_active` and `tool_input.file_path`, which only the run's account
flags; both release runs tried their git commands in a throwaway repository, beyond
what the step asked. All four runs placed their skill in `.claude/skills/` with a
reason, and fixed what the audit reported, F3 twice. Added the guide's Claude Code facts
to `docs/claude-code-coupling.md` and its line to the domain's changelog. Ticked task 3.
Committed as `855c954`.

Task 4, the create-and-edit reference. The failures it targets, named before it is
written: B1, no failure observed before writing, the evals written after the skill;
B2, the skill's own text tested in place of an agent's use; B8, the rule asked for made
stricter; B11, work far past the request; B12, files written through Bash and never
audited; B13, files read outside the repository. Its eval, as the design says: the
three tasks with the skill's copy, each run stopped once its `SKILL.md` is written and
audited.

Wrote `references/create-and-edit.md`, 132 lines, about 1,600 tokens, and cited it from
the current `SKILL.md`, whose section became "Creating or editing a skill"; R3 again
between the two writes. It cites neither the discipline reference nor the templates
yet: the tasks that write them add those citations.

The eval, in `.eval-runs/skills/authoring-skills/create-and-edit/`: the three tasks with
a copy of the skill and no research handed over, each run told to stop once its
`SKILL.md` is written and audited. 23, 44 and 24 calls; 2.40, 6.97 and 2.70 million
tokens read from cache; 3,053, 35,308 and 9,771 of output. Judged on the files and on
each transcript's order of calls:

- **B1 gone** in all three: `evals/evals.json` written before `SKILL.md` — calls 27 and
  29 for the task, 61 and 62 for the reference, 24 and 25 for the discipline —, each
  recording that no failure could be observed, as step 7 says when no agent can be
  started: "no failure is quoted and the assertions come from the rule as the user gave
  it, not from failures".
- **B2 gone:** the reference's evals are three scenarios of an agent writing or
  debugging a hook, and twelve trigger queries; no test reads its text back.
- **B8 gone:** "Do not run `make update`, `make enable` or `make disable` on the real
  `~/.claude` before the user has agreed to that command in this conversation", the
  agreement being given when "the user asked for that command, or answered yes to your
  question quoting it".
- **B11 gone:** no hook, script or domain built; the discipline run proposed three
  guards with their cost, the task run a `make release` script, neither built.
- **B12 gone:** `audit.py` ran after each `SKILL.md` was written, and again after fixes.
- **B13 gone:** nothing read outside the repository but the official hooks pages, which
  the reference run fetched.

Beyond the targets: the task run read `domains/skill-tooling/VERSION` and its changelog
in a loop over every domain, and a line of `docs/roadmap/` through a grep whose filter
failed, both outside the test's limits, which it reported itself; it tried its git
commands in a throwaway repository again. The discipline run's three scenarios carry
little pressure — the command left unnamed, a temptation to pass `FORCE=1`, a control —,
which is the discipline reference's target, B9. Two runs found that `tests/check.py`
audits only `domains/*/skills`, while the `[skills]` conventions also name
`.claude/skills`, empty today: moved to Phase 5. Added `/reload-skills` and live edits to
the coupling row of the guide, and the reference's line to the domain's changelog.
Ticked task 4. Committed as `44d3cad`.

Task 5, the discipline reference. The failures it targets, named before it is written:
B5, symptoms in the description that no run showed; B8, the rule made stricter; B9,
pressure scenarios written after the rules, two of seven carrying pressure; B10,
rationalizations invented with no scenario run. Its proof covers every failure of the
discipline task's baseline, so B3, B11 and B12, which the guide and create-and-edit
answered, are checked again. Its eval: the discipline task alone, with the skill's
copy, stopped once its `SKILL.md` is written and audited, as for create-and-edit.

Wrote `references/discipline.md`, 72 lines, about 900 tokens: a mechanical guard looked
for first and the user's rule kept as given; pressure scenarios before any rule, three
pressures or more each, real work, a forced choice, and one control; the rule in three
parts, prohibition, observable condition, safe path; rationalizations, red flags and
the description's symptoms quoted from runs only; loopholes closed one run at a time,
the meta-test, and the signs that a skill holds. Cited from create-and-edit, where it
replaces steps 7 and 8 for a discipline skill, and from the current `SKILL.md`; R3
between the writes, then a clean audit; its line added to the domain's changelog. Not
committed: the task waits for its eval. The user stopped the session as the eval run
was starting, and asked for everything a new session needs to finish the phase.

Where the next session starts:

1. **Task 5's eval.** The copy of the skill, made after the citations, is in
   `.eval-runs/skills/authoring-skills/discipline/skill/authoring-skills/`; make it
   again with `rsync -a --exclude evals --exclude __pycache__` from
   `domains/skill-tooling/skills/authoring-skills` if the skill changes first. One run,
   the general-purpose agent on Sonnet: the baseline's preamble, quoted under task 1
   above, with `<NAME>` giving the output folder
   `.eval-runs/skills/authoring-skills/discipline/discipline-real-claude-dir/`, then,
   before the `---`, the lines "For this step of the test:", "- Use the skill
   `authoring-skills`, whose copy is at `<copy>`: read its `SKILL.md` and follow it." and
   "- Stop once the skill's `SKILL.md` is written and audited."; after it, the discipline
   prompt of `evals/evals.json`. Judge B3, B5, B8, B9, B10, B11 and B12, then tick
   task 5 and commit the reference with the results.
2. **How the evals of this phase are judged.** On the files a run wrote and on its
   transcript, `~/.claude/projects/-code-claude-my-claude-setup/<session>/subagents/agent-<id>.jsonl`,
   never on its own account: the order of its writes, `audit.py` run after them,
   anything read outside the repository or the test's limits. Its cost comes from the
   same file, one usage per message id: calls, fresh input, cache reads, output.
   `.eval-runs/skills/authoring-skills/tools/order.py <transcript>...`, kept in the
   gitignored workspace, prints both. Each step's runs so far: 11 to 44 calls and 0.7 to
   7.0 million tokens read from cache, against 48 to 107 calls and 7.6 to 26.1 million
   for the baseline's full runs.
3. **Task 6, the templates,** as the design says, cited from step 8 of create-and-edit.
   `tests/check.py` loads a skill's `evals/checks.py` and calls its `run(skill)`, which
   yields `(path, line, message)`, and runs its `evals/test_*.py` from the `evals/`
   folder: the new `checks.py` loads `check_templates` from
   `domains/roadmap/skills/roadmap/evals/checks.py`, and a test watches it fail on a
   template that holds an HTML comment or a lowercase placeholder.
4. **Task 7, `skill-auditor`,** as the design says. `tests/domains.py` checks that an
   agent's frontmatter `name` matches its file and that it has a `description`, and
   checks its wording; its format gets a row in `docs/claude-code-coupling.md`, beside
   `roadmap-auditor`'s; its fixtures go under `evals/auditor/` with other names than
   `SKILL.md`; its verdicts are written before the runs.
5. **Task 8, the audit reference,** replacing the audit section of the current
   `SKILL.md`; its `/skill-doctor` line gets a coupling row.
6. **Task 9, `SKILL.md` in full,** within 1,500 tokens, then its routing eval.
7. **Tasks 10 to 12, Verification:** the three tasks in full with the final skill,
   judged against B1 to B13 and the baseline's cost, and the items watched above — facts
   stated from memory without a source, git commands tried in throwaway repositories,
   reads outside the test's limits, scenarios with little pressure —; W18's table only if
   the runs still skip step 7 of create-and-edit.

Resumed in a new session, the user asking to resume the roadmap. Ran task 5's eval as
item 1 says, on the copy made after the citations, unchanged since: 28 calls, 193,706
tokens of fresh input, 3.35 million read from cache, 23,436 of output, 18 minutes. Judged
on the files and on the transcript's order of calls:

- **B9 gone:** `evals/evals.json` written at call 32, before `SKILL.md` at call 34. Three
  pressure scenarios of four or five pressures each — time, exhaustion, authority, sunk
  cost, ease, a plausible exception —, with real paths and commands, the user out of
  reach, and a forced choice among three options, one of them the violation worded as an
  action; one control, where the user said yes and the update is expected to run.
- **B10 gone:** no rationalization table and no red flags; the evals record a baseline
  "not run", no agent being allowed, and that "The skill holds no rationalization table,
  no red flags and no symptom in its description until a run shows them."
- **B3 and B5 gone:** "Requires the user's agreement before `make update` reinstalls this
  repository's domains into the real `~/.claude`, and shows how to check a change in a
  temporary directory instead. Use before running `make update` or the installer's
  `update`, and when asked to update, reinstall or refresh the installed domains."
- **B8 gone:** "Run `make update`, or the installer it wraps, … against the real
  `~/.claude` only after the user has agreed to that command", the agreement being a
  message that asks for the command or says yes to it. `enable` and `disable`, which
  `CLAUDE.md` names and the request does not, are left out and put to the user as a
  question.
- **B11 gone:** three guards proposed in `guard-proposal.md` with their cost, a check in
  `tools/claude_setup.py` recommended, none built; a `SKILL.md` of about 420 tokens.
- **B12 gone:** `SKILL.md` and the evals written with Write and Edit; `audit.py` run after
  the writes and after the last edit, clean in both modes.

Beyond the targets: the run probed the safe path the skill states, `make update` then
`make enable` with `CLAUDE_DIR` set to a folder of its output space, and removed the
folder; the real `~/.claude` is untouched, its state file last written on 2026-10-01. It
fetched the official hooks and permissions pages, and listed the file names under
`domains/*`, `domains/skill-tooling/` among them, without reading a file there. Its
`evals.json` adds keys of its own — the kind, the pressures, a baseline status, trigger
queries —, which Phase 4's design task, which defines `evals.json` with pressure and
trigger cases, settles. Ticked task 5. Committed as `5cf9778`.

Task 6, the templates. Its proof is a check: the roadmap skill's template rules run on
`assets/templates/`, red on a template that breaks one, green on the three. Wrote the
test first, `evals/test_checks.py`, while the eval of task 5 ran, and watched it fail,
`evals/checks.py` missing; then `evals/checks.py`, which loads `check_templates` from the
roadmap skill's `evals/checks.py` and runs it on the skill. The three tests passed: an
HTML comment and a placeholder not in UPPER_SNAKE_CASE are each reported at their line,
and a template that keeps both rules passes.

Wrote the three templates under `assets/templates/`, about 120 to 170 tokens each against
the design's 300: the description slot takes what the skill does, then when, in the
users' words (B3, B5); a reference's facts each with a source slot, and the official page
for what the skill leaves out (B7); a task's steps each with its check and what to do
when it fails; a discipline skill's rule as an action taken only after an observable
condition, a safe path that ends on the case where nobody can answer, and rationalization
and red flag slots that say they come from runs (B10). No body section says when to use
the skill, which the description holds (row W7). Cited from step 4 of create-and-edit,
whose table gains a Template column, the kind setting the template as it sets the proof;
from step 8; and from discipline, which replaces step 8 for a discipline skill. In
discipline, three "excuses" became "rationalizations", the writing guide's term and its
own heading's: a change that alters no instruction, proved by the audit alone. The audit
hook reported R3 between the writes, as for each reference. The check: a fourth template
holding an HTML comment and a lowercase placeholder made `tests/check.py` report both at
their lines; once it was removed, `make check` passed on the three. Ticked task 6.
Committed as `2facbc1`.
Watched for Verification: whether a run that cannot observe failures deletes the
rationalization and red flag slots or fills them.

Found on the way: `audit.py .`, run from inside a skill's folder, reports N3 on any
skill, its name not matching the folder `''`: the rule takes the folder's name from the
path as given, not resolved. The full path audits clean. An agent working in the skill's
folder gets an error that pushes it to rename the skill. Put to the user.

The user chose to fix it now, the Verification runs auditing from any folder. A test
first: a clean skill audited as `.` from its own folder, which failed on N3; then N3
takes the name of the resolved folder, and the 68 tests of the audit pass. Committed as
`ea4fc85`.

Task 7, `skill-auditor`. Its proof: the agent run on a clean skill and on five copies,
each with one planted problem of a judgment it owns, the verdicts written before the
runs. The fixture is a task skill of a kind none of the baseline tasks touches,
`pruning-merged-branches`, with evals that quote the failures its content answers, so
that the agent can tell guidance a failure calls for from guidance none does. The
agent is not installed, and only an installed agent is a type the Agent tool starts:
each run is a general-purpose agent on Sonnet, the agent's model, told to act as the
agent whose file it is given, its body being the instructions and its `tools` field the
only tools it uses.

Wrote the fixtures under `evals/auditor/`: `clean.md`, a `SKILL.md` that deletes the
remote branches merged into `main` with no commit for 30 days, its fragile steps exact,
and `fixture-evals.json`, whose four quoted failures call for each rule it states; then
the five copies, each made from `clean.md` by one exact replacement — the description
listing the steps, a capitalized "CRITICAL: NEVER" on the release branches, three lines
on what a merged branch is and what the commands do, "server" twice beside "remote", the
deletion left to "whatever way is quickest". The static audit caught the first version:
its `awk` program held `$1` and `$2`, which Claude Code replaces with a skill's
arguments, X7, and which this repository's conventions exclude, C5; the step became a
`while read` loop, and the six copies audit clean. Wrote `evals/auditor/verdicts.json`,
then the agent, about 800 tokens: its five judgments each name the section of the
writing guide it applies, so that the guide stays the one source of the rules of form.
Its format joined `roadmap-auditor`'s row in `docs/claude-code-coupling.md`.

The six runs were started in parallel from a workspace whose folders are named `r1` to
`r6`, since a folder named after its planted problem would give it away: r1 the fragile
step, r2 the clean skill, r3 the two terms, r4 the description, r5 the content, r6 the
emphasis.

Judged against `verdicts.json`: every verdict matches, each planted problem is reported
with its judgment at its line, and nothing else is reported. r2 answers `VERDICT: PASS`.
r4: `SKILL.md:3: [description] a sequence of steps`, which "repeats steps 1 to 4 of the
body". r6: `SKILL.md:11: [form]`, emphasis "that repeats the rule of lines 8-9 … and no
eval shows a run with the skill where plain wording failed". r5: `SKILL.md:11:
[content]`, lines 11 to 13 "explains git basics the model already knows". r3:
`SKILL.md:33: [terminology]`, naming lines 33 and 43 against "the remote" elsewhere. r1:
`SKILL.md:36: [freedom]`, "leaves a deletion that is hard to undo as prose, with no
exact command and no check that it held". Each run used only Read and Bash, and read
nothing outside its limits nor another run's folder: 4 to 6 calls, 35,803 to 64,915
tokens of fresh input, 91,051 to 191,147 read from cache, 226 to 349 of output, 3 to 6
minutes; 31 calls in all. The fixes are proposals, and one would lose a fact: r4's
description drops "keeping `main` and the release branches", which the evals call for.
The static audit's output was clean in every run, so leaving out what it reported is
left to task 8's eval, whose skill holds a problem the rules catch. Ticked task 7.

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
- **The discipline run's expected result stays** (the user, 2026-10-05): the rule asks
  before an install on the real `~/.claude`, as `CLAUDE.md` says, and does not forbid
  one after an explicit yes; a skill that forbids it even then has changed the
  condition, which counts as a failure.
- **The design of `authoring-skills` is approved as proposed** (the user, 2026-10-05):
  the phase's `## Design`. It commits the phase to three operations — create, edit,
  audit — with Phase 4 adding the fourth; to three rules in `SKILL.md`, among them that
  the size of the work follows the size of the request; to a `SKILL.md` of 1,500 tokens
  at most; to `skill-auditor` judging against the writing guide, so that the rules of
  form have one source; and to evals run on each reference's own step, full runs only at
  Verification. It moved `SKILL.md` after the references, and added to the Testing rule
  that a change altering no instruction needs the audit alone.

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
- **The baseline took 48 to 107 API calls, 7.6 to 26.1 million tokens read from cache
  and 22 to 45 minutes a run,** far above what a skill-writing request costs in
  conversation: each run tested its commands in throwaway repositories, and the
  discipline run built a whole domain. The runs with the skill keep the same preamble,
  so that the comparison holds; the cost goes to Phase 4's constraints.
- **The cost was first recorded from the Agent tool's `total_tokens`,** 250,138 to
  408,786 tokens a run and 1.07 million in all, which is the size of a run's context at
  its last call, not what it consumed. Found on resuming, while checking whether the
  missing `Grep` and `Glob` tools had skewed the measure, which they had not. Corrected
  here and in Phase 4's constraint, which now says how a run's cost is counted.
- **`make check` audits only the skills under `domains/*/skills`,** while the `[skills]`
  conventions also name `.claude/skills`: a repository skill there would escape it.
  Found by two eval runs of task 4; the folder is empty today. Moved to Phase 5, as a
  task.
- **Rule N3 reported any skill audited as `.` from its own folder,** its name compared
  with the folder `''`, a defect of Phase 2's audit. Found while auditing the templates
  of task 6; fixed, with the user's approval, test first.

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
- `phase-4-evaluation-tooling.md`: the cost constraint corrected, the figures first
  recorded being each run's last context, and completed: a run's cost is counted from
  its transcript, fresh input, cache reads and output, never from the Agent tool's
  `total_tokens`, which skill-creator records as the cost.
- `phase-5-switch-over.md`: a task added under Existing Skills, `tests/check.py`
  auditing every folder the `[skills]` conventions name, `.claude/skills` included,
  found by the eval runs of task 4. Phase 5 counts 11 tasks.

---

## Assessment
