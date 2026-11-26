# What a record can prove

A record is worth having only if a good one is cheap to earn with real skill and expensive to fake.
This section shows that a complete record has that property for forecasts, under a condition on the baseline stated below, and that it adds less to the older logic of bonds and
reputation for promises than one might hope. Neither argument assumes that the agent values
honesty. Both assume only that it prefers more standing and more sats to fewer. Omohundro argues
that most goals give an agent a reason to acquire resources [@omohundro2008], and Turner and
colleagues prove that, for optimal policies in environments with certain symmetries, most reward
functions make it optimal to keep options open [@turner2021]. The same argument says an agent values
not being stopped, so escaping its guardians may be worth more to it than any stake.

## Faking a record of forecasts

An identity's forecasts are scored in rounds that do not overlap: a round's claims are committed in
one entry, the round settles when the last of them resolves, and the next round's claims count only
if their entry comes after that. Each claim has a forecast q, a weight w committed with it (a round's
weights sum to one) and a baseline b published by an independent party. When the round settles, the
identity's score is multiplied by the weighted mean of the claims' likelihood ratios, the sum of
w·q(y)/b(y) over its claims, where y is each claim's outcome.

The condition the bound needs, **H0**, constrains the baseline and the agent together. Each
baseline is the law of its outcome given everything public when the round opens, including the
forecasts other identities have disclosed; the agent's forecasts and weights use only that public
information; and its actions do not move the outcomes. The first part is an efficient-market
assumption about the baseline that no relying party can check. The second is what it means to have
no edge. The third the scheme cannot check either. An earlier draft of this paper called H0 a
property of the baseline alone, which was wrong.

**Theorem 1.** Under H0, for any strategy that uses only what is public when each round opens and
does not move outcomes (adaptive, coordinated with other identities, or built on claims that move
together), the probability that an identity's score ever reaches λ is at most 1/λ. An adversary with K identities gets at least one score of λ or more with probability
at most K/λ, so a success probability of π needs at least πλ identities and costs at least πλ times
the cost of one identity.

The proof is short. Given the past, each claim's ratio has expectation one under its baseline, so a
weighted mean of them does too, by linearity of expectation, whatever the joint law of the outcomes;
in the language of testing by betting, a mean of e-values is an e-value under any dependence
[@vovk2021].
The score is therefore a nonnegative martingale over rounds starting at one, and Ville's inequality
bounds the chance that such a process ever reaches λ by 1/λ [@ville1939; @shafer2019]. A union bound
over identities gives K/λ. The bound is tight: the old fraud of sending opposite predictions to 2^m
recipients, so that one of them sees m correct calls, meets it with certainty.

None of this is new. A round's factor is the return on a unit stake split across bets at the
baseline's odds, which is Shafer's testing by betting [@shafer2021]; the bound is Ville's inequality
and a union bound; comparing an expert with a second forecaster by likelihood is Al-Najjar and
Weinstein's comparative test [@alnajjar2008], made sequential and anytime-valid by Choe and Ramdas
[@choe2024]; and pricing the lucky accounts of a many-identity attack with stakes is how Numerai
answered it [@craib2021numerai]. What this section adds is the application to a Bitcoin record.

## Why rounds and means

