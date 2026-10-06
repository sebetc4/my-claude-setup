"""Tests for workspace.py: an iteration of a skill's evals prepared under the repository's
[skills] workspace, per the design of Phase 4 of roadmap skill-tooling."""

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills/authoring-skills/scripts"
_spec = importlib.util.spec_from_file_location("skill_workspace", SCRIPTS / "workspace.py")
workspace = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(workspace)

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
FIXTURES = """#!/usr/bin/env python3
import sys
from pathlib import Path
folder = Path(sys.argv[2])
(folder / "built-for.txt").write_text(sys.argv[1], encoding="utf-8")
"""


def case(**fields):
    return {"id": 1, "name": "first-case", "kind": "task", "setup": "empty", "prompt": "Do the thing.",
            "expected_output": "The thing, done.", "assertions": ["The thing is done"], **fields}


class Case(unittest.TestCase):
    """A git repository holding the skill demo, its evals and files around it."""

    def setUp(self):
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve() / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\nignored.txt\n")
        self.write("README.md", "The repository.\n")
        self.write("ignored.txt", "never copied\n")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: Old.\n---\n\nOld body.\n")
        self.write("skills/demo/scripts/tool.py", "#!/usr/bin/env python3\n", mode=0o755)
        self.write("skills/demo/evals/files/input.txt", "input\n")
        self.evals(case())
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "first")
        self.first = self.git("rev-parse", "HEAD")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: New.\n---\n\nNew body.\n")
        self.write("notes.txt", "untracked, not ignored\n")

    def write(self, path, text, mode=None):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        if mode:
            target.chmod(mode)
        return target

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
                              env=GIT_ENV).stdout.strip()

    def evals(self, *cases, **top):
        data = {"skill_name": "demo", "evals": list(cases), **top}
        self.write("skills/demo/evals/evals.json", json.dumps(data, indent=2))

    def prepare(self, **options):
        return workspace.prepare(self.skill, **options)

    def refused(self, *expected, **options):
        before = sorted((self.repo / ".eval-runs").rglob("*"))
        with self.assertRaises(workspace.Refused) as caught:
            self.prepare(**options)
        text = "\n".join(caught.exception.problems)
        for part in expected:
            self.assertIn(part, text)
        self.assertEqual(sorted((self.repo / ".eval-runs").rglob("*")), before,
                         "a refused preparation wrote into the workspace")
        return caught.exception.problems

    def json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))


class Layout(Case):
    def test_the_iteration_lies_under_the_skill_folder_of_the_workspace(self):
        iteration = self.prepare()
        self.assertEqual(iteration, self.repo / ".eval-runs/skills/demo/iteration-1")
        self.assertEqual(self.prepare(), self.repo / ".eval-runs/skills/demo/iteration-2")

    def test_one_folder_per_case_configuration_and_run(self):
        self.evals(case(), case(id=2, name="second-case"))
        iteration = self.prepare(runs=2)
        for name in ("first-case", "second-case"):
            for configuration in ("with_skill", "without_skill"):
                runs = sorted(p.name for p in (iteration / name / configuration).iterdir())
                self.assertEqual(runs, ["run-1", "run-2"])

    def test_iteration_json_records_the_conditions(self):
        iteration = self.prepare(runs=2, model="claude-opus-5-5", effort="max", budget=3.0)
        recorded = self.json(iteration / "iteration.json")
        self.assertEqual(recorded["skill_name"], "demo")
        self.assertEqual(recorded["root"], str(self.repo))
        self.assertEqual(recorded["cases"], ["first-case"])
        self.assertEqual(recorded["configurations"], ["with_skill", "without_skill"])
        self.assertEqual((recorded["runs"], recorded["model"], recorded["effort"], recorded["budget_usd"]),
                         (2, "claude-opus-5-5", "max", 3.0))
        self.assertIsNone(recorded["baseline"])

    def test_the_defaults_are_the_designs(self):
        recorded = self.json(self.prepare() / "iteration.json")
        self.assertEqual((recorded["runs"], recorded["model"], recorded["effort"], recorded["budget_usd"]),
                         (3, "claude-sonnet-5-5", "xhigh", 5.0))

    def test_eval_metadata_holds_the_case(self):
        self.evals(case(review=["The tone suits a user"], pressures=["urgency"], kind="discipline"))
        metadata = self.json(self.prepare() / "first-case/eval_metadata.json")
        for key, value in (("id", 1), ("name", "first-case"), ("kind", "discipline"), ("setup", "empty"),
                           ("prompt", "Do the thing."), ("expected_output", "The thing, done."),
                           ("assertions", ["The thing is done"]), ("review", ["The tone suits a user"]),
                           ("pressures", ["urgency"]), ("files", []), ("exclude", [])):
            self.assertEqual(metadata[key], value, key)
        self.assertIn("digest", metadata)

    def test_only_the_cases_named(self):
        self.evals(case(), case(id=2, name="second-case"))
        iteration = self.prepare(cases=["second-case"])
        self.assertFalse((iteration / "first-case").exists())
        self.assertEqual(self.json(iteration / "iteration.json")["cases"], ["second-case"])
        self.refused("no case named `third-case`", cases=["third-case"])


