"""Tests for the reader of .agent-conventions.toml: lookup, validation, output, and the command."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "conventions.py"
_spec = importlib.util.spec_from_file_location("conventions", SCRIPT)
conventions = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(conventions)

VALID = """\
language   = "english"
versioning = "git"
checks     = ["make check"]

[roadmap]
root = "docs/roadmap"

[skills]
dirs = ["domains/*/skills"]
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.personal = self.tmp / "home/.claude"
        self.personal.mkdir(parents=True)
        self.repo = self.tmp / "repo"
        (self.repo / ".git").mkdir(parents=True)

    def conventions(self, text):
        write(self.repo / ".agent-conventions.toml", text)

    def read(self, tool="roadmap", start=None):
        return conventions.read(tool, start or self.repo, personal=self.personal)

    def problems(self, text, tool="roadmap"):
        self.conventions(text)
        result = self.read(tool)
        self.assertEqual(result.status, "invalid", result.problems)
        return result.problems


class Lookup(Case):
    def test_the_root_is_found_from_a_path_below_it(self):
        self.conventions(VALID)
        result = self.read(start=self.repo / "docs/roadmap/on-progress")
        self.assertEqual((result.status, result.root), ("ok", self.repo))

    def test_the_root_is_found_from_a_file_path(self):
        self.conventions(VALID)
        write(self.repo / "src/main.py", "")
        self.assertEqual(self.read(start=self.repo / "src/main.py").root, self.repo)

    def test_a_worktree_git_file_marks_the_root(self):
        worktree = self.tmp / "worktree"
        write(worktree / ".git", "gitdir: elsewhere\n")
        write(worktree / ".agent-conventions.toml", VALID)
        self.assertEqual(self.read(start=worktree / "a/b").root, worktree)

    def test_the_lookup_never_goes_above_the_repository_root(self):
        write(self.tmp / ".agent-conventions.toml", VALID)
        result = self.read(start=self.repo / "sub")
        self.assertEqual((result.status, result.root), ("missing", self.repo))

    def test_a_folder_without_git_is_found_through_its_file(self):
        project = self.tmp / "nogit"
        write(project / ".agent-conventions.toml", VALID)
        self.assertEqual(self.read(start=project / "deep/er").root, project)

    def test_a_nested_file_wins_below_the_git_root(self):
        self.conventions(VALID)
        write(self.repo / "sub/.agent-conventions.toml", VALID.replace("english", "français"))
        result = self.read(start=self.repo / "sub/x")
        self.assertEqual((result.root, result.values["language"]), (self.repo / "sub", "français"))

    def test_the_personal_directory_is_the_root_of_personal_skills(self):
        write(self.personal / ".agent-conventions.toml", VALID)
        result = self.read("skills", start=self.personal / "skills/roadmap")
        self.assertEqual((result.status, result.root), ("ok", self.personal))

    def test_no_root_when_nothing_marks_one(self):
        result = self.read(start=self.tmp / "loose/dir")
        self.assertEqual((result.status, result.root), ("no-root", None))

    def test_missing_file(self):
        result = self.read()
        self.assertEqual((result.status, result.root, result.file), ("missing", self.repo, None))


