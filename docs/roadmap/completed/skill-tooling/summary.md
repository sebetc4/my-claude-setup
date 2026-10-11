# Summary — skill-tooling

---

## Where We Started

On 2026-09-28, skills were written and checked with two external tools that overlapped
and contradicted each other. `superpowers:writing-skills` 6.4.1 brought a method, watching
an agent fail before writing, and no tooling. The skill-creator plugin brought tooling,
evals with and without the skill, grading, benchmark, review viewer and description
tuning, and thinner writing guidance. Neither audited an existing skill, neither followed
its own rules, and both drifted from the official documentation. The only automated
audit, `tests/skills.py`, ran on `domains/` alone and read frontmatter with PyYAML. Each
repository's contract with the roadmap skill sat in its `CLAUDE.md`, loaded into every
session.

The roadmap set out to replace both tools with one of this setup's own, which creates,
edits, audits and evaluates skills in any repository and takes each repository's
conventions from a file at its root.

---

## Where We Landed

On 2026-10-11, the domain `skill-tooling` 0.1.0 is installed and tagged
`skill-tooling-v0.1.0`:
- the skill `authoring-skills` creates, edits, audits and evaluates skills. Its
  `SKILL.md` of 54 lines routes to a writing guide, a create-and-edit procedure, a
  reference for skills that enforce a rule, the audit, the evaluation procedure and the
  eval files' schemas, with one template per kind of skill;
- `audit.py` checks the 46 rules of `docs/decisions/2026-10-03-skill-audit-rules.md`, and
  a hook runs it at each edit of a skill, in any project;
- eight eval scripts prepare iterations, start runs as isolated `claude -p` sessions,
  grade, benchmark, show a review page, measure trigger rates, tune a description and
  compare two versions blind. Each announces its sessions' count and cost and starts none
  without `--start`;
- three agents: `skill-auditor` judges what no static rule can, `skill-grader` grades a
  run, `skill-comparator` compares two outputs blind.

Three shared modules serve these tools. `shared/conventions/` reads and writes
`.agent-conventions.toml`, which this repository, scriptorium and forma-rust carry.
`shared/frontmatter/` is a strict YAML subset, so no Python file imports PyYAML any more.
`shared/usage/` counts a session's tokens and cost from its transcript, to the cent.
The roadmap skill, now 2.0.2, reads its contract from the conventions file, and its
evals run on the new scripts.

On three skill-writing cases, `authoring-skills` scored 87% against 53% for no skill,
60% for `writing-skills` and 49% for skill-creator, or 83% against 63%, 71% and 58%
without the audit assertions only it could pass. Its description triggers on 12 of 12
queries the old tools answered and on none of 12 near misses. Every plugin is
uninstalled, and `docs/decisions/2026-10-11-skill-tooling-switch-over.md` closes the
matter of the old tools. The tool reviews now watch it in real use.

---

## What Each Phase Delivered

- **Phase 0 Framing.** The decision record `docs/decisions/2026-09-28-skill-tooling.md`:
  68 capabilities of both sources ruled keep, improve or drop, and five rules settled:
  description, tone, testing, sizes and scripts. It also chose the names and added the
  Apache 2.0 `LICENSE` and `docs/claude-code-coupling.md`. The user set this
  repository's principles: checks raise alerts, the documentation informs without
  capping, tools address the agent. Probes showed that `allowed-tools` grants nothing in
  a headless run and that `skillOverrides` cannot hide a plugin skill. Both old tools
  were turned off at the start, so the new one was built and tested without them.
- **Phase 1 Agent Conventions.** `.agent-conventions.toml`, with its reader and writer
  in `shared/conventions/`, 51 tests, the procedure that fills or fixes the file, and
  `tools/shared.py`, which keeps each skill's copy equal to its source. Roadmap 2.0.0
  read its contract there. The session hook went from a Work Log excerpt to one
  conditional line. At the user's request, sub-roadmaps and parent roadmaps were dropped.
- **Phase 2 Static Audit.** The rule catalogue and `audit.py`, each of the 46 rules with
  its own test watched failing first, and the audit hook. A probe chose the parser:
  Claude Code's reads frontmatter that YAML rejects, and `claude plugin validate` checks
  no field name or value. `tests/skills.py` became a client of the audit, and the dev
  hook gave one line per failing test instead of whole tracebacks.
- **Phase 3 Writing Method.** `authoring-skills`'s create, edit and audit operations,
  designed from 13 failures watched in three realistic tasks run without the skill. With
  it, none of the 13 came back, nor the four the user added, in 31, 51 and 37 API calls
  against 48, 107 and 87. It also delivered `skill-auditor`, the rule that every fact
  names its source, `docs/conventions/` on the conventions agents share, and
  `docs/claude-code-builtins.md`. Every plugin was uninstalled with its cache.
- **Phase 4 Evaluation Tooling.** The evaluate operation: the scripts, `skill-grader`,
  `skill-comparator`, the review page adapted from skill-creator, and `shared/usage/`.
  A sample skill ran end to end at 100% against 28%. The reference turned a request to
  evaluate an edit from an audit into a prepared and announced iteration, 6/6 in three
  runs against 1/6. The runs' effort was set to `xhigh`: `max` led by one assertion a
  task for 2.4 times the cost.
