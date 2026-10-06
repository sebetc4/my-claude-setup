# Claude Code Coupling

Every place where a tool of this repository depends on Claude Code, the agent it is
installed for and tested with today (`CLAUDE.md`, Principles). Each row says what another
agent would have to provide, so that a move starts from this list. A change that adds or
removes a tie updates its row.

Listed on 2026-09-28, from the tracked files outside `docs/roadmap/` and `docs/decisions/`.

## Install Target

| Tie | Where | What another agent needs |
|---|---|---|
| Install directory `~/.claude`, with `skills/`, `agents/`, `commands/` and `hooks/<domain>/` | `tools/claude_setup.py` (`COPIED_KINDS`, `domain_files`), `Makefile` (`CLAUDE_DIR`) | Its own directories; the installer already takes the target as `CLAUDE_DIR=` |
| `settings.json` receives each domain's `hooks.json` and `permissions.json`, with the placeholders `{{HOOKS_DIR}}`, `{{CLAUDE_DIR}}` and `{{REPO_DIR}}` resolved | `tools/claude_setup.py` (`resolve`, the merge), `domains/*/hooks.json`, `domains/*/permissions.json` | Its own hook registry and permission store, and a converter per format |
| Install state in `~/.claude/my-claude-setup.json` | `tools/claude_setup.py` (`STATE_FILE`) | A state file beside its own directories |
| Permission rule syntax: `Bash(<path>:*)`, `Edit(//<path>)`, `Read(//<path>/**)` | `domains/*/permissions.json`, `domains/*/tests/test_permissions.py`, `tests/test_domains.py` | Its own permission syntax, or none |
| Skill switches: `syncClaudeAiSkills` in the user settings; no plugin is installed since 2026-10-04 | `~/.claude/settings.json` (not tracked) | Its own way to turn a skill source off |

## Hooks

| Tie | Where | What another agent needs |
|---|---|---|
| Events and matchers: `PostToolUse` on `Edit\|Write\|MultiEdit` (and `Bash` for the dev hook), `SessionStart`, `Stop` | `domains/roadmap/hooks.json`, `domains/review/hooks.json`, `domains/skill-tooling/hooks.json`, `.claude/settings.json` | Equivalent lifecycle events, and its own tool names |
| Input on stdin: `tool_name`, `tool_input.file_path`, `tool_input.command`, `cwd`, `transcript_path`, `stop_hook_active` | `domains/roadmap/hooks/progress_guard.py`, `session_resume.py`, `domains/review/hooks/review.py`, `domains/skill-tooling/hooks/audit_skill.py`, `.claude/hooks/check-skills.py` | The same fields, or an adapter |
| Output: exit 2 with stderr shown to the agent; `hookSpecificOutput.additionalContext`; `{"decision": "block", "reason": …}` on `Stop` | the same files | A way to hand a message back to the agent, and to hold a stop |
| Environment: `CLAUDE_PROJECT_DIR` in the commands of the dev hook and of the repository's audit hook, `CLAUDE_CODE_SESSION_ATTENDED` in the review hook | `.claude/settings.json`, `domains/review/hooks/review.py` | Equivalent variables |
| A PreToolUse hook added to an evaluation run through `--settings`, refusing a call with `hookSpecificOutput.permissionDecision: deny` and its `permissionDecisionReason` | `domains/skill-tooling/skills/authoring-skills/scripts/guard.py`, `scripts/harness.py` (`hook_settings`, `guard_command`) | A hook before each tool call, given per session, that can refuse the call |

## Sessions And Transcripts

