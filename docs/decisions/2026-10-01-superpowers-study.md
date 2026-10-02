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
2. **Conversations:** the main transcripts `~/.claude/projects/*/*.jsonl`, as for the
   baseline, grouped into conversations: two transcripts that share an assistant message
   id (`message.id`) belong to one, since a resumed or forked session copies the history
   it continues — under a new `sessionId`, often with new `uuid`s, sometimes with new
   timestamps. One conversation of 2026-09-10 sits in six transcripts. A conversation is a
   working one when one of its user messages carries `origin.kind` `human`; the others
   are runs — evals, probes — counted apart. On 2026-10-01, 81 of the 529 transcripts held
   working conversations; the rest were 443 runs, 441 of them under temporary folders or
   the home folder, the roadmap skill's evals among them, and 5 stubs holding no
   conversation. A working conversation counts when one of its events falls in the
   window; this repository's count only by their events before 2026-09-28 18:30 UTC, when
   an edit of `.claude/settings.local.json` turned the plugin off here, a day after its
   last call there.
3. **Calls:** the `tool_use` blocks named `Skill`, by `input.skill`, counted once per
   `tool_use` id, which copies keep: `superpowers:<name>`, or a bare `<name>` among the
   plugin's fifteen when no other installed skill bears it — on 2026-10-01 every call to
   the plugin carried the prefix. A call whose `tool_result` is an error —
   `Skill(superpowers:writing-skills)` has been refused since 2026-09-28 — is counted
   apart.
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
7. **Result:** the baseline's table — skill, calls, conversations, projects, `SKILL.md`
   tokens — with columns for the version, the subagent calls and the refused calls; the
   skills never invoked; and the share of working conversations calling a superpowers
   skill, against the baseline's below.

**The baseline, by working conversations.** Measured on 2026-10-01, by the rules above,
over the plugin's first period, 2026-09-04 to 2026-09-18: 32 working conversations in 10
project folders, held in 41 transcripts, beside 434 runs and stubs. 11 of them, 34 %,
called a superpowers skill, in 7 project folders; 24, 75 %, called a skill of any kind.
They made 29 distinct calls: `brainstorming` 10, `writing-plans` 5,
`subagent-driven-development` 4, `finishing-a-development-branch` 4, `executing-plans` 2,
`test-driven-development` 2, `systematic-debugging` 1, `writing-skills` 1. The 2026-09-18
record counted copies — its 51 calls are 29 calls and 22 copies — and its "only 8 % of
sessions invoke any skill at all" was taken over 479 transcripts, runs included: 434 of
the 475 of that period still on disk are runs or stubs. Phase 0 first counted transcripts
— 41 sessions, 41 % calling superpowers — and Phase 1 grouped them into conversations.

**Retention.** Claude Code deletes transcripts, subagent transcripts included, once they
are older than `cleanupPeriodDays`, 30 days by default (docs § Cleaned up automatically).
The user settings do not set it, and the user chose on 2026-10-01 to leave it so: the
roadmap runs ahead of the deadline. On 2026-10-01 the oldest transcript starts on
2026-08-31, which matches a baseline that began on 2026-08-21: older transcripts were
already gone on 2026-09-18. The baseline period's transcripts go from about 2026-10-04 —
the 11 working conversations where the plugin served, held in 17 transcripts, from about
2026-10-10 — and the window's first day about 2026-10-19: the recount runs by 2026-10-18,
and the figures above stay the only baseline by working conversations.

## Capability Matrix

### Design And Planning

Written by Phase 1. Its observed evidence comes from the transcripts, read on 2026-10-01
before they go, and from the user's session review of 2026-09-27 (`local-review/`, cited
as **review 09-27**), which followed a whole 6.4.1 chain in this repository.

#### Observed `brainstorming` Calls

One row per distinct call, 13 in all: 10 in the baseline period, 3 since.

| Date | Project | Version | Path announced | Outcome | Next |
|---|---|---|---|---|---|
| 2026-09-08 | pdf-creator | 6.3.0 | bounded, stepped up when the scope grew | outline approved in chat, kept "as the spec" | implementation |
| 2026-09-10 | pdf-creator | 6.3.0 | architectural | spec in `docs/superpowers/specs/`, written through Bash | `writing-plans`, then `subagent-driven-development` |
| 2026-09-10 | forma-rust | 6.3.0 | architectural | a roadmap, `revue-croisee` | — |
| 2026-09-10 | my-skills, copied into five transcripts of my-claude | 6.3.0 | architectural | design by sections | `writing-plans` |
| 2026-09-12 | pdf-creator | 6.3.0 | architectural | the document a roadmap phase named, `docs/architecture.md` | the phase went on |
| 2026-09-13 | my-claude | 6.3.0 | — | spec in the scratchpad, outside the repository | `writing-plans` |
| 2026-09-17 | my-claude-setup | 6.3.0 | architectural | spec in `.superpowers/specs/`, after the user's correction | `writing-plans` |
| 2026-09-17 | scriptorium | 6.3.0 | — | design in chat | `test-driven-development` |
| 2026-09-17 | my-claude-setup | 6.3.0 | — | spec in `.superpowers/specs/` | `writing-plans` |
| 2026-09-17 | scriptorium | 6.3.0 | architectural | a roadmap, `session-review` | — |
| 2026-09-25 | scriptorium | 6.4.1 | architectural | a roadmap, `library-catalogue` | — |
| 2026-09-26 | my-claude-setup | 6.4.1 | architectural | spec in `.superpowers/specs/` | `writing-plans`, then `executing-plans` |
| 2026-09-27 | my-claude-setup | 6.4.1 | — | a roadmap, `skill-tooling`, at the user's proposal | `roadmap` |

