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


if __name__ == "__main__":
    unittest.main()
