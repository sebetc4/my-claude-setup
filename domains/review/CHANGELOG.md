# Changelog — review

## 0.1.1 — 2026-09-27

- `measure.py` and `record.py` run as commands, `<base>/scripts/measure.py`, no longer through `python3 -B`: a project hook may refuse the system interpreter in a command (scriptorium's does, and the first real review had to run them through `.venv/bin/python`, outside the permission rules). The scripts are executable, and the allow rules name them.

## 0.1.0 — 2026-09-27

- Hook `review.py` (Stop): when a tool listed in `hooks/tools.json` and installed by this repository served in a session, requests a review of it once per session, then closes the review turn that follows.
- Skill `tool-review`: `measure.py` prints the measured block, what the review must explain and the draft's path; `record.py` validates the draft and writes the review under the repository's `reviews/`. Both share `transcript.py` and `reviewfile.py`.
- `permissions.json`: the two scripts, the drafts under `reviews/`, and the skill's own files, allowed without a prompt.
