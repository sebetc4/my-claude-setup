#!/usr/bin/env python3
"""Print what the tool reviews under reviews/ say, in the idiom of `make list`.

Usage: python3 tools/reviews.py [--reviews DIR] [--domains DIR]

A header line, one line per tool (reviews, skipped, versions, median cost), the findings
grouped by kind and target, most recurrent first, then the hook errors, the requests no
Stop came back to, and the files that are not readable reviews.
"""

import argparse
import importlib.util
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "reviewfile", ROOT / "domains" / "review" / "skills" / "tool-review" / "scripts" / "reviewfile.py")
reviewfile = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reviewfile)

RANK = {"high": 0, "medium": 1, "low": 2}
STALE = timedelta(days=1)


def when(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def version_key(version):
    return tuple(int(part) for part in re.findall(r"\d+", str(version)))


def load(reviews_dir):
    """(readable reviews as (path, meta), unreadable paths)."""
    readable, unreadable = [], []
    for path in sorted(Path(reviews_dir).glob("*.md")):
        try:
            readable.append((path, reviewfile.parse(path.read_text(encoding="utf-8"))[0]))
        except (OSError, reviewfile.FormatError):
            unreadable.append(path)
    return readable, unreadable


def header(reviews):
    counts = {status: sum(1 for _, meta in reviews if meta.get("status") == status) for status in reviewfile.STATUSES}
    sessions = {meta.get("session") for _, meta in reviews}
    projects = {meta.get("project") for _, meta in reviews}
    dates = sorted(str(meta.get("date")) for _, meta in reviews)
    span = f" · {dates[0]} → {dates[-1]}" if dates else ""
    return (f"{len(reviews)} reviews ({counts['complete']} complete, {counts['skipped']} skipped, "
            f"{counts['requested']} requested) · {len(sessions)} sessions · {len(projects)} projects{span}")


def cost(tool_id, entries):
    """A tool's median cost over the entries its reviews measured."""
    kind = tool_id.split(":", 1)[0]
    if kind == "skill":
        values = [entry["chars"] for entry in entries if isinstance(entry.get("chars"), int)]
        return f"loaded {statistics.median(values):,.0f} chars" if values else ""
    if kind == "agent":
        runs = [run for entry in entries for run in entry.get("runs", []) if isinstance(run, dict)]
        fresh = [run["fresh"] for run in runs if "fresh" in run]
        seconds = [run["seconds"] for run in runs if "seconds" in run]
        parts = [f"{statistics.median(fresh):,.0f} fresh"] if fresh else []
        parts += [f"{statistics.median(seconds):,.0f} s a run"] if seconds else []
        return " · ".join(parts)
    injected = [entry["injected_chars"] for entry in entries if entry.get("injected_chars")]
    if injected:
        return f"{statistics.median(injected):,.0f} chars injected"
    blocks = [entry["blocks"] for entry in entries if isinstance(entry.get("blocks"), int)]
    return f"{statistics.median(blocks):,.0f} blocks" if blocks else ""


def tool_rows(reviews):
    tools = defaultdict(lambda: {"reviews": 0, "skipped": 0, "versions": set(), "entries": []})
    for _, meta in reviews:
        for tool in meta.get("tools") or []:
            row = tools[tool["id"]]
            row["reviews"] += 1
            row["skipped"] += meta.get("status") == "skipped"
            if tool.get("version"):
                row["versions"].add(str(tool["version"]))
            entry = ((meta.get("measured") or {}).get("setup") or {}).get(tool["id"])
            if isinstance(entry, dict):
                row["entries"].append(entry)
    lines = [f"{'tool':<32} {'reviews':>7} {'skipped':>8}  {'versions':<13} median cost"]
    for tool_id in sorted(tools):
        row = tools[tool_id]
        versions = ", ".join(sorted(row["versions"], key=version_key))
        lines.append(f"{tool_id:<32} {row['reviews']:>7} {row['skipped']:>8}  {versions:<13} "
                     f"{cost(tool_id, row['entries'])}".rstrip())
    return lines


def domain_of(target):
    parts = Path(str(target)).parts
    return parts[1] if len(parts) > 2 and parts[0] == "domains" else None


def current_version(domains_dir, domain):
    if domain is None:
        return None
    try:
        return (Path(domains_dir) / domain / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return None


def finding_groups(reviews, domains_dir):
    groups = defaultdict(list)
    for _, meta in reviews:
        versions = {tool.get("domain"): str(tool["version"]) for tool in meta.get("tools") or [] if tool.get("version")}
        for finding in meta.get("findings") or []:
            groups[(finding.get("kind"), finding.get("target"))].append((meta, finding, versions))
    ordered = sorted(groups.items(), key=lambda item: (
        -len(item[1]), min(RANK.get(finding.get("severity"), 3) for _, finding, _ in item[1]), str(item[0])))
    lines = ["findings, most recurrent first"] if ordered else ["no finding yet"]
    for (kind, target), items in ordered:
        domain = domain_of(target)
        seen = sorted({versions[domain] for _, _, versions in items if domain in versions}, key=version_key)
        severities = "/".join(sorted({finding.get("severity") for _, finding, _ in items}, key=lambda s: RANK.get(s, 3)))
        current = current_version(domains_dir, domain)
        since = f"  not seen since {current}" if seen and current and version_key(current) > version_key(seen[-1]) else ""
        latest = max(items, key=lambda item: str((item[0].get("slice") or {}).get("to", "")))[1]
        lines.append(f"  {len(items)}×  {kind}  {target}  {severities}  {', '.join(seen) or '-'}{since}")
        lines.append(f"      {latest.get('fix', '')}")
    return lines


def errors(reviews_dir):
    try:
        logged = (Path(reviews_dir) / "errors.log").read_text(encoding="utf-8").splitlines()
    except OSError:
        logged = []
    return [f"hook errors: {len(logged)}"] + ([f"  last: {logged[-1]}"] if logged else [])


def stale(reviews, now):
    old = [path.name for path, meta in reviews if meta.get("status") == "requested"
           and (moment := when((meta.get("slice") or {}).get("to"))) and now - moment > STALE]
    return [f"requests no Stop came back to: {len(old)}"] + [f"  {name}" for name in old] if old else []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reviews", type=Path, default=ROOT / "reviews")
    parser.add_argument("--domains", type=Path, default=ROOT / "domains")
    args = parser.parse_args(argv)
    reviews, unreadable = load(args.reviews)
    lines = [header(reviews)]
    if reviews:
        lines += [""] + tool_rows(reviews) + [""] + finding_groups(reviews, args.domains)
    lines += [""] + errors(args.reviews) + stale(reviews, datetime.now(timezone.utc))
    lines += [f"unreadable: {path.name}" for path in unreadable]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
