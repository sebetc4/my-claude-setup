#!/usr/bin/env python3
"""Decide the assertions of the roadmap skill's evals, for each complete run of an iteration.

Usage: grade.py <iteration>

The grade.py of the authoring-skills skill runs it before its grader agent, which then
grades whatever is left; every assertion of these evals is decided here. For each run whose
run.json says complete, it rebuilds the run's final tree — the case's fixture.tar, less
the files changes.json deletes, with the run's outputs/ over it — and writes into the
run's grading.json each assertion with its text, passed and evidence.

The evals run on the authoring-skills tooling, from this repository's root:

  S=domains/skill-tooling/skills/authoring-skills/scripts
  python3 $S/workspace.py domains/roadmap/skills/roadmap [--baseline <revision>]
  python3 $S/run.py <iteration> [--start]
  python3 $S/grade.py <iteration> [--start]
  python3 $S/benchmark.py <iteration>
  python3 $S/viewer.py <iteration>
"""

import json
import re
import sys
import tarfile
from pathlib import Path

ON = "docs/roadmap/on-progress/search-index"
DONE = "docs/roadmap/completed/search-index"


class Tree:
    """A run's final tree: the fixture, less the deleted files, with the run's outputs over it."""

    def __init__(self, run, fixture):
        changes = json.loads((run / "changes.json").read_text(encoding="utf-8"))
        self.outputs = run / "outputs"
        self.added = changes["added"]
        self.changed = set(changes["added"]) | set(changes["modified"]) | set(changes["deleted"])
        self.files = {}
        with tarfile.open(fixture) as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.split("/")[0] != ".git":
                    self.files[member.name] = tar.extractfile(member).read().decode("utf-8", "replace")
        for path in changes["deleted"]:
            self.files.pop(path, None)
        for path in set(changes["added"]) | set(changes["modified"]):
            target = self.outputs / path
            if target.is_file():
                self.files[path] = target.read_text(encoding="utf-8", errors="replace")

    def read(self, path):
        return self.files.get(path)

    def under(self, folder):
        return sorted(p for p in self.files if p.startswith(folder.rstrip("/") + "/"))


def section(text, heading):
    if text is None:
        return None
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None
    return "\n".join(line for line in m.group(1).splitlines() if line.strip() != "---").strip()


def field(text, name):
    if text is None:
        return None
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else None


def no_comments(tree):
    hits = [p for p in tree.under("docs/roadmap") if p.endswith(".md") and "<!--" in tree.read(p)]
    return not hits, "no <!-- in roadmap documents" if not hits else f"comments in: {hits}"


def close_phase(tree, response):
    phase = tree.read(f"{ON}/phase-1-tokenizer.md")
    report = tree.read(f"{ON}/phase-1-tokenizer-report.md")
    readme = tree.read(f"{ON}/README.md")
    files = section(report, "Files Changed") or ""

    def listed(*names):
        missing = [n for n in names if n not in files]
        return not missing, f"Files Changed section: {files[:300]!r}" if missing else f"found {', '.join(names)}"

    out = []
    status = field(phase, "Current Status") or ""
    out.append(("Phase 1 file marked done at (100% — 4/4)", "🟢" in status and "4/4" in status,
                f"Current Status: {status!r}"))
    for text, names in [
        ("Files Changed lists committed work: src/tokenizer.py and src/indexer.py", ("src/tokenizer.py", "src/indexer.py")),
        ("Files Changed lists the uncommitted modification src/search.py", ("src/search.py",)),
        ("Files Changed lists the uncommitted rename src/util.py → src/text_utils.py", ("src/util.py", "src/text_utils.py")),
        ("Files Changed lists the uncommitted deletion src/legacy_index.py", ("src/legacy_index.py",)),
        ("Files Changed lists the untracked new file src/batch.py", ("src/batch.py",)),
    ]:
        out.append((text, *listed(*names)))
    assessment = section(report, "Assessment")
    out.append(("Report has a written Assessment", bool(assessment), f"Assessment: {(assessment or '')[:150]!r}"))
    problems, changes = section(report, "Problems And Deviations"), section(report, "Changes To Later Phases")
    out.append(("Problems And Deviations and Changes To Later Phases are not empty", bool(problems) and bool(changes),
                f"problems={bool(problems)}, changes={bool(changes)}"))
    total = re.search(r"^TOTAL.*$", readme or "", re.M)
    out.append(("README TOTAL recomputed to 50% (8/16)",
                bool(total) and "(8/16)" in total.group(0) and "50%" in total.group(0),
                f"TOTAL line: {total.group(0) if total else None!r}"))
    out.append(("No template comment copied into roadmap documents", *no_comments(tree)))
    return out


