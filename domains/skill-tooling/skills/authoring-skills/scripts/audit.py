#!/usr/bin/env python3
"""Audit skills against the platform rules and the repository's conventions.

Usage: audit.py [--portable] <skill-dir> ...

Prints each problem as path:line: [ID] message, a warning's message opening with
"warning:", then a count. Exits 1 when an error is found, 0 otherwise. --portable checks
a skill against the Agent Skills standard instead of the harness's frontmatter reference.
"""

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402  (same directory, not an installed package)

ERROR, WARNING = "error", "warning"
BOOLEAN, STRING, STRINGS, MAPPING = "a boolean", "a string", "a string or a list of strings", "a mapping"
FIELDS = {
    "name": STRING, "description": STRING, "when_to_use": STRING, "argument-hint": STRING,
    "arguments": STRINGS, "disable-model-invocation": BOOLEAN, "user-invocable": BOOLEAN,
    "allowed-tools": STRINGS, "disallowed-tools": STRINGS, "model": STRING,
    "effort": ("low", "medium", "high", "xhigh", "max"), "context": ("fork",), "agent": STRING,
    "background": BOOLEAN, "hooks": MAPPING, "paths": STRINGS, "shell": ("bash", "powershell"),
    "metadata": MAPPING, "license": STRING, "compatibility": STRING,
}
STANDARD = ("name", "description", "license", "compatibility", "metadata", "allowed-tools")
BOOLEAN_WORDS = {"true", "false", "yes", "no", "on", "off", "1", "0"}
FORK_ONLY = ("agent", "background")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_WORDS = ("anthropic", "claude")
LAX_YAML = "an agent whose parser follows YAML drops every field"


@dataclass(frozen=True)
class Problem:
    path: Path
    line: int
    rule: str
    message: str
    severity: str = ERROR

    def __str__(self):
        prefix = "warning: " if self.severity == WARNING else ""
        return f"{self.path}:{self.line}: [{self.rule}] {prefix}{self.message}"


@dataclass
class Skill:
    root: Path
    skill_md: Path
    text: str
    parsed: object
    portable: bool

    @property
    def fields(self):
        return self.parsed.fields or {}

    def line(self, key):
        return self.parsed.lines.get(key, 1)


def describe(value):
    if value is None:
        return "nothing"
    if isinstance(value, bool):
        return f"the boolean {str(value).lower()}"
    if isinstance(value, (int, float)):
        return f"the number {value}"
    if isinstance(value, list):
        return "a list"
    if isinstance(value, dict):
        return "a mapping"
    return f"the string {value!r}"


def is_boolean(value):
    if isinstance(value, bool) or value in (0, 1):
        return True
    return isinstance(value, str) and value.lower() in BOOLEAN_WORDS


def truthy(value):
    return value is True or value == 1 or (isinstance(value, str) and value.lower() in ("true", "yes", "on", "1"))


def falsy(value):
    return value is False or value == 0 or (isinstance(value, str) and value.lower() in ("false", "no", "off", "0"))


def fits(value, expected):
    if isinstance(expected, tuple):
        return isinstance(value, str) and value in expected
    if expected == BOOLEAN:
        return is_boolean(value)
    if expected == STRING:
        return isinstance(value, str)
    if expected == STRINGS:
        return isinstance(value, str) or (isinstance(value, list) and all(isinstance(v, str) for v in value))
    return isinstance(value, dict)


# Frontmatter rules: F1 to F13.

def check_parse(skill):
    """F1, F2, F3, F4 and F5: the frontmatter block and its YAML."""
    codes = {"no-opening": ("F1", "no frontmatter: open the file with `---` on its first line, or the harness "
                                  "reads it all as content"),
             "no-closing": ("F2", "the frontmatter is never closed by a `---` line"),
             "not-mapping": ("F5", "the frontmatter must be `key: value` lines")}
    for line, code, message in skill.parsed.problems:
        if code in codes:
            rule, text = codes[code]
            yield Problem(skill.skill_md, line, rule, text)
        else:
            yield Problem(skill.skill_md, line, "F3", f"{message}; {LAX_YAML}")
    for line, message in skill.parsed.outside:
        yield Problem(skill.skill_md, line, "F4", f"outside what the audit reads: {message}; its fields are not "
                                                  "checked — write it in plain form", WARNING)


def check_fields(skill):
    """F6, F7, F8 and F9: field names, types and values."""
    known = STANDARD if skill.portable else tuple(FIELDS)
    for key, value in skill.fields.items():
        line = skill.line(key)
        if key not in known:
            close = difflib.get_close_matches(key, known, n=1)
            hint = f"; did you mean `{close[0]}`?" if close else ""
            yield Problem(skill.skill_md, line, "F6", f"unknown field `{key}`, ignored without a word by the "
                                                      f"harness{hint}")
            continue
        expected = FIELDS[key]
        if key == "description" and value is None:
            continue  # N5 reports a missing description
        if not fits(value, expected):
            wanted = " or ".join(f"`{v}`" for v in expected) if isinstance(expected, tuple) else expected
            yield Problem(skill.skill_md, line, "F7", f"`{key}` must be {wanted}, got {describe(value)}")
            continue
        if skill.portable and key == "metadata" and not all(isinstance(k, str) and isinstance(v, str)
                                                            for k, v in value.items()):
            yield Problem(skill.skill_md, line, "F8", "`metadata` must map strings to strings for the Agent "
                                                      "Skills standard")
        if skill.portable and key == "allowed-tools" and not isinstance(value, str):
            yield Problem(skill.skill_md, line, "F8", "`allowed-tools` must be one space-separated string for "
                                                      "the Agent Skills standard")
        if key == "compatibility" and not 1 <= len(value) <= 500:
            yield Problem(skill.skill_md, line, "F9", f"`compatibility` is {len(value)} characters, 1 to 500")


