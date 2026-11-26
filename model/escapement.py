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


def nakamoto_p(q: float, z: int) -> float:
    """Nakamoto 2008, section 11: the chance an attacker with hashrate share q ever catches up
    from z blocks behind."""
    p = 1 - q
    if q >= p:
        return 1.0
    lam = z * (q / p)
    total = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam) * lam**k / math.factorial(k)
        total -= poisson * (1 - (q / p) ** (z - k))
    return total


def depth_for(q: float, target: float) -> int:
    for z in range(0, 10000):
        if nakamoto_p(q, z) < target:
            return z
    raise ValueError("no depth reaches the target")


def here() -> str:
    frame = inspect.currentframe().f_back
    return f"model/escapement.py#L{frame.f_lineno}"


def build(overrides: dict | None = None) -> Ledger:
    L = Ledger(overrides=dict(overrides or {}))
    d = L.derive

    # The clock. Blocks arrive as a Poisson process with a 600 s mean, so a delay counted in blocks
    # is a random wall-clock time: these are the chances a delay is much shorter than its mean.
    d("blocks-per-day", lambda q: 86400 / q["block-interval-s"], "86400 / block-interval-s",
      "blocks", label="blocks in a day at the target interval", defined_in=here())
    d("tier2-delay-mean-min", lambda q: q["tier2-delay-blocks"] * q["block-interval-s"] / 60,
      "tier2-delay-blocks * block-interval-s / 60", "minutes",
      label="mean wall-clock length of the Tier 2 delay", defined_in=here())
    d("tier2-delay-p-under-half",
      lambda q: erlang_cdf(int(q["tier2-delay-blocks"]), 1 / q["block-interval-s"],
                           0.5 * q["tier2-delay-blocks"] * q["block-interval-s"]),
      "ErlangCDF(k = tier2-delay-blocks, t = half the mean)", fmt=".1%",
      label="chance the Tier 2 delay ends in under half its mean time", defined_in=here())
    d("tier3-delay-mean-h", lambda q: q["tier3-delay-blocks"] * q["block-interval-s"] / 3600,
      "tier3-delay-blocks * block-interval-s / 3600", "hours",
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

    # Cheating the clock without a hashrate majority: blocks come faster only with more hashrate,
    # and only until the next difficulty adjustment.
    d("clock-2x-power-gw", lambda q: q["hashrate-eh"] * 1e6 * q["asic-efficiency-j-th"] / 1e9,
      "hashrate-eh * 1e6 TH/EH * asic-efficiency-j-th / 1e9", "GW", fmt=",.1f",
      label="power drawn by enough new hardware to double the network's hashrate", defined_in=here())
    d("clock-2x-hardware-busd", lambda q: q["hashrate-eh"] * 1e6 * q["asic-price-usd-th"] / 1e9,
      "hashrate-eh * 1e6 TH/EH * asic-price-usd-th / 1e9", "billion USD", fmt=",.1f",
      label="cost of that hardware at current street prices", defined_in=here())
    d("clock-2x-days-gained", lambda q: q["blocks-per-retarget"] * q["block-interval-s"] / 2 / 86400,
      "blocks-per-retarget * block-interval-s / 2 / 86400", "days",
      label="days a doubled block rate gains before the next adjustment cancels it", defined_in=here())
    d("tier3-compress-factor", lambda q: q["tier3-delay-mean-h"] / q["tier3-compress-target-h"],
      "tier3-delay-mean-h / tier3-compress-target-h", "x",
      label="how many times the network's hashrate an adversary needs to shrink a Tier 3 delay to the target",
      defined_in=here())
    d("tier3-compress-power-gw",
      lambda q: (q["tier3-compress-factor"] - 1) * q["hashrate-eh"] * 1e6 * q["asic-efficiency-j-th"] / 1e9,
      "(tier3-compress-factor - 1) * hashrate-eh * 1e6 * asic-efficiency-j-th / 1e9", "GW", fmt=",.0f",
      label="power the added hardware would draw", defined_in=here())

    # Finality: Nakamoto's own catch-up probability for an attacker with share q, z blocks behind.
    d("reorg-p-largest-6", lambda q: nakamoto_p(q["pool-largest-share"], int(q["confirmations-standard"])),
      "Nakamoto(q = pool-largest-share, z = confirmations-standard)", fmt=".1%",
      label="chance the largest pool alone rewrites a block six deep", defined_in=here())
    d("reorg-p-top2-6", lambda q: nakamoto_p(q["pool-top2-share"], int(q["confirmations-standard"])),
      "Nakamoto(q = pool-top2-share, z = confirmations-standard)", fmt=".0%",
      label="chance the two largest pools, colluding, rewrite a block six deep", defined_in=here())
    d("depth-for-target-largest", lambda q: depth_for(q["pool-largest-share"], q["reorg-risk-target"]),
      "least z with Nakamoto(pool-largest-share, z) < reorg-risk-target", "blocks",
      label="confirmations before the largest pool alone has under the target chance of a rewrite",
      defined_in=here())
    d("reorg-p-top2-144", lambda q: nakamoto_p(q["pool-top2-share"], int(q["tier3-delay-blocks"])),
      "Nakamoto(q = pool-top2-share, z = tier3-delay-blocks)", fmt=".2%",
      label="chance the two largest pools rewrite an anchor a Tier 3 delay deep", defined_in=here())

    # Blockspace: what the chain can carry.
    d("vbytes-per-block", lambda q: q["block-weight-limit"] / 4, "block-weight-limit / 4", "vB",
      label="virtual bytes in a full block", defined_in=here())
    d("vbytes-per-day", lambda q: q["vbytes-per-block"] * q["blocks-per-day"],
      "vbytes-per-block * blocks-per-day", "vB", label="virtual bytes the chain carries in a day",
      defined_in=here())
    d("seal-tx-vbytes", lambda q: q["tx-overhead-vb"] + q["p2tr-input-vb"] + q["p2tr-output-vb"],
      "tx-overhead-vb + p2tr-input-vb + p2tr-output-vb", "vB",
      label="a seal: one Taproot input spending the last seal, one Taproot output committing the new head",
      defined_in=here())
    d("anchor-tx-vbytes",
      lambda q: q["tx-overhead-vb"] + q["p2tr-input-vb"] + q["p2tr-output-vb"] + q["opreturn32-output-vb"],
      "tx-overhead-vb + p2tr-input-vb + p2tr-output-vb + opreturn32-output-vb", "vB",
      label="an anchor that also carries its commitment in a 32-byte OP_RETURN", defined_in=here())
    d("seal-tx-per-day-max", lambda q: q["vbytes-per-day"] / q["seal-tx-vbytes"],
      "vbytes-per-day / seal-tx-vbytes", "transactions", fmt="sig2",
      label="seal transactions a day if they filled every block", defined_in=here())
    d("seal-capacity-vs-2026", lambda q: q["seal-tx-per-day-max"] / q["tx-per-day-2026"],
      "seal-tx-per-day-max / tx-per-day-2026", "x", fmt=",.1f",
      label="that capacity as a multiple of all of 2026's daily transactions", defined_in=here())
    d("tier3-capacity-per-day", lambda q: q["seal-tx-per-day-max"] * q["tier3-blockspace-share"],
      "seal-tx-per-day-max * tier3-blockspace-share", "actions", fmt="sig2",
      label="Tier 3 actions a day the world could anchor one by one in the assumed share of blockspace",
      defined_in=here())

    # The seal: what non-equivocating logs cost.
    for level in ("2026", "2023", "halving", "peak-day"):
        d(f"seal-cost-{level}", lambda q, lv=level: q["seal-tx-vbytes"] * q[f"feerate-{lv}"],
          f"seal-tx-vbytes * feerate-{level}", "sats", fmt="sig3",
          label=f"one seal at the {level.replace('-', ' ')} fee rate", defined_in=here())
    d("seals-per-day", lambda q: q["blocks-per-day"] / q["seal-epoch-blocks"],
      "blocks-per-day / seal-epoch-blocks", "seals", label="seals a gateway makes in a day",
      defined_in=here())
    d("gateway-seal-cost-day-2026", lambda q: q["seals-per-day"] * q["seal-cost-2026"],
      "seals-per-day * seal-cost-2026", "sats", fmt="sig3",
      label="a gateway's daily sealing cost at 2026's median fee rate", defined_in=here())
    d("gateway-seal-cost-day-halving", lambda q: q["seals-per-day"] * q["seal-cost-halving"],
      "seals-per-day * seal-cost-halving", "sats", fmt="sig3",
      label="a gateway's daily sealing cost at the halving block's fee rate", defined_in=here())
    d("agent-seal-cost-day-halving", lambda q: q["gateway-seal-cost-day-halving"] / q["agents-per-pool"],
      "gateway-seal-cost-day-halving / agents-per-pool", "sats", fmt="sig3",
      label="one agent's daily sealing cost in a shared pool, at the halving block's fee rate", defined_in=here())
    d("seal-blockspace-share-pools",
      lambda q: q["seals-per-day"] * q["seal-pools"] * q["seal-tx-vbytes"] / q["vbytes-per-day"],
      "seals-per-day * seal-pools * seal-tx-vbytes / vbytes-per-day", fmt=".2%",
      label="share of blockspace the assumed number of seal pools would use", defined_in=here())
    d("headers-mb-per-year", lambda q: q["header-bytes"] * q["blocks-per-day"] * 365 / 1e6,
      "header-bytes * blocks-per-day * 365 / 1e6", "MB", fmt=",.1f",
      label="block headers a device must read in a year to keep its own clock", defined_in=here())

    # The bond: deterrence needs the expected sanction at least the gain (Becker; Polinsky and
    # Shavell), so a bond B deters a gain G caught with probability p only if B >= G / p.
    for p in ("10", "50", "90"):
        d(f"bond-deter-p{p}", lambda q, pp=p: q["gain-from-violation"] / (int(pp) / 100),
          f"gain-from-violation / {int(p) / 100:.2f}", "sats", fmt="sig2",
          label=f"bond that deters a violation worth the assumed gain when it is caught {p}% of the time",
          defined_in=here())
    d("bond-judgment-proof-btc", lambda q: q["harm-catastrophic-btc"] / q["p-detect-rare"],
      "harm-catastrophic-btc / p-detect-rare", "BTC", fmt="sig2",
      label="bond that would fully deter a large, rarely detected harm", defined_in=here())
    d("bond-coverage", lambda q: q["coverage-ratio"] * q["allowance-per-lease"] * q["leases-at-risk"],
      "coverage-ratio * allowance-per-lease * leases-at-risk", "sats", fmt="sig2",
      label="bond that covers what the agent can spend before anyone can stop it", defined_in=here())

    # Swarms: costly identity prices a swarm; it does not stop one.
    d("swarm-capital-btc", lambda q: q["swarm-size"] * q["bond-coverage"] / 1e8,
      "swarm-size * bond-coverage / 1e8", "BTC", fmt=",.0f",
      label="capital a swarm of chartered agents must lock", defined_in=here())
    d("incident-swarm-capital-btc", lambda q: q["incident-agents-attack"] * q["bond-coverage"] / 1e8,
      "incident-agents-attack * bond-coverage / 1e8", "BTC", fmt=",.1f",
      label="the same for the 2026 incident's attacking agents, had each needed a charter", defined_in=here())
    d("incident-days", lambda q: q["incident-stop-day"] - q["incident-first-day"],
      "incident-stop-day - incident-first-day", "days",
      label="days from the first message-board entry to the start of the stop", defined_in=here())
    d("split-authority-ratio-squared", lambda q: 1 / q["swarm-size"],
      "(N * (C/N)^2) / C^2 = 1/N with N = swarm-size", fmt="sig2",
      label="total authority of N agents relative to one agent holding the same capital, under squared bond value",
      defined_in=here())
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
