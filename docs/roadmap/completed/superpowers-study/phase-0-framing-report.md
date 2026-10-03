# Phase 0 Report: Framing

**Phase:** [phase-0-framing.md](phase-0-framing.md)
**Start Commit:** 39b1374

---

## Work Log

### 2026-10-01

Opened the phase, the roadmap's first: no previous phase to read, no pending
restructuring to settle, and no other phase of the roadmap in progress. Read the
README and the phase file before starting. The working tree already held two
uncommitted changes when the phase opened, both outside its work: `.gitignore`
swaps `/pending/` for `/study/`, and `skill-tooling/phase-2-static-audit.md`
carries a stray edit in its While Working line.

At the user's word, reverted the stray edit: `skill-tooling/phase-2-static-audit.md`
matches `HEAD` again. The `.gitignore` change stays the user's.

Read the 2026-09-18 audit, the 2026-09-28 skill-tooling record for its matrix, and
Phases 1 to 4, to know what this phase prepares for each.

The copy matches the installed 6.4.1 (`diff -rq`, 231 files). Measuring the skills, the
sizes did not match the audit's — `executing-plans` about 5,100 tokens against 576.
6.3.0 is on disk too, and its sizes are exactly the audit's: the baseline measured 6.3.0,
and the 6.4.1 cache only appeared on 2026-09-24. `installed_plugins.json` shows 6.3.0
still local to pdf-creator and my-claude.

Read the six skills of the chain whole, then `using-superpowers` and
`diagnosing-superpowers`; for the other six, their headings and every line that names a
skill or a file. Two reviewer prompts are cited by no file — their callers went in 5.0.6,
per the release notes — and five files of `systematic-debugging` are cited nowhere.
Searched the conventions and the mentions of Claude: the prose is already
harness-neutral, and the tie to Claude Code is the vocabulary, which
`claude-code-tools.md` declares.

For the recount, read the transcripts' fields rather than assume them. Subagent
transcripts sit under `<session>/subagents/`, outside the baseline's glob. Every call to
the plugin carries the `superpowers:` prefix. The "Base directory for this skill" line
names the version of each load, and its 6.3.0 lines give exactly the baseline's 51 calls,
skill by skill: the method reproduces the baseline. The same check showed figures for
6.4.1, left to Phase 4. `attributionSkill`, on assistant messages that carry `usage`,
could measure the cost per skill once its coverage is established.

Found that Claude Code deletes transcripts after `cleanupPeriodDays`, 30 days by
default, and that the user settings leave it unset (docs § Cleaned up automatically,
fetched today): the oldest transcript starts on 2026-08-31, and the baseline period's go
from about 2026-10-04.

Counting sessions per period gave 475 from 2026-09-04 to 2026-09-18 against 51 since —
a drop that turned out to be eval runs: 432 short transcripts under temporary folders and
the home folder. The entry point does not tell them apart, every one being
`claude-vscode`; `origin.kind` `human` does, checked on the seven transcripts outside
those folders that lack it: five stubs and two runs, a probe and a skill-creator
description run. As the baseline period's transcripts go within days, measured the
baseline by working sessions now: 41 sessions, 17 of them (41 %) with a superpowers call,
32 (78 %) with a call to any skill. The audit's 8 % counted the runs.

Wrote the draft record `docs/decisions/2026-10-01-superpowers-study.md` — inventory,
hand-overs, conventions, ties to Claude Code, notes for later phases, the matrix format
and the recount method — and ticked the five tasks. Asked the user about retention.

The user chose to leave `cleanupPeriodDays` unset and to run the roadmap without waiting
for 2026-10-18. Checked what that leaves at risk. The recount's window survives until
about 2026-10-19, and the baseline by working sessions is already measured. But the 23
sessions where the plugin served, 17 of them before 2026-09-19, are also the only
observed evidence of how its skills worked, and they go from about 2026-10-10. Checked
too when the plugin went off in this repository: an edit of `.claude/settings.local.json`
on 2026-09-28 at 18:30 UTC, a day after its last call there; the record's rule now names
that time. Added the two deadlines to Phases 1 and 4.

---

## Decisions

- **The matrix adds a `Goes to` column to the 2026-09-28 format.** Phase 1's mapping and
  Phase 4's target architecture need each kept capability's destination. Phases 1 to 3
  fill it, `open` until their mapping decides, and Phase 4 builds the architecture from
  it.
- **Row ids carry a two-letter prefix per skill:** BR, WP, EP, SD, DP, TD, VC, SY, RQ, RC,
  GW, FB, US, DS, and HK for the hook. One letter would collide across fifteen sources.
  Later phases number their rows under these prefixes.
- **Five rules of evidence:** every reason cites evidence; the documentation and this
  repository's checks weigh, never bind; a claim about what an agent does says whether it
  was observed or reasoned; usage never justifies a verdict alone; the rules settled on
  2026-09-28 are cited, not ruled again. They bind every verdict of Phases 1 to 3.
