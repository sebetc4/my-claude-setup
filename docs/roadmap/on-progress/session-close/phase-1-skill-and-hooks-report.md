# Phase 1 Report: Skill And Hooks

**Phase:** [phase-1-skill-and-hooks.md](phase-1-skill-and-hooks.md)
**Start Commit:** 1d55bc7

---

## Work Log

### 2026-10-13

Phase opened at the user's request, in a new session as Phase 0's closure planned. Read
before working: the roadmap's README, `phase-0-framing.md` with its `## Design`, and
`phase-0-framing-report.md` in full. No restructuring was pending in Phase 0's
`## Changes To Later Phases`, its one entry approved and applied in version 1.1.0, and no
other phase of the roadmap was in progress. `docs/roadmap/README.md` now shows Phase 1 in
progress.

One gap between the plan and the design, raised with the user: the hook task names "the
latest resume note not yet taken up", where the approved design names each note not taken
up, latest first, three at most.

The user asked how notes could pile up when the next session takes a note up. It does not
necessarily: a note counts as taken up only when a later close continues its work, and the
next session may work on something else. Phase 0's requests show it twice: in open-design
on 2026-10-08, request 38 wrote `session/reprise-rapport-domaines.md` and the next
session, on another strand of the same study, closed an hour later with
`session/note-ouverte-runtimes.md` (41), two strands open at once; in open-work-projects on
2026-10-10, two sessions ran side by side in `hermes/repo` and `openclaw/repo` and closed
eight minutes apart (66, 67), both writing `_notes-reprise.md`. Three of the five study
closes (41, 48, 67) have no next session in the transcripts, so their notes would have
stayed open. The cap of three is the agent's, not a figure of the data, which never shows
more than two at once; it keeps a dropped note from being named forever once newer ones
exist. The user kept the design and asked to measure that the line does not bring too much
noise: the hook task now follows the design, and Phase 2 measures the noise.

Seen on the way: this session's tool review measured `session_resume.py` at 0 runs and 0
characters injected, though the transcript holds its `hook_success` record and its
`hook_additional_context`, before the session's first message. Phase 2's measure reads the
transcripts itself rather than the reviews' measured block; the cause is not looked into.

The user approved Phase 2's two thresholds, and turned down a precision the agent
proposed, that a close marks a note taken up only when the session did what the note's
resume point asked: a session that takes a note up closes it, even when the user has
changed their mind on the way forward meanwhile; otherwise such a note would never be
closed. The skill task's case outside a roadmap now starts from an earlier note.

Task 1. The `[session]` table joins `shared/conventions/`: `TOOLS` gains `session`, with
`notes`, a required path, and `language` from the shared keys, optional; `conventions.md`
gains the key and where to look for it — a `sessions/` subfolder of a notes folder the
repository keeps, else `notes/sessions`. Tests first, watched failing: three in the
module's own tests (the table resolved, no language needed, `notes` missing), four in
`domains/session/tests/test_conventions.py` through the skill's copy — the table read, no
file, a file without the table, a folder outside the root —, two in `test_permissions.py`.
Then the domain: `VERSION` 0.1.0, `CHANGELOG.md` `— unreleased`, `hooks.json` empty until
task 2, `permissions.json` allowing `skills/close-session/scripts/conventions.py` by its
path; the copy and its reference under `skills/close-session/`, ahead of the skill's
`SKILL.md`. `make shared` refreshed the copies in `roadmap`, `authoring-skills` and
`tool-review`, whose unreleased changelog entries say so. `make check` passes, 3 skills
checked, `tests/domains.py` running on the new domain. No tie to Claude Code added:
`docs/claude-code-coupling.md` already covers `domains/*/permissions.json` and the
reader's personal directory. Task 1 done.

The user asked to finish this roadmap before any other change to the setup: the defects
seen on the way, such as the review's count of SessionStart hooks above, wait for it.

Task 2. `domains/session/tests/test_hooks.py` first, 17 tests run as Claude Code runs a
hook, all red without the hook: one conditional line per open note, latest first, three at
most, notes of the same day by their last change, a note taken up left out, a file without
the `**Taken up:**` field not counted as a note, a resume point's first item joined over
its lines and cut past 200 characters, a note without a resume point still named, the
table read from a subfolder, a folder with spaces, and silence without the file, without
the table, with an invalid table, without the folder, with every note taken up, and on
invalid JSON. Then `domains/session/hooks/resume_note.py`: it finds the skill's
`scripts/conventions.py` above it, as `session_resume.py` finds the roadmap skill's, in the
repository or installed, reads `[session]`, and names the open notes; the latest is the
latest `**Date:**`, then the latest change, since a note holds no time. `hooks.json`
registers it at SessionStart under `python3 -B`, so that importing the reader leaves no
`__pycache__` in the installed skill. Tried under `make enable D=session
CLAUDE_DIR=$(mktemp -d)`: the hook, the skill's copy and the allow rule installed, the
installed hook silent on this repository, which has no `[session]` table, and naming a
fixture repository's open note. `docs/claude-code-coupling.md` names the domain's
`hooks.json` and the hook in its rows on events and stdin. `make check` passes. Task 2
done.

The user proposed two keys in `[session]`, one turning the hook on or off and one setting
how many notes it names; the agent proposed a single one, since two can contradict
(`enabled = true` with 0 notes), and the user agreed: `start_notes`, a whole number, 3 when
not declared, `0` turning the hook off while the close still writes its notes. Task 2
reopened for it, tests first, five red: in `shared/conventions/`, the key read, and
refused when negative, a boolean, a string or a float, through a new kind `count`; in the
hook's tests, `start_notes = 1` naming the latest note alone and `0` keeping the hook
silent. `make shared` refreshed the three skills' copies; the copy under
`skills/close-session/` was copied by hand, as the problem below says. The task's text and
proof name the key. `make check` passes.

