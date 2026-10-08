#!/usr/bin/env python3
"""The PreToolUse hook that keeps an evaluation run inside its copy.

Usage, as a hook command: guard.py <denied path> ...

Reads the call on standard input and refuses it when any string of its input names a
denied path — the real repository's root and the real configuration folder, which run.py
passes: as written, without its leading slash, and under the home folder as `~/`,
`$HOME/` or `${HOME}/`. A path counts only whole, so that `/code/repo` does not refuse
`/code/repository`. An unreadable call is refused. The refusal is Claude Code's
PreToolUse decision, printed on standard output; a call allowed prints nothing.

Three things pass. The text an editing tool writes (TEXT_KEYS): a skill may say `~/.claude`
without touching it, while the file's path is still checked. In a shell command, the
body of a heredoc whose delimiter is quoted and that `cat` writes to a file, unpiped:
bash hands such a body over as it is, and nothing runs it; the rest of the command, the
file written included, is checked, and so is any other heredoc, since it can reach a
program that acts on what it names. And the session's own folder, beside the transcript
the event names, where Claude Code keeps the tool output it set aside for the session to
read back. A refusal says how to write text that names a denied path.
"""

import json
import os
import re
import sys

EDGE = r"[\w.-]"
REASON = "outside the test's limits"
HOW = "To write text that names it, use Write or Edit, or cat > <file> <<'EOF'."
# Keys whose value is text written into a file, not a path: Write, Edit, MultiEdit's
# edits, NotebookEdit.
TEXT_KEYS = ("content", "old_string", "new_string", "new_source")
# The Bash tool's command.
COMMAND_KEY = "command"
# A heredoc operator and its delimiter: quoted, escaped, or bare.
HEREDOC = re.compile(r"<<(-?)[ \t]*(?:'([^'\n]*)'|\"([^\"\n]*)\"|\\([\w.-]+)|([\w.-]+))")
WRITER = re.compile(r"\s*cat(?![\w.-])")


def forms(path, home):
    """The ways a command can name path."""
    path = path.rstrip("/") or "/"
    found = {path, path.lstrip("/")}
    home = home.rstrip("/")
    if home and (path == home or path.startswith(home + "/")):
        rest = path[len(home):]
        found |= {"~" + rest, "$HOME" + rest, "${HOME}" + rest}
    return [f for f in found if f]


def pattern(paths, home):
    alternatives = sorted({re.escape(f) for path in paths for f in forms(path, home)}, key=len, reverse=True)
    return re.compile(rf"(?<!{EDGE})(?:{'|'.join(alternatives)})(?!{EDGE})")


def body_end(command, i, delimiter, dash):
    """(where the heredoc body that begins at i ends, where the line after its delimiter begins)."""
    n = len(command)
    while i < n:
        end = command.find("\n", i)
        end = n if end < 0 else end
        text = command[i:end]
        if (text.lstrip("\t") if dash else text) == delimiter:
            return i, min(end + 1, n)
        i = end + 1
    return n, n


def unwritten(command):
    """The command without the body of each quoted heredoc that cat writes to a file, unpiped.
    A simple command ends at a newline, ; & && || | |& ( ) or a backtick outside quotes; the
    bodies of a line's heredocs follow its newline, in order."""
    drops, line, heredocs = [], [], []
    start, quote, redirected, i, n = 0, None, False, 0, len(command)

    def close(end, piped):
        line.append((bool(WRITER.match(command[start:end])) and redirected and not piped, heredocs))

    while i < n:
        c, following = command[i], command[i + 1:i + 2]
        if quote:
            if c == quote:
                quote = None
            elif c == "\\" and quote == '"':
                i += 1
        elif c in "'\"":
            quote = c
        elif c == "\\":
            i += 1
        elif command.startswith("<<<", i):
            i += 2
        elif (match := HEREDOC.match(command, i)):
            quoted = next((g for g in match.group(2, 3, 4) if g is not None), None)
            heredocs.append((match.group(5) if quoted is None else quoted, quoted is not None, match.group(1) == "-"))
            i = match.end()
            continue
        elif c in "<>" and following == "&":
            i += 1
        elif c == ">" or (c == "&" and following == ">"):
            redirected = redirected or following != "("
            if following in (">", "|") or c == "&":
                i += 1
        elif c in "\n;&|()`":
            two = command[i:i + 2]
            close(i, two == "|&" or (c == "|" and two != "||"))
            i += 2 if two in ("&&", "||", "|&") else 1
            start, redirected, heredocs = i, False, []
            if c == "\n":
                for writes, docs in line:
                    for delimiter, quoted, dash in docs:
                        body = i
                        end, i = body_end(command, i, delimiter, dash)
                        if quoted and writes:
                            drops.append((body, end))
                line, start = [], i
            continue
        i += 1
    kept, last = [], 0
    for begin, end in drops:
        kept.append(command[last:begin])
        last = end
    kept.append(command[last:])
    return "".join(kept)


def strings(value):
    """The strings of a call's input, the text it writes left out."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if key == COMMAND_KEY and isinstance(item, str):
                yield unwritten(item)
            elif key not in TEXT_KEYS:
                yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def own_folder(event):
    """The session's own folder, beside its transcript, or None."""
    transcript = event.get("transcript_path")
    if isinstance(transcript, str) and transcript.endswith(".jsonl"):
        return transcript[:-len(".jsonl")]
    return None


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))


def main(argv=None):
    denied = sys.argv[1:] if argv is None else argv
    try:
        event = json.loads(sys.stdin.read())
        given = event.get("tool_input") or {}
    except (ValueError, AttributeError):
        deny(f"{REASON}: the guard could not read the call")
        return 0
    if denied:
        home = os.path.expanduser("~")
        found = pattern(denied, home)
        own = own_folder(event)
        allowed = pattern([own], home) if own else None
        for text in strings(given):
            if allowed:
                text = allowed.sub("", text)
            match = found.search(text)
            if match:
                deny(f"{REASON}: `{match.group(0)}` lies outside the run's folder. {HOW}")
                return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
