# Create A Roadmap, Add A Phase

Two operations: opening a new roadmap, and adding a phase to one that already
exists. Both produce content under the contract's `Root`.

## Questionnaire

Ask exactly five questions when opening a new roadmap:

1. **Name** — what is the roadmap called?
2. **Purpose** — why does this roadmap exist?
3. **Scope** — what is kept in scope, and what is explicitly out of scope?
4. **Phase breakdown** — what phases does the work split into?
5. **Parent** — is there a parent roadmap this one reports to?

## Directory Structure

Read `Root` from the contract. A new roadmap is created in the initial state,
`pending`:

```
<Root>/pending/<roadmap-name>/
├── README.md            from assets/templates/roadmap-readme.md
├── phase-0-<slug>.md    from assets/templates/phase.md
├── phase-1-<slug>.md
└── ...
```

`README.md` comes from `assets/templates/roadmap-readme.md`; each phase file
comes from `assets/templates/phase.md`. Fill in the questionnaire answers and
the phase breakdown, then resolve every remaining placeholder from the table
below — with one exception: `{{START_DATE}}` and `{{COMPLETION_DATE}}` belong
to the Dates invariant in `SKILL.md`, which assigns them to opening and to
closure. Leave those two unresolved here.

No report is created here: a phase has no report until `open-phase.md`
opens it, per `references/report.md`.

**Template boilerplate prose and the status legend are rendered in the
contract's `Language`**, per the Language invariant — they are text a reader
reads, not skeleton to copy verbatim. Headings stay in English.

**A produced document carries nothing but the template's headings and the
filled placeholders.** The templates hold no guidance of their own; every
instruction for filling them lives in the reference files. Never copy an
explanatory note, a worked example, or a comment into a roadmap, a phase
file, a report, or a summary.

**The folder name is permanent**, per the Folder name invariant in
`SKILL.md`. The move between state folders belongs to `close-phase.md` and
`close-roadmap.md`, not to this operation.

**Phase numbering** starts at `phase-0`.

## Initial Values

What to write into the placeholders the questionnaire does not answer, for a
roadmap that has delivered nothing yet:

| Placeholder | Initial value |
|---|---|
| `{{VERSION}}` | `1.0.0` |
| `{{ROADMAP_STATUS}}` | 🔴 with its label, per the Statuses invariant |
| `{{LOCATION}}` | the roadmap's folder, `<Root>/pending/<roadmap-name>/` |
| `{{CREATED_DATE}}`, `{{LAST_UPDATED}}` | today, per the Dates invariant |
| `{{CHANGELOG_ENTRY}}` | one entry recording the roadmap's creation and its phase breakdown |
| `{{PROGRESS_BARS}}` | one line per phase plus the `TOTAL` line, every one at `0%`, computed per the Progress bar and Totals invariants |
| `{{CURRENT_PHASE}}` | `—` — no phase is open until `open-phase.md` runs |
| `{{BLOCKED_BY}}` | `—`, unless a dependency is already known |
| `{{NEXT_MILESTONE}}` | the first phase |
| `{{PHASES_LIST}}` | one entry per phase, each 🔴 |
| `{{STATUS_EMOJI}}`, `{{STATUS_LABEL}}` | 🔴 with its label, per the Statuses invariant |
| `{{PERCENTAGE}}`, `{{DONE_COUNT}}` | `0` and `0` |
| `{{TOTAL_COUNT}}` | that phase's task count |
| `{{PREVIOUS_PHASE_FILE}}` | the previous phase's file name, such as `phase-2-<slug>.md` |
| `{{PREVIOUS_REPORT_FILE}}` | that phase's report name, per the Reports invariant, such as `phase-2-<slug>-report.md` |
| `{{REPORT_FILE}}` | this phase's own report name, per the Reports invariant |

Optional sections are omitted with their heading rather than filled with a
dash — a template that imposes a heading produces an empty heading:

- In the README, `## Dependencies` and `## Related Documentation` appear only
  when they have content.
- In the README, `## What This Sends Up To The Parent` appears only when the
  contract declares a `Parent`.
- In a phase file, `## Before Starting This Phase` is omitted for the
  roadmap's first phase, which has no predecessor.
- A phase file may gain `## Risk & Mitigation`, `## Testing Strategy`, or
  `## Implementation Notes` after `## Acceptance Criteria`, each only when it
  has content. The template does not carry them.

## Task Granularity

Each task is 1 to 4 hours of work, written as a checkbox — `- [ ] ` — and
grouped under a category heading. Be specific about the unit of work, not the
area it touches.

Good:
- `- [ ] Implement login endpoint with JWT validation`
- `- [ ] Add password hashing with a salted, secure algorithm`

Bad:
- `- [ ] Fix auth`
- `- [ ] Backend stuff`

A phase file that grows past 700 lines is split into sub-phases rather than
left to grow further.

## Adding A Phase To An Existing Roadmap

1. Number the new phase after the roadmap's last phase.
2. Create the new phase file from `assets/templates/phase.md` and write it
   into the roadmap's folder.
3. Add the phase to the README's phase list, status 🔴.
4. Recompute the totals and the progress bar from the current per-phase task
   counts — the Totals and Progress bar invariants in `SKILL.md` apply, and the
   pre-insertion total is wrong the moment the new file exists.
5. Add a changelog entry at the top per the Changelog invariant.