Five designs ended in a roadmap, six in `writing-plans`, two in direct implementation; the
visual companion was never offered.

#### brainstorming

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| BR1 | Description: "You MUST use this before any creative work", then what it explores (`:3`) | improve | `shaping-work` | Reasoned: emphatic wording and a "when" covering any creative work fall under the Description and Tone rules of 2026-09-28; evals then tune the trigger. |
| BR2 | Shared understanding: find the intent, write it back with what was said apart from what is assumed, carry it into the design (`:14-36`, new in 6.4.1) | keep | `shaping-work` | Observed once, 6.4.1 being the only version with it: on 2026-09-27 the agent wrote back what it had understood, and the user confirmed it and added the goal that shaped the skill-tooling roadmap — skills made anywhere, in the repository's format. |
| BR3 | Hard gate: no implementation before the path's approvals, each approval covering only the stage presented (`:38-56`) | keep | `shaping-work` | Observed held in every call read: the bounded ESP32 guide waited for "très bien" (2026-09-08), the architectural designs for one "oui" per section. This setup's design tasks already end on the user's approval. |
| BR4 | Three paths — spike, bounded, architectural — announced, the heavier one in doubt, raised mid-task and never lowered (`:58-88`) | keep | `shaping-work` | Observed: announced in 9 of the 13 calls, raised once when the scope grew ("Je monte donc d'un cran", 2026-09-08). It sizes the ceremony to the task; the roadmap skill knows one size. |
| BR5 | "Too simple to need approval" and the red flags table (`:90-108`) | drop | — | Reasoned: a rationalization table answers an observed discipline failure only (Tone, 2026-09-28), and no call read skipped the gate. |
| BR6 | A checklist per path, one todo per item (`:110-138`) | improve | `shaping-work` | Reasoned: the steps stay, written once; the todo per item goes, being Claude Code's vocabulary (`using-superpowers/references/claude-code-tools.md:3-4`). |
| BR7 | Process flow as a `dot` graph (`:140-182`) | drop | — | Row W15 of 2026-09-28: a list carries the same decision for less. |
| BR8 | After an architectural design, `writing-plans` and nothing else (`:184-189`, `:263-266`) | improve | `shaping-work` | Observed: 5 of the 13 designs ended in a roadmap instead, one at the user's proposal (2026-09-27, "Je te propose qu'on rédige une roadmap pour tout noter"). The hand-over follows where this setup puts plans, task 4 of Phase 1. |
| BR9 | Understanding the idea: the project first, a scope check that splits a request into sub-projects, one question per message, multiple choice preferred (`:199-207`) | improve | `shaping-work` | Observed: every call explored before asking, the user answers lettered options with one letter, and one question at a time surfaced two corrections before any code (review 09-27, § 2). Add: read every file the user points to before describing it — review 09-27 found `note.md` cited through a whole design unread (finding 6). |
| BR10 | Two or three approaches with their trade-offs, the recommended one first; YAGNI (`:209-214`) | keep | `shaping-work` | Observed in 2026-09-13, 2026-09-17 and 2026-09-26; in the last, the user chose another approach than the one recommended, which the comparison made possible. |
| BR11 | The design in sections scaled to their complexity, approved one by one, covering architecture, components, data flow, errors, testing (`:216-222`) | keep | `shaping-work` | Observed in every architectural call ("je te demande de valider chacune", then "oui" three times, 2026-09-17); review 09-27 credits it with two requirements absent from the request. |
| BR12 | Design for isolation: units with one purpose and clear interfaces (`:224-229`) | keep | `shaping-work` | Reasoned: what `writing-plans`' File Structure and Interfaces blocks then make mechanical (review 09-27, § 2). |
| BR13 | In an existing codebase: follow its patterns, improve what the work touches, no unrelated refactoring (`:231-235`) | keep | `shaping-work` | Reasoned: scopes the design to the request. |
| BR14 | The spec in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, committed, unless the user prefers otherwise (`:135`, `:239-244`) | improve | roadmap phase file, `## Design` | Observed: the default held in 1 of the 13 calls (2026-09-10); otherwise the spec went to `.superpowers/specs/` after the user's correction, to the scratchpad outside the repository, or to the document a roadmap phase named, or a roadmap replaced it. Where specs live is task 4's, and `.superpowers/` goes (decision at opening). |
| BR15 | `elements-of-style:writing-clearly-and-concisely` if available (`:243`) | drop | — | Reasoned: a skill of another plugin, installed nowhere in this setup on 2026-10-01. |
| BR16 | Spec self-review: placeholders, consistency, scope, ambiguity, fixed inline (`:246-254`) | keep | `shaping-work` | Observed: it caught a factual error on `epub.css` (2026-09-12) and a stale-state entry (review 09-27). It replaced a reviewer subagent in 5.0.6, at "3-5 real bugs per run in ~30s instead of ~25 min" (`RELEASE-NOTES.md:388`). |
| BR17 | The user reviews the written spec before any plan (`:256-261`) | keep | `shaping-work` | Observed ("tu peux y aller", 2026-09-13; "non tu peux rédiger", 2026-09-12). |
| BR18 | Visual companion: offered just in time in a message of its own, then browser or terminal decided per question (`:268-285`, `visual-companion.md`) | drop | — | Observed: never offered nor launched in 13 calls, the EPUB covers and colours of 2026-09-10 included. Its guide is ~3,350 tokens, its launch written per harness (`visual-companion.md:60-93`). Reasoned: a harness with its own display, such as Claude Code's artifacts, shows a mockup without a server. |
| BR19 | The companion's scripts: a Node server with session keys, start and stop scripts, helper, frame template, screens under `.superpowers/brainstorm/` (`scripts/`) | drop | — | Goes with BR18: 723 lines of server and 12 test files (`tests/brainstorm-server/`) for a feature never used here. |
| BR20 | `spec-document-reviewer-prompt.md` | drop | — | Cited by no file since 5.0.6, which BR16 replaced (`RELEASE-NOTES.md:381-388`). |

