# my-claude-setup

Source of truth for the user's Claude Code setup: domains of skills, agents, commands and hooks, installed into `~/.claude` by copy.

## Layout

- `domains/<domain>/{skills,agents,commands,hooks}/` + `hooks.json` + `permissions.json` - one folder per domain; only the folders are copied; `hooks.json` and `permissions.json` (`{"allow": [...]}`) are merged into `settings.json`, where `{{HOOKS_DIR}}` resolves to `~/.claude/hooks/<domain>`, `{{CLAUDE_DIR}}` to `~/.claude` and `{{REPO_DIR}}` to this repository
- `domains/<domain>/skills/<name>/evals/` - `evals.json`, `checks.py` (skill-specific static checks), `test_*.py`; never installed
- `tools/claude_setup.py` - install logic (plan, conflicts, copy, merge hooks and permission rules into `settings.json`, state in `~/.claude/my-claude-setup.json` with each domain's `repo`); disable also removes a `__pycache__` a hook import left behind; `Makefile` only wraps it
- `domains/<domain>/VERSION` + `CHANGELOG.md` - `X.Y.Z`; the changelog's first `## ` entry must match; `make list` shows installed and repository versions
- `domains/<domain>/tests/test_*.py` - domain tests (hooks…); never installed
- `domains/roadmap/hooks/` - `progress_guard.py` (PostToolUse: progress block consistency, single 🟡) and `session_resume.py` (SessionStart: open phase context); both find `skills/roadmap/scripts/progress.py` by walking their ancestor directories, which works in the repo and once installed
- `domains/roadmap/agents/roadmap-auditor.md` - read-only closure audit, called from the `## Audit` section of `close-phase.md` and `close-roadmap.md`
- `domains/review/` - temporary tool reviews: `hooks/review.py` (Stop: requests a review once per tool and session when a tool of `hooks/tools.json` installed by this repository served), skill `tool-review` (`measure.py`, `record.py`, sharing `transcript.py` and `reviewfile.py`)
- `reviews/` - gitignored: one review per file and `errors.log`, written from any project by the review domain; read by `tools/reviews.py`
- `tests/check.py` - runs `tests/skills.py` on every skill, each skill's `evals/checks.py`, `tests/domains.py` on every domain (version, changelog, agents), and all `test_*.py`
- `.claude/hooks/check-skills.py` - dev hook: runs `tests/check.py` after edits under `domains/`, `tests/`, `tools/`; exit 2 shows failures
- `docs/decisions/YYYY-MM-DD-<subject>.md` - committed decision records: what was decided, the figures it rests on, and when to revisit
- `.superpowers/` - gitignored specs, plans, SDD workspaces; never commit

## Commands

- `make check` - all static checks and unit tests
- `python3 -B -m unittest -q tests/test_claude_setup.py` - installer tests
- `make list | enable D=<d> | update [D=<d>] | disable D=<d>` - add `FORCE=1` to override conflicts, `CLAUDE_DIR=<dir>` to target another dir
- `make enable D=roadmap CLAUDE_DIR=$(mktemp -d)` - try an install safely; never run enable/update/disable on the real `~/.claude` without asking
- `python3 domains/roadmap/skills/roadmap/scripts/progress.py [--check] <roadmap-folder>` - compute or verify a roadmap's progress block
- `make reviews` - what the tool reviews say: usage and median cost per tool, findings by recurrence

## Conventions

- Python standard library only, `unittest`; TDD (failing test first)
- English in code, messages and skill files; `tests/skills.py` rejects French words, compatibility wording (`legacy`, `deprecated`…) and a space before `%`
- Every file under a skill's `references/`, `assets/`, `scripts/` must be cited from `SKILL.md` or a file it cites
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

## Roadmaps

Root       : docs/roadmap/{pending,on-progress,completed}/
Language   : english
Checks     : make check
Versioning : git
