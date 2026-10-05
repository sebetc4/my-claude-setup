# Auditing A Skill

Two passes, then one report: the static audit checks what a rule can decide, and the
agent `skill-auditor` judges what only a reading can. Change no file of the skill unless
the user asks.

## 1. The Static Audit

Run `scripts/audit.py <skill-dir>` as a command, by its path in this skill's directory
and with no interpreter in front: permission rules name the script, and a project may
refuse `python3` in a command. It prints each problem as `path:line: [ID] message`, a
warning's message opening with `warning:`, then a count, and exits 1 when it found an
error.

Add `--portable` for a skill meant for other agents: it checks the skill against the
Agent Skills standard alone. Add `--checks` to run the repository's check commands too.

The audit reads frontmatter with `scripts/frontmatter.py`, a strict subset of YAML that
refuses what any agent's parser might drop, and the repository's `[skills]` conventions
with `scripts/conventions.py`. Without a valid `[skills]` table no convention rule
applies: to write or fix the table, run `scripts/conventions.py skills` and follow
`references/conventions.md`.

## 2. The Judgment

Start the agent `skill-auditor`, and give it:

- the skill's folder, by its full path; it reads the skill's evals there;
- the full path of `references/writing-guide.md` in this skill's directory;
- the static audit's output, as printed.

It answers `VERDICT: PASS` or `VERDICT: FAIL`, then one line per problem,
`path:line: [judgment] problem — fix`.

When no agent can be started, judge the skill yourself, with its evals at hand, against
the writing guide's sections The Description, What Goes In, The Form Follows The
Failure, Terminology and Degrees Of Freedom, and say in the report that no agent ran.

## 3. The Report

Report in this order: the static audit's errors, its warnings, then the agent's verdict
and problems. Give each problem its fix: the agent's lines carry theirs; for the static
audit's, say what to change. A fix the user then asks for is an edit, made by the Edit
section of `references/create-and-edit.md`.

In Claude Code, `/skill-doctor` shows each skill's listing cost, its tokens over seven
days and its uses: name it to the user when the audit is about a skill's cost or use.
