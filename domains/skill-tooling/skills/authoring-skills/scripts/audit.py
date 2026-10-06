#!/usr/bin/env python3
"""Audit skills against the platform rules and the repository's conventions.

Usage: audit.py [--portable] [--checks] <skill-dir> ...

Prints each problem as path:line: [ID] message, a warning's message opening with
"warning:", then a count. Exits 1 when an error is found, 0 otherwise. --portable checks
a skill against the Agent Skills standard instead of the harness's frontmatter reference;
--checks also runs the repository's check commands. The repository's conventions come
from its .agent-conventions.toml, read by conventions.py; without a valid [skills] table,
no convention rule applies.
"""

import argparse
import difflib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the skill's folder, installed or not
sys.path.insert(0, str(Path(__file__).resolve().parent))
import conventions  # noqa: E402  (same directory, not an installed package)
import frontmatter  # noqa: E402

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
AGENT_FIELDS = {"tools": "allowed-tools"}  # an agent's field, written in a skill
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
INJECTED_RE = re.compile(r"(?:^|(?<=\s))!`([^`\n]+)`", re.M)
INJECTED_BLOCK_RE = re.compile(r"^```!\s*\n(.*?)^```", re.M | re.S)
INTERPRETER_RE = re.compile(r"\b(python3?|bash|sh|node|ruby|perl)\s+(?:-\S+\s+)*[\"']?[^\s\"'`]*?(scripts/[\w./-]*\w)")
AT_RE = re.compile(r"(?:^|(?<=\s))@([\w./-]*\w)")
ULTRATHINK_RE = re.compile(r"\bultrathink\b", re.I)
MONEY_RE = re.compile(r"(?<!\\)\$\d+[.,]\d+")
ARGUMENT_RE = re.compile(r"(?<!\\)\$(?:ARGUMENTS\b|\d+)")
SUBSTITUTION_RE = re.compile(r"(?<!\\)\$(?:ARGUMENTS\b|\d+|\{CLAUDE_\w+\})")
FRENCH_RE = re.compile(r"\b(le|la|les|des|une|est|sont|dans|pour|avec|qui|que|cette|doit|faut|chaque|toute)\b", re.I)
PERCENT_RE = re.compile(r"\d %")
MODEL_RE = re.compile(r"\bClaude\b(?!\s+Code)|\b(?:Opus|Sonnet|Haiku|Fable)\b")
EVAL_FILE_RE = re.compile(r"^(evals\.json|checks\.py|test_.*\.py)$")
COMPATIBILITY_RE = re.compile(r"\blegacy\b|backwards?[- ]compat|\bpre-existing\b|\bbefore (this|the) feature\b"
                              r"|\bdeprecated\b", re.I)
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
    conventions: dict
    repo: Path | None

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

    @property
    def evals(self):
        return self.conventions.get("evals", EVALS)

    def markdown(self):
        return [self.skill_md] + [p for p in self.files() if p.suffix == ".md" and p != self.skill_md]

    def files(self, folder="."):
        """The skill's files under folder, without its evaluations, caches and hidden files."""
        base = self.root / folder
        if not base.is_dir():
            return []
        found = []
        for path in base.rglob("*"):
            parts = path.relative_to(self.root).parts
            if (path.is_file() and parts[0] != self.evals and "__pycache__" not in parts
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
            close = [AGENT_FIELDS[key]] if AGENT_FIELDS.get(key) in known else difflib.get_close_matches(key, known, n=1)
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
    fields, folder = skill.fields, skill.root.resolve().name
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


# Execution rules: X1 to X7.

def body_line(skill, index):
    return skill.parsed.body_line - 1 + line_at(skill.body, index)


def split_rules(value):
    """The rules of an allowed-tools value: a list, or a string split on spaces and commas
    outside parentheses."""
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    rules, depth, current = [], 0, ""
    for c in value if isinstance(value, str) else "":
        depth += (c == "(") - (c == ")")
        if c in " ," and depth == 0:
            rules.append(current); current = ""
        else:
            current += c
    return [r for r in rules + [current] if r]


def imported(script, others):
    """Whether another script imports this module — a package marker with its package — or
    names this file."""
    module = script.parent.name if script.name == "__init__.py" else script.stem
    for other in others:
        text = other.read_text(encoding="utf-8", errors="replace")
        if script.name != "__init__.py" and script.name in text:
            return True
        for m in IMPORT_RE.finditer(text) if other.suffix == ".py" else ():
            names = [m.group(1)] if m.group(1) else [n.strip().split(" ")[0] for n in m.group(2).split(",")]
            for name in names:
                if module in name.strip(".").split(".") or (script.name == "__init__.py" and name.startswith(".")
                                                             and other.parent == script.parent):
                    return True
    return False


def check_execution(skill):
    """X1 to X7: injected commands, scripts and how they run, allowed-tools, @ references,
    ultrathink, and the $ the harness replaces."""
    body = skill.body
    commands = [(m.start(), m.group(1)) for m in INJECTED_RE.finditer(body)]
    for m in INJECTED_BLOCK_RE.finditer(body):
        commands += [(m.start(), line) for line in m.group(1).splitlines() if line.strip()]
    for index, command in commands:
        if not command.rstrip().endswith("|| true"):
            yield Problem(skill.skill_md, body_line(skill, index), "X1", "an injected command that exits non-zero "
                          "aborts the whole skill: make it exit 0, or append `|| true`", WARNING)
    scripts = skill.files("scripts")
    for script in scripts:
        relative = script.relative_to(skill.root).as_posix()
        with open(script, "rb") as handle:
            shebang = handle.read(2) == b"#!"
        if shebang and not os.access(script, os.X_OK):
            yield Problem(script, 1, "X2", f"`{relative}` has a shebang but not the executable bit")
        elif not shebang and not imported(script, [s for s in scripts if s != script]):
            yield Problem(script, 1, "X2", f"`{relative}` has no shebang and no script imports it")
    for path in [skill.skill_md] + [p for p in skill.files() if p.suffix == ".md" and p != skill.skill_md]:
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in INTERPRETER_RE.finditer(text):
            if (skill.root / m.group(2)).is_file():
                yield Problem(path, line_at(text, m.start()), "X3",
                              f"`{m.group(2)}` is run through `{m.group(1)}`: call it by its path", WARNING)
    for rule in split_rules(skill.fields.get("allowed-tools")):
        m = re.fullmatch(r"Bash\((.*)\)", rule)
        prefix = re.sub(r"(:\*|\s*\*)$", "", m.group(1)).strip() if m else ""
        if prefix and prefix not in body:
            yield Problem(skill.skill_md, skill.line("allowed-tools"), "X4",
                          f"`allowed-tools` rule `{rule}` matches no command of the skill", WARNING)
    for m in AT_RE.finditer(body):
        if (skill.root / m.group(1)).is_file():
            yield Problem(skill.skill_md, body_line(skill, m.start()), "X5",
                          f"`@{m.group(1)}` attaches the file at every invocation: cite it by its path", WARNING)
    m = ULTRATHINK_RE.search(body)
    if m:
        yield Problem(skill.skill_md, body_line(skill, m.start()), "X6", "`ultrathink` turns on deep reasoning at "
                      "every invocation: remove it unless meant", WARNING)
    expects = "arguments" in skill.fields or "argument-hint" in skill.fields
    tokens = {m.start(): m.group(0) for m in MONEY_RE.finditer(body)}
    if not expects:
        tokens.update({m.start(): m.group(0) for m in ARGUMENT_RE.finditer(body) if m.start() not in tokens})
    for index, token in sorted(tokens.items()):
        yield Problem(skill.skill_md, body_line(skill, index), "X7",
                      f"`{token}` is replaced when the skill gets arguments: write `\\{token}`", WARNING)


# Repository conventions: C1 to C7, where .agent-conventions.toml declares the key.

def key_line(path, key):
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if re.match(rf"\s*{re.escape(key)}\s*=", line):
            return number
    return 1


def check_conventions(skill, run_checks=False):
    """C1 to C7: where skills and evals live, language, addressee, excluded features, the
    eval workspace, and the repository's check commands."""
    values, repo = skill.conventions, skill.repo
    if repo is None:
        return
    file = repo / conventions.FILE
    if "dirs" in values:
        folders = {Path(os.path.normpath(p)).resolve() for d in values["dirs"] for p in repo.glob(d) if p.is_dir()}
        root = skill.root.resolve()
        # Eval runs put their copies and outputs under the workspace, by design.
        in_workspace = "workspace" in values and (repo / values["workspace"]).resolve() in root.parents
        if root.parent not in folders and not in_workspace:
            yield Problem(skill.skill_md, 1, "C1", f"`{skill.root.name}` is outside the skill folders "
                                                   f"{', '.join(values['dirs'])}")
    if "evals" in values:
        for path in skill.files():
            if EVAL_FILE_RE.match(path.name):
                yield Problem(path, 1, "C2", f"`{path.name}` belongs in `{values['evals']}/`")
    if values.get("language", "").lower() == "english":
        for path in skill.markdown():
            text = path.read_text(encoding="utf-8", errors="replace")
            for m in FRENCH_RE.finditer(text):
                yield Problem(path, line_at(text, m.start()), "C3",
                              f"`{m.group(0)}`: skill files are written in english")
            for m in PERCENT_RE.finditer(text):
                yield Problem(path, line_at(text, m.start()), "C3", "space before `%`: English takes none")
    if values.get("address") == "agent":
        for path in skill.markdown():
            text = path.read_text(encoding="utf-8", errors="replace")
            for m in MODEL_RE.finditer(text):
                yield Problem(path, line_at(text, m.start()), "C4", f"`{m.group(0)}` names a model: address the agent")
    excluded = values.get("exclude", [])
    if "allowed-tools" in excluded and "allowed-tools" in skill.fields:
        yield Problem(skill.skill_md, skill.line("allowed-tools"), "C5",
                      "`allowed-tools` is excluded by the repository's conventions")
    if "dynamic-context" in excluded:
        body = skill.body
        found = [m.start() for m in INJECTED_RE.finditer(body)] + [m.start() for m in INJECTED_BLOCK_RE.finditer(body)]
        for index in sorted(found):
            yield Problem(skill.skill_md, body_line(skill, index), "C5",
                          "an injected command: `dynamic-context` is excluded by the repository's conventions")
    if "substitutions" in excluded:
        for m in SUBSTITUTION_RE.finditer(skill.body):
            yield Problem(skill.skill_md, body_line(skill, m.start()), "C5",
                          f"`{m.group(0)}`: `substitutions` is excluded by the repository's conventions")
    if "workspace" in values:
        probe = subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", f"{values['workspace']}/x"],
                               capture_output=True)
        if probe.returncode == 1:
            yield Problem(file, key_line(file, "workspace"), "C6", f"the eval workspace `{values['workspace']}` is not "
                                                                   "ignored by git: runs would land in commits")
    if run_checks:
        for check in values.get("checks", []):
            result = subprocess.run(check["run"], shell=True, cwd=repo / check["dir"], capture_output=True, text=True)
            if result.returncode:
                head = " / ".join((result.stdout + result.stderr).strip().splitlines()[:3])
                yield Problem(file, key_line(file, "checks"), "C7", f"`{check['run']}` failed: {head}")


