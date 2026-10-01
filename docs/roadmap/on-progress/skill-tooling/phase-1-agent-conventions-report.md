# Phase 1 Report: Agent Conventions

**Phase:** [phase-1-agent-conventions.md](phase-1-agent-conventions.md)
**Start Commit:** 1073ead

---

## Work Log

### 2026-09-29

Resumed the phase, opened on 2026-09-28 with an empty report. Read Phase 0 and its
report, the decision record's script rule and ownership answer, the roadmap skill, its
hook, the installer, and the contracts of scriptorium and forma-rust: forma-rust runs its
checks from a subfolder and lists its residue files in prose, so the design needs a
working directory per check and a residue list. Phase 0 names the shared keys as its
output, but neither its report nor the decision record settles them: the design proposes
them.

At the user's request, read `note.md` and the tool reviews (`make reviews`). Three
reviews and the note report the same noise: `session_resume.py` injects the open phase
and its last Work Log entry into every session, related or not, and that text is reread
at every turn. Other findings touch files this phase already changes: `open-phase.md`
(an opened phase with an empty report), `references/report.md` (say what the previous
report carries before working).

The user approved adding three of them to this phase: cutting the hook's injection to
one conditional line, `open-phase.md` on an empty report, `references/report.md` on what
a resume tells the user. The phase grows from 16 to 19 tasks; the README's progress
block and phase list follow `progress.py`.

### 2026-10-01

Wrote the design in `.superpowers/specs/2026-10-01-agent-conventions-design.md`: the
shared keys (`language`, `versioning`, `residue`, `checks`, overridable per table), the
`[roadmap]` and `[skills]` tables, a lookup that stops at the first `.git` or
`.agent-conventions.toml`, a reader that always exits 0 and prints a status line, the
validation messages, checked copies of one source as the packaging, and the
fill-or-fix procedure. Four points left for the user to decide.
The user approved the design and its four points as proposed.

Wrote 37 failing tests of the reader in `shared/conventions/tests/test_conventions.py`
(lookup, resolution, every validation message, output, the command), then
`shared/conventions/conventions.py`; all pass. `tests/check.py` now runs
`shared/*/tests/test_*.py`, and `make check` is green. The reader validates through a
schema held in the module, `SHARED` and `TOOLS`: a new table or key is a change there.

Added `--write <draft> [--root <dir>]`, ten tests first: it validates the draft with the
reader's messages, never overwrites, writes the file and adds `/.agent-conventions.toml`
to `.gitignore` only when the root holds `.git`. `--root` was not in the design: it
serves the `no-root` case, where the user names the root (design § 5, step 4).

Packaged the reader: `tools/shared.py`, eight tests first, copies each file of a
`shared/<module>/` into the skills that already hold one of its copies (`.py` into
`scripts/`, `.md` into `references/`), and `--check` reports a differing or missing
copy; `tests/check.py` runs that check and `make shared` refreshes. Copied the reader
into `domains/roadmap/skills/roadmap/scripts/`, cited it in the skill's Scripts section,
and gave the domain its first `permissions.json`, tested in
`domains/roadmap/tests/test_permissions.py`. Checked that a copy edited by hand turns
`make check` red and that a trial install into a temporary directory carries the
reader. `CLAUDE.md` documents `shared/` and `make shared`.

Wrote the procedure, `shared/conventions/conventions.md`: what each status calls for,
the stop without a conversation, creating, fixing and rooting the file in one, the
keys, where to look for candidates, and how an old `## Roadmaps` block maps to the
keys. A test fails when the module knows a key, an allowed value or a status the
procedure does not name. Copied it into the roadmap skill with `make shared`.

