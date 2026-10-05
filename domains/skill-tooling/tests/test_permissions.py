"""Tests for permissions.json: the skill-tooling domain pre-approves only the skill audit."""

import json
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
RULES = json.loads((DOMAIN / "permissions.json").read_text(encoding="utf-8"))["allow"]
SKILL = DOMAIN / "skills" / "authoring-skills"
SCRIPT = SKILL / "scripts" / "audit.py"


class Permissions(unittest.TestCase):
    def test_only_the_audit_runs_without_a_prompt(self):
        self.assertEqual(RULES, ["Bash({{CLAUDE_DIR}}/skills/authoring-skills/scripts/audit.py:*)"])

    def test_the_audit_runs_as_a_command(self):
        # The rule names the script path, so the script runs without an interpreter in front.
        self.assertTrue(SCRIPT.stat().st_mode & 0o111, "audit.py is not executable")
        self.assertEqual(SCRIPT.read_text(encoding="utf-8").splitlines()[0], "#!/usr/bin/env python3")

    def test_the_skill_runs_the_audit_by_its_path(self):
        texts = [path.read_text(encoding="utf-8") for path in SKILL.rglob("*.md")
                 if path.relative_to(SKILL).parts[0] != "evals"]
        self.assertTrue(any("`scripts/audit.py <skill-dir>`" in text for text in texts))
        self.assertFalse(any("python3 scripts/audit.py" in text for text in texts))


if __name__ == "__main__":
    unittest.main()
