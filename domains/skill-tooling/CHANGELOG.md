# Changelog — skill-tooling

## 0.1.0 — unreleased

- Domain created, to hold the tool that creates, edits, audits and evaluates skills: `VERSION`, this changelog and `permissions.json`.
- Skill `authoring-skills`, with a first `SKILL.md` for its audit: `scripts/audit.py <skill-dir>` checks the frontmatter rules F1 to F13 and the name and description rules N1 to N10 of the catalogue of 2026-10-03, `--portable` against the Agent Skills standard; `scripts/frontmatter.py`, copied from `shared/frontmatter/`, reads frontmatter as a strict subset of YAML. Its allow rule is in `permissions.json`.