# Text rule: T1.

def check_text(skill):
    """T1: compatibility wording, a skill stating only its target behavior."""
    for path in skill.markdown():
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in COMPATIBILITY_RE.finditer(text):
            yield Problem(path, line_at(text, m.start()), "T1", f"compatibility wording `{m.group(0)}`: a skill "
                                                                 "states only its target behavior", WARNING)


CHECKS = (check_parse, check_fields, check_combinations, check_names, check_sizes, check_resources, check_execution,
          check_text)


def load(root, portable=False):
    root = Path(root)
    skill_md = root / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    found = conventions.read("skills", root)
    values, repo = (found.values, found.root) if found.status == "ok" else ({}, None)
    return Skill(root, skill_md, text, frontmatter.parse(text), portable, values, repo)


def audit(root, portable=False, checks=False):
    """Every problem of the skill at root, errors and warnings, in rule order."""
    skill = load(root, portable)
    problems = [problem for check in CHECKS for problem in check(skill)]
    return problems + list(check_conventions(skill, checks))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit skills against the Agent Skills standard, the harness's "
                                                 "rules and the repository's conventions.")
    parser.add_argument("--portable", action="store_true", help="check against the Agent Skills standard")
    parser.add_argument("--checks", action="store_true", help="also run the repository's check commands")
    parser.add_argument("skills", nargs="+", type=Path)
    args = parser.parse_args(argv)
    problems = dict.fromkeys(p for root in args.skills for p in audit(root, args.portable, args.checks))
    errors = warnings = 0
    for problem in problems:
        print(problem)
        errors += problem.severity == ERROR
        warnings += problem.severity == WARNING
    count = len(args.skills)
    print(f"{count} skill{'s' if count != 1 else ''} audited, {errors} error{'s' if errors != 1 else ''}, "
          f"{warnings} warning{'s' if warnings != 1 else ''}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
