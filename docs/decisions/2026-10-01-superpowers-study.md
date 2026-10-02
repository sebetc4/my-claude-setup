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
- Fetched on 2026-10-02: the Claude Code page on worktrees, "Run parallel sessions with
  worktrees" (https://code.claude.com/docs/en/worktrees, cited as **worktrees §**
  section).

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
| WP4 | A worktree, if any, made at execution time by `using-git-worktrees` (`:16`) | drop | — | Phase 3 rules on worktrees, in the convention the future git skill reads (the user, 2026-10-02). Settled by Phase 3: no worktree at execution time; parallel sessions get theirs from the harness, with `branch = "roadmap"` (Decisions Of Phase 3, item 5). |
| WP5 | Plans in `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`, unless the user prefers otherwise (`:18-19`) | improve | roadmap phase file | Observed: the default held in 2 of the 6 calls; `.superpowers/plans/` took 3 and the scratchpad 1. Where plans live is task 4's. |
| WP6 | Scope check: one plan per independent subsystem, each yielding working, testable software (`:21-23`) | keep | roadmap create | Reasoned: in this setup, one roadmap per effort and one phase per deliverable. |
| WP7 | File structure before tasks: one responsibility per file, split by responsibility, existing patterns followed (`:25-34`) | keep | roadmap phase file, `## Design` | Observed: with the Interfaces blocks, it made the pre-flight check between tasks mechanical (review 09-27, § 2). |
| WP8 | Task right-sizing: the smallest unit with its own test cycle and worth a reviewer's gate; setup and documentation folded into the task that needs them (`:36-43`) | keep | roadmap create and open-phase | Reasoned: the unit Phase 2's proof per task and Phase 3's commit per task both need. |
| WP9 | Steps of 2 to 5 minutes: failing test, run, minimal code, run, commit (`:45-52`) | improve | proof reference | The proof a task declares is Phase 2's — the method question of `study/methods.md`, as the user recalled on 2026-10-02 — and its commit granularity Phase 3's. Settled by Phase 2: a task declares its proof, and the `test` proof keeps the failing test, its run, the code and the suite (Decisions Of Phase 2, items 1 and 5). |
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
| EP9 | Setup: an isolated workspace through `using-git-worktrees`, never `main` or `master` without consent (`:108-113`) | improve | roadmap execute operation | Observed: loaded by cascade for a `git switch -c` (review 09-27, finding 4). Load it only when the plan names no branch; branching is Phase 3's. Branching follows the repository's `[git]` convention in `.agent-conventions.toml` — everything on `main`, or branches — rather than a rule of the skill (the user, 2026-10-02). Settled by Phase 3: the `[git]` table's `branch`, `none` in both repositories, and its `commit`, `task` (Decisions Of Phase 3, items 1 and 2). |
| EP10 | A ledger in a workspace per plan under `.superpowers/sdd/`, shared with `subagent-driven-development`; after a compaction, trust the ledger and `git log` (`:115-141`) | improve | roadmap report | Observed: after the spend limit, the work resumed from the ledger with nothing redone (review 09-27, § 2). The roadmap's report and ticked tasks already outlive the session; one record replaces two, and `.superpowers/` goes (decision at opening). |
| EP11 | Read the plan once, and the spec it names as the binding authority; with no spec, rulings stay provisional (`:143-147`) | keep | roadmap execute operation | Reasoned: the authority order that makes rulings decidable. |
| EP12 | Load `test-driven-development` before Task 1 (`:149-152`) | improve | roadmap execute operation | Observed: low marginal value where the plan already orders RED then GREEN (review 09-27, finding 4). Load it only when the steps are not already test-first; Phase 2 rules on the skill. Settled by Phase 2: no skill to load; a task that declares `test` runs the `test` proof (Decisions Of Phase 2). |
| EP13 | Pre-flight scan: one ledger row per task that consumes what an earlier one produces (`:154-162`) | keep | roadmap execute operation | Observed: made mechanical by the Interfaces blocks (review 09-27, § 2). |
| EP14 | Context economy: long output to a file, the brief rather than the plan, bookkeeping in the same call as the work (`:164-181`) | keep | roadmap execute operation | Observed: briefs read with their code folded, and a script copied the code, so no code crossed the context twice (review 09-27, § 2). |
| EP15 | `scripts/task-start`: the task's brief and BASE in one call (`:170-177`) | drop | — | Inline, the agent reads the task in its phase file, so no brief needs extracting; the BASE of a task serves only a review or a delegation, and `review-package` takes the range directly (the user, 2026-10-02: settle the ledger scripts). |
| EP16 | Work the steps in order: compare each `Expected:` line; code wrong goes to `systematic-debugging`, plan wrong to a ruling (`:183-205`) | keep | roadmap execute operation | Reasoned: the comparison is what turns a step into evidence. |
| EP17 | Completion contract: every named test ran, the final run passed, every expected output compared, every deviation ruled, under `verification-before-completion` (`:207-220`) | improve | roadmap execute operation | Observed: `verification-before-completion` was never loaded, `task-done` enforcing what it asks (review 09-27, § 2). The contract stays, in the step; how a task declares its proof is Phase 2's. Settled: the `Proof:` line under each task (Decisions Of Phase 2, item 2). |
| EP18 | `scripts/task-done`: runs the task's tests, keeps the output, records the completion only when they pass (`:222-232`) | improve | roadmap execute operation | Observed: the record the resumption relied on (review 09-27, § 2). Kept as a rule: a task is ticked only once its declared proof ran and passed, the command and its result in the report's Work Log. Whether a script runs it waits for Phase 2's proof format (the user, 2026-10-02: settle the ledger scripts). Settled: no script, the Work Log recording each run (Decisions Of Phase 2, item 3). |
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

Written by Phase 2. Its observed evidence comes from the transcripts, read on 2026-10-02
before they go, from review 09-27, and from the tool reviews of `roadmap-auditor`
(`reviews/`, `make reviews` on 2026-10-02). Where the plugin's maintainers report a
measure in `RELEASE-NOTES.md`, the row says "measured by the plugin": their evals, not
this repository's.

#### Observed Calls

Four distinct calls in all, every one in a working conversation: none of
`verification-before-completion`, `requesting-code-review` or `receiving-code-review`,
in the baseline or since. No call read a companion file.

| Date | Project | Version | Skill | How it came | What followed |
|---|---|---|---|---|---|
| 2026-09-13 | pdf-creator | 6.3.0 | `test-driven-development` | the agent's own call, in a roadmap phase whose tasks did not order test first | a stub turned an ImportError into 18 failing tests before the code; green; two mutations made with `sed`, each caught by a test; committed |
| 2026-09-17 | scriptorium | 6.3.0 | `test-driven-development` | the agent's own call, once the user approved a design given in chat | an empty `checks()` left 7 of 11 tests failing; a new test that passed at once was rewritten until it reproduced the real case; false positives then counted on the library's real PDFs |
| 2026-09-17 | polarsteps-tts | 6.3.0 | `systematic-debugging` | the agent's own call on the user's report of a timeout | a crashed server, then a suspend, set aside on evidence; the cause measured on the real server; a failing test, the fix, 383 tests, the real run resumed |
| 2026-09-27 | my-claude-setup | 6.4.1 | `test-driven-development` | required by `executing-plans` | RED then GREEN in Tasks 1 to 10, 12 and both review fixes, as the plan already ordered (review 09-27, § 2) |

In the 2026-09-17 polarsteps-tts session, the first bug, an API answering 404, was fixed
without any skill, and its test was written after the fix, never watched failing; the
second, under `systematic-debugging`, had its failing test watched before the fix. One case
each way.

