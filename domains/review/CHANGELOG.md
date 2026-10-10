# Changelog — review

## 0.2.1 — 2026-10-10

- Skill `tool-review`, on what `skill-auditor` raised in three runs: the facts on the permission rules and on `python3` name their sources, `permissions.json`, Claude Code's permissions page and `CLAUDE.md`'s Gotchas; the section "What this skill never does", which repeated the description and the procedure, is removed, and what only it said moves into the procedure: the findings stay out of the conversation, which `make reviews` reads, and a review changes no file but through `record.py`.

## 0.2.0 — 2026-10-10

- `hooks/tools.json` takes, under `watch`, the points a review checks for a tool, by its id; `measure.py` adds each point of a tool under review to what the review must explain, so that the review judges what the tool produced, not only how it served. `authoring-skills` gets the three its comparison with the old tools left: a convention the model already knows explained, a step that can fail without its check, a rule enforced before a mechanical guard was weighed. `test_tools_json.py` refuses a point on a tool the lists do not name.

## 0.1.3 — 2026-10-09

- `hooks/tools.json` lists the skill-tooling domain's tools a session uses itself: skill `authoring-skills`, agent `skill-auditor` and hook `skill-tooling/audit_skill.py`. Agents `skill-grader` and `skill-comparator` stay out: `grade.py` and `compare.py` start them in unattended sessions, which the Stop hook never reviews.

## 0.1.2 — 2026-09-27

- A review stays out of the conversation it interrupts: no message while it runs, no report of its path or findings, and the turn ends on the question or next step the session had reached before the review. The Stop hook's request says so, and reads "This session used" since a tool may have served in an earlier turn.

## 0.1.1 — 2026-09-27

- `measure.py` and `record.py` run as commands, `<base>/scripts/measure.py`, no longer through `python3 -B`: a project hook may refuse the system interpreter in a command (scriptorium's does, and the first real review had to run them through `.venv/bin/python`, outside the permission rules). The scripts are executable, and the allow rules name them.

## 0.1.0 — 2026-09-27

- Hook `review.py` (Stop): when a tool listed in `hooks/tools.json` and installed by this repository served in a session, requests a review of it once per session, then closes the review turn that follows.
- Skill `tool-review`: `measure.py` prints the measured block, what the review must explain and the draft's path; `record.py` validates the draft and writes the review under the repository's `reviews/`. Both share `transcript.py` and `reviewfile.py`.
- `permissions.json`: the two scripts, the drafts under `reviews/`, and the skill's own files, allowed without a prompt.