**Cost.** `SKILL.md` is ~4,400 tokens in 6.4.1, ~3,900 in 6.3.0, loaded when the work
starts and kept to the end: review 09-27 measured ~802,000 tokens carried over 185 calls,
the most of any skill. Task 4 weighs it when it places the kept rows.

#### Observed `writing-plans` And `executing-plans` Calls

| Date | Project | Version | Skill | What it did | Next |
|---|---|---|---|---|---|
| 2026-09-04 | forma-rust, copied into two transcripts | 6.3.0 | `executing-plans` | ran a roadmap's phases, each closed with the user's former `close-phase` skill | the next phase |
| 2026-09-10 | pdf-creator | 6.3.0 | `writing-plans` | plan in `docs/superpowers/plans/`, through Bash heredocs; self-review fixed 6 inconsistencies | `subagent-driven-development` |
| 2026-09-11 | my-claude, copied into five transcripts | 6.3.0 | `writing-plans` | plan in `docs/superpowers/plans/`, 8 tasks; self-review fixed 3 defects; method asked with options | `subagent-driven-development` |
| 2026-09-13 | my-claude | 6.3.0 | `writing-plans` | plan in the scratchpad, outside the repository, 7 tasks | `executing-plans`, as the agent recommended |
| 2026-09-13 | my-claude | 6.3.0 | `executing-plans` | the 7 tasks | `finishing-a-development-branch` |
| 2026-09-17 | my-claude-setup | 6.3.0 | `writing-plans`, twice | plans in `.superpowers/plans/`; the user chose "1", subagent-driven, both times | `subagent-driven-development` |
| 2026-09-27 | my-claude-setup | 6.4.1 | `writing-plans` | plan in `.superpowers/plans/`, complete code in one 164,030-character Write; a dry-run, on the agent's initiative, found 3 defects | `executing-plans` |
| 2026-09-27 | my-claude-setup | 6.4.1 | `executing-plans` | 13 tasks in 15 minutes; resumed from the ledger after the spend limit, nothing redone | `finishing-a-development-branch` |

The roadmap skill already carries part of a plan: a phase file has an objective, an
overview, one line per task, files, dependencies, constraints and acceptance criteria;
its report keeps a work log, decisions, files changed, problems and changes to later
phases, and survives the session. It has no per-task detail — files, interfaces, steps,
expected outputs — no review focus, and no step that executes the tasks.