Migrated the roadmap skill. The snapshot for the eval comparison is the skill at the
start commit `1073ead`, which `grade.py`'s procedure archives itself. `SKILL.md` runs
the reader first and shows two TOML files; `evals/checks.py` now validates every TOML
example of `SKILL.md` with the reader (a mutated example is caught). Renamed the
contract's keys in every reference and in the `roadmap-auditor` agent — `Versioning:
git` became `versioning = "git"`, and so on — and turned the closures' `CLAUDE.md`
step into "the instruction file"; residue now comes from `residue`.

Rewrote `session_resume.py`, eleven tests first: it reads `[roadmap].root` through the
skill's `conventions.py`, looks under `on-progress/` and `pending/`, and injects one
line per open phase — roadmap, phase, task count, file, and an instruction that holds
only when the request concerns the phase. The Work Log excerpt, the pending lines and
the 4,000-character cap are gone. It stays silent unless the reader says `ok`, so a
repository whose contract is still in `CLAUDE.md` gets nothing until its file exists.
`docs/claude-code-coupling.md` trades the `CLAUDE.md` contract row for the personal
root and the instruction file.

`open-phase.md` now replaces the README's progress block with `progress.py`'s output,
and opens with A Phase Already Open: a 🟡 phase with a `**Started:**` date is resumed,
and an empty Work Log gets its first entry. `references/report.md` has the resuming
agent tell the user, unasked, what carries into the session — binding decisions, owned
defects, unsettled dependencies — from the previous report while its own is empty.

Moved the roadmap evals. The fixtures declare the contract twice, since both versions
run on the same repository: `.agent-conventions.toml`, gitignored, for the migrated
skill, and the `## Roadmaps` block for the snapshot at `1073ead`. Built them once:
the reader says `ok`, `ok` and `invalid` (missing `versioning`), and the file stays out
of `git status`. Scenario 3 changed with the design: a run agent cannot ask the user,
so it is graded on stopping and naming the missing key, no longer on asking.

Walked the user through what each `[skills]` key does, on a fictitious skill. Naming the
workspace `.evals` beside a skill's `evals/` confused the two — eval definitions,
committed and never installed, against run outputs, gitignored and disposable — so it
became `.eval-runs`; `dirs` gained `.claude/skills` for skills proper to this repository.
Created this repository's `.agent-conventions.toml` with the writer: both tables read
`ok`, and `.gitignore`, which ended without a newline, received the file's line, then
`/.eval-runs/`. The `## Roadmaps` block stays in `CLAUDE.md` until the installed skill
reads the new file. Bumped the roadmap domain to 2.0.0 with its `CHANGELOG.md` entry.

Launched the three roadmap evals with the user's go-ahead, per `grade.py`'s procedure, in
the new workspace `.eval-runs/skills/roadmap/`: `skill-new` copied without `evals/`,
`skill-snapshot` archived from `1073ead`, six background agents on the same prompt, each
told to work from its fixture repository, to leave `~/.claude/skills` and the Skill tool
alone, and to put in its final answer what it would otherwise ask. Two biases, equal
for both versions: this repository's dev hook runs `tests/check.py` (about 3.75 s)
after every Bash command while `domains/` has uncommitted changes, and the installed
`progress_guard.py` 1.1.1 fires on their roadmap edits.

The six runs finished; each transcript shows the run used only its own copy — the
mentions of `~/.claude/skills` are the prohibition passed on to the `roadmap-auditor`.
Graded with `grade.py`, aggregated with skill-creator's `aggregate_benchmark.py`, and
viewed in `.eval-runs/skills/roadmap/iteration-1/review.html`:

| Scenario | Migrated | Snapshot `1073ead` |
|---|---|---|
| Close a phase with uncommitted work | 10/10 — 133k tokens, 16 min | 10/10 — 148k tokens, 17 min |
| Close the whole roadmap | 10/10 — 104k tokens, 10 min | 10/10 — 116k tokens, 12 min |
| Create with an incomplete contract | 3/3 — 44k tokens, 2 min | 2/3 — 108k tokens, 8 min |

The migrated skill passes 23 assertions out of 23, the snapshot 22: given a contract
without `Versioning`, the snapshot wrote the whole roadmap, then asked; the migrated
skill ran the reader, stopped on `invalid`, named the key and proposed the fix unapplied.
Three things the assertions do not grade. Both closures of a whole roadmap had Write
refuse `summary.md` — Claude Code refuses, in a subagent, any file whose name matches
`^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$` (found in the 2.1.286 binary) — and both
wrote it through a heredoc. Facing the user's uncommitted work at a phase closure, the
migrated run left it alone and held the next phase until the user commits, while the
snapshot committed it itself and opened the next phase; the skill says neither, in either
version. The auditor again ran `git status`, outside its allowed commands.

