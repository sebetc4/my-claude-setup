#!/usr/bin/env python3
"""Compare the outputs of two versions of a skill blind, for when the benchmark does not separate them.

Usage: compare.py <iteration> [<other-iteration>] [--case NAME ...] [--start] [--jobs N] [--timeout MINUTES]
                  [--budget USD]

The two versions: with one iteration, its two configurations, the skill's first —
with_skill against old_skill or without_skill —; with two iterations of the same skill,
the first configuration of each, on the cases both hold with the same prompt. A version
is named <iteration>/<configuration>. Each case's runs of the same number, complete in
both versions, make a pair, which the agent skill-comparator judges in three sessions;
its file lies in the agents folder beside the skills folder. A session sees the two
outputs as A and B: the first session's labels are drawn at random and the next ones
alternate them, so that each version is shown in both places. The key stays in the
comparison's folder, which the sessions' guard refuses, as it refuses the iterations.

Lists the pairs, and the cases and runs left out with the reason, with the number of
sessions to start and their estimated cost: the mean cost of the skill's complete
comparator sessions at the agent's model and effort, or $0.45 a session when there is
none, never above the ceiling. Starts nothing without --start; with it, starts the
sessions not yet complete, --jobs at a time, each at the model and effort of the agent's
frontmatter in a temporary folder outside any repository, holding a/ and b/ — each
output's outputs/ and response.md, never its transcript — and the case's files as
inputs/.

Writes comparison-N/ beside the iterations, the one that compares the same two versions
when there is one: comparison.json — the versions, each pair's labels, sessions and
verdict, the pairs left out and a summary —, comparison.md, and each session's files in
<case>/run-N/session-M/, with session.json, where the answer is unblinded: its winner,
scores, assertions, strengths and weaknesses keyed by version, its reason as written
beside the labels. A pair's verdict is the version, or the tie, that two sessions agree
on, split when every session is complete and none agree. A stopped session, or one whose
answer cannot be read, counts for no version, and the next --start starts it again with
the same labels.
"""

import argparse
import json
import random
import shutil
import statistics
import sys
import tempfile
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grade  # noqa: E402  (same directory, not an installed package)
import harness  # noqa: E402
import run as runs  # noqa: E402

# The agents folder lies beside the skills folder, in the repository's domain and in ~/.claude.
AGENT = Path(__file__).resolve().parents[3] / "agents" / "skill-comparator.md"
SESSIONS = 3
JOBS = 4
TIMEOUT = 20
BUDGET = 1.0
DEFAULT_COST = 0.45
LABELS = ("A", "B")
CRITERIA = ("correctness", "completeness", "form")
DRAW = random.SystemRandom()

Refused = runs.Refused
AnswerError = grade.AnswerError


@dataclass
class Version:
    iteration: Path
    recorded: dict
    configuration: str

    @property
    def name(self):
        return f"{self.iteration.name}/{self.configuration}"

    def run(self, case, number):
        return runs.Run(case, self.configuration, number, self.iteration / case / self.configuration / f"run-{number}")

    def metadata(self, case):
        return runs.read_json(self.iteration / case / "eval_metadata.json")


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def read_iteration(folder):
    try:
        return runs.read_json(folder / "iteration.json")
    except (OSError, ValueError) as error:
        raise Refused(f"no iteration at {folder}: {error}")


def versions_of(first, second=None):
    """The two versions compared; Refused when the iterations cannot give two."""
    recorded = read_iteration(first)
    if second is None:
        configurations = recorded["configurations"]
        if len(configurations) != 2:
            raise Refused(f"{first.name} holds one configuration, {configurations[0]}: name a second iteration to "
                          "compare with")
        return Version(first, recorded, configurations[0]), Version(first, recorded, configurations[1])
    if second == first:
        raise Refused(f"{first.name} is named twice: name it once to compare its two configurations")
    other = read_iteration(second)
    if other["skill_name"] != recorded["skill_name"]:
        raise Refused(f"{first.name} is of the skill {recorded['skill_name']} and {second.name} of the skill "
                      f"{other['skill_name']}: compare two versions of one skill")
    a, b = Version(first, recorded, recorded["configurations"][0]), Version(second, other, other["configurations"][0])
    if a.name == b.name:
        raise Refused(f"both versions are named {a.name}: compare iterations of one workspace")
    return a, b


