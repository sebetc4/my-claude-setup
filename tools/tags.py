#!/usr/bin/env python3
"""Find and create the release tags of the domains.

Usage: tools/tags.py [--repo <dir>] [--create]

A release is a version a domain's VERSION took on main, at the first commit of main's
first-parent history where VERSION holds it and its CHANGELOG.md entry carries a date,
"## X.Y.Z — YYYY-MM-DD": the merge when the version came from a branch. An entry headed
"## X.Y.Z — unreleased" is not released yet. Its tag is <domain>-vX.Y.Z. Without --create, prints each release that has no tag, with its
commit. --create makes each missing tag, annotated, on its commit: the subject
"<domain> domain X.Y.Z", then the version's entry of the domain's CHANGELOG.md at that
commit. Nothing is pushed. tests/check.py prints a warning for each missing tag.
"""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANCH = "main"
DOMAIN_FILE_RE = re.compile(r"^domains/([^/]+)/(?:VERSION|CHANGELOG\.md)$")
DATE_RE = r"\d{4}-\d{2}-\d{2}"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class Release:
    domain: str
    version: str
    commit: str

    @property
    def tag(self):
        return f"{self.domain}-v{self.version}"


def git(repo, *args, stdin=None):
    """git's output, or None when the command fails."""
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, input=stdin)
    return result.stdout if result.returncode == 0 else None


def releases(repo, branch=BRANCH):
    """Every Release on branch, by domain, oldest first; none when branch or git is missing."""
    if git(repo, "rev-parse", "--verify", "-q", f"refs/heads/{branch}") is None:
        return []
    log = git(repo, "log", "--first-parent", "--reverse", "--format=commit %H", "--name-only",
              f"refs/heads/{branch}", "--", "domains/*/VERSION", "domains/*/CHANGELOG.md") or ""
    found, commit, seen = {}, None, set()
    for line in log.splitlines():
        if line.startswith("commit "):
            commit, seen = line.split()[1], set()
            continue
        match = DOMAIN_FILE_RE.match(line)
        if not match or commit is None or match.group(1) in seen:
            continue
        domain = match.group(1)
        seen.add(domain)
        version = released(repo, commit, domain)
        if version:
            found.setdefault((domain, version), commit)
    return sorted((Release(domain, version, commit) for (domain, version), commit in found.items()),
                  key=lambda r: (r.domain, tuple(int(n) for n in r.version.split("."))))


def released(repo, commit, domain):
    """The version domain's VERSION holds at commit when its changelog entry is dated, else None."""
    version = (git(repo, "show", f"{commit}:domains/{domain}/VERSION") or "").strip()
    if not VERSION_RE.match(version):
        return None
    changelog = git(repo, "show", f"{commit}:domains/{domain}/CHANGELOG.md") or ""
    dated = re.search(rf"^## {re.escape(version)}\b[^\n]*\b{DATE_RE}\b", changelog, re.M)
    return version if dated else None


def missing(repo, branch=BRANCH):
    """The releases that have no tag."""
    tagged = set((git(repo, "tag", "-l") or "").split())
    return [r for r in releases(repo, branch) if r.tag not in tagged]


def message(repo, release):
    """The tag's message: its subject, then the version's changelog entry at the release."""
    subject = f"{release.domain} domain {release.version}"
    changelog = git(repo, "show", f"{release.commit}:domains/{release.domain}/CHANGELOG.md") or ""
    entry = re.search(rf"^## {re.escape(release.version)}\b[^\n]*\n(.*?)(?=^## |\Z)", changelog, re.M | re.S)
    body = entry.group(1).strip() if entry else ""
    return f"{subject}\n\n{body}" if body else subject


def create(repo, branch=BRANCH):
    """Makes every missing tag; returns their names."""
    made = []
    for release in missing(repo, branch):
        if git(repo, "tag", "-a", release.tag, release.commit, "-F", "-", stdin=message(repo, release)) is None:
            raise RuntimeError(f"git could not create {release.tag} on {release.commit[:7]}")
        made.append(release.tag)
    return made


def warnings(repo):
    """One (path, line, message) per missing tag, for tests/check.py."""
    return [(repo / "domains" / r.domain / "VERSION", 1,
             f"{r.domain} {r.version}, set in {r.commit[:7]}, has no tag {r.tag}: run make tags")
            for r in missing(repo)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Find and create the release tags of the domains.")
    parser.add_argument("--repo", type=Path, default=ROOT, help="the repository, this one by default")
    parser.add_argument("--create", action="store_true", help="make the missing tags")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if args.create:
        absent = missing(repo)
        made = create(repo)
        for release in absent:
            if release.tag in made:
                print(f"created {release.tag} on {release.commit[:7]}")
        if not absent:
            print("no tag missing")
        return 0
    absent = missing(repo)
    for release in absent:
        print(f"{release.tag} {release.commit[:7]}")
    if absent:
        noun = "tag" if len(absent) == 1 else "tags"
        print(f"{len(absent)} {noun} missing: tools/tags.py --create makes {'it' if len(absent) == 1 else 'them'}")
    else:
        print("no tag missing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
