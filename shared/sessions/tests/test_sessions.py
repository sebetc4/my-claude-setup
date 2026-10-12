"""Tests for the selection of a window's sessions, on a fixture repository and its transcripts."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SHARED = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SHARED / "usage"))  # in a skill, the copy of usage.py sits beside sessions.py
_spec = importlib.util.spec_from_file_location("sessions", SHARED / "sessions" / "sessions.py")
sessions = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sessions)

# git reads neither the user's nor the system's configuration, and commits under a fixed name.
GIT_ENV = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
           "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com"}

INSIDE, PARALLEL, CONTINUED, ACROSS, BEFORE = (f"{n}{n * 7}-{n * 4}-4{n * 3}-8{n * 3}-{n * 12}" for n in "12345")
PROBE, RUN, LATE, EARLY, JUDGE, SCRATCH, STRANGER, TRIGGER, OTHER, WAITED = (
    f"{n}{n * 7}-{n * 4}-4{n * 3}-8{n * 3}-{n * 12}" for n in "6789abcde0")
ELSEWHERE = "ffffffff-ffff-4fff-8fff-ffffffffffff"  # a session another project holds


def at(clock, day=2):
    return f"2026-03-0{day}T{clock}.000Z"


def human(clock, day=2, cwd=None):
    """A person's prompt."""
    record = {"type": "user", "timestamp": at(clock, day), "origin": {"kind": "human"},
              "message": {"role": "user", "content": "go on"}}
    return dict(record, cwd=cwd) if cwd else record


def prompt(clock):
    """A claude -p session's prompt: no origin."""
    return {"type": "user", "timestamp": at(clock), "message": {"role": "user", "content": "run the case"}}


def call(message_id, clock, day=2, sidechain=False):
    return {"type": "assistant", "timestamp": at(clock, day), "isSidechain": sidechain,
            "message": {"id": message_id, "model": "claude-opus-5-5", "stop_reason": "end_turn",
                        "content": [{"type": "text"}],
                        "usage": {"input_tokens": 1, "output_tokens": 100, "cache_read_input_tokens": 0,
                                  "cache_creation_input_tokens": 0}}}


