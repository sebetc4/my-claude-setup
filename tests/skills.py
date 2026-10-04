"""Static checks on every skill, delegated to the audit of the skill-tooling domain.

Each skill gets domains/skill-tooling/skills/authoring-skills/scripts/audit.py, which
checks the rule catalogue of docs/decisions/2026-10-03-skill-audit-rules.md: run() yields
its errors, warnings() its warnings. The wording checks below serve the agents, read by
tests/domains.py.
"""

import functools
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "skill_audit", ROOT / "domains/skill-tooling/skills/authoring-skills/scripts/audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.S)
FRENCH_RE = audit.FRENCH_RE
PERCENT_RE = audit.PERCENT_RE
COMPATIBILITY_RE = audit.COMPATIBILITY_RE

WORDING = (
    (COMPATIBILITY_RE, "compatibility wording: a file describes only its target behavior"),
    (FRENCH_RE, "non-English word: files are written in English"),
    (PERCENT_RE, "space before %: English percentages take none"),
)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def wording_problems(path, text):
    for pattern, message in WORDING:
        for match in pattern.finditer(text):
            yield path, line_of(text, match.start()), f"{message} ({match.group(0)!r})"


@functools.lru_cache(maxsize=None)
def _problems(skill):
    return tuple(audit.audit(skill))


def run(skill: Path):
    for problem in _problems(Path(skill)):
        if problem.severity == audit.ERROR:
            yield problem.path, problem.line, f"[{problem.rule}] {problem.message}"


def warnings(skill: Path):
    for problem in _problems(Path(skill)):
        if problem.severity == audit.WARNING:
            yield problem.path, problem.line, f"[{problem.rule}] warning: {problem.message}"
