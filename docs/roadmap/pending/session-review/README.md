# Roadmap: session-review

---

## Status Indicators

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Done
- ⏸️ Blocked
- ⚠️ Needs Review

---

## Overall Progress

```
Phase 0  Framing                    🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/4)
Phase 1  Standard Skill             🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
Phase 2  Adoption And Release       🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/5)
TOTAL                                  ░░░░░░░░░░░░░░░░░░░░   0%  (0/14)
```

**Current Phase:** —
**Blocked By:** —
**Next Milestone:** Phase 0 — Framing

---

## Why This Roadmap Exists

`session-review` was built in scriptorium, by a roadmap of four phases closed on
2026-09-18. Run by hand once a task is finished, it reviews what the task cost and what
should change in the repository's own tools, so that the next task of the same kind
costs less. It measures the task's slice of the transcript, sets each measure beside the
median of earlier reviews of the same skill, and prints the obligations the review must
meet. A SessionStart hook keeps a ledger of every session, reviewed or not, and
`aggregate.py` reads the reviews as a corpus.

This setup's review domain grew from it: `tool-review` reviews the tools this setup
installs, from any project, when a Stop hook asks. The two tools share an aim, reviewing
tools, and differ in their input: a repository's own tools, or this setup's. Yet
`session-review` works in scriptorium only, tied to its `.venv`, its `core.doc` import,
the list of skills written in `corpus.py`, its measure of PDF page images and its
`reviews/` path.

This roadmap makes it a standard tool of this setup:
- any repository reviews the tools it builds for itself, a task at a time;
- its settings are the repository's own, in `.agent-conventions.toml`;
- it shares with `tool-review` what both need, and moves forward with the findings of
  the tool reviews;
- scriptorium runs the installed version, its reviews still read.

---

## Decisions Taken At Opening

Taken with the user on 2026-10-11:

- `session-review` comes into this repository as a standard tool, to review the tools
  any repository builds for itself. Its aim is that of `tool-review`, a review of tools;
  its input differs.
- It is run by hand, at the end of a task.
- It uses the transcript reader of roadmap `token-usage` rather than a second one.

---

## Deliberately Out Of Scope

- The cost reader and the review of several sessions: roadmap `token-usage`.
- Changing `tool-review` beyond what the two tools share.
- Reviewing code or documents: `code-review` and each repository's own reviewers.
- How long the transcripts are kept: roadmap `token-usage` sets `cleanupPeriodDays`.

---

## Phases

| # | Phase | Tasks | Status |
|---|---|---|---|
| 0 | [Framing](phase-0-framing.md) | 4 | 🔴 Not Started |
| 1 | [Standard Skill](phase-1-standard-skill.md) | 5 | 🔴 Not Started |
| 2 | [Adoption And Release](phase-2-adoption-and-release.md) | 5 | 🔴 Not Started |

---

## Dependencies

- Roadmap `token-usage`: the transcript reader its Phase 1 extends, which Phase 1 of
  this roadmap uses.

---

## Related Documentation

- [Skill audit rules, 2026-10-03](../../../decisions/2026-10-03-skill-audit-rules.md) — `session-review`'s description, which a strict YAML reader rejects.

---

## Metadata

**Roadmap Status:** 🔴 Not Started
**Location:** `docs/roadmap/pending/session-review/`
**Version:** 1.0.0
**Created:** 2026-10-11
**Last Updated:** 2026-10-11

---

## Changelog

### 1.0.0 (2026-10-11)

- Roadmap created with three phases: Phase 0 Framing, Phase 1 Standard Skill, Phase 2
  Adoption And Release. Phase 1 waits for Phase 1 of roadmap `token-usage`, whose reader
  it uses. Each task declares its proof, approved by the user.
