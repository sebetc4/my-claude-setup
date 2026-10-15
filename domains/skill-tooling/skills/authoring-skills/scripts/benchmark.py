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
assertions over its case's, each run weighing alike in the mean. A run's duration is its
session's wall time. An output whose output_source is `estimated`, holding calls whose final
usage the transcripts lack and no reported total gives, is counted with usage.py's estimate,
and marked; one taken from the reported total is exact, and noted.
With two configurations, the delta is the first's mean less the second's: with_skill
less without_skill or old_skill.

Then the pass rate per case; each assertion's results per configuration, with its kind:
a check, a guard, or a measure's item; each measure's count per configuration, its items
passed over those graded; the models and efforts of the runs' calls; the cost of the runs
and of their grading; and notes computed from these: the pass-rate delta beside the cost
and duration deltas, the checks with one result in every run of both configurations,
which do not tell them apart, the checks whose result varies within a configuration, the
guards that failed in a run of with_skill, the checks and items the grader named weak,
never a guard, the session's own calls on another model or effort than the iteration's, its
agents' shown beside them in the Runs table, the estimated and the reported outputs,
the unknown costs, and the runs left out.

The failures of with_skill are read by class from the iteration's classes.json: each class
that stands, by the conditions references/eval-files.md gives, the others counted `skill`,
the default, with the reason; a `grader` class puts the second reading in place of the
first; the share of failures classed an instrument's, and the failures not classed yet.

The criterion is read per assertion over with_skill, its runs pooled from every iteration of
the skill beside this one whose copies of the skill, agents and hooks hold the same digest,
at the same model and effort, a case's runs where its world's digest is this iteration's:
a guard is met with no failure classed `skill` or `variance`; a check, a measure's item
alike, with none classed `skill` and, once one is classed `variance`, a pass rate of 80% or
more over five runs or more; each with three runs at least. A failure not classed, one
classed an instrument's, or a run of with_skill left out makes the criterion wait; so does
a `variance` failure that more runs, five in all, could bring to 80%.

Writes benchmark.json and benchmark.md into the iteration's folder, prints their paths,
then benchmark.md. Starts no session. Exits 1 when the iteration has no graded run.
"""

import argparse
import json
import re
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
import workspace  # noqa: E402

METRICS = ("pass_rate", "duration_s", "input", "cache_read", "cache_write", "output", "cost_usd")
LABELS = {"pass_rate": "Pass rate", "duration_s": "Duration", "input": "Fresh input", "cache_read": "Cache reads",
          "cache_write": "Cache writes", "output": "Output", "cost_usd": "Cost"}
DIGITS = 6
RATE, RATE_RUNS, LEAST_RUNS = 80, 5, 3


class Refused(Exception):
    pass


@dataclass
class Counted:
    """A run that counts: its figures as benchmark.json lists them, and what the notes read."""
    name: str
    case: str
    configuration: str
    figures: dict
    assertions: list
    results: list
    again: dict
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


def output_source(record):
    """Where the run's output comes from, as run.json says; a run.json older than the key, from its estimated calls."""
    return record.get("output_source") or ("estimated" if record.get("estimated_calls") else "transcript")


def agents_of(record):
    """{agent type: its calls, models, efforts and output_source} of run.json's agents."""
    found = {}
    for name, entry in (record.get("agents") or {}).items():
        if isinstance(entry, dict):
            found[name] = {"calls": entry.get("calls") or 0, "models": entry.get("models") or {},
                           "efforts": entry.get("efforts") or {}, "output_source": entry.get("output_source")}
    return found


