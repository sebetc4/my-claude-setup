# Lean Workflow — 2026-10-16

Decided with the user on 2026-10-16, in roadmap `lean-workflow`, Phase 0: **the workflow
is lightened by cutting steps, records and tools that serve little, never a check against
a failure that would be silent.** The design in full is the phase's `## Design`
(roadmap `lean-workflow`: `phase-0-measure-and-design.md`); this record keeps the
decision, its figures and when to revisit it.

## The Figures

From the transcripts of 2026-09-28 to 2026-10-15, through `shared/sessions/`, at API
prices (roadmap `lean-workflow`: `phase-0-measure-and-design-report.md`):

- 85 working sessions and 885 `claude -p` sessions, $1,040; the working sessions make 76%.
- Eval iterations: 2.4 of the user's yeses each. Eval runs, those made as subagents
  included, $359, a third of the cost.
- Reports: 131,408 words for 181 tasks, 726 per task. The READMEs' changelogs: 53% of
  their words, read by no tool.
- `roadmap-auditor`: 26 closures passed of 26, one FAIL since, on a section's wording.
  `compare.py` started twice in working sessions, `tuning.py` once; one feedback saved
  against 34 benchmarks.
- The cheapest checks caught most: `audit_skill.py` 40 blocks, `check-skills.py` 4 new
  failures, `check_links.py` 3 broken links.
- The tool reviews: 272 findings for about $30, 97 of them on the review domain itself.
  Saturation at 5 reviews instead of 10 would have saved about $7 and lost 5 of the 69
  targets raised.

## Decisions

- **A failure that would be silent keeps its check** (the user): a fix from use answers a
  failure that shows, and nobody reports a check that does not exist. A failure that
  shows can wait for use.
- **`authoring-skills`** (Phase 1): `viewer.py`, `compare.py` with `skill-comparator`, and
  `tuning.py` removed; `references/eval-files.md` cut to the files the agent writes; one
  yes per iteration; the regimes of `2026-10-15-validation-weight.md` written in.
- **The roadmap skill** (Phase 2): under git, no Files Changed; no README Changelog,
  Version or Last Updated; the phase template without the sections that repeat the skill
  or the tasks' `Proof:` lines; four report sections, short entries, the latest hand-over
  only; a resume reading the phase file, the Decisions, the Deviations and the last
  hand-over; the first opening moving the folder. `roadmap-auditor` audits a phase
  closure on two points, each ticked task's proof and each moved task present in its later
  phase, kept on condition that its reviews show it pays.
- **Conventions and memories** (Phase 2): `CLAUDE.md` at most 1,000 words; three
  memories left, the rest carried by the tools.
- **The review domain**: kept, no longer temporary, its requests unchanged; its own
  defects fixed.
- **The measure**: `tools/measure.py`, run again in Phase 3.

## Targets

Judged in Phase 3 on real use:

| Measure | 2026-10-15 | Target |
|---|---|---|
| A tool, request to install | 1.2 to 2.3 days, $94 to $127 | ≤ 1 day, ≤ $50 |
| The user's yeses per eval iteration | 2.4 | 1 |
| `authoring-skills`: words, agents | 13,052, 3 | ≤ 9,000, 2 |
| Roadmap skill: words; auditor's words | 8,333; 467 | ≤ 6,000; ≤ 250 |
| `CLAUDE.md` words, memories | 1,960, 12 | ≤ 1,000, 3 |
| Report words per task | 726 | ≤ 300 |
| Review findings on the review domain | 36% | ≤ 10% |

## What It Replaces

The revisit of `2026-10-04-plugins-removed.md`, tied to the close of `working-method` and
`roadmap-execution`, both cut: planning comes back through the roadmap skill's
`## Design` and `Proof:`, design or debugging through the tool Phase 3 builds first, and
a capability missed in use is a request for a tool under the default regime.

## When To Revisit

- At Phase 3's judgment: each target met or not, and whether `roadmap-auditor`'s two
  points paid, from its reviews.
- When a failure the workflow let through is found late and silent: which check it
  lacked.