class Resolution(Case):
    def test_a_table_is_resolved_against_the_shared_keys(self):
        self.conventions(VALID)
        result = self.read()
        self.assertEqual(result.status, "ok", result.problems)
        self.assertEqual(result.values, {
            "language": "english", "versioning": "git",
            "checks": [{"run": "make check", "dir": "."}], "root": "docs/roadmap"})
        self.assertEqual(result.undeclared, [])

    def test_a_table_key_overrides_the_shared_one_whole(self):
        self.conventions(VALID.replace(
            'root = "docs/roadmap"', 'root = "docs/roadmap"\nlanguage = "français"\nchecks = []'))
        result = self.read()
        self.assertEqual((result.values["language"], result.values["checks"]), ("français", []))

    def test_checks_take_a_working_directory(self):
        self.conventions(VALID.replace('["make check"]', '[{ run = "make test", dir = "sub/project" }]'))
        self.assertEqual(self.read().values["checks"], [{"run": "make test", "dir": "sub/project"}])

    def test_residue_comes_with_versioning_none(self):
        self.conventions(VALID.replace('"git"', '"none"').replace(
            "checks", 'residue = ["__pycache__/", "save_*.json"]\nchecks'))
        result = self.read()
        self.assertEqual(result.status, "ok", result.problems)
        self.assertEqual(result.values["residue"], ["__pycache__/", "save_*.json"])

    def test_the_skills_table_keeps_only_declared_conventions(self):
        self.conventions(VALID.replace('dirs = ["domains/*/skills"]',
                                       'dirs = ["domains/*/skills"]\naddress = "agent"\n'
                                       'exclude = ["allowed-tools", "dynamic-context"]'))
        result = self.read("skills")
        self.assertEqual(result.status, "ok", result.problems)
        self.assertEqual(result.values["exclude"], ["allowed-tools", "dynamic-context"])
        self.assertEqual(result.undeclared, ["evals", "workspace"])

    def test_other_tables_are_not_validated(self):
        self.conventions(VALID + '\n[docs]\nanything = 1\n')
        self.assertEqual(self.read().status, "ok")

    def test_an_unknown_tool_is_an_error(self):
        self.conventions(VALID)
        result = self.read("rodmap")
        self.assertEqual(result.status, "error")
        self.assertIn("did you mean roadmap?", result.problems[0])


class Validation(Case):
    def test_a_toml_error_gives_its_line(self):
        problems = self.problems('language = "english"\nversioning = git\n')
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith("line 2: TOML error: "), problems)

    def test_an_unknown_key_gives_its_line_and_a_suggestion(self):
        problems = self.problems(VALID.replace('root = "docs/roadmap"', 'roots = "docs/roadmap"'))
        self.assertIn("line 6: [roadmap] roots is not a key of [roadmap]; did you mean root?", problems)

    def test_an_unknown_shared_key(self):
        problems = self.problems("langage = \"english\"\n" + VALID)
        self.assertIn("line 1: langage is not a shared key; did you mean language?", problems)

    def test_a_wrong_type(self):
        problems = self.problems(VALID.replace('root = "docs/roadmap"', "root = 3"))
        self.assertIn("line 6: [roadmap] root must be a string, got an integer", problems)

    def test_a_value_outside_its_allowed_set(self):
        problems = self.problems(VALID.replace('versioning = "git"', 'versioning = "svn"'))
        self.assertIn('line 2: versioning = "svn" is not one of "git", "none"', problems)

    def test_an_excluded_feature_outside_its_allowed_set(self):
        problems = self.problems(VALID + 'exclude = ["hooks"]\n', tool="skills")
        self.assertIn('line 10: [skills] exclude = "hooks" is not one of '
                      '"allowed-tools", "dynamic-context", "substitutions"', problems)

    def test_a_check_table_with_an_unknown_field(self):
        problems = self.problems(VALID.replace('["make check"]', '[{ cmd = "make" }]'))
        self.assertIn('line 3: checks must hold strings or { run, dir } tables', problems)

    def test_a_path_outside_the_root(self):
        for path in ("/abs/roadmap", "../roadmap", "docs/../../x"):
            with self.subTest(path=path):
                problems = self.problems(VALID.replace('"docs/roadmap"', f'"{path}"'))
                self.assertIn(f'line 6: [roadmap] root = "{path}" must be relative to the root, without ".."',
                              problems)

    def test_roadmaps_have_no_sub_roadmaps_and_no_parent(self):
        # Every roadmap lives under root; a dependency between roadmaps is a Blocked By link.
        for key in ("sub_roadmaps", "parent"):
            with self.subTest(key=key):
                problems = self.problems(VALID.replace('root = "docs/roadmap"', f'root = "docs/roadmap"\n{key} = "x"'))
                self.assertTrue(any(p.startswith(f"line 7: [roadmap] {key} is not a key of [roadmap]") for p in problems),
                                problems)

    def test_a_missing_required_key(self):
        problems = self.problems(VALID.replace('language   = "english"\n', ""))
        self.assertIn("[roadmap] language is missing: declare it at the top or in [roadmap]", problems)

    def test_a_missing_table_suggests_a_close_name(self):
        problems = self.problems(VALID.replace("[roadmap]", "[roadmaps]"))
        self.assertIn("no [roadmap] table; found [roadmaps], did you mean [roadmap]?", problems)

    def test_residue_is_required_with_versioning_none(self):
        problems = self.problems(VALID.replace('"git"', '"none"'))
        self.assertIn('residue is required with versioning = "none"', problems)

    def test_residue_is_refused_with_versioning_git(self):
        problems = self.problems('residue = ["x"]\n' + VALID)
        self.assertIn('line 1: residue is only used with versioning = "none"', problems)

    def test_every_problem_is_reported(self):
        problems = self.problems(VALID.replace('"git"', '"svn"').replace('root = "docs/roadmap"', "root = 3"))
        self.assertEqual(len(problems), 2, problems)


