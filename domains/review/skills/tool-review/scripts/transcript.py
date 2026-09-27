"""Read a session transcript: which tools of this setup served, and what a slice cost.

Shared by the review domain's Stop hook and by the tool-review scripts. It counts and never
judges. Three properties of the transcript govern it, each seen on real sessions: one API
message is written as one record per content block, each repeating the same usage, so
usage is counted once per message id; a subagent has its own transcript under
<session>/subagents/, beside a .meta.json naming its agentType and the Agent call that
started it; a record can be half-written while the session runs, so a line that does not
parse is skipped.
"""

import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DOMAIN = "review"
REVIEW_SKILL = "tool-review"
BASE_PREFIX = "Base directory for this skill: "
MARKERS = (BASE_PREFIX, '"subagent_type"', '"hook_')
ERROR_TYPES = ("hook_non_blocking_error", "hook_error_during_execution", "hook_cancelled")
IDLE_MINUTES = 5


@dataclass(frozen=True)
class Tool:
    id: str
    kind: str
    name: str
    domain: str
    version: str | None


def when(value):
    """An ISO timestamp as an aware UTC datetime; None when it is not one."""
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def stamp(moment):
    """A datetime written the way the transcript writes it: 2026-09-26T21:42:11.395Z."""
    moment = moment.astimezone(timezone.utc)
    return moment.strftime("%Y-%m-%dT%H:%M:%S.") + f"{moment.microsecond // 1000:03d}Z"


def records(path, markers=None):
    """Each record of a transcript as a dict, in order; with `markers`, only the lines holding one."""
    try:
        handle = open(path, encoding="utf-8")
    except OSError:
        return
    with handle:
        for line in handle:
            if markers and not any(marker in line for marker in markers):
                continue
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                yield record


