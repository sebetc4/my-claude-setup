# Changelog — roadmap

## 2.0.0 — 2026-10-01

- The contract moves from the `## Roadmaps` block of `CLAUDE.md` to the `[roadmap]` table of `.agent-conventions.toml`, read by `scripts/conventions.py`, a copy of `shared/conventions/`. Keys: `root` (without the brace group), `language`, `versioning`, `checks` (a string, or `{ run, dir }` for a command run from a subfolder); `versioning = "none"` requires a `residue` list of `.gitignore` patterns, which a closure removes. A repository whose contract is still in `CLAUDE.md` is offered the move, key by key (`references/conventions.md`); without a conversation, the skill names the problem and stops.
- Every reference and the `roadmap-auditor` agent name the keys as the file does: `versioning = "git"`, `checks`, `language`, `root`. The closures' `CLAUDE.md` step becomes the repository's instruction file.
- Sub-roadmaps and parent roadmaps are gone: every roadmap of a repository lives under `root`. The questionnaire asks four questions, the closures no longer write into another roadmap, and the README and summary templates lose `## What This Sends Up To The Parent`.
- Hook `session_resume.py`: reads `root` from `.agent-conventions.toml`, also finds a phase in progress under `pending/`, and injects one line per open phase, to act on only when the request concerns it — no Work Log excerpt, no pending approvals.
- `open-phase.md`: the README's progress block is replaced with the output of `progress.py`; a phase already open is resumed, and an empty Work Log gets its first entry.
- `report.md`: on resuming a phase, the agent tells the user what carries into the session before any work.
- `permissions.json`: allows `scripts/conventions.py`, run by its path.
- Evals: the fixtures declare `.agent-conventions.toml`; the incomplete-contract scenario grades a stop that names the missing key.

## 1.1.1 — 2026-09-19

- `close-phase.md` and `close-roadmap.md`: the roadmap folder moves with `git mv` under `Versioning: git`. Left unstaged, the move reads as a deletion of every file at its old path, and the frozen report says so.

## 1.1.0 — 2026-09-19

- `close-phase.md`: the ritual is reordered. `## Files Changed` is computed last, once the roadmap folder has moved; the audit runs before the commit; the next phase is opened after the commit, so its `**Start Commit:**` is the commit that closed the phase before it.
- `close-roadmap.md`: the audit runs before a commit step of its own.
- `report.md`: a path the diff reports that belongs to earlier work is listed with a one-line reason, and `### Files Changed` says when it is written.

## 1.0.0 — 2026-09-17

- Skill `roadmap`: create, open, and close multi-phase roadmaps with one report per phase and a per-repository contract.
- Scripts `progress.py` (progress block, `--check`) and `check_links.py` (relative links).
- Hook `progress_guard.py`: keeps the README progress block consistent after each edit.
- Hook `session_resume.py`: brings back the open phase, its last Work Log entry, and its pending approvals at session start.
- Agent `roadmap-auditor`: audits a phase or roadmap closure before it is reported.