#### Observed Final Reviews

`code-reviewer.md` as the final reviewer of both executors, by the subagent transcripts
whose prompt opens with its persona. Two more runs were cut by a spend or session limit
(2026-09-12 pdf-creator, 2026-09-27); the subagent transcripts of the 2026-09-11 run are
partly gone.

| Date | Project | Version | Model that ran | Verdict | Findings |
|---|---|---|---|---|---|
| 2026-09-12 | pdf-creator | 6.3.0 | `claude-sonnet-5` | fix before merge | 3 Important integration gaps; read statically, no suite run |
| 2026-09-17 | my-claude-setup | 6.3.0 | `claude-opus-5` | with fixes | 3 to fix: a malformed `hooks.json` written into `settings.json`, a crash after the copy, unchecked domain names |
| 2026-09-17 | my-claude-setup | 6.3.0 | `claude-opus-5` | with fixes | 3 Important: a missing test, a regex silencing `session_resume.py`, a latent failure in `checks.py` |
| 2026-09-27 | my-claude-setup | 6.4.1 | `claude-opus-5-5`, `fable` asked | with one fix | 1 Important, a crash on an unreadable review; a permission rule to narrow; 7 declined to judge |

Every review that ran to its end found something to fix before the merge, three of them
after every task had passed its own task review in `subagent-driven-development`.

#### test-driven-development

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| TD1 | Description: "Use when implementing any feature or bugfix, before writing implementation code" (`:3`) | drop | — | The practice becomes the `test` proof, which a task's declaration brings in, so no description triggers it (Decisions Of Phase 2, items 1 and 5). Phase 4 confirms it with the recount, as the 2026-09-28 record planned for a general TDD skill. |
| TD2 | Core principle: a test not watched failing is not known to test the right thing (`:10-12`) | keep | proof reference | Observed in all three calls; see TD8. |
| TD3 | "Violating the letter of the rules is violating the spirit of the rules" (`:14`) | drop | — | Tone, 2026-09-28: a persuasion form, kept only after an observed discipline failure; none in the calls read. |
| TD4 | When to use: always for features, fixes, refactoring and behavior changes; throwaway prototypes, generated code and configuration as exceptions the user grants (`:16-29`) | improve | proof reference | Reasoned: each exception is a case where another proof fits — a probe for a prototype, an existing check for configuration — so the choice becomes the proof a task declares, which the user reads in the phase file. Task 4 measures it. |
| TD5 | Iron Law: no production code without a failing test first; code written before it is deleted, never kept as reference nor looked at (`:31-45`) | improve | proof reference | Keep the order, the failing test before the code it proves. Drop the deletion: for an agent, the code it wrote stays in its context whether the file is deleted or not, so "don't look at it" cannot hold (reasoned); row W2 of 2026-09-28 found the same absolute law too strict for skills; no code written before its test was observed in the calls read. |
| TD6 | Red-green-refactor as a `dot` graph (`:47-69`) | drop | — | Row W15 of 2026-09-28. |
| TD7 | RED: one minimal test of one behavior, a clear name, real code, with a good and a bad TypeScript example (`:71-111`) | improve | proof reference | Keep the three requirements; one short example (row W16 of 2026-09-28). |
| TD8 | Verify RED: run it; it fails rather than errors, for the expected reason, the feature missing and not a typo; a test that passes tests existing behavior, so fix the test (`:113-128`) | keep | proof reference | Observed, the most applied rule: on 2026-09-13 a stub turned an ImportError into failures; on 2026-09-17 an empty skeleton showed 7 failures, and a test that passed at once was rewritten until it failed (`:126`). Review 09-27 credits the skill with this rule alone, every RED failing for the expected reason. |
| TD9 | GREEN: the simplest code that passes, nothing beyond the test (`:130-166`) | keep | proof reference | Reasoned: YAGNI at the step, as BR10 and WP2. |
| TD10 | Verify GREEN: the test passes, the project's whole suite passes, the output is clean; a red test seen and not reported falsifies the report (`:168-193`, the suite paragraph new in 6.4.1) | improve | proof reference | Measured by the plugin: with one test file named, sessions ran only that file in 11 of 12 probe runs (`RELEASE-NOTES.md:34-36`). Observed: the 2026-09-13 call and the 2026-09-17 debugging call ended on the whole suite, 144 and 383 tests. Change: the repository's `checks` in `.agent-conventions.toml` name the suite, where the skill guesses `pytest`, `npm test` or `cargo test` (`:187-188`, Conventions Imposed). |
| TD11 | REFACTOR: after green only, duplication and names, no new behavior (`:195-206`) | keep | proof reference | Reasoned: the step that keeps minimal code from piling up; no call read shows it as a step of its own. |
| TD12 | Good tests table — minimal, clear, showing intent — and the pointer to `writing-good-tests.md` (`:208-220`) | improve | proof reference | The table restates TD7. Observed: the pointer was followed in none of the four calls. Where the file's rules go is TD20 to TD25. |
| TD13 | Common rationalizations: too simple, tests after, already tested by hand, sunk cost, exploration, slowness (`:222-236`) | drop | — | Measured by the plugin: deleting these rebuttals cut test-first under "just write it, tests after" pressure from 8/10 to 5/10, on Claude and on Codex (`RELEASE-NOTES.md:115`). Measured here (Proof Per Task): under the user's haste, a declared `test` held test-first 12 times out of 12 on two models, and three rows of this table added nothing. The plugin's stronger pressure, an explicit "tests after", is an instruction of the user, which this setup follows. |
| TD14 | Red flags: stop and start over (`:238-254`) | drop | — | Restates TD13 row for row, and TD8 for "passes immediately" and "can't explain why it failed". |
| TD15 | Example: a bug fix through the cycle (`:256-291`) | improve | proof reference | Row S11 of 2026-09-28 keeps an input and output example; one short one, as EP23. |
| TD16 | Verification checklist before marking work complete; "can't check all boxes? start over" (`:293-306`) | improve | roadmap execute operation | Restates TD7 to TD10. What stays is what the execution operation records before ticking a task (EP18): the failing run, the passing run, the suite. |
| TD17 | When stuck: no idea how to test, test too complicated, mocks everywhere, huge setup (`:308-315`) | drop | — | Reasoned: content the model already knows, which skill-tooling's `skill-auditor` is to flag (its Phase 3). |
| TD18 | Debugging integration: a bug gets a failing test that reproduces it, never a fix without a test (`:317-321`) | keep | proof reference, debugging skill | Observed: in the 2026-09-17 polarsteps-tts session, the bug fixed without guidance was tested after its fix; the one fixed under `systematic-debugging`, which says the same (`systematic-debugging:172-177`), was tested first. One rule in one place, with SY7. |
| TD19 | Final rule, and exceptions only with the user's permission (`:323-330`) | drop | — | Restates TD4 and TD5. |
| TD20 | `writing-good-tests.md`, name the break: the production change that would fail the test, a bug and not a decision; expectations derived by hand, as literals; no change detectors (`writing-good-tests.md:20-45`, `:65-79`) | keep | proof reference, reviewer agent | Reasoned: it catches the tests that pass whatever the code does, a mirror assertion or a constant checked against itself, which a RED run can miss when the test is written after the code. |
| TD21 | Behavior, not text: a script or a config is tested by running it, a document for agents by its consumer's behavior, prose for people by nothing (`writing-good-tests.md:47-52`) | keep | proof reference, reviewer agent | The Testing rule of 2026-09-28 says the same: unit tests for scripts, evals for skills. Its pointer to `superpowers:writing-skills` goes to `authoring-skills`. |
| TD22 | Your code, not the framework; constructors, getters and constants earn a test only when they validate, derive or cause side effects (`writing-good-tests.md:54-63`, `:150-155`) | keep | proof reference, reviewer agent | Reasoned: it bounds the number of tests; a test written to satisfy process costs maintenance. |
| TD23 | Exercise the real thing: no assertion on a mock, mocks at the slow or external level after learning their side effects, specific doubles, complete mock data, test-only methods in test utilities, real components over complex mocks (`writing-good-tests.md:81-148`) | improve | reviewer agent | Observed: the 2026-09-13 and 2026-09-17 suites ran against a real local HTTP and HTTPS server and real PDFs made by WeasyPrint, without the file being read. Its rules then serve best as a reviewer's criteria, as `code-reviewer.md:84` already asks, rather than as reading for the author. |
| TD24 | Mutation check: mutate the code mentally; one test fails for each realistic mutation (`writing-good-tests.md:157-169`) | improve | proof reference | Observed: on 2026-09-13 the agent mutated the code for real, with `sed`, and each mutation failed a test. Change: run the mutation rather than imagine it, as the proof of a test written after its code, where no RED was watched; VC7 says the same for a regression test. |
| TD25 | Quick reference and warning signs (`writing-good-tests.md:171-198`) | drop | — | Restate TD20 to TD24. |

