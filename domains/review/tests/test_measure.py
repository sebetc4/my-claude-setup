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
from review_world import RUN_MODEL, SCRIPTS, World, run_call, text_dollars, usage  # noqa: E402


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
        self.assertTrue([line for line in lines if line.startswith("  skill:roadmap (roadmap 1.1.1): $")], lines)
        self.assertIn("- did the conversation need the 3912 characters hook:roadmap/session_resume.py injected?", lines)
        self.assertIn("measured:", lines)
        self.assertLessEqual(len(lines), 50)

    def test_a_requested_review_is_measured_whole_once_its_tool_leaves_the_table(self):
        self.world.load_skill("roadmap")
        self.world.run_hook()
        self.world.review_table("[review]\ntools = []\n")
        self.world.load_skill("tool-review")
        result = self.world.run_script("measure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue([line for line in result.stdout.splitlines() if line.startswith("  skill:roadmap (roadmap 1.1.1): $")],
                        result.stdout)
        self.assertIn("    skill:roadmap: {loads: 1, chars: 99, files_read: {}, scripts: {}, script_errors: 0}",
                      result.stdout.splitlines())

    def test_the_points_to_watch_of_the_tools_that_served(self):
        watch = {"skill:roadmap": ["the report read in full", "a task ticked without its proof"],
                 "agent:roadmap-auditor": ["a closure audited twice"]}
        world = World(self.enterContext(tempfile.TemporaryDirectory()), watch=watch)
        world.load_skill("roadmap")
        world.load_skill("tool-review")
        lines = world.run_script("measure.py").stdout.splitlines()
        self.assertIn("- point to watch for skill:roadmap: the report read in full; a finding when the slice shows it", lines)
        self.assertIn("- point to watch for skill:roadmap: a task ticked without its proof; a finding when the slice shows it",
                      lines)
        self.assertFalse([line for line in lines if "a closure audited twice" in line])

    def test_no_point_to_watch_for_a_tool_without_one(self):
        self.world.load_skill("roadmap")
        self.world.load_skill("tool-review")
        lines = self.world.run_script("measure.py").stdout.splitlines()
        self.assertFalse([line for line in lines if "point to watch" in line])

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

    def earlier(self, number, tool_id, version, dollars, status="complete"):
        """An earlier review of the tool, in another session, whose block gives the tool's cost."""
        session = f"{number:08d}-0000-0000-0000-000000000000"
        meta = {"review": 1, "status": status, "date": "2026-10-01", "session": session, "project": "/p",
                "trigger": "hook", "slice": {"from": "2026-10-01T10:00:00.000Z", "to": "2026-10-01T11:00:00.000Z"},
                "tools": [{"id": tool_id, "domain": "roadmap", "version": version}],
                "measured": {"setup": {}, "derived": {"tool_cost": {"value": {tool_id: {"tokens": 1, "dollars": dollars}},
                                                                    "rule": "the rule"}}}}
        reviewfile.write_text(self.world.repo / "reviews" / f"2026-10-01-{session[:8]}-x.md",
                              reviewfile.render(meta, "Prose.\n"))

    def test_prints_each_tool_s_cost_beside_its_median_and_owes_an_explanation_past_one_and_a_half(self):
        self.world.hook("roadmap/session_resume.py", context="x" * 2600)
        self.world.prompt("close the phase")
        load = self.world.load_skill("roadmap")
        self.world.call_agent("roadmap-auditor", effort="medium", output=600)
        self.world.call_agent("general-purpose", effort="max", output=700)
        self.world.reply()
        self.world.run_hook()
        self.world.request_at_clock()
        # four calls in the slice: Skill, Agent, Agent and the reply; the skill's load is held by the last three
        hook = round(text_dollars(2600, 4)[1], 4)
        skill = round(text_dollars(len(load["message"]["content"][0]["text"]), 3)[1], 4)
        agent = round(run_call(usage.estimate("output", "roadmap-auditor", "medium").value) + run_call(600), 4)
        medians = [round(hook / 2, 4), round(hook / 3, 4), round(hook / 1.8, 4)]
        for number, dollars in enumerate(medians, 1):
            self.earlier(number, "hook:roadmap/session_resume.py", "1.1.1", dollars)
        self.earlier(4, "hook:roadmap/session_resume.py", "1.0.0", 9.0)
        self.earlier(5, "hook:roadmap/session_resume.py", "1.1.1", 9.0, status="skipped")
        self.earlier(6, "skill:roadmap", "1.1.1", skill)
        self.world.load_skill("tool-review")
        result = self.world.run_script("measure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        median = round(hook / 2, 4)
        ratio = hook / median
        for line in (
                f"  hook:roadmap/session_resume.py (roadmap 1.1.1): ${hook:.4f}, {ratio:.2f} times its median "
                f"${median:.4f} over 3 reviews of 1.1.1",
                f"  skill:roadmap (roadmap 1.1.1): ${skill:.4f}; no median, 1 earlier review of 1.1.1",
                f"  agent:roadmap-auditor (roadmap 1.1.1): ${agent:.4f}; no median, 0 earlier reviews of 1.1.1",
                f"- why hook:roadmap/session_resume.py cost {ratio:.2f} times its median: ${hook:.4f} against "
                f"${median:.4f}",
                "  cost:", "  derived:"):
            self.assertIn(line, lines)
        self.assertFalse([line for line in lines if line.startswith("- why skill:roadmap")])
        subagents = [line for line in lines if line.startswith("    subagents: ")]
        self.assertTrue(subagents and f"{RUN_MODEL}: {{medium: " in subagents[0] and "max: " in subagents[0], lines)
        self.assertLessEqual(len(lines), 50)

    def test_layout_cuts_the_measured_block_first(self):
        lines = load_measure().layout(["h"] * 5, ["d"] * 5, [f"m{n}" for n in range(60)])
        self.assertEqual(len(lines), 50)
        self.assertEqual(lines[:10], ["h"] * 5 + ["d"] * 5)
        self.assertEqual(lines[-1], "# … 21 more line(s) of the measured block")


if __name__ == "__main__":
    unittest.main()
