"""Tests for run.py, harness.py and guard.py: an iteration's runs started as claude -p
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


workspace = load("workspace")
harness = load("harness")
run = load("run")

GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
           "GIT_COMMITTER_NAME": "dev", "GIT_COMMITTER_EMAIL": "dev@example.com"}
CONVENTIONS = '[skills]\ndirs = ["skills"]\nevals = "evals"\nworkspace = ".eval-runs"\n'

# The stub answers --version, logs what it received, changes its folder, writes a
# transcript under $CLAUDE_CONFIG_DIR/projects/ and prints a json result.
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
files = sorted(p.relative_to(cwd).as_posix() for p in cwd.rglob("*")
               if p.is_file() and ".git" not in p.relative_to(cwd).parts)
above = [str(p) for p in cwd.parent.parents
         if (p / ".git").exists() or (p / ".agent-conventions.toml").exists()]
skill = value("--add-dir")
log = {{"argv": args, "cwd": str(cwd), "env": dict(os.environ), "prompt": sys.stdin.read(), "files": files,
        "own_git": (cwd / ".git").is_dir(), "repositories_above": above,
        "skill_files": sorted(p.relative_to(skill).as_posix() for p in Path(skill).rglob("*") if p.is_file())
        if skill else None,
        "skill_text": (Path(skill) / "SKILL.md").read_text() if skill else None,
        "repository_skill_text": (cwd / "skills/demo/SKILL.md").read_text()
        if (cwd / "skills/demo/SKILL.md").exists() else None}}
with open(os.environ["STUB_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(log) + "\\n")
(cwd / "answer.txt").write_text("answer\\n", encoding="utf-8")
if (cwd / "README.md").exists():
    (cwd / "README.md").write_text("changed\\n", encoding="utf-8")
model, effort = value("--model"), value("--effort")
calls = ([("Read", {{"file_path": skill + "/SKILL.md"}})] if skill else []) + [
    ("Write", {{"file_path": str(cwd / "answer.txt"), "content": "answer\\n"}})]
usage = {{"input_tokens": 10, "output_tokens": 100, "cache_read_input_tokens": 1000,
          "cache_creation_input_tokens": 0}}
records = [{{"type": "user", "message": {{"role": "user", "content": "the prompt"}}}}]
for i, (name, given) in enumerate(calls):
    records.append({{"type": "assistant", "effort": effort, "message": {{
        "id": f"msg_{{i}}", "model": model, "stop_reason": "tool_use", "usage": usage,
        "content": [{{"type": "tool_use", "id": f"tu_{{i}}", "name": name, "input": given}}]}}}})
    records.append({{"type": "user", "message": {{"role": "user", "content": [
        {{"type": "tool_result", "tool_use_id": f"tu_{{i}}", "content": "ok"}}]}}}})
records.append({{"type": "assistant", "effort": effort, "message": {{
    "id": "msg_end", "model": model, "stop_reason": "end_turn", "usage": usage,
    "content": [{{"type": "text", "text": "Done: wrote answer.txt."}}]}}}})
session = str(uuid.uuid4())
folder = Path(os.environ["CLAUDE_CONFIG_DIR"]) / "projects" / "-stub"
folder.mkdir(parents=True, exist_ok=True)
(folder / f"{{session}}.jsonl").write_text("".join(json.dumps(r) + "\\n" for r in records), encoding="utf-8")
subtype = os.environ.get("STUB_SUBTYPE", "success")
print(json.dumps({{"type": "result", "subtype": subtype, "is_error": subtype != "success",
                  "session_id": session, "total_cost_usd": 0.0123, "duration_ms": 4000, "num_turns": 3,
                  "result": "Done: wrote answer.txt.",
                  "permission_denials": json.loads(os.environ.get("STUB_DENIALS", "[]"))}}))
"""
# Three calls of 10 input, 100 output and 1,000 cache-read tokens on Sonnet 5.5, in dollars;
# two in a run without the skill, which reads no copy.
WITH_COST = 3 * (10 * 2.0 + 100 * 10.0 + 1000 * 0.20) / 1e6
WITHOUT_COST = 2 * (10 * 2.0 + 100 * 10.0 + 1000 * 0.20) / 1e6


