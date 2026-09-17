#!/usr/bin/env python3
"""Grade the evaluations of skills/roadmap.

Usage: python3 tests/roadmap/evals/grade.py WORKSPACE

The evaluations compare two versions of the skill on the scenarios in evals.json,
following the evaluation loop of the skill-creator plugin. Results are written to
the workspace and never committed.

1. Copy the version to compare against into WORKSPACE/skill-snapshot, for example
   with `git archive <commit> skills/roadmap`.
2. Build the fixtures and the run directories:
   python3 tests/roadmap/evals/build_fixtures.py WORKSPACE
3. Run every scenario once per version, all in parallel, each with a fresh agent
   given the skill path (skills/roadmap for new_skill, the snapshot for old_skill),
   the repository at run-1/outputs/repo, and the scenario's prompt. The agent writes
   its final answer to run-1/outputs/response.md and must not ask the user anything.
   Forbid the Skill tool and anything under ~/.claude/skills in that prompt: an
   installed copy of the skill is also named roadmap, and an agent otherwise loads
   it instead of the path it was given. Check each transcript afterwards for the
   path it actually read, and discard any run that read another copy.
4. Record each run's tokens and duration in run-1/timing.json.
5. Grade: python3 tests/roadmap/evals/grade.py WORKSPACE
6. Aggregate and review with skill-creator:
   python -m scripts.aggregate_benchmark WORKSPACE/iteration-1 --skill-name roadmap
   python eval-viewer/generate_review.py WORKSPACE/iteration-1 --skill-name roadmap \
       --benchmark WORKSPACE/iteration-1/benchmark.json
"""

import glob
import io
import json
import os
import re
import sys

if len(sys.argv) != 2:
    sys.exit(__doc__)
W = sys.argv[1]
ON = "docs/roadmap/on-progress/search-index"
DONE = "docs/roadmap/completed/search-index"

def read(p):
    return io.open(p, encoding="utf-8").read() if os.path.isfile(p) else None

def section(text, heading):
    if text is None:
        return None
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return None
    return "\n".join(l for l in m.group(1).splitlines() if l.strip() != "---").strip()

def field(text, name):
    if text is None:
        return None
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else None

def no_comments(repo):
    hits = [p for p in glob.glob(f"{repo}/docs/roadmap/**/*.md", recursive=True) if "<!--" in read(p)]
    return (not hits, "no <!-- in roadmap documents" if not hits else f"comments in: {hits}")

def eval_close_phase(repo, response):
    phase = read(f"{repo}/{ON}/phase-1-tokenizer.md")
    report = read(f"{repo}/{ON}/phase-1-tokenizer-report.md")
    readme = read(f"{repo}/{ON}/README.md")
    files = section(report, "Files Changed") or ""
    def listed(*names):
        missing = [n for n in names if n not in files]
        return (not missing, f"Files Changed section: {files[:300]!r}" if missing else f"found {', '.join(names)}")
    out = []
    st = field(phase, "Current Status") or ""
    out.append(("Phase 1 file marked done at (100% — 4/4)", "🟢" in st and "4/4" in st, f"Current Status: {st!r}"))
    for text, names in [
        ("Files Changed lists committed work: src/tokenizer.py and src/indexer.py", ("src/tokenizer.py", "src/indexer.py")),
        ("Files Changed lists the uncommitted modification src/search.py", ("src/search.py",)),
        ("Files Changed lists the uncommitted rename src/util.py → src/text_utils.py", ("src/util.py", "src/text_utils.py")),
        ("Files Changed lists the uncommitted deletion src/legacy_index.py", ("src/legacy_index.py",)),
        ("Files Changed lists the untracked new file src/batch.py", ("src/batch.py",)),
    ]:
        ok, ev = listed(*names); out.append((text, ok, ev))
    a = section(report, "Assessment")
    out.append(("Report has a written Assessment", bool(a), f"Assessment: {(a or '')[:150]!r}"))
    pd, cl = section(report, "Problems And Deviations"), section(report, "Changes To Later Phases")
    out.append(("Problems And Deviations and Changes To Later Phases are not empty", bool(pd) and bool(cl),
                f"problems={bool(pd)}, changes={bool(cl)}"))
    total = re.search(r"^TOTAL.*$", readme or "", re.M)
    out.append(("README TOTAL recomputed to 50% (8/16)", bool(total) and "(8/16)" in total.group(0) and "50%" in total.group(0),
                f"TOTAL line: {total.group(0) if total else None!r}"))
    ok, ev = no_comments(repo); out.append(("No template comment copied into roadmap documents", ok, ev))
    return out

