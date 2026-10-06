#!/usr/bin/env python3
"""Sum up the graded runs of an iteration per configuration, in benchmark.json and benchmark.md.

Usage: benchmark.py <iteration>

A run counts when run.py marked it complete and its grading.json grades every assertion
of its case; the others are listed as left out, with the reason. Per configuration, over
the runs that count: the pass rate, the duration, the fresh input, the cache reads, the
cache writes, the output and the cost, each with n, the mean, the sample's standard
deviation (none for a single value), the minimum and the maximum. A figure a run lacks,
such as a cost the price table cannot give, is left out of that metric, never counted as
zero, and n says how many runs the metric rests on. A run's pass rate is its passed
assertions over its case's, each run weighing alike in the mean. An output holding calls
whose final usage the transcript lacks is counted with usage.py's estimate, and marked.
With two configurations, the delta is the first's mean less the second's: with_skill
less without_skill or old_skill.

Then the pass rate per case; each assertion's results per configuration; the models and
efforts of the runs' calls; the cost of the runs and of their grading; and notes computed
from these: the pass-rate delta beside the cost and duration deltas, the assertions with
one result in every run of both configurations, which do not tell them apart, the
assertions whose result varies within a configuration, the assertions the grader named
weak, the calls on another model or effort than the iteration's, the estimated outputs,
the unknown costs, and the runs left out.

Writes benchmark.json and benchmark.md into the iteration's folder, prints their paths,
then benchmark.md. Starts no session. Exits 1 when the iteration has no graded run.
"""

import argparse
import json
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grade  # noqa: E402  (same directory, not an installed package)
import run as runs  # noqa: E402
import usage  # noqa: E402

METRICS = ("pass_rate", "duration_s", "input", "cache_read", "cache_write", "output", "cost_usd")
LABELS = {"pass_rate": "Pass rate", "duration_s": "Duration", "input": "Fresh input", "cache_read": "Cache reads",
          "cache_write": "Cache writes", "output": "Output", "cost_usd": "Cost"}
DIGITS = 6


class Refused(Exception):
    pass


@dataclass
class Counted:
    """A run that counts: its figures as benchmark.json lists them, and what the notes read."""
    name: str
    case: str
    configuration: str
    figures: dict
    results: list
    weak: dict
    grading_cost: float | None


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def stats(values):
    values = [v for v in values if v is not None]
    if not values:
        return {"n": 0, "mean": None, "stddev": None, "min": None, "max": None}
    return {"n": len(values), "mean": round(statistics.mean(values), DIGITS),
            "stddev": round(statistics.stdev(values), DIGITS) if len(values) > 1 else None,
            "min": round(min(values), DIGITS), "max": round(max(values), DIGITS)}


def difference(first, reference):
    if first["mean"] is None or reference["mean"] is None:
        return None
    return round(first["mean"] - reference["mean"], DIGITS)


def total(values):
    """The sum, or None when one value is unknown."""
    values = list(values)
    return None if any(v is None for v in values) else round(sum(values), DIGITS)


def merged(counts):
    summed = Counter()
    for count in counts:
        summed.update(count)
    return dict(summed.most_common())


def counted_run(run, record, grading, assertions):
    graded = {a.get("text"): a for a in grading["assertions"] if isinstance(a, dict)}
    results = [graded[text].get("passed") is True for text in assertions]
    tokens = record.get("tokens") if isinstance(record.get("tokens"), dict) else {}
    writes = [tokens.get("write_5m"), tokens.get("write_1h")]
    passed = sum(results)
    figures = {"case": run.case, "configuration": run.configuration, "run": run.number,
               "passed": passed, "total": len(results),
               "pass_rate": round(passed / len(results), DIGITS) if results else None,
               "duration_s": record.get("duration_s"), "input": tokens.get("input"),
               "cache_read": tokens.get("cache_read"), "cache_write": total(writes) if tokens else None,
               "output": tokens.get("output"), "cost_usd": record.get("cost_usd"),
               "estimated_calls": record.get("estimated_calls") or 0,
               "models": record.get("models") or {}, "efforts": record.get("efforts") or {},
               "claude_version": record.get("claude_version")}
    weak = {}
    for item in grading.get("weak") or []:
        if isinstance(item, dict) and item.get("text") in assertions:
            weak.setdefault(item["text"], str(item.get("reason") or "").strip())
    grader = grading.get("grader")
    cost = grader.get("cost_usd") if isinstance(grader, dict) else 0.0
    return Counted(run.name, run.case, run.configuration, figures, results, weak, cost)


