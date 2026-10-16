# Phase 0 Report: Measure And Design

**Phase:** [phase-0-measure-and-design.md](phase-0-measure-and-design.md)
**Start Commit:** e13f1ed

---

## Work Log

### 2026-10-15

Phase opened on the user's word, while roadmap `session-close` still has its Phase 2's
tasks 4 and 7 open: the start line's noise, which waits for starts to accumulate, and the
release.

Task 1, through `shared/sessions/`, from 2026-09-28 to 2026-10-15 22:23: 85 working
sessions, 885 `claude -p` sessions, 233 commits, every call priced. A call goes to the
roadmap its session's next commit names, else its session's last commit, else the
repository's next commit; a commit naming none keeps the previous one's, one creating a
roadmap moves nothing; a `claude -p` session follows its working session. Checked against
`docs/decisions/2026-10-15-validation-weight.md`: `skill-tooling`, 44 sessions and $173
of runs, the same. Every figure below comes from
`notes/lean-workflow/baseline.py 2026-09-28T00:00:00+02:00 2026-10-15T22:23:53+02:00`, the
days from the creation commits and the installs it lists.

| Roadmap | Opening to tool installed | Sessions | Cost | `claude -p` | Working share |
|---|---|---|---|---|---|
| `skill-tooling` | 13.4 days, 1.4 paused | 44 | $657 | $173 | 74% |
| `superpowers-study` | a study, closed in 1.4 days | 4 | $69 | $0 | 100% |
| `token-usage` | its usage reader in `review` at 6.4 days; its skill not built | 14 | $88 | $0 | 99% |
| `session-close` | 2.3 days, 1.3 blocked | 13 | $94 | $42 | 56% |
| `skill-validation` | 1.2 days, to `skill-tooling` 0.1.2 | 16 | $127 | $35 | 73% |
| all | | 85 | $1,040 | $250 | 76% |

The working sessions make 76% of the cost: main threads 64%, their subagents 12%.

The 21 reports of opened phases, this one aside, hold 131,408 words for 181 tasks: 6,258
per report, 726 per task, from 364 per task in `superpowers-study` to 886 in
`skill-validation`; `skill-tooling`'s Phase 4 alone, 26,064 words, 1,862 per task.

In the eval phases, 32 iterations: 2.4 of the user's yeses and 5.5 prompts per iteration;
`skill-tooling`'s Phases 4 and 5, which built the eval scripts, 4.2 and 11.6 over nine;
`session-close`'s Phase 1, 1.5 and 3.1 over eleven; `skill-validation`, 1.8 and 3.2 over
twelve. A yes is a prompt of at most 60 characters opening on an approval, a lower bound.
Beyond the task: 74 of the user's 314 prompts since 2026-09-28, 24%, record, end or resume
a session, or report a limit. Task 1 done.

Task 2, same window, from `notes/lean-workflow/tools.py` with the same bounds. Costs at API
prices; an agent's output is partly estimated, so its runs are a floor.

| Tool | Imposes | Caught | Cost |
|---|---|---|---|
| Roadmap skill, 8,333 words, and `roadmap-auditor` | contract check before any operation; 10 invariants; a 6-step opening; the report kept at each step, read whole at each resume; a closure of checks, 6-step ritual, `progress.py --check`, `check_links.py`, the auditor, commit, next phase; a proof per task | auditor 26 runs, 26 PASS; `progress_guard.py` 4 blocks; `--check` 48 problems in 210 runs, mostly the README's lag by design; links 3 broken in 116 runs; 121 review findings | 83 loads, about $0.06 each; reports read $24 and written $15, phase files $15, READMEs $3, through Read and edits only; auditor $7.6 |
| `authoring-skills`, 13,052 words, and its 3 agents, 1,405 | create in 10 steps, edit, audit by 46 static rules and the auditor, evaluate with announced runs and the user's yes, 13 eval file schemas | `audit_skill.py` 40 blocks: R3 28, X2 16, C4 7, N3 3; `skill-auditor` 50 runs, 34 FAIL, 14 PASS; 45 review findings | `claude -p` $250: runs $185, graders and comparators $31, triggers $24, probes $11; eval runs as subagents before the scripts $109; auditor $5.7; 2.4 yeses per iteration |
| Review domain: Stop hook, `tool-review` 2,749 words | a review turn per tool and session at Stop | 272 findings: defect 116, skill-gap 67, tooling-gap 23, noise 20, waste 18; 97 of them on the review domain itself; the most recurrent, 34×, still open | 107 requests here, 93 loads; 158 reviews from every project, $0.19 median over the 60 measured, about $30 |
| `CLAUDE.md`, 1,960 words | 3 principles, 7 conventions — standard library, test-first, English files, every skill file reached, coupling doc, commit format, release —, 12 gotchas; `check-skills.py` after every edit | `check-skills.py` 385 blocks; of the 210 after Edit or Write, 120 test-first's red step, 86 still failing, 4 new after a code edit | loaded at every call, $8.5 |
| Memories, 12 files, 2,865 words | French replies, roadmaps cited by name, commit once a step is recorded, records in the report, costs announced as a limit, the auditor's verdict by regime, short records, the coupling doc | each came from a correction of the user's | index $1.6; no memory file read with Read |

