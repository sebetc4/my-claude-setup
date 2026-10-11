"""Tests for tools/tags.py, on temporary git repositories."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tags.py"
_spec = importlib.util.spec_from_file_location("tags", TOOL)
tags = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tags)

# git reads neither the user's nor the system's configuration, and commits under a fixed name.
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
           "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"}


class Repository(unittest.TestCase):
    def setUp(self):
        self.enterContext(mock.patch.dict(os.environ, GIT_ENV))
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.git("init", "-q", "-b", "main")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True,
                              check=True).stdout.strip()

    def commit(self, files, message="change"):
        """Writes {path: text} and commits it; returns the commit's id."""
        for path, text in files.items():
            target = self.repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def release(self, domain, version, entries):
        """The files of a domain at version, its changelog holding entries, newest first."""
        changelog = f"# Changelog — {domain}\n\n" + "".join(
            f"## {v} — 2026-10-0{i + 1}\n\n- {text}\n\n" for i, (v, text) in enumerate(entries))
        return {f"domains/{domain}/VERSION": version + "\n", f"domains/{domain}/CHANGELOG.md": changelog}

    def history(self):
        """Four commits on main: a 0.1.0, an unrelated change, a 0.1.1, then a 0.2.0 with b 1.0.0."""
        c1 = self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.commit({"README.md": "readme\n"})
        c3 = self.commit(self.release("a", "0.1.1", [("0.1.1", "Second."), ("0.1.0", "First.")]))
        c4 = self.commit({**self.release("a", "0.2.0", [("0.2.0", "Third."), ("0.1.1", "Second."),
                                                        ("0.1.0", "First.")]),
                          **self.release("b", "1.0.0", [("1.0.0", "Only.")])})
        return c1, c3, c4

    def found(self, function):
        return [(r.domain, r.version, r.commit) for r in function(self.repo)]


class Releases(Repository):
    def test_each_version_a_domain_took_on_main_is_a_release_at_the_commit_that_set_it(self):
        c1, c3, c4 = self.history()
        self.assertEqual(self.found(tags.releases),
                         [("a", "0.1.0", c1), ("a", "0.1.1", c3), ("a", "0.2.0", c4), ("b", "1.0.0", c4)])

    def test_a_tagged_release_is_not_missing(self):
        c1, c3, c4 = self.history()
        self.git("tag", "-a", "a-v0.1.0", c1, "-m", "a domain 0.1.0")
        self.assertEqual(self.found(tags.missing),
                         [("a", "0.1.1", c3), ("a", "0.2.0", c4), ("b", "1.0.0", c4)])

    def test_a_version_set_only_on_another_branch_is_not_a_release(self):
        c1 = self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.git("switch", "-q", "-c", "feature")
        self.commit(self.release("a", "0.2.0", [("0.2.0", "Next."), ("0.1.0", "First.")]))
        self.git("switch", "-q", "main")
        self.assertEqual(self.found(tags.releases), [("a", "0.1.0", c1)])

    def test_a_version_merged_into_main_is_released_at_the_merge(self):
        self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.git("switch", "-q", "-c", "feature")
        self.commit(self.release("a", "0.2.0", [("0.2.0", "Next."), ("0.1.0", "First.")]))
        self.git("switch", "-q", "main")
        self.git("merge", "-q", "--no-ff", "feature", "-m", "merge feature")
        merge = self.git("rev-parse", "HEAD")
        self.assertEqual(self.found(tags.releases)[-1], ("a", "0.2.0", merge))

    def test_a_version_is_released_once_its_changelog_entry_has_a_date(self):
        undated = "# Changelog — a\n\n## 0.1.0 — unreleased\n\n- First.\n"
        self.commit({"domains/a/VERSION": "0.1.0\n", "domains/a/CHANGELOG.md": undated})
        self.commit({"domains/a/code.py": "pass\n"})
        released = self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.commit({"domains/a/code.py": "pass  # later\n"})
        self.assertEqual(self.found(tags.releases), [("a", "0.1.0", released)])

    def test_a_version_not_of_the_form_x_y_z_is_not_a_release(self):
        self.commit({"domains/a/VERSION": "draft\n"})
        self.assertEqual(self.found(tags.releases), [])

    def test_a_repository_without_a_main_branch_has_no_release(self):
        self.git("switch", "-q", "-c", "trunk")
        self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.assertEqual(self.found(tags.releases), [])

    def test_a_folder_outside_git_has_no_release(self):
        plain = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        (plain / "domains/a").mkdir(parents=True)
        (plain / "domains/a/VERSION").write_text("0.1.0\n", encoding="utf-8")
        self.assertEqual(tags.releases(plain), [])
        self.assertEqual(tags.warnings(plain), [])


class Creation(Repository):
    def test_the_tag_message_holds_the_changelog_entry_of_the_release(self):
        self.history()
        release = tags.releases(self.repo)[1]
        self.assertEqual(tags.message(self.repo, release), "a domain 0.1.1\n\n- Second.")

    def test_create_makes_annotated_tags_on_the_release_commits_once(self):
        c1, c3, c4 = self.history()
        self.assertEqual(tags.create(self.repo), ["a-v0.1.0", "a-v0.1.1", "a-v0.2.0", "b-v1.0.0"])
        self.assertEqual(self.git("cat-file", "-t", "a-v0.1.1"), "tag")
        self.assertEqual(self.git("rev-list", "-n", "1", "a-v0.1.1"), c3)
        self.assertEqual(self.git("rev-list", "-n", "1", "b-v1.0.0"), c4)
        self.assertEqual(self.git("tag", "-l", "--format=%(contents)", "a-v0.2.0"), "a domain 0.2.0\n\n- Third.")
        self.assertEqual(tags.create(self.repo), [])

    def test_warnings_name_the_version_file_and_the_command(self):
        c1 = self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))
        self.assertEqual(tags.warnings(self.repo),
                         [(self.repo / "domains/a/VERSION", 1,
                           f"a 0.1.0, set in {c1[:7]}, has no tag a-v0.1.0: run make tags")])

    def test_the_command_lists_without_creating_then_creates_with_create(self):
        c1 = self.commit(self.release("a", "0.1.0", [("0.1.0", "First.")]))

        def run(*args):
            result = subprocess.run([sys.executable, "-B", str(TOOL), "--repo", str(self.repo), *args],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

        self.assertEqual(run(), f"a-v0.1.0 {c1[:7]}\n1 tag missing: tools/tags.py --create makes it\n")
        self.assertEqual(self.git("tag", "-l"), "")
        self.assertEqual(run("--create"), f"created a-v0.1.0 on {c1[:7]}\n")
        self.assertEqual(run(), "no tag missing\n")


if __name__ == "__main__":
    unittest.main()
