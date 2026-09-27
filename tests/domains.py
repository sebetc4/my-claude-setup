"""Static checks on each domain under domains/: its version, changelog, agents, hooks and permissions."""

import importlib.util
import json
import re
from pathlib import Path

import yaml

_spec = importlib.util.spec_from_file_location("skill_checks", Path(__file__).resolve().parent / "skills.py")
skills = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(skills)

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
ENTRY_RE = re.compile(r"^## (.+)$", re.M)
HOOKS_DIR_REF_RE = re.compile(r"\{\{HOOKS_DIR\}\}/([^\s\"]+)")
PERMISSION_PATH_RE = re.compile(r"\{\{(CLAUDE_DIR|HOOKS_DIR)\}\}/([^\s):\"*]+)")


def check_version(domain):
    """The domain has a VERSION of the form X.Y.Z, and its CHANGELOG.md opens with that version."""
    version_file = domain / "VERSION"
    if not version_file.is_file():
        yield version_file, 1, "missing VERSION file: every domain has one, of the form X.Y.Z"
        return
    version = version_file.read_text(encoding="utf-8").strip()
    if not VERSION_RE.match(version):
        yield version_file, 1, f"{version!r} is not of the form X.Y.Z"
        return
    changelog = domain / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8") if changelog.is_file() else ""
    entry = ENTRY_RE.search(text)
    if entry is None:
        yield changelog, 1, "missing CHANGELOG.md, or no ## entry in it"
    elif entry.group(1).split()[0] != version:
        yield changelog, skills.line_of(text, entry.start()), \
            f"first entry {entry.group(1)!r} does not match VERSION {version}"


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


def check_hooks(domain):
    """Every {{HOOKS_DIR}}/<name> a hooks.json command names exists under the domain's hooks/."""
    path = domain / "hooks.json"
    if not path.is_file():
        return
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        yield path, 1, f"invalid JSON: {error}"
        return
    for groups in (config.values() if isinstance(config, dict) else ()):
        for group in groups if isinstance(groups, list) else ():
            for hook in group.get("hooks", []) if isinstance(group, dict) else ():
                command = hook.get("command", "") if isinstance(hook, dict) else ""
                for name in HOOKS_DIR_REF_RE.findall(command):
                    if not (domain / "hooks" / name).is_file():
                        yield path, 1, f"{name}: no such file under {domain.name}/hooks/"


def check_permissions(domain):
    """permissions.json holds {"allow": [rule, ...]}, and each path a rule names in the Claude directory exists in the domain."""
    path = domain / "permissions.json"
    if not path.is_file():
        return
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        yield path, 1, f"invalid JSON: {error}"
        return
    rules = config.get("allow") if isinstance(config, dict) else None
    if (set(config if isinstance(config, dict) else ()) != {"allow"} or not isinstance(rules, list)
            or not all(isinstance(rule, str) and rule for rule in rules)):
        yield path, 1, 'must be {"allow": [rule, ...]} with non-empty string rules'
        return
    for rule in rules:
        for placeholder, rest in PERMISSION_PATH_RE.findall(rule):
            rest = rest.rstrip("/")
            parts = rest.split("/")
            if placeholder == "HOOKS_DIR":
                target = domain / "hooks" / rest
            elif parts[0] in ("skills", "agents", "commands"):
                target = domain / rest
            elif parts[0] == "hooks" and len(parts) > 2 and parts[1] == domain.name:
                target = domain / "hooks" / "/".join(parts[2:])
            else:
                yield path, 1, f"{rest}: not a path this domain installs"
                continue
            if not target.exists():
                yield path, 1, f"{target.relative_to(domain)}: no such path in {domain.name}/"


CHECKS = (check_version, check_agents, check_hooks, check_permissions)


def run(domain: Path):
    for check in CHECKS:
        yield from check(domain)