class Output(Case):
    def test_ok_prints_the_status_then_the_resolved_table(self):
        self.conventions(VALID)
        self.assertEqual(conventions.render(self.read()), "\n".join([
            "status: ok",
            f"root: {self.repo}",
            f"file: {self.repo / '.agent-conventions.toml'}",
            "[roadmap]",
            'language = "english"',
            'versioning = "git"',
            'checks = [{ run = "make check", dir = "." }]',
            'root = "docs/roadmap"',
        ]))

    def test_invalid_prints_one_problem_per_line(self):
        self.conventions(VALID.replace('"git"', '"svn"'))
        lines = conventions.render(self.read()).splitlines()
        self.assertEqual(lines[0], "status: invalid")
        self.assertEqual(lines[3], 'problem: line 2: versioning = "svn" is not one of "git", "none"')

    def test_no_root_prints_the_status_alone(self):
        self.assertEqual(conventions.render(self.read(start=self.tmp / "x")), "status: no-root")


class Command(Case):
    def run_script(self, *args, cwd=None):
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.personal))
        return subprocess.run([str(SCRIPT), *args], capture_output=True, text=True, cwd=cwd or self.repo, env=env)

    def test_it_runs_by_its_path_and_reads_from_the_working_directory(self):
        self.conventions(VALID)
        result = self.run_script("roadmap")
        self.assertEqual((result.returncode, result.stdout.splitlines()[0]), (0, "status: ok"))

    def test_from_sets_the_starting_path(self):
        self.conventions(VALID)
        result = self.run_script("roadmap", "--from", str(self.repo / "docs"), cwd=self.tmp)
        self.assertEqual(result.stdout.splitlines()[:2], ["status: ok", f"root: {self.repo}"])

    def test_the_personal_directory_comes_from_claude_config_dir(self):
        write(self.personal / ".agent-conventions.toml", VALID)
        result = self.run_script("skills", cwd=self.personal)
        self.assertEqual(result.stdout.splitlines()[:2], ["status: ok", f"root: {self.personal}"])

    def test_it_exits_0_on_every_status(self):
        self.conventions("broken = [")
        for args, cwd in ((["roadmap"], None), (["nothing"], None), ([], None), (["roadmap"], self.tmp)):
            with self.subTest(args=args):
                result = self.run_script(*args, cwd=cwd)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.startswith("status: "), result.stdout)

    def test_an_unexpected_error_still_exits_0(self):
        self.conventions(VALID)
        (self.repo / ".agent-conventions.toml").chmod(0)
        try:
            result = self.run_script("roadmap")
        finally:
            (self.repo / ".agent-conventions.toml").chmod(0o644)
        if os.geteuid() == 0:
            self.skipTest("root reads any file")
        self.assertEqual((result.returncode, result.stdout.splitlines()[0]), (0, "status: error"))


