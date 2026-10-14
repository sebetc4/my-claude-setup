#!/usr/bin/env python3
"""Tune a skill's description on its trigger queries: split them into a training and a
held-out set, score each description that triggers.py measured on both sets, have a
session that sees the training results alone propose each rewrite, and keep the best
description on the held-out set.

Usage: tuning.py split <skill-dir> [--seed N]
       tuning.py score <tuning-dir> <results-file>
       tuning.py propose <tuning-dir> [--notes FILE] [--model ID] [--effort LEVEL]
                         [--budget USD] [--timeout MINUTES] [--start]
       tuning.py best <tuning-dir>

split writes <workspace>/skills/<skill-name>/tuning-N/tuning.json: the trigger queries of
evals.json divided per class with a fixed seed, 40% held out, so that each set holds
queries that should trigger and queries that should not; a class of fewer than two
queries is refused.

score records the description a triggers.py results file measured, with its origin — the
skill's own description, a proposal, or given — and the queries it passed in each set.
It refuses another skill's results, a query of the split left unmeasured, results at
another model, effort or number of runs than the first description scored, and a file
already scored.

propose prints the one session it would start and its estimated cost: the mean of the
skill's recorded proposals at that model and effort, else $0.10; never past its ceiling.
Starts nothing without --start. With it, starts a session without any tool, in an empty
folder outside any repository, whose prompt holds the instructions of
assets/description-rewrite.md, the skill's body, the best description on the training
queries — a tie going to the latest — with its training failures, the earlier
descriptions with their training results, and the notes given. No held-out query or
result reaches it. Its answer becomes proposals/N.txt in the tuning folder, to measure
with triggers.py --description; an answer without a description, longer than 1,024
characters or repeating an earlier description is refused and recorded. propose refuses
before any session when no description is scored, when the last proposal is not scored
yet, when every training query passes, after five rewrites, after two rewrites in a row
that gained nothing on the training queries, and when the notes quote a held-out query.

best lists each description's scores and names the best on the held-out queries, a tie
going to the shorter, then to the earlier. split, score and best start no session.
"""

import argparse
import json
import os
import random
import re
import shutil
import statistics
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402  (same directory, not an installed package)
import harness  # noqa: E402
import run as runs  # noqa: E402
import triggers  # noqa: E402
import usage  # noqa: E402
import workspace  # noqa: E402

HERE = Path(__file__).resolve().parent
INSTRUCTIONS = HERE.parent / "assets/description-rewrite.md"
TRIGGERS = HERE / "triggers.py"
FILE = "tuning.json"
HELD_OUT = 0.4
SEED = 42
REWRITES = 5
BUDGET = 0.50
TIMEOUT = 5
# A guess until the skill has a recorded proposal: one turn of Opus 5.5 at xhigh, without tools.
PROPOSAL = 0.10
# The Agent Skills standard's limit on a description.
LIMIT = 1024
ANSWER = re.compile(r"<new_description>(.*?)</new_description>", re.DOTALL)


