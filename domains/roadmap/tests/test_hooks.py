"""Tests for the roadmap domain's hooks, run the way Claude Code runs them: event JSON on stdin."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent
HOOKS = DOMAIN / "hooks"
_spec = importlib.util.spec_from_file_location("roadmap_progress", DOMAIN / "skills/roadmap/scripts/progress.py")
progress = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(progress)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_hook(name, event):
    stdin = event if isinstance(event, str) else json.dumps(event)
    return subprocess.run([sys.executable, "-B", str(HOOKS / name)], input=stdin, capture_output=True, text=True)


def make_roadmap(folder, phases):
    """Write one phase file per (name, emoji, done, total) and a README whose progress block matches them."""
    for number, (name, emoji, done, total) in enumerate(phases):
        tasks = "\n".join(f"- [{'x' if i < done else ' '}] Task {i}" for i in range(total))
        write(folder / f"phase-{number}-{name.lower()}.md",
              f"# Phase {number}: {name}\n\n## Status\n\n**Current Status:** {emoji} Label "
              f"({progress.percent(done, total)}% — {done}/{total})\n\n## Tasks\n\n{tasks}\n")
    block = "\n".join(progress.render(progress.read_phases(folder)))
    write(folder / "README.md", f"# Roadmap: x\n\n## Overall Progress\n\n```\n{block}\n```\n")


class ProgressGuard(unittest.TestCase):
    def setUp(self):
        root = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.folder = root / "docs/roadmap/on-progress/search"
        make_roadmap(self.folder, [("Framing", "🟢", 2, 2), ("Build", "🟡", 1, 3), ("Ship", "🔴", 0, 2)])

    def edit(self, path):
        return run_hook("progress_guard.py", {"tool_name": "Edit", "tool_input": {"file_path": str(path)}})

    def break_total(self):
        readme = self.folder / "README.md"
        write(readme, readme.read_text(encoding="utf-8").replace("(3/7)", "(3/8)"))

    def assert_silent(self, result):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_a_consistent_roadmap_is_silent(self):
        self.assert_silent(self.edit(self.folder / "README.md"))

    def test_an_inconsistent_block_exits_2_with_the_problem(self):
        self.break_total()
        result = self.edit(self.folder / "README.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("TOTAL: shows 3/8, the phase lines add up to 3/7", result.stderr)
        self.assertIn("scripts/progress.py", result.stderr)

    def test_editing_a_phase_file_checks_its_roadmap(self):
        self.break_total()
        self.assertEqual(self.edit(self.folder / "phase-1-build.md").returncode, 2)

    def test_two_phases_in_progress_exit_2(self):
        make_roadmap(self.folder, [("Framing", "🟡", 1, 2), ("Build", "🟡", 1, 3), ("Ship", "🔴", 0, 2)])
        result = self.edit(self.folder / "phase-0-framing.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("🟡 on more than one phase: phase-0-framing.md, phase-1-build.md", result.stderr)

    def test_a_report_edit_is_ignored(self):
        self.break_total()
        report = self.folder / "phase-1-build-report.md"
        write(report, "# Phase 1 Report: Build\n")
        self.assert_silent(self.edit(report))

    def test_a_file_outside_a_roadmap_is_ignored(self):
        notes = self.folder.parent / "notes.md"
        write(notes, "notes\n")
        self.assert_silent(self.edit(notes))

    def test_invalid_event_json_is_ignored(self):
        self.assert_silent(run_hook("progress_guard.py", "{"))


if __name__ == "__main__":
    unittest.main()
