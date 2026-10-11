# Phase 2 Report: Static Audit

**Phase:** [phase-2-static-audit.md](phase-2-static-audit.md)
**Start Commit:** a8acdf1

---

## Work Log

### 2026-10-03

Opened the phase, the roadmap having resumed once roadmap `superpowers-study` closed
(commit `a8acdf1`). Read Phase 1's file and its report in full: no restructuring
pending, and no other phase in progress. What binds this phase: Phase 1's decisions —
this repository's `[skills]` table, read through `conventions.py skills`, whose
workspace the reader does not check for being ignored, a check this phase owns —; the
2026-09-28 record's rules, budgets and names, the domain being `skill-tooling`, and its
gap on PyYAML, which this phase's parser decision covers for `tests/skills.py`,
`tests/domains.py` and `domains/review/tests/test_reviewfile.py`; and, since this phase
was written, the decisions of the superpowers study: a phase's design in its
`## Design` section or a decision record rather than `.superpowers/`, each task's
declared proof, a commit per task, test-first for code and scripts. At the user's rule,
the opening ends the turn: no work on the phase yet.

Put two points to the user: where the rule catalogue goes, since the first task named
`.superpowers/specs/`, and whether this phase, written before the study, takes a
`Proof:` line per task. The user approved both. Reworded the first task, added a
`## Design` section citing the record to be created, and listed it under Files to Modify.
Drafted a proof for each of the 13 tasks, naming its object, and put them to the user;
the dev hook having no test yet, its task's proof creates its test file. The user
approved the 13 proofs as proposed; wrote each on an indented `Proof:` line under its
task.

Started on the two design tasks together, since both feed the same record. Read the
2026-09-28 record, `tests/skills.py` and the `[skills]` schema, and fetched the skills
page, the Agent Skills specification and the best practices as Markdown: the frontmatter
reference still lists 20 fields; the specification adds that `name` has no doubled,
leading or trailing hyphen; the best practices forbid `anthropic` and `claude` in a name
and XML tags in name and description.

The parser probe, in `study/frontmatter-probe/`: a corpus of 39 distinct `SKILL.md` —
this repository's two, 27 from the plugin caches, 10 from scriptorium — and 35 controls.
`claude plugin validate` found no component until pointed at a folder named `skills`,
and then reported 8 controls: a missing or unclosed block, a `...` closer, an unclosed
quote, a list, a numeric name, `metadata` not a map, no description; never an unknown
key, a value out of range or a name rule, even with `--strict`. Claude Code's parser
read what YAML forbids — a `: ` inside a plain value, a reserved indicator first, a tab,
a duplicated key — and so passed scriptorium's `session-review`, whose description
PyYAML rejects. Wrote a subset parser prototype; three fixes brought it in line with
Claude Code on what Claude Code refuses (only `---` closes; a byte order mark passes;
plain scalars typed by YAML 1.2). It then gave PyYAML's values on every real
frontmatter, the agents' included, and on every control both parsed but `yes`. A
literal block first differed by a final newline: the comparison's extraction dropped
it, not the parser. The review files use a richer YAML — keys with `:` and `/`, nested
flow mappings — that the subset does not read; `test_reviewfile.py` keeps PyYAML only as
an outside reader of that format.

Drafted `docs/decisions/2026-10-03-skill-audit-rules.md`: severities and profiles, the
parser decision with the probe's table, 46 rules in seven families, the mapping of
`tests/skills.py`'s checks, and what the rules find here. Checking that last part
against the files changed two rules: the roadmap skill says "run with `python3`" once,
in prose, so a script cannot be judged "called by its path" line by line, and
`tool-review` cites the modules its scripts import. X2 now reads the shebang: with one, a
script needs the executable bit; without one, another script imports it. Found that way:
two errors, `progress.py` and `check_links.py` without the bit, and one warning of X3,
`close-phase.md:192`.

