# Claude Code

The conventions of the harness this setup installs into: which agent files Claude Code
reads, where, in what format and with what precedence. Read from
https://code.claude.com/docs/en/ on 2026-10-06, against Claude Code 2.1.283 installed
here; the page index is https://code.claude.com/docs/llms.txt. What Claude Code ships is
listed in [claude-code-builtins.md](../claude-code-builtins.md), and where this setup's
tools depend on it in [claude-code-coupling.md](../claude-code-coupling.md).

## The Agent Files

From the [`.claude` directory page](https://code.claude.com/docs/en/claude-directory),
§ File reference and § What's not shown. Project files sit in the repository's `.claude/`
(`CLAUDE.md`, `AGENTS.md`, `.mcp.json` and `.worktreeinclude` at its root), user files in
`~/.claude/`.

| File | Scope | What it does | Page |
|---|---|---|---|
| `CLAUDE.md` | project, user, managed | Instructions loaded every session | [memory](https://code.claude.com/docs/en/memory) |
| `CLAUDE.local.md` | project | Personal instructions for one project, kept out of git | memory |
| `AGENTS.md` | project, any folder | Instructions written for any coding agent, read when no `CLAUDE.md` is there ([agents-md.md](agents-md.md)) | memory § AGENTS.md |
| `rules/*.md` | project, user | Instructions by topic, optionally limited to paths | memory |
| `settings.json` | project, user, managed | Permissions, hooks, environment, model defaults | [settings](https://code.claude.com/docs/en/settings) |
| `settings.local.json` | project | Personal overrides, kept out of git | settings |
| `.mcp.json` | project | MCP servers shared with the team | [mcp](https://code.claude.com/docs/en/mcp) |
| `skills/<name>/SKILL.md` | project, user, managed, plugin | Skills, invoked by `/name` or by the model | [skills](https://code.claude.com/docs/en/skills) |
| `commands/*.md` | project, user, plugin | One-file skills, the older format, same mechanism | skills |
| `agents/*.md` | project, user, managed, plugin | Subagents, each with its own prompt and tools | [sub-agents](https://code.claude.com/docs/en/sub-agents) |
| `output-styles/*.md` | project, user, managed | Instruction sets that change how Claude Code works | [output-styles](https://code.claude.com/docs/en/output-styles) |
| `workflows/*.js` | project, user | Scripts that orchestrate subagents, each a `/name` command | [workflows](https://code.claude.com/docs/en/workflows) |
| `agent-memory/<name>/` | project, user | A subagent's persistent memory | sub-agents |
| `~/.claude.json` | user | App state, sign-in, personal MCP servers | [settings-reference](https://code.claude.com/docs/en/settings-reference) |
| `projects/<project>/memory/` | user | Auto memory, notes kept across sessions | memory § Auto memory |
| `plugins/` | user | Installed plugins and marketplaces, managed by `claude plugin` | [plugins](https://code.claude.com/docs/en/plugins/overview) |

`~/.claude/` also holds what Claude Code writes as it works — transcripts, history, file
snapshots, caches —, in plain text (§ Application data).

## Frontmatter By File

From the same page, § Frontmatter fields by file. Each kind accepts its own fields, and
Claude Code ignores an unknown field without an error.

| File | Fields |
|---|---|
| `skills/<name>/SKILL.md` | `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` |
| `commands/*.md` | The skill fields but `name` and `paths` |
| `agents/*.md` | `name`, `description` (both required), `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental` |
| `output-styles/*.md` | `name`, `description`, `keep-coding-instructions`, `force-for-plugin` |
| `rules/*.md` | `paths` |

A plugin's agents honor a subset of the subagent fields.

## Instructions

From the [memory page](https://code.claude.com/docs/en/memory):

- **Locations, broadest first:** managed (`/etc/claude-code/CLAUDE.md` on Linux), user
  (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md` or `./.claude/CLAUDE.md`), local
  (`./CLAUDE.local.md`). Files in the folders above the working directory load at launch,
  those in subfolders when Claude Code works there (§ Choose where to put CLAUDE.md
  files).
- **Imports:** `@path` in a `CLAUDE.md` loads that file at launch; a relative path
  resolves from the importing file; four hops at most; an `@path` inside backticks or a
  code block stays text (§ Import additional files).
- **Rules:** `.claude/rules/*.md`, optionally limited to files by a `paths` field.
- **`AGENTS.md`:** read instead of `CLAUDE.md` when the project has none, or beside it
  by a setting, since v2.1.277 ([agents-md.md](agents-md.md)).

## Skills

From the [skills page](https://code.claude.com/docs/en/skills):

- **Locations** (§ Choose where skills load): managed, `~/.claude/skills/`, the
  project's `.claude/skills/` and those of the folders above it up to the repository's
  root, a subfolder's `.claude/skills/` once Claude Code works there, the `.claude/skills/`
  of a folder passed with `--add-dir`, a plugin's `skills/` (invoked as
  `/plugin:skill`), and skills synced from claude.ai into `~/.claude/skills/synced/`.
  Claude Code does not read `.agents/skills/`.
- **Commands** are merged into skills: `.claude/commands/deploy.md` and
  `.claude/skills/deploy/SKILL.md` both make `/deploy`, the skill winning a collision.
- **The listing** (§ Skill descriptions are cut short): every name, and descriptions
  within a budget of 1% of the context window, the descriptions of the least invoked
  skills dropped first; `description` and `when_to_use` together cut at 1,536 characters.
  The budget, the cap and per-skill entries are settings: `skillListingBudgetFraction`,
  `skillListingMaxDescChars`, `skillOverrides`.
- **Who invokes** (§ Control who invokes a skill): `disable-model-invocation: true`
  takes the description out of the listing, so only the user starts the skill;
  `user-invocable: false` leaves it to the model.
- **Lifecycle** (§ Skill content lifecycle): an invoked skill stays in the conversation
  and is not read again; after compaction, the latest invocation of each skill comes
  back, its first 5,000 tokens, within 25,000 tokens for all skills, the most recent
  first.
- **Live edits** (§ Edit a skill during a session): a change to a watched skills folder
  applies in the running session; a skills folder created after the session started
  needs `/reload-skills`.
- **Body syntax** Claude Code alone reads: the substitutions `$ARGUMENTS`, `$N`,
  `${CLAUDE_SKILL_DIR}` and others (§ Available string substitutions); `` !`command` ``
  injections, run before the skill reaches the model (§ Inject dynamic context);
  `ultrathink` anywhere in the content for deeper reasoning (same section); `@path`,
  which attaches the file for a local skill (§ How Claude Code handles the body of a
  synced skill).
- **Fields that change how it acts:** `context: fork` runs the skill in a subagent
  (§ Run skills in a subagent); `paths` and `hooks` (§ Frontmatter reference);
  `allowed-tools` grants the listed tools for the invoking turn, even in a folder never
  trusted, and `disallowed-tools` removes tools while the skill is active
  (§ Pre-approve tools for a skill).
- **Access** (§ Restrict Claude's skill access, § Override skill visibility from
  settings): `Skill(name)` permission rules, and `skillOverrides` in the settings.
- **Cost and use:** `/skill-doctor`, from v2.1.252 (§ Find unused skills).

## Subagents

From the [subagents page](https://code.claude.com/docs/en/sub-agents):

- **Locations, by priority** (§ Choose the subagent scope): managed settings, the
  `--agents` flag, the project's `.claude/agents/` (the folders from the working
  directory up to the repository's root, the closest winning), `~/.claude/agents/`, a
  plugin's `agents/`. Folders are scanned recursively, and a subagent is known by its
  `name` field, not its file name.
- **The file** (§ Write subagent files): frontmatter, then the body, which becomes the
  subagent's whole system prompt. Multi-word fields are in camelCase, and an unknown one
  is ignored without an error.
- **What it starts with** (§ What loads at startup): its own prompt and environment
  details, the task message, the session's `CLAUDE.md` and `AGENTS.md` files unless
  `omitClaudeMd` is set, a git status, the skills its `skills` field preloads. Not the
  conversation, not the output style, not the session's auto memory.
- **Watching:** an edited file applies at the next delegation; a new `agents/` folder
  needs a restart.

## Hooks

From the [hooks reference](https://code.claude.com/docs/en/hooks):

- **Locations** (§ Hook locations): `settings.json` at user, project and local level,
  managed settings, a plugin's `hooks/hooks.json`, a skill's frontmatter (from its
  invocation to the end of the session), a subagent's frontmatter (while it runs).
  Entries from every level add up, and hooks from settings and plugins also run inside
  subagents.
- **Events** (§ Hook lifecycle): 33 on 2026-10-06, among them `SessionStart`,
  `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`,
  `Stop`, `InstructionsLoaded`, `PreCompact`, `PostCompact` and `SessionEnd`.
- **Contract** (§ Hook input and output): a JSON event on stdin; exit 0 to go on, exit 2
  to block and show stderr to the agent; or JSON on stdout for a decision or added
  context.

## Settings And Permissions

From the [settings](https://code.claude.com/docs/en/settings) and
[permissions](https://code.claude.com/docs/en/permissions) pages:

- **Files:** `~/.claude/settings.json` (user), `.claude/settings.json` (shared project),
  `.claude/settings.local.json` (personal project), managed settings.
- **Precedence**, highest first: managed, the command line, local, project, user. Lists
  such as `permissions.allow` merge across files instead of replacing each other
  (§ Settings precedence).
- **Permission rules:** `Tool` or `Tool(specifier)`, such as `Bash(git push *)`
  (§ Permission rule syntax).

## Plugins

From [plugin components](https://code.claude.com/docs/en/plugins/components): a plugin
folder holds `.claude-plugin/plugin.json`, its manifest, then default folders for each
kind of component — `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`,
`output-styles/` and others. Its skills are invoked as `/plugin:skill`. A `CLAUDE.md` at
a plugin's root is not loaded: a plugin's instructions are written as a skill, and a rule
that must always hold as a hook.

## Where This Setup Stands

- Its installer, `tools/claude_setup.py`, copies each domain's `skills/`, `agents/` and
  `commands/` into `~/.claude/`, its hooks into `~/.claude/hooks/<domain>/`, and merges
  its `hooks.json` and `permissions.json` into `~/.claude/settings.json`; this repository
  registers its own hooks in `.claude/settings.json`.
- The skill audit's default profile is Claude Code's skill fields and syntax
  (`docs/decisions/2026-10-03-skill-audit-rules.md`), and `skill-auditor` and
  `roadmap-auditor` use the subagent format.
- Behaviors this setup probed rather than read, such as `allowed-tools` granting nothing
  in headless runs or a heredoc no permission rule matches, are in `CLAUDE.md`, Gotchas,
  and in `docs/decisions/2026-09-28-skill-tooling.md`, Platform Facts.

## Refreshing This File

Fetch https://code.claude.com/docs/llms.txt for new pages; fetch the pages cited here
with a `.md` suffix, such as https://code.claude.com/docs/en/claude-directory.md, and
compare their file and field tables with the ones above. Update the date and the version
at the top with what changed.
