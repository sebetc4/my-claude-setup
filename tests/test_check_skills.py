"""Tests for the dev hook .claude/hooks/check-skills.py and the options of tests/check.py it runs."""

import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = load("check_skills_hook", ROOT / ".claude" / "hooks" / "check-skills.py")
check = load("check_runner", ROOT / "tests" / "check.py")

FAILING = '''import unittest


class Demo(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1, 2)

    def test_two(self):
        raise KeyError("x")
'''


def unittest_stderr(source):
    """What unittest writes when it runs a test file holding source."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "test_demo.py").write_text(source, encoding="utf-8")
        return subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", "test_demo.py"],
                              capture_output=True, text=True, cwd=tmp).stderr


class Brief(unittest.TestCase):
    def test_a_failure_is_reported_by_its_test_id_and_first_line(self):
        lines = check.brief(unittest_stderr(FAILING))
        self.assertEqual(lines, ["ERROR test_two (test_demo.Demo.test_two): KeyError: 'x'",
                                 "FAIL test_one (test_demo.Demo.test_one): AssertionError: 1 != 2"])

    def test_a_module_that_does_not_load_is_one_line(self):
        lines = check.brief(unittest_stderr("def broken(:\n"))
        self.assertEqual(len(lines), 1)
        self.assertIn("SyntaxError", lines[0])


class Quiet(unittest.TestCase):
    def test_no_report_after_a_bash_command_that_ran_the_checks(self):
        for command in ("make check", "make -s check", "python3 -B tests/check.py", "cd x && make check; echo $?"):
            with self.subTest(command=command):
                self.assertFalse(hook.touched({"tool_name": "Bash", "tool_input": {"command": command}}))


class Narrow(unittest.TestCase):
    def test_the_dev_hook_runs_no_skill_check(self):
        self.assertIn("--skip-skills", hook.command())
        self.assertIn("--brief", hook.command())

    def test_the_dev_hook_writes_no_bytecode(self):
        # tests/check.py loads each skill's audit.py: without -B, a __pycache__ lands in the skill
        self.assertEqual(hook.command()[:2], [sys.executable, "-B"])

    def test_skip_skills_leaves_out_every_skill(self):
        self.assertEqual(check.options(["--skip-skills"]).skills, [])
        self.assertNotEqual(check.options([]).skills, [])


# A skill whose name differs from its folder: an error of the skill audit.
BROKEN = "---\nname: other-name\ndescription: Broken.\n---\n\nBody.\n"
# git reads neither the user's nor the system's configuration, and commits under a fixed name.
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
           "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"}


class Folders(unittest.TestCase):
    """The skills checked are those under the folders the [skills] conventions name."""

    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_check(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check.main([], root=self.root)
        return code, out.getvalue()

    def test_a_skill_under_every_folder_the_conventions_name_is_checked(self):
        self.write(".agent-conventions.toml", '[skills]\ndirs = ["domains/*/skills", ".claude/skills"]\n')
        self.write(".claude/skills/broken/SKILL.md", BROKEN)
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn(".claude/skills/broken/SKILL.md:2: [N3]", out)

    def test_without_conventions_the_domains_skills_are_checked_and_a_warning_says_so(self):
        self.write("domains/demo/skills/broken/SKILL.md", BROKEN)
        self.write(".claude/skills/ignored/SKILL.md", BROKEN.replace("other-name", "elsewhere"))
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("domains/demo/skills/broken/SKILL.md:2: [N3]", out)
        self.assertNotIn("ignored", out)
        self.assertIn(".agent-conventions.toml:1: [skills] not read (no file): checking domains/*/skills", out)

    def test_a_release_on_main_without_its_tag_is_a_warning(self):
        self.write("domains/demo/VERSION", "0.1.0\n")
        self.write("domains/demo/CHANGELOG.md", "# Changelog — demo\n\n## 0.1.0 — 2026-10-11\n\n- First.\n")
        self.write("domains/demo/skills/broken/SKILL.md", BROKEN)
        with mock.patch.dict(os.environ, GIT_ENV):
            for args in (["init", "-q", "-b", "main"], ["add", "-A"], ["commit", "-q", "-m", "release"]):
                subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
            _, out = self.run_check()
        self.assertRegex(out, r"domains/demo/VERSION:1: demo 0\.1\.0, set in [0-9a-f]{7}, "
                              r"has no tag demo-v0\.1\.0: run make tags")


if __name__ == "__main__":
    unittest.main()