- **Phase 5 Switch-Over.** The four-arm comparison in 36 runs, the trigger queries, and
  the matrix checked: 51 rows built as ruled, 10 dropped, 6 built otherwise, W18 dropped
  until a run calls for it. `skill-auditor` audited `roadmap`, `tool-review` and
  `authoring-skills`, and roadmap 2.0.2 was proven against 2.0.1. The roadmap evals
  moved onto the new scripts, and the domain was installed and released. Each tool
  gained points to watch in its reviews, and `tools/reviews.py` now tells a version no
  session used from one whose findings are gone.

---

## What We Learned

- **Probe the harness before building on it.** Seven premises fell to probes that cost
  cents: `allowed-tools`, `skillOverrides`, `disableAllHooks` dropping the hooks
  `--settings` adds, an installed copy shadowing the one under test, an agent's `effort`
  ignored under `--agent`, an older `claude` mapping `sonnet` to an older model, and auto
  memory left on. Four of them overturned Phase 4's approved design, and one a note read
  from the binary, where the documentation was right.
- **Watch the failure before writing the guidance.** The baseline's 13 failures shaped
  the design, and four behaviors the user ruled failures came from runs, not from
  expectation. A proof that stops a run early hides what comes after: the first "gone"
  of B1 owed to a step eval that stopped at `SKILL.md`, and the full runs found it again.
- **When a run fails an assertion, read the assertion first.** "SKILL.md is short"
  failed five runs within the writing guide's budget: a word with no measure. An
  assertion carries the measure the rule gives. An assertion that one arm alone can pass,
  such as the audit, is reported with and without it, or it decides the comparison.
- **An agent's verdict is a sample.** `skill-auditor` reported one, three, then four
  problems on a file left unchanged. Three runs make a verdict, and a problem raised by
  one run of three is not kept. When a fixture fails, asking the run why found the
  fixture's own fault: a source that covered the planted fact.
- **Cost comes from the transcript, counted per message.** The Agent tool's
  `total_tokens` is the last context's size, not the consumption. A subagent's transcript
  lacks its final output tokens, and cache writes are priced by their lifetime. A main
  thread at `max` with a context of 631,000 tokens took half of Phase 3's $176. Phase 4's
  shorter sessions at `xhigh` read less cache a call but made more calls, and cost as
  much.
- **A guard refuses access, not words.** The first guard refused any call naming
  `~/.claude`, and so refused the text this repository's skills must write, which biased
  the runs. It is a tripwire, not a sandbox: a script that builds the path passes it.
- **Paid automation needs a stop between runs, and small batches near a limit.** The
  subscription's limit stopped runs in Phases 3, 4 and 5, and a run started from the
  editor died with its window. In Phases 4 and 5, about $30 went to runs lost that way
  or made under the first guard. Each script announces before it starts, `run.py
  --stop` lets the running sessions end, and each paid step waits for its own yes.
- **A measure that cannot fail tells nothing.** The 24 trigger queries could not tell two
  descriptions apart: every query that should trigger names a skill, and only one skill
  writes skills. An eval's preamble is part of its conditions: "assume rather than ask"
  overrode a skill's stop in one run of six.

---

## What We Are Leaving Open

- **The real-use period.** `tools.json` gives `authoring-skills` three points to watch:
  a convention the model knows explained, a step without its check, and a guard weighed
  after the skill. Each comes with its condition to revisit in the 2026-10-11 record, and
  all three leave after ten reviews that raise none.
- **The other repositories.** Neither scriptorium nor forma-rust has a `[skills]` table,
  and scriptorium held 85 audit errors on 2026-10-04, which the installed hook reports
  at each edit of a skill there. Each
  conforms later, guided by the user, scriptorium first. forma-rust's file still declares
  `sub_roadmaps`, which the reader refuses since Phase 1: its roadmaps move under `root`
  from a session in that repository.
- **The eval tooling's gaps,** listed in the 2026-10-11 record. `run.py`'s estimate
  mixes a skill's cases, and it does not refuse a second `--start` on a running
  iteration. The guard refuses Python heredocs that name `~/.claude` and trial installs
  into `mktemp -d`. A `triggers.py` session can pass its ceiling by half, and `grade.py`
  announces graders the skill's own script makes needless.
- **What the comparison did not measure.** The old tools' test loops, and
  `authoring-skills`'s fourth case, which starts `skill-auditor`, wait for runs allowed
  the Agent tool.
- **Assertions to revise:** assertion 4 of `task-release-domain`, to split at the next
  run of the evals, and assertion 7 of `read-the-results`, which asks more than the
  reference.
- **Rulings kept without an eval:** `roadmap`'s "Not for …" exclusion until a trigger
  measure of `roadmap`, and `tool-review`'s T1 and T4, that skill having no evals.
  Phase 1's fill-or-fix conversation, where the agent can ask the user, has no eval
  either.
- **Outside this roadmap:** the review domain's `measure.py:94` and `record.py:125` still
  tell the agent to run `make update D=review`, and its `transcript.py` reads output
  tokens the transcripts do not hold; roadmap `token-usage` takes on both. Moving this
  repository's instructions to `AGENTS.md`, or installing into `.agents/skills/`, is not
  decided.
