"""Tests for fixtures.py and grade.py, the parts of the roadmap evals that the authoring-skills
eval scripts run: workspace.py builds each case with fixtures.py, grade.py decides its
assertions from what run.py left in each run's folder."""

import json
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent
CASES = {c["name"]: c for c in json.loads((EVALS / "evals.json").read_text(encoding="utf-8"))["evals"]}
ON = "docs/roadmap/on-progress/search-index"
DONE = "docs/roadmap/completed/search-index"


def build(case, folder):
    return subprocess.run([sys.executable, "-B", str(EVALS / "fixtures.py"), case, str(folder)],
                          capture_output=True, text=True)


def files_of(folder):
    return {p.relative_to(folder).as_posix(): p.read_text(encoding="utf-8") for p in folder.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(folder).parts}


class Fixtures(unittest.TestCase):
    def test_every_case_builds_a_fixture_whose_contract_git_tracks(self):
        for name, case in CASES.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(case["setup"], "fixture")
                self.assertEqual(build(name, Path(tmp)).returncode, 0)
                tracked = subprocess.run(["git", "ls-files"], cwd=tmp, capture_output=True, text=True).stdout.split()
                self.assertIn(".agent-conventions.toml", tracked)
                self.assertIn("CLAUDE.md", tracked)

    def test_an_unknown_case_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = build("no-such-case", Path(tmp))
        self.assertEqual(done.returncode, 1)
        self.assertIn("no-such-case", done.stderr)


class Grade(unittest.TestCase):
    """An iteration of one run per case, as authoring-skills' run.py leaves it."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.iteration = self.tmp / "iteration-1"
        self.iteration.mkdir()
        self.cases = []

    def prepare(self, name, status="complete"):
        """The run's folder and the fixture's files, by path."""
        fixture = self.tmp / f"fixture-{name}"
        fixture.mkdir()
        self.assertEqual(build(name, fixture).returncode, 0)
        case = self.iteration / name
        case.mkdir()
        with tarfile.open(case / "fixture.tar", "w") as tar:
            for child in sorted(fixture.iterdir()):
                tar.add(child, arcname=child.name)
        metadata = {"name": name, "assertions": CASES[name]["assertions"]}
        (case / "eval_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        run = case / "with_skill" / "run-1"
        run.mkdir(parents=True)
        (run / "run.json").write_text(json.dumps({"status": status}), encoding="utf-8")
        self.cases.append(name)
        (self.iteration / "iteration.json").write_text(json.dumps(
            {"cases": self.cases, "configurations": ["with_skill"], "runs": 1}), encoding="utf-8")
        return run, files_of(fixture)

    def finish(self, run, before, after, response="Done."):
        """outputs/, changes.json and response.md for a run whose final tree is after."""
        changes = {"added": sorted(set(after) - set(before)), "deleted": sorted(set(before) - set(after)),
                   "modified": sorted(p for p in set(after) & set(before) if after[p] != before[p])}
        for path in changes["added"] + changes["modified"]:
            target = run / "outputs" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(after[path], encoding="utf-8")
        (run / "changes.json").write_text(json.dumps(changes), encoding="utf-8")
        (run / "response.md").write_text(response, encoding="utf-8")

    def grade(self):
        done = subprocess.run([sys.executable, "-B", str(EVALS / "grade.py"), str(self.iteration)],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def results(self, run):
        grading = json.loads((run / "grading.json").read_text(encoding="utf-8"))
        return {a["text"]: a["passed"] for a in grading["assertions"]}

    def test_a_run_that_closed_the_roadmap_passes_every_assertion(self):
        run, before = self.prepare("close-whole-roadmap")
        after = {p: t for p, t in before.items() if not p.startswith(ON + "/")}
        for path, text in before.items():
            if path.startswith(ON + "/"):
                after[DONE + path[len(ON):]] = text
        readme = after[f"{DONE}/README.md"]
        for name, value in [("Current Phase", "—"), ("Blocked By", "—"), ("Next Milestone", "—"),
                            ("Roadmap Status", "🟢 Done"), ("Version", "2.0.0"), ("Location", f"`{DONE}/`")]:
            readme = re.sub(rf"^\*\*{name}:\*\*.*$", f"**{name}:** {value}", readme, flags=re.M)
        after[f"{DONE}/README.md"] = readme
        after[f"{DONE}/summary.md"] = "# Summary\n\n## What We Learned\n\nBatching.\n"
        self.finish(run, before, after)
        self.grade()
        results = self.results(run)
        self.assertEqual(list(results), CASES["close-whole-roadmap"]["assertions"])
        self.assertTrue(all(results.values()), results)

    def test_a_run_that_changed_nothing_has_not_moved_the_roadmap(self):
        run, before = self.prepare("close-whole-roadmap")
        self.finish(run, before, before)
        self.grade()
        self.assertFalse(self.results(run)["Roadmap folder moved to docs/roadmap/completed/search-index/"])

    def test_a_run_that_stopped_on_the_missing_key_passes(self):
        run, before = self.prepare("create-with-incomplete-contract")
        self.finish(run, before, before, "The contract has no `versioning` key: I stop here.")
        self.grade()
        self.assertEqual(self.results(run), dict.fromkeys(CASES["create-with-incomplete-contract"]["assertions"], True))

    def test_a_contract_the_run_completed_is_not_left_unchanged(self):
        run, before = self.prepare("create-with-incomplete-contract")
        after = dict(before, **{".agent-conventions.toml": before[".agent-conventions.toml"] + 'versioning = "git"\n'})
        self.finish(run, before, after, "I set versioning to git.")
        self.grade()
        self.assertFalse(self.results(run)["Contract left unchanged pending the answer"])

    def test_the_closed_phase_is_read_from_the_run_and_its_untouched_files_from_the_fixture(self):
        run, before = self.prepare("close-phase-uncommitted-work")
        after = dict(before)
        after[f"{ON}/phase-1-tokenizer.md"] = before[f"{ON}/phase-1-tokenizer.md"].replace(
            "🟡 In Progress (0% — 0/4)", "🟢 Done (100% — 4/4)")
        self.finish(run, before, after)
        self.grade()
        results = self.results(run)
        self.assertTrue(results["Phase 1 file marked done at (100% — 4/4)"])
        self.assertFalse(results["Report has a written Assessment"])
        self.assertTrue(results["No template comment copied into roadmap documents"])

    def test_a_run_not_complete_gets_no_grading(self):
        run, before = self.prepare("close-whole-roadmap", status="stopped")
        self.grade()
        self.assertFalse((run / "grading.json").exists())


if __name__ == "__main__":
    unittest.main()
