"""Static checks specific to skills/roadmap."""

import re
from pathlib import Path

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
BAR_LINE_RE = re.compile(
    r"^\s*(?P<label>Phase \d+\s.*?|TOTAL)\s+(?P<emoji>🟢|🟡|🔴)?\s*(?P<bar>[█░]+)\s+(?P<pct>\d+)%\s+\((?P<done>\d+)/(?P<total>\d+)\)\s*$",
    re.M,
)
STATUS_EMOJI_RE = re.compile(r"🔴|🟡|🟢|⏸️|⚠️")
CONTRACT_BLOCK_RE = re.compile(r"```markdown\n## Roadmaps\n(.*?)```", re.S)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def skill_files(skill):
    return sorted(p for p in skill.rglob("*.md") if p.relative_to(skill).parts[0] != "evals")


def half_up(value):
    return int(value + 0.5)


def check_history(skill):
    for path in skill_files(skill):
        text = path.read_text(encoding="utf-8")
        for match in HISTORY_RE.finditer(text):
            yield path, line_of(text, match.start()), f"wording from the skill's history ({match.group(0)!r})"


def check_progress_bar_example(skill):
    """Every worked bar line in SKILL.md obeys the Progress bar invariant."""
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    lines = list(BAR_LINE_RE.finditer(text))
    if not lines:
        yield path, 1, "no worked progress bar example found"
    for match in lines:
        done, total, bar = int(match["done"]), int(match["total"]), match["bar"]
        where = line_of(text, match.start())
        if len(bar) != 20:
            yield path, where, f"bar is {len(bar)} characters, 20 expected"
            continue
        filled = half_up(done / total * 20)
        started = match["emoji"] == "🟡" or (match["label"] == "TOTAL" and 0 < done < total)
        if started:
            filled = max(filled, 1)
        if done < total:
            filled = min(filled, 19)
        if bar != "█" * filled + "░" * (20 - filled):
            yield path, where, f"{done}/{total} needs {filled} filled cells, the bar shows {bar.count('█')}"
        if int(match["pct"]) != half_up(done / total * 100):
            yield path, where, f"{done}/{total} is {half_up(done / total * 100)}%, the line shows {match['pct']}%"


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