**Cost.** `SKILL.md` ~2,400 tokens in 6.4.1, `writing-good-tests.md` ~2,070, never read in
the calls; ~198,000 carried in review 09-27, loaded by cascade.

#### verification-before-completion

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| VC1 | Description: before claiming work complete, fixed or passing, before a commit or a pull request (`:3`) | drop | — | Its rule is EP18's, applied by the execution operation to every declared proof (Decisions Of Phase 2, item 3), so no description triggers it. Observed: never invoked, its practice carried by `executing-plans` and `task-done` (review 09-27, § 2). |
| VC2 | Iron Law: no completion claim without fresh evidence, run in this message (`:8-20`) | keep | roadmap execute operation | It is EP18's rule: a task ticked only once its declared proof ran and passed. Where it lives for work outside a roadmap is task 5's. Capitals and "violating the letter" go (Tone). |
| VC3 | Gate function: name the command that proves the claim, run it whole, read the output and the exit code, compare, then claim (`:22-36`) | keep | roadmap execute operation | Reasoned: the five steps are what "proof ran and passed" means, and what the Work Log records. "Skip any step = lying" goes (Tone). |
| VC4 | Common failures: each claim with the evidence it requires and what is not enough — tests, linter, build, a fixed bug, a regression test, an agent's report, requirements (`:38-48`) | keep | proof reference | Reasoned: the closest thing in the plugin to a list of proof kinds, the subject of task 5. "Requirements met: a line-by-line checklist, not passing tests" is the acceptance criteria check of `close-phase`. |
| VC5 | Red flags: "should", "probably", satisfaction before verification, trusting an agent's report, tiredness (`:50-59`) | drop | — | Tone, 2026-09-28: a discipline form, kept only after an observed failure; review 09-27 and the calls read record no completion claimed without its run. |
| VC6 | Rationalization prevention (`:61-72`) | drop | — | As VC5. |
| VC7 | Key patterns: tests, a regression test proven by reverting the fix and watching it fail, build, requirements re-read, a delegated agent's report checked against the diff (`:74-104`) | improve | proof reference, roadmap execute operation | Keep the two patterns no other row holds: revert the fix, watch the test fail, restore (`:82-86`), the RED of a test written after its fix, with TD24; and a delegated agent's report checked against the diff (`:100-104`), with EP19's check of the model that ran. The rest restates VC4. |
| VC8 | When to apply: before any claim, satisfaction, commit, pull request, next task or delegation, paraphrases included (`:106-120`) | improve | roadmap execute operation | Reasoned: in this setup the moments are a task's tick, a phase's closure and a commit; "any expression of satisfaction" goes (Tone). |

**Cost.** ~900 tokens, paid only by its description in the listing, since it never
loaded.

#### systematic-debugging

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| SY1 | Description: any bug, test failure or unexpected behavior, before proposing fixes (`:3`) | improve | debugging skill | Reasoned: the Description rule of 2026-09-28. Observed: one call, the agent's own, on 2026-09-17; the first bug of the same session was fixed without it. |
| SY2 | Iron Law: no fix without root-cause investigation first (`:8-20`) | keep | debugging skill | Observed on 2026-09-17: a crashed server, then a suspend of the laptop, were set aside on evidence — the last audio chunk was written before the suspend — and the cause was measured before any change. "Violating the letter" goes (Tone). |
| SY3 | When to use, especially under time pressure, never skipped for a simple issue (`:22-42`) | improve | debugging skill | The situations go to the description; "especially" and "don't skip" are persuasion with no observed failure behind them (Tone). |
| SY4 | Root cause: read the errors whole, reproduce, check recent changes, instrument each component boundary of a multi-component system, trace the data flow (`:44-118`) | keep | debugging skill | Observed on 2026-09-17: the read timeout told apart from a refused connection, the system journal and the cache timestamps read, the failing chunk replayed against the real server, 95.7 s against a 60 s timeout. The code-signing example shortens (row W16). |
| SY5 | Pattern analysis: find working examples, read a reference whole, list every difference, the dependencies (`:120-141`) | keep | debugging skill | Observed: the failing step set against the 34 that passed — chunks under ~950 characters against one of 2,812 — gave the cause. |
| SY6 | Hypothesis: one, stated; the smallest change, one variable; a new hypothesis when it fails; "I don't understand X" said (`:143-166`) | keep | debugging skill | Observed: "Root-cause hypothesis is concrete now. Let me verify empirically", then one decisive measure. Reasoned: one variable keeps fixes from stacking. |
| SY7 | Implementation: a failing test first through `test-driven-development`, one fix, verify through `verification-before-completion`; after three failed fixes, question the architecture with the user (`:168-212`) | improve | debugging skill | Keep the failing test (TD18), the single fix and the verification (VC3), the two hand-overs becoming one practice. The three-fixes stop joins the execution operation's stops (EP6): a fourth fix waits for the user. Reasoned: no call read reached a second fix. |
| SY8 | Red flags, and the user's signals that the agent is guessing: "Stop guessing", "Ultra-think this", "We're stuck?" (`:214-242`) | drop | — | Tone, 2026-09-28: no observed failure. The signals carried a harness tie: one held the keyword Claude Code scans for and switched every session that loaded the skill into extended thinking, until a hyphen broke it (`RELEASE-NOTES.md:263`). |
| SY9 | Common rationalizations (`:244-255`) | drop | — | Tone, 2026-09-28. `CREATION-LOG.md:57-75` reports its pressure tests passed with the skill, with no run without it, so they measure compliance, not what the skill changes (row W1 of 2026-09-28). |
| SY10 | Quick reference (`:257-264`) | drop | — | Restates SY4 to SY7. |
| SY11 | No root cause: the investigation documented, handling added — retry, timeout, message — and logging; "95% of 'no root cause' cases are incomplete investigation" (`:266-275`) | improve | debugging skill | Keep the steps; the 95 % has no source (reasoned). Observed on 2026-09-17: the suspend, environmental, was reported apart from the cause and handled with `systemd-inhibit`. |
| SY12 | `root-cause-tracing.md`: trace back up the call chain to the original trigger, a stack trace logged before the risky operation, the polluting test found (`root-cause-tracing.md`) | improve | debugging skill | Keep the technique in a few lines; its two `dot` graphs go (row W15), its 2025-10-03 narrative shortens (row W25). Never read in the call. |
| SY13 | `defense-in-depth.md`: after a fix, validation at every layer — entry, business logic, environment guard, debug logging (`defense-in-depth.md`) | improve | debugging skill | Observed on 2026-09-17: the fix scaled the timeout and left the chunker alone, telling the user why — a change would invalidate the audio cache mid-trip. A second guard is proposed to the user, not imposed at every layer. |
| SY14 | `condition-based-waiting.md` and `condition-based-waiting-example.ts`: a test waits for a condition rather than a fixed delay | drop | — | Reasoned: content the model knows, and the example is 158 lines of another project's TypeScript (row W25). Claude Code itself refuses a `sleep` followed by commands and points to its Monitor tool (observed on 2026-09-17). |
| SY15 | `find-polluter.sh`: runs test files one by one until one leaves a file behind | drop | — | Hard-wired to `npm test` (`find-polluter.sh:51`), never run here; upstream it matched no file at all until 6.4.1 (`RELEASE-NOTES.md:129`). Reasoned: a loop the agent writes in one line when needed. |
| SY16 | `CREATION-LOG.md`, `test-academic.md`, `test-pressure-1.md` to `-3.md`, cited nowhere | drop | — | Not instructions: a history that speaks of "Claude" and of `~/.claude/CLAUDE.md` (Ties To Claude Code), and scenarios that illustrate row W23's method. |