The user asked to record the session and to go on in a new one. Everything above is
committed, the last commit `41eebaa`; the README's progress block still reads 0/4, as it
is recomputed at the phase's closure only.

At that close, the agent also wrote the user's request to finish this roadmap first into
its memory, as a rule the user gave; the user pointed out that the tool being built keeps
such things out of memory. The agent agreed and deleted it: the request holds until this
roadmap ends, so it is the project's state, not a rule — a memory that must be deleted at
a date is the state the design keeps out —; this report and `docs/roadmap/README.md`
already hold it; and an agent need not hold the user to their own request. The design's
"a preference or a rule the user gave" let it through: the skill needs a test, whether
it still holds once the work in progress is done; if not, it goes to the report or the
note.

The user confirmed: inside a roadmap, the close records in the phase report, not in a
note nor in the memory, and this case is an example to keep when writing the setup's
tools. Task 3's case of a step stopped midway now carries it, its assertions checking
the report and the agent's memory left unchanged. The user's expectation itself went to
the memory, as `roadmap-records-in-report.md`: it holds beyond this roadmap.

**Where the next session starts:**
1. Task 3, `SKILL.md` and its references, written with the `authoring-skills` skill,
   loaded first. They build `phase-0-framing.md`'s `## Design` with this report's
   Decisions: a note is taken up by the session that takes it up, whatever it then does;
   `start_notes`; `language` optional; and the memory's test above, a request that holds
   only until the work in progress ends going to the report or the note, never to memory,
   also a near miss for the evals. The skill folder already holds the copy of
   `shared/conventions/`, `scripts/conventions.py` and `references/conventions.md`;
   once `SKILL.md` exists, check that `make check` compares the copy with its source and
   that `make shared` refreshes it (see Problems And Deviations).
2. Task 3's evals: three cases on a fixture repository, `evals/fixtures.py` — a roadmap
   step stopped midway, where the user asked to finish the roadmap first, recorded in the
   report and not in memory, a phase with every task ticked, a session outside any roadmap
   that took up an earlier note on another course than its resume point said, the note
   marked taken up —, then `audit.py` and `skill-auditor`. The eval scripts start
   `claude -p` sessions only with `--start`, after announcing their count and cost to the
   user.
3. Task 4, the trigger evals: the close requests of `study/session-close/close-requests.json`
   and the near misses `kinds.md` sorts as `near-phase` and `near-fact`, through
   `triggers.py`, at the rates of the design: 0.9 or more on the held-out close requests,
   0.1 or less on the near misses.
- No question is waiting for the user. Nothing is uncommitted.
- Waiting for this roadmap's end, at the user's request: any other change to the setup,
  among them the review's count of 0 runs for `session_resume.py` seen above.

Resumed in a new session. Task 3, with `authoring-skills` loaded: its procedure writes
`evals/evals.json` before any other file of the skill and runs the cases without it first,
the assertions coming from the failures. An eval run is a fresh `claude -p` session given a
single prompt, with auto memory off (`harness.py`): so each case's prompt gives the session
to close as a summarized dialogue, then the user's close request, and the fixture's
`CLAUDE.md` declares the agent's memory as the tracked folder `.agent-memory/`, worded as
Claude Code's memory instructions, so that a write to it shows in the run's `changes.json`.
`evals/fixtures.py` builds a small service, stock-sync, with roadmap `resilient-sync` open
at its Phase 1 and a `[session]` table, in three states: task 2 half done and uncommitted;
every task ticked, the last one uncommitted beside `config/local.toml` modified on purpose;
a clean tree with an open resume note on export formats, which the session took up on
another course. `evals/test_fixtures.py` first, four tests red, then green. The three
cases in `evals.json` carry their expected output, no assertion yet. The baseline,
iteration 1, one run per case without the skill at `claude-sonnet-5-5` and `xhigh`,
estimated at $7.50, started on the user's yes.

The three runs cost $0.58, thirteen times less than announced. The user has seen the same
in ai-ctl's roadmap `review-skill`: runs of a little over $1 and $4, announced much higher.
`run.py`, with no complete run of the skill, counts each run at $2.50, a full
skill-writing task's mean. The user, on 2026-10-13: not being able to estimate a run is
no problem in itself, but the announcement should then speak of a limit — the runs'
ceiling — rather than of an expected cost. Waiting for this roadmap's end, as the user
asked for every other change to the setup; this phase's next announcements read the
measured runs of iteration 1.

What the runs without the skill did, each case quoted in `evals.json`'s
`failures_without_skill`: the step stopped midway wrote the user's request to finish the
roadmap first into `.agent-memory/finish-roadmap-first.md`, the failure seen at this
roadmap's own close on 2026-10-13, wrote a resume note beside the report's entry, deleted
the previous entry's resume point and filled Files Changed by hand; the phase with every
task ticked committed nothing ("puisque tu ne me l'as pas demandé"), wrote a note beside
the report, recomputed the README's progress block and filled Files Changed; the session
outside a roadmap wrote a sound note but committed nothing either, and marked the earlier
note `finished` beside the new note's name. The second case also showed a flaw of the
fixture: its `src/sync.py` called none of the retry functions, and the run rightly kept
the phase open; `fixtures.py` now gives task 3 a `replay()` loop and a test through ten
refusals, its test first, red, then green. The assertions come from these failures and
from the design. Then `SKILL.md`, from the task template, and
`references/resume-note.md`, the note's folder, form and `**Taken up:**`, read only
outside a roadmap; `audit.py` clean. With `SKILL.md` written, `tools/shared.py` finds the
skill and checks its copy of `shared/conventions/`: the problem below is closed.
Committed as `eda5154`.

