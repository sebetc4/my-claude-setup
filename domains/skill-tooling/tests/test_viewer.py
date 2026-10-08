"""Tests for viewer.py: the review page of an iteration, adapted from skill-creator's
eval-viewer — each run's prompt, response, outputs and grades, the case's review items, the
benchmark, and the feedback saved to the iteration's feedback.json — per the design of
Phase 4 of roadmap skill-tooling."""

import base64
import contextlib
import importlib.util
import io
import json
import re
import socket
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "skills/authoring-skills/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(f"skill_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


viewer = load("viewer")

MODEL, EFFORT = "claude-sonnet-5-5", "xhigh"
ASSERTIONS = {"alpha": ["The note exists", "The note says yes"], "beta": ["The table is sorted"]}
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGD4DwABBAEAwS2OUAAAAABJRU5ErkJggg==")
DATA_RE = re.compile(r"const EMBEDDED_DATA = (.*?);\n", re.S)


class Case(unittest.TestCase):
    """An iteration as workspace.py, run.py, grade.py and benchmark.py leave it: alpha's
    runs complete and graded, beta's with_skill run-1 complete and ungraded, its run-2
    stopped, and its without_skill runs not started."""

    def setUp(self):
        tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.skills = tmp / ".eval-runs/skills/demo"
        self.iteration = self.prepare("iteration-1")
        self.complete("alpha", "with_skill", 1, {"notes/2026-10-08-yes.md": "# Yes\n\nYes.\n"}, grades=[True, True])
        self.complete("alpha", "with_skill", 2, {"notes/a.md": "yes", "chart.png": PNG}, grades=[True, False])
        self.complete("alpha", "without_skill", 1, {"note.txt": "no"}, grades=[False, False])
        self.complete("alpha", "without_skill", 2, {}, grades=[True, False])
        self.complete("beta", "with_skill", 1, {"table.md": "| a |\n|---|\n| b |\n"})
        self.complete("beta", "with_skill", 2, {}, status="stopped", reason="timeout")

    def prepare(self, name):
        iteration = self.skills / name
        self.write(iteration, "iteration.json", {
            "skill_name": "demo", "cases": list(ASSERTIONS), "configurations": ["with_skill", "without_skill"],
            "runs": 2, "model": MODEL, "effort": EFFORT, "budget_usd": 1.0})
        for number, (case, assertions) in enumerate(ASSERTIONS.items(), 1):
            self.write(iteration, f"{case}/eval_metadata.json", {
                "id": number, "name": case, "prompt": f"Write the {case} file.",
                "expected_output": f"A {case} file.", "assertions": assertions,
                "review": [f"Whether the {case} file reads well"]})
        return iteration

    def write(self, iteration, path, data):
        target = iteration / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            target.write_bytes(data)
        elif isinstance(data, str):
            target.write_text(data, encoding="utf-8")
        else:
            target.write_text(json.dumps(data, indent=1), encoding="utf-8")

    def complete(self, case, configuration, run, outputs, grades=None, status="complete", reason=None,
                 iteration=None):
        iteration = iteration or self.iteration
        folder = f"{case}/{configuration}/run-{run}"
        self.write(iteration, f"{folder}/run.json", {
            "case": case, "configuration": configuration, "run": run, "status": status, "reason": reason,
            "claude_version": "2.1.292", "model": MODEL, "effort": EFFORT, "duration_s": 12.5, "calls": 4,
            "models": {MODEL: 4}, "efforts": {EFFORT: 4}, "cost_usd": 0.05, "skill_reads": ["SKILL.md"]})
        self.write(iteration, f"{folder}/response.md", f"I wrote {case}.\n")
        self.write(iteration, f"{folder}/changes.json", {"added": sorted(outputs), "modified": [], "deleted": []})
        (iteration / folder / "outputs").mkdir(parents=True, exist_ok=True)
        for path, content in outputs.items():
            self.write(iteration, f"{folder}/outputs/{path}", content)
        if grades is not None:
            entries = [{"text": text, "passed": passed, "evidence": "seen in the note", "by": "grader"}
                       for text, passed in zip(ASSERTIONS[case], grades)]
            self.write(iteration, f"{folder}/grading.json", {
                "assertions": entries,
                "summary": {"passed": sum(grades), "failed": len(grades) - sum(grades), "total": len(grades),
                            "pass_rate": round(sum(grades) / len(grades), 2)},
                "weak": [{"text": ASSERTIONS[case][0], "reason": "any note passes"}],
                "claims": [{"claim": "I wrote it", "verified": True, "evidence": "outputs/"}],
                "grader": {"agent": "skill-grader", "cost_usd": 0.02}})

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = viewer.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def static(self, *options):
        page = self.iteration / "review.html"
        code, out, err = self.main(self.iteration, "--static", page, *options)
        self.assertEqual(code, 0, err)
        return page.read_text(encoding="utf-8")

    def embedded(self, html):
        found = DATA_RE.search(html)
        self.assertIsNotNone(found, "the page embeds no data")
        return json.loads(found.group(1))

    def runs(self, data):
        return {run["name"]: run for run in data["runs"]}


