# Writing Guide

The rules of form for a skill's text: its description, its body and its other files.
They hold for any skill, in any repository; the repository's conventions come on top.

Where a rule needs more, read the source rather than a copy of it. Each fact below names
its source, with the page's section:

- "specification": the Agent Skills standard, https://agentskills.io/specification,
  which binds every harness that implements it; its guides on writing, describing,
  evaluating and scripting skills start at
  https://agentskills.io/skill-creation/best-practices;
- "Claude Code" and a page: https://code.claude.com/docs/en/ and that page, such as
  `skills`, for what only Claude Code does;
- "my-claude-setup": the repository this skill comes from, for what it probed;
- "writing-skills": the superpowers plugin's skill of that name, version 6.4.1,
  https://github.com/obra/superpowers.

Any other page of those two documentation sites is listed in
https://agentskills.io/llms.txt and https://code.claude.com/docs/llms.txt.

## The Description

Every skill's name and description are in the agent's context at every turn, and the
agent decides from them alone whether to load the skill; the body is read only once the
skill is chosen (specification § Progressive disclosure). So everything that says when
to use the skill goes in the description.

Write, in this order:

1. What the skill does, in one clause that names its operations or its outputs.
2. When to use it: the key use case first, then the situations in the words users say —
   keywords, synonyms, symptoms, error messages, file types, tool names.

Then check it against these rules:

- No sequence of steps: an agent that finds the workflow in the description follows it
  and skips the body (writing-skills § Rich Description Field).
- An exclusion ("Not for …") only after a false trigger was observed, in an eval or in
  real use: each costs listing tokens at every turn, and a guessed one can block a real
  use.
- For a skill that enforces a rule, the symptoms of a coming violation only when a run
  without the skill showed them.
- Third person; no model named; the harness named only when the skill is about it.
- Everything in `description`, nothing in `when_to_use`, which only Claude Code reads
  (Claude Code skills § Frontmatter reference).
- 1,024 characters at most, the standard's limit (specification § `description` field).
  Claude Code cuts `description` and `when_to_use` together at 1,536 characters in its
  listing, which holds about 1% of the context window and drops the descriptions of the
  least used skills first (Claude Code skills § Skill descriptions are cut short): the
  key use case goes in the first sentence.
- Broader or narrower is decided by measure, not by style: a skill that triggers too
  rarely widens its situations; one that triggers too often narrows them first, then
  gains exclusions.

A skill only the user starts can set `disable-model-invocation: true`, which takes its
description out of Claude Code's listing (Claude Code skills § Control who invokes a
skill).

```yaml
# Steps the body defines, and an exclusion nothing called for:
description: Reads the failing test, replaces its sleeps with waits on conditions, runs it ten times and commits. Not for unit tests.
# What, then when, in the users' words:
description: Fixes tests that fail intermittently by waiting on conditions instead of time. Use when a test is flaky, passes and fails without a code change, times out or hangs in CI.
```

## What Goes In

Write what an agent without the skill got wrong or cannot know, and nothing else; the
runs without the skill show which is which.

- Leave out what the model already knows — a language, a common tool, a widespread
  convention such as semantic versioning or git usage: name the convention, and state
  only where this repository or this task departs from it. Every line costs tokens at
  every use, the whole body being loaded once the skill is chosen (specification § Body
  content).
- Test each line before keeping it: when an agent without the skill would act the same
  way, cut the line, even when it restates a convention through an example of this
  repository.
- Give each fact its source, a fact about the repository included, so that a reader can
  check it and the next edit can update it: a documentation page, linked; a probe, with
  its date and the harness version; a file of the repository, by its path.
- Link an official page rather than copying it, and take from it only what the skill
  uses: a copy goes stale and costs tokens for parts no step needs.
- State the target behavior only: no date that will expire, no history of the skill, no
  wording about earlier versions.
- Give one default, with the condition for its exception, rather than a list of options.

## The Form Follows The Failure

State what to do, in the imperative and in positive form, addressed to the agent: "Run
the audit", not "the audit should be run". Then match the form of each instruction to
the failure a run showed:

| Failure observed | Form | Not |
|---|---|---|
| The output has the wrong shape | A recipe: what the output holds, in order | A list of things to avoid |
| An element is left out of an output | A required slot in the template | A reminder in prose near the template |
| The right behavior depends on a condition | A conditional on a predicate the agent can observe | A general rule with exemption clauses |
| A known rule is broken under pressure | A prohibition with its condition and safe path, a rationalization table and red flags quoted from runs | Soft wording |

For any form:

- Give a reason in one clause when the rule needs judgment, that is when the agent must
  apply it to cases the text does not list; no narration.
- Write no nuance clause such as "unless it matters": a real exception becomes its own
  conditional.
- An exemption does not scope a rule: when part of the output must escape it,
  restructure so that the rule cannot reach that part.
