"""Tests for record.py, run as the tool-review skill runs it."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import reviewfile  # noqa: E402
from review_world import World  # noqa: E402

FINDING = {"kind": "noise", "severity": "high", "target": "domains/roadmap/hooks/session_resume.py",
           "fix": "Inject one line instead of the phase and its Work Log.", "note": "Injected 3,912 characters."}
DRAFT = {"task": "can we close phase 3?", "outcome": "delivered", "corrections": 1,
         "tools": {"skill:roadmap": "The close-phase ritual and progress.py."}, "findings": [FINDING]}
PROSE = "The skill's load was the largest cost of ours; it bought the closure ritual."


class Record(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))
        self.world.load_skill("roadmap")
        self.world.run_hook()
        [self.review] = self.world.reviews()
        self.draft = reviewfile.draft_of(self.review)

    def write_draft(self, data=DRAFT, prose=PROSE):
        self.draft.write_text(json.dumps(data, indent=2) + "\n---\n" + prose + "\n", encoding="utf-8")

    def record(self, draft=None, cwd=None):
        return self.world.run_script("record.py", str(draft or self.draft), cwd=cwd)

    def test_a_valid_draft_becomes_a_complete_review(self):
        self.write_draft()
        result = self.record()
        self.assertEqual(result.returncode, 0, result.stderr)
        meta, body = reviewfile.parse(self.review.read_text(encoding="utf-8"))
        self.assertEqual((meta["status"], meta["task"], meta["outcome"], meta["corrections"]),
                         ("complete", DRAFT["task"], "delivered", 1))
        self.assertEqual(meta["tools"], [{"id": "skill:roadmap", "domain": "roadmap", "version": "1.1.1",
                                          "brought": DRAFT["tools"]["skill:roadmap"]}])
        self.assertEqual(meta["findings"], [FINDING])
        self.assertEqual(meta["measured"]["setup"]["skill:roadmap"]["loads"], 1)
        self.assertEqual(body, PROSE + "\n")
        self.assertFalse(self.draft.exists())
        self.assertIn(f"review written: {self.review}", result.stdout)
        self.assertIn(f"- high noise {FINDING['target']}: {FINDING['fix']}", result.stdout)

    def test_text_is_kept_on_one_line(self):
        self.write_draft({**DRAFT, "task": 'line one\n  "quoted": two'})
        self.assertEqual(self.record().returncode, 0)
        meta, _ = reviewfile.parse(self.review.read_text(encoding="utf-8"))
        self.assertEqual(meta["task"], 'line one "quoted": two')

    def test_a_relative_path_to_the_draft_works(self):
        self.write_draft()
        result = self.record(draft=os.path.relpath(self.draft, self.world.project), cwd=self.world.project)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_every_problem_is_reported_and_nothing_is_written(self):
        cases = {
            "missing key: outcome": {key: value for key, value in DRAFT.items() if key != "outcome"},
            "unknown key: mood": {**DRAFT, "mood": "fine"},
            "task must be a non-empty string": {**DRAFT, "task": " "},
            "outcome must be one of delivered, partial, abandoned": {**DRAFT, "outcome": "done"},
            "corrections must be an integer, 0 or more": {**DRAFT, "corrections": -1},
            "tools: skill:roadmap is under review and missing": {**DRAFT, "tools": {}},
            "tools: agent:x is not under review": {**DRAFT, "tools": {**DRAFT["tools"], "agent:x": "y"}},
            "finding 1: kind must be one of": {**DRAFT, "findings": [{**FINDING, "kind": "bug"}]},
            "finding 1: severity must be one of low, medium, high": {**DRAFT, "findings": [{**FINDING, "severity": "huge"}]},
            "finding 1: target nope.py is not a file of the repository": {**DRAFT, "findings": [{**FINDING, "target": "nope.py"}]},
            "finding 1: target must be a path relative to the repository, without ..":
                {**DRAFT, "findings": [{**FINDING, "target": "../x"}]},
            "finding 1: missing fix": {**DRAFT, "findings": [{key: value for key, value in FINDING.items() if key != "fix"}]},
        }
        before = self.review.read_text(encoding="utf-8")
        for expected, data in cases.items():
            with self.subTest(expected=expected):
                self.write_draft(data)
                result = self.record()
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)
                self.assertEqual(self.review.read_text(encoding="utf-8"), before)
                self.assertTrue(self.draft.exists())

    def test_the_prose_rules(self):
        for expected, prose in {"the prose after --- is empty": "",
                                "the prose is 301 words, 300 at most": "word " * 301}.items():
            with self.subTest(expected=expected):
                self.write_draft(prose=prose)
                result = self.record()
                self.assertEqual(result.returncode, 1)
                self.assertIn(expected, result.stderr)

    def test_a_draft_without_its_separator_or_its_json(self):
        self.draft.write_text(json.dumps(DRAFT), encoding="utf-8")
        self.assertIn("the draft has no line ---", self.record().stderr)
        self.draft.write_text("{oops\n---\nprose\n", encoding="utf-8")
        self.assertIn("the JSON object does not parse", self.record().stderr)

    def test_a_draft_of_no_requested_review_is_refused(self):
        other = self.world.repo / "reviews" / "other.draft"
        other.write_text("{}", encoding="utf-8")
        result = self.record(draft=other)
        self.assertEqual(result.returncode, 1)
        self.assertIn("run measure.py first", result.stderr)


if __name__ == "__main__":
    unittest.main()
