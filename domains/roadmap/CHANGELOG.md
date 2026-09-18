# Changelog — roadmap

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
