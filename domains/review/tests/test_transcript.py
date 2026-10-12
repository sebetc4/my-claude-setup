"""Tests for transcript.py: which tools of this setup a transcript shows, and what a slice cost."""

import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tool-review" / "scripts"))

import transcript  # noqa: E402
from review_world import MODEL, REPLY, RUN_MODEL, World, iso, priced, run_call, text_dollars  # noqa: E402

usage = transcript.usage


def used(world, **window):
    state = transcript.load_state(world.claude)
    catalog = transcript.load_catalog(world.claude, state)
    return list(transcript.uses(world.transcript, catalog, world.claude, str(world.project), **window))


class Detection(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def other_world(self, **options):
        return World(self.enterContext(tempfile.TemporaryDirectory()), **options)

    def test_our_skill_loaded_by_the_skill_tool(self):
        self.world.load_skill("roadmap")
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_our_skill_typed_as_a_command(self):
        self.world.load_skill("roadmap", typed=True)
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_a_project_skill_of_the_same_name_is_not_ours(self):
        self.world.load_skill("roadmap", base=self.world.project / ".claude" / "skills" / "roadmap")
        self.assertEqual(used(self.world), [])

    def test_a_plugin_skill_is_not_ours(self):
        self.world.load_skill("superpowers:brainstorming",
                              base=self.world.claude / "plugins" / "cache" / "superpowers" / "skills" / "brainstorming")
        self.assertEqual(used(self.world), [])

    def test_quoting_the_base_directory_line_is_not_a_load(self):
        line = f"Base directory for this skill: {self.world.claude / 'skills' / 'roadmap'}"
        self.world.reply({"type": "text", "text": line})
        call = self.world.tool_use("Bash", command="grep Base")
        self.world.result(call, line)
        self.assertEqual(used(self.world), [])

    def test_our_agent(self):
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world), ["agent:roadmap-auditor"])

    def test_an_agent_shadowed_by_a_project_agent_is_not_ours(self):
        agents = self.world.project / ".claude" / "agents"
        agents.mkdir(parents=True)
        (agents / "roadmap-auditor.md").write_text("mine\n", encoding="utf-8")
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world), [])

    def test_our_hooks_with_an_effect_in_order_of_first_use(self):
        self.world.hook("roadmap/session_resume.py")
        self.world.hook("roadmap/progress_guard.py", kind="hook_blocking_error", event="PostToolUse")
        self.assertEqual(used(self.world), ["hook:roadmap/session_resume.py", "hook:roadmap/progress_guard.py"])

    def test_a_hook_that_produced_nothing_did_nothing(self):
        self.world.hook("roadmap/session_resume.py", context="")
        self.assertEqual(used(self.world), [])

    def test_a_tool_missing_from_tools_json_is_ignored(self):
        world = self.other_world(tools={"skills": [], "agents": [], "hooks": []})
        world.load_skill("roadmap")
        self.assertEqual(used(world), [])

    def test_a_tool_this_repository_did_not_install_is_ignored(self):
        world = self.other_world(installed=False)
        world.load_skill("roadmap")
        self.assertEqual(used(world), [])

    def test_tool_review_is_never_a_tool_under_review(self):
        world = self.other_world(tools={"skills": ["tool-review"]})
        world.load_skill("tool-review")
        self.assertEqual(used(world), [])

    def test_uses_within_a_window(self):
        self.world.load_skill("roadmap")
        middle = self.world.clock + timedelta(seconds=30)
        self.world.clock = middle + timedelta(seconds=30)
        self.world.call_agent("roadmap-auditor")
        self.assertEqual(used(self.world, start=middle), ["agent:roadmap-auditor"])
        self.assertEqual(used(self.world, end=middle), ["skill:roadmap"])

    def test_a_half_written_last_line_is_skipped(self):
        self.world.load_skill("roadmap")
        with self.world.transcript.open("a", encoding="utf-8") as handle:
            handle.write('{"type": "user", "isMeta": tr')
        self.assertEqual(used(self.world), ["skill:roadmap"])

    def test_session_start_is_the_first_record(self):
        first = self.world.prompt("hello")
        self.world.load_skill("roadmap")
        self.assertEqual(transcript.session_start(self.world.transcript), transcript.when(first["timestamp"]))

    def test_review_load_is_the_latest_load_of_tool_review(self):
        self.world.load_skill("tool-review")
        second = self.world.load_skill("tool-review")
        self.assertEqual(transcript.review_load(self.world.transcript, self.world.claude),
                         (transcript.when(second["timestamp"]), str(self.world.project)))

    def test_stamp_writes_what_when_reads(self):
        self.assertEqual(transcript.stamp(transcript.when("2026-09-26T21:42:11.395Z")), "2026-09-26T21:42:11.395Z")

    def test_the_repository_of_the_review_domain(self):
        self.assertEqual(transcript.repo_of(transcript.load_state(self.world.claude)), self.world.repo)
        self.assertIsNone(transcript.repo_of({"domains": {}}))


