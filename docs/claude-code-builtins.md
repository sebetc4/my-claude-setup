# What Claude Code Ships

The skills, agents, tools, commands and plugins that Claude Code brings, so that this
setup's tools neither take one of their names nor duplicate one of them without saying
why. Taken on 2026-10-05 from Claude Code 2.1.283 on this machine: the init event of a
fresh headless session started outside any project, the skill listing that session
showed the model, and the definitions inside the executable. Refresh it after each
update, with the commands under Refreshing This Page.

## Rules For This Setup

- A name listed here is taken: no skill, agent or command of this setup uses it.
- A tool of this setup that does what a built-in does says, in its decision record, what
  the built-in lacks; otherwise it is not built.
- A description of this setup does not trigger where a built-in should: its trigger evals
  take the built-in's requests as near misses, those of `run-skill-generator` for
  `authoring-skills`.

## Skills

### Listed To The Model

Their name and description sit in every session's context, and the model may invoke
them.

| Skill | What it does | Overlap with this setup |
|---|---|---|
| `dataviz` | Charts, dashboards and stat tiles: form, colors, accessibility | — |
| `artifact-design` | Design guidance to load before writing an Artifact page | — |
| `artifact-diagramming` | Diagrams in Artifacts, in inline SVG | — |
| `artifact-capabilities` | What a published Artifact page can be granted: live data, shared state, files | — |
| `update-config` | Changes `settings.json`: hooks, permissions, environment variables | The installer merges each domain's `hooks.json` and `permissions.json` into `settings.json`; `update-config` serves hand edits |
| `keybindings-help` | Keyboard shortcuts, in `~/.claude/keybindings.json` | — |
| `code-review` | Reviews the diff or a pull request for correctness bugs, at a chosen effort | The `phase-reviewer` agent of roadmap `roadmap-execution`, which reviews a phase's diff against its design and its declared proofs |
| `simplify` | Cleans up the changed code: reuse, simplification, efficiency | — |
| `fewer-permission-prompts` | Adds an allow list to the project's `.claude/settings.json`, drawn from the transcripts | Each domain's `permissions.json`, merged into the user settings |
| `loop` | Runs a prompt or a command at an interval | — |
| `schedule` | Scheduled cloud agents | — |
| `claude-api` | Reference for the Claude API and the Anthropic SDKs | — |
| `run` | Launches the project's app to see a change working | — |
| `init` | Writes a first `CLAUDE.md` | — |
| `security-review` | Security review of the pending changes | — |

### Invoked By The User Only

Hidden from the model, so they cost no context; each is a slash command.

| Skill | What it does | Overlap with this setup |
|---|---|---|
| `batch` | Plans a large change, then runs it in 5 to 30 worktree agents that each open a pull request | The `execute-phase` operation of `roadmap-execution`, which runs a phase inline, task by task, and delegates only at the user's request |
| `debug` | Turns on Claude Code's debug logging and investigates problems | `finding-root-causes` of roadmap `working-method` debugs the user's code: the words overlap, the jobs do not |
| `design` | Makes a new Design artifact from a brief | `shaping-work` of `working-method`, named so because "design" was taken (2026-10-01 record) |
| `slides` | Makes a new Slides deck artifact from a brief | — |
| `design-sync` | Pushes design system components to claude.ai/design | — |
| `doctor` | Health-checks the setup and fixes issues: installation, unused extensions, duplicated or bloated memory files, slow hooks, updates, permissions; alias `checkup` | `tool-review` and `make reviews`, which measure how this setup's tools serve |
| `run-skill-generator` | Writes a skill that knows how to run the project's app | `authoring-skills`, which writes any skill, this kind included |
| `verify` | No description found in the executable | — |

`doctor` is marked to survive the switch that turns the bundled skills off, and the
environment variable `DISABLE_DOCTOR_COMMAND` removes it.

### Not Listed Here

- `artifact-components`, which embeds reusable components in an Artifact, and
  `claude-in-chrome`, which browses pages in Chrome: defined in the executable, gated
  off on this account. Their names are taken all the same.
- `plugin-authoring`, which writes Claude Code mods — panes, status lines, hooks — as
  plugins of function hooks: listed in the VS Code session that took this inventory, not
  in the headless one. This setup's hooks are scripts declared in each domain's
  `hooks.json`.

## Agents

| Agent | What it does | Overlap with this setup |
|---|---|---|
| `general-purpose` | Research and multi-step tasks, with every tool | — |
| `claude` | Catch-all, the default when no agent is named | — |
| `Explore` | Read-only fan-out search | — |
| `Plan` | Designs an implementation plan, read-only | The roadmap skill, whose phases hold the plan of long work |
| `claude-code-guide` | Answers questions on Claude Code, the Agent SDK and the Claude API | — |
| `statusline-setup` | Configures the status line | — |

