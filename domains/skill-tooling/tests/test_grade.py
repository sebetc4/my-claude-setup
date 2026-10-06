"""Tests for grade.py: an iteration's complete runs graded by the skill's own evals/grade.py,
then by the grader agent started as a claude -p session, here a stub standing for claude,
per the design of Phase 4 of roadmap skill-tooling."""

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "skills/authoring-skills/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(f"skill_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workspace = load("workspace")
grade = load("grade")

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
ASSERTIONS = ["The answer file exists", "The answer says yes", "The account names the file"]
AGENT = """---
name: test-grader
description: Grades a run's assertions.
tools: Read, Bash
model: claude-sonnet-5-5
effort: high
---

You grade runs. Answer with one JSON object.
"""

# The stub answers --version, logs what it received, writes a transcript under
# $CLAUDE_CONFIG_DIR/projects/ and prints a json result whose text is $STUB_ANSWER, or an
# answer that passes every numbered assertion of the prompt.
STUB = f"""#!{sys.executable}
import json, os, re, sys, uuid
from pathlib import Path
args = sys.argv[1:]
if args == ["--version"]:
    print("2.1.292 (Claude Code)")
    sys.exit(0)
def value(flag):
    return args[args.index(flag) + 1] if flag in args else None
cwd = Path.cwd()
prompt = sys.stdin.read()
agents = value("--agents")
above = [str(p) for p in cwd.parent.parents
         if (p / ".git").exists() or (p / ".agent-conventions.toml").exists()]
log = {{"argv": args, "cwd": str(cwd), "env": dict(os.environ), "prompt": prompt, "repositories_above": above,
        "files": sorted(p.relative_to(cwd).as_posix() for p in cwd.rglob("*") if p.is_file()),
        "agents": json.loads(Path(agents).read_text()) if agents else None}}
with open(os.environ["STUB_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(log) + "\\n")
numbers = [int(n) for n in re.findall(r"^(\\d+)\\. ", prompt, re.M)]
answer = os.environ.get("STUB_ANSWER") or json.dumps({{
    "assertions": [{{"assertion": n, "passed": True, "evidence": f"seen {{n}}"}} for n in numbers],
    "weak": [], "claims": []}})
model, effort = value("--model"), value("--effort")
usage = {{"input_tokens": 10, "output_tokens": 100, "cache_read_input_tokens": 1000,
          "cache_creation_input_tokens": 0}}
records = [{{"type": "user", "message": {{"role": "user", "content": prompt}}}},
           {{"type": "assistant", "effort": effort, "message": {{
               "id": "msg_1", "model": model, "stop_reason": "end_turn", "usage": usage,
               "content": [{{"type": "text", "text": answer}}]}}}}]
session = str(uuid.uuid4())
folder = Path(os.environ["CLAUDE_CONFIG_DIR"]) / "projects" / "-stub"
folder.mkdir(parents=True, exist_ok=True)
(folder / f"{{session}}.jsonl").write_text("".join(json.dumps(r) + "\\n" for r in records), encoding="utf-8")
subtype = os.environ.get("STUB_SUBTYPE", "success")
print(json.dumps({{"type": "result", "subtype": subtype, "is_error": subtype != "success",
                  "session_id": session, "total_cost_usd": 0.0123, "duration_ms": 2000, "num_turns": 1,
                  "result": answer, "permission_denials": []}}))
"""
# One call of 10 input, 100 output and 1,000 cache-read tokens on Sonnet 5.5, in dollars.
SESSION_COST = (10 * 2.0 + 100 * 10.0 + 1000 * 0.20) / 1e6


def case(**fields):
    return {"id": 1, "name": "answer", "kind": "task", "setup": "empty", "prompt": "Answer yes in answer.txt.",
            "expected_output": "answer.txt saying yes.", "assertions": ASSERTIONS, "files": ["evals/files/input.txt"],
            **fields}


