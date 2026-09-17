#!/usr/bin/env python3
"""Install the domains of this repository into a Claude Code directory.

Usage: python3 tools/claude_setup.py [--claude-dir DIR] [--domains-dir DIR] [--force]
                                     {list,enable,update,disable} [DOMAIN]

A domain is a folder under domains/. Its skills/, agents/ and commands/ are
copied into the Claude Code directory, its hooks/ into hooks/<domain>/, and its
hooks.json is merged into settings.json. What was installed is recorded in
my-claude-setup.json there, so that update and disable touch nothing else.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATE_FILE = "my-claude-setup.json"
PLACEHOLDER = "{{HOOKS_DIR}}"
COPIED_KINDS = ("skills", "agents", "commands")


class SetupError(Exception):
    """A problem that stops a command, with or without --force."""


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unit(rel):
    """The top entry a file belongs to: skills/<name>, agents/<file>, hooks/<domain>."""
    return "/".join(rel.split("/")[:2])


def domain_files(domain_dir):
    """Map each installed path, relative to the Claude directory, to its source file."""
    sources = [(domain_dir / kind, kind) for kind in COPIED_KINDS]
    sources.append((domain_dir / "hooks", f"hooks/{domain_dir.name}"))
    files = {}
    for base, prefix in sources:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            parts = path.relative_to(base).parts
            if not path.is_file() or "__pycache__" in parts:
                continue
            if prefix == "skills" and len(parts) > 1 and parts[1] == "evals":
                continue
            files[f"{prefix}/{'/'.join(parts)}"] = path
    return files


def domain_hooks(domain_dir, claude_dir):
    """The domain's hooks.json, with {{HOOKS_DIR}} resolved; {} when it has none."""
    path = domain_dir / "hooks.json"
    if not path.is_file():
        return {}
    hooks_dir = json.dumps(str(claude_dir / "hooks" / domain_dir.name))[1:-1]
    try:
        return json.loads(path.read_text(encoding="utf-8").replace(PLACEHOLDER, hooks_dir))
    except ValueError as error:
        raise SetupError(f"{path}: invalid JSON: {error}") from error
