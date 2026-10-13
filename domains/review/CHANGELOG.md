# Changelog — review

## 0.3.0 — unreleased

- `scripts/reviewfile.py` is a copy of `shared/reviewfile/`, its source, so that the review of several sessions writes the same format; `tools/reviews.py` still reads `tool-review`'s copy.
- `scripts/usage.py` and `scripts/usage.toml`, copied from `shared/usage/`: `scripts/transcript.py` reads an agent's runs through `usage.calls()`, each call once, their fresh and cached tokens unchanged.
- A review's measured block carries its cost in dollars: `cost`, the slice's calls by model, then by effort where the model uses one, main thread and subagents apart, every subagent included, the part resting on estimates and the prices' date; `derived.tool_cost`, each tool's own cost, a skill's or a hook's text priced at 2.6 characters a token, an agent's runs at their cost; `review`, the review's own turn up to the call after `record.py`, written by the Stop hook when it closes the turn. `tokens`, `turns` and the context peak take each call's final usage.
- `measure.py` prints each tool's cost beside its median over the earlier reviews of the same version, from three, and asks why past 1.5 times; the draft gives each tool `served`, `full`, `partial` or `none`, beside `brought`, which `record.py` checks and the review keeps.
- `scripts/reviewfile.py` writes and reads decimal numbers, so that a review holds dollars.
- The tools reviewed are chosen: the Stop hook asks for a review of a tool only when the `[review]` table of the setup repository's `.agent-conventions.toml` lists it, by its id, `agent:skill-auditor`, or by its domain, `roadmap`; the table is read by its path at every Stop, so that a change applies without `make update`, and never from the session's working directory; without it, or with `tools = []`, no review is asked for. `hooks/tools.json` keeps only `watch`, the points to watch. `scripts/conventions.py` and `references/conventions.md`, copied from `shared/conventions/`, read the table. A review requested is measured whole after its tool leaves the table, a review the user asks for covers every tool this repository installed, and the review domain's own tools are never reviewed.

## 0.2.2 — 2026-10-12

- The repository is renamed `my-agent-setup`, and its texts name it so: the Stop hook's request, the description and procedure of `tool-review`, `references/format.md`. `scripts/transcript.py` reads the installer's state from `~/.claude/my-agent-setup.json`, the state file's new name.

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