Put the catalogue to the user with six points to settle — F3's lax YAML an error in both
profiles, T1 a warning, the template rules moved to the roadmap skill, the executable bit
set when X2 lands, `checks` run only under `--checks`, a task added for PyYAML — and,
at the user's request, a French translation in `local-review/`, which git ignores. The
user asked whether to read the rest of the superpowers-study matrix first; advised
against mixing the two reviews: its kept rows come back in each follow-up roadmap's
Framing phase, its 69 drops are the ones worth reading, before `working-method` turns
the plugin off.

### 2026-10-04

Resumed in a new session. The user approved the whole catalogue and the six points.
Recorded the approval in the record. Task 1's proof, `review`: the catalogue approved on
2026-10-04 before any check is written. Task 2's proof, `probe`: the subset prototype,
PyYAML and `claude plugin validate` run on the 39 skills, the agents and 35 controls,
recorded in the record's Parser section. Ticked both. Added the approved task that takes
PyYAML out of `tests/domains.py` and `test_reviewfile.py`, with its proof, and listed
the files the decision touches under Files to Modify. Committed as `75ae69e`.

Task 3, the domain. Its proof, `check`: with `domains/skill-tooling/` holding only an
empty `permissions.json`, `make check` failed on "missing VERSION file" (exit 2), and
the dev hook reported it too; with `VERSION` at 0.1.0 and a changelog whose first entry,
"0.1.0 — unreleased", Phase 5's release will date, it passed. The allow list stays empty
until a script needs a rule, since `tests/domains.py` refuses a rule naming a path the
domain does not hold. Committed as `6ff5faa`.

Task 4, the frontmatter checks. First the parser, `shared/frontmatter/frontmatter.py`,
from the probe's prototype: 22 tests written first ran against an empty stub, 29
assertions failing; then the module, all passing. On the probe's 74 files it gave the
same verdicts and values as the prototype. Then the audit: the skill
`domains/skill-tooling/skills/authoring-skills/`, with a short `SKILL.md` on the audit
alone, which Phase 3 rewrites, and the parser copied into its `scripts/` by hand, since
`tools/shared.py` would also have copied `conventions.py`, which only the `[skills]`
rules of task 9 use. Its proof, `test`: 23 tests, one skill per rule F1 to F13 — no
opening `---`, an unclosed block, five lax YAML forms, an anchor, a list, unknown and
misspelled keys, the six standard fields under `--portable`, wrong types and values,
the boolean forms, `metadata` and `allowed-tools` under `--portable`, `compatibility`'s
length, the fork-only fields, a `metadata` key named like a field, a skill nobody can
invoke, a comment cutting a value — and the command's exit codes and output, ran
against a stub returning nothing, 33 assertions failing; then `audit.py`, all passing,
and `make check`. This repository's three skills audit clean on these rules;
scriptorium's `session-review` reports F3 on its line 3. The dev hook pasted every
traceback of the red runs into the conversation, hundreds of lines, which task 13
addresses. Committed as `7a4081b`.

Task 5, the name and description rules. Its proof, `test`: ten tests — a portable skill
without a name, six malformed names, a name unlike its folder, three reserved names, a
missing, empty or blank description, 1,025 characters, an angle bracket, a name holding
`claude`, a `when_to_use`, and `description` with `when_to_use` past 1,536 — failed
before the rules existed, 19 assertions; then `check_names`, all 33 tests passing, and
`make check`. The red run showed an empty `description:` reported by F7 as "got
nothing": F7 now leaves a null description to N5. N4 follows the documentation rather
than the catalogue's shorthand: a folder or name is reserved when it is `synced` in any
case, `anthropic-skills`, or starts with `anthropic-skills:` — the colon form Claude Code
skips — so `anthropic-skills-tools` is left to N8's warning. Committed as `585a8b8`,
and the record's N4 row stated the same way in `5105131`.

