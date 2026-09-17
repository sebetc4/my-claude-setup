"""Static checks on each domain under domains/: its agents."""

import importlib.util
from pathlib import Path

import yaml

_spec = importlib.util.spec_from_file_location("skill_checks", Path(__file__).resolve().parent / "skills.py")
skills = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(skills)


def check_agents(domain):
    """Each agent has frontmatter with a name matching its file and a description, and clean wording."""
    for path in sorted((domain / "agents").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = skills.FRONTMATTER_RE.match(text)
        if not match:
            yield path, 1, "missing YAML frontmatter"
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            yield path, 1, f"invalid YAML frontmatter: {error}"
            continue
        if not isinstance(meta, dict):
            yield path, 1, "frontmatter is not a mapping"
            continue
        if meta.get("name") != path.stem:
            yield path, 1, f"name {meta.get('name')!r} does not match the file name {path.stem!r}"
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip():
            yield path, 1, "description is missing"
        yield from skills.wording_problems(path, text)


CHECKS = (check_agents,)


def run(domain: Path):
    for check in CHECKS:
        yield from check(domain)
