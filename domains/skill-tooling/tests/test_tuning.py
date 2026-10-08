"""Tests for tuning.py: a skill's trigger queries split into training and held-out sets,
descriptions scored on both from fixed trigger results, the best chosen on the held-out
set, and each rewrite proposed by a session that sees the training results alone, here
a stub standing for claude, per the design of Phase 4 of roadmap skill-tooling."""

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

SCRIPTS = Path(__file__).resolve().parent.parent / "skills/authoring-skills/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(f"skill_{name}", SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tuning = load("tuning")

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
DESCRIPTION = "Writes notes. Use when asked for a note."
SHOULD = ["Write a note about the standup.", "Take a note of this decision.", "Record what we agreed today.",
          "Jot down the outcome of the meeting.", "Make a note for tomorrow's review."]
SHOULD_NOT = ["Explain what a B-tree is.", "Write a README for this project.", "Summarize this file.",
              "Draft an email to the team.", "Fix the failing test."]
ANSWER = "Takes notes of meetings and decisions. Use when asked to note, record or jot something down."
MODEL = "claude-opus-5-5"

# The stub answers --version, then logs what it received, writes a transcript of one call
# under $CLAUDE_CONFIG_DIR/projects/ and prints a json result whose text is STUB_ANSWER.
STUB = f"""#!{sys.executable}
import json, os, sys, uuid
from pathlib import Path
args = sys.argv[1:]
if args == ["--version"]:
    print(os.environ.get("STUB_VERSION", "2.1.292") + " (Claude Code)")
    sys.exit(0)
def value(flag):
    return args[args.index(flag) + 1] if flag in args else None
cwd = Path.cwd()
prompt = sys.stdin.read()
session = value("--session-id") or str(uuid.uuid4())
answer = os.environ["STUB_ANSWER"]
above = [str(p) for p in cwd.parents if (p / ".git").exists() or (p / ".agent-conventions.toml").exists()]
log = {{"argv": args, "cwd": str(cwd), "env": dict(os.environ), "prompt": prompt,
        "files": sorted(p.name for p in cwd.rglob("*")), "repositories_above": above}}
with open(os.environ["STUB_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(log) + "\\n")
record = {{"type": "assistant", "effort": value("--effort"), "message": {{
    "id": "msg_1", "model": value("--model"), "stop_reason": "end_turn",
    "usage": {{"input_tokens": 1000, "output_tokens": 500, "cache_read_input_tokens": 0,
              "cache_creation_input_tokens": 0}},
    "content": [{{"type": "text", "text": answer}}]}}}}
folder = Path(os.environ["CLAUDE_CONFIG_DIR"]) / "projects" / "-stub"
folder.mkdir(parents=True, exist_ok=True)
(folder / f"{{session}}.jsonl").write_text(json.dumps(record) + "\\n", encoding="utf-8")
print(json.dumps({{"type": "result", "subtype": "success", "is_error": False, "session_id": session,
                  "total_cost_usd": 0.014, "duration_ms": 1000, "num_turns": 1, "result": answer,
                  "permission_denials": []}}))
"""
# The stub's one call: 1,000 input and 500 output tokens on Opus 5.5.
CALL_COST = (1000 * 4.0 + 500 * 20.0) / 1e6


def tagged(text):
    return f"Here it is.\n<new_description>\n{text}\n</new_description>"


