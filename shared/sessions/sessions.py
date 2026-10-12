#!/usr/bin/env python3
"""Select the sessions of a window of work in a repository, from Claude Code's transcripts.

window(repo, start, end) takes two commits or two times, a commit standing for its committer's
time, the end now by default, and gives:
- the repository's working sessions: the transcripts of its project folder, which Claude Code
  names after the repository's path, that a person prompted, whatever their cwd, since a moved
  repository's older sessions keep theirs; each call counted by its time, and once
  (usage.distinct());
- the claude -p sessions: the transcripts of any project folder that no person prompted and
  that start in the window, each given to a working session by the scratchpad folder that names
  it, else by the span that holds its start, from the session's own first call to its last
  record, after which runs it started in the background may go on; in two spans, given to
  the first and marked shared; in none, or named by a session the repository does not hold, left
  out as another project's;
- the repository's commits in the window, on any local branch, each given to a session by its
  span the same way.

It imports usage.py, which sits beside it wherever it is copied.
"""

import re
import subprocess
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

import usage

PROJECTS = Path.home() / ".claude" / "projects"
SCRATCHPAD = re.compile(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})-scratchpad")


@dataclass
class Working:
    """A working session of the repository: its calls in the window, and the span of its own calls."""
    id: str
    path: Path
    session: usage.Session
    span: tuple  # (first, last): its own first main-thread call and its last record, the window aside


@dataclass
class Headless:
    """A claude -p session started in the window, whole, and the working session it is given to."""
    id: str
    path: Path
    session: usage.Session
    owner: str
    by: str              # scratchpad or time
    shared: bool = False  # its start in two spans


@dataclass
class Commit:
    hash: str
    time: str
    owner: str | None    # None in no span
    shared: bool = False  # in two spans


@dataclass
class Window:
    start: str
    end: str
    sessions: list   # Working, by the start of their span
    headless: list   # Headless, by their start
    commits: list    # Commit, by their time


def folder_of(path):
    """The project folder Claude Code names after a path: every character but a letter or a digit turned into -."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def stamp(moment):
    """A datetime as a transcript writes a time, UTC to the millisecond; a naive one taken as local."""
    return moment.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def git(repo, *args):
    """git's output, or None when the command fails."""
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def instant(repo, given):
    """The time a bound stands for: a commit's committer time, a time, or now for None."""
    if given is None:
        return stamp(datetime.now(timezone.utc))
    committed = git(repo, "show", "-s", "--format=%cI", f"{given}^{{commit}}", "--")
    try:
        return stamp(datetime.fromisoformat(committed or given))
    except ValueError:
        raise ValueError(f"{given}: neither a commit of {repo} nor a time") from None


def prompted(path):
    """Whether a person prompted the session: a record of origin kind human."""
    return any(isinstance(record.get("origin"), dict) and record["origin"].get("kind") == "human"
               for record in usage.records(path))


def cut(session, first, last):
    """The session's calls between two times in seconds, with their runs, compactions and rebuilds."""
    def within(time):
        return first <= usage.moment(time) <= last
    runs = [replace(run, calls=[call for call in run.calls if within(call.time)]) for run in session.runs]
    return replace(session, main=[call for call in session.main if within(call.time)],
                   runs=[run for run in runs if run.calls],
                   compactions=[found for found in session.compactions if within(found.time)],
                   rebuilds=[found for found in session.rebuilds if within(found.call.time)])


def holder(spans, time):
    """(owner, shared): the first session whose span holds the time, None for none, and whether a second one does."""
    held = [key for key, (first, last) in spans if usage.moment(first) <= usage.moment(time) <= usage.moment(last)]
    return (held[0] if held else None), len(held) > 1


def window(repo, start, end=None, projects=PROJECTS):
    """The Window of the repository between two bounds, each a commit or a time; the end now by default."""
    repo, projects = Path(repo).resolve(), Path(projects)
    start, end = instant(repo, start), instant(repo, end)
    first, last = usage.seconds(start), usage.seconds(end)
    own, working, started = projects / folder_of(repo), [], []
    for path in sorted(projects.glob("*/*.jsonl")):
        if path.stat().st_mtime < first:
            continue  # last written before the window
        if prompted(path):
            if path.parent == own:
                working.append(path)
        else:
            session = usage.session(path)
            if first <= usage.moment(session.started) <= last:
                started.append((path, session))

    sessions = []
    for path, session in zip(working, usage.distinct([usage.session(path) for path in working])):
        times = sorted((call.time for call in session.main if call.time), key=usage.moment)
        inside = cut(session, first, last)
        if times and inside.calls:
            span = (times[0], max(times[-1], session.ended, key=usage.moment))
            sessions.append(Working(path.stem, path, inside, span))
    sessions.sort(key=lambda found: (usage.moment(found.span[0]), found.id))
    spans, ids = [(found.id, found.span) for found in sessions], {found.id for found in sessions}

    headless = []
    for path, session in sorted(started, key=lambda pair: (usage.moment(pair[1].started), pair[0].stem)):
        named = SCRATCHPAD.search(path.parent.name)
        if named:
            if named.group(1) in ids:
                headless.append(Headless(path.stem, path, session, named.group(1), "scratchpad"))
            continue
        owner, shared = holder(spans, session.started)
        if owner:
            headless.append(Headless(path.stem, path, session, owner, "time", shared))

    commits = []
    for line in (git(repo, "log", "--branches", "--format=%H %cI") or "").splitlines():
        commit, time = line.split()
        time = stamp(datetime.fromisoformat(time))
        if first <= usage.seconds(time) <= last:
            commits.append(Commit(commit, time, *holder(spans, time)))
    commits.sort(key=lambda found: (usage.seconds(found.time), found.hash))
    return Window(start, end, sessions, headless, commits)