Task 6, the size rules. Its proof, `test`: a body of 20,006 characters against one of
20,001, 501 lines against 500, a 300-line reference without `## Contents` against one
with it and one of 299 lines, and a reference reached only through another — four
tests that failed before the rules, then passed with `check_sizes`, and `make check`.
Lines are counted as the file's lines, so a final newline adds none, where
`tests/skills.py` counted one more. The citations Z4 follows — paths under
`references/`, `assets/` and `scripts/` — are the ones `tests/skills.py` finds; task 7
widens them to relative links. Committed as `ff218cf`.

Task 7, the resource rules. Its proof, `test`: a missing file cited by path and by link,
a citation leaving the skill, two orphan files, and a backslash path failed before the
rules, 5 assertions; then `check_resources`, passing. Run on the corpus, R3 reported 192
files, nearly all false: files outside the three folders cited by path (`agents/`,
`prompts/`, root companions), dotted imports (`from scripts.utils import`), paths behind
`${CLAUDE_SKILL_DIR}/` or a plugin prefix, extensionless scripts, a cited folder; and R1
took example links inside code blocks and `<placeholder>` links for missing files. Each
became a test that failed, then passed: reachability now counts any path of the skill a
reached file names, or its tail, a name the skill holds once, a cited folder, dotted and
relative imports; R1 skips links in code blocks and links holding `<`. What stays on the
corpus is what the 2026-10-01 record already called cited nowhere — `CREATION-LOG.md`,
the pressure tests, the two reviewer prompts, `gemini-tools.md` — scripts scriptorium
runs only through `make`, `LICENSE.txt`, which skill-creator never names, and the
example paths of `writing-skills` and scriptorium, which the 2026-09-28 record already
counted as misfires of R1. The record's R1 and R3 rows now say how citations are read.
47 tests and `make check` pass. Committed as `4d51616`.

Task 8, the execution rules. Its proof, `test`: an injected command inline and in a
block, against one ending in `|| true` and one not after a space; a script with a
shebang but no executable bit, then a module nothing imports; `python3 scripts/run.py`;
`Bash(gh *)` with no `gh` in the body; `@references/guide.md`; `ultrathink`; `$1.00` and
`$ARGUMENTS` — nine assertions failing before the rules, then `check_execution`,
passing. X7 was narrowed while writing its test: an amount such as `$1.00` is always
reported, `$ARGUMENTS` or `$1` only where the skill declares neither `arguments` nor
`argument-hint`, since a skill taking arguments writes them on purpose; the record's
row says so. On this repository the rules found what the record foresaw — X2 on the
roadmap skill's `progress.py` and `check_links.py`, X3 on `close-phase.md:192` — and the
two scripts got their executable bit, no instruction changed. On the corpus, a package's
`__init__.py` was reported as imported by nothing: a test, then the fix. Scriptorium has
22 scripts with a shebang and no executable bit, errors of X2 there until a `chmod +x`.
55 tests and `make check` pass. Committed as `bf4b528`.

Task 9, the convention rules. The skill now holds `conventions.py` and
`references/conventions.md`, copied by `tools/shared.py`, and `SKILL.md` cites them; the
audit reads `[skills]` through the reader and applies no convention rule without a
valid table. Its proof, `test`, on real git repositories: a skill outside `dirs`, a
`test_*.py` outside `evals/`, French words and a space before `%`, a named model
against "Claude Code", each of the three excluded features, a workspace git does not
ignore, then ignores, and `checks = ["false"]` with and without `--checks` — eight
assertions failing and one error before the rules, then `check_conventions`, all 63
tests passing. C6 runs for every skill, and the command removes repeated problems, so
a repository is reported once. On this repository, with its conventions, the three
skills hold no error; `--checks` runs `make check` in about 4 s. Committed as `33743be`.

