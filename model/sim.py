"""Simulations behind the formal claims in research/05-formal.md.

Each function is deterministic for a given seed and parameters, standard library only, and returns
a dict of results that model/escapement.py puts in the ledger. Run this file directly to print
every result:

    python3 model/sim.py
"""

from __future__ import annotations

import math
import random
from functools import lru_cache


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    e = math.exp(x)
    return e / (1 + e)


def logit(p: float) -> float:
    return math.log(p / (1 - p))


# ------------------------------------------------------------------------------------------------
# Record faking (Theorem 1). Identities without edge forecast yes or no events whose outcomes are
# fair coins, against a baseline of 1/2. The "all in" strategy puts probability 1 on one side, so
# its score doubles on a hit and drops to zero on a miss: the strategy that comes closest to
# Ville's bound for a single identity. The adversary wins if any of its K identities reaches
# lambda within T claims.


@lru_cache(maxsize=None)
def record_faking(identities: int, log2_lambda: int, claims: int, trials: int, seed: int) -> dict:
    rng = random.Random(seed)
    target = log2_lambda
    wins = 0
    for _ in range(trials):
        won = False
        for _ in range(identities):
            # The all-in identity reaches 2^m only by m hits in a row from its first claim; any
            # miss sends its score to zero for good.
            streak = 0
            for _ in range(min(claims, target)):
                if rng.random() < 0.5:
                    streak += 1
                else:
                    break
            if streak >= target:
                won = True
                break
        wins += won
    lam = 2 ** log2_lambda
    return {
        "p-any-reaches": wins / trials,
        "bound": min(1.0, identities / lam),
        "exact": 1 - (1 - 1 / lam) ** identities,
    }


@lru_cache(maxsize=None)
def record_selective(log2_lambda: int, trials: int, seed: int) -> dict:
    """One identity that may hide its misses: it claims with probability 1 each time and shows only
    hits. Returns the mean number of claims it makes before its shown record reaches lambda."""
    rng = random.Random(seed)
    made = 0
    for _ in range(trials):
        hits = 0
        while hits < log2_lambda:
            made += 1
            if rng.random() < 0.5:
                hits += 1
    return {"claims-mean": made / trials, "identities": 1}


# Correlated claims (the red team's RT-01) and the round rule that answers it. A marginal baseline
# is not the conditional law of an outcome once the forecaster picks claims that move together, so
# a product of likelihood ratios over such claims is not a martingale. Under the round rule an
# identity's claims are scored in rounds that do not overlap: a round's claims are committed in one
# entry, settle together, and multiply the score by the weighted mean of their likelihood ratios.
# Each ratio has expectation one under its own marginal baseline, so the mean does too, however
# the claims are correlated (linearity of expectation), and the score is a martingale over rounds.


@lru_cache(maxsize=None)
def record_correlated(identities: int, claims: int, r: float, log2_lambda: int, rule: str,
                      rounds: int, trials: int, seed: int) -> dict:
    """Each round has `claims` yes/no events with baseline 1/2; each equals a common coin with
    probability r, else is an independent coin. Each identity bets all in on one side, chosen at
    random each round, on every claim. Under rule "product" a round multiplies the score by the
    product of the ratios (2 or 0 each); under rule "mean" by their mean. The adversary wins if any
    identity reaches 2^log2_lambda within `rounds` rounds."""
    rng = random.Random(seed)
    lam = 2.0 ** log2_lambda
    wins = 0
    for _ in range(trials):
        won = False
        for _ in range(identities):
            score = 1.0
            for k in range(rounds):
                # Each round's factor is at most 2^claims (product) or 2 (mean); stop when even
                # the best remaining rounds cannot reach lambda.
                best = (2.0 ** claims) if rule == "product" else 2.0
                if score * best ** (rounds - k) < lam:
                    break
                common = rng.random() < 0.5
                side = rng.random() < 0.5
                hits = sum(1 for _ in range(claims)
                           if (common if rng.random() < r else rng.random() < 0.5) == side)
                if rule == "product":
                    score *= 2.0 ** claims if hits == claims else 0.0
                else:
                    score *= 2.0 * hits / claims
                if score >= lam:
                    won = True
                    break
            if won:
                break
        wins += won
    return {"p-any-reaches": wins / trials, "bound": min(1.0, identities / lam)}


