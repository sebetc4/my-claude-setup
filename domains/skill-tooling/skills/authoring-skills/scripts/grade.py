#!/usr/bin/env python3
"""Grade the complete runs of an iteration: the skill's own evals/grade.py, then the grader agent.

Usage: grade.py <iteration> [--start] [--jobs N] [--timeout MINUTES] [--budget USD]

Lists the complete runs whose grading.json does not hold every assertion of their case,
with the number of grader sessions they may take and their estimated cost: the mean cost
of the skill's complete gradings at the agent's model and effort, or $0.45 a session when
there is none, never above the ceiling. Starts nothing without --start; with it:

1. The listed runs' grading.json files are removed. The skill's evals/grade.py
   <iteration>, when it exists, writes into a run's grading.json the assertions it
   decides, each with its text, passed and evidence. A non-zero exit, or an assertion the
   case does not hold, stops the grading with its message. The other runs' grading.json
   files are kept as they were.
2. Each listed run with assertions left is graded by the agent skill-grader, whose file
   lies in the agents folder beside the skills folder, started as an unattended session
   at the model and effort of its frontmatter, --jobs at a time. The session works in a
   temporary copy of the run's outputs/, changes.json, transcript.md and response.md, and
   of the case's files as inputs/, outside any repository, and answers one JSON object
   that grades the assertions by their numbers in its request.

grading.json holds each assertion with its text, passed, evidence and by (script or
grader), in the case's order; summary; weak, the assertions a wrong output would also
pass, with the reason; claims, the run's claims checked against its files; and grader,
the session's agent, model, effort, tokens and cost, or null. The session's files are
kept in the run's grader/. A stopped session or an answer that cannot be read leaves the
run ungraded, printed with its reason; the next --start grades it again.
"""

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402  (same directory, not an installed package)
import harness  # noqa: E402
import run as runs  # noqa: E402
import usage  # noqa: E402

# The agents folder lies beside the skills folder, in the repository's domain and in ~/.claude.
AGENT = Path(__file__).resolve().parents[3] / "agents" / "skill-grader.md"
JOBS = 4
TIMEOUT = 20
BUDGET = 1.0
DEFAULT_COST = 0.45
RUN_FILES = ("outputs", "changes.json", "transcript.md", "response.md")
FENCE_RE = re.compile(r"```(?:json)?[ \t]*\n(.*?)\n```", re.S)

Refused = runs.Refused


class AnswerError(Exception):
    pass


@dataclass
class Agent:
    """The grader's definition; a session without a name runs without one, as a baseline."""
    name: str
    description: str
    prompt: str
    tools: list
    model: str
    effort: str


@dataclass
class Pending:
    run: runs.Run
    metadata: dict
    scripted: dict = field(default_factory=dict)

    @property
    def left(self):
        return [a for a in self.metadata["assertions"] if a not in self.scripted]


