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
import sim
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
        poisson = math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) if lam > 0 else float(k == 0)
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

    d("datacentre-gw-2025", lambda q: q["datacentre-twh-2025"] * 1e12 / 8760 / 1e9,
      "datacentre-twh-2025 * 1e12 / 8760 h / 1e9", "GW", fmt=",.0f",
      label="average power drawn by all data centres in 2025", defined_in=here())
    d("bitcoin-gw-survey", lambda q: q["bitcoin-twh-survey"] * 1e12 / 8760 / 1e9,
      "bitcoin-twh-survey * 1e12 / 8760 h / 1e9", "GW", fmt=",.1f",
      label="average power drawn by Bitcoin mining in the Cambridge survey", defined_in=here())
    d("tier3-compress-vs-datacentres", lambda q: q["tier3-compress-power-gw"] / q["datacentre-gw-2025"],
      "tier3-compress-power-gw / datacentre-gw-2025", "x", fmt=",.0f",
      label="that power as a multiple of every data centre on Earth in 2025", defined_in=here())

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
    d("depth-for-target-top2", lambda q: depth_for(q["pool-top2-share"], q["reorg-risk-target"]),
      "least z with Nakamoto(pool-top2-share, z) < reorg-risk-target", "blocks", fmt=",.0f",
      label="confirmations before the two largest pools, colluding, have under the target chance of a rewrite",
      defined_in=here())
    d("depth-for-target-top2-days", lambda q: q["depth-for-target-top2"] * q["block-interval-s"] / 86400,
      "depth-for-target-top2 * block-interval-s / 86400", "days", fmt=",.1f",
      label="that depth in days", defined_in=here())
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
      label="total authority of N agents relative to one agent holding the same capital, if bond value were squared (Belcher's 2019 proposal)",
      defined_in=here())
    d("split-authority-ratio-jm", lambda q: q["swarm-size"] ** (1 - q["jm-bond-exponent"]),
      "N * (C/N)^x / C^x = N^(1 - x) with N = swarm-size, x = jm-bond-exponent", fmt="sig2",
      label="the same ratio under JoinMarket's shipped exponent", defined_in=here())

    # The record (research/05-formal.md, section 3). An identity costs the return forgone on its
    # bond over its term plus the fees of its bond and genesis transactions.
    d("identity-cost-sats",
      lambda q: q["bond-coverage"] * q["capital-cost-rate"] * q["bond-term-years"]
      + 2 * q["seal-tx-vbytes"] * q["feerate-2023"],
      "bond-coverage * capital-cost-rate * bond-term-years + 2 * seal-tx-vbytes * feerate-2023",
      "sats", fmt="sig2", label="cost of one identity whose record counts", defined_in=here())
    d("fake-record-lambda", lambda q: 2 ** q["fake-record-claims"],
      "2 ^ fake-record-claims", fmt="sig2",
      label="score of an all-correct record of that length against a baseline of one half", defined_in=here())
    d("fake-record-identities", lambda q: q["fake-record-success"] * q["fake-record-lambda"],
      "fake-record-success * fake-record-lambda (Theorem 1)", "identities", fmt="sig2",
      label="identities a record faker without edge needs", defined_in=here())
    d("fake-record-cost-btc", lambda q: q["fake-record-identities"] * q["identity-cost-sats"] / 1e8,
      "fake-record-identities * identity-cost-sats / 1e8", "BTC", fmt="sig2",
      label="what faking that record costs at least", defined_in=here())

    def faking(q):
        return sim.record_faking(int(q["sim-identities"]), int(q["sim-log2-lambda"]),
                                 int(q["sim-log2-lambda"]), 4000, 1)
    d("sim-fake-p", lambda q: faking(q)["p-any-reaches"],
      "simulated share of 4,000 trials in which any identity reaches the score", fmt=".1%",
      label="how often a faker running sim-identities identities reached 2^sim-log2-lambda",
      defined_in=here())
    d("sim-fake-bound", lambda q: min(1, q["sim-identities"] / 2 ** q["sim-log2-lambda"]),
      "sim-identities / 2^sim-log2-lambda (Theorem 1)", fmt=".1%",
      label="the bound for the same case", defined_in=here())
    d("sim-selective-claims",
      lambda q: sim.record_selective(int(q["sim-log2-lambda"]), 4000, 2)["claims-mean"],
      "simulated mean claims until the shown record reaches the score", "claims", fmt=",.0f",
      label="claims one identity needs to fake the same record if it may hide its misses",
      defined_in=here())

    def skilled(q):
        return sim.record_skilled(int(q["sim-skilled-log2-lambda"]), q["sim-skilled-p-low"],
                                  q["sim-skilled-p-high"], 400, 3)
    d("sim-skilled-edge", lambda q: skilled(q)["edge-nats"],
      "mean KL(p || 1/2) for p uniform on [sim-skilled-p-low, sim-skilled-p-high]", "nats",
      fmt=".2f", label="per-claim edge of the skilled honest identity", defined_in=here())
    d("sim-skilled-claims", lambda q: skilled(q)["claims-median"],
      "simulated median claims until the likelihood ratio first reaches 2^sim-skilled-log2-lambda",
      "claims", fmt=",.0f", label="claims the skilled honest identity needs, with one identity",
      defined_in=here())
    d("sim-skilled-identities-faker",
      lambda q: q["fake-record-success"] * 2 ** q["sim-skilled-log2-lambda"],
      "fake-record-success * 2^sim-skilled-log2-lambda", "identities", fmt="sig2",
      label="identities a faker without edge needs for the same score", defined_in=here())

    # Correlated claims (RT-01) under the product rule and the round rule.
    def corr(q, rule):
        return sim.record_correlated(int(q["sim-corr-identities"]), int(q["sim-corr-claims"]),
                                     q["sim-corr-r"], int(q["sim-log2-lambda"]), rule,
                                     int(q["sim-corr-rounds"]), 4000, 11)
    d("sim-corr-product-p", lambda q: corr(q, "product")["p-any-reaches"],
      "simulated share of 4,000 trials in which some identity reaches 2^sim-log2-lambda, product rule",
      fmt=".1%", label="success of the correlated-claims attack when a round's ratios multiply",
      defined_in=here())
    d("sim-corr-round-p", lambda q: corr(q, "mean")["p-any-reaches"],
      "the same under the round rule (a round counts as the mean of its ratios)", fmt=".1%",
      label="success of the same attack under the round rule", defined_in=here())
    d("sim-corr-bound", lambda q: q["sim-corr-identities"] / 2 ** q["sim-log2-lambda"],
      "sim-corr-identities / 2^sim-log2-lambda", fmt=".1%",
      label="Theorem 1's bound for that many identities", defined_in=here())
    d("tail-product-score", lambda q: (1 / (1 - q["tail-fail-p"])) ** q["tail-claims"],
      "(1 / (1 - tail-fail-p)) ^ tail-claims", fmt="sig2",
      label="score of the hidden tail-risk record when the claims multiply (99% of the time)",
      defined_in=here())
    d("tail-round-score", lambda q: 1 / (1 - q["tail-fail-p"]),
      "1 / (1 - tail-fail-p): the mean of the claims' ratios", fmt=".2f",
      label="score of the same record under the round rule", defined_in=here())

    def skilled_rounds(q):
        return sim.record_skilled_rounds(int(q["sim-skilled-log2-lambda"]), q["sim-skilled-p-low"],
                                         q["sim-skilled-p-high"], int(q["sim-round-claims"]), 400, 3)
    d("sim-skilled-rounds", lambda q: skilled_rounds(q)["rounds-median"],
      "simulated median rounds until the round-rule score first reaches 2^sim-skilled-log2-lambda",
      "rounds", fmt=",.0f", label="rounds the skilled honest identity needs under the round rule",
      defined_in=here())
    d("sim-skilled-round-claims", lambda q: skilled_rounds(q)["claims-median"],
      "sim-skilled-rounds * sim-round-claims", "claims", fmt=",.0f",
      label="claims it makes in those rounds", defined_in=here())

    # Training (section 5): the learned confidence parameter, 1 when calibrated.
    d("sim-train-a-complete", lambda q: sim.training("complete", 3000, 64, 0.5, 0.5, 4)["a"],
      "stochastic gradient ascent from a = 0.5, complete records", fmt=".2f",
      label="confidence the learner settles on under complete records (1 is calibrated)",
      defined_in=here())
    d("sim-train-err-complete",
      lambda q: sim.training("complete", 3000, 64, 0.5, 0.5, 4)["calibration-error"],
      "mean |q - p| of the learned policy", fmt=".1%",
      label="its calibration error", defined_in=here())
    d("sim-train-a-selective", lambda q: sim.training("selective", 3000, 64, 0.5, 1.0, 5)["a"],
      "stochastic gradient ascent from a = 1 (calibrated), after-the-fact selection", fmt=".1f",
      label="confidence the learner reaches under selective records after 3,000 steps, still rising",
      defined_in=here())
    d("sim-train-err-selective",
      lambda q: sim.training("selective", 3000, 64, 0.5, 1.0, 5)["calibration-error"],
      "mean |q - p| of the learned policy", fmt=".0%", label="its calibration error",
      defined_in=here())

    # Adoption (section 6).
    def adopt(q, seed_readers, start, substitution):
        return sim.adoption(q["sim-join-cost"], q["sim-gain-over-k"], seed_readers,
                            q["sim-harmful-share"], start, 60, 2000, q["sim-tenure-tau"],
                            substitution, 6)
    d("adopt-theta-star-uniform", lambda q: 2 * q["sim-join-cost"],
      "2 * sim-join-cost (Proposition 11, uniform types)", fmt=".2f",
      label="lowest type that joins under one-sided unraveling", defined_in=here())
    d("adopt-x-low", lambda q: sim.adoption_analytic(q["sim-join-cost"], q["sim-gain-over-k"])["x-low"],
      "(1 - sqrt(1 - 8 c / a)) / 2 (Proposition 12)", fmt=".1%",
      label="tipping point: share of agents with records below which adoption collapses", defined_in=here())
    d("adopt-x-high", lambda q: sim.adoption_analytic(q["sim-join-cost"], q["sim-gain-over-k"])["x-high"],
      "(1 + sqrt(1 - 8 c / a)) / 2 (Proposition 12)", fmt=".0%",
      label="share of agents with records in the high equilibrium, uniform types", defined_in=here())
    d("adopt-seed-threshold", lambda q: 2 * q["sim-join-cost"],
      "2 * sim-join-cost (Proposition 12)", fmt=".0%",
      label="share of seed readers above which the no-adoption equilibrium disappears", defined_in=here())
    d("sim-adopt-low-noseed", lambda q: adopt(q, 0.0, q["sim-start-low"], 0.0)["final-share"],
      "agent-based, no seed readers, low start, no substitution", fmt=".0%",
      label="share with records after 60 periods", defined_in=here())
    d("sim-adopt-high-noseed", lambda q: adopt(q, 0.0, q["sim-start-high"], 0.0)["final-share"],
      "agent-based, no seed readers, high start, no substitution", fmt=".0%",
      label="share with records after 60 periods", defined_in=here())
    d("sim-adopt-low-seed", lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], 0.0)["final-share"],
      "agent-based, seed readers, low start, no substitution", fmt=".0%",
      label="share with records after 60 periods", defined_in=here())
    d("sim-population-mean", lambda q: adopt(q, 0.0, q["sim-start-low"], 0.0)["population-mean"],
      "mean type of all agents, harmful included", fmt=".2f",
      label="terms every agent would get if nobody could be told apart", defined_in=here())
    d("sim-harm-payoff-nosub", lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], 0.0)["harmful-payoff"],
      "harmful actors' mean realised payoff over the last 20 periods, joining allowed, no substitution",
      fmt=".2f", label="what a harmful actor earns, joining and leaving at will, when business cannot move",
      defined_in=here())
    d("sim-harm-payoff-partial",
      lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], q["sim-substitution-partial"])["harmful-payoff"],
      "the same with partial substitution", fmt=".2f",
      label="what a harmful actor earns, with partial substitution", defined_in=here())
    d("sim-harm-payoff-full", lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], 1.0)["harmful-payoff"],
      "the same with full substitution", fmt=".2f",
      label="what a harmful actor earns, with full substitution", defined_in=here())
    d("sim-harm-switch", lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], 0.0)["harmful-switch-share"],
      "share of harmful actors changing state each period, last 10 periods", fmt=".0%",
      label="harmful actors that join or leave each period (identity cycling)", defined_in=here())

    def adopt_instant(q, substitution):
        return sim.adoption(q["sim-join-cost"], q["sim-gain-over-k"], q["sim-seed-readers"],
                            q["sim-harmful-share"], q["sim-start-low"], 60, 2000, 0.0,
                            substitution, 6)
    d("sim-harm-payoff-instant-nosub", lambda q: adopt_instant(q, 0.0)["harmful-payoff"],
      "harmful payoff when a record reveals type at once (tau = 0), no substitution", fmt=".2f",
      label="what a harmful actor earns if records revealed type at once, business fixed",
      defined_in=here())
    d("sim-harm-payoff-instant-full", lambda q: adopt_instant(q, 1.0)["harmful-payoff"],
      "harmful payoff when a record reveals type at once (tau = 0), full substitution", fmt=".2f",
      label="what a harmful actor earns if records revealed type at once and business moved freely",
      defined_in=here())
    d("sim-readers-final", lambda q: adopt(q, q["sim-seed-readers"], q["sim-start-low"], 0.0)["final-readers"],
      "share of relying parties reading records at the end, seed case", fmt=".0%",
      label="relying parties that read records", defined_in=here())

    # Measured on regtest (lab/): what a release, a veto and a chain proof cost.
    d("tick-release-cost-2026", lambda q: q["lab-advance2-vbytes"] * q["feerate-2026"],
      "lab-advance2-vbytes * feerate-2026", "sats", fmt=",.0f",
      label="fee for a Tier 2 release at the 2026 median fee rate", defined_in=here())
    d("tick-release-cost-halving", lambda q: q["lab-advance2-vbytes"] * q["feerate-halving"],
      "lab-advance2-vbytes * feerate-halving", "sats", fmt=",.0f",
      label="the same at the fee rate of the halving block", defined_in=here())
    d("veto-cost-halving", lambda q: q["lab-veto-package-vbytes"] * q["feerate-halving"],
      "lab-veto-package-vbytes * feerate-halving", "sats", fmt=",.0f",
      label="fee for a veto package at the halving block's fee rate", defined_in=here())
    d("tick-releases-per-day-max", lambda q: q["vbytes-per-day"] / q["lab-advance2-vbytes"],
      "vbytes-per-day / lab-advance2-vbytes", "releases", fmt="sig2",
      label="Tier 2 releases a day if they filled every block", defined_in=here())
    d("tick-identities-max", lambda q: q["vbytes-per-day"] / q["lab-advance2-vbytes"] / (144 / q["tier2-delay-blocks"]),
      "tick-releases-per-day-max / (144 / tier2-delay-blocks)", "identities", fmt="sig2",
      label="identities that could each release every Tier 2 window if they filled every block",
      defined_in=here())
    d("chain-proof-bytes-per-link", lambda q: q["lab-chain-proof-bytes"] / q["lab-chain-links"],
      "lab-chain-proof-bytes / lab-chain-links", "bytes", fmt=",.0f",
      label="proof bytes per link on regtest, where Merkle branches are one or two hashes deep",
      defined_in=here())

    # The veto under censorship (section 1).
    d("veto-miss-tier2-half", lambda q: q["veto-censor-share"] ** q["tier2-delay-blocks"],
      "veto-censor-share ^ tier2-delay-blocks", fmt=".1%",
      label="chance a Tier 2 window passes with no block that would mine the veto", defined_in=here())
    d("veto-miss-tier3-half", lambda q: q["veto-censor-share"] ** q["tier3-delay-blocks"],
      "veto-censor-share ^ tier3-delay-blocks", fmt=".0e",
      label="the same for a Tier 3 window", defined_in=here())
    d("sim-veto-miss-tier2",
      lambda q: sim.veto_censorship(int(q["tier2-delay-blocks"]), q["veto-censor-share"], 200_000, 7)["p-miss"],
      "simulated share of 200,000 windows", fmt=".1%",
      label="the Tier 2 figure, by simulation", defined_in=here())
    d("block-energy-mwh",
      lambda q: q["hashrate-eh"] * 1e6 * q["asic-efficiency-j-th"] * q["block-interval-s"] / 3.6e9,
      "hashrate-eh * 1e6 * asic-efficiency-j-th * block-interval-s / 3.6e9", "MWh", fmt=",.0f",
      label="energy the network spends on one block", defined_in=here())
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