#### writing-plans

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| WP1 | Description: a spec or requirements for a multi-step task, before touching code (`:3`) | improve | roadmap skill description | Reasoned: the Description rule of 2026-09-28 — what the skill does, then when. |
| WP2 | The plan written for an engineer with zero context and "questionable taste": everything to know, DRY, YAGNI, TDD, frequent commits (`:8-12`) | improve | roadmap phase file | Keep "a task carries everything its executor needs", which made the briefs work (review 09-27, § 2); drop the persona, which narrates rather than says what to do (Tone, 2026-09-28). |
| WP3 | Announce the skill at start (`:14`) | drop | — | Reasoned: the harness already shows a skill's load, and the announcement adds a line to every run. |
| WP4 | A worktree, if any, made at execution time by `using-git-worktrees` (`:16`) | open | git convention | Phase 3 rules on worktrees, in the convention the future git skill reads (the user, 2026-10-02). |
| WP5 | Plans in `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`, unless the user prefers otherwise (`:18-19`) | improve | roadmap phase file | Observed: the default held in 2 of the 6 calls; `.superpowers/plans/` took 3 and the scratchpad 1. Where plans live is task 4's. |
| WP6 | Scope check: one plan per independent subsystem, each yielding working, testable software (`:21-23`) | keep | roadmap create | Reasoned: in this setup, one roadmap per effort and one phase per deliverable. |
| WP7 | File structure before tasks: one responsibility per file, split by responsibility, existing patterns followed (`:25-34`) | keep | roadmap phase file, `## Design` | Observed: with the Interfaces blocks, it made the pre-flight check between tasks mechanical (review 09-27, § 2). |
| WP8 | Task right-sizing: the smallest unit with its own test cycle and worth a reviewer's gate; setup and documentation folded into the task that needs them (`:36-43`) | keep | roadmap create and open-phase | Reasoned: the unit Phase 2's proof per task and Phase 3's commit per task both need. |
| WP9 | Steps of 2 to 5 minutes: failing test, run, minimal code, run, commit (`:45-52`) | open | open | The proof a task declares is Phase 2's — the method question of `study/methods.md`, as the user recalled on 2026-10-02 — and its commit granularity Phase 3's. |
| WP10 | The plan's header: goal, architecture, stack, spec, executor, global constraints copied verbatim (`:54-77`) | improve | roadmap phase file | Observed: the constraints were copied into every task (review 09-27, § 2). A phase file already holds the objective, the overview and the constraints; the executor line goes with task 5. |
| WP11 | Review Focus: five input classes the spec implies and no test exercises, each then pinned by a test in its task (`:79-89`, `:163`) | improve | roadmap phase file | Observed: the final reviewer checked each one and found one test too narrow, which led to the Important fix (review 09-27, § 2). Written only when the need is really felt (the user, 2026-10-02). |
| WP12 | Task structure: files with line ranges, interfaces consumed and produced, checkbox steps with complete code, commands and their expected output, a commit step (`:94-141`) | improve | roadmap phase file | Observed both ways: complete code made execution a transcription, 13 tasks in 15 minutes, but wrote the implementation twice — planning produced 47 % of the session's output (review 09-27, § 2). Reasoned: complete code pays when another agent or a cheaper model executes; for the same agent inline, the step names files, interfaces, tests and expected outputs. |
| WP13 | No placeholders: no "TBD", no "similar to Task N", no step without its content (`:143-151`) | keep | roadmap create and open-phase | Reasoned: what lets an executor work from a task alone, by brief. |
| WP14 | Self-review against the spec: coverage, placeholders, type consistency, review focus, fixed inline (`:153-165`) | improve | roadmap open-phase | Observed: it fixed 6 and 3 defects (2026-09-10, 2026-09-11). Add, when the plan carries complete code: run it in a scratch copy before the hand-over — on 2026-09-27 that found 3 defects the self-review missed (review 09-27, finding 3). |
| WP15 | Hand-over: the user reviews the plan and chooses subagent-driven or native, with the agent's recommendation (`:167-192`) | keep | roadmap execute operation | Observed: four plans went to subagent-driven execution and two inline; the user chose or approved the method in five of the six. The model behind the choice is task 5's. |
| WP16 | `plan-document-reviewer-prompt.md` | drop | — | Cited by no file since 5.0.6, which WP14 replaced (`RELEASE-NOTES.md:381-388`). |

**Cost.** ~2,300 tokens in 6.4.1, ~1,800 in 6.3.0; ~299,000 carried in review 09-27,
where planning also produced 251,844 output tokens.