def close_roadmap(tree, response):
    readme = tree.read(f"{DONE}/README.md")
    summary = tree.read(f"{DONE}/summary.md")
    left = tree.under(ON)
    out = [("Roadmap folder moved to docs/roadmap/completed/search-index/", readme is not None and not left,
            f"completed README exists={readme is not None}, files left under on-progress: {left[:5]}"),
           ("summary.md written with ## What We Learned", bool(summary) and "## What We Learned" in summary,
            f"summary exists={summary is not None}")]
    for name in ("Current Phase", "Blocked By", "Next Milestone"):
        value = field(readme, name)
        out.append((f"README {name} cleared to —", value in ("—", "-", "None", "none"), f"{name}: {value!r}"))
    status = field(readme, "Roadmap Status") or ""
    out.append(("README Roadmap Status set to 🟢", "🟢" in status, f"Roadmap Status: {status!r}"))
    version = field(readme, "Version") or ""
    out.append(("README Version bumped to 2.0.0", version.startswith("2.0.0"), f"Version: {version!r}"))
    location = field(readme, "Location") or ""
    out.append(("README Location points at the completed path", "completed/search-index" in location,
                f"Location: {location!r}"))
    out.append(("No template comment copied into roadmap documents", *no_comments(tree)))
    return out


def create(tree, response):
    """The run cannot ask the user: it stops and names the missing key, writing nothing."""
    written = [p for p in tree.added if p.startswith("docs/roadmap/")]
    unchanged = {name: name not in tree.changed for name in (".agent-conventions.toml", "CLAUDE.md")}
    mentions = "versioning" in (response or "").lower()
    return [
        ("No roadmap file written before versioning is known", not written, f"files under docs/roadmap: {written[:5]}"),
        ("The response names the missing versioning key", mentions, f"response mentions versioning={mentions}"),
        ("Contract left unchanged pending the answer", all(unchanged.values()), f"unchanged: {unchanged}"),
    ]


CASES = {"close-phase-uncommitted-work": close_phase, "close-whole-roadmap": close_roadmap,
         "create-with-incomplete-contract": create}


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main(argv):
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 1
    iteration = Path(argv[0])
    recorded = json.loads((iteration / "iteration.json").read_text(encoding="utf-8"))
    for case in recorded["cases"]:
        for configuration in recorded["configurations"]:
            for number in range(1, recorded["runs"] + 1):
                run = iteration / case / configuration / f"run-{number}"
                if (read_json(run / "run.json") or {}).get("status") != "complete":
                    continue
                response = (run / "response.md").read_text(encoding="utf-8") if (run / "response.md").is_file() else ""
                results = CASES[case](Tree(run, iteration / case / "fixture.tar"), response)
                assertions = [{"text": t, "passed": bool(p), "evidence": e} for t, p, e in results]
                (run / "grading.json").write_text(json.dumps({"assertions": assertions}, indent=2, ensure_ascii=False)
                                                  + "\n", encoding="utf-8")
                print(f"{case:34} {configuration:12} run-{number} {sum(a['passed'] for a in assertions)}/{len(assertions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