This setup's agents — `roadmap-auditor`, and `skill-auditor`, `skill-grader`,
`skill-comparator`, `phase-reviewer` and `task-implementer` to come — are named after
their object with an agent noun, a form none of these takes.

## Tools

The headless init event lists 28: `Task` — the Agent tool —, `Artifact`,
`ArtifactComments`, `ArtifactData`, `Bash`, `CronCreate`, `CronDelete`, `CronList`,
`DesignSync`, `Edit`, `EnterWorktree`, `ExitWorktree`, `ListAgents`, `Monitor`,
`NotebookEdit`, `PushNotification`, `Read`, `RemoteTrigger`, `ReportFindings`,
`ScheduleWakeup`, `SendMessage`, `Skill`, `TaskStop`, `TodoWrite`, `ToolSearch`,
`WebFetch`, `WebSearch` and `Write`. The VS Code session that took this inventory had
`AskUserQuestion`, `EnterPlanMode` and `ExitPlanMode` besides, and no `TodoWrite`.

Neither list holds `Grep` or `Glob`: search goes through `Bash`. `roadmap-auditor` still
declares both in its `tools`.

## Slash Commands

Besides the skills above, the headless init event lists 36 commands: `advisor`,
`agents`, `auto-mode-setup`, `autocompact`, `clear`, `color`, `compact`, `config`,
`context`, `design-consent`, `design-revoke`, `effort`, `extra-usage`, `fast`, `focus`,
`goal`, `heapdump`, `import`, `init`, `insights`, `list-agents`, `mcp`, `model`,
`output-style`, `recap`, `reload-plugins`, `reload-skills`, `rename`, `security-review`,
`skill-doctor`, `team-onboarding`, `ultrareview`, `usage`, `usage-credits`,
`workflow-launch-exec` and `__remote-workflow`. An interactive session defines more,
among them `help`, `plugin`, `skills`, `hooks`, `permissions`, `memory` and `resume`.

Those that touch this setup's work:

- `/skill-doctor` gives each skill's listing cost, its tokens over seven days and its
  uses: from the harness's side, part of what `tool-review` measures per session.
- `/reload-skills` loads a skills directory created during the session.
- `/ultrareview` and `/security-review` review code, as `code-review` does.

No domain of this setup has a `commands/` folder yet.

## Plugins

Two builtin plugins load in every session: `agents-md` and `telemetry`. No other plugin
is installed since 2026-10-04: superpowers, skill-creator, claude-code-setup,
claude-md-management and diagram-design were uninstalled with their cache, and copies of
the first four are kept under `study/`, which git ignores.

## CLI Commands For Skills And Plugins

`claude plugin` takes `validate`, `eval`, `details`, `init`, `install`, `uninstall`,
`enable`, `disable`, `list` and `marketplace`. Three overlap with this setup:

- `validate` reports frontmatter that does not parse; the skill audit checks field names
  and values besides (2026-10-03 record).
- `eval` runs its own eval format, which roadmap `skill-tooling` leaves out of scope.
- `init` scaffolds a plugin under `~/.claude/skills/<name>/`, the folder where the
  installer copies this setup's skills: a scaffold named like one of them becomes a
  conflict at the next `make update`.

## Skills Synced From claude.ai

Off since 2026-09-18, by `syncClaudeAiSkills: false` in the user settings: 8 skills, one
of them a copy of `skill-creator`, which cost about 1,300 tokens per session for 2 calls
in a month (2026-09-18 record). Claude Code reserves their folder name `synced` and their
namespace `anthropic-skills`. `~/.claude/plugins/synced/` holds empty buckets that
claude.ai manages.

## Settings That Control Them

| Setting | Effect |
|---|---|
| `disableBundledSkills` | Removes the bundled skills, `doctor` excepted |
| `skillOverrides` | Hides or narrows a personal skill's listing; no effect on a plugin skill (probe of 2026-09-28); untested on a bundled skill |
| A `Skill(<name>)` deny rule | Refuses the invocation; the skill stays listed |
| `syncClaudeAiSkills: false` | Stops the claude.ai sync |
| `enabledPlugins` | Turns a plugin on or off, per scope |

## Refreshing This Page

From a folder outside any project, so that no project skill or hook joins the lists:

```bash
claude -p "Reply with OK." --model haiku --max-turns 1 --output-format stream-json --verbose
```

Its event of subtype `init` lists `skills`, `slash_commands`, `agents`, `tools` and
`plugins`, with `claude_code_version`. The skills listed to the model, with their
descriptions:

```bash
claude -p "Copy verbatim, from your system prompt, the name and the description of every skill you can invoke with the Skill tool, one skill per line as 'name: description'. Output nothing else." --model haiku
```

The user-only skills' descriptions are in the executable, `readlink -f "$(command -v
claude)"`, written `name:"<skill>",menuDescription:"…"`; this machine's `grep`, ugrep,
refuses long patterns on it, where Python's `re` does not.
