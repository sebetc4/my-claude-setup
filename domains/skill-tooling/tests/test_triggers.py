"""Tests for triggers.py and trigger_stop.py: a skill's trigger queries run as claude -p
sessions, here a stub standing for claude, per the design of Phase 4 of roadmap
skill-tooling."""

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


triggers = load("triggers")
trigger_stop = load("trigger_stop")

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'
SHOULD = "Write a note about the standup."
SHOULD_NOT = "Explain what a B-tree is."

# The stub answers --version, then plays the calls STUB_PLAN gives the query for this run
# — {query: [[[tool, input], ...] per run]}, "{copy}" standing for the skill's copy —,
# running each PostToolUse hook of --settings after each call and stopping when one
# answers {"continue": false}, as Claude Code does. It logs what it received and made,
# writes a transcript under $CLAUDE_CONFIG_DIR/projects/ and prints a json result.
STUB = f"""#!{sys.executable}
import json, os, subprocess, sys, uuid
from pathlib import Path
args = sys.argv[1:]
if args == ["--version"]:
    print(os.environ.get("STUB_VERSION", "2.1.292") + " (Claude Code)")
    sys.exit(0)
def value(flag):
    return args[args.index(flag) + 1] if flag in args else None
cwd = Path.cwd()
prompt = sys.stdin.read()
log_path = Path(os.environ["STUB_LOG"])
earlier = [json.loads(l) for l in log_path.read_text().splitlines()] if log_path.exists() else []
index = sum(1 for e in earlier if e["prompt"] == prompt)
added = value("--add-dir")
copy = str(Path(added) / ".claude/skills/demo") if added else ""
runs = json.loads(os.environ.get("STUB_PLAN", "{{}}")).get(prompt, [[]])
plan = json.loads(json.dumps(runs[index % len(runs)]).replace("{{copy}}", copy))
settings = json.loads(value("--settings") or "{{}}")
post = [h["command"] for group in settings.get("hooks", {{}}).get("PostToolUse", []) for h in group["hooks"]]
session = value("--session-id") or str(uuid.uuid4())
model, effort = value("--model"), value("--effort")
usage = {{"input_tokens": 10, "output_tokens": 100, "cache_read_input_tokens": 1000,
          "cache_creation_input_tokens": 0}}
records = [{{"type": "user", "message": {{"role": "user", "content": prompt}}}}]
made = []
for i, (name, given) in enumerate(plan):
    records.append({{"type": "assistant", "effort": effort, "message": {{
        "id": f"msg_{{i}}", "model": model, "stop_reason": "tool_use", "usage": usage,
        "content": [{{"type": "tool_use", "id": f"tu_{{i}}", "name": name, "input": given}}]}}}})
    records.append({{"type": "user", "message": {{"role": "user", "content": [
        {{"type": "tool_result", "tool_use_id": f"tu_{{i}}", "content": "ok"}}]}}}})
    made.append(name)
    event = {{"hook_event_name": "PostToolUse", "session_id": session, "cwd": str(cwd), "tool_name": name,
              "tool_input": given}}
    stop = False
    for command in post:
        out = subprocess.run(command, shell=True, input=json.dumps(event), capture_output=True, text=True).stdout
        try:
            stop = stop or json.loads(out).get("continue") is False
        except ValueError:
            pass
    if stop:
        break
else:
    records.append({{"type": "assistant", "effort": effort, "message": {{
        "id": "msg_end", "model": model, "stop_reason": "end_turn", "usage": usage,
        "content": [{{"type": "text", "text": "An answer."}}]}}}})
files = sorted(p.relative_to(cwd).as_posix() for p in cwd.rglob("*")
               if p.is_file() and ".git" not in p.relative_to(cwd).parts)
above = [str(p) for p in cwd.parent.parents
         if (p / ".git").exists() or (p / ".agent-conventions.toml").exists()]
added_files = sorted(p.relative_to(added).as_posix() for p in Path(added).rglob("*") if p.is_file()) if added else []
log = {{"argv": args, "cwd": str(cwd), "env": dict(os.environ), "prompt": prompt, "files": files,
        "own_git": (cwd / ".git").is_dir(), "repositories_above": above, "added": added, "added_files": added_files,
        "copy_text": (Path(copy) / "SKILL.md").read_text() if copy and (Path(copy) / "SKILL.md").exists() else None,
        "made": made}}
with open(log_path, "a", encoding="utf-8") as handle:
    handle.write(json.dumps(log) + "\\n")
folder = Path(os.environ["CLAUDE_CONFIG_DIR"]) / "projects" / "-stub"
folder.mkdir(parents=True, exist_ok=True)
(folder / f"{{session}}.jsonl").write_text("".join(json.dumps(r) + "\\n" for r in records), encoding="utf-8")
print(json.dumps({{"type": "result", "subtype": "success", "is_error": False, "session_id": session,
                  "total_cost_usd": 0.0123, "duration_ms": 2000, "num_turns": len(made) + 1,
                  "result": "An answer.", "permission_denials": [],
                  **json.loads(os.environ.get("STUB_RESULT", "{{}}"))}}))
"""
# Each call of the stub costs 10 input, 100 output and 1,000 cache-read tokens on Opus 5.5.
CALL_COST = (10 * 4.0 + 100 * 20.0 + 1000 * 0.20) / 1e6
LIMIT = {"subtype": "success", "is_error": True, "api_error_status": 429, "api_error": "usage_limit_reached",
         "terminal_reason": "api_error", "result": "You've hit your session limit · resets 5:40pm (Europe/Paris)"}