With the user's go-ahead, installed roadmap 2.0.0 (`make update D=roadmap`, no
conflict): the installed reader says `ok` here, its allow rule is in `settings.json`, and
the installed hook injects one line in this repository and stays silent in scriptorium,
which has no file yet. Removed the `## Roadmaps` block from `CLAUDE.md`, documented
`.agent-conventions.toml` in its Layout, updated the hook's line, and added the Write
refusal to its Gotchas, as the user approved.

Moved the two other contracts with the writer, at the user's go-ahead. scriptorium: its
file written and gitignored — its `.gitignore` already held uncommitted changes of the
user's, left as they were — its `## Roadmaps` block removed, and the installed hook now
shows its open phase in one line. forma-rust, which has no git: its `CLAUDE.md` backed up
first, the three checks run from `formation/projects/donjon-rpg/` and passing, so they
became `{ run, dir }` entries; its section went from 41 lines to 15 — the contract, the
explanations the skill already gives, and the history of the 2026-09-18 decision gave way
to two sentences, and the `progress.py` paragraph stayed word for word. The user means to
rewrite forma-rust's `CLAUDE.md` from a session in that repository.

Writing forma-rust's `residue` showed two things. Every lesson workspace keeps a
legitimate `Cargo.lock`, so the prose's "stray `Cargo.lock`" has no pattern that spares
them: left out. And nothing said how a `residue` entry matches, while "paths are relative
to the root" read `target/` as the root's only: entries are now `.gitignore` patterns, in
`conventions.md` and in `close-phase.md`'s residue step, which `CHANGELOG.md` 2.0.0
states. The installed 2.0.0 predates that wording. Also found that the hook stays silent
in forma-rust, whose open phase sits in a sub-roadmap: it scans `<root>` only, as 1.1.1
did.

The user then asked to drop sub-roadmaps altogether — roadmaps nesting like Russian dolls
and scattered through the tree — for scriptorium's flat layout, and asked about a fourth
`blocked/` state folder. Advised against the folder: blocking is a relation, not a state,
it is often partial (one phase waits, not the roadmap), and every move breaks paths; the
`Blocked By` fields and ⏸️ already exist. The user agreed, and asked for the final
version at once rather than keeping the keys until the redesign, so that nothing of them
lingers in the tools. Removed `sub_roadmaps` and `parent` from the reader — a test now
refuses both — the procedure, `SKILL.md` (whose complete example also lost `Cargo.lock`
from its residue), `create.md` (four questions), both closures (their Parent step,
renumbered), both templates and the evals' Parent assertion; `make check` caught the
`SKILL.md` example first. Regraded the six existing runs on the new grid: 22/22 for the
migrated skill, 21/22 for the snapshot. Installed the final 2.0.0; forma-rust's file now
reads `invalid` on `sub_roadmaps`, left so for the session there, where the user will
explain the change.

---

## Decisions

- **`session_resume.py` injects one conditional line.** The roadmap, the phase in
  progress and its file, and "read them only if the request concerns this phase"; no
  Work Log excerpt. Approved by the user on 2026-09-29, after `note.md` and three tool
  reviews reported the current injection as noise in unrelated sessions.
- **The design of `.agent-conventions.toml` is approved** as written in
  `.superpowers/specs/2026-10-01-agent-conventions-design.md`, on 2026-10-01: shared keys
  `language`, `versioning`, `residue`, `checks`, each overridable by a tool's table; a
  string `address = "agent"`; a repository without git found through its file alone;
  one source under `shared/conventions/` with checked copies in each skill, kept equal
  by `tests/check.py`. Phase 2's `[skills]` checks read the keys this design defines.
- **The skill names the contract's keys as the file does:** `versioning = "git"`,
  `checks`, `language`, `parent`, `root`, `sub_roadmaps`, in `SKILL.md`, every reference
  and the `roadmap-auditor` agent, so the agent meets one vocabulary, the reader's. `<Root>`
  stays as the path placeholder. Taken on 2026-10-01; the task named only the closures.
