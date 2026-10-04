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
which nothing names. `make check` passes, the X3 warning printed.

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

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