def survey(iteration, recorded, metadata):
    """(counted, left out): the runs that count, and {run, reason} for the others."""
    counted, left_out = [], []
    for run in runs.plan(iteration, recorded):
        record = run.recorded()
        assertions = metadata[run.case]["assertions"]
        if record is None:
            reason = "not started"
        elif record.get("status") != "complete":
            reason = f"not complete: {record.get('status')}" + (f" ({record['reason']})" if record.get("reason") else "")
        elif not grade.complete_grading(run.folder, assertions):
            reason = "not graded"
        else:
            counted.append(counted_run(run, record, grade.grading_of(run.folder), assertions))
            continue
        left_out.append({"run": run.name, "reason": reason})
    return counted, left_out


def summary_of(counted):
    summary = {"runs": len(counted), "estimated_runs": sum(1 for c in counted if c.figures["estimated_calls"])}
    for metric in METRICS:
        summary[metric] = stats([c.figures[metric] for c in counted])
    summary["models"] = merged(c.figures["models"] for c in counted)
    summary["efforts"] = merged(c.figures["efforts"] for c in counted)
    return summary


def assertion_entries(recorded, metadata, counted, configurations):
    entries = []
    for case in recorded["cases"]:
        of_case = [c for c in counted if c.case == case]
        for number, text in enumerate(metadata[case]["assertions"], 1):
            results = {}
            for configuration in configurations:
                mine = [c for c in of_case if c.configuration == configuration]
                results[configuration] = {"passed": sum(c.results[number - 1] for c in mine), "runs": len(mine)}
            discriminates = None
            if len(configurations) > 1 and all(r["runs"] for r in results.values()):
                same = (all(r["passed"] == r["runs"] for r in results.values())
                        or all(r["passed"] == 0 for r in results.values()))
                discriminates = not same
            weak = [c.weak[text] for c in of_case if text in c.weak]
            entries.append({"case": case, "number": number, "text": text, "results": results,
                            "discriminates": discriminates,
                            "varies_in": [k for k, r in results.items() if 0 < r["passed"] < r["runs"]],
                            "weak": len(weak), "weak_reason": next((r for r in weak if r), None),
                            "runs": len(of_case)})
    return entries


def show(metric, value):
    if value is None:
        return "unknown"
    if metric == "pass_rate":
        return f"{value * 100:.0f}%"
    if metric == "duration_s":
        return f"{value:.1f} s"
    if metric == "cost_usd":
        return f"${value:.3f}"
    return f"{value:,.0f}"


def shift(metric, value):
    if value is None:
        return "—"
    sign, size = ("+" if value >= 0 else "-"), abs(value)
    if metric == "pass_rate":
        return f"{sign}{size * 100:.0f} pts"
    if metric == "duration_s":
        return f"{sign}{size:.1f} s"
    if metric == "cost_usd":
        return f"{sign}${size:.3f}"
    return f"{sign}{size:,.0f}"


def delta_note(data):
    first, reference = data["delta_of"]
    delta, base = data["delta"], data["summary"][reference]
    parts = [f"pass rate {shift('pass_rate', delta['pass_rate'])}"]
    if delta["cost_usd"] is None:
        parts.append("cost unknown")
    else:
        part = f"cost {shift('cost_usd', delta['cost_usd'])} a run"
        if base["cost_usd"]["mean"]:
            part += f" ({delta['cost_usd'] / base['cost_usd']['mean'] * 100:+.0f}%)"
        parts.append(part)
    parts.append(f"duration {shift('duration_s', delta['duration_s'])} a run")
    return f"{first} against {reference}: " + ", ".join(parts) + "."


