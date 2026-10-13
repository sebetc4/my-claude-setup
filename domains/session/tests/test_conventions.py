"""Tests for the [session] table, read through the copy of shared/conventions/ in the skill close-session."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
SCRIPT = DOMAIN / "skills" / "close-session" / "scripts" / "conventions.py"


def load():
    spec = importlib.util.spec_from_file_location("session_conventions", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SessionTable(unittest.TestCase):
    def setUp(self):
        self.conventions = load()
        tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.personal = tmp / "home/.claude"
        self.personal.mkdir(parents=True)
        self.repo = tmp / "repo"
        (self.repo / ".git").mkdir(parents=True)

    def read(self, text=None):
        if text is not None:
            (self.repo / ".agent-conventions.toml").write_text(text, encoding="utf-8")
        return self.conventions.read("session", self.repo, personal=self.personal)

    def test_the_table_names_the_notes_folder(self):
        result = self.read('language = "french"\n\n[session]\nnotes = "notes/sessions"\n')
        self.assertEqual(result.status, "ok", result.problems)
        self.assertEqual(result.values, {"language": "french", "notes": "notes/sessions"})

    def test_a_repository_without_the_file(self):
        self.assertEqual(self.read().status, "missing")

    def test_a_file_without_the_table(self):
        result = self.read('language = "english"\n\n[roadmap]\nroot = "docs/roadmap"\n')
        self.assertEqual(result.status, "invalid")
        self.assertEqual(result.problems, ["no [session] table"])

    def test_a_notes_folder_outside_the_repository(self):
        result = self.read('[session]\nnotes = "../notes"\n')
        self.assertEqual(result.status, "invalid")
        self.assertEqual(result.problems,
                         ['line 2: [session] notes = "../notes" must be relative to the root, without ".."'])


if __name__ == "__main__":
    unittest.main()
