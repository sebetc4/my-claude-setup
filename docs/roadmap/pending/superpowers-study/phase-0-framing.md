# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/5)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Inventory the plugin as it is — skills, companion files, agent prompts, hook, scripts,
and how the skills hand work over to each other — and set the method of the study
before judging anything.

---

## Overview

### Why This Phase Matters
superpowers is a chain, not a set of separate skills: `brainstorming` hands over to
`writing-plans`, which hands over to `executing-plans` or `subagent-driven-development`,
which ends in `finishing-a-development-branch`, with test-driven development and
verification inside. Judging one skill alone misses what it relies on.

### What It Enables
Phases 1 to 3 rule on each family with one matrix format and one standard of evidence,
and Phase 4 has its recount method.

### Out of Scope
Verdicts on capabilities: Phases 1 to 3.

---

## Tasks

### Inventory
- [ ] Check that `study/superpowers/6.4.1/` matches the installed plugin, and list its parts: the 15 skills with their companion files, the agent prompts, the SessionStart hook, the scripts and the tests
- [ ] Map how the skills hand work over to each other — which skill names which, in what order, and which files pass between them: specs, plans, worktrees
- [ ] List every convention the plugin imposes on a repository — `docs/superpowers/`, commits, branches, worktrees, test commands — and every place it addresses Claude rather than the agent

### Method
- [ ] Set the matrix format and the standard of evidence from skill-tooling's Phase 0: one row per capability, keep, improve or drop, and a reason citing a source file, the documentation, a tool review or a measure
- [ ] Write the recount method: Skill tool calls per skill in `~/.claude/projects/*/*.jsonl` since 2026-09-18, this repository's sessions since 2026-09-28 left out, compared with the 2026-09-18 baseline

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-superpowers-study.md    new, drafted from Phase 0 on
```

### Dependencies
The plugin's copy under `study/superpowers/6.4.1/`, and the installed plugin.

### Constraints
No code and no change to any tool in this phase.

---

## Acceptance Criteria

- [ ] Every part of the plugin is listed with its hand-overs
- [ ] The matrix format and the recount method are written into the draft decision record
