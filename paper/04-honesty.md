# Honesty as the cheapest strategy

A record is worth having only if a good one is cheap to earn honestly and expensive to fake. This
section shows that a complete record has that property for forecasts, with a bound that holds
whatever the faker does, and that it strengthens the older logic of bonds and reputation for
promises. Neither argument assumes that the agent values honesty. Both assume only that it prefers
more standing and more sats to fewer, which almost any goal gives it a reason to do
[@omohundro2008; @turner2021].

## Faking a record of forecasts

Let an identity forecast distinct events, committing forecast q_t for event t in an entry created
before the event resolves, and let b_t be the public baseline for that event. Its score after T
resolved events is the likelihood ratio of its forecasts against the baseline, the product over t
of q_t(y_t) / b_t(y_t), where y_t is the outcome. Call an identity **without edge** if, given
everything known before each event resolves, the outcome follows the baseline.

**Theorem 1.** For an identity without edge, whatever its strategy (adaptive, or coordinated with
other identities), the probability that its score ever reaches λ is at most 1/λ. An adversary that
controls K identities, none with edge, gets at least one score of λ or more with probability at most
K/λ, so a success probability of π needs at least πλ identities and costs at least πλ times the
cost of one identity.

The proof is two lines. Given the past, each factor q_t(y_t)/b_t(y_t) has expectation one under the
baseline, so the score is a nonnegative martingale starting at one, and Ville's inequality bounds
the chance that such a process ever reaches λ by 1/λ [@ville1939; @shafer2019]. A union bound over
identities gives K/λ. The bound is tight: the old fraud of sending opposite predictions to 2^m
recipients, so that one of them sees m correct calls, meets it with certainty.

The numbers are steep. At the reference cost of
[13,000 sats](../research/numbers.md#identity-cost-sats) an identity (the return forgone on the
bond for a year at [5%/yr](../research/numbers.md#capital-cost-rate), plus two transactions' fees), an
all-correct record of [20 claims](../research/numbers.md#fake-record-claims) against a baseline of
one half has a score of about [1,000,000](../research/numbers.md#fake-record-lambda), and faking it
with even odds needs [520,000 identities](../research/numbers.md#fake-record-identities) and at least
[70 BTC](../research/numbers.md#fake-record-cost-btc). An honest identity that knows the true
probabilities, with an average edge of [0.12 nats](../research/numbers.md#sim-skilled-edge) per
claim, reaches the same score in a median of [116 claims](../research/numbers.md#sim-skilled-claims)
in simulation, with one identity. A simulated faker running
[256 identities](../research/numbers.md#sim-identities) reached a score of 2^10 in
[22.9%](../research/numbers.md#sim-fake-p) of trials, under the bound of
[25.0%](../research/numbers.md#sim-fake-bound).

The theorem needs each rule of section 3, and fails without it. If misses can be dropped after the
fact, the product over the kept claims is no longer a martingale, and in simulation one identity
reached the same 2^10 by showing only its hits after about
[20 claims](../research/numbers.md#sim-selective-claims). If an identity may forecast one event
twice, the expectation of the product can exceed one: with a baseline of one half and two forecasts
that both put probability one on the same outcome, it is two. If the baseline is worse than public
information, identities that merely read public information well look skilled; the bound measures
edge over the baseline and nothing else. And if outcomes are resolved by a captured party, nothing
here holds.

## Why the record sorts and a bond does not

Signalling sorts types only when the signal costs bad types more than good ones [@spence1973]. A
bond fails that test: sats cost an honest and a dishonest principal the same, so a bond says that
someone with money stands behind an agent and nothing about the agent. A complete record passes it.
The honest, skilled identity produces its record as a by-product of acting, at the cost of one
identity; the identity without edge must buy the same record with a number of identities that grows
in proportion to the score. The bond's job in Escapement is only to make identities cost something.
The record does the sorting.

## Promises

For promises the logic is older and the record's contribution is narrower. If breaking a promise
forfeits a stake s with probability a (the adjudicator's accuracy) and, with probability p, costs
the standing V that future partners would otherwise have extended, then keeping a promise worth G
to break is the agent's best response whenever G is at most a(s + pV). This is the reputation
argument of Klein and Leffler and of Shapiro [@klein1981; @shapiro1983]. A complete record makes p
equal to one for every partner who checks, and a costly identity is the remedy Friedman and Resnick
proposed for cheap pseudonyms, which otherwise force everyone to distrust newcomers [@friedman2001].
The stake needed to make honesty the best response therefore falls as standing grows.

The limits are the classical ones. Near the end of an identity's life its standing is worth little,
and the last promises need a stake that covers the whole gain on its own: the exit scam. A gain
larger than stake plus standing is not deterred by anything in this section; that is the
judgment-proof problem, and for catastrophic harms no feasible bond solves it [@polinsky2005;
@shavell1986]. The caps and delays of section 8 are what Escapement relies on there.
