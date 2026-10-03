# Phase 3 Report: Git

**Phase:** [phase-3-git.md](phase-3-git.md)
**Start Commit:** 53488cd

---

## Work Log

### 2026-10-02

Opened the phase from Phase 2's closure, committed as `53488cd`. Read Phase 2's file and
its report, written in this session: no restructuring pending, and no other phase in
progress. What binds this phase: the matrix format and the rules of evidence of the draft
record; the constraint Phase 1 added, the `[git]` table deciding per repository between
`main` and branches and when the execution operation commits (EP9, WP4); and what Phase 2
handed over — a task's commit comes after its declared proof passed and was recorded, row
RC10 is ruled with the pull-request rows, and `study/proof-micro-tests/` holds a
micro-test script for any wording this phase measures. At the user's rule, the opening
ends the turn: no work on the phase yet.

The user started the work. Read both skills in full: identical in 6.3.0 and 6.4.1, their
history in the release notes — consent before a worktree and provenance-based cleanup
(`RELEASE-NOTES.md:288-296`), discard taken off the menu (`:116`), removal no longer
forced over untracked files (`:89`) — and the plugin's two worktree tests, one of which
reports 50 of 50 runs choosing the harness's own tool once the skill names it. Read
first the transcripts, since the baseline period's go from about 2026-10-04: six distinct
calls, counted once per `tool_use` id — five of `finishing-a-development-branch`, four
in the baseline period, and one of `using-git-worktrees`, by cascade from
`executing-plans` on 2026-09-27, for a `git switch -c` the plan had already named.
Every finish ended in the base branch fast-forwarded, or a branch renamed `main`: no
pull request, no kept branch, no discard. The menu was given as written once, in English
inside a French conversation, and the user answered outside it ("merge et push"); twice
it went through a question tool; once the agent put a better option, the rename; once
the user said "on peut merger sur main" before any menu. On 2026-09-12 the agent saw
that switching to `master` would refuse or overwrite the user's uncommitted
`.gitignore`, and moved `master` with `git fetch . epub:master` instead.

Counted every git operation in the transcripts the same way: branches only under
superpowers' executors, each merged `--ff-only` and deleted the same day; three
`git worktree add`, each a temporary checkout of a revision in the session's scratchpad —
a build from the tree before a phase, a proof without `library/`, the reviewer's
instruction — never a workspace; no `EnterWorktree`, no `gh pr create`, no thread reply;
pushes only in this repository, at the user's request. Fetched the Claude Code pages on
worktrees for the harness's own mechanism: `--worktree`, `EnterWorktree`, subagent
isolation, cleanup on exit.

Surveyed the three repositories (task 2). forma-rust has no git: its contract says
`versioning = "none"`. This repository: 56 commits, linear, no merge commit, `(type)
description` with a body and a `Co-Authored-By` trailer, seven annotated
`<domain>-vX.Y.Z` tags, `main` ten commits ahead of `origin`; one commit per task under
the executors (13 in nine minutes on 2026-09-27), one per phase closure under the
roadmaps, skill-tooling's Phase 1 closing in 36 files. scriptorium: 71 commits, all on
`main`, never a branch nor a tag, the same format capitalized, a phase's work and its
closure often in one commit ("Add the svg skill and make proof, closing phase 3", 30
files), twelve commits ahead of `origin`. The format is written only in this
repository's `CLAUDE.md`; scriptorium follows it without a written rule. Before
2026-09-17 the user's repositories wrote French verb-first subjects (pdf-creator) and
Conventional Commits with a scope (my-claude), which `study/git/commit-message.md`, the
user's former command, prescribes.

Wrote the two matrices into the draft record under Git, with a table of the six calls
and one of the repositories' practice: 26 rows, 3 kept, 13 improved, 10 dropped. The
worktree rows go to a future git domain or to the harness, which makes, places and
removes its own worktrees; the integration rows go to the roadmap's closure, where the
`[git]` table puts a branch. FB8, the pull request, is dropped on the evidence — never
chosen, never made — and RC10 waits for the user's answer on it. Checked the cited
lines and counts before moving on.

Drew the `[git]` table from the survey and put it to the user: two keys, `branch` —
`trunk` or `roadmap` — and `commit` — `task` or `closure` —; the message format left to
the history and the instruction file, where it held in every commit observed, written or
not; push, pull requests, tags, trailers and worktrees outside the table, each with its
reason.

The user chose commits per task and pull requests dropped for now, and asked what
`trunk` and `roadmap` meant and why no `message` key. Explained both values — every
commit on `main`, or a branch per roadmap merged at its closure — and renamed `trunk`
`none`, the jargon being the obstacle; gave the reasons against the key — no failure
observed, two sources in a committed file and an ignored one, sessions outside the tools
reading only `CLAUDE.md` — and those for it, the second answered if the key is the only
written source. The user chose `none | roadmap` with `none` in both repositories, and
the key as the only source. Wrote the table and the five decisions into the draft
record, settled WP4, EP9, RC10 and RQ18, which waited for this phase — no `open` verdict
is left in the record —, and carried the decisions into Phase 4 as a constraint.
`make check` passed. The user asked to close the phase; `make check` passed again.