def case(**fields):
    return {"id": 1, "name": "in-repo", "kind": "task", "setup": "repository", "prompt": "Do the thing.",
            "expected_output": "The thing, done.", "assertions": ["The thing is done"], **fields}


class Case(unittest.TestCase):
    """A git repository holding the skill demo, an iteration of its evals, and the stub."""

    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo = self.tmp / "repo"
        self.skill = self.repo / "skills/demo"
        self.write(".agent-conventions.toml", CONVENTIONS)
        self.write(".gitignore", "/.eval-runs/\n/.agent-conventions.toml\n")
        self.write("README.md", "The repository.\n")
        self.write("docs/secret.md", "The expected answer.\n")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: Old.\n---\n\nOld body.\n")
        self.write("skills/demo/evals/files/input.txt", "input\n")
        self.evals(case(exclude=["docs/"]))
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "first")
        self.first = self.git("rev-parse", "HEAD")
        self.write("skills/demo/SKILL.md", "---\nname: demo\ndescription: New.\n---\n\nNew body.\n")
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

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
                              env=GIT_ENV).stdout.strip()

    def evals(self, *cases, **top):
        data = {"skill_name": "demo", "evals": list(cases), **top}
        self.write("skills/demo/evals/evals.json", json.dumps(data, indent=2))

    def prepare(self, **options):
        return workspace.prepare(self.skill, runs=1, **options)

    def main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = run.main([str(a) for a in argv])
        return code, out.getvalue(), err.getvalue()

    def sessions(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def session(self, configuration):
        """The last session of an arm: with the skill's copy, or without."""
        found = [s for s in self.sessions() if ("--add-dir" in s["argv"]) == (configuration != "without_skill")]
        return found[-1]

    def json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))


class Announce(Case):
    def test_nothing_starts_without_start(self):
        iteration = self.prepare()
        code, out, _ = self.main(iteration)
        self.assertEqual(code, 0)
        self.assertEqual(self.sessions(), [])
        self.assertIn("in-repo/with_skill/run-1", out)
        self.assertIn("in-repo/without_skill/run-1", out)
        self.assertIn("2 runs to start, estimated $5.00", out)
        self.assertIn("--start", out)

    def test_the_estimate_follows_the_skills_complete_runs(self):
        iteration = self.prepare()
        self.main(iteration, "--start")
        code, out, _ = self.main(self.prepare())
        mean = (WITH_COST + WITHOUT_COST) / 2
        self.assertIn(f"2 runs to start, estimated ${2 * mean:.2f}", out)
        self.assertIn("mean of 2 complete runs", out)
        _, out, _ = self.main(self.prepare(effort="max"))
        self.assertIn("estimated $5.00", out)

    def test_the_estimate_never_passes_the_ceiling(self):
        _, out, _ = self.main(self.prepare(budget=1.0))
        self.assertIn("2 runs to start, estimated $2.00", out)
        self.assertIn("the run's ceiling, $1.00", out)

    def test_an_old_claude_is_refused_before_any_session(self):
        iteration = self.prepare()
        with mock.patch.dict(os.environ, {"STUB_VERSION": "2.1.283"}):
            code, _, err = self.main(iteration, "--start")
        self.assertEqual(code, 1)
        self.assertIn("2.1.283", err)
        self.assertIn("2.1.291", err)
        self.assertEqual(self.sessions(), [])