#### executing-plans

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| EP1 | Description: execute a plan in this session as its implementer, when inline was chosen or no subagent tool exists (`:3`) | improve | roadmap skill description | Reasoned: the Description rule of 2026-09-28. |
| EP2 | Why inline: one context and one final reviewer; the brief stands for the spec, the ledger for memory, TDD for the per-task gate (`:8-22`) | improve | roadmap execute operation | Reasoned: one clause of reason, not a paragraph (Tone, 2026-09-28); the trade-off itself belongs to task 5's decision. |
| EP3 | Narration: at most one short line between tool calls (`:24-25`) | keep | roadmap execute operation | Reasoned: every printed line is re-read on every later call (`:166-168`). |
| EP4 | Continuous execution: no check-in between tasks (`:27-30`) | keep | roadmap execute operation | Observed: 13 tasks in 15 minutes without a pause (review 09-27); on 2026-09-04 a roadmap's phases ran one after another. Within one phase only: closing a phase and opening the next ends the turn, no phase chained to the next (the user, 2026-10-02), unlike the forma-rust run of 2026-09-04. |
| EP5 | Rulings, not stalls: decide with the spec as authority, ledgered as "what — why — cost if wrong" (`:32-37`) | keep | roadmap report | Observed: seven rulings reached the user with their cost (review 09-27, § 2). The report's Decisions hold the decision and its reason; the cost if wrong is new. |
| EP6 | Four stops: an irreversible act, a security-sensitive one, a side effect outside the worktree such as a merge or a push, a plan broken past guessing (`:39-43`) | keep | roadmap execute operation | Reasoned: the bounds that make continuous execution safe. |
| EP7 | When to use, and when to prefer subagents: a gate on every task, or a plan long enough to outlast the context (`:45-64`) | improve | roadmap execute operation | Decided with the user on 2026-10-01: inline by default, a task delegated only at the user's request (Decisions Of Phase 1, item 3). |
| EP8 | Process flow as a `dot` graph (`:66-106`) | drop | — | Row W15 of 2026-09-28. |
| EP9 | Setup: an isolated workspace through `using-git-worktrees`, never `main` or `master` without consent (`:108-113`) | improve | roadmap execute operation | Observed: loaded by cascade for a `git switch -c` (review 09-27, finding 4). Load it only when the plan names no branch; branching is Phase 3's. Branching follows the repository's `[git]` convention in `.agent-conventions.toml` — everything on `main`, or branches — rather than a rule of the skill (the user, 2026-10-02). |
| EP10 | A ledger in a workspace per plan under `.superpowers/sdd/`, shared with `subagent-driven-development`; after a compaction, trust the ledger and `git log` (`:115-141`) | improve | roadmap report | Observed: after the spend limit, the work resumed from the ledger with nothing redone (review 09-27, § 2). The roadmap's report and ticked tasks already outlive the session; one record replaces two, and `.superpowers/` goes (decision at opening). |
| EP11 | Read the plan once, and the spec it names as the binding authority; with no spec, rulings stay provisional (`:143-147`) | keep | roadmap execute operation | Reasoned: the authority order that makes rulings decidable. |
| EP12 | Load `test-driven-development` before Task 1 (`:149-152`) | improve | roadmap execute operation | Observed: low marginal value where the plan already orders RED then GREEN (review 09-27, finding 4). Load it only when the steps are not already test-first; Phase 2 rules on the skill. |
| EP13 | Pre-flight scan: one ledger row per task that consumes what an earlier one produces (`:154-162`) | keep | roadmap execute operation | Observed: made mechanical by the Interfaces blocks (review 09-27, § 2). |
| EP14 | Context economy: long output to a file, the brief rather than the plan, bookkeeping in the same call as the work (`:164-181`) | keep | roadmap execute operation | Observed: briefs read with their code folded, and a script copied the code, so no code crossed the context twice (review 09-27, § 2). |
| EP15 | `scripts/task-start`: the task's brief and BASE in one call (`:170-177`) | drop | — | Inline, the agent reads the task in its phase file, so no brief needs extracting; the BASE of a task serves only a review or a delegation, and `review-package` takes the range directly (the user, 2026-10-02: settle the ledger scripts). |
| EP16 | Work the steps in order: compare each `Expected:` line; code wrong goes to `systematic-debugging`, plan wrong to a ruling (`:183-205`) | keep | roadmap execute operation | Reasoned: the comparison is what turns a step into evidence. |
| EP17 | Completion contract: every named test ran, the final run passed, every expected output compared, every deviation ruled, under `verification-before-completion` (`:207-220`) | improve | roadmap execute operation | Observed: `verification-before-completion` was never loaded, `task-done` enforcing what it asks (review 09-27, § 2). The contract stays, in the step; how a task declares its proof is Phase 2's. |
| EP18 | `scripts/task-done`: runs the task's tests, keeps the output, records the completion only when they pass (`:222-232`) | improve | roadmap execute operation | Observed: the record the resumption relied on (review 09-27, § 2). Kept as a rule: a task is ticked only once its declared proof ran and passed, the command and its result in the report's Work Log. Whether a script runs it waits for Phase 2's proof format (the user, 2026-10-02: settle the ledger scripts). |
| EP19 | Final whole-branch review: a review package, `code-reviewer.md` on the most capable model with the Review Focus and the rulings; a recorded self-review without a subagent tool (`:234-258`) | improve | reviewer agent | Observed: it found the only Important bug and a permission rule broader than needed (review 09-27, § 2). Add: check the model that actually ran, in the reviewer's transcript — `fable` was asked, the author's model ran (finding 5). Conditional: run when the phase changes code or scripts; the tool reviews then weigh its value against its tokens (the user, 2026-10-02). |
| EP20 | Findings re-graded by effect; Critical and Important in one fix pass, each fix test-first with the whole suite; Minor deferred; "Declined to judge" ruled; no re-review (`:260-289`) | keep | roadmap execute operation | Observed: both review fixes went test-first, and seven declined items became rulings (review 09-27, § 2). |
| EP21 | Finish: "Rulings I made" and "Deferred minors" in the final message, then the workspace deleted and `finishing-a-development-branch` (`:291-304`) | improve | roadmap report | Reasoned: the final message is the only place the rulings survive (Hand-Overs); the report keeps them past the conversation. |
| EP22 | Rationalizations table (`:306-321`) | drop | — | Reasoned: no observed failure it answers (Tone, 2026-09-28). |
| EP23 | Example workflow (`:323-373`) | improve | roadmap execute operation | Reasoned: an input and output example is a kept writing pattern (row S11 of 2026-09-28); 50 lines of one are not. |

