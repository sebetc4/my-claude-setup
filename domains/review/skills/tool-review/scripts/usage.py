#!/usr/bin/env python3
"""Count the tokens and cost of agent sessions from their Claude Code transcripts.

Usage: usage.py <transcript.jsonl> ...  — prints the count of the transcripts as JSON.

calls(path) returns one Call per assistant message id, in the order the ids first appear.
Claude Code writes a message as one record per content block, each repeating the usage,
so the last record of an id is kept, its first giving the call's time. Records of the model
"<synthetic>" are Claude Code's own messages, not API calls, and are left out.

A record that carries a stop_reason holds the message's final usage; one without keeps the
usage written when the message started streaming, as most records of a subagent's
transcript do (seen on 2026-10-05 and 2026-10-06, docs/decisions/2026-10-06-token-costs.md).
Such a call's output is replaced by the estimate for its agent type and effort, and the call
is marked estimated. Input, cache reads and cache writes stand in every record.

session(path) reads a main transcript with its runs under <session>/subagents/: a run's
last call takes its final output from the Agent result, or, for a run in the background,
from its notification, still estimated; each compaction's call, which no transcript holds,
is derived and marked; rebuilds() finds the calls that write the cache again, with their
cause. text_cost() prices a text the agent was given, by its characters.

cost(call) prices a call at PRICES, in dollars; None when the table lacks its model or a
rate for a kind of token the call holds, a price never taken as zero. Each Price carries its
source, published or fitted, the date it was read and where; a model with several rate cards
is priced by the length of the call's prompt. tally(calls) adds calls by model and effort,
with the part resting on estimates. A conversation continued in a new process copies the
history it continues, message ids and times kept; distinct(sessions) and count(paths) count
each message id once, by the transcript whose record of it comes first, at equal times the one
whose last record comes first.

The prices and the estimates are data, in usage.toml beside this script, so that a model or
a provider is added or repriced by an entry alone; table() reads them and refuses a
malformed entry, every problem named. Only calls() and session() read Claude Code's
transcripts: the counting and the pricing take any agent's calls.
"""

import json
import math
import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import datetime
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
# What each kind of estimate gives: the output of a call, or the characters of a token.
ESTIMATE_FIELDS = {"output": "tokens", "compaction": "tokens", "text": "characters"}


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
    """A figure the transcripts lack, output tokens or characters a token, with when and from what it was measured."""
    value: float
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


def estimate_from(entry, field, where, problems):
    if not isinstance(entry, dict):
        problems.append(f"{where}: a table of {field}, measured and origin")
        return None
    unknown_keys(entry, {field, "measured", "origin"}, where, problems)
    value = entry.get(field)
    if field == "tokens" and not (isinstance(value, int) and not isinstance(value, bool) and value >= 0):
        problems.append(f"{where}.tokens: a whole number of 0 or more")
    elif field == "characters" and not (amount(value) and value > 0):
        problems.append(f"{where}.characters: the characters of a token, a number above 0")
    if not (isinstance(entry.get("measured"), str) and DATE.match(entry["measured"])):
        problems.append(f"{where}.measured: a date, YYYY-MM-DD")
    if not (isinstance(entry.get("origin"), str) and entry["origin"]):
        problems.append(f"{where}.origin: what the figure was measured from")
    return Estimate(value, entry.get("measured"), entry.get("origin"))


def estimates_from(data, problems):
    """{kind: {name: Estimate, or {effort: Estimate}}}; each kind's default is a single Estimate."""
    estimates = {}
    for kind, entries in data.items():
        field = ESTIMATE_FIELDS.get(kind)
        if field is None or not isinstance(entries, dict):
            problems.append(f"estimates: unknown estimate {kind}")
            continue
        estimates[kind] = {}
        for name, entry in entries.items():
            where = f"estimates.{kind}.{name}"
            if name == "default" or not isinstance(entry, dict) or field in entry:
                estimates[kind][name] = estimate_from(entry, field, where, problems)
            else:  # one estimate per effort
                estimates[kind][name] = {effort: estimate_from(level, field, f"{where}.{effort}", problems)
                                         for effort, level in entry.items()}
    for kind in ESTIMATE_FIELDS:
        if "default" not in data.get(kind, {}):
            problems.append(f"estimates.{kind}.default: missing, the figure for what the table lacks")
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
# The output of a call whose final usage the transcript lacks, for an agent type and effort the table lacks.
ESTIMATED_OUTPUT = ESTIMATES["output"]["default"].value
# How long a cache entry lives, in seconds, by the kind of write that made it.
LIFETIMES = {"write_5m": 300, "write_1h": 3600}
NOTIFIED = re.compile(r"<task-id>([^<]+)</task-id>.*?<subagent_tokens>(\d+)</subagent_tokens>", re.S)