def own(figures, key):
    """The run's calls by model or effort, its agents' left out: those of the session the iteration sets."""
    left = Counter(figures[key])
    for entry in figures["agents"].values():
        left.subtract(entry[key])
    return {name: n for name, n in left.items() if n > 0}


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
               "estimated_calls": record.get("estimated_calls") or 0, "output_source": output_source(record),
               "models": record.get("models") or {}, "efforts": record.get("efforts") or {},
               "agents": agents_of(record), "claude_version": record.get("claude_version")}
    again = {text: graded[text]["again"].get("passed") is True for text in assertions
             if isinstance(graded[text].get("again"), dict)}
    weak = {}
    for item in grading.get("weak") or []:
        if isinstance(item, dict) and item.get("text") in assertions:
            weak.setdefault(item["text"], str(item.get("reason") or "").strip())
    costs = [session.get("cost_usd") if isinstance(session, dict) else 0.0
             for session in (grading.get("grader"), grading.get("grader_again"))]
    cost = None if None in costs else sum(costs)
    return Counted(run.name, run.case, run.configuration, figures, list(assertions), results, again, weak, cost)


def recount(run):
    """The run's passed and pass_rate, once a class has upheld a second reading."""
    passed = sum(run.results)
    run.figures["passed"] = passed
    run.figures["pass_rate"] = round(passed / len(run.results), DIGITS) if run.results else None


def class_problem(entry, failure, runs, upheld):
    """Why classes.json's entry cannot stand, or None. runs: the counted runs of the skill's arm; upheld: the
    failures, by run name and text, whose second reading a `grader` class upholds."""
    kind, evidence, yes = entry.get("class"), str(entry.get("evidence") or ""), str(entry.get("yes") or "")
    if kind not in grade.CLASSES:
        return f"`{kind}` is no class: {', '.join(grade.CLASSES)}"
    if kind != "skill" and not evidence.strip():
        return f"`{kind}` without its evidence"
    if kind in grade.INSTRUMENTS and not yes.strip():
        return f"`{kind}`, an instrument's class, without the user's yes"
    run, text = failure
    if kind == "grader" and not run.again.get(text):
        return "`grader` without a second reading that passes it (grade.py --again)"
    if kind == "variance":
        index = run.assertions.index(text)
        others = [other for other in runs if other.case == run.case and other is not run]
        failing = [other.name for other in others
                   if not other.results[index] and (other.name, text) not in upheld]
        if not others:
            return f"`variance` with no other run of {run.configuration} on its case"
        if failing:
            return f"`variance` while {', '.join(failing)} fails it too"
    return None


def classed(iteration, counted):
    """(classes, notes, kinds): the failures of the skill's arm by class, from the iteration's classes.json,
    and {(run name, assertion text): class} of those classed. A class that cannot stand counts as `skill`, the
    default; a `grader` class upholds the second reading, which replaces the first in the run's results."""
    mine = [c for c in counted if c.configuration == grade.SKILL_ARM]
    failures = {(c.name, text): (c, text) for c in mine for text, ok in zip(c.assertions, c.results) if not ok}
    notes, entries = [], []
    path = iteration / grade.CLASSES_FILE
    if path.is_file():
        try:
            entries = json.loads(path.read_text(encoding="utf-8")).get("classes")
            if not isinstance(entries, list):
                raise ValueError("no `classes` list")
        except (ValueError, AttributeError) as error:
            notes.append(f"{grade.CLASSES_FILE} cannot be read ({error}): every failure left unclassed.")
            entries = []

    def named(key):
        run, text = failures[key]
        return f'{run.name}, assertion {run.assertions.index(text) + 1} ("{text}")'

    found = {}
    for entry in entries:
        key = (entry.get("run"), entry.get("assertion")) if isinstance(entry, dict) else None
        if key not in failures:
            shown = f'{key[0]}, "{key[1]}"' if key else repr(entry)
            notes.append(f"{grade.CLASSES_FILE}: {shown} is not a failure of a counted {grade.SKILL_ARM} run.")
        elif key in found:
            notes.append(f"{grade.CLASSES_FILE}: {named(key)} classed twice; the first entry kept.")
        else:
            found[key] = entry
    kinds = {}
    upheld = {key for key, entry in found.items() if entry.get("class") == "grader"
              and class_problem(entry, failures[key], mine, set()) is None}
    for key, entry in found.items():
        problem = class_problem(entry, failures[key], mine, upheld)
        if problem:
            notes.append(f"{grade.CLASSES_FILE}: {named(key)}: {problem}; counted `skill`.")
            kinds[key] = "skill"
        else:
            kinds[key] = entry["class"]
    for key in upheld:
        run, text = failures[key]
        run.results[run.assertions.index(text)] = True
        recount(run)
        notes.append(f"{named(key)}: classed `grader`, its second reading, which passes it, counted.")
    by_class = {kind: n for kind in grade.CLASSES if (n := sum(1 for k in kinds.values() if k == kind))}
    instruments = sum(n for kind, n in by_class.items() if kind in grade.INSTRUMENTS)
    unclassed = [{"run": name, "assertion": text} for name, text in failures if (name, text) not in kinds]
    share = round(instruments / len(failures), DIGITS) if kinds else None
    if by_class:
        note = (f"Failures of {grade.SKILL_ARM} by class: "
                + ", ".join(f"{kind} {n}" for kind, n in by_class.items())
                + f"; {instruments} of {len(failures)} an instrument's")
        notes.append(note + (": more than one in four, raise it with the user." if share > 0.25 else "."))
    if unclassed:
        notes.append(f"{plural(len(unclassed), 'failure')} of {grade.SKILL_ARM} not classed: grade.py --again "
                     "classes them, `skill` by default.")
    return {"configuration": grade.SKILL_ARM, "failures": len(failures), "by_class": by_class,
            "unclassed": unclassed, "instrument_share": share}, notes, kinds


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


