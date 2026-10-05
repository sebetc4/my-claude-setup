# Changelog — skill-tooling

## 0.1.0 — unreleased

- Domain created, to hold the tool that creates, edits, audits and evaluates skills: `VERSION`, this changelog and `permissions.json`.
- Skill `authoring-skills`, with a first `SKILL.md` for its audit: `scripts/audit.py <skill-dir>` checks the frontmatter rules F1 to F13 and the name and description rules N1 to N10 the size rules Z1 to Z4, the resource rules R1 to R4, the execution rules X1 to X7, the text rule T1 and, where the repository's `.agent-conventions.toml` declares them, the convention rules C1 to C7 of the catalogue of 2026-10-03; `--portable` checks against the Agent Skills standard, `--checks` runs the repository's check commands. `scripts/frontmatter.py`, copied from `shared/frontmatter/`, reads frontmatter as a strict subset of YAML; `scripts/conventions.py` and `references/conventions.md`, copied from `shared/conventions/`, read the conventions. Its allow rule is in `permissions.json`.
- Rule C1 leaves out the `[skills] workspace`, where eval runs put their copies and outputs.
- Hook `audit_skill.py` (PostToolUse on Edit, Write and MultiEdit): audits the skill that holds the edited file and, on errors, exits 2 with one line per failing rule; warnings, a clean skill and a file outside any skill stay silent.
