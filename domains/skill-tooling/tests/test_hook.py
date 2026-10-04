"""Tests for the skill audit hook, run the way the harness runs a PostToolUse hook: the
event as JSON on stdin."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "audit_skill.py"
CLEAN = "---\nname: demo\ndescription: Does a thing. Use when asked.\n---\n\nBody.\n"


def run_hook(event):
    stdin = event if isinstance(event, str) else json.dumps(event)
    return subprocess.run([sys.executable, "-B", str(HOOK)], input=stdin, capture_output=True, text=True)


def edit(path):
    return {"tool_name": "Edit", "tool_input": {"file_path": str(path)}}


class Hook(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.skill = self.tmp / "demo"
        self.skill.mkdir()

    def write(self, relative, text):
        path = self.skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_an_edited_file_of_a_skill_with_an_error_is_reported(self):
        self.write("SKILL.md", CLEAN.replace("description:", "tools: Read\ndescription:"))
        reference = self.write("references/guide.md", "Guide.\n")
        result = run_hook(edit(reference))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("[F6] unknown field `tools`", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_a_file_outside_any_skill_is_left_alone(self):
        other = self.tmp / "notes.md"
        other.write_text("Notes.\n", encoding="utf-8")
        result = run_hook(edit(other))
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_a_clean_skill_and_warnings_stay_silent(self):
        for text in (CLEAN, CLEAN.replace("Body.", "Keep the legacy format.")):
            with self.subTest(text=text[-30:]):
                result = run_hook(edit(self.write("SKILL.md", text)))
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_the_report_holds_one_line_per_failing_rule(self):
        body = "".join(f"See `references/missing-{i}.md`.\n" for i in range(5))
        result = run_hook(edit(self.write("SKILL.md", CLEAN.replace("tools:", "") .replace("Body.\n", body)
                                                       .replace("description:", "tools: Read\ndescription:"))))
        self.assertEqual(result.returncode, 2, result.stderr)
        lines = [line for line in result.stderr.splitlines() if line.startswith("- ")]
        self.assertEqual([line.split("]")[0] for line in lines], ["- [F6", "- [R1"])
        self.assertIn("and 4 more", lines[1])

    def test_an_unreadable_event_is_ignored(self):
        self.assertEqual(run_hook("not json").returncode, 0)


if __name__ == "__main__":
    unittest.main()