class Runs(Case):
    def test_each_run_with_a_record_is_shown_in_the_iterations_order(self):
        data = self.embedded(self.static())
        self.assertEqual([run["name"] for run in data["runs"]], [
            "alpha/with_skill/run-1", "alpha/with_skill/run-2", "alpha/without_skill/run-1",
            "alpha/without_skill/run-2", "beta/with_skill/run-1", "beta/with_skill/run-2"])

    def test_a_run_shows_its_case_prompt_expected_output_and_review_items(self):
        run = self.runs(self.embedded(self.static()))["alpha/without_skill/run-1"]
        self.assertEqual((run["case"], run["configuration"], run["run"]), ("alpha", "without_skill", 1))
        self.assertEqual(run["prompt"], "Write the alpha file.")
        self.assertEqual(run["expected_output"], "A alpha file.")
        self.assertEqual(run["review"], ["Whether the alpha file reads well"])

    def test_a_run_shows_its_response_status_and_figures(self):
        runs = self.runs(self.embedded(self.static()))
        run = runs["alpha/with_skill/run-1"]
        self.assertEqual(run["response"], "I wrote alpha.\n")
        self.assertEqual((run["status"], run["reason"]), ("complete", None))
        self.assertEqual(run["figures"]["cost_usd"], 0.05)
        self.assertEqual(run["figures"]["duration_s"], 12.5)
        self.assertEqual(run["figures"]["models"], {MODEL: 4})
        self.assertEqual(run["figures"]["efforts"], {EFFORT: 4})
        self.assertEqual(run["figures"]["claude_version"], "2.1.292")
        self.assertEqual((runs["beta/with_skill/run-2"]["status"], runs["beta/with_skill/run-2"]["reason"]),
                         ("stopped", "timeout"))

    def test_outputs_are_read_at_their_paths_under_outputs(self):
        run = self.runs(self.embedded(self.static()))["alpha/with_skill/run-1"]
        self.assertEqual(run["outputs"], [{"path": "notes/2026-10-08-yes.md", "type": "text",
                                           "content": "# Yes\n\nYes.\n"}])
        self.assertEqual(run["changes"], {"added": ["notes/2026-10-08-yes.md"], "modified": [], "deleted": []})

    def test_an_image_is_embedded_and_a_text_without_extension_stays_text(self):
        self.write(self.iteration, "alpha/with_skill/run-2/outputs/Makefile", "all:\n\ttrue\n")
        self.write(self.iteration, "alpha/with_skill/run-2/outputs/data.bin", b"\x00\x01\x02")
        outputs = {o["path"]: o for o in self.runs(self.embedded(self.static()))["alpha/with_skill/run-2"]["outputs"]}
        self.assertEqual(outputs["chart.png"]["type"], "image")
        self.assertEqual(outputs["chart.png"]["data_uri"], "data:image/png;base64," + base64.b64encode(PNG).decode())
        self.assertEqual(outputs["Makefile"], {"path": "Makefile", "type": "text", "content": "all:\n\ttrue\n"})
        self.assertEqual(outputs["data.bin"]["type"], "binary")
        self.assertTrue(outputs["data.bin"]["data_uri"].endswith(base64.b64encode(b"\x00\x01\x02").decode()))

    def test_a_run_shows_its_grading_or_none(self):
        runs = self.runs(self.embedded(self.static()))
        grading = runs["alpha/with_skill/run-2"]["grading"]
        self.assertEqual([(a["text"], a["passed"], a["by"]) for a in grading["assertions"]],
                         [("The note exists", True, "grader"), ("The note says yes", False, "grader")])
        self.assertEqual(grading["weak"], [{"text": "The note exists", "reason": "any note passes"}])
        self.assertEqual(grading["claims"][0]["claim"], "I wrote it")
        self.assertIsNone(runs["beta/with_skill/run-1"]["grading"])

    def test_the_page_names_the_skill_iteration_model_and_effort(self):
        data = self.embedded(self.static())
        self.assertEqual((data["skill_name"], data["iteration"], data["model"], data["effort"]),
                         ("demo", "iteration-1", MODEL, EFFORT))

    def test_text_that_closes_a_script_cannot_end_the_pages_data(self):
        hostile = "<script>alert(1)</script></script><!--"
        self.write(self.iteration, "alpha/with_skill/run-1/response.md", hostile)
        html = self.static()
        script = html[html.index("const EMBEDDED_DATA"):]
        self.assertNotIn("</script><!--", script[:script.index(";\n")])
        self.assertEqual(self.runs(self.embedded(html))["alpha/with_skill/run-1"]["response"], hostile)

    def test_the_page_is_the_adapted_template_with_its_data(self):
        html = self.static()
        template = (SCRIPTS.parent / "assets/viewer.html").read_text(encoding="utf-8")
        self.assertIn(viewer.PLACEHOLDER, template)
        self.assertNotIn(viewer.PLACEHOLDER, html)
        self.assertEqual(html.replace(DATA_RE.search(html).group(0), viewer.PLACEHOLDER + "\n", 1), template)


