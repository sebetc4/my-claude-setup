# Skill audit rules — 2026-10-03

Recorded by Phase 2 of the skill-tooling roadmap: the rule catalogue the static audit
checks, and how it parses a skill's frontmatter. Approved by the user on 2026-10-04, as
proposed.

## Decision

1. **The audit checks the rules of the catalogue below,** each with its source, its
   severity and its message, on a skill directory and against the repository's `[skills]`
   conventions when `.agent-conventions.toml` declares them.
2. **It parses frontmatter with a strict subset of YAML of its own,** standard library
   only, in a shared module `shared/frontmatter/`; `claude plugin validate` is not part of
   the audit (The Parser).
3. **An error fails the check, a warning only reports.** Errors fail `audit.py` and
   `make check`, and the hook reports them to the agent; warnings are printed by
   `audit.py` and `make check`, never by the hook.

## Sources

- Fetched on 2026-10-03 as Markdown: the Claude Code skills page
  (https://code.claude.com/docs/en/skills, **docs §**), the Agent Skills specification
  (https://agentskills.io/specification, **spec §**) and the skill authoring best
  practices (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices,
  **best practices §**). The frontmatter reference still lists the 20 fields of
  2026-09-28.
- `docs/decisions/2026-09-28-skill-tooling.md`: its Platform Facts, its Checks Run On The
  Sources and its settled rules (Description, Size Budgets, Scripts, Tone).
- `tests/skills.py`, whose ten checks the audit takes over (From `tests/skills.py`).
- The parser probe of 2026-10-03 (The Parser), kept in `study/frontmatter-probe/`, which
  `.gitignore` keeps out of the repository.

## Severities And Profiles

- **error** — the harness misreads or drops part of the skill, or a settled rule of this
  setup or a declared convention is broken.
- **warning** — a likely mistake, a portability risk, or a budget alert: reported, never
  failing a check, as the Size Budgets keep 500 lines "an alert only".
- **Profiles.** The default profile checks a skill against Claude Code's frontmatter
  reference, the install target. `--portable` checks it against the Agent Skills
  standard: only its six fields, `name` required, `metadata` a map of strings, and
  `allowed-tools` a space-separated string.
- **`--checks`** runs the repository's `checks` commands of `[skills]` after the rules;
  the hook and `make check` never pass it, the second because `make check` is itself one
  of those commands here.

## The Parser

**The probe.** A prototype of the subset parser, `study/frontmatter-probe/subset.py`, ran
on 39 distinct `SKILL.md` files — this repository's two skills, 27 of the installed
plugins, 10 of scriptorium —, on 35 control frontmatters, each written to break one rule
or to try one form, and on the agents' frontmatter; PyYAML and `claude plugin validate`
(Claude Code 2.1.283) ran on the same files.

| What | Subset | PyYAML | `claude plugin validate` |
|---|---|---|---|
| 38 of the 39 skills | parsed, values equal to PyYAML's | parsed | passed |
| scriptorium's `session-review`: `: ` inside a plain description | rejected | rejected | passed |
| A value starting with `@` or a backtick; a tab in the indentation | rejected | rejected | passed |
| A duplicated key | rejected | the last value wins | passed |
| No opening `---` on line 1; never closed; closed by `...`; a value never closed; a list instead of a mapping | rejected | rejected | rejected |
| A name typed as a number; `metadata` not a map; no description | parsed; field rules F7 and N5 report them | parsed | reported |
| Anchors and aliases, a quoted key, a quoted value over two lines | unverifiable, outside the subset | parsed | passed |
| An unknown or misspelled key; `effort: extreme`; a name in capitals or unlike its folder | parsed; field rules report them | parsed | passed |
| A byte order mark; CRLF line ends; folded, literal and multi-line plain values; flow sequences and mappings; a nested `hooks` map | parsed, values equal to PyYAML's | parsed | passed |

What it shows:

1. **Claude Code's parser is laxer than YAML.** It read a `: ` inside a plain value, a
   value opening on a reserved indicator, a tab in the indentation and a duplicated key,
   which YAML forbids and PyYAML rejects but for the duplicate. An agent whose parser
   follows YAML drops every field of such a skill, scriptorium's `session-review` among
   them: rule F3 reports them as errors in both profiles.
2. **`claude plugin validate` reports eight of the 35 controls, and the subset with its
   field rules all eight.**
   It checks no field name and no value range — not even with `--strict`, whose
   unrecognized fields concern plugin manifests — reads skills only from a folder named
   `skills`, and needs Claude Code installed. It stays this probe's oracle for Claude
   Code's parser, run again when that parser changes.
3. **The subset covers what skills and agents write.** Every real frontmatter it parsed,
   and every control both parsed, gave PyYAML's values but one: `yes`, a boolean for
   YAML 1.1, which YAML 1.2 and the subset keep as a string and rule F7 accepts for a
   boolean field. Valid YAML outside it is reported as unverifiable (F4), never as
   invalid.

**The subset:** block mappings and sequences at any depth; plain, single-quoted,
double-quoted and block scalars; flow sequences and mappings of scalars on one line;
comments; plain scalars typed by YAML 1.2's core schema. Outside it: anchors, aliases,
tags, quoted and complex keys, quoted values over several lines, nested flow
collections, directives.

**The module:** `shared/frontmatter/frontmatter.py`, with its tests, copied into the
audit's `scripts/` by `tools/shared.py`. `tests/domains.py` reads agents' frontmatter
with it in place of PyYAML. `domains/review/tests/test_reviewfile.py` uses PyYAML as an
outside reader of the review format — keys such as `hook:a/b.py`, nested flow mappings —
richer than frontmatter: its two PyYAML assertions become literal expectations of the
rendered text, so that no file of the repository imports PyYAML.

## The Catalogue

Messages are printed as `path:line: [ID] message`. "Both" means both profiles.

### Frontmatter

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| F1 | `SKILL.md` opens with `---` on its first line, a byte order mark aside | docs § Frontmatter reference; probe | error | no frontmatter: open the file with `---` on its first line, or the harness reads it all as content |
| F2 | The frontmatter closes with a `---` line | probe: Claude Code takes no `...` | error | the frontmatter is never closed by a `---` line |
| F3 | The frontmatter is YAML: no `: ` in a plain value, no value opening on a reserved indicator, no tab in the indentation, no duplicated key, no unclosed quote | spec § `SKILL.md` format; docs § Frontmatter reference; probe | error, both | the parser's message, then: an agent whose parser follows YAML drops every field; quote the value |
| F4 | The frontmatter stays within the audited subset | The Parser | warning | outside what the audit reads: `<construct>`; its fields are not checked — write it in plain form |
| F5 | The frontmatter is a mapping | spec § `SKILL.md` format; probe | error | the frontmatter must be `key: value` lines |
| F6 | Every key is a known field: Claude Code's 20, or the standard's 6 under `--portable` | docs § Frontmatter reference: an unknown field is ignored without error; docs § Using skill frontmatter outside Claude Code: an upload fails on it | error, both | unknown field `<key>`, ignored without a word by the harness; did you mean `<closest field>`? |
| F7 | Each value has its field's type and allowed values: `true`, `false`, `yes`, `no`, `on`, `off`, `1`, `0` for `disable-model-invocation`, `user-invocable`, `background`; `effort` among `low`, `medium`, `high`, `xhigh`, `max`; `context: fork`; `shell` `bash` or `powershell`; a string for `name`, `description`, `when_to_use`, `argument-hint`, `model`, `agent`, `license`, `compatibility`; a string or a list of strings for `arguments`, `allowed-tools`, `disallowed-tools`, `paths`; a mapping for `metadata` and `hooks` | docs § Frontmatter reference; probe | error | `<field>` must be `<expected>`, got `<actual>` |
| F8 | Under `--portable`, `metadata` maps strings to strings and `allowed-tools` is one space-separated string | spec § `metadata` field, § `allowed-tools` field | error, `--portable` | `<field>` must be `<expected>` for the Agent Skills standard |
| F9 | `compatibility` holds 1 to 500 characters | spec § `compatibility` field; docs § Frontmatter reference | error | `compatibility` is `<n>` characters, 500 at most |
| F10 | `agent` and `background` come with `context: fork` | docs § Frontmatter reference | warning | `<field>` applies only with `context: fork`; here it does nothing |
| F11 | No `metadata` key repeats a frontmatter field name | docs § Frontmatter reference, `metadata` | warning | `metadata` key `<key>` repeats a field name; rename it |
| F12 | Not both `disable-model-invocation: true` and `user-invocable: false` | docs § Frontmatter reference, § Control who invokes a skill | error | neither the model nor the user can invoke this skill |
| F13 | No ` #` inside a plain value | YAML: ` #` opens a comment; probe | warning | ` #` starts a comment: the rest of the value is dropped; quote the value |

### Name And Description

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| N1 | `name` is present | spec § Frontmatter: required; Claude Code defaults to the folder | error, `--portable` | `name` is required by the Agent Skills standard |
| N2 | `name` is lowercase letters, digits and single hyphens, neither first nor last, 64 characters at most | spec § `name` field; best practices § Naming conventions | error | `name` `<value>` must be lowercase letters, digits and single inner hyphens, 64 characters at most |
| N3 | `name` equals the skill's folder | spec § `name` field: must match | error | `name` `<value>` does not match the folder `<folder>`: other agents refuse it, and Claude Code then answers to both names |
| N4 | The folder is not `synced` in any capitalization, and neither folder nor `name` is `anthropic-skills` or starts with `anthropic-skills:` | docs § Choose where skills load | error | reserved name `<name>`: the harness skips this skill |
| N5 | `description` is present and not empty | spec § `description` field: required; docs: recommended, else the body's first line | error | no description: the agent cannot tell when to use the skill |
| N6 | `description` holds 1,024 characters at most | spec § `description` field; Size Budgets of 2026-09-28 | error | `description` is `<n>` characters, 1,024 at most |
| N7 | No `<` or `>` in `name` or `description` | best practices § Skill structure: no XML tags | error | `<field>` holds an angle bracket: the platform refuses XML tags |
| N8 | `name` contains neither `anthropic` nor `claude` | best practices § Skill structure: reserved words | warning; error, `--portable` | `name` holds the reserved word `<word>`: claude.ai and the API refuse it |
| N9 | No `when_to_use` | Description rule 4 of 2026-09-28: only Claude Code reads it | warning | move `when_to_use` into `description`: other agents never read it |
| N10 | `description` plus `when_to_use` holds 1,536 characters at most | docs § Frontmatter reference: cut in the listing | error | `description` and `when_to_use` are `<n>` characters; the listing cuts at 1,536 |

### Size

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| Z1 | The body of `SKILL.md` is 5,000 tokens at most, estimated as characters divided by four | Size Budgets of 2026-09-28; docs § Skill content lifecycle; spec § Progressive disclosure | error | the body is about `<n>` tokens, 5,000 at most: compaction keeps only the first 5,000; move detail to `references/` |
| Z2 | `SKILL.md` is 500 lines at most | spec § Progressive disclosure; Size Budgets: an alert only | warning | `SKILL.md` is `<n>` lines; 500 is the alert |
| Z3 | A reference file of 300 lines or more has a `## Contents` section | Size Budgets of 2026-09-28; best practices § Structure longer reference files | error | `<n>` lines without a `## Contents` section |
| Z4 | A file of `references/` is cited from `SKILL.md`, not only from another reference | spec § File references: one level deep; best practices § Keep references one level deep | warning | reached only through `<file>`: cite it from `SKILL.md` |

### Resources

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| R1 | Every path the skill cites under `references/`, `assets/` or `scripts/`, or by a relative link, exists | `tests/skills.py`; spec § File references | error | cites `<path>`, which does not exist |
| R2 | No citation leaves the skill's folder | spec § `scripts/`: self-contained; Checks Run On The Sources of 2026-09-28 | warning | cites `<path>`, outside the skill: it breaks wherever the skill is installed alone |
| R3 | Every file of the skill is reached from `SKILL.md` — through citations, links, the `license` field, script imports and `-m` module names — but the evaluations folder and caches | `tests/skills.py`; `CLAUDE.md` Conventions; Checks Run On The Sources: companions at the root and module imports | error | not reached from `SKILL.md`: no file cites it |
| R4 | File paths use forward slashes | best practices § Avoid Windows-style paths | warning | `<path>` uses backslashes: write it with forward slashes |

### Execution

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| X1 | An injected command of `SKILL.md` — `` !`…` `` at a line's start or after a space, or a ` ```! ` block, code blocks included — ends in `\|\| true` | docs § Inject dynamic context, § When an injected command fails | warning | an injected command that exits non-zero aborts the whole skill: make it exit 0, or append `\|\| true` |
| X2 | A file of `scripts/` with a shebang has the executable bit; one without a shebang is imported by another script of the skill | Scripts rule of 2026-09-28: an executable called by its path | error | `<script>` has a shebang but not the executable bit / `<script>` has no shebang and no script imports it |
| X3 | No line runs a script of the skill through an interpreter | Scripts rule of 2026-09-28; `CLAUDE.md` Gotchas: a permission rule names the path, a project hook may refuse `python3` | warning | `<script>` is run through `<interpreter>`: call it by its path |
| X4 | Each `Bash(…)` rule of `allowed-tools` matches a command the body runs | docs § Pre-approve tools for a skill | warning | `allowed-tools` rule `<rule>` matches no command of the skill |
| X5 | No `@` reference to a file of the skill | row W14 of 2026-09-28; docs § How Claude Code handles the body of a synced skill | warning | `@<path>` attaches the file at every invocation: cite it by its path |
| X6 | No `ultrathink` in `SKILL.md` | docs § Inject dynamic context, tip; `RELEASE-NOTES.md:263` of superpowers 6.4.1 | warning | `ultrathink` turns on deep reasoning at every invocation: remove it unless meant |
| X7 | No unescaped `$` before a digit, `ARGUMENTS` or a declared argument name in `SKILL.md` | docs § Available string substitutions | warning | `<token>` is replaced when the skill gets arguments: write `\<token>` |

### Repository Conventions

Applied only where `.agent-conventions.toml` declares the key, as Phase 1 decided.

| # | Rule | Key | Severity | Message |
|---|---|---|---|---|
| C1 | The skill sits in one of the `dirs` | `dirs` | error | `<skill>` is outside the skill folders `<dirs>` |
| C2 | Its evaluations — `evals.json`, `test_*.py`, `checks.py` — sit in its `<evals>/` folder | `evals` | error | `<file>` belongs in `<evals>/` |
| C3 | Its files are in the declared language: for `english`, none of the common French words `tests/skills.py` lists, and no space before `%` | `language` | error | `<word>`: skill files are written in `<language>` / space before `%`: English takes none |
| C4 | Its files address the agent: no named model — Claude, Opus, Sonnet, Haiku, Fable — Claude Code being a harness, not a model | `address = "agent"` | error | `<word>` names a model: address the agent |
| C5 | It uses none of the excluded features: the `allowed-tools` field; injected commands; substitutions — `$ARGUMENTS`, `$N`, a declared `$name`, `${CLAUDE_…}` — in `SKILL.md` | `exclude` | error | `<feature>` is excluded by the repository's conventions |
| C6 | The `workspace` folder is ignored by git, checked once per repository | `workspace` | error | the eval workspace `<path>` is not ignored by git: runs would land in commits |
| C7 | The repository's `checks` commands pass, under `--checks` only | `checks` | error | `<command>` failed: `<first lines>` |

### Text

| # | Rule | Source | Severity | Message |
|---|---|---|---|---|
| T1 | No compatibility wording — `legacy`, `deprecated`, backward compatibility, `pre-existing`, "before this feature" — in the skill's files | `tests/skills.py`; Tone rule 2 of 2026-09-28: no narration, no history | warning | compatibility wording `<word>`: a skill states only its target behavior |

## From `tests/skills.py`

Each of its checks, re-justified rather than carried over as it stands:

| Its check | Becomes | What changes |
|---|---|---|
| Frontmatter present, parsed by PyYAML, a mapping | F1, F2, F3, F5 | The subset parser in place of PyYAML; Claude Code's laxer reading named in F3's message |
| `name` kebab-case, 64 characters at most | N2 | Single inner hyphens, as the spec requires |
| `name` matches the folder | N3 | — |
| `description` present, 1,024 characters at most, no angle brackets | N5, N6, N7 | Angle brackets checked in `name` too |
| Cited resources exist | R1 | Relative links count as citations; a citation leaving the folder becomes R2 |
| Resources reachable from `SKILL.md` | R3 | Every file of the skill, imports and module names followed |
| No HTML comment in a template, placeholders in `UPPER_SNAKE_CASE` | the roadmap skill's `evals/checks.py` | Rules of the roadmap skill's own templates, the only skill that has them |
| Compatibility wording | T1 | A warning, without `previous version` and `old version`, which name an edit's baseline (Checks Run On The Sources) |
| French words, space before `%` | C3 | Applied where `language` is declared |
| 500 lines; a table of contents from 300 | Z2, Z3 | 500 lines a warning, as the Size Budgets say |

## Applied To This Repository

On 2026-10-03, by the probe and by hand, the catalogue finds in `roadmap` and
`tool-review`:

- **Two errors of X2:** the roadmap skill's `progress.py` and `check_links.py` have their
  shebang but not the executable bit. Setting the bit changes no instruction: it lands
  with X2's task, so that `make check` stays green when the audit takes over.
- **One warning of X3:** `references/close-phase.md:192` runs `check_links.py` through
  `python3`. The roadmap skill's "run with `python3`" (`SKILL.md`, Scripts) is prose
  beyond a static rule; Phase 5's audit, with the `skill-auditor`, settles both.
- `tool-review`'s `transcript.py` and `reviewfile.py`, without a shebang, are imported by
  `measure.py` and `record.py`: X2 holds.

## When To Revisit

- **Claude Code's parser,** when a release notes a change to it: run the probe's
  controls through `claude plugin validate` again.
- **The field list and its values,** when the frontmatter reference changes: F6, F7 and
  N4 follow it.
- **Severities,** after a month of the hook's reports in the tool reviews: an error
  nobody fixes becomes a warning, a warning always fixed becomes an error.