def assertion_notes(entry):
    named = f'{entry["case"]}, assertion {entry["number"]} ("{entry["text"]}")'
    notes = []
    if entry["discriminates"] is False:
        result = "passed" if all(r["passed"] for r in entry["results"].values()) else "failed"
        notes.append(f"{named}: {result} in every run of both configurations; it does not tell them apart.")
    if entry["varies_in"]:
        parts = [f'passed in {entry["results"][k]["passed"]} of {entry["results"][k]["runs"]} {k} runs'
                 for k in entry["varies_in"]]
        notes.append(f"{named}: " + "; ".join(parts) + ".")
    if entry["weak"]:
        note = f"{named}: named weak by the grader in {entry['weak']} of {entry['runs']} runs"
        notes.append(note + (f": {entry['weak_reason']}" if entry["weak_reason"] else "."))
    return notes


def run_notes(counted, model, effort):
    notes = []
    for run in counted:
        figures = run.figures
        calls = sum(figures["models"].values())
        for other, n in figures["models"].items():
            if other != model:
                notes.append(f"{run.name}: {n} of {calls} calls on {other}, where the iteration sets {model}.")
        calls = sum(figures["efforts"].values())
        for other, n in figures["efforts"].items():
            if other != effort:
                at = "without a recorded effort" if other == "none" else f"at {other}"
                notes.append(f"{run.name}: {n} of {calls} calls {at}, where the iteration sets {effort}.")
        if figures["estimated_calls"]:
            notes.append(f"{run.name}: output estimated for {plural(figures['estimated_calls'], 'call')}, at "
                         f"{usage.ESTIMATED_OUTPUT:,} tokens a call: the transcript lacks their final usage.")
        if figures["cost_usd"] is None:
            unpriced = [m for m in figures["models"] if usage.price_of(m) is None]
            note = f"{run.name}: cost unknown, left out of the cost figures"
            notes.append(note + (f"; usage.py has no price for {', '.join(unpriced)}." if unpriced else "."))
    return notes


def compute(iteration, recorded):
    """The benchmark of the iteration; Refused when no run is graded."""
    metadata = {case: runs.read_json(iteration / case / "eval_metadata.json") for case in recorded["cases"]}
    configurations = recorded["configurations"]
    counted, left_out = survey(iteration, recorded, metadata)
    if not counted:
        raise Refused(f"no graded run in {iteration}: run grade.py <iteration> first")
    summary = {k: summary_of([c for c in counted if c.configuration == k]) for k in configurations}
    delta_of = [configurations[0], configurations[-1]] if len(configurations) > 1 else None
    delta = ({m: difference(summary[delta_of[0]][m], summary[delta_of[1]][m]) for m in METRICS}
             if delta_of else None)
    by_case = {}
    for case in recorded["cases"]:
        rates = {k: stats([c.figures["pass_rate"] for c in counted if (c.case, c.configuration) == (case, k)])
                 for k in configurations}
        rates["delta"] = difference(rates[delta_of[0]], rates[delta_of[1]]) if delta_of else None
        by_case[case] = rates
    assertions = assertion_entries(recorded, metadata, counted, configurations)
    data = {"skill_name": recorded["skill_name"], "iteration": iteration.name,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": recorded["model"], "effort": recorded["effort"], "cases": recorded["cases"],
            "configurations": configurations, "runs_per_configuration": recorded["runs"],
            "delta_of": delta_of, "summary": summary, "delta": delta, "by_case": by_case,
            "assertions": assertions,
            "runs": [c.figures for c in counted], "left_out": left_out,
            "cost_usd": {"runs": total(c.figures["cost_usd"] for c in counted),
                         "grading": total(c.grading_cost for c in counted)}}
    notes = [delta_note(data)] if delta_of else []
    for entry in assertions:
        notes += assertion_notes(entry)
    notes += run_notes(counted, recorded["model"], recorded["effort"])
    if left_out:
        notes.append(f"{plural(len(left_out), 'run')} left out: "
                     + "; ".join(f"{item['run']} ({item['reason']})" for item in left_out) + ".")
    data["notes"] = notes
    return data


