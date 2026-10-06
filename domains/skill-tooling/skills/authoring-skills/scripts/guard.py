#!/usr/bin/env python3
"""The PreToolUse hook that keeps an evaluation run inside its copy.

Usage, as a hook command: guard.py <denied path> ...

Reads the call on standard input and refuses it when any string of its input names a
denied path — the real repository's root and the real configuration folder, which run.py
passes: as written, without its leading slash, and under the home folder as `~/`,
`$HOME/` or `${HOME}/`. A path counts only whole, so that `/code/repo` does not refuse
`/code/repository`. An unreadable call is refused. The refusal is Claude Code's
PreToolUse decision, printed on standard output; a call allowed prints nothing.
"""

import json
import os
import re
import sys

EDGE = r"[\w.-]"
REASON = "outside the test's limits"


def forms(path, home):
    """The ways a command can name path."""
    path = path.rstrip("/") or "/"
    found = {path, path.lstrip("/")}
    home = home.rstrip("/")
    if home and (path == home or path.startswith(home + "/")):
        rest = path[len(home):]
        found |= {"~" + rest, "$HOME" + rest, "${HOME}" + rest}
    return [f for f in found if f]


def pattern(denied, home):
    alternatives = sorted({re.escape(f) for path in denied for f in forms(path, home)}, key=len, reverse=True)
    return re.compile(rf"(?<!{EDGE})(?:{'|'.join(alternatives)})(?!{EDGE})")


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))


def main(argv=None):
    denied = sys.argv[1:] if argv is None else argv
    try:
        event = json.loads(sys.stdin.read())
        given = event.get("tool_input") or {}
    except (ValueError, AttributeError):
        deny(f"{REASON}: the guard could not read the call")
        return 0
    if denied:
        found = pattern(denied, os.path.expanduser("~"))
        for text in strings(given):
            match = found.search(text)
            if match:
                deny(f"{REASON}: `{match.group(0)}` lies outside the run's folder")
                return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