class Measures(unittest.TestCase):
    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def measure(self, ids, start=None, end=None):
        state = transcript.load_state(self.world.claude)
        catalog = transcript.load_catalog(self.world.claude, state)
        end = end or self.world.clock + timedelta(seconds=1)
        return transcript.measure(self.world.transcript, catalog, self.world.claude, start, end, ids)

    def test_usage_is_counted_once_per_message(self):
        self.world.reply({"type": "text", "text": "a"},
                         {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}},
                         fresh=100, cached=1000, output=50)
        measured = self.measure([])
        self.assertEqual(measured["tokens"], {"fresh": 100, "cache_read": 1000, "output": 50})
        self.assertEqual((measured["turns"], measured["tools"]), (1, {"Bash": 1}))

    def test_friction(self):
        call = self.world.tool_use("Bash", command="false")
        self.world.result(call, "exit 1", error=True)
        self.world.prompt("[Request interrupted by user]")
        self.assertEqual(self.measure([])["friction"], {"tool_errors": 1, "interruptions": 1})

    def test_a_skill_s_loads_files_and_scripts(self):
        self.world.load_skill("roadmap")
        skill = self.world.claude / "skills" / "roadmap"
        self.world.tool_use("Read", file_path=str(skill / "references" / "close-phase.md"))
        fine = self.world.tool_use("Bash", command=f"python3 {skill}/scripts/progress.py docs/roadmap")
        self.world.result(fine, "fine")
        broken = self.world.tool_use("Bash", command=f"python3 {skill}/scripts/progress.py --check docs/roadmap")
        self.world.result(broken, "inconsistent", error=True)
        entry = self.measure(["skill:roadmap"])["setup"]["skill:roadmap"]
        self.assertEqual(entry["loads"], 1)
        self.assertGreater(entry["chars"], 0)
        self.assertEqual(entry["files_read"], {"references/close-phase.md": 1})
        self.assertEqual((entry["scripts"], entry["script_errors"]), ({"progress.py": 2}, 1))

    def test_an_agent_s_runs_come_from_its_own_transcript(self):
        self.world.call_agent("roadmap-auditor", fresh=500, cached=2000, seconds=40)
        runs = self.measure(["agent:roadmap-auditor"])["setup"]["agent:roadmap-auditor"]["runs"]
        self.assertEqual(runs, [{"fresh": 500, "cache_read": 2000, "seconds": 40}])

    def test_a_hook_s_effects(self):
        self.world.hook("roadmap/session_resume.py", context="x" * 3912)
        self.world.hook("roadmap/session_resume.py", kind="hook_blocking_error")
        self.world.hook("roadmap/session_resume.py", kind="hook_non_blocking_error", context="")
        entry = self.measure(["hook:roadmap/session_resume.py"])["setup"]["hook:roadmap/session_resume.py"]
        self.assertEqual(entry, {"runs": 1, "injected_chars": 3912, "blocks": 1, "errors": 1})

    def test_a_slice_counts_only_its_own_records(self):
        self.world.reply(fresh=10, cached=0, output=1)
        middle = self.world.clock
        self.world.reply(fresh=20, cached=0, output=1)
        self.assertEqual(self.measure([], start=middle + timedelta(milliseconds=1))["tokens"]["fresh"], 20)
        self.assertEqual(self.measure([], end=middle)["tokens"]["fresh"], 10)

    def test_derived_measures_carry_their_rule(self):
        self.world.reply(fresh=10, cached=90)
        self.world.reply(fresh=10, cached=190)
        derived = self.measure([])["derived"]
        self.assertEqual(derived["context_peak"], {"value": 200, "rule": "largest input of one API call, fresh and cached"})
        self.assertEqual(derived["active_minutes"], {"value": 0, "rule": "wall clock minus every gap over 5 min"})