- **The recount counts working sessions:** those with a message of `origin.kind` `human`.
  In the baseline period, 434 of 475 transcripts were runs or stubs. Phase 4 compares with
  the baseline by working sessions measured today, not with the 8 % of 2026-09-18.
- **The baseline by working sessions was measured in this phase,** ahead of Phase 4's
  recount, because its transcripts go from about 2026-10-04: read-only commands, no tool
  changed.
- **The record is named `2026-10-01-superpowers-study.md`,** the study's opening date, as
  skill-tooling's record carries the date of its Phase 0.
- **`cleanupPeriodDays` stays unset** (the user, 2026-10-01): the roadmap runs without
  waiting for 2026-10-18. Phase 4 recounts by 2026-10-18 at the latest, and Phase 1 reads
  before about 2026-10-10 the plugin sessions its verdicts cite.

---

## Files Changed

**Added**
- `docs/decisions/2026-10-01-superpowers-study.md`
- `docs/roadmap/on-progress/superpowers-study/phase-0-framing-report.md`

**Modified**
- `.gitignore` — the user's change, uncommitted when the phase opened: `/study/`, where
  the plugin's copies now live, replaces `/pending/`

**Renamed**
- `docs/roadmap/pending/superpowers-study/README.md` → `docs/roadmap/on-progress/superpowers-study/README.md` — also modified
- `docs/roadmap/pending/superpowers-study/phase-0-framing.md` → `docs/roadmap/on-progress/superpowers-study/phase-0-framing.md` — also modified
- `docs/roadmap/pending/superpowers-study/phase-1-design-and-planning.md` → `docs/roadmap/on-progress/superpowers-study/phase-1-design-and-planning.md` — also modified
- `docs/roadmap/pending/superpowers-study/phase-2-proof.md` → `docs/roadmap/on-progress/superpowers-study/phase-2-proof.md`
- `docs/roadmap/pending/superpowers-study/phase-3-git.md` → `docs/roadmap/on-progress/superpowers-study/phase-3-git.md`
- `docs/roadmap/pending/superpowers-study/phase-4-decisions.md` → `docs/roadmap/on-progress/superpowers-study/phase-4-decisions.md` — also modified

Outside the diff: the revert of the stray edit in `skill-tooling/phase-2-static-audit.md`
leaves that file as committed; the agent's memory, outside the repository, gained a note
on transcripts, and its note on the 2026-10-18 recount was brought up to date.

---

## Problems And Deviations

- **The baseline measured 6.3.0, while the study reads 6.4.1.** The cost of a call changed
  with the version, `executing-plans` ninefold. The recount gives cost per version, as
  the method now says.
- **The baseline's session figures counted eval runs.** Its 479 sessions and its 8 % rest
  mostly on runs. Fixed for the comparison: the method counts working sessions, and the
  draft record holds the baseline by working sessions.
- **Transcript retention threatens the recount.** Unless `cleanupPeriodDays` changes, the
  baseline period's transcripts go from about 2026-10-04, and the window's first day
  about 2026-10-19. Settled by the user on 2026-10-01: the setting stays, and the roadmap
  runs ahead of the deadline, which went to Phases 1 and 4.
- **The recount task done more broadly than written.** It named Skill calls in
  `*/*.jsonl` from 2026-09-18; the method keeps that count, and adds runs left out of the
  session counts, subagent calls and refused calls counted apart, the version of each
  call, and a window opening on 2026-09-19, since the baseline's 51 calls are all before.

---

## Changes To Later Phases

- `phase-1-design-and-planning.md`: added a constraint — a verdict that cites one of the
  17 working sessions where the plugin served before 2026-09-19 reads it before about
  2026-10-10, when they start going.
- `phase-4-decisions.md`: added a constraint — the recount runs by 2026-10-18 at the
  latest, since its window opens on 2026-09-19 and transcripts older than 30 days go.

---

## Assessment

The phase delivered what Phases 1 to 4 need, in the draft record
`docs/decisions/2026-10-01-superpowers-study.md`: an inventory of superpowers 6.4.1 —
fifteen skills with their companion files, the prompts, the hook, the scripts, the tests —
with the chain of hand-overs, the conventions the plugin imposes and its ties to Claude
Code; and a method — the 2026-09-28 matrix with a `Goes to` column and a prefix per
skill, five rules of evidence, and a recount by working sessions.

Two premises of the roadmap did not hold. The 2026-09-18 baseline measured 6.3.0, not the
6.4.1 the study reads, and its session figures counted eval runs: the comparison now
rests on a baseline by working sessions, measured in this phase. And the evidence is
perishable — transcripts go after 30 days — which the user chose to outrun rather than
extend.

What Phase 1 needs to know first: its family moves as one block, since `executing-plans`
runs `subagent-driven-development`'s scripts and both executors read
`requesting-code-review`'s `code-reviewer.md`; the 17 working sessions where the plugin
served before 2026-09-19, mostly on this family, go from about 2026-10-10, so the ones a
verdict cites are read first; and its two mapping tasks wait for the user's approval.