Task 10, `tests/skills.py` onto the audit. First the last rule, T1, with two tests that
failed — three wordings reported, "old version" and "previous version" allowed — and the
template rules moved into the roadmap skill's `evals/checks.py`, with two tests that
failed there; then T1 in the audit, the template rules in `check_templates`, and
`tests/skills.py` rewritten to delegate: `run()` yields the audit's errors, `warnings()`
its warnings, and `tests/check.py` prints warnings without failing. The wording checks
`tests/domains.py` applies to agents stay in `tests/skills.py`, with T1's narrower
pattern; it no longer imports PyYAML. Its proof, `check`: `python3 tests/check.py` here,
on `writing-skills` 6.4.1 and on skill-creator `fa59bc903774`, before and after.

| | Before | After |
|---|---|---|
| This repository | 0 problems | 0 problems, 1 warning: X3 on `close-phase.md:192` |
| `writing-skills` | 20 problems | 13 errors, 8 warnings |
| skill-creator | 11 problems | 3 errors |

Every earlier problem is still reported, or changed as the catalogue decided:
`writing-skills`' two `references/*-tools.md` citations are now R2 warnings, citations
leaving the skill; its 500-line alert and its `Legacy` and `deprecated` are warnings, Z2
and T1; its duplicated `tool.sh` is reported once; two `ooxml/scripts/*.py` paths, which
name a folder of the example and not the skill's `scripts/`, are no longer read as
citations. Skill-creator's nine unreachable scripts are reached through `-m` module names
and imports, as the 2026-09-28 record asked; its "old version" is allowed, as the
catalogue decided; Z3 still reports `schemas.md`. New rules add Z1 on both — 6,595 and
8,156 tokens — R2 and R4 on `writing-skills`, and R3 on skill-creator's `LICENSE.txt`,
which nothing names. `make check` passes, the X3 warning printed. Committed as
`02c65a1`.

The added task, PyYAML out of the last two files. Before it, `git grep -l "import yaml"`
listed `tests/domains.py`, `test_reviewfile.py`, and this phase file, whose proof line
quotes the import: the command now reads `-- '*.py'`, the files it was meant for.
`tests/domains.py` reads agents' frontmatter with `shared/frontmatter/`. In
`test_reviewfile.py`, the two assertions where PyYAML read the format back became
literal expectations: the whole rendered front matter of the fixture, and the line each
awkward string renders to, both as PyYAML read them back on 2026-10-04 before the import
went — a change to the rendering now shows as a difference of text. Its proof, `check`:
`git grep -l "import yaml" -- '*.py'` finds nothing (exit 1), and `make check` passes.
Committed as `8b18168`.

Tasks 12 and 13, the audit hook, committed together so that no commit leaves
`make check` red. Task 12's proof, `test`: `domains/skill-tooling/tests/test_hook.py`
runs the hook as the harness does, the event on stdin — an edited reference of a skill
with an unknown field, a file outside any skill, a clean skill and one with only a
warning, a report of five R1 errors and one F6, and an event that is not JSON — and
watched all of them fail, six assertions, the hook not existing yet. Task 13's proof,
`test`: `hooks/audit_skill.py` — it finds the skill by walking up from the edited file
to a folder holding `SKILL.md`, finds `audit.py` above itself as the roadmap hooks find
their script, reports errors only, one line per failing rule with its first place and
how many more, and stays silent on anything unexpected — then `hooks.json` and
`tests/test_permissions.py`, which checks the one allow rule, the audit's executable bit
and shebang, and that `SKILL.md` runs it by its path, as the roadmap domain's does. The
eight tests and `make check` pass. The criterion of a real session, the hook reporting
an unknown key to the agent in a scratch project, is left to the closure. Committed as
`8037d56`.

Task 14, the dev hook. Its proof, `test`: `tests/test_check_skills.py`, written first —
a real unittest failure and error summarized to one line each, a module that does not
load summarized to its `SyntaxError`, four Bash commands that ran the checks, and the
hook's command leaving the skills out — failed, four assertions and four errors; then
`tests/check.py` gained `--skip-skills` and `--brief`, and the hook runs both, stays
silent after a command that ran `make check` or `tests/check.py`, watches `shared/` too,
and caps its report at 20 lines. The first green run differed only in order — unittest
lists errors before failures, and the summary keeps its order — so the test now expects
that order. Since the skills are no longer checked by the dev hook and the audit hook is
not installed before Phase 5, `.claude/settings.json` registers the repository's
`audit_skill.py` for edits until then; Phase 5's install task now removes that
registration. Both hooks, fed real events, stay silent on this repository. 5 tests and
`make check` pass. Committed as `d329d39`.

