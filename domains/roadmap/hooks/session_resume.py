#!/usr/bin/env python3
"""Claude Code SessionStart hook: name each open roadmap phase, in one line per roadmap.

Reads the [roadmap] root of the project's .agent-conventions.toml through the skill's
scripts/conventions.py, finds every phase in progress under <root>/on-progress/ and
<root>/pending/ (where a roadmap's first phase stays until it closes), and adds one line
per phase to the session's context: the roadmap, the phase, its file, and an instruction
that applies only when the request concerns that phase. Prints nothing when the
conventions are not ok or no phase is in progress, and exits 0 in every case, an
unexpected error included.
"""

import importlib.util
import json
import sys
from pathlib import Path

STATES = ("on-progress", "pending")


def find_scripts():
    """The roadmap skill's scripts/, found above this hook whether run from the repository
    (domains/roadmap/hooks/) or installed (hooks/roadmap/), where it sits one level deeper
    than here. None when it can't be found, including when an ancestor directory can't be
    stat'd."""
    try:
        for candidate in Path(__file__).resolve().parents:
            scripts = candidate / "skills" / "roadmap" / "scripts"
            if (scripts / "progress.py").is_file() and (scripts / "conventions.py").is_file():
                return scripts
    except OSError:
        return None
    return None


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def describe(repo, folder, phase):
    return (f"Roadmap {folder.name}, Phase {phase.number} {phase.name} in progress "
            f"({phase.done}/{phase.total} tasks): {phase.path.relative_to(repo)}. "
            "If the request concerns this phase, load the roadmap skill and read the phase file "
            "and its report before working on it; otherwise, ignore this line.")


def main():
    try:
        event = json.load(sys.stdin)
        scripts = find_scripts()
        if scripts is None:
            return 0
        conventions = load("roadmap_conventions", scripts / "conventions.py")
        result = conventions.read("roadmap", Path(event.get("cwd") or ".").resolve())
        if result.status != "ok":
            return 0
        progress = load("roadmap_progress", scripts / "progress.py")
        root = result.root / result.values["root"]
        lines = [describe(result.root, folder, phase)
                 for state in STATES if (root / state).is_dir()
                 for folder in sorted(p for p in (root / state).iterdir() if p.is_dir())
                 for phase in progress.read_phases(folder)
                 if phase.emoji == progress.IN_PROGRESS]
        if not lines:
            return 0
        output = json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                    "additionalContext": "\n".join(lines)}},
                            ensure_ascii=False)
    except Exception:
        return 0
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