**Cost.** ~5,100 tokens in 6.4.1, ~600 in 6.3.0; ~439,000 carried in review 09-27, plus
~342,000 for the two skills it loads by cascade.

#### Observed `subagent-driven-development` Runs

Four distinct runs, all on 6.3.0; every dispatch went to a `general-purpose` subagent.

| Date | Project | Plan | Dispatches | Models asked | Subagent tokens: fresh, cache read |
|---|---|---|---|---|---|
| 2026-09-10 | pdf-creator | EPUB output, 15 tasks | 15 implementations, 20 reviews, 8 re-reviews, 3 final | sonnet 39, haiku 6, opus 1 | 8.1 M, 125.8 M |
| 2026-09-11 | my-claude | roadmap skills rework | 6 implementations, 10 reviews, 3 re-reviews, 3 final, 12 eval runs | sonnet 19, opus 3 | partly copied away; 0.5 M, 11.7 M in its own folder |
| 2026-09-17 | my-claude-setup | the installer, then the roadmap hooks and agent: two runs in one session | 11 implementations, 11 reviews, 7 re-reviews, 4 final | haiku 10, sonnet 21, opus 2 | 4.5 M, 66.5 M for both |

The models asked are the models that ran, by the subagent transcripts. Re-reviews, one per
fix round, came to about one for every two tasks; the rounds the descriptions name went to
round 2 at most. No subagent called the Skill tool. For scale,
the inline run of 2026-09-27 executed 13 tasks on 146,559 fresh tokens, its reviewer on
117,576 (review 09-27, § 1).

