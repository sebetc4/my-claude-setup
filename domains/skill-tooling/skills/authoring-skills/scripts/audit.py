#!/usr/bin/env python3
"""Audit skills against the platform rules and the repository's conventions.

Usage: audit.py [--portable] <skill-dir> ...

Prints each problem as path:line: [ID] message, a warning's message opening with
"warning:", then a count. Exits 1 when an error is found, 0 otherwise. --portable checks
a skill against the Agent Skills standard instead of the harness's frontmatter reference.
"""

import argparse
import difflib
import os
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
RESOURCE_RE = re.compile(r"(?<![\w./-])((?:references|assets|scripts)/[\w./-]*\w\.\w+)")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
OUTSIDE_RE = re.compile(r"(?<![\w./-])(\.\./[\w./-]*\w)")
BACKSLASH_RE = re.compile(r"(?<![\w.\\-])((?:references|assets|scripts)\\[\w.\\-]*\w)")
MODULE_RE = re.compile(r"-m\s+(scripts(?:\.\w+)+)")
IMPORT_RE = re.compile(r"^\s*(?:from\s+(\.*[\w.]*)\s+import|import\s+([\w., ]+))", re.M)
TOKEN_RE = re.compile(r"[\w.-]+(?:/[\w.-]+)*")
FENCE_RE = re.compile(r"^```.*?^```[^\n]*$", re.M | re.S)
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
EVALS = "evals"
CONTENTS_RE = re.compile(r"^## (Contents|Table of Contents)\s*$", re.M)
BODY_TOKENS, SKILL_LINES, CONTENTS_LINES = 5000, 500, 300
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

    @property
    def body(self):
        if self.parsed.fields is None and self.parsed.problems and self.parsed.problems[0][1] == "no-opening":
            return self.text
        return "\n".join(self.text.split("\n")[self.parsed.body_line - 1:])

    def files(self, folder="."):
        """The skill's files under folder, without its evaluations, caches and hidden files."""
        base = self.root / folder
        if not base.is_dir():
            return []
        found = []
        for path in base.rglob("*"):
            parts = path.relative_to(self.root).parts
            if (path.is_file() and parts[0] != EVALS and "__pycache__" not in parts
                    and not any(part.startswith(".") for part in parts) and path.suffix != ".pyc"):
                found.append(path)
        return sorted(found)


def cited(text):
    """The paths under references/, assets/ or scripts/ a text cites."""
    return {m.group(1) for m in RESOURCE_RE.finditer(text)}


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


# Size rules: Z1 to Z4.

def check_sizes(skill):
    """Z1 to Z4: the body's tokens, SKILL.md's lines, long references and their depth."""
    tokens = len(skill.body) // 4
    if tokens > BODY_TOKENS:
        yield Problem(skill.skill_md, skill.parsed.body_line, "Z1",
                      f"the body is about {tokens} tokens, {BODY_TOKENS:,} at most: compaction keeps only the first "
                      f"{BODY_TOKENS:,}; move detail to `references/`")
    lines = len(skill.text.splitlines())
    if lines > SKILL_LINES:
        yield Problem(skill.skill_md, 1, "Z2", f"`SKILL.md` is {lines} lines; {SKILL_LINES} is the alert", WARNING)
    references = [p for p in skill.files("references") if p.suffix == ".md"]
    for path in references:
        text = path.read_text(encoding="utf-8")
        count = len(text.splitlines())
        if count >= CONTENTS_LINES and not CONTENTS_RE.search(text):
            yield Problem(path, 1, "Z3", f"{count} lines without a `## Contents` section")
    from_skill = cited(skill.text)
    for path in references:
        relative = path.relative_to(skill.root).as_posix()
        if relative in from_skill:
            continue
        through = [other for other in references if other != path
                   and relative in cited(other.read_text(encoding="utf-8"))]
        if through:
            yield Problem(path, 1, "Z4", f"reached only through `{through[0].relative_to(skill.root).as_posix()}`: "
                                         "cite it from `SKILL.md`", WARNING)


# Resource rules: R1 to R4.

def line_at(text, index):
    return text.count("\n", 0, index) + 1


