"""Tests for the usage reader: the tokens and cost of sessions, counted from their transcripts."""

import contextlib
import importlib.util
import io
import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / "usage.py"
_spec = importlib.util.spec_from_file_location("usage", SCRIPT)
usage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(usage)

# The tests price on this table, never on the shipped one, so that a model added to
# usage.toml or repriced there changes no test.
TABLE = """
[providers.anthropic]
cache_read = { times = 0.1 }
write_5m = { times = 1.25 }
write_1h = { times = 2.0 }
source = "published"
read = "2026-10-12"
origin = "the tests' provider"

[models]
claude-opus-5-5 = { provider = "anthropic", input = 4.0, output = 20.0, cache_read = 0.20 }
claude-sonnet-5-5 = { provider = "anthropic", input = 2.0, output = 10.0 }
claude-haiku-4-5 = { provider = "anthropic", input = 1.0, output = 5.0 }
claude-haiku-5-5 = { provider = "anthropic", input = 0.10, output = 0.50, tiers = [{ above = 100_000, input = 0.50, output = 2.50 }] }
gpt-test = { input = 1.25, output = 10.0, cache_read = 0.125, ids = ["openai/gpt-test"], source = "fitted", read = "2026-10-01", origin = "a provider without cache writes" }

[estimates.output]
default = { tokens = 5400, measured = "2026-10-06", origin = "the tests' estimate" }
roadmap-auditor.medium = { tokens = 350, measured = "2026-10-12", origin = "the tests' measure at medium" }
roadmap-auditor.max = { tokens = 2300, measured = "2026-10-12", origin = "the tests' measure at max" }
pdf-reviewer = { tokens = 900, measured = "2026-10-12", origin = "one figure at any effort" }

[estimates.compaction]
default = { tokens = 8000, measured = "2026-10-12", origin = "the tests' compaction" }

[estimates.text]
default = { characters = 2.5, measured = "2026-10-12", origin = "the tests' characters a token" }
"""
PRICES, ESTIMATES = usage.table(tomllib.loads(TABLE))


def at(clock):
    return f"2026-10-12T{clock}.000Z"


def assistant(message_id, model="claude-opus-5-5", effort="xhigh", stop="end_turn", sidechain=False, block="text",
              input_tokens=0, output=0, read=0, write_5m=0, write_1h=0, time=None):
    """One assistant record as Claude Code writes it: one per content block, each repeating the usage."""
    record = {
        "type": "assistant", "isSidechain": sidechain,
        "message": {"id": message_id, "model": model, "role": "assistant", "stop_reason": stop,
                    "content": [{"type": block}],
                    "usage": {"input_tokens": input_tokens, "output_tokens": output,
                              "cache_read_input_tokens": read, "cache_creation_input_tokens": write_5m + write_1h,
                              "cache_creation": {"ephemeral_5m_input_tokens": write_5m,
                                                 "ephemeral_1h_input_tokens": write_1h}}},
    }
    if effort is not None:
        record["effort"] = effort
    if time is not None:
        record["timestamp"] = at(time)
    return record


def organization(clock, uuid):
    return {"type": "attachment", "timestamp": at(clock),
            "attachment": {"type": "credential_org", "organizationUuid": uuid}}


def agent_result(agent_id, clock, **used):
    """The record that brings a run's answer back to the main thread, with its last call's final usage."""
    return {"type": "user", "timestamp": at(clock),
            "toolUseResult": {"status": "completed", "agentId": agent_id,
                              "usage": assistant("last", **used)["message"]["usage"]}}


def notification(agent_id, tokens, clock):
    """The notification Claude Code queues when a run started in the background ends."""
    return {"type": "queue-operation", "operation": "enqueue", "timestamp": at(clock),
            "content": f"<task-notification>\n<task-id>{agent_id}</task-id>\n<status>completed</status>\n"
                       f"<usage><subagent_tokens>{tokens}</subagent_tokens><tool_uses>3</tool_uses>"
                       f"<duration_ms>42180</duration_ms></usage>\n</task-notification>"}


def compaction(clock, pre, post, duration_ms):
    """A compaction as the probe of 2026-10-12 found it: the boundary, then the summary, no record of its call."""
    return [{"type": "system", "subtype": "compact_boundary", "content": "Conversation compacted",
             "timestamp": at(clock), "uuid": "boundary-1",
             "compactMetadata": {"trigger": "manual", "preTokens": pre, "postTokens": post,
                                 "cumulativeDroppedTokens": pre - post, "durationMs": duration_ms}},
            {"type": "user", "isCompactSummary": True, "isVisibleInTranscriptOnly": True, "timestamp": at(clock),
             "message": {"role": "user", "content": "This session is being continued from a previous conversation."}}]


