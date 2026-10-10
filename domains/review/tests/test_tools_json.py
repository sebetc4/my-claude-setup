"""Tests for hooks/tools.json: every tool it lists exists in a domain of this repository."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads((ROOT / "domains" / "review" / "hooks" / "tools.json").read_text(encoding="utf-8"))
LISTS = {"skill": "skills", "agent": "agents", "hook": "hooks"}


def unlisted_watches(config):
    """The tool ids under `watch` that the config's lists do not name."""
    return [tool_id for tool_id in config.get("watch", {})
            if tool_id.split(":", 1)[-1] not in config.get(LISTS.get(tool_id.split(":", 1)[0], ""), [])]


class ToolsJson(unittest.TestCase):
    def test_only_known_kinds(self):
        self.assertLessEqual(set(CONFIG), {"skills", "agents", "hooks", "watch"})

    def test_every_watched_tool_is_listed(self):
        self.assertEqual(unlisted_watches(CONFIG), [])

    def test_a_point_on_a_tool_not_listed_is_refused(self):
        config = {"skills": ["roadmap"], "watch": {"skill:roadmap": ["x"], "skill:other": ["y"], "agent:roadmap": ["z"]}}
        self.assertEqual(unlisted_watches(config), ["skill:other", "agent:roadmap"])

    def test_every_point_is_a_sentence(self):
        for tool_id, points in CONFIG.get("watch", {}).items():
            with self.subTest(tool=tool_id):
                self.assertTrue(points)
                self.assertTrue(all(isinstance(point, str) and point.strip() for point in points))

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
