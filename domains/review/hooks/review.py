#!/usr/bin/env python3
"""Claude Code Stop hook: ask for a tool review when a tool of this setup served.

At every Stop, first close the turn that just ended: a review still `requested` becomes
`skipped`, with its measured block, and its draft is deleted; every review not closed yet
gets this Stop's time as `closed`. Then, unless a stop hook already drives the conversation
or the session is unattended, find the tools of tools.json that this repository installed
and that the session used without a review yet. If there are some, write the review
request under the repository's reviews/ and block the stop with a short instruction to load
the tool-review skill. Exits 0 in every case; an unexpected error is appended to
reviews/errors.log.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True


def find_scripts():
    """skills/tool-review/scripts/, found above this hook in the repository and once installed."""
    try:
        for candidate in Path(__file__).absolute().parents:
            scripts = candidate / "skills" / "tool-review" / "scripts"
            if (scripts / "transcript.py").is_file():
                return scripts
    except OSError:
        return None
    return None


def close_turn(reviewfile, transcript, reviews, session, path, catalog, claude_dir, now):
    for review, meta in reviewfile.session_reviews(reviews, session):
        if meta.get("closed"):
            continue
        body = reviewfile.parse(review.read_text(encoding="utf-8"))[1]
        if meta.get("status") == "requested":
            ids = [tool["id"] for tool in meta.get("tools", [])]
            meta["measured"] = transcript.measure(path, catalog, claude_dir, transcript.when(meta["slice"]["from"]),
                                                  transcript.when(meta["slice"]["to"]), ids)
            meta["status"] = "skipped"
            reviewfile.draft_of(review).unlink(missing_ok=True)
        meta["closed"] = transcript.stamp(now)
        reviewfile.write_text(review, reviewfile.render(meta, body))


def request(reviewfile, transcript, reviews, session, path, catalog, claude_dir, cwd, now):
    """Write a review request for the tools used without a review; returns their Tools, or []."""
    existing = reviewfile.session_reviews(reviews, session)
    covered = {tool["id"] for _, meta in existing for tool in meta.get("tools", [])}
    tools = [tool for tool_id, tool in transcript.uses(path, catalog, claude_dir, cwd).items() if tool_id not in covered]
    if not tools:
        return []
    start = transcript.when(reviewfile.next_start(existing)) or transcript.session_start(path) or now
    meta = {
        "review": reviewfile.FORMAT, "status": "requested", "date": now.date().isoformat(),
        "session": session, "project": cwd, "trigger": "hook",
        "slice": {"from": transcript.stamp(start), "to": transcript.stamp(now)},
        "tools": [{"id": tool.id, "domain": tool.domain, "version": tool.version} for tool in tools],
    }
    review = reviewfile.new_path(reviews, meta["date"], session, reviewfile.slug(tools[0].id))
    reviewfile.write_text(review, reviewfile.render(meta))
    return tools


def reason(tools):
    named = ", ".join(f"{tool.id} ({tool.domain} {tool.version})" if tool.version else f"{tool.id} ({tool.domain})"
                      for tool in tools)
    return f"This turn used tools of my-claude-setup: {named}. Load the tool-review skill and write the review now."


def log_error(reviews, session, error):
    if reviews is None:
        return
    try:
        reviews.mkdir(parents=True, exist_ok=True)
        with open(reviews / "errors.log", "a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {session or '-'} "
                         f"{type(error).__name__}: {error}\n")
    except OSError:
        pass


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--claude-dir", type=Path, default=Path(__file__).absolute().parents[2])
    args = parser.parse_args(argv)
    reviews, session = None, ""
    try:
        event = json.load(sys.stdin)
        session = str(event.get("session_id") or "")
        scripts = find_scripts()
        if scripts is None or not session:
            return 0
        sys.path.insert(0, str(scripts))
        import reviewfile
        import transcript
        state = transcript.load_state(args.claude_dir)
        repo = transcript.repo_of(state)
        path = Path(str(event.get("transcript_path") or ""))
        if repo is None or not path.is_file():
            return 0
        reviews = repo / "reviews"
        catalog = transcript.load_catalog(args.claude_dir, state)
        now = datetime.now(timezone.utc)
        close_turn(reviewfile, transcript, reviews, session, path, catalog, args.claude_dir, now)
        if event.get("stop_hook_active") or os.environ.get("CLAUDE_CODE_SESSION_ATTENDED") == "0":
            return 0
        tools = request(reviewfile, transcript, reviews, session, path, catalog, args.claude_dir,
                        str(event.get("cwd") or ""), now)
        if tools:
            print(json.dumps({"decision": "block", "reason": reason(tools)}))
    except Exception as error:  # a Stop hook must never break the session it runs in
        log_error(reviews, session, error)
    return 0


if __name__ == "__main__":
    sys.exit(main())
