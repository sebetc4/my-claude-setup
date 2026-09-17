#!/usr/bin/env python3
"""Claude Code SessionStart hook: bring back where each open roadmap phase stopped.

Reads the Root of the `## Roadmaps` contract in the project's CLAUDE.md, finds every
phase in progress under <Root>/on-progress/, and adds to the session's context the
phase file, its report, the last Work Log entry, and the report's lines marked
**Pending approval**. Prints nothing when there is no contract or no phase in
progress, and exits 0 in every case, an unexpected error included.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

MAX_LOG_LINES = 20
MAX_CONTEXT = 4000
SECTION_RE = re.compile(r"^## Roadmaps\s*$(.*?)(?=^## |\Z)", re.M | re.S)
ROOT_RE = re.compile(r"^Root\s*:\s*(.+?)\s*$", re.M)
WORK_LOG_RE = re.compile(r"^## Work Log\s*$(.*?)(?=^## |\Z)", re.M | re.S)
ENTRY_RE = re.compile(r"^### \d{4}-\d{2}-\d{2}\s*$", re.M)


def find_progress():
    """scripts/progress.py, found above this hook whether run from the repository
    (domains/roadmap/hooks/) or installed (hooks/roadmap/), where it sits one level
    deeper than here. None when it can't be found, including when an ancestor
    directory can't be stat'd."""
    try:
        for candidate in Path(__file__).resolve().parents:
            script = candidate / "skills" / "roadmap" / "scripts" / "progress.py"
            if script.is_file():
                return script
    except OSError:
        return None
    return None


def load_progress(script):
    spec = importlib.util.spec_from_file_location("roadmap_progress", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def roadmap_root(project):
    """<project>/<Root> from the CLAUDE.md contract, or None."""
    claude_md = project / "CLAUDE.md"
    if not claude_md.is_file():
        return None
    section = SECTION_RE.search(claude_md.read_text(encoding="utf-8"))
    root = ROOT_RE.search(section.group(1)) if section else None
    if not root:
        return None
    return project / re.sub(r"\{[^}]*\}/?$", "", root.group(1)).rstrip("/")


def last_work_log_entry(report):
    work_log = WORK_LOG_RE.search(report)
    entries = list(ENTRY_RE.finditer(work_log.group(1))) if work_log else []
    if not entries:
        return ""
    lines = work_log.group(1)[entries[-1].start():].strip().splitlines()
    if len(lines) > MAX_LOG_LINES:
        lines = lines[:MAX_LOG_LINES] + ["[…]"]
    return "\n".join(lines)


def describe(project, phase):
    report_path = phase.path.with_name(f"{phase.path.stem}-report.md")
    parts = [f"Roadmap phase in progress: {phase.path.relative_to(project)} "
             f"({phase.done}/{phase.total} tasks ticked)."]
    if not report_path.is_file():
        parts.append(f"Its report {report_path.relative_to(project)} is missing.")
        return "\n\n".join(parts)
    report = report_path.read_text(encoding="utf-8")
    parts.append(f"Report: {report_path.relative_to(project)}. "
                 "Read the phase file and its report in full before working on this phase.")
    entry = last_work_log_entry(report)
    if entry:
        parts.append("Last Work Log entry:\n" + entry)
    pending = [line.strip() for line in report.splitlines() if "**Pending approval**" in line]
    if pending:
        parts.append("Pending approval, to settle with the user:\n" + "\n".join(pending))
    return "\n\n".join(parts)


def main():
    try:
        event = json.load(sys.stdin)
        project = Path(event.get("cwd") or ".").resolve()
        root = roadmap_root(project)
        if root is None or not (root / "on-progress").is_dir():
            return 0
        script = find_progress()
        if script is None:
            return 0
        progress = load_progress(script)
        blocks = [describe(project, phase)
                  for folder in sorted(p for p in (root / "on-progress").iterdir() if p.is_dir())
                  for phase in progress.read_phases(folder)
                  if phase.emoji == progress.IN_PROGRESS]
        if not blocks:
            return 0
        context = "\n\n---\n\n".join(blocks)
        if len(context) > MAX_CONTEXT:
            context = context[:MAX_CONTEXT - 1] + "…"
        output = json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}},
                            ensure_ascii=False)
    except Exception:
        return 0
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