#### subagent-driven-development

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| SD1 | Description: execute a plan with independent tasks in this session (`:3`) | improve | roadmap skill description | Reasoned: the Description rule of 2026-09-28. |
| SD2 | A fresh subagent per task, a task review of spec and quality after each, a broad final review; no subagent inherits the session's context (`:8-12`) | improve | roadmap execute operation | Decided with the user on 2026-10-01: per-task subagents and reviews only at the user's request (Decisions Of Phase 1, item 3). Observed: per-task reviews led to about one fix round for every two tasks, at 4.5 to 8.1 M fresh tokens of subagents per session, where the inline run's single final review found one Important bug for 117,576. A phase that needs subagents says so explicitly in the roadmap (the user, 2026-10-02). |
| SD3 | Narration, continuous execution, rulings, the four stops (`:14-31`) | keep | roadmap execute operation | As EP3 to EP6. |
| SD4 | When to use, as a `dot` graph, and the comparison with inline (`:33-57`) | drop | — | Row W15 of 2026-09-28 for the graph; the comparison goes to task 5's decision. |
| SD5 | Process flow as a `dot` graph (`:59-122`) | drop | — | Row W15 of 2026-09-28. |
| SD6 | Setup: worktree, a ledger per plan, recovery from the ledger and `git log` (`:124-154`) | improve | roadmap report | As EP9 and EP10. |
| SD7 | The plan read once, the spec as binding authority (`:156-160`) | keep | roadmap execute operation | As EP11. |
| SD8 | Pre-flight table: one row per pair of tasks sharing a file or an interface, one per task checking itself, rulings before Task 1 (`:162-182`) | keep | roadmap execute operation | As EP13, with the self-consistency rows added. |
| SD9 | Model selection: the least capable model fit for each role, the most capable for design and the final review, the model always named; turns cost more than token price (`:184-219`) | improve | implementer agent, reviewer agent | Observed: the tiers asked are the tiers that ran in the four runs; in review 09-27, `fable` was asked and the author's model ran (finding 5). Add: read the model that ran in the subagent's transcript. Tiers, not model names, keep it agent-neutral. |
| SD10 | Batch small same-shape edits into one dispatch (`:223-229`) | keep | roadmap execute operation | Reasoned: one dispatch per one-line edit pays a fresh context each time. |
| SD11 | Artifacts handed over as files; a dispatch describes one task, never the session's history (`:231-233`, `:267-271`) | keep | roadmap execute operation | Observed by the plugin: "a real session's dispatch hit 42k chars of which 99% was pasted history" (`:269-270`); briefs as files worked inline too (review 09-27, § 2). |
| SD12 | Waiting on subagents: bounded stretches, then a status line and a check of the live ones (`:235-244`) | drop | — | Reasoned: Claude Code notifies the agent when a background subagent finishes, which makes the rule moot where this setup runs. |
| SD13 | Dispatching the implementer: BASE recorded, the brief extracted by script, a five-part dispatch, a report file named after the brief, no subagents of its own, never two implementers at once (`:246-284`) | improve | roadmap execute operation, implementer agent | Reasoned: keep the dispatch; enforce "no subagents" by the worker's tool list rather than by prose, as `roadmap-auditor` does (`domains/roadmap/agents/roadmap-auditor.md:4`). A report named `task-N-report.md` passes the Write refusal of report-named files in subagents, which only catches names starting with REPORT, SUMMARY, FINDINGS or ANALYSIS (`CLAUDE.md`, Gotchas). |
| SD14 | Four statuses — DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED — and what the controller does with each (`:286-306`) | keep | implementer agent | Reasoned: a closed set the controller can act on without reading the report. |
| SD15 | Implementer prompt: questions first, exactly the task, test-driven "if task says to", commit, a self-review checklist, an escalation that carries no penalty, a full report in a file and a short reply (`implementer-prompt.md`) | improve | implementer agent | Reasoned: the proof follows what the task declares, Phase 2's question, rather than "if task says to" (`implementer-prompt.md:36`); the rest stays. Observed: no implementer loaded a skill in four runs, so a worker without the Skill tool loses nothing, as eval run agents already work (`CLAUDE.md`, Gotchas). |
| SD16 | Task review: spec and quality both required, the diff in a file, the brief, report and verbatim constraints as inputs, no open-ended directive, no re-run of the implementer's tests, no pre-judged finding; "cannot verify" items settled by the controller (`:308-352`) | keep | reviewer agent | Observed: the reviews led to about one fix round for every two tasks. Whether reviews come per task or once is task 5's. |
| SD17 | Task reviewer prompt: the report is a claim to verify; a focused test only on a specific doubt; spec compliance as missing, extra, misunderstood; quality; Important means "cannot be trusted until fixed"; a plan-mandated defect reported as Important (`task-reviewer-prompt.md`) | keep | reviewer agent | Reasoned: the calibration keeps a plan from grading itself (`task-reviewer-prompt.md:145-157`). It overlaps `code-reviewer.md`, which Phase 2 rules on. |
| SD18 | The fix loop: Minor deferred, plan conflicts ruled, rounds 1 to 3 resume the implementer, 4 and 5 a fresh one on a stronger model, a scoped re-review each round, a breaker at 5 that parks or rules (`:354-429`) | improve | roadmap execute operation | Lightened (the user, 2026-10-02): one fix round, then back to the user; the five rounds, the model escalation and the breaker go. Flexibility and lightness, conditions rather than forced ceremony. |
| SD19 | Re-review prompt: each finding ADDRESSED or NOT ADDRESSED, new breakage in the fix diff only (`re-review-prompt.md`) | keep | reviewer agent | Observed: 18 re-reviews across the runs, each scoped to a fix round. |
| SD20 | A task completes only with its review clean or every open finding parked with a ruling (`:431-443`) | keep | roadmap execute operation | Reasoned: no task moves on over an open Critical or Important finding. |
| SD21 | Final review on the most capable model with `code-reviewer.md`, the deferred and parked lines; one fix dispatch, one scoped re-review, residuals adjudicated (`:445-469`) | improve | reviewer agent | As EP19 and EP20; the plugin observed a final fix wave "cost more than all its tasks combined" with one fixer per finding (`:460-461`), hence one dispatch. Conditional, as EP19. |
| SD22 | Finish: the exhaustive rulings list, the workspace deleted, `finishing-a-development-branch` (`:471-487`) | improve | roadmap report | As EP21. |
| SD23 | Rationalizations table (`:489-501`) | drop | — | As EP22. |
| SD24 | Example workflow (`:503-568`) | improve | roadmap execute operation | As EP23. |
| SD25 | Scripts: `sdd-workspace`, a workspace per plan under `.superpowers/sdd/`; `task-brief`, a task's text to a file; `review-package`, log, stat and diff of a range in a file (`scripts/`) | improve | roadmap execute operation | `sdd-workspace` goes with `.superpowers/` (decision at opening); `task-brief` goes too, a rare delegation writing its brief itself; `review-package` stays, the diff of a range in one file for the reviewer (the user, 2026-10-02). |
| SD26 | Under Claude Code, one orchestrator subagent on a mid-tier model runs the whole plan, with nested subagents (`using-superpowers/references/claude-code-tools.md:9-29`) | drop | — | Decided with the user on 2026-10-01: a delegated worker gets no Agent tool (Decisions Of Phase 1, item 3), so no orchestrator subagent dispatches others; never observed. Confirmed (the user, 2026-10-02): no subagent multiplied without need, and a phase that needs subagents says so in the roadmap. |

