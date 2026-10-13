"""Read a session transcript: which tools of this setup served, and what a slice cost.

Shared by the review domain's Stop hook and by the tool-review scripts. It counts and never
judges. Three properties of the transcript govern it, each seen on real sessions: one API
message is written as one record per content block, each repeating the same usage, so
usage is counted once per message id; a subagent has its own transcript under
<session>/subagents/, beside a .meta.json naming its agentType and the Agent call that
started it; a record can be half-written while the session runs, so a line that does not
parse is skipped. The calls, a session's runs and their cost are read by usage.py, the reader
copied beside it from shared/usage/: each call once, its final usage, its time its first
record's, its model and effort.
"""

import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import conventions
import usage

DOMAIN = "review"
REVIEW_SKILL = "tool-review"
BASE_PREFIX = "Base directory for this skill: "
MARKERS = (BASE_PREFIX, '"subagent_type"', '"hook_')
ERROR_TYPES = ("hook_non_blocking_error", "hook_error_during_execution", "hook_cancelled")
IDLE_MINUTES = 5
DIGITS = 4  # dollars are kept to the hundredth of a cent
EFFORTS = ("low", "medium", "high", "xhigh", "max")


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
    """The installer's state, my-agent-setup.json; an empty one when it cannot be read."""
    try:
        state = json.loads((Path(claude_dir) / "my-agent-setup.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"domains": {}}
    return state if isinstance(state, dict) else {"domains": {}}


def repo_of(state):
    """The repository the review domain was installed from, while it still exists."""
    repo = ((state.get("domains") or {}).get(DOMAIN) or {}).get("repo")
    return Path(repo) if repo and Path(repo).is_dir() else None


def load_config(claude_dir):
    """The installed tools.json, <claude>/hooks/review/tools.json: the points to watch."""
    return json.loads((Path(claude_dir) / "hooks" / DOMAIN / "tools.json").read_text(encoding="utf-8"))


def installed(state):
    """Every tool this repository installed, by id, with its domain and version; the review domain's left out."""
    found = {}
    for domain, entry in (state.get("domains") or {}).items():
        if domain == DOMAIN:
            continue
        for rel in entry.get("files") or {}:
            parts = rel.split("/")
            if len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
                kind, name = "skill", parts[1]
            elif len(parts) == 2 and parts[0] == "agents" and parts[1].endswith(".md"):
                kind, name = "agent", parts[1].removesuffix(".md")
            elif len(parts) == 3 and parts[0] == "hooks" and parts[1] == domain:
                kind, name = "hook", f"{domain}/{parts[2]}"
            else:
                continue
            found[f"{kind}:{name}"] = Tool(f"{kind}:{name}", kind, name, domain, entry.get("version"))
    return found


def reviewed(repo):
    """The [review] table's tools in repo's .agent-conventions.toml, read by its path; [] unless it reads ok."""
    path = Path(repo) / conventions.FILE
    if not path.is_file():
        return []
    result = conventions.load(DOMAIN, Path(repo), path)
    return result.values["tools"] if result.status == "ok" else []


def chosen(catalog, entries):
    """The tools of `catalog` that an entry names, by its id or by its domain."""
    return {tool_id: tool for tool_id, tool in catalog.items() if tool_id in entries or tool.domain in entries}


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


def count_skill_files(block, setup, scripts_of, claude_dir, texts_of=None):
    """Count a Read of a skill's own file, or a Bash run of one of its scripts; texts_of takes the call's id."""
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
                    if texts_of is not None:
                        texts_of[block.get("id")] = tool_id
                    break
        elif block.get("name") == "Bash":
            script = script_run(str(params.get("command") or ""), name, claude_dir)
            if script:
                entry["scripts"][script] = entry["scripts"].get(script, 0) + 1
                scripts_of[block.get("id")] = tool_id
                if texts_of is not None:
                    texts_of[block.get("id")] = tool_id


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
        transcript = meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))
        stamps = [moment for moment in (when(record.get("timestamp")) for record in records(transcript)) if moment]
        calls = usage.calls(transcript) if transcript.is_file() else []
        run = {"fresh": sum(call.input + call.write_5m + call.write_1h for call in calls),
               "cache_read": sum(call.cache_read for call in calls)}
        if len(stamps) > 1:
            run["seconds"] = round((max(stamps) - min(stamps)).total_seconds())
        runs.append((min(stamps) if stamps else datetime.max.replace(tzinfo=timezone.utc), run))
    return [run for _, run in sorted(runs, key=lambda item: item[0])]


