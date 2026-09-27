"""Read and write a tool review: YAML front matter, then Markdown prose.

Only the YAML subset this module writes is read back: plain and double-quoted scalars,
`>-` folded blocks, block mappings, block sequences of mappings, and flow mappings whose
keys hold no colon and whose leaves are integers. Standard library only, so that the Stop
hook, the tool-review scripts and the report share one reader without PyYAML.
"""

import json
import os
import re
import tempfile
from pathlib import Path

FORMAT = 1
STATUSES = ("requested", "complete", "skipped")
TRIGGERS = ("hook", "manual")
OUTCOMES = ("delivered", "partial", "abandoned")
SEVERITIES = ("low", "medium", "high")
KINDS = ("skill-gap", "skill-drift", "trigger", "tooling-gap", "noise", "waste", "defect", "unverified")
ORDER = ("review", "status", "date", "session", "project", "trigger", "slice", "closed", "tools",
         "task", "outcome", "corrections", "measured", "findings")

WIDTH = 88
SHORT = 60
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./:@+-]*")
INT_RE = re.compile(r"-?[0-9]+")
RESERVED = {"true", "false", "yes", "no", "on", "off", "null", "y", "n"}


class FormatError(ValueError):
    """A review file this module cannot read."""


# --- writing -----------------------------------------------------------------

def plain(text):
    """True when `text` can be written unquoted and read back, here and by PyYAML, as the same string."""
    return bool(TOKEN_RE.fullmatch(text)) and text.lower() not in RESERVED


def flowable(mapping):
    """True for a non-empty mapping whose keys are plain and hold no colon, and whose leaves are
    integers or such mappings. A tool id holds a colon, so `setup` always stays in block style."""
    if not isinstance(mapping, dict) or not mapping:
        return False
    for key, value in mapping.items():
        if not (isinstance(key, str) and plain(key) and ":" not in key):
            return False
        if isinstance(value, dict):
            if value and not flowable(value):
                return False
        elif isinstance(value, bool) or not isinstance(value, int):
            return False
    return True


def flow(mapping):
    return "{" + ", ".join(f"{key}: {flow(value) if isinstance(value, dict) else value}"
                           for key, value in mapping.items()) + "}"


def key_text(key):
    return key if plain(key) else json.dumps(key, ensure_ascii=False)


def wrap(text, indent):
    lines, current = [], ""
    for word in text.split(" "):
        if current and indent + len(current) + 1 + len(word) > WIDTH:
            lines.append(" " * indent + current)
            current = word
        else:
            current = f"{current} {word}" if current else word
    lines.append(" " * indent + current)
    return lines


def string_lines(head, text, indent):
    if plain(text):
        return [f"{head} {text}"]
    if " ".join(text.split()) != text or len(text) <= SHORT:
        return [f"{head} {json.dumps(text, ensure_ascii=False)}"]
    return [f"{head} >-"] + wrap(text, indent + 2)


def entry_lines(head, value, indent):
    """The lines of one entry whose key line, indented by `indent`, is `head`."""
    if isinstance(value, bool):
        raise TypeError("booleans are not part of the review format")
    if isinstance(value, int):
        return [f"{head} {value}"]
    if isinstance(value, str):
        return string_lines(head, value, indent)
    if isinstance(value, dict):
        if not value:
            return [f"{head} {{}}"]
        if flowable(value):
            return [f"{head} {flow(value)}"]
        return [head] + mapping_lines(value, indent + 2)
    if isinstance(value, list):
        if not value:
            return [f"{head} []"]
        lines = [head]
        for item in value:
            if not isinstance(item, dict) or not item:
                raise TypeError("a list holds non-empty mappings only")
            if flowable(item):
                lines.append(" " * (indent + 2) + "- " + flow(item))
                continue
            item_lines = mapping_lines(item, indent + 4)
            item_lines[0] = " " * (indent + 2) + "- " + item_lines[0][indent + 4:]
            lines.extend(item_lines)
        return lines
    raise TypeError(f"{type(value).__name__} is not part of the review format")


def mapping_lines(mapping, indent):
    lines = []
    for key, value in mapping.items():
        if value is not None:
            lines.extend(entry_lines(" " * indent + key_text(key) + ":", value, indent))
    return lines


def render(meta, body=""):
    """A review's text: `meta` as front matter, its known keys in the format's order, then `body`."""
    known = {key: meta[key] for key in ORDER if key in meta}
    ordered = {**known, **{key: value for key, value in meta.items() if key not in known}}
    text = "---\n" + "\n".join(mapping_lines(ordered, 0)) + "\n---\n"
    if body.strip():
        text += "\n" + body.strip("\n") + "\n"
    return text


# --- reading -----------------------------------------------------------------

def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def next_content(lines, index):
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def split_key(content, number):
    if content.startswith('"'):
        try:
            key, end = json.JSONDecoder().raw_decode(content)
        except ValueError as error:
            raise FormatError(f"line {number}: {error}") from error
        if not content[end:].startswith(":"):
            raise FormatError(f"line {number}: expected : after the key")
        return key, content[end + 1:].strip()
    colon = content.find(": ")
    if colon != -1:
        return content[:colon], content[colon + 2:].strip()
    if content.endswith(":"):
        return content[:-1], ""
    raise FormatError(f"line {number}: expected key: value")


