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
- **Task 4's record says what replaces the revisit of
  `docs/decisions/2026-10-04-plugins-removed.md`**, tied to the close of `working-method`
  and `roadmap-execution`, both cut.

---

## Files Changed

---

## Problems And Deviations

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

---

## Assessment
