# Old Contract

When `scripts/conventions.py roadmap` reports `missing` and the repository's instruction
file holds a `## Roadmaps` block, map it line by line into the proposal of
`references/conventions.md`, Create The File, each value with the line it comes from.

| Old line | New key |
|---|---|
| `Root : docs/roadmap/{pending,on-progress,completed}/` | `root = "docs/roadmap"`, without the brace group |
| `Language : english` | `language = "english"` |
| `Versioning : git` | `versioning = "git"`; with `none`, the residue the block's prose names goes to `residue` |
| `Checks :` one command per line | `checks = [...]`, one string each; a command run from a subfolder becomes `{ run, dir }` |

An old line that no row maps has no key in the file: leave it out, and name it to the user.