class Transcripts(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.enterContext(mock.patch.object(usage, "PRICES", PRICES))
        self.enterContext(mock.patch.object(usage, "ESTIMATES", ESTIMATES))
        self.enterContext(mock.patch.object(usage, "ESTIMATED_OUTPUT", ESTIMATES["output"]["default"].value))

    def transcript(self, *records, name="session.jsonl"):
        path = Path(self.folder.name) / name
        path.write_text("".join((r if isinstance(r, str) else json.dumps(r)) + "\n" for r in records),
                        encoding="utf-8")
        return path


class OneUsagePerMessage(Transcripts):
    def test_a_message_written_as_several_records_is_counted_once_from_its_last_record(self):
        path = self.transcript(
            assistant("msg_1", stop=None, block="thinking", input_tokens=3, output=8, read=1000, write_1h=50),
            assistant("msg_1", stop=None, block="text", input_tokens=3, output=8, read=1000, write_1h=50),
            assistant("msg_1", stop="tool_use", block="tool_use", input_tokens=3, output=420, read=1000, write_1h=50),
            {"type": "user", "message": {"role": "user", "content": "result"}},
            assistant("msg_2", input_tokens=1, output=30, read=1100, write_1h=10),
        )
        calls = usage.calls(path)
        self.assertEqual([c.id for c in calls], ["msg_1", "msg_2"])
        self.assertEqual((calls[0].input, calls[0].output, calls[0].cache_read, calls[0].write_1h), (3, 420, 1000, 50))
        total = usage.count([path])
        self.assertEqual(total.calls, 2)
        self.assertEqual(total.tokens, {"input": 4, "output": 450, "cache_read": 2100, "write_5m": 0, "write_1h": 60})

    def test_a_calls_time_is_its_first_records(self):
        path = self.transcript(assistant("msg_1", block="thinking", time="10:00:00"),
                               assistant("msg_1", block="text", time="10:00:05"))
        self.assertEqual(usage.calls(path)[0].time, at("10:00:00"))

    def test_other_records_and_unreadable_lines_are_ignored(self):
        path = self.transcript(
            {"type": "user", "message": {"role": "user", "content": "hello"}},
            "not json",
            {"type": "cost-state", "totalCostUSD": 9.99},
            assistant("msg_1", output=5),
        )
        self.assertEqual([c.id for c in usage.calls(path)], ["msg_1"])

    def test_claude_codes_own_messages_are_not_calls(self):
        path = self.transcript(assistant("msg_1", model="<synthetic>", stop="stop_sequence"), assistant("msg_2", output=5))
        self.assertEqual([c.id for c in usage.calls(path)], ["msg_2"])


class Prices(Transcripts):
    def test_each_model_is_priced_at_its_rates_with_writes_priced_by_their_lifetime(self):
        opus = usage.calls(self.transcript(
            assistant("msg_1", input_tokens=10, output=1000, read=100_000, write_1h=2000)))[0]
        # 10 × $4 + 1,000 × $20 + 100,000 × $0.20 + 2,000 × $8 (one-hour write: twice the input price)
        self.assertAlmostEqual(usage.cost(opus), 0.05604)
        sonnet = usage.calls(self.transcript(
            assistant("msg_2", model="claude-sonnet-5-5", input_tokens=2, output=500, read=40_000, write_5m=4000),
            name="sonnet.jsonl"))[0]
        # 2 × $2 + 500 × $10 + 40,000 × $0.20 + 4,000 × $2.50 (five-minute write: 1.25 times the input price)
        self.assertAlmostEqual(usage.cost(sonnet), 0.023004)

    def test_a_providers_default_applies_unless_the_model_sets_its_own(self):
        path = self.transcript(assistant("msg_1", read=100_000),
                               assistant("msg_2", model="claude-haiku-4-5", read=100_000))
        opus, haiku = usage.calls(path)
        self.assertAlmostEqual(usage.cost(opus), 0.02)    # 100,000 × $0.20, its own rate, not 0.1 × $4
        self.assertAlmostEqual(usage.cost(haiku), 0.01)   # 100,000 × 0.1 × $1, the provider's multiple

    def test_a_kind_of_token_without_a_rate_leaves_the_call_unpriced(self):
        path = self.transcript(
            assistant("msg_1", model="gpt-test", input_tokens=1000, output=100, read=10_000),
            assistant("msg_2", model="gpt-test", input_tokens=1000, write_5m=500))
        priced, written = usage.calls(path)
        self.assertAlmostEqual(usage.cost(priced), 0.0035)  # 1,000 × $1.25 + 100 × $10 + 10,000 × $0.125
        self.assertIsNone(usage.cost(written))               # no rate for a cache write: unpriced, never zero
        self.assertEqual(usage.count([path]).unknown, ["gpt-test"])

    def test_an_alias_takes_its_models_price(self):
        alias = usage.calls(self.transcript(assistant("msg_1", model="openai/gpt-test", input_tokens=1000)))[0]
        self.assertAlmostEqual(usage.cost(alias), 0.00125)

    def test_a_models_source_is_its_own_or_its_providers(self):
        self.assertEqual((PRICES["claude-opus-5-5"].source, PRICES["claude-opus-5-5"].read,
                          PRICES["claude-opus-5-5"].origin), ("published", "2026-10-12", "the tests' provider"))
        self.assertEqual((PRICES["gpt-test"].source, PRICES["gpt-test"].read, PRICES["gpt-test"].origin),
                         ("fitted", "2026-10-01", "a provider without cache writes"))

    def test_a_long_prompt_takes_its_models_long_prompt_rates(self):
        # Claude Haiku 5.5: $0.10 / $0.50 up to 100,000 prompt tokens, $0.50 / $2.50 beyond, each card's
        # cache reads and writes at the provider's multiples of its own input. The prompt adds input,
        # cache reads and writes.
        long = usage.calls(self.transcript(assistant(
            "msg_1", model="claude-haiku-5-5", input_tokens=2000, output=1000, read=150_000, write_1h=10_000)))[0]
        # 2,000 × $0.50 + 1,000 × $2.50 + 150,000 × $0.05 + 10,000 × $1 (one-hour write: twice $0.50)
        self.assertAlmostEqual(usage.cost(long), 0.021)
        at_the_bound = usage.calls(self.transcript(
            assistant("msg_2", model="claude-haiku-5-5", read=100_000), name="bound.jsonl"))[0]
        self.assertAlmostEqual(usage.cost(at_the_bound), 0.001)  # 100,000 × $0.01
        past_it = usage.calls(self.transcript(
            assistant("msg_3", model="claude-haiku-5-5", input_tokens=1, read=100_000), name="past.jsonl"))[0]
        self.assertAlmostEqual(usage.cost(past_it), 0.0050005)  # 1 × $0.50 + 100,000 × $0.05
        opus = usage.calls(self.transcript(
            assistant("msg_4", read=200_000), name="opus.jsonl"))[0]
        self.assertAlmostEqual(usage.cost(opus), 0.04)  # 200,000 × $0.20: one rate card at any length

    def test_a_write_without_its_lifetime_is_priced_at_the_one_hour_rate(self):
        record = assistant("msg_1", write_5m=1000)
        del record["message"]["usage"]["cache_creation"]
        call = usage.calls(self.transcript(record))[0]
        self.assertEqual((call.write_5m, call.write_1h), (0, 1000))
        self.assertAlmostEqual(usage.cost(call), 0.008)

    def test_a_dated_model_id_takes_the_price_of_its_model(self):
        haiku = usage.calls(self.transcript(
            assistant("msg_1", model="claude-haiku-4-5-20251001", input_tokens=2245, output=17)))[0]
        self.assertAlmostEqual(usage.cost(haiku), 0.00233)

    def test_a_model_the_table_lacks_is_unknown_never_zero(self):
        path = self.transcript(assistant("msg_1", output=100),
                               assistant("msg_2", model="claude-future-9", input_tokens=5, output=100))
        future = usage.calls(path)[1]
        self.assertIsNone(usage.cost(future))
        total = usage.count([path])
        self.assertEqual(total.unknown, ["claude-future-9"])
        self.assertIsNone(total.cost)
        self.assertAlmostEqual(total.models["claude-opus-5-5"].cost, 0.002)
        self.assertIsNone(total.models["claude-future-9"].cost)
        self.assertEqual(total.models["claude-future-9"].tokens["output"], 100)

    def test_the_total_cost_adds_each_models_cost(self):
        path = self.transcript(assistant("msg_1", output=1000),
                               assistant("msg_2", model="claude-sonnet-5-5", output=1000))
        self.assertAlmostEqual(usage.count([path]).cost, 0.03)


class Table(unittest.TestCase):
    def broken(self, *edits):
        data = tomllib.loads(TABLE)
        for edit in edits:
            edit(data)
        with self.assertRaises(ValueError) as caught:
            usage.table(data)
        return str(caught.exception)

    def test_a_malformed_entry_is_refused_by_its_place(self):
        opus = lambda data: data["models"]["claude-opus-5-5"]  # noqa: E731
        cases = [
            (lambda d: opus(d).update(cache_raed=0.2), "models.claude-opus-5-5: unknown key cache_raed"),
            (lambda d: opus(d).update(output="20"), "models.claude-opus-5-5.output"),
            (lambda d: opus(d).update(input=-4.0), "models.claude-opus-5-5.input"),
            (lambda d: opus(d).update(input={"times": 2}), "models.claude-opus-5-5.input"),
            (lambda d: opus(d).pop("output"), "models.claude-opus-5-5.output"),
            (lambda d: opus(d).update(source="guessed"), "models.claude-opus-5-5.source"),
            (lambda d: opus(d).update(read="12/10/2026"), "models.claude-opus-5-5.read"),
            (lambda d: d["models"]["gpt-test"].pop("origin"), "models.gpt-test.origin"),
            (lambda d: opus(d).update(provider="anthropik"), "models.claude-opus-5-5.provider"),
            (lambda d: d["models"]["claude-haiku-5-5"]["tiers"].append({"above": 50_000, "input": 1.0, "output": 5.0}),
             "models.claude-haiku-5-5.tiers"),
            (lambda d: d["models"]["claude-sonnet-5-5"].update(ids=["openai/gpt-test"]), "openai/gpt-test"),
            (lambda d: d["models"]["gpt-test"]["ids"].append("claude-opus-5-5"), "claude-opus-5-5"),
            (lambda d: d["providers"]["anthropic"].update(write_5m={"times": "1.25"}), "providers.anthropic.write_5m"),
            (lambda d: d["estimates"]["output"].pop("default"), "estimates.output.default"),
            (lambda d: d["estimates"]["output"]["default"].update(tokens=-1), "estimates.output.default.tokens"),
            (lambda d: d["estimates"]["output"]["roadmap-auditor"]["max"].update(tokens=2.5),
             "estimates.output.roadmap-auditor.max.tokens"),
            (lambda d: d["estimates"]["output"]["default"].update(medium={}), "estimates.output.default: unknown key"),
            (lambda d: d["estimates"].pop("compaction"), "estimates.compaction.default"),
            (lambda d: d["estimates"]["text"]["default"].update(characters=0), "estimates.text.default.characters"),
            (lambda d: d["estimates"].update(input={}), "estimates: unknown estimate input"),
            (lambda d: d.update(model={}), "unknown table model"),
        ]
        for edit, place in cases:
            with self.subTest(place=place):
                self.assertIn(place, self.broken(edit))

    def test_every_problem_is_named_at_once(self):
        message = self.broken(lambda d: d["models"]["claude-opus-5-5"].update(source="guessed"),
                              lambda d: d["models"]["gpt-test"].pop("origin"))
        self.assertIn("models.claude-opus-5-5.source", message)
        self.assertIn("models.gpt-test.origin", message)

    def test_the_estimates_are_read_with_their_measure(self):
        default = ESTIMATES["output"]["default"]
        self.assertEqual((default.value, default.measured, default.origin), (5400, "2026-10-06", "the tests' estimate"))
        self.assertEqual(ESTIMATES["output"]["roadmap-auditor"]["max"].value, 2300)
        self.assertEqual(ESTIMATES["text"]["default"].value, 2.5)

    def test_an_unreadable_table_names_its_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "usage.toml"
            path.write_text("[models\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                usage.load(path)
        self.assertIn(str(path), str(caught.exception))

    def test_the_shipped_table_loads(self):
        prices, estimates = usage.load(usage.TABLE)
        self.assertTrue(prices)
        for kind in ("output", "compaction", "text"):
            self.assertIn("default", estimates[kind])


class Estimates(Transcripts):
    def test_a_runs_output_is_estimated_by_its_agent_type_and_effort(self):
        self.assertEqual(usage.estimate("output", "roadmap-auditor", "medium").value, 350)
        self.assertEqual(usage.estimate("output", "roadmap-auditor", "max").value, 2300)

    def test_an_agent_type_may_hold_one_figure_for_every_effort(self):
        self.assertEqual(usage.estimate("output", "pdf-reviewer", "xhigh").value, 900)

    def test_a_pair_the_table_lacks_takes_the_default(self):
        self.assertEqual(usage.estimate("output", "roadmap-auditor", "high").value, 5400)
        self.assertEqual(usage.estimate("output", "general-purpose", "medium").value, 5400)
        self.assertEqual(usage.estimate("output").value, 5400)

    def test_an_estimate_by_model_takes_the_dated_ids_of_its_model(self):
        self.assertEqual(usage.estimate("text", "claude-opus-5-5-20261001").value, 2.5)


class Effort(Transcripts):
    def test_the_effort_of_each_call_is_recorded(self):
        path = self.transcript(assistant("msg_1", effort="max"), assistant("msg_2", effort="xhigh"),
                               assistant("msg_3", effort="xhigh"), assistant("msg_4", effort=None))
        self.assertEqual([c.effort for c in usage.calls(path)], ["max", "xhigh", "xhigh", None])
        self.assertEqual(usage.count([path]).efforts, {"max": 1, "xhigh": 2, None: 1})

    def test_the_calls_of_each_model_are_counted(self):
        path = self.transcript(assistant("msg_1"), assistant("msg_2", model="claude-sonnet-5-5"), assistant("msg_3"))
        total = usage.count([path])
        self.assertEqual({m: t.calls for m, t in total.models.items()}, {"claude-opus-5-5": 2, "claude-sonnet-5-5": 1})


class SubagentOutput(Transcripts):
    def test_a_message_without_a_final_record_has_its_output_estimated_and_marked(self):
        path = self.transcript(
            assistant("msg_1", model="claude-sonnet-5-5", sidechain=True, stop=None, block="thinking", output=8),
            assistant("msg_1", model="claude-sonnet-5-5", sidechain=True, stop=None, block="tool_use", output=8),
            assistant("msg_2", model="claude-sonnet-5-5", sidechain=True, stop="tool_use", output=214),
            name="agent-a1.jsonl")
        first, second = usage.calls(path)
        self.assertEqual((first.final, first.estimated, first.output), (False, True, usage.ESTIMATED_OUTPUT))
        self.assertEqual((second.final, second.estimated, second.output), (True, False, 214))
        total = usage.count([path])
        self.assertEqual(total.estimated, 1)
        self.assertEqual(total.tokens["output"], usage.ESTIMATED_OUTPUT + 214)
        self.assertEqual(total.models["claude-sonnet-5-5"].estimated, 1)

    def test_a_main_sessions_final_output_is_counted_as_recorded(self):
        path = self.transcript(assistant("msg_1", output=3000), assistant("msg_2", output=12))
        total = usage.count([path])
        self.assertEqual((total.estimated, total.tokens["output"]), (0, 3012))


class Session(Transcripts):
    """A session with its runs, shaped as Claude Code 2.1.296 writes them; every figure computed by hand.

    Main thread on Claude Opus 5.5 ($4 input, $20 output, $0.20 read, $8 one-hour write), at xhigh then
    max; two runs on Claude Sonnet 5.5 ($2, $10, $0.20, $2.50 five-minute write) at medium: A, a
    roadmap-auditor in the foreground, B, a general-purpose run in the background.
    """

    def setUp(self):
        super().setUp()
        sonnet = {"model": "claude-sonnet-5-5", "effort": "medium", "sidechain": True, "stop": None}
        main = [
            organization("09:59:00", "org-1"),
            assistant("m1", time="10:00:00", input_tokens=3, output=500, read=20_000, write_1h=10_000),
            agent_result("A", "10:03:00", input_tokens=2, output=900, read=15_000, write_5m=600),
            assistant("m2", time="10:04:00", input_tokens=2, output=300, read=30_000, write_1h=1_500),
            {"type": "user", "timestamp": at("10:04:01"), "toolUseResult": {"status": "async_launched", "agentId": "B"}},
            notification("B", 14_802, "10:10:00"),
            # past the hour: 31,500 tokens were cached, 10,000 are read
            assistant("m3", effort="max", time="12:00:00", input_tokens=2, output=400, read=10_000, write_1h=22_000),
            organization("12:10:00", "org-2"),
            # eleven minutes later, another organization: 32,000 cached, 8,000 read
            assistant("m4", effort="max", time="12:11:00", input_tokens=2, output=100, read=8_000, write_1h=25_000),
            *compaction("12:31:00", pre=36_000, post=5_000, duration_ms=60_000),
            assistant("m5", time="12:32:00", input_tokens=3, output=200, read=9_000, write_1h=4_000),
        ]
        runs = {
            "A": ({"agentType": "roadmap-auditor", "toolUseId": "toolu_A", "requestShape": "foreground"}, [
                assistant("a1", time="10:01:00", input_tokens=3, output=4, read=12_000, write_5m=2_000, **sonnet),
                assistant("a2", time="10:02:00", input_tokens=2, output=6, read=14_000, write_5m=1_000, **sonnet),
                assistant("a3", time="10:02:30", input_tokens=2, output=8, read=15_000, write_5m=600, **sonnet)]),
            "B": ({"agentType": "general-purpose", "toolUseId": "toolu_B", "requestShape": "background"}, [
                assistant("b1", time="10:05:00", input_tokens=3, output=5, read=10_000, write_5m=3_000, **sonnet),
                assistant("b2", time="10:09:00", input_tokens=2, output=7, read=13_000, write_5m=1_000, **sonnet)]),
        }
        path = self.transcript(*main, name="S.jsonl")
        folder = path.with_suffix("") / "subagents"
        folder.mkdir(parents=True)
        for agent_id, (meta, records) in runs.items():
            (folder / f"agent-{agent_id}.meta.json").write_text(json.dumps(meta), encoding="utf-8")
            (folder / f"agent-{agent_id}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records),
                                                            encoding="utf-8")
        self.session = usage.session(path)
        self.calls = {call.id: call for call in self.session.calls}

    def test_every_run_is_counted_beside_the_main_thread(self):
        self.assertEqual([call.id for call in self.session.main if not call.derived], ["m1", "m2", "m3", "m4", "m5"])
        self.assertEqual([(run.id, run.agent, [c.id for c in run.calls]) for run in self.session.runs],
                         [("A", "roadmap-auditor", ["a1", "a2", "a3"]), ("B", "general-purpose", ["b1", "b2"])])
        self.assertEqual({self.calls[i].agent for i in ("a1", "b1")}, {"roadmap-auditor", "general-purpose"})
        self.assertIsNone(self.calls["m1"].agent)

    def test_a_calls_output_is_estimated_by_its_agent_type_and_effort(self):
        self.assertEqual([(self.calls[i].output, self.calls[i].estimated) for i in ("a1", "a2", "b1")],
                         [(350, True), (350, True), (5400, True)])

    def test_a_runs_last_call_takes_its_output_from_the_agent_result(self):
        self.assertEqual((self.calls["a3"].output, self.calls["a3"].estimated), (900, False))

    def test_a_background_runs_last_output_comes_from_its_notification_marked_estimated(self):
        # 14,802 tokens less the call's 2 input, 13,000 read and 1,000 written
        self.assertEqual((self.calls["b2"].output, self.calls["b2"].estimated), (800, True))

    def test_the_cost_is_given_per_model_and_effort(self):
        total = usage.tally(self.session.calls)
        self.assertEqual(total.tokens, {"input": 3022, "output": 17_300, "cache_read": 174_002,
                                        "write_5m": 7600, "write_1h": 62_500})
        self.assertAlmostEqual(total.cost, 0.8338644)
        self.assertAlmostEqual(total.models["claude-opus-5-5"].cost, 0.7240404)
        self.assertAlmostEqual(total.models["claude-sonnet-5-5"].cost, 0.109824)
        cells = {key: (t.calls, round(t.cost, 7)) for key, t in total.by_effort.items()}
        self.assertEqual(cells, {("claude-opus-5-5", "xhigh"): (3, 0.155832),
                                 ("claude-opus-5-5", "max"): (3, 0.5682084),
                                 ("claude-sonnet-5-5", "medium"): (5, 0.109824)})

    def test_the_estimated_part_is_marked_in_every_total(self):
        total = usage.tally(self.session.calls)
        self.assertEqual(total.estimated, 5)  # a1, a2, b1, b2 and the compaction's call
        # the compaction's whole call, $0.1785924, and the estimated outputs: 350, 350, 5,400 and 800 at $10
        self.assertAlmostEqual(total.estimated_cost, 0.2475924)
        self.assertEqual(total.models["claude-sonnet-5-5"].estimated, 4)
        self.assertAlmostEqual(total.by_effort[("claude-opus-5-5", "max")].estimated_cost, 0.1785924)

    def test_the_main_thread_and_the_runs_are_counted_apart(self):
        self.assertAlmostEqual(usage.tally(self.session.main).cost, 0.7240404)
        self.assertAlmostEqual(usage.tally(c for run in self.session.runs for c in run.calls).cost, 0.109824)

    def test_each_cache_rebuild_has_its_size_cost_and_cause(self):
        # tokens written again over a read of them: $8 less $0.20 a million
        self.assertEqual([(r.call.id, r.tokens, round(r.cost, 7), r.cause, r.run) for r in self.session.rebuilds],
                         [("m3", 21_500, 0.1677, "pause", None), ("m4", 24_000, 0.1872, "organization", None)])

    def test_a_compaction_is_counted_with_its_call_and_the_context_it_leaves(self):
        [compacted] = self.session.compactions
        self.assertEqual((compacted.time, compacted.trigger, compacted.pre_tokens, compacted.post_tokens),
                         (at("12:31:00"), "manual", 36_000, 5_000))
        call = compacted.call
        # read: m4's context, 2 + 8,000 + 25,000; input: the rest of preTokens; output: the estimate
        self.assertEqual((call.model, call.effort, call.input, call.cache_read, call.write_1h, call.output),
                         ("claude-opus-5-5", "max", 2998, 33_002, 0, 8000))
        self.assertTrue(call.derived and call.estimated)
        self.assertAlmostEqual(usage.cost(call), 0.1785924)
        self.assertEqual(compacted.left, 13_003)  # m5: 3 + 9,000 + 4,000
        self.assertEqual([c.id for c in self.session.main][-2:], [call.id, "m5"])


def records_of(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def copied(record, session_id, clock=None):
    """A record as a continued conversation copies it: its own uuid and session id, its time kept unless given."""
    record = dict(record, uuid=f"{session_id}-{record.get('uuid', 'r')}", sessionId=session_id)
    if clock is not None:
        record["timestamp"] = at(clock)
    return record


class Continued(Transcripts):
    """A conversation continued in a new process, as 2.1.294 wrote c3561bb8 and a556427b: the
    continuation copies the history with its times and message ids, under its own uuids and session id,
    its first record earlier than the original's; it copies no run."""

    def setUp(self):
        super().setUp()
        history = [
            assistant("m1", time="08:24:53", input_tokens=3, output=100, read=20_000, write_1h=5_000),
            assistant("m2", block="thinking", time="08:30:00", input_tokens=2, output=200, read=25_000, write_1h=1_000),
            assistant("m2", block="text", time="08:30:04", input_tokens=2, output=200, read=25_000, write_1h=1_000),
        ]
        self.original = self.transcript(
            {"type": "queue-operation", "operation": "enqueue", "timestamp": at("08:24:44")},
            *[copied(r, "A") for r in history],
            assistant("m3", time="09:24:40", input_tokens=2, output=50, read=26_000, write_1h=500),
            name="A.jsonl")
        self.continuation = self.transcript(
            {"type": "attachment", "timestamp": at("08:23:52"), "attachment": {"type": "skill_listing"}},
            *[copied(r, "B") for r in history[:2]],
            copied(history[2], "B", "11:39:18"),  # the text block written again at the resumption
            assistant("m4", time="11:40:00", input_tokens=2, output=70, read=1_000, write_1h=26_000),
            assistant("m5", time="11:41:00", input_tokens=2, output=30, read=27_000, write_1h=100),
            name="B.jsonl")

    def test_a_session_records_when_it_started_and_ended(self):
        self.assertEqual((usage.session(self.original).started, usage.session(self.original).ended),
                         (at("08:24:44"), at("09:24:40")))
        self.assertEqual((usage.session(self.continuation).started, usage.session(self.continuation).ended),
                         (at("08:23:52"), at("11:41:00")))

    def test_the_shared_calls_go_to_the_transcript_that_ends_first_whatever_the_order_given(self):
        for given in ([self.continuation, self.original], [self.original, self.continuation]):
            total = usage.count(given)
            self.assertEqual((total.calls, total.tokens["output"]), (5, 450))
        continued, original = usage.distinct([usage.session(self.continuation), usage.session(self.original)])
        self.assertEqual([c.id for c in original.main], ["m1", "m2", "m3"])
        self.assertEqual([c.id for c in continued.main], ["m4", "m5"])
        self.assertEqual(original.main[1].time, at("08:30:00"))

    def test_a_copy_dated_later_yields_its_calls_to_the_transcript_that_recorded_them_first(self):
        # A teleported transcript, as 348d400d: every record dated at the teleport, its last before the original's
        teleported = self.transcript(*[copied(assistant(message_id, output=100), "T", f"09:00:0{i}")
                                       for i, message_id in enumerate(["m1", "m2"])], name="T.jsonl")
        sessions = usage.distinct([usage.session(teleported), usage.session(self.original)])
        self.assertEqual([[c.id for c in s.main] for s in sessions], [[], ["m1", "m2", "m3"]])
        self.assertEqual([c.time for c in sessions[1].main][:2], [at("08:24:53"), at("08:30:00")])
        self.assertEqual(usage.count([teleported, self.original]).calls, 3)

    def test_a_chain_of_continuations_gives_each_call_to_the_first_that_holds_it(self):
        third = self.transcript(*[copied(r, "C") for r in records_of(self.continuation)],
                                assistant("m6", time="12:00:00", output=10), name="C.jsonl")
        sessions = usage.distinct([usage.session(p) for p in (third, self.continuation, self.original)])
        self.assertEqual([[c.id for c in s.main] for s in sessions], [["m6"], ["m4", "m5"], ["m1", "m2", "m3"]])

    def test_a_copied_compaction_its_call_and_its_rebuilds_are_counted_once(self):
        history = [assistant("m1", time="10:00:00", input_tokens=2, read=20_000, write_1h=5_000),
                   *compaction("10:20:00", pre=26_000, post=4_000, duration_ms=60_000),
                   assistant("m2", time="10:21:00", input_tokens=2, read=4_000, write_1h=10_000),
                   # past the hour: the context written again
                   assistant("m3", time="11:30:00", input_tokens=2, read=1_000, write_1h=14_000)]
        original = self.transcript(*[copied(r, "A") for r in history], name="A2.jsonl")
        continuation = self.transcript(*[copied(r, "B") for r in history],
                                       assistant("m4", time="11:31:00", read=15_000, write_1h=200), name="B2.jsonl")
        kept, copy = usage.distinct([usage.session(original), usage.session(continuation)])
        self.assertEqual([c.id for c in kept.main if not c.derived], ["m1", "m2", "m3"])
        self.assertEqual(([c.call.id for c in kept.rebuilds], len(kept.compactions)), (["m3"], 1))
        self.assertEqual(([c.id for c in copy.main], copy.compactions, copy.rebuilds), (["m4"], [], []))
        self.assertEqual(usage.tally(kept.main + copy.main).estimated, 1)  # the compaction's call, once

    def test_a_sessions_runs_stay_with_it(self):
        folder = self.continuation.with_suffix("") / "subagents"
        folder.mkdir(parents=True)
        (folder / "agent-R.jsonl").write_text(json.dumps(assistant("r1", time="11:40:30", sidechain=True)) + "\n",
                                              encoding="utf-8")
        continued, _ = usage.distinct([usage.session(self.continuation), usage.session(self.original)])
        self.assertEqual([[c.id for c in run.calls] for run in continued.runs], [["r1"]])


class Rebuilds(Transcripts):
    def test_a_compaction_past_the_hour_writes_its_context_again(self):
        path = self.transcript(assistant("m1", time="10:00:00", input_tokens=2, read=20_000, write_1h=5_000),
                               *compaction("11:31:00", pre=26_000, post=4_000, duration_ms=60_000))
        call = usage.session(path).compactions[0].call
        self.assertEqual((call.input, call.cache_read, call.write_1h), (998, 0, 25_002))

    def test_a_change_of_model_rebuilds_and_a_loss_without_a_known_cause_is_said_so(self):
        path = self.transcript(
            assistant("m1", time="10:00:00", read=20_000, write_1h=10_000),
            assistant("m2", model="claude-sonnet-5-5", time="10:01:00", write_1h=30_000),
            assistant("m3", model="claude-sonnet-5-5", time="10:02:00", read=2000, write_1h=30_000),
            assistant("m4", model="claude-sonnet-5-5", time="10:03:00", read=32_000, write_1h=500))
        found = usage.rebuilds(usage.calls(path))
        self.assertEqual([(r.call.id, r.tokens, r.cause) for r in found], [("m2", 30_000, "model"), ("m3", 28_000, "unknown")])

    def test_a_thread_on_five_minute_entries_loses_them_past_five_minutes(self):
        path = self.transcript(
            assistant("s1", time="10:00:00", read=10_000, write_5m=5000),
            assistant("s2", time="10:07:00", read=1000, write_5m=14_000))
        self.assertEqual([(r.tokens, r.cause) for r in usage.rebuilds(usage.calls(path))], [(14_000, "pause")])


class ToolText(Transcripts):
    def test_a_text_is_written_once_and_read_by_every_later_call(self):
        path = self.transcript(assistant("m1"), assistant("m2"), assistant("m3"))
        tokens, cost = usage.text_cost(5000, usage.calls(path))
        self.assertEqual(tokens, 2000)               # 5,000 characters at 2.5 a token
        self.assertAlmostEqual(cost, 0.0168)         # 2,000 × $8, then 2 × 2,000 × $0.20

    def test_a_text_read_by_a_model_the_table_lacks_has_no_cost(self):
        path = self.transcript(assistant("m1"), assistant("m2", model="claude-future-9"))
        self.assertEqual(usage.text_cost(5000, usage.calls(path)), (2000, None))


class CommandLine(Transcripts):
    def test_it_prints_the_count_as_json(self):
        path = self.transcript(assistant("msg_1", output=1000, effort="xhigh"),
                               assistant("msg_2", model="claude-sonnet-5-5", effort=None, sidechain=True, stop=None,
                                         output=3))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(usage.main([str(path)]), 0)
        printed = json.loads(out.getvalue())
        self.assertEqual(printed["calls"], 2)
        self.assertEqual(printed["estimated"], 1)
        self.assertAlmostEqual(printed["estimated_cost"], usage.ESTIMATED_OUTPUT * 10 / 1e6)
        self.assertEqual(printed["efforts"], {"xhigh": 1, "none": 1})
        self.assertEqual(printed["models"]["claude-sonnet-5-5"]["efforts"]["none"]["calls"], 1)
        self.assertAlmostEqual(printed["cost"], 0.02 + usage.ESTIMATED_OUTPUT * 10 / 1e6)
        self.assertEqual(printed["prices"], usage.PRICES_READ)
        self.assertEqual(sorted(printed["models"]), ["claude-opus-5-5", "claude-sonnet-5-5"])
        opus = usage.PRICES["claude-opus-5-5"]
        self.assertEqual(printed["models"]["claude-opus-5-5"]["price"],
                         {"source": opus.source, "read": opus.read, "origin": opus.origin})

    def test_a_model_the_table_lacks_prints_no_price(self):
        path = self.transcript(assistant("msg_1", model="claude-future-9", output=10))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            usage.main([str(path)])
        printed = json.loads(out.getvalue())
        self.assertEqual(printed["unknown"], ["claude-future-9"])
        self.assertIsNone(printed["cost"])
        self.assertIsNone(printed["models"]["claude-future-9"]["price"])


if __name__ == "__main__":
    unittest.main()
