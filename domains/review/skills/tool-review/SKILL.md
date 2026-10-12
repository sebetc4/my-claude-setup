---
name: tool-review
description: Review how the tools of my-agent-setup (its skills, agents and hooks) served in this session, and record the review in the my-agent-setup repository. Use only when a Stop hook of my-agent-setup asks for a tool review, when the user types /tool-review, or when the user asks in words for a review of this setup's tools. Never on its own initiative, never to review code, and never in a subagent.
---

# Reviewing this setup's tools

A session grading itself gives itself a good mark. So a review is not an account of how
well things went: the scripts measure, and the measures set what the review must explain.
Numbers come from the scripts and are never written by hand.

## The procedure

`<base>` below is the absolute path given above as "Base directory for this skill". Use it
as printed: the allow rules name that path (my-agent-setup
`domains/review/permissions.json`), and a rule matches the whole command, so `~` or
`$HOME` would prompt (Claude Code permissions § Bash). The two scripts are commands: run
them as written, with no interpreter in front, since a project hook may refuse `python3`
in a command (my-agent-setup `CLAUDE.md`, Gotchas) and the rules name the script itself.

1. Run `<base>/scripts/measure.py`. It prints the review's path, the draft's path, the
   tools under review, what the review must explain, and the `measured` block.
2. Write your part to the draft with the Write tool, in the shape below.
3. Run `<base>/scripts/record.py <draft>`. It checks the draft, writes the review with its
   `measured` block, and deletes the draft. When it lists problems, fix the draft and run
   it again.
4. Say nothing about the review to the user, nor about its findings: the conversation it
   interrupted goes on, and `make reviews` in my-agent-setup reads them. End the turn by
   repeating, word for word, the question or next step your message before the
   review ended with; if it ended with neither, end the turn without text.

Budget: two commands and one Write, and no message to the user while the review runs: the
tool calls are enough. Read `references/format.md` only when the shape below is not
enough. No subagent, no other read, and no fix: a review proposes, it never repairs, and
changes no file of my-agent-setup but through `record.py`.
Prose of 300 words at most.

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
- A finding needs a `target`, a file of the my-agent-setup repository relative to its
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
