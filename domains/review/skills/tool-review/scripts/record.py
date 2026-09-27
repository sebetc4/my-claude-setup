#!/usr/bin/env python3
"""Validate a tool review's draft, then write the review and delete the draft.

Usage: record.py <draft>

The draft holds the session's part: a JSON object, then a line that is exactly ---, then
the prose. It must belong to the session's requested review. Every problem is reported at
once, nothing is written, and the draft stays to be fixed.
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).absolute().parent))

import reviewfile  # noqa: E402  (same directory, not an installed package)
import transcript  # noqa: E402

KEYS = ("task", "outcome", "corrections", "tools", "findings")
FINDING_KEYS = ("kind", "severity", "target", "fix", "note")
REQUIRED = ("kind", "severity", "target", "fix")
MAX_WORDS = 300


def fail(message):
    print(f"record: {message}", file=sys.stderr)
    return 1


def filled(value):
    return isinstance(value, str) and bool(value.strip())


def clean(value):
    """A text on one line, its runs of white space made single spaces."""
    return " ".join(str(value).split())


def split_draft(content):
    """(data, prose, problem): the JSON object before the first --- line, and the prose after it."""
    lines = content.split("\n")
    if "---" not in lines:
        return None, "", "the draft has no line --- between the JSON object and the prose"
    cut = lines.index("---")
    try:
        data = json.loads("\n".join(lines[:cut]))
    except ValueError as error:
        return None, "", f"the JSON object does not parse: {error}"
    return data, "\n".join(lines[cut + 1:]).strip(), None


def tool_problems(tools, tool_ids):
    if not isinstance(tools, dict):
        return ["tools must map each tool under review to what it brought"]
    problems = [f"tools: {tool_id} is under review and missing" for tool_id in tool_ids if tool_id not in tools]
    problems += [f"tools: {tool_id} is not under review" for tool_id in tools if tool_id not in tool_ids]
    problems += [f"tools.{tool_id} must be a non-empty string" for tool_id in tool_ids
                 if tool_id in tools and not filled(tools[tool_id])]
    return problems


def finding_problems(finding, name, repo):
    if not isinstance(finding, dict):
        return [f"{name} must be a JSON object"]
    problems = [f"{name}: missing {key}" for key in REQUIRED if key not in finding]
    problems += [f"{name}: unknown key {key}" for key in finding if key not in FINDING_KEYS]
    if "kind" in finding and finding["kind"] not in reviewfile.KINDS:
        problems.append(f"{name}: kind must be one of {', '.join(reviewfile.KINDS)}")
    if "severity" in finding and finding["severity"] not in reviewfile.SEVERITIES:
        problems.append(f"{name}: severity must be one of {', '.join(reviewfile.SEVERITIES)}")
    if "target" in finding:
        target = finding["target"]
        if not filled(target) or target.startswith("/") or ".." in Path(target).parts:
            problems.append(f"{name}: target must be a path relative to the repository, without ..")
        elif not (repo / target).is_file():
            problems.append(f"{name}: target {target} is not a file of the repository")
    for key in ("fix", "note"):
        if key in finding and not filled(finding[key]):
            problems.append(f"{name}: {key} must be a non-empty string")
    return problems


def problems_in(data, prose, tool_ids, repo):
    """Every problem of the session's part."""
    if not isinstance(data, dict):
        return ["the part before --- must be a JSON object"]
    problems = [f"missing key: {key}" for key in KEYS if key not in data]
    problems += [f"unknown key: {key}" for key in data if key not in KEYS]
    if "task" in data and not filled(data["task"]):
        problems.append("task must be a non-empty string")
    if "outcome" in data and data["outcome"] not in reviewfile.OUTCOMES:
        problems.append(f"outcome must be one of {', '.join(reviewfile.OUTCOMES)}")
    if "corrections" in data and not (type(data["corrections"]) is int and data["corrections"] >= 0):
        problems.append("corrections must be an integer, 0 or more")
    if "tools" in data:
        problems += tool_problems(data["tools"], tool_ids)
    if "findings" in data:
        if isinstance(data["findings"], list):
            for number, finding in enumerate(data["findings"], 1):
                problems += finding_problems(finding, f"finding {number}", repo)
        else:
            problems.append("findings must be a list")
    if not prose:
        problems.append("the prose after --- is empty")
    elif len(prose.split()) > MAX_WORDS:
        problems.append(f"the prose is {len(prose.split())} words, {MAX_WORDS} at most")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("draft", type=Path)
    parser.add_argument("--claude-dir", type=Path, default=Path(__file__).absolute().parents[3])
    parser.add_argument("--session", default=os.environ.get("CLAUDE_CODE_SESSION_ID"))
    args = parser.parse_args(argv)
    if not args.session:
        return fail("no session: CLAUDE_CODE_SESSION_ID is unset and --session was not given")
    state = transcript.load_state(args.claude_dir)
    repo = transcript.repo_of(state)
    if repo is None:
        return fail("the review domain does not know its repository: run make update D=review in it")
    draft = args.draft.resolve()
    requested = [(review, meta) for review, meta in reviewfile.session_reviews(repo / "reviews", args.session)
                 if meta.get("status") == "requested"]
    match = next(((review, meta) for review, meta in requested if reviewfile.draft_of(review).resolve() == draft), None)
    if match is None:
        return fail(f"{args.draft} is the draft of no requested review of this session: run measure.py first")
    if not draft.is_file():
        return fail(f"no draft at {draft}: write it first")
    review, meta = match
    tool_ids = [tool["id"] for tool in meta.get("tools", [])]
    data, prose, problem = split_draft(draft.read_text(encoding="utf-8"))
    problems = [problem] if problem else problems_in(data, prose, tool_ids, repo)
    if problems:
        print("record: the review was not written:\n" + "\n".join(f"- {item}" for item in problems), file=sys.stderr)
        return 1
    path = transcript.find_transcript(args.claude_dir, args.session)
    if path is None:
        return fail(f"no transcript for session {args.session} under {args.claude_dir / 'projects'}")
    catalog = transcript.load_catalog(args.claude_dir, state)
    meta["measured"] = transcript.measure(path, catalog, args.claude_dir, transcript.when(meta["slice"]["from"]),
                                          transcript.when(meta["slice"]["to"]), tool_ids)
    meta["tools"] = [{**tool, "brought": clean(data["tools"][tool["id"]])} for tool in meta.get("tools", [])]
    meta.update(status="complete", task=clean(data["task"]), outcome=data["outcome"], corrections=data["corrections"])
    meta["findings"] = [{key: clean(finding[key]) if key in ("fix", "note") else finding[key]
                         for key in FINDING_KEYS if key in finding} for finding in data["findings"]]
    reviewfile.write_text(review, reviewfile.render(meta, prose))
    draft.unlink()
    high = [finding for finding in meta["findings"] if finding["severity"] == "high"]
    print(f"review written: {review}")
    print(f"{len(meta['findings'])} finding(s), {len(high)} high")
    for finding in high:
        print(f"- high {finding['kind']} {finding['target']}: {finding['fix']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
