#!/usr/bin/env python3
"""Claude Code PostToolUse hook: keep a roadmap's progress block consistent.

After Edit, Write or MultiEdit on a roadmap's README.md or phase file, check that
every line of the README's progress block agrees with its own count, that TOTAL
adds up the phase lines, and that at most one phase is in progress. The README is
not compared with the ticked tasks: the roadmap skill recomputes it only when a
phase opens or closes. Problems exit 2 on stderr, which Claude Code shows to the
agent. Every other case, an unexpected error included, exits 0 without output.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

PHASE_FILE_RE = re.compile(r"^phase-\d+-.+\.md$")


def find_progress():
    """scripts/progress.py, found above this hook whether run from the repository
    (domains/roadmap/hooks/) or installed (hooks/roadmap/), where it sits one level
    deeper than here."""
    for candidate in Path(__file__).resolve().parents:
        script = candidate / "skills" / "roadmap" / "scripts" / "progress.py"
        if script.is_file():
            return script
    return None


PROGRESS = find_progress()


def load_progress():
    spec = importlib.util.spec_from_file_location("roadmap_progress", PROGRESS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_phase_file(path):
    return bool(PHASE_FILE_RE.match(path.name)) and not path.name.endswith("-report.md")


def roadmap_folder(file_path):
    """The roadmap folder a changed file belongs to, or None."""
    path = Path(file_path)
    if path.name != "README.md" and not is_phase_file(path):
        return None
    folder = path.parent
    readme = folder / "README.md"
    if not readme.is_file() or "## Overall Progress" not in readme.read_text(encoding="utf-8"):
        return None
    if not any(is_phase_file(child) for child in folder.iterdir()):
        return None
    return folder


def problems_in(folder, progress):
    problems = progress.check_block((folder / "README.md").read_text(encoding="utf-8"))
    in_progress = [phase.path.name for phase in progress.read_phases(folder) if phase.emoji == progress.IN_PROGRESS]
    if len(in_progress) > 1:
        problems.append(f"{progress.IN_PROGRESS} on more than one phase: {', '.join(in_progress)}")
    return problems


def main():
    try:
        event = json.load(sys.stdin)
        folder = roadmap_folder(event.get("tool_input", {}).get("file_path", ""))
        if folder is None or PROGRESS is None:
            return 0
        problems = problems_in(folder, load_progress())
    except Exception:
        return 0
    if not problems:
        return 0
    sys.stderr.write(f"Roadmap progress block in {folder} is inconsistent:\n"
                     + "".join(f"- {problem}\n" for problem in problems)
                     + f"Replace the block with the output of scripts/progress.py {folder}.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
