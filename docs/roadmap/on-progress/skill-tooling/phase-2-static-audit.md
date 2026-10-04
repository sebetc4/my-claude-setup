# Phase 2: Static Audit

---

## Status

**Current Status:** 🟢 Done (100% — 14/14)
**Started:** 2026-10-03
**Completed:** 2026-10-04
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-agent-conventions.md` and `phase-1-agent-conventions-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-static-audit-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

One audit script checks any skill against the platform rules and against the repository's
`[skills]` conventions; a hook runs it after every edit of a skill, in any project; and
`tests/skills.py` delegates to it.

---

## Overview

### Why This Phase Matters
Neither source audits an existing skill. skill-creator's `quick_validate.py` rejects
fields Claude Code accepts, such as `disable-model-invocation` and `when_to_use`, while
Claude Code itself ignores an unknown field, or a frontmatter that does not parse,
without reporting anything. The only automated audit today, `tests/skills.py`, runs only
on this repository's `domains/`.

### What It Enables
Every skill written from Phase 3 on is checked at each edit, the new skill included, and
Phase 5 audits the existing skills with it.

### Out of Scope
Checks that need judgment — description quality, guidance matched to the failure it
targets — which belong to the `skill-auditor` agent of Phase 3.

---

## Design

The rule catalogue — each rule with its source, its severity and its message — and the
parser decision live in the decision record
[2026-10-03-skill-audit-rules.md](../../../decisions/2026-10-03-skill-audit-rules.md),
approved by the user on 2026-10-04.

---

## Tasks

### Design
- [x] Write the rule catalogue — each rule with its source (documentation section, Agent Skills standard, or repository convention), its severity and its message — in the decision record `docs/decisions/2026-10-03-skill-audit-rules.md`, cited from `## Design`, and get the user's approval
  Proof: review — the catalogue, each rule with its source, severity and message, approved before any check is written
- [x] Decide how the audit parses YAML frontmatter with the standard library only — a strict subset parser, `claude plugin validate`, or both — by trying each on this repository's skills and on the two sources
  Proof: probe — a strict subset parser and `claude plugin validate`, each run on this repository's skills, the two sources' and malformed frontmatters as controls, before the audit relies on one

### Domain
- [x] Create the domain — `VERSION`, `CHANGELOG.md`, `permissions.json` — and pass `tests/domains.py`
  Proof: check — `make check`, red while `domains/skill-tooling/` lacks its `VERSION` or `CHANGELOG.md`, green once the domain is complete

### Platform Rules
- [x] Test and implement the frontmatter checks: opening `---` on the first line, parse errors, unknown keys against the full Claude Code field list, value types and allowed values, and a `--portable` mode limited to the six Agent Skills fields
  Proof: test — one skill per frontmatter rule that breaks it: no `---` on line 1, a parse error, an unknown key, a wrong type or value, a non-standard field under `--portable`
- [x] Test and implement the name and description checks: kebab-case within 64 characters, reserved names, the directory match, a present description, 1,024 characters for the standard and 1,536 for `description` plus `when_to_use`, no angle brackets
  Proof: test — one skill per name and description rule that breaks it: case or length of the name, a reserved name, a directory mismatch, no description, either length limit, angle brackets
- [x] Test and implement the size checks: SKILL.md lines, an estimate of its tokens against the 5,000 kept after compaction, and long references without a table of contents
  Proof: test — one skill per size rule that breaks it: SKILL.md too long in lines, a token estimate over 5,000, a long reference without a table of contents
- [x] Test and implement the resource checks carried over from `tests/skills.py`: every cited file exists, and every file under `references/`, `assets/` and `scripts/` is reachable from SKILL.md
  Proof: test — a cited file that does not exist, and a file under `references/`, `assets/` or `scripts/` that SKILL.md does not reach
- [x] Test and implement the execution checks: a `!` command that can exit non-zero, a bundled script without a shebang or an executable bit, an `allowed-tools` rule that matches no command of the body, an `@` reference that force-loads a file
  Proof: test — one skill per execution rule that breaks it: a `!` command that can exit non-zero, a script without shebang or executable bit, an `allowed-tools` rule matching no command, an `@` reference

