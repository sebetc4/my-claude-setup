# Skill tooling — 2026-09-28

Decision: **one tool of this repository — the skill `authoring-skills` with its agents —
replaces `superpowers:writing-skills` and the skill-creator plugin. It keeps, improves or
drops each of their capabilities as the matrix says, and follows the settled rules below.
Both sources are turned off from today.**

Recorded by Phase 0 of the skill-tooling roadmap, from the sources, the documentation and
the measures cited in each section.

## Principles

Set by the user on 2026-09-28, they govern every verdict and rule below:

- **Tools address the agent, never Claude.** The setup is meant to serve other agents
  later; only the install target — `~/.claude`, `settings.json`, the hooks format — stays
  Claude Code's for now.
- **This repository's check and test scripts raise alerts; they do not define the
  rules.** They were written from one of the two sources, and the new tool redefines the
  rules.
- **The official documentation informs; it does not cap.** A tool may go past a
  documented limit or recommendation when its evaluations show it does better.

## Sources

- `superpowers:writing-skills` 6.4.1 — local copy `pending/skill/writing-skills/`,
  identical to the installed `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/writing-skills/`.
  Cited below as **WS**.
- The skill-creator plugin, cache `fa59bc903774` — local copy `pending/skill/create-skill/`,
  identical to the installed one. Cited below as **SC**.
