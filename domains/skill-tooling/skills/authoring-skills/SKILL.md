---
name: authoring-skills
description: Creates, edits and audits skills — a `SKILL.md` with its references, scripts, templates and evals — by the repository's conventions. Use when asked to write, create, change, fix, improve, review, audit or check a skill or its description, or to turn a workflow of the session into a skill.
---

# Authoring Skills

Create, edit and audit skills — a skill's `SKILL.md` and every file it cites — in any
repository, by that repository's conventions.

## The Conventions

Before creating or editing a skill, run `scripts/conventions.py skills`. On
`status: ok`, it prints the repository's `[skills]` table: the folders that hold skills,
the folder of a skill's evals, the workspace where eval runs write, and the features the
repository excludes, which the audit checks. On any other status, follow
`references/conventions.md` before going further.

## Rules For Every Operation

1. Guidance answers an observed failure. For a new skill or a change meant to alter
   behavior, first run the scenarios without it — for an edit, with the previous
   version —, then write only what answers the failures the runs show; when no run is
   possible, write only what the request states. Any other change takes the proof that
   `references/create-and-edit.md` lists for its kind.
2. The size of the work follows the size of the request: deliver what was asked. A hook,
   a script, a new domain or tests beyond the skill's evals are proposed with their
   cost, and built only on the user's yes.
3. After any write to a skill, whatever tool made it, run `scripts/audit.py <skill-dir>`
   and fix its errors: a file written through a shell command escapes an audit hook that
   matches the editing tools (https://code.claude.com/docs/en/hooks, § Matcher patterns).

## Routing

| Request | Operation | Read |
|---|---|---|
| Write a new skill, or turn a workflow of the session into one | Create | `references/create-and-edit.md`, which sends to `references/writing-guide.md`, to `references/discipline.md` for a skill that enforces a rule, and to a template under `assets/templates/` |
| Change a skill: its behavior, description, facts, scripts or wording | Edit | The Edit section of `references/create-and-edit.md`, then the parts of `references/writing-guide.md` the change touches |
| Audit, review or check a skill | Audit | `references/audit.md` |
| Write or fix the repository's `[skills]` table | — | `references/conventions.md` |
| Anything else | — | Nothing from this skill |

## Scripts

Run each as a command, by its path in this skill's folder and with no interpreter in
front: permission rules name the scripts and match the whole command
(https://code.claude.com/docs/en/permissions, § Bash). Run them rather than read their
code: the audit names each problem with its rule when it runs, after the writes.

- `scripts/audit.py <skill-dir>` audits a skill against the Agent Skills standard, the
  harness's rules and the repository's conventions, and exits 1 on an error; `--help`
  gives its options.
- `scripts/conventions.py skills` prints the repository's `[skills]` table, or what is
  wrong with the conventions file.
