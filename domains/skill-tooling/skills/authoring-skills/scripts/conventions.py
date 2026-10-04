#!/usr/bin/env python3
"""Read a repository's .agent-conventions.toml for one tool, and print its table resolved.

Usage: conventions.py <tool> [--from <path>]
       conventions.py <tool> --write <draft> [--root <dir>]

The root is the first directory, from <path> (the working directory by default) upwards,
that holds .agent-conventions.toml or .git; inside the personal directory
($CLAUDE_CONFIG_DIR, otherwise ~/.claude), the root is that directory. The first line
printed is the status: ok, missing, invalid, no-root or error. On ok, the tool's table
follows, resolved against the shared keys, in TOML; otherwise one problem per line.
Exits 0 in every case, an unexpected error included.

--write validates a draft as the reader does, writes it as the root's
.agent-conventions.toml, never over an existing file, and adds the file to the root's
.gitignore when the root holds .git. --root names the root when none is found.

One source in shared/conventions/ of my-claude-setup, copied into each tool that reads
the file; edit the source, never a copy.
"""

import difflib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

FILE = ".agent-conventions.toml"
EXCLUDABLE = ("allowed-tools", "dynamic-context", "substitutions")

# key: (kind, allowed values or None). Kinds: string, path, paths, strings, checks.
SHARED = {
    "language": ("string", None),
    "versioning": ("string", ("git", "none")),
    "residue": ("paths", None),
    "checks": ("checks", None),
}
TOOLS = {
    "roadmap": {
        "shared": ("language", "versioning", "residue", "checks"),
        "keys": {"root": ("path", None)},
        "required": ("language", "versioning", "root"),
    },
    "skills": {
        "shared": ("language", "checks"),
        "keys": {"dirs": ("paths", None), "evals": ("path", None), "workspace": ("path", None),
                 "address": ("string", ("agent",)), "exclude": ("strings", EXCLUDABLE)},
        "required": ("dirs",),
    },
}
TABLE_RE = re.compile(r"^\s*\[\s*([^\]\s]+)\s*\]\s*(#.*)?$")
TOML_LINE_RE = re.compile(r"\s*\(at line (\d+), column \d+\)\s*$")
TYPE_NAMES = {str: "a string", int: "an integer", float: "a float", bool: "a boolean", list: "a list", dict: "a table"}


@dataclass
class Result:
    status: str
    root: Path = None
    file: Path = None
    tool: str = None
    values: dict = field(default_factory=dict)
    undeclared: list = field(default_factory=list)
    problems: list = field(default_factory=list)
    written: Path = None
    gitignore: Path = None


def personal_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def find_root(start, personal=None):
    """The directory that holds the conventions for start, or None."""
    start = Path(start).resolve()
    personal = Path(personal if personal is not None else personal_dir()).resolve()
    if start.is_relative_to(personal):
        return personal
    for directory in (start, *start.parents):
        if (directory / FILE).is_file() or (directory / ".git").exists():
            return directory
    return None


def suggestion(name, candidates, form="{}"):
    close = difflib.get_close_matches(name, list(candidates), n=1)
    return f"; did you mean {form.format(close[0])}?" if close else ""


def type_name(value):
    return next((name for kind, name in TYPE_NAMES.items() if type(value) is kind), "a date")


def key_lines(text):
    """{(table or None, key): line number} for every `key =` line of the file."""
    lines, table = {}, None
    for number, line in enumerate(text.splitlines(), 1):
        header = TABLE_RE.match(line)
        if header:
            table = header.group(1)
            continue
        key = re.match(r"""^\s*["']?([A-Za-z0-9_-]+)["']?\s*=""", line)
        if key:
            lines.setdefault((table, key.group(1)), number)
    return lines


def is_relative(path):
    return bool(path) and not path.startswith("/") and ".." not in path.split("/")


