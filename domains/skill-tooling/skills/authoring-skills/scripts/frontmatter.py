"""Read the frontmatter of a skill or an agent: a strict subset of YAML, standard library only.

parse(text) returns a Result:
- fields: the top-level mapping, {} for an empty block, None when there is no block or
  when it cannot be read;
- problems: (line, code, message) for what YAML or the harness refuses, code being
  "no-opening", "no-closing", "not-mapping" or "yaml";
- outside: (line, message) for valid YAML the subset does not read;
- lines: {key: line} for each top-level key;
- cut: (line, key) for each plain value a " #" comment cut short;
- body_line: the first line after the closing ---.

Lines count from 1 in the file. Plain scalars are typed as YAML 1.2's core schema types
them. The subset: block mappings and sequences at any depth; plain, single-quoted,
double-quoted and block scalars; flow sequences and mappings of scalars on one line;
comments. Outside it: anchors, aliases, tags, quoted and complex keys, quoted values over
several lines, nested or multi-line flow collections, directives.
"""

import re
from dataclasses import dataclass, field

KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)[ \t]*:(?:[ \t]+(.*)|[ \t]*)$")
QUOTED_KEY_RE = re.compile(r"^(\"[^\"]*\"|'[^']*')[ \t]*:")
BLOCK_HEADER_RE = re.compile(r"^([|>])([+-]?)([1-9]?)([+-]?)[ \t]*(#.*)?$")
NULL_RE = re.compile(r"^(~|null|Null|NULL)$")
BOOL_RE = re.compile(r"^(true|True|TRUE|false|False|FALSE)$")
INT_RE = re.compile(r"^([-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)$")
FLOAT_RE = re.compile(r"^([-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?|[-+]?\.(inf|Inf|INF)|\.(nan|NaN|NAN))$")
ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", '"': '"', "/": "/", "0": "\0", " ": " "}
FORBIDDEN_FIRST = "%@`"
NODE_FIRST = "&*!"


@dataclass
class Result:
    fields: dict | None = None
    problems: list = field(default_factory=list)
    outside: list = field(default_factory=list)
    lines: dict = field(default_factory=dict)
    cut: list = field(default_factory=list)
    body_line: int = 1


class Stop(Exception):
    """A line the subset refuses: a YAML error, or valid YAML outside the subset."""

    def __init__(self, line, message, outside=False):
        super().__init__(message)
        self.line, self.message, self.outside = line, message, outside


def typed(text):
    if text == "" or NULL_RE.match(text):
        return None
    if BOOL_RE.match(text):
        return text.lower() == "true"
    if INT_RE.match(text):
        return int(text, 0) if text[:2] in ("0o", "0x") else int(text)
    if FLOAT_RE.match(text):
        lowered = text.lower()
        if lowered.endswith(".inf"):
            return float("-inf") if lowered.startswith("-") else float("inf")
        return float("nan") if lowered == ".nan" else float(text)
    return text


def indent_of(text):
    return len(text) - len(text.lstrip(" "))


