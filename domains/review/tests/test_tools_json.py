"""Tests for hooks/tools.json: the points to watch, each on a tool that exists in a domain of this repository."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads((ROOT / "domains" / "review" / "hooks" / "tools.json").read_text(encoding="utf-8"))
FILES = {"skill": "domains/*/skills/{}/SKILL.md", "agent": "domains/*/agents/{}.md"}


def missing_tools(config, root=ROOT):
    """The tool ids under `watch` that name no skill, agent or hook of a domain under root."""
    missing = []
    for tool_id in config.get("watch", {}):
        kind, _, name = tool_id.partition(":")
        if kind == "hook":
            domain, _, file = name.partition("/")
            found = bool(domain and file) and (root / "domains" / domain / "hooks" / file).is_file()
        else:
            found = kind in FILES and bool(name) and bool(list(root.glob(FILES[kind].format(name))))
        if not found:
            missing.append(tool_id)
    return missing


class ToolsJson(unittest.TestCase):
    def test_only_the_points_to_watch(self):
        self.assertEqual(set(CONFIG), {"watch"})

    def test_every_watched_tool_exists(self):
        self.assertEqual(missing_tools(CONFIG), [])

    def test_a_point_on_a_tool_that_does_not_exist_is_refused(self):
        config = {"watch": {"skill:roadmap": ["x"], "skill:other": ["y"], "agent:roadmap": ["z"],
                            "hook:roadmap/session_resume.py": ["w"], "hook:roadmap/none.py": ["v"], "roadmap": ["u"]}}
        self.assertEqual(missing_tools(config), ["skill:other", "agent:roadmap", "hook:roadmap/none.py", "roadmap"])

    def test_every_point_is_a_sentence(self):
        for tool_id, points in CONFIG.get("watch", {}).items():
            with self.subTest(tool=tool_id):
                self.assertTrue(points)
                self.assertTrue(all(isinstance(point, str) and point.strip() for point in points))

    def test_tool_review_is_never_watched(self):
        self.assertNotIn("skill:tool-review", CONFIG.get("watch", {}))


if __name__ == "__main__":
    unittest.main()