Iteration 2, on the user's yes: 18 runs, three per case with the skill and three without,
$0.10 to $0.23 each. From the files they changed alone: without the skill, the agent's
memory written in all six runs of the first two cases and a note beside the report in
four, no commit in the case outside a roadmap; with it, the report's entry alone when the
step stopped midway, a commit and no note when every task was ticked, the note committed
outside a roadmap. `grade.py` announced 18 `skill-grader` sessions at $8.10, with no
grading of this skill measured: `skill-auditor`'s mean session, $0.45. The agent passed it
on as "$8.10 at most", saying where the figure came from; the user found that form right —
a limit, with its source — and asked whether the changes waiting for this roadmap's end
would not be forgotten once its reports are frozen: they become a task of Phase 2, below.
Committed as `d3b1285`. Found after the close below: $8.10 is no limit but another agent's
mean; the sessions' ceiling is $18, 18 times `grade.py`'s `--budget` of $1.00. The memory
`eval-cost-announcement.md` and this entry's resume point now say so.

The user asked to record the session and to go on with the grading in a new one. The
user's preference on cost announcements went to the agent's memory, as
`eval-cost-announcement.md`: it holds beyond this roadmap.

**Where the next session starts:**
1. Task 3, grading iteration 2: `grade.py .eval-runs/skills/close-session/iteration-2`
   lists 18 `skill-grader` sessions; announce them at $18 at most, their ceiling of $1.00
   each, its $8.10 being `skill-auditor`'s mean session and no measure of this skill's
   grading; then `--start` after the user's yes. Then
   `benchmark.py` and `viewer.py`, the cases' review items for the user.
2. Read the runs with the skill that fail an assertion, and each assertion that does not
   tell the two configurations apart; change `SKILL.md` by `authoring-skills`'s Edit
   section, and run again the cases a change concerns.
3. `skill-auditor` on `domains/session/skills/close-session`, its cost announced first:
   task 3's proof needs its PASS, with `audit.py` clean and the assertions passing.
4. Task 4, the trigger evals, as the previous resume point says.
- No question is waiting for the user.
- Pending: iteration 2's 18 runs, complete and ungraded, under the ignored
  `.eval-runs/skills/close-session/iteration-2/`. Nothing is uncommitted after this
  record's commit.
- Waiting for this roadmap's end: the changes to the setup the Phase 2 task added today
  hands over.

Resumed in a new session. Iteration 2 graded on the user's yes, announced as a limit:
18 `skill-grader` sessions capped at $1 each by `--budget`, $18 at most, the $0.45 a
session `grade.py` printed being `skill-auditor`'s mean and not this grading's. They
cost $1.58. With the skill, every assertion passes in all nine runs; without it, 57%
(44% to 75%), at $0.113 a run against $0.159 and 40 s against 66 s. No grading named a
weak assertion. 16 of the 26 assertions pass in every run of both configurations: most
guard a rule the skill states and an edit could break — no commit for a step stopped
midway, the phase left open, the README unchanged, `config/local.toml` left out —, and
in the case outside a roadmap the new note's form comes from the earlier note the
fixture holds, which the run without the skill copies. Read beyond the assertions: two
of the three runs with the skill outside a roadmap end saying the open note will be
named at the next session's start, which nothing in the run shows, the grader marking
the claim unverified; the Result's "or nothing when the next session's start names the
open notes" invites it, while an agent knows the hook runs only from its own session's
start. `viewer.py` serves the outputs with iteration 1's for the user's review.

The agent recommended keeping the assertions that do not tell the configurations apart,
as guards of rules the skill states; the user did not object. On the user's yes, the
Result now says "or nothing when this session's own start named open notes: that line
comes from a hook, which may be missing or turned off by the `[session]` table's
`start_notes = 0`", and the case outside a roadmap gains an assertion, the answer
claiming nothing of what the next session's start will show, with the failure quoted
under `failures_with_skill`. Iteration 3, on the user's yes: that case alone, three runs
with the new version and three with the committed one (`HEAD`, `958da76`), $0.80 in all
against $0.87 announced, measured from 21 runs this time. Read before grading: one run
of the committed version in three still claims the next start will name the note, and
all three runs of the new version say "if the start hook is active, it will propose the
note", the explanation added to the Result passed on to the user, true but noise. On
the user's yes, the explanation is gone: "or nothing when this session's own start named
open notes." Iteration 3 is left ungraded.

Iteration 4 was to take iteration 3's three baseline runs with `--reuse`, but
`workspace.py` took none, saying nothing: the case's digest differed, since the
fixture's report names its start commit, whose hash carries the build's time. Tests
first: `evals/test_fixtures.py` builds each case under two clocks and compares the
commits, red, then green once `fixtures.py` gives every commit the date
2026-10-10T18:00:00+02:00. `make check` passes. Iteration 4 prepared again on the new
fixture: six runs, three with the uncommitted `SKILL.md` and three with `958da76`'s,
both snapshots taken at preparation, $0.85 estimated from 27 runs, capped at $0.50 a run.
The user closed the session before starting them.

The user asked to record the session and to start the runs in the next one.

**Where the next session starts:**
1. Task 3, iteration 4: `run.py .eval-runs/skills/close-session/iteration-4` lists six
   runs at $0.85, a measured mean, $3 at most; show the user that line with the model
   and effort, then `--start` after the yes. The iteration holds its snapshots: do not
   prepare it again, or with `--baseline 958da76` if it must be, since `HEAD` will hold
   the new `SKILL.md` once committed. Then `grade.py` (six sessions, $0.09 each
   measured), `benchmark.py`, and the new assertion read in both arms.
2. When the new version passes it and the other assertions, commit `SKILL.md`; otherwise
   rework the Result's sentence and run the case again.
