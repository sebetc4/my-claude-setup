# Summary — skill-validation

---

## Where We Started

On 2026-10-14 two skills built with `authoring-skills`, `close-session` here and
`reviewing-delivered-code` in ai-ctl, were paused: both beat their baseline by their
second iteration, then spent most of their work answering the validation's instruments
rather than the skill's use. Their notes listed the defects, V1 to V7 and R1 to R6: a
run's world unlike the installed one, a judgment's spread read as a signal, rules of
evidence in the wrong place.

---

## Where We Landed

`skill-tooling` 0.1.2, released and installed on 2026-10-15. A run meets the world the
installed skill meets. The grader sees what each session started with. Each failure is
classed before any change, and the criterion is read in rates. The auditor's verdict is
reproducible on a fixed request. `docs/decisions/2026-10-15-validation-weight.md`
proportions the validation to the tool's risk. Both paused skills are handed back under
the default regime, `session-close` unblocked.

---

## What Each Phase Delivered

- **Phase 0, Framing.** The measures before the design: 26 auditor passes and 54 gradings
  showed the instruments stable at fixed inputs, so the design fixes the inputs — the
  request, the world, the premises, the effort — rather than adding passes.
- **Phase 1, Run World.** A case's domain hooks given through `--settings`, the skill
  laid out as an install lays it; `context/` and `whole/` for the grader; a later step's
  case from a recorded run; exact figures for runs with agents. Four wordings and eight
  iterations for two sentences of `references/evaluate.md`.
- **Phase 2, Judgments.** Six classes and `grade.py --again`; guards, checks and measures;
  the criterion in rates over pooled runs; the auditor's request and effort fixed. 97%
  against 69% on `authoring-skills`' own cases. The validation-weight decision, mid-phase,
  cut the rest of the roadmap from five phases to four and moved the regimes to
  `lean-workflow`.
- **Phase 3, Release.** Every auditor point on `authoring-skills` fixed at its source,
  mostly by cuts, over three iterations at the cap; the release, the tag, the hand-over.

---

## What We Learned

- An instrument stable at fixed inputs still misleads when its inputs drift: fix the
  request, the world and the premises before counting passes.
- A run read before its grading is no evidence; the grading decides.
- The weight of a validation lies in its iterations and their ceremony, not in the runs:
  a proof sized to the tool's risk, then real use, costs less and finds what matters.
- The auditor's verdict reproduces, its list of points does not: each pass samples a
  large skill anew, so "two PASS" on a 12,600-word skill is out of reach in three
  iterations.

---

## What We Are Leaving Open

- V4, where a portable skill's sources go, dropped on 2026-10-15, to revisit.
- V5 and R6, real-use failures as grounds for a prohibition, and the regimes written into
  `authoring-skills`: roadmap `lean-workflow`, Phase 1.
- The auditor's list of points not converging; `usage.py --help` ending on a traceback;
  `workspace.py --reuse` not carrying the grading (V7, `session-close`'s Phase 2).