class Reader:
    def __init__(self, rows):
        self.rows = rows  # [(line number, text)] of the block, without its --- lines
        self.cut = []

    # scalars

    def plain(self, value, line, key):
        """A plain scalar's text, its comment removed; refuses what YAML refuses."""
        first = value[0]
        if first in NODE_FIRST:
            raise Stop(line, f"{first!r} opens an anchor, an alias or a tag", outside=True)
        if first in FORBIDDEN_FIRST or value.startswith(("- ", "? ", ": ")) or value in ("-", "?", ":"):
            raise Stop(line, f"a plain value cannot start with {first!r}: quote the value")
        comment = re.search(r"[ \t]#", value)
        text = value[:comment.start()].rstrip() if comment else value.rstrip()
        if comment:
            self.cut.append((line, key))
        if re.search(r":([ \t]|$)", text):
            raise Stop(line, "a plain value holds ': ', which YAML reads as a nested mapping: quote the value")
        return text

    def quoted(self, value, line):
        quote = value[0]
        out, i = [], 1
        while i < len(value):
            c = value[i]
            if quote == '"' and c == "\\":
                n = value[i + 1:i + 2]
                if n in ESCAPES:
                    out.append(ESCAPES[n]); i += 2
                elif n == "u" and re.fullmatch(r"[0-9A-Fa-f]{4}", value[i + 2:i + 6]):
                    out.append(chr(int(value[i + 2:i + 6], 16))); i += 6
                else:
                    raise Stop(line, f"unknown escape \\{n} in a double-quoted value")
            elif c == quote:
                if quote == "'" and value[i + 1:i + 2] == "'":
                    out.append("'"); i += 2
                    continue
                rest = value[i + 1:].strip()
                if rest and not rest.startswith("#"):
                    raise Stop(line, "text after the closing quote")
                return "".join(out)
            else:
                out.append(c); i += 1
        if any(quote in text for number, text in self.rows if number > line):
            raise Stop(line, "a quoted value over several lines", outside=True)
        raise Stop(line, "a quoted value is never closed")

    def scalar(self, value, line, key):
        if value[0] in "\"'":
            return self.quoted(value, line)
        return typed(self.plain(value, line, key))

    def flow(self, value, line, key):
        close = "]" if value[0] == "[" else "}"
        comment = re.search(r"[ \t]#", value)
        body = (value[:comment.start()] if comment else value).rstrip()
        if not body.endswith(close):
            raise Stop(line, "a flow collection over several lines", outside=True)
        items, buf, quote = [], "", None
        for c in body[1:-1]:
            if quote:
                buf += c
                quote = None if c == quote else quote
            elif c in "\"'":
                quote = c; buf += c
            elif c in "[]{}":
                raise Stop(line, "a flow collection nested in another", outside=True)
            elif c == ",":
                items.append(buf.strip()); buf = ""
            else:
                buf += c
        if quote:
            raise Stop(line, "a quoted value is never closed")
        if buf.strip():
            items.append(buf.strip())
        if close == "]":
            return [self.scalar(item, line, key) for item in items]
        out = {}
        for item in items:
            m = re.match(r"^([^:]+?)[ \t]*:[ \t]+(.+)$", item)
            if not m:
                raise Stop(line, f"a flow mapping entry is not 'key: value': {item!r}")
            out[self.scalar(m.group(1), line, key)] = self.scalar(m.group(2), line, key)
        return out

    def block_scalar(self, header, start, parent, line):
        m = BLOCK_HEADER_RE.match(header)
        if not m:
            raise Stop(line, f"a malformed block scalar header {header!r}")
        style, chomp = m.group(1), m.group(2) or m.group(4)
        collected, i = [], start
        while i < len(self.rows) and (not self.rows[i][1].strip() or indent_of(self.rows[i][1]) > parent):
            collected.append(self.rows[i][1]); i += 1
        trailing = 0
        while collected and not collected[-1].strip():
            collected.pop(); trailing += 1
        if not collected:
            return "", i
        width = int(m.group(3)) if m.group(3) else min(indent_of(t) for t in collected if t.strip())
        body = [t[width:] if t.strip() else "" for t in collected]
        text = "\n".join(body) if style == "|" else fold(body)
        if chomp == "-":
            return text, i
        return text + "\n" + ("\n" * trailing if chomp == "+" else ""), i

    # collections

    def value(self, rest, i, indent, line, key):
        """The value after a key (or a dash) at row i; returns (value, next row)."""
        if rest is None or rest == "" or rest.startswith("#"):
            j = i + 1
            while j < len(self.rows) and not self.rows[j][1].strip():
                j += 1
            if j < len(self.rows):
                text = self.rows[j][1]
                child = indent_of(text)
                if child > indent or (child == indent and text[indent:].startswith("- ")):
                    return self.block(j, child)
            return None, i + 1
        if rest[0] in "|>":
            return self.block_scalar(rest, i + 1, indent, line)
        if rest[0] in "[{":
            return self.flow(rest, line, key), i + 1
        if rest[0] in "\"'":
            return self.quoted(rest, line), i + 1
        parts, j = [self.plain(rest, line, key)], i + 1
        while j < len(self.rows) and (not self.rows[j][1].strip() or indent_of(self.rows[j][1]) > indent):
            number, text = self.rows[j]
            stripped = text.strip()
            if stripped:
                if KEY_RE.match(stripped) or stripped.startswith("- "):
                    raise Stop(number, "a more indented line under a plain value: put a nested mapping or "
                                       "list under a key alone on its line")
                parts.append(self.plain(stripped, number, key))
            else:
                parts.append("")
            j += 1
        while parts and parts[-1] == "":
            parts.pop()
        return (typed(parts[0]) if len(parts) == 1 else fold(parts)), j

    def block(self, start, indent):
        text = self.rows[start][1][indent:]
        if text.startswith("- ") or text == "-":
            return self.sequence(start, indent)
        return self.mapping(start, indent)[:2]

    def mapping(self, start, indent):
        out, lines, i = {}, {}, start
        while i < len(self.rows):
            number, text = self.rows[i]
            if not text.strip() or text.strip().startswith("#"):
                i += 1
                continue
            current = indent_of(text)
            if current < indent:
                break
            if current > indent:
                raise Stop(number, "a line indented deeper than its mapping")
            body = text[indent:]
            if QUOTED_KEY_RE.match(body) or body.startswith("? "):
                raise Stop(number, "a quoted or complex key", outside=True)
            if body.startswith("- "):
                raise Stop(number, "a list item where a 'key: value' line is expected")
            m = KEY_RE.match(body)
            if not m:
                raise Stop(number, f"not a 'key: value' line: {body[:40]!r}")
            key, rest = m.group(1), m.group(2)
            if key in out:
                raise Stop(number, f"duplicate key {key!r}: parsers disagree on which value wins")
            lines[key] = number
            out[key], i = self.value(rest, i, indent, number, key)
        return out, i, lines

    def sequence(self, start, indent):
        out, i = [], start
        while i < len(self.rows):
            number, text = self.rows[i]
            if not text.strip() or text.strip().startswith("#"):
                i += 1
                continue
            if indent_of(text) != indent or not (text[indent:].startswith("- ") or text[indent:] == "-"):
                if indent_of(text) > indent:
                    raise Stop(number, "a line indented deeper than its list")
                break
            item = text[indent + 2:] if text[indent:] != "-" else ""
            if item.startswith("- "):
                raise Stop(number, "a list nested in a list item", outside=True)
            if item.strip() and KEY_RE.match(item.strip()):
                saved = self.rows[i]
                self.rows[i] = (number, " " * (indent + 2) + item)
                try:
                    value, end, _ = self.mapping(i, indent + 2)
                finally:
                    self.rows[i] = saved
                out.append(value)
                i = end
                continue
            value, i = self.value(item, i, indent, number, None)
            out.append(value)
        return out, i