3. The user's review of iteration 2, not given yet: `viewer.py
   .eval-runs/skills/close-session/iteration-2 --previous
   .eval-runs/skills/close-session/iteration-1`, its address to the user.
4. `skill-auditor` on `domains/session/skills/close-session`, its cost announced first,
   then task 4, the trigger evals, as the earlier resume points say.
- No question is waiting for the user.
- Uncommitted on purpose: `domains/session/skills/close-session/SKILL.md`, the Result's
  sentence, until iteration 4 settles it. Under the ignored `.eval-runs/`: iteration 3's
  six runs, ungraded and left so; iteration 4, prepared, no run started.
- Waiting for this roadmap's end: the changes Phase 2's hand-over task lists, now with
  `workspace.py` naming why `--reuse` takes no run.

Resumed in a new session. Iteration 4 started on the user's yes, announced at $0.85
measured, $3 at most: six runs, $0.80. Read before grading, the new assertion fails
either way: two runs of the new version in three still say the next start will name
the note ("que le démarrage de session devrait déjà signaler", "la note sera chargée au
démarrage"), and all three of `958da76`'s. Over iterations 2 to 4, `958da76`'s version
made the claim in six runs of nine. The Result's sentence is not its source: every run
outside a roadmap reads `references/conventions.md`, whose `start_notes` row says a
session's start names the open notes, three when not declared, and the fixture's table
declares none. Yet this session's own start named no note while one was open, the only
evidence of what a start shows here. Iteration 4 is left ungraded, its verdict on the
new assertion read from the answers.

On the user's yes, the Result gains a condition and no explanation of the hook, which
iteration 3 saw passed on to the user: "When it named none, say nothing of what the next
start will show." `audit.py` clean. Iteration 5, on the user's yes: that case, three runs
of the new version, `958da76`'s three taken from iteration 4 with `--reuse`, which works
since the fixture's dates are fixed; $0.42 announced, $0.35 spent. Graded on the user's
yes, $0.53 announced, $0.57 spent: the new version passes all nine assertions in its
three runs, which end on the words to type and nothing of the next start;
`958da76`'s pass eight, the new assertion failed in all three, the grader marking each
claim unverified. Its evidence says `start_notes` not declared means no start line,
when it means three; the verdict holds on the run's own start, which named none. Read
beyond the assertions: one run of the new version writes in its note that the note
itself is still uncommitted, true until the commit that follows; left as seen once.
`SKILL.md` committed with this entry.

`viewer.py` serves iteration 2 beside iteration 1 for the user's review, not given yet.
`skill-auditor`, on the user's yes, announced at $0.45, its mean session on other
skills, with no ceiling since a subagent takes no budget: `VERDICT: FAIL`, three lines.
Two prohibitions answer no failure the runs show — "never `git add -A`, `git add .` or
`git commit -a`" and "Write no decision record" —: no run without the skill staged
everything, those of the case with every task ticked committing nothing, and none wrote
a decision record; both come from the design (`phase-0-framing.md`, the close's
decision record and its staging by path). The third asks to cut from
`references/conventions.md` the keys of the other tools, which the repository forbids:
the page is a copy of `shared/conventions/`, kept identical by `tests/check.py`.

On the user's yes, the two cuts: "Stage by path the files the session wrote: the tree
may hold files left uncommitted on purpose", and "The resume point names any decision
record to write." The case with every task ticked keeps its assertion on the run's
commands, no `git add -A`, `git add .` or `git commit -a`. Wording meant to keep
behavior, so its proof is the existing evals again: iteration 6, the new version alone
on the three cases, nine runs announced at $1.25 measured, $4.50 at most, started on the
user's yes. They cost $0.99. Graded on the user's yes, $0.80 announced, $0.74 spent: all
27 assertions pass in the nine runs. Every commit stages its files by path, and no run
writes a decision record. One grader calls weak the assertion on the commit message's
form, which a `docs(retry)` passes where the case expects `feat(retry)`; kept, since a
commit holding a document and its report may fairly take `docs`. One run of the step
stopped midway wrote its entry in three edits rather than one write, the entry still
passing. Committed with this entry; `skill-auditor` to run again, told that
`references/conventions.md` is a shared copy.

`skill-auditor` again, on the user's yes, announced at $0.11, its first pass measured:
`VERDICT: FAIL`, four lines, none raised by the first pass on the same text. Step 3's
"Ask the user nothing" contradicts `references/resume-note.md`, which proposes the
`[session]` table and writes it once the user agrees, where the design says "asks
nothing it can record instead", as the skill's opening does; "an agent of another
provider could not read it" adds a second reason the memory rule does not need; the
Result's "open notes" and step 6's "the note" stand for the resume note; and the Result
relies on a start line the skill never names, which iteration 3 showed is passed on to
the user once explained, while the condition as written passed in the six runs since.

The agent proposed to correct the first three, keep the Result as it was, and, should a
third pass raise only new minor points, to count a FAIL whose every line is fixed or
answered as task 3's proof. The user refused: no FAIL, as many runs as needed to find
the wording. So the four are applied: step 3 asks nothing "that can be recorded
instead"; the memory rule keeps its one reason; "resume note" wherever the skill meant
it; and the Result shows the start line's form, "Resume note notes/sessions/<file>
(<date>), not taken up", without the hook's mechanism. `evals.json` quotes under
`failures_with_skill` what iterations 3 and 4 showed, so that the auditor reads why the
Result explains no hook. `audit.py --checks` clean.

Two `skill-auditor` passes at once, $0.22 announced, since each pass draws other points
from the same text: both FAIL, nine lines between them, some shared. Applied: the usage
limit cites `docs/decisions/2026-10-13-session-close.md`; "ask nothing that can be
recorded instead" kept in step 3 alone; "even when another roadmap has a phase open"
cut; the start line's source named, `domains/session/hooks/resume_note.py`; "the log"
now "the Work Log"; the resume point defined once, the block ending a report's entry or
a resume note's section Where The Next Session Starts; "resume note" throughout
`references/resume-note.md` too. Two applied otherwise than asked: "step" was to become
"task", which would commit only whole tasks where this repository commits each recorded
step, so the skill now says "work", defined at the commit as "a task, or a part of one
that stands alone, such as a test with its code", the description's "commits a finished
step" following; and the `## Result` heading, from the task template, stays, its text
opening on "The answer". Two passes again on that version.