def snapshot_of(iteration, recorded):
    """The digest of the skill's arm, its copies of the skill, agents and hooks, as workspace.py gives the
    baseline's."""
    return workspace.arm_digest(iteration, grade.SKILL_ARM, recorded["skill_name"], recorded.get("agents"),
                                recorded.get("hooks"))


def pooled(iteration, recorded, read):
    """[(iteration's name, metadata, counted runs, kinds, left out)] of the skill's iterations whose skill's
    arm holds this one's snapshot, run at its model and effort, in their order; read: this iteration's own."""
    snapshot, found = snapshot_of(iteration, recorded), []
    numbered = sorted((int(m.group(1)), folder) for folder in iteration.parent.glob("iteration-*")
                      if (m := re.fullmatch(r"iteration-(\d+)", folder.name)))
    for _, folder in numbered:
        if folder == iteration:
            found.append((folder.name, *read))
            continue
        try:
            other = runs.read_json(folder / "iteration.json")
            if (grade.SKILL_ARM not in other["configurations"]
                    or (other["model"], other["effort"]) != (recorded["model"], recorded["effort"])
                    or snapshot_of(folder, other) != snapshot):
                continue
            metadata = {case: runs.read_json(folder / case / "eval_metadata.json") for case in other["cases"]}
        except (OSError, ValueError, KeyError):
            continue
        counted, left_out = survey(folder, other, metadata)
        found.append((folder.name, metadata, counted, classed(folder, counted)[2], left_out))
    return found


def judged(kind, total_runs, passed, failures):
    """(status, reason) of one assertion over the runs pooled: met, not met, or waits."""
    unclassed = failures.get("unclassed", 0)
    pending = sum(failures.get(k, 0) for k in grade.INSTRUMENTS)
    variance = failures.get("variance", 0)
    if unclassed:
        return "waits", f"{plural(unclassed, 'failure')} not classed: grade.py --again classes them"
    if pending:
        return "waits", (f"{plural(pending, 'failure')} classed an instrument's: the instrument fixed and the runs "
                         "judged again on it first")
    if failures.get("skill"):
        return "not met", f"{plural(failures['skill'], 'failure')} classed `skill`"
    if kind == "guard" and variance:
        return "not met", f"a guard, {plural(variance, 'failure')} classed `variance`, where it must hold in every run"
    if not variance:
        if total_runs >= LEAST_RUNS:
            return "met", None
        return "waits", (f"{plural(total_runs, 'run')}: {plural(LEAST_RUNS - total_runs, 'more run')} on this "
                         f"snapshot, {LEAST_RUNS} at least")
    rate = f"{passed} of {total_runs} runs passed, {passed * 100 / total_runs:.0f}%"
    if total_runs >= RATE_RUNS:
        return ("met", rate) if passed * 100 >= RATE * total_runs else ("not met", f"{rate}, under {RATE}%")
    if (passed + RATE_RUNS - total_runs) * 100 >= RATE * RATE_RUNS:
        return "waits", (f"{plural(variance, 'failure')} classed `variance` in {plural(total_runs, 'run')}: "
                         f"{plural(RATE_RUNS - total_runs, 'more run')} on this snapshot (workspace.py --extend), "
                         f"the rate read over {RATE_RUNS} runs or more")
    return "not met", f"{rate}: under {RATE}% even over {RATE_RUNS} runs"


