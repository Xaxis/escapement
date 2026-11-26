#!/usr/bin/env python3
"""Escapement's model: every derived number in the design and the paper.

  python3 model/escapement.py                 every number
  python3 model/escapement.py --only ID       one number with its formula and inputs
  python3 model/escapement.py --set ID=VALUE  rerun with an input changed (repeatable)
  python3 model/escapement.py --json          every number as JSON
  python3 model/escapement.py --write         write data/numbers.json and research/numbers.md

Inputs are in data/inputs.toml with their basis and source. This file only derives. Sections
follow the design document (research/02-design.md): the clock, the seal, the ladder, the bond,
seasoning, and what it would cost to cheat the clock.
"""

from __future__ import annotations

import inspect
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ledger import Ledger, write_outputs  # noqa: E402


def erlang_cdf(k: int, rate: float, t: float) -> float:
    """P(the k-th block arrives within time t) when blocks arrive as a Poisson process."""
    x = rate * t
    return 1.0 - sum(math.exp(-x) * x**n / math.factorial(n) for n in range(k))


def here() -> str:
    frame = inspect.currentframe().f_back
    return f"model/escapement.py#L{frame.f_lineno}"


def build(overrides: dict | None = None) -> Ledger:
    L = Ledger(overrides=dict(overrides or {}))
    d = L.derive

    # The clock: blocks arrive as a Poisson process with a 600 s mean, so a delay counted in blocks
    # is a random wall-clock time. These are the chances a delay is much shorter than its mean.
    d("blocks-per-day", lambda q: 86400 / q["block-interval-s"], "86400 / block-interval-s",
      "blocks", label="blocks in a day at the target interval", defined_in=here())
    d("tier2-delay-mean-min", lambda q: q["tier2-delay-blocks"] * q["block-interval-s"] / 60,
      "tier2-delay-blocks * block-interval-s / 60", "minutes", label="mean wall-clock length of the Tier 2 delay",
      defined_in=here())
    d("tier2-delay-p-under-half",
      lambda q: erlang_cdf(int(q["tier2-delay-blocks"]), 1 / q["block-interval-s"],
                           0.5 * q["tier2-delay-blocks"] * q["block-interval-s"]),
      "ErlangCDF(k = tier2-delay-blocks, t = half the mean)", fmt=".1%",
      label="chance the Tier 2 delay ends in under half its mean time", defined_in=here())
    d("tier3-delay-mean-h", lambda q: q["tier3-delay-blocks"] * q["block-interval-s"] / 3600,
      "tier3-delay-blocks * block-interval-s / 3600", "hours", fmt=",.0f",
      label="mean wall-clock length of the Tier 3 delay", defined_in=here())
    d("tier3-delay-p-under-80pct",
      lambda q: erlang_cdf(int(q["tier3-delay-blocks"]), 1 / q["block-interval-s"],
                           0.8 * q["tier3-delay-blocks"] * q["block-interval-s"]),
      "ErlangCDF(k = tier3-delay-blocks, t = 80% of the mean)", fmt=".2%",
      label="chance the Tier 3 delay ends in under 80% of its mean time", defined_in=here())
    d("lease-mean-h", lambda q: q["lease-blocks"] * q["block-interval-s"] / 3600,
      "lease-blocks * block-interval-s / 3600", "hours", label="mean wall-clock length of a lease",
      defined_in=here())
    d("season-days", lambda q: q["season-blocks"] / q["blocks-per-day"],
      "season-blocks / blocks-per-day", "days", label="time for a bond to season fully", defined_in=here())

    # Blockspace: what the chain can carry, in anchors.
    d("vbytes-per-block", lambda q: q["block-weight-limit"] / 4, "block-weight-limit / 4", "vB",
      label="virtual bytes in a full block", defined_in=here())
    d("vbytes-per-day", lambda q: q["vbytes-per-block"] * q["blocks-per-day"],
      "vbytes-per-block * blocks-per-day", "vB", label="virtual bytes the chain carries in a day",
      defined_in=here())
    d("seal-tx-per-day-max", lambda q: q["vbytes-per-day"] / q["seal-tx-vbytes"],
      "vbytes-per-day / seal-tx-vbytes", "transactions", fmt="sig2",
      label="seal transactions a day if they filled every block", defined_in=here())
    d("tier3-capacity-per-day", lambda q: q["seal-tx-per-day-max"] * q["tier3-blockspace-share"],
      "seal-tx-per-day-max * tier3-blockspace-share", "actions", fmt="sig2",
      label="Tier 3 actions a day the world could anchor one by one at the assumed share of blockspace",
      defined_in=here())

    # The seal: what non-equivocating logs cost.
    for level in ("low", "median", "high"):
        d(f"seal-cost-{level}", lambda q, lv=level: q["seal-tx-vbytes"] * q[f"feerate-{lv}"],
          f"seal-tx-vbytes * feerate-{level}", "sats", label=f"one seal transaction at the {level} fee rate",
          defined_in=here())
    d("seals-per-day", lambda q: q["blocks-per-day"] / q["seal-epoch-blocks"],
      "blocks-per-day / seal-epoch-blocks", "seals", fmt=",.0f", label="seals a gateway makes in a day",
      defined_in=here())
    d("gateway-seal-cost-day-median", lambda q: q["seals-per-day"] * q["seal-cost-median"],
      "seals-per-day * seal-cost-median", "sats", label="a gateway's daily sealing cost at the median fee rate",
      defined_in=here())
    d("gateway-seal-cost-day-high", lambda q: q["seals-per-day"] * q["seal-cost-high"],
      "seals-per-day * seal-cost-high", "sats", label="a gateway's daily sealing cost at the high fee rate",
      defined_in=here())
    d("agent-seal-cost-day-pooled", lambda q: q["gateway-seal-cost-day-high"] / q["agents-per-pool"],
      "gateway-seal-cost-day-high / agents-per-pool", "sats", fmt=",.1f",
      label="one agent's daily sealing cost in a shared pool, at the high fee rate", defined_in=here())
    d("seal-blockspace-share-pools",
      lambda q: q["seals-per-day"] * q["seal-pools"] * q["seal-tx-vbytes"] / q["vbytes-per-day"],
      "seals-per-day * seal-pools * seal-tx-vbytes / vbytes-per-day", fmt=".2%",
      label="share of blockspace the assumed number of seal pools would use", defined_in=here())

    # The bond: deterrence (expected loss at least the gain) and coverage (the governed ceiling).
    for p in ("10", "50", "90"):
        d(f"bond-deter-p{p}", lambda q, pp=p: q["gain-from-violation"] / (int(pp) / 100),
          f"gain-from-violation / 0.{p}" if p != "10" else "gain-from-violation / 0.10", "sats", fmt="sig2",
          label=f"bond that deters a violation worth the assumed gain when it is caught {p}% of the time",
          defined_in=here())
    d("bond-coverage", lambda q: q["coverage-ratio"] * q["allowance-per-lease"] * q["leases-at-risk"],
      "coverage-ratio * allowance-per-lease * leases-at-risk", "sats", fmt="sig2",
      label="bond that covers what the agent can spend before anyone can stop it", defined_in=here())

    # Seasoning: a swarm costs capital times time, and time cannot be bought.
    d("swarm-capital", lambda q: q["swarm-size"] * q["bond-coverage"],
      "swarm-size * bond-coverage", "sats", fmt="sig2", label="capital a swarm of chartered agents must lock",
      defined_in=here())
    d("swarm-capital-btc", lambda q: q["swarm-capital"] / 1e8, "swarm-capital / 1e8", "BTC", fmt=",.0f",
      label="the same, in bitcoin", defined_in=here())
    d("split-authority-ratio-squared", lambda q: 1 / q["swarm-size"],
      "(N * (C/N)^2) / C^2 = 1/N with N = swarm-size", fmt="sig2",
      label="total authority of N agents relative to one agent holding the same capital, under squared bond value",
      defined_in=here())

    # Cheating the clock: making blocks come faster needs hashrate the size of the network's.
    d("clock-2x-extra-hashrate-eh", lambda q: q["hashrate-eh"],
      "hashrate-eh (to double the block rate, add as much hashrate as the network has)", "EH/s", fmt=",.0f",
      label="extra hashrate needed to make blocks come twice as fast until the next retarget", defined_in=here())
    d("clock-2x-power-gw", lambda q: q["hashrate-eh"] * 1e6 * q["fleet-efficiency-j-th"] / 1e9,
      "hashrate-eh * 1e6 TH/EH * fleet-efficiency-j-th / 1e9", "GW", fmt=",.0f",
      label="electric power that extra hashrate draws", defined_in=here())
    d("clock-2x-hours-saved-per-epoch", lambda q: 2016 * q["block-interval-s"] / 3600 / 2,
      "2016 blocks * block-interval-s / 3600 / 2", "hours", fmt=",.0f",
      label="hours a doubled block rate gains over one difficulty period", defined_in=here())

    return L


def parse_sets(argv: list[str]) -> dict:
    sets = {}
    for i, arg in enumerate(argv):
        if arg == "--set":
            key, _, value = argv[i + 1].partition("=")
            sets[key] = float(value)
    return sets


def main(argv: list[str]) -> int:
    L = build(parse_sets(argv))
    if "--write" in argv:
        write_outputs(L)
        print(f"wrote data/numbers.json and research/numbers.md ({len(L.order)} numbers)")
        return 0
    if "--json" in argv:
        print(json.dumps(L.to_json(), indent=2))
        return 0
    if "--only" in argv:
        key = argv[argv.index("--only") + 1]
        q = L.q[key]
        print(f"{key} = {q.display()}  ({q.basis})")
        if q.label:
            print(f"  {q.label}")
        if q.formula:
            print(f"  formula: {q.formula}")
            for i in q.inputs:
                print(f"    {i} = {L.q[i].display()}")
        if q.source:
            print(f"  source: {q.source} {q.date}")
        print(f"  defined in: {q.defined_in}")
        return 0
    for key in L.order:
        q = L.q[key]
        print(f"{key:40} {q.display():>28}  {q.basis}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
