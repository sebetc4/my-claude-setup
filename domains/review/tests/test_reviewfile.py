"""Tests for reviewfile.py: the review format, read back by this module and by PyYAML."""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import reviewfile  # noqa: E402

META = {
    "review": 1,
    "status": "complete",
    "date": "2026-09-26",
    "session": "aabb0fa1-f563-4ec2-8228-00c695fa7a0c",
    "project": "/code/claude/scriptorium",
    "trigger": "hook",
    "slice": {"from": "2026-09-26T21:42:11.000Z", "to": "2026-09-26T21:46:03.395Z"},
    "closed": "2026-09-26T21:48:10.120Z",
    "tools": [{"id": "hook:roadmap/session_resume.py", "domain": "roadmap", "version": "1.1.1",
               "brought": "Nothing: the conversation was about a PDF; the injected phase was never used."}],
    "task": "can we pick up the guide's layout again?",
    "outcome": "delivered",
    "corrections": 0,
    "measured": {
        "tokens": {"fresh": 33979, "cache_read": 412727, "output": 5445},
        "turns": 9,
        "tools": {"Bash": 6, "Read": 2},
        "friction": {"tool_errors": 0, "interruptions": 0},
        "setup": {
            "hook:roadmap/session_resume.py": {"runs": 1, "injected_chars": 3912, "blocks": 0, "errors": 0},
            "agent:roadmap-auditor": {"runs": [{"fresh": 23075, "cache_read": 74289, "seconds": 44},
                                               {"fresh": 10, "cache_read": 20}]},
            "skill:roadmap": {"loads": 1, "chars": 18230, "files_read": {"references/close-phase.md": 1},
                              "scripts": {}, "script_errors": 0},
        },
        "derived": {
            "active_minutes": {"value": 4, "rule": "wall clock minus every gap over 5 min"},
            "context_peak": {"value": 57062, "rule": "largest input of one API call, fresh and cached"},
        },
    },
    "findings": [{"kind": "noise", "severity": "medium", "target": "domains/roadmap/hooks/session_resume.py",
                  "fix": "Inject one line (roadmap, open phase, file path) instead of the phase and its Work Log.",
                  "note": 'Quotes "like this", a colon: here, and a # sign.'}],
}
BODY = "The hook's 3,912 characters were the only cost of ours in this slice.\n"


def front_matter(text):
    return text.split("\n---\n", 1)[0][4:]


class Format(unittest.TestCase):
    def test_a_review_reads_back_as_written(self):
        self.assertEqual(reviewfile.parse(reviewfile.render(META, BODY)), (META, BODY))

    def test_pyyaml_reads_the_same_front_matter(self):
        self.assertEqual(yaml.safe_load(front_matter(reviewfile.render(META, BODY))), META)

    def test_the_layout_is_the_documented_one(self):
        text = reviewfile.render(META, BODY)
        for line in ("status: complete", 'date: "2026-09-26"', 'project: "/code/claude/scriptorium"',
                     "  - id: hook:roadmap/session_resume.py", '    version: "1.1.1"',
                     "  tokens: {fresh: 33979, cache_read: 412727, output: 5445}",
                     "        - {fresh: 23075, cache_read: 74289, seconds: 44}", "    fix: >-"):
            self.assertIn(line + "\n", text)

    def test_keys_follow_the_format_order(self):
        text = reviewfile.render({"findings": [], "status": "requested", "review": 1})
        self.assertEqual(text, "---\nreview: 1\nstatus: requested\nfindings: []\n---\n")

    def test_setup_stays_in_block_style_whatever_its_tools(self):
        text = reviewfile.render({"measured": {"setup": {"hook:a/b.py": {"runs": 1}}}})
        self.assertIn("  setup:\n    hook:a/b.py: {runs: 1}\n", text)

    def test_awkward_strings_read_back_everywhere(self):
        for value in ("true", "", "2026-09-26", "a: b", "x\ny", "#tag", "1.1", "- dash", "é" * 70, "two  spaces " * 8):
            with self.subTest(value=value):
                text = reviewfile.render({"task": value})
                self.assertEqual(reviewfile.parse(text)[0], {"task": value})
                self.assertEqual(yaml.safe_load(front_matter(text)), {"task": value})

    def test_a_long_text_is_folded_within_the_width(self):
        text = reviewfile.render({"task": "word " * 40 + "end"})
        self.assertIn("task: >-\n", text)
        self.assertTrue(all(len(line) <= reviewfile.WIDTH for line in text.splitlines()))

    def test_a_text_without_front_matter_is_refused(self):
        with self.assertRaises(reviewfile.FormatError):
            reviewfile.parse("just prose\n")

    def test_a_bad_indentation_is_refused(self):
        with self.assertRaises(reviewfile.FormatError):
            reviewfile.parse("---\nstatus: complete\n   task: x\n---\n")


class Files(unittest.TestCase):
    def setUp(self):
        self.reviews = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve() / "reviews"
        self.session = META["session"]

    def add(self, name, **meta):
        path = self.reviews / name
        reviewfile.write_text(path, reviewfile.render({"review": 1, "session": self.session, **meta}))
        return path

    def test_session_reviews_are_the_session_s_own_in_slice_order(self):
        prefix = f"2026-09-26-{self.session[:8]}"
        late = self.add(f"{prefix}-b.md", slice={"from": "x", "to": "2026-09-26T22:00:00.000Z"})
        early = self.add(f"{prefix}-a.md", slice={"from": "x", "to": "2026-09-26T21:00:00.000Z"})
        self.add(f"{prefix}-c.md", session=self.session[:8] + "-0000-other")
        (self.reviews / f"{prefix}-d.md").write_text("not a review\n", encoding="utf-8")
        self.assertEqual([path for path, _ in reviewfile.session_reviews(self.reviews, self.session)], [early, late])

    def test_next_start_is_the_latest_close_or_slice_end(self):
        reviews = [(None, {"slice": {"to": "2026-09-26T21:00:00.000Z"}, "closed": "2026-09-26T21:05:00.000Z"}),
                   (None, {"slice": {"to": "2026-09-26T21:10:00.000Z"}})]
        self.assertEqual(reviewfile.next_start(reviews), "2026-09-26T21:10:00.000Z")
        self.assertIsNone(reviewfile.next_start([]))

    def test_a_taken_name_gets_a_number(self):
        first = reviewfile.new_path(self.reviews, "2026-09-26", self.session, "roadmap")
        self.add(first.name)
        second = reviewfile.new_path(self.reviews, "2026-09-26", self.session, "roadmap")
        reviewfile.draft_of(second).write_text("{}", encoding="utf-8")
        third = reviewfile.new_path(self.reviews, "2026-09-26", self.session, "roadmap")
        base = f"2026-09-26-{self.session[:8]}-roadmap"
        self.assertEqual([first.name, second.name, third.name], [f"{base}.md", f"{base}-2.md", f"{base}-3.md"])

    def test_slug(self):
        self.assertEqual(reviewfile.slug("skill:roadmap"), "roadmap")
        self.assertEqual(reviewfile.slug("agent:roadmap-auditor"), "roadmap-auditor")
        self.assertEqual(reviewfile.slug("hook:roadmap/session_resume.py"), "session-resume")

    def test_draft_of(self):
        self.assertEqual(reviewfile.draft_of(Path("reviews/x-2.md")), Path("reviews/x-2.draft"))


if __name__ == "__main__":
    unittest.main()