class Benchmark(Case):
    def test_the_benchmark_is_embedded_when_the_iteration_has_one(self):
        benchmark = {"skill_name": "demo", "summary": {}, "notes": ["with_skill against without_skill: +50 pts."]}
        self.write(self.iteration, "benchmark.json", benchmark)
        self.assertEqual(self.embedded(self.static())["benchmark"], benchmark)

    def test_without_a_benchmark_the_page_still_shows_the_runs(self):
        data = self.embedded(self.static())
        self.assertIsNone(data["benchmark"])
        self.assertEqual(len(data["runs"]), 6)


class Feedback(Case):
    def test_the_iterations_feedback_fills_the_page(self):
        self.write(self.iteration, "feedback.json", {"reviews": [
            {"run": "alpha/with_skill/run-1", "feedback": "Too long.", "at": "2026-10-08T10:00:00+00:00"},
            {"run": "alpha/with_skill/run-2", "feedback": "", "at": "2026-10-08T10:00:00+00:00"}],
            "status": "complete"})
        self.assertEqual(self.embedded(self.static())["feedback"], {"alpha/with_skill/run-1": "Too long."})

    def test_without_feedback_the_page_starts_empty(self):
        self.assertEqual(self.embedded(self.static())["feedback"], {})

    def test_an_unreadable_feedback_file_is_named_and_left_alone(self):
        self.write(self.iteration, "feedback.json", "{not json")
        code, _, err = self.main(self.iteration, "--static", self.iteration / "review.html")
        self.assertEqual(code, 0, err)
        self.assertIn("feedback.json", err)
        self.assertEqual((self.iteration / "feedback.json").read_text(encoding="utf-8"), "{not json")

    def test_a_saved_review_is_written_to_the_iterations_feedback_file(self):
        payload = {"reviews": [{"run": "alpha/with_skill/run-1", "feedback": "Good.", "at": "2026-10-08T10:00:00Z"}],
                   "status": "in_progress"}
        viewer.save_feedback(self.iteration, payload)
        self.assertEqual(json.loads((self.iteration / "feedback.json").read_text(encoding="utf-8")), payload)

    def test_a_review_of_another_shape_is_refused(self):
        for payload in ({"reviews": "Good."}, {"status": "complete"}, [], {"reviews": [{"feedback": "x"}]},
                        {"reviews": [{"run": "gamma/with_skill/run-1", "feedback": "x"}]}):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    viewer.save_feedback(self.iteration, payload)
                self.assertFalse((self.iteration / "feedback.json").exists())