- Keep emphasis — capitals, "critical", stacked intensifiers, repeated warnings — for a
  failure that plain wording and the discipline form did not fix in a run, with the eval
  that shows it.
- Use no persuasion technique — authority, scarcity, social proof: firmness comes from
  the observed failure.

## Degrees Of Freedom

Constrain each step as much as it is fragile:

- Several approaches hold, or the decision depends on context: prose giving the goal and
  the criteria.
- A preferred pattern with room for variation: a template, or a script with parameters.
- One safe path, where a mistake is costly or hard to undo: exact commands or an exact
  script, in order.

A step that can fail gets its check — the command or the observation that shows it held
— and what to do when it did not.

## Structure

- The skill's folder holds `SKILL.md`, then `scripts/`, `references/` and `assets/` as
  needed (specification § Directory structure), unless the repository's conventions
  declare another layout.
- `SKILL.md` holds what applies to the whole task, those instructions first; a reference
  holds what one step or one variant needs. Claude Code keeps an invoked skill in
  context and, after compaction, restores only the first 5,000 tokens of its `SKILL.md`
  (Claude Code skills § Skill content lifecycle).
- Keep `SKILL.md` under 5,000 tokens (specification § Progressive disclosure), counted
  as characters divided by four; 500 lines is an alert.
- Cite each reference from `SKILL.md`, with when to read it: a file reached only through
  another reference may never be read (specification § File references).
- Give each variant — a platform, a framework, a kind of input — its own reference, so
  that the agent reads only the one it needs.
- Open a reference of 300 lines or more with a `## Contents` section.
- Cross-reference rather than repeat, and send a script's options to its `--help`
  rather than listing them.

## Scripts And Permissions

- Cite a script by its path relative to the skill's folder, such as
  `scripts/<name>.py`; the agent builds the absolute path from the folder its harness
  gives (specification § File references).
- Make each script an executable with a shebang, `#!/usr/bin/env python3` for Python,
  called by its path and never through an interpreter: permission rules name the path
  and match the whole command (Claude Code permissions § Bash), and a project hook may
  refuse `python3` in a command (my-claude-setup `CLAUDE.md`, Gotchas).
- Pass data through files or arguments, never a heredoc, which no permission rule
  matches (my-claude-setup `CLAUDE.md`, Gotchas).
- Print plain text, document the exit codes, and handle errors in the script rather than
  leaving them to the agent.
- Use the standard library, or what the repository's conventions allow.
- Write no permission syntax and no `allowed-tools`, which pre-approved nothing in
  Claude Code's headless runs (my-claude-setup `CLAUDE.md`, Gotchas): a skill installed
  for every project gets its permissions from the installer, a repository skill from the
  harness's settings in that repository or from the user's approval at the first run.
- Use an injected command (`!` and a command in backticks) only as a Claude Code
  optimization (Claude Code skills § Inject dynamic context), with a fallback step for
  other harnesses; the repository lists it with its other ties to Claude Code
  (my-claude-setup `CLAUDE.md`, Conventions).
- No surprise: the skill does what its description says, and says when it changes
  files, runs commands or reaches the network.

## Terminology

Use one term per thing, the same in every file of the skill and in its scripts' output:
an agent that meets two words assumes two things. Take the words of the repository and
of the users' requests.

## Examples And Templates

- One complete example from a real case, runnable when it is code, beats several
  partial ones; write no version per language.
- Give an output template where the shape of the output matters: placeholders in
  UPPER_SNAKE_CASE, and no HTML comment, which every file produced from it would copy.
- Show an input and its output where a transformation is easier shown than described.
- Write the technique a session revealed, not the story of that session.

## Names And Citations

- Name a skill after what the agent does, verb first or as a gerund, such as
  `fixing-flaky-tests`: lowercase letters, digits and hyphens, the same as its folder
  (specification § `name` field). Check that no skill, agent or command built into the
  harness has that name.
- Cite another skill by its name, with when to use it, never by `@` and a path, which
  Claude Code attaches at every invocation (Claude Code skills § How Claude Code handles
  the body of a synced skill).

## Harness Features

Claude Code reads frontmatter fields and body syntax that the standard does not:
`context: fork` runs the skill in a subagent, without the conversation; `paths` limits
it to matching files; `disallowed-tools` and `hooks` change what it may do; `$ARGUMENTS`,
`${CLAUDE_SKILL_DIR}` and the other substitutions are filled at invocation; `ultrathink`
in the body turns on deep reasoning at every use (Claude Code skills § Frontmatter
reference, § Available string substitutions, § Inject dynamic context, § Run skills in a
subagent). Each ties the skill to Claude Code:
use one only when the skill needs it, and never one that the repository's conventions
exclude. `scripts/audit.py` checks every field and its values.
