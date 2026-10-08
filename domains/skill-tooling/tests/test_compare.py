"""Tests for compare.py: the outputs of two versions of a skill judged blind by the comparator
agent, started as claude -p sessions, here a stub standing for claude, per the design of
Phase 4 of roadmap skill-tooling."""

import contextlib
import importlib.util
import io
import json
import os
import shutil
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
compare = load("compare")

CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
ASSERTIONS = ["The answer file exists", "The answer says yes", "The account names the file"]
AGENT = """---
name: test-comparator
description: Compares two outputs.
tools: Read, Bash
model: claude-sonnet-5-5
effort: high
---

You compare outputs. Answer with one JSON object.
"""
BETTER, PLAIN = "yes, the better answer\n", "yes\n"
NEW, OLD = "iteration-1/with_skill", "iteration-1/old_skill"

# The stub answers --version, logs what it received, writes a transcript under
# $CLAUDE_CONFIG_DIR/projects/ and prints a json result whose text is $STUB_ANSWER; else the
# winner the session's place in $STUB_WINNERS gives, else the output whose answer.txt says
# "better". Its scores give A 4 and B 3, and its assertions fail the second for B.
STUB = f"""#!{sys.executable}
import json, os, re, sys, uuid
from pathlib import Path
args = sys.argv[1:]
if args == ["--version"]:
    print("2.1.292 (Claude Code)")
    sys.exit(0)
def value(flag):
    return args[args.index(flag) + 1] if flag in args else None
def read(path):
    target = cwd / path
    return target.read_text() if target.is_file() else ""
cwd = Path.cwd()
prompt = sys.stdin.read()
agents = value("--agents")
above = [str(p) for p in cwd.parent.parents
         if (p / ".git").exists() or (p / ".agent-conventions.toml").exists()]
log_path = Path(os.environ["STUB_LOG"])
done = len(log_path.read_text().splitlines()) if log_path.exists() else 0
log = {{"argv": args, "cwd": str(cwd), "env": dict(os.environ), "prompt": prompt, "repositories_above": above,
        "files": sorted(p.relative_to(cwd).as_posix() for p in cwd.rglob("*") if p.is_file()),
        "agents": json.loads(Path(agents).read_text()) if agents else None,
        "a": read("a/outputs/answer.txt"), "b": read("b/outputs/answer.txt")}}
with open(log_path, "a", encoding="utf-8") as handle:
    handle.write(json.dumps(log) + "\\n")
numbers = [int(n) for n in re.findall(r"^(\\d+)\\. ", prompt, re.M)]
winners = os.environ.get("STUB_WINNERS")
if winners:
    winner = winners.split(",")[done]
else:
    winner = "A" if "better" in log["a"] else "B" if "better" in log["b"] else "tie"
answer = os.environ.get("STUB_ANSWER") or json.dumps({{
    "winner": winner, "reason": f"{{winner}} answers better",
    "A": {{"correctness": 4, "completeness": 4, "form": 4, "strengths": ["strength of A"], "weaknesses": []}},
    "B": {{"correctness": 3, "completeness": 3, "form": 3, "strengths": [], "weaknesses": ["weakness of B"]}},
    "assertions": [{{"assertion": n, "A": True, "B": n != 2, "evidence": f"seen {{n}}"}} for n in numbers]}}, indent=2)
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


def case(name, prompt="Answer yes in answer.txt."):
    return {"id": 1 if name == "answer" else 2, "name": name, "kind": "task", "setup": "empty", "prompt": prompt,
            "expected_output": "answer.txt saying yes.", "assertions": ASSERTIONS,
            "files": ["evals/files/input.txt"]}


class Case(unittest.TestCase):
    """A repository holding the skill demo, an edit iteration whose two arms are complete —
    with_skill answering better than old_skill —, a comparator agent's file, and the stub."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo = self.tmp / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\n")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: Demo.\n---\n\nBody.\n")
        self.write("skills/demo/evals/files/input.txt", "input\n")
        self.write("skills/demo/evals/evals.json",
                   json.dumps({"skill_name": "demo", "evals": [case("answer"), case("second")]}))
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        old = self.tmp / "old/demo"
        old.mkdir(parents=True)
        (old / "SKILL.md").write_text("---\nname: demo\ndescription: Old demo.\n---\n\nOld body.\n", encoding="utf-8")
        self.iteration = workspace.prepare(self.skill, baseline=str(old), runs=1)
        for name in ("answer", "second"):
            self.complete(self.iteration, name, "with_skill", BETTER)
            self.complete(self.iteration, name, "old_skill", PLAIN)
        self.agent = self.tmp / "agents/test-comparator.md"
        self.agent.parent.mkdir()
        self.agent.write_text(AGENT, encoding="utf-8")
        self.enterContext(mock.patch.object(compare, "AGENT", self.agent))
        # The first session of a pair shows the first version as A, unless a test draws otherwise.
        self.enterContext(mock.patch.object(compare, "DRAW", mock.Mock(choice=lambda options: options[0])))
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

    def complete(self, iteration, name, configuration, text, status="complete"):
        """Write the run's folder as run.py leaves it."""
        folder = iteration / name / configuration / "run-1"
        (folder / "outputs").mkdir(parents=True, exist_ok=True)
        (folder / "outputs/answer.txt").write_text(text, encoding="utf-8")
        (folder / "transcript.md").write_text(f"## Prompt\n\nUse the skill at skill/demo ({configuration}).\n",
                                              encoding="utf-8")
        (folder / "response.md").write_text("I wrote answer.txt.\n", encoding="utf-8")
        (folder / "changes.json").write_text(json.dumps({"added": ["answer.txt"], "modified": [], "deleted": []}))
        (folder / "run.json").write_text(json.dumps({"status": status, "cost_usd": 0.5}), encoding="utf-8")

    def skill_only(self, text):
        """A further iteration of the skill's arm alone, its runs complete."""
        iteration = workspace.prepare(self.skill, skill_only=True, runs=1)
        for name in ("answer", "second"):
            self.complete(iteration, name, "with_skill", text)
        return iteration

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = compare.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def start(self, *argv, **env):
        with mock.patch.dict(os.environ, env):
            return self.main(self.iteration, "--start", "--jobs", "1", *argv)

    def sessions(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def comparisons(self):
        return sorted(self.iteration.parent.glob("comparison-*"))

    def comparison(self, number=1):
        path = self.iteration.parent / f"comparison-{number}" / "comparison.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def pair(self, name="answer", number=1):
        return next(p for p in self.comparison(number)["pairs"] if p["case"] == name)


class Announce(Case):
    def test_nothing_starts_without_start(self):
        code, out, _ = self.main(self.iteration)
        self.assertEqual(code, 0)
        self.assertEqual(self.sessions(), [])
        self.assertIn(f"Comparing {NEW} with {OLD}", out)
        self.assertIn("answer/run-1", out)
        self.assertIn("second/run-1", out)
        self.assertIn("2 pairs, 6 comparator sessions to start, estimated $2.70", out)
        self.assertIn("--start", out)
        self.assertEqual(self.comparisons(), [])

    def test_an_iteration_of_one_configuration_needs_another(self):
        alone = self.skill_only(BETTER)
        code, _, err = self.main(alone)
        self.assertEqual(code, 1)
        self.assertIn("one configuration", err)
        self.assertIn("name a second iteration", err)

    def test_two_iterations_compare_the_skills_arm_of_each(self):
        first, second = self.skill_only(BETTER), self.skill_only(PLAIN)
        code, out, err = self.main(first, second)
        self.assertEqual(code, 0, err)
        self.assertIn("Comparing iteration-2/with_skill with iteration-3/with_skill", out)
        self.assertIn("2 pairs", out)

    def test_iterations_of_two_skills_are_refused(self):
        self.write("skills/other/SKILL.md", "---\nname: other\ndescription: Other.\n---\n\nBody.\n")
        self.write("skills/other/evals/files/input.txt", "input\n")
        self.write("skills/other/evals/evals.json", json.dumps({"skill_name": "other", "evals": [case("answer")]}))
        other = workspace.prepare(self.repo / "skills/other", skill_only=True, runs=1)
        code, _, err = self.main(self.iteration, other)
        self.assertEqual(code, 1)
        self.assertIn("demo", err)
        self.assertIn("other", err)

    def test_the_same_iteration_twice_is_refused(self):
        code, _, err = self.main(self.iteration, self.iteration)
        self.assertEqual(code, 1)
        self.assertIn("once", err)

    def test_a_pair_without_both_runs_complete_is_left_out(self):
        self.complete(self.iteration, "second", "old_skill", PLAIN, status="stopped")
        _, out, _ = self.main(self.iteration)
        self.assertIn(f"second/run-1: left out, {OLD}/run-1 is not complete", out)
        self.assertIn("1 pair, 3 comparator sessions to start", out)

    def test_a_case_whose_prompt_differs_is_left_out(self):
        first, second = self.skill_only(BETTER), self.skill_only(PLAIN)
        path = second / "second/eval_metadata.json"
        metadata = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps({**metadata, "prompt": "Answer no."}), encoding="utf-8")
        _, out, _ = self.main(first, second)
        self.assertIn("second: left out, the prompts differ", out)
        self.assertIn("1 pair, 3 comparator sessions", out)

    def test_case_limits_the_pairs(self):
        _, out, _ = self.main(self.iteration, "--case", "answer")
        self.assertIn("1 pair, 3 comparator sessions", out)
        self.assertNotIn("second/run-1", out)
        code, _, err = self.main(self.iteration, "--case", "missing")
        self.assertEqual(code, 1)
        self.assertIn("no case named `missing`", err)

    def test_the_estimate_never_passes_the_ceiling(self):
        _, out, _ = self.main(self.iteration, "--budget", "0.25")
        self.assertIn("estimated $1.50", out)
        self.assertIn("the session's ceiling, $0.25", out)

    def test_the_estimate_follows_earlier_comparisons(self):
        self.start("--case", "answer")
        _, out, _ = self.main(self.iteration)
        self.assertIn(f"2 pairs, 3 comparator sessions to start, estimated ${3 * SESSION_COST:.2f}", out)
        self.assertIn("mean of 3 complete comparator sessions", out)


