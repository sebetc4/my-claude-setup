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

cost(call) prices a call at PRICES, in dollars; None when the table lacks its model or a
rate for a kind of token the call holds, a price never taken as zero. Each Price carries its
source, published or fitted, the date it was read and where; a model with several rate cards
is priced by the length of the call's prompt. count(paths) adds the calls of several
transcripts, each message id counted once, the first transcript that holds it keeping it, as
a resumed session copies the history it continues.

The prices and the estimates are data, in usage.toml beside this script, so that a model or
a provider is added or repriced by an entry alone; table() reads them and refuses a
malformed entry, every problem named. Only calls() reads Claude Code's transcripts: the
counting and the pricing take any agent's calls.
"""

import json
import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

TABLE = Path(__file__).with_name("usage.toml")
KINDS = ("input", "output", "cache_read", "write_5m", "write_1h")
SOURCES = ("published", "fitted")
SYNTHETIC = "<synthetic>"
DATED = re.compile(r"-\d{8}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROVIDER_KEYS = set(KINDS) | {"source", "read", "origin"}
MODEL_KEYS = PROVIDER_KEYS | {"provider", "tiers", "ids"}
TIER_KEYS = set(KINDS) | {"above"}
ESTIMATE_KEYS = {"tokens", "measured", "origin"}


@dataclass(frozen=True)
class Price:
    """A model's rates in dollars per million tokens, by kind of token, with their source.

    cards holds (above, rates) pairs in ascending order, the first above 0: a call whose prompt,
    input, cache reads and cache writes together, passes a card's bound takes that card's rates.
    source is "published" or "fitted" (to cost-state records); read is the date the price was
    read or fitted, origin where.
    """
    cards: tuple
    source: str
    read: str
    origin: str

    def rates(self, prompt):
        chosen = self.cards[0][1]
        for above, rates in self.cards[1:]:
            if prompt > above:
                chosen = rates
        return chosen


@dataclass(frozen=True)
class Estimate:
    """A figure the transcripts lack, with when and from what it was measured."""
    tokens: int
    measured: str
    origin: str


def amount(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def card(entry, where, problems):
    """{kind: dollars per million} of one rate card: a rate in dollars, or { times = n } of the card's input."""
    rates = {}
    if not amount(entry.get("input")):
        problems.append(f"{where}.input: dollars per million tokens, a number of 0 or more")
    if "output" not in entry:
        problems.append(f"{where}.output: missing")
    for kind in KINDS:
        value = entry.get(kind)
        if value is None:
            continue
        if amount(value):
            rates[kind] = float(value)
        elif kind != "input" and isinstance(value, dict) and set(value) == {"times"} and amount(value["times"]):
            if amount(entry.get("input")):
                rates[kind] = value["times"] * entry["input"]
        elif kind != "input":
            problems.append(f"{where}.{kind}: dollars per million tokens, or {{ times = n }} of the input price")
    return rates


def unknown_keys(entry, allowed, where, problems):
    problems.extend(f"{where}: unknown key {key}" for key in sorted(set(entry) - allowed))


def defaults_of(name, defaults, problems):
    where = f"providers.{name}"
    unknown_keys(defaults, PROVIDER_KEYS, where, problems)
    for kind in set(KINDS) & set(defaults):
        value = defaults[kind]
        times = isinstance(value, dict) and set(value) == {"times"} and amount(value["times"])
        if not (amount(value) or (times and kind != "input")):
            problems.append(f"{where}.{kind}: dollars per million tokens, or {{ times = n }} of the input price")


def price_from(model, entry, providers, problems):
    where = f"models.{model}"
    unknown_keys(entry, MODEL_KEYS, where, problems)
    provider = entry.get("provider")
    if provider is not None and provider not in providers:
        problems.append(f"{where}.provider: no providers.{provider} table")
    defaults = providers.get(provider, {})
    merged = {**defaults, **entry}
    if merged.get("source") not in SOURCES:
        problems.append(f"{where}.source: one of {', '.join(SOURCES)}")
    if not (isinstance(merged.get("read"), str) and DATE.match(merged["read"])):
        problems.append(f"{where}.read: a date, YYYY-MM-DD")
    if not (isinstance(merged.get("origin"), str) and merged["origin"]):
        problems.append(f"{where}.origin: where the price was read or fitted")
    cards = [(0, card(merged, where, problems))]
    tiers = entry.get("tiers", [])
    if not isinstance(tiers, list):
        problems.append(f"{where}.tiers: a list of rate cards")
        tiers = []
    for index, tier in enumerate(tiers):
        place = f"{where}.tiers[{index}]"
        if not isinstance(tier, dict):
            problems.append(f"{place}: a rate card")
            continue
        unknown_keys(tier, TIER_KEYS, place, problems)
        above = tier.get("above")
        if not (isinstance(above, int) and not isinstance(above, bool) and above > cards[-1][0]):
            problems.append(f"{where}.tiers: each card's above a whole number of prompt tokens past the one before")
            continue
        cards.append((above, card({**{k: v for k, v in defaults.items() if k in KINDS}, **tier}, place, problems)))
    return Price(tuple(cards), merged.get("source"), merged.get("read"), merged.get("origin"))


