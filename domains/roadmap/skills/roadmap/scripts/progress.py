#!/usr/bin/env python3
"""Compute a roadmap's progress block from its phase files.

Usage:
  python3 progress.py ROADMAP_DIR           print the block for README.md
  python3 progress.py --check ROADMAP_DIR   compare the README and the phase files
                                            with the computed figures

A phase's count is the checkboxes under its `## Tasks` heading; acceptance
criteria and reports are not counted. --check exits 1 and prints one line per
problem when the README block or a phase's `**Current Status:**` count disagree
with the phase files, when a 🟢 phase keeps an unticked task, or when more than
one phase is 🟡.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

CELLS = 20
MIN_LABEL_WIDTH = 36
IN_PROGRESS = "🟡"
DONE = "🟢"

PHASE_FILE_RE = re.compile(r"^phase-(\d+)-.+\.md$")
HEADING_RE = re.compile(r"^# Phase \d+:\s*(.+?)\s*$", re.M)
STATUS_RE = re.compile(r"^\*\*Current Status:\*\*\s*(\S+)[^\n]*?\((\d+)% — (\d+)/(\d+)\)", re.M)
TASKS_RE = re.compile(r"^## Tasks\s*$(.*?)(?=^## |\Z)", re.M | re.S)
CHECKBOX_RE = re.compile(r"^\s*- \[([ xX])\] ", re.M)
BLOCK_RE = re.compile(r"^## Overall Progress\s*\n+```\n(.*?)^```", re.M | re.S)

LINE_RE = re.compile(
    r"^\s*(?P<label>Phase \d+\s.*?|TOTAL)\s+(?P<emoji>🟢|🟡|🔴|⏸️|⚠️)?\s*(?P<bar>[█░]+)\s+"
    r"(?P<pct>\d+)%\s+\((?P<done>\d+)/(?P<total>\d+)\)\s*$"
)


@dataclass
class Phase:
    path: Path
    number: int
    name: str
    emoji: str
    done: int
    total: int
    status_line: str


def half_up(value):
    return int(value + 0.5)


def bar(done, total, started):
    filled = half_up(done / total * CELLS) if total else 0
    if started and done < total:
        filled = max(filled, 1)
    if done < total:
        filled = min(filled, CELLS - 1)
    return "█" * filled + "░" * (CELLS - filled)


def percent(done, total):
    return half_up(done / total * 100) if total else 0


def read_phases(folder):
    phases = []
    for path in Path(folder).iterdir():
        match = PHASE_FILE_RE.match(path.name)
        if not match or path.name.endswith("-report.md"):
            continue
        text = path.read_text(encoding="utf-8")
        heading, status, tasks = HEADING_RE.search(text), STATUS_RE.search(text), TASKS_RE.search(text)
        boxes = CHECKBOX_RE.findall(tasks.group(1)) if tasks else []
        phases.append(Phase(
            path=path,
            number=int(match.group(1)),
            name=heading.group(1) if heading else path.stem,
            emoji=status.group(1) if status else "",
            done=sum(box != " " for box in boxes),
            total=len(boxes),
            status_line=status.group(0) if status else "",
        ))
    return sorted(phases, key=lambda p: p.number)


def render(phases):
    labels = [f"Phase {p.number}  {p.name}" for p in phases]
    width = max([MIN_LABEL_WIDTH] + [len(label) + 2 for label in labels])
    lines = []
    for label, p in zip(labels, phases):
        started = p.emoji == IN_PROGRESS or p.done > 0
        lines.append(f"{label.ljust(width)}{p.emoji} {bar(p.done, p.total, started)} "
                     f"{percent(p.done, p.total):>3}%  ({p.done}/{p.total})")
    done, total = sum(p.done for p in phases), sum(p.total for p in phases)
    lines.append(f"{'TOTAL'.ljust(width)}   {bar(done, total, done > 0)} "
                 f"{percent(done, total):>3}%  ({done}/{total})")
    return lines


def check_lines(lines):
    """Problems in progress lines: each bar and percentage against its own count, TOTAL against the phases."""
    problems, phases, total_line = [], [], None
    for line in lines:
        match = LINE_RE.match(line)
        if not match:
            continue
        label = " ".join(match["label"].split())
        done, total = int(match["done"]), int(match["total"])
        if label == "TOTAL":
            total_line, started = (done, total), done > 0
        else:
            phases.append((done, total))
            started = match["emoji"] == IN_PROGRESS or done > 0
        expected, shown = bar(done, total, started), match["bar"]
        if shown != expected:
            problems.append(f"{label}: {done}/{total} needs {expected.count('█')} filled cells, "
                            f"the bar shows {shown.count('█')} of {len(shown)}")
        if int(match["pct"]) != percent(done, total):
            problems.append(f"{label}: {done}/{total} is {percent(done, total)}%, the line shows {match['pct']}%")
    if total_line and phases:
        sums = (sum(done for done, _ in phases), sum(total for _, total in phases))
        if total_line != sums:
            problems.append(f"TOTAL: shows {total_line[0]}/{total_line[1]}, "
                            f"the phase lines add up to {sums[0]}/{sums[1]}")
    return problems


def check_block(text):
    """check_lines on the block under ## Overall Progress; [] when the README has none."""
    block = BLOCK_RE.search(text)
    return check_lines(block.group(1).splitlines()) if block else []


def check(folder):
    folder = Path(folder)
    phases = read_phases(folder)
    if not phases:
        return [f"{folder}: no phase-N-*.md file found"]
    problems = []
    for p in phases:
        if not p.status_line:
            problems.append(f"{p.path.name}: no **Current Status:** line with a (P% — done/total) count")
            continue
        expected = f"({percent(p.done, p.total)}% — {p.done}/{p.total})"
        if not p.status_line.endswith(expected):
            problems.append(f"{p.path.name}: **Current Status:** shows {p.status_line[p.status_line.rindex('('):]}, "
                            f"the tasks give {expected}")
        if p.emoji == DONE and p.done < p.total:
            left = p.total - p.done
            problems.append(f"{p.path.name}: {DONE} with {left} unticked task{'s' if left > 1 else ''} — "
                            "move each to a later phase before closing")
    in_progress = [p.path.name for p in phases if p.emoji == IN_PROGRESS]
    if len(in_progress) > 1:
        problems.append(f"{IN_PROGRESS} on more than one phase: {', '.join(in_progress)}")

    readme = folder / "README.md"
    block = BLOCK_RE.search(readme.read_text(encoding="utf-8")) if readme.is_file() else None
    if not block:
        problems.append("README.md: no fenced block under ## Overall Progress")
        return problems
    written = [line.rstrip() for line in block.group(1).splitlines() if line.strip()]
    computed = render(phases)
    for i, line in enumerate(computed):
        found = written[i] if i < len(written) else "(missing)"
        if found != line:
            label = line.split("  ")[0]
            problems.append(f"README.md: {label} line reads\n    {found}\n  expected\n    {line}")
    for extra in written[len(computed):]:
        problems.append(f"README.md: unexpected line in the progress block\n    {extra}")
    return problems


def main(argv):
    args = [a for a in argv if a != "--check"]
    if len(args) != 1:
        print(__doc__.strip())
        return 2
    if "--check" in argv:
        problems = check(args[0])
        for problem in problems:
            print(problem)
        print(f"{len(problems)} progress problem(s)")
        return 1 if problems else 0
    phases = read_phases(args[0])
    if not phases:
        print(f"{args[0]}: no phase-N-*.md file found")
        return 1
    print("\n".join(render(phases)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
