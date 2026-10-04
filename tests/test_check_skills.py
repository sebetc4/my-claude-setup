"""Tests for the dev hook .claude/hooks/check-skills.py and the options of tests/check.py it runs."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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

    def test_skip_skills_leaves_out_every_skill(self):
        self.assertEqual(check.options(["--skip-skills"]).skills, [])
        self.assertNotEqual(check.options([]).skills, [])


if __name__ == "__main__":
    unittest.main()