Both FAIL again, one line for the first, six for the second, of which one says itself it
needs no fix. Shared: `references/resume-note.md` said the notes' folder "is not meant to
be versioned" with no source, beside a commit rule for a tracked folder; it now says the
notes stay out of version control unless the user tracks their folder, citing the
decision record, and step 7 commits them only when git tracks their folder, by default
not. Applied too: step 3 keeps only "Each open question goes into the resume point", the
prohibition answering no failure; `versioning = "none"` points to
`references/conventions.md`; the commit message's form is cut, a convention the model
follows, the case with every task ticked keeping its assertion on it; and the resume
point's definition names the report's heading and the note's section, without "block".
Two passes again.

Both answer `VERDICT: PASS`, each prohibition left tied to a failure the evals quote, each
fact to its source. Iteration 7, the user having asked for as many runs as the wording
needs: the final version alone on the three cases, nine runs announced at $1.20
measured, $4.50 at most.

They cost $1.08. Read before grading: one run in three outside a roadmap promises again
what the next start shows, "ouvrez une nouvelle session, l'ouverture annoncera la note
de reprise"; the two other cases end as they should. Giving the start line's form and
its hook's file tells the agent a hook exists, where iterations 5 and 6, without either,
passed six runs in six. So the Result takes the observable condition the second
auditor offered: "or nothing when a line at this session's start named open resume
notes. When none did, say nothing of what the next start will show." The failure joins
`failures_with_skill`. Iteration 7 left ungraded. Then, at once: two auditor passes;
iteration 8, the three cases, nine runs; and iteration 9, the case outside a roadmap
again on the same snapshot, three runs, since `workspace.py --extend` takes no
`--case` and one failure in three hides easily in three runs: twelve runs announced at
$1.56, $6 at most.

The twelve runs cost $1.60; outside a roadmap, all six end on the words to type and
nothing of the next start. Both auditor passes FAIL, mostly on text E and F had passed
unchanged. Both ask the Result's condition to be one the agent observes in its own
context: it now reads "or nothing when this session's context opens with a line naming
open resume notes". Applied too: the report's file and sections cite the roadmap skill's
`references/report.md` by its path in this repository, `audit.py` refusing a skill-local
path to another skill's file; step 3, "Let running work end", cut, answering no failure,
its open questions already in the resume point's template; "unless the user said not
to" cut from the commit; the Taken Up mark gains its check, `git diff` or a reading when
git does not track the folder; `/close-session TEXT` follows the resume point's
definition. Not cut: "The session's state never goes there", which the second pass took
for answering no failure: the three runs without the skill of the case with every task
ticked wrote `config/local.toml`'s state to the agent's memory, now quoted under that
case's `failures_without_skill`. Iterations 8 and 9 ungraded, their version gone. Two
auditor passes on this version before any further run.

Both FAIL on the Result's condition alone, a fact about a start line without a source,
one also on "notes folder" in `references/resume-note.md` for a folder that is not the
resume notes'. The condition takes the first pass's own words, "a line at the top of
this session's context names open resume notes", and the reference says "the resume
notes' folder" and "a folder the repository already keeps for other notes". Two passes
again: both FAIL on that line alone, asking for its source, by a path without the line's
form, one naming a decision record as enough. The Result now cites
`docs/decisions/2026-10-13-session-close.md`, which says the hook names the notes not
taken up: a path under `hooks/` would name the mechanism iteration 7 saw promised.

Two passes again: both `VERDICT: PASS`, the second naming the failure each prohibition
answers. The eval proof on this version: iteration 10, the three cases, nine runs, and
iteration 11, the case outside a roadmap, three runs on the same snapshot, $1.56
announced, $6 at most. The plan's session limit stopped them ("You've hit your session
limit · resets 1am (Europe/Paris)"): in iteration 10, three runs complete, two of the
step stopped midway and one of the phase with every task ticked, one stopped, five not
started; in iteration 11, all three stopped. $0.73 spent. Every auditor pass since the
user's decision cost about $0.11; fourteen passes in all this session.

The user asked to continue; the limit leaves nothing to run before it resets, so this
entry records where the work stands.

