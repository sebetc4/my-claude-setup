"""Tests for permissions.json: the review domain grants no more than its procedure needs."""

import json
import unittest
from pathlib import Path

RULES = json.loads((Path(__file__).resolve().parent.parent / "permissions.json").read_text(encoding="utf-8"))["allow"]


class Permissions(unittest.TestCase):
    def test_sessions_may_write_drafts_only(self):
        self.assertEqual([rule for rule in RULES if rule.startswith("Edit(")], ["Edit(/{{REPO_DIR}}/reviews/*.draft)"])

    def test_only_the_two_scripts_run_without_a_prompt(self):
        self.assertEqual([rule for rule in RULES if rule.startswith("Bash(")], [
            "Bash(python3 -B {{CLAUDE_DIR}}/skills/tool-review/scripts/measure.py:*)",
            "Bash(python3 -B {{CLAUDE_DIR}}/skills/tool-review/scripts/record.py:*)",
        ])


if __name__ == "__main__":
    unittest.main()
