"""Build, start and read the agent sessions that evaluations run: Claude Code's `claude -p`.

Every tie to Claude Code that the evaluation scripts have, but the usage count of
usage.py, lies here: the command line and its flags, the minimum version, the variables
removed from a session's environment, the settings that add a hook, the json result, and
where a session's transcript is written and what its records hold. Another agent needs
another harness.py.

Probed on 2026-10-06 (Phase 4 of roadmap skill-tooling, task 2), on 2.1.291 and 2.1.292:
--setting-sources project,local leaves out the user's hooks, skills, agents, permission
rules and model settings while the project's hooks and the skills of --add-dir stay;
--strict-mcp-config keeps out the claude.ai connectors; --permission-mode auto with
--permission-prompts none refuses a call that would wait for a person; --model and
--effort apply to every call, where 2.1.283 did not know claude-sonnet-5-5 and ignored
the effort.
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

COMMAND = "claude"
MIN_VERSION = (2, 1, 291)
DISALLOWED = ("Skill", "Agent")
VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")
# Variables of the starting session a run must not inherit: CLAUDECODE refuses a nested
# session, CLAUDE_EFFORT carries the parent's effort, CLAUDE_CODE_SESSION_ATTENDED=1 makes
# hooks act as in an attended session. CLAUDE_CONFIG_DIR names the user's configuration,
# credentials included, and stays.
KEPT = ("CLAUDE_CONFIG_DIR",)
# The api_error of a session the subscription's usage limit stopped (2.1.292, 2026-10-07).
LIMIT_ERROR = "usage_limit_reached"
SHOWN = 2000


class HarnessError(Exception):
    pass


def config_dir(env=None):
    env = os.environ if env is None else env
    return Path(env.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")


def binary():
    found = shutil.which(COMMAND)
    if not found:
        raise HarnessError(f"no `{COMMAND}` on the PATH")
    return found


def recent_enough(text):
    match = VERSION_RE.search(text)
    return bool(match) and tuple(int(n) for n in match.groups()) >= MIN_VERSION


def version(path):
    """The binary's version, refused when older than MIN_VERSION."""
    result = subprocess.run([path, "--version"], capture_output=True, text=True)
    text = result.stdout.strip()
    match = VERSION_RE.search(text)
    if not match or not recent_enough(text):
        minimum = ".".join(map(str, MIN_VERSION))
        raise HarnessError(f"`{COMMAND}` {text or 'of unknown version'} is older than {minimum}, the version the "
                           "evaluation's flags were probed on: update it first")
    return match.group(0)


def environment(parent, extra):
    """The parent's environment without its session's CLAUDE* variables, plus extra."""
    kept = {k: v for k, v in parent.items() if not k.startswith("CLAUDE") or k in KEPT}
    return {**kept, **extra}


def hook_settings(event, command, matcher="*"):
    """The --settings value that adds one command hook."""
    return json.dumps({"hooks": {event: [{"matcher": matcher, "hooks": [{"type": "command", "command": command}]}]}})


def guard_command(guard, denied):
    """The command of the PreToolUse hook that refuses calls naming the denied paths."""
    return shlex.join([sys.executable, "-B", str(guard), *(str(p) for p in denied)])


def command(path, model, effort, budget, settings, add_dirs=(), disallowed=DISALLOWED, agent=None, session_id=None):
    """The command line of an unattended session; the prompt goes on its standard input.
    session_id, a UUID: the session's id, known before it starts, so that its transcript
    can be followed while it runs.
    agent, (file, name): the session runs as that agent, defined in the file that
    agents_file wrote. Its model and effort still come from model and effort: probed on
    2.1.291, a session started with --agent takes the agent's model but not its effort."""
    line = [path, "-p", "--model", model, "--effort", effort, "--max-budget-usd", str(budget),
            "--permission-mode", "auto", "--permission-prompts", "none",
            "--setting-sources", "project,local", "--strict-mcp-config",
            "--settings", settings, "--output-format", "json"]
    if disallowed:
        line += ["--disallowed-tools", *disallowed]
    for folder in add_dirs:
        line += ["--add-dir", str(folder)]
    if agent:
        line += ["--agents", str(agent[0]), "--agent", agent[1]]
    if session_id:
        line += ["--session-id", session_id]
    return line


