"""Tests for the usage reader: the tokens and cost of sessions, counted from their transcripts."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "usage.py"
_spec = importlib.util.spec_from_file_location("usage", SCRIPT)
usage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(usage)


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

    def test_every_model_of_the_table_is_priced_by_hand(self):
        # One usage for all: 1,000 input, 2,000 output, 50,000 cache reads, 3,000 five-minute and
        # 4,000 one-hour writes, a prompt of 58,000 tokens. Writes at 1.25 and 2 times the input
        # price, so the call costs 12,750 × input + 2,000 × output + 50,000 × cache read.
        by_hand = {
            "claude-fable-5-1": 0.24,      # 12,750 × $10 + 2,000 × $50 + 50,000 × $0.25
            "claude-mythos-5-1": 0.24,     # as Claude Fable 5.1
            "claude-fable-5": 0.2775,      # 12,750 × $10 + 2,000 × $50 + 50,000 × $1
            "claude-opus-5-5": 0.101,      # 12,750 × $4 + 2,000 × $20 + 50,000 × $0.20
            "claude-opus-5": 0.13875,      # 12,750 × $5 + 2,000 × $25 + 50,000 × $0.50
            "claude-opus-4-8": 0.13875,    # as Claude Opus 5
            "claude-opus-4-7": 0.13875,
            "claude-opus-4-6": 0.13875,
            "claude-sonnet-5-5": 0.0555,   # 12,750 × $2 + 2,000 × $10 + 50,000 × $0.20
            "claude-sonnet-5": 0.0555,
            "claude-sonnet-4-6": 0.08325,  # 12,750 × $3 + 2,000 × $15 + 50,000 × $0.30
            "claude-haiku-5-5": 0.002775,  # 12,750 × $0.10 + 2,000 × $0.50 + 50,000 × $0.01
            "claude-haiku-4-5": 0.02775,   # 12,750 × $1 + 2,000 × $5 + 50,000 × $0.10
        }
        self.assertEqual(sorted(usage.PRICES), sorted(by_hand))
        path = self.transcript(*(assistant(f"msg_{model}", model=model, input_tokens=1000, output=2000, read=50_000,
                                           write_5m=3000, write_1h=4000) for model in by_hand))
        for call in usage.calls(path):
            with self.subTest(model=call.model):
                self.assertAlmostEqual(usage.cost(call), by_hand[call.model])

    def test_each_price_carries_its_source_and_the_date_it_was_read(self):
        for model, price in usage.PRICES.items():
            with self.subTest(model=model):
                self.assertIn(price.source, ("published", "fitted"))
                self.assertRegex(price.read, r"^\d{4}-\d{2}-\d{2}$")
                self.assertTrue(price.origin)
        self.assertEqual(usage.PRICES["claude-haiku-5-5"].source, "published")

    def test_a_long_prompt_takes_its_models_long_prompt_rates(self):
        # Claude Haiku 5.5: $0.10 / $0.50, cache reads $0.01, up to 100,000 prompt tokens;
        # $0.50 / $2.50, cache reads $0.05, beyond. The prompt adds input, cache reads and writes.
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
