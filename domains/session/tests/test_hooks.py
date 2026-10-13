"""Tests for the session domain's hooks, run the way Claude Code runs them: event JSON on stdin."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parent.parent / "hooks"
CONVENTIONS = 'language = "french"\n\n[session]\nnotes = "notes/sessions"\n'
POINT = "1. Lire le code du daemon des runtimes.\n2. Demander quelle CLI essayer.\n"
SUFFIX = ". If the request continues that work, read the note before working; otherwise, ignore this line."


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_hook(name, event):
    stdin = event if isinstance(event, str) else json.dumps(event)
    return subprocess.run([sys.executable, "-B", str(HOOKS / name)], input=stdin, capture_output=True, text=True)


def note(date="2026-10-13", taken="—", point=POINT):
    return (f"# Runtimes\n\n**Date:** {date}\n**Taken up:** {taken}\n\n"
            f"## Where The Next Session Starts\n\n{point}\n## Done\n\n- Le daemon est lu.\n")


class ResumeNote(unittest.TestCase):
    def setUp(self):
        self.project = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        (self.project / ".git").mkdir()
        write(self.project / ".agent-conventions.toml", CONVENTIONS)
        self.notes = self.project / "notes/sessions"

    def add(self, name, text):
        write(self.notes / name, text)

    def start(self, cwd=None):
        return run_hook("resume_note.py",
                        {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(cwd or self.project)})

    def context(self, cwd=None):
        result = self.start(cwd)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        return output["additionalContext"]

    def names(self):
        return [line.split()[2] for line in self.context().splitlines()]

    def assert_silent(self, result):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_names_an_open_note_in_one_conditional_line(self):
        self.add("2026-10-13-runtimes.md", note())
        self.assertEqual(self.context(), (
            "Resume note notes/sessions/2026-10-13-runtimes.md (2026-10-13), not taken up: "
            "Lire le code du daemon des runtimes" + SUFFIX))

    def test_one_line_per_open_note_latest_first(self):
        self.add("2026-10-12-domains.md", note("2026-10-12"))
        self.add("2026-10-13-runtimes.md", note("2026-10-13"))
        self.assertEqual(self.names(), ["notes/sessions/2026-10-13-runtimes.md",
                                        "notes/sessions/2026-10-12-domains.md"])

    def test_three_notes_at_most(self):
        for day in range(10, 15):
            self.add(f"2026-10-{day}-strand.md", note(f"2026-10-{day}"))
        self.assertEqual(self.names(), ["notes/sessions/2026-10-14-strand.md",
                                        "notes/sessions/2026-10-13-strand.md",
                                        "notes/sessions/2026-10-12-strand.md"])

    def test_notes_of_the_same_day_by_their_last_change(self):
        self.add("2026-10-13-a-later.md", note())
        self.add("2026-10-13-b-earlier.md", note())
        os.utime(self.notes / "2026-10-13-b-earlier.md", (1_000_000_000, 1_000_000_000))
        self.assertEqual(self.names(), ["notes/sessions/2026-10-13-a-later.md",
                                        "notes/sessions/2026-10-13-b-earlier.md"])

    def test_a_note_taken_up_is_left_out(self):
        self.add("2026-10-12-domains.md", note("2026-10-12", taken="2026-10-13, 2026-10-13-runtimes.md"))
        self.add("2026-10-11-plugins.md", note("2026-10-11", taken="2026-10-12, finished"))
        self.add("2026-10-13-runtimes.md", note())
        self.assertEqual(self.names(), ["notes/sessions/2026-10-13-runtimes.md"])

    def test_a_file_without_the_taken_up_field_is_not_a_note(self):
        write(self.notes / "README.md", "# Notes\n\nResume notes of this repository.\n")
        self.add("2026-10-13-runtimes.md", note())
        self.assertEqual(self.names(), ["notes/sessions/2026-10-13-runtimes.md"])

    def test_a_first_item_on_several_lines_is_joined(self):
        self.add("2026-10-13-runtimes.md", note(point="1. Lire le code du daemon\n   des runtimes.\n2. Ensuite.\n"))
        self.assertIn("not taken up: Lire le code du daemon des runtimes. If", self.context())

    def test_a_long_first_item_is_cut(self):
        self.add("2026-10-13-runtimes.md", note(point="1. " + "mot " * 100 + "\n"))
        line = self.context()
        self.assertIn("mot mot…" + SUFFIX, line)
        self.assertLess(len(line), 400)

    def test_a_note_without_a_resume_point_is_still_named(self):
        self.add("2026-10-13-runtimes.md", note(point=""))
        self.assertEqual(self.context(), (
            "Resume note notes/sessions/2026-10-13-runtimes.md (2026-10-13), not taken up" + SUFFIX))

    def test_reads_the_table_from_a_subdirectory_of_the_repository(self):
        (self.project / "src").mkdir()
        self.add("2026-10-13-runtimes.md", note())
        self.assertIn("notes/sessions/2026-10-13-runtimes.md", self.context(self.project / "src"))

    def test_a_notes_folder_with_spaces(self):
        write(self.project / ".agent-conventions.toml", CONVENTIONS.replace("notes/sessions", "my notes/sessions"))
        write(self.project / "my notes/sessions/2026-10-13-runtimes.md", note())
        self.assertIn("my notes/sessions/2026-10-13-runtimes.md", self.context())

    def test_silent_without_agent_conventions(self):
        self.add("2026-10-13-runtimes.md", note())
        (self.project / ".agent-conventions.toml").unlink()
        self.assert_silent(self.start())

    def test_silent_without_a_session_table(self):
        self.add("2026-10-13-runtimes.md", note())
        write(self.project / ".agent-conventions.toml", '[roadmap]\nroot = "docs/roadmap"\n')
        self.assert_silent(self.start())

    def test_silent_with_an_invalid_table(self):
        self.add("2026-10-13-runtimes.md", note())
        write(self.project / ".agent-conventions.toml", '[session]\nnotes = "../notes"\n')
        self.assert_silent(self.start())

    def test_silent_without_the_notes_folder(self):
        self.assert_silent(self.start())

    def test_silent_when_every_note_is_taken_up(self):
        self.add("2026-10-12-domains.md", note("2026-10-12", taken="2026-10-13, finished"))
        self.assert_silent(self.start())

    def test_invalid_event_json_is_ignored(self):
        self.assert_silent(run_hook("resume_note.py", "{"))


if __name__ == "__main__":
    unittest.main()
