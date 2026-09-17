"""Static checks specific to domains/roadmap/skills/roadmap."""

import importlib.util
import re
from pathlib import Path

_spec = importlib.util.spec_from_file_location("roadmap_progress", Path(__file__).resolve().parent.parent / "scripts" / "progress.py")
progress = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(progress)

# Wording removed by the audit of this skill: explanations of its own history,
# or rules that only served roadmaps created before a feature existed.
HISTORY_RE = re.compile(
    "|".join(p.replace(" ", r"\s+") for p in [
        '\\bfabricated\\b',
        'no-script rule',
        'admitted exception',
        'narrows its own',
        'regularly-practiced',
        'editorial sections included',
        'change the two together',
        'does not restate',
        'deliberately not restated',
        'hit for real',
        'kept wherever it already exists',
        'already uses under',
        'already used in the documents',
        'prior roadmap',
        'previous skill',
        'old ritual',
        'Target Completion',
        'subtasks\\)`',
    ]),
    re.I,
)
STATUS_EMOJI_RE = re.compile(r"🔴|🟡|🟢|⏸️|⚠️")
CONTRACT_BLOCK_RE = re.compile(r"```markdown\n## Roadmaps\n(.*?)```", re.S)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def skill_files(skill):
    return sorted(p for p in skill.rglob("*.md") if p.relative_to(skill).parts[0] != "evals")


def check_history(skill):
    for path in skill_files(skill):
        text = path.read_text(encoding="utf-8")
        for match in HISTORY_RE.finditer(text):
            yield path, line_of(text, match.start()), f"wording from the skill's history ({match.group(0)!r})"


def check_progress_bar_example(skill):
    """Every worked bar line in SKILL.md obeys the Progress bar and Totals invariants."""
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    line_re = re.compile(progress.LINE_RE.pattern, re.M)
    matches = list(line_re.finditer(text))
    if not matches:
        yield path, 1, "no worked progress bar example found"
        return
    lines = [match.group(0) for match in matches]
    # Map normalized labels to their line numbers
    label_to_line = {}
    for match in matches:
        label = " ".join(match["label"].split())
        label_to_line[label] = line_of(text, match.start())
    # Report each problem at its own line
    first_line = line_of(text, matches[0].start())
    for problem in progress.check_lines(lines):
        # Extract label from problem message (text before first ": ")
        problem_label = problem.split(": ", 1)[0]
        where = label_to_line.get(problem_label, first_line)
        yield path, where, problem


def check_status_legend(skill):
    """The README template's legend lists the Statuses invariant, in the same order."""
    skill_md, readme = skill / "SKILL.md", skill / "assets/templates/roadmap-readme.md"
    invariant = re.search(r"^3\. \*\*Statuses\*\* — (.*)$", skill_md.read_text(encoding="utf-8"), re.M)
    legend = re.search(r"^## Status Indicators\n(.*?)\n---", readme.read_text(encoding="utf-8"), re.S | re.M)
    if not invariant or not legend:
        yield readme, 1, "Statuses invariant or Status Indicators legend not found"
        return
    expected = STATUS_EMOJI_RE.findall(invariant.group(1).split(". ")[0])
    found = STATUS_EMOJI_RE.findall(legend.group(1))
    if expected != found:
        yield readme, 1, f"legend lists {found}, the Statuses invariant lists {expected}"


def check_report_rules_home(skill):
    """The report's rules live only in references/report.md."""
    home = skill / "references/report.md"
    for phrase in ("git diff -M --name-status", "git ls-files --others", "never organized by the phase"):
        for path in skill_files(skill):
            if path != home and phrase in path.read_text(encoding="utf-8"):
                yield path, 1, f"{phrase!r} belongs to references/report.md only"
    text = home.read_text(encoding="utf-8")
    if re.search(r"git diff\b[^\n]*\.\.HEAD", text):
        yield home, 1, "Files Changed diffs against HEAD, which misses uncommitted work"


def check_no_notes(skill):
    for path in skill_files(skill):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"^## Notes\s*$|\{\{NOTES\}\}", text, re.M):
            yield path, line_of(text, match.start()), "phase notes are replaced by the phase report"


def check_contract_examples(skill):
    """Every contract example carries the three required keys."""
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    blocks = list(CONTRACT_BLOCK_RE.finditer(text))
    if not blocks:
        yield path, 1, "no contract example found"
    for block in blocks:
        keys = set(re.findall(r"^(\w[\w-]*)\s*:", block.group(1), re.M))
        missing = {"Root", "Language", "Versioning"} - keys
        if missing:
            yield path, line_of(text, block.start()), f"contract example lacks required key(s): {', '.join(sorted(missing))}"


CHECKS = (check_history, check_progress_bar_example, check_status_legend,
          check_report_rules_home, check_no_notes, check_contract_examples)


def run(skill: Path):
    for check in CHECKS:
        yield from check(skill)