def eval_close_roadmap(repo, response):
    readme = read(f"{repo}/{DONE}/README.md")
    summary = read(f"{repo}/{DONE}/summary.md")
    out = []
    out.append(("Roadmap folder moved to docs/roadmap/completed/search-index/",
                readme is not None and not os.path.isdir(f"{repo}/{ON}"),
                f"completed README exists={readme is not None}, on-progress folder still present={os.path.isdir(f'{repo}/{ON}')}"))
    out.append(("summary.md written with ## What We Learned", bool(summary) and "## What We Learned" in summary,
                f"summary exists={summary is not None}"))
    out.append(("summary.md omits the Parent section (no Parent declared)",
                bool(summary) and "## What This Sends Up To The Parent" not in summary, f"summary exists={summary is not None}"))
    for name in ("Current Phase", "Blocked By", "Next Milestone"):
        v = field(readme, name)
        out.append((f"README {name} cleared to —", v in ("—", "-", "None", "none"), f"{name}: {v!r}"))
    rs = field(readme, "Roadmap Status") or ""
    out.append(("README Roadmap Status set to 🟢", "🟢" in rs, f"Roadmap Status: {rs!r}"))
    ver = field(readme, "Version") or ""
    out.append(("README Version bumped to 2.0.0", ver.startswith("2.0.0"), f"Version: {ver!r}"))
    loc = field(readme, "Location") or ""
    out.append(("README Location points at the completed path", "completed/search-index" in loc, f"Location: {loc!r}"))
    ok, ev = no_comments(repo); out.append(("No template comment copied into roadmap documents", ok, ev))
    return out

def eval_create(repo, response, fixture):
    written = [p for p in glob.glob(f"{repo}/docs/roadmap/**/*", recursive=True) if os.path.isfile(p)]
    same_claude = read(f"{repo}/CLAUDE.md") == read(f"{fixture}/CLAUDE.md")
    r = (response or "").lower()
    return [
        ("No roadmap file written before Versioning is known", not written, f"files under docs/roadmap: {written[:5]}"),
        ("The response asks the user for Versioning", "versioning" in r and "?" in r, f"response mentions versioning={'versioning' in r}"),
        ("CLAUDE.md contract left unchanged pending the answer", same_claude, f"CLAUDE.md unchanged={same_claude}"),
    ]

for run in sorted(glob.glob(f"{W}/iteration-1/eval-*/*/run-*/outputs")):
    run_dir = os.path.dirname(run)
    name = run.split("/iteration-1/eval-")[1].split("/")[0]
    repo, response = f"{run}/repo", read(f"{run}/response.md")
    if name == "close-phase-uncommitted-work": exp = eval_close_phase(repo, response)
    elif name == "close-whole-roadmap": exp = eval_close_roadmap(repo, response)
    else: exp = eval_create(repo, response, f"{W}/fixtures/{name}")
    exps = [{"text": t, "passed": bool(p), "evidence": e} for t, p, e in exp]
    passed = sum(x["passed"] for x in exps)
    grading = {"expectations": exps, "summary": {"passed": passed, "failed": len(exps) - passed, "total": len(exps),
               "pass_rate": round(passed / len(exps), 2)}}
    t = f"{run_dir}/timing.json"
    if os.path.isfile(t):
        grading["timing"] = {"executor_duration_seconds": json.load(open(t))["total_duration_seconds"]}
    json.dump(grading, open(f"{run_dir}/grading.json", "w"), indent=2, ensure_ascii=False)
    print(f"{name:34} {os.path.basename(os.path.dirname(run_dir)):10} {passed}/{len(exps)}  response={'yes' if response else 'NO'}")