def estimate(kind, key=None, effort=None):
    """The Estimate of kind for key, an agent type or a model id, at effort; the kind's default for what the table lacks."""
    entries = ESTIMATES[kind]
    entry = (entries.get(key) or entries.get(DATED.sub("", key))) if key else None
    if isinstance(entry, dict):
        entry = entry.get(effort)
    return entry or entries["default"]


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
    time: str | None = None
    agent: str | None = None  # the agent type of a run's call
    derived: bool = False     # rebuilt from the transcript, as a compaction's call: no figure of it recorded

    @property
    def estimated(self):
        return not self.final

    @property
    def prompt(self):
        return self.input + self.cache_read + self.write_5m + self.write_1h

    @property
    def cached(self):
        """The tokens the call leaves in the cache: those it read, then those it wrote."""
        return self.cache_read + self.write_5m + self.write_1h


@dataclass
class Totals:
    calls: int = 0
    estimated: int = 0
    tokens: dict = field(default_factory=lambda: dict.fromkeys(KINDS, 0))
    cost: float | None = 0.0
    estimated_cost: float | None = 0.0

    def add(self, call):
        self.calls += 1
        self.estimated += call.estimated
        for kind in KINDS:
            self.tokens[kind] += getattr(call, kind)
        price, part = cost(call), estimated_cost(call)
        self.cost = None if price is None or self.cost is None else self.cost + price
        self.estimated_cost = None if part is None or self.estimated_cost is None else self.estimated_cost + part


@dataclass
class Count(Totals):
    models: dict = field(default_factory=dict)
    efforts: Counter = field(default_factory=Counter)
    by_effort: dict = field(default_factory=dict)  # {(model, effort): Totals}

    @property
    def unknown(self):
        return sorted(model for model, totals in self.models.items() if totals.cost is None)

    def add(self, call):
        super().add(call)
        self.models.setdefault(call.model, Totals()).add(call)
        self.efforts[call.effort] += 1
        self.by_effort.setdefault((call.model, call.effort), Totals()).add(call)


@dataclass
class Run:
    id: str
    agent: str | None
    calls: list
    tool_use: str | None = None  # the id of the Agent call that started the run


@dataclass
class Compaction:
    """A compaction from its compact_boundary record: its call derived, and the prompt of the first call after it."""
    time: str
    trigger: str | None
    pre_tokens: int
    post_tokens: int
    call: Call | None = None
    left: int | None = None


@dataclass
class Rebuild:
    """A call that wrote the cache again: the tokens written again, their cost over a read of them, the cause."""
    call: Call
    tokens: int
    cost: float | None
    cause: str              # pause, organization, model or unknown
    run: str | None = None  # the run's id, None on the main thread


@dataclass
class Session:
    main: list
    runs: list
    compactions: list
    rebuilds: list
    started: str | None = None  # the time of the main transcript's earliest record
    ended: str | None = None    # the time of its latest record

    @property
    def calls(self):
        return self.main + [call for run in self.runs for call in run.calls]


def records(path):
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                yield record


def is_call(record):
    message = record.get("message")
    return (record.get("type") == "assistant" and isinstance(message, dict) and bool(message.get("id"))
            and message.get("model") != SYNTHETIC)


def to_call(record, agent=None, time=None):
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
    effort = record.get("effort")
    return Call(id=message["id"], model=message.get("model") or "", effort=effort,
                sidechain=bool(record.get("isSidechain")), final=final,
                input=used.get("input_tokens") or 0,
                output=(used.get("output_tokens") or 0) if final else estimate("output", agent, effort).value,
                cache_read=used.get("cache_read_input_tokens") or 0, write_5m=write_5m, write_1h=write_1h,
                time=time or record.get("timestamp"), agent=agent)