class Costs(unittest.TestCase):
    """The slice's cost and each tool's own, every figure worked out here at the table's rates."""

    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))

    def measure(self, ids=()):
        state = transcript.load_state(self.world.claude)
        catalog = transcript.load_catalog(self.world.claude, state)
        return transcript.measure(self.world.transcript, catalog, self.world.claude, None,
                                  self.world.clock + timedelta(seconds=1), list(ids))

    def out(self, tokens, model=RUN_MODEL):
        return tokens * usage.price_of(model).rates(0)["output"] / 1e6

    def test_the_slice_costs_by_model_and_effort_main_thread_and_subagents_apart(self):
        self.world.reply()
        self.world.reply(effort="max")
        self.world.call_agent("roadmap-auditor", effort="medium", output=600)
        self.world.call_agent("general-purpose", effort="max", output=700)
        medium, top = (usage.estimate("output", agent, effort).value
                       for agent, effort in (("roadmap-auditor", "medium"), ("general-purpose", "max")))
        runs = {"medium": run_call(medium) + run_call(600), "max": run_call(top) + run_call(700)}
        guessed = {"medium": self.out(medium), "max": self.out(top)}
        self.assertEqual(self.measure()["cost"], {
            "prices": usage.PRICES_READ,
            "dollars": round(4 * REPLY + runs["medium"] + runs["max"], 4),
            "estimated": round(guessed["medium"] + guessed["max"], 4),
            "main": {"calls": 4, "dollars": round(4 * REPLY, 4), "estimated": 0.0,
                     "models": {MODEL: {"xhigh": {"calls": 3, "dollars": round(3 * REPLY, 4)},
                                        "max": {"calls": 1, "dollars": round(REPLY, 4)}}}},
            "subagents": {"calls": 4, "dollars": round(runs["medium"] + runs["max"], 4),
                          "estimated": round(guessed["medium"] + guessed["max"], 4),
                          "models": {RUN_MODEL: {
                              effort: {"calls": 2, "dollars": round(runs[effort], 4),
                                       "estimated": round(guessed[effort], 4)} for effort in ("medium", "max")}}},
        })

    def test_a_model_without_effort_takes_its_figures_directly(self):
        self.world.reply(model="claude-haiku-4-5", effort=None)
        self.world.reply()
        self.world.reply(effort=None)
        haiku = priced("claude-haiku-4-5", input=1, output=50, cache_read=1000, write_1h=99)
        self.assertEqual(self.measure()["cost"]["main"]["models"], {
            "claude-haiku-4-5": {"calls": 1, "dollars": round(haiku, 4)},
            MODEL: {"xhigh": {"calls": 1, "dollars": round(REPLY, 4)}, "none": {"calls": 1, "dollars": round(REPLY, 4)}}})

    def test_a_model_the_table_lacks_is_named_and_its_calls_left_unpriced(self):
        self.world.reply()
        self.world.reply(model="claude-unknown-1", effort=None)
        cost = self.measure()["cost"]
        self.assertEqual(cost["unknown"], {"claude-unknown-1": 1})
        self.assertEqual(cost["main"]["models"]["claude-unknown-1"], {"calls": 1})
        self.assertEqual((cost["main"]["calls"], cost["main"]["dollars"], cost["dollars"]),
                         (2, round(REPLY, 4), round(REPLY, 4)))

    def test_the_token_counts_take_each_call_s_final_usage(self):
        first = {"input_tokens": 1, "cache_creation_input_tokens": 99, "cache_read_input_tokens": 1000,
                 "output_tokens": 2}

        def record(message_id, block, **message):
            return {"type": "assistant", "effort": "xhigh", "message": {
                "id": message_id, "model": MODEL, "role": "assistant", "content": [{"type": block}], **message}}

        # streamed: the first record keeps the stream's first usage, the last the final one
        self.world.add(record("msg_s", "thinking", usage=first))
        self.world.add(record("msg_s", "text", usage={**first, "output_tokens": 50}, stop_reason="end_turn"))
        # interrupted: no record holds the final usage
        self.world.add(record("msg_u", "thinking", usage=first))
        measured = self.measure()
        self.assertEqual(measured["tokens"], {"fresh": 200, "cache_read": 2000, "output": 50})
        self.assertEqual(measured["turns"], 2)
        guess = usage.estimate("output", None, "xhigh").value
        main = measured["cost"]["main"]
        self.assertEqual((main["calls"], main["estimated"]), (2, round(self.out(guess, MODEL), 4)))

    def test_a_compaction_s_call_is_counted_in_the_cost_alone_marked_estimated(self):
        self.world.reply()
        self.world.compact(pre=1200)
        self.world.reply()
        measured = self.measure()
        # its call reads the 1,100 tokens the call before held, and takes the rest of 1,200 as input
        compaction = priced(MODEL, input=100, output=usage.estimate("compaction", MODEL).value, cache_read=1100)
        self.assertEqual((measured["turns"], measured["tokens"]["fresh"]), (2, 200))
        self.assertEqual(measured["cost"]["main"], {
            "calls": 3, "dollars": round(2 * REPLY + compaction, 4), "estimated": round(compaction, 4),
            "models": {MODEL: {"xhigh": {"calls": 3, "dollars": round(2 * REPLY + compaction, 4),
                                         "estimated": round(compaction, 4)}}}})

    def test_each_tool_s_own_cost_comes_from_its_text_or_its_runs(self):
        self.world.hook("roadmap/session_resume.py", context="x" * 2600)
        load = self.world.load_skill("roadmap")
        skill = self.world.claude / "skills" / "roadmap"
        read = self.world.tool_use("Read", file_path=str(skill / "references" / "close-phase.md"))
        self.world.result(read, "r" * 1300)
        script = self.world.tool_use("Bash", command=f"{skill}/scripts/progress.py docs/roadmap")
        self.world.result(script, "p" * 650)
        self.world.call_agent("roadmap-auditor", effort="medium", output=600)
        self.world.call_agent("general-purpose", effort="max")
        self.world.reply()
        derived = self.measure(["skill:roadmap", "hook:roadmap/session_resume.py", "agent:roadmap-auditor"])["derived"]
        cost = derived["tool_cost"]["value"]
        # six calls on the main thread: Skill, Read, Bash, Agent, Agent, the reply
        hook = text_dollars(2600, 6)
        texts = [text_dollars(len(transcript.text_of(load)), 5), text_dollars(1300, 4), text_dollars(650, 3)]
        self.assertEqual(cost["hook:roadmap/session_resume.py"], {"tokens": hook[0], "dollars": round(hook[1], 4)})
        self.assertEqual(cost["skill:roadmap"], {"tokens": sum(tokens for tokens, _ in texts),
                                                 "dollars": round(sum(dollars for _, dollars in texts), 4)})
        guess = usage.estimate("output", "roadmap-auditor", "medium").value
        run = run_call(guess) + run_call(600)
        self.assertEqual(cost["agent:roadmap-auditor"], {
            "calls": 2, "dollars": round(run, 4), "estimated": round(self.out(guess), 4),
            "models": {RUN_MODEL: {"medium": {"calls": 2, "dollars": round(run, 4),
                                              "estimated": round(self.out(guess), 4)}}}})
        self.assertIn(f"{usage.estimate('text').value:g} characters a token", derived["tool_cost"]["rule"])

    def test_a_text_is_read_until_the_next_compaction_and_a_block_s_reason_is_a_text(self):
        self.world.hook("roadmap/session_resume.py", context="x" * 2600)
        self.world.reply()
        self.world.reply()
        self.world.compact(pre=1200)
        self.world.reply()
        self.world.hook("roadmap/session_resume.py", kind="hook_blocking_error", context="b" * 520)
        self.world.reply()
        cost = self.measure(["hook:roadmap/session_resume.py"])["derived"]["tool_cost"]["value"]
        # the two calls and the compaction's hold the first text, the last call the reason
        injected, reason = text_dollars(2600, 3), text_dollars(520, 1)
        self.assertEqual(cost["hook:roadmap/session_resume.py"],
                         {"tokens": injected[0] + reason[0], "dollars": round(injected[1] + reason[1], 4)})


