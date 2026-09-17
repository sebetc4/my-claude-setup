"""Unit tests for the scripts bundled with domains/roadmap/skills/roadmap."""

import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


progress = load("progress")


def phase_file(number, name, emoji, done, total):
    tasks = "\n".join(f"- [{'x' if i < done else ' '}] Task {i}" for i in range(total))
    pct = progress.half_up(done / total * 100) if total else 0
    return textwrap.dedent(f"""\
        # Phase {number}: {name}

        ## Status

        **Current Status:** {emoji} Label ({pct}% — {done}/{total})

        ## Tasks

        ### Work
        """) + tasks + textwrap.dedent("""

        ## Acceptance Criteria

        - [ ] Unticked criterion that must not be counted
        - [x] Ticked criterion that must not be counted
        """)


EXAMPLE = [
    "Phase 0  Framing                    🟢 ████████████████████ 100%  (7/7)",
    "Phase 1  Implementation             🟡 █████████████░░░░░░░  64%  (7/11)",
    "Phase 2  Validation                 🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/15)",
    "TOTAL                                  ████████░░░░░░░░░░░░  42%  (14/33)",
]


class Bar(unittest.TestCase):
    def test_rounds_half_up(self):
        self.assertEqual(progress.bar(1, 8, started=True), "███" + "░" * 17)  # 2.5 → 3

    def test_started_phase_never_shows_zero_cells(self):
        self.assertEqual(progress.bar(1, 50, started=True), "█" + "░" * 19)

    def test_unstarted_empty_phase_shows_zero_cells(self):
        self.assertEqual(progress.bar(0, 15, started=False), "░" * 20)

    def test_unfinished_phase_never_shows_twenty_cells(self):
        self.assertEqual(progress.bar(49, 50, started=True), "█" * 19 + "░")

    def test_finished_phase_is_full(self):
        self.assertEqual(progress.bar(7, 7, started=True), "█" * 20)

    def test_empty_phase_is_empty(self):
        self.assertEqual(progress.bar(0, 0, started=False), "░" * 20)


class Roadmap(unittest.TestCase):
    def make(self, phases, readme_block=None):
        folder = Path(self.enterContext(tempfile.TemporaryDirectory()))
        for number, (name, emoji, done, total) in enumerate(phases):
            slug = name.lower()
            (folder / f"phase-{number}-{slug}.md").write_text(phase_file(number, name, emoji, done, total), encoding="utf-8")
            (folder / f"phase-{number}-{slug}-report.md").write_text("- [ ] not a task\n", encoding="utf-8")
        block = "\n".join(readme_block if readme_block is not None else EXAMPLE)
        (folder / "README.md").write_text(f"# Roadmap: x\n\n## Overall Progress\n\n```\n{block}\n```\n", encoding="utf-8")
        return folder

    def example(self, **changes):
        return self.make([("Framing", "🟢", 7, 7), ("Implementation", "🟡", 7, 11), ("Validation", "🔴", 0, 15)], **changes)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "progress.py"), *map(str, args)],
                              capture_output=True, text=True)

    def test_renders_the_skill_example(self):
        self.assertEqual(progress.render(progress.read_phases(self.example())), EXAMPLE)

    def test_counts_only_the_tasks_section_and_ignores_reports(self):
        phases = progress.read_phases(self.example())
        self.assertEqual([(p.done, p.total) for p in phases], [(7, 7), (7, 11), (0, 15)])

    def test_orders_phases_numerically(self):
        folder = self.make([(f"P{i}", "🔴", 0, 1) for i in range(11)], readme_block=[])
        self.assertEqual([p.number for p in progress.read_phases(folder)], list(range(11)))

    def test_widens_the_label_column_for_long_names(self):
        folder = self.make([("A" * 40, "🔴", 0, 1)], readme_block=[])
        lines = progress.render(progress.read_phases(folder))
        self.assertEqual(lines[0].index("🔴") + 3, lines[1].index("░"))

    def test_prints_the_block(self):
        result = self.run_script(self.example())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), EXAMPLE)

    def test_check_passes_on_a_consistent_roadmap(self):
        result = self.run_script("--check", self.example())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_reports_a_stale_total(self):
        stale = EXAMPLE[:3] + ["TOTAL                                  ████████░░░░░░░░░░░░  42%  (14/32)"]
        result = self.run_script("--check", self.example(readme_block=stale))
        self.assertEqual(result.returncode, 1)
        self.assertIn("TOTAL", result.stdout)

    def test_check_reports_a_wrong_phase_status_count(self):
        folder = self.example()
        path = folder / "phase-1-implementation.md"
        path.write_text(path.read_text(encoding="utf-8").replace("(64% — 7/11)", "(64% — 7/10)"), encoding="utf-8")
        result = self.run_script("--check", folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn("phase-1-implementation.md", result.stdout)

    def test_check_reports_a_done_phase_with_unticked_tasks(self):
        folder = self.make([("Closed", "🟢", 3, 4), ("Next", "🔴", 0, 2)], readme_block=[])
        folder.joinpath("README.md").write_text(
            "## Overall Progress\n\n```\n" + "\n".join(progress.render(progress.read_phases(folder))) + "\n```\n",
            encoding="utf-8")
        result = self.run_script("--check", folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn("phase-0-closed.md: 🟢 with 1 unticked task", result.stdout)

    def test_check_reports_two_phases_in_progress(self):
        folder = self.make([("One", "🟡", 1, 2), ("Two", "🟡", 1, 2)], readme_block=[])
        folder.joinpath("README.md").write_text(
            "## Overall Progress\n\n```\n" + "\n".join(progress.render(progress.read_phases(folder))) + "\n```\n",
            encoding="utf-8")
        result = self.run_script("--check", folder)
        self.assertEqual(result.returncode, 1)
        self.assertIn("🟡", result.stdout)


class Links(unittest.TestCase):
    def run_script(self, cwd, *globs):
        return subprocess.run([sys.executable, str(SCRIPTS / "check_links.py"), *globs],
                              capture_output=True, text=True, cwd=cwd)

    def tree(self):
        root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        folder = root / "docs/roadmap/on-progress/my roadmap (rc1)"
        folder.mkdir(parents=True)
        (folder / "phase-0-a.md").write_text("x\n", encoding="utf-8")
        return root, folder

    def test_counts_resolving_links(self):
        root, folder = self.tree()
        (folder / "README.md").write_text(
            "[a](phase-0-a.md) [b](phase-0-a.md#tasks) [c](https://x.org) [d](#top) [e](mailto:a@b.c)\n",
            encoding="utf-8")
        result = self.run_script(root, "docs/roadmap/*/*/*.md")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("2 relative links, 0 broken", result.stdout)

    def test_reports_a_broken_link(self):
        root, folder = self.tree()
        (folder / "README.md").write_text("[gone](phase-9-gone.md)\n", encoding="utf-8")
        result = self.run_script(root, "docs/roadmap/*/*/*.md", "CLAUDE.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("phase-9-gone.md", result.stdout)
        self.assertIn("1 broken", result.stdout)

    def test_decodes_percent_encoded_links(self):
        root, folder = self.tree()
        (root / "CLAUDE.md").write_text("[r](docs/roadmap/on-progress/my%20roadmap%20%28rc1%29/phase-0-a.md)\n",
                                        encoding="utf-8")
        result = self.run_script(root, "CLAUDE.md")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fails_when_no_file_matches(self):
        root, _ = self.tree()
        result = self.run_script(root, "nothing/*/*/*.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("no files matched", result.stdout)


if __name__ == "__main__":
    unittest.main()