class Session(Case):
    def setUp(self):
        super().setUp()
        self.code, self.out, self.err = self.start()

    def test_every_pair_is_judged_three_times(self):
        self.assertEqual(self.code, 0, self.err)
        self.assertEqual(len(self.sessions()), 6)
        self.assertIn(f"answer/run-1/session-1: {NEW} wins", self.out)
        self.assertIn(f"answer/run-1: {NEW}, 3 of 3", self.out)
        self.assertIn(f"second/run-1: {NEW}, 3 of 3", self.out)

    def test_the_session_runs_the_agent_at_its_model_and_effort(self):
        for session in self.sessions():
            argv = session["argv"]
            self.assertEqual(argv[argv.index("--agent") + 1], "test-comparator")
            definition = session["agents"]["test-comparator"]
            self.assertEqual(definition["prompt"].strip(), "You compare outputs. Answer with one JSON object.")
            self.assertEqual(definition["tools"], ["Read", "Bash"])
            self.assertEqual(argv[argv.index("--model") + 1], "claude-sonnet-5-5")
            self.assertEqual(argv[argv.index("--effort") + 1], "high", "the agent's effort is not applied")

    def test_the_session_takes_the_flags_of_a_run(self):
        folder = self.comparisons()[0]
        for session in self.sessions():
            argv = session["argv"]
            for flag, value in (("--max-budget-usd", "1.0"), ("--permission-mode", "auto"),
                                ("--permission-prompts", "none"), ("--setting-sources", "project,local"),
                                ("--output-format", "json")):
                self.assertEqual(argv[argv.index(flag) + 1], value, flag)
            self.assertIn("--strict-mcp-config", argv)
            settings = json.loads(argv[argv.index("--settings") + 1])
            command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
            for denied in ("guard.py", str(self.repo), str(self.iteration), str(folder)):
                self.assertIn(denied, command)
            self.assertIs(settings["autoMemoryEnabled"], False)
            for name in ("CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED"):
                self.assertNotIn(name, session["env"])

    def test_the_session_sees_the_two_outputs_and_nothing_that_names_them(self):
        for session in self.sessions():
            self.assertEqual(session["files"], ["a/outputs/answer.txt", "a/response.md", "b/outputs/answer.txt",
                                                "b/response.md", "inputs/files/input.txt"])
            self.assertEqual(session["repositories_above"], [])
            self.assertFalse(Path(session["cwd"]).is_relative_to(self.repo))
            self.assertFalse(Path(session["cwd"]).exists(), "the comparator's temporary folder was left behind")
            for word in ("with_skill", "old_skill", "iteration-"):
                self.assertNotIn(word, session["prompt"])

    def test_the_request_names_the_case_and_numbers_the_assertions(self):
        prompt = self.sessions()[0]["prompt"]
        self.assertIn("Answer yes in answer.txt.", prompt)
        self.assertIn("answer.txt saying yes.", prompt)
        for number, text in enumerate(ASSERTIONS, 1):
            self.assertIn(f"\n{number}. {text}\n", prompt + "\n")
        for name in ("a/outputs/", "b/outputs/", "a/response.md", "b/response.md", "inputs/"):
            self.assertIn(f"`{name}`", prompt)

    def test_labels_alternate_within_a_pair(self):
        labels = self.pair()["labels"]
        self.assertEqual(len(labels), 3)
        self.assertEqual(labels[0], labels[2])
        self.assertEqual(labels[1], {"A": labels[0]["B"], "B": labels[0]["A"]})
        self.assertEqual(sorted(labels[0].values()), sorted([NEW, OLD]))
        shown = {NEW: BETTER, OLD: PLAIN}
        for session, label in zip(self.sessions()[:3], labels):
            self.assertEqual((session["a"], session["b"]), (shown[label["A"]], shown[label["B"]]))

    def test_the_winner_is_unblinded(self):
        pair = self.pair()
        self.assertEqual([s["winner"] for s in pair["sessions"]], [NEW, NEW, NEW])
        self.assertEqual(pair["verdict"], NEW)
        summary = self.comparison()["summary"]
        self.assertEqual(summary["verdicts"], {NEW: 2, OLD: 0, "tie": 0, "split": 0, "pending": 0})
        self.assertEqual(summary["label_wins"], {"A": 4, "B": 2, "tie": 0})

    def test_scores_assertions_and_reasons_are_mapped_to_the_versions(self):
        folder = self.comparisons()[0] / "answer/run-1/session-1"
        recorded = json.loads((folder / "session.json").read_text(encoding="utf-8"))
        shown_a, shown_b = recorded["labels"]["A"], recorded["labels"]["B"]
        answer = recorded["answer"]
        self.assertEqual(answer["scores"][shown_a], {"correctness": 4, "completeness": 4, "form": 4})
        self.assertEqual(answer["scores"][shown_b], {"correctness": 3, "completeness": 3, "form": 3})
        self.assertEqual(answer["assertions"][1], {"text": ASSERTIONS[1], "passed": {shown_a: True, shown_b: False},
                                                   "evidence": "seen 2"})
        self.assertEqual(answer["strengths"], {shown_a: ["strength of A"], shown_b: []})
        self.assertEqual(answer["weaknesses"], {shown_a: [], shown_b: ["weakness of B"]})
        self.assertEqual(answer["reason"], "A answers better")
        # The new version is shown as A in sessions 1 and 3 of each pair: 3 + 2 + 3 passed, then 2 + 3 + 2.
        summary = self.comparison()["summary"]
        self.assertEqual(summary["assertions"], {NEW: {"passed": 16, "checked": 18},
                                                 OLD: {"passed": 14, "checked": 18}})

    def test_the_comparison_is_written_with_its_key(self):
        text = (self.comparisons()[0] / "comparison.md").read_text(encoding="utf-8")
        self.assertIn(f"`{NEW}`", text)
        self.assertIn(f"`{OLD}`", text)
        self.assertIn("A answers better", text)
        recorded = self.comparison()
        self.assertEqual([v["name"] for v in recorded["versions"]], [NEW, OLD])
        self.assertEqual(recorded["sessions_per_pair"], 3)
        self.assertAlmostEqual(recorded["summary"]["cost_usd"], 6 * SESSION_COST)

    def test_the_sessions_files_are_kept(self):
        folder = self.comparisons()[0] / "answer/run-1/session-2"
        for name in ("prompt.md", "response.md", "result.json", "transcript.jsonl", "transcript.md", "session.json"):
            self.assertTrue((folder / name).is_file(), name)
        recorded = json.loads((folder / "session.json").read_text(encoding="utf-8"))
        self.assertEqual((recorded["agent"], recorded["model"], recorded["effort"]),
                         ("test-comparator", "claude-sonnet-5-5", "high"))
        self.assertAlmostEqual(recorded["cost_usd"], SESSION_COST)

    def test_a_complete_session_is_skipped(self):
        code, out, _ = self.start()
        self.assertEqual(code, 0)
        self.assertIn("0 comparator sessions to start", out)
        self.assertEqual(len(self.sessions()), 6)
        self.assertEqual(len(self.comparisons()), 1)


