---
name: pruning-merged-branches
description: Deletes the remote branches of this repository that are merged into `main` and have had no commit for 30 days, keeping `main` and the release branches. Use when asked to clean up, prune or delete old branches, or when the remote has too many branches.
---

# Pruning Merged Branches

Run every command from the repository root. The team keeps `main` and every
`release/*` branch, merged or not (`CONTRIBUTING.md` § Branches).

A branch is merged into `main` when every one of its commits is reachable from `main`, so
deleting it loses no work. `git for-each-ref` lists references with the fields that
`--format` names, and `git push origin --delete` removes a branch from the remote.

## Steps

1. Update the remote-tracking branches:

   ```bash
   git fetch --prune origin
   ```

2. List the branches to delete: merged into `main`, no commit for 30 days (`CONTRIBUTING.md` § Branches), neither
   `main` nor a release branch.

   ```bash
   cutoff=$(date -d '30 days ago' +%F)
   git for-each-ref refs/remotes/origin --merged origin/main \
     --format='%(committerdate:short) %(refname:lstrip=3)' \
     | while read -r day branch; do [[ "$day" < "$cutoff" ]] && echo "$branch"; done \
     | grep -v -x -E 'HEAD|main|release/.*' > .git/prune-list.txt
   ```

   When `.git/prune-list.txt` is empty, delete it and stop: no branch is old enough.

3. Show the user the list and its count, and wait for a yes to deleting those branches
   on the remote: a branch deleted there is gone for everyone who has not fetched it.
   On anything but a yes, delete `.git/prune-list.txt` and stop.

4. Delete the listed branches on the remote:

   ```bash
   xargs git push origin --delete < .git/prune-list.txt
   ```

   Check: `git ls-remote --heads origin` lists none of them. A branch still listed is
   protected on the remote: report it.

5. Delete `.git/prune-list.txt`, and report the branches deleted and any that remain.
