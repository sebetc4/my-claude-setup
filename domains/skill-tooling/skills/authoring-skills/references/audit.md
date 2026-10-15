# Auditing A Skill

The static audit checks what a rule can decide, the agent `skill-auditor` judges what only
a reading can, and one report gives both. Change no file of the skill unless the user
asks.

## 1. The Static Audit

Run `scripts/audit.py <skill-dir>` as a command, by its path in this skill's folder
and with no interpreter in front: permission rules name the script and match the whole
command (https://code.claude.com/docs/en/permissions, § Bash), and a project may refuse
`python3` in a command (my-agent-setup `CLAUDE.md`, Gotchas). It prints each problem as
`path:line: [ID] message`, a warning's message opening with `warning:`, then a count,
and exits 1 when it found an error.

Add `--portable` for a skill meant for other harnesses: it checks the skill against the
Agent Skills standard alone. Add `--checks` to run the repository's check commands too.

The audit reads frontmatter with `scripts/frontmatter.py`, a strict subset of YAML that
refuses what any harness's parser might drop
(https://agentskills.io/client-implementation/adding-skills-support, § Handling
malformed YAML), and the repository's `[skills]` conventions
with `scripts/conventions.py`. Without a valid `[skills]` table no convention rule
applies: to write or fix the table, run `scripts/conventions.py skills` and follow
`references/conventions.md`.

## 2. The Judgment

Start two passes of the agent `skill-auditor` together, each with this request word for
word, the placeholders replaced by full paths and the static audit's output, and nothing
added:

```
Audit the skill at <skill folder>; its evals are in its evals/ folder.

Writing guide: <this skill's folder>/references/writing-guide.md
Templates: <this skill's folder>/assets/templates/

Static audit output, as printed by scripts/audit.py:
<output>
```

Each answers `VERDICT: PASS` or `VERDICT: FAIL`, then one line per problem,
`path:line: [judgment] problem — fix`. The verdict is PASS when both pass. A FAIL whose
lines are all answered never counts: the fixed text gets two new passes.

When no agent can be started, judge the skill yourself, with its evals at hand, against
the writing guide's sections The Description, What Goes In, The Form Follows The
Failure, Terminology and Degrees Of Freedom, and say in the report that no agent ran.

## 3. The Report

Report in this order: the static audit's errors, its warnings, then the agent's verdict
and problems. Give each problem its fix: the agent's lines carry theirs; for the static
audit's, say what to change. A fix the user then asks for is an edit, made by the Edit
section of `references/create-and-edit.md`.

The skill answers each point first, by a wording of its own; a fix that changes behavior
counts once the evals ran on it. A point is `skill-auditor`'s defect only on this evidence:
the evals show its fix regressing a case, quoted; the point names none of the five
judgments; or it cites a line past its file's end. Propose it to the user as
`skill-auditor`'s defect, with its evidence. On their yes, revert the fix, quote the point beside the regression under
the case's `failures_with_skill`, and fix `skill-auditor` with a fixture under this
skill's `evals/auditor/`; never reword the skill to satisfy the point. The skill's PASS
then comes from two passes of the fixed `skill-auditor`.

In Claude Code, `/skill-doctor` shows each skill's listing cost, its tokens over seven
days and its uses (https://code.claude.com/docs/en/skills, § Find unused skills): name
it to the user when the audit is about a skill's cost or use.