### Repository Conventions
- [x] Test and implement the `[skills]` checks: where skills and evals live, the language of skill files, who the files address — the agent, never a named model — the harness features the repository's `exclude` names (`allowed-tools`, `dynamic-context` for `!` commands, `substitutions`), a `workspace` that git does not ignore, and the repository's own check commands
  Proof: test — one skill or table per `[skills]` rule that breaks it: a skill or its evals out of place, a file in another language, a named model addressed, an excluded feature used, a workspace git does not ignore, a check command that fails
- [x] Move the rules of `tests/skills.py` into the audit, each re-justified in the rule catalogue rather than carried over as it stands, and make `tests/skills.py` call it
  Proof: check — `python3 tests/check.py` here and `python3 tests/check.py <skills-dir>` on the two sources report the same problems before and after the move
- [x] Replace PyYAML in `tests/domains.py` with the shared frontmatter parser, and the two PyYAML assertions of `domains/review/tests/test_reviewfile.py` with literal expectations of the rendered text
  Proof: check — `git grep -l "import yaml" -- '*.py'` finds nothing, and `make check` passes

### Hook
- [x] Write the failing tests of the PostToolUse hook: it audits the skill that contains the edited file, stays silent outside a skill and on a clean skill, and otherwise exits 2 with a report capped to the failing rules
  Proof: test — the four cases watched failing because the hook does not exist yet: a skill's file edited, a file outside any skill, a clean skill, a report capped to the failing rules
- [x] Implement the hook, its `hooks.json` entry and its permission rule
  Proof: test — the previous task's four cases pass, the permission rule tested as in `domains/roadmap/tests/test_permissions.py`, then `make check`
- [x] Narrow `.claude/hooks/check-skills.py` to domain checks and unit tests, cap its report to the failing test ids and their first lines, and keep it silent after a Bash command that ran the checks itself
  Proof: test — in a new `tests/test_check_skills.py`, watched failing first: a failure reported by its test ids and first lines only, no report after a Bash command that ran the checks itself, no skill check left in the dev hook

---

## Technical Details

### Files to Modify
```
docs/decisions/2026-10-03-skill-audit-rules.md                    new
shared/frontmatter/frontmatter.py                                 new
shared/frontmatter/tests/test_frontmatter.py                      new
domains/skill-tooling/VERSION                                     new
domains/skill-tooling/CHANGELOG.md                                new
domains/skill-tooling/permissions.json                            new
domains/skill-tooling/hooks.json                                  new
domains/skill-tooling/hooks/audit_skill.py                        new
domains/skill-tooling/skills/authoring-skills/scripts/audit.py    new
domains/skill-tooling/tests/test_audit.py                         new
domains/skill-tooling/tests/test_hook.py                          new
domains/roadmap/skills/roadmap/evals/checks.py                    the template rules
domains/roadmap/skills/roadmap/scripts/progress.py                executable bit
domains/roadmap/skills/roadmap/scripts/check_links.py             executable bit
domains/review/tests/test_reviewfile.py
tests/skills.py
tests/domains.py
tests/test_check_skills.py                                        new
.claude/hooks/check-skills.py
```

### Dependencies
Phase 0: the settled rules, the size budgets and the names. Phase 1: the reader of the
`[skills]` table.

### Constraints
Standard library only, the frontmatter parser included. A hook that fires on every edit
in every project stays silent outside a skill and on a clean skill, finishes well within
its timeout, and never pastes a full test or audit output into the conversation.

---

## Acceptance Criteria

- [x] Every rule of the catalogue has a test that fails without it
- [x] On this repository, `make check` reports the same problems as before, now produced by the audit
- [ ] On the two sources, the audit reports every problem `tests/skills.py` reported in Phase 0
- [x] In a scratch project, a skill edited with an unknown frontmatter key makes the hook report it to the agent

---

## Risk & Mitigation

- A standard-library parser can misjudge valid YAML: a construct outside the supported
  subset is reported as unverifiable, never as invalid, and the design task compares the
  parser with `claude plugin validate`.
- A hook in every project can turn into noise, as the dev hook did (about 2.15 million
  cached tokens carried in one session of 2026-09-27): it blocks only on errors of the
  catalogue, its report is capped, and its tests cover the silent cases.
