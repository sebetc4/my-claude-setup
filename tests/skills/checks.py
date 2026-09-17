"""Static checks that apply to every skill under skills/."""

import re
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.S)
PLACEHOLDER_RE = re.compile(r"\{\{([^}]*)\}\}")
RESOURCE_RE = re.compile(r"\b((?:references|assets|scripts)/[\w./-]*\w\.\w+)")
FRENCH_RE = re.compile(r"\b(le|la|les|des|une|est|sont|dans|pour|avec|qui|que|cette|doit|faut|chaque|toute)\b", re.I)
PERCENT_RE = re.compile(r"\d %")
TOC_RE = re.compile(r"^## (Contents|Table of Contents)\s*$", re.M)

# Wording that only makes sense for artifacts produced by an earlier version of a skill.
COMPATIBILITY_RE = re.compile(
    r"\blegacy\b|backwards?[- ]compat|\bprevious (skill|version)\b|\bold (skill|version|format)\b"
    r"|\bpre-existing\b|\bbefore (this|the) feature\b|\bdeprecated\b",
    re.I,
)

SKILL_MAX_LINES = 500
REFERENCE_TOC_THRESHOLD = 300


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def skill_files(skill):
    return sorted(p for p in skill.rglob("*") if p.is_file() and p.suffix == ".md")


def check_frontmatter(skill):
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        yield path, 1, "missing YAML frontmatter"
        return
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        yield path, 1, f"invalid YAML frontmatter: {error}"
        return
    if not isinstance(meta, dict):
        yield path, 1, "frontmatter is not a mapping"
        return
    name, description = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        yield path, 1, f"name {name!r} must be kebab-case, 64 characters at most"
    elif name != skill.name:
        yield path, 1, f"name {name!r} does not match the directory {skill.name!r}"
    if not isinstance(description, str) or not description.strip():
        yield path, 1, "description is missing"
    else:
        if len(description) > 1024:
            yield path, 1, f"description is {len(description)} characters, 1024 at most"
        if "<" in description or ">" in description:
            yield path, 1, "description contains angle brackets"


def check_resources(skill):
    """Every cited resource exists, and every resource is reachable from SKILL.md."""
    for path in skill_files(skill):
        text = path.read_text(encoding="utf-8")
        for match in RESOURCE_RE.finditer(text):
            if not (skill / match.group(1)).is_file():
                yield path, line_of(text, match.start()), f"cites {match.group(1)}, which does not exist"

    reached, queue = set(), [skill / "SKILL.md"]
    while queue:
        current = queue.pop()
        if current in reached or not current.is_file():
            continue
        reached.add(current)
        if current.suffix == ".md":
            text = current.read_text(encoding="utf-8")
            queue.extend(skill / m.group(1) for m in RESOURCE_RE.finditer(text))
    for folder in ("references", "assets", "scripts"):
        for resource in sorted((skill / folder).rglob("*")) if (skill / folder).is_dir() else []:
            if resource.is_file() and resource not in reached:
                yield resource, 1, "not reachable from SKILL.md: no file cites it"


def check_templates(skill):
    templates = skill / "assets" / "templates"
    for path in sorted(templates.rglob("*")) if templates.is_dir() else []:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"<!--", text):
            yield path, line_of(text, match.start()), "HTML comment in a template: it would be copied into every produced document"
        for match in PLACEHOLDER_RE.finditer(text):
            if not re.fullmatch(r"[A-Z0-9_]+", match.group(1)):
                yield path, line_of(text, match.start()), f"placeholder {{{{{match.group(1)}}}}} is not UPPER_SNAKE_CASE"


def check_wording(skill):
    for path in skill_files(skill):
        text = path.read_text(encoding="utf-8")
        for pattern, message in (
            (COMPATIBILITY_RE, "compatibility wording: a skill describes only its target behavior"),
            (FRENCH_RE, "non-English word: skill files are written in English"),
            (PERCENT_RE, "space before %: English percentages take none"),
        ):
            for match in pattern.finditer(text):
                yield path, line_of(text, match.start()), f"{message} ({match.group(0)!r})"


def check_sizes(skill):
    skill_md = skill / "SKILL.md"
    lines = skill_md.read_text(encoding="utf-8").count("\n") + 1
    if lines > SKILL_MAX_LINES:
        yield skill_md, 1, f"SKILL.md is {lines} lines, {SKILL_MAX_LINES} at most"
    references = skill / "references"
    for path in sorted(references.glob("*.md")) if references.is_dir() else []:
        text = path.read_text(encoding="utf-8")
        if text.count("\n") + 1 > REFERENCE_TOC_THRESHOLD and not TOC_RE.search(text):
            yield path, 1, f"over {REFERENCE_TOC_THRESHOLD} lines without a '## Contents' section"


CHECKS = (check_frontmatter, check_resources, check_templates, check_wording, check_sizes)


def run(skill: Path):
    for check in CHECKS:
        yield from check(skill)
