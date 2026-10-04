---
name: authoring-skills
description: Audits a skill's files against the Agent Skills standard and the harness's frontmatter reference, and reports each problem with its rule. Use when a skill is created or edited, or when asked to check, audit or validate a skill or its frontmatter.
---

# Authoring skills

## Auditing a skill

Run `scripts/audit.py <skill-dir>` by its path in this skill's directory. It prints each
problem as `path:line: [ID] message`, a warning's message opening with `warning:`, then a
count, and exits 1 when it found an error. Fix each error, and weigh each warning.

Add `--portable` for a skill meant for other agents: it checks the skill against the
Agent Skills standard alone.

The audit reads frontmatter with `scripts/frontmatter.py`, a strict subset of YAML that
refuses what any agent's parser might drop.