class Command(Case):
    def setUp(self):
        super().setUp()
        self.iteration = self.prepare()
        self.code, self.out, self.err = self.main(self.iteration, "--start")

    def test_every_run_ends_with_a_line(self):
        self.assertEqual(self.code, 0, self.err)
        self.assertEqual(len(self.sessions()), 2)
        self.assertIn("in-repo/with_skill/run-1: complete", self.out)
        self.assertIn("in-repo/without_skill/run-1: complete", self.out)

    def test_the_command_sets_the_conditions(self):
        for session in self.sessions():
            argv = session["argv"]
            self.assertIn("-p", argv)
            for flag, value in (("--model", "claude-sonnet-5-5"), ("--effort", "xhigh"),
                                ("--max-budget-usd", "5.0"), ("--permission-mode", "auto"),
                                ("--permission-prompts", "none"), ("--setting-sources", "project,local"),
                                ("--output-format", "json")):
                self.assertEqual(argv[argv.index(flag) + 1], value, flag)
            self.assertEqual(argv[argv.index("--disallowed-tools") + 1:argv.index("--disallowed-tools") + 3],
                             ["Skill", "Agent"])
            self.assertIn("--strict-mcp-config", argv)

    def test_the_guard_is_given_the_real_repository_and_config(self):
        for session in self.sessions():
            argv = session["argv"]
            settings = json.loads(argv[argv.index("--settings") + 1])
            hook = settings["hooks"]["PreToolUse"][0]
            self.assertEqual(hook["matcher"], "*")
            command = hook["hooks"][0]["command"]
            self.assertIn("guard.py", command)
            self.assertIn(str(self.repo), command)
            self.assertIn(str(self.config), command)

    def test_the_folder_lies_outside_any_repository_and_holds_no_evals(self):
        for session in self.sessions():
            self.assertEqual(session["repositories_above"], [])
            self.assertTrue(session["own_git"], "the run's folder is not a git repository")
            self.assertFalse(Path(session["cwd"]).is_relative_to(self.repo))
            self.assertFalse([f for f in session["files"] if "evals" in Path(f).parts])
            self.assertFalse([f for f in session["skill_files"] or [] if "evals" in Path(f).parts])
            self.assertFalse(Path(session["cwd"]).exists(), "the run's temporary folder was left behind")

    def test_each_arm_holds_its_own_version_of_the_skill(self):
        with_skill, without = self.session("with_skill"), self.session("without_skill")
        self.assertIn("skills/demo/SKILL.md", with_skill["files"])
        self.assertFalse([f for f in without["files"] if f.startswith("skills/demo")])
        self.assertEqual(with_skill["skill_files"], ["SKILL.md"])
        self.assertIsNone(without["skill_files"])
        self.assertNotIn("--add-dir", without["argv"])
        for session in (with_skill, without):
            self.assertIn("README.md", session["files"])
            self.assertIn(".agent-conventions.toml", session["files"])
            self.assertNotIn("docs/secret.md", session["files"], "the case's exclude was not applied")

    def test_the_environment_drops_the_parent_session(self):
        for session in self.sessions():
            env = session["env"]
            for name in ("CLAUDECODE", "CLAUDE_EFFORT", "CLAUDE_CODE_SESSION_ATTENDED"):
                self.assertNotIn(name, env)
            self.assertEqual(env["CLAUDE_CONFIG_DIR"], str(self.config))

    def test_the_prompt_holds_the_preamble_and_the_case(self):
        with_skill, without = self.session("with_skill"), self.session("without_skill")
        for session in (with_skill, without):
            preamble, request = session["prompt"].split("\n---\n", 1)
            self.assertIn("Nobody can answer", preamble)
            self.assertIn("Do not start a `claude` session", preamble)
            self.assertEqual(request.strip(), "Do the thing.")
        skill_line = with_skill["prompt"].split("\n---\n", 1)[0]
        copy = with_skill["argv"][with_skill["argv"].index("--add-dir") + 1]
        self.assertIn(f"Use the skill `demo`, whose copy is at `{copy}`", skill_line)
        self.assertTrue(copy.endswith("/skill/demo"), copy)
        self.assertNotIn("Use the skill", without["prompt"])

    def test_run_json_is_written_from_the_transcript(self):
        folder = self.iteration / "in-repo/with_skill/run-1"
        recorded = self.json(folder / "run.json")
        self.assertEqual(recorded["status"], "complete")
        self.assertEqual((recorded["model"], recorded["effort"], recorded["budget_usd"]),
                         ("claude-sonnet-5-5", "xhigh", 5.0))
        self.assertEqual(recorded["claude_version"], "2.1.292")
        self.assertEqual(recorded["models"], {"claude-sonnet-5-5": 3})
        self.assertEqual(recorded["efforts"], {"xhigh": 3})
        self.assertEqual(recorded["calls"], 3)
        self.assertEqual(recorded["estimated_calls"], 0)
        self.assertEqual(recorded["tokens"]["output"], 300)
        self.assertAlmostEqual(recorded["cost_usd"], WITH_COST)
        self.assertEqual(recorded["reported_cost_usd"], 0.0123)
        self.assertEqual((recorded["duration_s"], recorded["turns"]), (4.0, 3))
        self.assertTrue(recorded["session_id"])
        self.assertEqual(recorded["skill_reads"], ["SKILL.md"])
        self.assertEqual(recorded["repository_paths"], [])
        self.assertEqual(recorded["refusals"], [])
        self.assertEqual(self.json(self.iteration / "in-repo/without_skill/run-1/run.json")["skill_reads"], [])

    def test_the_run_keeps_its_transcript_outputs_and_changes(self):
        folder = self.iteration / "in-repo/with_skill/run-1"
        self.assertTrue((folder / "transcript.jsonl").is_file())
        rendered = (folder / "transcript.md").read_text(encoding="utf-8")
        self.assertIn("Read", rendered)
        self.assertIn("Done: wrote answer.txt.", rendered)
        self.assertEqual((folder / "response.md").read_text(encoding="utf-8").strip(), "Done: wrote answer.txt.")
        self.assertEqual((folder / "outputs/answer.txt").read_text(encoding="utf-8"), "answer\n")
        self.assertEqual((folder / "outputs/README.md").read_text(encoding="utf-8"), "changed\n")
        self.assertEqual(self.json(folder / "changes.json"),
                         {"added": ["answer.txt"], "modified": ["README.md"], "deleted": []})
        self.assertIn("Do the thing.", (folder / "prompt.md").read_text(encoding="utf-8"))


