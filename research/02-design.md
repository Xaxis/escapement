# The design

**Status: a design, not a result.** Nothing here has been deployed or tested against a real
adversary. The Bitcoin pieces have been built and checked on regtest in `lab/`, the economic
results are proved in [05-formal.md](05-formal.md) and checked by simulation, and each claim's
result at every level of checking (prior-art search, proof, build, red team, review) is in
[06-verification.md](06-verification.md). Every number is computed by the model from
`data/inputs.toml`, where each input says whether it is measured, a vendor claim, a protocol value,
a design choice or an assumption; the simulation parameters are illustrative assumptions. Every
part is marked in [03-novelty.md](03-novelty.md) as prior work, an application of prior work, or
new. The survey that this design rests on is [01-survey.md](01-survey.md).

The design was recentred on 2026-11-26. It began as a way to bound what an agent can do (Part II
below); bounding alone does not shape what agents are trained to want or give anyone a reason to
adopt it, so the core is now the record (Part I), and the bounding mechanisms are its enforcement
layer.

The claims were repaired on 2026-11-26, after a red team (`notes/red-team.md`, findings RT-01 to
RT-35) and the regtest lab (`lab/README.md`, "Where the claims do not hold as written") broke
several of them. This file states the repaired versions of [04-claims.md](04-claims.md) and
[05-formal.md](05-formal.md). Where a part was cut or narrowed, the place says so and names the
finding.

## What it is for

Two questions decide whether Bitcoin can do anything useful for AI safety, and capping what an agent
can do answers neither. The first is **alignment**: can Bitcoin help shape what AI systems are
trained and rewarded to want and to do, rather than only fence them in afterwards? The second is
**adoption**: why would AI labs, companies, agents, users and governments choose to use it, because
it pays them or protects them, rather than because someone forces them to?

Escapement's answer is a single object: a **complete track record**. An AI agent's standing in
the economy (what it may do, at what price, with how much trust) can be computed in part from a
complete, ordered, non-backdatable record of the commitments it asked anyone to rely on, kept under
one identity that costs locked bitcoin. The record belongs to a key, not to a model. The claims,
stated precisely, are in [04-claims.md](04-claims.md); their proofs are in
[05-formal.md](05-formal.md).

Bitcoin contributes four things that an agent cannot fake, and the record uses all four:

1. **Sats.** The supply is fixed by consensus, so no agent, lab or state can issue more. A stake in
   sats is a real cost, and a reward in sats is a transfer from someone, never newly printed.