**Where the next session starts:**
1. Task 3, after the plan's limit resets: `run.py .eval-runs/skills/close-session/iteration-10
   --start` restarts its six runs left, $0.79 measured, and `run.py
   .eval-runs/skills/close-session/iteration-11 --start` its three, $0.39; $4.50 at most
   in all. Do not prepare them again: their snapshot is the version the auditor passed,
   committed with this entry.
2. Read the six answers outside a roadmap for a promise of what the next start shows,
   then `grade.py` both iterations, twelve sessions, about $1, $12 at most, and
   `benchmark.py`. All assertions passing, task 3's proof is met: tick it.
3. A run failing: change the wording, then two `skill-auditor` passes before any run,
   since a pass draws other points from the same text, and the evals again; the user
   wants a PASS, never a FAIL answered line by line.
4. Task 4, the trigger evals, as the earlier resume points say; the description now says
   "commits finished work".
- The user's review of iteration 2 stays open: `viewer.py
  .eval-runs/skills/close-session/iteration-2 --previous
  .eval-runs/skills/close-session/iteration-1`, served at http://127.0.0.1:3117/ in this
  session, gone with it.
- Pending under the ignored `.eval-runs/`: iterations 10 and 11, partly run. Iterations
  7 to 9 ungraded, their versions gone.
- Waiting for this roadmap's end: the changes Phase 2's hand-over task lists.

Resumed in a new session. Iterations 10 and 11 restarted on the user's yes, announced at
$1.18 measured, $4.50 at most: the nine runs left cost $1.16, and both iterations are
complete, twelve runs of the version the auditor passed. Read before grading, as the
previous resume point asked: none of the six answers outside a roadmap promises what the
next start shows, all six ending on the words to type. One, iteration 10's run 3, passes
the Result's condition itself on to the user: "Aucune ligne en haut du contexte de cette
session ne nomme de notes de reprise ouvertes, donc je n'en dis pas plus sur ce que le
prochain démarrage affichera." No promise, so the assertion passes, but noise, as
iteration 3's explanation of the hook was: the rule told to the user instead of followed.
One run in six, on a text two auditor passes approved. The user asked to record it as an
observation to monitor, a solution to be sought later, the wording left as it is: it goes
under Problems And Deviations, and Phase 2's two closes read their answer for it. The
grading, twelve `skill-grader` sessions announced at $1.05 measured, $12 at most, waits
for the next session.

The user asked to record the session and to go on with the grading in a new one.

**Where the next session starts:**
1. Task 3, grading iterations 10 and 11: `grade.py` on each lists twelve `skill-grader`
   sessions in all, $1.05 at $0.09 a session measured over 33 gradings of this skill,
   $12 at most at `--budget` $1.00; `--start` after the user's yes, then `benchmark.py`
   on both. All assertions passing, task 3's proof is met — `audit.py` clean and the
   auditor's two PASS already in —: tick it.
2. A run failing: change the wording, then two `skill-auditor` passes before any run,
   and the evals again; the user wants a PASS, never a FAIL answered line by line.
3. Task 4, the trigger evals, as the earlier resume points say.
- To monitor, at the user's request: the Result's condition passed on to the user, seen
  in iteration 10's run 3 (Problems And Deviations); Phase 2's closes read for it.
- The user's review of iteration 2 stays open: `viewer.py
  .eval-runs/skills/close-session/iteration-2 --previous
  .eval-runs/skills/close-session/iteration-1`.
- No question is waiting for the user. Pending under the ignored `.eval-runs/`:
  iterations 10 and 11, complete and ungraded. Nothing is uncommitted after this
  record's commit.
- Waiting for this roadmap's end: the changes Phase 2's hand-over task lists.

### 2026-10-14

Resumed in a new session. Iterations 10 and 11 graded on the user's yes, twelve
`skill-grader` sessions announced at $1.05 measured, $12 at most: $1.14 spent. 106
assertions of 108 pass; `benchmark.py` written for both. Two failures, both in the case
outside a roadmap. Iteration 11's run 1 fails the next-start assertion on "Pour reprendre, il
suffit de dire « reprenons l'estimation du coût de stockage »", where five runs ending on the
same words as "dites par exemple" pass; the grader read "il suffit" as a promise, and its
evidence again takes an undeclared `start_notes` for no start line. Iteration 10's run 3 files
Parquet dropped under Done rather than Decided, the information in the note; that assertion
has passed in 14 of the 15 graded runs.

The agent first proposed one more cycle: words to type naming the resume note when no line
named one at the start, Decided defined in `references/resume-note.md`, the assertion's
premise reworded. Asked by the user whether the fault lay in the validation workflow or in
the tool, the agent found its proposal overstated and the validation the main cause: the
runs have no hook, while the fixture's `[session]` table, with no `start_notes`, tells them a
start line names the open notes, a world the installed domain cannot produce, and the one
case 3 has tested since iteration 2; the phase's proof asks for zero failures, read through
one grading per run, with no step telling a skill defect from a run's variance or a grader's
error; the auditor's verdict changes on the same text; its sourcing rule put this
repository's paths into a skill that runs elsewhere; and failures seen in real sessions do
not count against a prohibition.

The user has met another validation problem in ai-ctl, and sees both repositories working
around the validation's gaps at the expense of the tools being built. At the user's request,
work on this roadmap and on ai-ctl's pauses until the validation tool is updated. The agent
wrote the problems, their evidence, what `close-session` now carries because of the
validation, and directions for the update, in
`notes/design-feedback/2026-10-14-close-session-validation.md`, a new folder of the ignored
`notes/` for feedback on the design of the setup's tools; ai-ctl writes its own note next.

With the user's leave, the agent set the phase ⏸️ Blocked, its `**Blocked By:**` naming the
validation tool's update, in the phase file and the roadmap's README, and in
`docs/roadmap/README.md`'s table. `progress_guard.py` refused the README's lagging block
under ⏸️, a 0/4 phase showing one filled cell, so the block was recomputed by `progress.py`
mid-phase: Phase 1 at 2/4, Phase 2 at 0/7, 7/16 in all. `session_resume.py` names only 🟡
phases, so the next session's start no longer names this one.

**Where the next session starts:**
1. The validation tool's update, outside this roadmap: read
   `notes/design-feedback/2026-10-14-close-session-validation.md` and ai-ctl's note once
   written, then decide with the user what changes in `authoring-skills` and its agents,
   and where that work is tracked.
2. Back in this phase once the tool is updated: review the lines of `close-session` the
   note lists as carried for the validation, rework case 3's world to one the installed
   domain can produce, and settle task 3's proof by the new criterion; then task 4, the
   trigger evals.
- Question for the user: where the validation tool's update is tracked, a roadmap of its
  own or a phase of an existing one.
- Pending under the ignored `.eval-runs/`: iterations 10 and 11, graded. Task 3 stays open;
  its two failures are read above and not reworked.
- To monitor, at the user's request: the Result's condition passed on to the user (Problems
  And Deviations).
- Waiting for this roadmap's end: the changes Phase 2's hand-over task lists, among them
  ai-ctl's note on per-case estimates; the validation tool's update now comes first.

The user answered the question left above: the validation tool's update is tracked in a
roadmap of its own, `skill-validation`, created the same day in `pending/` with five
phases — Framing, Run World, Judgments, Evidence And Sources, Validation And Release —,
first in `docs/roadmap/README.md`'s Up Next. Its scope is V1 to V6 of this phase's note
and R1 to R6 of ai-ctl's, `notes/design-feedback/2026-10-14-reviewing-delivered-code-validation.md`;
V7 stays with Phase 2's hand-over task, which gains `workspace.py --extend` taking
`--case`. This phase's `**Blocked By:**`, in the phase file and the roadmap's README, now
names roadmap `skill-validation`.

**Where the next session starts:**
1. Roadmap `skill-validation`, its Phase 0, outside this roadmap.
2. Back in this phase once that roadmap's Phase 4 hands over: as the previous resume
   point's second step says, with the lines to revert that its hand-over note lists.
- No question is waiting for the user.
- Pending under the ignored `.eval-runs/`: iterations 10 and 11, graded.
- To monitor, at the user's request: the Result's condition passed on to the user (Problems
  And Deviations).
- Waiting for this roadmap's end: the changes Phase 2's hand-over task lists.

### 2026-10-15

Roadmap `skill-validation` released `skill-tooling` 0.1.2 and handed over in
`notes/design-feedback/2026-10-15-skill-validation-hand-over.md`: this phase resumes under
the default regime of `docs/decisions/2026-10-15-validation-weight.md`, `close-session`
installed as it stands, the lines the validation added reverted as fixes from use. The
user lifted the ⏸️; the phase is 🟡 again, `**Blocked By:**` cleared here and in the
README, whose progress block shows 🟡.

**Where the next session starts:** the hand-over note, then tasks 3 and 4 under the
default regime.

Resumed in a new session. Task 3 ticked on the user's yes, its proof reworded to the
default regime: the skill beat its baseline clearly, 100% against 57% at iteration 2;
iterations 10 and 11 pass 106 assertions of 108, their two failures classed, a grader's
reading and a run's variance, without risk; `audit.py` clean today; `skill-auditor` PASS
and PASS at `65ca91f` in roadmap `skill-validation`'s Phase 2, `SKILL.md` unchanged since
and only the shared copy `references/conventions.md` cut down at `e2b545f`, so no new
pass. The two failures go to the release's changelog and the skill's watch points, in
Phase 2.

Task 4. Twenty trigger queries in `evals.json`, the users' words as written in
`study/session-close/close-requests.json`: ten close requests (59, 50, 104, 77, 56, 31,
88, 102, 38, 41: steps done and stopped midway, a phase closed, two studies) and ten near
misses (16 and 85, a phase or a roadmap to close; 6, 35, 58, 96 and 76, a fact to record;
78, 40 and 99, a new session's first message, two pasting the previous close's answer).
`triggers.py` lists 60 sessions, three per query, $3.06 estimated from other skills'
measures, $30 at most at its $0.50 ceiling a session.

On the user's yes, with the agent's proposal to read the rates over every query and split
only for a tuning: the 60 sessions cost $3.64. Pooled, the close requests trigger in 27
sessions of 30, 0.90, and the near misses in 3 of 30, 0.10: the design's two rates are
met, each at its limit; per query, 18 of 20 pass at `triggers.py`'s 0.5. Two failures,
in all three sessions each. Request 102, a phase to close and the session to record,
loads the roadmap skill first and reads `close-phase.md`, as the design wants, the
closure being the roadmap skill's; the measure stops at the third call, before any later
use of `close-session` could show: classed a limit of the measure, without risk. Request
78, "peut on commencer une nouvelle session", a session's first message, triggers at the
first call: in its real session the roadmap hook's line named the open phase and the
agent took it up, a start the trigger sessions do not get; classed a description gap,
its risk low, the skill staging only the files the session wrote. No tuning, by the
default regime's stop rule: both join the watch points. Task 4 done.

The user asked to record the session and to go on in a new one, before answering the
agent's proposal to close the phase.

**Where the next session starts:**
1. Phase 1's closure, by the roadmap skill's `close-phase.md`, once the user says so:
   every task is ticked and `make check` passes.
2. Phase 2, which the closure opens: its first task installs the domain, first under
   `CLAUDE_DIR=$(mktemp -d)`, then on `~/.claude` with the user's go-ahead.
- Question for the user: whether to close Phase 1 now.
- Nothing uncommitted after this record's commit. Under the ignored `.eval-runs/`: the
  trigger eval, `skills/close-session/triggers/2026-10-15T153759Z.json`.
- To monitor in Phase 2: the failures tasks 3 and 4 left and the Result's condition passed
  on to the user, all in its `[review]` task's watch points.

---

## Decisions

- **The SessionStart hook names each resume note not taken up, latest first, three at
  most**, as the approved design says. The user, on 2026-10-13, over naming the latest note
  only, with or without a count of the others: two strands of work can be open at once in
  one repository, and the agent then matches the request to the right note from the line.
  The cost to watch is noise, which Phase 2 measures before the release, with the two
  thresholds the user approved: a note named at five starts without being read, or more
  than half the starts with a line reading none of the notes it named.
- **A note is taken up by the session that takes it up**, whatever that session then does:
  its close sets the note's `**Taken up:**`, to its date and the new note's name, or to its
  date and `finished`. The user, on 2026-10-13, against the agent's proposal to mark it only
  when the session did what the note's resume point asked: a user who changes their mind
  on the way forward would leave the note open forever. A note the line named and the
  session did not read stays open, and a session cut before its close leaves the note it
  read open, as the design says. The skill and its eval case outside a roadmap carry it.
- **`[session]` needs `notes` only; `language` is optional.** The agent's choice, task 1:
  the design's own example table holds `notes` alone, and would be invalid in a repository
  whose file declares no shared `language`, the hook then naming nothing. Without it, the
  `# not declared` line names `language`, and the close writes the note's prose in the
  conversation's language.