class Arms(Case):
    def test_the_baseline_runs_on_its_own_version(self):
        iteration = self.prepare(baseline=self.first)
        self.main(iteration, "--start")
        texts = sorted((s["skill_text"], s["repository_skill_text"]) for s in self.sessions())
        self.assertEqual(len(texts), 2)
        self.assertIn("New body.", texts[0][0])
        self.assertIn("New body.", texts[0][1])
        self.assertIn("Old body.", texts[1][0])
        self.assertIn("Old body.", texts[1][1])

    def test_an_empty_case_holds_its_files(self):
        self.evals(case(name="empty-one", setup="empty", files=["evals/files/input.txt"]))
        self.main(self.prepare(baseline_only=True), "--start")
        (session,) = self.sessions()
        self.assertEqual(session["files"], ["files/input.txt"])
        self.assertTrue(session["own_git"])

    def test_the_env_of_the_evals_reaches_the_run(self):
        self.evals(case(), env={"CLAUDE_DIR": "{tmp}/claude", "PLAIN": "value"})
        self.main(self.prepare(baseline_only=True), "--start")
        (session,) = self.sessions()
        self.assertEqual(session["env"]["PLAIN"], "value")
        claude_dir = Path(session["env"]["CLAUDE_DIR"])
        self.assertEqual(claude_dir.name, "claude")
        self.assertEqual(claude_dir.parent, Path(session["cwd"]).parent)