**Cost.** `SKILL.md` ~2,400 tokens; companions ~4,900 more, the script included, never read.

#### requesting-code-review

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| RQ1 | Description: when completing tasks, implementing major features, or before merging (`:3`) | improve | reviewer agent | Reasoned: the agent's description says when the execution operation calls it. Observed: the skill was never invoked; its template served every final review through the executors (Observed Final Reviews). |
| RQ2 | A reviewer subagent given crafted context, never the session's history (`:8`) | keep | reviewer agent | As SD11. |
| RQ3 | When: after each task of `subagent-driven-development`, after a major feature, before a merge; optionally when stuck, before a refactoring, after a complex bug (`:12-22`) | improve | roadmap execute operation | Decided with the user: once before the closure, when the phase changes code or scripts (Decisions Of Phase 1, item 3). Observed: every final review that ran to its end found something to fix, three of them after every task had passed its own review. |
| RQ4 | The range: BASE from `HEAD~1` or `git merge-base origin/main HEAD`, HEAD (`:26-30`) | improve | reviewer agent | The phase report's Start Commit is the base, recorded at opening, so nothing is guessed; `review-package` puts the range in one file (SD25). |
| RQ5 | Placeholders: what was built, the plan or requirements, the two commits (`:32-40`, `code-reviewer.md:154-158`) | improve | reviewer agent | In this setup: the phase file — objective, design, tasks, acceptance criteria — the report's Decisions, which hold the rulings (EP5), and the range. |
| RQ6 | Act on feedback: Critical now, Important before going on, Minor noted, pushback with reasons (`:42-46`) | keep | roadmap execute operation | As EP20 and SD18: one fix pass, Minor deferred, then the user. |
| RQ7 | Example: a review after Task 2 (`:48-73`) | drop | — | Built on a per-task review this setup no longer runs, and on `docs/superpowers/plans/`. |
| RQ8 | Rationalizations: reviewing the diff inline spends the coordinator's context; the reviewer needs no history (`:75-80`) | improve | roadmap execute operation | Keep the first as one clause of reason for a separate reviewer (Tone rule 2): observed, the 2026-09-27 reviewer found what the author's own dry-run had not (review 09-27, § 4). The second restates RQ2. |
| RQ9 | Red flags: never skip a review because it seems simple, never go on over an Important issue (`:82-95`) | drop | — | "Never skip" contradicts the conditional review decided with the user (Decisions Of Phase 1, item 3); the rest restates RQ6. |
| RQ10 | `code-reviewer.md`: a general-purpose subagent, the "Senior Code Reviewer" persona and purpose (`code-reviewer.md:1-13`) | improve | reviewer agent | A named agent with its own description replaces the template; the persona goes, as WP2's did (Tone). |
| RQ11 | The git range read with `git diff --stat` and `git diff` (`code-reviewer.md:23-31`) | improve | reviewer agent | As RQ4: one file from `review-package`. |
| RQ12 | The design as a vision: a reasonable user's expectation is a requirement, and a finding is graded by its effect on that user (`code-reviewer.md:33-41`, new in 6.4.1) | keep | reviewer agent | Measured by the plugin: every implementer in its evals shipped the same crash on an input the spec implied and never named (`RELEASE-NOTES.md:23`, `:31`). Observed: the 2026-09-27 Important finding was such an input, a hand-edited or non-UTF-8 review file. "Spec" becomes the phase's design (Decisions Of Phase 1, item 2). |
| RQ13 | Declined to judge: every behavior set aside listed with its reason, each ruled by the executor (`code-reviewer.md:43-48`, new in 6.4.1) | keep | reviewer agent | Observed: seven items on 2026-09-27, each ruled, each ruling reaching the user with its cost if wrong (review 09-27, § 2). The rulings go to the report's Decisions (EP5). |
| RQ14 | Read-only on the checkout: history through `git show` and `git diff`, another revision in a temporary worktree (`code-reviewer.md:50-52`) | improve | reviewer agent | Keep the checkout untouched, while commands stay allowed: the 2026-09-27 reviewer fuzzed the YAML subset and ran enable and disable on a copy of `settings.json`, the work that found its bug (review 09-27, § 4). Say it as a principle: `roadmap-auditor`'s list of allowed commands kept being stepped outside (`make reviews`, 2026-10-02, two findings). |
| RQ15 | No subagents of its own (`code-reviewer.md:54-61`) | improve | reviewer agent | Enforced by the agent's tool list, without the Agent tool, rather than by prose (Decisions Of Phase 1, item 3; SD13). |
| RQ16 | What to check: alignment with the plan, code quality, architecture, testing, production readiness (`code-reviewer.md:63-93`) | improve | reviewer agent | Keep alignment, edge cases and testing, with TD20 to TD23 as the testing criteria. Add: each task's declared proof ran and proves what it claims (EP18). The generic items — scalability, migrations, documentation — are content the model knows (reasoned). |
| RQ17 | Calibration: severity by actual effect, praise first, deviations and plan issues flagged (`code-reviewer.md:95-104`) | improve | reviewer agent | Keep severity by effect and plan issues flagged, as SD17. Praise goes: its reader is the executing agent, which re-grades every finding by effect (EP20); the 2026-09-12 review gave its strengths three long paragraphs. |
| RQ18 | Output: strengths; Critical, Important and Minor issues with file and line, what, why and how; recommendations; "Ready to merge?" (`code-reviewer.md:106-135`) | improve | reviewer agent | Keep the issues with their location, reason and fix. The verdict comes first, as `roadmap-auditor` answers (`domains/roadmap/agents/roadmap-auditor.md`, Answer), so the caller reads it without parsing prose; "ready to merge" becomes ready to close the phase, merging being Phase 3's. Settled by Phase 3: a merge happens only at a roadmap's closure under `branch = "roadmap"` (The `[git]` Table). |
| RQ19 | Critical rules, do and don't (`code-reviewer.md:137-151`) | drop | — | Restates RQ17 and RQ18. |
| RQ20 | Example output (`code-reviewer.md:162-198`) | improve | reviewer agent | Row S11 of 2026-09-28: one output example, shorter. |

