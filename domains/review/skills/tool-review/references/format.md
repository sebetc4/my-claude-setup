# The review format

A review is one file under the my-claude-setup repository's `reviews/`, named
`YYYY-MM-DD-<session8>-<tool>.md`: YAML front matter, then prose. `record.py` writes it
from the draft; nobody writes it by hand.

## Who writes what

| Field | Written by | What it holds |
|---|---|---|
| `review` | scripts | Format version, `1`. |
| `status` | scripts | `requested`, then `complete`, or `skipped` when no review came. |
| `date`, `session`, `project` | scripts | The day of the request, the full session id, the session's working directory. |
| `trigger` | scripts | `hook` when the Stop hook asked, `manual` when the user did. |
| `slice` | scripts | `from` and `to`: the part of the session under review. |
| `closed` | scripts | When the review turn ended; the next slice starts there. |
| `tools` | both | `id`, `domain` and `version` by the scripts; `brought` by the session. |
| `task` | session | What was asked, in the user's words and language. |
| `outcome` | session | `delivered`, `partial` or `abandoned`. |
| `corrections` | session | How many times the user corrected, redirected or rejected something. |
| `measured` | scripts | Below. Never written or corrected by hand. |
| `findings` | session | Below. |

## The measured block

- `tokens`: `fresh` (input plus cache creation), `cache_read` and `output` of the main
  context, counted once per API message.
- `turns`: API calls. `tools`: calls by tool name.
- `friction`: `tool_errors` and `interruptions`.
- `setup`, one entry per tool under review:
  - a skill: `loads`, the `chars` its loads injected, `files_read` among its own files,
    `scripts` run, `script_errors`;
  - an agent: `runs`, one entry each, with `fresh`, `cache_read` and `seconds`;
  - a hook: `runs` with an effect, `injected_chars`, `blocks`, `errors`.
- `derived`: `active_minutes` and `context_peak`, each with the `rule` that made it.

A measure missing from the block could not be read; a zero was counted and found none.

## Findings

`kind`, `severity`, `target` and `fix` are required; `note` is one sentence of evidence.
`target` is the file of the my-claude-setup repository that would change, relative to its
root; `fix` says what it would say or do instead.

| `kind` | What it names | Example |
|---|---|---|
| `skill-gap` | The instructions of a skill or an agent were followed and did not say what the session needed. | The closing ritual never says to move the folder with `git mv`; the move read as a deletion. |
| `skill-drift` | The session departed from an instruction for a sound reason: the instruction is wrong. | The report template asks for a section the phase cannot have, and the session left it out. |
| `trigger` | A tool loaded without need, or a job done without the tool that covers it. The target is the `SKILL.md` or agent file whose description fired, or failed to. | `roadmap` loaded on a question about a changelog. |
| `tooling-gap` | A missing check or script that would have caught the problem earlier. | Nothing checks that a phase's start commit exists. |
| `noise` | A tool injected, reported or blocked something useless or wrong. | `session_resume.py` injected a whole phase and its Work Log into a conversation about a PDF. |
| `waste` | Cost paid for nothing, where a cheaper path existed. | The auditor re-read every phase to check one. |
| `defect` | A tool malfunctioned: a script error, a hook firing wrongly, a wrong agent verdict. | `progress.py` failed on a phase title holding a colon. |
| `unverified` | Something delivered resting on an assumption nobody checked. | The phase was closed on tests that were never run. |

Severity is the finding's, never the session's:

- `high`: it cost real tokens or shipped something wrong, and it will happen again on the
  next task of this kind.
- `medium`: real, recurring, cheap each time.
- `low`: worth recording, so that recurrence can promote it.

## A complete review

    ---
    review: 1
    status: complete
    date: "2026-09-26"
    session: aabb0fa1-f563-4ec2-8228-00c695fa7a0c
    project: "/code/claude/scriptorium"
    trigger: hook
    slice:
      from: "2026-09-26T21:42:11.000Z"
      to: "2026-09-26T21:46:03.395Z"
    closed: "2026-09-26T21:48:10.120Z"
    tools:
      - id: hook:roadmap/session_resume.py
        domain: roadmap
        version: "1.1.1"
        brought: >-
          Nothing: the conversation was about a PDF; the injected phase was never used.
    task: "can we pick up the guide's layout again?"
    outcome: delivered
    corrections: 0
    measured:
      tokens: {fresh: 33979, cache_read: 412727, output: 5445}
      turns: 9
      tools: {Bash: 6, Read: 2}
      friction: {tool_errors: 0, interruptions: 0}
      setup:
        hook:roadmap/session_resume.py: {runs: 1, injected_chars: 3912, blocks: 0, errors: 0}
      derived:
        active_minutes:
          value: 4
          rule: "wall clock minus every gap over 5 min"
        context_peak:
          value: 57062
          rule: "largest input of one API call, fresh and cached"
    findings:
      - kind: noise
        severity: medium
        target: domains/roadmap/hooks/session_resume.py
        fix: >-
          Inject one line (roadmap, open phase, file path) instead of the phase and its Work
          Log.
        note: >-
          Phase 4 and its whole Work Log were injected into a conversation about a PDF, and
          re-read at every exchange.
    ---

    The hook's 3,912 characters were the only cost of ours in this slice. The conversation
    was about a PDF's layout; nothing in it read the roadmap again.
