"""Tests for hooks/tools.json: every tool it lists exists in a domain of this repository."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads((ROOT / "domains" / "review" / "hooks" / "tools.json").read_text(encoding="utf-8"))


class ToolsJson(unittest.TestCase):
    def test_only_known_kinds(self):
        self.assertLessEqual(set(CONFIG), {"skills", "agents", "hooks"})

    def test_every_skill_exists(self):
        for name in CONFIG.get("skills", []):
            with self.subTest(skill=name):
                self.assertTrue(list(ROOT.glob(f"domains/*/skills/{name}/SKILL.md")))

    def test_every_agent_exists(self):
        for name in CONFIG.get("agents", []):
            with self.subTest(agent=name):
                self.assertTrue(list(ROOT.glob(f"domains/*/agents/{name}.md")))

    def test_every_hook_exists(self):
        for name in CONFIG.get("hooks", []):
            with self.subTest(hook=name):
                domain, file = name.split("/", 1)
                self.assertTrue((ROOT / "domains" / domain / "hooks" / file).is_file())

    def test_tool_review_is_never_reviewed(self):
        self.assertNotIn("tool-review", CONFIG.get("skills", []))


if __name__ == "__main__":
    unittest.main()