def read_flow(text, position, number):
    """The flow mapping opening at text[position]; returns it and the position after its }."""
    mapping = {}
    position += 1
    if text.startswith("}", position):
        return mapping, position + 1
    while True:
        colon = text.find(": ", position)
        if colon == -1:
            raise FormatError(f"line {number}: a key of a flow mapping has no value")
        key = text[position:colon].strip()
        position = colon + 2
        if text.startswith("{", position):
            value, position = read_flow(text, position, number)
        else:
            ends = [index for index in (text.find(",", position), text.find("}", position)) if index != -1]
            if not ends:
                raise FormatError(f"line {number}: a flow mapping is not closed")
            raw = text[position:min(ends)].strip()
            value = int(raw) if INT_RE.fullmatch(raw) else raw
            position = min(ends)
        mapping[key] = value
        if text.startswith(", ", position):
            position += 2
        elif text.startswith("}", position):
            return mapping, position + 1
        else:
            raise FormatError(f"line {number}: expected , or }} in a flow mapping")


def read_inline(text, number):
    if text.startswith("{"):
        value, end = read_flow(text, 0, number)
        if text[end:].strip():
            raise FormatError(f"line {number}: text after a flow mapping")
        return value
    if text == "[]":
        return []
    if text.startswith('"'):
        try:
            return json.loads(text)
        except ValueError as error:
            raise FormatError(f"line {number}: {error}") from error
    return int(text) if INT_RE.fullmatch(text) else text


def read_mapping(lines, index, indent):
    mapping = {}
    index = next_content(lines, index)
    while index < len(lines):
        line = lines[index]
        if indent_of(line) < indent:
            break
        if indent_of(line) > indent:
            raise FormatError(f"line {index + 2}: unexpected indentation")
        content = line[indent:]
        if content.startswith("- "):
            break
        key, rest = split_key(content, index + 2)
        index += 1
        if rest == ">-":
            words = []
            while index < len(lines) and (not lines[index].strip() or indent_of(lines[index]) > indent):
                words.extend(lines[index].split())
                index += 1
            mapping[key] = " ".join(words)
        elif rest:
            mapping[key] = read_inline(rest, index + 1)
        else:
            index = next_content(lines, index)
            if index >= len(lines) or indent_of(lines[index]) <= indent:
                raise FormatError(f"line {index + 1}: {key} has no value")
            child = indent_of(lines[index])
            if lines[index][child:].startswith("- "):
                mapping[key], index = read_sequence(lines, index, child)
            else:
                mapping[key], index = read_mapping(lines, index, child)
        index = next_content(lines, index)
    return mapping, index


def read_sequence(lines, index, indent):
    items = []
    while index < len(lines) and indent_of(lines[index]) == indent and lines[index][indent:].startswith("- "):
        rest = lines[index][indent + 2:]
        if rest.startswith("{"):
            items.append(read_inline(rest, index + 2))
            index = next_content(lines, index + 1)
            continue
        lines[index] = " " * (indent + 2) + rest
        item, index = read_mapping(lines, index, indent + 2)
        items.append(item)
    return items, index


def parse(text):
    """(meta, body) of a review's text; FormatError when it is not a review this module wrote."""
    if not text.startswith("---\n"):
        raise FormatError("line 1: a review opens with ---")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise FormatError("the front matter is not closed by ---")
    lines = text[4:end].split("\n")
    meta, index = read_mapping(lines, 0, 0)
    if index < len(lines):
        raise FormatError(f"line {index + 2}: unexpected indentation")
    body = text[end + 5:]
    return meta, body[1:] if body.startswith("\n") else body


# --- files -------------------------------------------------------------------

def session_reviews(reviews_dir, session):
    """(path, meta) of each readable review of `session`, in the order of their slices."""
    found = []
    for path in Path(reviews_dir).glob(f"*-{session[:8]}-*.md"):
        try:
            meta, _ = parse(path.read_text(encoding="utf-8"))
        except (OSError, FormatError):
            continue
        if meta.get("session") == session:
            found.append((path, meta))
    return sorted(found, key=lambda item: str((item[1].get("slice") or {}).get("to", "")))


def next_start(reviews):
    """Where a session's next slice starts: the latest `closed`, or `slice.to` for a review not closed yet."""
    ends = [str(meta.get("closed") or (meta.get("slice") or {}).get("to") or "") for _, meta in reviews]
    return max((end for end in ends if end), default=None)


def slug(tool_id):
    """The name a review takes from its first tool: `hook:roadmap/session_resume.py` gives `session-resume`."""
    name = tool_id.split(":", 1)[-1].rsplit("/", 1)[-1]
    name = name[:-3] if name.endswith(".py") else name
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "review"


def draft_of(path):
    return Path(path).with_suffix(".draft")


def new_path(reviews_dir, date, session, name):
    """reviews/<date>-<session8>-<name>.md, numbered -2, -3… when the name or its draft is taken."""
    base = f"{date}-{session[:8]}-{name}"
    path, number = Path(reviews_dir) / f"{base}.md", 2
    while path.exists() or draft_of(path).exists():
        path, number = Path(reviews_dir) / f"{base}-{number}.md", number + 1
    return path


def write_text(path, text):
    """Write through a temporary file and a rename, so that no reader sees half a review."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        stream.write(text)
    os.chmod(temporary, 0o644)
    os.replace(temporary, path)
