# Agent Skills

The open standard for skills: what a skill folder holds, how its `SKILL.md` is written,
and how an agent discovers and loads it. Read from https://agentskills.io on 2026-10-06;
the site's page index is https://agentskills.io/llms.txt. The standard defines the format
only: where skills are installed is each client's choice, with one shared convention,
below.

## The Skill Format

From the [specification](https://agentskills.io/specification):

| Item | Rule | Section |
|---|---|---|
| Folder | Holds `SKILL.md`; optionally `scripts/` (code agents run), `references/` (documentation read on demand), `assets/` (templates, images, data), and any other file | Directory structure, Optional directories |
| Frontmatter | YAML between `---` lines at the top of `SKILL.md`, then a Markdown body | `SKILL.md` format |
| `name` | Required; 1 to 64 characters; lowercase letters, digits and hyphens; no hyphen at either end and no two in a row; matches the folder's name | `name` field |
| `description` | Required; 1 to 1,024 characters; says what the skill does and when to use it, with the keywords that let an agent match a task | `description` field |
| `license` | Optional; a license name or a bundled license file | `license` field |
| `compatibility` | Optional; 1 to 500 characters; environment requirements, such as the intended product, packages or network access | `compatibility` field |
| `metadata` | Optional; a map of string keys to string values, for client-specific properties | `metadata` field |
| `allowed-tools` | Optional; a space-separated list of pre-approved tools; experimental, its support varies between agents | `allowed-tools` field |
| Body | Markdown with no format restriction; the agent loads the whole file once it activates the skill | Body content |
| Loading | Name and description of every skill at startup, about 100 tokens each; the body on activation, under 5,000 tokens recommended; other files only when needed; `SKILL.md` under 500 lines | Progressive disclosure |
| File references | Paths relative to the skill's root; references one level deep from `SKILL.md` | File references |
| Validation | `skills-ref validate <skill-dir>`, from the standard's reference library | Validation |

## Where Clients Look For Skills

From the [client implementation guide](https://agentskills.io/client-implementation/adding-skills-support),
Step 1:

- Two scopes at least: the project, relative to the working directory, and the user,
  relative to the home directory.
- In each scope, the client's own folder, `.<client>/skills/`, and the shared
  `.agents/skills/`, "a widely-adopted convention for cross-client skill sharing". Some
  clients also scan `.claude/skills/`, where many skills already live.
- A skill is a subfolder holding a file named exactly `SKILL.md`.
- On a name collision, the project's skill overrides the user's.
- Project skills may come from an untrusted repository: the guide advises loading them
  only once the user trusts the folder.
- Loading is lenient: a name that does not match its folder or is too long gets a
  warning, a missing description or unparseable YAML skips the skill. Skills written for
  other clients may hold YAML that only their parser accepts, such as an unquoted value
  holding a colon.

## How Clients Use A Skill

From the same guide, Steps 3 to 5:

- **Catalog.** Name, description and optionally the location of every skill, about 50
  to 100 tokens each, in the system prompt or in an activation tool's description. A
  skill the user disabled, or one that opts out of model invocation, is left out of the
  catalog entirely.
- **Activation.** By the model reading `SKILL.md` with its file tool, or through a
  dedicated tool; by the user with a slash command or a mention. Relative paths resolve
  against the skill's folder.
- **Resources.** Listed, never read ahead; skill folders are allowlisted so that reading
  a bundled file needs no permission prompt.
- **Over time.** Skill content is protected from context compaction, and a skill already
  in context is not loaded twice. Running a skill in a subagent is an optional pattern
  that some clients support.

## The Guides

Agent-neutral guidance on writing and testing skills, beside the specification:

| Page | What it covers |
|---|---|
| [Best practices](https://agentskills.io/skill-creation/best-practices) | Start from real expertise and refine with real runs, reading their traces; add what the agent lacks and omit what it knows; moderate detail; tell the agent when to load each file; match specificity to fragility; defaults, not menus; gotchas sections; output templates; checklists, validation loops, plan-validate-execute; bundle the script runs keep rewriting |
| [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) | About 20 trigger queries, half that should trigger and half near misses that should not; each run 3 times, a trigger rate against a 0.5 threshold; a fixed 60/40 train and validation split; about five iterations, the best chosen on the validation set |
| [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) | Cases in `evals/evals.json` (prompt, expected output, files), two or three at first; each run with and without the skill, or with the previous version; assertions checkable from the output, and a person's review for what needs judgment; grading with evidence; a benchmark of means, deviations and deltas |
| [Using scripts](https://agentskills.io/skill-creation/using-scripts) | Pinned one-off commands; scripts cited by paths from the skill's root; dependencies declared inline; no interactive prompt; `--help`; error messages that say what to try; structured output on stdout and diagnostics on stderr; documented exit codes; dry runs; bounded output, since harnesses cut long output |
| [Quickstart](https://agentskills.io/skill-creation/quickstart) | A first skill, shown in VS Code |

## Who Implements It

46 clients on the [client page](https://agentskills.io/clients) on 2026-10-06, among
them Claude Code and Claude, ChatGPT and Codex, Gemini CLI, Cursor, GitHub Copilot and
VS Code, OpenCode, OpenHands, Goose, Amp, Junie, Kiro, Roo Code, Factory, Letta, Tabnine
and Mistral AI Vibe. Most entries link the client's own setup page.

## Where This Setup Stands

- `authoring-skills` audits a skill against this standard with
  `scripts/audit.py --portable`, and against Claude Code's profile on top of it by
  default: rules of `docs/decisions/2026-10-03-skill-audit-rules.md`.
- This setup installs global skills into `~/.claude/skills/`, and a repository keeps its
  own where its `[skills]` conventions say: Claude Code reads neither `.agents/skills/`
  nor `~/.agents/skills/` ([claude-code.md](claude-code.md), Skills).
- The settled rules of `docs/decisions/2026-09-28-skill-tooling.md` depart from the
  guides in four places, the documentation informing without capping (`CLAUDE.md`,
  Principles):
  - Descriptions: the guide asks for imperative phrasing, "Use this skill when…" rather
    than "This skill does…", and to "err on the side of being pushy"; the Description
    rules ask for what the skill does, then when to use it, in the third person, with
    breadth decided by trigger measurements.
  - Scripts: the guide's examples call scripts through an interpreter,
    `python3 scripts/process.py`; the Scripts rule makes each an executable called by
    its path, which Claude Code's permission rules can name and which a project hook
    refusing `python3` lets through.
  - Output: the guide prefers structured output, JSON or CSV; the Scripts rule says
    plain text, with documented exit codes.
  - Evaluation: the guide puts the workspace beside the skill's folder, writes the
    assertions after the first runs, and records tokens from the task notification's
    `total_tokens`; this setup puts the workspace where the `[skills]` conventions say,
    writes the assertions from the failures of the runs without the skill, and counts a
    run's cost from its transcript, `total_tokens` being the size of its last context
    (Phase 3 of roadmap `skill-tooling`).
- Agreed with the guides: what the agent already knows stays out; one default rather
  than a menu; the trigger measurement's near misses, repetitions and held-out queries;
  bundling the scripts runs keep rewriting; a person's review for what no assertion can
  check, which Phase 4 of roadmap `skill-tooling` carries.

## Refreshing This File

Fetch https://agentskills.io/llms.txt and compare its pages with the ones cited here;
fetch https://agentskills.io/specification.md and compare its frontmatter table with the
one above. Update the date at the top with what changed.
