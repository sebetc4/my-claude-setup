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

---

## Decisions

- **Opened before `session-close`'s end.** The roadmap's opening decision had it finish
  first; the user opened Phase 0 with its tasks 4 and 7 still open. The README's
  `**Blocked By:**` is left as it stands until they close.
- **The measure's script stays out of git.** `baseline.py`, in the ignored `notes/`, on the
  user's word: the design says where it belongs, a tool of its own or `token-usage`'s
  script; Phase 3 runs it again on its window.

---

## Files Changed

---

## Problems And Deviations

---

## Changes To Later Phases

---

## Assessment