The first version of this design multiplied every claim's ratio, and read H0 as "the agent has no
edge". The red team broke it. A marginal baseline, such as a market price for each claim on its own,
is not the conditional law of an outcome once the agent chooses claims that move together. With
claims that mostly follow one common coin, [16 identities](../research/numbers.md#sim-corr-identities) each betting one side of every claim reached a score of 2^10 in
[99.8%](../research/numbers.md#sim-corr-product-p) of simulated trials, against Theorem 1's bound of
[1.6%](../research/numbers.md#sim-corr-bound). And a single identity that made [1,000 claims](../research/numbers.md#tail-claims) of "no failure" on sub-events that all fail together in one event of
probability [1%](../research/numbers.md#tail-fail-p) scored about
[23,000](../research/numbers.md#tail-product-score), 99% of the time.

That second attack is the objection Foster and Young raised against track records in finance: a
manager without skill can buy a good-looking record by taking hidden tail risk, so return histories
cannot separate the skilled from the unskilled [@foster2010]. The product rule did not escape it. The
round rule does, for forecasts: the same correlated attack succeeded in
[1.1%](../research/numbers.md#sim-corr-round-p) of trials, inside the bound, and the tail-risk
record scored [1.01](../research/numbers.md#tail-round-score). It does so without anyone having to
decide which claims are correlated, which is what the alternative, one claim per cluster of related
events, would need.

The repair has a cost the red team did not see. With more than one claim in a round the round rule
is a betting score, not a proper score: the report that grows it fastest is not the truth. With ten
independent claims of true probability [0.60](../research/numbers.md#edge-p) against a baseline of [0.50](../research/numbers.md#edge-b), a
truthful report grows the score [0.037 nats](../research/numbers.md#round-growth-truthful) a round, and a report of
[0.999](../research/numbers.md#round-best-report) on each grows it [0.143 nats](../research/numbers.md#round-growth-best) (Proposition 7b of the
formal statements). An identity that wants standing bets; it does not forecast. Its reports cannot be
read as probabilities unless each round holds one claim, which is proper but slow, or each leaf
carries a forecast and a separate stake.

The price is speed. An identity that knows each event's probability when the best public forecast
is one half (private knowledge, which is what edge means here), with a mean edge of
[0.12 nats](../research/numbers.md#sim-skilled-edge) a claim, reaches a score of 2^20 in a median
of [116 claims](../research/numbers.md#sim-skilled-claims) made one a round, or
[74 rounds](../research/numbers.md#sim-skilled-rounds) of
[10 claims](../research/numbers.md#sim-round-claims), with one identity. That is the most
favourable case: an agent that knows each event's probability against a public forecast that knows
nothing. With a smaller edge, [0.60](../research/numbers.md#edge-p) against a baseline of [0.55](../research/numbers.md#edge-b-close), a
truthful identity needs about [2,722 rounds](../research/numbers.md#rounds-close-single) of one claim, or
[1,449 rounds](../research/numbers.md#rounds-close-ten) of ten. Rounds are serial for one identity and each lasts until
its slowest claim resolves, so with daily events that is years. Rounds, not claims, are the unit of
time a record takes to build.

## The numbers

At the reference cost of [13,000 sats](../research/numbers.md#identity-cost-sats) an identity (the
return forgone on the bond for a year at [5%/yr](../research/numbers.md#capital-cost-rate), plus two
transactions' fees), an all-correct record of [20 claims](../research/numbers.md#fake-record-claims)
in one-claim rounds against a baseline of one half has a score of about
[1,000,000](../research/numbers.md#fake-record-lambda), and faking it with even odds needs
[520,000 identities](../research/numbers.md#fake-record-identities) and about
[70 BTC](../research/numbers.md#fake-record-cost-btc). That price assumes a one-year bond. With
bonds locked only for the season the same fake costs about [21 BTC](../research/numbers.md#fake-record-cost-season-btc),
and either price assumes one chain per bond, which section 3 shows is not yet enforced. A simulated faker running
[256 identities](../research/numbers.md#sim-identities) reached a score of 2^10 in
[22.9%](../research/numbers.md#sim-fake-p) of trials, under the bound of
[25.0%](../research/numbers.md#sim-fake-bound); that run checks the arithmetic of one strategy and
adds no evidence beyond the theorem.

## What breaks the bound

Each rule of section 3 is needed, and so is H0.

- **Private information or influence.** An agent that knows more than the public, or can move an
  outcome, is outside the theorem. An agent that can make an outcome equal its forecast multiplies
  its score by 1/b each round, so influence over outcomes breaks standing exactly as it breaks
  training (section 5).
- **Copying.** If the baseline ignores forecasts other identities have disclosed, an identity that
  copies a skilled one shows edge it does not have. A baseline with a known public bias does the
  same for anyone who corrects it.
- **One bond, many chains.** Until a chain is bound to its bond, one bond can back many chains,
  and the price per identity does not hold (section 3).

- **Dropping misses.** If misses can be dropped after the fact, the product over the kept claims is
  not a martingale; in simulation one identity reached 2^10 by showing only its hits after about
  [20 claims](../research/numbers.md#sim-selective-claims).
- **Two forecasts on one event.** With a baseline of one half and two forecasts that both put
  probability one on the same outcome, the expected product is two.
- **A bad baseline.** A stale baseline, one in a thin market the agent can move, one the agent or
  the scorer chose, or one on events the agent wrote itself all make apparent edge cheap. A market baseline
  counts only with a stated depth and averaging window, and the bound then holds only up to the cost
  of moving the market. The event list, the baseline and the resolvers are therefore run by parties
  that relying parties have to trust, which section 7 returns to.
- **Too many identities.** Among a million identities without edge, one may reach a score of a
  million by luck. A score means something only when λ exceeds the number of identities in use, and
  relying parties cannot observe that number, since an operator's identities are unlinked by
  design.
- **A sold record.** A record stays with its keys, and keys can be sold.

## What a record of forecasts separates

Signalling sorts types only when the signal costs bad types more than good ones [@spence1973]. A
bond fails that test: sats cost every principal the same, so a bond says that someone with money
stands behind an agent and nothing about the agent. A complete record passes it for one trait,
**edge over the stated baseline**: the identity with edge produces its record as a by-product of
forecasting, at the cost of one identity, while the identity without edge must buy the same record
with a number of identities that grows in proportion to the score. It does not separate honesty. A
forecaster without edge earns nothing by being honest, and an honest one with no edge looks the
same as a dishonest one with none. The bond's job is only to make identities cost something; the
record does the sorting, on the one trait it can see.

That trait is the wrong one for safety. Edge is a product of capability, which a misaligned agent
has as much as an aligned one, and standing brings access. A record of forecasting edge therefore
routes trust fastest to the most capable agents, whatever their goals. It measures what an agent can
do, not what it wants.

## Promises

For promises the logic is older and the record's contribution is narrower still. If the adjudicator finds a breach with probability a (its accuracy), and a breach it finds forfeits a stake s and, with probability p, costs the standing V that future partners would otherwise extend, then keeping a promise worth G to
break is a best response whenever G is at most a(s + pV). This is the reputation argument: Klein and
Leffler's condition that a firm which breaks faith loses a stream of future rents larger than its
gain, and Shapiro's price premium that repays an investment in reputation [@klein1981; @shapiro1983].
A complete record makes p equal to one for every partner who checks, provided adjudicators publish
their verdicts on chains of their own. A bond is an entry fee of the kind Friedman and Resnick
discuss for cheap pseudonyms and set aside, because it excludes some players, in favour of free but
unreplaceable pseudonyms [@friedman2001].

Who holds a promise's stake is not specified here. The identity bond can be spent only by the
principal after its timelock, so it cannot be forfeited; a forfeitable stake needs a separate
coverage bond with an adjudicator's spending path (section 8), whose custody and payout this paper
leaves open.

Two limits keep this modest. First, a record of kept promises can be faked by wash trading: an agent
makes promises to its own sybil counterparties, judged by a sybil adjudicator, keeps them all, and
pays only fees. So promise history counts only against an agent, as a record of breaches, never for
it, and V grows only through forecasting edge and age. Second, the condition holds promise by
promise, for promises whose gain G the enforcement layer caps. Near the end of an identity's life
its standing is worth little and the last promises need a stake that covers the whole gain on its
own: the exit scam, which has already been modelled for AI agents that can abandon identities
[@gatta2026]. A gain larger than stake plus standing is not deterred, which is the judgment-proof
problem [@shavell1986]; for catastrophic harms we see no feasible bond that would solve it. And an
agent whose aims are not monetary is not deterred by money. The caps and delays of section 8 are
what Escapement relies on there.
