"""Tests for benchmark.py: an iteration's graded runs summed up per configuration — pass
rate, duration, tokens and cost with mean, standard deviation, minimum and maximum, the
delta between configurations, the model and effort of each run — with notes computed from
the assertions, per the design of Phase 4 of roadmap skill-tooling."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "skills/authoring-skills/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(f"skill_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


benchmark = load("benchmark")

MODEL, EFFORT = "claude-sonnet-5-5", "xhigh"
CASES = {"alpha": ["The file exists", "The file says yes", "The account names the file"],
         "beta": ["The table has a header", "The table is sorted"]}
T, F = True, False
# (case, configuration, run): (grades, duration in seconds, cost in dollars,
# (input, output, cache read, five-minute write, one-hour write)).
RUNS = {
    ("alpha", "with_skill", 1): ([T, T, T], 10, 0.10, (10, 100, 1000, 0, 500)),
    ("alpha", "with_skill", 2): ([T, F, T], 20, 0.20, (20, 200, 2000, 0, 500)),
    ("beta", "with_skill", 1): ([F, T], 30, 0.30, (30, 300, 3000, 0, 500)),
    ("beta", "with_skill", 2): ([F, T], 40, 0.40, (40, 400, 4000, 0, 500)),
    ("alpha", "without_skill", 1): ([T, F, F], 5, 0.05, (10, 50, 1000, 0, 100)),
    ("alpha", "without_skill", 2): ([T, F, F], 5, 0.05, (10, 50, 1000, 0, 100)),
    ("beta", "without_skill", 1): ([F, F], 5, 0.10, (10, 150, 1000, 0, 100)),
    ("beta", "without_skill", 2): ([F, F], 5, 0.10, (10, 150, 1000, 0, 100)),
}
GRADING_COST = 0.01

# Computed by hand from RUNS: the runs' pass rates are 1, 2/3, 1/2, 1/2 with the skill and
# 1/3, 1/3, 0, 0 without; the standard deviation is the sample's, divided by n - 1.
EXPECTED = {
    "with_skill": {
        "pass_rate": (0.666667, 0.235702, 0.5, 1.0),
        "duration_s": (25.0, 12.909944, 10.0, 40.0),
        "input": (25.0, 12.909944, 10.0, 40.0),
        "cache_read": (2500.0, 1290.994449, 1000.0, 4000.0),
        "cache_write": (500.0, 0.0, 500.0, 500.0),
        "output": (250.0, 129.099445, 100.0, 400.0),
        "cost_usd": (0.25, 0.129099, 0.10, 0.40),
    },
    "without_skill": {
        "pass_rate": (0.166667, 0.192450, 0.0, 0.333333),
        "duration_s": (5.0, 0.0, 5.0, 5.0),
        "input": (10.0, 0.0, 10.0, 10.0),
        "cache_read": (1000.0, 0.0, 1000.0, 1000.0),
        "cache_write": (100.0, 0.0, 100.0, 100.0),
        "output": (100.0, 57.735027, 50.0, 150.0),
        "cost_usd": (0.075, 0.028868, 0.05, 0.10),
    },
}
DELTA = {"pass_rate": 0.5, "duration_s": 20.0, "input": 15.0, "cache_read": 1500.0, "cache_write": 400.0,
         "output": 150.0, "cost_usd": 0.175}


class Case(unittest.TestCase):
    """An iteration as workspace.py, run.py and grade.py leave it, written from RUNS."""

    configurations = ("with_skill", "without_skill")
    runs = 2

    def setUp(self):
        tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.iteration = tmp / ".eval-runs/skills/demo/iteration-1"
        self.iteration.mkdir(parents=True)
        self.write("iteration.json", {
            "skill_name": "demo", "cases": list(CASES), "configurations": list(self.configurations),
            "runs": self.runs, "model": MODEL, "effort": EFFORT, "budget_usd": 1.0})
        for number, (name, assertions) in enumerate(CASES.items(), 1):
            self.write(f"{name}/eval_metadata.json", {"id": number, "name": name, "prompt": "Do it.",
                                                      "assertions": assertions, "review": []})
        for (name, configuration, run), (grades, duration, cost, tokens) in RUNS.items():
            if configuration in self.configurations and run <= self.runs:
                self.complete(name, configuration, run, grades, duration, cost, tokens)

    def write(self, path, data):
        target = self.iteration / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=1), encoding="utf-8")

    def complete(self, name, configuration, run, grades, duration=5, cost=0.1, tokens=(10, 100, 1000, 0, 100),
                 status="complete"):
        folder = f"{name}/{configuration}/run-{run}"
        keys = ("input", "output", "cache_read", "write_5m", "write_1h")
        self.write(f"{folder}/run.json", {
            "case": name, "configuration": configuration, "run": run, "status": status, "reason": None,
            "claude_version": "2.1.292", "model": MODEL, "effort": EFFORT, "duration_s": duration,
            "models": {MODEL: 3}, "efforts": {EFFORT: 3}, "calls": 3, "estimated_calls": 0,
            "tokens": dict(zip(keys, tokens)), "cost_usd": cost, "reported_cost_usd": cost})
        if grades is not None:
            self.grade(name, configuration, run, grades)

    def grade(self, name, configuration, run, grades, weak=()):
        assertions = CASES[name]
        entries = [{"text": text, "passed": passed, "evidence": "seen", "by": "grader"}
                   for text, passed in zip(assertions, grades)]
        passed = sum(e["passed"] for e in entries)
        self.write(f"{name}/{configuration}/run-{run}/grading.json", {
            "assertions": entries,
            "summary": {"passed": passed, "failed": len(entries) - passed, "total": len(entries),
                        "pass_rate": round(passed / len(entries), 2)},
            "weak": [{"text": assertions[n - 1], "reason": reason} for n, reason in weak], "claims": [],
            "grader": {"agent": "skill-grader", "model": MODEL, "effort": EFFORT, "cost_usd": GRADING_COST}})

    def edit_run(self, name, configuration, run, **fields):
        path = self.iteration / f"{name}/{configuration}/run-{run}/run.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(fields)
        path.write_text(json.dumps(data), encoding="utf-8")

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = benchmark.main([str(a) for a in (argv or (self.iteration,))])
        return code, out.getvalue(), err.getvalue()

    def result(self):
        code, _, err = self.main()
        self.assertEqual(code, 0, err)
        return json.loads((self.iteration / "benchmark.json").read_text(encoding="utf-8"))

    def markdown(self):
        return (self.iteration / "benchmark.md").read_text(encoding="utf-8")

    def assertStats(self, stats, mean, stddev, low, high, n=None):
        self.assertAlmostEqual(stats["mean"], mean, places=4)
        if stddev is None:
            self.assertIsNone(stats["stddev"])
        else:
            self.assertAlmostEqual(stats["stddev"], stddev, places=4)
        self.assertAlmostEqual(stats["min"], low, places=4)
        self.assertAlmostEqual(stats["max"], high, places=4)
        if n is not None:
            self.assertEqual(stats["n"], n)

    def notes(self, data, *words):
        return [note for note in data["notes"] if all(word in note for word in words)]


class Summary(Case):
    def test_each_metric_per_configuration(self):
        summary = self.result()["summary"]
        for configuration, metrics in EXPECTED.items():
            self.assertEqual(summary[configuration]["runs"], 4)
            for metric, (mean, stddev, low, high) in metrics.items():
                with self.subTest(configuration=configuration, metric=metric):
                    self.assertStats(summary[configuration][metric], mean, stddev, low, high, n=4)

    def test_the_delta_is_the_first_configuration_less_the_reference(self):
        data = self.result()
        self.assertEqual(data["delta_of"], ["with_skill", "without_skill"])
        for metric, value in DELTA.items():
            with self.subTest(metric=metric):
                self.assertAlmostEqual(data["delta"][metric], value, places=4)

    def test_pass_rate_per_case(self):
        by_case = self.result()["by_case"]
        self.assertStats(by_case["alpha"]["with_skill"], 0.833333, 0.235702, 0.666667, 1.0, n=2)
        self.assertStats(by_case["alpha"]["without_skill"], 0.333333, 0.0, 0.333333, 0.333333, n=2)
        self.assertAlmostEqual(by_case["alpha"]["delta"], 0.5, places=4)
        self.assertStats(by_case["beta"]["with_skill"], 0.5, 0.0, 0.5, 0.5, n=2)
        self.assertAlmostEqual(by_case["beta"]["delta"], 0.5, places=4)

    def test_each_run_with_its_figures(self):
        runs = {(r["case"], r["configuration"], r["run"]): r for r in self.result()["runs"]}
        self.assertEqual(len(runs), 8)
        run = runs[("alpha", "with_skill", 2)]
        self.assertEqual((run["passed"], run["total"]), (2, 3))
        self.assertAlmostEqual(run["pass_rate"], 0.666667, places=4)
        self.assertEqual((run["duration_s"], run["cost_usd"], run["output"], run["cache_write"]), (20, 0.20, 200, 500))
        self.assertEqual(run["estimated_calls"], 0)

    def test_the_cost_of_the_runs_and_of_their_grading(self):
        cost = self.result()["cost_usd"]
        self.assertAlmostEqual(cost["runs"], 1.30, places=4)
        self.assertAlmostEqual(cost["grading"], 8 * GRADING_COST, places=4)

    def test_both_files_written_and_the_summary_printed(self):
        code, out, _ = self.main()
        self.assertEqual(code, 0)
        self.assertTrue((self.iteration / "benchmark.json").is_file())
        text = self.markdown()
        self.assertIn(str(self.iteration / "benchmark.json"), out)
        self.assertIn(text.strip(), out)
        self.assertIn("| Metric | with_skill | without_skill | Delta |", text)
        self.assertIn("| Pass rate | 67% ± 24% (50% to 100%) | 17% ± 19% (0% to 33%) | +50 pts |", text)
        self.assertIn("| Duration | 25.0 s ± 12.9 s (10.0 s to 40.0 s) | 5.0 s ± 0.0 s (5.0 s to 5.0 s) | +20.0 s |",
                      text)
        self.assertIn("| Output | 250 ± 129 (100 to 400) | 100 ± 58 (50 to 150) | +150 |", text)
        self.assertIn("| Cost | $0.250 ± $0.129 ($0.100 to $0.400) | $0.075 ± $0.029 ($0.050 to $0.100) | +$0.175 |",
                      text)
        self.assertIn("| alpha | 83% ± 24% (67% to 100%) | 33% ± 0% (33% to 33%) | +50 pts |", text)
        self.assertIn("| alpha/with_skill/run-2 | 2/3 | 20.0 s | 200 | $0.200 | claude-sonnet-5-5 ×3 | xhigh ×3 |",
                      text)
        for note in self.result()["notes"]:
            self.assertIn(f"- {note}", text)


class ModelAndEffort(Case):
    def test_reported_per_run_and_per_configuration(self):
        data = self.result()
        self.assertEqual((data["model"], data["effort"]), (MODEL, EFFORT))
        run = next(r for r in data["runs"] if r["case"] == "beta" and r["configuration"] == "without_skill")
        self.assertEqual((run["models"], run["efforts"]), ({MODEL: 3}, {EFFORT: 3}))
        self.assertEqual(data["summary"]["with_skill"]["models"], {MODEL: 12})
        self.assertEqual(data["summary"]["with_skill"]["efforts"], {EFFORT: 12})

    def test_a_call_on_another_model_or_effort_is_noted(self):
        self.edit_run("alpha", "with_skill", 1, models={MODEL: 2, "claude-opus-5-5": 1},
                      efforts={EFFORT: 1, "high": 2})
        data = self.result()
        self.assertEqual(data["summary"]["with_skill"]["models"], {MODEL: 11, "claude-opus-5-5": 1})
        self.assertEqual(data["summary"]["with_skill"]["efforts"], {EFFORT: 10, "high": 2})
        self.assertTrue(self.notes(data, "alpha/with_skill/run-1", "1 of 3 calls", "claude-opus-5-5", MODEL))
        self.assertTrue(self.notes(data, "alpha/with_skill/run-1", "2 of 3 calls", "high", EFFORT))
        self.assertFalse(self.notes(data, "beta/with_skill/run-1"))


class UnknownFigures(Case):
    def test_an_estimated_output_is_counted_and_marked_never_zero(self):
        # The run's one call without its final usage counts usage.py's 5,400 output tokens.
        self.edit_run("beta", "without_skill", 2, estimated_calls=1,
                      tokens={"input": 10, "output": 5550, "cache_read": 1000, "write_5m": 0, "write_1h": 100})
        data = self.result()
        without = data["summary"]["without_skill"]
        self.assertStats(without["output"], 1450.0, 2733.739807, 50.0, 5550.0, n=4)
        self.assertEqual(without["estimated_runs"], 1)
        self.assertEqual(data["summary"]["with_skill"]["estimated_runs"], 0)
        run = next(r for r in data["runs"] if (r["case"], r["configuration"], r["run"]) == ("beta", "without_skill", 2))
        self.assertEqual(run["estimated_calls"], 1)
        self.assertTrue(self.notes(data, "beta/without_skill/run-2", "estimated"))
        text = self.markdown()
        self.assertIn("| Output | 250 ± 129 (100 to 400) | 1,450 ± 2,734 (50 to 5,550) * |", text)
        self.assertIn("| beta/without_skill/run-2 | 0/2 | 5.0 s | 5,550 * |", text)
        self.assertIn("* ", text.split("| Output |")[1])

    def test_an_unknown_cost_is_left_out_never_zero(self):
        self.edit_run("alpha", "with_skill", 1, cost_usd=None, models={"claude-new-model": 3})
        data = self.result()
        self.assertStats(data["summary"]["with_skill"]["cost_usd"], 0.30, 0.10, 0.20, 0.40, n=3)
        self.assertAlmostEqual(data["delta"]["cost_usd"], 0.225, places=4)
        self.assertIsNone(data["cost_usd"]["runs"])
        self.assertTrue(self.notes(data, "alpha/with_skill/run-1", "cost", "unknown"))
        self.assertIn("$0.300 ± $0.100 ($0.200 to $0.400), 3 of 4 runs", self.markdown())

    def test_an_unknown_grading_cost_leaves_the_total_unknown(self):
        path = self.iteration / "alpha/with_skill/run-1/grading.json"
        grading = json.loads(path.read_text(encoding="utf-8"))
        grading["grader"]["cost_usd"] = None
        path.write_text(json.dumps(grading), encoding="utf-8")
        self.assertIsNone(self.result()["cost_usd"]["grading"])

    def test_a_grading_by_the_script_alone_costs_nothing(self):
        path = self.iteration / "alpha/with_skill/run-1/grading.json"
        grading = json.loads(path.read_text(encoding="utf-8"))
        grading["grader"] = None
        path.write_text(json.dumps(grading), encoding="utf-8")
        self.assertAlmostEqual(self.result()["cost_usd"]["grading"], 7 * GRADING_COST, places=4)


class Notes(Case):
    def test_the_delta_note_puts_the_cost_beside_the_pass_rate(self):
        data = self.result()
        self.assertEqual(data["notes"][0], "with_skill against without_skill: pass rate +50 pts, "
                                           "cost +$0.175 a run (+233%), duration +20.0 s a run.")

    def test_an_assertion_with_one_result_everywhere_does_not_discriminate(self):
        data = self.result()
        found = {(a["case"], a["number"]): a for a in data["assertions"]}
        self.assertIs(found[("alpha", 1)]["discriminates"], False)
        self.assertIs(found[("beta", 1)]["discriminates"], False)
        self.assertIs(found[("alpha", 3)]["discriminates"], True)
        self.assertIs(found[("alpha", 2)]["discriminates"], True)
        self.assertEqual(found[("alpha", 1)]["results"], {"with_skill": {"passed": 2, "runs": 2},
                                                          "without_skill": {"passed": 2, "runs": 2}})
        self.assertTrue(self.notes(data, "alpha, assertion 1", "passed in every run of both configurations"))
        self.assertTrue(self.notes(data, "beta, assertion 1", "failed in every run of both configurations"))
        self.assertFalse(self.notes(data, "alpha, assertion 3"))
        self.assertFalse(self.notes(data, "beta, assertion 2"))

    def test_an_assertion_that_varies_within_a_configuration(self):
        data = self.result()
        found = {(a["case"], a["number"]): a for a in data["assertions"]}
        self.assertEqual(found[("alpha", 2)]["varies_in"], ["with_skill"])
        self.assertEqual(found[("alpha", 3)]["varies_in"], [])
        self.assertTrue(self.notes(data, "alpha, assertion 2", "passed in 1 of 2 with_skill runs"))

    def test_an_assertion_the_grader_named_weak(self):
        self.grade("alpha", "with_skill", 1, [T, T, T], weak=[(3, "Any file passes.")])
        self.grade("alpha", "without_skill", 2, [T, F, F], weak=[(3, "A wrong file passes.")])
        data = self.result()
        found = {(a["case"], a["number"]): a for a in data["assertions"]}
        self.assertEqual(found[("alpha", 3)]["weak"], 2)
        self.assertEqual(found[("alpha", 1)]["weak"], 0)
        self.assertTrue(self.notes(data, "alpha, assertion 3", "weak", "2 of 4 runs", "Any file passes."))


class LeftOut(Case):
    runs = 3

    def setUp(self):
        super().setUp()
        self.complete("alpha", "with_skill", 3, [F, F, F], duration=999, cost=9.99, status="stopped")
        self.edit_run("alpha", "with_skill", 3, reason="budget")
        self.complete("beta", "with_skill", 3, None, duration=999, cost=9.99)

    def test_only_complete_and_graded_runs_count(self):
        data = self.result()
        for metric, (mean, stddev, low, high) in EXPECTED["with_skill"].items():
            with self.subTest(metric=metric):
                self.assertStats(data["summary"]["with_skill"][metric], mean, stddev, low, high, n=4)
        left = {item["run"]: item["reason"] for item in data["left_out"]}
        self.assertEqual(left, {"alpha/with_skill/run-3": "not complete: stopped (budget)",
                                "beta/with_skill/run-3": "not graded",
                                "alpha/without_skill/run-3": "not started",
                                "beta/without_skill/run-3": "not started"})
        self.assertTrue(self.notes(data, "4 runs left out", "alpha/with_skill/run-3"))

    def test_a_grading_without_every_assertion_is_not_counted(self):
        path = self.iteration / "alpha/with_skill/run-2/grading.json"
        grading = json.loads(path.read_text(encoding="utf-8"))
        grading["assertions"].pop()
        path.write_text(json.dumps(grading), encoding="utf-8")
        data = self.result()
        self.assertEqual(data["summary"]["with_skill"]["runs"], 3)
        self.assertIn({"run": "alpha/with_skill/run-2", "reason": "not graded"}, data["left_out"])


class OneRun(Case):
    runs = 1

    def test_one_run_has_no_deviation(self):
        data = self.result()
        self.assertStats(data["by_case"]["alpha"]["with_skill"], 1.0, None, 1.0, 1.0, n=1)
        self.assertIn("| alpha | 100% | 33% | +67 pts |", self.markdown())


class OneConfiguration(Case):
    configurations = ("without_skill",)

    def test_no_delta_and_no_discrimination(self):
        data = self.result()
        self.assertIsNone(data["delta"])
        self.assertIsNone(data["delta_of"])
        self.assertEqual(list(data["summary"]), ["without_skill"])
        self.assertTrue(all(a["discriminates"] is None for a in data["assertions"]))
        self.assertFalse(self.notes(data, "against"))
        self.assertIn("| Metric | without_skill |\n", self.markdown())


class Refusals(Case):
    def test_no_graded_run(self):
        for path in self.iteration.glob("*/*/run-*/grading.json"):
            path.unlink()
        code, _, err = self.main()
        self.assertEqual(code, 1)
        self.assertIn("no graded run", err)
        self.assertIn("grade.py", err)
        self.assertFalse((self.iteration / "benchmark.json").exists())
        self.assertFalse((self.iteration / "benchmark.md").exists())

    def test_no_iteration(self):
        code, _, err = self.main(self.iteration.parent / "iteration-9")
        self.assertEqual(code, 1)
        self.assertIn("no iteration", err)


if __name__ == "__main__":
    unittest.main()
