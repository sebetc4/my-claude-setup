#!/usr/bin/env python3
"""PostToolUse hook: audit the skill that holds an edited file.

After Edit, Write or MultiEdit on a file inside a skill — a folder holding SKILL.md, the
file itself or an ancestor — run the skill audit on that skill. Errors exit 2 with one
line per failing rule on stderr, which the harness shows to the agent; warnings, a clean
skill, a file outside any skill and any unexpected failure exit 0 without output.
"""

import importlib.util
import json
import sys
from pathlib import Path


def find_audit():
    """scripts/audit.py of the authoring-skills skill, found above this hook whether run
    from the repository (domains/skill-tooling/hooks/) or installed (hooks/skill-tooling/)."""
    for candidate in Path(__file__).resolve().parents:
        script = candidate / "skills" / "authoring-skills" / "scripts" / "audit.py"
        if script.is_file():
            return script
    return None


def skill_of(file_path):
    """The skill folder that holds file_path, or None."""
    path = Path(file_path)
    for folder in (path.parent, *path.parent.parents):
        if (folder / "SKILL.md").is_file():
            return folder
    return None


def report(skill, errors, script):
    lines, seen = [], {}
    for problem in errors:
        seen.setdefault(problem.rule, []).append(problem)
    for rule, problems in seen.items():
        first = problems[0]
        more = f" (and {len(problems) - 1} more)" if len(problems) > 1 else ""
        lines.append(f"- [{rule}] {first.message} — {first.path}:{first.line}{more}\n")
    return (f"The skill audit found {len(errors)} error(s) in {skill}:\n" + "".join(lines)
            + f"Run {script} {skill} for every problem.\n")


def main():
    try:
        event = json.load(sys.stdin)
        skill = skill_of(event.get("tool_input", {}).get("file_path", ""))
        script = find_audit()
        if skill is None or script is None:
            return 0
        sys.dont_write_bytecode = True  # no __pycache__ in the skill's folder
        spec = importlib.util.spec_from_file_location("skill_audit", script)
        audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(audit)
        errors = [p for p in audit.audit(skill) if p.severity == audit.ERROR]
    except Exception:
        return 0
    if not errors:
        return 0
    sys.stderr.write(report(skill, errors, script))
    return 2


if __name__ == "__main__":
    sys.exit(main())
