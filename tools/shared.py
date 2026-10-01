#!/usr/bin/env python3
"""Keep the copies of the shared modules equal to their source.

Usage: tools/shared.py [--repo <dir>] [--check] [<skill-dir> ...]

A shared module is a folder shared/<module>/ whose files are copied into each skill that
uses it: a .py file into the skill's scripts/, a .md file into its references/; its tests/
stay in shared/. A skill uses a module when it holds a copy of one of its files. Named
skill directories receive every module; then every copy is refreshed from its source.
--check changes nothing: it prints each stale or missing copy and exits 1 when there is one.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = {".py": "scripts", ".md": "references"}


def sources(repo):
    """{module: [source files]} for each folder under shared/."""
    modules = {}
    for folder in sorted(p for p in (repo / "shared").glob("*") if p.is_dir()):
        modules[folder.name] = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix in FOLDERS)
    return modules


def copies(repo, skill, module=None):
    """{source: copy in skill} for every module, or for one."""
    return {source: skill / FOLDERS[source.suffix] / source.name
            for name, files in sources(repo).items() if module in (None, name) for source in files}


def used(repo, skill):
    """The modules skill holds at least one copy of."""
    return [name for name in sources(repo) if any(c.exists() for c in copies(repo, skill, name).values())]


def skills(repo):
    return sorted(p.parent for p in repo.glob("domains/*/skills/*/SKILL.md"))


def stale(repo):
    """(path, line, message) for each copy that differs from its source or is missing."""
    for skill in skills(repo):
        for module in used(repo, skill):
            for source, copy in copies(repo, skill, module).items():
                shown = source.relative_to(repo)
                if not copy.is_file():
                    yield copy, 1, f"missing copy of {shown}; run make shared"
                elif copy.read_bytes() != source.read_bytes():
                    yield copy, 1, f"differs from {shown}; edit the source, then run make shared"


def install(repo, skill):
    """Copy every module into skill."""
    for source, copy in copies(repo, Path(skill)).items():
        copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, copy)


def refresh(repo):
    """Bring every stale or missing copy back to its source; the copies written."""
    written = []
    for skill in skills(repo):
        for module in used(repo, skill):
            for source, copy in copies(repo, skill, module).items():
                if not copy.is_file() or copy.read_bytes() != source.read_bytes():
                    copy.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(source, copy)
                    written.append(copy)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description="Keep the copies of the shared modules equal to their source.")
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("skills", nargs="*", type=Path)
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if args.check:
        problems = list(stale(repo))
        for path, line, message in problems:
            print(f"{path.relative_to(repo)}:{line}: {message}")
        return 1 if problems else 0
    for skill in args.skills:
        install(repo, skill.resolve())
    for copy in refresh(repo):
        print(f"refreshed {copy.relative_to(repo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
