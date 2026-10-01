"""Tests for tools/shared.py: copies of the shared modules into the skills that use them."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "shared.py"
_spec = importlib.util.spec_from_file_location("shared", TOOL)
shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shared)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class Shared(unittest.TestCase):
    def setUp(self):
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        write(self.repo / "shared/conventions/conventions.py", "#!/usr/bin/env python3\nSOURCE = 1\n")
        (self.repo / "shared/conventions/conventions.py").chmod(0o755)
        write(self.repo / "shared/conventions/conventions.md", "# Procedure\n")
        write(self.repo / "shared/conventions/tests/test_conventions.py", "")
        self.skill = self.repo / "domains/roadmap/skills/roadmap"
        write(self.skill / "SKILL.md", "")

    def copy_path(self, name):
        return self.skill / ("scripts" if name.endswith(".py") else "references") / name

    def test_the_sources_map_to_scripts_and_references(self):
        self.assertEqual(sorted(shared.copies(self.repo, self.skill).values()),
                         [self.copy_path("conventions.md"), self.copy_path("conventions.py")])

    def test_tests_are_never_copied(self):
        self.assertNotIn("test_conventions.py", {p.name for p in shared.copies(self.repo, self.skill).values()})

    def test_install_copies_into_a_skill_and_keeps_the_executable_bit(self):
        shared.install(self.repo, self.skill)
        script = self.copy_path("conventions.py")
        self.assertEqual(script.read_text(encoding="utf-8"), "#!/usr/bin/env python3\nSOURCE = 1\n")
        self.assertTrue(script.stat().st_mode & 0o111)

    def test_a_fresh_copy_is_clean(self):
        shared.install(self.repo, self.skill)
        self.assertEqual(list(shared.stale(self.repo)), [])

    def test_a_copy_that_differs_is_reported(self):
        shared.install(self.repo, self.skill)
        write(self.copy_path("conventions.py"), "edited\n")
        self.assertEqual([(path, message) for path, _, message in shared.stale(self.repo)],
                         [(self.copy_path("conventions.py"),
                           "differs from shared/conventions/conventions.py; edit the source, then run make shared")])

    def test_a_skill_with_one_copy_is_reported_for_the_missing_one(self):
        write(self.copy_path("conventions.py"), "#!/usr/bin/env python3\nSOURCE = 1\n")
        self.assertEqual([(path, message) for path, _, message in shared.stale(self.repo)],
                         [(self.copy_path("conventions.md"),
                           "missing copy of shared/conventions/conventions.md; run make shared")])

    def test_refresh_updates_every_skill_that_uses_a_module(self):
        shared.install(self.repo, self.skill)
        write(self.repo / "shared/conventions/conventions.py", "#!/usr/bin/env python3\nSOURCE = 2\n")
        other = self.repo / "domains/skill-tooling/skills/authoring-skills"
        write(other / "SKILL.md", "")
        refreshed = shared.refresh(self.repo)
        self.assertEqual(refreshed, [self.copy_path("conventions.py")])
        self.assertIn("SOURCE = 2", self.copy_path("conventions.py").read_text(encoding="utf-8"))
        self.assertFalse((other / "scripts").exists())

    def test_the_command_installs_into_a_named_skill_then_refreshes(self):
        result = subprocess.run([sys.executable, "-B", str(TOOL), "--repo", str(self.repo), str(self.skill)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.copy_path("conventions.md").is_file())
        check = subprocess.run([sys.executable, "-B", str(TOOL), "--repo", str(self.repo), "--check"],
                               capture_output=True, text=True)
        self.assertEqual((check.returncode, check.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