def cases_of(a, b, wanted):
    """(the cases compared, [(case, reason)] left out); Refused for a case neither version holds."""
    held = list(dict.fromkeys(a.recorded["cases"] + b.recorded["cases"]))
    unknown = [name for name in wanted or [] if name not in held]
    if unknown:
        raise Refused("\n".join(f"no case named `{name}` in {a.iteration.name} or {b.iteration.name}"
                                for name in unknown))
    chosen, left_out = [], []
    for name in held:
        if wanted and name not in wanted:
            continue
        if name not in a.recorded["cases"] or name not in b.recorded["cases"]:
            holder = a if name in a.recorded["cases"] else b
            left_out.append((name, f"only {holder.iteration.name} holds it"))
        elif a.iteration != b.iteration and a.metadata(name)["prompt"] != b.metadata(name)["prompt"]:
            left_out.append((name, "the prompts differ"))
        else:
            chosen.append(name)
    return chosen, left_out


def pairs_of(a, b, cases):
    """([(case, number)], [(name, reason)]): the runs complete in both versions pair by number."""
    pairs, left_out = [], []
    for case in cases:
        for number in range(1, min(a.recorded["runs"], b.recorded["runs"]) + 1):
            missing = [f"{v.name}/run-{number}" for v in (a, b) if v.run(case, number).status() != "complete"]
            if missing:
                verb = "is" if len(missing) == 1 else "are"
                left_out.append((f"{case}/run-{number}", f"{' and '.join(missing)} {verb} not complete"))
            else:
                pairs.append((case, number))
    return pairs, left_out


def same_versions(recorded, a, b):
    found = [(v.get("iteration"), v.get("configuration")) for v in recorded.get("versions", [])]
    return found == [(str(a.iteration), a.configuration), (str(b.iteration), b.configuration)]


def comparison_of(a, b):
    """(folder, record): the comparison of these two versions, or the next folder and None."""
    parent, numbers = a.iteration.parent, [0]
    for folder in sorted(parent.glob("comparison-*")):
        suffix = folder.name.removeprefix("comparison-")
        if suffix.isdigit():
            numbers.append(int(suffix))
        try:
            recorded = runs.read_json(folder / "comparison.json")
        except (OSError, ValueError):
            continue
        if same_versions(recorded, a, b):
            return folder, recorded
    return parent / f"comparison-{max(numbers) + 1}", None


def labels_of(a, b):
    """Each session's labels: the first drawn, the next alternating."""
    first = {"A": a.name, "B": b.name}
    if DRAW.choice((False, True)):
        first = {"A": b.name, "B": a.name}
    second = {"A": first["B"], "B": first["A"]}
    return [dict(first if index % 2 == 0 else second) for index in range(SESSIONS)]


def session_folder(folder, case, number, index):
    return folder / case / f"run-{number}" / f"session-{index}"


def session_of(folder, case, number, index):
    try:
        return runs.read_json(session_folder(folder, case, number, index) / "session.json")
    except (OSError, ValueError):
        return None


def complete(record):
    return bool(record) and record.get("status") == "complete"


def estimate(parent, agent, ceiling):
    """(cost per session, what it rests on)."""
    costs = []
    for path in parent.glob("comparison-*/*/run-*/session-*/session.json"):
        try:
            record = runs.read_json(path)
        except (OSError, ValueError):
            continue
        if complete(record) and (record.get("model"), record.get("effort")) == (agent.model, agent.effort) \
                and record.get("cost_usd") is not None:
            costs.append(record["cost_usd"])
    if costs:
        cost = statistics.mean(costs)
        basis = (f"${cost:.2f} a session, the mean of {plural(len(costs), 'complete comparator session')} of this "
                 f"skill at {agent.model} and {agent.effort}")
    else:
        cost = DEFAULT_COST
        basis = (f"$0.45 a session, the mean of skill-auditor's runs measured on 2026-10-06, since no comparator "
                 f"session of this skill at {agent.model} and {agent.effort} is complete")
    if cost > ceiling:
        return ceiling, f"the session's ceiling, ${ceiling:.2f}, below {basis}"
    return cost, basis