def check_value(name, value, kind, allowed):
    """The problems of one value, without the line prefix; the normalized value when none."""
    if kind in ("string", "path"):
        if not isinstance(value, str):
            return [f"{name} must be a string, got {type_name(value)}"], None
        if kind == "path" and not is_relative(value):
            return [f'{name} = "{value}" must be relative to the root, without ".."'], None
        if allowed and value not in allowed:
            return [f'{name} = "{value}" is not one of ' + ", ".join(f'"{a}"' for a in allowed)], None
        if not value:
            return [f"{name} must not be empty"], None
        return [], value
    if kind == "checks":
        if not isinstance(value, list):
            return [f"{name} must be a list, got {type_name(value)}"], None
        checks = []
        for item in value:
            if isinstance(item, str) and item:
                checks.append({"run": item, "dir": "."})
            elif (isinstance(item, dict) and set(item) <= {"run", "dir"}
                  and isinstance(item.get("run"), str) and item["run"]
                  and isinstance(item.get("dir", "."), str) and is_relative(item.get("dir", "."))):
                checks.append({"run": item["run"], "dir": item.get("dir", ".")})
            else:
                return [f"{name} must hold strings or {{ run, dir }} tables"], None
        return [], checks
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return [f"{name} must be a list of strings, got {type_name(value)}"], None
    problems = []
    for item in value:
        if kind == "paths" and not is_relative(item):
            problems.append(f'{name} = "{item}" must be relative to the root, without ".."')
        elif allowed and item not in allowed:
            problems.append(f'{name} = "{item}" is not one of ' + ", ".join(f'"{a}"' for a in allowed))
    return problems, (None if problems else list(value))


def validate(tool, data, text):
    """(values, undeclared, problems) for tool's table resolved against the shared keys."""
    spec, lines = TOOLS[tool], key_lines(text)
    problems, shared, own, present = [], {}, {}, {}

    def line(table, key):
        number = lines.get((table, key))
        return f"line {number}: " if number else ""

    for key, value in data.items():
        if isinstance(value, dict):
            continue
        if key not in SHARED:
            problems.append(f"{line(None, key)}{key} is not a shared key" + suggestion(key, SHARED))
            continue
        present[key] = None
        found, normalized = check_value(key, value, *SHARED[key])
        if normalized is None:
            problems.extend(line(None, key) + p for p in found)
        else:
            shared[key] = normalized

    table = data.get(tool)
    if not isinstance(table, dict):
        tables = [k for k, v in data.items() if isinstance(v, dict)]
        close = difflib.get_close_matches(tool, tables, n=1)
        problems.append(f"no [{tool}] table" + (f"; found [{close[0]}], did you mean [{tool}]?" if close else ""))
        return {}, [], problems

    allowed = {**{k: SHARED[k] for k in spec["shared"]}, **spec["keys"]}
    for key, value in table.items():
        if key not in allowed:
            problems.append(f"{line(tool, key)}[{tool}] {key} is not a key of [{tool}]" + suggestion(key, allowed))
            continue
        present[key] = tool
        found, normalized = check_value(f"[{tool}] {key}", value, *allowed[key])
        if normalized is None:
            problems.extend(line(tool, key) + p for p in found)
        else:
            own[key] = normalized

    values = {}
    for key in spec["shared"]:
        if key in own:
            values[key] = own[key]
        elif key in shared:
            values[key] = shared[key]
    for key in spec["keys"]:
        if key in own:
            values[key] = own[key]

    for key in spec["required"]:
        if key not in present:
            where = f"declare it at the top or in [{tool}]" if key in SHARED else f"declare it in [{tool}]"
            problems.append(f"[{tool}] {key} is missing: {where}")
    if "residue" in spec["shared"]:
        versioning = values.get("versioning")
        if versioning == "none" and "residue" not in present:
            problems.append('residue is required with versioning = "none"')
        elif versioning == "git" and "residue" in present:
            problems.append(f'{line(present["residue"], "residue")}residue is only used with versioning = "none"')

    undeclared = [key for key in (*spec["shared"], *spec["keys"])
                  if key not in values and key not in spec["required"]
                  and not (key == "residue" and values.get("versioning") != "none")]
    return values, undeclared, problems


def unknown_tool(tool):
    return Result("error", tool=tool, problems=[f"unknown tool {tool!r}" + suggestion(tool, TOOLS)])