def agents_file(path, name, description, prompt, tools, model, effort):
    """Write the --agents file that defines one agent."""
    definition = {"description": description, "prompt": prompt, "tools": list(tools), "model": model,
                  "effort": effort}
    Path(path).write_text(json.dumps({name: definition}, indent=1) + "\n", encoding="utf-8")


@dataclass
class Session:
    returncode: int
    stdout: str
    stderr: str
    seconds: float
    timed_out: bool = False


def start(line, cwd, prompt, env, timeout=None):
    """Run one session to its end."""
    began = time.monotonic()
    try:
        done = subprocess.run(line, cwd=cwd, input=prompt, capture_output=True, text=True, env=env, timeout=timeout)
    except subprocess.TimeoutExpired as expired:
        out = expired.stdout.decode() if isinstance(expired.stdout, bytes) else expired.stdout or ""
        return Session(-1, out, "", time.monotonic() - began, timed_out=True)
    return Session(done.returncode, done.stdout, done.stderr, time.monotonic() - began)


def result_of(stdout):
    """The json result a session printed, or None."""
    for line in reversed(stdout.strip().splitlines()):
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if isinstance(value, dict) and value.get("type") == "result":
            return value
    try:
        value = json.loads(stdout)
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def outcome(session, result):
    """(status, reason): complete, or stopped with what stopped it."""
    if session.timed_out:
        return "stopped", "timeout"
    if result is None:
        return "stopped", f"no result, exit code {session.returncode}: {session.stderr.strip()[:300]}"
    if result.get("subtype") == "success" and not result.get("is_error"):
        return "complete", None
    subtype = result.get("subtype")
    cause = (result.get("api_error") or (subtype if subtype != "success" else None) or result.get("terminal_reason")
             or "error")
    if result.get("api_error") and result.get("result"):
        cause += ": " + result["result"].strip()[:SHOWN // 10]
    return "stopped", cause


def limit_reached(result):
    """Whether the subscription's usage limit stopped the session."""
    return bool(result) and result.get("api_error") == LIMIT_ERROR


def figures(result):
    """What the run.json keeps from the json result."""
    result = result or {}
    duration = result.get("duration_ms")
    return {"session_id": result.get("session_id"), "reported_cost_usd": result.get("total_cost_usd"),
            "duration_s": duration / 1000 if duration is not None else None, "turns": result.get("num_turns"),
            "refusals": result.get("permission_denials") or [], "response": result.get("result") or ""}


def transcript_of(session_id, env=None):
    """The session's transcript file, or None."""
    if not session_id:
        return None
    found = sorted((config_dir(env) / "projects").glob(f"*/{session_id}.jsonl"))
    return found[0] if found else None


def records(path):
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                yield record


def blocks(record):
    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [b for b in content or [] if isinstance(b, dict)]


def tool_calls(path):
    """[(tool name, input)] of the transcript's calls, in order, each tool_use id once."""
    seen, calls = set(), []
    for record in records(path):
        if record.get("type") != "assistant":
            continue
        for block in blocks(record):
            if block.get("type") == "tool_use" and block.get("id") not in seen:
                seen.add(block.get("id"))
                calls.append((block.get("name"), block.get("input") or {}))
    return calls


def strings(value):
    """Every string inside a tool's input."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def shorten(text):
    return text if len(text) <= SHOWN else text[:SHOWN] + f"\n… ({len(text) - SHOWN} more characters)"


def result_text(block):
    content = block.get("content")
    if isinstance(content, list):
        content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return str(content or "")


def render(path):
    """The transcript as Markdown: the prompt, then each text, call and result in order."""
    lines, seen = [], set()
    for record in records(path):
        kind = record.get("type")
        if kind not in ("user", "assistant") or record.get("isMeta"):
            continue
        for block in blocks(record):
            key = block.get("id") or block.get("tool_use_id")
            if key and (kind, key) in seen:
                continue
            seen.add((kind, key))
            if block.get("type") == "text" and block.get("text", "").strip():
                lines += [f"## {'Prompt' if kind == 'user' else 'Agent'}", "", shorten(block["text"].strip()), ""]
            elif block.get("type") == "tool_use":
                given = json.dumps(block.get("input") or {}, ensure_ascii=False, indent=1)
                lines += [f"### Call: {block.get('name')}", "", "```json", shorten(given), "```", ""]
            elif block.get("type") == "tool_result":
                state = " (error)" if block.get("is_error") else ""
                lines += [f"### Result{state}", "", "```", shorten(result_text(block)), "```", ""]
    return "\n".join(lines)