def estimates_from(data, problems):
    estimates = {}
    for kind, entries in data.items():
        if kind != "output" or not isinstance(entries, dict):
            problems.append(f"estimates: unknown estimate {kind}")
            continue
        estimates[kind] = {}
        for name, entry in entries.items():
            where = f"estimates.{kind}.{name}"
            if not isinstance(entry, dict):
                problems.append(f"{where}: a table of tokens, measured and origin")
                continue
            unknown_keys(entry, ESTIMATE_KEYS, where, problems)
            tokens = entry.get("tokens")
            if not (isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0):
                problems.append(f"{where}.tokens: a whole number of 0 or more")
            if not (isinstance(entry.get("measured"), str) and DATE.match(entry["measured"])):
                problems.append(f"{where}.measured: a date, YYYY-MM-DD")
            if not (isinstance(entry.get("origin"), str) and entry["origin"]):
                problems.append(f"{where}.origin: what the figure was measured from")
            estimates[kind][name] = Estimate(tokens, entry.get("measured"), entry.get("origin"))
        if "default" not in entries:
            problems.append(f"estimates.{kind}.default: missing, the figure for an agent type the table lacks")
    if "output" not in data:
        problems.append("estimates.output.default: missing, the figure for an agent type the table lacks")
    return estimates


def table(data):
    """({model id or alias: Price}, {kind: {agent type: Estimate}}) from a parsed usage.toml.

    A model's entry takes its provider's defaults, rates and source, for every key it does not
    set; a rate card past a prompt length takes the provider's rates, multiples of its own
    input. Raises ValueError naming every problem, each by its place in the table.
    """
    problems = []
    unknown_keys(data, {"providers", "models", "estimates"}, "the table", problems)
    problems[:] = [problem.replace("the table: unknown key", "unknown table") for problem in problems]
    providers = data.get("providers", {})
    for name, defaults in providers.items():
        defaults_of(name, defaults, problems)
    models = data.get("models", {})
    prices = {model: price_from(model, entry, providers, problems) for model, entry in models.items()}
    for model, entry in models.items():
        ids = entry.get("ids", [])
        if not (isinstance(ids, list) and all(isinstance(alias, str) for alias in ids)):
            problems.append(f"models.{model}.ids: a list of model ids")
            continue
        for alias in ids:
            if alias in prices:
                problems.append(f"models.{model}.ids: {alias} names another model already")
            else:
                prices[alias] = prices[model]
    estimates = estimates_from(data.get("estimates", {}), problems)
    if problems:
        raise ValueError("\n".join(problems))
    return prices, estimates


def load(path=TABLE):
    """The prices and estimates of the table file at path; ValueError naming the file and every problem."""
    try:
        with open(path, "rb") as handle:
            data = tomllib.load(handle)
        return table(data)
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        raise ValueError(f"{path}: {error}") from None


PRICES, ESTIMATES = load()
PRICES_READ = max(price.read for price in PRICES.values())
# The output of a call whose final usage the transcript lacks.
ESTIMATED_OUTPUT = ESTIMATES["output"]["default"].tokens


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
    """The call's cost in dollars, or None when the price table lacks its model or a rate the call needs."""
    price = price_of(call.model)
    if price is None:
        return None
    rates = price.rates(call.input + call.cache_read + call.write_5m + call.write_1h)
    held = [kind for kind in KINDS if getattr(call, kind)]
    if any(kind not in rates for kind in held):
        return None
    return sum(getattr(call, kind) * rates[kind] for kind in held) / 1e6


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

    def source(model):
        price = price_of(model)
        return price and {"source": price.source, "read": price.read, "origin": price.origin}
    return {**totals(total), "unknown": total.unknown, "prices": PRICES_READ,
            "efforts": {effort or "none": n for effort, n in total.efforts.items()},
            "models": {model: {**totals(t), "price": source(model)} for model, t in sorted(total.models.items())}}


def main(argv=None):
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print(__doc__.splitlines()[2], file=sys.stderr)
        return 2
    print(json.dumps(as_json(count(paths)), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