def widen(span, record):
    """span, the (earliest, latest) times seen, widened to the record's; a time that cannot be read left out."""
    time, first, last = record.get("timestamp"), *span
    found = seconds(time)
    if found is None:
        return span
    return (time if first is None or found < seconds(first) else first,
            time if last is None or found > seconds(last) else last)


def transcript(path, agent=None):
    """(calls, ended): one Call per assistant message id, its last record kept, its time its first record's,
    and the time of the transcript's latest record; agent, a run's agent type."""
    started, last, span = {}, {}, (None, None)
    for record in records(path):
        span = widen(span, record)
        if is_call(record):
            started.setdefault(record["message"]["id"], record.get("timestamp"))
            last[record["message"]["id"]] = record
    return [to_call(record, agent, started[key]) for key, record in last.items()], span[1]


def calls(path, agent=None):
    """One Call per assistant message id of the transcript, its last record kept; agent, a run's agent type."""
    return transcript(path, agent)[0]


def seconds(stamp):
    try:
        return datetime.fromisoformat(stamp).timestamp()
    except (TypeError, ValueError):
        return None


def moment(stamp):
    """The stamp in seconds, an unknown time after every known one."""
    found = seconds(stamp)
    return math.inf if found is None else found


def lifetime(thread):
    """How long the thread's cache entries live: an hour when it writes one-hour entries, else five minutes when it writes any."""
    if any(call.write_1h for call in thread) or not any(call.write_5m for call in thread):
        return LIFETIMES["write_1h"]
    return LIFETIMES["write_5m"]


def cause(previous, call, span, organizations):
    before, after = seconds(previous.time), seconds(call.time)
    if before is not None and after is not None:
        if after - before > span:
            return "pause"
        held = None
        for moment, uuid in sorted((seconds(time), uuid) for time, uuid in organizations if seconds(time) is not None):
            if moment <= before:
                held = uuid
            elif moment <= after and held is not None and uuid != held:
                return "organization"
    return "model" if call.model != previous.model else "unknown"


def rebuild_cost(call, tokens):
    price = price_of(call.model)
    rates = price.rates(call.prompt) if price else {}
    writes = [kind for kind in ("write_5m", "write_1h") if getattr(call, kind)]
    if any(kind not in rates for kind in [*writes, "cache_read"]):
        return None
    write = sum(getattr(call, kind) * rates[kind] for kind in writes) / (call.write_5m + call.write_1h)
    return tokens * (write - rates["cache_read"]) / 1e6


def rebuilds(thread, organizations=(), run=None):
    """The calls of one thread that write again most of what the previous call left in the cache.

    A call rebuilds when it reads back less than half the tokens the previous call read and wrote;
    the tokens it writes again are those lost, up to what it writes. The cause: a pause past the
    thread's cache lifetime, an organization changed between the two calls (organizations holds the
    time and uuid of each credential_org record), a change of model, or unknown.
    """
    thread = list(thread)
    span, found = lifetime(thread), []
    for previous, call in zip(thread, thread[1:]):
        lost = previous.cached - call.cache_read
        tokens = min(lost, call.write_5m + call.write_1h)
        if tokens > 0 and 2 * lost >= previous.cached:
            found.append(Rebuild(call, tokens, rebuild_cost(call, tokens), cause(previous, call, span, organizations), run))
    return found


def compacted(boundary, previous, thread):
    """The Compaction of a compact_boundary record, its call derived from the call before it.

    No transcript holds the compaction's call. Its cache read is the previous call's prompt, written
    instead when the pause since that call passed the thread's cache lifetime; its fresh input the
    rest of preTokens; its output the estimate for its model, the call marked estimated.
    """
    meta = boundary.get("compactMetadata") or {}
    found = Compaction(boundary.get("timestamp"), meta.get("trigger"), meta.get("preTokens") or 0,
                       meta.get("postTokens") or 0)
    if previous is None:
        return found
    span = lifetime(thread)
    started, before = seconds(found.time), seconds(previous.time)
    lost = started is not None and before is not None and started - (meta.get("durationMs") or 0) / 1000 - before > span
    context = previous.prompt
    found.call = Call(id=f"compaction:{previous.id}", model=previous.model, effort=previous.effort,
                      sidechain=False, final=False, input=max(found.pre_tokens - context, 0),
                      output=estimate("compaction", previous.model).value, cache_read=0 if lost else context,
                      write_5m=context if lost and span == LIFETIMES["write_5m"] else 0,
                      write_1h=context if lost and span == LIFETIMES["write_1h"] else 0,
                      time=found.time, derived=True)
    return found


