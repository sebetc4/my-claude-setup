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
"""
PRICES, ESTIMATES = usage.table(tomllib.loads(TABLE))


def assistant(message_id, model="claude-opus-5-5", effort="xhigh", stop="end_turn", sidechain=False, block="text",
              input_tokens=0, output=0, read=0, write_5m=0, write_1h=0):
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
    return record


class Transcripts(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.enterContext(mock.patch.object(usage, "PRICES", PRICES))
        self.enterContext(mock.patch.object(usage, "ESTIMATED_OUTPUT", ESTIMATES["output"]["default"].tokens))

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

    def test_a_message_held_by_two_transcripts_is_counted_once_by_the_first(self):
        first = self.transcript(assistant("msg_1", output=100), name="first.jsonl")
        resumed = self.transcript(assistant("msg_1", output=100), assistant("msg_2", output=7), name="resumed.jsonl")
        total = usage.count([first, resumed])
        self.assertEqual((total.calls, total.tokens["output"]), (2, 107))

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
        self.assertEqual((default.tokens, default.measured, default.origin), (5400, "2026-10-06", "the tests' estimate"))

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
        self.assertIn("default", estimates["output"])


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
        self.assertEqual(printed["efforts"], {"xhigh": 1, "none": 1})
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