def answer(*grades, weak=(), claims=()):
    return json.dumps({"assertions": [{"assertion": n, "passed": p, "evidence": f"evidence {n}"}
                                      for n, p in enumerate(grades, 1)],
                       "weak": [{"assertion": n, "reason": f"reason {n}"} for n in weak],
                       "claims": list(claims)})


class Case(unittest.TestCase):
    """A repository holding the skill demo, an iteration whose runs are complete, a grader
    agent's file, and the stub."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo = self.tmp / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\n")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: Demo.\n---\n\nBody.\n")
        self.write("skills/demo/evals/files/input.txt", "input\n")
        self.write("skills/demo/evals/evals.json", json.dumps({"skill_name": "demo", "evals": [case()]}))
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        self.iteration = workspace.prepare(self.skill, runs=1)
        for configuration in ("with_skill", "without_skill"):
            self.complete(configuration)
        self.agent = self.tmp / "agents/test-grader.md"
        self.agent.parent.mkdir()
        self.agent.write_text(AGENT, encoding="utf-8")
        self.enterContext(mock.patch.object(grade, "AGENT", self.agent))
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        stub = bin_dir / "claude"
        stub.write_text(STUB, encoding="utf-8")
        stub.chmod(0o755)
        self.config = self.tmp / "config"
        self.log = self.tmp / "stub.log"
        self.enterContext(mock.patch.dict(os.environ, {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "CLAUDE_CONFIG_DIR": str(self.config),
            "STUB_LOG": str(self.log), "CLAUDECODE": "1", "CLAUDE_EFFORT": "max",
            "CLAUDE_CODE_SESSION_ATTENDED": "1"}))

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_folder(self, configuration):
        return self.iteration / "answer" / configuration / "run-1"

    def complete(self, configuration, status="complete"):
        """Write the run's folder as run.py leaves it."""
        folder = self.run_folder(configuration)
        (folder / "outputs").mkdir(parents=True, exist_ok=True)
        (folder / "outputs/answer.txt").write_text("yes\n", encoding="utf-8")
        (folder / "transcript.md").write_text("## Prompt\n\nAnswer yes.\n", encoding="utf-8")
        (folder / "response.md").write_text("I wrote answer.txt.\n", encoding="utf-8")
        (folder / "changes.json").write_text(json.dumps({"added": ["answer.txt"], "modified": [], "deleted": []}))
        (folder / "run.json").write_text(json.dumps({"status": status, "cost_usd": 0.5}), encoding="utf-8")

    def skill_grader(self, body):
        """The skill's own evals/grade.py."""
        self.write("skills/demo/evals/grade.py", body)

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = grade.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def sessions(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def grading(self, configuration):
        return json.loads((self.run_folder(configuration) / "grading.json").read_text(encoding="utf-8"))


# A skill's grade.py that decides the first assertion of every complete run.
FIRST_DECIDED = """import json, sys
from pathlib import Path
for run in Path(sys.argv[1]).glob("*/*/run-*"):
    if json.loads((run / "run.json").read_text())["status"] != "complete":
        continue
    (run / "grading.json").write_text(json.dumps({"assertions": [
        {"text": "The answer file exists", "passed": True, "evidence": "answer.txt is in outputs/"}]}))
"""


class Announce(Case):
    def test_nothing_starts_without_start(self):
        code, out, _ = self.main(self.iteration)
        self.assertEqual(code, 0)
        self.assertEqual(self.sessions(), [])
        self.assertIn("answer/with_skill/run-1", out)
        self.assertIn("answer/without_skill/run-1", out)
        self.assertIn("2 runs to grade, 2 grader sessions at most, estimated $0.90", out)
        self.assertIn("--start", out)
        self.assertFalse(self.run_folder("with_skill").joinpath("grading.json").exists())

    def test_a_run_not_complete_is_left_out(self):
        self.complete("without_skill", status="stopped")
        _, out, _ = self.main(self.iteration)
        self.assertIn("1 run to grade", out)
        self.assertIn("answer/without_skill/run-1: not complete, left out", out)

    def test_a_graded_run_is_skipped(self):
        self.main(self.iteration, "--start")
        code, out, _ = self.main(self.iteration, "--start")
        self.assertEqual(code, 0)
        self.assertIn("0 runs to grade", out)
        self.assertEqual(len(self.sessions()), 2)

    def test_the_estimate_follows_the_skills_gradings(self):
        self.main(self.iteration, "--start")
        (self.run_folder("with_skill") / "grading.json").unlink()
        _, out, _ = self.main(self.iteration)
        self.assertIn(f"estimated ${SESSION_COST:.2f}", out)
        self.assertIn("mean of 1 complete grading", out)

    def test_the_estimate_never_passes_the_ceiling(self):
        _, out, _ = self.main(self.iteration, "--budget", "0.25")
        self.assertIn("estimated $0.50", out)
        self.assertIn("the session's ceiling, $0.25", out)

    def test_the_skills_grade_py_is_announced_not_run(self):
        self.skill_grader(FIRST_DECIDED)
        _, out, _ = self.main(self.iteration)
        self.assertIn("evals/grade.py", out)
        self.assertFalse(self.run_folder("with_skill").joinpath("grading.json").exists())


class Session(Case):
    def setUp(self):
        super().setUp()
        self.code, self.out, self.err = self.main(self.iteration, "--start")

    def test_every_run_ends_with_a_line(self):
        self.assertEqual(self.code, 0, self.err)
        self.assertEqual(len(self.sessions()), 2)
        self.assertIn("answer/with_skill/run-1: graded, 3/3 passed", self.out)

    def test_the_session_runs_the_agent(self):
        for session in self.sessions():
            argv = session["argv"]
            self.assertEqual(argv[argv.index("--agent") + 1], "test-grader")
            definition = session["agents"]["test-grader"]
            self.assertEqual(definition["prompt"].strip(), "You grade runs. Answer with one JSON object.")
            self.assertEqual(definition["description"], "Grades a run's assertions.")
            self.assertEqual(definition["tools"], ["Read", "Bash"])
            self.assertEqual(argv[argv.index("--model") + 1], "claude-sonnet-5-5")
            self.assertEqual(argv[argv.index("--effort") + 1], "high", "the agent's effort is not applied")

    def test_the_session_takes_the_flags_of_a_run(self):
        for session in self.sessions():
            argv = session["argv"]
            for flag, value in (("--max-budget-usd", "1.0"), ("--permission-mode", "auto"),
                                ("--permission-prompts", "none"), ("--setting-sources", "project,local"),
                                ("--output-format", "json")):
                self.assertEqual(argv[argv.index(flag) + 1], value, flag)
            self.assertIn("--strict-mcp-config", argv)
            self.assertEqual(argv[argv.index("--disallowed-tools") + 1:argv.index("--disallowed-tools") + 3],
                             ["Skill", "Agent"])
            command = json.loads(argv[argv.index("--settings") + 1])["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            self.assertIn("guard.py", command)
            self.assertIn(str(self.repo), command)
            for name in ("CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED"):
                self.assertNotIn(name, session["env"])

    def test_the_session_works_on_a_copy_outside_any_repository(self):
        for session in self.sessions():
            self.assertEqual(session["repositories_above"], [])
            self.assertFalse(Path(session["cwd"]).is_relative_to(self.repo))
            self.assertEqual(session["files"], ["changes.json", "inputs/files/input.txt", "outputs/answer.txt",
                                                "response.md", "transcript.md"])
            self.assertFalse(Path(session["cwd"]).exists(), "the grader's temporary folder was left behind")

    def test_the_prompt_names_the_case_and_numbers_the_assertions(self):
        prompt = self.sessions()[0]["prompt"]
        self.assertIn("Answer yes in answer.txt.", prompt)
        self.assertIn("answer.txt saying yes.", prompt)
        for number, text in enumerate(ASSERTIONS, 1):
            self.assertIn(f"\n{number}. {text}\n", prompt + "\n")
        for name in ("outputs/", "changes.json", "transcript.md", "response.md", "inputs/"):
            self.assertIn(f"`{name}`", prompt)

    def test_grading_json_is_written_from_the_answer(self):
        recorded = self.grading("with_skill")
        self.assertEqual(recorded["assertions"],
                         [{"text": text, "passed": True, "evidence": f"seen {n}", "by": "grader"}
                          for n, text in enumerate(ASSERTIONS, 1)])
        self.assertEqual(recorded["summary"], {"passed": 3, "failed": 0, "total": 3, "pass_rate": 1.0})
        self.assertEqual((recorded["weak"], recorded["claims"]), ([], []))
        grader = recorded["grader"]
        self.assertEqual((grader["agent"], grader["model"], grader["effort"]),
                         ("test-grader", "claude-sonnet-5-5", "high"))
        self.assertEqual((grader["models"], grader["efforts"]), ({"claude-sonnet-5-5": 1}, {"high": 1}))
        self.assertAlmostEqual(grader["cost_usd"], SESSION_COST)
        self.assertEqual(grader["reported_cost_usd"], 0.0123)
        self.assertEqual(grader["claude_version"], "2.1.292")
        self.assertTrue(grader["session_id"])

    def test_the_graders_session_is_kept(self):
        folder = self.run_folder("with_skill") / "grader"
        for name in ("prompt.md", "response.md", "result.json", "transcript.jsonl", "transcript.md"):
            self.assertTrue((folder / name).is_file(), name)


class Answers(Case):
    def start(self, text):
        with mock.patch.dict(os.environ, {"STUB_ANSWER": text}):
            return self.main(self.iteration, "--start")

    def test_failures_weak_assertions_and_claims_are_kept(self):
        claim = {"claim": "answer.txt says yes", "verified": False, "evidence": "it says no"}
        self.start(answer(True, False, True, weak=[3], claims=[claim]))
        recorded = self.grading("with_skill")
        self.assertEqual([a["passed"] for a in recorded["assertions"]], [True, False, True])
        self.assertEqual(recorded["summary"], {"passed": 2, "failed": 1, "total": 3, "pass_rate": 0.67})
        self.assertEqual(recorded["weak"], [{"text": ASSERTIONS[2], "reason": "reason 3"}])
        self.assertEqual(recorded["claims"], [claim])

    def test_an_answer_in_a_fence_is_read(self):
        _, out, _ = self.start("Here is the grading.\n\n```json\n" + answer(True, True, False) + "\n```\n")
        self.assertIn("graded, 2/3 passed", out)

    def test_an_unreadable_answer_leaves_the_run_ungraded(self):
        _, out, _ = self.start("All assertions pass.")
        self.assertIn("answer/with_skill/run-1: stopped (unreadable answer", out)
        self.assertFalse(self.run_folder("with_skill").joinpath("grading.json").exists())
        self.assertIn("All assertions pass.", (self.run_folder("with_skill") / "grader/response.md").read_text())
        _, out, _ = self.main(self.iteration)
        self.assertIn("2 runs to grade", out)

    def test_an_answer_that_skips_an_assertion_is_refused(self):
        _, out, _ = self.start(answer(True, True))
        self.assertIn("stopped (unreadable answer: assertion 3 is not graded)", out)

    def test_an_answer_naming_an_unknown_assertion_is_refused(self):
        _, out, _ = self.start(answer(True, True, True, weak=[4]))
        self.assertIn("unreadable answer", out)
        self.assertIn("4", out)

    def test_a_stopped_session_leaves_the_run_ungraded(self):
        with mock.patch.dict(os.environ, {"STUB_SUBTYPE": "error_max_budget_usd"}):
            _, out, _ = self.main(self.iteration, "--start")
        self.assertIn("answer/with_skill/run-1: stopped (error_max_budget_usd)", out)
        self.assertFalse(self.run_folder("with_skill").joinpath("grading.json").exists())


class SkillScript(Case):
    def test_the_skills_grade_py_decides_first(self):
        self.skill_grader(FIRST_DECIDED)
        code, _, err = self.main(self.iteration, "--start")
        self.assertEqual(code, 0, err)
        prompt = self.sessions()[0]["prompt"]
        self.assertNotIn(ASSERTIONS[0], prompt)
        self.assertIn(f"1. {ASSERTIONS[1]}", prompt)
        self.assertIn(f"2. {ASSERTIONS[2]}", prompt)
        recorded = self.grading("with_skill")
        self.assertEqual([(a["text"], a["by"]) for a in recorded["assertions"]],
                         [(ASSERTIONS[0], "script"), (ASSERTIONS[1], "grader"), (ASSERTIONS[2], "grader")])
        self.assertEqual(recorded["assertions"][0]["evidence"], "answer.txt is in outputs/")
        self.assertEqual(recorded["summary"]["total"], 3)

    def test_a_skill_deciding_every_assertion_starts_no_session(self):
        self.skill_grader(FIRST_DECIDED.replace(
            '"answer.txt is in outputs/"}', '"answer.txt is in outputs/"}' + "".join(
                f', {{"text": "{t}", "passed": False, "evidence": "no"}}' for t in ASSERTIONS[1:])))
        code, out, err = self.main(self.iteration, "--start")
        self.assertEqual(code, 0, err)
        self.assertEqual(self.sessions(), [])
        recorded = self.grading("with_skill")
        self.assertEqual(recorded["summary"], {"passed": 1, "failed": 2, "total": 3, "pass_rate": 0.33})
        self.assertIsNone(recorded["grader"])
        self.assertIn("answer/with_skill/run-1: graded, 1/3 passed", out)

    def test_a_failing_grade_py_stops_the_grading_with_its_message(self):
        self.skill_grader("import sys\nsys.exit('the fixture is missing')\n")
        code, _, err = self.main(self.iteration, "--start")
        self.assertEqual(code, 1)
        self.assertIn("evals/grade.py", err)
        self.assertIn("the fixture is missing", err)
        self.assertEqual(self.sessions(), [])

    def test_an_assertion_the_case_does_not_hold_stops_the_grading(self):
        self.skill_grader(FIRST_DECIDED.replace("The answer file exists", "Another assertion"))
        code, _, err = self.main(self.iteration, "--start")
        self.assertEqual(code, 1)
        self.assertIn("Another assertion", err)
        self.assertEqual(self.sessions(), [])

    def test_a_complete_grading_survives_the_skills_grade_py(self):
        self.main(self.iteration, "--start")
        before = self.grading("with_skill")
        self.complete("without_skill")
        (self.run_folder("without_skill") / "grading.json").unlink()
        self.skill_grader(FIRST_DECIDED)
        self.main(self.iteration, "--start")
        self.assertEqual(self.grading("with_skill"), before)
        self.assertEqual(self.grading("without_skill")["assertions"][0]["by"], "script")


class Agent(unittest.TestCase):
    def test_the_agent_is_found_beside_the_skills_folder(self):
        self.assertEqual(grade.AGENT, SCRIPTS.parents[2] / "agents" / "skill-grader.md")
        agent = grade.read_agent(grade.AGENT)
        self.assertEqual((agent.name, agent.tools), ("skill-grader", ["Read", "Bash"]))

    def test_an_agent_without_model_or_effort_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test-grader.md"
            path.write_text(AGENT.replace("effort: high\n", ""), encoding="utf-8")
            with self.assertRaises(grade.Refused) as raised:
                grade.read_agent(path)
        self.assertIn("effort", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
