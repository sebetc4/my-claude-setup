"""Tests for transcript.py: which tools of this setup a transcript shows, and what a slice cost."""

import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import transcript  # noqa: E402
from review_world import World  # noqa: E402


def used(world, **window):
    state = transcript.load_state(world.claude)
    catalog = transcript.load_catalog(world.claude, state)
    return list(transcript.uses(world.transcript, catalog, world.claude, str(world.project), **window))


class Detection(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def other_world(self, **options):
        return World(self.enterContext(tempfile.TemporaryDirectory()), **options)

    def test_our_skill_loaded_by_the_skill_tool(self):
        self.world.load_skill("roadmap")
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_our_skill_typed_as_a_command(self):
        self.world.load_skill("roadmap", typed=True)
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_a_project_skill_of_the_same_name_is_not_ours(self):
        self.world.load_skill("roadmap", base=self.world.project / ".claude" / "skills" / "roadmap")
        self.assertEqual(used(self.world), [])

    def test_a_plugin_skill_is_not_ours(self):
        self.world.load_skill("superpowers:brainstorming",
                              base=self.world.claude / "plugins" / "cache" / "superpowers" / "skills" / "brainstorming")
        self.assertEqual(used(self.world), [])

    def test_quoting_the_base_directory_line_is_not_a_load(self):
        line = f"Base directory for this skill: {self.world.claude / 'skills' / 'roadmap'}"
        self.world.reply({"type": "text", "text": line})
        call = self.world.tool_use("Bash", command="grep Base")
        self.world.result(call, line)
        self.assertEqual(used(self.world), [])

    def test_our_agent(self):
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world), ["agent:roadmap-auditor"])

    def test_an_agent_shadowed_by_a_project_agent_is_not_ours(self):
        agents = self.world.project / ".claude" / "agents"
        agents.mkdir(parents=True)
        (agents / "roadmap-auditor.md").write_text("mine\n", encoding="utf-8")
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world), [])

    def test_our_hooks_with_an_effect_in_order_of_first_use(self):
        self.world.hook("roadmap/session_resume.py")
        self.world.hook("roadmap/progress_guard.py", kind="hook_blocking_error", event="PostToolUse")
        self.assertEqual(used(self.world), ["hook:roadmap/session_resume.py", "hook:roadmap/progress_guard.py"])

    def test_a_hook_that_produced_nothing_did_nothing(self):
        self.world.hook("roadmap/session_resume.py", context="")
        self.assertEqual(used(self.world), [])

    def test_a_tool_missing_from_tools_json_is_ignored(self):
        world = self.other_world(tools={"skills": [], "agents": [], "hooks": []})
        world.load_skill("roadmap")
        self.assertEqual(used(world), [])

    def test_a_tool_this_repository_did_not_install_is_ignored(self):
        world = self.other_world(installed=False)
        world.load_skill("roadmap")
        self.assertEqual(used(world), [])

    def test_tool_review_is_never_a_tool_under_review(self):
        world = self.other_world(tools={"skills": ["tool-review"]})
        world.load_skill("tool-review")
        self.assertEqual(used(world), [])

    def test_uses_within_a_window(self):
        self.world.load_skill("roadmap")
        middle = self.world.clock + timedelta(seconds=30)
        self.world.clock = middle + timedelta(seconds=30)
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world, start=middle), ["agent:roadmap-auditor"])
        self.assertEqual(used(self.world, end=middle), ["skill:roadmap"])

    def test_a_half_written_last_line_is_skipped(self):
        self.world.load_skill("roadmap")
        with self.world.transcript.open("a", encoding="utf-8") as handle:
            handle.write('{"type": "user", "isMeta": tr')
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_session_start_is_the_first_record(self):
        first = self.world.prompt("hello")
        self.world.load_skill("roadmap")
        self.assertEqual(transcript.session_start(self.world.transcript), transcript.when(first["timestamp"]))

    def test_review_load_is_the_latest_load_of_tool_review(self):
        self.world.load_skill("tool-review")
        second = self.world.load_skill("tool-review")
        self.assertEqual(transcript.review_load(self.world.transcript, self.world.claude),
                         (transcript.when(second["timestamp"]), str(self.world.project)))

    def test_stamp_writes_what_when_reads(self):
        self.assertEqual(transcript.stamp(transcript.when("2026-09-26T21:42:11.395Z")), "2026-09-26T21:42:11.395Z")

    def test_the_repository_of_the_review_domain(self):
        self.assertEqual(transcript.repo_of(transcript.load_state(self.world.claude)), self.world.repo)
        self.assertIsNone(transcript.repo_of({"domains": {}}))


if __name__ == "__main__":
    unittest.main()
