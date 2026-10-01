# Superpowers study — 2026-10-01

Draft. The superpowers-study roadmap writes this record from its Phase 0 on: Phase 0 sets
the inventory and the method, Phases 1 to 3 add the verdicts, and Phase 4 writes the
decision, the target architecture and when to revisit. Until then nothing below is
decided, except where a section says who decided it and when.

The decisions taken at the roadmap's opening, in its README, bind every verdict: the
plugin is turned off everywhere rather than vendored, a kept capability is rewritten for
this setup with superpowers' MIT notice wherever its text is adapted, `writing-skills` is
out, and `.superpowers/` is not kept.

## Decision

Written by Phase 4.

## Sources

- superpowers 6.4.1, released upstream on 2026-09-18, commit `5bf4e78`, MIT, "Copyright
  (c) 2025 Jesse Vincent". Local copy `study/superpowers/6.4.1/`, which `.gitignore` keeps
  out of the repository, identical to the installed
  `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/` (`diff -rq`,
  2026-10-01): 231 files.
- superpowers 6.3.0, tag `v6.3.0`, commit `b36e082`. Local copy `study/superpowers/6.3.0/`,
  a git clone, identical to its cache: the version the 2026-09-18 baseline measured.
- Fetched on 2026-10-01: the Claude Code page on the `.claude` directory
  (https://code.claude.com/docs/en/claude-directory, cited as **docs §** section). Later
  phases add the pages they cite.

Line numbers refer to 6.4.1, and to a skill's `SKILL.md` unless a file is named.

## Inventory

### Versions In Use

From `~/.claude/plugins/installed_plugins.json` on 2026-10-01:

| Scope | Version | Installed, last updated |
|---|---|---|
| user, every project | 6.4.1 | 2026-09-11, 2026-09-24 |
| local, this repository | 6.4.1, off since 2026-09-28 (`.claude/settings.local.json`) | 2026-09-17, 2026-09-26 |
| local, `/code/claude/scriptorium` and `~/Bookmarks/projects/scriptorium` | 6.4.1 | 2026-09-17 and 2026-09-29 |
| local, `/code/learn/forma-rust` | 6.4.1 | 2026-09-18, 2026-09-24 |
| local, `/code/claude/pdf-creator` and `/code/claude/my-claude` | 6.3.0 | 2026-09-11 and 2026-09-12 |

The 6.4.1 cache appeared on 2026-09-24: every session before that day ran 6.3.0.

### Skills

Tokens are characters divided by four, as the 2026-09-28 record measured them.

| Skill | Phase | `SKILL.md` | Companion files | Since 6.3.0 |
|---|---|---|---|---|
| `brainstorming` | 1 | 285 lines, ~4,400 tk | `visual-companion.md`; `scripts/start-server.sh`, `stop-server.sh`, `server.cjs`, `helper.js`, `frame-template.html`; `spec-document-reviewer-prompt.md`, cited nowhere | `SKILL.md` ~3,900 → ~4,400; companion guide revised |
| `writing-plans` | 1 | 192, ~2,300 | `plan-document-reviewer-prompt.md`, cited nowhere | ~1,800 → ~2,300 |
| `executing-plans` | 1 | 373, ~5,100 | `scripts/task-start`, `scripts/task-done`, new; also runs `subagent-driven-development`'s `sdd-workspace` and `review-package` | ~600 → ~5,100: rewritten around a ledger and a final review |
| `subagent-driven-development` | 1 | 568, ~8,100 | `implementer-prompt.md`, `task-reviewer-prompt.md`, `re-review-prompt.md`; `scripts/sdd-workspace`, `task-brief`, `review-package` | `SKILL.md`, two prompts and the three scripts revised |
| `dispatching-parallel-agents` | 1 | 167, ~1,500 | — | unchanged |
| `test-driven-development` | 2 | 330, ~2,400 | `writing-good-tests.md` | ~2,250 → ~2,400 |
| `verification-before-completion` | 2 | 120, ~900 | — | unchanged |
| `systematic-debugging` | 2 | 283, ~2,400 | `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md` with `condition-based-waiting-example.ts`, `find-polluter.sh`; `CREATION-LOG.md`, `test-academic.md`, `test-pressure-1.md` to `-3.md`, cited nowhere | `root-cause-tracing.md` revised |
| `requesting-code-review` | 2 | 95, ~750 | `code-reviewer.md`, also the final reviewer of both executors | both files revised |
| `receiving-code-review` | 2 | 205, ~1,550 | — | unchanged |
| `using-git-worktrees` | 3 | 167, ~1,700 | — | unchanged |
| `finishing-a-development-branch` | 3 | 225, ~1,950 | — | unchanged |
| `using-superpowers` | 4 | 65, ~800 | `references/`, one tool note per harness: antigravity, claude-code (new), codex, gemini, hermes, muse (new), pi | ~780 → ~800 |
| `diagnosing-superpowers` | 4 | 120, ~1,700 | `prompts/`, 11 subagent prompts; `references/`, 4; `templates/`, 4 | new in 6.4.1 |
| `writing-skills` | out | 681, ~6,650 | ruled by skill-tooling's Phase 0, rows W1 to W30 of `2026-09-28-skill-tooling.md` | — |

### Agent Prompts

The plugin defines no named agent and has no `agents/` folder: every dispatch is a
general-purpose subagent given a template, which opens with `Subagent (general-purpose):`
and a `model:` field (`implementer-prompt.md:6-10`).

| Prompt | Dispatched by | When |
|---|---|---|
| `implementer-prompt.md` | `subagent-driven-development` | once per task; resumed for fix rounds 1 to 3, replaced on a stronger model for rounds 4 and 5 (`subagent-driven-development:375-386`) |
| `task-reviewer-prompt.md` | `subagent-driven-development` | after each task: spec compliance and quality |
| `re-review-prompt.md` | `subagent-driven-development` | after each fix round, on the fix diff only |
| `requesting-code-review/code-reviewer.md` | both executors, `requesting-code-review` | the final whole-branch review, on the most capable model; otherwise on demand |
| `spec-document-reviewer-prompt.md`, `plan-document-reviewer-prompt.md` | nobody | their callers went in 5.0.6 (2026-03-24), when inline self-review replaced the review loops (`RELEASE-NOTES.md:381-388`) |
| `diagnosing-superpowers/prompts/`: seven analysts — `skill-timeline`, `plan-adherence`, `repeated-work`, `stumbles`, `quality-evidence`, `request-conflicts`, `cost-and-time` — with `analyst-common.md`, `scrub.md`, `scrub-audit.md`, `similar-session.md` | `diagnosing-superpowers` | the analysts in parallel at triage, scrub and audit for an export, one per candidate for similar sessions (`diagnosing-superpowers:36-43`, `:55-70`) |

Every worker prompt forbids its worker to dispatch subagents (`implementer-prompt.md:52`,
`task-reviewer-prompt.md:57`, `re-review-prompt.md:48`, `code-reviewer.md:56`).

### SessionStart Hook

`hooks/hooks.json` matches `startup|clear|compact` and runs `hooks/run-hook.cmd
session-start`, a file that both cmd.exe and bash run. `hooks/session-start` reads
`skills/using-superpowers/SKILL.md` whole and returns it wrapped in
`<EXTREMELY_IMPORTANT>You have superpowers.` (`session-start:27`), in the output field
each harness expects, chosen from environment variables: Cursor, Claude Code, Muse, then
Copilot CLI and the SDK standard. `hooks/hooks-cursor.json` is Cursor's copy. 6.4.1 adds
the Muse branch only.

### Scripts

Run by the skills:

| Script | Skill | What it does |
|---|---|---|
| `start-server.sh`, `stop-server.sh`, `server.cjs`, `helper.js`, `frame-template.html` | `brainstorming` | the visual companion: a dependency-free Node server on a local port, its screens under `<project>/.superpowers/brainstorm/<session>/`, or `/tmp` (`start-server.sh:9`, `:117-121`) |
| `task-start`, `task-done` | `executing-plans` | print a task's brief and BASE; run the task's tests and append its completion line to the ledger, only when they pass (`executing-plans:172-176`, `:224-231`) |
| `sdd-workspace`, `task-brief`, `review-package` | both executors | one workspace per plan under `.superpowers/sdd/`, ignored by its own `.gitignore` (`sdd-workspace:1-25`); a task's text extracted to a file; the log, stat and `diff -U10` of a range in one file |
| `find-polluter.sh` | `systematic-debugging` | finds by bisection the test that leaves unwanted files or state behind |
| `render-graphs.js` | `writing-skills` | out of scope |

`scripts/` at the plugin root — `bump-version.sh`, `lint-shell.sh`,
`package-codex-plugin.sh`, `sync-to-codex-plugin.sh` — serves the plugin's releases, never
a skill.

### Tests

`tests/` holds 66 files in 17 suites: per harness (antigravity, codex, codex-plugin-sync,
devin, hermes, kimi, opencode, pi), per component (brainstorm-server with 12 files, hooks,
shell-lint, version-bump) and per skill — `claude-code/`, headless `claude -p` runs on
`subagent-driven-development`, worktrees and the `executing-plans` scripts;
`explicit-skill-requests/`, whether a skill named in a prompt fires, under an isolated
`HOME`; the structure of `diagnosing-superpowers`; `find-polluter.sh`; `render-graphs.js`.
The behavior evaluations, real sessions graded by an agent, live in another repository,
superpowers-evals, and do not ship with the plugin (`docs/testing.md`).
`systematic-debugging/` carries its own test material: `test-academic.md` and three
pressure scenarios.

### Other Files

Manifests and entry points for other harnesses — `.agents/`, `.codex-plugin/`,
`.cursor-plugin/`, `.devin-plugin/`, `.hermes-plugin/`, `.kimi-plugin/`, `.muse-plugin/`,
`.opencode/`, `.pi/`, `gemini-extension.json`, `index.js` — beside Claude Code's
`.claude-plugin/`; `docs/`, with the plugin's own specs and plans under
`docs/superpowers/`, 2026-01 to 2026-08, a porting guide and the testing page;
`RELEASE-NOTES.md`; contributor files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/`).

### Fixed Cost Per Session

Paid by every session where the plugin is on, whether a skill of it serves or not:

| | 6.3.0 | 6.4.1 |
|---|---:|---:|
| SessionStart injection | ~830 tk | ~850 tk |
| Skill listing, names and descriptions | ~600 tk, 14 skills | ~710 tk, 15 skills |
| Total | ~1,430 tk | ~1,560 tk |

The 2026-09-18 record measured about 1,400 on 6.3.0. The listing figure counts the
`superpowers:` names and the descriptions, not the harness's framing around them.

## Hand-Overs

The chain, as the skills write it:

1. **`using-superpowers`**, injected at every start, clear and compaction, has the agent
   invoke a skill at "even a 1% chance" that it applies (`using-superpowers:11`):
   `brainstorming` before building anything or entering plan mode, `systematic-debugging`
   before fixing a bug (`:22`, `:28-31`).
2. **`brainstorming`** classifies the request — spike, bounded or architectural — and
   gates any implementation behind the user's approval (`:38-88`). A spike ends on a
   recommendation; a bounded change goes straight to implementation, test-driven, with no
   plan (`:127`); an architectural one writes a spec, commits it, has the user review it,
   and hands over to `writing-plans` and nothing else (`:129-138`, `:184-186`, `:237-266`).
3. **`writing-plans`** writes a plan whose header names the spec and the executor
   (`:18`, `:61`, `:69`), asks the user to review it and to choose: subagent-driven, to
   `subagent-driven-development`; native, to `executing-plans` (`:167-192`).
4. **`executing-plans`** and **`subagent-driven-development`** start with
   `using-git-worktrees` (`executing-plans:110-113`, `subagent-driven-development:126-129`)
   and share one workspace and ledger, so that a plan can change executor midway
   (`executing-plans:121-139`). Inline, the agent loads `test-driven-development` before
   Task 1 (`executing-plans:149-152`), turns to `systematic-debugging` when a step's output
   shows the code wrong (`:195`), and lets `verification-before-completion` govern each
   completion claim (`:219`). With subagents, each task goes from implementer to task
   reviewer to scoped re-review, up to five fix rounds, through brief, report and review
   package files (`subagent-driven-development:246-443`).
5. Both end with a **final whole-branch review** by `requesting-code-review`'s
   `code-reviewer.md` on the most capable model, delete the plan's workspace, and hand
   over to **`finishing-a-development-branch`** (`executing-plans:234-304`,
   `subagent-driven-development:445-487`).
6. **`finishing-a-development-branch`** runs the suite, detects a worktree, confirms the
   base branch, offers a local merge, a pull request or nothing, and removes the worktrees
   under `.worktrees/` or `worktrees/`, the ones it takes as its own
   (`finishing-a-development-branch:14-201`).

Outside the chain: `systematic-debugging` sends to `test-driven-development` for the
failing test and to `verification-before-completion` before claiming success
(`systematic-debugging:177`, `:189`); `requesting-code-review` dispatches
`code-reviewer.md` (`:34`); no skill hands over to `receiving-code-review`,
`dispatching-parallel-agents` or `diagnosing-superpowers`, the second being named only in
Codex's tool note (`using-superpowers/references/codex-tools.md:11`).

What passes between them:

| Artifact | Written by | Read by | Kept |
|---|---|---|---|
| Spec, `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | `brainstorming` | `writing-plans`; both executors, as the binding authority (`executing-plans:143-147`) | committed (`brainstorming:244`) |
| Plan, `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` | `writing-plans` | both executors, the final reviewer | saved; no skill says to commit it |
| Worktree, `.worktrees/<branch>` by default | `using-git-worktrees` | every later step | removed after a local merge or a confirmed discard |
| Ledger, `.superpowers/sdd/<plan>/progress.md` | both executors, `task-done` | both executors, after a compaction | deleted with the workspace once the final review is clean (`executing-plans:300-302`, `subagent-driven-development:482-485`) |
| Brief, report and review package, in the same workspace | `task-brief`, the implementer, `review-package` | the implementer, the reviewers | deleted with the workspace |
| "Rulings I made" and "Deferred minors" | both executors, from the ledger | the user, in the final message | in the conversation only (`executing-plans:293-298`, `subagent-driven-development:473-480`) |

## Conventions Imposed On A Repository

| Convention | Where | Overridable |
|---|---|---|
| Specs in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, committed | `brainstorming:135`, `:241-244` | by "user preferences" (`:242`) |
| Plans in `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` | `writing-plans:18-19` | by "user preferences" |
| A workspace per plan under `.superpowers/sdd/`, ignored by its own `.gitignore` | `sdd-workspace:6-25`, `:46` | no: the script fixes the path |
| Companion screens under `.superpowers/brainstorm/`, and a reminder to add `.superpowers/` to `.gitignore` | `visual-companion.md:56-58`, `start-server.sh:117-121` | `--project-dir`, or `/tmp` without it |
| Diagnosis cases under `~/.superpowers/diagnosing-superpowers/<session-id>/`, in the home directory | `diagnosing-superpowers:33` | no |
| Worktrees under a declared directory, else `.worktrees/` or `worktrees/` if one exists, else `.worktrees/`; the directory added to `.gitignore` and committed when git does not ignore it | `using-git-worktrees:63-98` | a declared preference first (`:67`) |
| A worktree only with the user's consent, unless a preference is declared, and through the harness's own worktree tool first | `using-git-worktrees:41-57` | yes |
| No implementation on `main` or `master` without the user's consent | `executing-plans:112-113`, `subagent-driven-development:128-129` | the user's consent |
| Review ranges from `git merge-base main HEAD`, or `origin/main` | `executing-plans:236-238`, `subagent-driven-development:447-449`, `requesting-code-review:28` | given as examples |
| A commit closing each task's steps, the message shown as `feat: add specific feature` | `writing-plans:45-52`, `:135-140` | the plan's own steps |
| Integration by local merge, pull request through the forge's CLI, or nothing; a discard only on request, confirmed by typing `discard` | `finishing-a-development-branch:53-157` | no |
| Test commands guessed per ecosystem: `npm test`, `cargo test`, `pytest`, `go test ./...` | `finishing-a-development-branch:16`, `using-git-worktrees:121-132`, `test-driven-development:187-188` | the plan's commands (`executing-plans:224-229`) |
| Dependencies installed without asking: `npm install`, `cargo build`, `pip install -r requirements.txt`, `poetry install`, `go mod download` | `using-git-worktrees:102-119` | no |
| One todo per checklist item, and the skill announced at start | `using-superpowers:24`, `brainstorming:110-113`, `writing-plans:14`, `finishing-a-development-branch:12`, `using-git-worktrees:14` | no |
| GitHub through `gh`: pull requests, issue search and creation, review-thread replies | `finishing-a-development-branch:121-124`, `diagnosing-superpowers/references/github-issues.md:10`, `:30`, `receiving-code-review:205` | the forge's CLI, for pull requests |
| Precedence: the user's instruction files and requests, then skills, then default behavior | `using-superpowers:63-65` | — |

## Ties To Claude Code

The prose already addresses the agent — "you", and the user as "your human partner": the
plugin's spec of 2026-05-05 took "Claude" out of its generic prose
(`docs/superpowers/specs/2026-05-05-platform-neutral-prose-design.md`). The ties left:

- **Vocabulary.** "Claude Code is the reference harness: skills speak its vocabulary
  (`Agent` for a subagent dispatch, todos, `Skill`)"
  (`using-superpowers/references/claude-code-tools.md:3-4`); each other harness gets a
  translation note. The templates name a general-purpose subagent and a model
  (`implementer-prompt.md:6-10`, `code-reviewer.md:8`, `dispatching-parallel-agents:71-73`);
  `using-git-worktrees` names `EnterWorktree` and `--worktree` (`:53`, `:164`);
  `using-superpowers` names plan mode (`:22`); the companion's launch note names the Bash
  tool's `run_in_background` (`visual-companion.md:62-68`).
- **The hook** answers in `hookSpecificOutput.additionalContext` under Claude Code
  (`session-start:42-44`).
- **A platform fact in a script:** the workspace sits in the working tree because Claude
  Code refuses agent writes under `.git/` (`sdd-workspace:21-25`).
- **Instruction files:** `CLAUDE.md` named beside `AGENTS.md` and `GEMINI.md`
  (`using-superpowers:65`, `diagnosing-superpowers/prompts/request-conflicts.md:13`).
- **History:** `systematic-debugging/CREATION-LOG.md` records the skill's extraction from
  `~/.claude/CLAUDE.md` and speaks of "Claude" (`:7`, `:102`).

Models are chosen by tier — "fast, cheap", "standard", "most capable"
(`subagent-driven-development:184-219`) — never by name.

## Notes For Later Phases

Facts of the inventory that a later phase rules on:

- **Phase 1.** `executing-plans` does not stand alone: it runs
  `subagent-driven-development`'s scripts by relative path (`executing-plans:126`, `:236`),
  and both executors read `requesting-code-review/code-reviewer.md` (`executing-plans:243`,
  `subagent-driven-development:454`). The ledger's rulings reach the user only through the
  final message before the workspace is deleted, where this setup's roadmap keeps a
  phase's decisions in its report. The two document reviewer prompts are dead files.
- **Phase 2.** `executing-plans` requires `test-driven-development` and
  `verification-before-completion` (`:149`, `:219`), while the implementer prompt applies
  test-driven development only "if task says to" (`implementer-prompt.md:36`): the two
  executors do not hold one proof standard.
- **Phase 3.** The spec is committed when it is written (`brainstorming:244`), before any
  worktree exists (`writing-plans:16`, `executing-plans:110`): it lands on whatever branch
  the design ran on. A local merge starts with `git pull` on the base
  (`finishing-a-development-branch:95`).
- **Phase 4.** The fixed cost rose from ~1,430 to ~1,560 tokens per session with 6.4.1.
  `diagnosing-superpowers` overlaps this repository's review domain: both read session
  transcripts to explain how a tool served, one for superpowers' maintainers, the other
  for this repository.

## Method

### Capability Matrix

Phases 1 to 3 rule in the format of the 2026-09-28 record (Capability Matrix), adapted on
two points: a column says where a kept capability goes, and row ids carry a prefix per
skill.

- **One table per skill**, one row per capability: `| # | Capability | Verdict | Goes to
  | Reason |`.
- **Verdicts,** as on 2026-09-28: **keep** takes the capability as it is, rewritten for
  this setup; **improve** takes it with the change stated; **drop** leaves it out; **open**
  waits for a question the reason names.
- **Goes to:** for keep and improve, what receives the capability — an operation or a
  reference of the roadmap skill, a new skill, an agent, a hook, a key of
  `.agent-conventions.toml` — or `open` until the phase's mapping decides; `—` for drop.
  Phase 4 builds the target architecture from this column.
- **Row ids:** BR `brainstorming`, WP `writing-plans`, EP `executing-plans`, SD
  `subagent-driven-development`, DP `dispatching-parallel-agents`, TD
  `test-driven-development`, VC `verification-before-completion`, SY
  `systematic-debugging`, RQ `requesting-code-review`, RC `receiving-code-review`, GW
  `using-git-worktrees`, FB `finishing-a-development-branch`, US `using-superpowers`, DS
  `diagnosing-superpowers`, HK the SessionStart hook; numbered from 1 in each.
- **Citations:** in a skill's table, `:N` or `:N-M` is that skill's `SKILL.md` in 6.4.1; a
  companion file is named (`implementer-prompt.md:52`), another skill too
  (`executing-plans:149`), and 6.3.0 is written out (`6.3.0 executing-plans:12`).
- **Completeness:** every part this inventory lists — companion file, prompt, script,
  convention, hand-over — is covered by at least one row, if only by a drop; the phase
  that owns the skill checks it before closing.

The standard of evidence:

1. **Every reason cites evidence:** a source line; the documentation (docs §, spec §,
   best practices §, as on 2026-09-28, each page dated under Sources); a tool review
   (`reviews/<file>.md`, kept locally, or a `make reviews` figure with its date); a measure
   — the recount below, a size, a probe, an eval, or a wording micro-test by the method of
   row W22 of 2026-09-28 (one fresh sample per call, a no-guidance control, five
   repetitions or more); or this repository's record — a decision record, a phase report,
   `CLAUDE.md`, the user's session review of 2026-09-27 kept under `local-review/`. A
   decision of the user is cited with its date.
2. **The documentation and this repository's checks are evidence to weigh, not rules to
   obey,** as the Principles of 2026-09-28 say.
3. **Observed or reasoned:** a reason that predicts what an agent does says whether it was
   observed — in a transcript, a tool review, an eval, a probe — or reasoned from the text.
4. **Usage weighs need, never alone:** the 2026-09-18 figures measure adoption, not habit,
   and a practice can serve through another skill that requires it (`executing-plans:149`,
   `:219`). A drop resting on usage says where the practice lives instead, or that it
   lives nowhere.
5. **Settled rules are cited, not ruled again:** flowcharts (row W15), emphatic wording
   and rationalization tables (Tone), descriptions (Description), size budgets and
   scripts, all of 2026-09-28.

### Usage Recount

Phase 4 runs it on 2026-10-18, or up to the day if it runs sooner. Every figure comes from
a command run on the transcripts, as the baseline's did.

1. **Window:** events dated, by their UTC `timestamp`, from 2026-09-19 to the recount day.
   The baseline's 51 calls are exactly the 51 loads of 6.3.0 that the transcripts hold on
   2026-10-01 — the "Base directory for this skill" line of each load names its version —
   so no call falls between the baseline and the window.
2. **Working sessions:** the main transcripts `~/.claude/projects/*/*.jsonl`, as for the
   baseline. A session is a working session when one of its user messages carries
   `origin.kind` `human`; the others are runs — evals, probes — counted apart. On
   2026-10-01, 81 of the 529 transcripts were working sessions; the rest were 443 runs,
   441 of them under temporary folders or the home folder, the roadmap skill's evals among
   them, and 5 stubs holding no conversation. A working session counts when
   one of its events falls in the window; this repository's count only by their events
   before 2026-09-28 18:30 UTC, when an edit of `.claude/settings.local.json` turned the
   plugin off here, a day after its last call there.
3. **Calls:** the `tool_use` blocks named `Skill`, by `input.skill`: `superpowers:<name>`,
   or a bare `<name>` among the plugin's fifteen when no other installed skill bears it —
   on 2026-10-01 every call to the plugin carried the prefix. A call whose `tool_result`
   is an error — `Skill(superpowers:writing-skills)` has been refused since 2026-09-28 — is
   counted apart.
4. **Version:** the "Base directory for this skill" line that follows a call names the
   version that served it. Cost per call is given per version, since `executing-plans`
   grew from ~600 to ~5,100 tokens.
5. **Subagents:** `~/.claude/projects/*/*/subagents/*.jsonl`, which the baseline's glob
   did not read, are counted in a column of their own, outside the comparison.
6. **Cost per skill, once established:** assistant messages carry `attributionSkill` and
   `attributionPlugin` beside their `usage`; 1,452 of them named a superpowers skill on
   2026-10-01. Phase 4 first establishes, from a transcript it reads, which turns the
   attribution covers; until then the cost of a call stays the size of its `SKILL.md`, as
   in the baseline.
7. **Result:** the baseline's table — skill, calls, sessions, projects, `SKILL.md` tokens —
   with columns for the version, the subagent calls and the refused calls; the skills
   never invoked; and the share of working sessions calling a superpowers skill, against
   the baseline's below.

**The baseline, by working sessions.** Measured on 2026-10-01, by the rules above, over
the plugin's first period, 2026-09-04 to 2026-09-18: 41 working sessions in 10 projects,
beside 434 runs and stubs. 17 of them, 41 %, called a superpowers skill, in 7 projects,
and made all 51 calls; 32, 78 %, called a skill of any kind. The 2026-09-18 record's "only
8 % of sessions invoke any skill at all" was taken over 479 sessions, runs included: 434
of the 475 transcripts of that period still on disk are runs or stubs.

**Retention.** Claude Code deletes transcripts, subagent transcripts included, once they
are older than `cleanupPeriodDays`, 30 days by default (docs § Cleaned up automatically).
The user settings do not set it, and the user chose on 2026-10-01 to leave it so: the
roadmap runs ahead of the deadline. On 2026-10-01 the oldest transcript starts on
2026-08-31, which matches a baseline that began on 2026-08-21: older transcripts were
already gone on 2026-09-18. The baseline period's transcripts go from about 2026-10-04 —
the 17 working sessions where the plugin served, from about 2026-10-10 — and the window's
first day about 2026-10-19: the recount runs by 2026-10-18, and the figures above stay the
only baseline by working sessions.

## Capability Matrix

### Design And Planning

Written by Phase 1.

### Proof

Written by Phase 2.

### Git

Written by Phase 3.

### Plugin

Written by Phase 4.

## When To Revisit

Written by Phase 4.
