# Changelog — roadmap

## 2.0.4 — unreleased

- `scripts/conventions.py` and `references/conventions.md`, the copy of `shared/conventions/`, know the review domain's `[review]` table, its key `tools`; the skill still reads `[roadmap]` alone.

## 2.0.3 — 2026-10-12

- The repository is renamed `my-agent-setup`, and its texts name it so: `close-phase.md` and `close-roadmap.md`, where they say where `make enable D=roadmap` runs, and `scripts/conventions.py`, the copy of `shared/conventions/`.

## 2.0.2 — 2026-10-10

- The skill's text follows the writing guide of `authoring-skills`, on what `skill-auditor` raised in three runs: rules no longer in bold, which no eval called for; `close-phase.md`'s exception for a red check recorded as a known defect written as a conditional; the persuasion around the report in `close-phase.md` and `open-phase.md` cut to one clause of reason; the Traps sections of `close-phase.md` and `close-roadmap.md` removed, their rules being the Editing and Changelog invariants; `old-contract.md` states the mapping without the skill's history; "folder" for the skill's own folder and for every other, and `scripts/conventions.py` where `SKILL.md` said "the reader"; `create.md` loses its task duration and its phase-file length, which had no source.
- `close-phase.md`, step 5 Residue: the paths matching `residue` are listed with exact `find` commands, removed one by one, and listed again to check that none stays; a path that stays keeps the phase from being declared closed.

## 2.0.1 — 2026-10-09

- `references/conventions.md`, the copy of `shared/conventions/`: the mapping of a `## Roadmaps` block moves to `references/old-contract.md`, which `SKILL.md` names on `missing`, since only this skill had such a block; the `residue` row no longer restates how `.gitignore` patterns match; `scripts/conventions.py` is named where the file said "the reader", and "folder" replaces "directory" for the skill's own; a `checks` command is run as any other, never as one already approved, in place of a claim on the permission flow.
- `scripts/progress.py` and `scripts/check_links.py` are called by their path, as `scripts/conventions.py` is; `permissions.json` still allows the conventions reader alone.
- Evals: they run on the eval scripts of `authoring-skills` (skill-tooling) in place of skill-creator's, kept under `study/`. `evals/fixtures.py <case> <folder>`, formerly `build_fixtures.py`, builds one case, its `.agent-conventions.toml` tracked so that a run's change to it shows; `evals/grade.py <iteration>` decides every assertion from the fixture, the run's `changes.json` and `outputs/`, and writes `assertions` where skill-creator's format said `expectations`; each case is `kind = "task"`, `setup = "fixture"`.

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