def result_chars(block):
    """The characters of a tool result's text, its images left out."""
    content = block.get("content")
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(str(item.get("text") or "")) for item in content
                   if isinstance(item, dict) and item.get("type") == "text")
    return 0


def blocked_chars(record):
    """The characters of the reason a hook's block gave the agent."""
    reason = ((record.get("attachment") or {}).get("blockingError") or {}).get("blockingError")
    return len(reason) if isinstance(reason, str) else 0


def dollars(value):
    return round(value, DIGITS)


def effort_rank(effort):
    if effort in EFFORTS:
        return 0, EFFORTS.index(effort), ""
    return (1, 0, effort) if effort else (2, 0, "")


def priced(calls):
    """(dollars, estimated dollars) of the calls the price table prices; the others are left out."""
    total = estimated = 0.0
    for call in calls:
        cost = usage.cost(call)
        if cost is not None:
            total += cost
            estimated += usage.estimated_cost(call)
    return total, estimated


def leaf(calls):
    """{calls, dollars, estimated}: dollars when the table prices a call, estimated when a call rests on one."""
    found = {"calls": len(calls)}
    if any(usage.cost(call) is not None for call in calls):
        total, estimated = priced(calls)
        found["dollars"] = dollars(total)
        if any(call.estimated for call in calls):
            found["estimated"] = dollars(estimated)
    return found


def by_model(calls):
    """The calls' figures by model, then by effort for a model whose calls carry one, `none` for those without."""
    found = {}
    for model in sorted({call.model for call in calls}):
        own = [call for call in calls if call.model == model]
        efforts = sorted({call.effort for call in own}, key=effort_rank)
        if efforts == [None]:
            found[model] = leaf(own)
        else:
            found[model] = {effort or "none": leaf([call for call in own if call.effort == effort])
                            for effort in efforts}
    return found


def part(calls):
    """{calls, dollars, estimated, models} of a part of the slice: its main thread, its subagents, a run, a turn."""
    total, estimated = priced(calls)
    return {"calls": len(calls), "dollars": dollars(total), "estimated": dollars(estimated), "models": by_model(calls)}


def slice_cost(main, subagents):
    """The slice's cost: the prices' date, its dollars and estimated part, its main thread and subagents apart."""
    total, estimated = priced(main + subagents)
    found = {"prices": usage.PRICES_READ, "dollars": dollars(total), "estimated": dollars(estimated),
             "main": part(main), "subagents": part(subagents)}
    unknown = Counter(call.model for call in main + subagents if usage.cost(call) is None)
    if unknown:
        found["unknown"] = dict(sorted(unknown.items()))
    return found


def holders(main, moment):
    """The main thread's calls after `moment` that hold a text given then: up to the next compaction's call."""
    found = []
    for call in main:
        if when(call.time) is None or when(call.time) <= moment:
            continue
        found.append(call)
        if call.derived:
            break
    return found


def text_cost(texts, main):
    """{tokens, dollars} of texts given as (time, characters), each priced on the calls that hold it."""
    tokens, total = 0, 0.0
    for moment, characters in texts:
        found, cost = usage.text_cost(characters, holders(main, moment))
        tokens += found
        total = None if cost is None or total is None else total + cost
    return {"tokens": tokens} if total is None else {"tokens": tokens, "dollars": dollars(total)}


def tool_cost_rule():
    return (f"a tool's text at {usage.estimate('text').value:g} characters a token, one one-hour write and a read "
            "by each later call up to a compaction; an agent's runs at their own cost")


def active_minutes(stamps):
    ordered = sorted(stamps)
    gaps = ((later - earlier).total_seconds() for earlier, later in zip(ordered, ordered[1:]))
    return round(sum(gap for gap in gaps if gap <= IDLE_MINUTES * 60) / 60)