- Fetched as Markdown on 2026-09-28: the Claude Code skills page
  (https://code.claude.com/docs/en/skills, cited as **docs §** section), the Agent Skills
  specification (https://agentskills.io/specification, **spec §**) and the platform best
  practices (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices,
  **best practices §**).

Line numbers refer to each source's `SKILL.md` unless a file is named.

On 2026-09-28, at the user's request, both sources were taken out of the sessions so that
they cannot compete with the new tool in its tests: the skill-creator plugin is disabled
in user settings — its cache stays on disk for `grade.py` — and `superpowers:writing-skills`
is refused by the permission rule `Skill(superpowers:writing-skills)`. No setting hides a
single plugin skill, so it stays listed; a probe measured it (Platform Facts). The same
day, again at the user's request, the whole superpowers plugin was turned off in this
repository's `.claude/settings.local.json` until the new tool is built; that file had
also kept skill-creator enabled here, over the user settings, and now disables it too.
Other projects keep superpowers, whose usage study goes on there.

## Capability Matrix

**Keep** takes the capability as it is, rewritten in the new tool. **Improve** takes it
with the change stated. **Drop** leaves it out. **Open** waits for an open question
below. A reason that cites the documentation or this repository's checks cites evidence
to weigh, not a rule to obey.

### writing-skills

| # | Capability | Verdict | Reason |
|---|---|---|---|
| W1 | Baseline first: run the task without the skill and watch it fail before writing (`:14-16`, `:558-565`) | keep | The only guard in either source against guidance written for a failure nobody observed; SC runs its baseline only after the draft (SC `:169-186`). |
| W2 | Iron Law: no skill and no edit without a failing test first, "delete means delete" (`:376-395`) | improve | Absolute even for a typo; the testing rule scales evaluation to the kind of edit. |
| W3 | Required background `superpowers:test-driven-development` (`:18`, `:395`) | improve | Test-first holds: best practices § Build evaluations first prescribes it for skills. The new tool states its own proportional version instead of requiring another plugin's skill; superpowers stays installed and under study, only `writing-skills` is retired. |
| W4 | When to create a skill, and when not: one-offs, documented practice, constraints a script can enforce (`:47-59`) | improve | Sound, except that it sends a project's conventions to the instructions file, never to a skill; docs § Types of skill content lists conventions as skill content. The new tool writes both kinds: global skills, like this setup's, used across repositories, and repository skills, bound to one repository's conventions and context. |
| W5 | Skill types — technique, pattern, reference — and a test design for each, discipline included (`:61-70`, `:397-444`) | keep | The type decides the test design; Phase 4's case types start from this map. |
| W6 | Layout: flat namespace, companion files at the skill root, split at 100+ lines (`:72-91`, `:347-372`) | improve | Companions at the root escape the reachability check, which follows `references/`, `assets/`, `scripts/` only; the layout becomes a declared convention, the spec's folders otherwise. |
| W7 | SKILL.md skeleton: Overview, When to Use, Core Pattern, Quick Reference, Implementation, Common Mistakes (`:105-137`) | improve | Useful for technique skills, but the body is read only after the skill triggered: trigger conditions belong in the description (SC `:67`, docs § Frontmatter reference). |
| W8 | Frontmatter facts: two required fields, 1,024 characters for the whole frontmatter, example name `Skill-Name-With-Hyphens` (`:95-108`) | improve | Wrong three times: Claude Code requires no field (docs § Frontmatter reference), 1,024 is the spec's limit on `description` alone, and the spec forbids capitals in `name`. |
| W9 | Description: "Use when…" trigger conditions only, never what the skill does (`:99-103`, `:150-172`) | improve | Contradicts the docs, the spec and the best practices ("what the skill does and when to use it"); the evidence it cites (`:154-156`) supports a narrower rule — no step-by-step workflow, while a short mention of what the skill does is fine (the user, 2026-09-28) — settled with the description rule. |
| W10 | Keyword coverage: error messages, symptoms, synonyms, tool names (`:199-205`) | keep | The first step of docs § Skill not triggering. |
| W11 | Naming: verb-first, gerunds (`:207-211`, `:268-276`) | keep | Matches best practices § Naming conventions; the hard rules become Phase 2 checks. |
| W12 | Word budgets: under 150, 200 or 500 words (`:213-266`) | improve | Unmeasured, and broken by the skill itself: 3,814 words against its own 500. Replaced by the size budgets. |
| W13 | Token techniques: details to `--help`, cross-reference instead of repeating, compress examples (`:222-259`) | keep | In line with docs § Types of skill content: "every line is a recurring token cost". |
| W14 | Cite other skills by name with REQUIRED markers; never `@` links, which force-load files (`:278-288`) | keep | Docs § How Claude Code handles the body of a synced skill confirms that a local skill attaches the files its `@` references name; the "200k+" figure goes, being unmeasured. |
| W15 | Graphviz flowcharts, with `graphviz-conventions.dot` and `render-graphs.js` (`:290-322`) | drop | Measured (Flowchart Measurement below): the same decision as a `dot` block, a table or a numbered list fixed the failure equally, 6/6 each against 0/6 without guidance, while the flowchart cost about 255 input tokens against 100 and 90, and its reasons drifted more. |
| W16 | One excellent runnable example; no multi-language, no fill-in-the-blank templates (`:324-345`) | improve | Keep for code examples; output templates are a documented pattern (best practices § Template pattern) that this repository's roadmap skill uses. |
| W17 | Run scripts through their interpreter, never by bare path (`:374`) | improve | Contradicts this repository's finding that a skill script under `~/.claude` runs by its path (`CLAUDE.md`, Gotchas) and the `${CLAUDE_SKILL_DIR}` pattern of docs § Available string substitutions; settled with the script rule. `${CLAUDE_SKILL_DIR}` is Claude Code's: the agent-neutral form is a path relative to the skill directory (spec § File references), resolved by the harness or at install time. |
| W18 | Rationalizations for skipping tests (`:446-459`) | improve | Discipline guidance: kept only if a baseline shows sessions skipping evaluation, per W19. |
| W19 | Match the form to the failure: prohibition for a discipline failure, recipe for wrong-shaped output, required slot for an omission, conditional on an observable predicate; no nuance clauses; exemptions don't scope (`:461-476`) | keep | The only rule in either source backed by a controlled wording test (`:472`); it becomes the tone rule. |
| W20 | Bulletproofing: explicit loopholes, spirit versus letter, rationalization table, red flags, violation symptoms in the description (`:478-552`) | keep | Scoped, as the source scopes it (`:482`), to observed discipline failures. |
| W21 | Persuasion principles: authority, commitment, scarcity, social proof, unity (`persuasion-principles.md`) | drop | The study it cites measures compliance with objectionable requests, not instruction following; W19 already decides when firm wording is warranted. |
| W22 | Wording micro-tests: one fresh sample per call, a no-guidance control, 5+ repetitions, every flagged match read, variance as a metric (`:577-587`) | keep | Cheap and controlled; neither SC nor this repository tests wording on its own. |
| W23 | Pressure scenarios: 3+ combined pressures, forced choice, meta-testing, signs of a bulletproof skill (`testing-skills-with-subagents.md`) | improve | The only method for compliance under pressure; its scenarios join the output evals' format so one harness runs both. |
| W24 | Worked campaign on `CLAUDE.md` variants (`examples/CLAUDE_MD_TESTING.md`) | drop | A plan with expected results and no measured ones; W22 carries the method. |
| W25 | Anti-patterns: narratives instead of techniques, multi-language examples, code in flowcharts, generic labels (`:22-28`, `:595-614`) | keep | The first two; the flowchart ones go with W15. |
| W26 | One skill at a time, with a mandatory checklist and a todo per item (`:616-665`) | improve | Keep "verify each skill before the next"; the checklist's mechanical items become Phase 2 checks. |
| W27 | Deployment: commit, push to a fork, contribute upstream (`:666-668`) | drop | superpowers-specific; the repository's conventions decide versioning. |
| W28 | Discovery by grepping skill descriptions (`:670-681`) | drop | The Agent Skills standard loads every skill's name and description at startup (spec § Progressive disclosure), so any compliant agent, not only Claude Code, discovers skills from a listing. |
| W29 | Paths for Codex, Copilot CLI and Gemini CLI, `~/.agents/skills/` (`:12`) | drop | The install target stays `~/.claude` for now, and a repository skill goes where that repository's conventions say. Every tie to Claude Code is listed in `docs/claude-code-coupling.md` (to be created) to ease the move to other agents. |
| W30 | A bundled copy of the best practices (`anthropic-best-practices.md`, 1,150 lines, `:20`) | improve | A copy of Anthropic's "Skill authoring best practices" page. Its rewrite from "Claude" to "agent" — 5 occurrences of "Claude" against 108 on the live page — is the direction this setup takes; the flaw is a stale copy passing an edited text for the official one. Link the live page, found through the indexes `https://platform.claude.com/llms.txt` and `https://code.claude.com/docs/llms.txt`, and write our own guidance for the agent. |

### skill-creator

| # | Capability | Verdict | Reason |
|---|---|---|---|
| S1 | The loop: intent, draft, test prompts, qualitative and quantitative review, rewrite, a wider test set (`:10-20`) | keep | The backbone of Phases 3 and 4. |
| S2 | Enter at the user's stage; evaluation may be skipped (`:22-28`) | improve | Keep the flexible entry; skipping evaluation becomes an explicit choice under the testing rule. |
| S3 | Adapt jargon to the user's familiarity (`:32-41`) | drop | The tool serves people writing skills in repositories; plain wording is already the default. |
| S4 | Capture intent in four questions, answers drawn first from the conversation (`:47-54`) | keep | Turning a workflow already done in the session into a skill is the common entry point. |
| S5 | Interview and research: edge cases, formats, success criteria, dependencies (`:56-60`) | keep | Settles before writing what would otherwise surface as failed evals. |
| S6 | "Pushy" descriptions against undertriggering (`:67`) | improve | Docs § Skill triggers too often answers with a more specific description, and the listing is capped; trigger evals decide, under the description rule. |
| S7 | Anatomy: `SKILL.md`, `scripts/`, `references/`, `assets/` (`:73-84`) | keep | The spec's layout and this repository's. |
| S8 | Progressive disclosure: metadata, body under 500 lines, resources on demand, one reference per variant (`:86-109`) | keep | Matches the docs and the spec; completed with the lifecycle facts below. |
| S9 | Table of contents for references over 300 lines (`:98`) | improve | Best practices § Structure longer reference files with table of contents says 100 lines; settled with the size budgets. |
| S10 | Principle of lack of surprise (`:111-113`) | keep | Extended to the audit: a project skill grants itself tools without workspace trust (docs § Pre-approve tools for a skill). |
| S11 | Writing patterns: imperative form, output templates, input and output examples (`:115-135`) | keep | Best practices § Template pattern and § Examples pattern. |
| S12 | Explain the why rather than MUSTs; generalize; redraft with fresh eyes (`:137-139`, `:296-306`) | improve | Docs § Types of skill content asks the reverse for bodies — "state what to do rather than narrating how or why"; reconciled in the tone rule. |
| S13 | Test cases: 2-3 realistic prompts in `evals/evals.json`, assertions later (`:141-161`) | keep | The roadmap evals already use the format. |
| S14 | Eval workspace `<skill-name>-workspace/` created beside the skill's folder (`:167`) | improve | For `domains/roadmap/skills/roadmap/`, that is `domains/roadmap/skills/roadmap-workspace/`: inside the repository, and inside a folder the installer copies whole into `~/.claude/skills/` (`tools/claude_setup.py`, `domain_files`). The workspace goes where the repository's conventions say — `.superpowers/` here, gitignored. |
| S15 | With-skill and baseline subagents launched together; baseline without the skill, or a snapshot of the edited version (`:169-186`, `:313`) | improve | Run agents get a copy without `evals/` and no Skill tool, or an installed copy shadows the one under test (`CLAUDE.md`, Gotchas). |
| S16 | Named evals with `eval_metadata.json` (`:188-197`) | keep | Readable results across iterations. |
| S17 | Assertions drafted while runs go: objectively checkable, descriptive names, judgment left to people (`:199-205`) | keep | Uses the waiting time without forcing assertions on judgment calls. |
| S18 | Tokens and duration copied by hand from each notification into `timing.json` (`:207-219`) | improve | Lost when missed. Run transcripts are a harness feature — Claude Code writes them under `~/.claude/projects/` — so Phase 4 reads them through a per-harness adapter, the notification figures being the fallback, and lists the tie in the coupling page. |
| S19 | Grader agent: evidence per assertion, a pass only for real completion, claims checked, weak assertions criticized (`agents/grader.md`) | keep | Criticizing weak assertions keeps a passing benchmark honest. |
| S20 | Scripts for assertions a script can decide (`:225`) | keep | The roadmap evals already do it. |
| S21 | Benchmark: mean, standard deviation, minimum and maximum per configuration, and the delta (`scripts/aggregate_benchmark.py`) | keep | `domains/roadmap/skills/roadmap/evals/grade.py` depends on it; adapted with its notice. |
| S22 | Analyst pass: assertions that never discriminate, flaky evals, time and token trade-offs (`agents/analyzer.md`) | keep | Finds what averages hide. |
| S23 | Review viewer: outputs, previous iteration, grades, feedback to `feedback.json`, benchmark tab, `--static` (`eval-viewer/`) | keep | Decided at opening; standard library only. |
| S24 | Improving a skill: generalize from feedback, keep the prompt lean, read transcripts, bundle the script every run rewrote (`:296-306`) | keep | Each point is a concrete habit a reviewer can check. |
| S25 | Iterations with `--previous-workspace`, stopping on satisfaction, empty feedback or no progress (`:308-321`) | keep | Clear stopping conditions. |
| S26 | Blind comparison and post-hoc analysis (`:325-329`, `agents/comparator.md`, `agents/analyzer.md`) | keep | As an option, run only when the benchmark does not separate two versions (Open Questions). |
| S27 | Trigger queries: 20, realistic and detailed, negatives that nearly match (`:337-358`) | keep | Near misses are what test a description; docs § Evaluate and iterate on a skill asks for the same two measures. |
| S28 | Trigger set review in `assets/eval_review.html`, exported to `~/Downloads/eval_set.json` (`:360-373`) | improve | A round trip through the browser's download folder; Phase 4 reviews the set in the file or in the kept viewer. |
| S29 | Trigger measurement (`scripts/run_eval.py`) | improve | Writes the description as a command file into the project's `.claude/commands/`, counts only the first tool call — a session that reads a file before loading the skill scores a miss — and runs with the user's whole configuration. |
| S30 | Description tuning: 60/40 split, 3 runs per query, rewrites by `claude -p`, best on held-out queries, HTML report (`:375-394`, `scripts/run_loop.py`, `improve_description.py`, `generate_report.py`) | improve | The session proposes each rewrite and a script only measures it (Open Questions): the rewrite keeps the intent and the user's feedback, and no longer depends on `claude -p`. |
| S31 | Simple one-step queries trigger no skill (`:396-400`) | keep | Shapes the trigger queries. |
| S32 | Validator (`scripts/quick_validate.py`) | improve | Allows only the spec's six fields, so it rejects fields Claude Code accepts (docs § Using skill frontmatter outside Claude Code), and needs PyYAML. Phase 2 checks the standard's fields as the base for any agent, and each harness's extensions — Claude Code's for now — as a declared profile, flagging a skill that relies on one harness. |
| S33 | Frontmatter parser (`scripts/utils.py`) | improve | Hand-written and reads two keys; the audit needs the whole frontmatter, with the standard library (see the checks below). |
| S34 | JSON schemas (`references/schemas.md`) | keep | The contract between scripts and viewer; it gains a table of contents. |
| S35 | `.skill` packaging (`:408-416`, `scripts/package_skill.py`) | drop | Out of scope. |
| S36 | Claude.ai and Cowork instructions (`:420-455`) | drop | Out of scope. |
| S37 | An edited skill keeps its name (`:438-441`) | keep | A rename breaks invocations and `Skill(name)` rules (docs § Restrict Claude's skill access); the `/tmp` staging is claude.ai's and goes. |
| S38 | "Do NOT use `/skill-test`", todo-list reminders (`:165`, `:483`) | drop | Meaningful only beside competing tools. |

## Platform Facts Neither Source Encodes

Facts of the Agent Skills standard, which hold for any agent that implements it, and of
Claude Code, the current install target. They inform the rules without capping them;
the scope column says which agents they bind.

| Fact | Scope | Where | Encoded in |
|---|---|---|---|
| Every skill's `name` and `description` load at startup; the body loads when the skill activates, other files when needed | standard | spec § Progressive disclosure | Phase 3 |
| A body under 5,000 tokens and a `SKILL.md` under 500 lines are recommended | standard | spec § Progressive disclosure | Phase 0 (size budgets) |
| Files are referenced by paths relative to the skill root | standard | spec § File references | Phase 0 (script rule), Phase 2 |
| `allowed-tools` is experimental, and its support varies between agents | standard | spec § `allowed-tools` field | Phase 0 (script rule) |
| `name` must match the directory; Claude Code lets them differ | standard, Claude Code | spec § `name` field; docs § How a skill gets its command name | Phase 2 |
| Claude Code accepts 20 frontmatter fields, all optional: `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` | Claude Code | docs § Frontmatter reference | Phase 2 |
| An unknown field is ignored without error, so a misspelled field fails silently | Claude Code | docs § Frontmatter reference | Phase 2 |
| Frontmatter is read only when `---` is the first line; YAML that does not parse loads the skill with no fields | Claude Code | docs § Frontmatter reference | Phase 2 |
| Boolean fields also accept `yes`, `no`, `on`, `off`, `1`, `0` (v2.1.218) | Claude Code | docs § Frontmatter reference | Phase 2 |
| `description` plus `when_to_use` is cut at 1,536 characters in the listing; key use case first | Claude Code | docs § Frontmatter reference, § Skill descriptions are cut short | Phase 2, Phase 3 |
| The listing gets 1% of the context window and drops the descriptions of the least-used skills first; `disable-model-invocation: true` takes the description out of context | Claude Code | docs § Skill descriptions are cut short, § Control who invokes a skill | Phase 3 |
| An invoked skill stays in context and is never re-read; after compaction, the first 5,000 tokens of each skill's latest invocation come back, within 25,000 tokens for all skills | Claude Code | docs § Skill content lifecycle | Phase 2, Phase 3 |
| A failing `` !`command` `` aborts the whole invocation; exit 1 passes only for search and comparison commands; outside auto mode, a command not allowed by the permission rules aborts; commands run in the session's working directory | Claude Code | docs § Inject dynamic context | Phase 1 (the reader exits 0), Phase 2 |
| Substitutions `$ARGUMENTS`, `$N`, `$name`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`; a literal `$1.00` needs `\$1.00` | Claude Code | docs § Available string substitutions | Phase 3; candidate rule for Phase 2 |
| `allowed-tools` grants for the invoking turn only, restricts nothing, and applies without workspace trust | Claude Code | docs § Pre-approve tools for a skill | Phase 0 (script rule), Phase 2 |
| `context: fork` runs the skill without the conversation; `-p` waits for the fork | Claude Code | docs § Run skills in a subagent | Phase 3 |
| Reserved names: a folder named `synced`, the `anthropic-skills` namespace | Claude Code | docs § Choose where skills load, § Names reserved for synced skills | Phase 0 (names), Phase 2 |
| Changes to `SKILL.md` apply live; a new top-level skills directory needs `/reload-skills`; `--add-dir` directories are watched from launch | Claude Code | docs § Edit a skill during a session, § Load skills from a directory outside the project | Phase 3, Phase 4 |
| A local skill's body attaches the files its `@` references name | Claude Code | docs § How Claude Code handles the body of a synced skill | Phase 2 |
| `claude plugin validate <dir>` reports frontmatter that does not parse (v2.1.233) | Claude Code | docs § Skill not triggering | Phase 2 |
| `/skill-doctor` reports each skill's context cost and use, as text under `-p` (v2.1.252) | Claude Code | docs § Find unused skills | Phase 3 (audit reference) |
| The documented evaluation: fresh sessions, with the skill and with it turned off in `skillOverrides` | Claude Code | docs § Evaluate and iterate on a skill | Phase 4 |
| A body should "state what to do rather than narrating how or why" | Claude Code | docs § Types of skill content | Phase 0 (tone rule) |
| `paths`, `disallowed-tools`, `hooks` and `ultrathink` change when and how a skill acts | Claude Code | docs § Frontmatter reference, § Inject dynamic context | Phase 3 |
| `skillOverrides` hides a personal skill but not a plugin skill, whether keyed `plugin:skill` or by the bare name; a `Skill(plugin:skill)` deny rule refuses the invocation and leaves the skill listed | Claude Code | docs § Override skill visibility from settings; probe of 2026-09-28 on 2.1.283 | Phase 4 |
| In headless runs, `allowed-tools` pre-approved nothing — with `${CLAUDE_SKILL_DIR}` or with a literal path — and declaring it made the skill itself need an approval in the default permission mode; interactive sessions untested | Claude Code | probes of 2026-09-27 and 2026-09-28 on 2.1.283, against docs § Pre-approve tools for a skill | Phase 0 (script rule) |
| `claude -p --output-format stream-json --verbose` opens with an init event listing the session's skills, slash commands and plugins; `--settings <file>` changes them for one run without touching user settings | Claude Code | probe of 2026-09-28 on 2.1.283 | Phase 4 |

## Checks Run On The Sources

`tests/skills.py` run on each skill directory: 20 problems in WS, 11 in SC, none in this
repository's `roadmap` and `tool-review`. Kept as test cases for the Phase 2 audit, as
alerts to weigh rather than rules:

| Problem found | Where | Holds? | What the audit needs |
|---|---|---|---|
| `SKILL.md` is 682 lines, over 500 | WS | yes | An alert, not a limit: the size budgets decide what the audit reports. |
| A 430-line reference without a table of contents | SC `references/schemas.md` | yes | Kept; the threshold is settled with the size budgets. |
| Cites `references/codex-tools.md` and `references/gemini-tools.md`, missing | WS `:12` | yes, misreported | The path is `../using-superpowers/references/…`: report a citation that leaves the skill directory as such. |
| Cites `scripts/tool.sh` and `scripts/tool.js`, missing | WS `:374` | no | Paths given as examples in prose. |
| 12 cited `scripts/*.py`, missing | WS `anthropic-best-practices.md` | no | Paths inside example code. Skipping code blocks is no answer — real invocations live there too. |
| 9 files under `scripts/` unreachable from `SKILL.md` | SC | mostly no | Three are cited as modules (`python -m scripts.run_loop`), the rest imported by those: follow module names and imports. |
| Compatibility wording `Legacy`, `deprecated` | WS `anthropic-best-practices.md:570` | no | An example of an "old patterns" section: a repository convention applied to a foreign skill, where it was never declared. |
| Compatibility wording `old version` | SC `:186` | no | A skill's previous version is the baseline of an edit, so the new tool's own skill needs these words: the convention must allow them before Phase 3 writes it. |
| Not checked at all: companion files at the skill root, `agents/`, `eval-viewer/` | WS, SC | gap | Reachability follows only `references/`, `assets/`, `scripts/`. |
| `tests/skills.py`, `tests/domains.py` and `domains/review/tests/test_reviewfile.py` import PyYAML | this repository | gap | Breaks the standard-library-only convention; the Phase 2 parser decision covers these three files too. |

## Settled Rules

### Description

Settled with the user on 2026-09-28. No trigger measurement exists in this repository yet:
Phase 4's trigger evals test the rule, and Phase 5 applies it to `authoring-skills`.

1. **Content, in this order:** what the skill does, in one clause that names its
   operations or outputs — never the sequence of steps the body defines; then when to use
   it: the key use case first, then the trigger situations in the words users say —
   keywords, synonyms, symptoms, file types.
2. **Exclusions** ("Not for …") only after a false trigger was observed, in an eval or in
   real use: each one costs listing tokens at every turn.
3. **Form:** third person, never naming the model; the harness only when the skill is
   about it.
4. **Everything in `description`, nothing in `when_to_use`:** only Claude Code reads that
   field, so another agent would lose those triggers.
5. **Length:** set with the size budgets. The key use case sits in the first sentence,
   since listings truncate.
6. **Tuned by measurement:** a broader or a more specific description is not a style
   chosen beforehand. When the skill triggers too rarely, its situations widen; too
   often, they narrow and gain exclusions.
7. **Discipline skills** add the symptoms of an imminent violation, only when a run
   without the skill shows that violation.

Evidence:

- **Content:** WS wants the "when" only (`:99-103`) and SC both (`:67`); the docs
  (§ Frontmatter reference), the spec (§ `description` field) and the best practices
  (§ Writing effective descriptions) say what the skill does and when to use it. WS's only
  evidence (`:154-156`) supports forbidding the workflow, not the "what".
- **Order:** docs § Frontmatter reference, "put the key use case first"; the spec's
  example gives the "what", then "Use when".
- **Exclusions:** SC's near-miss negative queries (`:356-358`); docs § Skill triggers too
  often; the roadmap skill's "Not for …".
- **Third person:** WS `:179`; best practices § Writing effective descriptions.
- **`when_to_use`:** in docs § Frontmatter reference only, absent from the spec.
- **Broader or more specific:** SC `:67` against undertriggering, without data; docs
  § Skill triggers too often against overtriggering — two remedies for two symptoms that
  only a measure tells apart.
- **Discipline symptoms:** WS `:546-552`.

### Testing

Settled with the user on 2026-09-28.

- **A new skill, or a change meant to alter behavior:** run the target tasks without the
  skill — or with its previous version — first; write the evals on the gaps observed;
  then write the minimum, and compare with that baseline.
- **A script:** unit tests first.
- **A description:** the should-trigger and should-not-trigger queries first, run before
  and after the change.
- **A wording change meant to keep behavior:** run the existing evals again; add a wording
  micro-test (row W22) when the wording shapes behavior.
- **A fact in a reference:** a check that the agent finds the fact and applies it.
- **A discipline skill:** pressure scenarios (row W23).
- **A harness mechanism — permissions, injection, hooks:** a probe before relying on it.
- **A change that alters no instruction — a typo, a link, formatting:** the audit alone.
  Added on 2026-10-05, with the user's approval of the design of Phase 3 of roadmap
  `skill-tooling`: rerunning evals for such a change costs runs and tells nothing.
- **No evaluation** only when the user chooses it, and the choice is recorded.

Evidence: best practices § Build evaluations first; row W1; the user's session review of
2026-09-27, kept locally under `local-review/`, where test-first paid for the scripts and
headless probes overturned two design assumptions; the probes of this phase, which
contradicted a memory on `skillOverrides` and the docs on `allowed-tools`.

### Size Budgets

Settled with the user on 2026-09-28.

- **`SKILL.md`: 5,000 tokens at most,** the instructions that must hold for the whole task
  first. Claude Code keeps the first 5,000 tokens of a skill after compaction, and the
  spec recommends the same bound. 500 lines stays an alert only: skill-creator is 485
  lines and about 8,300 tokens.
- **Description: 1,024 characters at most,** the standard's limit and the portable one;
  Claude Code cuts at 1,536.
- **References: a table of contents from 300 lines,** as `tests/skills.py` checks today.
  The best practices say 100; no measured gain supports it, and five of this repository's
  references would need one.

Measured on 2026-09-28, characters divided by four: `roadmap` about 1,800 tokens,
`tool-review` about 1,000, `writing-skills` about 6,700, skill-creator about 8,300.

### Tone

Settled with the user on 2026-09-28: emphatic wording as a last resort, and a reason in
one clause when a rule needs judgment.

1. **By default, state what to do,** in the imperative and in positive form, rather than
   what not to do.
2. **A reason in one clause when the rule needs judgment,** that is when the agent must
   apply it to cases the text does not list; no narration, no history.
3. **The form follows the observed failure:** wrong-shaped output → a recipe of what the
   output contains, in order; an omitted element → a required slot in the template;
   behavior that depends on a condition → a conditional on an observable predicate; a
   known rule broken under pressure → prohibition, rationalization table and red flags,
   in this case only.
4. **Emphatic wording is a last resort** — capitals, "CRITICAL", "MUST", stacked
   intensifiers, repeated warnings: only after an observed discipline failure that plain
   wording and the discipline form did not fix, with the eval that shows it.
5. **No nuance or exemption clauses:** a real exception becomes its own conditional; if
   part of the output must escape a rule, restructure so that the rule cannot reach it.
6. **Constraint proportional to fragility:** free instructions where several approaches
   hold, a template or a parameterized script where a pattern is preferred, an exact
   script where only one path is safe.
7. **No persuasion techniques** (row W21).

Evidence: the prompting best practices
(https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
— "Tell Claude what to do instead of what not to do"; § Add context to improve
performance, where "NEVER use ellipses" works better with its reason; recent models
overtrigger, so "dial back any aggressive language". Docs § Types of skill content —
"state what to do rather than narrating how or why". WS `:461-476`, the only rule backed
by a controlled wording test (`:472`), and `:474-476` on nuance clauses. SC `:137-139` and
`:302` — capitals as a yellow flag. Best practices § Set appropriate degrees of freedom,
and § Develop Skills iteratively, where a stronger "MUST" follows an observed failure. No
wording measurement exists in this repository: the micro-tests of row W22 check our own
wording in Phase 3. Observed in the session that settled it: the line "if you think there
is even a 1% chance a skill might apply … you ABSOLUTELY MUST invoke the skill", injected
by superpowers, led to loading a skill that added the whole settings schema, tens of
thousands of characters, for a two-line edit.

### Scripts

Settled with the user on 2026-09-28. The skill stays portable content; whatever depends on
an agent lives around it and is set at install.

- **In the skill:** a script is cited by its path relative to the skill's directory
  (spec § File references), and the agent builds the absolute path from the directory
  its harness gives. No `${CLAUDE_SKILL_DIR}` in the text, no `allowed-tools`, no
  permission syntax. A `!` command appears only as a Claude Code optimization, with a
  fallback step and a row in `docs/claude-code-coupling.md`.
- **The script:** an executable with `#!/usr/bin/env python3`, called by its path, never
  through `python3 …`; the standard library, or what the repository's conventions allow;
  data through files or arguments, never a heredoc; plain text output and documented exit
  codes; exit 0 in every case when a `!` command may run it.
- **Around the skill:** a global skill's permissions come from the installer's allow
  rules — `permissions.json`, merged today into Claude Code's settings — and a repository
  skill's from the agent's settings in that repository, or the user's approval at the
  first run.

Evidence: the `allowed-tools` probes (Platform Facts) and spec § `allowed-tools` field,
"experimental"; `CLAUDE.md`, Gotchas — a permission rule never matches a command that
carries a heredoc, and a project hook may refuse `python3`; the installer keeps the
executable bit (`tools/claude_setup.py`, `shutil.copy`).

### No Separate TDD Skill

Decided by the user on 2026-09-28: the new tool carries its own testing rule, centered on
what each change needs, instead of a TDD skill loaded beside it. The user's review of
2026-09-27 found `superpowers:test-driven-development`, loaded by cascade, of low marginal
value for about 198,000 carried tokens. Whether a general TDD skill for code is kept
belongs to the superpowers recount.

## Flowchart Measurement

Run on 2026-09-28 for row W15, with the wording micro-test of row W22: one fresh headless
session per sample on Claude Haiku 4.5, its system prompt a role line plus one form of the
guidance, no tools, no settings, 6 samples per form and scenario. The guidance was the
same two- or three-branch decision from the roadmap skill's closure, written as a `dot`
flowchart, a table and a numbered list, against a control without guidance. A form's
token cost is its input tokens minus the control's.

| Test | Control | Flowchart | Table | List |
|---|---|---|---|---|
| Unticked task, forced choice among four described options | 12/12 | 12/12 | 12/12 | 12/12 |
| Failing check at closure, forced choice among four described options | 12/12 | 12/12 | 12/12 | 12/12 |
| Failing check, recorded defect, one-word answer | 5/6 | 6/6 | 6/6 | 6/6 |
| Failing check, unrecorded failure, one-word answer | 0/6 — "FIX" every time | 6/6 | 6/6 | 6/6 |
| Input tokens above the control | — | ~255 | ~100 | ~90 |

The two forced-choice tests could not discriminate: the described options gave the answer
away, and the control never failed. In the last test, the only one where the control
failed, every form fixed the failure; the reasons given under the table and the list all
said to stop, report and wait, while two of the six flowchart reasons drifted to "it must
be fixed". Limits: one small model, short prompts, a decision with two or three branches;
loops and larger decision trees — the cases writing-skills claims for flowcharts — were
not tested. 144 samples, about $0.61.

## Open Questions

Answered by the user on 2026-09-28.

- **Who owns `.agent-conventions.toml`: a shared module.** One source, copied into each
  tool that reads the file. It adds no dependency at run time and is standard-library
  Python that any agent can run; its cost is a copy step, and versions that can differ
  between domains until the next `make update`. A dedicated skill would cost context in
  every tool that loads it, cannot hold a conversation from a hook or a subagent, and
  relies on one skill invoking another, a harness mechanism; per-tool code would
  duplicate the parsing and drift. Decided without the token and maintenance
  measurement the task planned. How the copy is made — by the installer, or as checked
  copies in each domain — is Phase 1's design.
- **Description tuning: the session proposes, a script measures.** The agent in the
  conversation writes each rewrite, knowing the skill's intent and the user's feedback;
  a script measures it on training and held-out queries, and the best on held-out
  queries wins. Only the measure depends on the harness. skill-creator's loop rewrote
  through `claude -p`, blind to both.
- **Blind comparison: kept as an option,** run only when the benchmark does not separate
  two versions of a skill.
- **Names:** the domain `skill-tooling`, like this roadmap; the skill `authoring-skills`,
  in the gerund form the best practices recommend (§ Naming conventions); the agents
  `skill-auditor`, `skill-grader` and `skill-comparator`. The skill may take the name
  `writing-skills` once superpowers' skill of that name is gone; a rename breaks
  `Skill(name)` permission rules and every file that names the skill (row S37).

## Licensing

- The repository is under the Apache License 2.0: `LICENSE` at its root holds the
  canonical text of https://www.apache.org/licenses/LICENSE-2.0.txt.
- No code of either source is in the repository yet: `grade.py` runs skill-creator's
  scripts from the plugin cache, and `tests/skills.py` implements its own checks.
- A file adapted from skill-creator (Apache 2.0, no upstream `NOTICE`) keeps a header
  naming its origin — repository, path, commit — and its license, and says that it was
  modified (Apache 2.0, § 4 (b) and (c)).
- A file adapted from superpowers (MIT, "Copyright (c) 2025 Jesse Vincent") keeps that
  copyright line and the MIT permission notice, which the MIT license requires in every
  copy or substantial portion.
- A `NOTICE` file at the root, created with the first adapted file — skill-creator's
  review viewer in Phase 4 — lists each adapted file with its origin, license and changes.

## When To Revisit

- **The description rule,** when Phase 4's trigger evals give the first trigger rates.
- **Row W15,** if a Phase 3 micro-test on a loop or a larger decision tree shows a table
  or a list failing where a flowchart holds.
- **The `allowed-tools` and `skillOverrides` facts,** when Claude Code changes either
  field: run the probes again, with the method under Platform Facts.
- **A general TDD skill,** at the superpowers recount of 2026-10-18.
- **The whole matrix,** at Phase 5, which checks each row against what was built.
- **The script rule and row S32,** when a second agent is installed:
  `docs/claude-code-coupling.md` lists what it needs.