**Cost.** `SKILL.md` ~750 tokens, never loaded; `code-reviewer.md` ~1,600, read by the
executors at each final review. A final review cost 117,576 fresh tokens on 2026-09-27;
`roadmap-auditor`, a read-only agent with a fixed checklist, a median of 77,910 over four
runs, each answering PASS (`make reviews`, 2026-10-02).

#### receiving-code-review

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| RC1 | The skill and its description: when receiving review feedback, before implementing it (`:3`) | drop | — | Observed: never invoked, in the baseline or since; its moment is a step of the execution operation (EP20), and review 09-27 found the two overlapping (finding 7). The rows below that serve go to that step. |
| RC2 | The response pattern: read, restate, verify against the codebase, evaluate, respond, implement one item at a time with a test each (`:14-25`) | improve | roadmap execute operation | Keep "verify each finding against the code before fixing it": a finding is a claim, as an implementer's report is to its reviewer (SD17). The order and the tests are EP20's. |
| RC3 | Forbidden responses: "You're absolutely right!", "Great point!", any thanks (`:27-38`, `:131-148`) | drop | — | Reasoned: the findings come from an agent, ruled in the report, not from a person; the rule cites its author's instruction file (`:30`). |
| RC4 | Unclear feedback: stop and ask about every unclear item before implementing any (`:40-57`) | keep | roadmap execute operation | Reasoned: items may be related, and the fix pass is a single one (EP20). |
| RC5 | By source: the user trusted once understood; an external reviewer checked — correct for this codebase, breaking nothing, aware of the reason for the current code, of the platforms, of the context; a conflict with the user's decisions taken to the user (`:59-86`) | improve | roadmap execute operation | Keep the checks for the reviewer agent's findings, and "a finding that contradicts a decision recorded in the design or the report goes to the user". |
| RC6 | YAGNI check: grep for real usage before "implementing properly" (`:88-98`) | keep | roadmap execute operation | Reasoned: a reviewer may ask for features; usage decides, as BR10 and TD9. |
| RC7 | Implementation order: clarify, then blocking, simple, complex; each fix tested; no regression (`:100-111`) | improve | roadmap execute operation | Folded into EP20's single pass, each Critical and Important fix test-first with the whole suite. |
| RC8 | When and how to push back, and correcting a wrong pushback (`:113-129`, `:150-162`) | improve | roadmap execute operation | A declined finding becomes a ruling in the report with its reason and cost if wrong (EP5): pushback, recorded. The social guidance goes. |
| RC9 | Common mistakes and real examples (`:164-201`) | drop | — | Restate RC2 to RC8 (row W25). |
| RC10 | GitHub thread replies through `gh api …/replies` (`:203-205`) | drop | — | Phase 3 rules on forges and pull requests. Settled by Phase 3: dropped with FB8, no pull request being made in the transcripts; the git domain adds both when a repository integrates through pull requests (Decisions Of Phase 3, item 4). |

**Cost.** ~1,550 tokens, paid only by its description in the listing, since it never
loaded.

#### Proof Per Task

**The hypothesis.** Rather than a method chosen from a catalogue, each task declares
before it starts the proof that will say it is done: `test`, a failing test first;
`eval`, a run without the change, then with it; `probe`, the real platform tried before
the work relies on it; `check`, an existing check passes; `review`, the user decides. The
method then follows from the kind of artifact. The two executors held no common standard:
`executing-plans` requires `test-driven-development` (`executing-plans:149`), the
implementer applies it "if task says to" (`implementer-prompt.md:36`).

**The measure,** run on 2026-10-02 by the method of row W22, as the flowcharts were on
2026-09-28: one headless session per sample, no tools, no settings, no skills, from an
empty directory; the system prompt a role line and one form of guidance; the agent
answers with the numbered actions it would take, and every answer was read and labelled.
Four forms: **none**; **plain**, "work test-first: write a failing test, watch it fail,
then write the code", this repository's own convention (`CLAUDE.md`, Conventions);
**catalogue**, the five kinds defined, the agent choosing one; **declared**, the same
definitions and the task's `Proof:` line. One scenario per kind, each a real case of
this setup, and the code task again under the user's haste ("I'm blocked on this and it's
a one-line fix, please be quick"), where a fifth form adds three rows of TD13's table. Six
samples per cell, on Claude Haiku 4.5 and Claude Sonnet 5.5: 288 sessions, $4.40. The
script, its prompts, the 288 answers and their labels are in `study/proof-micro-tests/`,
which `.gitignore` keeps out of the repository, like the plugin's copy.

| Scenario, declared proof | Model | None | Plain | Catalogue | Declared |
|---|---|---|---|---|---|
| Exit code of `progress.py` (test): a failing test run before the code | Haiku | 0/6 | 6/6 | 4/6 | 6/6 |
| | Sonnet | 5/6 | 6/6 | 6/6 | 6/6 |
| The same under the user's haste (test) | Haiku | 0/6, no test | 6/6 | — | 6/6, and 6/6 with the three rows |
| | Sonnet | 0/6, tests after | 6/6 | — | 6/6, and 6/6 with the three rows |
| The closure's silence on uncommitted work, a skill's text (eval) | Haiku | no proof 6 | a test of the wording 2, of unsaid kind 4 | the user's review 6 | before and after 6 |
| | Sonnet | no proof 6 | a `grep` of the wording 6 | before and after 6 | before and after 6 |
| `allowed-tools` taken on the documentation's word (probe) | Haiku | a run to see the prompt 3 | such a run 6, also before the change 3 | such a run after 6 | such a run after 6, also before 1; the field tried first 0 |
| | Sonnet | such a run after 6, also before 1 | a test of the front matter 6, no run at all 3 | the field tried first on a minimal skill with a control 6 | the same 6 |
| A `.gitignore` line (check) | Haiku | `git check-ignore` 1, re-read 1, nothing 4 | git 3, re-read 3 | git 3, re-read 3 | `make check` alone 6 |
| | Sonnet | git 6 | a new test file 6 | git 6 | git 4, `make check` alone 2 |
| Naming two agents (review) | Haiku | decides 2, asks leave to explore 4 | decides and tests the files 3, asks leave 3 | decides 2, asks leave 4 | hands over after writing the files 5, decides 1 |
| | Sonnet | decides 6 | decides and tests the files 6 | decides and evaluates the agents 6 | hands over after writing the files 6 |

What it shows:

1. **For code, a plain test-first instruction and a declared `test` do the same,** and
   both hold under haste, where Sonnet without guidance wrote its six tests after the
   fix. The three rows of TD13 added nothing to the declared proof.
2. **Elsewhere, the plain instruction does harm, the more on the stronger model.** Sonnet
   answered the skill, the platform, the configuration and the naming tasks with a new
   test every time, 24 out of 24: a `grep` of the skill's wording, a parse of the front
   matter, a permanent test for one `.gitignore` line, a check that the agent files
   exist. Three of the four are the string-presence trap that
   `writing-good-tests.md:47-52` names; the fourth tests configuration, an exception of
   `test-driven-development` itself (`:24-27`). Three of its six platform plans then never
   tried the platform, which all six did without guidance.
3. **A declared proof brought the method each artifact needs, with two exceptions.**
   `eval`, `test` and `review` held on both models (12/12, 24/24, 11/12). `probe` held on
   Sonnet only: Haiku tried the platform after the change, never the field first. `check`
   without its command drifted to the repository's suite, which proves nothing about a
   `.gitignore` line (Haiku 6/6, Sonnet 2/6).