| Tie | Where | What another agent needs |
|---|---|---|
| Session id from `CLAUDE_CODE_SESSION_ID` | `domains/review/skills/tool-review/scripts/measure.py`, `record.py` | The session id, passed as `--session` otherwise |
| Transcripts in `~/.claude/projects/<project>/<session>.jsonl`, subagents under `<session>/subagents/` with a `.meta.json`; records marked `isMeta`, `tool_use` blocks for `Skill` and `Agent` with `subagent_type`, token usage | `domains/review/skills/tool-review/scripts/transcript.py`, `domains/review/tests/review_world.py` | A transcript reader per agent (row S18 of `docs/decisions/2026-09-28-skill-tooling.md`) |
| Token usage in transcripts: one record per content block of an assistant message, the last per `message.id` kept; `message.model`, the `<synthetic>` model of Claude Code's own messages, `message.stop_reason` marking a final usage, `usage.cache_creation` splitting writes into five-minute and one-hour entries, the record's `effort` and `isSidechain`; Claude Code's prices, cache writes at 1.25 or 2 times the input price by lifetime | `shared/usage/usage.py` | A usage reader per agent, and its prices |
| An evaluation run is `claude -p` with `--model`, `--effort`, `--max-budget-usd`, `--permission-mode auto`, `--permission-prompts none`, `--setting-sources project,local`, `--strict-mcp-config`, `--settings`, `--output-format json`, `--disallowed-tools Skill Agent` and `--add-dir`, the prompt on standard input, version 2.1.291 or later; the starting session's `CLAUDE*` variables removed but `CLAUDE_CONFIG_DIR`; the run's preamble forbids a nested `claude` session | `domains/skill-tooling/skills/authoring-skills/scripts/harness.py` (`command`, `environment`, `MIN_VERSION`, `DISALLOWED`), `scripts/run.py` (`PREAMBLE`) | Its own headless command line taking a model, an effort, a cost ceiling, denied tools, settings and extra folders, in another `harness.py` |
| A grading session is an evaluation run that runs the agent `skill-grader` from its file: `--agents <file>` holding `{name: {description, prompt, tools, model, effort}}` and `--agent <name>`, with `--model` and `--effort` read from the agent's frontmatter, since `--agent` applies the agent's model but not its effort (probed on 2.1.291) | `scripts/harness.py` (`command`, `agents_file`), `scripts/grade.py` (`read_agent`, `judge`) | Its own way to start a session as a defined agent, at a set model and effort, in another `harness.py` |
| The json result of `claude -p`: `type` `result`, `subtype` (`success` or what stopped the session), `is_error`, `session_id`, `total_cost_usd`, `duration_ms`, `num_turns`, `result`, `permission_denials`; the session's transcript found as `projects/*/<session>.jsonl` under `$CLAUDE_CONFIG_DIR` or `~/.claude`, its `tool_use` and `tool_result` blocks and `isMeta` records rendered for the grader | `scripts/harness.py` (`result_of`, `outcome`, `figures`, `transcript_of`, `tool_calls`, `render`) | Its own result and transcript, read by another `harness.py` |
| The line "Base directory for this skill: " that marks a loaded skill and gives its directory | `transcript.py`, `domains/review/skills/tool-review/SKILL.md`, `domains/roadmap/skills/roadmap/SKILL.md` | The skill's directory, given another way |

## Skills And Agents

| Tie | Where | What another agent needs |
|---|---|---|
| Agent format: frontmatter `name`, `description`, `tools` (`Read, Grep, Glob, Bash`; `Read, Bash`), `model: sonnet` | `domains/roadmap/agents/roadmap-auditor.md`, `domains/skill-tooling/agents/skill-auditor.md` | Its own subagent format, or none: the audit then runs in the session |
| Default install path written in text: `~/.claude/skills/roadmap/scripts/progress.py` | `domains/roadmap/agents/roadmap-auditor.md` | The path of its own install |
| Tool names in instructions: "Write tool", "the Skill tool" | `domains/review/skills/tool-review/SKILL.md`, `domains/roadmap/skills/roadmap/evals/grade.py` | Its own tool names |
| The root of personal skills is `$CLAUDE_CONFIG_DIR`, otherwise `~/.claude`: a path inside it reads that directory's `.agent-conventions.toml` | `shared/conventions/conventions.py` (`personal_dir`) and its copies | Its own personal directory, or a variable naming it |
| The skill audit's default profile is Claude Code's: its 20 frontmatter fields and their values, the 1,536-character listing cap, the reserved names `synced` and `anthropic-skills`, `` !`…` `` injections, `@` references, `$ARGUMENTS` and `${CLAUDE_…}` substitutions, `ultrathink` | `domains/skill-tooling/skills/authoring-skills/scripts/audit.py` (`FIELDS`, rules F6, F7, F10 to F12, N4, N9, N10, X1, X4 to X7, C5) | A profile of its own fields and body features; `--portable` already checks the Agent Skills standard alone |
| The writing guide states Claude Code's facts, each marked as such: the listing's 1,536-character cut and its share of the context, `disable-model-invocation`, `when_to_use`, compaction restoring the first 5,000 tokens of a skill, `context: fork`, `paths`, `disallowed-tools`, `hooks`, substitutions, `ultrathink`, `!` injections, and the two documentation indexes; the create-and-edit reference, that a `SKILL.md` change applies in the running session and a new skills folder needs `/reload-skills`; the audit reference, that `/skill-doctor` shows each skill's listing cost, tokens and uses | `domains/skill-tooling/skills/authoring-skills/references/writing-guide.md`, `references/create-and-edit.md`, `references/audit.md` | Its own listing, compaction, reload, cost report and frontmatter facts, beside the standard's, which the guide already gives |
| A closure may update or check the repository's instruction file, named `CLAUDE.md` in the examples | `domains/roadmap/skills/roadmap/references/close-phase.md`, `references/close-roadmap.md` | Its own instruction file, such as `AGENTS.md` |

## Evaluation And Development

| Tie | Where | What another agent needs |
|---|---|---|
| Dev hook `.claude/hooks/check-skills.py`, and the repository's skill audit hook until the skill-tooling domain is installed, registered in `.claude/settings.json` | those files and `domains/skill-tooling/hooks/audit_skill.py` | A hook of the development agent, or `make check` run by hand |
| Project instructions in `CLAUDE.md` | `CLAUDE.md` | The agent's own instruction file |