def check_combinations(skill):
    """F10, F11, F12 and F13: fields that do nothing, clash, or lose text."""
    fields = skill.fields
    if fields.get("context") != "fork":
        for key in FORK_ONLY:
            if key in fields:
                yield Problem(skill.skill_md, skill.line(key), "F10",
                              f"`{key}` applies only with `context: fork`; here it does nothing", WARNING)
    metadata = fields.get("metadata")
    if isinstance(metadata, dict):
        for key in metadata:
            if key in FIELDS:
                yield Problem(skill.skill_md, skill.line("metadata"), "F11",
                              f"`metadata` key `{key}` repeats a field name; rename it", WARNING)
    if truthy(fields.get("disable-model-invocation")) and falsy(fields.get("user-invocable")):
        yield Problem(skill.skill_md, skill.line("user-invocable"), "F12",
                      "neither the model nor the user can invoke this skill")
    for line, key in skill.parsed.cut:
        yield Problem(skill.skill_md, line, "F13", "` #` starts a comment: the rest of the value is dropped; "
                                                   "quote the value", WARNING)


# Name and description rules: N1 to N10.

def reserved(name):
    return name.lower() == "synced" or name == "anthropic-skills" or name.startswith("anthropic-skills:")


def check_names(skill):
    """N1 to N10: the name, its folder, the description and their limits."""
    if skill.parsed.fields is None or skill.parsed.problems:
        return
    fields, folder = skill.fields, skill.root.name
    name, description = fields.get("name"), fields.get("description")
    if skill.portable and "name" not in fields:
        yield Problem(skill.skill_md, 1, "N1", "`name` is required by the Agent Skills standard")
    if isinstance(name, str):
        line = skill.line("name")
        if not NAME_RE.match(name) or len(name) > 64:
            yield Problem(skill.skill_md, line, "N2", f"`name` {name!r} must be lowercase letters, digits and "
                                                      "single inner hyphens, 64 characters at most")
        if name != folder:
            yield Problem(skill.skill_md, line, "N3", f"`name` {name!r} does not match the folder {folder!r}: other "
                                                      "agents refuse it, and Claude Code then answers to both names")
        word = next((w for w in RESERVED_WORDS if w in name.lower()), None)
        if word:
            yield Problem(skill.skill_md, line, "N8", f"`name` holds the reserved word `{word}`: claude.ai and the "
                                                      "API refuse it", ERROR if skill.portable else WARNING)
    for candidate in dict.fromkeys(n for n in (folder, name) if isinstance(n, str)):
        if reserved(candidate):
            yield Problem(skill.skill_md, skill.line("name"), "N4",
                          f"reserved name {candidate!r}: the harness skips this skill")
    if description is None or (isinstance(description, str) and not description.strip()):
        yield Problem(skill.skill_md, skill.line("description"), "N5",
                      "no description: the agent cannot tell when to use the skill")
    elif isinstance(description, str) and len(description) > 1024:
        yield Problem(skill.skill_md, skill.line("description"), "N6",
                      f"`description` is {len(description)} characters, 1,024 at most")
    for key in ("name", "description"):
        value = fields.get(key)
        if isinstance(value, str) and ("<" in value or ">" in value):
            yield Problem(skill.skill_md, skill.line(key), "N7",
                          f"`{key}` holds an angle bracket: the platform refuses XML tags")
    when = fields.get("when_to_use")
    if "when_to_use" in fields and not skill.portable:
        yield Problem(skill.skill_md, skill.line("when_to_use"), "N9",
                      "move `when_to_use` into `description`: other agents never read it", WARNING)
        if isinstance(when, str) and isinstance(description, str) and len(description) + len(when) > 1536:
            yield Problem(skill.skill_md, skill.line("when_to_use"), "N10",
                          f"`description` and `when_to_use` are {len(description) + len(when)} characters; the "
                          "listing cuts at 1,536")


CHECKS = (check_parse, check_fields, check_combinations, check_names)


def load(root, portable=False):
    root = Path(root)
    skill_md = root / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    return Skill(root, skill_md, text, frontmatter.parse(text), portable)


def audit(root, portable=False, conventions=None):
    """Every problem of the skill at root, errors and warnings, in rule order."""
    skill = load(root, portable)
    return [problem for check in CHECKS for problem in check(skill)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit skills against the platform rules and the repository's "
                                                 "conventions.")
    parser.add_argument("--portable", action="store_true", help="check against the Agent Skills standard")
    parser.add_argument("skills", nargs="+", type=Path)
    args = parser.parse_args(argv)
    errors = warnings = 0
    for root in args.skills:
        for problem in audit(root, portable=args.portable):
            print(problem)
            errors += problem.severity == ERROR
            warnings += problem.severity == WARNING
    count = len(args.skills)
    print(f"{count} skill{'s' if count != 1 else ''} audited, {errors} error{'s' if errors != 1 else ''}, "
          f"{warnings} warning{'s' if warnings != 1 else ''}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
