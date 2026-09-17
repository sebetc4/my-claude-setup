#!/usr/bin/env python3
"""Install the domains of this repository into a Claude Code directory.

Usage: python3 tools/claude_setup.py [--claude-dir DIR] [--domains-dir DIR] [--force]
                                     {list,enable,update,disable} [DOMAIN]

A domain is a folder under domains/. Its skills/, agents/ and commands/ are
copied into the Claude Code directory, its hooks/ into hooks/<domain>/, and its
hooks.json is merged into settings.json. What was installed is recorded in
my-claude-setup.json there, so that update and disable touch nothing else.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
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


def read_json(path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise SetupError(f"{path}: invalid JSON, fix it by hand first: {error}") from error


def write_json(path, data):
    """Write through a temporary file and a rename, keeping the existing file's mode."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.chmod(tmp, path.stat().st_mode & 0o777 if path.exists() else 0o644)
    os.replace(tmp, path)


def load_state(claude_dir):
    return read_json(claude_dir / STATE_FILE, {"domains": {}})


def current_commit():
    try:
        result = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True)
    except OSError:
        return None
    return result.stdout.strip() or None


@dataclass
class Plan:
    name: str
    install: bool
    files: dict
    hooks: dict
    recorded: dict
    conflicts: list = field(default_factory=list)


def make_plan(domains_dir, claude_dir, name, install=True):
    """Work out what installing (or removing) a domain does, without writing anything."""
    state = load_state(claude_dir)
    settings = read_json(claude_dir / "settings.json", {})
    recorded = state["domains"].get(name, {"files": {}, "hooks": {}})
    files, hooks = {}, {}
    if install:
        domain_dir = domains_dir / name
        if not domain_dir.is_dir():
            raise SetupError(f"no domain named {name!r} under {domains_dir}")
        files, hooks = domain_files(domain_dir), domain_hooks(domain_dir, claude_dir)
    plan = Plan(name, install, files, hooks, recorded)
    plan.conflicts = find_conflicts(plan, state, settings, claude_dir)
    return plan


def find_conflicts(plan, state, settings, claude_dir):
    """Everything that makes the plan overwrite or lose something it did not install."""
    conflicts = []
    for rel, expected in plan.recorded["files"].items():
        target = claude_dir / rel
        if not target.is_file():
            conflicts.append(f"{rel}: removed from {claude_dir}")
        elif digest(target) != expected:
            conflicts.append(f"{rel}: modified in {claude_dir}")
    owners = {unit(rel): other for other, entry in state["domains"].items()
              if other != plan.name for rel in entry["files"]}
    own_units = {unit(rel) for rel in plan.recorded["files"]}
    for entry in sorted({unit(rel) for rel in plan.files}):
        if entry in owners:
            conflicts.append(f"{entry}: installed by domain {owners[entry]!r}")
        elif entry not in own_units and (claude_dir / entry).exists():
            conflicts.append(f"{entry}: already exists and was not installed by this repository")
    current = settings.get("hooks", {})
    for event, groups in plan.recorded["hooks"].items():
        for group in groups:
            if group not in current.get(event, []):
                conflicts.append(f"settings.json: a {event} hook installed by {plan.name!r} was changed or removed")
    return conflicts


def remove_file(claude_dir, rel):
    """Delete an installed file, then the directories it leaves empty, up to its kind's directory."""
    target = claude_dir / rel
    if target.is_file():
        target.unlink()
    top = claude_dir / rel.split("/")[0]
    parent = target.parent
    while parent != top and parent.is_dir() and not any(parent.iterdir()):
        parent.rmdir()
        parent = parent.parent


def update_settings(claude_dir, old, new):
    """Replace the hook groups `old` with `new` in settings.json, after a backup."""
    path = claude_dir / "settings.json"
    settings = read_json(path, {})
    if path.is_file():
        backup = claude_dir / "backups" / "my-claude-setup" / f"settings-{datetime.now():%Y%m%d-%H%M%S-%f}.json"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, backup)
    hooks = settings.setdefault("hooks", {})
    for event, groups in old.items():
        for group in groups:
            if group in hooks.get(event, []):
                hooks[event].remove(group)
    for event, groups in new.items():
        hooks.setdefault(event, []).extend(groups)
    for event in [event for event, groups in hooks.items() if not groups]:
        del hooks[event]
    if not hooks:
        del settings["hooks"]
    write_json(path, settings)


def apply_plan(plan, claude_dir):
    """Carry out a plan; returns True when settings.json changed."""
    for rel in sorted(set(plan.recorded["files"]) - set(plan.files)):
        remove_file(claude_dir, rel)
    installed = {}
    for rel, source in plan.files.items():
        target = claude_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, target)
        installed[rel] = digest(target)
    hooks_changed = plan.hooks != plan.recorded["hooks"]
    if hooks_changed:
        update_settings(claude_dir, plan.recorded["hooks"], plan.hooks)
    state = load_state(claude_dir)
    if plan.install:
        state["domains"][plan.name] = {"commit": current_commit(), "files": installed, "hooks": plan.hooks}
    else:
        state["domains"].pop(plan.name, None)
    write_json(claude_dir / STATE_FILE, state)
    return hooks_changed


def run(command, names, domains_dir, claude_dir, state, force):
    plans = []
    for name in names:
        if command in ("update", "disable") and name not in state["domains"]:
            raise SetupError(f"{name!r} is not enabled")
        plans.append(make_plan(domains_dir, claude_dir, name, install=command != "disable"))
    blocked = [plan for plan in plans if plan.conflicts]
    if blocked and not force:
        for plan in blocked:
            print(f"{plan.name}: blocked by conflicts")
            for conflict in plan.conflicts:
                print(f"  - {conflict}")
        print("Nothing was changed. Run again with FORCE=1 to override.")
        return 1
    hooks_changed = False
    for plan in plans:
        hooks_changed |= apply_plan(plan, claude_dir)
        verb = {"enable": "enabled", "update": "updated", "disable": "disabled"}[command]
        print(f"{plan.name}: {verb}, {len(plan.files)} file(s) installed")
    if hooks_changed:
        print("Hooks changed: restart Claude Code to load them.")
    return 0


def parse(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--domains-dir", type=Path, default=REPO / "domains")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("command", choices=("list", "enable", "update", "disable"))
    parser.add_argument("domain", nargs="?")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse(argv)
    claude_dir = args.claude_dir.expanduser().resolve()
    domains_dir = args.domains_dir.expanduser().resolve()
    try:
        if args.command in ("enable", "disable") and not args.domain:
            raise SetupError(f"{args.command} needs a domain: make {args.command} D=<domain>")
        state = load_state(claude_dir)
        return run(args.command, [args.domain], domains_dir, claude_dir, state, args.force)
    except SetupError as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
