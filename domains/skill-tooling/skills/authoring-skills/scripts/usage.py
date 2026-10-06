#!/usr/bin/env python3
"""Count the tokens and cost of agent sessions from their Claude Code transcripts.

Usage: usage.py <transcript.jsonl> ...  — prints the count of the transcripts as JSON.

calls(path) returns one Call per assistant message id, in the order the ids first appear.
Claude Code writes a message as one record per content block, each repeating the usage,
so the last record of an id is kept. Records of the model "<synthetic>" are Claude Code's
own messages, not API calls, and are left out.

A record that carries a stop_reason holds the message's final usage; one without keeps the
usage written when the message started streaming, as most records of a subagent's
transcript do (seen on 2026-10-05 and 2026-10-06, docs/decisions/2026-10-06-token-costs.md).
Such a call's output is replaced by ESTIMATED_OUTPUT and the call is marked estimated.
Input, cache reads and cache writes stand in every record.

cost(call) prices a call at PRICES, in dollars; None when the table lacks its model, a
price never taken as zero. count(paths) adds the calls of several transcripts, each
message id counted once, the first transcript that holds it keeping it, as a resumed
session copies the history it continues.
"""

import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

# Dollars per million tokens: input, output, cache read. Input and output from the
# claude-api skill of Claude Code 2.1.289; cache reads fitted to cost-state records and to
# the results of claude -p sessions, 2026-10-04 to 2026-10-06. Haiku 4.5's cache read is
# taken as a tenth of its input price, without a record to check it against.
PRICES_READ = "2026-10-06"
PRICES = {
    "claude-opus-5-5": (4.0, 20.0, 0.20),
    "claude-sonnet-5-5": (2.0, 10.0, 0.20),
    "claude-opus-5": (5.0, 25.0, 0.50),
    "claude-sonnet-5": (2.0, 10.0, 0.20),
    "claude-haiku-4-5": (1.0, 5.0, 0.10),
}
# A cache write costs a multiple of the input price by its lifetime: subagents write
# five-minute entries, main sessions one-hour entries.
WRITE_5M = 1.25
WRITE_1H = 2.0
# The output of a call whose final usage the transcript lacks: the mean over Phase 3's
# subagent calls without a final record, from the cost-state records of its five sessions
# (5,371 tokens, measured on 2026-10-06).
ESTIMATED_OUTPUT = 5400
SYNTHETIC = "<synthetic>"
DATED = re.compile(r"-\d{8}$")
KINDS = ("input", "output", "cache_read", "write_5m", "write_1h")


@dataclass
class Call:
    id: str
    model: str
    effort: str | None
    sidechain: bool
    final: bool
    input: int
    output: int
    cache_read: int
    write_5m: int
    write_1h: int

    @property
    def estimated(self):
        return not self.final


@dataclass
class Totals:
    calls: int = 0
    estimated: int = 0
    tokens: dict = field(default_factory=lambda: dict.fromkeys(KINDS, 0))
    cost: float | None = 0.0

    def add(self, call):
        self.calls += 1
        self.estimated += call.estimated
        for kind in KINDS:
            self.tokens[kind] += getattr(call, kind)
        price = cost(call)
        self.cost = None if price is None or self.cost is None else self.cost + price


@dataclass
class Count(Totals):
    models: dict = field(default_factory=dict)
    efforts: Counter = field(default_factory=Counter)

    @property
    def unknown(self):
        return sorted(model for model, totals in self.models.items() if totals.cost is None)

    def add(self, call):
        super().add(call)
        self.models.setdefault(call.model, Totals()).add(call)
        self.efforts[call.effort] += 1


def records(path):
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                yield record


def to_call(record):
    message = record["message"]
    used = message.get("usage") or {}
    written = used.get("cache_creation_input_tokens") or 0
    split = used.get("cache_creation") or {}
    if split:
        write_5m = split.get("ephemeral_5m_input_tokens") or 0
        write_1h = split.get("ephemeral_1h_input_tokens") or 0
    else:  # the lifetime unknown: priced at the dearer one-hour rate
        write_5m, write_1h = 0, written
    final = message.get("stop_reason") is not None
    return Call(id=message["id"], model=message.get("model") or "", effort=record.get("effort"),
                sidechain=bool(record.get("isSidechain")), final=final,
                input=used.get("input_tokens") or 0,
                output=(used.get("output_tokens") or 0) if final else ESTIMATED_OUTPUT,
                cache_read=used.get("cache_read_input_tokens") or 0, write_5m=write_5m, write_1h=write_1h)


def calls(path):
    """One Call per assistant message id of the transcript, its last record kept."""
    last = {}
    for record in records(path):
        message = record.get("message")
        if record.get("type") != "assistant" or not isinstance(message, dict) or not message.get("id"):
            continue
        if message.get("model") == SYNTHETIC:
            continue
        last[message["id"]] = record
    return [to_call(record) for record in last.values()]


def price_of(model):
    return PRICES.get(model) or PRICES.get(DATED.sub("", model))


def cost(call):
    """The call's cost in dollars, or None when the price table lacks its model."""
    price = price_of(call.model)
    if price is None:
        return None
    input_price, output_price, read_price = price
    return (call.input * input_price + call.output * output_price + call.cache_read * read_price
            + call.write_5m * input_price * WRITE_5M + call.write_1h * input_price * WRITE_1H) / 1e6


def count(paths):
    """The Count of every call of the transcripts, each message id once."""
    total, seen = Count(), set()
    for path in paths:
        for call in calls(path):
            if call.id not in seen:
                seen.add(call.id)
                total.add(call)
    return total


def as_json(total):
    def totals(t):
        return {"calls": t.calls, "estimated": t.estimated, "tokens": t.tokens, "cost": t.cost}
    return {**totals(total), "unknown": total.unknown, "prices": PRICES_READ,
            "efforts": {effort or "none": n for effort, n in total.efforts.items()},
            "models": {model: totals(t) for model, t in sorted(total.models.items())}}


def main(argv=None):
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print(__doc__.splitlines()[2], file=sys.stderr)
        return 2
    print(json.dumps(as_json(count(paths)), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