def cell(metric, values, runs_counted, marked=False):
    if not values["n"]:
        text = "—"
    elif values["n"] == 1:
        text = show(metric, values["mean"])
    else:
        text = (f"{show(metric, values['mean'])} ± {show(metric, values['stddev'])} "
                f"({show(metric, values['min'])} to {show(metric, values['max'])})")
    if values["n"] and values["n"] < runs_counted:
        text += f", {values['n']} of {runs_counted} runs"
    return text + (" *" if marked else "")


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return lines + ["| " + " | ".join(row) + " |" for row in rows]


def calls_of(counts):
    return ", ".join(f"{name} ×{n}" for name, n in counts.items()) or "—"


def markdown(data):
    configurations, summary, delta = data["configurations"], data["summary"], data["delta"]
    header = ["Metric", *configurations] + (["Delta"] if delta else [])
    rows = []
    for metric in METRICS:
        row = [LABELS[metric]] + [
            cell(metric, summary[k][metric], summary[k]["runs"],
                 marked=metric == "output" and summary[k]["estimated_runs"] > 0) for k in configurations]
        rows.append(row + ([shift(metric, delta[metric])] if delta else []))
    left = len(data["left_out"])
    cost = data["cost_usd"]
    lines = [f"# Benchmark: {data['skill_name']}, {data['iteration']}", "",
             f"Model and effort as the iteration sets them: {data['model']} at {data['effort']}; "
             f"{plural(data['runs_per_configuration'], 'run')} per case and configuration; "
             f"cases: {', '.join(data['cases'])}.",
             f"{plural(len(data['runs']), 'run')} counted, {left} left out. Cost of the counted runs: "
             f"{show('cost_usd', cost['runs'])}; of their grading: {show('cost_usd', cost['grading'])}.",
             "", "## Summary", "", *table(header, rows)]
    estimated = sum(summary[k]["estimated_runs"] for k in configurations)
    if estimated:
        lines += ["", f"* The output of {plural(estimated, 'run')} counts calls estimated at "
                      f"{usage.ESTIMATED_OUTPUT:,} tokens each: the transcript lacks their final usage."]
    by_case = [[case] + [cell("pass_rate", rates[k], rates[k]["n"]) for k in configurations]
               + ([shift("pass_rate", rates["delta"])] if delta else []) for case, rates in data["by_case"].items()]
    lines += ["", "## Pass Rate By Case", "", *table(["Case", *configurations] + (["Delta"] if delta else []), by_case)]
    run_rows = []
    for run in data["runs"]:
        output = show("output", run["output"]) + (" *" if run["estimated_calls"] else "")
        run_rows.append([f"{run['case']}/{run['configuration']}/run-{run['run']}", f"{run['passed']}/{run['total']}",
                         show("duration_s", run["duration_s"]), output, show("cost_usd", run["cost_usd"]),
                         calls_of(run["models"]), calls_of(run["efforts"])])
    lines += ["", "## Runs", "",
              *table(["Run", "Assertions", "Duration", "Output", "Cost", "Models", "Efforts"], run_rows)]
    if data["notes"]:
        lines += ["", "## Notes", "", *(f"- {note}" for note in data["notes"])]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sum up the graded runs of an iteration per configuration.")
    parser.add_argument("iteration", type=Path, help="the iteration's folder")
    args = parser.parse_args(argv)
    iteration = args.iteration.resolve()
    try:
        recorded = runs.read_json(iteration / "iteration.json")
        data = compute(iteration, recorded)
    except (OSError, ValueError) as error:
        print(f"no iteration at {iteration}: {error}", file=sys.stderr)
        return 1
    except Refused as error:
        print(error, file=sys.stderr)
        return 1
    text = markdown(data)
    (iteration / "benchmark.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    (iteration / "benchmark.md").write_text(text, encoding="utf-8")
    print(iteration / "benchmark.json")
    print(iteration / "benchmark.md")
    print()
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