**Cost.** ~8,100 tokens in both versions, the largest `SKILL.md` but `writing-skills`.

#### dispatching-parallel-agents

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| DP1 | The skill: one agent per independent problem domain, working at once, when two or more tasks share no state (`:1-14`) | drop | — | Observed: never invoked, in the baseline or since, and review 09-27 found no job for it. Independent agents were dispatched without it — the twelve eval runs of 2026-09-11, the old skill against the new. Reasoned: Claude Code's own Agent tool already describes parallel, background dispatch to the agent. Confirmed (the user, 2026-10-02): speed is not a reason; several subagents answer a real need only. |
| DP2 | When to use it, and when not: related failures, a need for the whole system, shared state (`:16-45`, `:129-134`) | improve | roadmap execute operation | Kept as the condition of any parallel dispatch, written where task 5 puts delegation; the `dot` graph goes (row W15). |
| DP3 | The pattern: group by domain; give each agent a scope, a goal, constraints and an expected output; then check for conflicts and run the whole suite (`:47-85`) | improve | roadmap execute operation | Reasoned: the integration step — conflicts checked, whole suite run — is the part a parallel dispatch cannot skip; the rest is SD11 and SD13. |
| DP4 | Agent prompt structure and common mistakes: focused, self-contained, specific about its output (`:87-127`) | improve | roadmap execute operation | Folded into SD11 and SD13, which say the same for one implementer. |
| DP5 | A real example and a verification section (`:136-167`) | drop | — | Reasoned: a narrative rather than a technique (row W25 of 2026-09-28). |

**Cost.** ~1,500 tokens, paid only by its description in the listing, since it never
loaded.

#### Decisions Of Phase 1

Taken with the user on 2026-10-01; the "Goes to" column above follows them.

1. **Design work goes to a skill of its own,** built in this setup's skill architecture,
   from the kept rows of `brainstorming`. Its exit follows the path: a recommendation for
   a spike; for bounded work, a design approved in the chat, then the implementation; for
   architectural work, a roadmap, or the `## Design` of the phase under way. The user
   added that any kept capability may become a new skill, agent or hook, and that any of
   them may be reworded: the aim is this setup's own architecture and workflow. Its name
   comes from shaping, as in Shape Up, rather than design, which UI design skills
   already use: `shaping-work`, on the model of `authoring-skills`; its trigger must not overlap the roadmap skill or the skills to come,
   which trigger evals check (the user, 2026-10-02).
2. **Specs and plans.** A roadmap's design lives in its README. A phase's design lives in
   a `## Design` section of its phase file, approved when the phase starts; it cites a
   decision record when the section is not enough — the two complement each other, as the
   user put it. The plan is the phase's tasks, with detail per task — files, interfaces,
   expected outputs — when the phase calls for it, and complete code only for a delegated
   task (row WP12). Lasting decisions go to `docs/decisions/`; bounded work stays in the
   chat, with no file. `.superpowers/` goes. A Review Focus section is written in the phase
   file only when the need is really felt (the user, 2026-10-02; row WP11). The words
   "spec" and "plan" leave this setup's tools: a design says what is built and why,
   the tasks say how and in what order, and a roadmap holds both for long work (the user, 2026-10-02).
3. **Execution.** The roadmap skill gains an operation that executes a phase in the main
   conversation, task by task in order, with no pause but the four stops (row EP6).
   Rulings go to the report's Decisions with their cost if wrong; the report, the ticked
   tasks and `git log` replace the ledger. Before the closure, a reviewer agent with
   read-only tools reviews the phase's diff, its model chosen by tier and checked after
   the run. A task is delegated only at the user's request, to a named agent whose tool
   list holds neither the Skill nor the Agent tool. The user's reason: tasks are meant to
   run in chronological order, so delegation by default does not fit. Completed on
   2026-10-02 with the user: the operation runs one phase — closing a phase and opening
   the next ends the turn, and the work never chains into the next phase; commits come
   at the end of each task or at the closure, as the `.agent-conventions.toml` git
   convention says (Phase 3). The reviewer agent runs only when the phase changes code
   or scripts. A phase that needs subagents says so in the roadmap, and delegation
   stays light: one implementer, one reviewer, one fix round, then back to the user.

The design skill is named `shaping-work` (the user, 2026-10-02); the operation and the two
agents are named in Phase 4.

### Proof

Written by Phase 2.

### Git

Written by Phase 3.

### Plugin

Written by Phase 4.

## When To Revisit

Written by Phase 4.
