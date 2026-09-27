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


def blank(tool_id):
    """A tool's setup entry before counting: zeros are counts, never guesses."""
    kind = tool_id.split(":", 1)[0]
    if kind == "skill":
        return {"loads": 0, "chars": 0, "files_read": {}, "scripts": {}, "script_errors": 0}
    if kind == "agent":
        return {"runs": []}
    return {"runs": 0, "injected_chars": 0, "blocks": 0, "errors": 0}


def script_run(command, name, claude_dir):
    """The script of skill `name` that a Bash command runs, or None."""
    prefixes = [f"{home / name / 'scripts'}/" for home in skill_homes(claude_dir)]
    if Path(claude_dir).resolve() == (Path.home() / ".claude").resolve():
        prefixes += [f"~/.claude/skills/{name}/scripts/", f"$HOME/.claude/skills/{name}/scripts/"]
    for prefix in prefixes:
        index = command.find(prefix)
        if index != -1:
            match = re.match(r"[\w.-]+", command[index + len(prefix):])
            if match:
                return match.group(0)
    return None


def count_skill_files(block, setup, scripts_of, claude_dir):
    """Count a Read of a skill's own file, or a Bash run of one of its scripts."""
    params = block.get("input") or {}
    for tool_id, entry in setup.items():
        if not tool_id.startswith("skill:"):
            continue
        name = tool_id.split(":", 1)[1]
        if block.get("name") == "Read":
            file_path = str(params.get("file_path") or "")
            for home in skill_homes(claude_dir):
                prefix = f"{home / name}/"
                if file_path.startswith(prefix):
                    relative = file_path[len(prefix):]
                    entry["files_read"][relative] = entry["files_read"].get(relative, 0) + 1
                    break
        elif block.get("name") == "Bash":
            script = script_run(str(params.get("command") or ""), name, claude_dir)
            if script:
                entry["scripts"][script] = entry["scripts"].get(script, 0) + 1
                scripts_of[block.get("id")] = tool_id


def agent_runs(path, name, call_ids):
    """One entry per run of agent `name` started by one of `call_ids`: {fresh, cache_read, seconds}."""
    runs = []
    folder = Path(path).with_suffix("") / "subagents"
    for meta_path in sorted(folder.glob("agent-*.meta.json")) if folder.is_dir() else []:
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if meta.get("agentType") != name or meta.get("toolUseId") not in call_ids:
            continue
        seen, fresh, cached, stamps = set(), 0, 0, []
        for record in records(meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))):
            moment = when(record.get("timestamp"))
            if moment:
                stamps.append(moment)
            message = record.get("message") or {}
            key = message.get("id") or record.get("uuid")
            if record.get("type") != "assistant" or key in seen:
                continue
            seen.add(key)
            usage = message.get("usage") or {}
            fresh += (usage.get("input_tokens") or 0) + (usage.get("cache_creation_input_tokens") or 0)
            cached += usage.get("cache_read_input_tokens") or 0
        run = {"fresh": fresh, "cache_read": cached}
        if len(stamps) > 1:
            run["seconds"] = round((max(stamps) - min(stamps)).total_seconds())
        runs.append((min(stamps) if stamps else datetime.max.replace(tzinfo=timezone.utc), run))
    return [run for _, run in sorted(runs, key=lambda item: item[0])]


def active_minutes(stamps):
    ordered = sorted(stamps)
    gaps = ((later - earlier).total_seconds() for earlier, later in zip(ordered, ordered[1:]))
    return round(sum(gap for gap in gaps if gap <= IDLE_MINUTES * 60) / 60)


def measure(path, catalog, claude_dir, start, end, tool_ids):
    """The measured block of the slice [start, end], with one setup entry per tool under review."""
    seen, turns, stamps, peak = set(), 0, [], 0
    tokens = {"fresh": 0, "cache_read": 0, "output": 0}
    tools, friction = Counter(), {"tool_errors": 0, "interruptions": 0}
    setup = {tool_id: blank(tool_id) for tool_id in tool_ids}
    calls = {tool_id: [] for tool_id in tool_ids if tool_id.startswith("agent:")}
    scripts_of = {}
    for record in records(path):
        moment = when(record.get("timestamp"))
        if not within(moment, start, end):
            continue
        message = record.get("message") or {}
        content = message.get("content")
        blocks = [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []
        if record.get("type") == "assistant":
            key = message.get("id") or record.get("requestId") or record.get("uuid")
            if key not in seen:
                seen.add(key)
                usage = message.get("usage") or {}
                fresh = (usage.get("input_tokens") or 0) + (usage.get("cache_creation_input_tokens") or 0)
                cached = usage.get("cache_read_input_tokens") or 0
                tokens["fresh"] += fresh
                tokens["cache_read"] += cached
                tokens["output"] += usage.get("output_tokens") or 0
                peak = max(peak, fresh + cached)
                turns += 1
                stamps.append(moment)
            for block in blocks:
                if block.get("type") == "tool_use":
                    tools[str(block.get("name", "?"))] += 1
                    count_skill_files(block, setup, scripts_of, claude_dir)
        elif record.get("type") == "user":
            if "[Request interrupted" in text_of(record):
                friction["interruptions"] += 1
            for block in blocks:
                if block.get("type") == "tool_result" and block.get("is_error"):
                    friction["tool_errors"] += 1
                    owner = scripts_of.get(block.get("tool_use_id"))
                    if owner:
                        setup[owner]["script_errors"] += 1
        for tool_id, what, amount in events(record, catalog, claude_dir, ""):
            entry = setup.get(tool_id)
            if entry is None:
                continue
            if what == "load":
                entry["loads"] += 1
                entry["chars"] += amount
            elif what == "call":
                calls[tool_id].append(amount)
            elif what == "run":
                entry["runs"] += 1
                entry["injected_chars"] += amount
            elif what == "block":
                entry["blocks"] += 1
            elif what == "error":
                entry["errors"] += 1
    for tool_id, call_ids in calls.items():
        setup[tool_id]["runs"] = agent_runs(path, tool_id.split(":", 1)[1], call_ids)
    return {
        "tokens": tokens,
        "turns": turns,
        "tools": dict(tools.most_common()),
        "friction": friction,
        "setup": setup,
        "derived": {
            "active_minutes": {"value": active_minutes(stamps), "rule": f"wall clock minus every gap over {IDLE_MINUTES} min"},
            "context_peak": {"value": peak, "rule": "largest input of one API call, fresh and cached"},
        },
    }
