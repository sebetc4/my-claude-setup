# Skill Validation — 2026-10-14

Decided with the user on 2026-10-14, in roadmap `skill-validation`, Phase 0 (its design in
`phase-0-framing.md`, its measures in `phase-0-framing-report.md`): **the validation of
`authoring-skills` fixes its instruments' inputs and judgments, and every failure or
auditor point ends in a fix of the skill or of an instrument, the skill's by default,
never in a failure accepted.** Two skills built with the tool had bent to it:
`close-session` in this repository (roadmap `session-close`, Phase 1) and
`reviewing-delivered-code` in ai-ctl (roadmap `review-skill`, Phase 3), each paused and
described in the ignored `notes/design-feedback/2026-10-14-close-session-validation.md`
(V1 to V7) and `notes/design-feedback/2026-10-14-reviewing-delivered-code-validation.md`
(R1 to R6).

## The Problems

The validation has five instruments — the run's world, the grader's view, the
assertions, the auditor, the figures — and its procedure offered one lever, the skill,
with a proof asking every check to pass. When an instrument was wrong, the agent changed
the skill until the instrument passed. The phase's report maps each problem to its lines
in `domains/skill-tooling/`; in short:

- **The world a run meets**: no hook of the skill's domain in a run, the harness leaving
  out the user's and the run copying the skill alone (V1); the grader's rendering keeping
  only the turns, not what a session starts with (R1); one session per case (R2); a run
  with agents given a duration from the json result and per-agent output shared by call
  count, unmarked (R3).
- **Judgments read as signals**: one grading per run under a zero-failure proof, no step
  classing a failure (V2); an auditor whose verdict depended on what the caller wrote,
  its points drawn by an open search (V3); a premise inside an assertion (V6); guards
  told to discriminate (R4); a list failing whole on one item (R5).
- **Evidence in the wrong place**: sources only the editor reads, loaded at every use
  (V4); failures seen in real sessions or in a study counting for nothing (V5, R6).

## The Measures

On `close-session` at `65ca91f`, its text unchanged, $2.81 in all:

- **`skill-auditor`, twelve passes as subagents.** Six on the bare request of
  `references/audit.md`: six FAIL, one point in all six, five raised by one to three.
  Six on the request of 2026-10-13's last pair, which added a free-text "Context the
  files do not hold": six PASS. Read with the sixteen passes of 2026-10-13, which had
  seven requests between them, no verdict changed across 26 passes on a text and request
  held fixed; every change came with a change of text, of request, or both. All 28
  passes ran at `medium`, the agent's frontmatter setting no effort; two cited lines past
  a file's end. $0.05 to $0.10 a pass.
- **`skill-grader`, six runs of iterations 10 and 11 graded three times again**: one
  verdict in 54 changed, on an assertion carrying a premise (V6); the Parquet failure
  held four times in four; one reading in 24 named four guards weak. $0.08 to $0.12 a
  session.

So the instruments are stable at fixed inputs, and their inputs were not held.

## Decisions

- **No failure stands.** A failed assertion and an auditor's point are each a defect of
  the skill or of an instrument. Each ends in a fix, then a run or pass that succeeds;
  fixing an instrument never validates the skill by itself. The user's rule of
  2026-10-13 stands, a FAIL whose lines are answered never counts, and asking for a PASS
  at any cost is dropped: the user saw it degrade the tool, one auditor point making
  `close-session` worse until the evals caught it.
- **A failure is the skill's by default.** Six classes: `skill` and `variance`, the
  skill's; `grader`, `assertion`, `world` and `tool`, an instrument's. `skill` is the
  default; an instrument's class needs the evidence its row lists, produced by the tools
  — a second grading, the skill's line and the assertion quoted side by side, the hook
  named, the evals' regression — and the user's yes. Recorded in the iteration's
  `classes.json`, with a second grading of the failed assertions alone.
- **Why the procedure names the instruments' defects only as conditions.** Instruments
  do err, as the measures show; a rule saying so would hand the agent a way out. So
  `references/evaluate.md`, `references/audit.md` and both agents state the classes as
  conditions with their evidence, and nothing more general; this record holds the
  reason. The share of instrument classes is shown per iteration and raised with the
  user past one in four.
- **A case's world**: a `hooks` key in `evals/evals.json` installs the skill's domain's
  hooks in the run's folder as project hooks, each arm its version; a case turns one off
  through its fixture's configuration. The grader reads each session's starting context,
  kept whole under `context/`. A workflow's later step is tested from a fixture holding
  its intermediate state. A run with agents gets its wall duration and output marked
  where it is shared.
- **The criterion**, per assertion over the runs of one snapshot pooled: a guard with no
  failure classed `skill` or `variance`; a check with none classed `skill` and 80% or
  more over five runs or more; a list read item by item. Why 80% over five: the grader
  changed one verdict in 54 and `close-session`'s Parquet failure came once in fifteen
  graded runs; one such failure in five runs passes, two do not.
- **The auditor's verdict**: a request fixed word for word, its context in the skill's
  `evals/`; `effort: medium`, the effort of every measured pass; two passes started
  together, PASS when both pass. Each point is answered by a wording of the skill first;
  the auditor is at fault only when the evals show the fix regress a case, or the point
  names no judgment or a missing line, and is then fixed with a fixture under
  `evals/auditor/`, never by rewording the skill.
- **Sources** go to the skill's `evals/sources.md`, never installed nor loaded; a fact
  the agent observes in its own context needs none. **Failures seen in use** go to
  `failures_in_use` in `evals/evals.json`, each with its transcript or study, and ground
  a prohibition; a practice a study recommends that answers no failure does not.
- **Proof**: the two skills' recorded evidence judged again with the updated tool, in
  the roadmap's Phase 4; the skills resume in their own roadmaps.

## Not Done

- V7, the scripts' estimates before any measured run and `workspace.py`'s silent
  options: roadmap `session-close`'s Phase 2 hands them over.
- A case of several sessions in sequence: the fixture form covers a later step.
- Trigger evals and description tuning: no problem was raised with them.

## When To Revisit

- After the roadmap's Phase 4 and the first two skills validated with the update: the
  80% rate and the five runs; the `medium` effort, should the auditor's fixtures show
  points missed; a sequence of sessions in one case.
- As soon as more than one failure or point in four is classed as an instrument's over a
  skill's validation: whether the instruments are weak or the class serves as a way out.
- When a hand-off between sessions fails in use while the cases of both steps pass.
