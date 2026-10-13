"""Tests for the Stop hook review.py, run the way Claude Code runs it: event JSON on stdin."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import reviewfile  # noqa: E402
from review_world import MODEL, REPLY, World  # noqa: E402


class StopHook(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def stop(self, **options):
        result = self.world.run_hook(**options)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        return json.loads(result.stdout) if result.stdout.strip() else None

    def reviews(self):
        return [reviewfile.parse(path.read_text(encoding="utf-8"))[0] for path in self.world.reviews()]

    def test_silent_without_a_tool_of_ours(self):
        self.world.load_skill("superpowers:brainstorming",
                              base=self.world.claude / "plugins" / "x" / "skills" / "brainstorming")
        self.assertIsNone(self.stop())
        self.assertEqual(self.world.reviews(), [])

    def test_requests_a_review_for_our_skill(self):
        self.world.load_skill("roadmap")
        answer = self.stop()
        self.assertEqual(answer["decision"], "block")
        self.assertTrue(answer["reason"].startswith(
            "This session used tools of my-agent-setup: skill:roadmap (roadmap 1.1.1). Load the tool-review skill"))
        self.assertIn("without mentioning it to the user", answer["reason"])
        self.assertIn("end the turn where the conversation stood", answer["reason"])
        [meta] = self.reviews()
        self.assertEqual((meta["status"], meta["trigger"], meta["session"], meta["project"]),
                         ("requested", "hook", self.world.session, str(self.world.project)))
        self.assertEqual(meta["tools"], [{"id": "skill:roadmap", "domain": "roadmap", "version": "1.1.1"}])

    def test_asks_only_for_the_tools_the_review_table_lists(self):
        world = World(self.enterContext(tempfile.TemporaryDirectory()), reviewed=["roadmap", "agent:skill-auditor"])
        world.load_skill("authoring-skills")
        world.hook("skill-tooling/audit_skill.py", kind="hook_blocking_error", event="PostToolUse")
        world.load_skill("roadmap")
        world.call_agent("skill-auditor")
        answer = json.loads(world.run_hook().stdout)
        self.assertTrue(answer["reason"].startswith("This session used tools of my-agent-setup: skill:roadmap "
                                                    "(roadmap 1.1.1), agent:skill-auditor (skill-tooling 0.1.2). "))
        [path] = world.reviews()
        meta, _ = reviewfile.parse(path.read_text(encoding="utf-8"))
        self.assertEqual([tool["id"] for tool in meta["tools"]], ["skill:roadmap", "agent:skill-auditor"])

    def test_no_request_without_the_review_table_nor_with_an_empty_one(self):
        for reviewed in (None, []):
            with self.subTest(reviewed=reviewed):
                world = World(self.enterContext(tempfile.TemporaryDirectory()), reviewed=reviewed)
                world.load_skill("roadmap")
                self.assertEqual((world.run_hook().stdout, world.reviews()), ("", []))

    def test_the_table_is_the_repository_s_read_at_each_stop_never_the_project_s(self):
        world = World(self.enterContext(tempfile.TemporaryDirectory()), reviewed=None)
        (world.project / ".agent-conventions.toml").write_text('[review]\ntools = ["roadmap"]\n', encoding="utf-8")
        world.load_skill("roadmap")
        self.assertEqual(world.run_hook().stdout, "")
        world.review_table('[review]\ntools = ["skill:roadmap"]\n')
        self.assertEqual(json.loads(world.run_hook().stdout)["decision"], "block")

    def test_a_review_requested_is_measured_whole_once_its_tool_leaves_the_table(self):
        self.world.load_skill("roadmap")
        self.stop()
        self.world.review_table("[review]\ntools = []\n")
        self.stop(stop_hook_active=True)
        [meta] = self.reviews()
        self.assertEqual((meta["status"], meta["measured"]["setup"]["skill:roadmap"]["loads"]), ("skipped", 1))

    def past_reviews(self, tool_id, version, folder=None, count=10):
        """`count` complete reviews of tool_id at version in other sessions, none raising a finding."""
        for number in range(1, count + 1):
            session = f"{number:08d}-0000-0000-0000-000000000000"
            stamp = f"2026-10-01T{number:02d}:00:00.000Z"
            meta = {"review": 1, "status": "complete", "date": "2026-10-01", "session": session, "project": "/p",
                    "trigger": "hook", "slice": {"from": stamp, "to": stamp}, "closed": stamp,
                    "tools": [{"id": tool_id, "domain": "roadmap", "version": version}], "findings": []}
            reviewfile.write_text((folder or self.world.repo / "reviews") / f"2026-10-01-{session[:8]}-x.md",
                                  reviewfile.render(meta, "Prose.\n"))

    def test_a_saturated_tool_version_is_left_out_of_the_request(self):
        self.past_reviews("skill:roadmap", "1.1.1")
        self.world.hook("roadmap/session_resume.py")
        self.world.load_skill("roadmap")
        self.assertIn("used tools of my-agent-setup: hook:roadmap/session_resume.py (roadmap 1.1.1). ",
                      self.stop()["reason"])
        [meta] = [meta for meta in self.reviews() if meta["session"] == self.world.session]
        self.assertEqual([tool["id"] for tool in meta["tools"]], ["hook:roadmap/session_resume.py"])

    def test_no_request_when_every_tool_used_is_saturated(self):
        self.past_reviews("skill:roadmap", "1.1.1")
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop())
        self.assertEqual(len(self.world.reviews()), 10)

    def test_a_tool_is_asked_for_again_at_its_next_version_or_after_an_archive(self):
        for name, version, folder in (("next version", "1.1.0", None),
                                      ("archive", "1.1.1", ("archive", "2026-10-13")),
                                      ("nine reviews", "1.1.1", None)):
            with self.subTest(name):
                self.world = World(self.enterContext(tempfile.TemporaryDirectory()))
                self.past_reviews("skill:roadmap", version, count=9 if name == "nine reviews" else 10,
                                  folder=self.world.repo.joinpath("reviews", *folder) if folder else None)
                self.world.load_skill("roadmap")
                self.assertEqual(self.stop()["decision"], "block")

    def test_one_request_covers_every_tool_of_the_turn(self):
        self.world.hook("roadmap/session_resume.py")
        self.world.load_skill("roadmap")
        self.stop()
        [meta] = self.reviews()
        self.assertEqual([tool["id"] for tool in meta["tools"]], ["hook:roadmap/session_resume.py", "skill:roadmap"])

    def test_an_unanswered_request_is_skipped_at_the_next_stop(self):
        self.world.load_skill("roadmap")
        self.stop()
        [path] = self.world.reviews()
        reviewfile.draft_of(path).write_text("{}", encoding="utf-8")
        self.assertIsNone(self.stop(stop_hook_active=True))
        [meta] = self.reviews()
        self.assertEqual(meta["status"], "skipped")
        self.assertEqual(meta["measured"]["setup"]["skill:roadmap"]["loads"], 1)
        self.assertIn("closed", meta)
        self.assertFalse(reviewfile.draft_of(path).exists())

    def test_a_completed_review_is_closed_at_the_next_stop(self):
        self.world.load_skill("roadmap")
        self.stop()
        [path] = self.world.reviews()
        meta, _ = reviewfile.parse(path.read_text(encoding="utf-8"))
        meta["status"] = "complete"
        reviewfile.write_text(path, reviewfile.render(meta, "Prose.\n"))
        self.stop(stop_hook_active=True)
        meta, body = reviewfile.parse(path.read_text(encoding="utf-8"))
        self.assertEqual((meta["status"], body), ("complete", "Prose.\n"))
        self.assertIn("closed", meta)

    def test_a_complete_review_gets_its_own_turn_up_to_the_call_after_record_py(self):
        self.world.load_skill("roadmap")
        self.stop()
        path = self.world.request_at_clock()
        self.world.load_skill("tool-review")
        scripts = self.world.claude / "skills" / "tool-review" / "scripts"
        self.world.result(self.world.tool_use("Bash", command=f"{scripts}/measure.py"), "review: x")
        self.world.result(self.world.tool_use("Bash", command=f"{scripts}/record.py {reviewfile.draft_of(path)}"),
                          "review written")
        meta, _ = reviewfile.parse(path.read_text(encoding="utf-8"))
        meta.update(status="complete", measured={"setup": {}})
        reviewfile.write_text(path, reviewfile.render(meta, "Prose.\n"))
        self.world.reply()
        self.world.reply(effort="max")
        self.stop(stop_hook_active=True)
        meta, body = reviewfile.parse(path.read_text(encoding="utf-8"))
        # Skill, measure.py, record.py, and the call after it: the conversation's next call is not the review's
        self.assertEqual(meta["measured"]["review"], {
            "calls": 4, "dollars": round(4 * REPLY, 4), "estimated": 0.0,
            "models": {MODEL: {"xhigh": {"calls": 4, "dollars": round(4 * REPLY, 4)}}}})
        self.assertEqual(body, "Prose.\n")

    def test_a_skipped_review_has_no_turn_of_its_own(self):
        self.world.load_skill("roadmap")
        self.stop()
        self.world.reply()
        self.stop(stop_hook_active=True)
        [meta] = self.reviews()
        self.assertEqual(meta["status"], "skipped")
        self.assertNotIn("review", meta["measured"])

    def test_one_review_per_tool_and_session(self):
        self.world.load_skill("roadmap")
        self.stop()
        self.stop(stop_hook_active=True)
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop())
        self.assertEqual(len(self.world.reviews()), 1)

    def test_a_new_tool_later_gets_its_own_review_from_where_the_last_closed(self):
        self.world.load_skill("roadmap")
        self.stop()
        self.stop(stop_hook_active=True)
        self.world.call_agent("roadmap-auditor")
        answer = self.stop()
        self.assertIn("agent:roadmap-auditor", answer["reason"])
        by_tool = {meta["tools"][0]["id"]: meta for meta in self.reviews()}
        first, second = by_tool["skill:roadmap"], by_tool["agent:roadmap-auditor"]
        self.assertEqual(second["slice"]["from"], first["closed"])
        self.assertEqual([tool["id"] for tool in second["tools"]], ["agent:roadmap-auditor"])

    def test_no_new_request_while_a_stop_hook_drives_the_conversation(self):
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop(stop_hook_active=True))
        self.assertEqual(self.world.reviews(), [])

    def test_no_request_in_an_unattended_session(self):
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop(attended="0"))
        self.assertEqual(self.world.reviews(), [])

    def test_silent_when_the_review_domain_knows_no_repository(self):
        path = self.world.claude / "my-agent-setup.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        del state["domains"]["review"]["repo"]
        path.write_text(json.dumps(state), encoding="utf-8")
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop())

    def test_an_error_is_logged_and_the_session_goes_on(self):
        path = self.world.claude / "my-agent-setup.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["domains"]["roadmap"] = "broken"
        path.write_text(json.dumps(state), encoding="utf-8")
        self.world.load_skill("roadmap")
        self.assertIsNone(self.stop())
        log = (self.world.repo / "reviews" / "errors.log").read_text(encoding="utf-8")
        self.assertIn(self.world.session, log)
        self.assertIn("AttributeError", log)

    def test_invalid_event_json_is_ignored(self):
        result = self.world.run_hook(raw="{")
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_a_broken_review_of_the_session_does_not_stop_the_hook(self):
        reviews = self.world.repo / "reviews"
        reviews.mkdir(parents=True)
        name = f"2026-09-26-{self.world.session[:8]}"
        (reviews / f"{name}-bytes.md").write_bytes(b"---\nreview: 1\n\xff\xfe\n---\n")
        (reviews / f"{name}-shape.md").write_text(f"---\nsession: {self.world.session}\nslice: foo\n---\n",
                                                  encoding="utf-8")
        self.world.load_skill("roadmap")
        self.assertEqual(self.stop()["decision"], "block")
        self.assertFalse((reviews / "errors.log").exists())


if __name__ == "__main__":
    unittest.main()
