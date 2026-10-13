# Phase 2: Reviews And Reports

---

## Status

**Current Status:** 🟡 In Progress (36% — 4/11)
**Started:** 2026-10-12
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## Before Starting This Phase

Read `phase-1-usage-reader.md` and `phase-1-usage-reader-report.md` in full before
touching anything here: the decisions already taken, the problems and
deviations recorded, and the changes made to this phase.

---

## While Working

Keep `phase-2-reviews-and-reports-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Put the figures where they lead to a conclusion:
- each tool review's measured block, the tool's cost beside what it brought;
- `make reviews`, each tool's cost and the tools it flags, and the reviews processed and
  archived;
- the tools reviewed chosen by a list, and a review's own cost kept within a budget;
- `reviewing-token-usage`, a skill of the review domain, run by hand, that reviews
  several sessions, a phase, a roadmap or a stretch of work, and has the agent conclude
  on what served, what did harm and how to go on after a stop, and records its figures
  and conclusions so that a longer window reads them.

Fix the domain's four open defects along the way.

---

## Overview

### Why This Phase Matters
A review judges how a tool worked: with its cost beside it, the judgment weighs what the
tool costs against what it brings. The review of several sessions does with a tool what
the three counts by hand did, ending in what to change.

### What It Enables
Decisions on effort, sessions and eval runs that rest on measures taken as the work
happens, rather than on a one-off analysis.

### Out of Scope
A phase closure that starts the review of several sessions or writes a phase's cost into
its report: the roadmap and review domains stay independent (the user, 2026-10-11).

---

## Tasks

### Reviews
- [x] Test and implement the measured block the design chose: the slice's calls and cost per model and effort, main thread and subagents apart, every subagent included, estimates marked, beside the token counts it carries today; each tool's own cost, derived and marked, printed by `measure.py` beside its median with an explanation owed past 1.5 times; `served` in the draft, checked by `record.py`; the review's own turn, written by the Stop hook when it closes the turn; no cache rebuild
  Proof: test — `measure.py` on a fixture session with two subagents at two efforts and fixture reviews of its tools prints the block, each tool's cost and its ratio; `record.py` refuses a draft without `served`; the Stop hook writes the review's own turn up to the call after `record.py`; red before the change
- [x] Test and implement the tools reviewed by choice: the Stop hook reads the `[review]` table of the setup repository's `.agent-conventions.toml` by its path, each entry a tool id or a domain, and asks for no review when the table is missing or empty; `tools.json` keeps only the points to watch
  Proof: test — a fixture repository whose table names a domain and an agent: the hook asks for those tools only; without the table, for none; red before the change
- [x] Test and implement the saturation: the Stop hook leaves out a tool version holding ten complete reviews not archived whose last five raised no kind and target the earlier ones had not, and asks for no review when every tool used is left out
  Proof: test — fixture reviews: a saturated version left out, its next version asked for again, and the archive starting the count again; red before the change
- [x] Test and implement `tools/reviews.py --archive`, which moves the reviews it read into `reviews/archive/<date>/`: the findings and the saturation count only the reviews not archived, the medians of cost read the archive too
  Proof: test — fixture reviews archived leave the findings and the saturation count and stay in the medians; red before the change
- [ ] Test and implement `make reviews` reporting each tool's median cost in dollars over its current version beside its current measures, flagging the tools the design names, one whose current version costs past 1.5 times its earlier versions and one whose reviews say `served: none` in a third of them, each from three reviews; the reviews' own median and total cost against their budget; the windows recorded; the reviews waiting since the last archive; the `[review]` table missing, empty or invalid, with its problems; and the proposals on the list of tools reviewed
  Proof: test — `tools/reviews.py` on fixture reviews with known costs prints each tool's median in dollars, flags the two fixture tools built to be flagged, flags the reviews past their budget and proposes the fixture tool built to be dropped, red before the change

### Review Of Several Sessions
- [ ] Test and implement the script of `reviewing-token-usage`, on the copies of `shared/usage/`, `shared/sessions/` and `shared/reviewfile/` that `make shared` keeps: a window given by `--from` and `--to`, commits or times, through `sessions.window()`, with `--repo` and `--exclude`; the cost per model and effort, split into main thread, subagents, `claude -p` sessions by kind of folder and tool reviews, estimates marked; each session's opening, peak, cost, break-even and commits; the three ways of going on after a stop compared; the flags the design names; the comparison with earlier windows; the obligations; the record it writes under `reviews/windows/`, read by a longer window in place of transcripts past 30 days unless `--recount`, and its warning when a window starts before the oldest transcript kept
  Proof: test — a fixture repository and its transcripts, the window's totals computed by hand, each flagged pattern and each way of going on built into the fixture; a window made of recorded phases read from their records; a window older than the fixture's oldest transcript warned; red before the code
- [ ] Write the skill `reviewing-token-usage`, run by hand, that runs the script and draws the conclusions, with `authoring-skills`
  Proof: eval — a case on a fixture window whose conclusions are known, its assertions passing, and `audit.py` clean on the skill

### Defects
- [ ] Count the run of `session_resume.py` in a session it opened, the session starting at its earliest record, and a hook's run for each of its blocks and errors
  Proof: test — a fixture session that opens as `bbaa7e41` does, the hook's line dated before the first record: the measured block counts one run and its characters; a hook that blocks twice counts two runs and two blocks; red before the fix
- [ ] Count a skill's files read through a Bash `cat` or `sed` as through the Read tool
  Proof: test — a fixture session reading a reference with `cat`: `files_read` names it, red before the fix
- [ ] Replace the `make update` message of `measure.py` and `record.py` as the design settled
  Proof: test — a domain that does not know its repository: neither script tells the agent to run `make update`, red before the change
- [ ] Count each agent run's output tokens, estimated and marked as the reader does, beside its fresh and cached tokens
  Proof: test — a fixture subagent whose records keep the stream's first usage: its run carries an output estimate marked as such, red before the change

---

## Technical Details

### Files to Modify
```
domains/review/skills/tool-review/scripts/transcript.py
domains/review/skills/tool-review/scripts/measure.py
domains/review/skills/tool-review/scripts/record.py
domains/review/skills/tool-review/scripts/conventions.py   copy of shared/conventions, for the [review] table
domains/review/skills/tool-review/references/format.md
domains/review/hooks/review.py
domains/review/hooks/tools.json
domains/review/skills/reviewing-token-usage/          new, the review of several sessions
domains/review/permissions.json
tools/reviews.py
domains/review/tests/test_*.py
tests/test_reviews.py
docs/claude-code-coupling.md
```

### Dependencies
Phase 1: the extended reader.

### Constraints
Standard library only; test first. The Stop hook runs at every stop of every session:
whatever it gains is timed on a long transcript before it ships. It reads the `[review]`
table of the setup repository's `.agent-conventions.toml` by its path, never climbing
from the session's working directory. The reviews already
written keep their measured block as recorded; `make reviews` reads both shapes. The
review of several sessions is started by hand only. The transcripts stay at Claude
Code's 30 days (the user, 2026-10-11): a window is reviewed within that time, and a
longer one reads the records of the reviews it spans.

---

## Acceptance Criteria

- [ ] A review written in a session with subagents carries its cost in dollars per model
- [ ] The review of several sessions, run on a closed phase of this repository, gives its cost and its conclusions
- [ ] Each of the four defects has a passing test
- [ ] A tool the `[review]` table does not list is never asked for, and processed reviews
  are archived