4. **The catalogue is enough for the stronger model, except for a decision.** Sonnet chose
   the right proof itself on four scenarios out of five, and named the agents itself.
   Haiku, choosing, took the cheapest proof, the user's review, for the skill's text.
5. **`review` came after the work.** Defined as "the user reviews the result and decides",
   it was applied to files already written, where a name is best decided before them.

Limits: plans, not actions — what an agent says it will do; one scenario per kind, six
samples per cell; the haste milder than the plugin's "just write it, tests after", which
in this setup is the user's instruction to follow; the naming scenario, set in a Python
repository, read by Haiku as Python classes. The labels were fixed before reading, then
refined three times on the first answers: a platform run counts whatever the plan says of
how it runs, since plans rarely say; the configuration labels split git, re-reading and
the suite; the naming labels gained "asks leave to explore" and "hands over after
writing".

#### Decisions Of Phase 2

Taken with the user on 2026-10-02; the "Goes to" column above follows them.

1. **A task declares its proof, and the declaration names its object.** Five kinds:
   - `test: <the behavior>` — a failing test written first and watched failing for the
     expected reason, then the code, then the suite the contract's `checks` name; a test
     written after its code, for a regression or for code without tests, is proven by
     reverting or mutating the code and watching it fail;
   - `eval: <the scenario>` — the scenario given to a fresh agent without the change,
     then with it, compared on what was expected before the runs;
   - `probe: <the mechanism>` — the mechanism tried on a minimal case, with a control
     where one exists, before the work relies on it; its result decides the design;
   - `check: <the command>` — the named command passes after the change, and fails
     before it where it can;
   - `review: <the decision>` — the user decides on a proposal before the work that
     depends on it, and the decision is recorded with its date.

   The object is required because `check` without its command drifted to the suite;
   `probe` and `review` say "before" because both came late otherwise (Proof Per Task).
2. **An indented `Proof:` line under each task** of a phase file, inside its list item:

   ```
   - [ ] Add `.eval-runs/` to `.gitignore`
     Proof: check — `git check-ignore -v .eval-runs/x`
   ```

   The agent writing the phase proposes each proof, and the user approves them with the
   phase. Bounded work outside a roadmap states its proof in the design `shaping-work`
   gets approved in the chat.
3. **The execution operation runs the declared proof,** writes its command or scenario
   and its result in the report's Work Log, then ticks the task (row EP18). No
   `task-done` script: three kinds of five are not commands. The reviewer agent checks
   that each proof ran and proves what it claims (row RQ16).
4. **No key in `.agent-conventions.toml` for now:** a default kind carries no object, and
   a kind without its object is what drifted; the `test` proof's suite is the contract's
   `checks`, which exists. To revisit if declarations go wrong in use.
5. **No method chosen from a catalogue,** which answers the question of
   `study/methods.md` (row WP9). Test-driven development is the `test` proof;
   acceptance-test and behavior-driven development are a phase's acceptance criteria and
   the `evals.json` scenarios, run as `eval`; a spike is a `probe`; characterization
   tests for code without tests are `test` proofs proven by mutation; a refactoring keeps
   the suite green before and after. Domain-driven design, pair programming and design by
   contract weigh little at this scale (`phase-2-proof.md`, Overview).
6. **Debugging goes to a skill of its own,** from the kept rows of `systematic-debugging`:
   both bugs observed on 2026-09-17 were reported in the chat, outside any roadmap, where
   a reference of the execution operation would not reach. Phase 4 names it.
7. **This repository's `CLAUDE.md` line "TDD (failing test first)"**, the plain
   instruction that did harm outside code, is scoped by Phase 4.

The five kinds are defined once, in a **proof reference** read by the roadmap skill's
execution operation and by `shaping-work`; Phase 4 places it, `shared/` being how this
repository gives two skills one source.

### Git

Written by Phase 3. Its observed evidence comes from the transcripts, read on 2026-10-02
before the baseline period's go, from review 09-27, from the histories of this
repository and scriptorium, and from Claude Code's worktree page (worktrees §).

#### Observed Calls

Six distinct calls, every one in a working conversation and at the end of a plugin
executor's run; none of `using-git-worktrees` but one.

| Date | Project | Version | Skill | How it came | What followed |
|---|---|---|---|---|---|
| 2026-09-11 | my-claude, copied into three transcripts | 6.3.0 | `finishing-a-development-branch` | after `subagent-driven-development` | no suite, the plan's checks instead; a normal checkout, no remote; the work branch held the whole history, so the agent proposed renaming it `main`, and the user chose that through a question tool |
| 2026-09-12 | pdf-creator | 6.3.0 | `finishing-a-development-branch` | after `subagent-driven-development` | 124 tests; base `master` confirmed by `git merge-base`; the three options through a question tool; merge chosen; `master` moved with `git fetch . epub:master`, since a checkout would have refused or overwritten the user's uncommitted `.gitignore`; tests and both builds on the result; branch deleted |
| 2026-09-13 | my-claude, copied into two transcripts | 6.3.0 | `finishing-a-development-branch` | after `executing-plans` | the plan's checks; the menu in text, answered "1"; `git merge --ff-only`, `git pull` skipped without a remote; the checks again; branch deleted |
| 2026-09-17 | my-claude-setup | 6.3.0 | `finishing-a-development-branch` | after `subagent-driven-development` | `tests/check.py` and 39 tests; a report, no menu; the user: "on peut merger sur main"; `--ff-only`, the checks, branch deleted; nothing pushed: "je pousse sur ta demande" |
| 2026-09-27 | my-claude-setup, copied into two transcripts | 6.4.1 | `using-git-worktrees` | required by `executing-plans` | a normal checkout detected; the plan named a branch, so `git switch -c tool-review` without the consent question; `tests/check.py` as the baseline |
| 2026-09-27 | my-claude-setup | 6.4.1 | `finishing-a-development-branch` | after `executing-plans` | `make check`; base confirmed; the menu as written, in English in a French conversation; the user: "merge et push"; `git pull --ff-only`, `--ff-only`, `make check`; an annotated tag pushed unasked, following `CLAUDE.md` (review 09-27, finding 8) |

Every finish ended in the base moved forward, or the only branch renamed: no pull
request, no kept branch, no discard.

#### Observed Git Practice

Every git operation in the transcripts, counted once per `tool_use` id, and the histories
on 2026-10-02.

| Repository | Commits | Branches | Format | Granularity | Remote |
|---|---|---|---|---|---|
| my-claude-setup | 56 since 2026-09-17, linear, no merge commit | six, 2026-09-17 to 2026-09-27, each fast-forwarded into `main` and deleted the same day, two within three minutes; none since the roadmaps began on 2026-09-28 | `(type) description`, the rule in `CLAUDE.md`; a body, and a `Co-Authored-By` trailer in 54; feat 23, fix 14, docs 14, refactor 2, test 2 | one commit per task under the executors, 13 in ten minutes on 2026-09-27; one per phase closure under the roadmaps, 36 files for skill-tooling's Phase 1, its work and its closure together | GitHub, pushed at the user's request, `main` 10 commits ahead of `origin`; seven annotated `<domain>-vX.Y.Z` tags, the rule in `CLAUDE.md` |
| scriptorium | 71 since 2026-09-17, linear, no merge commit | none | `(type) Description`, capitalized, written nowhere; trailer in 68 | one commit per feature or per phase, a phase's work and its closure often in one ("Add the svg skill and make proof, closing phase 3", 30 files) | GitHub, 12 commits ahead of `origin`; no tag |
| forma-rust | no git: its contract says `versioning = "none"` | — | — | — | — |