class Copies(Case):
    def test_the_skill_is_copied_without_its_evals(self):
        copy = self.prepare() / "with_skill/demo"
        self.assertIn("New body.", (copy / "SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue((copy / "scripts/tool.py").stat().st_mode & 0o100, "the copy lost the executable bit")
        self.assertFalse((copy / "evals").exists())

    def test_caches_are_left_out(self):
        self.write("skills/demo/scripts/__pycache__/tool.cpython-314.pyc", "")
        self.assertFalse((self.prepare() / "with_skill/demo/scripts/__pycache__").exists())

    def test_a_new_skill_has_no_snapshot(self):
        iteration = self.prepare()
        self.assertFalse((iteration / "old_skill").exists())
        self.assertFalse((iteration / "without_skill").exists())

    def test_the_snapshot_of_a_git_revision(self):
        iteration = self.prepare(baseline=self.first[:7])
        snapshot = iteration / "old_skill/demo"
        self.assertIn("Old body.", (snapshot / "SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue((snapshot / "scripts/tool.py").stat().st_mode & 0o100)
        self.assertFalse((snapshot / "evals").exists())
        recorded = self.json(iteration / "iteration.json")
        self.assertEqual(recorded["configurations"], ["with_skill", "old_skill"])
        self.assertEqual(recorded["baseline"], {"revision": self.first[:7], "commit": self.first})
        self.assertTrue((iteration / "first-case/old_skill/run-1").is_dir())

    def test_the_snapshot_of_a_folder(self):
        old = self.repo.parent / "old-demo"
        (old / "evals").mkdir(parents=True)
        (old / "SKILL.md").write_text("Folder body.\n", encoding="utf-8")
        (old / "evals/evals.json").write_text("{}", encoding="utf-8")
        iteration = self.prepare(baseline=str(old))
        snapshot = iteration / "old_skill/demo"
        self.assertEqual((snapshot / "SKILL.md").read_text(encoding="utf-8"), "Folder body.\n")
        self.assertFalse((snapshot / "evals").exists())
        self.assertEqual(self.json(iteration / "iteration.json")["baseline"], {"folder": str(old)})

    def test_a_revision_without_the_skill_is_refused(self):
        tree = self.git("hash-object", "-t", "tree", "/dev/null")
        empty = self.git("commit-tree", tree, "-m", "nothing")
        self.refused("holds no `skills/demo`", baseline=empty)

    def test_an_unknown_revision_is_refused(self):
        self.refused("neither a folder nor a git revision", baseline="no-such-revision")

    def test_the_baseline_alone_while_the_skill_is_not_written(self):
        (self.skill / "SKILL.md").unlink()
        self.refused("no `SKILL.md`", "--baseline-only")
        iteration = self.prepare(baseline_only=True)
        self.assertEqual(self.json(iteration / "iteration.json")["configurations"], ["without_skill"])
        self.assertFalse((iteration / "with_skill").exists())
        self.assertTrue((iteration / "first-case/without_skill/run-1").is_dir())
        self.assertFalse((iteration / "first-case/with_skill").exists())


class Inputs(Case):
    def members(self, archive):
        with tarfile.open(archive) as tar:
            return {m.name for m in tar.getmembers() if not m.isdir()}

    def test_no_base_without_a_repository_case(self):
        self.assertFalse((self.prepare() / "base.tar").exists())

    def test_the_base_holds_the_repository_without_the_skill(self):
        self.evals(case(setup="repository"))
        iteration = self.prepare()
        members = self.members(iteration / "base.tar")
        self.assertIn("README.md", members)
        self.assertIn("notes.txt", members, "an untracked file git does not ignore is left out")
        self.assertIn(".agent-conventions.toml", members)
        self.assertIn(".gitignore", members)
        self.assertNotIn("ignored.txt", members)
        self.assertFalse([m for m in members if m.startswith("skills/demo")], "the skill reached the base")
        self.assertFalse([m for m in members if m.startswith(".eval-runs") or m.startswith(".git/")])
        recorded = self.json(iteration / "iteration.json")
        self.assertEqual(recorded["skill_path"], "skills/demo")
        self.assertTrue(recorded["base_digest"])

    def test_the_base_digest_ignores_the_skill(self):
        self.evals(case(setup="repository"))
        first = self.json(self.prepare() / "iteration.json")["base_digest"]
        self.write("skills/demo/SKILL.md", "Changed again.\n")
        self.assertEqual(self.json(self.prepare() / "iteration.json")["base_digest"], first)
        self.write("README.md", "Changed.\n")
        self.assertNotEqual(self.json(self.prepare() / "iteration.json")["base_digest"], first)

    def test_a_repository_case_needs_git(self):
        self.evals(case(setup="repository"))
        subprocess.run(["rm", "-rf", str(self.repo / ".git")], check=True)
        self.refused("needs a git repository")

    def test_the_case_files_are_copied_at_their_path_in_the_evals(self):
        self.write("skills/demo/assets/table.txt", "table\n")
        self.evals(case(files=["evals/files/input.txt", "assets/table.txt"]))
        files = self.prepare() / "first-case/files"
        self.assertEqual((files / "files/input.txt").read_text(encoding="utf-8"), "input\n")
        self.assertEqual((files / "assets/table.txt").read_text(encoding="utf-8"), "table\n")
        self.assertFalse((files / "evals").exists())

    def test_the_fixture_is_built_once(self):
        self.write("skills/demo/evals/fixtures.py", FIXTURES, mode=0o755)
        self.evals(case(setup="fixture"))
        iteration = self.prepare()
        with tarfile.open(iteration / "first-case/fixture.tar") as tar:
            built = tar.extractfile("built-for.txt").read().decode()
        self.assertEqual(built, "first-case")

    def test_a_failing_fixture_stops_the_preparation(self):
        self.write("skills/demo/evals/fixtures.py", "#!/usr/bin/env python3\nimport sys\nsys.exit('no such fixture')\n",
                   mode=0o755)
        self.evals(case(setup="fixture"))
        with self.assertRaises(workspace.Refused) as caught:
            self.prepare()
        self.assertIn("no such fixture", "\n".join(caught.exception.problems))

    def test_the_digest_follows_what_a_run_receives(self):
        digest = self.json(self.prepare() / "first-case/eval_metadata.json")["digest"]
        self.evals(case(assertions=["Another check"], review=["Another look"]))
        self.assertEqual(self.json(self.prepare() / "first-case/eval_metadata.json")["digest"], digest)
        self.evals(case(prompt="Do another thing."))
        self.assertNotEqual(self.json(self.prepare() / "first-case/eval_metadata.json")["digest"], digest)


class Reuse(Case):
    def finish(self, iteration, configuration="without_skill"):
        for run in (iteration / "first-case" / configuration).iterdir():
            (run / "run.json").write_text('{"status": "complete"}', encoding="utf-8")
            (run / "grading.json").write_text("{}", encoding="utf-8")

    def test_the_baseline_runs_are_taken_again(self):
        previous = self.prepare()
        self.finish(previous)
        self.finish(previous, "with_skill")
        iteration = self.prepare(reuse="iteration-1")
        run = iteration / "first-case/without_skill/run-1"
        self.assertTrue((run / "run.json").is_file())
        self.assertFalse((run / "grading.json").exists(), "a reused run keeps its old grades")
        self.assertFalse((iteration / "first-case/with_skill/run-1/run.json").exists())
        self.assertEqual(self.json(iteration / "iteration.json")["reused"], {"first-case": "iteration-1"})

    def test_a_changed_case_is_run_again(self):
        self.finish(self.prepare())
        self.evals(case(prompt="Do another thing."))
        iteration = self.prepare(reuse="iteration-1")
        self.assertFalse((iteration / "first-case/without_skill/run-1/run.json").exists())
        self.assertEqual(self.json(iteration / "iteration.json")["reused"], {})

    def test_other_conditions_are_run_again(self):
        self.finish(self.prepare())
        iteration = self.prepare(reuse="iteration-1", effort="max")
        self.assertFalse((iteration / "first-case/without_skill/run-1/run.json").exists())

    def test_an_unknown_iteration_is_refused(self):
        self.prepare()
        self.refused("no iteration `iteration-7`", reuse="iteration-7")


class Validation(Case):
    def test_an_unknown_key_is_named(self):
        self.evals(case(expectations=["x"]))
        self.refused("evals[0]: unknown key `expectations`")

    def test_a_wrong_type_is_named(self):
        self.evals(case(assertions="one"))
        self.refused("evals[0].assertions: expected a list of strings")

    def test_a_value_outside_its_set_is_named(self):
        self.evals(case(kind="howto"))
        self.refused("evals[0].kind: expected one of reference, task, discipline")

    def test_a_missing_key_is_named(self):
        broken = case()
        del broken["setup"]
        self.evals(broken)
        self.refused("evals[0]: missing key `setup`")

    def test_the_top_level(self):
        self.evals(case(), extra=1)
        self.refused("unknown key `extra`")
        self.evals(case(), env={"CLAUDE_DIR": 3})
        self.refused("env.CLAUDE_DIR: expected a string")
        self.evals(case(), triggers=[{"query": "q", "should_trigger": "yes"}])
        self.refused("triggers[0].should_trigger: expected a boolean")

    def test_the_skill_name_matches_the_folder(self):
        self.write("skills/demo/evals/evals.json", json.dumps({"skill_name": "other", "evals": [case()]}))
        self.refused("skill_name: `other` is not the skill's folder name `demo`")

    def test_names_and_ids_are_unique_and_names_are_folders(self):
        self.evals(case(), case())
        self.refused("evals[1].id: 1 is already used", "evals[1].name: `first-case` is already used")
        self.evals(case(name="First case"))
        self.refused("evals[0].name: expected lowercase letters, digits and hyphens")

    def test_setup_specific_keys(self):
        self.evals(case(exclude=["docs/"]))
        self.refused("evals[0].exclude: only a `repository` case excludes paths")
        self.evals(case(setup="fixture"))
        self.refused("evals[0].setup: a `fixture` case needs `evals/fixtures.py`")

    def test_files_lie_inside_the_skill(self):
        self.evals(case(files=["evals/files/missing.txt", "../outside.txt"]))
        self.refused("evals[0].files: `evals/files/missing.txt` does not exist",
                     "evals[0].files: `../outside.txt` lies outside the skill")

    def test_unreadable_evals(self):
        (self.skill / "evals/evals.json").write_text("{", encoding="utf-8")
        self.refused("evals/evals.json is not valid JSON")
        (self.skill / "evals/evals.json").unlink()
        self.refused("no `evals/evals.json`")

    def test_the_workspace_must_be_declared(self):
        self.write(".agent-conventions.toml", '[skills]\ndirs = ["skills"]\n')
        self.refused("`workspace` is not declared in the [skills] table", "references/conventions.md")


class CommandLine(Case):
    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = workspace.main([str(self.skill), *argv])
        return code, out.getvalue(), err.getvalue()

    def test_prints_the_iteration_and_its_runs(self):
        code, out, _ = self.main("--runs", "2")
        self.assertEqual(code, 0)
        self.assertIn(str(self.repo / ".eval-runs/skills/demo/iteration-1"), out)
        self.assertIn("first-case: with_skill 2 runs, without_skill 2 runs", out)

    def test_a_refusal_exits_1_with_each_problem(self):
        self.evals(case(expectations=["x"], kind="howto"))
        code, _, err = self.main()
        self.assertEqual(code, 1)
        self.assertIn("unknown key `expectations`", err)
        self.assertIn("expected one of reference, task, discipline", err)



class Sample(unittest.TestCase):
    """The sample skill the evaluation scripts are checked on, under the skill's evals/sample/."""

    def test_the_sample_builds_validates_and_passes_the_audit(self):
        sample = SCRIPTS.parent / "evals/sample"
        spec = importlib.util.spec_from_file_location("sample_build", sample / "build.py")
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        audit_spec = importlib.util.spec_from_file_location("sample_audit", SCRIPTS / "audit.py")
        audit = importlib.util.module_from_spec(audit_spec)
        audit_spec.loader.exec_module(audit)
        with tempfile.TemporaryDirectory() as tmp:
            skill = build.build(Path(tmp) / "repo")
            self.assertEqual([c["name"] for c in workspace.load(skill)["evals"]], ["decision-note", "nothing-follows"])
            self.assertEqual(audit.audit(skill), [])
            iteration = workspace.prepare(skill, runs=1, cases=["decision-note"])
            self.assertTrue((iteration / "decision-note/with_skill/run-1").is_dir())


if __name__ == "__main__":
    unittest.main()
