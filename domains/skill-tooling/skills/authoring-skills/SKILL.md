---
name: authoring-skills
description: Audits a skill's files against the Agent Skills standard, the harness's frontmatter reference and the repository's conventions, and reports each problem with its rule. Use when a skill is created or edited, or when asked to check, audit or validate a skill or its frontmatter.
---

# Authoring skills

## Creating or editing a skill

Follow `references/create-and-edit.md`, and `references/discipline.md` for a skill that
enforces a rule. Write the skill's description, body and other files by
`references/writing-guide.md`, then audit the skill as below.

## Auditing a skill

Run `scripts/audit.py <skill-dir>` by its path in this skill's directory. It prints each
problem as `path:line: [ID] message`, a warning's message opening with `warning:`, then a
count, and exits 1 when it found an error. Fix each error, and weigh each warning.

Add `--portable` for a skill meant for other agents: it checks the skill against the
Agent Skills standard alone. Add `--checks` to run the repository's check commands too.

The audit reads frontmatter with `scripts/frontmatter.py`, a strict subset of YAML that
refuses what any agent's parser might drop, and the repository's `[skills]` conventions
with `scripts/conventions.py`. Without a valid `[skills]` table no convention rule
applies: to write or fix the table, run `scripts/conventions.py skills` and follow
`references/conventions.md`.