Reading, for the design: the checks that cost least caught most — `audit_skill.py`,
`check-skills.py`'s 4, the links —, while `roadmap-auditor` passed every closure. The weight
lies in what the rules ask of the session, not in the checks: the eval runs, $359 with
those made as subagents, a third of the cost; the reports, 131,408 words; and a review turn
whose findings fall for a third on its own domain.

Limits of the list: files read through Bash, `cat` or `sed`, are not counted, nor
`check-skills.py`'s 175 blocks after a Bash edit; an auditor's verdict comes as a tool's
input in its own transcript, not as text, which `tools.py` reads. Session closed on the
user's word with the list shown, not yet approved.

**Where the next session starts:**
1. Task 2's proof: show the user the list above for their reading; on their yes, tick
   task 2, the phase's count at 2/4, the README's block from `progress.py`, and commit
   with this record.
2. Task 3: decide with the user, for `roadmap-dependencies`, `roadmap-execution`,
   `working-method`, `git-domain`, `session-review` and `token-usage`'s remaining tasks:
   keep, merge into this roadmap, or cut; in this report and `docs/roadmap/README.md`.
- Put to the user: does task 2's list suit them?
- Uncommitted: this report, task 2's list and this entry. Out of git by decision:
  `notes/lean-workflow/baseline.py` and `tools.py`.

### 2026-10-16

Task 2's list read by the user, who found it a good view of how the tools are used. Task 2
done, committed as `9a10c5e`.

Task 3: the five waiting roadmaps and `token-usage`'s remaining tasks read, a proposal
for each put to the user, approved but for `git-domain`, which the user keeps (Decisions).
Recorded in this roadmap's Phases 2 and 3, `git-domain`'s README, `session-close`'s
Dependencies, `docs/claude-code-builtins.md` and the overview, whose Cut table points to
`9a10c5e` for the cut roadmaps' files. Two memories updated: `roadmap-cite-by-name` now
waits for Phase 2, `superpowers-docs-location` notes that `.superpowers/` has no owner left.
Task 3 done.

Roadmap `token-usage` closed as decided: Phase 2 closed with 4 tasks of 12, Phase 3
removed, the roadmap moved to `completed/`; `roadmap-auditor` failed the phase's closure
once, on its Changes To Later Phases, then passed both. The four cut roadmaps' folders
are still in `pending/`: their `git rm` was refused by the permission classifier, left to
the user.

