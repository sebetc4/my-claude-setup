"""A temporary world for the review domain's tests: a Claude directory with its installer
state and tools.json, a repository, a project, and the transcript of one session."""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
HOOK = DOMAIN / "hooks" / "review.py"
SCRIPTS = DOMAIN / "skills" / "tool-review" / "scripts"
SESSION = "aabb0fa1-f563-4ec2-8228-00c695fa7a0c"
TOOLS = {"skills": ["roadmap"], "agents": ["roadmap-auditor"],
         "hooks": ["roadmap/session_resume.py", "roadmap/progress_guard.py"]}
INSTALLED = ("skills/roadmap/SKILL.md", "skills/roadmap/scripts/progress.py", "agents/roadmap-auditor.md",
             "hooks/roadmap/session_resume.py", "hooks/roadmap/progress_guard.py")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%S.") + f"{moment.microsecond // 1000:03d}Z"


class World:
    def __init__(self, root, tools=TOOLS, installed=True):
        root = Path(root).resolve()
        self.claude, self.repo, self.project = root / "claude", root / "repo", root / "project"
        self.session = SESSION
        self.transcript = self.claude / "projects" / "-project" / f"{SESSION}.jsonl"
        self.clock = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(hours=1)
        self.lines, self.counter = [], 0
        files = {rel: "digest" for rel in INSTALLED} if installed else {}
        state = {"domains": {
            "roadmap": {"version": "1.1.1", "files": files, "hooks": {}},
            "review": {"version": "0.1.0", "repo": str(self.repo),
                       "files": {"skills/tool-review/SKILL.md": "digest"}, "hooks": {}},
        }}
        write(self.claude / "my-claude-setup.json", json.dumps(state))
        write(self.claude / "hooks" / "review" / "tools.json", json.dumps(tools))
        write(self.repo / "domains" / "roadmap" / "hooks" / "session_resume.py", "print()\n")
        self.project.mkdir(parents=True)
        self.save()

    def tick(self, seconds=5):
        self.clock += timedelta(seconds=seconds)
        return iso(self.clock)

    def next_id(self, prefix):
        self.counter += 1
        return f"{prefix}{self.counter:04d}"

    def save(self):
        self.transcript.parent.mkdir(parents=True, exist_ok=True)
        self.transcript.write_text("".join(line + "\n" for line in self.lines), encoding="utf-8")

    def add(self, record):
        record.setdefault("timestamp", self.tick())
        record.setdefault("cwd", str(self.project))
        record.setdefault("sessionId", self.session)
        self.lines.append(json.dumps(record))
        self.save()
        return record

    def prompt(self, text):
        return self.add({"type": "user", "message": {"role": "user", "content": text}})

    def reply(self, *blocks, fresh=100, cached=1000, output=50):
        """One API message, written as one record per content block, each repeating the same usage."""
        message_id = self.next_id("msg_")
        usage = {"input_tokens": 1, "cache_creation_input_tokens": fresh - 1,
                 "cache_read_input_tokens": cached, "output_tokens": output}
        for block in blocks or ({"type": "text", "text": "ok"},):
            self.add({"type": "assistant", "message": {"id": message_id, "role": "assistant",
                                                       "content": [block], "usage": usage}})
        return message_id

    def tool_use(self, name, **params):
        call = self.next_id("toolu_")
        self.reply({"type": "tool_use", "id": call, "name": name, "input": params})
        return call

    def result(self, call, text="done", error=False):
        return self.add({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": call, "content": text, "is_error": error}]}})

    def load_skill(self, name, base=None, typed=False):
        """Load a skill by a Skill call, or by /name typed by the user; returns the isMeta record."""
        base = base or self.claude / "skills" / name
        record = {"type": "user", "isMeta": True, "message": {"role": "user", "content": [
            {"type": "text", "text": f"Base directory for this skill: {base}\n\n# {name}\n\nThe skill's body."}]}}
        if typed:
            self.prompt(f"<command-name>/{name}</command-name>")
        else:
            record["sourceToolUseID"] = self.tool_use("Skill", skill=name)
        return self.add(record)

    def call_agent(self, name, fresh=500, cached=2000, seconds=40):
        """An Agent call, and the run's own transcript and meta file under <session>/subagents/."""
        call = self.tool_use("Agent", subagent_type=name, description="audit", prompt="audit it")
        folder = self.transcript.with_suffix("") / "subagents"
        agent = self.next_id("agent-a")
        write(folder / f"{agent}.meta.json", json.dumps({"agentType": name, "toolUseId": call}))
        run = [{"type": "assistant", "timestamp": iso(self.clock + timedelta(seconds=offset)),
                "message": {"id": f"{agent}-{offset}", "role": "assistant", "content": [{"type": "text", "text": "x"}],
                            "usage": {"input_tokens": 0, "cache_creation_input_tokens": fresh // 2,
                                      "cache_read_input_tokens": cached // 2, "output_tokens": 1}}}
               for offset in (1, 1 + seconds)]
        write(folder / f"{agent}.jsonl", "".join(json.dumps(record) + "\n" for record in run))
        self.result(call, "VERDICT: PASS")
        return call

    def hook(self, name, kind="hook_success", context="Roadmap phase in progress.", event="SessionStart"):
        """A record of the hook <claude>/hooks/<name>: an output, a block, or an error."""
        command = f'python3 "{self.claude}/hooks/{name}"'
        if kind == "hook_blocking_error":
            attachment = {"type": kind, "hookEvent": event, "blockingError": {"blockingError": "no", "command": command}}
        else:
            stdout = json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}) if context else ""
            attachment = {"type": kind, "hookEvent": event, "command": command, "stdout": stdout, "exitCode": 0}
        return self.add({"type": "attachment", "attachment": attachment})

    def run_hook(self, stop_hook_active=False, attended="1", raw=None):
        event = raw if raw is not None else json.dumps({
            "session_id": self.session, "transcript_path": str(self.transcript), "cwd": str(self.project),
            "hook_event_name": "Stop", "stop_hook_active": stop_hook_active})
        env = {**os.environ, "CLAUDE_CODE_SESSION_ATTENDED": attended}
        return subprocess.run([sys.executable, "-B", str(HOOK), "--claude-dir", str(self.claude)],
                              input=event, capture_output=True, text=True, env=env)

    def run_script(self, name, *args, cwd=None):
        return subprocess.run([sys.executable, "-B", str(SCRIPTS / name), *args,
                               "--claude-dir", str(self.claude), "--session", self.session],
                              capture_output=True, text=True, cwd=cwd)

    def reviews(self):
        return sorted((self.repo / "reviews").glob("*.md"))