def read_agent(path):
    """The agent's definition from its file; Refused when it cannot serve."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise Refused(f"no grader agent at {path}: {error}")
    parsed = frontmatter.parse(text)
    fields = parsed.fields
    if not fields or parsed.problems:
        raise Refused(f"the frontmatter of {path} cannot be read")
    missing = [key for key in ("name", "description", "model", "effort")
               if not isinstance(fields.get(key), str) or not fields[key].strip()]
    if missing:
        raise Refused(f"{path} names no {' and no '.join(missing)} in its frontmatter: the grader's session "
                      "takes its model and effort from there")
    tools = fields.get("tools") or []
    tools = [t.strip() for t in tools.split(",") if t.strip()] if isinstance(tools, str) else list(tools)
    body = "\n".join(text.splitlines()[parsed.body_line - 1:]).strip() + "\n"
    return Agent(fields["name"], fields["description"], body, tools, fields["model"], fields["effort"])


def grading_of(folder):
    try:
        return json.loads((folder / "grading.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def complete_grading(folder, assertions):
    grading = grading_of(folder)
    if not isinstance(grading, dict) or not isinstance(grading.get("assertions"), list):
        return False
    graded = {a.get("text") for a in grading["assertions"] if isinstance(a, dict)}
    return all(a in graded for a in assertions)


def survey(iteration, recorded):
    """(pending, not complete): the complete runs to grade, and the runs not complete."""
    metadata = {case: runs.read_json(iteration / case / "eval_metadata.json") for case in recorded["cases"]}
    pending, left_out = [], []
    for run in runs.plan(iteration, recorded):
        if run.status() != "complete":
            left_out.append(run)
        elif not complete_grading(run.folder, metadata[run.case]["assertions"]):
            pending.append(Pending(run, metadata[run.case]))
    return pending, left_out


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def estimate(iteration, agent, ceiling):
    """(cost per session, what it rests on)."""
    costs = []
    for path in iteration.parent.glob("iteration-*/*/*/run-*/grading.json"):
        try:
            grader = runs.read_json(path).get("grader") or {}
        except (OSError, ValueError, AttributeError):
            continue
        if (grader.get("model"), grader.get("effort")) == (agent.model, agent.effort) and \
                grader.get("cost_usd") is not None:
            costs.append(grader["cost_usd"])
    if costs:
        cost = statistics.mean(costs)
        basis = (f"${cost:.2f} a session, the mean of {plural(len(costs), 'complete grading')} of this skill "
                 f"at {agent.model} and {agent.effort}")
    else:
        cost = DEFAULT_COST
        basis = (f"$0.45 a session, the mean of skill-auditor's runs measured on 2026-10-06, since no grading of "
                 f"this skill at {agent.model} and {agent.effort} is complete")
    if cost > ceiling:
        return ceiling, f"the session's ceiling, ${ceiling:.2f}, below {basis}"
    return cost, basis


def skill_script(recorded):
    return Path(recorded["skill"]) / recorded.get("evals", "evals") / "grade.py"


def state(folder):
    path = folder / "grading.json"
    return path.read_bytes() if path.is_file() else None


def restore(folder, content):
    path = folder / "grading.json"
    if content is None:
        path.unlink(missing_ok=True)
    else:
        path.write_bytes(content)


def scripted_of(task, shown):
    """The assertions evals/grade.py decided for the run, by text; Refused when it wrote
    one the case does not hold."""
    path = task.run.folder / "grading.json"
    if not path.is_file():
        return {}
    try:
        items = json.loads(path.read_text(encoding="utf-8")).get("assertions")
    except (ValueError, AttributeError) as error:
        raise Refused(f"{shown} wrote a grading.json that cannot be read, for {task.run.name}: {error}")
    if not isinstance(items, list):
        raise Refused(f"{shown} wrote a grading.json without an `assertions` list, for {task.run.name}")
    scripted = {}
    for item in items:
        text = item.get("text") if isinstance(item, dict) else None
        if text not in task.metadata["assertions"]:
            raise Refused(f"{shown} graded an assertion the case does not hold, for {task.run.name}: {text!r}")
        if not isinstance(item.get("passed"), bool):
            raise Refused(f"{shown} gave no boolean `passed` to {text!r}, for {task.run.name}")
        scripted[text] = {"text": text, "passed": item["passed"], "evidence": str(item.get("evidence") or ""),
                          "by": "script"}
    return scripted


def run_skill_script(script, recorded, iteration, pending, others):
    """Run the skill's evals/grade.py and read what it decided; Refused when it fails."""
    shown = f"{recorded.get('evals', 'evals')}/grade.py"
    kept = {run.folder: state(run.folder) for run in others}
    done = subprocess.run([sys.executable, "-B", str(script), str(iteration)], cwd=recorded["root"],
                          capture_output=True, text=True)
    for folder, content in kept.items():
        restore(folder, content)
    try:
        if done.returncode != 0:
            message = (done.stderr.strip() or done.stdout.strip() or "no message")[-2000:]
            raise Refused(f"{shown} stopped the grading, exit code {done.returncode}: {message}")
        for task in pending:
            task.scripted = scripted_of(task, shown)
    except Refused:
        for task in pending:
            restore(task.run.folder, None)
        raise


def request(metadata, left, inputs):
    """What the grader's session is asked: the run's files, the case, and the assertions numbered."""
    files = ["- `outputs/`: the files the run added or changed, at their paths",
             "- `changes.json`: the paths the run added, modified and deleted",
             "- `transcript.md`: the run's prompt, then its calls and their results, in order",
             "- `response.md`: the run's closing account"]
    if inputs:
        files.append("- `inputs/`: the case's files, as the run received them")
    quoted = "\n".join("> " + line if line.strip() else ">" for line in metadata["prompt"].strip().splitlines())
    parts = ["Grade a run of an evaluation case against its assertions. The run's files are in this folder:",
             "\n".join(files), "The run was asked:", quoted]
    if metadata.get("expected_output"):
        parts.append(f"Expected output: {metadata['expected_output']}")
    parts += ["Assertions:", "\n".join(f"{n}. {text}" for n, text in enumerate(left, 1))]
    return "\n\n".join(parts) + "\n"