class Refused(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normal(text):
    return " ".join(text.lower().split())


def tally(rows, part):
    chosen = [r for r in rows if r["set"] == part]
    return {"passed": sum(1 for r in chosen if r["passed"]), "queries": len(chosen)}


def split_queries(queries, seed, share=HELD_OUT):
    """(training queries, held-out queries), each class divided apart, in evals.json's order."""
    seen = set()
    for query in queries:
        if query["query"] in seen:
            raise Refused(f"the query `{query['query']}` appears twice in evals.json")
        seen.add(query["query"])
    rng = random.Random(seed)
    train, held_out = [], []
    for should in (True, False):
        chosen = [q for q in queries if q["should_trigger"] is should]
        if len(chosen) < 2:
            label = "should trigger" if should else "should not trigger"
            raise Refused(f"each set needs queries of both classes, and evals.json holds "
                          f"{triggers.queries_word(len(chosen))} that {label}: 2 at least")
        count = min(max(round(len(chosen) * share), 1), len(chosen) - 1)
        picked = set(rng.sample(range(len(chosen)), count))
        held_out += [q for i, q in enumerate(chosen) if i in picked]
        train += [q for i, q in enumerate(chosen) if i not in picked]
    order = {q["query"]: i for i, q in enumerate(queries)}
    return sorted(train, key=lambda q: order[q["query"]]), sorted(held_out, key=lambda q: order[q["query"]])


def new_folder(base):
    numbers = [int(p.name[len("tuning-"):]) for p in base.glob("tuning-*") if p.name[len("tuning-"):].isdigit()]
    folder = base / f"tuning-{max(numbers, default=0) + 1}"
    folder.mkdir(parents=True)
    return folder


def load_state(folder):
    path = folder / FILE
    if not path.is_file():
        raise Refused(f"no {FILE} in {folder}: start a tuning with `tuning.py split <skill-dir>`")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(folder, state):
    (folder / FILE).write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def figures_of(entry):
    return (f"description {entry['number']} ({entry['origin']}), {entry['characters']} characters: training "
            f"{entry['train']['passed']}/{entry['train']['queries']}, held-out "
            f"{entry['held_out']['passed']}/{entry['held_out']['queries']}")


def best_of(state):
    """The best description on the held-out queries, a tie going to the shorter, then the earlier."""
    return max(state["descriptions"], key=lambda d: (d["held_out"]["passed"], -d["characters"], -d["number"]))


def best_on_training(state):
    """The description a rewrite starts from: the best on the training queries, a tie going to the latest."""
    return max(state["descriptions"], key=lambda d: (d["train"]["passed"], d["number"]))


def origin_of(state, description):
    if description == state["description"]:
        return "skill"
    for proposal in state["proposals"]:
        if proposal["status"] == "proposed" and proposal["description"] == description:
            return f"proposal {proposal['number']}"
    return "given"


def gains(state):
    """For each description after the first, whether it passed more training queries than every one before."""
    found, most = [], None
    for entry in state["descriptions"]:
        passed = entry["train"]["passed"]
        if most is not None:
            found.append(passed > most)
        most = passed if most is None else max(most, passed)
    return found


def stop_reason(state, folder):
    """Why no rewrite may be proposed now, or None."""
    if not state["descriptions"]:
        return (f"no description is scored yet: score the skill's own first, measured by `{TRIGGERS} "
                f"{state['skill_path']} --start`, with `tuning.py score {folder} <results-file>`")
    origins = {d["origin"] for d in state["descriptions"]}
    for proposal in state["proposals"]:
        if proposal["status"] == "proposed" and f"proposal {proposal['number']}" not in origins:
            return (f"proposal {proposal['number']} is not measured yet: `{TRIGGERS} {state['skill_path']} "
                    f"--description {folder / proposal['file']} --start`, then `tuning.py score {folder} "
                    "<results-file>`")
    start = best_on_training(state)
    if start["train"]["passed"] == start["train"]["queries"]:
        return (f"every training query passes with description {start['number']}: nothing left to rewrite from; "
                f"`tuning.py best {folder}` names the description to keep")
    if sum(1 for p in state["proposals"] if p["status"] == "proposed") >= REWRITES:
        return f"five rewrites made, the most a tuning takes: `tuning.py best {folder}` names the description to keep"
    if len(gains(state)) >= 2 and not any(gains(state)[-2:]):
        return (f"two rewrites in a row gained nothing on the training queries: `tuning.py best {folder}` names the "
                "description to keep")
    return None


def split(args):
    skill = args.skill.resolve()
    try:
        _, space, evals = workspace.read_conventions(skill)
        data = workspace.load(skill, evals)
    except workspace.Refused as error:
        raise Refused("\n".join(error.problems))
    queries = data.get("triggers") or []
    if not queries:
        raise Refused(f"no trigger queries in {evals}/evals.json: write about twenty, half that should trigger "
                      "and half near misses that should not, each with `near`")
    train, held_out = split_queries(queries, args.seed)
    description = triggers.description_of((skill / "SKILL.md").read_text(encoding="utf-8"))
    folder = new_folder(space / "skills" / skill.name)
    save_state(folder, {"skill_name": skill.name, "skill_path": str(skill), "created": now(), "seed": args.seed,
                        "held_out_share": HELD_OUT, "description": description, "train": train,
                        "held_out": held_out, "descriptions": [], "proposals": [], "best": None})

    def counts(part):
        should = sum(1 for q in part if q["should_trigger"])
        return f"{should} that should trigger and {len(part) - should} that should not"
    print(f"Split {triggers.queries_word(len(queries))}: {len(train)} for training, {counts(train)}; "
          f"{len(held_out)} held out, {counts(held_out)}.")
    print(f"Written to {folder / FILE}")
    print(f"Next: measure the skill's own description with `{TRIGGERS} {skill}`, which lists its sessions and "
          f"their cost before --start, then `tuning.py score {folder} <results-file>`.")


def score(args):
    folder = args.tuning.resolve()
    state = load_state(folder)
    path = args.results.resolve()
    try:
        results = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Refused(f"cannot read {path}: {error}")
    if results.get("skill_name") != state["skill_name"]:
        raise Refused(f"{path} measured the skill {results.get('skill_name')}, not {state['skill_name']}")
    for entry in state["descriptions"]:
        if entry["results"] == str(path):
            raise Refused(f"{path} is already scored, as description {entry['number']}")
    if state["descriptions"]:
        first = state["descriptions"][0]
        for key in ("model", "effort", "runs"):
            if results.get(key) != first[key]:
                raise Refused(f"{path} was measured with {key} {results.get(key)}, description 1 with {first[key]}: "
                              "descriptions compare only when measured alike")
    description = results.get("description")
    if not isinstance(description, str) or not description:
        raise Refused(f"{path} records no description")
    measured = {q.get("query"): q for q in results.get("queries", [])}
    rows, missing = [], []
    for part in ("train", "held_out"):
        for query in state[part]:
            found = measured.get(query["query"])
            if found is None or found.get("passed") is None:
                missing.append(query["query"])
                continue
            rows.append({"query": query["query"], "set": part, "should_trigger": query["should_trigger"],
                         "triggered": found.get("triggered"), "counted": found.get("counted"),
                         "rate": found.get("rate"), "passed": found["passed"]})
    if missing:
        raise Refused(f"{path} leaves queries of the split unmeasured, which triggers.py measures again with "
                      "--start: " + "; ".join(missing))
    entry = {"number": len(state["descriptions"]) + 1, "origin": origin_of(state, description),
             "description": description, "characters": len(description), "results": str(path),
             "model": results.get("model"), "effort": results.get("effort"), "runs": results.get("runs"),
             "train": tally(rows, "train"), "held_out": tally(rows, "held_out"), "queries": rows}
    state["descriptions"].append(entry)
    state["best"] = best_of(state)["number"]
    save_state(folder, state)
    print(figures_of(entry)[0].upper() + figures_of(entry)[1:] + ".")
    failures = [r for r in rows if r["set"] == "train" and not r["passed"]]
    if failures:
        print("Training failures:")
        for row in failures:
            should = "should trigger" if row["should_trigger"] else "should not trigger"
            print(f"- {should}, used in {row['triggered']} of {row['counted']} sessions: {row['query']}")
    print(f"Best on the held-out queries so far: description {state['best']}.")
    reason = stop_reason(state, folder)
    print(f"The loop stops: {reason}." if reason else
          f"Next: `tuning.py propose {folder}`, which gives the session's cost before --start.")


def request(state, skill_text, start, notes):
    """The prompt of the rewriting session: training results only."""
    parsed = frontmatter.parse(skill_text)
    body = "\n".join(skill_text.split("\n")[parsed.body_line - 1:]).strip()
    near = {q["query"]: q.get("near") for q in state["train"]}

    def results_of(entry, failed_only):
        lines = []
        for row in entry["queries"]:
            if row["set"] != "train" or (failed_only and row["passed"]):
                continue
            line = (f"- {'passed' if row['passed'] else 'failed'}, "
                    f"{'should trigger' if row['should_trigger'] else 'should not trigger'}, used in "
                    f"{row['triggered']} of {row['counted']} sessions: \"{row['query']}\"")
            if not row["should_trigger"] and near.get(row["query"]):
                line += f", a near miss on: {near[row['query']]}"
            lines.append(line)
        return lines

    parts = [INSTRUCTIONS.read_text(encoding="utf-8").strip(), "",
             "## The Skill", "",
             f"Its name: `{state['skill_name']}`. Its body, which an agent reads only once it has chosen the skill:",
             "", "<skill_body>", body, "</skill_body>", "",
             "## The Description To Rewrite", "",
             "<description>", start["description"], "</description>", "",
             f"It passes {start['train']['passed']} of {start['train']['queries']} queries, each run in "
             f"{start['runs']} sessions; a query that should trigger passes when the skill was used in half of "
             "them or more, one that should not when it was used in fewer than half. The queries it got wrong:",
             "", *results_of(start, True)]
    earlier = [d for d in state["descriptions"] if d["number"] != start["number"]]
    if earlier:
        parts += ["", "## Earlier Descriptions"]
        for entry in earlier:
            parts += ["", f"### Passing {entry['train']['passed']} of {entry['train']['queries']}", "",
                      "<description>", entry["description"], "</description>", "", *results_of(entry, False)]
    if notes:
        parts += ["", "## Notes From The Skill's Author", "", notes.strip()]
    return "\n".join(parts) + "\n"


def recorded_proposals(base, model, effort):
    costs = []
    for path in base.glob(f"tuning-*/{FILE}"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for proposal in data.get("proposals", []):
            if (proposal.get("model"), proposal.get("effort")) == (model, effort) and \
                    proposal.get("cost_usd") is not None:
                costs.append(proposal["cost_usd"])
    return costs


def answer_of(text, state):
    """(the description answered, None) or (None, why it is refused)."""
    found = ANSWER.findall(text or "")
    description = " ".join(found[-1].split()) if found else ""
    if not description:
        return None, "the answer holds no description between <new_description> tags"
    if len(description) > LIMIT:
        return None, f"the description is {len(description):,} characters, {LIMIT:,} at most"
    for entry in state["descriptions"]:
        if entry["description"] == description:
            return None, f"the description repeats description {entry['number']}"
    return description, None


def propose(args):
    folder = args.tuning.resolve()
    state = load_state(folder)
    reason = stop_reason(state, folder)
    if reason:
        raise Refused(f"no rewrite now: {reason}")
    notes = args.notes.read_text(encoding="utf-8") if args.notes else ""
    quoted = [q["query"] for q in state["held_out"] if normal(q["query"]) in normal(notes)]
    if quoted:
        raise Refused("the notes quote a held-out query, which the rewriting session must not see: "
                      + "; ".join(quoted))
    start = best_on_training(state)
    costs = recorded_proposals(folder.parent, args.model, args.effort)
    if costs:
        cost = statistics.mean(costs)
        basis = f"the mean of {runs.plural(len(costs), 'proposal')} of this skill recorded at {args.model} and {args.effort}"
    else:
        cost = PROPOSAL
        basis = f"a guess until this skill has a proposal recorded at {args.model} and {args.effort}"
    if cost > args.budget:
        cost, basis = args.budget, basis + f", the session's ceiling of ${args.budget:.2f} capping it"
    print(f"1 session: a rewrite of description {start['number']} by {args.model} at {args.effort}, without tools, "
          f"estimated ${cost:.2f}: {basis}.")
    if not args.start:
        print("Nothing started: run again with --start to start it.")
        return 0
    skill = Path(state["skill_path"])
    prompt = request(state, (skill / "SKILL.md").read_text(encoding="utf-8"), start, notes)
    binary = harness.binary()
    version = harness.version(binary)
    runs.check_outside(Path(tempfile.gettempdir()).resolve())
    tmp = Path(tempfile.mkdtemp(prefix="skill-rewrite-")).resolve()
    session_id = str(uuid.uuid4())
    try:
        runs.check_outside(tmp)
        line = harness.command(binary, args.model, args.effort, args.budget, harness.session_settings(),
                               disallowed=(), tools=(), session_id=session_id)
        session = harness.start(line, tmp, prompt, harness.environment(os.environ, {}), args.timeout * 60)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    result = harness.result_of(session.stdout)
    status, why = harness.outcome(session, result)
    figures = harness.figures(result, session.seconds)
    number = len(state["proposals"]) + 1
    record = {"number": number, "rewrote": start["number"], "status": "stopped" if status != "complete" else None,
              "reason": why, "description": None, "file": None, "notes": bool(notes), "model": args.model,
              "effort": args.effort, "budget_usd": args.budget, "claude_version": version,
              "session_id": figures["session_id"] or session_id, "duration_s": figures["duration_s"],
              "reported_cost_usd": figures["reported_cost_usd"], "cost_usd": None, "started": now()}
    transcript = harness.transcript_of(record["session_id"])
    if transcript:
        counted = usage.as_json(usage.count([transcript]))
        record.update({"models": {m: t["calls"] for m, t in counted["models"].items()},
                       "efforts": counted["efforts"], "cost_usd": counted["cost"]})
    proposals = folder / "proposals"
    proposals.mkdir(exist_ok=True)
    (proposals / f"{number}-request.md").write_text(prompt, encoding="utf-8")
    (proposals / f"{number}-answer.md").write_text(figures["response"], encoding="utf-8")
    if status == "complete":
        description, why = answer_of(figures["response"], state)
        record.update({"status": "proposed" if description else "refused", "reason": why,
                       "description": description})
        if description:
            record["file"] = f"proposals/{number}.txt"
            (folder / record["file"]).write_text(description + "\n", encoding="utf-8")
    state["proposals"].append(record)
    save_state(folder, state)
    cost = "an unknown cost" if record["cost_usd"] is None else f"${record['cost_usd']:.3f}"
    if record["status"] != "proposed":
        print(f"Proposal {number}, {record['status']}, {cost}: {why}. The answer is in "
              f"{proposals / f'{number}-answer.md'}.", file=sys.stderr)
        if harness.limit_reached(result):
            print("The subscription's limit was reached: propose again once it resets.", file=sys.stderr)
        return 1
    print(f"Proposal {number}, a rewrite of description {start['number']}, {cost}:")
    print(record["description"])
    print(f"Written to {folder / record['file']}. Measure it with `{TRIGGERS} {skill} --description "
          f"{folder / record['file']}`, which lists its sessions and their cost before --start, then "
          f"`tuning.py score {folder} <results-file>`.")
    return 0


def best(args):
    folder = args.tuning.resolve()
    state = load_state(folder)
    if not state["descriptions"]:
        raise Refused(f"no description is scored yet: score the skill's own first, with `tuning.py score {folder} "
                      "<results-file>`")
    for entry in state["descriptions"]:
        print(figures_of(entry)[0].upper() + figures_of(entry)[1:])
    chosen = best_of(state)
    print(f"Best on the held-out queries: {figures_of(chosen)}:")
    print(chosen["description"])
    proposal = next((p for p in state["proposals"] if f"proposal {p['number']}" == chosen["origin"]), None)
    if proposal:
        print(f"Its file: {folder / proposal['file']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Tune a skill's description on its trigger queries.")
    commands = parser.add_subparsers(dest="command", required=True)
    one = commands.add_parser("split", help="divide the skill's trigger queries into a training and a held-out set")
    one.add_argument("skill", type=Path, help="the skill's folder")
    one.add_argument("--seed", type=int, default=SEED, help=f"the seed of the split ({SEED})")
    one = commands.add_parser("score", help="record a description's results on both sets")
    one.add_argument("tuning", type=Path, help="the tuning folder that split wrote")
    one.add_argument("results", type=Path, help="a results file that triggers.py wrote")
    one = commands.add_parser("propose", help="have a session without tools rewrite the description")
    one.add_argument("tuning", type=Path, help="the tuning folder that split wrote")
    one.add_argument("--notes", type=Path, help="a file of notes on the skill's intent and the user's feedback, "
                     "for the session; never a held-out query")
    one.add_argument("--model", default=triggers.MODEL, help=f"the session's model, by its full id ({triggers.MODEL})")
    one.add_argument("--effort", choices=workspace.EFFORTS, default=workspace.EFFORT,
                     help=f"the session's effort ({workspace.EFFORT})")
    one.add_argument("--budget", type=float, default=BUDGET, help=f"the session's ceiling, in dollars ({BUDGET})")
    one.add_argument("--timeout", type=float, default=TIMEOUT, help=f"minutes before the session is stopped ({TIMEOUT})")
    one.add_argument("--start", action="store_true", help="start the session; without it, only announce it")
    one = commands.add_parser("best", help="name the best description on the held-out queries")
    one.add_argument("tuning", type=Path, help="the tuning folder that split wrote")
    args = parser.parse_args(argv)
    try:
        return {"split": split, "score": score, "propose": propose, "best": best}[args.command](args) or 0
    except (Refused, harness.HarnessError, runs.Refused) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