class Draw(Case):
    def test_the_first_sessions_labels_are_drawn(self):
        for index, shown_first in ((0, NEW), (1, OLD)):
            with self.subTest(shown_first=shown_first):
                for folder in self.comparisons():
                    shutil.rmtree(folder)
                draw = mock.Mock(choice=lambda options, index=index: options[index])
                with mock.patch.object(compare, "DRAW", draw):
                    self.start("--case", "answer")
                self.assertEqual(self.pair()["labels"][0]["A"], shown_first)


class Answers(Case):
    def test_a_verdict_needs_two_sessions_that_agree(self):
        # The labels alternate, so "A, tie, B" gives the first version, a tie, then the first again,
        # and "A, B, A" the version shown first in sessions 1 and 3 three times.
        for winners, expected in (("A,tie,B", "split"), ("tie,tie,A", "tie"), ("A,A,A", None)):
            with self.subTest(winners=winners):
                for folder in self.comparisons():
                    shutil.rmtree(folder)
                self.log.unlink(missing_ok=True)
                self.start("--case", "answer", STUB_WINNERS=winners)
                pair = self.pair()
                first = pair["labels"][0]["A"]
                if winners == "A,tie,B":
                    self.assertEqual([s["winner"] for s in pair["sessions"]],
                                     [first, "tie", pair["labels"][0]["B"]])
                if expected is None:
                    expected = first
                self.assertEqual(pair["verdict"], expected)

    def test_an_unreadable_answer_is_started_again_with_the_same_labels(self):
        _, out, _ = self.start(STUB_ANSWER="A is better.")
        self.assertIn("answer/run-1/session-1: stopped (unreadable answer", out)
        labels = self.pair()["labels"]
        self.assertIsNone(self.pair()["verdict"])
        self.assertEqual(self.comparison()["summary"]["verdicts"]["pending"], 2)
        _, out, _ = self.main(self.iteration)
        self.assertIn("6 comparator sessions to start", out)
        self.start()
        self.assertEqual(self.pair()["labels"], labels)
        self.assertEqual(self.pair()["verdict"], NEW)
        self.assertEqual(len(self.comparisons()), 1)

    GOOD = {"winner": "A", "reason": "r",
            "A": {"correctness": 4, "completeness": 4, "form": 4, "strengths": ["s"], "weaknesses": []},
            "B": {"correctness": 3, "completeness": 3, "form": 3, "strengths": [], "weaknesses": ["w"]},
            "assertions": [{"assertion": n, "A": True, "B": True, "evidence": "e"} for n in (1, 2, 3)]}

    def test_answers_that_cannot_serve_are_refused(self):
        good = self.GOOD
        without = {key: value for key, value in good["B"].items() if key != "weaknesses"}
        broken = {
            "winner C": {**good, "winner": "C"},
            "no reason": {**good, "reason": " "},
            "a score of 6": {**good, "B": {**good["B"], "correctness": 6}},
            "a criterion missing": {**good, "A": {k: v for k, v in good["A"].items() if k != "completeness"}},
            "no weaknesses for B": {**good, "B": without},
            "strengths not a list": {**good, "A": {**good["A"], "strengths": "s"}},
            "assertion 3 not compared": {**good, "assertions": good["assertions"][:2]},
            "an assertion without B": {**good, "assertions": [{"assertion": 1, "A": True, "evidence": "e"},
                                                               *good["assertions"][1:]]},
            "the earlier format": {"winner": "A", "reason": "r", "assertions": good["assertions"],
                                   "scores": {"A": {"correctness": 4, "completeness": 4, "form": 4},
                                              "B": {"correctness": 3, "completeness": 3, "form": 3}},
                                   "strengths": {"A": [], "B": []}, "weaknesses": {"A": [], "B": []}},
        }
        self.assertEqual(compare.read_answer(json.dumps(good), 3)["winner"], "A")
        self.assertEqual(compare.read_answer(json.dumps({**good, "winner": "TIE"}), 3)["winner"], "tie")
        for name, answer in broken.items():
            with self.subTest(name), self.assertRaises(compare.AnswerError):
                compare.read_answer(json.dumps(answer), 3)

    def test_an_object_left_open_is_refused_though_the_json_parses(self):
        # Seen on 2026-10-08: an object left open, closed by an extra brace at the end, puts the
        # next key inside it; the JSON still parses.
        good = self.GOOD
        a_open = {key: value for key, value in good.items() if key != "B"}
        a_open["A"] = {**good["A"], "B": good["B"]}
        b_open = {key: value for key, value in good.items() if key != "assertions"}
        b_open["B"] = {**good["B"], "assertions": good["assertions"]}
        for name, answer, said in (("A left open", a_open, "`A` holds `B`"),
                                   ("B left open", b_open, "`B` holds `assertions`")):
            with self.subTest(name):
                with self.assertRaises(compare.AnswerError) as caught:
                    compare.read_answer(json.dumps(answer), 3)
                self.assertIn(said, str(caught.exception))

    def test_a_score_and_its_lists_are_read_per_output(self):
        answer = compare.read_answer(json.dumps(self.GOOD), 3)
        self.assertEqual(answer["scores"], {"A": {"correctness": 4, "completeness": 4, "form": 4},
                                            "B": {"correctness": 3, "completeness": 3, "form": 3}})
        self.assertEqual(answer["strengths"], {"A": ["s"], "B": []})
        self.assertEqual(answer["weaknesses"], {"A": [], "B": ["w"]})

    def test_a_stopped_session_counts_for_no_version(self):
        _, out, _ = self.start(STUB_SUBTYPE="error_max_budget_usd")
        self.assertIn("answer/run-1/session-1: stopped (error_max_budget_usd)", out)
        pair = self.pair()
        self.assertEqual([s["winner"] for s in pair["sessions"]], [None, None, None])
        self.assertIsNone(pair["verdict"])

    def test_two_other_versions_get_their_own_comparison(self):
        self.start("--case", "answer")
        first, second = self.skill_only(BETTER), self.skill_only(PLAIN)
        code, _, err = self.main(first, second, "--start", "--jobs", "1", "--case", "answer")
        self.assertEqual(code, 0, err)
        self.assertEqual([p.name for p in self.comparisons()], ["comparison-1", "comparison-2"])
        self.assertEqual([v["name"] for v in self.comparison(2)["versions"]],
                         ["iteration-2/with_skill", "iteration-3/with_skill"])
        self.assertEqual(self.pair(number=2)["verdict"], "iteration-2/with_skill")



class Agent(unittest.TestCase):
    def test_the_agent_is_found_beside_the_skills_folder(self):
        self.assertEqual(compare.AGENT, SCRIPTS.parents[2] / "agents" / "skill-comparator.md")
        agent = grade.read_agent(compare.AGENT)
        self.assertEqual((agent.name, agent.tools, agent.model, agent.effort),
                         ("skill-comparator", ["Read", "Bash"], "sonnet", "xhigh"))

    def test_the_agents_example_answer_is_read(self):
        text = compare.AGENT.read_text(encoding="utf-8")
        example = text.split("```json\n", 1)[1].split("```", 1)[0]
        self.assertEqual(compare.read_answer(example, 1)["winner"], "A")


if __name__ == "__main__":
    unittest.main()