def load(tool, root, path):
    """Parse and validate the file at path for tool."""
    try:
        import tomllib
    except ImportError:
        return Result("error", root=root, file=path, tool=tool,
                      problems=["Python 3.11 or later is needed to read TOML"])
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return Result("error", root=root, file=path, tool=tool, problems=[f"cannot read {path}: {error}"])
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        message = str(error)
        number = getattr(error, "lineno", None)
        match = TOML_LINE_RE.search(message)
        if match:
            number = number or int(match.group(1))
            message = message[:match.start()]
        prefix = f"line {number}: " if number else ""
        return Result("invalid", root=root, file=path, tool=tool,
                      problems=[f"{prefix}TOML error: {getattr(error, 'msg', None) or message}"])
    values, undeclared, problems = validate(tool, data, text)
    if problems:
        return Result("invalid", root=root, file=path, tool=tool, problems=problems)
    return Result("ok", root=root, file=path, tool=tool, values=values, undeclared=undeclared)


def read(tool, start=".", personal=None):
    """Read and validate the conventions for tool, starting from start."""
    if tool not in TOOLS:
        return unknown_tool(tool)
    root = find_root(start, personal)
    if root is None:
        return Result("no-root", tool=tool)
    path = root / FILE
    if not path.is_file():
        return Result("missing", root=root, tool=tool)
    return load(tool, root, path)


def ignore(root):
    """Add the file to root's .gitignore when root holds .git; the .gitignore changed, or None."""
    if not (root / ".git").exists():
        return None
    gitignore = root / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    if any(line.strip() in (FILE, "/" + FILE) for line in text.splitlines()):
        return None
    separator = "\n" if text and not text.endswith("\n") else ""
    gitignore.write_text(f"{text}{separator}/{FILE}\n", encoding="utf-8")
    return gitignore


def write(tool, draft, start=".", root=None, personal=None):
    """Create root's file from draft once draft is valid for tool, then read it back."""
    if tool not in TOOLS:
        return unknown_tool(tool)
    root = Path(root).resolve() if root is not None else find_root(start, personal)
    if root is None:
        return Result("no-root", tool=tool)
    target = root / FILE
    if target.exists():
        return Result("error", root=root, file=target, tool=tool,
                      problems=[f"{target} already exists; edit it instead"])
    checked = load(tool, root, Path(draft))
    if checked.status != "ok":
        return checked
    target.write_text(Path(draft).read_text(encoding="utf-8"), encoding="utf-8")
    gitignore = ignore(root)
    result = load(tool, root, target)
    result.written, result.gitignore = target, gitignore
    return result


def toml_value(value):
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{k} = {toml_value(v)}" for k, v in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    return json.dumps(value, ensure_ascii=False)


def render(result):
    lines = [f"status: {result.status}"]
    if result.root is not None:
        lines.append(f"root: {result.root}")
    if result.file is not None:
        lines.append(f"file: {result.file}")
    if result.written is not None:
        lines.append(f"written: {result.written}")
    if result.gitignore is not None:
        lines.append(f"gitignored in: {result.gitignore}")
    if result.status == "ok":
        lines.append(f"[{result.tool}]")
        lines.extend(f"{key} = {toml_value(value)}" for key, value in result.values.items())
        if result.undeclared:
            lines.append("# not declared: " + ", ".join(result.undeclared))
    lines.extend(f"problem: {problem}" for problem in result.problems)
    return "\n".join(lines)


def main(argv):
    try:
        if len(argv) == 1:
            result = read(argv[0])
        elif len(argv) == 3 and argv[1] == "--from":
            result = read(argv[0], argv[2])
        elif len(argv) == 3 and argv[1] == "--write":
            result = write(argv[0], argv[2])
        elif len(argv) == 5 and argv[1] == "--write" and argv[3] == "--root":
            result = write(argv[0], argv[2], root=argv[4])
        else:
            result = Result("error", problems=["usage: conventions.py <tool> [--from <path>] "
                                               "| <tool> --write <draft> [--root <dir>]"])
        print(render(result))
    except Exception as error:
        print(f"status: error\nproblem: unexpected {type(error).__name__}: {error}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