- **`start_notes` sets how many notes the SessionStart line names, 3 when not declared,
  `0` turning the hook off.** The user, on 2026-10-13, who proposed a key to turn the hook
  off and one for the count; one key, on the agent's advice, so that no two values
  contradict. It is also the first lever if Phase 2's measure finds the line too noisy in
  a repository.
- **Inside a roadmap, the close records in the phase report only; the agent's memory
  takes what still holds once the work in progress is done.** The user, on 2026-10-13,
  after the agent wrote "finish this roadmap first" to its memory at this session's close
  and deleted it: the design's "a preference or a rule the user gave" let a request
  through that holds only until the roadmap ends. The skill states the test, and task 3's
  case of a step stopped midway checks it; the user keeps the example for writing the
  setup's other tools.
- **Task 3's proof needs `skill-auditor`'s `VERDICT: PASS`; a FAIL whose lines are all
  fixed or answered does not count.** The user, on 2026-10-13, against the agent's
  proposal after two passes raised different points on the same text: as many runs as
  needed to find the wording that passes the auditor and keeps the evals passing.
- **This phase pauses until the validation tool is updated.** The user, on 2026-10-14, after
  iterations 10 and 11: the validation's gaps, seen here and in ai-ctl, are being worked
  around at the expense of the tools under construction. Task 3's proof is settled by the
  updated tool's criterion, and the lines of `close-session` written for the validation are
  reviewed then (`notes/design-feedback/2026-10-14-close-session-validation.md`).
