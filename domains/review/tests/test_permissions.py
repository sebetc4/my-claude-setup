"""Tests for permissions.json: the review domain grants no more than its procedure needs."""

import json
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
RULES = json.loads((DOMAIN / "permissions.json").read_text(encoding="utf-8"))["allow"]
SKILL = DOMAIN / "skills" / "tool-review"


class Permissions(unittest.TestCase):
    def test_sessions_may_write_drafts_only(self):
        self.assertEqual([rule for rule in RULES if rule.startswith("Edit(")], ["Edit(/{{REPO_DIR}}/reviews/*.draft)"])

    def test_only_the_two_scripts_run_without_a_prompt(self):
        self.assertEqual([rule for rule in RULES if rule.startswith("Bash(")], [
            "Bash({{CLAUDE_DIR}}/skills/tool-review/scripts/measure.py:*)",
            "Bash({{CLAUDE_DIR}}/skills/tool-review/scripts/record.py:*)",
        ])


    def test_the_two_scripts_run_as_commands(self):
        # A project hook may refuse `python3` in command position (scriptorium's does),
        # and the rules name the script path: the scripts run without an interpreter.
        for name in ("measure.py", "record.py"):
            with self.subTest(script=name):
                script = SKILL / "scripts" / name
                self.assertTrue(script.stat().st_mode & 0o111, f"{name} is not executable")
                self.assertEqual(script.read_text(encoding="utf-8").splitlines()[0], "#!/usr/bin/env python3")

    def test_the_skill_runs_the_scripts_as_commands(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Run `<base>/scripts/measure.py`", text)
        self.assertIn("Run `<base>/scripts/record.py <draft>`", text)
        self.assertNotIn("python3 -B <base>", text)

if __name__ == "__main__":
    unittest.main()
