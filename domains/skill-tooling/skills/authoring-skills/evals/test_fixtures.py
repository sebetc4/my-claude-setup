"""Unit tests for evals/fixtures.py, which builds the folder a fixture case of these evals
starts in, as scripts/workspace.py runs it: fixtures.py <case> <folder>."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SCRIPTS = EVALS.parent / "scripts"
SAMPLE = (EVALS / "sample/skill.md").read_text(encoding="utf-8")
RESULTS = EVALS / "evaluate/results"


def load(name, path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workspace = load("fixtures_workspace", SCRIPTS / "workspace.py")
benchmark = load("fixtures_benchmark", SCRIPTS / "benchmark.py")


def git(folder, *args):
    return subprocess.run(["git", *args], cwd=folder, capture_output=True, text=True, check=True).stdout


class Fixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name) / "fixture"
        self.folder.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, case):
        return subprocess.run([sys.executable, str(EVALS / "fixtures.py"), case, str(self.folder)],
                              capture_output=True, text=True)

    def test_an_unknown_case_is_refused_by_name(self):
        done = self.build("no-such-case")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("no-such-case", done.stderr)

    def test_the_edit_fixture_holds_the_change_in_its_last_commit(self):
        self.assertEqual(self.build("evaluate-an-edit").returncode, 0)
        skill = self.folder / "skills/writing-notes"
        self.assertEqual(len(git(self.folder, "log", "--format=%H").split()), 2)
        before = git(self.folder, "show", "HEAD~1:skills/writing-notes/SKILL.md")
        self.assertNotIn("## Next", before)
        self.assertEqual((skill / "SKILL.md").read_text(encoding="utf-8"), SAMPLE)
        self.assertEqual(git(self.folder, "diff", "--name-only", "HEAD~1", "HEAD").split(),
                         ["skills/writing-notes/SKILL.md"])
        self.assertFalse((skill / "evals").exists())
        self.assertIn("[skills]", (self.folder / ".agent-conventions.toml").read_text(encoding="utf-8"))
        self.assertEqual(git(self.folder, "status", "--porcelain"), "")

    def test_the_results_fixture_holds_a_graded_iteration_and_a_trigger_eval(self):
        self.assertEqual(self.build("read-the-results").returncode, 0)
        skill = self.folder / "skills/writing-notes"
        evals = workspace.load(skill)
        found = self.folder / ".eval-runs/skills/writing-notes"
        triggers = json.loads(next((found / "triggers").glob("*.json")).read_text(encoding="utf-8"))
        asked = [{k: q[k] for k in ("query", "should_trigger", "near") if k in q} for q in triggers["queries"]]
        self.assertEqual(evals["triggers"], asked)
        iteration = found / "iteration-1"
        recorded = json.loads((iteration / "iteration.json").read_text(encoding="utf-8"))
        kept = json.loads((iteration / "benchmark.json").read_text(encoding="utf-8"))
        again = benchmark.compute(iteration, recorded)
        for key in ("summary", "delta", "by_case", "assertions", "left_out", "cost_usd", "notes"):
            self.assertEqual(again[key], kept[key], key)
        self.assertEqual(git(self.folder, "status", "--porcelain"), "")

    def test_the_trigger_eval_summary_agrees_with_its_queries(self):
        data = json.loads(next((RESULTS / "triggers").glob("*.json")).read_text(encoding="utf-8"))
        queries = data["queries"]
        for query in queries:
            counted = [s for s in query["sessions"] if s["counted"]]
            self.assertEqual(query["counted"], len(counted))
            self.assertEqual(query["triggered"], sum(1 for s in counted if s["triggered"]))
        self.assertEqual(data["summary"]["passed"], sum(1 for q in queries if q["passed"]))
        self.assertEqual(data["summary"]["failed"], sum(1 for q in queries if q["passed"] is False))


if __name__ == "__main__":
    unittest.main()