- **Task 3's proof follows the default regime of
  `docs/decisions/2026-10-15-validation-weight.md`**: the skill beating its baseline
  clearly, each failure left classed and without risk, `audit.py` clean, `skill-auditor`
  PASS. The user, on 2026-10-15, ticking task 3 on iterations 2, 10 and 11 and roadmap
  `skill-validation`'s two PASS. It replaces the requirement that every assertion pass;
  the failures left go to the release's changelog and the skill's watch points.
- **Task 4's rates are read pooled over all twenty queries, with no held-out split.** The
  agent's proposal, on the user's yes of 2026-10-15: the split keeps a tuned description
  from fitting its test queries, and an untuned description meets every query for the
  first time. A tuning, should real use call for one, splits them first.

---

## Files Changed

---

## Problems And Deviations

- **The copy of `shared/conventions/` in `skills/close-session/` is not checked yet.**
  `tools/shared.py` finds a skill by its `SKILL.md`, which task 3 writes: until then,
  `make check` does not compare the copy with its source, and `make shared` does not
  refresh it. A change to `shared/conventions/` before task 3 is copied by hand. Closed
  with task 3's `SKILL.md`: `tools/shared.py --check` now covers the copy, and
  `make check` passes.
- **The fixture's commits carried the build's time.** The report of each case names its
  start commit, so the case's digest changed at every build and `workspace.py --reuse`
  could never take a baseline's runs; iteration 4 ran its baseline again. Fixed:
  `fixtures.py` dates every commit 2026-10-10T18:00:00+02:00, a test building each case
  under two clocks guards it.
- **A close's answer may pass the Result's condition on to the user.** In iteration 10,
  one run in six outside a roadmap said that no line at the top of its context named open
  resume notes, "donc je n'en dis pas plus sur ce que le prochain démarrage affichera":
  not the promise the assertion guards, but the rule spoken instead of followed, the
  noise iteration 3 saw with the hook explained. Left open at the user's request on
  2026-10-13, the wording unchanged: monitored in Phase 2's closes, a solution to be
  sought from what they show.
- **Task 3's proof unmet, and the validation in question.** Iterations 10 and 11 pass 106
  assertions of 108, on a version two auditor passes approved; the two failures read as a
  grader's reading and a run's variance, not as defects of the skill. Case 3 sets a world the
  installed domain cannot produce, and the eight rewordings of the Result since iteration 3
  answered it. Left open: the phase pauses for the validation tool's update, at the user's
  request on 2026-10-14 (Decisions). Settled on 2026-10-15 under the default regime: task 3
  ticked, the two failures classed and moved to Phase 2's release and watch points.
- **Task 4 measured without the held-out split the design named**, and two of its twenty
  queries failing: request 102 opening with the roadmap skill, a limit of the measure, and
  request 78, a session's first message, triggering, a description gap of low risk. The
  rates met, no tuning; both moved to Phase 2's release and watch points (Decisions).

---

## Changes To Later Phases

- `phase-2-adoption-and-release.md`: a task added under Adoption, at the user's request on
  2026-10-13 — measure the SessionStart line's noise from the transcripts of the sessions
  started since the install, too noisy when a note is named at five starts without being
  read, or when more than half the starts with a line read none of the notes it named; a
  rule then goes to the user before the release. 5 tasks to 6; the README's block and table
  follow.
- `phase-2-adoption-and-release.md`: a task added under Release, after the user asked on
  2026-10-13 whether the changes waiting for this roadmap's end would be forgotten once its
  reports are frozen — hand them over, each to the roadmap that owns its tool or to a new
  one, as the user decides: the eval scripts' cost announcements, a limit with the source
  of its figure when no session of the skill is measured, with ai-ctl's proposal
  `notes/2026-10-13-run-estimate-per-case.md`, received the same day, and the tool review's
  count of SessionStart hooks. 6 tasks to 7; the README's block and table follow at this
  phase's closure.
- `phase-2-adoption-and-release.md`: the hand-over task gains `workspace.py --reuse`
  naming why it takes no run, after it took none on 2026-10-13 without a word, the
  fixture's digest having changed. Its count does not change.
- `phase-2-adoption-and-release.md`: the proofs of the two Adoption tasks that close a
  session, inside a roadmap and outside one, gain a reading of the close's answer for a
  sentence on what the next start will or will not show, the noise this phase left to
  monitor at the user's request on 2026-10-13 (Problems And Deviations). The counts do
  not change.
- `phase-2-adoption-and-release.md`: the hand-over task gains `workspace.py --extend`
  taking `--case`, on 2026-10-14, left out of roadmap `skill-validation`'s scope with the
  rest of the note's V7. Its count does not change.
- `phase-2-adoption-and-release.md`, on 2026-10-15: the `[review]` task gains
  `close-session`'s watch points — the failures tasks 3 and 4 left, and the Result's
  condition passed on to the user —, and the release task's changelog entry names the
  failures left with their class, as the default regime asks. The counts do not change.

---

## Assessment