def request(metadata, inputs):
    """What the comparator's session is asked: the two outputs' files, the case, and the assertions numbered."""
    files = ["- `a/outputs/` and `b/outputs/`: the files each output added or changed, at their paths",
             "- `a/response.md` and `b/response.md`: each output's closing account"]
    if inputs:
        files.append("- `inputs/`: the case's files, as both outputs received them")
    quoted = "\n".join("> " + line if line.strip() else ">" for line in metadata["prompt"].strip().splitlines())
    parts = ["Compare two outputs of the same request, A and B. Their files are in this folder:",
             "\n".join(files), "Both were asked:", quoted]
    if metadata.get("expected_output"):
        parts.append(f"Expected output: {metadata['expected_output']}")
    if metadata["assertions"]:
        parts += ["Assertions:", "\n".join(f"{n}. {text}" for n, text in enumerate(metadata["assertions"], 1))]
    return "\n\n".join(parts) + "\n"


def copy_outputs(source, target):
    target.mkdir()
    if (source / "outputs").is_dir():
        shutil.copytree(source / "outputs", target / "outputs", symlinks=True)
    else:
        (target / "outputs").mkdir()
    if (source / "response.md").is_file():
        shutil.copy2(source / "response.md", target / "response.md")


def read_answer(text, count):
    """The comparator's answer, by label: winner (A, B or tie), reason, scores, assertions
    {number: ({label: passed}, evidence)}, strengths and weaknesses. Each output's object
    holds its scores and lists and nothing else, so that an object left open, whose next key
    falls inside it while the JSON still parses, is refused."""
    value = grade.json_object(text)
    given = value.get("winner")
    winner = given.strip() if isinstance(given, str) else ""
    if winner.upper() in LABELS:
        winner = winner.upper()
    elif winner.lower() == "tie":
        winner = "tie"
    else:
        raise AnswerError(f"winner {given!r}, where A, B or tie is asked")
    reason = value.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise AnswerError("no reason")
    checked, lists = {}, {"strengths": {}, "weaknesses": {}}
    for label in LABELS:
        output = value.get(label)
        if not isinstance(output, dict):
            raise AnswerError(f"no `{label}` object")
        extra = [key for key in output if key not in (*CRITERIA, *lists)]
        if extra:
            raise AnswerError(f"`{label}` holds " + ", ".join(f"`{key}`" for key in extra)
                              + ", which the answer's format puts elsewhere: an object is left open")
        for criterion in CRITERIA:
            mark = output.get(criterion)
            if not isinstance(mark, int) or isinstance(mark, bool) or not 1 <= mark <= 5:
                raise AnswerError(f"{label}'s {criterion} scored {mark!r}, where 1 to 5 is asked")
        checked[label] = {criterion: output[criterion] for criterion in CRITERIA}
        for key in lists:
            items = output.get(key)
            if not isinstance(items, list):
                raise AnswerError(f"{label}'s `{key}` must be a list")
            lists[key][label] = [str(item) for item in items]
    items = value.get("assertions", [])
    if not isinstance(items, list):
        raise AnswerError("`assertions` must be a list")
    compared = {}
    for item in items:
        number = grade.number_of(item, count, "an assertion")
        if number in compared:
            raise AnswerError(f"assertion {number} is compared twice")
        if not all(isinstance(item.get(label), bool) for label in LABELS):
            raise AnswerError(f"assertion {number} has no boolean A and B")
        evidence = item.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            raise AnswerError(f"assertion {number} has no evidence")
        compared[number] = ({label: item[label] for label in LABELS}, evidence.strip())
    missing = [str(n) for n in range(1, count + 1) if n not in compared]
    if missing:
        raise AnswerError(f"assertion {missing[0]} is not compared" if len(missing) == 1
                          else f"assertions {', '.join(missing)} are not compared")
    return {"winner": winner, "reason": reason.strip(), "scores": checked, "assertions": compared, **lists}