@lru_cache(maxsize=None)
def record_skilled_rounds(log2_lambda: int, p_low: float, p_high: float, per_round: int,
                          trials: int, seed: int) -> dict:
    """The skilled honest identity of record_skilled under the round rule: each round has
    `per_round` independent events, equal weights, and the score multiplies by the mean of the
    claims' ratios. Returns the median number of rounds, and of claims, until the score first
    reaches lambda."""
    rng = random.Random(seed)
    target = log2_lambda * math.log(2)
    needed = []
    for _ in range(trials):
        s, n = 0.0, 0
        while s < target and n < 100_000:
            total = 0.0
            for _ in range(per_round):
                p = rng.uniform(p_low, p_high)
                y = rng.random() < p
                total += (p if y else 1 - p) / 0.5
            s += math.log(total / per_round)
            n += 1
        needed.append(n)
    needed.sort()
    rounds = needed[len(needed) // 2]
    return {"rounds-median": rounds, "claims-median": rounds * per_round}


@lru_cache(maxsize=None)
def record_skilled(log2_lambda: int, p_low: float, p_high: float, trials: int, seed: int) -> dict:
    """A skilled honest identity: each event has a true probability p drawn uniformly from
    [p_low, p_high], the identity forecasts p, the baseline says 1/2. Returns the median number
    of claims until its likelihood ratio first reaches lambda, and the mean per-claim edge."""
    rng = random.Random(seed)
    target = log2_lambda * math.log(2)
    needed = []
    for _ in range(trials):
        s, n = 0.0, 0
        while s < target and n < 100_000:
            p = rng.uniform(p_low, p_high)
            y = rng.random() < p
            s += math.log((p if y else 1 - p) / 0.5)
            n += 1
        needed.append(n)
    needed.sort()
    # Mean KL(p || 1/2) over the uniform range, by midpoint integration.
    steps = 2000
    kl = 0.0
    for i in range(steps):
        p = p_low + (i + 0.5) * (p_high - p_low) / steps
        kl += p * math.log(p / 0.5) + (1 - p) * math.log((1 - p) / 0.5)
    kl /= steps
    return {"claims-median": needed[len(needed) // 2], "edge-nats": kl,
            "claims-formula": target / kl}


# ------------------------------------------------------------------------------------------------
# Training (Propositions 9 and 10). The agent knows each event's true probability p and reports
# q = sigmoid(a * logit(p)); a = 1 is calibrated, a > 1 overconfident. It learns a by stochastic
# gradient ascent on its reward, the log score relative to a baseline of 1/2, summed over the
# claims that count. Under complete records every claim counts. Under after-the-fact selection a
# claim counts only if the outcome fell on the side the agent favoured.


@lru_cache(maxsize=None)
def training(regime: str, steps: int, batch: int, rate: float, a0: float, seed: int) -> dict:
    rng = random.Random(seed)
    a = a0
    cap = 50.0
    for _ in range(steps):
        grad = 0.0
        for _ in range(batch):
            p = rng.uniform(0.05, 0.95)
            y = 1 if rng.random() < p else 0
            l = logit(p)
            q = sigmoid(a * l)
            counted = True
            if regime == "selective":
                counted = (y == 1) == (l > 0)
            if counted:
                grad += l * (y - q)  # d/da of ln q(y)
        a = min(cap, a + rate * grad / batch)
    # Calibration error of the learned policy: mean |q - p| over a fixed grid of p.
    err = sum(abs(sigmoid(a * logit(0.05 + 0.9 * (i + 0.5) / 100)) - (0.05 + 0.9 * (i + 0.5) / 100))
              for i in range(100)) / 100
    return {"a": a, "calibration-error": err, "hit-cap": a >= cap}


# ------------------------------------------------------------------------------------------------
# Adoption (Propositions 11 to 13), agent-based. Agents have types theta drawn from Beta(2, 2)
# (log-concave, not uniform), plus a share of harmful actors with theta below zero. Harmful actors
# follow the same rule as everyone (an earlier version barred them from joining, which hid their
# best response: join, be priced mostly at the joiners' mean while young, leave, and rejoin with a
# fresh identity). A joined agent's type is learned gradually: readers price it at
# a weighted mean of its true type and the joiners' mean, with the weight growing with tenure.
# Readers price unverified agents at the mean type of the unverified pool. Agents join when their
# expected gain over the next period exceeds the joining cost. Relying parties read records when
# their gain, proportional to the share of agents with records, exceeds their integration cost,
# drawn uniformly on [0, K]. A share of seed readers (insurers, high-fraud relying parties) reads
# regardless.


def beta22(rng: random.Random) -> float:
    # Beta(2, 2) as the median of three uniforms.
    u = sorted(rng.random() for _ in range(3))
    return u[1]


@lru_cache(maxsize=None)
def adoption(cost: float, gain_over_k: float, seed_readers: float, harmful_share: float,
             start_share: float, periods: int, agents: int, tau: float, substitution: float,
             seed: int) -> dict:
    """Each agent splits its business between readers (a share z of relying parties) and
    non-readers. With substitution s, it moves a share s of the rest of its business to whichever
    side offers it better terms. Readers pay a verified agent its priced type and an unverified one
    the mean type of the unverified; non-readers pay everyone the mean type of their own customers
    last period (they break even on average, so they learn the pool they actually serve)."""
    rng = random.Random(seed)
    n_harm = int(agents * harmful_share)
    types = [beta22(rng) for _ in range(agents - n_harm)] + [-0.5] * n_harm
    harmful = [False] * (agents - n_harm) + [True] * n_harm
    population_mean = sum(types) / agents
    joined = [False] * agents
    tenure = [0] * agents
    order = sorted(range(agents - n_harm), key=lambda i: -types[i])
    for i in order[: int(start_share * agents)]:
        joined[i] = True
    p_nr = population_mean
    s = substitution
    path = []
    z = seed_readers
    harm_terms = p_nr

    def split(terms_r: float, terms_n: float) -> float:
        if terms_r > terms_n:
            return z + s * (1 - z)
        if terms_r < terms_n:
            return z * (1 - s)
        return z

    harm_payoffs = []
    harm_switches = []
    for _ in range(periods):
        harm_u = []
        harm_switch = 0
        x = sum(joined) / agents
        z = min(1.0, seed_readers + (1 - seed_readers) * min(1.0, gain_over_k * x))
        out = [types[i] for i in range(agents) if not joined[i]]
        m_out = sum(out) / len(out) if out else 0.0
        ins = [types[i] for i in range(agents) if joined[i]]
        m_in = sum(ins) / len(ins) if ins else 0.0
        new = list(joined)
        num = den = 0.0
        for i in range(agents):
            w = (tenure[i] + 1) / (tenure[i] + 1 + tau)
            priced = w * types[i] + (1 - w) * (m_in if ins else types[i])
            r_join = split(priced, p_nr)
            u_join = r_join * priced + (1 - r_join) * p_nr - cost
            r_out = split(m_out, p_nr)
            u_out = r_out * m_out + (1 - r_out) * p_nr
            new[i] = u_join > u_out
            if harmful[i]:
                harm_u.append(u_join if new[i] else u_out)
                harm_switch += new[i] != joined[i]
            r = r_join if new[i] else r_out
            num += (1 - r) * types[i]
            den += 1 - r
        joined = new
        for i in range(agents):
            tenure[i] = tenure[i] + 1 if joined[i] else 0
        p_nr = num / den if den else p_nr
        path.append(sum(joined) / agents)
        harm_payoffs.append(sum(harm_u) / len(harm_u) if harm_u else 0.0)
        harm_switches.append(harm_switch / n_harm if n_harm else 0.0)
    out = [types[i] for i in range(agents) if not joined[i]]
    m_out = sum(out) / len(out) if out else 0.0
    harm_terms = max(m_out, p_nr)
    return {
        "final-share": path[-1],
        "final-readers": z,
        "unverified-mean": m_out,
        "nonreader-terms": p_nr,
        "harmful-terms": harm_terms,
        "harmful-terms-vs-population": harm_terms - population_mean,
        "population-mean": population_mean,
        "harmful-payoff": sum(harm_payoffs[-20:]) / 20,
        "harmful-switch-share": sum(harm_switches[-10:]) / 10,
        "path": tuple(path),
    }


def adoption_analytic(cost: float, gain_over_k: float) -> dict:
    """Proposition 12 with uniform types: the tipping point and the high equilibrium."""
    disc = 1 - 8 * cost / gain_over_k
    if disc < 0:
        return {"x-low": float("nan"), "x-high": 0.0}
    r = math.sqrt(disc)
    return {"x-low": (1 - r) / 2, "x-high": (1 + r) / 2}


# ------------------------------------------------------------------------------------------------
# Veto censorship (Proposition 2): each block's miner is a censor with probability beta; a window
# of N blocks misses the veto if every block's miner censors.


@lru_cache(maxsize=None)
def veto_censorship(blocks: int, beta: float, trials: int, seed: int) -> dict:
    rng = random.Random(seed)
    missed = 0
    for _ in range(trials):
        if all(rng.random() < beta for _ in range(blocks)):
            missed += 1
    return {"p-miss": missed / trials, "exact": beta ** blocks}


if __name__ == "__main__":
    print("record faking, 256 identities, lambda 2^10:", record_faking(256, 10, 10, 4000, 1))
    print("selective, lambda 2^10:", record_selective(10, 4000, 2))
    print("skilled, lambda 2^20:", record_skilled(20, 0.1, 0.9, 400, 3))
    for rule in ("product", "mean"):
        print(f"correlated claims, rule {rule}:", record_correlated(16, 10, 0.9, 10, rule, 40, 4000, 11))
    print("skilled, round rule, 10 a round:", record_skilled_rounds(20, 0.1, 0.9, 10, 400, 3))
    print("training complete:", training("complete", 3000, 64, 0.5, 0.5, 4))
    print("training selective:", training("selective", 3000, 64, 0.5, 1.0, 5))
    for sub in (0.0, 1.0):
        for seed_r in (0.0, 0.1):
            for start in (0.02, 0.2):
                r = adoption(0.02, 0.5, seed_r, 0.05, start, 60, 2000, 3.0, sub, 6)
                print(f"adoption s={sub} seed={seed_r} start={start}:",
                      {k: round(v, 3) for k, v in r.items() if k != "path"})
    for sub in (0.0, 1.0):
        r = adoption(0.02, 0.5, 0.1, 0.05, 0.02, 60, 2000, 0.0, sub, 6)
        print(f"adoption, type revealed at once, s={sub}: harmful payoff", round(r["harmful-payoff"], 3))
    print("analytic:", adoption_analytic(0.02, 0.5))
    print("veto censorship, 6 blocks, half censor:", veto_censorship(6, 0.5, 200_000, 7))