class Window(unittest.TestCase):
    """A phase opened at 09:00 on 2026-03-02 and closed at 15:00, its repository's sessions in their
    project folder, the claude -p sessions it started in folders of their own."""

    def setUp(self):
        self.enterContext(mock.patch.dict(os.environ, GIT_ENV))
        root = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.repo, self.projects = root / "repo", root / "projects"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.before = self.commit("2026-03-01T08:00:00Z")
        self.opening = self.commit("2026-03-02T09:00:00Z")
        self.shared = self.commit("2026-03-02T10:50:00Z")   # in INSIDE's span and PARALLEL's
        self.copied = self.commit("2026-03-02T11:15:00Z")   # in INSIDE's span, which CONTINUED copies
        self.closing = self.commit("2026-03-02T15:00:00Z")
        self.after = self.commit("2026-03-03T10:00:00Z")

        history = [human("09:58:00", cwd="/old/path/of/repo"), call("i1", "10:00:00"), call("i2", "10:40:00"),
                   call("i3", "11:30:00")]
        own = self.projects / sessions.folder_of(self.repo)
        # INSIDE's last call starts runs in the background; their notification comes at 11:50
        self.transcript(own / f"{INSIDE}.jsonl", *history,
                        {"type": "queue-operation", "operation": "enqueue", "timestamp": at("11:50:00")})
        self.transcript(own / INSIDE / "subagents" / "agent-R.jsonl", call("r1", "10:41:00", sidechain=True))
        self.transcript(own / f"{PARALLEL}.jsonl", human("10:29:00"), call("p1", "10:30:00"), call("p2", "11:00:00"))
        self.transcript(own / f"{CONTINUED}.jsonl", *history, human("12:04:00"), call("k1", "12:05:00"),
                        call("k2", "12:30:00"))
        self.transcript(own / f"{ACROSS}.jsonl", human("13:58:00"), call("a1", "14:00:00"), call("a2", "14:50:00"),
                        call("a3", "15:30:00"))
        self.transcript(own / f"{BEFORE}.jsonl", human("10:00:00", day=1), call("b1", "10:01:00", day=1))
        self.transcript(own / f"{PROBE}.jsonl", prompt("10:10:00"), call("x1", "10:11:00"))

        runs = self.projects / "-tmp-skill-run-abc-work"
        self.transcript(runs / f"{RUN}.jsonl", prompt("10:20:00"), call("y1", "10:21:00"))
        self.transcript(runs / f"{LATE}.jsonl", prompt("16:30:00"), call("y2", "16:31:00"))
        self.transcript(runs / f"{EARLY}.jsonl", prompt("08:00:00"), call("y3", "08:01:00"))
        self.transcript(runs / f"{WAITED}.jsonl", prompt("11:40:00"), call("y4", "11:41:00"))
        self.transcript(self.projects / "-tmp-skill-judge-def-work" / f"{JUDGE}.jsonl", prompt("10:45:00"),
                        call("j1", "10:46:00"))
        self.transcript(self.projects / f"-tmp-claude-1000--code-x-{INSIDE}-scratchpad-probe" / f"{SCRATCH}.jsonl",
                        prompt("13:00:00"), call("s1", "13:01:00"))
        self.transcript(self.projects / f"-tmp-claude-1000--code-other-{ELSEWHERE}-scratchpad" / f"{STRANGER}.jsonl",
                        prompt("10:15:00"), call("s2", "10:16:00"))
        self.transcript(self.projects / "-tmp-skill-trigger-ghi-work" / f"{TRIGGER}.jsonl", prompt("13:30:00"),
                        call("t1", "13:31:00"))
        self.transcript(self.projects / "-code-other" / f"{OTHER}.jsonl", human("10:00:00"), call("o1", "10:01:00"))

    def git(self, *args, env=None):
        return subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True, check=True,
                              env={**os.environ, **(env or {})}).stdout.strip()

    def commit(self, time):
        self.git("commit", "-q", "--allow-empty", "-m", time,
                 env={"GIT_AUTHOR_DATE": time, "GIT_COMMITTER_DATE": time})
        return self.git("rev-parse", "HEAD")

    def transcript(self, path, *records):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")

    def window(self, start=None, end=None):
        return sessions.window(self.repo, start or self.opening, end or self.closing, projects=self.projects)

    def test_a_project_folder_is_named_after_its_path(self):
        self.assertEqual(sessions.folder_of(Path("/code/ai/my-agent-setup")), "-code-ai-my-agent-setup")
        self.assertEqual(sessions.folder_of(Path("/tmp/claude-1000/a_b.c")), "-tmp-claude-1000-a-b-c")

    def test_a_window_is_given_by_two_commits_or_two_times(self):
        by_commits = self.window()
        self.assertEqual((by_commits.start, by_commits.end), (at("09:00:00"), at("15:00:00")))
        by_times = self.window("2026-03-02T09:00:00Z", "2026-03-02T15:00:00+00:00")
        self.assertEqual((by_times.start, by_times.end), (at("09:00:00"), at("15:00:00")))
        self.assertEqual([m.id for m in by_times.sessions], [m.id for m in by_commits.sessions])

    def test_the_repositorys_working_sessions_are_those_of_its_project_folder_whatever_their_cwd(self):
        found = self.window()
        self.assertEqual([m.id for m in found.sessions], [INSIDE, PARALLEL, CONTINUED, ACROSS])
        self.assertEqual(found.sessions[0].path, self.projects / sessions.folder_of(self.repo) / f"{INSIDE}.jsonl")

    def test_each_call_is_counted_by_its_time_once(self):
        calls = {m.id: ([c.id for c in m.session.main], [[c.id for c in r.calls] for r in m.session.runs])
                 for m in self.window().sessions}
        self.assertEqual(calls, {INSIDE: (["i1", "i2", "i3"], [["r1"]]), PARALLEL: (["p1", "p2"], []),
                                 CONTINUED: (["k1", "k2"], []), ACROSS: (["a1", "a2"], [])})

    def test_a_sessions_span_runs_from_its_own_first_call_to_its_last_record(self):
        spans = {m.id: m.span for m in self.window().sessions}
        self.assertEqual(spans[INSIDE], (at("10:00:00"), at("11:50:00")))
        self.assertEqual(spans[CONTINUED], (at("12:05:00"), at("12:30:00")))
        self.assertEqual(spans[ACROSS], (at("14:00:00"), at("15:30:00")))

    def test_a_claude_p_session_is_given_by_its_scratchpad_folder_or_by_the_span_holding_its_start(self):
        found = {h.id: (h.owner, h.by, h.shared) for h in self.window().headless}
        self.assertEqual(found, {PROBE: (INSIDE, "time", False), RUN: (INSIDE, "time", False),
                                 JUDGE: (INSIDE, "time", True), WAITED: (INSIDE, "time", False),
                                 SCRATCH: (INSIDE, "scratchpad", False)})

    def test_a_claude_p_session_keeps_its_calls_and_its_start(self):
        [run] = [h for h in self.window().headless if h.id == RUN]
        self.assertEqual(([c.id for c in run.session.calls], run.session.started), (["y1"], at("10:20:00")))
        self.assertEqual(run.path, self.projects / "-tmp-skill-run-abc-work" / f"{RUN}.jsonl")

    def test_each_commit_is_given_to_the_session_whose_span_holds_it(self):
        commits = [(c.hash, c.owner, c.shared) for c in self.window().commits]
        self.assertEqual(commits, [(self.opening, None, False), (self.shared, INSIDE, True),
                                   (self.copied, INSIDE, False), (self.closing, ACROSS, False)])
        self.assertEqual(self.window().commits[1].time, at("10:50:00"))

    def test_the_window_ends_now_by_default(self):
        found = sessions.window(self.repo, self.opening, projects=self.projects)
        across = [m for m in found.sessions if m.id == ACROSS][0]
        self.assertEqual([c.id for c in across.session.main], ["a1", "a2", "a3"])
        self.assertEqual([c.hash for c in found.commits][-1], self.after)


if __name__ == "__main__":
    unittest.main()