def fold(lines):
    """Folded text: lines joined by spaces, an empty line kept as a line break."""
    text = ""
    for i, line in enumerate(lines):
        if i == 0:
            text = line
        elif line == "":
            text += "\n"
        elif lines[i - 1] == "":
            text += line
        elif line.startswith((" ", "\t")) or lines[i - 1].startswith((" ", "\t")):
            text += "\n" + line
        else:
            text += " " + line
    return text


def parse(text):
    if text.startswith("﻿"):
        text = text[1:]
    lines = [line[:-1] if line.endswith("\r") else line for line in text.split("\n")]
    if not lines or lines[0].rstrip() != "---":
        return Result(problems=[(1, "no-opening", "the file does not open with --- on its first line")])
    close = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if close is None:
        return Result(problems=[(1, "no-closing", "the opening --- is never closed by a --- line")])
    result = Result(body_line=close + 2)
    rows = [(i + 1, lines[i]) for i in range(1, close)]
    for number, line in rows:
        if line[:len(line) - len(line.lstrip(" \t"))].count("\t"):
            result.problems.append((number, "yaml", "a tab in the indentation: YAML allows spaces only"))
            return result
        if line.startswith("%"):
            result.outside.append((number, "a directive"))
            return result
    meaningful = [(n, t) for n, t in rows if t.strip() and not t.strip().startswith("#")]
    if not meaningful:
        result.fields = {}
        return result
    first_number, first = meaningful[0]
    if first == "-" or first.startswith("- "):
        result.problems.append((first_number, "not-mapping", "the frontmatter is a list, not a mapping"))
        return result
    if indent_of(first) != 0:
        result.problems.append((first_number, "yaml", "the frontmatter's first line is indented"))
        return result
    if len(meaningful) == 1 and not KEY_RE.match(first) and ": " not in first and not first.endswith(":"):
        result.problems.append((first_number, "not-mapping", "the frontmatter is a single value, not a mapping"))
        return result
    reader = Reader(rows)
    try:
        fields, _, keys = reader.mapping(0, 0)
    except Stop as stop:
        if stop.outside:
            result.outside.append((stop.line, stop.message))
        else:
            result.problems.append((stop.line, "yaml", stop.message))
        return result
    result.fields, result.lines, result.cut = fields, keys, reader.cut
    return result