def unblind(answer, labels, assertions):
    """The answer keyed by version; its reason stays as written, beside the labels."""
    def keyed(by_label):
        return {labels[label]: by_label[label] for label in LABELS}
    return {"winner": answer["winner"] if answer["winner"] == "tie" else labels[answer["winner"]],
            "reason": answer["reason"], "scores": keyed(answer["scores"]),
            "assertions": [{"text": text, "passed": keyed(answer["assertions"][n][0]),
                            "evidence": answer["assertions"][n][1]} for n, text in enumerate(assertions, 1)],
            "strengths": keyed(answer["strengths"]), "weaknesses": keyed(answer["weaknesses"])}


def judge(folder, case, number, index, labels, versions, agent, denied, binary, version, timeout, budget):
    """One comparator session on a pair; its record, written to the session's session.json."""
    first = versions[0]
    metadata = first.metadata(case)
    shown = {version.name: version for version in versions}

    def prepare(work):
        for label in LABELS:
            copy_outputs(shown[labels[label]].run(case, number).folder, work / label.lower())
        files = first.iteration / case / "files"
        if files.is_dir():
            shutil.copytree(files, work / "inputs", symlinks=True)
        return request(metadata, (work / "inputs").is_dir())

    target = session_folder(folder, case, number, index)
    record, text = grade.converse(agent, target, prepare, denied, binary, version, timeout, budget)
    record.update({"case": case, "run": number, "session": index, "labels": labels, "winner": None,
                   "shown_winner": None, "answer": None})
    if record["status"] == "complete":
        try:
            answer = read_answer(text, len(metadata["assertions"]))
        except AnswerError as error:
            record["status"], record["reason"] = "stopped", f"unreadable answer: {error}"
        else:
            record["answer"] = unblind(answer, labels, metadata["assertions"])
            record["winner"], record["shown_winner"] = record["answer"]["winner"], answer["winner"]
    (target / "session.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return record


def verdict(sessions):
    """(verdict, how many sessions agree): the winner two complete sessions agree on; split
    when every session is complete and none agree; None while sessions are missing."""
    winners = [s["winner"] for s in sessions if complete(s)]
    if winners:
        top, count = Counter(winners).most_common(1)[0]
        if count >= 2:
            return top, count
    return ("split" if len(winners) == SESSIONS else None), 0


def mean(values):
    return round(statistics.mean(values), 2) if values else None


def summarize(folder, a, b, plan, left_out, agent):
    """The comparison's record, read from its sessions' files."""
    names = (a.name, b.name)
    pairs, judged = [], []
    for entry in plan:
        sessions = [session_of(folder, entry["case"], entry["run"], index) for index in range(1, SESSIONS + 1)]
        judged += [s for s in sessions if s]
        found, agreeing = verdict(sessions)
        pairs.append({**entry, "sessions": [
            {"session": index, "status": (s or {}).get("status", "not started"), "reason": (s or {}).get("reason"),
             "winner": (s or {}).get("winner"), "cost_usd": (s or {}).get("cost_usd")}
            for index, s in enumerate(sessions, 1)], "verdict": found, "agreeing": agreeing})
    answers = [s["answer"] for s in judged if complete(s)]
    verdicts = Counter("pending" if p["verdict"] is None else p["verdict"] for p in pairs)
    costs = [s.get("cost_usd") for s in judged if "cost_usd" in s]
    summary = {
        "pairs": len(pairs),
        "verdicts": {key: verdicts.get(key, 0) for key in (*names, "tie", "split", "pending")},
        "sessions": dict(Counter(s.get("status") for s in judged)),
        "label_wins": {key: sum(1 for s in judged if complete(s) and s["shown_winner"] == key)
                       for key in (*LABELS, "tie")},
        "scores": {name: {criterion: mean([x["scores"][name][criterion] for x in answers])
                          for criterion in CRITERIA} for name in names},
        "assertions": {name: {"passed": sum(item["passed"][name] for x in answers for item in x["assertions"]),
                              "checked": sum(len(x["assertions"]) for x in answers)} for name in names},
        "cost_usd": None if None in costs else sum(costs),
    }
    return {"skill_name": a.recorded["skill_name"],
            "versions": [{"name": v.name, "iteration": str(v.iteration), "configuration": v.configuration}
                         for v in (a, b)],
            "agent": {"name": agent.name, "model": agent.model, "effort": agent.effort},
            "sessions_per_pair": SESSIONS, "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pairs": pairs, "left_out": [{"name": name, "reason": reason} for name, reason in left_out],
            "summary": summary}


def shown(value):
    return f"`{value}`" if value not in (None, "tie", "split") else (value or "pending")


def markdown(data, folder):
    names = [v["name"] for v in data["versions"]]
    summary = data["summary"]
    agent = data["agent"]
    lines = [f"# Blind Comparison: {data['skill_name']}", "",
             f"`{names[0]}` against `{names[1]}`, {data['sessions_per_pair']} sessions a pair, judged by "
             f"{agent['name']} on {agent['model']} at {agent['effort']}.", "",
             "| Pair | Verdict | " + " | ".join(f"Session {n}" for n in range(1, data["sessions_per_pair"] + 1)) + " |",
             "|---" * (data["sessions_per_pair"] + 2) + "|"]
    for pair in data["pairs"]:
        found = shown(pair["verdict"]) + (f", {pair['agreeing']} of {data['sessions_per_pair']}"
                                           if pair["agreeing"] else "")
        cells = [shown(s["winner"]) if s["status"] == "complete" else s["status"] for s in pair["sessions"]]
        lines.append(f"| {pair['case']}/run-{pair['run']} | {found} | " + " | ".join(cells) + " |")
    lines += ["", "| Version | Pairs won | " + " | ".join(c.capitalize() for c in CRITERIA) + " | Assertions passed |",
              "|---|---|---|---|---|---|"]
    for name in names:
        marks = " | ".join("—" if summary["scores"][name][c] is None else f"{summary['scores'][name][c]:.2f}"
                           for c in CRITERIA)
        passed = summary["assertions"][name]
        lines.append(f"| `{name}` | {summary['verdicts'][name]} | {marks} | {passed['passed']}/{passed['checked']} |")
    verdicts, wins = summary["verdicts"], summary["label_wins"]
    cost = "unknown" if summary["cost_usd"] is None else f"${summary['cost_usd']:.2f}"
    lines += ["", f"Ties {verdicts['tie']}, split {verdicts['split']}, pending {verdicts['pending']}. The output "
              f"shown as A won {wins['A']} sessions, as B {wins['B']}, and {wins['tie']} were ties. Cost: {cost}.",
              "", "## Reasons"]
    for pair in data["pairs"]:
        for entry, labels in zip(pair["sessions"], pair["labels"]):
            record = session_of(folder, pair["case"], pair["run"], entry["session"])
            if not complete(record):
                continue
            answer = record["answer"]
            lines += ["", f"### {pair['case']}/run-{pair['run']}, session {entry['session']}", "",
                      f"A = `{labels['A']}`, B = `{labels['B']}`. Winner: {shown(answer['winner'])}.", "",
                      answer["reason"], ""]
            for key in ("strengths", "weaknesses"):
                for name in names:
                    if answer[key][name]:
                        lines.append(f"- {key.capitalize()} of `{name}`: " + "; ".join(answer[key][name]))
    if data["left_out"]:
        lines += ["", "## Left Out", ""] + [f"- {item['name']}: {item['reason']}" for item in data["left_out"]]
    return "\n".join(lines) + "\n"


def write(folder, data):
    (folder / "comparison.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    (folder / "comparison.md").write_text(markdown(data, folder), encoding="utf-8")


def line_of(case, number, index, record):
    text = f"{case}/run-{number}/session-{index}: "
    if record["status"] == "complete":
        text += "tie" if record["winner"] == "tie" else f"{record['winner']} wins"
    else:
        text += f"{record['status']} ({record['reason']})"
    if record.get("cost_usd") is not None:
        text += f", ${record['cost_usd']:.2f}"
    return text


def verdict_line(pair):
    name = f"{pair['case']}/run-{pair['run']}"
    if pair["verdict"] is None:
        done = sum(1 for s in pair["sessions"] if s["status"] == "complete")
        return f"{name}: pending, {done} of {SESSIONS} sessions complete"
    if pair["verdict"] == "split":
        return f"{name}: split, " + ", ".join(str(s["winner"]) for s in pair["sessions"])
    return f"{name}: {pair['verdict']}, {pair['agreeing']} of {SESSIONS}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare the outputs of two versions of a skill blind.")
    parser.add_argument("iteration", type=Path, help="an iteration: its two configurations, or its first against "
                        "the other iteration's")
    parser.add_argument("other", type=Path, nargs="?", help="a second iteration of the same skill")
    parser.add_argument("--case", dest="cases", action="append", help="a case whose pairs to compare; every case "
                        "by default")
    parser.add_argument("--start", action="store_true", help="start the sessions; without it, only list them")
    parser.add_argument("--jobs", type=int, default=JOBS, help=f"comparator sessions at a time ({JOBS})")
    parser.add_argument("--timeout", type=float, default=TIMEOUT,
                        help=f"minutes before a comparator session is stopped ({TIMEOUT})")
    parser.add_argument("--budget", type=float, default=BUDGET,
                        help=f"dollars a comparator session may spend ({BUDGET})")
    args = parser.parse_args(argv)
    try:
        a, b = versions_of(args.iteration.resolve(), args.other.resolve() if args.other else None)
        cases, left_cases = cases_of(a, b, args.cases)
        agent = grade.read_agent(AGENT)
    except Refused as error:
        print(error, file=sys.stderr)
        return 1
    pairs, left_runs = pairs_of(a, b, cases)
    folder, recorded = comparison_of(a, b)
    print(f"Comparing {a.name} with {b.name}, in {folder.name}" + ("" if recorded else ", new") + ".")
    for name, reason in left_cases + left_runs:
        print(f"{name}: left out, {reason}")
    todo = []
    for case, number in pairs:
        missing = [i for i in range(1, SESSIONS + 1) if not complete(session_of(folder, case, number, i))]
        print(f"{case}/run-{number}: " + (f"{plural(len(missing), 'session')} to start" if missing else "judged"))
        todo += [(case, number, index) for index in missing]
    per_session, basis = estimate(a.iteration.parent, agent, args.budget)
    print(f"{plural(len(pairs), 'pair')}, {plural(len(todo), 'comparator session')} to start, estimated "
          f"${len(todo) * per_session:.2f}: {basis}.")
    if not args.start:
        print("Nothing started: run again with --start to start them.")
        return 0
    if not todo:
        return 0
    try:
        binary = harness.binary()
        version = harness.version(binary)
        runs.check_outside(Path(tempfile.gettempdir()).resolve())
    except (harness.HarnessError, Refused) as error:
        print(error, file=sys.stderr)
        return 1
    plan = list((recorded or {}).get("pairs", []))
    plan = [{"case": p["case"], "run": p["run"], "labels": p["labels"]} for p in plan]
    known = {(p["case"], p["run"]) for p in plan}
    plan += [{"case": case, "run": number, "labels": labels_of(a, b)}
             for case, number in pairs if (case, number) not in known]
    labels = {(p["case"], p["run"]): p["labels"] for p in plan}
    left_out = left_cases + left_runs
    folder.mkdir(parents=True, exist_ok=True)
    write(folder, summarize(folder, a, b, plan, left_out, agent))
    denied = list(dict.fromkeys([*runs.denied_paths(a.recorded), a.iteration, b.iteration, folder]))
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=max(args.jobs, 1)) as pool:
        futures = {pool.submit(judge, folder, case, number, index, labels[(case, number)][index - 1], (a, b), agent,
                               denied, binary, version, args.timeout * 60, args.budget): (case, number, index)
                   for case, number, index in todo}
        for future in as_completed(futures):
            with lock:
                print(line_of(*futures[future], future.result()), flush=True)
    data = summarize(folder, a, b, plan, left_out, agent)
    write(folder, data)
    for pair in data["pairs"]:
        print(verdict_line(pair))
    verdicts, wins = data["summary"]["verdicts"], data["summary"]["label_wins"]
    print(f"Verdicts: {a.name} {verdicts[a.name]}, {b.name} {verdicts[b.name]}, tie {verdicts['tie']}, split "
          f"{verdicts['split']}, pending {verdicts['pending']}; the output shown as A won {wins['A']} sessions, as B "
          f"{wins['B']}. In {folder / 'comparison.md'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
