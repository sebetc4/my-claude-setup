# Phase 2: Static Audit

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/13)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
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

## Tasks

### Design
- [ ] Write the rule catalogue — each rule with its source (documentation section, Agent Skills standard, or repository convention), its severity and its message — in `.superpowers/specs/`, and get the user's approval
- [ ] Decide how the audit parses YAML frontmatter with the standard library only — a strict subset parser, `claude plugin validate`, or both — by trying each on this repository's skills and on the two sources

### Domain
- [ ] Create the domain — `VERSION`, `CHANGELOG.md`, `permissions.json` — and pass `tests/domains.py`

### Platform Rules
- [ ] Test and implement the frontmatter checks: opening `---` on the first line, parse errors, unknown keys against the full Claude Code field list, value types and allowed values, and a `--portable` mode limited to the six Agent Skills fields
- [ ] Test and implement the name and description checks: kebab-case within 64 characters, reserved names, the directory match, a present description, 1,024 characters for the standard and 1,536 for `description` plus `when_to_use`, no angle brackets
- [ ] Test and implement the size checks: SKILL.md lines, an estimate of its tokens against the 5,000 kept after compaction, and long references without a table of contents
- [ ] Test and implement the resource checks carried over from `tests/skills.py`: every cited file exists, and every file under `references/`, `assets/` and `scripts/` is reachable from SKILL.md
- [ ] Test and implement the execution checks: a `!` command that can exit non-zero, a bundled script without a shebang or an executable bit, an `allowed-tools` rule that matches no command of the body, an `@` reference that force-loads a file

### Repository Conventions
- [ ] Test and implement the `[skills]` checks: where skills and evals live, the language of skill files, who the files address — the agent, never a named model — the harness features the repository's `exclude` names (`allowed-tools`, `dynamic-context` for `!` commands, `substitutions`), a `workspace` that git does not ignore, and the repository's own check commands
- [ ] Move the rules of `tests/skills.py` into the audit, each re-justified in the rule catalogue rather than carried over as it stands, and make `tests/skills.py` call it

### Hook
- [ ] Write the failing tests of the PostToolUse hook: it audits the skill that contains the edited file, stays silent outside a skill and on a clean skill, and otherwise exits 2 with a report capped to the failing rules
- [ ] Implement the hook, its `hooks.json` entry and its permission rule
- [ ] Narrow `.claude/hooks/check-skills.py` to domain checks and unit tests, cap its report to the failing test ids and their first lines, and keep it silent after a Bash command that ran the checks itself

---

## Technical Details

### Files to Modify
```
domains/<domain>/VERSION                           new
domains/<domain>/CHANGELOG.md                      new
domains/<domain>/permissions.json                  new
domains/<domain>/hooks.json                        new
domains/<domain>/hooks/<audit hook>.py             new
domains/<domain>/skills/<skill>/scripts/audit.py   new
domains/<domain>/tests/test_audit.py               new
domains/<domain>/tests/test_hook.py                new
tests/skills.py
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

- [ ] Every rule of the catalogue has a test that fails without it
- [ ] On this repository, `make check` reports the same problems as before, now produced by the audit
- [ ] On the two sources, the audit reports every problem `tests/skills.py` reported in Phase 0
- [ ] In a scratch project, a skill edited with an unknown frontmatter key makes the hook report it to the agent

---

## Risk & Mitigation

- A standard-library parser can misjudge valid YAML: a construct outside the supported
  subset is reported as unverifiable, never as invalid, and the design task compares the
  parser with `claude plugin validate`.
- A hook in every project can turn into noise, as the dev hook did (about 2.15 million
  cached tokens carried in one session of 2026-09-27): it blocks only on errors of the
  catalogue, its report is capped, and its tests cover the silent cases.
