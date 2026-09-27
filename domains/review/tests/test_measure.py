"""Tests for measure.py, run as the tool-review skill runs it."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import reviewfile  # noqa: E402
from review_world import SCRIPTS, World  # noqa: E402


def load_measure():
    spec = importlib.util.spec_from_file_location("measure_script", SCRIPTS / "measure.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Measure(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def test_prints_what_the_requested_review_needs(self):
        self.world.hook("roadmap/session_resume.py", context="x" * 3912)
        self.world.load_skill("roadmap")
        self.world.run_hook()
        self.world.load_skill("tool-review")
        result = self.world.run_script("measure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        [review] = self.world.reviews()
        lines = result.stdout.splitlines()
        self.assertEqual(lines[:2], [f"review: {review}", f"draft: {reviewfile.draft_of(review)}"])
        self.assertIn("  skill:roadmap (roadmap 1.1.1)", lines)
        self.assertIn("- did the conversation need the 3912 characters hook:roadmap/session_resume.py injected?", lines)
        self.assertIn("measured:", lines)
        self.assertLessEqual(len(lines), 50)

    def test_a_review_the_user_asked_for_is_created(self):
        self.world.load_skill("roadmap")
        load = self.world.load_skill("tool-review")
        self.world.reply()
        result = self.world.run_script("measure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        [review] = self.world.reviews()
        meta, _ = reviewfile.parse(review.read_text(encoding="utf-8"))
        self.assertEqual((meta["trigger"], meta["status"], meta["slice"]["to"]), ("manual", "requested", load["timestamp"]))
        self.assertEqual([tool["id"] for tool in meta["tools"]], ["skill:roadmap"])

    def test_a_manual_review_without_a_tool_of_ours(self):
        self.world.load_skill("tool-review")
        result = self.world.run_script("measure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("  none", result.stdout.splitlines())
        [review] = self.world.reviews()
        self.assertTrue(review.name.endswith("-manual.md"))

    def test_runs_as_a_command_without_an_interpreter(self):
        self.world.load_skill("tool-review")
        result = subprocess.run([str(SCRIPTS / "measure.py"), "--claude-dir", str(self.world.claude),
                                 "--session", self.world.session], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("review: "))

    def test_without_a_session(self):
        env = {key: value for key, value in os.environ.items() if key != "CLAUDE_CODE_SESSION_ID"}
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "measure.py"), "--claude-dir", str(self.world.claude)],
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no session", result.stderr)

    def test_layout_cuts_the_measured_block_first(self):
        lines = load_measure().layout(["h"] * 5, ["d"] * 5, [f"m{n}" for n in range(60)])
        self.assertEqual(len(lines), 50)
        self.assertEqual(lines[:10], ["h"] * 5 + ["d"] * 5)
        self.assertEqual(lines[-1], "# … 21 more line(s) of the measured block")


if __name__ == "__main__":
    unittest.main()