---

## Decisions

- **Commits per task** (the user, 2026-10-02): `commit = "task"` in this repository and
  scriptorium. A task's commit follows its recorded proof; the opening is a commit of
  its own and the closure commit holds the closure documents only. `closure`, the
  phase's work and closure in one commit, stays a value for a repository that wants it.
- **Branching takes two values, `none` and `roadmap`, both repositories on `none`** (the
  user, 2026-10-02). `roadmap` — a branch per roadmap, made at its first phase's
  opening, fast-forwarded into its base at its closure — is built by the follow-up
  roadmap only when a repository asks for it.
- **The message format is the `message` key, its only written source** (the user,
  2026-10-02): `(type) description` here, `(type) Description` in scriptorium. This
  repository's `CLAUDE.md` line goes, or points to the key, once a tool reads it — not
  before, or nothing would state the format.
- **Pull requests and review-thread replies are dropped for now** (the user,
  2026-10-02): FB8 and RC10. A push, of a branch or of a tag, waits for the user's
  request; no key.
- **No worktree key and no worktree at execution time** (WP4): parallel sessions get
  theirs from the harness and go with `branch = "roadmap"`; a temporary checkout of a
  revision goes outside the tree. Worktree creation, setup and cleanup are the git
  domain's, which Phase 4 names with the follow-up roadmaps.
- **The `[git]` table is read through `conventions.py`**, present when the contract says
  `versioning = "git"`, its values proposed from the history when it is missing, as for
  the other tables.

---

## Files Changed

**Added**
- `docs/roadmap/on-progress/superpowers-study/phase-3-git-report.md` — created at the
  opening, committed with it in `5ebcf1b`

**Modified**
- `docs/decisions/2026-10-01-superpowers-study.md`
- `docs/roadmap/on-progress/superpowers-study/README.md` — the opening's edits, committed
  in `5ebcf1b`, then this closure's
- `docs/roadmap/on-progress/superpowers-study/phase-3-git.md` — the opening's status,
  committed in `5ebcf1b`, then the work and the closure
- `docs/roadmap/on-progress/superpowers-study/phase-4-decisions.md`

---

## Problems And Deviations

- **The worktree rows rest on no observed use:** no worktree ever served as a workspace
  in the transcripts, so GW3 to GW10 and FB11 stand on Claude Code's worktree page, the
  plugin's own measure and reasoning. Left as a limit of the record; the git domain's
  evals measure them once it is built.
- **forma-rust has no git,** so the survey of how it commits found nothing to survey:
  its contract says `versioning = "none"`, and its answer is a repository without a
  `[git]` table. pdf-creator and my-claude, no longer on disk, were read from the
  transcripts only.
- **Two of the table's values serve no repository yet:** `branch = "roadmap"` and
  `commit = "closure"`. The first is built only when a repository asks for it; the
  second is the roadmap skill's behavior today.
- **This phase closes in one commit, its work and its closure together,** the practice
  its first decision replaces: no tool reads the `[git]` table yet.
- **The design took a second round of questions:** `trunk` was jargon the user did not
  follow, renamed `none`; and the user overturned the agent's advice against a
  `message` key, after asking for its reasons. Both recorded under Decisions.
- **No wording was measured:** the micro-test script of Phase 2 stayed unused, every
  choice of this phase being the user's on the evidence rather than a question of
  wording.

---

## Changes To Later Phases

- `phase-4-decisions.md`: added to its constraints — the follow-up roadmaps carry Phase
  3's decisions: the `[git]` table read by the execution operation, `close-phase` and
  `close-roadmap`, its values for this repository and scriptorium, `branch = "roadmap"`
  built on demand, this repository's `CLAUDE.md` line on commit messages replaced once a
  tool reads the key, and a git domain named in Phase 4.

---

## Assessment

The phase ruled on the two git skills — 26 rows in the draft record, 3 kept, 13
improved, 10 dropped — and settled the four rows earlier phases left to it, so that no
`open` verdict remains. With the user it designed the `[git]` table of
`.agent-conventions.toml`: `branch`, `none` or `roadmap`; `commit`, `task` or `closure`;
and `message`, the format's only written source. This repository and scriptorium take
`none`, `task` and their own format; forma-rust, without git, takes no table.

Its evidence is what the plugin's git skills actually did: five finishes, each ending in
the base moved forward and never in a pull request, the menu bypassed or reworded four
times out of five; one worktree call, for a `git switch -c`; branches only under the
executors, fast-forwarded the same day, and none since the roadmaps began. The worktree
capabilities that survive go to the harness, which makes and removes its own, and to a
git domain.

What Phase 4 needs to know first: the kept and improved rows of this phase go to a git
domain it names, and to the roadmap skill's execution operation, `close-phase` and
`close-roadmap`, which read the `[git]` table; the follow-up roadmap builds
`branch = "roadmap"` only on demand, and replaces this repository's `CLAUDE.md` line on
commit messages once a tool reads the key. Phase 4's constraints already carry this.