Checked the acceptance criteria. Every one of the 46 rules has a test in
`test_audit.py`, each watched failing before its rule. `make check` reports on this
repository what it reported before the audit, no problem, with one new warning, X3.
On the two sources, every earlier problem is still reported or changed as the catalogue
decided — not "every problem" word for word: skill-creator's "old version" and nine
unreachable scripts, and two `ooxml/` paths of `writing-skills`, are no longer reported
(task 10's table). For the last criterion, a headless session of Claude Code 2.1.283 on
Haiku, in a scratch project with the hook given through `--settings`, added `tools:
Read` to a skill's frontmatter: the hook reported F6 and the agent quoted the report
word for word, $0.03. A first run had the skill under `.claude/skills/`, where the edit
waited for a permission even in `acceptEdits`: the scratch skill moved to `skills/`.
The report suggested `hooks` for `tools`, `difflib`'s closest name: a test, then the
audit names `allowed-tools` for that agent field. The narrowed dev hook showed the
failing test in one line, where it pasted tracebacks before.

---

## Decisions

- **The rule catalogue and the parser decision go to a decision record,**
  `docs/decisions/<date>-skill-audit-rules.md`, cited from the phase's `## Design`
  (the user, 2026-10-03), rather than `.superpowers/specs/`, which the superpowers study
  set aside.
- **This phase's tasks declare their proofs** (the user, 2026-10-03), applied by hand
  until roadmap `roadmap-execution` builds the operation that runs them.
- **The rule catalogue is approved as proposed** (the user, 2026-10-04): 46 rules, an
  error failing the check and a warning only reporting, the hook reporting errors only,
  `--portable` for the Agent Skills standard, `--checks` for the repository's commands.
  Phases 2 to 5 check skills by it; a rule changes through the record, not in code.
- **The audit parses frontmatter with its own strict subset of YAML,** in
  `shared/frontmatter/` (the user, 2026-10-04). Claude Code's laxer parser reads
  frontmatter that other agents drop, so F3 reports it in both profiles; scriptorium's
  `session-review` is one case.
- **A task is added to this phase:** PyYAML out of `tests/domains.py` and
  `test_reviewfile.py` (the user, 2026-10-04), so that no file of the repository imports
  it, as the 2026-09-28 record's parser gap asked.
- **The audit lives in the skill `authoring-skills`,** the name of 2026-09-28, with a
  short `SKILL.md` on the audit alone: `tools/shared.py` checks only folders holding a
  `SKILL.md`, and the hook finds `audit.py` in the skill as the roadmap hooks find their
  scripts. Phase 3 rewrites `SKILL.md` around it.
- **Reaching a file is generous, citing a missing one is strict.** R3 counts any path of
  the skill a reached file names, its tail, a name the skill holds once, a cited folder
  and Python imports, so that it reports only what nothing names; R1 keeps to paths under
  the three folders and to links outside code blocks. The record's R1 and R3 rows say so.
- **Four rows of the approved catalogue were stated more precisely while their tests
  were written,** each in line with its source: N4's reserved prefix is
  `anthropic-skills:`, as the documentation writes it; R1 and R3 say how citations are
  read; X7 reports `$ARGUMENTS` only where a skill expects no arguments. The intent of
  each rule is unchanged; the record and the code say the same.
- **The hook reports errors only, one line per failing rule,** with its first place and
  how many more, and names the command that lists every problem; `make check` prints
  warnings without failing; the dev hook runs `tests/check.py --skip-skills --brief`.
- **Until Phase 5 installs the domain, `.claude/settings.json` registers the
  repository's audit hook,** so that skills here are still checked at each edit once the
  dev hook leaves them out.

---

## Files Changed

**Added**
- `docs/decisions/2026-10-03-skill-audit-rules.md`
- `docs/roadmap/on-progress/skill-tooling/phase-2-static-audit-report.md` — created at
  the opening, committed with it in `da8f005`
- `domains/skill-tooling/CHANGELOG.md`
- `domains/skill-tooling/VERSION`
- `domains/skill-tooling/hooks.json`
- `domains/skill-tooling/hooks/audit_skill.py`
- `domains/skill-tooling/permissions.json`
- `domains/skill-tooling/skills/authoring-skills/SKILL.md`
- `domains/skill-tooling/skills/authoring-skills/references/conventions.md` — a copy of
  `shared/conventions/conventions.md`
- `domains/skill-tooling/skills/authoring-skills/scripts/audit.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/conventions.py` — a copy of
  `shared/conventions/conventions.py`
- `domains/skill-tooling/skills/authoring-skills/scripts/frontmatter.py` — a copy of
  `shared/frontmatter/frontmatter.py`
- `domains/skill-tooling/tests/test_audit.py`
- `domains/skill-tooling/tests/test_hook.py`
- `domains/skill-tooling/tests/test_permissions.py`
- `shared/frontmatter/frontmatter.py`
- `shared/frontmatter/tests/test_frontmatter.py`
- `tests/test_check_skills.py`

**Modified**
- `.claude/hooks/check-skills.py`
- `.claude/settings.json`
- `CLAUDE.md`
- `docs/claude-code-coupling.md`
- `docs/roadmap/on-progress/skill-tooling/README.md` — the opening's edits, committed in
  `da8f005`, then this closure's
- `docs/roadmap/on-progress/skill-tooling/phase-2-static-audit.md` — the opening's
  status, committed in `da8f005`, then the design, the proofs, the work and the closure
- `docs/roadmap/on-progress/skill-tooling/phase-3-writing-method.md`
- `docs/roadmap/on-progress/skill-tooling/phase-4-evaluation-tooling.md`
- `docs/roadmap/on-progress/skill-tooling/phase-5-switch-over.md`
- `domains/review/tests/test_reviewfile.py`
- `domains/roadmap/skills/roadmap/evals/checks.py`
- `domains/roadmap/skills/roadmap/evals/test_scripts.py`
- `domains/roadmap/skills/roadmap/scripts/check_links.py` — mode only, the executable
  bit
- `domains/roadmap/skills/roadmap/scripts/progress.py` — mode only, the executable bit
- `tests/check.py`
- `tests/domains.py`
- `tests/skills.py`

Outside the diff: `study/frontmatter-probe/`, the probe's corpus, controls, prototype
and comparison, and `local-review/2026-10-03-skill-audit-rules-fr.md`, the French
translation of the record, both ignored by git.

---

## Problems And Deviations

- **Acceptance criterion not ticked: "the audit reports every problem `tests/skills.py`
  reported in Phase 0" on the two sources.** Every earlier problem is reported or changed
  as the catalogue decided, not every one word for word: skill-creator's "old version"
  is allowed by T1, its nine scripts are reached through `-m` module names and imports,
  and two `ooxml/scripts/*.py` paths of `writing-skills` are no longer read as citations
  of the skill's own `scripts/`. The 2026-09-28 record had judged all three misfires.
  Left as is, by decision.
- **`docs/claude-code-coupling.md` was not updated in the commits that added Claude Code
  ties,** as the repository's convention asks: the audit hook's events, input and output,
  the domain's permission rule, and the audit's default profile, which encodes Claude
  Code's frontmatter reference. Done at this closure.
- **Commits per task, with three exceptions:** tasks 1 and 2 in one commit, both writing
  the one record; tasks 12 and 13 in one commit, so that no commit holds the hook's red
  tests; and two record corrections committed apart, N4 then X7 and R1 and R3 with their
  tasks.
- **The roadmap skill changed without a roadmap release:** `progress.py` and
  `check_links.py` gained their executable bit, mode only. The next roadmap release, by
  roadmap `roadmap-dependencies`, carries it.
- **R1 still reports example paths written in prose,** `scripts/tool.sh` in
  `writing-skills`, `assets/x.svg` in scriptorium: the misfire the 2026-09-28 record
  noted, kept since skipping code or prose would also skip real invocations.
- **Scriptorium will see errors once the hook is installed:** 85 over its ten skills —
  55 R3 on the test files its skills keep in `tests/`, which a `[skills]` table with
  `evals = "tests"` would set aside, scriptorium having no such table; 23 scripts with a
  shebang and no executable bit (X2); 4 R1 on example paths; 2 skills over 5,000 tokens
  (Z1); `session-review`'s frontmatter (F3). Nothing was changed there.
- **Until task 14, the dev hook pasted every traceback of a red run,** hundreds of lines
  for each step of each test-first cycle of this phase; it now shows one line per failing
  test.
- **The hook's first real run suggested `hooks` for `tools`,** `difflib`'s closest name;
  fixed with a test, the audit naming `allowed-tools` for that agent field.
- **An Edit under `.claude/` waits for a permission in a headless run, even with
  `acceptEdits`** (2.1.283): the hook probe moved its scratch skill to `skills/`. Carried
  to Phase 4, whose eval runs edit skills.
- **The README's Tasks column for Phase 2 moves from 13 to 14,** with the task the user
  added on 2026-10-04.

---

## Changes To Later Phases

- `phase-3-writing-method.md`: its design task writes the design in the phase's
  `## Design`, citing a decision record where needed, rather than `.superpowers/specs/`,
  as the superpowers study decided and the user approved for this phase; a constraint
  says that `authoring-skills` already exists, its `SKILL.md` limited to the audit, to be
  rewritten, and that the template rules are now the roadmap skill's own checks; its
  Files to Modify name the domain and the skill.
- `phase-4-evaluation-tooling.md`: a constraint — in a headless run, an Edit under
  `.claude/` waits for a permission even with `acceptEdits`; a scenario's skill sits
  elsewhere or the run grants that permission.
- `phase-5-switch-over.md`: the install task also removes from `.claude/settings.json`
  the registration of the repository's audit hook that this phase added, or the hook runs
  twice here; a constraint says what the hook would report in scriptorium once installed,
  for the user to decide first.

No restructuring is pending.

---

## Assessment

The phase built the static audit the roadmap needed: `authoring-skills/scripts/audit.py`
checks the 46 rules of the catalogue approved on 2026-10-04 — frontmatter, name and
description, size, resources, execution, the repository's `[skills]` conventions, and
compatibility wording — each with its own test, watched failing first; a hook runs it at
each edit of a skill, in any project, and reports one line per failing rule;
`tests/skills.py` runs through it; and the dev hook, narrowed, no longer pastes
tracebacks. A probe chose the parser — a strict subset of YAML of the repository's own,
in `shared/frontmatter/` — after finding Claude Code's parser laxer than YAML and
`claude plugin validate` blind to field names and values; no Python file of the
repository imports PyYAML any more.

Run on 39 real skills, the audit's first drafts reported hundreds of false orphans;
each became a test, until what remains is what the 2026-09-28 and 2026-10-01 records
already called cited nowhere or misfired. This repository's three skills hold no error,
one warning; scriptorium holds 85 errors that the installed hook will raise, 55 of
them on test files a `[skills]` table would set aside.

What Phase 3 needs to know first: `authoring-skills` exists, its `SKILL.md` limited to
the audit and to be rewritten around the method; the audit and its catalogue are what
Phase 3's writing guide and `skill-auditor` build on, the agent taking the judgment the
rules leave out; and the design goes in the phase's `## Design`, not in `.superpowers/`.
