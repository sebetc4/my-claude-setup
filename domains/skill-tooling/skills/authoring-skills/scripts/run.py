#!/usr/bin/env python3
"""Start the runs of an iteration that workspace.py prepared, as unattended agent sessions.

Usage: run.py <iteration> [--start] [--jobs N] [--timeout MINUTES] [--case NAME ...] [--run N ...]
              | --status | --stop

Lists the runs to start — each case, configuration and number not yet complete — with
their count and estimated cost: the mean cost of the skill's complete runs at the
iteration's model and effort, or $2.50 a run when there is none. Starts nothing without
--start; with it, starts them --jobs at a time and prints one line per run as it starts
and as it ends. A run the subscription's usage limit stops leaves the runs not yet
started unstarted, since each would stop at once. --status prints where each run
stands, a running one with its calls, its cost so far and its last call, read from its
transcript as it is written; it starts nothing. --case limits the runs listed and started
to the cases named, --run to the numbers named, one run of each case and configuration
each. --stop, from another shell, writes stop.json in the iteration: the
run.py going starts no new run, and the runs going end as they would. The next --start
clears it. A skill that starts agents and has no complete run is estimated at the run's
ceiling.

Each run works in a temporary folder outside any repository: work/, where the session
starts, holds the repository without the skill's folder and with the arm's version put
back at its path, the case's fixture, or an empty folder, with the case's files, made a
git repository; a skill's arm adds skills/<skill-name>/, the copy the prompt names. A
baseline naming another skill, another tool, is that copy only, never at the skill's
path. For a skill with agents, a skill's arm puts its version of them in work/'s
.claude/agents/, where the session finds them, and, in the repository, back at their
paths. For a skill with hooks, a skill's arm copies its version of the hook files into
hooks/<folder>/, beside skills/ as an install puts them, <folder> the hooks file's own,
and gives the session its hooks file through --settings, {{HOOKS_DIR}} resolved to that
copy, leaving work/ as it is; in the repository, both go back at their paths too. The
session takes the iteration's model, effort and ceiling, the evals' env, and
guard.py, which refuses any call naming the real repository or the real configuration
folder. It is denied the Skill tool, and the Agent tool unless the skill starts agents,
in every arm then, so that the baseline has the tools the skill's arm has.
The prompt is a preamble, a line `---`, then the case's prompt.

Into the run's folder go prompt.md, result.json, response.md, transcript.jsonl and
transcript.md, context/ (each instruction file and hook context the session was given,
whole, which transcript.md names where it came), outputs/ (the files the run added or changed, at their paths),
changes.json, and run.json: status, claude version, models and efforts read from the
transcript, tokens, cost, duration, refusals, the files of the skill's copy the run
named and any path of the real repository it named, its agents' calls included. A run
that started agents adds subagents/, their transcripts, and agents/<type>-<id>.md, each
rendered, listed at the head of transcript.md, their context in context/<type>-<id>/; its figures count them, the output their
transcripts lack taken from the result's total per model (output_source `reported`), or
estimated without one (`estimated`), and run.json's agents gives them by agent type. A run stopped by its ceiling, a
limit or an error is marked stopped; the next --start starts it again from a fresh
folder, and skips the complete runs. While a run goes, its folder holds running.json: its
session id, start and the pid of run.py.
"""

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
import tempfile
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402  (same directory, not an installed package)
import usage  # noqa: E402

GUARD = Path(__file__).resolve().parent / "guard.py"
STOP = "stop.json"
JOBS = 4
TIMEOUT = 120
DEFAULT_COST = 2.50
PREAMBLE = ("Work on the request below, in this folder. Nobody can answer a question during this "
            "session: where you would ask one, take the most reasonable assumption, say which, and "
            f"go on. Do not start a `{harness.COMMAND}` session. End with an account of what you did.")
SKILL_LINE = "Use the skill `{name}`, whose copy is at `{path}`: read its `SKILL.md` and follow it."
GIT_ENV = {"GIT_AUTHOR_NAME": "eval", "GIT_AUTHOR_EMAIL": "eval@localhost",
           "GIT_COMMITTER_NAME": "eval", "GIT_COMMITTER_EMAIL": "eval@localhost"}
