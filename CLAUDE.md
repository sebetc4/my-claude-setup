# my-claude-setup

Source of truth for the user's agent setup: domains of skills, agents, commands and hooks, written for any agent and installed for now into Claude Code's `~/.claude` by copy.

## Principles

- Tools address the agent, never Claude: skills, agents, commands, hook messages and script output say "the agent" and assume no particular model, so that the setup can serve other agents later; only the install target is Claude Code's for now (`~/.claude`, `settings.json`, the hooks format), because the tools are built and tested with Claude Code
- Check and test scripts raise alerts, they do not define the rules: they were written from the skills this setup replaces, so when a tool improves a rule, the check follows the tool
- The official documentation informs, it does not cap: a tool may go past a documented limit or recommendation when its evaluations show it does better

## Layout

- `domains/<domain>/{skills,agents,commands,hooks}/` + `hooks.json` + `permissions.json` - one folder per domain; only the folders are copied; `hooks.json` and `permissions.json` (`{"allow": [...]}`) are merged into `settings.json`, where `{{HOOKS_DIR}}` resolves to `~/.claude/hooks/<domain>`, `{{CLAUDE_DIR}}` to `~/.claude` and `{{REPO_DIR}}` to this repository
- `domains/<domain>/skills/<name>/evals/` - `evals.json`, `checks.py` (skill-specific static checks), `test_*.py`; never installed
- `shared/<module>/` - one source for code several skills use, with its `tests/`; `tools/shared.py` copies each `.py` into a skill's `scripts/` and each `.md` into its `references/`, and `tests/check.py` fails on a copy that differs; edit the source, never a copy
- `shared/conventions/conventions.py` - reader and writer of `.agent-conventions.toml`, copied into the roadmap skill and imported by its hook; `shared/frontmatter/frontmatter.py` - a strict YAML subset that reads skill and agent frontmatter, copied into the skill audit and read by `tests/domains.py`
- `.agent-conventions.toml` - gitignored, at the root: this repository's conventions for the roadmap and skill tools (`[roadmap]` under `docs/roadmap`; `[skills]` under `domains/*/skills` and `.claude/skills`, eval runs in the gitignored `.eval-runs/`); a tool that finds it missing proposes values and writes it once the user agrees
- `tools/claude_setup.py` - install logic (plan, conflicts, copy, merge hooks and permission rules into `settings.json`, state in `~/.claude/my-claude-setup.json` with each domain's `repo`); disable also removes a `__pycache__` a hook import left behind; `Makefile` only wraps it
- `domains/<domain>/VERSION` + `CHANGELOG.md` - `X.Y.Z`; the changelog's first `## ` entry must match; `make list` shows installed and repository versions
- `domains/<domain>/tests/test_*.py` - domain tests (hooks…); never installed
- `domains/roadmap/hooks/` - `progress_guard.py` (PostToolUse: progress block consistency, single 🟡) and `session_resume.py` (SessionStart: one line per open phase, root read through `conventions.py`); both find the skill's `scripts/` by walking their ancestor directories, which works in the repo and once installed
- `domains/roadmap/agents/roadmap-auditor.md` - read-only closure audit, called from the `## Audit` section of `close-phase.md` and `close-roadmap.md`
- `domains/skill-tooling/` - skill `authoring-skills`, so far its audit: `scripts/audit.py` checks a skill against the rule catalogue of `docs/decisions/2026-10-03-skill-audit-rules.md`; hook `audit_skill.py` (PostToolUse: audits the skill holding an edited file, one line per failing rule), registered here in `.claude/settings.json` until the domain is installed
- `domains/review/` - temporary tool reviews: `hooks/review.py` (Stop: requests a review once per tool and session when a tool of `hooks/tools.json` installed by this repository served), skill `tool-review` (`measure.py`, `record.py`, sharing `transcript.py` and `reviewfile.py`)
- `reviews/` - gitignored: one review per file and `errors.log`, written from any project by the review domain; read by `tools/reviews.py`
- `tests/check.py` - runs `tests/skills.py` (the skill audit; errors fail, warnings print) on every skill, each skill's `evals/checks.py`, `tests/domains.py` on every domain (version, changelog, agents), and all `test_*.py`; `--skip-skills` leaves the skills out, `--brief` gives one line per failing test
- `.claude/hooks/check-skills.py` - dev hook: runs `tests/check.py --skip-skills --brief` after edits under `domains/`, `shared/`, `tests/`, `tools/`, silent after a command that ran the checks; exit 2 shows failures
- `docs/decisions/YYYY-MM-DD-<subject>.md` - committed decision records: what was decided, the figures it rests on, and when to revisit
- `docs/claude-code-coupling.md` - every place a tool depends on Claude Code, and what another agent would need instead
- `.superpowers/` - gitignored specs, plans, SDD workspaces; never commit

## Commands

- `make check` - all static checks and unit tests
- `make shared` - refresh the copies of `shared/` modules; `python3 tools/shared.py <skill-dir>` adds them to a new skill
- `python3 -B -m unittest -q tests/test_claude_setup.py` - installer tests
- `make list | enable D=<d> | update [D=<d>] | disable D=<d>` - add `FORCE=1` to override conflicts, `CLAUDE_DIR=<dir>` to target another dir
- `make enable D=roadmap CLAUDE_DIR=$(mktemp -d)` - try an install safely; never run enable/update/disable on the real `~/.claude` without asking
- `python3 domains/roadmap/skills/roadmap/scripts/progress.py [--check] <roadmap-folder>` - compute or verify a roadmap's progress block
- `make reviews` - what the tool reviews say: usage and median cost per tool, findings by recurrence
- `domains/skill-tooling/skills/authoring-skills/scripts/audit.py [--portable] [--checks] <skill-dir>` - audit a skill, in any repository

## Conventions

- Python standard library only, `unittest`
- Code and scripts test-first: a failing test, watched failing, then the code. Other artifacts take the proof that fits them — an eval for a skill's text, a probe for a platform behavior, the command that checks a configuration —, never a test that reads a text back
- English in code, messages and skill files; the skill audit rejects French words and a space before `%` in skill files, and warns on compatibility wording (`legacy`, `deprecated`…)
- Every file of a skill but its `evals/` must be reached from `SKILL.md`, through a file that names it or a script that imports it
- A change that adds or removes a dependency on Claude Code updates `docs/claude-code-coupling.md` in the same commit
- Commit messages: `(type) description`, e.g. `(feat)`, `(fix)`, `(refactor)`
- Releasing a domain: bump `VERSION`, add a `CHANGELOG.md` entry, then tag `<domain>-vX.Y.Z` on `main` after the merge

## Gotchas

- Installs are copies: repo edits reach `~/.claude` only via `make update`; hand edits in `~/.claude` become conflicts
- `~/.claude/skills/synced/` is managed by claude.ai; the installer must never touch it
- Hook changes in `settings.json` reach running sessions (seen in 2.1.283: a Stop hook enabled mid-session fired in a conversation started hours before), so a hook being tried fires in every open conversation; the VS Code extension runs its own Claude Code binary (`CLAUDE_CODE_EXECPATH`), whose version can differ from the CLI's
- Skill evals: give run agents a copy of the skill without `evals/` (see `evals/grade.py`) and forbid the Skill tool, or an installed copy shadows the one under test
- Roadmap README progress block is recomputed only at phase open/close; mid-phase it lags the ticked tasks by design
- The review domain writes into this repository's `reviews/` from every project; after moving the clone, `make update D=review`
- A script a skill runs from `~/.claude` is an executable called by its path: a permission rule never matches a Bash command carrying a heredoc (hand data through a file), and a project hook may refuse `python3` in a command (scriptorium's does)
- Probed on 2.1.283: a skill's `allowed-tools` grants nothing in headless runs, so permissions come from the installer's allow rules; `skillOverrides` cannot hide a plugin skill, only a `Skill(plugin:skill)` deny rule stops one; this repository's `.claude/settings.local.json` overrides the user's `enabledPlugins` (superpowers and skill-creator are off here; roadmap `working-method` turns superpowers off everywhere)
- Seen in 2.1.286: in a subagent, Write refuses any file whose name matches `^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$`, case-insensitive, so an eval run closing a roadmap writes `summary.md` through Bash
