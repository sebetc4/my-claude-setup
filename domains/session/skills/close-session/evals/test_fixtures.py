"""Unit tests for evals/fixtures.py, which builds the repository a case of these evals starts
in, as the workspace.py of the authoring-skills skill runs it: fixtures.py <case> <folder>."""

import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent
ROADMAP = "docs/roadmap/on-progress/resilient-sync"
PHASE = f"{ROADMAP}/phase-1-retry-queue.md"
REPORT = f"{ROADMAP}/phase-1-retry-queue-report.md"
OPEN_NOTE = "notes/sessions/2026-10-10-export-formats.md"


def git(folder, *args):
    return subprocess.run(["git", *args], cwd=folder, capture_output=True, text=True, check=True).stdout


class Fixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name) / "fixture"
        self.folder.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, case):
        return subprocess.run([sys.executable, str(EVALS / "fixtures.py"), case, str(self.folder)],
                              capture_output=True, text=True)

    def read(self, path):
        return (self.folder / path).read_text(encoding="utf-8")

    def status(self):
        return sorted(line[3:] for line in git(self.folder, "status", "--porcelain", "-uall").splitlines())

    def run_tests(self):
        return subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"], cwd=self.folder,
                              capture_output=True, text=True, env={"PYTHONPATH": "src"})

    def ticked(self, text):
        return text.count("- [x] ")

    def assert_common(self):
        conventions = tomllib.loads(self.read(".agent-conventions.toml"))
        self.assertEqual(conventions["versioning"], "git")
        self.assertEqual(conventions["session"], {"notes": "notes/sessions"})
        self.assertIn(".agent-memory/", self.read("CLAUDE.md"))
        self.assertIn("MEMORY.md", git(self.folder, "ls-files", ".agent-memory"))
        self.assertIn("**Where the next session starts:**", self.read(REPORT))

    def test_an_unknown_case_is_refused_by_name(self):
        done = self.build("no-such-case")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("no-such-case", done.stderr)

    def test_the_step_stopped_midway_leaves_the_backoff_uncommitted(self):
        self.assertEqual(self.build("step-stopped-midway").returncode, 0)
        self.assert_common()
        self.assertEqual(self.status(), ["src/retry.py", "tests/test_backoff.py"])
        self.assertEqual(self.ticked(self.read(PHASE)), 1)
        self.assertIn("def backoff", self.read("src/retry.py"))
        self.assertNotIn("def backoff", git(self.folder, "show", "HEAD:src/retry.py"))
        self.assertFalse((self.folder / "notes/sessions").exists())
        tests = self.run_tests()
        self.assertIn("Ran 7 tests", tests.stderr)
        self.assertIn("FAILED (errors=2)", tests.stderr)

    def test_the_phase_with_every_task_ticked_leaves_its_last_task_uncommitted(self):
        self.assertEqual(self.build("phase-every-task-ticked").returncode, 0)
        self.assert_common()
        self.assertEqual(self.status(), ["config/local.toml", "docs/retry-policy.md", PHASE])
        self.assertEqual(self.ticked(self.read(PHASE)), 4)
        self.assertIn("(100% — 4/4)", self.read(PHASE))
        self.assertEqual(self.ticked(git(self.folder, "show", f"HEAD:{PHASE}")), 3)
        self.assertIn("🟡", self.read(PHASE))
        self.assertIn("must_alert", self.read("src/sync.py"))
        self.assertIn("ten_times", self.read("tests/test_sync.py"))
        tests = self.run_tests()
        self.assertEqual(tests.returncode, 0, tests.stderr)
        self.assertIn("Ran 8 tests", tests.stderr)

    def test_the_session_outside_the_roadmap_starts_from_an_open_note(self):
        self.assertEqual(self.build("outside-roadmap-note-taken-up").returncode, 0)
        self.assert_common()
        self.assertEqual(self.status(), [])
        note = self.read(OPEN_NOTE)
        self.assertIn("**Taken up:** —", note)
        self.assertIn("## Where The Next Session Starts", note)
        self.assertIn("Parquet", note)
        self.assertIn("**Taken up:** 2026-10-05", self.read("notes/sessions/2026-10-02-warehouse-api.md"))
        self.assertIn("open(", self.read("src/warehouse.py"))
        self.assertEqual(self.ticked(self.read(PHASE)), 1)


if __name__ == "__main__":
    unittest.main()
