#!/usr/bin/env python3
"""Check that the relative Markdown links in the given files resolve.

Usage: python3 check_links.py GLOB [GLOB ...]

Each GLOB is quoted so that the script, not the shell, expands it. Links to
http(s), mailto, and in-page anchors are skipped; a `#fragment` is ignored and
percent-encoding is decoded. Prints every broken link, then the count, and
exits 1 when a link is broken or when no file matched the globs.
"""

import glob
import os
import re
import sys
import urllib.parse

LINK_RE = re.compile(r"\]\(([^)]+)\)")


def main(patterns):
    if not patterns:
        print(__doc__.strip())
        return 2
    files = sorted({f for pattern in patterns for f in glob.glob(pattern)})
    if not files:
        print("no files matched the globs — fix the arguments before trusting the count")
        return 1
    total = broken = 0
    for path in files:
        base = os.path.dirname(path)
        with open(path, encoding="utf-8") as handle:
            links = LINK_RE.findall(handle.read())
        for link in links:
            if link.startswith(("http", "#", "mailto")):
                continue
            total += 1
            target = os.path.normpath(os.path.join(base, urllib.parse.unquote(link.split("#")[0])))
            if not os.path.exists(target):
                broken += 1
                print(f" x {path} -> {link}")
    print(f"{total} relative links, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