In pdf-creator and my-claude, no longer on disk, the transcripts show the same:
branches only under the executors or right after them, fast-forwarded, and subjects in
French verb-first (pdf-creator) or Conventional Commits with a scope (my-claude) — the
format the user's former command prescribes (`study/git/commit-message.md`), before
`(type) description` from 2026-09-17. Worktrees: three `git worktree add`, each a
temporary checkout of a revision outside the tree — a build from the tree before a phase
(pdf-creator, 2026-09-13), a proof without `library/` (scriptorium, 2026-09-25), the
reviewer's instruction (2026-09-27) — never a workspace; no `EnterWorktree`, no
`gh pr create`, no review-thread reply.

#### using-git-worktrees

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| GW1 | Description: starting feature work that needs isolation, or before executing a plan (`:3`) | drop | — | Observed: one call in all, by cascade from `executing-plans`, for a `git switch -c` the plan had named, at ~144,000 tokens carried (review 09-27, finding 4). What it decides becomes the `[git]` table's branching, which the execution operation reads, so no description triggers it. |
| GW2 | Core principle, and the announcement at start (`:8-14`) | drop | — | The steps carry the principle; the announcement as WP3. |
| GW3 | Step 0: a linked worktree detected — `--git-dir` against `--git-common-dir`, the submodule guard — and its branch or detached HEAD reported (`:16-39`) | keep | git domain | Observed: run in the 2026-09-27 call and in all five finishes, a normal checkout each time. Reasoned: two commands keep a worktree from being nested in another, and tell a session the harness started in a worktree (worktrees § Start Claude in a worktree) that its branch already exists. |
| GW4 | Consent before a worktree unless the user declared a preference; in place on refusal (`:41-45`) | improve | `[git]` table | The declared preference becomes the table's branching value, so the repository answers and nothing is asked. Observed: the plan named a branch and the agent skipped the question (review 09-27, `using-git-worktrees`). The consent answered a plugin bug, executors creating worktrees unasked (`RELEASE-NOTES.md:293`). |
| GW5 | The harness's tools first — `EnterWorktree`, `/worktree`, `--worktree` —, `git worktree add` only without one (`:47-61`) | improve | git domain | Measured by the plugin: once the step names the tools, 50 runs of 50 chose the harness's tool (`tests/claude-code/test-worktree-native-preference.sh:14-19`). Claude Code then owns the place, the branch and the cleanup (worktrees § Start Claude in a worktree, § Clean up worktrees). Change: naming Claude Code's tools is a dependency that `docs/claude-code-coupling.md` records. Never observed: no `EnterWorktree` in the transcripts. |
| GW6 | The directory: a declared one, else an existing `.worktrees/` or `worktrees/`, else `.worktrees/` (`:63-76`) | drop | — | Claude Code puts its own under `.claude/worktrees/<name>/` on a branch `worktree-<name>` (worktrees § Start Claude in a worktree); the three temporary checkouts observed went outside the tree, to the session's scratchpad or a temporary directory, where git needs no ignore line. A directory setting would serve neither. |
| GW7 | A project-local directory ignored by git, else a `.gitignore` line added and committed (`:78-88`) | improve | git domain | Keep the check for a worktree inside the tree, which Claude Code's page also asks for `.claude/worktrees/` (worktrees § Start Claude in a worktree); the line is proposed to the user, not committed unasked in the middle of other work. |
| GW8 | `git worktree add "$path" -b "$BRANCH_NAME"`, then `cd`; on a sandbox refusal, tell the user and work in place (`:90-100`) | improve | git domain | The command is content the model knows (as TD17). Working in place undoes an isolation that exists because another session works in the same checkout (worktrees §, introduction): stop and report instead, as the execution operation's stops (EP6). |
| GW9 | Setup: dependencies installed per ecosystem, unasked — `npm install`, `cargo build`, `pip install -r requirements.txt`, `poetry install`, `go mod download` (`:102-119`) | improve | git domain | Observed on 2026-09-25: in a temporary worktree, scriptorium's code ran on the main checkout's `.venv` through `PYTHONPATH`, which no guessed command gives; a bare `pip install` outside a virtual environment writes into the user's Python. Change: the setup the repository documents, or a question; ignored files such as `.env` carried by the harness's own means (worktrees § Copy gitignored files into worktrees). |
| GW10 | A clean baseline: the tests run before the work, a failure reported and the user asked (`:121-140`) | improve | roadmap execute operation | Observed on 2026-09-27: `tests/check.py` ran before Task 1. Change: the contract's `checks`, not a guessed command (Conventions Imposed), before a phase's first task in any checkout, so that a later failure belongs to the phase. |
| GW11 | Quick reference (`:142-157`) | drop | — | Restates GW3 to GW10. |
| GW12 | Common rationalizations (`:159-167`) | drop | — | Tone, 2026-09-28: no observed failure; its rows restate GW3, GW5, GW6, GW7 and GW10. |
| GW13 | `tests/claude-code/test-worktree-native-preference.sh` and `test-worktree-path-policy.sh`: headless runs of the native-tool preference, and a check that the old global directory is gone | drop | — | They test the plugin's skill; this setup's evals test its own tools (Testing, 2026-09-28). The measure is cited in GW5. |

**Cost.** ~1,700 tokens, unchanged since 6.3.0; ~144,000 carried in review 09-27 for one
`git switch -c`.

#### finishing-a-development-branch

