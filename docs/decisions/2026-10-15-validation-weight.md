# Validation Weight — 2026-10-15

Decided with the user on 2026-10-15, in roadmap `skill-validation`, Phase 2: **a tool's
validation is proportioned to its risk — a light regime by default, the full regime
argued in one line, an iteration cap — and real use is the main loop of improvement.**
No failure is marked passed and no rule is bent to pass one: each is fixed at its
source, in the tool or in the instrument. What changes is that a failure without risk no
longer holds back a release.

## The Figures

From the transcripts, through `shared/sessions/`, at API prices:

| Work | Days | Sessions | Cost | Runs and grading | State |
|---|---|---|---|---|---|
| `skill-tooling` | 14 | 44 | ~$720 | ~$173 | released |
| `close-session`, session-close Phases 0-1 | 1.5 | ~9 | ~$60-90 | ~$15 | blocked, not installed |
| `skill-validation`, to iteration 19 | 1.5 | 11 | ~$103 | ~$35 | Phase 2 of 5 |
| ai-ctl `review-skill` | 2 | 11 | ~$67 | ~$16 | blocked before any real use |

- The working sessions make 67 to 76% of the cost: the count of iterations, each with
  its announcements, yeses, readings and records, weighs more than the runs.
- Both paused skills were useful early: `close-session` passed 100% against 57% without
  it at iteration 2, `reviewing-delivered-code` 75% against 17%. `close-session` then
  took nine iterations and fourteen auditor passes, eight of them rewording one sentence
  that carried no risk.
- This roadmap's Phase 0 found the auditor's verdict unchanged over 26 passes at fixed
  inputs, and the grader changing one verdict in 54: what was missing was an exit. The
  roadmap meant to fix the validation made it heavier: `references/eval-files.md` went
  from 2,702 to 4,249 words, `references/evaluate.md` from 1,122 to 1,832.
- The tool reviews find defects in real use at little cost, but their most recurrent
  finding, raised in 24 reviews, waits unfixed behind a roadmap's end.

## Decisions

- **Default regime**, for any new tool or change: a baseline without the skill on two or
  three cases, one iteration with it, `audit.py` clean, one `skill-auditor` pass whose
  points are each fixed at their source — the skill, or the auditor when the point is
  wrong —, then the install and real use, watched by the tool reviews. About a day.
- **Full regime**, declared in one line when the roadmap or phase opens, only when one
  criterion holds: the tool builds or validates other tools (`authoring-skills`,
  `roadmap`); a failure would be silent or irreversible (destructive git, data lost,
  money spent unasked, security); a discipline skill. It keeps the criterion in rates and
  the auditor's two passes, PASS required, and stops at three iterations.
- **Stop rule**: once the tool beats its baseline clearly and the failures left carry no
  risk, iterating stops. Each failure left keeps its class, goes to the release's
  changelog and the tool's watch points, and real use brings its fix.
- **Fix from use**: a failure seen in a real session is quoted with its transcript,
  fixed at its source, checked by `audit.py`, released as a patch, and added to the
  skill's `failures_in_use` for its next evaluation. Such a fix lands at any time,
  during another roadmap included.
- **Short records**: a study on real data stays welcome; what it yields, a report entry
  or a design, is written short — what changed, the figures, the decisions.

## Applied

- Roadmap `skill-validation`: Phase 2's tasks 1, 2 and 5 met on iteration 19, 97%
  against 69%, its one failure classed `variance`, the eight runs it called for dropped;
  the Auditor task keeps its fixes with a proof of four passes instead of 24. Phases 3
  and 4 merge into one: the regimes, the fix from use, real-use failures as evidence,
  the release and the hand-over. Dropped: the replay of both skills' evidence, the
  sources' place (V4), the re-evaluation of `authoring-skills` on all its evals. The
  same day, the regimes, the fix from use and real-use failures as evidence moved to
  roadmap `lean-workflow`, which revises the workflow in depth; `skill-validation` keeps
  its release and hand-over.
- `close-session` is installed as it stands when its roadmap resumes; ai-ctl's
  `review-skill` goes to its Phase 4, the first review of real code, before any further
  iteration.
- The agent's memory on the auditor's verdict follows the two regimes.

## When To Revisit

- After the first three tools built under the default regime: whether real use found
  what the cut iterations would have, and at what cost.
- When a failure the default regime let through costs more in use than its iteration
  would have: whether the full regime's criteria miss a kind of tool.
- When the sources the auditor asks for weigh on a skill's runs: the sources' place, V4.
