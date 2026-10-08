#!/usr/bin/env python3
"""Measure how often a skill's description makes an agent use it: each trigger query of
the skill's evals.json run several times in fresh, unattended sessions.

Usage: triggers.py <skill-dir> [--description FILE] [--runs N] [--model ID] [--effort LEVEL]
                   [--budget USD] [--jobs N] [--timeout MINUTES] [--start]

Lists the queries and prints the sessions to start, queries × runs, with their estimated
cost: for a query's first session and for each repeat, the mean of the skill's recorded
trigger sessions at that model and effort, kept apart for queries that should trigger and
those that should not, since a near miss is answered in full. Without records, $0.09 and
$0.008 for a query that should trigger, measured on Opus 5.5 at xhigh on 2026-10-06, and
$0.12 and $0.04 for one that should not, measured on 2026-10-06 and 2026-10-08; a
session's estimate never passes its ceiling. Starts nothing without --start.

With it, each query gets a temporary folder outside any repository: work/, a copy of the
repository without the skill's folder, made a git repository, where the session starts;
and added/.claude/skills/, passed with --add-dir, holding the skill's copy without its
evals folder, its description replaced by the --description file's text when one is
given, beside copies of the user's other personal skills, never the installed copy of
the skill under test. A query's runs follow one another in its folder, so that each
repeat reads the first's context from the cache; queries go --jobs at a time. Each
session takes the query alone as its prompt; the model, effort and ceiling given; a run's
flags but the denied tools; the evals' env; guard.py; and trigger_stop.py, which stops it
once it triggered or at its third call. A session triggered when one of its first three
calls used the Skill tool on the skill or named a path under its copy; a call naming the
skill's source in the repository is recorded, not counted.

Writes <workspace>/skills/<skill-name>/triggers/<date-time>.json: the description, model
and effort; per query its sessions, its rate, and whether it passed, at a rate of 0.5 or
more for a query that should trigger and below 0.5 for one that should not; a summary. A
session the subscription's usage limit stops leaves the sessions not yet started
unstarted.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import statistics
import sys
import tempfile
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402  (same directory, not an installed package)
import harness  # noqa: E402
import run as runs  # noqa: E402
import trigger_stop  # noqa: E402
import usage  # noqa: E402
import workspace  # noqa: E402

HOOK = Path(__file__).resolve().parent / "trigger_stop.py"
# Where Claude Code finds the skills of a folder passed with --add-dir.
SKILLS = Path(".claude/skills")
MODEL = "claude-opus-5-5"
RUNS = 3
BUDGET = 0.50
JOBS = 4
TIMEOUT = 10
# A query's first session and a repeat in the same folder, on Opus 5.5 at xhigh, by whether
# the query should trigger (Phase 4 of roadmap skill-tooling): stopped at the trigger
# (task 2, 2026-10-06); a near miss answered in full, $0.12 in this repository (task 2) and
# repeats of $0.03 to $0.04 (task 11, 2026-10-08).
DEFAULTS = {True: (0.09, 0.008), False: (0.12, 0.04)}
MEASURED = {True: "measured on Opus 5.5 at xhigh on 2026-10-06",
            False: "a near miss answered in full, measured on Opus 5.5 at xhigh on 2026-10-06 and 2026-10-08"}
THRESHOLD = 0.5
FOLDER = "triggers"
TOKEN = r"[^\s'\"`;|&()<>]"


class Refused(Exception):
    pass


def queries_word(count):
    return f"{count} quer" + ("y" if count == 1 else "ies")


def description_of(text):
    fields = frontmatter.parse(text).fields or {}
    return fields.get("description")


def with_description(text, description):
    """SKILL.md's text with its frontmatter's description replaced."""
    parsed = frontmatter.parse(text)
    if not parsed.fields or "description" not in parsed.lines:
        raise Refused("the skill's SKILL.md has no description in its frontmatter")
    lines = text.split("\n")
    start = parsed.lines["description"]
    end = min([n for n in parsed.lines.values() if n > start] + [parsed.body_line - 1])
    lines[start - 1:end - 1] = ["description: " + json.dumps(description, ensure_ascii=False)]
    return "\n".join(lines)


def recorded_costs(folder, model, effort):
    """{should_trigger: ([cost of each first session], [cost of each repeat])} recorded at
    model and effort."""
    found = {True: ([], []), False: ([], [])}
    for path in folder.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (data.get("model"), data.get("effort")) != (model, effort):
            continue
        for query in data.get("queries", []):
            firsts, repeats = found[bool(query.get("should_trigger"))]
            for session in query.get("sessions", []):
                if session.get("counted") and session.get("cost_usd") is not None:
                    (firsts if session.get("run") == 1 else repeats).append(session["cost_usd"])
    return found


def estimate(folder, model, effort, budget):
    """({should_trigger: (cost of a query's first session, of a repeat)}, what they rest on)."""
    costs, parts, capped = {}, [], False
    for should, (firsts, repeats) in recorded_costs(folder, model, effort).items():
        label = "a query that should trigger" if should else "one that should not"
        if firsts:
            first = statistics.mean(firsts)
            repeat = statistics.mean(repeats) if repeats else DEFAULTS[should][1]
            source = (f"the means of {len(firsts)} first sessions and {len(repeats)} repeats of this skill recorded "
                      f"at {model} and {effort}")
        else:
            first, repeat = DEFAULTS[should]
            source = f"{MEASURED[should]}, this skill having no such session at {model} and {effort}"
        parts.append(f"{label}, ${first:.3f} for its first session and ${repeat:.3f} for each repeat, {source}")
        capped = capped or max(first, repeat) > budget
        costs[should] = (min(first, budget), min(repeat, budget))
    basis = "; ".join(parts)
    if capped:
        basis += f"; a session's ceiling of ${budget:.2f} capping them"
    return costs, basis


def source_reads(calls, name, copy):
    """The paths of the skill's source, outside its copy, that the calls name."""
    found = re.compile(TOKEN + r"*skills/" + re.escape(name) + r"(?:/" + TOKEN + r"*)?(?=$|[\s'\"`;|&()<>])")
    paths = []
    for _, given in calls:
        for text in harness.strings(given):
            for match in found.finditer(text.replace(str(copy), "")):
                if match.group(0) not in paths:
                    paths.append(match.group(0))
    return paths


def judge(calls, name, copy):
    """(triggered, the number of the call that triggered or None), from the first calls."""
    for number, (tool, given) in enumerate(calls[:trigger_stop.CALLS], 1):
        if trigger_stop.triggered(tool, given, name, copy):
            return True, number
    return False, None


class Trial:
    """What every session of one trigger eval shares."""

    def __init__(self, skill, root, evals, env, name, description, model, effort, budget, timeout, binary,
                 version, base, personal):
        self.skill, self.root, self.evals, self.env, self.name = skill, root, evals, env, name
        self.description, self.model, self.effort, self.budget = description, model, effort, budget
        self.timeout, self.binary, self.version, self.base, self.personal = timeout, binary, version, base, personal
        self.limit = threading.Event()

    def prepare(self, tmp):
        """The query's work/ and added/ folders; the skill's copy."""
        runs.check_outside(tmp)
        work = tmp / "work"
        work.mkdir()
        runs.extract(self.base, work)
        for args in (("init", "-q"), ("add", "-A", "-f"), ("commit", "-q", "--allow-empty", "-m", "base")):
            done = runs.git(work, *args)
            if done.returncode != 0:
                raise Refused(f"git {args[0]} in the query's folder failed: {done.stderr.strip()}")
        skills = tmp / "added" / SKILLS
        copy = skills / self.name
        workspace.copy_skill(self.skill, copy, self.evals)
        if self.description is not None:
            text = (copy / "SKILL.md").read_text(encoding="utf-8")
            (copy / "SKILL.md").write_text(with_description(text, self.description), encoding="utf-8")
        for other in self.personal:
            shutil.copytree(other, skills / other.name, symlinks=True)
        return work, tmp / "added", copy

    def session(self, number, query, work, added, copy, env, log):
        """One session of the query; its record."""
        session_id = str(uuid.uuid4())
        guard = harness.guard_command(runs.GUARD, runs.denied_paths({"root": self.root}))
        stop = shlex.join([sys.executable, "-B", str(HOOK), str(log), self.name, str(copy)])
        settings = harness.session_settings(("PreToolUse", guard), ("PostToolUse", stop))
        line = harness.command(self.binary, self.model, self.effort, self.budget, settings, add_dirs=[added],
                               disallowed=(), session_id=session_id)
        session = harness.start(line, work, query, env, self.timeout)
        result = harness.result_of(session.stdout)
        if harness.limit_reached(result):
            self.limit.set()
        status, reason = harness.outcome(session, result)
        figures = harness.figures(result)
        figures.pop("response")
        record = {"run": number, **figures, "session_id": figures["session_id"] or session_id, "status": status,
                  "reason": reason, "claude_version": self.version}
        transcript = harness.transcript_of(record["session_id"])
        calls = harness.tool_calls(transcript) if transcript else []
        record["counted"] = (transcript is not None and result is not None and not session.timed_out
                             and not result.get("api_error"))
        record["triggered"], record["trigger_call"] = judge(calls, self.name, copy)
        record["calls"] = [[tool, runs.short(given)] for tool, given in calls]
        record["source_reads"] = source_reads(calls, self.name, copy)
        if transcript:
            counted = usage.as_json(usage.count([transcript]))
            record.update({"models": {m: t["calls"] for m, t in counted["models"].items()},
                           "efforts": counted["efforts"], "cost_usd": counted["cost"]})
        if record["duration_s"] is None:
            record["duration_s"] = round(session.seconds, 1)
        return record

    def query(self, index, query, count):
        """The query's sessions, one after the other in one folder."""
        records = []
        tmp = Path(tempfile.mkdtemp(prefix="skill-trigger-")).resolve()
        try:
            work, added, copy = self.prepare(tmp)
            env = harness.environment(os.environ, {k: v.replace("{tmp}", str(tmp)) for k, v in self.env.items()})
            for number in range(1, count + 1):
                if self.limit.is_set():
                    break
                records.append(self.session(number, query, work, added, copy, env, tmp / f"calls-{number}.jsonl"))
        except Exception as error:  # a query that fails is recorded, the others go on
            records.append({"run": len(records) + 1, "status": "stopped", "reason": f"error: {error}",
                            "counted": False, "triggered": False, "trigger_call": None})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return records


def outcome_of(trigger, sessions):
    counted = [s for s in sessions if s.get("counted")]
    hits = sum(1 for s in counted if s["triggered"])
    rate = hits / len(counted) if counted else None
    passed = None if rate is None else (rate >= THRESHOLD if trigger["should_trigger"] else rate < THRESHOLD)
    found = {"query": trigger["query"], "should_trigger": trigger["should_trigger"]}
    if "near" in trigger:
        found["near"] = trigger["near"]
    return {**found, "triggered": hits, "counted": len(counted), "rate": rate, "passed": passed,
            "sessions": sessions}


def line_of(found):
    should = "should trigger" if found["should_trigger"] else "should not trigger"
    if found["rate"] is None:
        return f"not measured, {should}: {found['query']}"
    verdict = "passed" if found["passed"] else "failed"
    return (f"{found['triggered']}/{found['counted']} triggered, rate {found['rate']:.2f}, {should}: {verdict} — "
            f"{found['query']}")


def summary_of(results, planned):
    started = [s for q in results for s in q["sessions"]]
    costs = [s["cost_usd"] for s in started if s.get("cost_usd") is not None]

    def side(should):
        chosen = [q for q in results if q["should_trigger"] is should]
        return {"queries": len(chosen), "passed": sum(1 for q in chosen if q["passed"])}
    return {"queries": len(results), "passed": sum(1 for q in results if q["passed"]),
            "failed": sum(1 for q in results if q["passed"] is False),
            "not_measured": sum(1 for q in results if q["passed"] is None),
            "should_trigger": side(True), "should_not_trigger": side(False),
            "sessions": sum(1 for s in started if s.get("counted")), "not_started": planned - len(started),
            "source_reads": sum(len(s.get("source_reads", [])) for s in started),
            "cost_usd": sum(costs) if costs else None}


def results_path(folder):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    path, n = folder / f"{stamp}.json", 1
    while path.exists():
        n += 1
        path = folder / f"{stamp}-{n}.json"
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Measure how often a skill's description makes an agent use it.")
    parser.add_argument("skill", type=Path, help="the skill's folder")
    parser.add_argument("--description", type=Path, help="a file whose text replaces the skill's description in "
                        "the sessions' copy")
    parser.add_argument("--runs", type=int, default=RUNS, help=f"sessions per query ({RUNS})")
    parser.add_argument("--model", default=MODEL, help=f"the sessions' model, by its full id ({MODEL}): the model "
                        "of the sessions the skill serves")
    parser.add_argument("--effort", choices=workspace.EFFORTS, default=workspace.EFFORT,
                        help=f"the sessions' effort ({workspace.EFFORT})")
    parser.add_argument("--budget", type=float, default=BUDGET, help=f"the ceiling per session, in dollars ({BUDGET})")
    parser.add_argument("--jobs", type=int, default=JOBS, help=f"queries at a time ({JOBS})")
    parser.add_argument("--timeout", type=float, default=TIMEOUT, help=f"minutes before a session is stopped ({TIMEOUT})")
    parser.add_argument("--start", action="store_true", help="start the sessions; without it, only list them")
    args = parser.parse_args(argv)
    skill = args.skill.resolve()
    try:
        root, space, evals = workspace.read_conventions(skill)
        data = workspace.load(skill, evals)
    except workspace.Refused as error:
        for problem in error.problems:
            print(problem, file=sys.stderr)
        return 1
    queries = data.get("triggers") or []
    if not queries:
        print(f"no trigger queries in {evals}/evals.json: write about twenty, half that should trigger and half "
              "near misses that should not, each with `near`", file=sys.stderr)
        return 1
    given = args.description.read_text(encoding="utf-8").strip() if args.description else None
    name = skill.name
    folder = space / "skills" / name / FOLDER
    costs, basis = estimate(folder, args.model, args.effort, args.budget)
    for number, trigger in enumerate(queries, 1):
        should = "should trigger" if trigger["should_trigger"] else "should not trigger"
        print(f"{number}. {should}: {trigger['query']}")
    planned = len(queries) * args.runs
    cost = sum(costs[t["should_trigger"]][0] + (args.runs - 1) * costs[t["should_trigger"]][1] for t in queries)
    print(f"{runs.plural(planned, 'session')}: {queries_word(len(queries))} × {runs.plural(args.runs, 'run')}, "
          f"estimated ${cost:.2f}: {basis}.")
    if not args.start:
        print("Nothing started: run again with --start to start them.")
        return 0
    base_dir = None
    try:
        binary = harness.binary()
        version = harness.version(binary)
        runs.check_outside(Path(tempfile.gettempdir()).resolve())
        base_dir = Path(tempfile.mkdtemp(prefix="skill-triggers-")).resolve()
        workspace.write_base(root, workspace.base_files(root, skill, space), base_dir / "base.tar")
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        if given is not None:
            with_description(text, given)
        description = given if given is not None else description_of(text)
        personal = [d for d in sorted((harness.config_dir() / "skills").glob("*"))
                    if d.is_dir() and (d / "SKILL.md").is_file() and d.name != name]
        trial = Trial(skill, root, evals, data.get("env", {}), name, given, args.model, args.effort, args.budget,
                      args.timeout * 60, binary, version, base_dir / "base.tar", personal)
        started = datetime.now(timezone.utc).isoformat(timespec="seconds")
        lock = threading.Lock()

        def go(numbered):
            index, trigger = numbered
            found = outcome_of(trigger, trial.query(index, trigger["query"], args.runs))
            with lock:
                print(line_of(found), flush=True)
            return found

        with ThreadPoolExecutor(max_workers=max(args.jobs, 1)) as pool:
            results = list(pool.map(go, enumerate(queries, 1)))
    except (harness.HarnessError, runs.Refused, workspace.Refused, Refused) as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        if base_dir:
            shutil.rmtree(base_dir, ignore_errors=True)
    summary = summary_of(results, planned)
    record = {"skill_name": name, "description": description, "description_file": str(args.description.resolve())
              if args.description else None, "model": args.model, "effort": args.effort, "runs": args.runs,
              "budget_usd": args.budget, "threshold": THRESHOLD, "claude_version": version, "started": started,
              "ended": datetime.now(timezone.utc).isoformat(timespec="seconds"), "summary": summary,
              "queries": results}
    folder.mkdir(parents=True, exist_ok=True)
    path = results_path(folder)
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    should, should_not = summary["should_trigger"], summary["should_not_trigger"]
    cost = "an unknown cost" if summary["cost_usd"] is None else f"${summary['cost_usd']:.2f}"
    print(f"Should trigger: {should['passed']} of {should['queries']} passed; should not trigger: "
          f"{should_not['passed']} of {should_not['queries']} passed; "
          f"{runs.plural(summary['sessions'], 'session')} counted, {cost}.")
    if summary["source_reads"]:
        print(f"{runs.plural(summary['source_reads'], 'call')} named the skill's source in the repository: "
              "recorded, not counted.")
    if summary["not_started"] and trial.limit.is_set():
        print(f"{runs.plural(summary['not_started'], 'session')} not started: the subscription's limit was "
              "reached; run again with --start once it resets.")
    print(f"Written to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
