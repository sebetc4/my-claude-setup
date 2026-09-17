# Changelog — roadmap

## 1.0.0 — 2026-09-17

- Skill `roadmap`: create, open, and close multi-phase roadmaps with one report per phase and a per-repository contract.
- Scripts `progress.py` (progress block, `--check`) and `check_links.py` (relative links).
- Hook `progress_guard.py`: keeps the README progress block consistent after each edit.
- Hook `session_resume.py`: brings back the open phase, its last Work Log entry, and its pending approvals at session start.
- Agent `roadmap-auditor`: audits a phase or roadmap closure before it is reported.