def criterion_of(iteration, recorded, read):
    """The criterion per assertion over the skill's arm, the runs of one snapshot pooled across the skill's
    iterations, each case's runs where its world is this iteration's, and the iterations that gave runs; read:
    this iteration's (metadata, counted runs, kinds, left out)."""
    metadata = read[0]
    sources = pooled(iteration, recorded, read)
    entries, left, used = [], [], set()
    for case in recorded["cases"]:
        world = metadata[case].get("digest")
        mine = [(name, [c for c in counted if (c.case, c.configuration) == (case, grade.SKILL_ARM)], kinds, out)
                for name, data, counted, kinds, out in sources
                if case in data and data[case].get("digest") == world]
        used.update(name for name, *_ in mine)
        left += [{"iteration": name, **item} for name, _, _, out in mine for item in out
                 if item["run"].startswith(f"{case}/{grade.SKILL_ARM}/")]
        found = kinds_of(metadata[case])
        for number, text in enumerate(metadata[case]["assertions"], 1):
            kind, measure = found.get(text, ("check", None))
            results, failures = [], Counter()
            for _, counted, kinds, _ in mine:
                for run in counted:
                    if text in run.assertions:
                        results.append(run.results[run.assertions.index(text)])
                        if not results[-1]:
                            failures[kinds.get((run.name, text), "unclassed")] += 1
            status, reason = judged(kind, len(results), sum(results), failures)
            entries.append({"case": case, "number": number, "text": text, "kind": kind, "measure": measure,
                            "runs": len(results), "passed": sum(results), "failures": dict(failures),
                            "status": status, "reason": reason})
    blocked = left or any(e["failures"].get(k) for e in entries for k in ("unclassed", *grade.INSTRUMENTS))
    statuses = {e["status"] for e in entries}
    status = ("waits" if blocked else "not met" if "not met" in statuses else "waits" if "waits" in statuses
              else "met")
    return {"configuration": grade.SKILL_ARM, "iterations": [name for name, *_ in sources if name in used],
            "status": status, "rate": RATE, "rate_runs": RATE_RUNS, "least_runs": LEAST_RUNS,
            "assertions": entries, "left_out": left}


def summary_of(counted):
    summary = {"runs": len(counted),
               "estimated_runs": sum(1 for c in counted if c.figures["output_source"] == "estimated")}
    for metric in METRICS:
        summary[metric] = stats([c.figures[metric] for c in counted])
    summary["models"] = merged(c.figures["models"] for c in counted)
    summary["efforts"] = merged(c.figures["efforts"] for c in counted)
    return summary


def kinds_of(metadata):
    """{assertion text: (kind, its measure's text)} for the guards and measures' items; any other assertion is
    a check. An eval_metadata.json older than the kinds holds checks alone."""
    kinds = {text: ("guard", None) for text in metadata.get("guards") or []}
    for measure in metadata.get("measures") or []:
        kinds.update((text, ("measure", measure["text"])) for text in measure["assertions"])
    return kinds


