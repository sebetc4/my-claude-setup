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

    def test_a_readme_without_a_progress_block_is_ignored(self):
        folder = self.folder.parent / "no-block"
        write(folder / "README.md", "# Just a readme\n")
        self.assert_silent(self.edit(folder / "README.md"))

    def test_a_readme_without_phase_files_is_ignored(self):
        folder = self.folder.parent / "no-phases"
        write(folder / "README.md",
              "# Roadmap: x\n\n## Overall Progress\n\n```\n"
              "TOTAL                                  ████████░░░░░░░░░░░░  42%  (3/8)\n"
              "```\n")
        self.assert_silent(self.edit(folder / "README.md"))

    def test_invalid_event_json_is_ignored(self):
        self.assert_silent(run_hook("progress_guard.py", "{"))


CONVENTIONS = """language = "english"
versioning = "git"

[roadmap]
root = "docs/roadmap"
"""

REPORT = """# Phase 1 Report: Build

**Start Commit:** abc1234

## Work Log

### 2026-09-16

Batched the commits; builds now meet the target.

## Changes To Later Phases

- **Pending approval** — `phase-2-ship.md`: merge it into phase 1.
"""

OLD_CONTRACT = """# Project

## Roadmaps

Root       : docs/roadmap/{pending,on-progress,completed}/
Language   : english
Versioning : git
"""


class SessionResume(unittest.TestCase):
    def setUp(self):
        self.project = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        (self.project / ".git").mkdir()
        self.folder = self.project / "docs/roadmap/on-progress/search"
        make_roadmap(self.folder, [("Framing", "🟢", 2, 2), ("Build", "🟡", 1, 3)])
        write(self.project / ".agent-conventions.toml", CONVENTIONS)
        write(self.folder / "phase-1-build-report.md", REPORT)

    def start(self, cwd=None):
        return run_hook("session_resume.py",
                        {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(cwd or self.project)})

    def context(self, cwd=None):
        result = self.start(cwd)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        return output["additionalContext"]

    def assert_silent(self, result):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_names_the_open_phase_in_one_conditional_line(self):
        self.assertEqual(self.context(), (
            "Roadmap search, Phase 1 Build in progress (1/3 tasks): "
            "docs/roadmap/on-progress/search/phase-1-build.md. If the request concerns this phase, "
            "load the roadmap skill and read the phase file and its report before working on it; "
            "otherwise, ignore this line."))

    def test_carries_neither_the_work_log_nor_pending_approvals(self):
        context = self.context()
        self.assertNotIn("Batched the commits", context)
        self.assertNotIn("Pending approval", context)

    def test_finds_a_first_phase_while_its_roadmap_is_still_pending(self):
        make_roadmap(self.project / "docs/roadmap/pending/billing", [("Framing", "🟡", 0, 4)])
        self.assertIn("docs/roadmap/pending/billing/phase-0-framing.md", self.context())

    def test_one_line_per_roadmap_with_an_open_phase(self):
        make_roadmap(self.project / "docs/roadmap/pending/billing", [("Framing", "🟡", 0, 4)])
        lines = self.context().splitlines()
        self.assertEqual([line.split(",")[0] for line in lines], ["Roadmap search", "Roadmap billing"])

    def test_reads_the_root_from_a_subdirectory_of_the_repository(self):
        (self.project / "src").mkdir()
        self.assertIn("docs/roadmap/on-progress/search/phase-1-build.md", self.context(self.project / "src"))

    def test_reads_a_root_with_spaces(self):
        write(self.project / ".agent-conventions.toml", CONVENTIONS.replace('"docs/roadmap"', '"my docs/road map"'))
        make_roadmap(self.project / "my docs/road map/on-progress/search", [("Build", "🟡", 1, 3)])
        self.assertIn("my docs/road map/on-progress/search/phase-0-build.md", self.context())

    def test_silent_without_agent_conventions_even_with_a_contract_in_claude_md(self):
        (self.project / ".agent-conventions.toml").unlink()
        write(self.project / "CLAUDE.md", OLD_CONTRACT)
        self.assert_silent(self.start())

    def test_silent_with_invalid_conventions(self):
        write(self.project / ".agent-conventions.toml", CONVENTIONS.replace('"git"', '"svn"'))
        self.assert_silent(self.start())

    def test_silent_without_a_roadmap_table(self):
        write(self.project / ".agent-conventions.toml", 'language = "english"\nversioning = "git"\n')
        self.assert_silent(self.start())

    def test_silent_without_a_phase_in_progress(self):
        make_roadmap(self.folder, [("Framing", "🟢", 2, 2), ("Build", "🟢", 3, 3)])
        self.assert_silent(self.start())

    def test_invalid_event_json_is_ignored(self):
        self.assert_silent(run_hook("session_resume.py", "{"))


if __name__ == "__main__":
    unittest.main()