def load_state(claude_dir):
    """The installer's state, my-claude-setup.json; an empty one when it cannot be read."""
    try:
        state = json.loads((Path(claude_dir) / "my-claude-setup.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"domains": {}}
    return state if isinstance(state, dict) else {"domains": {}}


def repo_of(state):
    """The repository the review domain was installed from, while it still exists."""
    repo = ((state.get("domains") or {}).get(DOMAIN) or {}).get("repo")
    return Path(repo) if repo and Path(repo).is_dir() else None


def load_catalog(claude_dir, state):
    """The catalog of the installed tools.json, <claude>/hooks/review/tools.json."""
    config = json.loads((Path(claude_dir) / "hooks" / DOMAIN / "tools.json").read_text(encoding="utf-8"))
    return catalog(config, state)


def catalog(config, state):
    """The tools `config` lists that this repository installed, by id, with their domain and version."""
    owners = {}
    for domain, entry in (state.get("domains") or {}).items():
        for rel in entry.get("files") or {}:
            owners[rel] = (domain, entry.get("version"))
    found = {}
    for name in config.get("skills", []):
        owner = owners.get(f"skills/{name}/SKILL.md")
        if owner and name != REVIEW_SKILL:
            found[f"skill:{name}"] = Tool(f"skill:{name}", "skill", name, *owner)
    for name in config.get("agents", []):
        owner = owners.get(f"agents/{name}.md")
        if owner:
            found[f"agent:{name}"] = Tool(f"agent:{name}", "agent", name, *owner)
    for name in config.get("hooks", []):
        owner = owners.get(f"hooks/{name}")
        if owner and owner[0] == name.split("/", 1)[0]:
            found[f"hook:{name}"] = Tool(f"hook:{name}", "hook", name, *owner)
    return found


def find_transcript(claude_dir, session):
    matches = sorted((Path(claude_dir) / "projects").glob(f"*/{session}.jsonl"))
    return matches[0] if matches else None


def text_of(record):
    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(block.get("text", "") for block in content
                         if isinstance(block, dict) and block.get("type") == "text")
    return ""


def skill_homes(claude_dir):
    """<claude>/skills, as given and resolved: the transcript may name either."""
    return {Path(claude_dir) / "skills", Path(claude_dir).resolve() / "skills"}


def loaded_skill(record):
    """The directory of the skill a record loaded, or None: only a user record marked isMeta counts."""
    if record.get("type") != "user" or record.get("isMeta") is not True:
        return None
    text = text_of(record)
    if not text.startswith(BASE_PREFIX):
        return None
    return Path(text[len(BASE_PREFIX):].split("\n", 1)[0].strip())


def hook_name(command, claude_dir):
    """`<domain>/<file>` when `command` runs a file under <claude>/hooks/, else None."""
    for home in {Path(claude_dir), Path(claude_dir).resolve()}:
        match = re.search(re.escape(f"{home / 'hooks'}/") + r"([^/\s\"']+/[^/\s\"']+)", command or "")
        if match:
            return match.group(1)
    return None


def injected(stdout):
    """What a hook's output added to the context: its additionalContext, or the output itself."""
    try:
        output = json.loads(stdout)
    except ValueError:
        return len(stdout.strip())
    context = (output.get("hookSpecificOutput") or {}).get("additionalContext") if isinstance(output, dict) else None
    return len(context) if isinstance(context, str) else 0


def events(record, catalog, claude_dir, cwd):
    """(tool id, what, amount) for each use of a catalog tool in `record`.

    `load` carries the characters a skill injected, `call` the Agent tool_use id, `run` the
    characters a hook injected; `block` and `error` carry 1.
    """
    found = []
    kind = record.get("type")
    if kind == "user":
        base = loaded_skill(record)
        if base is not None and base.parent in skill_homes(claude_dir) and f"skill:{base.name}" in catalog:
            found.append((f"skill:{base.name}", "load", len(text_of(record))))
    elif kind == "assistant":
        content = (record.get("message") or {}).get("content")
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict) or block.get("type") != "tool_use" or block.get("name") not in ("Agent", "Task"):
                continue
            name = str((block.get("input") or {}).get("subagent_type") or "")
            project = Path(record.get("cwd") or cwd or ".")
            if f"agent:{name}" in catalog and not (project / ".claude" / "agents" / f"{name}.md").exists():
                found.append((f"agent:{name}", "call", block.get("id", "")))
    elif kind == "attachment":
        attachment = record.get("attachment") or {}
        command = attachment.get("command") or (attachment.get("blockingError") or {}).get("command")
        name = hook_name(command, claude_dir)
        if name is None or f"hook:{name}" not in catalog:
            return found
        what = attachment.get("type", "")
        if what == "hook_success" and str(attachment.get("stdout") or "").strip():
            found.append((f"hook:{name}", "run", injected(attachment["stdout"])))
        elif what == "hook_blocking_error":
            found.append((f"hook:{name}", "block", 1))
        elif what in ERROR_TYPES:
            found.append((f"hook:{name}", "error", 1))
    return found


def within(moment, start, end):
    return moment is not None and not (start and moment < start) and not (end and moment > end)


def uses(path, catalog, claude_dir, cwd, start=None, end=None):
    """The catalog tools the transcript shows in use between start and end, in order of first use."""
    found = {}
    for record in records(path, MARKERS):
        if not within(when(record.get("timestamp")), start, end):
            continue
        for tool_id, _, _ in events(record, catalog, claude_dir, cwd):
            found.setdefault(tool_id, catalog[tool_id])
    return found


def session_start(path):
    for record in records(path):
        moment = when(record.get("timestamp"))
        if moment:
            return moment
    return None


def review_load(path, claude_dir):
    """(time, working directory) of the latest record that loaded tool-review, or None."""
    latest = None
    for record in records(path, (BASE_PREFIX,)):
        base = loaded_skill(record)
        if base is not None and base.name == REVIEW_SKILL and base.parent in skill_homes(claude_dir):
            moment = when(record.get("timestamp"))
            if moment:
                latest = (moment, str(record.get("cwd") or ""))
    return latest
