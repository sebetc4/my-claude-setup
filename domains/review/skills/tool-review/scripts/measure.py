#!/usr/bin/env python3
"""Print what a tool review needs: its path, its draft, the measured block, what to explain.

Usage: measure.py [--session ID]

Run by the tool-review skill in the session under review. It takes the session's requested
review, or creates one when the user asked for the review — the slice then ends where
tool-review was loaded — measures the slice, and prints 50 lines at most: the measured
block is what gets cut, never what the review must explain.
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).absolute().parent))

import reviewfile  # noqa: E402  (same directory, not an installed package)
import transcript  # noqa: E402

MAX_LINES = 50


def fail(message):
    print(f"measure: {message}", file=sys.stderr)
    return 1


def manual_request(reviews, session, path, catalog, claude_dir):
    """Create the review the user asked for: the slice ends where tool-review was loaded."""
    load = transcript.review_load(path, claude_dir)
    end, cwd = load if load else (datetime.now(timezone.utc), os.getcwd())
    existing = reviewfile.session_reviews(reviews, session)
    start = transcript.when(reviewfile.next_start(existing)) or transcript.session_start(path) or end
    used = list(transcript.uses(path, catalog, claude_dir, cwd, start, end).values())
    meta = {
        "review": reviewfile.FORMAT, "status": "requested", "date": end.date().isoformat(),
        "session": session, "project": cwd, "trigger": "manual",
        "slice": {"from": transcript.stamp(start), "to": transcript.stamp(end)},
        "tools": [{"id": tool.id, "domain": tool.domain, "version": tool.version} for tool in used],
    }
    review = reviewfile.new_path(reviews, meta["date"], session, reviewfile.slug(used[0].id) if used else "manual")
    reviewfile.write_text(review, reviewfile.render(meta))
    return review, meta


def owed(measured, tools):
    """What the review must explain, from the measures: printed, never stored."""
    rows = []
    for tool in tools:
        tool_id = tool["id"]
        entry = (measured.get("setup") or {}).get(tool_id, {})
        rows.append(f"- what {tool_id} brought (tools.{tool_id}); nothing is an answer, and calls for a finding")
        if entry.get("injected_chars"):
            rows.append(f"- did the conversation need the {entry['injected_chars']} characters {tool_id} injected?")
        if entry.get("blocks"):
            rows.append(f"- was each of the {entry['blocks']} blocks by {tool_id} right?")
        for key in ("errors", "script_errors"):
            if entry.get(key):
                rows.append(f"- a finding or a justification for the {entry[key]} {key.replace('_', ' ')} of {tool_id}")
        if isinstance(entry.get("runs"), list) and len(entry["runs"]) > 1:
            rows.append(f"- why {tool_id} ran {len(entry['runs'])} times")
    if (measured.get("friction") or {}).get("tool_errors"):
        rows.append(f"- a finding or a justification for the {measured['friction']['tool_errors']} tool errors")
    rows.append("- each correction you received: count it, then a finding or a reason")
    rows.append("- any job of the slice done without the tool of ours that covers it: a trigger finding")
    return rows


def layout(head, duties, block, limit=MAX_LINES):
    """The printed lines: `head` and `duties` whole, the measured `block` cut to fit `limit`."""
    room = max(limit - len(head) - len(duties), 0)
    if len(block) > room:
        kept = max(room - 1, 0)
        block = block[:kept] + [f"# … {len(block) - kept} more line(s) of the measured block"]
    return head + duties + block


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claude-dir", type=Path, default=Path(__file__).absolute().parents[3])
    parser.add_argument("--session", default=os.environ.get("CLAUDE_CODE_SESSION_ID"))
    args = parser.parse_args(argv)
    if not args.session:
        return fail("no session: CLAUDE_CODE_SESSION_ID is unset and --session was not given")
    state = transcript.load_state(args.claude_dir)
    repo = transcript.repo_of(state)
    if repo is None:
        return fail("the review domain does not know its repository: run make update D=review in it")
    path = transcript.find_transcript(args.claude_dir, args.session)
    if path is None:
        return fail(f"no transcript for session {args.session} under {args.claude_dir / 'projects'}")
    catalog = transcript.load_catalog(args.claude_dir, state)
    reviews = repo / "reviews"
    requested = [(review, meta) for review, meta in reviewfile.session_reviews(reviews, args.session)
                 if meta.get("status") == "requested"]
    review, meta = requested[-1] if requested else manual_request(reviews, args.session, path, catalog, args.claude_dir)
    tools = meta.get("tools", [])
    measured = transcript.measure(path, catalog, args.claude_dir, transcript.when(meta["slice"]["from"]),
                                  transcript.when(meta["slice"]["to"]), [tool["id"] for tool in tools])
    head = [f"review: {review}", f"draft: {reviewfile.draft_of(review)}", "tools under review:"]
    head += [f"  {tool['id']} ({tool.get('domain', '?')} {tool.get('version') or 'no version'})" for tool in tools] or ["  none"]
    duties = ["", "# the review must explain"] + owed(measured, tools)
    block = [""] + reviewfile.render({"measured": measured}).splitlines()[1:-1]
    print("\n".join(layout(head, duties, block)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
