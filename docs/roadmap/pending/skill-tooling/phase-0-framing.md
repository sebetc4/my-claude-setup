# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/15)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Turn the three sources into recorded decisions before any code is written: what the new
tool keeps, improves or drops from `superpowers:writing-skills` and the skill-creator
plugin, the rules that settle their contradictions against the official documentation,
and the answers to the questions left open at opening.

---

## Overview

### Why This Phase Matters
A merge that is not inventoried becomes a concatenation. The two sources contradict each
other on descriptions, tone, testing and script invocation, and both drift from the
official documentation: skill-creator's validator rejects frontmatter fields Claude Code
accepts, and writing-skills breaks its own size budget. Deciding once, in writing, keeps
the later phases from arguing each point again.

### What It Enables
The capability matrix becomes the parity check of Phase 5. The settled rules become the
checks of the static audit in Phase 2 and the guidance of the writing method in Phase 3.
The decision on who owns `.agent-conventions.toml` shapes Phase 1.

### Out of Scope
Code, skills and agents: they start in Phase 1.

---

## Tasks

### Inventory
- [ ] List every capability of `superpowers:writing-skills` 6.4.1 — its SKILL.md and five companion files — as keep, improve or drop, each with a one-line reason
- [ ] List every capability of the skill-creator plugin — SKILL.md, three agents, its scripts and two HTML viewers — as keep, improve or drop, each with a one-line reason
- [ ] List the facts of the official skills page that neither source encodes — frontmatter fields, the 1,536-character listing cap, the 5,000 tokens kept after compaction, `!` injection failures, `claude plugin validate`, `/skill-doctor` — and name the phase that encodes each
- [ ] Run `tests/skills.py` on both sources and on this repository's skills, and keep the problems found as test cases for the Phase 2 audit

### Arbitration
- [ ] Settle the description rule — what the skill does and when to use it, key use case first, no workflow summary — citing what each source and the documentation say
- [ ] Settle the tone rule from the "match the form to the failure" table: prohibitions only for an observed discipline failure, recipes for wrong-shaped output, required slots for omissions, observable conditions for conditional behavior
- [ ] Settle the testing rule: when a baseline run is required before writing, and how much evaluation each kind of edit needs
- [ ] Settle the size budgets: SKILL.md lines and tokens, the table-of-contents threshold for references, and the description length for the Agent Skills standard and for Claude Code
- [ ] Settle the script rule: invocation by path through `${CLAUDE_SKILL_DIR}`, standard library only, and permission through `permissions.json` or `allowed-tools` — probe `allowed-tools` again first, since a headless probe of 2026-09-27 found it granted nothing

### Open Questions
- [ ] Measure the token cost and the maintenance cost of the three ways to own `.agent-conventions.toml` — a dedicated skill, per-tool code, a shared module copied into each tool from one source — and choose the cheapest
- [ ] Decide how description tuning rewrites a description: a script loop that rewrites and re-measures on its own, or the session proposing each rewrite while a script only measures
- [ ] Decide whether blind comparison between two versions of a skill is kept
- [ ] Choose the most self-explanatory names for the domain, the skill and the agents, clear of the reserved names `synced` and `anthropic-skills`

### Licensing
- [ ] Add the Apache 2.0 `LICENSE` at the repository root, and record how code adapted from skill-creator (Apache 2.0) and superpowers (MIT) keeps its notice

### Record
- [ ] Write the decision record under `docs/decisions/` with the capability matrix, the settled rules and the answers to the open questions

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-skill-tooling.md    new
LICENSE                                   new
```

### Dependencies
The two sources as installed — superpowers 6.4.1 and the skill-creator plugin, with local
copies under `pending/skill/` — and the official page https://code.claude.com/docs/en/skills.

### Constraints
Every decision cites its evidence: a source file, a documentation section, or a measured
figure. No code is written in this phase.

---

## Acceptance Criteria

- [ ] Every capability of both sources has a keep, improve or drop entry with its reason
- [ ] Every contradiction between the sources and the documentation has a settled rule
- [ ] The three open questions have an answer, and the names are chosen
- [ ] The decision record and the `LICENSE` are committed