class ReviewTurn(unittest.TestCase):
    """The review's own turn: from its request to the first call after record.py answered."""

    def setUp(self):
        self.world = World(self.enterContext(tempfile.TemporaryDirectory()))
        self.world.reply()
        self.requested = transcript.when(iso(self.world.clock))
        self.world.load_skill("tool-review")
        scripts = self.world.claude / "skills" / "tool-review" / "scripts"
        self.world.result(self.world.tool_use("Bash", command=f"{scripts}/measure.py"), "review: x")
        self.world.result(self.world.tool_use("Bash", command=f"{scripts}/record.py x.draft"),
                          "record: the review was not written", error=True)
        self.world.result(self.world.tool_use("Bash", command=f"{scripts}/record.py x.draft"), "review written")

    def turn(self, closed):
        return transcript.review_turn(self.world.transcript, self.world.claude, self.requested, closed)

    def test_it_runs_to_the_call_after_record_py_answered(self):
        self.world.reply()
        self.world.reply(effort="max")
        self.assertEqual(self.turn(self.world.clock + timedelta(seconds=1)), {
            "calls": 5, "dollars": round(5 * REPLY, 4), "estimated": 0.0,
            "models": {MODEL: {"xhigh": {"calls": 5, "dollars": round(5 * REPLY, 4)}}}})

    def test_it_ends_where_the_turn_closed_when_that_comes_first(self):
        closed = self.world.clock + timedelta(seconds=1)
        self.world.clock = closed
        self.world.reply()
        self.assertEqual(self.turn(closed)["calls"], 4)


if __name__ == "__main__":
    unittest.main()