class Previous(Case):
    def setUp(self):
        super().setUp()
        self.earlier = self.prepare("iteration-0")
        self.complete("alpha", "with_skill", 1, {"notes/old.md": "old"}, grades=[False, False], iteration=self.earlier)
        self.write(self.earlier, "feedback.json", {"reviews": [
            {"run": "alpha/with_skill/run-1", "feedback": "Name the date.", "at": "2026-10-07T10:00:00Z"}],
            "status": "complete"})

    def test_the_previous_iterations_outputs_and_feedback_are_shown_beside_each_run(self):
        data = self.embedded(self.static("--previous", self.earlier))
        self.assertEqual(data["previous"]["iteration"], "iteration-0")
        self.assertEqual(data["previous"]["feedback"], {"alpha/with_skill/run-1": "Name the date."})
        self.assertEqual(data["previous"]["outputs"]["alpha/with_skill/run-1"],
                         [{"path": "notes/old.md", "type": "text", "content": "old"}])
        self.assertNotIn("alpha/with_skill/run-2", data["previous"]["outputs"])

    def test_without_previous_none_is_shown(self):
        self.assertIsNone(self.embedded(self.static())["previous"])

    def test_a_previous_folder_that_is_no_iteration_is_refused(self):
        code, _, err = self.main(self.iteration, "--static", self.iteration / "review.html",
                                 "--previous", self.skills / "nothing")
        self.assertEqual(code, 1)
        self.assertIn("nothing", err)


class Refusals(Case):
    def test_a_folder_without_iteration_json_is_refused(self):
        code, _, err = self.main(self.skills, "--static", self.skills / "review.html")
        self.assertEqual(code, 1)
        self.assertIn("iteration.json", err)
        self.assertFalse((self.skills / "review.html").exists())

    def test_an_iteration_without_a_run_is_refused(self):
        empty = self.prepare("iteration-2")
        code, _, err = self.main(empty, "--static", empty / "review.html")
        self.assertEqual(code, 1)
        self.assertIn("no run", err)


class Server(Case):
    def serve(self):
        server = viewer.server(self.iteration, None, 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_address[1]}"

    def load(self, url):
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")

    def test_the_page_is_built_again_at_each_load(self):
        url = self.serve()
        first = self.embedded(self.load(url + "/"))
        self.write(self.iteration, "alpha/with_skill/run-1/response.md", "Changed.\n")
        second = self.embedded(self.load(url + "/"))
        self.assertEqual(self.runs(first)["alpha/with_skill/run-1"]["response"], "I wrote alpha.\n")
        self.assertEqual(self.runs(second)["alpha/with_skill/run-1"]["response"], "Changed.\n")

    def test_a_posted_review_is_saved_and_a_wrong_one_refused(self):
        url = self.serve() + "/api/feedback"
        payload = {"reviews": [{"run": "beta/with_skill/run-1", "feedback": "Sort it.", "at": "2026-10-08T10:00:00Z"}],
                   "status": "complete"}
        request = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(request) as response:
            self.assertEqual(response.status, 200)
        self.assertEqual(json.loads((self.iteration / "feedback.json").read_text(encoding="utf-8")), payload)
        wrong = urllib.request.Request(url, b'{"reviews": 3}', {"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(wrong)
        caught.exception.close()
        self.assertEqual(caught.exception.code, 400)
        self.assertEqual(json.loads((self.iteration / "feedback.json").read_text(encoding="utf-8")), payload)

    def test_a_port_in_use_is_left_to_its_process_and_another_taken(self):
        with socket.socket() as taken:
            taken.bind(("127.0.0.1", 0))
            taken.listen()
            port = taken.getsockname()[1]
            server = viewer.server(self.iteration, None, port)
            try:
                self.assertNotEqual(server.server_address[1], port)
            finally:
                server.server_close()
            self.assertEqual(taken.getsockname()[1], port)


if __name__ == "__main__":
    unittest.main()