class Writing(Case):
    def draft(self, text=VALID):
        path = self.tmp / "draft.toml"
        write(path, text)
        return path

    def target(self):
        return self.repo / ".agent-conventions.toml"

    def test_a_valid_draft_is_written_at_the_root_and_read_back(self):
        result = conventions.write("roadmap", self.draft(), start=self.repo / "docs", personal=self.personal)
        self.assertEqual((result.status, result.root), ("ok", self.repo), result.problems)
        self.assertEqual(self.target().read_text(encoding="utf-8"), VALID)

    def test_the_file_is_added_to_a_new_gitignore(self):
        conventions.write("roadmap", self.draft(), start=self.repo, personal=self.personal)
        self.assertEqual((self.repo / ".gitignore").read_text(encoding="utf-8"), "/.agent-conventions.toml\n")

    def test_the_file_is_appended_to_an_existing_gitignore(self):
        write(self.repo / ".gitignore", "build/")
        conventions.write("roadmap", self.draft(), start=self.repo, personal=self.personal)
        self.assertEqual((self.repo / ".gitignore").read_text(encoding="utf-8"), "build/\n/.agent-conventions.toml\n")

    def test_a_gitignore_that_lists_the_file_is_left_alone(self):
        for listed in ("/.agent-conventions.toml\n", ".agent-conventions.toml\n"):
            with self.subTest(listed=listed):
                write(self.repo / ".gitignore", listed)
                self.target().unlink(missing_ok=True)
                conventions.write("roadmap", self.draft(), start=self.repo, personal=self.personal)
                self.assertEqual((self.repo / ".gitignore").read_text(encoding="utf-8"), listed)

    def test_no_gitignore_outside_git(self):
        project = self.tmp / "nogit"
        project.mkdir()
        result = conventions.write("roadmap", self.draft(), root=project, personal=self.personal)
        self.assertEqual(result.status, "ok", result.problems)
        self.assertFalse((project / ".gitignore").exists())

    def test_an_invalid_draft_is_refused_with_the_reader_messages(self):
        result = conventions.write("roadmap", self.draft(VALID.replace('"git"', '"svn"')),
                                   start=self.repo, personal=self.personal)
        self.assertEqual(result.problems, ['line 2: versioning = "svn" is not one of "git", "none"'])
        self.assertEqual(result.status, "invalid")
        self.assertFalse(self.target().exists())
        self.assertFalse((self.repo / ".gitignore").exists())

    def test_an_existing_file_is_never_overwritten(self):
        self.conventions("# mine\n")
        result = conventions.write("roadmap", self.draft(), start=self.repo, personal=self.personal)
        self.assertEqual(result.status, "error")
        self.assertIn("already exists", result.problems[0])
        self.assertEqual(self.target().read_text(encoding="utf-8"), "# mine\n")

    def test_without_a_root_nothing_is_written(self):
        result = conventions.write("roadmap", self.draft(), start=self.tmp / "loose", personal=self.personal)
        self.assertEqual(result.status, "no-root")

    def test_the_command_writes_and_reports(self):
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.personal))
        draft = self.draft()
        result = subprocess.run([str(SCRIPT), "roadmap", "--write", str(draft)],
                                capture_output=True, text=True, cwd=self.repo, env=env)
        lines = result.stdout.splitlines()
        self.assertEqual((result.returncode, lines[0]), (0, "status: ok"))
        self.assertIn(f"written: {self.target()}", lines)
        self.assertIn(f"gitignored in: {self.repo / '.gitignore'}", lines)

    def test_the_command_takes_an_explicit_root(self):
        project = self.tmp / "nogit"
        project.mkdir()
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.personal))
        result = subprocess.run([str(SCRIPT), "roadmap", "--write", str(self.draft()), "--root", str(project)],
                                capture_output=True, text=True, cwd=self.tmp, env=env)
        self.assertEqual(result.stdout.splitlines()[:2], ["status: ok", f"root: {project}"])


class Procedure(unittest.TestCase):
    """conventions.md, the procedure skills follow, names everything the reader knows."""

    TEXT = (SCRIPT.parent / "conventions.md").read_text(encoding="utf-8")

    def test_every_key_is_documented(self):
        keys = set(conventions.SHARED) | {k for spec in conventions.TOOLS.values() for k in spec["keys"]}
        for key in sorted(keys):
            with self.subTest(key=key):
                self.assertIn(f"| `{key}` |", self.TEXT)

    def test_every_allowed_value_is_documented(self):
        specs = list(conventions.SHARED.values()) + [s for t in conventions.TOOLS.values() for s in t["keys"].values()]
        for value in sorted({v for _, allowed in specs for v in allowed or ()}):
            with self.subTest(value=value):
                self.assertIn(f'"{value}"', self.TEXT)

    def test_every_status_is_documented(self):
        for status in ("ok", "missing", "invalid", "no-root", "error"):
            with self.subTest(status=status):
                self.assertIn(f"| `{status}` |", self.TEXT)


if __name__ == "__main__":
    unittest.main()
