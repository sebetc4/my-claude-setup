"""Unit tests for the checks specific to domains/skill-tooling/skills/authoring-skills."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checks = load("authoring_checks", EVALS / "checks.py")


class TemplateChecks(unittest.TestCase):
    def skill_with_template(self, text):
        folder = Path(self.enterContext(tempfile.TemporaryDirectory()))
        (folder / "assets/templates").mkdir(parents=True)
        (folder / "assets/templates/task.md").write_text(text, encoding="utf-8")
        return folder

    def test_a_template_holds_no_html_comment(self):
        problems = list(checks.run(self.skill_with_template("# {{TITLE}}\n<!-- a note -->\n")))
        self.assertEqual([(line, message.split(":")[0]) for _, line, message in problems],
                         [(2, "HTML comment in a template")])

    def test_placeholders_are_upper_snake_case(self):
        problems = list(checks.run(self.skill_with_template("# {{Title}}\n")))
        self.assertEqual([line for _, line, _ in problems], [1])

    def test_a_template_that_keeps_both_rules_passes(self):
        self.assertEqual(list(checks.run(self.skill_with_template("# {{SKILL_NAME}}\n"))), [])


if __name__ == "__main__":
    unittest.main()
