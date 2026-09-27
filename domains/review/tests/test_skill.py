"""Tests for the tool-review SKILL.md: a review stays out of the conversation it interrupts."""

import unittest
from pathlib import Path

TEXT = (Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "SKILL.md").read_text(encoding="utf-8")


class Skill(unittest.TestCase):
    def test_the_last_step_resumes_the_conversation(self):
        self.assertIn("4. Say nothing about the review to the user", TEXT)
        self.assertIn("repeating, word for word, the question or next step", TEXT)
        self.assertNotIn("Tell the user in one line where the review is", TEXT)

    def test_no_message_while_the_review_runs(self):
        self.assertIn("no message to the user while the review runs", TEXT)

    def test_the_findings_are_never_reported_in_the_conversation(self):
        self.assertIn("- Report the review, or its findings, in the conversation", TEXT)


if __name__ == "__main__":
    unittest.main()
