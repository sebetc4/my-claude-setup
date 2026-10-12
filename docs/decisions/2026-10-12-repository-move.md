# Repository Move — 2026-10-12

Decided with the user on 2026-10-12, once Phase 0 of roadmap `token-usage` was closed:
**this repository moves from `/code/claude/my-claude-setup` to `/code/ai/my-agent-setup`,
its Claude Code history with it, and its content is renamed afterwards, in a session
started at the new path.** The GitHub repository keeps its name for now.

## Decisions

- **The name, `my-agent-setup`.** The setup is written for any agent; only its install
  target is Claude Code's (`CLAUDE.md`, Principles). Singular, as English puts a noun
  before a noun, and as `.agent-conventions.toml` and the Agent Skills standard do.
- **The place, `/code/ai/`,** beside `scriptorium`, out of `/code/claude/`.
- **Two steps.** First the move, by a script run in a terminal while no session or
  window works in the repository: a running session would go on writing its transcript
  under the old project folder. Then the content rename, as its own piece of work, before
  Phase 1 of roadmap `token-usage` opens, so that the phase's Start Commit follows both.
- **The history follows.** Claude Code keeps a project's sessions and auto memory under
  `~/.claude/projects/<the path, every character but a letter or a digit turned into ->`:
  `-code-claude-my-claude-setup` is renamed `-code-ai-my-agent-setup`. The transcripts are
  not rewritten, and their records keep `cwd` `/code/claude/my-claude-setup`.
- **GitHub unchanged.** The remote stays `git@github.com:sebetc4/my-claude-setup.git`
  until the user renames the repository there.

## Inventory

What names the old path on 2026-10-12, at `cc07914`:

- `~/.claude/projects/-code-claude-my-claude-setup/`: 88 entries, 191 MB, the memory
  index and seven notes.
- `~/.claude/my-claude-setup.json`, each domain's `repo`, and `~/.claude/settings.json`,
  the review domain's rule `Edit(//code/claude/my-claude-setup/reviews/*.draft)` from
  `{{REPO_DIR}}`. `make update` rewrites both: a domain whose `repo` is not the
  repository it runs from is outdated.
- 19 project folders of `claude -p` runs, `-tmp-claude-1000--code-claude-my-claude-setup-…`,
  named after the scratchpad they ran in: left as they are, their sessions found by id.
- Running sessions and windows only: `~/.claude/ide/*.lock`, `~/.claude/sessions/*.json`.
- Nothing in `~/.claude.json` (no entry for this repository, whose sessions run from the
  VS Code extension), `~/.claude/history.jsonl`, `.agent-conventions.toml`,
  `.claude/settings*.json`, another repository under `/code`, a git worktree or hook.
- The installed copy of the roadmap skill's `references/create.md` opens with a stray `o`,
  written on 2026-10-11 at 20:43: `make list` shows roadmap `modified`, and `make update`,
  which updates every domain at once, stops on it. It is the only difference;
  `make update FORCE=1` puts the repository's text back.
- The content: `my-claude-setup` on 76 lines of 29 tracked files, among them texts the
  tools install: the review domain's `review.py`, `transcript.py`, `tool-review`'s
  `SKILL.md` and `format.md`; the roadmap skill's `close-phase.md`, `close-roadmap.md` and
  `conventions.py`; `authoring-skills`' references and viewer. One closed report of
  roadmap `skill-tooling`, `phase-3-writing-method-report.md`, holds the absolute path.

## The Move

`move.sh`, kept out of the repository: without an option it checks and prints its plan;
`--apply` moves; `--force` passes `FORCE=1` to `make update`. A trial on a clone with a
scratch Claude directory refused a busy repository and a changed install, then moved both
folders, reinstalled the three domains and removed the stray `o`.

1. Checks, every one reported: the old path is a repository with a clean working tree;
   the new path and project folder do not exist yet; the script runs from outside the
   repository; no process has its working directory in the repository or a file open in
   it or in its project folder; no installed domain was changed, unless `--force`.
2. Moves the repository, then the project folder.
3. Runs `make update` from the new path, then `make list`.
4. Fails if the state file or `settings.json` still names the old path.

## Checks After The Move

In the first session at the new path, before any other work:

- the auto memory is loaded: its index is in the session's context;
- the VS Code extension's past conversations list this repository's sessions before
  2026-10-12;
- `make list` shows every domain `on`, and `make check` passes;
- the next tool review lands in the new path's `reviews/`.

## What Is Left

The content rename, in that session: the name in the texts above, `CLAUDE.md` and its
Gotcha on moving the clone; the installer's state file `~/.claude/my-claude-setup.json`,
and how the installer moves to a new name; a version and a changelog entry for each domain
whose installed texts change, then `make update`. The closed report keeps the old path:
a closed report is never rewritten.

## When To Revisit

- **When the GitHub repository is renamed:**
  `git remote set-url origin git@github.com:sebetc4/my-agent-setup.git`.
- **When Phase 1 of roadmap `token-usage` selects a window:** this repository's sessions
  from before the move keep the old `cwd` in the renamed folder
  ([Token Usage](2026-10-12-token-usage.md), When To Revisit).