class Restart(Case):
    def test_a_stopped_run_starts_again_and_a_complete_one_does_not(self):
        iteration = self.prepare()
        with mock.patch.dict(os.environ, {"STUB_SUBTYPE": "error_max_budget_usd"}):
            _, out, _ = self.main(iteration, "--start")
        self.assertIn("in-repo/with_skill/run-1: stopped (error_max_budget_usd)", out)
        recorded = self.json(iteration / "in-repo/with_skill/run-1/run.json")
        self.assertEqual((recorded["status"], recorded["reason"]), ("stopped", "error_max_budget_usd"))
        _, out, _ = self.main(iteration)
        self.assertIn("2 runs to start", out)
        self.main(iteration, "--start")
        self.assertEqual(len(self.sessions()), 4)
        _, out, _ = self.main(iteration, "--start")
        self.assertIn("0 runs to start", out)
        self.assertEqual(len(self.sessions()), 4)

    def test_a_restarted_run_starts_from_an_empty_folder(self):
        iteration = self.prepare()
        with mock.patch.dict(os.environ, {"STUB_SUBTYPE": "error_during_execution"}):
            self.main(iteration, "--start")
        stale = iteration / "in-repo/with_skill/run-1/outputs/stale.txt"
        stale.write_text("left by the stopped run\n", encoding="utf-8")
        self.main(iteration, "--start")
        self.assertFalse(stale.exists())

    def test_refusals_are_kept(self):
        denial = [{"tool_name": "Read", "tool_use_id": "tu_9", "tool_input": {"file_path": str(self.repo / "README.md")}}]
        iteration = self.prepare(baseline_only=True)
        with mock.patch.dict(os.environ, {"STUB_DENIALS": json.dumps(denial)}):
            self.main(iteration, "--start")
        recorded = self.json(iteration / "in-repo/without_skill/run-1/run.json")
        self.assertEqual(recorded["refusals"], denial)


class TemporaryFolder(Case):
    def test_a_temporary_folder_inside_a_repository_is_refused(self):
        iteration = self.prepare()
        inside = self.repo / "tmp-here"
        inside.mkdir()
        with mock.patch.object(tempfile, "tempdir", str(inside)):
            code, _, err = self.main(iteration, "--start")
        self.assertEqual(code, 1)
        self.assertIn("inside a repository", err)
        self.assertEqual(self.sessions(), [])


class Environment(unittest.TestCase):
    def test_claude_variables_are_dropped_but_the_config_dir(self):
        env = harness.environment({"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli", "CLAUDE_CONFIG_DIR": "/c",
                                   "PATH": "/bin"}, {"CLAUDE_DIR": "/t/claude"})
        self.assertEqual(env, {"CLAUDE_CONFIG_DIR": "/c", "PATH": "/bin", "CLAUDE_DIR": "/t/claude"})

    def test_versions_compare_as_numbers(self):
        self.assertTrue(harness.recent_enough("2.1.291 (Claude Code)"))
        self.assertTrue(harness.recent_enough("2.10.0 (Claude Code)"))
        self.assertFalse(harness.recent_enough("2.1.290 (Claude Code)"))
        self.assertFalse(harness.recent_enough("unknown"))


class Guard(unittest.TestCase):
    def guard(self, tool_input, *denied, home="/home/u"):
        event = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": tool_input})
        args = [sys.executable, "-B", str(SCRIPTS / "guard.py"), *denied]
        result = subprocess.run(args, input=event, capture_output=True, text=True,
                                env={**os.environ, "HOME": home})
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else None

    def denied(self, answer):
        output = answer["hookSpecificOutput"]
        self.assertEqual((output["hookEventName"], output["permissionDecision"]), ("PreToolUse", "deny"))
        self.assertIn("outside the test's limits", output["permissionDecisionReason"])

    def test_a_call_naming_a_denied_path_is_refused(self):
        self.denied(self.guard({"file_path": "/code/repo/CLAUDE.md"}, "/code/repo"))
        self.denied(self.guard({"command": "cat ../../code/repo/x"}, "/code/repo"))
        self.denied(self.guard({"command": "cd / && cat code/repo/x"}, "/code/repo"))

    def test_the_home_forms_of_a_denied_path(self):
        for command in ("ls ~/.claude/skills", "ls $HOME/.claude", "ls ${HOME}/.claude", "ls /home/u/.claude"):
            self.denied(self.guard({"command": command}, "/home/u/.claude"))

    def test_other_calls_pass(self):
        self.assertIsNone(self.guard({"command": "ls /tmp/run/work"}, "/code/repo", "/home/u/.claude"))
        self.assertIsNone(self.guard({"file_path": "/code/repository/x"}, "/code/repo"))

    def test_an_unreadable_call_is_refused(self):
        args = [sys.executable, "-B", str(SCRIPTS / "guard.py"), "/code/repo"]
        result = subprocess.run(args, input="not json", capture_output=True, text=True)
        self.denied(json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