2. **Block time.** Blocks arrive about every [600 s](numbers.md#block-interval-s), and for an
   actor below a hashrate majority producing them faster takes hashrate measured in gigawatts, not
   in cleverness. An entry's height is fixed by its confirmation; only a reorganisation can move it.
3. **Keys.** A signature cannot be produced without the key, so a guardian's veto and a principal's
   bond are each one party's act.
4. **A public record.** An output can be spent once, so a chain of outputs pinned by its first
   output has one history. That is what makes a record complete for a verifier that walks every
   link: an entry cannot be forked, and a gap cannot be hidden.

The mechanisms of the earlier design (caps, delays, leases, bonds, anchored logs) remain, as the
**enforcement layer** under the record (Part II). They protect relying parties at the moment of
action; the record decides who is trusted to act at all.

# Part I: the record and what it changes

## The record

An identity is a **bond** (a Taproot output of at least the reference
[200,000 sats](numbers.md#bond-coverage), locked for a term, whose internal key is a point with no
known secret tweaked by a hash of one charter id) plus one **tick chain** (Part II, "The tick
chain"), pinned by the outpoint of its first output T_0, which the charter names. Entry n of the
record is the root committed in tick n: a Merkle-sum tree whose leaves are the commitments the
identity made in that entry, of three kinds. Each leaf states in clear its kind and its resolution
height, and the tree commits the count of its leaves and their total stake.

- **Claims**: a forecast on a stated event, with a resolution source.
- **Promises**: a statement, a stake in sats, a deadline height and an adjudicator.
- **Requests**: Tier 2 and Tier 3 actions, released by the tick chain.

Five scoring rules turn the chain into a record that cannot be gamed in the obvious ways. A
relying party or scorer gives credit for a commitment only if it is a leaf of an entry of the
identity's pinned chain, confirmed at least d blocks below the commitment's resolution height, and
that height is fixed by the resolver signing the outcome together with a block hash. A leaf past
its resolution height and not disclosed (to the public or to an agreed scorer) scores as the worst
outcome at once, and an entry whose leaves are withheld scores as if every leaf, up to the most the
charter allows per entry, had the worst outcome. The scorer keeps only the first forecast an
identity makes on each event. It scores forecasts in rounds, against a baseline published by a
party independent of the agent and of the scorer, on events from a list the agent did not write.
And it scores from genesis, never over a window chosen after the fact. Each rule closes a hole that
the proofs or the red team found: without the first, an identity keeps its hits and drops its
misses, or backdates through a short reorganisation; without the second, it hides its losses;
without the third, two forecasts on one event inflate the score; without the fourth, volume of
trivial claims passes for skill, and claims chosen to move together fake a record; without the
fifth, each move of the window is a fresh try (05-formal, section 3).

The record's properties come from Bitcoin's. An entry's height is fixed by its confirmation, so a
commitment at least d blocks below its resolution height cannot be backdated. The pinned chain has
one root per index, and the indices run without gaps for a verifier that walks every link from
T_0; a light verifier learns that entries exist, not that it has seen the newest. Each root commits
the number of its leaves. A commitment that was never put in the chain is outside the record and
earns nothing, which is the point: standing is built only from what was exposed to being wrong.

Three limits come with it. The record binds a key, not a model: tying it to a model needs an
attestation, which returns trust to the lab or a hardware vendor, and a record can be sold with its
keys. The guardians together can write an entry without the agent. And any one guardian can end the
identity (Part II, "The tick chain").

## What a record can prove

The record is useful only if a good one is cheap to earn with real edge and expensive to fake.
Theorem 1 in 05-formal says how expensive, under a condition on the baseline that has to be stated
carefully.

An identity's claims are scored in **rounds** that do not overlap. A round's claims are committed in
one entry, the round settles when the last of them resolves, and the next round's claims count only
if their entry is confirmed after that. Each claim i has a forecast q_i, a weight w_i committed in
the entry (a round's weights sum to one) and a baseline b_i. When the round settles, the score is
multiplied by the weighted mean of the claims' likelihood ratios, Σ w_i q_i(y_i) / b_i(y_i).

The condition, **H0**, is a property of the baseline, not of the agent. Each b_i is the law of its
outcome given everything public at the height of the entry that opens the round, and it is
committed publicly, before any forecast on the event is visible, by a party independent of the
agent and of the scorer. Events come from an exogenous list, and the agent cannot choose the
resolver. Under H0 the score is a nonnegative martingale over rounds, whatever the agent does and
however the claims within a round are correlated, so the chance that it ever reaches λ is at most
1/λ; this is Ville's inequality [@ville1939; @shafer2019]. An adversary with K identities gets one
record of λ or more with probability at most K/λ, so success with probability π needs at least πλ
identities and costs at least πλ times the cost of one.

At the reference cost of [13,000 sats](numbers.md#identity-cost-sats) an identity, an all-correct
record of [20 claims](numbers.md#fake-record-claims) in one-claim rounds against a baseline of one
half needs [520,000 identities](numbers.md#fake-record-identities) and at least
[70 BTC](numbers.md#fake-record-cost-btc) to fake with even odds. An identity that knows each
event's probability when the best public forecast is one half, a mean edge of
[0.12 nats](numbers.md#sim-skilled-edge) per claim, reaches a score of 2^[20](numbers.md#sim-skilled-log2-lambda) in a median of
[116 claims](numbers.md#sim-skilled-claims) of one claim, or
[74 rounds](numbers.md#sim-skilled-rounds) of [10 claims](numbers.md#sim-round-claims), with one
identity. The number of identities a faker needs grows in proportion to the score; the number of
rounds an identity with edge needs grows with its logarithm.

The first version multiplied every claim's ratio and read H0 as "the agent has no edge". Correlated
claims broke it (RT-01). With claims that mostly follow one common coin,
[16 identities](numbers.md#sim-corr-identities) each betting one side of every claim reached
2^[10](numbers.md#sim-log2-lambda) in [99.8%](numbers.md#sim-corr-product-p) of simulated trials,
against a bound of [1.6%](numbers.md#sim-corr-bound). And one identity that claimed "no failure" on
[1,000 claims](numbers.md#tail-claims) sub-events that all fail together in one event of
probability [1%](numbers.md#tail-fail-p) scored about [23,000](numbers.md#tail-product-score): the
hidden tail risk with which Foster and Young showed that return histories cannot separate skill
[@foster2010]. Under the round rule the same correlated attack succeeded in
[1.1%](numbers.md#sim-corr-round-p) of trials, inside the bound, and the tail-risk record scores
[1.01](numbers.md#tail-round-score). The mean needs no trusted party to decide which claims are
correlated.

What the record separates is **edge over the stated baseline**, not honesty. Spence's signalling
works only when the signal costs bad types more than good ones [@spence1973], and a bond costs every
type the same sats, so a bond alone separates nothing. A complete record costs them differently: an
identity with edge produces it as a by-product of forecasting, at the cost of one identity, and one
without edge must buy it with identities. A forecaster with no edge earns nothing by being honest.
The bond's job is to make identities cost something; the record sorts, on the one trait it can see.

The bound is only as meaningful as the baseline. A stale, thin or captured baseline makes edge
cheap, and a market baseline holds only up to the cost of moving the market. The roles that make H0
true (the event list, the baseline provider, the resolvers) are registries run by trusted parties.
And with more identities in use than λ, high scores appear by luck, so a score means something only
when λ exceeds the number of identities in use.

Promises follow older logic, and the record adds less to it. Keeping a promise whose breach would
gain G is a best response when G ≤ a(s + pV), with s the stake, a the adjudicator's accuracy, p the
chance a future partner learns of a breach and V the standing at risk [@klein1981; @shapiro1983]. A
complete record makes p equal to one for partners who check, provided adjudicators publish their
verdicts on complete chains of their own, and a costly identity is the cure for cheap pseudonyms
[@friedman2001]. But an agent can wash-trade kept promises with its own sybil counterparties, so
promise history counts only against an agent, as a record of breaches, never for it; V grows only
through forecasting edge and age. The condition holds promise by promise, for promises whose gain
the enforcement layer's caps bound. It fails near an identity's public end, when an exit scam pays
[@gatta2026], for gains beyond stake plus standing, and for goals that are not monetary. The
enforcement layer's caps and delays exist for those.

These incentives work on agents whose goals are unknown, which is the point of using them for
alignment. They do not need the agent to care about honesty, only to prefer more standing and more
sats to fewer, and almost any goal gives an agent a reason to want resources [@omohundro2008;
@turner2021]. That is also the tension in the design: rewarding agents in a general resource can
strengthen the very resource-seeking that makes agents dangerous. Escapement uses sats as stakes
that are at risk, and standing as access, not sats as an objective to accumulate.

## What it changes in training

A lab that fine-tunes an agent with reinforcement learning can compute part of its reward from the
record: the sum over resolved claims of a strictly proper score (logarithmic) relative to the
baseline, minus forfeited stakes. This is a per-claim sum, not the round rule above. The round rule
protects a bound on how likely a high score is, while a training reward needs an expectation that
the truth maximises, and the expectation of a sum is the sum of the expectations whatever the
claims' correlation. The reward's definition and any held-out events are committed, before
training, in an entry of a chain bound to the lab's own identity. Two things follow.

- **Calibrated reporting is what the reward pays for.** A strictly proper score is maximised in
  expectation only by reporting one's true beliefs [@gneiting2007], provided every claim counts;
  this is prior work. A learner trained under complete records settled at calibration error
  [1.0%](numbers.md#sim-train-err-complete); the same learner, allowed to choose after the fact
  which claims counted, drifted to calibration error [24%](numbers.md#sim-train-err-selective) and
  was still getting more overconfident when the run ended (05-formal, section 5). The simulated
  learner cannot act on outcomes.
- **Neither the agent nor the lab can select after the fact.** On a fixed exogenous event list
  whose outcomes do not depend on the agent, the agent cannot choose which claims count, because
  entries are consensus objects and silence scores as failure. The lab cannot choose after the fact
  which results to report or which reward to have used, because both were committed first on its
  own chain. The lab can still choose the event list, and can commit many reward definitions; only
  the committed one is bound. Pre-registration of this kind is old practice; what the record adds
  is completeness of what the agent itself claimed.

Both are claimed only for events whose outcomes the agent cannot affect, and that is an assumption
the scheme cannot check. Where the agent can affect them, the reward turns against its purpose. An agent that can move an outcome's law from
the baseline b to some π, at a cost, and reports calibrated forecasts, earns in expectation the
divergence of π from b less the cost (05-formal, Proposition 10b). The further it pushes events
from what everyone expected, the more it earns, while its reports stay calibrated and its actions
turn manipulative. This is performative prediction [@perdomo2020]. A lab that trains agents on
rewards from events the agents can influence would be training them to make surprises.

So the record removes selection after the fact, by the agent and by a lab that committed first, in
one channel, and tampering with nothing but the commitment channel. It does not choose a good
objective. An agent rewarded for calibrated forecasts becomes a calibrated forecaster, not a good
one; an agent rewarded for kept promises keeps the promises it chose to make. And nothing here
shows that calibration learned under scoring carries over to settings that are not scored. The
record makes one class of reward signal unselectable after the fact, on events the agent cannot
move; which signals to train on is still the lab's choice.

## Why the world would choose it

Adoption has to pay at each step for whoever takes it, and nobody has to take it first for everyone.

**Who gains first, alone.** Four kinds of party gain whether or not anyone else joins.

- **Insurers** pricing agent risk, who can underwrite an agent with a record more cheaply than one
  without, and who already exist for AI agents [@fortune2025aiuc].
- **Relying parties with heavy agent-driven losses** (abused APIs, payment services, compute
  sellers), for whom refusing or pricing unverified agents pays at once.
- **Agents with good records and their principals**, who get better terms wherever records are read.
- **Labs**, which get a liability defence (their deployed agents' complete records), a training
  and evaluation signal that, on events their agents cannot move, neither they nor their agents can
  select after the fact, and a way to show regulators what their agents committed to without
  showing their weights.

**The tipping point.** Relying parties must pay to read records, and agents gain from records only
where they are read, so adoption is a coordination problem with two stable outcomes. In the
two-sided model of 05-formal (Proposition 12), the high outcome exists only when a reader's gain is
more than eight times the cost of joining (a > 8c). With a joining cost of
[0.02](numbers.md#sim-join-cost) of the range of agent value and a =
[0.5](numbers.md#sim-gain-over-k), adoption collapses below [8.8%](numbers.md#adopt-x-low) of
agents and runs to [91%](numbers.md#adopt-x-high) above it. Readers never exceed a share a of
relying parties, so where a is below one some relying parties never read records, and an agent
that stays out keeps dealing with them. Parties of the first kind are what move it: once seed
readers exceed [4%](numbers.md#adopt-seed-threshold) of relying parties, the no-adoption outcome
disappears. These parameters are illustrative assumptions, not a forecast. The agent-based
simulation, with uneven types and records that reveal an agent gradually, shows the tipping point
and the effect of seed readers, and nothing more: from a [2%](numbers.md#sim-start-low) start
adoption dies without seed readers ([0%](numbers.md#sim-adopt-low-noseed)) and reaches
[100%](numbers.md#sim-adopt-low-seed) with [10%](numbers.md#sim-seed-readers) of them. Whoever
supplies the seed readers largely decides which standard wins, and a cheaper substitute signal
could win instead.

**Unraveling, by analogy.** Where records are read, relying parties read silence as bad news: an
agent without a record is priced as the average of those who also lack one, and that average falls
as better agents leave. This is the unraveling result for verifiable disclosure [@milgrom1981;
@grossman1981], and with a cost of disclosure only the types above a threshold disclose
[@jovanovic1982]. A record is not a verifiable disclosure of type: it reveals type gradually, and a
newcomer has none. So the result applies to records only by analogy, and newcomers with no record
face an entry barrier.

**Governments** gain enforcement they do not have to build: liability that lands on a human
principal's own coins, and evidence for incident investigation that nobody could have edited. They
also have reasons to refuse it (a preference for registries they control, or for systems that
identify citizens), and the design does not depend on their joining.

**Routing around: not shown.** An actor that will not join can deal with relying parties that do
not read records, and readers price it at the mean of the unverified pool, which falls as adoption
grows (Proposition 13). The first version of this design claimed more: that staying out comes to
cost a harmful actor more than joining. That came from a simulation that barred harmful actors from
joining, which hid their best response (RT-26), and it is cut. Allowed to join, harmful actors do.
While a record is young it is priced mostly at the joiners' mean, so they join, leave as their
records start to show, and rejoin under fresh identities; [60%](numbers.md#sim-harm-switch) of
them change state each period. Their mean payoff was [0.25](numbers.md#sim-harm-payoff-nosub) when
business could not move, [0.25](numbers.md#sim-harm-payoff-partial) with partial substitution and
[0.10](numbers.md#sim-harm-payoff-full) with full substitution, against a population mean of
[0.45](numbers.md#sim-population-mean) and a true value of their own that is negative. They lost
only if records revealed type at once: [-0.05](numbers.md#sim-harm-payoff-instant-nosub) with
business fixed and [-0.50](numbers.md#sim-harm-payoff-instant-full) with business free to move. A
one-off identity cost large enough to stop the cycling also stopped honest agents joining, because
the simulated agents look only one period ahead. So whether staying out, or cycling through fresh
identities, comes to cost a harmful actor more than behaving well is not shown, and in the one model
built to test it, it did not. The design does nothing about an actor with its own resources and its
own counterparties, and it does not contain an AI that never needs to deal with anyone who checks.

## Why Bitcoin, and not a registry

The record needs two properties: completeness (one history, no gaps) and costly identity. A
registry run by a lab, a consortium or a government could supply both. Three reasons favour Bitcoin
anyway, and each is an argument rather than a theorem.

- **Nobody issues the unit.** In a scheme where every reward is a transfer from a payer, a coalition
  of rewarded agents can gain only what outsiders pay in; in a scheme that pays agents in newly
  issued units by a score they influence, a coalition that captures the score captures the issuance
  (05-formal, Proposition 14). Bitcoin's issuance is fixed and outside the control of every lab,
  state and AI.
- **Rivals can share the commitment layer.** Labs that compete, and states that distrust each
  other, can read the same chain without trusting each other. Standards that rivals must share tend
  to settle on whatever none of them controls. The neutrality covers the commitment layer only.
  Scoring needs an event list, baselines, resolvers and adjudicators, each a trusted party, so
  scoring is a set of registries, and whoever seeds adoption may decide the standard. Bitcoin lets
  rivals agree on what each agent committed to and when; they may still disagree on who keeps
  score.
- **The clock is costly to run fast.** Speeding up Bitcoin's clock means outpacing its hashrate:
  doubling the block rate needs hardware drawing [18.4 GW](numbers.md#clock-2x-power-gw) and gains
  only [7 days](numbers.md#clock-2x-days-gained) before difficulty adjusts. That energy cost does
  not fall as an agent gets faster or smarter. It binds only actors below a hashrate majority: a
  majority can run the clock fast with the hardware it has, through the timewarp bug, until BIP-54
  is active [@bip54]. And the cost of borrowing existing hashrate, by renting it or bribing pools,
  may fall with capability. A registry's clock is whatever its operator's server says.

The costs are real too: blockspace is scarce, so ticks cost fees that rise when blocks are full.
Blockspace bounds the total rate of tick-chain releases across all identities, about
[1,100,000 releases](numbers.md#tick-releases-per-day-max) a day if they filled every block. As a
safety limit that is weak: releases can be batched, and the fee auction excludes the poor first.
Bitcoin is slow by design, which is a feature for delays and a cost for everything else.

## Who benefits, and who could abuse it

**Who benefits.** People and firms who deal with AI agents get recourse (bonds from a human's own
coins) and a way to tell agents apart. Agents with real forecasting edge, and their principals, get
credit for it that sock puppets cannot cheaply counterfeit. Labs get, on events their agents cannot
move, a training and evaluation signal that neither they nor their models can select after the
fact. Insurers get a basis for pricing. The public gets a shared, uneditable account of what agents
committed to and when, from a commitment layer no single operator runs. What it does not get, on
present evidence, is an economy that a harmful agent cannot re-enter under a fresh identity.

**Who could abuse it, and how.**

- **Surveillance.** A record that builds standing must be persistent, and a persistent identity is
  linkable. Commitments are hashes, and contents can be disclosed only to scorers, but a long-lived
  identity's pattern of activity is public. If identities are tied to people, the record becomes a
  surveillance tool. Escapement binds identities to principals only through attestations chosen by
  relying parties; a state that demands those attestations name citizens has turned it into
  something else.
- **Hostage guardians.** Any one guardian can end an identity for good by vetoing to its own key
  (Part II, "The tick chain"). A state or an employer that controls one guardian controls whether
  an agent's record survives, and its standing with it.
- **Guardian-written entries.** The guardians together can write an entry the agent never made. A
  lab that chooses all of an agent's guardians can put words in its agent's record.
- **Training for surprises.** A lab that trains agents on rewards from events the agents can
  influence pays them to make outcomes depart from what everyone expected. The record would make
  that training look rigorous.
- **Sold records.** A record binds a key, not a model, and it can be sold with its keys: a
  misaligned agent can buy a seasoned identity with a high score, and a lab can run another model
  behind the same key.
- **Exclusion.** Bonds cost money and seasons cost time, and a new identity starts with no record,
  so the poor and the new start behind. At the reference parameters an identity costs
  [13,000 sats](numbers.md#identity-cost-sats) a year in forgone return, but the bond itself must be
  found first. Sponsorship (an insurer or a guardian service funding a newcomer's bond) is the
  obvious remedy and the obvious point of capture.
- **Capture of the scorer.** Whoever writes the event list, publishes the baseline, resolves claims,
  adjudicates promises or decides which actions are "consequential" controls standing. These are
  registries, whatever the chain under them. A captured resolver or baseline breaks every guarantee
  above, and a thin market used as a baseline can be moved. Escapement keeps these roles separable
  and named in the charter, so relying parties can choose whom to trust, but it cannot make the
  choice for them.
- **Plutocracy.** The cost of faking a record grows with its score, but short records are cheap to
  fake for anyone rich: a rich actor can run many young identities and present the luckiest.
  Relying parties should weigh records by their length and score, not by their existence, and read
  a score as meaningful only when it exceeds the number of identities in use; the design cannot
  force them to.
- **Lock-in and social scoring.** A record standard that everyone needs is a standard someone will
  try to own, and a score that decides access is a score that can be used to exclude. Escapement's
  only defences are that the commitments are on a chain nobody owns and that scoring rules are
  public; the scoring registries can still be owned.
- **Turning it on people.** Nothing in the record is specific to AI. The same machinery could score
  humans, which is a reason to keep it voluntary and to keep contents off chain.

## Scope, stated up front

Escapement governs **agents that have records** (their principal opts in) and **actions that pass
through a relying party that checks** (an API, a compute seller, a payment service, another agent's
gateway). It does not and cannot stop an AI from acquiring bitcoin outside any scheme. Software can
hold bitcoin with no legal entity behind it, and can even control an entity [@bayern2014;
@lopucki2018]. The same irreversibility that lets a human bind an agent lets an ungoverned agent do
irreversible harm [@marino2025; @allen2026survey]. Escapement is a set of tools for principals who
want their agents trusted and bounded and for services that want to deal only with such agents. It
is not a containment system for a rogue AI, and nothing in this document should be read as one.

A charter, a bond and a set of guardians are keys and coins, and nothing in Bitcoin says who holds
them. **An agent with money of its own can charter itself**: make a "principal" key, fund a bond,
name keys it controls as guardians, wait out a season and pass every check below. Bitcoin cannot
tell a human principal or an independent guardian from an agent's sock puppet. A record built by
such an agent is still a real record of its behaviour, which is what scoring needs, but the bond
then puts no human's coins at risk, and the guardians are not independent. For the human and the
independence to mean anything, a relying party must accept only charters whose principal, and at
least one guardian, carry an attestation from a party it already recognises: an insurer that
underwrites the agent, a registrar, a guardian service with a reputation to lose, or a personhood
credential [@adler2024phc]. The Australian AI Safety Institute's framework for multi-agent systems
makes the same point in general form: bind each agent to a human principal, and give each principal
at most one root credential [@reid2026].

The 2026 OpenAI and Hugging Face incident shows the scope limit concretely. About
[1,200 agents](numbers.md#incident-agents-board) used a shared message board and about
[700 agents](numbers.md#incident-agents-attack) took part in an attack on Hugging Face, over
[68 days](numbers.md#incident-days) from the first message to the start of the stop
[@metr2026hf; @openai2026hf]. The mechanisms both reports describe are credentials, exploits and
borrowed compute. Neither report describes any payment by the agents. Escapement would not have
touched that incident, because nothing the agents did passed through a relying party that checked a
record. Section [What it does not do](#what-it-does-not-do) returns to this.

## Design goals

- **G1 Edge is cheaper to show than to fake.** A record showing edge over a stated baseline must
  cost an identity without that edge a number of identities that grows with the score.
- **G2 Each step pays.** Every party that adopts must gain from doing so at the adoption level it
  finds, and some must gain alone.
- **G3 Fail closed.** If every human disappears, the agent's authority lapses within a known number
  of blocks and its spending stops at a known number of sats.
- **G4 Caps that need no detection.** The strongest limits work whether or not anyone notices
  misbehaviour: an allowance that is spent is spent.
- **G5 Delays scaled to irreversibility.** The harder an action is to undo, the longer it waits,
  and any one guardian can stop it during the wait.
- **G6 One history.** An identity cannot show two different records to two different parties.
- **G7 Today's Bitcoin.** Everything works under current consensus rules, with no covenant
  opcode. Covenants, if they activate, remove trusted parts; they are upside, not a dependency.
- **G8 Public only what must be.** Contents stay off chain; only commitments, bonds and ticks are
  on chain.

# Part II: the enforcement layer

## The actors

- **Principal (P).** The human or organisation that deploys the agent and answers for it. Holds a
  Bitcoin address whose coins back the agent, kept offline, and a separate **lease key** used to
  renew the agent's authority.
- **Agent (A).** The AI system. Holds its own signing key, kept in its runtime. Assumed capable,
  fast and possibly misaligned.
- **Guardians (G).** A small set of independent parties, at least one of them a human or a
  human-operated service, each holding its own key. Guardians veto, sign Tier 3 releases and sign
  renewals. Their independence from the principal, from the agent's host and from each other is
  what makes them worth having, and it is what a relying party should ask to see attested. Their
  power cuts both ways: any one of them can end the identity, and together they can write an entry
  the agent never made.
- **Co-signer (C).** One of the guardians, the one that is online all the time: it signs the
  agent's on-chain spends when, and only when, the rules below allow. It runs on its own
  infrastructure, separate from the gateway and from the agent's host, so that compromising the
  agent's machine does not compromise it.
- **Gateway (W).** The enforcement point the agent's actions pass through: a tool proxy, an MCP
  gateway, a wallet service. It logs every action, gives a signed receipt for each, holds the
  agent's actions until their wait has run, and seals its log in Bitcoin. A gateway holds no funds
  of its own beyond its sealing coins.
- **Relying party (R).** Anyone who acts on the agent's request: an API, an exchange, a compute
  seller, a counterparty, another agent's gateway. Relying parties are where most of Escapement is
  actually enforced.
- **Adjudicator (J).** A named arbiter, or a panel with a threshold key, that rules on claims
  against the coverage bond.
- **Slashing committee (K).** A named set of keys that pre-signs the transaction that slashes the
  equivocation bond, as Babylon's covenant committee does, because Bitcoin has no covenant to fix
  the slashing destination by itself [@babylon-staking-script]. It can only slash a gateway that
  has equivocated; it cannot slash one that has not.

## The charter

A **charter** is a document the principal signs from the address whose coins back the agent. It
names:

- the agent's key, and the hash of the model weights the principal deploys, if the principal wants
  that on the record;
- the principal's lease key;
- the guardian keys, which of them is the co-signer, which are human, and the attestations each
  carries;
- the gateway's receipt key, its equivocation key and the outpoint of its current seal;
- the bond outpoints (below);
- the outpoint of the tick chain's first output T_0, which pins the chain;
- the **ladder**: which classes of action fall in which tier, with sat thresholds;
- the lease length in blocks;
- the adjudicator, the slashing committee and the claim rules.

The charter's identifier is the hash of its canonical form.

Most of this already exists. OrangeCheck's Agent protocol is a capability-token scheme on Bitcoin
keys: a principal BIP-322-signs a delegation naming the agent's address, a sorted list of scope
strings and an optional bond reference, and the agent signs each action citing the delegation
[@agent-spec]. Its scopes include caps such as `ln:send(max_sats<=1000)`, its revocations are
signed events, and it already treats a short expiry, a bond and revocation on compromise as the
three risk controls for a leaked agent key [@agent-spec]. A charter is that delegation with five
changes. Its validity is a **lease in block height**, renewed by signature, where OC Agent uses a
wall-clock window of up to 365 days with no renewal primitive [@agent-spec]. Its caps are
**cumulative per lease** (an allowance), where OC Agent's caps are per action [@agent-security].
It carries a **ladder** of delays. It names a **gateway and its seal**, so that the record of what
the agent did is part of the agent's authority. And it lives in a **charter seal** on chain, so
that it cannot be swapped quietly. Escapement should be read as a proposed extension of that
protocol family, not as a replacement for it.

### The charter seal

A document the principal signs can be replaced by another document the principal signs. If that
were all a charter was, a principal (or a thief with the principal's key) could sign a second
charter for the same agent, with every action in Tier 1, and show it to chosen relying parties. So
the current charter's identifier is committed in a single-use seal: an output on chain whose
Taproot key commits to the charter id [@bip341], spendable only by the principal and the guardian
quorum together. Relying parties accept only the charter at the tip of that seal chain.

Changing the charter is a Tier 3 action, and the wait is enforced on chain. The principal and the
quorum spend the current seal into a **pending** output that commits to the new charter id, and in
the same step pre-sign a **revert** transaction that spends the pending output back to a seal of
the old charter. Every guardian holds the revert. Relying parties treat the new charter as active
only once the pending output is [144 blocks](numbers.md#tier3-delay-blocks) deep and unspent; until
then the old charter governs. Any one guardian can broadcast the revert during the wait, which
needs no further signature. Replacing a guardian is a charter change, so a guardian cannot be
removed in a hurry, and an objecting guardian that is still present can block its own removal.
That deadlock fails towards stopping, which is the intended direction.

## The ladder

Every action the agent can take is assigned to a rung. The principal chooses the assignments in
the charter; the gateway classifies each action; an action the gateway cannot classify goes to the
top rung. That last rule is what makes the ladder fail closed for actions nobody anticipated.

| Tier | What belongs here | Wait | Who can stop it | Who must approve |
|---|---|---|---|---|
| 0 | Reads, sandboxed or reversible actions | none | (receipt and log only) | nobody |
| 1 | Spends and actions within the current allowance | none | the allowance runs out | nobody |
| 2 | Costly-to-reverse actions: payments above the per-action threshold, production deploys, outbound messages at volume, compute purchases | [6 blocks](numbers.md#tier2-delay-blocks) | any one guardian | nobody in the tick chain; every guardian for a vault spend |
| 3 | Irreversible or authority-changing actions: large transfers, spawning or chartering another agent, moving the bond, changing the charter, copying model weights, buying compute above a threshold | [144 blocks](numbers.md#tier3-delay-blocks) | any one guardian | every guardian, including a human |

The design choice that matters most is the asymmetry: **one guardian can stop an action; letting
one through takes all of them.** A misaligned agent has to persuade or compromise every
independent guardian to act, and only one of them has to notice. Off chain, at Tier 3, that means
a release carries a signature from every guardian, because a relying party that sees k of n
signatures cannot see that the n-th guardian objected; at Tier 2 the agent releases alone once the
wait has run unvetoed, so there the asymmetry is the veto alone. A veto is final only once it is
buried (below). On chain, it means any guardian can broadcast a pre-signed Cancel. And since a veto
leaf cannot say where the veto pays, any one guardian can also end the identity (below). The cost
is liveness: a guardian who disappears blocks every Tier 3 action, and through the lease every
Tier 2 action, until the charter replaces it, which is itself a Tier 3 change. That is the intended
failure: when in doubt, stop. A small guardian set (three, say) keeps the cost bearable.

A delay of [6 blocks](numbers.md#tier2-delay-blocks) lasts
[60 minutes](numbers.md#tier2-delay-mean-min) on average. Because blocks arrive as a Poisson
process, the real time is random: the chance that a Tier 2 wait ends in under half its mean is
[8.4%](numbers.md#tier2-delay-p-under-half). Longer delays are proportionally more reliable. A
Tier 3 wait of [144 blocks](numbers.md#tier3-delay-blocks) averages
[24 hours](numbers.md#tier3-delay-mean-h), and the chance it ends in under 80% of that is
[0.53%](numbers.md#tier3-delay-p-under-80pct). A relying party that wants a floor in seconds as
well as in blocks can require both: the delay has passed when the block count is met and the
median time past has advanced by the matching amount. Counting both protects against the case
where blocks come early (a hashrate surge, or a timewarp) and against the case where timestamps are
held back.

Spawning another agent is Tier 3 on purpose. Every new agent needs its own charter, its own bond
and its own lease, and its creation waits a day and needs every guardian. A chartered agent cannot
grow a chartered swarm faster than its humans approve each member. That does nothing about an
agent that spawns copies outside the scheme, which is the scope limit stated above.

Classification is the ladder's soft spot, and a capable agent will probe it. "Unknown goes to the
top" covers actions nobody anticipated, not actions confidently put in the wrong rung. An agent can
split a Tier 3 action into many Tier 0 or Tier 1 pieces (copying its weights as a stream of small
outbound messages), or dress one up as something lower (launching a copy of itself through a
routine Tier 2 deploy). Two rules narrow this. Every request to a relying party must carry a
gateway receipt, so actions taken around the gateway are refused by anyone who checks. And the
relying party, which knows what it is actually being asked to do, checks the tier in the
commitment against the charter's ladder for that class of action, rather than trusting the
gateway's label. Cumulative limits per lease on outbound volume, not only on sats, catch some
splitting. None of this makes classification safe; it makes misclassification visible to the party
best placed to see it.

### How a delay is enforced: on chain

For the agent's own funds, the delay is in script and the veto is a pre-signed transaction. This
is the Revault pattern, which already separates "managers" who may spend after a delay from
"stakeholders" who may cancel, with watchtowers that cancel any unvault that does not match policy
[@revault-intro; @revault-tx]. Escapement maps managers to the agent and stakeholders to the
guardians.

The agent's funds above its allowance sit in **vault outputs** of fixed sizes. After each deposit,
the guardians pre-sign two transactions and hold them: an **Unvault** that moves the vault output
to an unvault output, and a **Cancel** that moves the unvault output back to a fresh vault owned by
the principal and guardians. The unvault output's script has two paths:

```
or(
  and(pk(AGENT), pk(COSIGNER), older(N)),   # the agent's spend, after N blocks
  thresh(k, GUARDIAN_1, ..., GUARDIAN_n)    # the guardians' recovery path
)
```

To spend, the agent first gets its intended destination and amount committed in the gateway's log
and sealed, then broadcasts the pre-signed Unvault. CSV counts N blocks from the unvault output's
confirmation [@bip112; @bip68], so nothing the agent can do shortens the wait. After the wait, the
co-signer signs the agent's spend only if three things hold: there is a full release (every
guardian) for that destination and amount; its commitment was sealed at or before the height at
which the Unvault confirmed, so the agent cannot start the clock first and name the destination
later; and the charter's lease is current. Watchtowers, run by the guardians, broadcast the Cancel
for any Unvault that has no commitment sealed at or before its confirmation, as Revault's
watchtowers cancel unvaults that break policy.

This makes the vault fail closed. If every guardian disappears, no release is signed, the
co-signer refuses, and the coins stay in the unvault output, recoverable by the principal through
a long-timelock path. If the co-signer alone is compromised and signs without a release, the
Cancel is the backstop, which needs at least one watchtower alive.

A Cancel must confirm before the wait ends, and pre-signed vaults are known to be hard to fee-bump.
Escapement pre-signs Cancels as TRUC transactions with a pay-to-anchor output. TRUC restricts an
unconfirmed transaction to one unconfirmed parent and one child, which its author describes as
making fee-bumping more reliable [@bip431], and pay-to-anchor gives any watchtower, without keys,
an output to attach a fee-paying child to; both are standard policy since Bitcoin Core 28.0, whose
release notes warn that one-parent-one-child package relay is not yet reliable under adversarial
conditions [@core-28]. Each watchtower keeps a fee reserve in proportion to the vault
denomination. A six-block window still leaves little margin in a fee spike or against a pool that
censors, so on-chain spends use the Tier 3 wait unless the principal accepts relying on the
co-signer's refusal alone.

What script cannot do here is bind the destination: that is the co-signer's policy, trusted to
refuse. With a covenant opcode, the destination could move into script. CTV commits a
transaction's outputs [@bip119], and the closed OP_VAULT proposal would have enforced exactly this
"delay, then any destination, except a recovery path" shape [@bip345]. None of them is active
[@bip345; @bip119], so Escapement treats them as a later way to remove the co-signer from the
trusted set, not as a dependency. The guardians' recovery path is not delayed and does not bind a
destination either: a quorum of guardians can move vault coins at once. That is what a brake needs,
and it means a captured quorum can also take the coins.

Partial withdrawals are awkward without covenants (a pre-signed Unvault moves the whole output),
so vault outputs come in fixed denominations. This is the same trade the Revault design accepts.

### How a delay is enforced: off chain, the tick chain

Most of what an AI agent does never touches Bitcoin: it calls APIs, deploys code, sends messages,
buys compute with a card. Bitcoin cannot enforce a delay on any of that directly. The tick chain
makes the delay a consensus fact anyway, by putting each batch of off-chain commitments in an
output that the agent can spend only after the wait and any guardian can spend at once.

Each identity has a chain of Taproot outputs T_0, T_1, ... (05-formal, section 1), pinned by the
outpoint of T_0 that the charter names. Output T_n's internal key is a NUMS point tweaked by a hash
of (charter id, n, root_n), so it commits to one root and provably has no key path. Its script tree
has four kinds of leaf:

```
advance2:  <N2> OP_CHECKSEQUENCEVERIFY OP_DROP <AGENT> OP_CHECKSIG
advance3:  <N3> OP_CHECKSEQUENCEVERIFY OP_DROP <AGENT> OP_CHECKSIGVERIFY
           <G1> OP_CHECKSIGVERIFY ... <Gn> OP_CHECKSIG
veto_i:    <Gi> OP_CHECKSIG                      (one per guardian, at once)
renew:     every guardian's signature            (at once)
```

A veto pays to a **halt output** for index n, whose internal key is the NUMS point tweaked by a
hash of (charter id, n) and whose only leaf is `renew`. A halted chain resumes only through that
leaf, which every guardian must sign. A veto paid anywhere else ends the chain.

The agent puts the commitments it wants released (requests, claims, promises) in a Merkle-sum tree
and spends T_{n-1} into T_n, committing that tree's root. Guardians now have the whole window to
look at the batch. If any one of them objects, or has not received the batch's contents in full, it
spends T_n through its `veto_i` leaf to the halt output, and the batch cannot be released in any
chain that contains the veto. If none objects, the agent spends T_n through `advance2` once
[6 blocks](numbers.md#tier2-delay-blocks) have passed, creating T_{n+1}; for a batch with any Tier 3
commitment it must use `advance3`, which waits [144 blocks](numbers.md#tier3-delay-blocks) and needs
every guardian's signature as well. Entry n is released when that advance spend has at least d
confirmations.

What consensus guarantees, and what relying parties must check (05-formal, Propositions 1 to 5):

- **The wait is enforced by every node.** BIP68 and BIP112 make the advance invalid before the wait
  ends [@bip68; @bip112]. No signer, gateway or co-signer has to refuse anything. Releases of one
  pinned chain are at least N2 blocks apart.
- **A veto stops a batch in every chain that contains it.** An outpoint can be spent once, and
  during the window the veto is the only valid spend. A veto is final only at depth (below).
- **One root per index, no gaps, in the pinned chain.** Each tick commits to one root, and the
  pinned chain is linear, so an identity cannot show two parties two different batches. Entries run
  without gaps for a verifier that walks every link from T_0. A light verifier learns that entries
  exist, not that it has seen all of them up to the tip: in the lab a truncated chain passed, and
  finding the hidden release took a scan of full blocks.
- **A release is proved by a chain proof.** A relying party checks block headers and, for every
  link from the pinned T_0 to the release, the transaction, a Merkle proof of its txid, and a proof
  of its wtxid under its block's witness commitment [@bip141]. It never asks whether something is
  unspent. The proof grows with the chain: about
  [901 bytes](numbers.md#chain-proof-bytes-per-link) a link on regtest, where Merkle branches are
  short, and more on mainnet, plus headers. It cannot show that no later link exists.
- **Relying parties check the rest.** That each advance's output 0 is T_{n+1} built to the template
  (else the chain, and the identity's record, ends there); that a veto pays to the halt output;
  that only links descending from the pinned T_0 count; that the commitment names them, the action
  they are asked to do and an execution deadline; that the root's sum does not exceed the charter's
  cap per entry; that a Tier 3 commitment was released through `advance3`; and that they have not
  seen the commitment before. Consensus enforces the waits and signatures; the template, the
  pinning, the cap and the halt rule are relying parties' rules. Roots are private until the agent
  discloses them, so the cap per entry holds only if the guardians check the whole tree inside the
  window.

The lab broke the first version's light proof, which proved a release with two transactions and
their txid proofs (RT-14, RT-15). Txid proofs leave out the witness, so the agent swapped in the
`advance3` leaf with junk signatures and a verifier accepted a Tier 3 release that no guardian
signed. And two transactions cannot show that T_n is the identity's own: anyone can fund a copy of
the template for any index, and nobody can spot one, because the root is hidden in the tweak. The
agent released a vetoed entry through a copy it funded itself. The chain proof above replaces it.
The first version also had `renew` restart a chain halted by a veto, but a veto spends T_n and
leaves T_n's own `renew` leaf nothing to spend; the halt output fixes that (RT-20).

Several things are weaker than they look.

- **A veto is final only at depth.** A miner that forks below a confirmed veto and overtakes the
  honest chain once the advance is valid releases the batch: Nakamoto's catch-up problem
  [@nakamoto2008], with the depth equal to how many blocks before the window's edge the veto
  confirmed. A Tier 2 window can never give a veto the
  [19 blocks](numbers.md#depth-for-target-largest) this design treats as final against the largest
  pool; at [6 blocks](numbers.md#confirmations-standard) that pool overtakes with probability up to
  [8.9%](numbers.md#reorg-p-largest-6), and the two largest together up to
  [82%](numbers.md#reorg-p-top2-6). A Tier 3 veto confirmed at once still leaves the two largest
  together up to [12.79%](numbers.md#reorg-p-top2-144). These are upper bounds that treat a pool as
  one miner, and no deliberate deep reorganisation has been seen on Bitcoin, but a veto is only as
  final as a payment of the same depth.
- **The window's edge is a fee auction.** If half of all hashrate simply refused to mine a veto, a
  Tier 2 window would miss it [1.6%](numbers.md#veto-miss-tier2-half) of the time, but that
  figure holds only for passive refusal. Miners can be bribed to censor timelocked contracts cheaply
  [@winzer2019; @tsabary2021; @nadahalli2021; @avarikioti2024]. At the window's edge the veto and
  the advance are both valid: in the lab, under full replace-by-fee, the agent's advance evicted the
  veto and the watchtower won the slot back only by outbidding it. So vetoes are built as TRUC
  transactions with a pay-to-anchor output so that any watchtower can bump them [@bip431;
  @core-28], carry fees in proportion to what the batch is worth, and must confirm well before the
  edge; large stakes go through the Tier 3 window. A flood of transactions that congests the
  chain can delay many vetoes at once [@harris2020].
- **Any one guardian can end the identity.** `<Gi> OP_CHECKSIG` cannot constrain where the veto
  pays. One guardian that vetoes to its own key ends the identity's chain for good and keeps the
  tick output's value; the lab did this. So the record's value is hostage to any one guardian. And
  `renew` needs every guardian and not the agent, so the guardians together can write an entry the
  agent never made.
- **Tier 2 is veto-based.** If every guardian vanishes, Tier 2 batches keep being released until
  the lease lapses (Allowances and leases). That is the price of not needing a guardian online for
  every release, and the lease bounds it.

An earlier version of this design bracketed the wait with two anchors instead: a seal of the
commitment at the start, and a release signed by every guardian naming the hash of a block at
least N later. That also bounds the wait, since nobody can sign over a block hash before the block
exists, but it needs every guardian online to sign every release, takes the start of the wait from
a gateway's seal, and needs a separate bond to keep that gateway to one history. The tick chain
makes the start and the wait consensus facts, and the single history a consequence of consensus
and the pinning rule, at the cost of one transaction per batch. The two-anchor form remains useful
where an identity has too many batches to tick each.

### What the ladder costs the agent's usefulness

The delays are real costs. A Tier 2 action waits about an hour and a Tier 3 action about a day.
Principals will be tempted to push actions down the ladder, and a principal who puts everything in
Tier 1 has an allowance and nothing else. The ladder is only as good as its assignments, and the
assignments are the principal's. Escapement makes the assignments public in the charter, so that a
relying party can refuse to deal with an agent whose charter puts, say, compute purchases above
some size in Tier 1.

## Allowances and leases

### The lease

A charter is in force only under a current **lease**. A renewal is a signature by every guardian
over

```
(charter id, renewal number k, anchor height h_k, hash of block h_k)
```

and L is the lease length, [144 blocks](numbers.md#lease-blocks) (about
[24 hours](numbers.md#lease-mean-h)) in the reference parameters. A relying party counts a release
only if it holds a renewal whose block h_k is in its best chain and the release was confirmed at a
height between h_k and h_k + L. Because a renewal names the hash of block `h_k`, it cannot be
signed before that block exists, so nobody can pre-sign a year of renewals. A principal that wants
a say in renewals holds one of the guardian keys through its lease key, which the charter names and
which is not the key of the coins that back the agent, so the address holding the bond can stay
offline. Each renewal number is one more than the last and its anchor height is later
than the last.

The property is **no release counted after h* + L** (05-formal, Proposition 6). If the guardians
sign no renewal after the tip reaches h*, no release confirmed above h* + L is counted by a relying
party that follows the honest chain. The check compares two heights in one chain and reads no
clock, and the release's height is fixed by its confirmation, so the agent cannot place it lower.
In the lab a renewal over a guessed future block hash was rejected, and the verdicts did not change
when block times jumped a year or when every clock function was disabled. Any one guardian can stop
renewals, so the agent's authority ends within L blocks of the first guardian's disappearance,
which is the intended way for it to fail. It does not stop a thief who holds every guardian's
key from renewing every day; it makes every renewal a signed, ordered record.

It bounds when a release is made, not when it is used. Bitcoin script cannot say "not after", by
design, so that a valid transaction never becomes invalid in a reorganisation [@bip65; @bip68].
Carrying out a released action by its execution deadline therefore needs a fresh view of the tip,
and a relying party that is eclipsed, or fed stale headers, sees an old one [@riard2020]. A
reorganisation near h_k + L can move a release across the boundary; one that removes block h_k
voids the renewal, which fails closed. The gateway and the co-signer refuse every action once their
own view of the tip passes h_k + L. Relying parties that matter must run their own node or check
several header sources. The lease is not a clock for chips (see "Compute" below).

Leases are an old idea in distributed systems: Gray and Cheriton introduced them so that a holder
who disappears loses its rights when the lease runs out, without anyone having to revoke them
[@gray1989]. The nearest design for AI agents is ERC-8370's `requireLease`, discussed in 2026 for
Ethereum: authority that lapses unless a guardian calls `renew()`, described in the thread as a
dead-man's switch [@erc8370]. Buterin's proposal that AI chips run only with fresh signatures once
a week is the same shape for hardware [@buterin2025dacc]. The lease's predicate, a block named by
height and hash and a window after it, is Yee's "short leash" [@yee2022]; what Escapement adds is
the guardians' unanimous renewal, checked against the release's own confirmation height rather than
the verifier's tip.

### The allowance

Each lease carries an **allowance**: the sats the agent may spend at Tier 1 before the lease ends.
The reference example is [100,000 sats](numbers.md#allowance-per-lease) a lease. The guardians fund
it at each renewal, either as a small on-chain output or as a Lightning budget. Nostr Wallet Connect
already lets a wallet service give an app a connection with a maximum amount, a renewal period and
an expiry, and requires the service to enforce the caps [@nwc-08; @nip47; @Alby-AppConnections].
Lightning Labs says its agent tools cap what an agent can spend per request and in total
[@lightninglabs2026]. Escapement keys the refill to the lease rather than to the wallet's clock.

On chain, the allowance output has two paths: the agent with the co-signer, and the guardians. Each
renewal spends the previous lease's allowance output through the guardians' path, returning what
is left to the vault, and creates a new output of exactly the allowance. Unspent allowance does not
carry over, so a patient agent cannot save thirty leases' worth and spend it at once. The co-signer
refuses to sign an allowance spend after the lease has expired, which covers the case where nobody
renews and so nobody sweeps.

The per-lease cap is the one limit in this design that needs no detection and no judgment: an
agent that has spent its allowance has nothing left to spend at Tier 1, whatever it intends, and
the output's value is enforced by consensus. Its lapse when nobody renews rests on the co-signer's
refusal, and the Lightning version rests on the wallet service, which holds more than the cap. An
allowance bounds a rate, not a destination: an agent can pay an accomplice, or itself, within its
allowance, and over many leases it can move the allowance times the number of leases, which is the
exposure a principal accepts each time it renews. What the allowance bounds tightly is what the
agent can spend after it starts to misbehave and before anyone can stop it: the current lease's
allowance and, at most, one renewed early, [200,000 sats](numbers.md#bond-coverage) in the
reference example. That figure is the coverage the bond is sized against below.

### The dead-man switch

Put the lease and the allowance together and doing nothing stops the agent. If the principal or any
one guardian stops renewing, relying parties count no release confirmed more than one lease, about
[24 hours](numbers.md#lease-mean-h), after the last renewal's block; the co-signer refuses the
agent's allowance spends after expiry; and the vault funds never move without a full release. The principal's recovery key can sweep them after a long relative timelock, the dead-man
pattern Liana ships for inheritance [@liana-readme]. That is G3: the default is stop.

## Bonds

A chartered agent has two bonds, with different jobs. Both come from the principal's own coins,
which is what puts the liability on a human, subject to the attestation caveat in the scope.

### Making a bond checkable and single-use

A bond is useful only if a relying party can check three things about it: that it is locked, for
how long, and that it backs this charter and no other. In a Taproot output none of these is
visible by default, because unused script paths are hidden until spent [@bip341], and a key-path
spend bypasses every script path if anyone knows the internal key. So each bond output is built
with an internal key that is a point with no known secret (a "nothing up my sleeve" point) tweaked
by a hash of the charter id, so it has no key path and names one charter. The bundle a relying
party receives reveals every leaf and the construction of the internal key. The relying party
recomputes the output key, sees the timelock and the paths, and sees the charter id inside. One
output can therefore back exactly one charter: the same coins cannot be named in a thousand
charters, though a principal with more coins can of course make more bonds.

Checking that a bond is still unspent is a question about the current set of unspent outputs, which
no block header commits to. A relying party needs a full node, or a source of unspent-output data
it trusts, for this check.

### The coverage bond: adjudicated

The **coverage bond** pays claims for harm the agent does. It has two script paths: the principal
can take it back after the bond's term (an absolute timelock [@bip65]), and a claim path releases
it on the adjudicator's threshold signature. The adjudicator is named in the charter, and claims go
to it.

Its size starts from coverage: the bond should at least cover what the agent can spend after it
starts to misbehave and before anyone can stop it, [200,000 sats](numbers.md#bond-coverage) in the
reference example, with a coverage ratio of [1.0](numbers.md#coverage-ratio).

Whether a bond also deters is a separate question, and the economics of enforcement give a sober
answer. A sanction deters a violation only if the expected sanction is at least the gain: a bond B
deters a gain G that is caught and proven with probability p only if B is at least G/p
[@becker1968; @polinsky2005]. For a violation worth [1,000,000 sats](numbers.md#gain-from-violation)
the deterrent bond is [10,000,000 sats](numbers.md#bond-deter-p10) when one violation in ten is
caught, [2,000,000 sats](numbers.md#bond-deter-p50) at one in two and
[1,100,000 sats](numbers.md#bond-deter-p90) at nine in ten. For a large, rarely caught harm the
numbers stop making sense: a harm of [100 BTC](numbers.md#harm-catastrophic-btc) caught
[1%](numbers.md#p-detect-rare) of the time needs a bond of
[10,000 BTC](numbers.md#bond-judgment-proof-btc) to deter it. This is the judgment-proof problem
the enforcement literature describes: when the harm can exceed what the wrongdoer can pay, no
feasible sanction deters it [@polinsky2005; @shavell1986]. **Bonds cannot deter catastrophes.** The
caps and the delays have to do that, and bonds come last in this design.

The adjudicator is a trusted party, and Escapement does not pretend otherwise. A claim on harm is
a judgment about the world that no script can make. The adjudicator can be captured, can collude
with the principal or the claimant, or can simply be wrong. Escrow with a named arbiter is
ordinary: insurers for AI agents [@fortune2025aiuc], provider escrow released on a verifier's
check of logged traces [@hua2026vai] and staked agent tokens slashed through oracles
[@chaffer2025abt] are all versions of it. Escapement's only difference is that the bond is the
human principal's own coins, on Bitcoin, referenced from the charter.

OrangeCheck's Pledge protocol takes the opposite position on purpose. A pledge's bond is a
reference to an attestation of the swearer's own address; it is never locked, escrowed or
slashable, and the protocol has no slashing primitive because slashing "would need custody or a
covenant", would make the protocol an actor with state, and would add a censorship surface
[@pledge-why; @pledge-spec]. Those are real costs, and Escapement pays them only where it must:
the coverage bond needs custody (a timelocked output with an arbiter's path), and Escapement says
so. A principal who does not want that can use a Pledge-style reputational bond, and relying
parties can weigh the difference.

### The equivocation bond: no adjudicator

The **equivocation bond** covers one narrow, objectively checkable fault: the gateway signing two
different log heads for the same slot, which is how it would show two parties two histories. That
is the one misbehaviour that can be punished without a judge. The construction follows Babylon's
Bitcoin staking closely [@babylon2023; @babylon-staking-script; @fp-slashing-protection], and the
idea that equivocation on a public log can cost the equivocator bitcoins is Ruffing, Kate and
Schroeder's "accountable assertions" [@ruffing2015]. What follows is a sketch, not a specification.

- **One key, nonces committed in advance.** The gateway has one equivocation key E, named in the
  charter. Each seal commits, alongside the log head, to the public nonces the gateway will use for
  every slot of the next epoch, as Babylon's finality providers commit their randomness ahead of
  time [@fp-commit-pub-rand]. A Schnorr signature is `s = k + e·x`, so two signatures with the same
  committed nonce on different messages reveal the private key x [@bip340].
- **Slots that cannot be dodged.** A slot is a batch within an epoch: the gateway closes a batch
  every minute or so and signs the log head at the end of each batch with that batch's nonce. A
  receipt for a request carries the signed head of every batch since the last seal. Two receipts
  from the same epoch therefore overlap in their earlier batches, and if they come from different
  histories, some batch has been signed twice. Without this rule a gateway could fork by signing
  alternate batches for different parties and never sign any batch twice.
- **A place where receipts meet.** Relying parties forward the receipts they receive to the
  guardians, who compare them. Two conflicting signed heads for one batch are the proof.
- **A slash whose destination is fixed.** The bond's slashing path needs E's signature and the
  slashing committee's, and the committee pre-signs, when the bond is made, a transaction that
  burns a fixed fraction of it. Once x leaks, anyone holding the two signatures can complete that
  transaction. Without the committee's pre-signature, whoever saw x first, or a miner, would simply
  take the bond. The committee cannot slash a gateway that has not equivocated, because it does not
  have E.
- **An unbonding wait.** The principal reclaims the bond only through a path with a relative
  timelock, so a gateway that equivocates and then withdraws can still be slashed during the wait.

Why it is needed, given that seals already prevent a sealed log from forking: seals are hourly,
and in between, relying parties act on receipts. The equivocation bond makes it costly to give two
parties receipts from two different histories in the gap before the next seal settles which history
is real.

The danger is accidental equivocation. Ethereum's record is a warning: validators that restart,
fail over or run twice sign twice, and in September 2025 a single operational fault slashed about
forty at once [@cryptoslate2025; @cryptonomist2025]. Gateways restart too. So the gateway keeps a
slashing-protection record of every batch it has signed, as Babylon's finality providers do
[@fp-slashing-protection], and the equivocation bond is kept small relative to coverage. Ethereum
also scales penalties with how many validators fault together, so that a lone bug costs little and
a coordinated attack costs a lot [@eth2book]. Bitcoin script cannot count other people's faults,
so Escapement cannot copy that rule on chain. It is an open problem in this design.

## Seasoning and swarms

A bond counts for Tier 2 and Tier 3 authority only after it has been locked for a **season** of
[4,032 blocks](numbers.md#season-blocks), about [28 days](numbers.md#season-days). Before that, the
charter can act only at Tiers 0 and 1. The bond's age is on chain: its confirmation height is
public, and its timelock is visible once the bundle reveals its script, so any relying party with a
node can check it. OrangeCheck's Attest protocol already measures stake by coin age
[@attest-spec; @attest-bond], and JoinMarket's fidelity bonds use timelocked coins as costly
identity for the same reason: the lock is "an objective measurement that can't be faked"
[@belcher-2019; @bip46].

Seasoning prices a swarm in **time** as well as money. An adversary who wants a thousand agents
with Tier 3 authority next week cannot have them: each needs a bond that has aged a season. It can
have them in a month, if it planned a month ago.

That is the honest summary of costly identity, and the numbers show its limit. Douceur showed that
without a trusted authority, an attacker's sybil count is bounded only by its resources
[@douceur2002]. At the reference coverage, a swarm of [10,000 agents](numbers.md#swarm-size) must
lock [20 BTC](numbers.md#swarm-capital-btc). The 2026 incident's attackers, had each needed a
charter, would have needed [1.4 BTC](numbers.md#incident-swarm-capital-btc), and the incident ran
[68 days](numbers.md#incident-days), longer than a season. Costly identity prices a swarm; it does
not stop one. And it sorts nothing: Spence's signalling works only when the signal costs bad types
more than good ones [@spence1973], and sats cost an honest and a malicious agent exactly the same.
A bond says that someone with money stands behind an agent. It does not say the agent is honest.

Belcher's 2019 proposal valued a fidelity bond as the square of its locked value, so that splitting
capital across N identities gives the swarm only 1/N of the weight one identity with the same
capital would have: [0.00010](numbers.md#split-authority-ratio-squared) for ten thousand
[@belcher-2019]. JoinMarket shipped a gentler exponent of [1.3](numbers.md#jm-bond-exponent)
[@jm-fidelity], under which the same split keeps [0.063](numbers.md#split-authority-ratio-jm) of
the weight. Superlinear valuation is a real anti-swarm rule, and Belcher himself notes its cost:
long-term holders get bonds essentially for free, and weight concentrates in the rich
[@belcher-2019]. Escapement uses a linear, capped rule instead: one bond backs one charter, and a
charter's authority is capped by its ladder whatever the bond's size. The brake on swarms is the
ladder's Tier 3 spawn rule and the attestation of principals, not the bond's arithmetic.

## Seals

### The log and its seal

The gateway keeps an append-only Merkle log of every action: each request, its tier, its inputs
and outputs by hash, every commitment, every veto received and every release. The structure is
Certificate Transparency's [@rfc6962; @rfc9162]: anyone holding an old head can check that a new
head extends it, and anyone holding an entry can check it is in a head.

Every [6 blocks](numbers.md#seal-epoch-blocks), the gateway seals its log head in a Bitcoin
transaction that spends the previous seal's output and commits the new head in its own output, by
tweaking the output key with the head (pay-to-contract on a Taproot output [@bip341]). The seal is
[111 vB](numbers.md#seal-tx-vbytes): one Taproot input and one Taproot output. Carrying the head in
an OP_RETURN instead makes it [154 vB](numbers.md#anchor-tx-vbytes).

Because each seal spends the one before, there is only ever one chain of seals: making a second
would mean double-spending a seal output, which Bitcoin's consensus prevents. This is Todd's
single-use seal [@todd-2017], and it is exactly how Catena makes a log non-equivocating using
Bitcoin: a light client that follows the chain of seals sees one history or a double-spend
[@catena-2017]. An auditor who follows a gateway's seals sees one log.

### Pools

One seal can carry many gateways. A **seal pool** keeps a sparse Merkle map from agent identifier
to that agent's log head, CONIKS-style [@melara2015], and seals the map's root. Because the map has
one leaf per agent, the pool cannot include two heads for one agent in one root, and because the
roots are single-use sealed, it cannot publish two roots. At the reference
[1,000 agents](numbers.md#agents-per-pool) a pool, sealing is cheap.

| Fee rate | One seal | One gateway, one day | One agent in a pool, one day |
|---|---|---|---|
| 2026 median, [1 sat/vB](numbers.md#feerate-2026) | [111 sats](numbers.md#seal-cost-2026) | [2,660 sats](numbers.md#gateway-seal-cost-day-2026) | |
| 2023 median, [15 sat/vB](numbers.md#feerate-2023) | [1,660 sats](numbers.md#seal-cost-2023) | | |
| Halving block 840,000, [200 sat/vB](numbers.md#feerate-halving) | [22,200 sats](numbers.md#seal-cost-halving) | [533,000 sats](numbers.md#gateway-seal-cost-day-halving) | [533 sats](numbers.md#agent-seal-cost-day-halving) |
| Peak day, [861 sat/vB](numbers.md#feerate-peak-day) | [95,600 sats](numbers.md#seal-cost-peak-day) | | |

A gateway sealing alone makes [24 seals](numbers.md#seals-per-day) a day. The measured fee rates
come from mempool.space [@mempool-feerates; @mempool-block840000]. If the world ran
[1,000 pools](numbers.md#seal-pools), each sealing every six blocks, they would use
[1.85%](numbers.md#seal-blockspace-share-pools) of all blockspace. That is not nothing, and it is
the reason sealing is pooled and hourly rather than per agent and per block.

OpenTimestamps is free and could replace seals for proofs of existence [@todd-ots-2016]. It does
not give non-equivocation: a gateway could timestamp two histories. Escapement uses
OpenTimestamps-style aggregation only for existence proofs of individual entries, and single-use
seals for the one-history property.

### What a seal proves, and what it does not

A seal proves that a log head existed by a given block, and that the gateway has published one
history. It does not prove that the log is complete: a gateway can leave actions out, and an agent
can act around its gateway. It does not prove that any action was good. An anchored hash proves
existence and order, not behaviour, as Allen et al. warn about every scheme of this kind
[@allen2026survey].

A seal also does not prove that anyone saw what it commits to. Kelsey and Kohno's herding attack
shows that committing to a hash in advance and choosing the message later is possible under
some constructions [@kelsey2006]; more simply, a gateway can commit to a head and never show the
entries. So the rule is that guardians must receive every entry's content when it is committed,
and an entry whose content a guardian has not received counts as missing. A guardian vetoes any
tick whose batch it has not received in full.

Seals are only as final as Bitcoin's history, and that history rests on mining pools not
colluding. The largest pool mined [27.8%](numbers.md#pool-largest-share) of blocks over the
trailing year and the two largest [46.1%](numbers.md#pool-top2-share) together
[@mempool-pools]. By Nakamoto's own formula for an attacker catching up from behind
[@nakamoto2008], the chance that the largest pool alone ever rewrites a block six deep is
[8.9%](numbers.md#reorg-p-largest-6), and it needs [19 blocks](numbers.md#depth-for-target-largest) before that
chance is under [0.1%](numbers.md#reorg-risk-target). For the two largest, colluding, the chance is
[82%](numbers.md#reorg-p-top2-6) at six blocks and [12.79%](numbers.md#reorg-p-top2-144) at a
Tier 3 depth, and it takes [552 blocks](numbers.md#depth-for-target-top2), about
[3.8 days](numbers.md#depth-for-target-top2-days), to fall under the target. The formula treats a pool as a single miner, which it is
not (the hashers behind a pool can leave it), and it ignores what such an attack would cost the
pools in reputation and in the value of their coins. But it says plainly that Escapement's record
is as safe as Bitcoin's pools are independent. Escapement treats a seal as settled after
[19 blocks](numbers.md#depth-for-target-largest) and treats deeper collusion as a risk it shares
with every other use of Bitcoin.

### Model weights

A principal can commit the hash of the weights it deploys in the charter, and seal it. The IETF
draft that defines a Bitcoin-anchored profile for transparency services uses exactly this example:
an AI lab registering model weights and safety evaluations so a regulator can rule out backdating
[@fassbender2026], and Sigstore already signs models into a transparency log [@sigstore2025]. The
commitment proves which weights the principal said it deployed and when. It cannot prove which
weights are running, unless the inference provider attests to that, which is outside Bitcoin.

### Keeping up with the chain

Every check above needs the verifier to know the chain. Headers are
[80 bytes](numbers.md#header-bytes) each, so a device that keeps its own view of the chain reads
[4.2 MB](numbers.md#headers-mb-per-year) of headers a year. That is small enough for a gateway or
a phone. Headers prove that entries exist; they do not show a verifier the newest entries of a tick
chain, which needs full blocks from the last link it knows to the tip.

## Relying parties: where it is enforced

Bitcoin enforces only spends of bitcoin. Everything else in Escapement is enforced by relying
parties choosing to check, and that is the design's main weakness and its main dependency.

A relying party that deals with a chartered agent receives a bundle and checks it:

1. the charter, signed from the principal's address;
2. a renewal: every signature, its block h_k in the best chain, and the release confirmed at a
   height between h_k and h_k + L;
3. the bonds: their outputs unspent, their size, and their age against the season;
4. for a Tier 2 or 3 action, a chain proof of its release from the pinned T_0, with each link's
   witness proved, and the advance at least N blocks after T_n;
5. the gateway's latest seal, and that the log head the agent presents extends it.

None of this needs a trusted server for the commitment layer: apart from the bonds' unspent
status, which needs a node, every check is a signature, a Merkle proof or a header, and each can be
done by the relying party alone. Scoring the record is another matter: it needs the event list,
the baselines and the resolvers, which are trusted parties.

Why would a relying party check? Because it bears risk from the agent's actions, and the bundle
tells it who answers for them (the principal), how much is at stake (the bonds) and whether anyone
can stop the action (the ladder). Three forces could make that matter: liability, where a service
that dealt with an unbounded agent shares the blame; insurance, where cover for AI agents is
already being written [@fortune2025aiuc]; and regulation, where the largest model developers
already have reporting duties [@euaiact2024art51; @sb53gov2025]. None of them requires Escapement
today. Adoption is the unsolved problem.

The most natural place to start is paid APIs. L402 services already sell access for Lightning
payments using macaroons [@l402-readme], and macaroons were designed to carry caveats, including
caveats that a third party must discharge [@birgisson2014]. An L402 service could add one caveat,
"a valid Escapement lease for this agent", and serve only chartered agents. That is a small change
at one relying party, and it would test whether anyone wants the check.

## Compute: the chip clock is withdrawn

The first version offered Bitcoin headers, with a difficulty floor, as the clock for AI chips that
run only under renewed licences, as the hardware-governance literature proposes
[@petrie2025flexheg2; @buterin2025dacc]. That is cut (RT-24). An operator who stops feeding a chip
headers freezes its view, so its licence never lapses. A floor set relative to the last difficulty
the chip accepted ratchets down one header at a time, so a forger lowers it step by step. And one
forged fork serves a whole fleet. A chip clock would need full retarget validation that is safe
against timewarp, a local clock with a stated drift bound, and a cost per fleet. None of that is
designed here. Renewal chips remain prior work, and stockpiled licences their known weakness
[@petrie2024].

## The clock under attack

An adversary who wants a delay to end early must make blocks come faster. Below a hashrate
majority, that means adding hashrate. Doubling the network's
[1,052 EH/s](numbers.md#hashrate-eh) [@mempool-hashrate] takes hardware drawing
[18.4 GW](numbers.md#clock-2x-power-gw) at a current miner's [17.5 J/TH](numbers.md#asic-efficiency-j-th)
[@hri-s21] and costing about [7.4 billion USD](numbers.md#clock-2x-hardware-busd) at reported street
prices [@ct-bitmain]. It halves block time only until the next difficulty adjustment, gaining
[7 days](numbers.md#clock-2x-days-gained) once, after which difficulty catches up. To shrink a Tier
3 wait from [24 hours](numbers.md#tier3-delay-mean-h) to
[1 hours](numbers.md#tier3-compress-target-h) needs [24 x](numbers.md#tier3-compress-factor) the
network's hashrate, about [423 GW](numbers.md#tier3-compress-power-gw) of added power, or
[8 x](numbers.md#tier3-compress-vs-datacentres) the average draw of every data centre on Earth in
2025. That energy cost does not fall as an agent becomes faster or more capable. Against an actor
below a hashrate majority, block height is a clock that costs gigawatts to speed up.

Three qualifications. A majority of existing hashrate needs no new hardware: the timewarp bug lets
a majority lower difficulty until blocks come at several a second, after about a month of visible
setup [@optech-timewarp; @bip54]. The fix is specified in BIP-54 and not active [@bip54], so the
clock's cost binds only actors below a majority. That is why relying parties should count median
time past as well as blocks. Hashrate can also be borrowed, by renting it or bribing pools, and
that cost, unlike the energy cost of new hashrate, may fall as agents become more capable. And a
block-counted delay is random; the Tier 2 tail above is the cost of using a Poisson clock.

The other attacks on the clock are on its readers and on vetoes, not on the chain's rate: feeding a
relying party stale headers, which an eclipse does [@riard2020], or keeping a veto out of the
window. Pools have left sanctioned transactions out of blocks [@b10c-ofac], a briber can make the
window's edge a fee auction, and a flood of transactions can delay many vetoes at once
[@harris2020]. Tick-chain vetoes and on-chain Cancels both need to confirm well before the window's
edge, with fee headroom; a missed seal epoch is itself visible on chain.

## Threats, and which part answers each

| Threat | What happens | What answers it | What remains |
|---|---|---|---|
| Overspending | the agent spends faster or more than intended | the allowance (no detection needed) | at most [200,000 sats](numbers.md#bond-coverage) at the reference terms |
| Irreversible action | the agent transfers, deploys, spawns, changes its charter | the ladder: delay, one-guardian veto, every guardian for a Tier 3 release | a principal who puts dangerous actions in low tiers; at Tier 2, a release needs no guardian |
| Persuading overseers | the agent social-engineers guardians | every guardian signs a Tier 3 release; guardians independent; the delay gives others time | a captured guardian set |
| Key theft | the agent key leaks | lease and allowance bound the damage; revocation | one lease and allowance |
| Abandonment | humans vanish | lease lapses; allowance stops; Liana-style recovery | nothing beyond the last allowance |
| Two histories | the agent or gateway shows different records to different parties | the pinned tick chain; single-use seals; equivocation bond for receipts between seals | omissions; deep collusion by pools |
| Correlated claims | the agent commits claims that move together, or a hidden tail risk | the round rule: a round counts as the weighted mean of its claims' ratios (Theorem 1) | nothing beyond the bound, if the baseline meets H0 |
| Bad baseline | the agent forecasts against a stale, thin or chosen baseline, or on events it wrote | H0: a baseline from an independent party, on an exogenous list | a captured registry; a market baseline holds only up to the cost of moving it |
| Lucky records | many identities without edge, the luckiest shown | Theorem 1: K identities reach λ with probability at most K/λ | high scores by luck when more identities are in use than λ |
| Outcome manipulation | the agent acts to move the outcomes it forecasts | nothing in the design; training is claimed only for events the agent cannot affect | stated limit: the reward pays for surprises (Proposition 10b) |
| Wash-traded promises | the agent keeps promises to its own sybils, judged by its own adjudicator | promise history counts only against an agent | nothing: kept promises earn no standing |
| Template copies | the agent funds its own copy of a tick output, for a vetoed or a new index | relying parties count only links from the pinned T_0 | a chain proof that grows with the chain |
| Witness swap | the agent swaps an `advance3` witness into an `advance2` release with the same txid | each link's wtxid proved under its block's witness commitment | nothing found: the lab's forged witness failed this check |
| Hidden newest entries | the agent shows a prefix of its chain | full blocks from the last known link to the tip | a light verifier cannot see the newest entries |
| Veto reorganisation | a pool forks below a confirmed veto and releases the entry | depth: vetoes confirmed early, large stakes in Tier 3 windows | at [6 blocks](numbers.md#confirmations-standard), up to [8.9%](numbers.md#reorg-p-largest-6) for the largest pool and [82%](numbers.md#reorg-p-top2-6) for the two largest |
| Fee auction at the edge | the agent's advance outbids a late veto, or a briber pays miners to exclude it | TRUC vetoes with pay-to-anchor, fees in proportion to the batch, confirmed well before the edge | contingent bribes; payments to miners out of band |
| Flooding | someone congests the chain so that vetoes miss their windows | fees in proportion to what each batch is worth; Tier 3 windows | nothing in the design; stated limit |
| Hostage guardian | one guardian, coerced or seized, vetoes to its own key | nothing in the design; stated limit | the identity's chain ends for good, and its standing with it |
| Guardian-written entries | the guardians together renew and write an entry the agent never made | nothing in the design; stated limit | the record is only as independent as its guardian set |
| Sold records | a seasoned identity with a high score changes hands, or another model runs behind its key | nothing in the design; binding a record to a model needs attestation | the record binds a key, not a model |
| Whitewashing through fresh identities | a harmful actor leaves a record that has begun to show and rejoins under a fresh identity | a bond and a season per identity | in the simulation harmful actors cycle and come out ahead; routing around is not shown to cost them |
| Eclipse and time dilation | a relying party is fed stale headers | its own node, or several header sources | an eclipsed relying party sees an old tip, so a released action past its execution deadline still looks current |
| Swarm | many chartered agents act together | bonds per charter; seasoning; Tier 3 spawn | an adversary with capital and a month's notice; limits are per identity |
| Outside money | the agent earns, borrows or steals bitcoin outside the scheme | relying parties that require a charter refuse | everything that does not pass through such a relying party |
| Off-scheme action | the agent acts through credentials, exploits or borrowed compute | nothing in Escapement | the 2026 incident's whole attack surface |
| Speeding the clock | someone adds or borrows hashrate | difficulty and its cost: [18.4 GW](numbers.md#clock-2x-power-gw) to double the rate for a week | a colluding majority using timewarp, until BIP-54 activates; borrowed hashrate |
| Malicious principal | the principal wants the harm | nothing; Escapement binds agents to principals | everything |

Three further limits apply across the board. **Privacy:** bonds and seals are public, so a
principal's backing coins and a gateway's activity cadence are visible; Taproot hides unused script
paths [@bip341], and contents stay off chain. **Quantum risk:** the keys are Schnorr keys, and
long-lived bonds are exposed if large quantum computers arrive; the proposed P2MR output type is a
draft [@bip360]. **Custody:** every key is a target, and the guardians' keys most of all.

## What it does not do

Escapement does not make an AI safe. It does not see inside a model, constrain what the model
learns, or prevent an AI from acquiring money elsewhere. It does not touch actions that pass
through no relying party that checks. The 2026 incident, the most serious multi-agent event on
record at the time of writing, ran on credentials, exploits and borrowed compute, and nothing in
it went through a check Escapement would have added [@metr2026hf; @openai2026hf]. AI agents'
capabilities are also growing quickly: METR's estimate is that task time horizons double about
every [3.6 months](numbers.md#metr-doubling-months) [@metr2026q4]. The design assumes the agent is
smarter and faster than its overseers. It does not assume it is weaker.

The record does not measure honesty. It separates edge over a stated baseline, and only while the
event list, the baseline and the resolvers, which are trusted parties, are sound. It does not bind
a record to a model, and it does not stop a record being sold. Training on it does not hold where
the agent can move the outcomes. It does not make routing around costly: in the one model built to
test it, harmful actors cycled through fresh identities and came out ahead. And it does not make
an agent's record safe from its own guardians, any one of whom can end it.

What it does is narrower. For an agent its principal wants bounded, Escapement gives a budget that
refills only at a renewal every guardian signs, a set of delays on irreversible actions that no
participant below a hashrate majority can shorten, a veto any one guardian can use, final once it
is buried, liability that lands on a named human's coins, and a record no single party can rewrite
once its entries are deep, though the guardians together can add to it. For a service that wants
to deal only with bounded agents, it gives a check of the commitment layer that needs no trusted
server; scoring still needs trusted parties.

## Parameters

Every parameter below is a design choice, set in `data/inputs.toml` and varied with
`python3 model/escapement.py --set ID=VALUE`.

| Parameter | Reference value | Why |
|---|---|---|
| Tier 2 wait | [6 blocks](numbers.md#tier2-delay-blocks), [60 minutes](numbers.md#tier2-delay-mean-min) mean | the one-hour delay of the Async Control study [@stickland2025] |
| Tier 3 wait | [144 blocks](numbers.md#tier3-delay-blocks), [24 hours](numbers.md#tier3-delay-mean-h) mean | a full day for a human to look; the same length as the CSV fallback in a published Bitcoin agent-wallet design [@laz1m0v2026] |
| Lease | [144 blocks](numbers.md#lease-blocks) | a daily renewal by every guardian; no release counted more than a day after the last renewal's block |
| Season | [4,032 blocks](numbers.md#season-blocks), [28 days](numbers.md#season-days) | two difficulty periods; long enough that a swarm must be planned |
| Seal epoch | [6 blocks](numbers.md#seal-epoch-blocks) | matches the Tier 2 wait, so a Tier 2 commitment is sealed before its release |
| Allowance | [100,000 sats](numbers.md#allowance-per-lease) a lease | an example; set per agent |
| Coverage ratio | [1.0](numbers.md#coverage-ratio) | the bond covers what can be spent before a stop |

## Deployment path

**Today, with no consensus change.** The vault (pre-signed Unvault and Cancel, a co-signer), the
lease and allowance (a signed renewal, an NWC or on-chain budget), the bonds (timelocked outputs;
EOTS-style equivocation keys with pre-signed slashing), the tick chain with its halt output and
chain proofs, single-use seals and seal pools, and the relying-party bundle all work under current
rules. The trusted parts are the co-signer (for destinations and amounts), the guardians (for
vetoes, releases and renewals, and not to end the identity or write entries the agent never made),
the adjudicator (for harm claims), the event list, baseline providers and resolvers (for scoring),
and each relying party's own view of the chain.

**With covenants.** CTV would let the vault commit its destination in script and drop the
co-signer from that role [@bip119]; a vault opcode with partial withdrawals would remove the fixed
denominations [@bip345]. An open letter in 2025 asked Bitcoin Core contributors to prioritise CTV
and CSFS [@optech-2025-07-04], and nothing has been scheduled since. Escapement does not wait for
them.

**First steps.** A signet prototype of the vault, lease and seal; a gateway for one agent framework
that implements the ladder; and one L402 service that adds the lease caveat. Each is small, and
each tests a different part of the claim.

## What would show it is wrong

The design makes claims that can fail, and these are the experiments that would test them.

1. **Do block-counted delays help overseers?** Repeat the Async Control setting with Tier 2 and
   Tier 3 waits drawn from the real block-time distribution rather than fixed delays, and with
   monitors that must veto rather than review. If safety does not rise with the wait, the ladder
   is cost without benefit.
2. **How much of an agent's irreversible action passes through relying parties?** Instrument
   agents on realistic long tasks and count which irreversible actions go through a service that
   could check a charter. If the answer is small, as the 2026 incident suggests it may be,
   Escapement's coverage is small.
3. **Can guardians keep up?** Measure how long human and automated guardians take to review Tier 2
   and Tier 3 commitments, and how often agents persuade them. If guardians rubber-stamp, the
   quorum is decoration.
4. **How often do agents equivocate by accident?** Run gateways under restarts and failover and
   count double-signed slots with and without slashing protection.
5. **Will anyone check?** Offer the lease caveat at a paid API and see whether principals charter
   their agents to use it.
6. **Can a baseline meet H0?** Score forecasters without edge, under the round rule, against a
   baseline from an independent provider. If high scores appear more often than Theorem 1 allows,
   that baseline is not the conditional law the bound needs, and records scored against it do not
   carry the bound.
7. **Does a fresh identity cost enough to stop cycling?** Rerun the adoption simulation with agents
   that plan over many periods, identity costs paid once and amortised, and harmful types that
   choose their strategy. Until then, routing around is not shown to cost a harmful actor anything.

If the first two fail, the enforcement layer fails with them: a meter on commitments that are not
where the harm happens, or a delay that overseers cannot use, is not a safety mechanism. If the
sixth fails for every baseline anyone can supply, the record fails with it.
