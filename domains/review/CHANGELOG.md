# Changelog — review

## 0.1.0 — 2026-09-27

- Hook `review.py` (Stop): when a tool listed in `hooks/tools.json` and installed by this repository served in a session, requests a review of it once per session, then closes the review turn that follows.
- Skill `tool-review`: `measure.py` prints the measured block, what the review must explain and the draft's path; `record.py` validates the draft and writes the review under the repository's `reviews/`. Both share `transcript.py` and `reviewfile.py`.
- `permissions.json`: the two scripts, the drafts under `reviews/`, and the skill's own files, allowed without a prompt.