The notes and the tool reviews gone through with the user. Notes, marked in their
`**Status:**` line: `agent-tool-before-agents`, `close-session-validation`,
`reviewing-delivered-code-validation` and `audit-t1-legacy-axis` processed;
`run-estimate-per-case` in progress, cited by Phases 1 and 2; the two hand-overs to ai-ctl
kept until its `review-skill` resumes; `studied-tools/md-manager/2026-10-14-ai-ctl-feedback.md`
kept out of this roadmap, for a future tool managing `CLAUDE.md`, made cross-agent with
`AGENTS.md`. Reviews: `make reviews`, 63 reviews, 43 findings; four already fixed in
`skill-tooling` 0.1.2 and 0.1.3 set aside (T1 `legacy`, the Agent tool before agents, the
failure classes, the auditor's request fixed); `resume_note.py`'s noise (2×) and
`close-session`'s Result line (1×) to `session-close`'s Phase 2; the rest below, into
Phase 1's Cut task and Phase 2's Roadmap and Reviews tasks.

| Phase | Target | Findings |
|---|---|---|
| 1 | `authoring-skills`' `SKILL.md` | a fix to the skill's scripts: edit procedure or test-first alone (6×) |
| 1 | `skill-auditor` | a fix relying on a shell variable across Bash calls (5×); shared copies judged as the skill's (3×); agents listed in `evals.json` not judged (1×) |
| 1 | `run.py` | duration from the last result message (4×); `--start` in the foreground unsaid (1×); earlier turns as a case key (1×) |
| 1 | `workspace.py`, `grade.py` | `--reuse` not carrying the grading (4×) nor taking a folder path (2×); `grade.py`'s budget not scaled to the run (2×) |
| 1 | references | a repository case's copy without history or ignored files (1×); scripts' tests under `evals/` (1×); a `probe.py` (1×); the fix-from-use row and the default regime's single auditor pass (1× each, Regimes tasks) |
| 2 | `tool-review`, `review.py`, `usage.py` | a SessionStart hook's context counted as a run (34×, D1 cut with `token-usage`); a review asked before an agent's background runs answer (1×); `usage.py --help` read as a path (2×); a `cat` read counted (1×, measure-fix task) |
| 2 | `session_resume.py` | the instruction repeated on each line (4×); no line for a roadmap with no phase open (1×) |
| 2 | `report.md` | a Problems entry refuted later rewritten (4×); short entries (2×); the resume reading the last hand-over (2×); a rename threshold (1×); the skill for the files to modify loaded on resume (1×); a waiting phase's Files Changed by roadmap (1×) |
| 2 | other roadmap references | Roadmap Status at the first opening (3×); adding or amending a task of a phase not open (3×); a 🟡 phase routed to the resume (1×); the next phase's opening committed (1×); tasks moved to another roadmap (1×) |
| 2 | `roadmap-auditor`, `progress.py` | each check named under the verdict (2×); a ⏸️ phase's floor (1×); `--check`'s mid-phase lag (1×); the 19-cell cap and `--write` (1× each, fixes task) |
| 2 | `roadmap-dependencies`' Phase 3, not named in Phase 2's fixes task | `session_resume.py` on a `resume` source injecting the state line alone (13×); `create.md` proposing the answers the conversation gives (5×); a git-ignored document cited with a backtick (5×); the auditor searching the old path after a move (5×) and listing its checks (4×), running read-only commands, without `Grep` and `Glob`; the user's uncommitted work at a closure; the README's Tasks column; file names for titles in forma-rust's block; `--check`'s agreement said in `SKILL.md` |

Two notes of ai-ctl came the same day, both to Phase 2 on the user's word, rather than a
patch now: `2026-10-16-progress-bar-full-while-in-progress.md`, a 🟡 phase at N/N showing
20 cells, to the fixes task with its option 1, the status saying a phase is finished;
`2026-10-16-subagent-output-default.md`, the 5,400-token default doubling the cost of
ai-ctl's read-only agents at `high` ($105.91 counted, $51.61 recorded), to the measure-fix
task with its option 2, a default by effort. Both marked processed.

The user ran the `git rm` of the four cut roadmaps, committed as `7b84048`. Asked whether
every improvement of the roadmap skill is in Phase 2: yes, explicitly or through the tables
above; ten of `roadmap-dependencies`' fixes, which only `9a10c5e` still held, were added to
the table. Left out: the stale review request
`reviews/2026-09-27-b93e102d-session-resume.md`, kept by `--archive`, for the user to
delete; this session's three tool reviews wait under `reviews/` for the next
`make reviews`, two findings of theirs not in the table: `review.py` asking again for a
tool reviewed before a mid-session archive, `tools/reviews.py` keeping a request no Stop
will come back to. Session closed at the user's word.

**Where the next session starts:**
1. Task 4: write the design in `phase-0-measure-and-design.md`'s `## Design` — what is
   removed, what changes, the targets of Phases 1 to 3 — from tasks 1 and 2's figures, the
   decisions of task 3 and the findings tables above, which Phases 1 and 2 must each fix,
   cut or set aside; the design also says where `baseline.py` and `tools.py` go, and what
   replaces the revisit of `docs/decisions/2026-10-04-plugins-removed.md`. Then the
   decision record `docs/decisions/<date>-lean-workflow.md`, and the user's approval.
2. Then Phase 0's closure; Phase 1 waits for `session-close`'s end, its tasks 4 and 7.
- No question waits for the user.
- Nothing uncommitted; out of git by decision: `notes/lean-workflow/baseline.py`,
  `tools.py`.

Task 4 resumed. Two measures for the design, by scratch scripts not kept. The eval
scripts started in working sessions since 2026-09-28: `run.py` in 27, `grade.py` 22,
`triggers.py` 5, `compare.py` 2, `tuning.py` 1, `viewer.py` served in 8 and one
`feedback.json` saved against 34 `benchmark.md`. The reviews' saturation, simulated on the
175 complete reviews: at 10 and 5, today's, 138 asked and 3 of 69 (kind, target) pairs
never raised; at 5 and 2, 101 and 8; at 3 and 1, 77 and 12. Design written in the phase
file and put to the user, who approved it and asked for the case on its two most
debatable cuts. `roadmap-auditor`'s nine points for a phase: three check what the design
cuts — acceptance criteria, Files Changed, the Changelog —, three are `progress.py
--check`'s, and three are left — a moved task present in its later phase, two sections
not empty, the `**Completed:**` date. The README's `## Changelog`: 7,864 of the 14,914
words of the 9 roadmap READMEs of this repository and the three others, 53%, 65 entries;
written by `create.md`, `close-phase.md` and `close-roadmap.md`, read by no tool but the
auditor's eighth point.

The Changelog's cut approved. On `roadmap-auditor`, the user asked who would say a check
is missing when it does not exist: a fix from use answers a failure that shows, never one
that is silent. Settled with the user (Decisions): the auditor keeps a phase closure's two
points of judgment, each ticked task's proof and each moved task present in its later
phase; the two mechanical points go to `progress.py --check`; the same rule adds the
Deviations to the resume's reading. Design updated, decision record
`docs/decisions/2026-10-16-lean-workflow.md` written, `plugins-removed`'s revisit marked
replaced, Phase 3's Judge task given the auditor's verdict, task 4 ticked.

**Where the next session starts:**
1. Phase 0's closure: every task is ticked; close it with the roadmap skill as installed,
   its auditor and Files Changed included — the design applies from Phase 2.
2. Then Phase 1, which waits for `session-close`'s tasks 4 and 7.
- No question waits for the user.
- Out of git by decision: `notes/lean-workflow/baseline.py`, `tools.py`.

Phase 0 closed on the user's word. Phase 1 not opened: the README's `**Blocked By:**`
holds it until `session-close` ends.

---

## Decisions

- **Opened before `session-close`'s end.** The roadmap's opening decision had it finish
  first; the user opened Phase 0 with its tasks 4 and 7 still open. The README's
  `**Blocked By:**` is left as it stands until they close.
- **The measure's script stays out of git.** `baseline.py`, in the ignored `notes/`, on the
  user's word: the design says where it belongs, a tool of its own or `token-usage`'s
  script; Phase 3 runs it again on its window.
- **The waiting roadmaps, with the user on 2026-10-16** (task 3):
  - `roadmap-dependencies` cut: its dependency model and generated overview add rules; the
    fixes of its Phase 3 that the reviews raised most go to Phase 2.
  - `roadmap-execution` cut: `execute-phase` and two agents add weight, and
    `roadmap-auditor` passed 26 of 26 closures; `Proof:` and `## Design` go to Phase 2 if
    the design keeps them, the `[git]` table to `git-domain`.
  - `working-method` cut; one of its skills proposed as Phase 3's first tool.
  - `session-review` cut: its aim is `tool-review`'s, whose domain already reviews itself
    for a third of its findings; scriptorium keeps its own.
  - `git-domain` kept, after this roadmap, on the user's word: the need is there though no
    repository asks — commits pile up without a convention, no branch strategy is set.
  - `token-usage` closed: two measure fixes, the release of review 0.3.0 and roadmap 2.0.4,
    installed unreleased, and the measure's scripts go to Phase 2; `reviewing-token-usage`,
    `make reviews`' costs, three defects and its Phase 3's validation cut.
- **ai-ctl's two notes of 2026-10-16 wait for Phase 2, no patch now** (the user): a
  proper fix there is cleaner than a temporary patch, though the 5,400-token default
  misleads ai-ctl's cost reads meanwhile.
- **Task 4's record says what replaces the revisit of
  `docs/decisions/2026-10-04-plugins-removed.md`**, tied to the close of `working-method`
  and `roadmap-execution`, both cut.
- **The design, approved by the user on 2026-10-16** (task 4), with two changes of
  theirs: the README's `## Changelog` cut as proposed; `roadmap-auditor` kept on a phase
  closure's two points of judgment rather than cut.
- **A failure that would be silent keeps its check; one that shows can wait for use**
  (the user): no cut of Phases 1 and 2 removes a check against a silent failure.

---

## Files Changed

**Added**

- `docs/decisions/2026-10-16-lean-workflow.md`
- `docs/roadmap/completed/token-usage/summary.md` — `token-usage`'s closure, decided in task 3
- `docs/roadmap/pending/lean-workflow/phase-0-measure-and-design-report.md`

**Modified**

- `docs/claude-code-builtins.md` — task 3
- `docs/decisions/2026-10-04-plugins-removed.md`
- `docs/roadmap/README.md`
- `docs/roadmap/on-progress/session-close/README.md` — task 3, its Dependencies
- `docs/roadmap/on-progress/session-close/phase-2-adoption-and-release-report.md` — task 3 and the findings handed to `session-close`'s Phase 2
- `docs/roadmap/pending/git-domain/README.md` — task 3
- `docs/roadmap/pending/git-domain/phase-0-framing.md` — task 3
- `docs/roadmap/pending/lean-workflow/README.md`
- `docs/roadmap/pending/lean-workflow/phase-0-measure-and-design.md`
- `docs/roadmap/pending/lean-workflow/phase-1-authoring-skills.md`
- `docs/roadmap/pending/lean-workflow/phase-2-roadmap-and-conventions.md`
- `docs/roadmap/pending/lean-workflow/phase-3-use-and-measure.md`

**Deleted**

The four roadmaps cut in task 3, their files at `9a10c5e`; and `token-usage`'s Phase 3,
removed at its closure:

- `docs/roadmap/pending/roadmap-dependencies/README.md`
- `docs/roadmap/pending/roadmap-dependencies/phase-0-framing.md`
- `docs/roadmap/pending/roadmap-dependencies/phase-1-dependencies.md`
- `docs/roadmap/pending/roadmap-dependencies/phase-2-overview-and-hook.md`
- `docs/roadmap/pending/roadmap-dependencies/phase-3-fixes.md`
- `docs/roadmap/pending/roadmap-dependencies/phase-4-validation-and-release.md`
- `docs/roadmap/pending/roadmap-execution/README.md`
- `docs/roadmap/pending/roadmap-execution/phase-0-framing.md`
- `docs/roadmap/pending/roadmap-execution/phase-1-proof-and-template.md`
- `docs/roadmap/pending/roadmap-execution/phase-2-git-table.md`
- `docs/roadmap/pending/roadmap-execution/phase-3-execute-phase.md`
- `docs/roadmap/pending/roadmap-execution/phase-4-validation-and-release.md`
- `docs/roadmap/pending/session-review/README.md`
- `docs/roadmap/pending/session-review/phase-0-framing.md`
- `docs/roadmap/pending/session-review/phase-1-standard-skill.md`
- `docs/roadmap/pending/session-review/phase-2-adoption-and-release.md`
- `docs/roadmap/pending/working-method/README.md`
- `docs/roadmap/pending/working-method/phase-0-framing.md`
- `docs/roadmap/pending/working-method/phase-1-shaping-work.md`
- `docs/roadmap/pending/working-method/phase-2-finding-root-causes.md`
- `docs/roadmap/pending/working-method/phase-3-release-and-turn-off.md`
- `docs/roadmap/on-progress/token-usage/phase-3-validation-and-release.md`

**Renamed**

`token-usage`'s closure, decided in task 3:

- `docs/roadmap/on-progress/token-usage/README.md → docs/roadmap/completed/token-usage/README.md`
- `docs/roadmap/on-progress/token-usage/phase-0-framing-report.md → docs/roadmap/completed/token-usage/phase-0-framing-report.md`
- `docs/roadmap/on-progress/token-usage/phase-0-framing.md → docs/roadmap/completed/token-usage/phase-0-framing.md`
- `docs/roadmap/on-progress/token-usage/phase-1-usage-reader-report.md → docs/roadmap/completed/token-usage/phase-1-usage-reader-report.md`
- `docs/roadmap/on-progress/token-usage/phase-1-usage-reader.md → docs/roadmap/completed/token-usage/phase-1-usage-reader.md`
- `docs/roadmap/on-progress/token-usage/phase-2-reviews-and-reports-report.md → docs/roadmap/completed/token-usage/phase-2-reviews-and-reports-report.md`
- `docs/roadmap/on-progress/token-usage/phase-2-reviews-and-reports.md → docs/roadmap/completed/token-usage/phase-2-reviews-and-reports.md`

---

## Problems And Deviations

- **Opened before `session-close`'s end**, against the roadmap's opening decision, on the
  user's word (Decisions); Phase 1 waits for it.
- **The measure's limits:** files read through Bash and `check-skills.py`'s blocks after a
  Bash edit are not counted, an auditor's verdict comes as a tool's input; the figures are
  floors there. The two scripts stay out of git until Phase 2's Measure task.
- **The cut roadmaps' `git rm` refused by the permission classifier**, run by the user,
  `7b84048`.
- **The roadmap folder stayed in `pending/` while Phase 0 was 🟡**, the skill moving it
  only at a closure that opens the next phase; it stays there until Phase 1 opens. The
  design moves it at the first opening, Phase 2.
- **`progress.py` drew 20 cells for Phase 0 at 4/4 while 🟡**, against the Progress bar
  invariant's ceiling: ai-ctl's note of 2026-10-16, Phase 2's fixes task.

---

## Changes To Later Phases

- `phase-2-roadmap-and-conventions.md`: three tasks added — the roadmap skill's fixes from
  `roadmap-dependencies`, two measure fixes from `token-usage`, the measure's scripts
  brought in —; the release names review 0.3.0 and roadmap 2.0.4. Approved by the user
  with task 3.
- `phase-3-use-and-measure.md`: the first task proposes `finding-root-causes` or
  `shaping-work`. Approved by the user with task 3.
- `phase-2-roadmap-and-conventions.md`: the Conventions task takes `CLAUDE.md`'s line on
  the review domain from `token-usage`'s Phase 3, removed at its closure on 2026-10-16.
- `phase-3-use-and-measure.md`: the Judge task also judges `roadmap-auditor`'s two points
  from their reviews, as the design keeps them on that condition.

---

## Assessment

The phase measured the workflow and set its design. The weight is in what the rules ask of
a session — iterations and their yeses, long reports, tools used once or twice —, not in
the checks: the cheapest caught most. Four waiting roadmaps were cut, `token-usage`
closed, `git-domain` kept; 43 review findings went to Phases 1 and 2. The design, approved
with the user's two changes, cuts steps, records and three eval scripts, keeps every check
against a silent failure, and sets seven targets for Phase 3
(`docs/decisions/2026-10-16-lean-workflow.md`).

What Phase 1 needs first: the design's Phase 1 section and its targets — `authoring-skills`
at most 9,000 words with two agents, one yes per iteration —, then the 2026-10-16
findings table's Phase 1 rows; it opens once `session-close` ends.
