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

    def test_the_hooked_fixture_holds_a_domain_whose_hook_names_the_open_notes(self):
        self.assertEqual(self.build("evaluate-a-hooked-skill").returncode, 0)
        domain = self.folder / "domains/notes"
        self.assertEqual(len(git(self.folder, "log", "--format=%H").split()), 2)
        self.assertEqual(git(self.folder, "diff", "--name-only", "HEAD~1", "HEAD").split(),
                         ["domains/notes/skills/writing-notes/SKILL.md"])
        self.assertNotIn("open note", git(self.folder, "show", "HEAD~1:domains/notes/skills/writing-notes/SKILL.md"))
        self.assertIn("open note", (domain / "skills/writing-notes/SKILL.md").read_text(encoding="utf-8"))
        self.assertFalse((domain / "skills/writing-notes/evals").exists())
        self.assertEqual(workspace.hook_problems(Path("domains/notes/hooks.json"), self.folder), [])
        groups = json.loads((domain / "hooks.json").read_text(encoding="utf-8"))["SessionStart"]
        command = groups[0]["hooks"][0]["command"].replace("{{HOOKS_DIR}}", str(domain / "hooks"))
        work = Path(self.tmp.name) / "work"
        (work / "notes").mkdir(parents=True)

        def start():
            done = subprocess.run(command, shell=True, capture_output=True, text=True, check=True,
                                  input=json.dumps({"hook_event_name": "SessionStart", "cwd": str(work)}))
            return done.stdout

        self.assertEqual(start(), "")
        (work / "notes/2026-10-12-pricing-review.md").write_text("---\nstatus: draft\n---\n\n# Pricing review\n",
                                                                 encoding="utf-8")
        (work / "notes/2026-10-01-hiring.md").write_text("---\nstatus: done\n---\n\n# Hiring\n", encoding="utf-8")
        context = json.loads(start())["hookSpecificOutput"]["additionalContext"]
        self.assertIn("notes/2026-10-12-pricing-review.md", context)
        self.assertNotIn("hiring", context)
        self.assertEqual(git(self.folder, "status", "--porcelain"), "")

    def test_the_later_step_fixture_holds_a_recorded_run_of_the_earlier_one(self):
        self.assertEqual(self.build("evaluate-a-later-step").returncode, 0)
        skill = self.folder / "skills/writing-notes"
        self.assertEqual(len(git(self.folder, "log", "--format=%H").split()), 2)
        self.assertEqual(git(self.folder, "diff", "--name-only", "HEAD~1", "HEAD").split(),
                         ["skills/writing-notes/SKILL.md"])
        self.assertNotIn("Closing", git(self.folder, "show", "HEAD~1:skills/writing-notes/SKILL.md"))
        self.assertIn("## Closing A Note", (skill / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual([case["name"] for case in workspace.load(skill)["evals"]], ["decision-note", "nothing-follows"])
        run = self.folder / ".eval-runs/skills/writing-notes/iteration-1/decision-note/with_skill/run-1"
        (added,) = json.loads((run / "changes.json").read_text(encoding="utf-8"))["added"]
        note = (run / "outputs" / added).read_text(encoding="utf-8")
        self.assertTrue(note.startswith("---\nstatus: draft\n---\n"))
        self.assertIn("## Next", note)
        self.assertIn("Alice", note.split("## Next")[1])
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