def assertion_entries(recorded, metadata, counted, configurations):
    entries = []
    for case in recorded["cases"]:
        of_case = [c for c in counted if c.case == case]
        kinds = kinds_of(metadata[case])
        for number, text in enumerate(metadata[case]["assertions"], 1):
            kind, measure = kinds.get(text, ("check", None))
            results = {}
            for configuration in configurations:
                mine = [c for c in of_case if c.configuration == configuration]
                results[configuration] = {"passed": sum(c.results[number - 1] for c in mine), "runs": len(mine)}
            discriminates = None
            if kind == "check" and len(configurations) > 1 and all(r["runs"] for r in results.values()):
                same = (all(r["passed"] == r["runs"] for r in results.values())
                        or all(r["passed"] == 0 for r in results.values()))
                discriminates = not same
            weak = [c.weak[text] for c in of_case if text in c.weak]
            entries.append({"case": case, "number": number, "text": text, "kind": kind, "measure": measure,
                            "results": results,
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


def measure_entries(recorded, metadata, assertions, configurations):
    """Each measure's count per configuration: its items passed over the items graded, every run's."""
    found = []
    for case in recorded["cases"]:
        for measure in metadata[case].get("measures") or []:
            items = [a for a in assertions if a["case"] == case and a["text"] in measure["assertions"]]
            found.append({"case": case, "text": measure["text"], "items": len(items), "results": {
                k: {"passed": sum(a["results"][k]["passed"] for a in items),
                    "checked": sum(a["results"][k]["runs"] for a in items)} for k in configurations}})
    return found


def assertion_notes(entry):
    """A check's notes; a guard's failures in the skill's arm, never a call to discriminate nor a weak flag; a
    measure's item, its weak flag alone, the measure counted as a whole."""
    named = f'{entry["case"]}, assertion {entry["number"]} ("{entry["text"]}")'
    if entry["kind"] == "guard":
        mine = entry["results"].get(grade.SKILL_ARM)
        if mine and mine["passed"] < mine["runs"]:
            return [f"{named}: a guard, failed in {mine['runs'] - mine['passed']} of {mine['runs']} "
                    f"{grade.SKILL_ARM} runs, where it must hold in every run."]
        return []
    notes = []
    if entry["discriminates"] is False:
        result = "passed" if all(r["passed"] for r in entry["results"].values()) else "failed"
        notes.append(f"{named}: {result} in every run of both configurations; it does not tell them apart.")
    if entry["varies_in"] and entry["kind"] == "check":
        parts = [f'passed in {entry["results"][k]["passed"]} of {entry["results"][k]["runs"]} {k} runs'
                 for k in entry["varies_in"]]
        notes.append(f"{named}: " + "; ".join(parts) + ".")
    if entry["weak"]:
        note = f"{named}: named weak by the grader in {entry['weak']} of {entry['runs']} runs"
        notes.append(note + (f": {entry['weak_reason']}" if entry["weak_reason"] else "."))
    return notes


def run_notes(counted, model, effort):
    """The notes of each run. The model and effort are those of the session's own calls: an agent's are the
    skill's to set, and shown beside them in the Runs table."""
    notes = []
    for run in counted:
        figures = run.figures
        models = own(figures, "models")
        calls = sum(models.values())
        for other, n in models.items():
            if other != model:
                notes.append(f"{run.name}: {n} of {calls} calls on {other}, where the iteration sets {model}.")
        efforts = own(figures, "efforts")
        calls = sum(efforts.values())
        for other, n in efforts.items():
            if other != effort:
                at = "without a recorded effort" if other == "none" else f"at {other}"
                notes.append(f"{run.name}: {n} of {calls} calls {at}, where the iteration sets {effort}.")
        if figures["output_source"] == "estimated":
            notes.append(f"{run.name}: output estimated for {plural(figures['estimated_calls'], 'call')}, at "
                         f"usage.py's estimate for their agent type and effort: the transcripts lack their final "
                         "usage, and no reported total gives it.")
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
    classes, class_notes, kinds = classed(iteration, counted) if grade.SKILL_ARM in configurations else (None, [], {})
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
    measures = measure_entries(recorded, metadata, assertions, configurations)
    data = {"skill_name": recorded["skill_name"], "iteration": iteration.name,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": recorded["model"], "effort": recorded["effort"], "cases": recorded["cases"],
            "configurations": configurations, "runs_per_configuration": recorded["runs"],
            "delta_of": delta_of, "summary": summary, "delta": delta, "by_case": by_case,
            "assertions": assertions, "measures": measures, "classes": classes,
            "criterion": (criterion_of(iteration, recorded, (metadata, counted, kinds, left_out))
                          if grade.SKILL_ARM in configurations else None),
            "runs": [c.figures for c in counted], "left_out": left_out,
            "cost_usd": {"runs": total(c.figures["cost_usd"] for c in counted),
                         "grading": total(c.grading_cost for c in counted)}}
    notes = [delta_note(data)] if delta_of else []
    for entry in assertions:
        notes += assertion_notes(entry)
    notes += class_notes
    notes += run_notes(counted, recorded["model"], recorded["effort"])
    reported = sum(1 for c in counted if c.figures["output_source"] == "reported")
    if reported:
        notes.append(f"{plural(reported, 'run')} take the output their transcripts lack from the session's reported "
                     "total: exact for the run; each agent's share of it, in run.json's agents, is settled by its "
                     "calls' estimates.")
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


def counted_items(result):
    if not result["checked"]:
        return "—"
    return f"{result['passed']}/{result['checked']} ({result['passed'] / result['checked'] * 100:.0f}%)"


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return lines + ["| " + " | ".join(row) + " |" for row in rows]


def calls_of(counts):
    return ", ".join(f"{name} ×{n}" for name, n in counts.items()) or "—"


def beside(run, key):
    """The run's calls by model or effort: the session's, then each agent's."""
    if not run["agents"]:
        return calls_of(run[key])
    return "; ".join([calls_of(own(run, key))] + [f"{name}: {calls_of(entry[key])}"
                                                   for name, entry in run["agents"].items()])


def criterion_lines(criterion):
    entries = criterion["assertions"]
    met = sum(1 for e in entries if e["status"] == "met")
    names = criterion["iterations"]
    of = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    lines = ["", "## Criterion", "",
             f"{criterion['status'].capitalize()}: {met} of {len(entries)} assertions met over "
             f"{criterion['configuration']}'s runs of {of}, one snapshot of the skill. A guard holds in every run; "
             f"a check, a measure's item alike, has no failure classed `skill` and passes in {criterion['rate']}% "
             f"of the runs or more, read over {criterion['rate_runs']} runs or more once one fails; "
             f"{criterion['least_runs']} runs at least."]
    rows = [[e["case"], f"{e['number']}. {e['text']}", e["kind"], f"{e['passed']}/{e['runs']}",
             e["status"] + (f": {e['reason']}" if e["reason"] else "")] for e in entries if e["status"] != "met"]
    if rows:
        lines += ["", *table(["Case", "Assertion", "Kind", "Passed", "Status"], rows)]
    if criterion["left_out"]:
        lines += ["", f"Waiting on {plural(len(criterion['left_out']), 'run')} of {criterion['configuration']} "
                      "left out: " + "; ".join(f"{i['iteration']}/{i['run']} ({i['reason']})"
                                               for i in criterion["left_out"]) + "."]
    return lines


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
        lines += ["", f"* The output of {plural(estimated, 'run')} counts calls whose final usage the transcripts "
                      "lack and no reported total gives, at usage.py's estimate for their agent type and effort "
                      f"({usage.ESTIMATED_OUTPUT:,} tokens a call by default)."]
    if data["criterion"]:
        lines += criterion_lines(data["criterion"])
    by_case = [[case] + [cell("pass_rate", rates[k], rates[k]["n"]) for k in configurations]
               + ([shift("pass_rate", rates["delta"])] if delta else []) for case, rates in data["by_case"].items()]
    lines += ["", "## Pass Rate By Case", "", *table(["Case", *configurations] + (["Delta"] if delta else []), by_case)]
    if data["measures"]:
        rows = [[m["case"], m["text"]] + [counted_items(m["results"][k]) for k in configurations]
                for m in data["measures"]]
        lines += ["", "## Measures", "", *table(["Case", "Measure", *configurations], rows)]
    run_rows = []
    for run in data["runs"]:
        output = show("output", run["output"]) + (" *" if run["output_source"] == "estimated" else "")
        run_rows.append([f"{run['case']}/{run['configuration']}/run-{run['run']}", f"{run['passed']}/{run['total']}",
                         show("duration_s", run["duration_s"]), output, show("cost_usd", run["cost_usd"]),
                         beside(run, "models"), beside(run, "efforts")])
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