class Case(unittest.TestCase):
    """A git repository holding the skill demo with ten trigger queries, a configuration
    folder, and the stub."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo = self.tmp / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\n")
        self.write("skills/demo/SKILL.md", f"---\nname: demo\ndescription: {DESCRIPTION}\n---\n\n"
                   "The body: a note opens with its status.\n")
        self.evals([{"query": q, "should_trigger": True} for q in SHOULD]
                   + [{"query": q, "should_trigger": False, "near": "writing"} for q in SHOULD_NOT])
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True, env=GIT_ENV)
        self.config = self.tmp / "config"
        self.config.mkdir()
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        stub = bin_dir / "claude"
        stub.write_text(STUB, encoding="utf-8")
        stub.chmod(0o755)
        self.log = self.tmp / "stub.log"
        self.enterContext(mock.patch.dict(os.environ, {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "CLAUDE_CONFIG_DIR": str(self.config),
            "STUB_LOG": str(self.log), "STUB_ANSWER": tagged(ANSWER), "CLAUDECODE": "1", "CLAUDE_EFFORT": "max",
            "CLAUDE_CODE_SESSION_ATTENDED": "1"}))
        self.results_made = 0

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def evals(self, triggers):
        self.write("skills/demo/evals/evals.json", json.dumps({
            "skill_name": "demo",
            "evals": [{"id": 1, "name": "one", "kind": "task", "setup": "empty", "prompt": "Do it.",
                       "expected_output": "Done."}],
            "triggers": triggers}, indent=1))

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = tuning.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def folders(self):
        found = (self.repo / ".eval-runs/skills/demo").glob("tuning-*/tuning.json")
        return sorted(found, key=lambda p: int(p.parent.name.split("-")[1]))

    def split(self, *options):
        code, out, err = self.main("split", self.skill, *options)
        self.assertEqual(code, 0, err)
        self.tuning = self.folders()[-1].parent
        return out

    def state(self):
        return json.loads((self.tuning / "tuning.json").read_text(encoding="utf-8"))

    def queries(self, part, should=None):
        return [q["query"] for q in self.state()[part] if should is None or q["should_trigger"] is should]

    def results(self, description, failing=(), *, model=MODEL, effort="xhigh", runs=3, skill="demo",
                unmeasured=()):
        """A triggers.py results file in which every query passes but those failing."""
        found = []
        for should, texts in ((True, SHOULD), (False, SHOULD_NOT)):
            for text in texts:
                if text in unmeasured:
                    rate, passed, hits, counted = None, None, 0, 0
                else:
                    passed = text not in failing
                    hits = runs if passed is should else 0
                    rate, counted = hits / runs, runs
                found.append({"query": text, "should_trigger": should, "triggered": hits, "counted": counted,
                              "rate": rate, "passed": passed, "sessions": []})
        self.results_made += 1
        path = self.tmp / f"results-{self.results_made}.json"
        path.write_text(json.dumps({"skill_name": skill, "description": description, "description_file": None,
                                    "model": model, "effort": effort, "runs": runs, "threshold": 0.5,
                                    "summary": {}, "queries": found}), encoding="utf-8")
        return path

    def score(self, description, failing=(), **options):
        code, out, err = self.main("score", self.tuning, self.results(description, failing, **options))
        self.assertEqual(code, 0, err)
        return out

    def propose(self, answer=ANSWER, *options):
        with mock.patch.dict(os.environ, {"STUB_ANSWER": tagged(answer)}):
            return self.main("propose", self.tuning, "--start", *options)

    def sessions(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]


class Split(Case):
    def test_each_set_holds_both_classes_sixty_forty(self):
        self.split()
        train, held_out = self.queries("train"), self.queries("held_out")
        self.assertEqual(len(self.queries("train", True)), 3)
        self.assertEqual(len(self.queries("train", False)), 3)
        self.assertEqual(len(self.queries("held_out", True)), 2)
        self.assertEqual(len(self.queries("held_out", False)), 2)
        self.assertEqual(sorted(train + held_out), sorted(SHOULD + SHOULD_NOT))
        self.assertEqual(set(train) & set(held_out), set())
        near = [q for q in self.state()["held_out"] if not q["should_trigger"]][0]
        self.assertEqual(near["near"], "writing")

    def test_the_split_is_fixed_by_its_seed(self):
        self.split()
        first = self.queries("held_out")
        self.split()
        self.assertEqual(self.queries("held_out"), first)
        self.assertEqual(len(self.folders()), 2)
        others = set()
        for seed in range(1, 6):
            self.split("--seed", seed)
            others.add(tuple(self.queries("held_out")))
        self.assertGreater(len(others), 1)

    def test_the_tuning_folder_lies_under_the_skills_workspace_with_the_description(self):
        out = self.split()
        self.assertEqual(self.tuning, self.repo / ".eval-runs/skills/demo/tuning-1")
        self.assertEqual(self.state()["description"], DESCRIPTION)
        self.assertEqual(self.state()["descriptions"], [])
        self.assertIn(str(self.tuning), out)
        self.assertIn("triggers.py", out)
        self.assertEqual(self.sessions(), [])

    def test_a_class_of_fewer_than_two_queries_is_refused(self):
        self.evals([{"query": SHOULD[0], "should_trigger": True}]
                   + [{"query": q, "should_trigger": False} for q in SHOULD_NOT])
        code, _, err = self.main("split", self.skill)
        self.assertEqual(code, 1)
        self.assertIn("1 query that should trigger", err)
        self.assertEqual(self.folders(), [])


class Score(Case):
    def setUp(self):
        super().setUp()
        self.split()

    def test_a_description_is_scored_on_both_sets(self):
        failing = [self.queries("train", True)[0], self.queries("held_out", False)[0]]
        out = self.score(DESCRIPTION, failing)
        [scored] = self.state()["descriptions"]
        self.assertEqual(scored["number"], 1)
        self.assertEqual(scored["origin"], "skill")
        self.assertEqual(scored["train"], {"passed": 5, "queries": 6})
        self.assertEqual(scored["held_out"], {"passed": 3, "queries": 4})
        self.assertEqual(scored["characters"], len(DESCRIPTION))
        self.assertEqual({q["query"]: q["set"] for q in scored["queries"]}[failing[1]], "held_out")
        self.assertIn("training 5/6", out)
        self.assertIn("held-out 3/4", out)
        self.assertIn(failing[0], out)

    def test_a_description_neither_the_skills_nor_proposed_is_given(self):
        self.score(DESCRIPTION)
        self.score("Another description.")
        self.assertEqual([d["origin"] for d in self.state()["descriptions"]], ["skill", "given"])

    def test_another_skills_results_are_refused(self):
        code, _, err = self.main("score", self.tuning, self.results(DESCRIPTION, skill="other"))
        self.assertEqual(code, 1)
        self.assertIn("other", err)
        self.assertEqual(self.state()["descriptions"], [])

    def test_a_query_left_unmeasured_is_refused(self):
        held_out = self.queries("held_out")[0]
        code, _, err = self.main("score", self.tuning, self.results(DESCRIPTION, unmeasured=[held_out]))
        self.assertEqual(code, 1)
        self.assertIn(held_out, err)
        self.assertEqual(self.state()["descriptions"], [])

    def test_another_model_effort_or_number_of_runs_is_refused(self):
        self.score(DESCRIPTION)
        for options, word in (({"model": "claude-sonnet-5-5"}, "claude-sonnet-5-5"), ({"effort": "max"}, "max"),
                              ({"runs": 2}, "2")):
            code, _, err = self.main("score", self.tuning, self.results("Another.", **options))
            self.assertEqual(code, 1, options)
            self.assertIn(word, err)
        self.assertEqual(len(self.state()["descriptions"]), 1)

    def test_a_results_file_is_scored_once(self):
        path = self.results(DESCRIPTION)
        self.main("score", self.tuning, path)
        code, _, err = self.main("score", self.tuning, path)
        self.assertEqual(code, 1)
        self.assertIn("already", err)
        self.assertEqual(len(self.state()["descriptions"]), 1)


class Best(Case):
    def setUp(self):
        super().setUp()
        self.split()

    def test_the_best_on_held_out_queries_wins_over_the_best_on_training(self):
        self.score(DESCRIPTION, self.queries("held_out")[:2])
        self.score("Takes notes when asked.", self.queries("train")[:2])
        self.score("Notes.", self.queries("train")[:1] + self.queries("held_out")[:1])
        code, out, err = self.main("best", self.tuning)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.state()["best"], 2)
        self.assertIn("description 2", out)
        self.assertIn("Takes notes when asked.", out)
        self.assertIn("training 6/6", out)
        self.assertIn("held-out 4/4", out)

    def test_a_tie_goes_to_the_shorter(self):
        self.score(DESCRIPTION, self.queries("held_out")[:1])
        self.score("A longer description than the skill's own, for notes.", self.queries("held_out")[1:2])
        self.score("Takes notes.", self.queries("train")[:3] + self.queries("held_out")[2:3])
        _, out, _ = self.main("best", self.tuning)
        self.assertEqual(self.state()["best"], 3)
        self.assertIn("Takes notes.", out)

    def test_nothing_scored_is_refused(self):
        code, _, err = self.main("best", self.tuning)
        self.assertEqual(code, 1)
        self.assertIn("score", err)


class Propose(Case):
    def setUp(self):
        super().setUp()
        self.split()
        self.train_failing = self.queries("train", True)[0]
        self.held_failing = self.queries("held_out", True)[0]
        self.score(DESCRIPTION, [self.train_failing, self.held_failing])

    def test_nothing_starts_without_start(self):
        code, out, _ = self.main("propose", self.tuning)
        self.assertEqual(code, 0)
        self.assertEqual(self.sessions(), [])
        self.assertIn("1 session", out)
        self.assertIn("$0.10", out)
        self.assertIn("--start", out)
        self.assertEqual(self.state().get("proposals", []), [])

    def test_the_session_has_no_tool_and_starts_in_an_empty_folder_outside_any_repository(self):
        code, _, err = self.propose()
        self.assertEqual(code, 0, err)
        [session] = self.sessions()
        argv = session["argv"]
        self.assertEqual(argv[argv.index("--tools") + 1], "")
        for flag, value in (("--model", MODEL), ("--effort", "xhigh"), ("--setting-sources", "project,local")):
            self.assertEqual(argv[argv.index(flag) + 1], value, flag)
        self.assertIn("--strict-mcp-config", argv)
        self.assertIs(json.loads(argv[argv.index("--settings") + 1])["autoMemoryEnabled"], False)
        self.assertEqual(session["files"], [])
        self.assertEqual(session["repositories_above"], [])
        self.assertFalse(Path(session["cwd"]).exists(), "the temporary folder was left behind")
        for name in ("CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED"):
            self.assertNotIn(name, session["env"])

    def test_the_prompt_holds_the_training_results_and_no_held_out_query(self):
        self.propose()
        prompt = self.sessions()[0]["prompt"]
        self.assertIn("The body: a note opens with its status.", prompt)
        self.assertIn(DESCRIPTION, prompt)
        self.assertIn(self.train_failing, prompt)
        self.assertIn("<new_description>", prompt)
        for query in self.queries("held_out"):
            self.assertNotIn(query, prompt)
        self.assertNotIn("held", prompt.lower())

    def test_the_answer_becomes_a_proposal_to_measure(self):
        _, out, _ = self.propose()
        [proposal] = self.state()["proposals"]
        self.assertEqual((proposal["number"], proposal["status"], proposal["rewrote"]), (1, "proposed", 1))
        self.assertEqual(proposal["description"], ANSWER)
        self.assertEqual((self.tuning / proposal["file"]).read_text(encoding="utf-8").strip(), ANSWER)
        self.assertAlmostEqual(proposal["cost_usd"], CALL_COST)
        self.assertEqual(proposal["model"], MODEL)
        self.assertIn(f"--description {self.tuning / proposal['file']}", out)
        self.assertIn(ANSWER, out)
        self.score(ANSWER, [self.held_failing])
        self.assertEqual(self.state()["descriptions"][1]["origin"], "proposal 1")

    def test_the_estimate_follows_the_recorded_proposals(self):
        self.propose()
        self.score(ANSWER, [self.train_failing])
        _, out, _ = self.main("propose", self.tuning)
        self.assertIn(f"${CALL_COST:.2f}", out)
        self.assertIn("recorded", out)

    def test_notes_reach_the_prompt(self):
        notes = self.tmp / "notes.md"
        notes.write_text("The user wants meetings named first.\n", encoding="utf-8")
        self.propose(ANSWER, "--notes", notes)
        self.assertIn("The user wants meetings named first.", self.sessions()[0]["prompt"])

    def test_notes_that_quote_a_held_out_query_are_refused(self):
        notes = self.tmp / "notes.md"
        notes.write_text(f"Make sure that   {self.held_failing.upper()} triggers.\n", encoding="utf-8")
        code, _, err = self.propose(ANSWER, "--notes", notes)
        self.assertEqual(code, 1)
        self.assertIn("held-out", err)
        self.assertEqual(self.sessions(), [])

    def test_an_unusable_answer_is_refused_and_recorded(self):
        for answer, word in (("", "no description"), ("x" * 1025, "1,024"), (DESCRIPTION, "description 1")):
            with mock.patch.dict(os.environ, {"STUB_ANSWER": tagged(answer) if answer else "No tags here."}):
                code, _, err = self.main("propose", self.tuning, "--start")
            self.assertEqual(code, 1, answer)
            self.assertIn(word, err)
        proposals = self.state()["proposals"]
        self.assertEqual([p["status"] for p in proposals], ["refused"] * 3)
        self.assertFalse(any(p.get("file") for p in proposals))
        code, _, err = self.propose()
        self.assertEqual(code, 0, err)

    def test_a_proposal_waits_for_its_measure(self):
        self.propose()
        code, _, err = self.propose("Another rewrite.")
        self.assertEqual(code, 1)
        self.assertIn("proposal 1", err)
        self.assertEqual(len(self.sessions()), 1)

    def test_the_rewrite_starts_from_the_best_on_training(self):
        self.propose()
        self.score(ANSWER, self.queries("train")[:2])
        self.propose("Second rewrite.")
        second = self.state()["proposals"][1]
        self.assertEqual(second["rewrote"], 1)
        prompt = self.sessions()[1]["prompt"]
        self.assertIn(ANSWER, prompt)

    def test_nothing_scored_is_refused(self):
        self.split()
        code, _, err = self.propose()
        self.assertEqual(code, 1)
        self.assertIn("score", err)
        self.assertEqual(self.sessions(), [])

    def test_a_training_set_that_all_passes_stops_the_loop(self):
        self.propose()
        self.score(ANSWER, [self.held_failing])
        code, _, err = self.propose("Another rewrite.")
        self.assertEqual(code, 1)
        self.assertIn("every training query", err)

    def test_two_rewrites_in_a_row_without_gain_stop_the_loop(self):
        train = self.queries("train")
        self.propose("First rewrite.")
        self.score("First rewrite.", train[:1])
        code, _, err = self.propose("Second rewrite.")
        self.assertEqual(code, 0, err)
        self.score("Second rewrite.", train[:2])
        code, _, err = self.propose("Third rewrite.")
        self.assertEqual(code, 1)
        self.assertIn("two rewrites in a row", err)
        self.assertEqual(len(self.sessions()), 2)

    def test_a_sixth_rewrite_is_refused(self):
        self.split()
        train = self.queries("train")
        self.score(DESCRIPTION, train)
        for n in range(1, 6):
            code, _, err = self.propose(f"Rewrite {n}.")
            self.assertEqual(code, 0, err)
            self.score(f"Rewrite {n}.", train[n:])
        code, _, err = self.propose("Rewrite 6.")
        self.assertEqual(code, 1)
        self.assertIn("five rewrites", err)
        self.assertEqual(len(self.sessions()), 5)

    def test_an_old_claude_is_refused_before_any_session(self):
        with mock.patch.dict(os.environ, {"STUB_VERSION": "2.1.283"}):
            code, _, err = self.propose()
        self.assertEqual(code, 1)
        self.assertIn("2.1.291", err)
        self.assertEqual(self.sessions(), [])


if __name__ == "__main__":
    unittest.main()
