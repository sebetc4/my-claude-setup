"""Tests for tests/domains.py, on temporary domains."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location("domain_checks", Path(__file__).resolve().parent / "domains.py")
domains = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(domains)

AGENT = "---\nname: auditor\ndescription: Audits things before they are reported.\ntools: Read\n---\n\nYou audit things.\n"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class AgentChecks(unittest.TestCase):
    def setUp(self):
        self.domain = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve() / "sample"
        self.domain.mkdir()

    def problems(self):
        return [message for _, _, message in domains.check_agents(self.domain)]

    def test_a_valid_agent_has_no_problem(self):
        write(self.domain / "agents/auditor.md", AGENT)
        self.assertEqual(self.problems(), [])

    def test_a_name_that_differs_from_the_file_name(self):
        write(self.domain / "agents/other.md", AGENT)
        self.assertEqual(self.problems(), ["name 'auditor' does not match the file name 'other'"])

    def test_a_missing_description(self):
        write(self.domain / "agents/auditor.md", AGENT.replace("description: Audits things before they are reported.\n", ""))
        self.assertEqual(self.problems(), ["description is missing"])

    def test_missing_frontmatter(self):
        write(self.domain / "agents/auditor.md", "You audit things.\n")
        self.assertEqual(self.problems(), ["missing YAML frontmatter"])

    def test_compatibility_wording_is_reported(self):
        write(self.domain / "agents/auditor.md", AGENT + "Keep the legacy format.\n")
        problems = self.problems()
        self.assertEqual(len(problems), 1)
        self.assertIn("compatibility wording", problems[0])

    def test_a_domain_without_agents_has_no_problem(self):
        self.assertEqual(self.problems(), [])


CHANGELOG = "# Changelog — sample\n\n## 1.0.0 — 2026-09-17\n\n- First release.\n"


class VersionChecks(unittest.TestCase):
    def setUp(self):
        self.domain = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve() / "sample"
        self.domain.mkdir()

    def problems(self):
        return [message for _, _, message in domains.check_version(self.domain)]

    def test_a_matching_version_and_changelog_have_no_problem(self):
        write(self.domain / "VERSION", "1.0.0\n")
        write(self.domain / "CHANGELOG.md", CHANGELOG)
        self.assertEqual(self.problems(), [])

    def test_a_missing_version_file(self):
        self.assertEqual(self.problems(), ["missing VERSION file: every domain has one, of the form X.Y.Z"])

    def test_a_malformed_version(self):
        write(self.domain / "VERSION", "v1\n")
        self.assertEqual(self.problems(), ["'v1' is not of the form X.Y.Z"])

    def test_a_missing_changelog(self):
        write(self.domain / "VERSION", "1.0.0\n")
        self.assertEqual(self.problems(), ["missing CHANGELOG.md, or no ## entry in it"])

    def test_a_changelog_opening_with_another_version(self):
        write(self.domain / "VERSION", "1.0.0\n")
        write(self.domain / "CHANGELOG.md", "# Changelog\n\n## 0.9.0 — 2026-09-01\n\n## 1.0.0 — 2026-09-17\n")
        self.assertEqual(self.problems(), ["first entry '0.9.0 — 2026-09-01' does not match VERSION 1.0.0"])


if __name__ == "__main__":
    unittest.main()