# git's empty tree, to compare against when a fixture brings a repository without a commit.
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
PATH_END = r"[^\s'\"`;|&()<>]*"
# The folder of an arm's agents in an iteration, as workspace.py writes it.
AGENTS = "{}_agents"
# The folder of an arm's hooks in an iteration, as workspace.py writes it, and the
# placeholder its hooks file names the hook files' folder by.
HOOKS = "{}_hooks"
HOOKS_DIR = "{{HOOKS_DIR}}"


class Refused(Exception):
    pass


@dataclass
class Run:
    case: str
    configuration: str
    number: int
    folder: Path

    @property
    def name(self):
        return f"{self.case}/{self.configuration}/run-{self.number}"

    def recorded(self):
        path = self.folder / "run.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def status(self):
        return (self.recorded() or {}).get("status")

    def running(self):
        try:
            return json.loads((self.folder / "running.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def plan(iteration, recorded):
    return [Run(case, configuration, number, iteration / case / configuration / f"run-{number}")
            for case in recorded["cases"] for configuration in recorded["configurations"]
            for number in range(1, recorded["runs"] + 1)]


def agent_tool(recorded):
    """Whether the iteration's runs have the Agent tool: the skill starts agents."""
    return bool(recorded.get("starts_agents") or recorded.get("agents"))


def estimate(iteration, recorded):
    """(cost per run, what it rests on)."""
    model, effort = recorded["model"], recorded["effort"]
    costs = []
    for path in iteration.parent.glob("iteration-*/*/*/run-*/run.json"):
        try:
            run = read_json(path)
        except (OSError, ValueError):
            continue
        if ((run.get("status"), run.get("model"), run.get("effort")) == ("complete", model, effort)
                and run.get("cost_usd") is not None):
            costs.append(run["cost_usd"])
    ceiling = recorded["budget_usd"]
    if not costs and agent_tool(recorded):
        return ceiling, (f"the run's ceiling, ${ceiling:.2f}, since the skill starts agents and no run of it at "
                         f"{model} and {effort} is complete")
    if costs:
        cost = statistics.mean(costs)
        basis = f"${cost:.2f} a run, the mean of {len(costs)} complete runs of this skill at {model} and {effort}"
    else:
        cost = DEFAULT_COST
        basis = (f"$2.50 a run, the mean of a full skill-writing task measured on 2026-10-06, since no run of this "
                 f"skill at {model} and {effort} is complete")
    if cost > ceiling:
        return ceiling, f"the run's ceiling, ${ceiling:.2f}, below {basis}"
    return cost, basis


def check_outside(folder):
    """Refuse a temporary folder that lies inside a repository."""
    for place in (folder, *folder.parents):
        for marker in (".git", ".agent-conventions.toml"):
            if (place / marker).exists():
                raise Refused(f"the temporary folder {folder} lies inside a repository ({place / marker}): "
                              "point TMPDIR outside any repository, or leave it unset")


def git(work, *args):
    return subprocess.run(["git", "-C", str(work), *args], capture_output=True, text=True,
                          env={**os.environ, **GIT_ENV})


def extract(archive, target, left_out=()):
    """Extract archive into target, without the paths left out."""
    left_out = [p.rstrip("/") for p in left_out]
    with tarfile.open(archive) as tar:
        members = [m for m in tar.getmembers()
                   if not any(m.name == p or m.name.startswith(p + "/") for p in left_out)]
        tar.extractall(target, members=members, filter="data")


def arm_copy(iteration, recorded, configuration):
    """The arm's version of the skill in the iteration, or None for the arm without it."""
    if configuration == "without_skill":
        return None
    return iteration / configuration / recorded["skill_name"]


def arm_agents(iteration, recorded, configuration):
    """The folder of the arm's agents, or None: the arm without the skill has none."""
    if configuration == "without_skill" or not recorded.get("agents"):
        return None
    folder = iteration / AGENTS.format(configuration)
    return folder if folder.is_dir() else None


def arm_hooks(iteration, recorded, configuration):
    """The folder of the arm's hooks, or None: the arm without the skill has none."""
    if configuration == "without_skill" or not recorded.get("hooks"):
        return None
    folder = iteration / HOOKS.format(configuration)
    return folder if folder.is_dir() else None


def session_hooks(held, path, tmp):
    """Copy the hook files of held, the arm's hooks, into tmp/hooks/<folder>/; the hooks file's
    groups, {{HOOKS_DIR}} resolved to that copy, {} when the arm lacks the file."""
    path = Path(os.path.normpath(path))
    if not (held / path).is_file():
        return {}
    copy = tmp / "hooks" / (path.parent.name or "hooks")
    if (held / path.parent / "hooks").is_dir():
        shutil.copytree(held / path.parent / "hooks", copy, symlinks=True)
    text = (held / path).read_text(encoding="utf-8")
    return json.loads(text.replace(HOOKS_DIR, json.dumps(str(copy))[1:-1]))


def place_agents(folder, work, in_repository):
    """Copy the agents' files where the session finds them and, in a repository, at their paths."""
    for source in sorted(p for p in folder.rglob("*") if p.is_file()):
        places = [harness.AGENTS_FOLDER / source.name] + ([source.relative_to(folder)] if in_repository else [])
        for place in places:
            (work / place).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, work / place)


def build_work(run, iteration, recorded, metadata, tmp):
    """The run's work/ folder, a git repository; its starting commit."""
    work = tmp / "work"
    work.mkdir()
    case_folder = iteration / run.case
    if metadata["setup"] == "repository":
        extract(iteration / "base.tar", work, metadata.get("exclude", []))
        source = arm_copy(iteration, recorded, run.configuration)
        if source and (run.configuration != "old_skill" or (recorded["baseline"] or {}).get("in_repository", True)):
            shutil.copytree(source, work / recorded["skill_path"], symlinks=True)
    elif metadata["setup"] == "fixture":
        extract(case_folder / "fixture.tar", work)
    agents = arm_agents(iteration, recorded, run.configuration)
    if agents:
        place_agents(agents, work, metadata["setup"] == "repository")
    hooks = arm_hooks(iteration, recorded, run.configuration)
    if hooks and metadata["setup"] == "repository":
        shutil.copytree(hooks, work, symlinks=True, dirs_exist_ok=True)
    if (case_folder / "files").is_dir():
        shutil.copytree(case_folder / "files", work, symlinks=True, dirs_exist_ok=True)
    if not (work / ".git").exists():
        for args in (("init", "-q"), ("add", "-A", "-f"), ("commit", "-q", "--allow-empty", "-m", "base")):
            done = git(work, *args)
            if done.returncode != 0:
                raise Refused(f"git {args[0]} in the run's folder failed: {done.stderr.strip()}")
    head = git(work, "rev-parse", "HEAD")
    return work, head.stdout.strip() if head.returncode == 0 else None


def prompt_of(metadata, name, copy):
    head = [PREAMBLE] + ([SKILL_LINE.format(name=name, path=copy)] if copy else [])
    return "\n\n".join(head) + "\n\n---\n\n" + metadata["prompt"].strip() + "\n"


def collect(work, start, outputs):
    """Copy the files the run added or changed into outputs; {added, modified, deleted}."""
    git(work, "add", "-A")
    listed = git(work, "diff", "--cached", "--name-status", "--no-renames", "-z", start or EMPTY_TREE)
    fields = [f for f in listed.stdout.split("\0") if f]
    changes = {"added": [], "modified": [], "deleted": []}
    for letter, path in zip(fields[::2], fields[1::2]):
        key = {"A": "added", "D": "deleted"}.get(letter[0], "modified")
        changes[key].append(path)
        if key != "deleted" and (work / path).is_file():
            target = outputs / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(work / path, target)
    return {key: sorted(paths) for key, paths in changes.items()}


def named(calls, folder):
    """The paths under folder that the calls name, relative to it."""
    found = re.compile(re.escape(str(folder)) + r"(?:/(" + PATH_END + "))?")
    paths = set()
    for _, given in calls:
        for text in harness.strings(given):
            for match in found.finditer(text):
                paths.add(match.group(1) or ".")
    return sorted(paths)


def safe(name):
    return re.sub(r"[^\w.-]", "-", name or "agent")


def render_agents(found, folder, target):
    """Write each run of an agent as Markdown, target/<type>-<id>.md; the lines that list them
    at the head of transcript.md, empty without any."""
    if not found.runs:
        return ""
    target.mkdir(exist_ok=True)
    lines = ["## Agents", "", "The agents the run started, each with its calls and results in its own file:", ""]
    for agent_run in found.runs:
        stem = f"{safe(agent_run.agent)}-{agent_run.id}"
        name = f"{stem}.md"
        rendered = harness.render(folder / f"agent-{agent_run.id}.jsonl", target.parent / "context" / stem,
                                  f"context/{stem}")
        (target / name).write_text(rendered, encoding="utf-8")
        lines.append(f"- `agents/{name}`: {agent_run.agent}, {plural(len(agent_run.calls), 'call')}")
    return "\n".join(lines) + "\n\n"


def counted(found, outputs):
    """run.json's figures of a session with its runs of agents. The output the runs' transcripts
    lack comes from outputs, the result's total per model, where it gives one for every model
    concerned, output_source `reported`; else it stays estimated, `estimated`."""
    calls = found.calls
    lacking = {call.model for call in calls if call.estimated}
    if not lacking:
        source = "transcript"
    elif lacking <= set(outputs):
        source, calls = "reported", usage.settle(calls, outputs)
    else:
        source = "estimated"
    total = usage.as_json(usage.tally(calls))
    agents, start = {}, len(found.main)
    for agent_run in found.runs:
        own = usage.tally(calls[start:start + len(agent_run.calls)])
        start += len(agent_run.calls)
        entry = agents.setdefault(agent_run.agent or "unknown", {"runs": 0, "calls": 0,
                                                                 "tokens": dict.fromkeys(usage.KINDS, 0),
                                                                 "cost_usd": 0.0})
        entry["runs"] += 1
        entry["calls"] += own.calls
        for kind in usage.KINDS:
            entry["tokens"][kind] += own.tokens[kind]
        entry["cost_usd"] = None if own.cost is None or entry["cost_usd"] is None else entry["cost_usd"] + own.cost
    return {"models": {m: t["calls"] for m, t in total["models"].items()}, "efforts": total["efforts"],
            "calls": total["calls"], "estimated_calls": total["estimated"], "tokens": total["tokens"],
            "cost_usd": total["cost"], "prices": total["prices"], "output_source": source, "agents": agents}


def denied_paths(recorded):
    paths = [Path(recorded["root"]), harness.config_dir()]
    home_config = Path.home() / ".claude"
    if home_config not in paths:
        paths.append(home_config)
    return paths


def execute(run, iteration, recorded, metadata, binary, version, timeout, limit=None):
    """Start one run and write its folder; its run.json. limit, a threading.Event, is set
    when the subscription's usage limit stopped the run."""
    for child in list(run.folder.iterdir()) if run.folder.exists() else []:
        shutil.rmtree(child) if child.is_dir() and not child.is_symlink() else child.unlink()
    run.folder.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    session_id = str(uuid.uuid4())
    (run.folder / "running.json").write_text(json.dumps({"session_id": session_id, "started": started,
                                                         "pid": os.getpid()}) + "\n", encoding="utf-8")
    record = {"case": run.case, "configuration": run.configuration, "run": run.number, "status": "stopped",
              "reason": None, "claude_version": version, "model": recorded["model"], "effort": recorded["effort"],
              "budget_usd": recorded["budget_usd"], "started": started, "hooks": []}
    tmp = Path(tempfile.mkdtemp(prefix="skill-run-")).resolve()
    try:
        check_outside(tmp)
        work, start = build_work(run, iteration, recorded, metadata, tmp)
        source = arm_copy(iteration, recorded, run.configuration)
        copy = None
        if source:
            copy = tmp / "skills" / recorded["skill_name"]
            shutil.copytree(source, copy, symlinks=True)
        held = arm_hooks(iteration, recorded, run.configuration)
        hooks = session_hooks(held, recorded["hooks"], tmp) if held else {}
        record["hooks"] = sorted(hooks)
        env = harness.environment(os.environ, {k: v.replace("{tmp}", str(tmp))
                                               for k, v in recorded.get("env", {}).items()})
        settings = harness.session_settings(("PreToolUse", harness.guard_command(GUARD, denied_paths(recorded))),
                                            groups=hooks)
        line = harness.command(binary, recorded["model"], recorded["effort"], recorded["budget_usd"], settings,
                               add_dirs=[copy] if copy else [], disallowed=harness.disallowed(agent_tool(recorded)),
                               session_id=session_id)
        prompt = prompt_of(metadata, recorded["skill_name"], copy)
        (run.folder / "prompt.md").write_text(prompt, encoding="utf-8")
        session = harness.start(line, work, prompt, env, timeout)
        result = harness.result_of(session.stdout)
        if result is not None:
            (run.folder / "result.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        else:
            (run.folder / "stdout.txt").write_text(session.stdout, encoding="utf-8")
        if session.stderr.strip():
            (run.folder / "stderr.txt").write_text(session.stderr, encoding="utf-8")
        record["status"], record["reason"] = harness.outcome(session, result)
        if limit is not None and harness.limit_reached(result):
            limit.set()
        figures = harness.figures(result)
        (run.folder / "response.md").write_text(figures.pop("response").strip() + "\n", encoding="utf-8")
        record.update(figures)
        record["session_id"] = record["session_id"] or session_id
        if record["duration_s"] is None:
            record["duration_s"] = round(session.seconds, 1)
        transcript = harness.transcript_of(record["session_id"])
        calls = []
        if transcript:
            shutil.copy2(transcript, run.folder / "transcript.jsonl")
            runs = harness.subagents_of(transcript)
            if runs.is_dir():
                shutil.copytree(runs, run.folder / "subagents")
            found = usage.session(transcript)
            head = render_agents(found, runs, run.folder / "agents")
            (run.folder / "transcript.md").write_text(head + harness.render(transcript, run.folder / "context"),
                                                      encoding="utf-8")
            record.update(counted(found, harness.reported_output(result)))
            calls = harness.tool_calls(transcript) + [call for path in sorted(runs.glob("agent-*.jsonl"))
                                                      for call in harness.tool_calls(path)]
        elif record["status"] == "complete":
            record["status"], record["reason"] = "stopped", "transcript not found"
        changes = collect(work, start, run.folder / "outputs")
        (run.folder / "changes.json").write_text(json.dumps(changes, indent=1) + "\n", encoding="utf-8")
        record["skill_reads"] = named(calls, copy) if copy else []
        record["repository_paths"] = named(calls, recorded["root"])
    except Exception as error:  # a run that fails is recorded and started again by the next --start
        record["status"], record["reason"] = "stopped", f"error: {error}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        (run.folder / "running.json").unlink(missing_ok=True)
        record["ended"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        (run.folder / "run.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def line_of(run, record):
    text = f"{run.name}: {record['status']}"
    if record.get("reason"):
        text += f" ({record['reason']})"
    if record.get("cost_usd") is not None:
        text += f", ${record['cost_usd']:.2f}"
    if record.get("duration_s") is not None:
        minutes, seconds = divmod(int(record["duration_s"]), 60)
        text += f", {minutes}m{seconds:02d}s"
    return text


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (PermissionError, TypeError, ValueError, OverflowError):
        return isinstance(pid, int)
    return True


def short(given, width=80):
    """A call's input in a few words: its command or path, else its JSON."""
    text = next((given[k] for k in ("command", "file_path", "path", "pattern", "url", "query")
                 if isinstance(given.get(k), str)), None) if isinstance(given, dict) else None
    text = " ".join((text if text is not None else json.dumps(given)).split())
    return text if len(text) <= width else text[:width - 1] + "…"


def progress(run, recorded):
    """(state, where the run stands in one line)."""
    running = run.running()
    if running:
        if not alive(running.get("pid")):
            return "interrupted", (f"{run.name}: interrupted, started {running.get('started')}: run.py ended "
                                   "before the run")
        text = f"{run.name}: running since {running.get('started')}"
        transcript = harness.transcript_of(running.get("session_id"))
        if not transcript:
            return "running", text + ", no call yet"
        so_far = usage.as_json(usage.tally(usage.session(transcript).calls))
        cost = "an unknown cost" if so_far["cost"] is None else f"${so_far['cost']:.2f}"
        text += f", {plural(so_far['calls'], 'call')}, {cost} of ${recorded['budget_usd']:.2f}"
        calls = harness.tool_calls(transcript)
        if calls:
            text += f", last: {calls[-1][0]} {short(calls[-1][1])}"
        return "running", text
    record = run.recorded()
    return (record["status"], line_of(run, record)) if record else ("not started", f"{run.name}: not started")


def show_status(iteration, recorded):
    runs = plan(iteration, recorded)
    found = [progress(run, recorded) for run in runs]
    for _, line in found:
        print(line)
    states = [state for state, _ in found]
    counts = {state: states.count(state) for state in dict.fromkeys(states)}
    print(", ".join(f"{count} {state}" for state, count in counts.items()) + f", of {plural(len(runs), 'run')}.")
    asked = stop_asked(iteration)
    if asked:
        print(f"A stop was asked at {asked.get('asked')}: run.py starts no new run until the next --start.")


def stop_asked(iteration):
    """The stop asked for the iteration, or None."""
    path = iteration / STOP
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def ask_stop(iteration, recorded):
    asked = datetime.now(timezone.utc).isoformat(timespec="seconds")
    (iteration / STOP).write_text(json.dumps({"asked": asked}) + "\n", encoding="utf-8")
    going = [run.name for run in plan(iteration, recorded)
             if (running := run.running()) and alive(running.get("pid"))]
    print(f"Stop asked at {asked}: run.py starts no new run of this iteration.")
    print(f"Runs going, left to end: {', '.join(going)}." if going
          else "No run is going: the next --start clears the stop.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Start the runs of an iteration that workspace.py prepared.")
    parser.add_argument("iteration", type=Path, help="the iteration's folder")
    parser.add_argument("--start", action="store_true", help="start the runs; without it, only list them")
    parser.add_argument("--jobs", type=int, default=JOBS, help=f"runs at a time ({JOBS})")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help=f"minutes before a run is stopped ({TIMEOUT})")
    parser.add_argument("--status", action="store_true", help="print where each run stands, and start nothing")
    parser.add_argument("--stop", action="store_true", help="ask the run.py going to start no new run; the runs "
                        "going end as they would")
    parser.add_argument("--case", dest="cases", action="append", help="a case whose runs to list or start; every "
                        "case by default")
    parser.add_argument("--run", dest="numbers", type=int, action="append", help="a run number to list or start, "
                        "in each case and configuration; every number by default")
    args = parser.parse_args(argv)
    iteration = args.iteration.resolve()
    try:
        recorded = read_json(iteration / "iteration.json")
    except (OSError, ValueError) as error:
        print(f"no iteration at {iteration}: {error}", file=sys.stderr)
        return 1
    if args.status:
        show_status(iteration, recorded)
        return 0
    if args.stop:
        ask_stop(iteration, recorded)
        return 0
    unknown = [name for name in args.cases or [] if name not in recorded["cases"]]
    if unknown:
        for name in unknown:
            print(f"no case named `{name}` in the iteration", file=sys.stderr)
        return 1
    unknown = [n for n in args.numbers or [] if not 1 <= n <= recorded["runs"]]
    if unknown:
        for number in unknown:
            print(f"no run numbered {number} in the iteration, which has {recorded['runs']} a configuration",
                  file=sys.stderr)
        return 1
    runs = [r for r in plan(iteration, recorded)
            if (not args.cases or r.case in args.cases) and (not args.numbers or r.number in args.numbers)]
    todo = [r for r in runs if r.status() != "complete"]
    per_run, basis = estimate(iteration, recorded)
    for run in todo:
        status = run.status()
        print(run.name + (f" (again, {status})" if status else ""))
    print(f"{plural(len(todo), 'run')} to start, estimated ${len(todo) * per_run:.2f}: {basis}; "
          f"{plural(len(runs) - len(todo), 'complete run')} skipped.")
    if not args.start:
        print("Nothing started: run again with --start to start them.")
        return 0
    if not todo:
        return 0
    try:
        binary = harness.binary()
        version = harness.version(binary)
        check_outside(Path(tempfile.gettempdir()).resolve())
    except (harness.HarnessError, Refused) as error:
        print(error, file=sys.stderr)
        return 1
    lock, limit = threading.Lock(), threading.Event()
    (iteration / STOP).unlink(missing_ok=True)

    def go(run):
        if limit.is_set() or stop_asked(iteration) is not None:
            return None
        with lock:
            print(f"{run.name}: started", flush=True)
        record = execute(run, iteration, recorded, read_json(iteration / run.case / "eval_metadata.json"),
                         binary, version, args.timeout * 60, limit)
        with lock:
            print(line_of(run, record), flush=True)
        return record

    with ThreadPoolExecutor(max_workers=max(args.jobs, 1)) as pool:
        records = list(pool.map(go, todo))
    left = records.count(None)
    if left and limit.is_set():
        print(f"{plural(left, 'run')} not started: the subscription's limit was reached; run again with --start "
              "once it resets.")
    elif left:
        print(f"{plural(left, 'run')} not started: a stop was asked; run again with --start to start "
              + ("it." if left == 1 else "them."))
    (iteration / STOP).unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