- **This repository's `[skills]` table** — approved by the user on 2026-10-01:
  `dirs = ["domains/*/skills", ".claude/skills"]`, for the setup's skills and for the
  skills proper to this repository (row W4's two kinds); `evals = "evals"`;
  `workspace = ".eval-runs"`, one gitignored folder with a subfolder per kind — skills now,
  agents later — named apart from a skill's `evals/`; `address = "agent"`;
  `exclude = ["allowed-tools", "substitutions"]`, `!` commands staying allowed with a
  fallback, per the script rule. `exclude` serves this repository's portability goal; a
  repository whose skills only run under Claude Code leaves it out.
- **`.superpowers/` is not kept.** The user does not mean to keep the folder superpowers'
  skills brought in; where specs and plans go instead is not settled yet.
- **The roadmap domain goes to 2.0.0:** the contract changes format and every
  repository migrates, a breaking change; 1.2.0 had been announced before.
- **`residue` entries are `.gitignore` patterns:** a name without a slash matches at any
  depth, a pattern with a slash is a path from the root, and no entry may match a file
  the repository keeps. Taken on 2026-10-01, when forma-rust's list made the question
  concrete.
- **No sub-roadmaps and no parent roadmaps: every roadmap lives under `root`.** Set by the
  user on 2026-10-01; a roadmap waiting for another says so in `Blocked By`, and no
  `blocked/` folder is added. The keys left the tools in this phase; the dependency
  mechanics — `Blocked By` as a link, a blocked phase that cannot open, the closure
  that unblocks, an overview of all roadmaps — go to a separate roadmap for the roadmap
  skill, with the defects this phase left out. The design spec still shows both keys.
- **Findings outside the conventions stay out of this phase:** `progress.py` printing file
  names instead of phase titles, the README's Tasks column at closure, and the
  `roadmap-auditor` agent's commands and `progress.py` path. Set on 2026-09-29.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/skill-tooling/phase-1-agent-conventions-report.md`
- `domains/roadmap/permissions.json`
- `domains/roadmap/skills/roadmap/references/conventions.md`
- `domains/roadmap/skills/roadmap/scripts/conventions.py`
- `domains/roadmap/tests/test_permissions.py`
- `shared/conventions/conventions.md`
- `shared/conventions/conventions.py`
- `shared/conventions/tests/test_conventions.py`
- `tests/test_shared.py`
- `tools/shared.py`

**Modified**
- `.gitignore` — this phase added `/.agent-conventions.toml` and `/.eval-runs/`; the same
  diff holds the user's own edits, `/pending/` removed and `/study/` added, kept out of
  the closure commit
- `CLAUDE.md`
- `Makefile`
- `docs/claude-code-coupling.md`
- `docs/roadmap/on-progress/skill-tooling/README.md`
- `docs/roadmap/on-progress/skill-tooling/phase-1-agent-conventions.md`
- `docs/roadmap/on-progress/skill-tooling/phase-2-static-audit.md` — also holds an edit
  of the user's, "sessijungle noireon" in its While Working section, kept out of the
  closure commit
- `docs/roadmap/on-progress/skill-tooling/phase-4-evaluation-tooling.md`
- `domains/roadmap/CHANGELOG.md`
- `domains/roadmap/VERSION`
- `domains/roadmap/agents/roadmap-auditor.md`
- `domains/roadmap/hooks/session_resume.py`
- `domains/roadmap/skills/roadmap/SKILL.md`
- `domains/roadmap/skills/roadmap/assets/templates/roadmap-readme.md`
- `domains/roadmap/skills/roadmap/assets/templates/summary.md`
- `domains/roadmap/skills/roadmap/evals/build_fixtures.py`
- `domains/roadmap/skills/roadmap/evals/checks.py`
- `domains/roadmap/skills/roadmap/evals/evals.json`
- `domains/roadmap/skills/roadmap/evals/grade.py`
- `domains/roadmap/skills/roadmap/references/close-phase.md`
- `domains/roadmap/skills/roadmap/references/close-roadmap.md`
- `domains/roadmap/skills/roadmap/references/create.md`
- `domains/roadmap/skills/roadmap/references/open-phase.md`
- `domains/roadmap/skills/roadmap/references/report.md`
- `domains/roadmap/tests/test_hooks.py`
- `tests/check.py`

Outside the diff: this repository's gitignored `.agent-conventions.toml` and
`.eval-runs/`; roadmap 2.0.0 installed in `~/.claude`; in scriptorium, uncommitted,
`.agent-conventions.toml`, `.gitignore` and `CLAUDE.md`; in forma-rust, which has no
git, `.agent-conventions.toml` and `CLAUDE.md`, backed up in the session's scratchpad.

---

## Problems And Deviations

- **Acceptance criterion not ticked: the eval comparison holds for the text it ran on, not
  for the final one.** The migrated skill passed 23 assertions to the snapshot's 22, and
  22 to 21 regraded once the Parent assertion went; the removal of sub-roadmaps and parent
  roadmaps came after the runs, and the final text was not run. Left open: a run of the
  three scenarios on the installed 2.0.0 settles it.
- **Acceptance criterion not ticked: the conversation half of the fill-or-fix behavior is
  unverified.** The subagent half holds — scenario 3 stopped, named `versioning` and
  wrote nothing — but no eval puts a missing or malformed file before an agent that can
  ask. Left open; Phase 4's case types can carry it.
- **`domains/` still names `CLAUDE.md`'s old block in two places, by design:** the
  procedure maps an old `## Roadmaps` block when it proposes values for a missing file,
  and the eval fixtures write one for the snapshot. Neither reads its contract there.
- **Eval scenario 3 grades a stop, no longer a question.** The run agent works without
  the user, which the procedure treats as no conversation; the assertion "asks the user
  for Versioning" became "names the missing versioning key", which the snapshot also
  passes when it asks. The conversation half of that acceptance criterion has no eval.
- **The phase grew from 16 to 19 tasks,** with the three tasks from the tool reviews above.
- **forma-rust's stray `Cargo.lock` is not in its `residue`.** Each lesson workspace keeps a
  legitimate one, which a `Cargo.lock` pattern would have a closure delete in a
  repository without git. Left out; the user can add the precise path once known.
- **The skill does not say what a closure does with the user's uncommitted work.** In the
  eval, one run left it and held the next phase, the other committed it unasked. A
  roadmap-skill defect outside the conventions; left open, for the user to place.

---

## Changes To Later Phases

- `phase-4-evaluation-tooling.md`: a constraint — in a subagent, Write refuses files named
  like reports, `summary.md` among them; the design decides between `claude -p` runs and
  a warning in the run prompt.
- `phase-2-static-audit.md`: the `[skills]` checks task names the three values of
  `exclude` and adds a `workspace` that git does not ignore, which the reader does not
  check.
- `phase-4-evaluation-tooling.md`: the workspace preparation task writes under the
  repository's `[skills] workspace`, in a `skills/<skill-name>/` subfolder, so evaluated
  agents can share the folder later.

---

## Assessment

The phase gave every tool of this setup one place to read a repository's conventions.
`shared/conventions/` holds the reader and writer of `.agent-conventions.toml`, 51 tests,
and the procedure that fills or fixes the file; `tools/shared.py` keeps their copies
equal; and the roadmap skill, its hook and its evals moved onto the file as roadmap
2.0.0, installed. Three repositories carry the file, and their `CLAUDE.md` no longer
carries a contract. The migrated skill did at least as well as the snapshot in the evals
— the snapshot wrote a whole roadmap on an incomplete contract — and the session hook
injects one conditional line instead of a Work Log excerpt.

The phase also changed what a roadmap can be: at the user's request, sub-roadmaps and
parent roadmaps are gone, every roadmap lives under `root`, and the dependency
mechanics, with the roadmap-skill defects left out here, go to a separate roadmap. Two
acceptance criteria stay open: the final text was not re-run after that removal, and the
conversation half of the fill-or-fix behavior has no eval.

Phase 2 needs to know first: this repository's `[skills]` table exists —
`dirs = ["domains/*/skills", ".claude/skills"]`, `evals = "evals"`,
`workspace = ".eval-runs"`, `address = "agent"`, `exclude = ["allowed-tools",
"substitutions"]` — and reads through `conventions.py skills`; the reader checks types and
allowed values but not that the workspace is gitignored, which Phase 2's checks now
cover; and a new skill gets the reader with `python3 tools/shared.py <skill-dir>`.
