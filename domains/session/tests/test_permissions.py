"""Tests for permissions.json: the session domain pre-approves only the conventions reader."""

import json
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
SCRIPT = DOMAIN / "skills" / "close-session" / "scripts" / "conventions.py"


class Permissions(unittest.TestCase):
    def test_only_the_conventions_reader_runs_without_a_prompt(self):
        rules = json.loads((DOMAIN / "permissions.json").read_text(encoding="utf-8"))["allow"]
        self.assertEqual(rules, ["Bash({{CLAUDE_DIR}}/skills/close-session/scripts/conventions.py:*)"])

    def test_the_reader_runs_as_a_command(self):
        # The rule names the script path, so the script runs without an interpreter in front.
        self.assertTrue(SCRIPT.stat().st_mode & 0o111, "conventions.py is not executable")
        self.assertEqual(SCRIPT.read_text(encoding="utf-8").splitlines()[0], "#!/usr/bin/env python3")


if __name__ == "__main__":
    unittest.main()