def json_object(text):
    candidates = [text.strip(), *FENCE_RE.findall(text)]
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        candidates.append(text[start:end + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except ValueError:
            continue
        if isinstance(value, dict):
            return value
    raise AnswerError("no JSON object")


def number_of(item, count, what):
    number = item.get("assertion") if isinstance(item, dict) else None
    if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= count:
        raise AnswerError(f"{what} numbered {number!r}, where the request numbers 1 to {count}")
    return number


def read_answer(text, count):
    """({number: (passed, evidence)}, [(number, reason)], claims) from the grader's answer."""
    value = json_object(text)
    items, weak_items, claim_items = value.get("assertions"), value.get("weak", []), value.get("claims", [])
    if not isinstance(items, list):
        raise AnswerError("no `assertions` list")
    if not isinstance(weak_items, list) or not isinstance(claim_items, list):
        raise AnswerError("`weak` and `claims` must be lists")
    grades = {}
    for item in items:
        number = number_of(item, count, "an assertion")
        if number in grades:
            raise AnswerError(f"assertion {number} is graded twice")
        evidence = item.get("evidence")
        if not isinstance(item.get("passed"), bool):
            raise AnswerError(f"assertion {number} has no boolean `passed`")
        if not isinstance(evidence, str) or not evidence.strip():
            raise AnswerError(f"assertion {number} has no evidence")
        grades[number] = (item["passed"], evidence.strip())
    missing = [str(n) for n in range(1, count + 1) if n not in grades]
    if missing:
        raise AnswerError(f"assertion {missing[0]} is not graded" if len(missing) == 1
                          else f"assertions {', '.join(missing)} are not graded")
    weak = [(number_of(item, count, "a weak assertion"), str(item.get("reason") or "").strip())
            for item in weak_items]
    claims = []
    for item in claim_items:
        if not isinstance(item, dict) or not isinstance(item.get("claim"), str) \
                or not isinstance(item.get("verified"), bool):
            raise AnswerError(f"a claim without its text or a boolean `verified`: {item!r}")
        claims.append({"claim": item["claim"], "verified": item["verified"],
                       "evidence": str(item.get("evidence") or "")})
    return grades, weak, claims


def write_grading(task, grades=None, weak=(), claims=(), grader=None):
    """grading.json from the script's assertions and the grader's; (passed, total)."""
    left = task.left
    entries = []
    for text in task.metadata["assertions"]:
        if text in task.scripted:
            entries.append(task.scripted[text])
        else:
            passed, evidence = grades[left.index(text) + 1]
            entries.append({"text": text, "passed": passed, "evidence": evidence, "by": "grader"})
    passed, total = sum(e["passed"] for e in entries), len(entries)
    summary = {"passed": passed, "failed": total - passed, "total": total,
               "pass_rate": round(passed / total, 2) if total else None}
    data = {"assertions": entries, "summary": summary,
            "weak": [{"text": left[number - 1], "reason": reason} for number, reason in weak],
            "claims": list(claims), "grader": grader}
    (task.run.folder / "grading.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    return passed, total


def copy_run(task, iteration, work):
    for name in RUN_FILES:
        source = task.run.folder / name
        if source.is_dir():
            shutil.copytree(source, work / name, symlinks=True)
        elif source.is_file():
            shutil.copy2(source, work / name)
    (work / "outputs").mkdir(exist_ok=True)
    files = iteration / task.run.case / "files"
    if files.is_dir():
        shutil.copytree(files, work / "inputs", symlinks=True)


def judge(task, iteration, recorded, agent, binary, version, timeout, budget):
    """Grade the run's assertions left in one session; the record of its line. The session's
    files go to the run's grader/, and grading.json is written when its answer reads."""
    folder = task.run.folder / "grader"
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    record = {"agent": agent.name, "status": "stopped", "reason": None, "claude_version": version,
              "model": agent.model, "effort": agent.effort, "budget_usd": budget,
              "started": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    tmp = Path(tempfile.mkdtemp(prefix="skill-grade-")).resolve()
    text = ""
    try:
        runs.check_outside(tmp)
        work = tmp / "run"
        work.mkdir()
        copy_run(task, iteration, work)
        chosen = None
        if agent.name:
            definition = tmp / "agents.json"
            harness.agents_file(definition, agent.name, agent.description, agent.prompt, agent.tools,
                                agent.model, agent.effort)
            chosen = (definition, agent.name)
        settings = harness.hook_settings("PreToolUse", harness.guard_command(runs.GUARD, runs.denied_paths(recorded)))
        line = harness.command(binary, agent.model, agent.effort, budget, settings, agent=chosen)
        prompt = request(task.metadata, task.left, (work / "inputs").is_dir())
        (folder / "prompt.md").write_text(prompt, encoding="utf-8")
        session = harness.start(line, work, prompt, harness.environment(os.environ, {}), timeout)
        result = harness.result_of(session.stdout)
        if result is not None:
            (folder / "result.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        else:
            (folder / "stdout.txt").write_text(session.stdout, encoding="utf-8")
        if session.stderr.strip():
            (folder / "stderr.txt").write_text(session.stderr, encoding="utf-8")
        record["status"], record["reason"] = harness.outcome(session, result)
        figures = harness.figures(result)
        text = figures.pop("response")
        (folder / "response.md").write_text(text.strip() + "\n", encoding="utf-8")
        record.update(figures)
        if record["duration_s"] is None:
            record["duration_s"] = round(session.seconds, 1)
        transcript = harness.transcript_of(record["session_id"])
        if transcript:
            shutil.copy2(transcript, folder / "transcript.jsonl")
            (folder / "transcript.md").write_text(harness.render(transcript), encoding="utf-8")
            counted = usage.as_json(usage.count([transcript]))
            record.update({"models": {m: t["calls"] for m, t in counted["models"].items()},
                           "efforts": counted["efforts"], "calls": counted["calls"],
                           "estimated_calls": counted["estimated"], "tokens": counted["tokens"],
                           "cost_usd": counted["cost"]})
        elif record["status"] == "complete":
            record["status"], record["reason"] = "stopped", "transcript not found"
    except Exception as error:  # a session that fails is recorded and started again by the next --start
        record["status"], record["reason"] = "stopped", f"error: {error}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        record["ended"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if record["status"] == "complete":
        try:
            grades, weak, claims = read_answer(text, len(task.left))
        except AnswerError as error:
            record["status"], record["reason"] = "stopped", f"unreadable answer: {error}"
        else:
            record["passed"], record["total"] = write_grading(task, grades, weak, claims, grader=record)
    (folder / "session.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def line_of(task, record):
    if record["status"] == "complete":
        text = f"{task.run.name}: graded, {record['passed']}/{record['total']} passed"
    else:
        text = f"{task.run.name}: {record['status']} ({record['reason']})"
    if record.get("cost_usd") is not None:
        text += f", ${record['cost_usd']:.2f}"
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description="Grade the complete runs of an iteration.")
    parser.add_argument("iteration", type=Path, help="the iteration's folder")
    parser.add_argument("--start", action="store_true", help="grade them; without it, only list them")
    parser.add_argument("--jobs", type=int, default=JOBS, help=f"grader sessions at a time ({JOBS})")
    parser.add_argument("--timeout", type=float, default=TIMEOUT,
                        help=f"minutes before a grader session is stopped ({TIMEOUT})")
    parser.add_argument("--budget", type=float, default=BUDGET, help=f"dollars a grader session may spend ({BUDGET})")
    args = parser.parse_args(argv)
    iteration = args.iteration.resolve()
    try:
        recorded = runs.read_json(iteration / "iteration.json")
        agent = read_agent(AGENT)
    except (OSError, ValueError) as error:
        print(f"no iteration at {iteration}: {error}", file=sys.stderr)
        return 1
    except Refused as error:
        print(error, file=sys.stderr)
        return 1
    pending, left_out = survey(iteration, recorded)
    for run in left_out:
        print(f"{run.name}: not complete, left out")
    for task in pending:
        print(task.run.name)
    per_session, basis = estimate(iteration, agent, args.budget)
    sessions = sum(1 for task in pending if task.left)
    print(f"{plural(len(pending), 'run')} to grade, {plural(sessions, 'grader session')} at most, "
          f"estimated ${sessions * per_session:.2f}: {basis}.")
    script = skill_script(recorded)
    if pending and script.is_file():
        print(f"With --start, the skill's {recorded.get('evals', 'evals')}/grade.py runs first and may decide some "
              "assertions.")
    if not args.start:
        print("Nothing started: run again with --start to grade them.")
        return 0
    if not pending:
        return 0
    try:
        binary = harness.binary()
        version = harness.version(binary)
        runs.check_outside(Path(tempfile.gettempdir()).resolve())
    except (harness.HarnessError, Refused) as error:
        print(error, file=sys.stderr)
        return 1
    for task in pending:
        restore(task.run.folder, None)
    if script.is_file():
        listed = {task.run.folder for task in pending}
        others = [run for run in runs.plan(iteration, recorded) if run.folder not in listed]
        try:
            run_skill_script(script, recorded, iteration, pending, others)
        except Refused as error:
            print(error, file=sys.stderr)
            return 1
    for task in pending:
        if not task.left:
            passed, total = write_grading(task)
            print(line_of(task, {"status": "complete", "passed": passed, "total": total}))
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=max(args.jobs, 1)) as pool:
        futures = {pool.submit(judge, task, iteration, recorded, agent, binary, version, args.timeout * 60,
                               args.budget): task for task in pending if task.left}
        for future in as_completed(futures):
            with lock:
                print(line_of(futures[future], future.result()), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
