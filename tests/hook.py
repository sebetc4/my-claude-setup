#!/usr/bin/env python3
"""Claude Code PostToolUse hook: run tests/check.py when a skill or a check changes.

Registered in .claude/settings.json after Edit, Write, MultiEdit and Bash. Bash is
included because files are often changed through scripts rather than through the
editing tools. The hook stays silent when nothing under skills/ or tests/ changed,
or when every check passes. Otherwise it exits 2 with the problems on stderr, which
Claude Code shows to the agent so it can fix them at once.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCHED = ("skills", "tests")


def touched(event):
    tool = event.get("tool_name", "")
    if tool in ("Edit", "Write", "MultiEdit"):
        try:
            relative = Path(event.get("tool_input", {}).get("file_path", "")).resolve().relative_to(ROOT)
        except ValueError:
            return False
        return bool(relative.parts) and relative.parts[0] in WATCHED
    if tool == "Bash":
        status = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *WATCHED],
                                capture_output=True, text=True)
        return bool(status.stdout.strip())
    return False


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if not touched(event):
        return 0
    result = subprocess.run([sys.executable, str(ROOT / "tests" / "check.py")],
                            capture_output=True, text=True, cwd=ROOT)
    if result.returncode == 0:
        return 0
    sys.stderr.write("Skill checks failed after this change:\n" + result.stdout + result.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
