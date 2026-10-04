#!/usr/bin/env python3
"""Claude Code PostToolUse hook: run the domain checks and unit tests when this repository changes.

Registered in .claude/settings.json after Edit, Write, MultiEdit and Bash. Bash is
included because files are often changed through scripts rather than through the
editing tools. The hook runs tests/check.py --skip-skills --brief: the skills themselves
are audited at each edit by the skill-tooling domain's audit hook. It stays silent when
nothing under domains/, shared/, tests/ or tools/ changed, after a Bash command that ran
the checks itself, and when every check passes. Otherwise it exits 2 with one line per
problem on stderr, which Claude Code shows to the agent so it can fix them at once.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCHED = ("domains", "shared", "tests", "tools")
RAN_CHECKS_RE = re.compile(r"\bmake\b[^|;&\n]*\bcheck\b|tests/check\.py")
MAX_LINES = 20


def touched(event):
    tool = event.get("tool_name", "")
    if tool in ("Edit", "Write", "MultiEdit"):
        try:
            relative = Path(event.get("tool_input", {}).get("file_path", "")).resolve().relative_to(ROOT)
        except ValueError:
            return False
        return bool(relative.parts) and relative.parts[0] in WATCHED
    if tool == "Bash":
        if RAN_CHECKS_RE.search(event.get("tool_input", {}).get("command", "")):
            return False
        status = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *WATCHED],
                                capture_output=True, text=True)
        return bool(status.stdout.strip())
    return False


def command():
    return [sys.executable, str(ROOT / "tests" / "check.py"), "--skip-skills", "--brief"]


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if not touched(event):
        return 0
    result = subprocess.run(command(), capture_output=True, text=True, cwd=ROOT)
    if result.returncode == 0:
        return 0
    lines = (result.stdout + result.stderr).strip().splitlines()
    shown = lines[:MAX_LINES] + ([f"... {len(lines) - MAX_LINES} more lines: run make check"]
                                 if len(lines) > MAX_LINES else [])
    sys.stderr.write("Checks failed after this change:\n" + "\n".join(shown) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
