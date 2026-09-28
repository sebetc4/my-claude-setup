# Phase 1: Agent Conventions

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/16)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-0-framing.md` and `phase-0-framing-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-1-agent-conventions-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Give every tool of this setup one place to read a repository's conventions,
`.agent-conventions.toml` at the repository root — its format, lookup, validation, and the
conversation that fills or fixes it — and move the roadmap contract out of `CLAUDE.md`
into it.

---

## Overview

### Why This Phase Matters
Contracts in `CLAUDE.md` cost context in every session for data that one tool reads when
it runs, and `session_resume.py` has to parse Markdown with a regular expression to read
one. The skill tool needs the same mechanism in Phases 2 and 3, and docs and git will
need it next.

### What It Enables
The static audit applies a repository's `[skills]` conventions, and the writing method
places a new skill where the repository wants it. Sessions stop carrying contracts.

### Out of Scope
The `[docs]` and `[git]` tables, and conventions for agents other than Claude Code.

---

## Tasks

### Design
- [ ] Write the design of `.agent-conventions.toml` — shared keys, the `[roadmap]` and `[skills]` tables with their types and allowed values, lookup, validation messages, the fill-or-fix conversation — in `.superpowers/specs/`, and get the user's approval

### Reader
- [ ] Write the failing tests of the reader: root found from a path, `~/.claude` as the root of personal skills, no lookup above the root, missing file, TOML error with its line, unknown key, wrong type, value outside its allowed set
- [ ] Implement the reader with `tomllib`: it prints a tool's table resolved against the shared keys, or the precise problems, and always exits 0; skills run it as a step of their procedure, not through a `!` command, per the Phase 0 script rule
- [ ] Implement the file creation: write the approved values and add `.agent-conventions.toml` to the repository's `.gitignore`, test first
- [ ] Package the reader as the shared module Phase 0 decided — one source, copied into each tool that reads the file, by the installer or as checked copies — with its permission rule, and pass `tests/domains.py`

### Conversation
- [ ] Write the fill-or-fix procedure: detect candidate values in the repository, propose them pre-filled, ask only for the calling tool's table and the missing shared keys, write after approval, and show the error with the proposed correction for a malformed file
- [ ] Write what a hook, a subagent or a `claude -p` run does without a valid file: report the missing or invalid keys and stop, never guess

### Roadmap Migration
- [ ] Rewrite the contract section of the roadmap SKILL.md to read the `[roadmap]` table through the reader, with a `residue` list for `versioning = "none"`
- [ ] Update `references/close-phase.md` and `references/close-roadmap.md` wherever they name `CLAUDE.md` or the `## Roadmaps` block
- [ ] Make `hooks/session_resume.py` read `root` from `.agent-conventions.toml` with `tomllib`, and look for the phase in progress under `pending/` too, where a roadmap's first phase stays until it closes — failing tests first in `tests/test_hooks.py`
- [ ] Make `references/open-phase.md` replace the README's progress block with the output of `scripts/progress.py` when a phase opens, as `progress.py --check` requires
- [ ] Move the roadmap evals to the new contract: `build_fixtures.py` writes the file, `grade.py` checks it instead of `CLAUDE.md`, and `evals/checks.py` checks the TOML contract examples
- [ ] Run the three roadmap evals, the migrated skill against a snapshot taken before the migration
- [ ] Bump the roadmap domain's `VERSION` and add its `CHANGELOG.md` entry

### Repositories
- [ ] Move this repository's `## Roadmaps` block into `.agent-conventions.toml`, and document the file in `CLAUDE.md`
- [ ] Move the contracts of scriptorium and forma-rust into their `.agent-conventions.toml`, carrying forma-rust's three checks and its residue files

---

## Technical Details

### Files to Modify
```
<source of the shared module, placed in Phase 1>          new: reader and procedure
domains/roadmap/skills/roadmap/SKILL.md
domains/roadmap/skills/roadmap/references/open-phase.md
domains/roadmap/skills/roadmap/references/close-phase.md
domains/roadmap/skills/roadmap/references/close-roadmap.md
domains/roadmap/skills/roadmap/evals/build_fixtures.py
domains/roadmap/skills/roadmap/evals/grade.py
domains/roadmap/skills/roadmap/evals/checks.py
domains/roadmap/hooks/session_resume.py
domains/roadmap/tests/test_hooks.py
domains/roadmap/VERSION
domains/roadmap/CHANGELOG.md
CLAUDE.md
.gitignore
```

### Dependencies
Phase 0: the owner of the file and the shared keys.

### Constraints
Python standard library only: `tomllib` needs Python 3.11 or later. A `!`-injected command
must exit 0 and be allowed by a permission rule, or the skill invocation aborts. Nothing
is installed into `~/.claude` without the user's go-ahead.

---

## Acceptance Criteria

- [ ] The reader's tests cover every case of the design and pass under `make check`
- [ ] No file under `domains/` reads a contract from `CLAUDE.md`
- [ ] The migrated roadmap skill passes at least as many eval assertions as the snapshot taken before the migration
- [ ] In conversation, a missing or malformed file leads to a pre-filled proposal and a question; in a subagent, to a stop that names the missing keys
- [ ] A newly created `.agent-conventions.toml` is listed in the repository's `.gitignore`

---

## Risk & Mitigation

- The migrated roadmap skill, run in a repository whose contract is still in `CLAUDE.md`,
  finds no file: the fill-or-fix conversation offers to move the block, so no repository
  is left without a contract.
- The reader runs at every roadmap invocation, where an exception or a missing
  permission rule would stop the procedure: it always exits 0, and its permission rule is
  tested with its domain. A `!` command would save one step in Claude Code only; per the
  Phase 0 script rule, it comes only with a fallback step and a row in
  `docs/claude-code-coupling.md`.