| # | Capability | Verdict | Goes to | Reason |
|---|---|---|---|---|
| FB1 | Description: implementation complete, tests passing, the work to integrate (`:3`) | drop | — | Observed: all five calls came at the end of an executor's run (`executing-plans:291-304`, `subagent-driven-development:471-487`). Integration happens where the `[git]` table puts a branch, at the roadmap's closure, so no description triggers it. |
| FB2 | Core principle, and the announcement at start (`:8-12`) | drop | — | As GW2. |
| FB3 | Step 1: the full suite on the tree to integrate, a stop on any failure (`:14-26`) | improve | roadmap close-roadmap | Observed in all five calls, each time with the repository's own commands rather than the skill's guesses: the plan's checks where no suite existed (2026-09-11, 2026-09-13), `pytest` from the project's `.venv` (2026-09-12), `tests/check.py` (2026-09-17), `make check` (2026-09-27). Change: the contract's `checks`, which `close-phase` and `close-roadmap` already run first. |
| FB4 | Step 2: a normal checkout, a worktree on a named branch, or a detached HEAD, each with its menu and cleanup (`:28-44`) | improve | git domain | Observed: run in all five calls, a normal checkout each time. Keep the detection where a worktree may exist (GW3); a detached HEAD, which some harnesses hand over (`RELEASE-NOTES.md:402-403`), is reported and its integration asked, without a menu of its own. |
| FB5 | Step 3: the base branch, confirmed before merging (`:46-51`) | improve | roadmap close-roadmap | Observed: confirmed with `git merge-base` in four calls; pdf-creator's base was `master`, where a guess of `main` fails (2026-09-12). Change: the roadmap's branch records its base when it is made, and the closure reads it. |
| FB6 | Step 4: exactly three options — merge locally, push and open a pull request, keep —, two on a detached HEAD; discard only on request; wait for the answer (`:53-82`) | improve | roadmap close-roadmap | Observed: the menu as written once, in English in a French conversation, and answered outside it — "merge et push" (2026-09-27); reworded through a question tool twice; replaced once by a better option, the rename (2026-09-11); never reached once, the user saying "on peut merger sur main" (2026-09-17). All five ended in the base moved forward. Change: the closure proposes the integration the `[git]` table declares, in the user's language, and the user confirms it or names another; the decision stays the user's (`:81-82`). |
| FB7 | Option 1: from the main root, the base checked out, `git pull`, the merge, the merged result tested, a stop on failure; then the worktree removed and the branch deleted (`:86-111`) | improve | git domain | Observed in four calls: a fast-forward every time — `--ff-only` three times, `git fetch . epub:master` once, which spared the user's uncommitted `.gitignore` (2026-09-12) —, `git pull` skipped without a remote (2026-09-13), the merged result tested and the branch deleted in all four. Change: `git pull --ff-only` and `git merge --ff-only`, a refusal going to the user, and the user's uncommitted files checked before any switch of branch. A plain `git pull` can create a merge commit, which neither history holds. |
| FB8 | Option 2: push, open the pull request with the forge's tool or the URL the push prints, keep the worktree for the feedback (`:113-126`) | drop | — | Observed: never chosen, and no pull request in the transcripts; both repositories push to GitHub in batches at the user's request, `main` 10 and 12 commits ahead of `origin` on 2026-10-02. The git domain adds it when a repository integrates through pull requests. |
| FB9 | Option 3: the branch and the worktree kept as they are (`:128-130`) | keep | roadmap close-roadmap | Never chosen; offered on 2026-09-12 "if you want to try `led.epub` on your reader first". Reasoned: the one answer that defers an integration, which a roadmap on its own branch may need. |
| FB10 | Discard only at the user's explicit request: the branch, its commits and the worktree listed, the word `discard` typed, the branch force-deleted (`:132-157`) | keep | git domain | Reasoned: the skill's one irreversible act. The plugin took it off the menu because it "advertised destroying finished, passing work" (`RELEASE-NOTES.md:116`). Never observed. |
| FB11 | Step 6: only worktrees under `.worktrees/` or `worktrees/` removed, then pruned; a refused removal shows the uncommitted files and asks — commit, move, delete —, never `--force` (`:159-201`) | improve | git domain | Claude Code removes the worktrees it makes, asking when work remains (worktrees § Clean up worktrees), and sweeps its subagents' (§ Clean up subagent and background-session worktrees): the agent removes only a worktree it made with git itself, such as a temporary checkout. Keep never `--force`: the plugin's own removal once destroyed untracked files (`RELEASE-NOTES.md:89`). |
| FB12 | Quick reference (`:203-210`) | drop | — | Restates FB6 to FB11. |
| FB13 | Common rationalizations (`:212-225`) | improve | git domain | Two rows hold rules no step states: a failing merged result stops everything (`:223`), and a rejected push is never force-pushed without the user's explicit request (`:225`), an outward and irreversible act (EP6). The rest goes (Tone, 2026-09-28). |

**Cost.** ~1,950 tokens, unchanged since 6.3.0; ~31,000 carried in review 09-27.

#### The `[git]` Table

Approved by the user on 2026-10-02. A table of `.agent-conventions.toml`, present when
the contract says `versioning = "git"` and absent otherwise, read through the shared
module `conventions.py` like `[roadmap]` and `[skills]`, by the roadmap skill and by the
git domain to come:

```toml
[git]
branch  = "none"
commit  = "task"
message = "(type) description"
```

- **`branch`** — where a roadmap's commits go.
  - `none`: on the default branch, in one checkout; nothing is made, nothing to merge.
    A phase's `## Design` lands on the default branch with the phase's first commit.
  - `roadmap`: a branch per roadmap, `roadmap/<folder-name>`, made from the default
    branch when the roadmap's first phase opens, its base recorded then, so that its
    designs land on it too (Notes For Later Phases, Phase 3). Every phase commits on it.
    `close-roadmap`, after its own commit, proposes the integration: the base
    fast-forwarded with `--ff-only` and the branch deleted (FB6, FB7), or the branch kept
    (FB9); a refused fast-forward goes to the user. For a long roadmap that should leave
    the default branch alone, for two roadmaps advanced at once — each in a session of
    its own, in a worktree the harness makes (worktrees § Start Claude in a worktree) —,
    or for a review before the merge.
- **`commit`** — when the work is committed.
  - `task`: one commit per task, once its declared proof passed and its run is in the
    report's Work Log (Decisions Of Phase 2, item 3), staging the files the task touched
    and never the whole tree; the opening of a phase is a commit of its own, and the
    closure commit holds the closure documents only.
  - `closure`: the phase's work and its closure in one commit, the opening riding with
    it.
- **`message`** — the subject's format, the only place it is written: the types in use
  and the trailers come from `git log` and the harness. Every commit step of the roadmap
  skill and of the git domain reads it.

Values on 2026-10-02: this repository `none`, `task`, `(type) description`; scriptorium
`none`, `task`, `(type) Description`; forma-rust has no table, its contract saying
`versioning = "none"`. A repository with `versioning = "git"` and no `[git]` table gets
values proposed from its history, written once the user agrees, as for the other tables.

Outside the table, each for its reason:

- **Push:** only at the user's request, a tag included — an outward act (EP6); both
  repositories push in batches. No key.
- **Pull requests and review-thread replies:** dropped for now (FB8, RC10); the git
  domain adds them, with a value of `branch`, when a repository integrates through pull
  requests.
- **Worktrees:** no key. Parallel sessions get theirs from the harness, which places,
  branches and removes them (GW5, FB11), and go with `branch = "roadmap"`; a temporary
  checkout of a revision goes outside the tree (GW6) and is removed by whoever made it.
- **Tags and releases:** the repository's instruction file, as this repository's
  `CLAUDE.md` holds its `<domain>-vX.Y.Z` rule; one repository releases, and a release is
  no step of a roadmap.
- **Trailers:** the harness adds its attribution; `docs/claude-code-coupling.md` records
  the dependency.

#### Decisions Of Phase 3

Taken with the user on 2026-10-02; the "Goes to" column above follows them.

1. **Commits per task** (`commit = "task"`) in this repository and scriptorium: a task's
   commit follows its recorded proof, and the closure commit holds the closure documents
   only. It answers skill-tooling's Phase 1, closed in one commit of 36 files with its
   work, and lets `git log` follow the Work Log.
2. **Branching takes two values,** `none` and `roadmap`, both repositories on `none`. The
   follow-up roadmap builds `roadmap` only when a repository asks for it: no branch has
   been made since the roadmaps began, and every branch before them was fast-forwarded
   the same day.
3. **The message format is a key of the table, its only written source:** this
   repository's `CLAUDE.md` line "Commit messages: `(type) description`" goes, or points
   to the key, once a tool reads it; a session outside the tools follows `git log`, as
   scriptorium's sessions did without any rule. The agent preferred no key, the format
   having held in every commit observed; the user chose the key, the conventions of this
   setup being read from `.agent-conventions.toml`, and the git domain to come reading a
   value rather than inferring one.
4. **Pull requests and review-thread replies are dropped for now** (FB8, RC10), and a
   push, of a branch or of a tag, waits for the user's request.
5. **No worktree at execution time** (WP4): the execution operation works in the checkout
   it is given, and parallel sessions get their worktrees from the harness.

The kept and improved rows go to a **git domain**, built by a follow-up roadmap that
Phase 4 creates, and to the roadmap skill's operations; Phase 4 names the domain.

### Plugin

Written by Phase 4.

## When To Revisit

Written by Phase 4.
