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
domain does not hold.

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