def outside_fences(text):
    """The text with its fenced code blocks blanked, line breaks kept."""
    return FENCE_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def citations(skill, path, text):
    """(kind, target, line, cited) for each citation of a Markdown file: kind "file" with the
    resolved path, "outside" for one leaving the skill, "backslash" for a Windows-style path."""
    root = skill.root.resolve()
    for m in RESOURCE_RE.finditer(text):
        yield "file", skill.root / m.group(1), line_at(text, m.start()), m.group(1)
    for m in OUTSIDE_RE.finditer(text):
        target = (path.parent / m.group(1)).resolve()
        if not target.is_relative_to(root):
            yield "outside", None, line_at(text, m.start()), m.group(1)
    for m in LINK_RE.finditer(outside_fences(text)):
        raw = m.group(1)
        if SCHEME_RE.match(raw) or raw.startswith(("#", "/")) or "<" in raw or "{{" in raw:
            continue
        cleaned = raw.split("#")[0].split("?")[0]
        if not cleaned or cleaned.startswith("../"):
            continue
        beside = Path(os.path.normpath(path.parent / cleaned))
        from_root = Path(os.path.normpath(skill.root / cleaned))
        yield "file", beside if beside.exists() or not from_root.exists() else from_root, line_at(text, m.start()), raw
    for m in BACKSLASH_RE.finditer(text):
        yield "backslash", None, line_at(text, m.start()), m.group(1)


def reached(skill):
    """The files reached from SKILL.md: any path of the skill a reached file names — relative
    to its folder or to the skill, or a file name the skill holds once —, Python imports,
    -m module names, and the license field."""
    root = Path(os.path.normpath(skill.root))
    files = set(skill.files())
    by_name = {}
    for path in files:
        by_name.setdefault(path.name, []).append(path)

    def resolve(token, folder):
        """The skill file a path token names: the path itself, then each shorter tail of it,
        relative to the citing file's folder or to the skill; a bare name held once."""
        token = token.rstrip(".")
        if "/" not in token and "." not in token:
            return []
        parts = token.split("/")
        for i in range(len(parts)):
            tail = "/".join(parts[i:])
            for base in (folder, root):
                candidate = Path(os.path.normpath(base / tail))
                if candidate in files:
                    return [candidate]
                if "/" in tail and candidate.is_dir() and candidate.is_relative_to(root) and candidate != root:
                    return [f for f in files if f.is_relative_to(candidate)]
        return by_name[parts[-1]] if len(by_name.get(parts[-1], [])) == 1 else []

    def module(name, folder):
        dots = len(name) - len(name.lstrip("."))
        parts = [p for p in name.lstrip(".").split(".") if p]
        bases = [folder.joinpath(*[".."] * max(dots - 1, 0))] if dots else [folder, root]
        found = []
        for base in bases:
            for i in range(1, len(parts) + 1):
                package = Path(os.path.normpath(base.joinpath(*parts[:i])))
                found += [p for p in (package.with_suffix(".py"), package / "__init__.py") if p in files]
        return found

    seen, queue = set(), [Path(os.path.normpath(skill.skill_md))]
    while queue:
        current = queue.pop()
        if current in seen or not current.is_file():
            continue
        seen.add(current)
        text = current.read_text(encoding="utf-8", errors="replace")
        for m in TOKEN_RE.finditer(text):
            queue.extend(resolve(m.group(0), current.parent))
        if current.suffix == ".md":
            queue.extend(Path(os.path.normpath(t)) for kind, t, _, _ in citations(skill, current, text) if kind == "file")
            for m in MODULE_RE.finditer(text):
                queue.extend(module(m.group(1), root))
        elif current.suffix == ".py":
            for m in IMPORT_RE.finditer(text):
                names = [m.group(1)] if m.group(1) else [n.strip().split(" ")[0] for n in m.group(2).split(",")]
                for name in names:
                    queue.extend(module(name, current.parent))
    return seen


def check_resources(skill):
    """R1 to R4: cited files exist inside the skill, every file is reached, paths use forward slashes."""
    for path in [skill.skill_md] + [p for p in skill.files() if p.suffix == ".md" and p != skill.skill_md]:
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, target, line, raw in dict.fromkeys(citations(skill, path, text)):
            if kind == "file" and not target.exists():
                yield Problem(path, line, "R1", f"cites `{raw}`, which does not exist")
            elif kind == "outside":
                yield Problem(path, line, "R2", f"cites `{raw}`, outside the skill: it breaks wherever the skill "
                                                "is installed alone", WARNING)
            elif kind == "backslash":
                yield Problem(path, line, "R4", f"`{raw}` uses backslashes: write it with forward slashes", WARNING)
    found = reached(skill)
    for path in skill.files():
        if path != skill.skill_md and Path(os.path.normpath(path)) not in found:
            yield Problem(path, 1, "R3", "not reached from `SKILL.md`: no file cites it")


CHECKS = (check_parse, check_fields, check_combinations, check_names, check_sizes, check_resources)


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
