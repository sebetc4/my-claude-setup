# AGENTS.md

The open format for a repository's instructions to coding agents, "a README for agents".
Read from https://agents.md on 2026-10-06. The format is stewarded by the Agentic AI
Foundation, under the Linux Foundation.

## The Format

- **One Markdown file, `AGENTS.md`, at the repository's root.** No required field and no
  required heading: the agent reads the text as written.
- **Nested files.** A package of a monorepo can hold its own `AGENTS.md`; agents read
  the nearest one in the directory tree, so the closest file to the edited one wins.
  The page counts 88 such files in OpenAI's main repository.
- **Precedence.** The closest `AGENTS.md` wins over the others, and the user's explicit
  prompts in the chat override every file.
- **Content.** What a new teammate would be told: a project overview, the build and test
  commands, code style, testing instructions, security considerations, commit and pull
  request rules, deployment steps. Checks the file lists are run by the agent, which
  fixes their failures before finishing.
- **Beside `README.md`.** The README stays for people; `AGENTS.md` holds the detail only
  agents need.
- **Living documentation**, updated like any other file.
- **Migrating** an earlier file: rename it `AGENTS.md` and leave a symbolic link under
  the old name, `mv AGENT.md AGENTS.md && ln -s AGENTS.md AGENT.md`.

## Who Reads It

The home page shows 23 agents on 2026-10-06 and links a longer list: Codex, Jules,
Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Autopilot and Coded Agents,
Junie, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Phoenix, Semgrep, GitHub Copilot's
coding agent, Ona, Windsurf and Augment Code. Two need a setting: Aider with
`read: AGENTS.md` in `.aider.conf.yml`, Gemini CLI with `"fileName": "AGENTS.md"` in the
context settings of `.gemini/settings.json`.

## Claude Code And AGENTS.md

Claude Code is not on that list, but reads the file since v2.1.277, through its builtin
plugin `agents-md` (`cc-plugin-agents-md@builtin` from v2.1.285). From the
[memory page, § AGENTS.md](https://code.claude.com/docs/en/memory#agents-md):

- **By default** (`claude-md-or-agents-md`), Claude Code reads every `AGENTS.md` and
  `.claude/AGENTS.md` from the working directory up when no `CLAUDE.md`,
  `.claude/CLAUDE.md` or `CLAUDE.local.md` sits there or above; with one of them, it
  reads the `CLAUDE.md` files only. `~/.claude/CLAUDE.md`, a managed `CLAUDE.md` and
  `.claude/rules/` load in either case. A subdirectory's `AGENTS.md` loads when a file
  there is read and the subdirectory has no `CLAUDE.md` of its own.
- **The setting** "Project instructions" in `/config`, or
  `pluginConfigs` › `cc-plugin-agents-md@builtin` › `options.instructionFiles` in the
  user settings, never in project or local ones: `claude-md-or-agents-md`,
  `claude-md-and-agents-md` (both, each folder's `CLAUDE.md` first), `claude-md`, or
  `managed-only`.
- **One shared file.** A `CLAUDE.md` holding `@AGENTS.md`, then any instruction only
  Claude Code needs, gives every agent the same file and works in sessions that cannot
  read `AGENTS.md` directly. A symbolic link `CLAUDE.md → AGENTS.md` works too, but the
  Edit and Write tools refuse to write through it, and a Windows clone may check it out
  as a one-line text file.
- **Where it differs from `CLAUDE.md`.** `InstructionsLoaded` hooks do not fire for an
  `AGENTS.md` read through the setting; directories added with `--add-dir` do not load
  their `AGENTS.md`; an `@path` import outside the working directory loads only if
  external imports were already approved.
- **Subagents** receive the `AGENTS.md` files the session loaded as project
  instructions, as they receive `CLAUDE.md`
  ([subagents page, § What loads at startup](https://code.claude.com/docs/en/sub-agents)).

## Where This Setup Stands

- This repository's instructions are in `CLAUDE.md`, and so are scriptorium's and
  forma-rust's; the roadmap skill and `authoring-skills` say "the repository's
  instruction file", never a file name (`docs/claude-code-coupling.md`).
- Moving a repository to `AGENTS.md` would take its shared instructions into
  `AGENTS.md`, and leave a `CLAUDE.md` holding `@AGENTS.md` and whatever only Claude Code
  needs, or no `CLAUDE.md` at all. Not decided: it touches every repository the setup
  serves, beyond the skill tooling.

## Refreshing This File

Fetch https://agents.md and compare its list of agents and its FAQ with this file; read
the memory page's `AGENTS.md` section again for Claude Code's support, which changed in
v2.1.277, v2.1.281 and v2.1.285. Update the date at the top with what changed.