def measure(path, catalog, claude_dir, start, end, tool_ids):
    """The measured block of the slice [start, end], with one setup entry per tool under review.

    The calls are usage.py's, each counted by its time: the token counts take the main thread's
    recorded figures, a call without its final usage adding no output; the cost adds the
    compactions' derived calls and the subagents, estimates marked.
    """
    session = usage.session(path)
    main = [call for call in session.main if within(when(call.time), start, end)]
    subagents = [call for run in session.runs for call in run.calls if within(when(call.time), start, end)]
    counted = [call for call in main if not call.derived]
    tokens = {"fresh": sum(call.input + call.write_5m + call.write_1h for call in counted),
              "cache_read": sum(call.cache_read for call in counted),
              "output": sum(call.output for call in counted if call.final)}
    tools, friction = Counter(), {"tool_errors": 0, "interruptions": 0}
    setup = {tool_id: blank(tool_id) for tool_id in tool_ids}
    calls = {tool_id: [] for tool_id in tool_ids if tool_id.startswith("agent:")}
    texts = {tool_id: [] for tool_id in tool_ids if not tool_id.startswith("agent:")}
    scripts_of, texts_of = {}, {}
    for record in records(path):
        moment = when(record.get("timestamp"))
        if not within(moment, start, end):
            continue
        message = record.get("message") or {}
        content = message.get("content")
        blocks = [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []
        if record.get("type") == "assistant":
            for block in blocks:
                if block.get("type") == "tool_use":
                    tools[str(block.get("name", "?"))] += 1
                    count_skill_files(block, setup, scripts_of, claude_dir, texts_of)
        elif record.get("type") == "user":
            if "[Request interrupted" in text_of(record):
                friction["interruptions"] += 1
            for block in blocks:
                if block.get("type") != "tool_result":
                    continue
                if block.get("tool_use_id") in texts_of:
                    texts[texts_of[block.get("tool_use_id")]].append((moment, result_chars(block)))
                if block.get("is_error"):
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
                texts[tool_id].append((moment, amount))
            elif what == "call":
                calls[tool_id].append(amount)
            elif what == "run":
                entry["runs"] += 1
                entry["injected_chars"] += amount
                texts[tool_id].append((moment, amount))
            elif what == "block":
                entry["blocks"] += 1
                texts[tool_id].append((moment, blocked_chars(record)))
            elif what == "error":
                entry["errors"] += 1
    own = {tool_id: text_cost(found, main) for tool_id, found in texts.items()}
    for tool_id, call_ids in calls.items():
        setup[tool_id]["runs"] = agent_runs(path, tool_id.split(":", 1)[1], call_ids)
        own[tool_id] = part([call for run in session.runs if run.tool_use in call_ids for call in run.calls])
    derived = {
        "active_minutes": {"value": active_minutes([when(call.time) for call in counted if when(call.time)]),
                           "rule": f"wall clock minus every gap over {IDLE_MINUTES} min"},
        "context_peak": {"value": max((call.prompt for call in counted), default=0),
                         "rule": "largest input of one API call, fresh and cached"},
    }
    if tool_ids:
        derived["tool_cost"] = {"value": {tool_id: own[tool_id] for tool_id in tool_ids}, "rule": tool_cost_rule()}
    return {
        "tokens": tokens,
        "turns": len(counted),
        "tools": dict(tools.most_common()),
        "friction": friction,
        "setup": setup,
        "cost": slice_cost(main, subagents),
        "derived": derived,
    }


def review_turn(path, claude_dir, requested, closed):
    """The review's own turn: the main thread's calls after its request, up to the first call after
    tool-review's record.py answered without an error, or up to `closed` when that comes first."""
    started, answered = set(), None
    for record in records(path, ('"tool_use"', '"tool_result"')):
        moment = when(record.get("timestamp"))
        if moment is None or moment <= requested:
            continue
        content = (record.get("message") or {}).get("content")
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if (block.get("type") == "tool_use" and block.get("name") == "Bash"
                    and script_run(str((block.get("input") or {}).get("command") or ""), REVIEW_SKILL,
                                   claude_dir) == "record.py"):
                started.add(block.get("id"))
            elif (block.get("type") == "tool_result" and block.get("tool_use_id") in started
                  and not block.get("is_error")):
                answered = answered or moment
        if answered:
            break
    turn = [call for call in usage.calls(path) if when(call.time) and requested < when(call.time) <= closed]
    later = [call for call in turn if answered and when(call.time) > answered]
    if later:
        turn = [call for call in turn if when(call.time) <= when(later[0].time)]
    return part(turn)
