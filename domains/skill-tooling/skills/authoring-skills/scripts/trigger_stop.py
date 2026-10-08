#!/usr/bin/env python3
"""The PostToolUse hook of a trigger session: records each call, and stops the session
once it triggered the skill or at its third call.

Usage, as triggers.py gives it in a session's --settings:
    trigger_stop.py <log> <skill-name> <copy>

The session triggered when it called the Skill tool on the skill's name, or named a path
under the skill's copy. The answer {"continue": false} ends the session after the call,
its transcript whole, where killing the process lost the transcript's tail (probed on
2026-10-06, Phase 4 of roadmap skill-tooling, task 2). A call it cannot read counts
toward the three.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402  (same directory, not an installed package)

CALLS = 3
SKILL_TOOL = "Skill"
SKILL_KEY = "skill"
PATH_END = r"(?=$|[/\s'\"`;|&()<>])"


def triggered(tool, given, name, copy):
    """Whether a call used the skill: the Skill tool on its name, or a path under its copy."""
    if tool == SKILL_TOOL and isinstance(given, dict) and given.get(SKILL_KEY) == name:
        return True
    under = re.compile(re.escape(str(copy)) + PATH_END)
    return any(under.search(text) for text in harness.strings(given))


def main(argv=None):
    log, name, copy = (sys.argv[1:] if argv is None else argv)[:3]
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    event = event if isinstance(event, dict) else {}
    tool, given = event.get("tool_name"), event.get("tool_input") or {}
    log = Path(log)
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"tool": tool, "input": given}) + "\n")
    count = len(log.read_text(encoding="utf-8").splitlines())
    hit = triggered(tool, given, name, copy)
    if hit or count >= CALLS:
        reason = f"the skill `{name}` triggered" if hit else f"{CALLS} calls without the skill `{name}`"
        print(json.dumps({"continue": False, "stopReason": f"Trigger eval: {reason}."}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
