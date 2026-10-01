"""Tests for permissions.json: the roadmap domain pre-approves only the conventions reader."""

import json
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
RULES = json.loads((DOMAIN / "permissions.json").read_text(encoding="utf-8"))["allow"]
SCRIPT = DOMAIN / "skills" / "roadmap" / "scripts" / "conventions.py"


class Permissions(unittest.TestCase):
    def test_only_the_conventions_reader_runs_without_a_prompt(self):
        self.assertEqual(RULES, ["Bash({{CLAUDE_DIR}}/skills/roadmap/scripts/conventions.py:*)"])

    def test_the_reader_runs_as_a_command(self):
        # The rule names the script path, so the script runs without an interpreter in front.
        self.assertTrue(SCRIPT.stat().st_mode & 0o111, "conventions.py is not executable")
        self.assertEqual(SCRIPT.read_text(encoding="utf-8").splitlines()[0], "#!/usr/bin/env python3")

    def test_the_skill_runs_the_reader_by_its_path(self):
        text = (DOMAIN / "skills" / "roadmap" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`scripts/conventions.py roadmap`", text)
        self.assertNotIn("python3 scripts/conventions.py", text)


if __name__ == "__main__":
    unittest.main()