def last_output(call, used, notified):
    """A run's last call takes the final output of the Agent result's usage, when its prompt is the call's.

    Without one, as for a run in the background, its notification's tokens less the call's prompt
    give the output, still estimated: they differ from a final usage by a few hundred tokens.
    """
    if used and ((used.get("input_tokens") or 0, used.get("cache_read_input_tokens") or 0,
                  used.get("cache_creation_input_tokens") or 0)
                 == (call.input, call.cache_read, call.write_5m + call.write_1h)):
        call.output, call.final = used.get("output_tokens") or 0, True
    elif notified is not None and notified >= call.prompt:
        call.output = notified - call.prompt


def meta_of(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def session(path):
    """The Session of a main transcript: its main thread with each compaction's call, its runs, its rebuilds.

    The runs are the transcripts of <session>/subagents/, each with its agent type and the Agent
    call that started it from its .meta.json. A main thread's compactions split it into threads for the rebuilds: the first call
    after a compaction holds the context it left, not a rebuild.
    """
    path = Path(path)
    first, started, last, boundaries, organizations, results, notified = {}, {}, {}, [], [], {}, {}
    span = (None, None)
    for index, record in enumerate(records(path)):
        span = widen(span, record)
        if is_call(record):
            first.setdefault(record["message"]["id"], index)
            started.setdefault(record["message"]["id"], record.get("timestamp"))
            last[record["message"]["id"]] = record
        elif record.get("type") == "system" and record.get("subtype") == "compact_boundary":
            boundaries.append((index, record))
        attachment, result = record.get("attachment"), record.get("toolUseResult")
        if isinstance(attachment, dict) and attachment.get("type") == "credential_org":
            organizations.append((record.get("timestamp"), attachment.get("organizationUuid")))
        if isinstance(result, dict) and result.get("agentId") and isinstance(result.get("usage"), dict):
            results[result["agentId"]] = result["usage"]
        if record.get("type") == "queue-operation" and isinstance(record.get("content"), str):
            notified.update((agent, int(tokens)) for agent, tokens in NOTIFIED.findall(record["content"]))
    timeline = sorted([(first[key], to_call(record, time=started[key])) for key, record in last.items()]
                      + boundaries, key=lambda pair: pair[0])
    main, compactions, threads, thread, previous = [], [], [], [], None
    for _, item in timeline:
        if isinstance(item, Call):
            if compactions and compactions[-1].left is None and not thread:
                compactions[-1].left = item.prompt
            main.append(item)
            thread.append(item)
            previous = item
        else:
            compactions.append(compacted(item, previous, thread))
            if compactions[-1].call:
                main.append(compactions[-1].call)
            threads.append(thread)
            thread = []
    threads.append(thread)
    runs = []
    for transcript in sorted((path.with_suffix("") / "subagents").glob("agent-*.jsonl")):
        run_id = transcript.stem.removeprefix("agent-")
        meta = meta_of(transcript.with_name(f"{transcript.stem}.meta.json"))
        run_calls = calls(transcript, meta.get("agentType"))
        if run_calls and not run_calls[-1].final:
            last_output(run_calls[-1], results.get(run_id), notified.get(run_id))
        runs.append(Run(run_id, meta.get("agentType"), run_calls, meta.get("toolUseId")))
    runs.sort(key=lambda run: (min((call.time or "" for call in run.calls), default=""), run.id))
    found = [rebuild for thread in threads for rebuild in rebuilds(thread, organizations)]
    found += [rebuild for run in runs for rebuild in rebuilds(run.calls, organizations, run.id)]
    return Session(main, runs, compactions, found, *span)


def owners(threads):
    """{message id: index of the thread that keeps it}; threads, (calls, ended) for each transcript.

    A call held by several, as a continued conversation copies the history it continues, goes to
    the transcript whose record of it comes first; at equal times, to the one whose last record
    comes first, the conversation the history was copied from. A teleported copy dates its records
    at the teleport, after the original's.
    """
    best = {}
    for index, (thread, ended) in enumerate(threads):
        for call in thread:
            rank = (moment(call.time), moment(ended), index)
            if call.id not in best or rank < best[call.id]:
                best[call.id] = rank
    return {key: rank[-1] for key, rank in best.items()}


def distinct(sessions):
    """The sessions with each main-thread call kept once, by owners(): a compaction or a rebuild goes with its call.

    A continuation copies no run (2026-10-12, 1,065 transcripts kept): runs stay with their session.
    """
    owner = owners([(kept.main, kept.ended) for kept in sessions])
    found = []
    for index, kept in enumerate(sessions):
        main = [call for call in kept.main if owner[call.id] == index]
        ids = {call.id for call in main}
        found.append(replace(kept, main=main,
                             compactions=[c for c in kept.compactions if c.call is None or c.call.id in ids],
                             rebuilds=[r for r in kept.rebuilds if r.run is not None or r.call.id in ids]))
    return found


def price_of(model):
    return PRICES.get(model) or PRICES.get(DATED.sub("", model))


def cost(call, kinds=KINDS):
    """The call's cost in dollars, of the given kinds of token; None when the table lacks its model or a rate the call needs."""
    price = price_of(call.model)
    if price is None:
        return None
    rates = price.rates(call.prompt)
    held = [kind for kind in KINDS if getattr(call, kind)]
    if any(kind not in rates for kind in held):
        return None
    return sum(getattr(call, kind) * rates[kind] for kind in held if kind in kinds) / 1e6


def estimated_cost(call):
    """The part of the call's cost resting on an estimate: all of a derived call, the output of one without its final usage."""
    if call.final:
        return 0.0
    return cost(call, KINDS if call.derived else ("output",))


def text_cost(characters, thread):
    """(tokens, dollars) of a text the agent was given, from its characters, for the calls of thread that hold it.

    Its tokens take the table's characters a token for the first call's model; the first call
    writes them once at the one-hour rate, each later one reads them. The dollars are None when a
    call's model or rate is unknown.
    """
    thread = list(thread)
    tokens = round(characters / estimate("text", thread[0].model if thread else None).value)
    dollars = 0.0
    for index, call in enumerate(thread):
        price = price_of(call.model)
        rates, kind = (price.rates(call.prompt) if price else {}), ("cache_read" if index else "write_1h")
        if kind not in rates:
            return tokens, None
        dollars += tokens * rates[kind] / 1e6
    return tokens, dollars


def tally(calls):
    """The Count of calls, each message id once."""
    total, seen = Count(), set()
    for call in calls:
        if call.id not in seen:
            seen.add(call.id)
            total.add(call)
    return total


def count(paths):
    """The Count of every call of the transcripts, each message id once, kept as owners() gives it."""
    threads = [transcript(path) for path in paths]
    owner = owners(threads)
    return tally(call for index, (found, _) in enumerate(threads) for call in found if owner[call.id] == index)


def as_json(total):
    def totals(t):
        return {"calls": t.calls, "estimated": t.estimated, "tokens": t.tokens, "cost": t.cost,
                "estimated_cost": t.estimated_cost}

    def source(model):
        price = price_of(model)
        return price and {"source": price.source, "read": price.read, "origin": price.origin}

    def efforts(model):
        return {effort or "none": totals(t) for (m, effort), t in total.by_effort.items() if m == model}
    return {**totals(total), "unknown": total.unknown, "prices": PRICES_READ,
            "efforts": {effort or "none": n for effort, n in total.efforts.items()},
            "models": {model: {**totals(t), "price": source(model), "efforts": efforts(model)}
                       for model, t in sorted(total.models.items())}}


def main(argv=None):
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print(__doc__.splitlines()[2], file=sys.stderr)
        return 2
    print(json.dumps(as_json(count(paths)), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
