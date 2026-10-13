#!/usr/bin/env python3
"""Claude Code SessionStart hook: name each resume note not taken up yet, in one line per note.

Reads the [session] notes folder of the project's .agent-conventions.toml through the
close-session skill's scripts/conventions.py, and adds one line per open note of that
folder to the session's context, latest first, three at most: the note, its date, the
first item of its resume point, and an instruction that applies only when the request
continues that work. A note is a .md file directly in the folder holding a **Taken up:**
field; it is open while that field is "—". The latest is the one with the latest
**Date:**, then the latest change. Prints nothing when the conventions are not ok or no
note is open, and exits 0 in every case, an unexpected error included.
"""

import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

LIMIT = 3
ITEM_LENGTH = 200
OPEN = ("", "—", "-")
HEADING = "where the next session starts"
ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+(.*)$")


@dataclass
class Note:
    path: Path
    date: str
    changed: float
    first: str


def find_conventions():
    """The close-session skill's scripts/conventions.py, found above this hook whether run
    from the repository (domains/session/hooks/) or installed (hooks/session/), where it
    sits one level deeper than here. None when it can't be found, including when an
    ancestor directory can't be stat'd."""
    try:
        for candidate in Path(__file__).resolve().parents:
            script = candidate / "skills" / "close-session" / "scripts" / "conventions.py"
            if script.is_file():
                return script
    except OSError:
        return None
    return None


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def field(text, name):
    """The value of a `**Name:**` line, or None when the note has none."""
    match = re.search(rf"^\*\*{re.escape(name)}:\*\*[ \t]*(.*?)[ \t]*$", text, re.M)
    return match.group(1) if match else None


def first_item(text):
    """The first item of the note's resume point, its lines joined, cut past ITEM_LENGTH."""
    lines, inside, item = text.splitlines(), False, None
    for line in lines:
        if line.startswith("#"):
            if item is not None:
                break
            inside = line.lstrip("#").strip().lower() == HEADING
            continue
        if not inside:
            continue
        match = ITEM_RE.match(line)
        if item is None:
            if match:
                item = [match.group(1).strip()]
        elif match or not line.strip():
            break
        else:
            item.append(line.strip())
    if not item:
        return ""
    joined = " ".join(item).rstrip(" .")
    if len(joined) > ITEM_LENGTH:
        joined = joined[:ITEM_LENGTH].rsplit(" ", 1)[0].rstrip(" .,;:") + "…"
    return joined


def open_notes(folder):
    """The notes of folder not taken up yet."""
    if not folder.is_dir():
        return []
    notes = []
    for path in sorted(folder.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
            changed = path.stat().st_mtime
        except (OSError, UnicodeDecodeError):
            continue
        taken = field(text, "Taken up")
        if taken is None or taken not in OPEN:
            continue
        notes.append(Note(path, field(text, "Date") or "", changed, first_item(text)))
    return notes


def describe(root, note):
    date = f" ({note.date})" if note.date else ""
    point = f": {note.first}" if note.first else ""
    return (f"Resume note {note.path.relative_to(root)}{date}, not taken up{point}. "
            "If the request continues that work, read the note before working; "
            "otherwise, ignore this line.")


def main():
    try:
        event = json.load(sys.stdin)
        script = find_conventions()
        if script is None:
            return 0
        conventions = load("session_conventions", script)
        result = conventions.read("session", Path(event.get("cwd") or ".").resolve())
        if result.status != "ok":
            return 0
        notes = sorted(open_notes(result.root / result.values["notes"]),
                       key=lambda note: (note.date, note.changed), reverse=True)[:LIMIT]
        if not notes:
            return 0
        output = json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(describe(result.root, note) for note in notes)}},
            ensure_ascii=False)
    except Exception:
        return 0
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
