# Phase 0: Framing

---

## Status

**Current Status:** 🔴 Not Started (0% — 0/4)
**Started:** {{START_DATE}}
**Completed:** {{COMPLETION_DATE}}
**Blocked By:** —

---

## While Working

Keep `phase-0-framing-report.md` current as the work happens — after each significant
step, and before every commit, pause, or end of session.

---

## Objective

Settle, before any code, what of scriptorium's `session-review` is generic and what is
scriptorium's own, and how the standard skill is built: its domain and its name, its
settings, what it shares with `tool-review` and with the reader of roadmap
`token-usage`, what becomes of the ledger, and whether it counts tokens or dollars.

---

## Overview

### Why This Phase Matters
`tool-review` grew from `session-review`, and the two have drifted apart: two review
formats, eight kinds of finding against nine, two transcript readers. A port made
without that inventory would add a third of each.

### What It Enables
Phase 1 ports a design the user approved.

### Out of Scope
Code: it starts in Phase 1.

---

## Tasks

### Inputs
- [ ] Read scriptorium's `session-review` — `SKILL.md`, `references/format.md`, `references/findings.md`, `metrics.py`, `corpus.py`, `aggregate.py`, its tests and `session-ledger.sh` — and list each part as generic or scriptorium's own, with what a standard version needs in place of each part of the second kind
  Proof: review — the list, each item tied to a line of the code, approved by the user
- [ ] Compare it with the review domain's `tool-review`: the review format, the kinds of finding, the transcript reader, the obligations, the slice and its bounds, the findings carried to a roadmap; list what the two can share and what stays apart
  Proof: review — the comparison, each item tied to a line of the code of both, approved by the user

### Design
- [ ] Write the design and get the user's approval: the domain and the skill's name, checked against `docs/claude-code-builtins.md`; the settings read from `.agent-conventions.toml` through `shared/conventions/`; what is shared with `tool-review` and with the reader of roadmap `token-usage`, and how; the ledger kept, changed or dropped, the transcripts being deleted after Claude Code's 30 days; tokens or dollars; what scriptorium's reviews and ledger entries become
  Proof: review — the design, each part tied to the two lists, approved by the user before any code
- [ ] Write the decision record under `docs/decisions/`
  Proof: review — the record, approved by the user with its date

---

## Technical Details

### Files to Modify
```
docs/decisions/<date>-session-review.md    new
```

### Dependencies
None to start. The design of roadmap `token-usage`'s Phase 0, once approved, says what
its reader counts and how it is shared: the design here reads it if it exists.

### Constraints
No change to scriptorium nor to any domain in this phase. scriptorium's copy is read in
place, `.claude/skills/session-review/` of `/code/ai/scriptorium`, which matched
`study/session-review/` on 2026-10-11; scriptorium then held 7 reviews and 44 ledger
entries. Its tests run under pytest, with a `conftest.py`; this repository's tests use
`unittest` only. Its description holds `: ` in a plain scalar, which
`shared/frontmatter/` rejects (`docs/decisions/2026-10-03-skill-audit-rules.md`). The
review is run by hand, at the end of a task (the user, 2026-10-11).

---

## Acceptance Criteria

- [ ] The design is approved by the user
- [ ] The decision record is committed
