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
import re
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
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


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
            if not path.is_file() or "__pycache__" in parts or any(part.startswith(".") for part in parts):
                continue
            if prefix == "skills" and len(parts) > 1 and parts[1] == "evals":
                continue
            files[f"{prefix}/{'/'.join(parts)}"] = path
    return files


def validate_hooks(hooks, source):
    """Check that hooks maps each event name to a list of hook groups."""
    valid = isinstance(hooks, dict) and all(
        isinstance(event, str) and isinstance(groups, list) and all(isinstance(group, dict) for group in groups)
        for event, groups in hooks.items()
    )
    if not valid:
        raise SetupError(f"{source}: hooks must map each event to a list of hook groups")


def domain_hooks(domain_dir, claude_dir):
    """The domain's hooks.json, with {{HOOKS_DIR}} resolved; {} when it has none."""
    path = domain_dir / "hooks.json"
    if not path.is_file():
        return {}
    hooks_dir = json.dumps(str(claude_dir / "hooks" / domain_dir.name))[1:-1]
    try:
        hooks = json.loads(path.read_text(encoding="utf-8").replace(PLACEHOLDER, hooks_dir))
    except ValueError as error:
        raise SetupError(f"{path}: invalid JSON: {error}") from error
    validate_hooks(hooks, path)
    return hooks


def domain_version(domain_dir):
    """The domain's VERSION, of the form X.Y.Z; None when it has none."""
    path = domain_dir / "VERSION"
    if not path.is_file():
        return None
    version = path.read_text(encoding="utf-8").strip()
    if not VERSION_RE.match(version):
        raise SetupError(f"{path}: {version!r} is not a version of the form X.Y.Z")
    return version


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
    version: object = None
    conflicts: list = field(default_factory=list)


def make_plan(domains_dir, claude_dir, name, install=True):
    """Work out what installing (or removing) a domain does, without writing anything."""
    state = load_state(claude_dir)
    settings_path = claude_dir / "settings.json"
    settings = read_json(settings_path, {})
    if not isinstance(settings, dict):
        raise SetupError(f"{settings_path}: must be a JSON object")
    validate_hooks(settings.get("hooks", {}), settings_path)
    recorded = state["domains"].get(name, {"files": {}, "hooks": {}})
    files, hooks, version = {}, {}, None
    if install:
        domain_dir = domains_dir / name
        if not domain_dir.is_dir():
            raise SetupError(f"no domain named {name!r} under {domains_dir}")
        files, hooks = domain_files(domain_dir), domain_hooks(domain_dir, claude_dir)
        version = domain_version(domain_dir)
    plan = Plan(name, install, files, hooks, recorded, version)
    plan.conflicts = find_conflicts(plan, state, settings, claude_dir)
    return plan


def symlink_component(claude_dir, rel):
    """True when a path component between claude_dir and rel is itself a symbolic link."""
    path = claude_dir
    for part in Path(rel).parts:
        path = path / part
        if path.is_symlink():
            return True
    return False


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
        elif entry not in own_units and os.path.lexists(claude_dir / entry):
            conflicts.append(f"{entry}: already exists and was not installed by this repository")
    for rel in sorted(plan.files):
        if rel not in plan.recorded["files"] and unit(rel) in own_units and os.path.lexists(claude_dir / rel):
            conflicts.append(f"{rel}: already exists and was not installed by this repository")
        if symlink_component(claude_dir, rel):
            conflicts.append(f"{rel}: a path component is a symbolic link")
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
        state["domains"][plan.name] = {"commit": current_commit(), "version": plan.version,
                                       "files": installed, "hooks": plan.hooks}
    else:
        state["domains"].pop(plan.name, None)
    write_json(claude_dir / STATE_FILE, state)
    return hooks_changed


def status(domains_dir, claude_dir, name, state):
    entry = state["domains"].get(name)
    if entry is None:
        return "off"
    for rel, expected in entry["files"].items():
        target = claude_dir / rel
        if not target.is_file() or digest(target) != expected:
            return "modified"
    domain_dir = domains_dir / name
    if not domain_dir.is_dir():
        return "outdated"
    files = {rel: digest(source) for rel, source in domain_files(domain_dir).items()}
    if (files != entry["files"] or domain_hooks(domain_dir, claude_dir) != entry["hooks"]
            or domain_version(domain_dir) != entry.get("version")):
        return "outdated"
    return "on"


def version_label(domains_dir, name, state, current):
    """The version column of `list`: installed version, repository version, or `installed → repository`."""
    domain_dir = domains_dir / name
    repository = domain_version(domain_dir) if domain_dir.is_dir() else None
    entry = state["domains"].get(name)
    if entry is None:
        return repository or ""
    installed = entry.get("version")
    if current == "outdated" and repository and repository != installed:
        return f"{installed or '?'} → {repository}"
    return installed or ""


def list_domains(domains_dir, claude_dir):
    state = load_state(claude_dir)
    names = set(state["domains"])
    if domains_dir.is_dir():
        names |= {path.name for path in domains_dir.iterdir()
                  if path.is_dir() and not path.name.startswith((".", "__"))}
    if not names:
        print(f"no domain under {domains_dir}")
    for name in sorted(names):
        current = status(domains_dir, claude_dir, name, state)
        print(f"{name:<24} {current:<10} {version_label(domains_dir, name, state, current)}".rstrip())
    return 0


def run(command, names, domains_dir, claude_dir, state, force):
    plans = []
    for name in names:
        if command in ("update", "disable") and name not in state["domains"]:
            raise SetupError(f"{name!r} is not enabled")
        if command == "update" and not (domains_dir / name).is_dir():
            print(f"{name}: no longer in the repository, left in place; make disable D={name} removes it")
            continue
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


def validate_domain_name(name):
    """Reject a domain name that could escape the domains or Claude directory."""
    if not name or name != Path(name).name or name.startswith((".", "__")):
        raise SetupError(f"invalid domain name {name!r}")


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
        if args.command == "list":
            return list_domains(domains_dir, claude_dir)
        if args.command in ("enable", "disable") and not args.domain:
            raise SetupError(f"{args.command} needs a domain: make {args.command} D=<domain>")
        if args.domain:
            validate_domain_name(args.domain)
        state = load_state(claude_dir)
        if args.command == "update" and not args.domain:
            names = sorted(state["domains"])
            if not names:
                print("no domain enabled")
        else:
            names = [args.domain]
        return run(args.command, names, domains_dir, claude_dir, state, args.force)
    except SetupError as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
