---
name: tool-review
description: Review how the tools of my-claude-setup (its skills, agents and hooks) served in this session, and record the review in the my-claude-setup repository. Use only when a Stop hook of my-claude-setup asks for a tool review, when the user types /tool-review, or when the user asks in words for a review of this setup's tools. Never on its own initiative, never to review code, and never in a subagent.
---

# Reviewing this setup's tools

A session grading itself gives itself a good mark. So a review is not an account of how
well things went: the scripts measure, and the measures set what the review must explain.
Numbers come from the scripts and are never written by hand.

## The procedure

`<base>` below is the absolute path given above as "Base directory for this skill". Use it
as printed: the permission rules name that path, and `~` or `$HOME` would prompt.

1. Run `python3 -B <base>/scripts/measure.py`. It prints the review's path, the draft's
   path, the tools under review, what the review must explain, and the `measured` block.
2. Write your part to the draft with the Write tool, in the shape below.
3. Run `python3 -B <base>/scripts/record.py <draft>`. It checks the draft, writes the
   review with its `measured` block, and deletes the draft. When it lists problems, fix
   the draft and run it again.
4. Tell the user in one line where the review is, then list each `high` finding in one
   line.

Budget: two commands and one Write. Read `references/format.md` only when the shape below
is not enough. No subagent, no other read, and no fix: a review proposes, it never
repairs. Prose of 300 words at most.

## Your part

A JSON object, then a line holding only `---`, then the prose:

    {
      "task": "what the user asked, in their own words and language",
      "outcome": "delivered",
      "corrections": 0,
      "tools": {"skill:roadmap": "what the tool brought, in one sentence"},
      "findings": [
        {"kind": "noise", "severity": "medium",
         "target": "domains/roadmap/hooks/session_resume.py",
         "fix": "what the target should say or do instead",
         "note": "one sentence of evidence"}
      ]
    }
    ---
    The prose, in English: what the costs bought, each point measure.py asked to
    explain, the corrections. No section on what went well.

- `outcome` is `delivered`, `partial` or `abandoned`: what the user ended up with.
- `corrections` counts the times the user corrected, redirected or rejected something.
- `tools` names exactly the tools measure.py listed. "Nothing" is a valid answer, and
  calls for a finding.
- A finding needs a `target`, a file of the my-claude-setup repository relative to its
  root, and a `fix`. Without both it is a complaint: put it in the prose. `findings: []`
  is a claim, not a default.
- `kind` is one of `skill-gap`, `skill-drift`, `trigger`, `tooling-gap`, `noise`,
  `waste`, `defect`, `unverified`, defined in `references/format.md`; `severity` is
  `low`, `medium` or `high`.
- Everything is in English except `task`.

## The scripts

`scripts/measure.py` and `scripts/record.py` are the two commands. They share
`scripts/transcript.py`, which reads the session's transcript (which tools of ours served,
and what the slice cost), and `scripts/reviewfile.py`, which reads and writes review
files. The review domain's Stop hook uses both too.

## What this skill never does

- Fix a tool, or change a file of my-claude-setup other than through `record.py`.
- Review code, a document, or the project the session works on.
- Run in a subagent, or on its own initiative.
