---
name: roadmap
description: Create, run, and close multi-phase project roadmaps — phase files with task checklists, a README with progress bars, one report per phase, and a per-repository contract. Use this skill for any request about a roadmap, whatever its kind — creating or writing one (even a short product roadmap), answering questions about one, or working inside one. Also use it whenever the user wants a long effort such as a migration, refactor, or rewrite split into tracked phases or steps; starts, opens, resumes, or continues a phase; says a phase is done or finished; acts on a phase report, for instance by merging, splitting, or reordering phases; closes a roadmap; or works on a phase-N-*.md or *-report.md file — even if the word "roadmap" is never used, and in whatever language the user writes. Not for CI pipeline stages, sprint boards in external tools, Gantt charts, changelogs, bug reports, or personal plans made in chat.
---

# Roadmap

Contract, invariants, and router for multi-phase project roadmaps. Operation detail lives in `references/`.

## The Repository Contract

Before any operation, run `scripts/conventions.py roadmap` from the repository, by its path in this skill's directory. On `status: ok`, it prints the contract: the `[roadmap]` table of the repository's `.agent-conventions.toml`, resolved against the file's shared keys. On any other status, follow `references/conventions.md` before going further: in a conversation, it proposes values and writes the file once the user agrees; without one, it reports and stops. A value is never guessed.

First, the minimal file — the three required keys:

```toml
language   = "english"
versioning = "git"

[roadmap]
root = "docs/roadmap"
```

Then the complete file, with the optional keys added:

```toml
language   = "english"
versioning = "none"
residue    = ["__pycache__/", "target/", "*.log"]
checks     = ["make lint", { run = "make test", dir = "packages/core" }]

[roadmap]
root = "docs/roadmap"
```

Key rules: `root`, `language`, and `versioning` are always present once the status is `ok`; `language` and `versioning` may sit at the top of the file or in `[roadmap]`. `versioning` is `git` or `none`, and `residue` comes with `none` only. `checks` applies only when declared: the reader names it on its `# not declared` line when it is absent.

`root` names the directory that **contains** the state folders, not one of them, and every roadmap of the repository lives there. So `<Root>` in any path template means its value, `docs/roadmap`, and a roadmap's own folder is `<Root>/pending/<roadmap-name>/`.

Two effects carry the actual portability:

- `versioning = "git"` adds a commit step per the repository's convention. `versioning = "none"` forbids one: the skill never promises a commit, never assumes a `git status` will catch a mistake, and instead checks that nothing matching `residue` is left before declaring a phase closed.
- Every `checks` command runs at the start of `close-phase` and `close-roadmap`, from its `dir`, relative to the repository root. **A red command stops the ritual**: a phase is not closable while a repository invariant is broken — report it and wait. With no `checks` declared, this step is skipped without comment.

## Invariants

Normative for every file under `references/`.

1. **Progress bar** — exactly 20 characters, `█` for done and `░` for the rest. Filled = `round(done / total × 20)`; percentage = `round(done / total × 100)`, rounded to an integer. Two guardrails: a phase that has started but is not finished never shows 0 filled cells (floor of 1); a phase that is not finished never shows 20 filled cells (ceiling of 19). Column alignment is preserved exactly. The line layout, for reference:

   ```
   Phase 0  Framing                    🟢 ████████████████████ 100%  (7/7)
   Phase 1  Implementation             🟡 █████████████░░░░░░░  64%  (7/11)
   Phase 2  Validation                 🔴 ░░░░░░░░░░░░░░░░░░░░   0%  (0/15)
   TOTAL                                  ████████░░░░░░░░░░░░  42%  (14/33)
   ```

   `scripts/progress.py` computes the block from the phase files; see Scripts below.
2. **Totals** — recalculated from the per-phase counts at every closure, never carried over from the previous figure: a phase adds and removes tasks along the way.
3. **Statuses** — 🔴 not started · 🟡 in progress · 🟢 done · ⏸️ blocked · ⚠️ needs review. Labels are rendered in the contract's language. **Only one phase may be 🟡 at a time** per roadmap. ⏸️ and ⚠️ are set by a person, never by this skill: no operation below writes or clears them.
4. **Editing** — exact string replacement, unique occurrence verified before writing, loud failure otherwise. Never a mass substitution: formats drift from one document to another, prose contains words that look like identifiers, and some directories are read-only. Every path is quoted — directories contain spaces, dots, and parentheses.
5. **Changelog** — an entry is added at the top; a past entry is never rewritten, it is a log. If names or paths have changed since, the old entry keeps the old ones and the new entry explains the change.
6. **Links** — never link to a source file: cite it with a backtick, `file.rs:123`. Never link to a missing file: write the note "to be created" instead. Relative links are checked before declaring a closing operation finished — `close-phase` and `close-roadmap` carry that check; the other two operations do not.
7. **Language** — every heading in English, all prose per `language`.
8. **Dates** — `Started` is written at opening, `Completed` at closure. Every date this skill writes — `Started`, `Completed`, `**Created:**`, `**Last Updated:**`, and the report's Work Log headings — is ISO `YYYY-MM-DD`.
9. **Folder name** — a roadmap's folder name is permanent. Chosen once at creation, it never changes afterwards: only the state segment of its path (`pending`, `on-progress`, `completed`) moves, and only the two closing operations move it.
10. **Reports** — every opened phase has exactly one report, beside its phase file and named after it with a `-report` suffix: `phase-N-<slug>-report.md`. It is created when the phase opens. Once the phase is closed, the report is a record and is never rewritten.

## Scripts

Bundled with this skill, run with `python3` from the repository root, the path taken from this skill's base directory:

- `scripts/progress.py <roadmap-folder>` prints the progress block, computed from the checkboxes under each phase file's `## Tasks`. Paste its output into the README instead of computing a bar or a total by hand.
- `scripts/progress.py --check <roadmap-folder>` compares the README block and every phase's `**Current Status:**` count with the phase files, and flags a 🟢 phase that keeps an unticked task or more than one 🟡 phase. Exit 1 lists each disagreement.
- `scripts/check_links.py '<glob>' ...` checks that relative links resolve. Quote each glob.
- `scripts/conventions.py roadmap` prints the contract, or what is wrong with it; see The Repository Contract. Run it by its path, without `python3`: it always exits 0, and its first line gives the status.

## Routing

| Intent | Read |
|---|---|
| Create a roadmap, add a phase to an existing one | `references/create.md` |
| Start work on a phase | `references/open-phase.md` |
| Resume work on an open phase | `references/report.md` |
| A phase is finished | `references/close-phase.md` |
| The whole roadmap is finished | `references/close-roadmap.md` |