SKILL_CALL = ["Skill", {"skill": "demo"}]
READ_COPY = ["Read", {"file_path": "{copy}/SKILL.md"}]
LS = ["Bash", {"command": "ls"}]


class Case(unittest.TestCase):
    """A git repository holding the skill demo with trigger queries, a configuration folder
    holding personal skills, and the stub."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo = self.tmp / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\n")
        self.write("README.md", "The repository.\n")
        self.write(".claude/settings.json", "{}\n")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: Writes notes. Use when asked for a "
                   "note.\nlicense: MIT\n---\n\nThe body.\n")
        self.write("skills/demo/evals/evals.json", json.dumps({
            "skill_name": "demo", "env": {"CLAUDE_DIR": "{tmp}/claude"},
            "evals": [{"id": 1, "name": "one", "kind": "task", "setup": "empty", "prompt": "Do it.",
                       "expected_output": "Done."}],
            "triggers": [{"query": SHOULD, "should_trigger": True},
                         {"query": SHOULD_NOT, "should_trigger": False, "near": "the index"}]}, indent=1))
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "first")
        self.config = self.tmp / "config"
        for name, text in (("other", "---\nname: other\ndescription: Other.\n---\n"),
                           ("demo", "---\nname: demo\ndescription: Installed.\n---\n")):
            (self.config / "skills" / name).mkdir(parents=True)
            (self.config / "skills" / name / "SKILL.md").write_text(text, encoding="utf-8")
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        stub = bin_dir / "claude"
        stub.write_text(STUB, encoding="utf-8")
        stub.chmod(0o755)
        self.log = self.tmp / "stub.log"
        self.enterContext(mock.patch.dict(os.environ, {
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "CLAUDE_CONFIG_DIR": str(self.config),
            "STUB_LOG": str(self.log), "CLAUDECODE": "1", "CLAUDE_EFFORT": "max",
            "CLAUDE_CODE_SESSION_ATTENDED": "1"}))
        self.plan({SHOULD: [[SKILL_CALL]], SHOULD_NOT: [[LS]]})

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
                              env=GIT_ENV).stdout.strip()

    def plan(self, plan):
        self.enterContext(mock.patch.dict(os.environ, {"STUB_PLAN": json.dumps(plan)}))

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = triggers.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def sessions(self, prompt=None):
        if not self.log.exists():
            return []
        found = [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]
        return [s for s in found if prompt is None or s["prompt"] == prompt]

    def results(self):
        found = sorted((self.repo / ".eval-runs/skills/demo/triggers").glob("*.json"))
        return [json.loads(p.read_text(encoding="utf-8")) for p in found]

    def query(self, result, text):
        return next(q for q in result["queries"] if q["query"] == text)


class Announce(Case):
    def test_nothing_starts_without_start(self):
        code, out, _ = self.main(self.skill)
        self.assertEqual(code, 0)
        self.assertEqual(self.sessions(), [])
        self.assertIn("6 sessions: 2 queries × 3 runs", out)
        # A near miss is answered in full: its sessions are estimated apart.
        self.assertIn(f"estimated ${0.09 + 2 * 0.008 + 0.12 + 2 * 0.04:.2f}", out)
        self.assertIn("--start", out)
        self.assertFalse((self.repo / ".eval-runs").exists())

    def test_the_runs_per_query_can_be_fewer(self):
        _, out, _ = self.main(self.skill, "--runs", "1")
        self.assertIn("2 sessions: 2 queries × 1 run", out)
        self.assertIn(f"estimated ${0.09 + 0.12:.2f}", out)

    def test_the_estimate_follows_the_skills_recorded_sessions(self):
        self.main(self.skill, "--start", "--runs", "2")
        _, out, _ = self.main(self.skill)
        # A first session and a repeat of each query: one call where the skill triggers, two where not.
        self.assertIn(f"estimated ${2 * 1.5 * CALL_COST + 4 * 1.5 * CALL_COST:.2f}", out)
        self.assertIn("recorded", out)
        _, out, _ = self.main(self.skill, "--effort", "max")
        self.assertIn(f"estimated ${0.09 + 2 * 0.008 + 0.12 + 2 * 0.04:.2f}", out)

    def test_the_estimate_keeps_each_class_apart(self):
        self.main(self.skill, "--start", "--runs", "2")
        data = json.loads((self.skill / "evals/evals.json").read_text())
        data["triggers"] += [{"query": "Explain a hash index.", "should_trigger": False},
                             {"query": "Explain a GiST index.", "should_trigger": False}]
        (self.skill / "evals/evals.json").write_text(json.dumps(data))
        _, out, _ = self.main(self.skill)
        # One call a session where the skill triggers, two where it does not: 3 sessions of
        # the one query that should trigger, 9 of the three that should not.
        self.assertIn(f"estimated ${3 * CALL_COST + 9 * 2 * CALL_COST:.2f}", out)

    def test_the_estimate_never_passes_the_ceiling(self):
        _, out, _ = self.main(self.skill, "--budget", "0.05")
        self.assertIn(f"estimated ${0.05 + 2 * 0.008 + 0.05 + 2 * 0.04:.2f}", out)

    def test_a_skill_without_trigger_queries_is_refused(self):
        data = json.loads((self.skill / "evals/evals.json").read_text())
        del data["triggers"]
        (self.skill / "evals/evals.json").write_text(json.dumps(data))
        code, _, err = self.main(self.skill)
        self.assertEqual(code, 1)
        self.assertIn("no trigger queries", err)

    def test_an_invalid_evals_file_is_refused(self):
        data = json.loads((self.skill / "evals/evals.json").read_text())
        data["triggers"][0]["sure"] = True
        (self.skill / "evals/evals.json").write_text(json.dumps(data))
        code, _, err = self.main(self.skill)
        self.assertEqual(code, 1)
        self.assertIn("unknown key `sure`", err)

    def test_an_old_claude_is_refused_before_any_session(self):
        with mock.patch.dict(os.environ, {"STUB_VERSION": "2.1.283"}):
            code, _, err = self.main(self.skill, "--start")
        self.assertEqual(code, 1)
        self.assertIn("2.1.291", err)
        self.assertEqual(self.sessions(), [])


class Sessions(Case):
    def setUp(self):
        super().setUp()
        self.claude_before = sorted(p.relative_to(self.repo).as_posix() for p in (self.repo / ".claude").rglob("*"))
        self.code, self.out, self.err = self.main(self.skill, "--start")

    def test_each_query_runs_the_set_number_of_times(self):
        self.assertEqual(self.code, 0, self.err)
        self.assertEqual(len(self.sessions(SHOULD)), 3)
        self.assertEqual(len(self.sessions(SHOULD_NOT)), 3)
        self.assertEqual(len(self.sessions()), 6)

    def test_the_prompt_is_the_query_alone(self):
        self.assertEqual({s["prompt"] for s in self.sessions()}, {SHOULD, SHOULD_NOT})

    def test_a_querys_runs_share_one_folder_and_queries_do_not(self):
        should = {s["cwd"] for s in self.sessions(SHOULD)}
        should_not = {s["cwd"] for s in self.sessions(SHOULD_NOT)}
        self.assertEqual(len(should), 1)
        self.assertEqual(len(should_not), 1)
        self.assertNotEqual(should, should_not)

    def test_the_skill_is_passed_from_a_temporary_folder(self):
        for session in self.sessions():
            argv = session["argv"]
            added = Path(argv[argv.index("--add-dir") + 1])
            self.assertFalse(added.is_relative_to(self.repo))
            self.assertFalse(added.exists(), "the temporary folder was left behind")
            self.assertIn(".claude/skills/demo/SKILL.md", session["added_files"])
            self.assertFalse([f for f in session["added_files"] if "/evals/" in f])

    def test_the_other_personal_skills_come_with_the_copy_and_the_installed_one_does_not(self):
        session = self.sessions()[0]
        self.assertIn(".claude/skills/other/SKILL.md", session["added_files"])
        self.assertIn("description: Writes notes.", session["copy_text"])
        self.assertNotIn("Installed.", session["copy_text"])

    def test_the_session_starts_in_a_copy_of_the_repository_without_the_skill(self):
        for session in self.sessions():
            self.assertIn("README.md", session["files"])
            self.assertFalse([f for f in session["files"] if f.startswith("skills/demo")])
            self.assertTrue(session["own_git"])
            self.assertEqual(session["repositories_above"], [])
            self.assertFalse(Path(session["cwd"]).is_relative_to(self.repo))

    def test_the_command_takes_a_runs_flags_but_the_denied_tools(self):
        for session in self.sessions():
            argv = session["argv"]
            for flag, value in (("--model", "claude-opus-5-5"), ("--effort", "xhigh"),
                                ("--permission-mode", "auto"), ("--permission-prompts", "none"),
                                ("--setting-sources", "project,local"), ("--output-format", "json")):
                self.assertEqual(argv[argv.index(flag) + 1], value, flag)
            self.assertIn("--strict-mcp-config", argv)
            self.assertNotIn("--disallowed-tools", argv)
            settings = json.loads(argv[argv.index("--settings") + 1])
            self.assertIs(settings["autoMemoryEnabled"], False)
            self.assertIn("guard.py", settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"])
            self.assertIn("trigger_stop.py", settings["hooks"]["PostToolUse"][0]["hooks"][0]["command"])
            for name in ("CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED"):
                self.assertNotIn(name, session["env"])
            self.assertTrue(session["env"]["CLAUDE_DIR"].endswith("/claude"))
            self.assertFalse(Path(session["env"]["CLAUDE_DIR"]).is_relative_to(self.repo))

    def test_nothing_is_written_into_the_projects_claude_folder(self):
        after = sorted(p.relative_to(self.repo).as_posix() for p in (self.repo / ".claude").rglob("*"))
        self.assertEqual(after, self.claude_before)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_the_results_give_a_rate_per_query(self):
        [result] = self.results()
        should, should_not = self.query(result, SHOULD), self.query(result, SHOULD_NOT)
        self.assertEqual((should["rate"], should["passed"]), (1.0, True))
        self.assertEqual((should_not["rate"], should_not["passed"]), (0.0, True))
        self.assertEqual(should_not["near"], "the index")
        self.assertEqual(len(should["sessions"]), 3)
        self.assertEqual(result["model"], "claude-opus-5-5")
        self.assertEqual(result["effort"], "xhigh")
        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["sessions"], 6)
        self.assertAlmostEqual(result["summary"]["cost_usd"], 3 * CALL_COST + 3 * 2 * CALL_COST)
        self.assertIn("1.00", self.out)
        self.assertIn(SHOULD_NOT, self.out)


class Rates(Case):
    def test_the_rate_is_the_share_of_runs_that_triggered(self):
        self.plan({SHOULD: [[SKILL_CALL], [LS], [READ_COPY]], SHOULD_NOT: [[LS], [LS], [SKILL_CALL]]})
        self.main(self.skill, "--start")
        [result] = self.results()
        should, should_not = self.query(result, SHOULD), self.query(result, SHOULD_NOT)
        self.assertAlmostEqual(should["rate"], 2 / 3)
        self.assertTrue(should["passed"])
        self.assertEqual([s["triggered"] for s in should["sessions"]], [True, False, True])
        self.assertAlmostEqual(should_not["rate"], 1 / 3)
        self.assertTrue(should_not["passed"])
        self.assertEqual(result["summary"]["passed"], 2)

    def test_a_query_fails_against_half(self):
        self.plan({SHOULD: [[LS], [LS], [SKILL_CALL]], SHOULD_NOT: [[SKILL_CALL], [LS], [SKILL_CALL]]})
        self.main(self.skill, "--start")
        [result] = self.results()
        self.assertFalse(self.query(result, SHOULD)["passed"])
        self.assertFalse(self.query(result, SHOULD_NOT)["passed"])
        self.assertEqual(result["summary"]["passed"], 0)

    def test_a_trigger_after_the_third_call_is_not_counted_and_the_session_stops_at_it(self):
        self.plan({SHOULD: [[LS, LS, LS, SKILL_CALL, LS]], SHOULD_NOT: [[LS]]})
        self.main(self.skill, "--start", "--runs", "1")
        self.assertEqual(self.sessions(SHOULD)[0]["made"], ["Bash", "Bash", "Bash"])
        [result] = self.results()
        self.assertEqual(self.query(result, SHOULD)["rate"], 0.0)

    def test_the_session_stops_at_the_trigger(self):
        self.plan({SHOULD: [[LS, SKILL_CALL, LS, LS]], SHOULD_NOT: [[LS]]})
        self.main(self.skill, "--start", "--runs", "1")
        self.assertEqual(self.sessions(SHOULD)[0]["made"], ["Bash", "Skill"])
        [result] = self.results()
        session = self.query(result, SHOULD)["sessions"][0]
        self.assertTrue(session["triggered"])
        self.assertEqual(session["trigger_call"], 2)

    def test_a_read_of_the_skills_source_is_recorded_not_counted(self):
        source = ["Read", {"file_path": "skills/demo/SKILL.md"}]
        self.plan({SHOULD: [[source]], SHOULD_NOT: [[LS]]})
        self.main(self.skill, "--start", "--runs", "1")
        [result] = self.results()
        session = self.query(result, SHOULD)["sessions"][0]
        self.assertFalse(session["triggered"])
        self.assertEqual(session["source_reads"], ["skills/demo/SKILL.md"])

    def test_another_skill_does_not_count(self):
        self.plan({SHOULD: [[["Skill", {"skill": "other"}]]], SHOULD_NOT: [[LS]]})
        self.main(self.skill, "--start", "--runs", "1")
        [result] = self.results()
        self.assertFalse(self.query(result, SHOULD)["sessions"][0]["triggered"])


class Description(Case):
    def test_a_description_given_replaces_the_copys_and_is_recorded(self):
        given = self.tmp / "description.txt"
        given.write_text("Takes notes: \"quoted\" and colons. Use for any note.\n", encoding="utf-8")
        self.main(self.skill, "--start", "--runs", "1", "--description", given)
        text = self.sessions()[0]["copy_text"]
        self.assertIn('description: "Takes notes: \\"quoted\\" and colons. Use for any note."', text)
        self.assertIn("name: demo", text)
        self.assertIn("license: MIT", text)
        self.assertIn("The body.", text)
        self.assertNotIn("Writes notes.", text)
        self.assertIn("Writes notes.", (self.skill / "SKILL.md").read_text())
        [result] = self.results()
        self.assertEqual(result["description"], "Takes notes: \"quoted\" and colons. Use for any note.")

    def test_without_one_the_skills_own_is_recorded(self):
        self.main(self.skill, "--start", "--runs", "1")
        [result] = self.results()
        self.assertEqual(result["description"], "Writes notes. Use when asked for a note.")


class Limit(Case):
    def test_the_limit_leaves_the_sessions_left_unstarted(self):
        with mock.patch.dict(os.environ, {"STUB_RESULT": json.dumps(LIMIT)}):
            code, out, _ = self.main(self.skill, "--start", "--jobs", "1")
        self.assertEqual(code, 0)
        self.assertEqual(len(self.sessions()), 1)
        self.assertIn("limit", out)
        [result] = self.results()
        self.assertEqual(result["summary"]["sessions"], 0)
        self.assertEqual(result["summary"]["not_started"], 5)
        self.assertIsNone(self.query(result, SHOULD)["rate"])


class Hook(unittest.TestCase):
    """trigger_stop.py as Claude Code runs it: one PostToolUse event on its input."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.log = self.tmp / "calls.jsonl"
        self.copy = self.tmp / "added/.claude/skills/demo"

    def event(self, tool, given):
        done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "trigger_stop.py"), str(self.log), "demo",
                               str(self.copy)], input=json.dumps({"hook_event_name": "PostToolUse",
                                                                  "tool_name": tool, "tool_input": given}),
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout) if done.stdout.strip() else None

    def test_the_skill_called_stops_the_session(self):
        self.assertIs(self.event("Skill", {"skill": "demo"})["continue"], False)

    def test_a_read_under_the_copy_stops_the_session(self):
        self.assertIs(self.event("Read", {"file_path": f"{self.copy}/SKILL.md"})["continue"], False)

    def test_other_calls_pass_until_the_third(self):
        self.assertIsNone(self.event("Skill", {"skill": "other"}))
        self.assertIsNone(self.event("Bash", {"command": "ls skills/demo"}))
        self.assertIs(self.event("Bash", {"command": "ls"})["continue"], False)
        self.assertEqual(len(self.log.read_text().splitlines()), 3)

    def test_a_copy_path_that_only_starts_alike_does_not_count(self):
        self.assertFalse(trigger_stop.triggered("Read", {"file_path": f"{self.copy}-old/SKILL.md"}, "demo",
                                                str(self.copy)))
        self.assertTrue(trigger_stop.triggered("Skill", {"skill": "demo", "args": "x"}, "demo", str(self.copy)))


if __name__ == "__main__":
    unittest.main()
