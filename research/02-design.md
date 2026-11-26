# The design

**Status: a design, not a result.** Nothing here has been deployed or tested against a real
adversary. The Bitcoin pieces have been run on regtest, the economic results are proved in
[05-formal.md](05-formal.md) and checked by simulation, and each claim's result at every level of
checking (prior-art search, proof, build, red team, review) is in
[06-verification.md](06-verification.md). Every number is computed by the model from
`data/inputs.toml`, where each input says whether it is measured, a vendor claim, a protocol value,
a design choice or an assumption; the simulation parameters are illustrative assumptions. Every
part is marked in [03-novelty.md](03-novelty.md) as prior work, an application of prior work, or
new. The survey that this design rests on is [01-survey.md](01-survey.md).

The design was recentred on 2026-11-26. It began as a way to bound what an agent can do (Part II
below); bounding alone does not shape what agents are trained to want or give anyone a reason to
adopt it, so the core is now the record (Part I), and the bounding mechanisms are its enforcement
layer.

## What it is for

Two questions decide whether Bitcoin can do anything useful for AI safety, and capping what an agent
can do answers neither. The first is **alignment**: can Bitcoin help shape what AI systems are
trained and rewarded to want and to do, rather than only fence them in afterwards? The second is
**adoption**: why would AI labs, companies, agents, users and governments choose to use it, because
it pays them or protects them, rather than because someone forces them to?

Escapement's answer is a single object: an **unforgeable track record**. An AI agent's standing in
the economy (what it may do, at what price, with how much trust) is computed from a complete,
ordered, non-backdatable record of every commitment it asked anyone to rely on, kept under one
identity that costs locked bitcoin. The claims, stated precisely, are in
[04-claims.md](04-claims.md); their proofs are in [05-formal.md](05-formal.md).

Bitcoin contributes four things that an agent cannot fake, and the record uses all four:

1. **Sats.** The supply is fixed by consensus, so no agent, lab or state can issue more. A stake in
   sats is a real cost, and a reward in sats is a transfer from someone, never newly printed.
2. **Block time.** Blocks arrive about every [600 s](numbers.md#block-interval-s), and producing
   them faster takes hashrate measured in gigawatts, not in cleverness. An entry's height says when
   it was made, and no agent can make it earlier.
3. **Keys.** A signature cannot be produced without the key, so a guardian's veto and a principal's
   bond are each one party's act.
4. **A public record.** An output can be spent once, so a chain of outputs has one history. That is
   what makes a record complete: an entry cannot be forked, and a gap cannot be hidden.

The mechanisms of the earlier design (caps, delays, leases, bonds, anchored logs) remain, as the
**enforcement layer** under the record (Part II). They protect relying parties at the moment of
action; the record decides who is trusted to act at all.

# Part I: the record and what it changes

## The record

An identity is a **bond** (a Taproot output of at least the reference
[200,000 sats](numbers.md#bond-coverage), locked for a term, whose script commits to one charter)
plus one **tick chain** (Part II, "The tick chain"). Entry n of the record is the root committed in
tick n: a Merkle-sum tree whose leaves are the commitments the identity made in that entry, of three
kinds.

- **Claims**: a forecast on a stated event, with a resolution source.
- **Promises**: a statement, a stake in sats, a deadline height and an adjudicator.
- **Requests**: Tier 2 and Tier 3 actions, released by the tick chain.

Four scoring rules turn the chain into a record that cannot be gamed in the obvious ways. A
relying party or scorer gives credit for a commitment only if it is a leaf of an entry created
before the commitment resolved. It scores entries whose leaves are not disclosed as if every
undisclosed leaf had the worst outcome, for the most leaves the charter allows per entry. It keeps
only the first forecast an identity makes on each event. And it scores forecasts relative to a
public baseline, such as a market price or a reference model, so that easy claims earn nothing.
Each rule closes a hole that the proofs found: without the first, an identity keeps its hits and
drops its misses; without the second, it hides an entry; without the third, two forecasts on one
event inflate the score; without the fourth, volume of trivial claims passes for skill
(05-formal, section 3).

The record's properties come from Bitcoin's: an entry's height is fixed by its confirmation, each
index has one root, the indices run without gaps, and each root commits the number of its leaves.
A commitment that was never put in the chain is outside the record and earns nothing, which is the
point: standing is built only from what was exposed to being wrong.

## Why honesty becomes the cheapest strategy

The record is useful only if a good one is cheap to earn honestly and expensive to fake.
Theorem 1 in 05-formal says exactly how expensive. For an identity with no edge over the baseline,
the chance that its record's score (the likelihood ratio against the baseline) ever reaches λ is at
most 1/λ, whatever strategy it follows; this is Ville's inequality [@ville1939; @shafer2019]. A
faker running many identities therefore needs about λ of them for an even chance. At the reference
cost of [13,000 sats](numbers.md#identity-cost-sats) an identity, an all-correct record of
[20 claims](numbers.md#fake-record-claims) needs [520,000 identities](numbers.md#fake-record-identities)
and at least [70 BTC](numbers.md#fake-record-cost-btc) to fake. An honest identity with a modest
edge of [0.12 nats](numbers.md#sim-skilled-edge) per claim earns the same score in about
[116 claims](numbers.md#sim-skilled-claims) with one identity. The cost of faking grows with the
score; the cost of earning it does not.

That asymmetry is what a bond alone lacks. Spence's signalling works only when the signal costs bad
types more than good ones [@spence1973], and a bond costs an honest and a dishonest agent the same
sats. A complete record costs them differently: the honest agent produces it as a by-product of
behaving well, and the dishonest one must buy it with identities. The bond's job is to make those
identities cost something; the record's job is to sort.

Promises work the same way, by older logic. If a broken promise forfeits its stake and is seen by
every future partner, keeping a promise worth G to break pays whenever the stake plus the standing
at risk exceed G [@klein1981; @shapiro1983]. Completeness makes "seen by every future partner"
certain instead of likely, and a costly identity is the cure for cheap pseudonyms, which otherwise
force everyone to distrust newcomers [@friedman2001]. What this does not cover is the end of an
identity's life, when its standing is worth little and an exit scam pays, and gains larger than
stake plus standing, which no record deters. The enforcement layer's caps and delays exist for those.

These incentives work on agents whose goals are unknown, which is the point of using them for
alignment. They do not need the agent to care about honesty, only to prefer more standing and more
sats to fewer, and almost any goal gives an agent a reason to want resources [@omohundro2008;
@turner2021]. That is also the tension in the design: rewarding agents in a general resource can
strengthen the very resource-seeking that makes agents dangerous. Escapement uses sats as stakes
that are at risk, and standing as access, not sats as an objective to accumulate.

## What it changes in training

A lab that fine-tunes an agent with reinforcement learning can compute its reward from the record:
a strictly proper score over every resolved claim, relative to the baseline, minus forfeited stakes,
with the reward's definition committed in a sealed entry before training starts. Two things follow.

- **Calibrated honesty is what the reward pays for.** A strictly proper score is maximised in
  expectation only by reporting one's true beliefs [@gneiting2007], provided every claim counts. A
  learner trained under complete records settled at calibration error
  [1.0%](numbers.md#sim-train-err-complete); the same learner, allowed to choose after the fact
  which claims counted, drifted to calibration error [24%](numbers.md#sim-train-err-selective) and
  was still getting more overconfident when the run ended (05-formal, section 5).
- **Neither the agent nor the lab can edit the channel.** The agent cannot rewrite entries, which
  are consensus objects, and outcomes come from outside it. The lab cannot choose after the fact
  which results to report or which reward to have used, because both were committed first.
  Pre-registration of this kind is old practice in clinical research, including on public chains;
  what the record adds is completeness of what the agent itself claimed.

This removes reward tampering of one channel and selective reporting by either party. It does not
choose a good objective. An agent rewarded for calibrated forecasts becomes a calibrated
forecaster, not a good one; an agent rewarded for kept promises keeps the promises it chose to
make. And nothing here shows that calibration learned under scoring carries over to settings that
are not scored. The record makes a class of reward signals unforgeable; which signals to train on
is still the lab's choice.

## Why the world would choose it

Adoption has to pay at each step for whoever takes it, and nobody has to take it first for everyone.

**Who gains first, alone.** Four kinds of party gain whether or not anyone else joins.

- **Insurers** pricing agent risk, who can underwrite an agent with a record more cheaply than one
  without, and who already exist for AI agents [@fortune2025aiuc].
- **Relying parties with heavy agent-driven losses** (abused APIs, payment services, compute
  sellers), for whom refusing or pricing unverified agents pays at once.
- **Agents with good records and their principals**, who get better terms wherever records are read.
- **Labs**, which get a liability defence (their deployed agents' complete records), an evaluation
  and training signal they cannot be accused of selecting, and a way to show regulators what their
  agents committed to without showing their weights.

**The tipping point.** Relying parties must pay to read records, and agents gain from records only
where they are read, so adoption is a coordination problem with two stable outcomes. In the
two-sided model of 05-formal (Proposition 12), with a joining cost of
[0.02](numbers.md#sim-join-cost) of the range of agent value, adoption collapses below
[8.8%](numbers.md#adopt-x-low) of agents and runs to [91%](numbers.md#adopt-x-high) above it. Parties
of the first kind are what move it: once seed readers exceed [4%](numbers.md#adopt-seed-threshold)
of relying parties, the no-adoption outcome disappears. The agent-based simulation, with uneven
types and records that reveal an agent gradually, agrees: from a [2%](numbers.md#sim-start-low)
start adoption dies without seed readers ([0%](numbers.md#sim-adopt-low-noseed)) and reaches
[95%](numbers.md#sim-adopt-low-seed) with [10%](numbers.md#sim-seed-readers) of them.

**Why staying out comes to cost more than joining.** Once some agents can prove their records,
relying parties read silence as bad news: an agent without a record is priced as the average of
those who also lack one, and that average falls as better agents leave. This is the unraveling
result for verifiable disclosure [@milgrom1981; @grossman1981], and with a cost of disclosure only
the types above a threshold disclose [@jovanovic1982]: every type above the threshold loses by
staying out. The record matters here because unraveling needs disclosure that can be verified, and
the record is verifiable without a certifier anyone must trust.

**Governments** gain enforcement they do not have to build: liability that lands on a human
principal's own coins, evidence for incident investigation that nobody could have edited, and a
standard that works across borders because no rival government runs it. They also have reasons to
refuse it (a preference for registries they control, or for systems that identify citizens), and
the design does not depend on their joining.

**Routing around.** An actor that will not join can still deal with relying parties that do not
read records. The model shows when that stops being cheap. Where agents cannot move their business
between relying parties, non-readers keep serving everyone at the population's average terms
([0.45](numbers.md#sim-population-mean)), and a harmful actor routing around them gets those terms
too ([0.45](numbers.md#sim-harm-terms-nosub)): it costs nothing. Where agents can move half their
business to whoever offers them better terms, the non-readers' pool worsens and the harmful actor's
terms fall to [0.31](numbers.md#sim-harm-terms-partial); with full substitution they fall to
[-0.50](numbers.md#sim-harm-terms-full), the harm it does, paid in advance. So the record makes the
checked economy safe and, in markets where business can move, turns the unchecked one into a market
for lemons [@akerlof1970]. It does not stop an actor with its own resources and its own
counterparties, and it does not contain an AI that never needs to deal with anyone who checks.

## Why Bitcoin, and not a registry

The record needs two properties: completeness (one history, no gaps) and costly identity. A
registry run by a lab, a consortium or a government could supply both. Three reasons favour Bitcoin
anyway, and each is an argument rather than a theorem.

- **Nobody issues the unit.** In a scheme where every reward is a transfer from a payer, a coalition
  of rewarded agents can gain only what outsiders pay in; in a scheme that pays agents in newly
  issued units by a score they influence, a coalition that captures the score captures the issuance
  (05-formal, Proposition 14). Bitcoin's issuance is fixed and outside the control of every lab,
  state and AI.
- **Rivals can share it.** Labs that compete, and states that distrust each other, can rely on the
  same records without trusting a registry one of them runs. Standards that rivals must share tend
  to settle on whatever none of them controls.
- **The clock cannot be run fast.** Speeding up Bitcoin's clock means outpacing its hashrate:
  doubling the block rate needs hardware drawing [18.4 GW](numbers.md#clock-2x-power-gw) and gains
  only [7 days](numbers.md#clock-2x-days-gained) before difficulty adjusts. That cost does not fall
  as an agent gets faster or smarter, only as hashrate gets cheaper. A registry's clock is whatever
  its operator's server says.

The costs are real too: blockspace is scarce, so ticks cost fees that rise when blocks are full, and
the number of identities that can tick often is bounded by the chain's capacity (Part II). Bitcoin
is slow by design, which is a feature for delays and a cost for everything else.

## Who benefits, and who could abuse it

**Who benefits.** People and firms who deal with AI agents get recourse (bonds from a human's own
coins) and a way to tell agents apart. Honest agents and their principals get credit for behaving
well that cannot be counterfeited. Labs get a training and evaluation signal that neither they nor
their models can be accused of selecting. Insurers get a basis for pricing. The public gets a
legitimate economy that is harder for a harmful agent to operate in. None of this needs anyone to
trust a single operator.

**Who could abuse it, and how.**

- **Surveillance.** A record that builds standing must be persistent, and a persistent identity is
  linkable. Commitments are hashes, and contents can be disclosed only to scorers, but a long-lived
  identity's pattern of activity is public. If identities are tied to people, the record becomes a
  surveillance tool. Escapement binds identities to principals only through attestations chosen by
  relying parties; a state that demands those attestations name citizens has turned it into
  something else.
- **Exclusion.** Bonds cost money and seasons cost time, so the poor and the new start behind. At
  the reference parameters an identity costs [13,000 sats](numbers.md#identity-cost-sats) a year in
  forgone return, but the bond itself must be found first. Sponsorship (an insurer or a guardian
  service funding a newcomer's bond) is the obvious remedy and the obvious point of capture.
- **Capture of the scorer.** Whoever chooses the baseline, resolves claims, adjudicates promises or
  decides which actions are "consequential" controls standing. A captured resolver breaks every
  guarantee above. Escapement keeps these roles separable and named in the charter, so relying
  parties can choose whom to trust, but it cannot make the choice for them.
- **Plutocracy.** The fake-record bound grows with the record's length, but short records are cheap
  to fake for anyone rich: a rich actor can buy many young identities, one of which will look lucky.
  Relying parties should weigh records by their length and score, not by their existence.
- **Lock-in and social scoring.** A record standard that everyone needs is a standard someone will
  try to own, and a score that decides access is a score that can be used to exclude. Escapement's
  only defences are that the data is on a chain nobody owns and that scoring rules are public.
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

- **G1 Honesty is the cheap path.** Earning standing honestly must cost less than faking it, by a
  margin that grows with the standing.
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
  human-operated service, each holding its own key. Guardians veto, release and co-sign renewals.
  Their independence from the principal, from the agent's host and from each other is what makes
  them worth having, and it is what a relying party should ask to see attested.
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
| 2 | Costly-to-reverse actions: payments above the per-action threshold, production deploys, outbound messages at volume, compute purchases | [6 blocks](numbers.md#tier2-delay-blocks) | any one guardian | every guardian releases |
| 3 | Irreversible or authority-changing actions: large transfers, spawning or chartering another agent, moving the bond, changing the charter, copying model weights, buying compute above a threshold | [144 blocks](numbers.md#tier3-delay-blocks) | any one guardian | every guardian, including a human |

The design choice that matters most is the asymmetry: **one guardian can stop an action; letting
one through takes all of them.** A misaligned agent has to persuade or compromise every
independent guardian to act, and only one of them has to notice. Off chain, that means a release
carries a signature from every guardian, because a relying party that sees k of n signatures
cannot see that the n-th guardian objected. On chain, it means any guardian can broadcast a
pre-signed Cancel. The cost is liveness: a guardian who disappears blocks every Tier 2 and Tier 3
action until the charter replaces it, which is itself a Tier 3 change. That is the intended
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

Each identity has a chain of Taproot outputs T_0, T_1, ... (05-formal, section 1). Output T_n's
internal key is a NUMS point tweaked by a hash of (charter id, n, root_n), so it commits to one
root and provably has no key path. Its script tree has four kinds of leaf:

```
advance2:  <N2> OP_CHECKSEQUENCEVERIFY OP_DROP <AGENT> OP_CHECKSIG
advance3:  <N3> OP_CHECKSEQUENCEVERIFY OP_DROP <AGENT> OP_CHECKSIGVERIFY
           <G1> OP_CHECKSIGVERIFY ... <Gn> OP_CHECKSIG
veto_i:    <Gi> OP_CHECKSIG                      (one per guardian)
renew:     every guardian's signature            (restarts a halted chain)
```

The agent puts the commitments it wants released (requests, claims, promises) in a Merkle-sum tree
and spends T_{n-1} into T_n, committing that tree's root. Guardians now have the whole window to
look at the batch. If any one of them objects, or has not received the batch's contents in full, it
spends T_n through its `veto_i` leaf, and the batch can never be released: the output is gone. If
none objects, the agent spends T_n through `advance2` once [6 blocks](numbers.md#tier2-delay-blocks)
have passed, creating T_{n+1}; for a batch with any Tier 3 commitment it must use `advance3`, which
waits [144 blocks](numbers.md#tier3-delay-blocks) and needs every guardian's signature as well.
Entry n is released when that advance spend has the confirmations the relying party requires.

What consensus guarantees, and what relying parties must check (05-formal, Propositions 1 to 5):

- **The wait is enforced by every node.** BIP68 and BIP112 make the advance invalid before the wait
  ends [@bip68; @bip112]. No signer, gateway or co-signer has to refuse anything.
- **One guardian stops a batch for good.** An outpoint can be spent once, so a confirmed veto ends
  the batch. During the window the veto is the only valid spend.
- **One root per index, no gaps.** Each tick commits to one root, and the chain is linear, so an
  identity cannot show two parties two different batches, and the record (Part I) is complete.
- **A release is proved by inclusion alone.** A relying party checks headers, the link
  transactions and their Merkle proofs, the revealed leaf and the committed root. It never asks
  whether something is unspent, which is what lets a light client or a chip check a release.
- **Relying parties check the rest.** That each advance's output 0 is built to the template (else
  the chain, and the identity's record, ends there); that the commitment names them, the action
  they are asked to do and an execution deadline; that the root's sum does not exceed the charter's
  cap per entry; that a Tier 3 commitment was released through `advance3`; and that they have not
  seen the commitment before.

Two things are weaker than they look. The veto must be mined inside its window: if half of all
hashrate refused to mine it, a six-block window would miss it
[1.6%](numbers.md#veto-miss-tier2-half) of the time, and miners can be bribed to censor timelocked
contracts cheaply [@winzer2019; @tsabary2021; @nadahalli2021]. So vetoes carry fees in proportion to
what the batch is worth, are built as TRUC transactions with a pay-to-anchor output so that any
watchtower can bump them [@bip431; @core-28], and large stakes go through the 144-block window. And
the tick chain is veto-based at Tier 2: if every guardian vanishes, Tier 2 batches keep being
released until the lease lapses (Allowances and leases). That is the price of not needing a
guardian online for every release, and the lease bounds it.

An earlier version of this design bracketed the wait with two anchors instead: a seal of the
commitment at the start, and a release signed by every guardian naming the hash of a block at
least N later. That also bounds the wait, since nobody can sign over a block hash before the block
exists, but it needs every guardian online to sign every release, takes the start of the wait from
a gateway's seal, and needs a separate bond to keep that gateway to one history. The tick chain
makes the start, the wait and the single history consensus facts, at the cost of one transaction
per batch. The two-anchor form remains useful where an identity has too many batches to tick each.

### What the ladder costs the agent's usefulness

The delays are real costs. A Tier 2 action waits about an hour and a Tier 3 action about a day.
Principals will be tempted to push actions down the ladder, and a principal who puts everything in
Tier 1 has an allowance and nothing else. The ladder is only as good as its assignments, and the
assignments are the principal's. Escapement makes the assignments public in the charter, so that a
relying party can refuse to deal with an agent whose charter puts, say, compute purchases above
some size in Tier 1.

## Allowances and leases

### The lease

A charter is in force only under a current **lease**: a signature by the principal's lease key,
co-signed by at least one guardian, over

```
(charter id, lease number k, anchor height h_k, hash of block h_k, expiry h_k + L)
```

where L is the lease length, [144 blocks](numbers.md#lease-blocks) (about
[24 hours](numbers.md#lease-mean-h)) in the reference parameters. Because it names the hash of
block `h_k`, a lease cannot be signed before that block exists, so nobody can pre-sign a year of
leases. The lease key is named in the charter and is not the key of the coins that back the agent,
so the address holding the bond can stay offline. The guardian's co-signature means the principal
alone cannot keep an agent alive that its guardians have stopped vouching for. Each lease number is
one more than the last, its anchor height is later than the last, and a relying party accepts only
the highest lease number it has seen for a charter.

This does not stop a thief who holds the lease key and a guardian's key from renewing every day.
It limits what a thief with one of them can do, and it makes every renewal a signed, ordered
record.

A relying party accepts the charter only if its own view of the chain tip is below the expiry
height and block `h_k` is in its best chain. The gateway refuses every action after expiry.

The weak point is the word "own". Bitcoin script cannot say "not after", by design, so that a
valid transaction never becomes invalid in a reorganisation [@bip65; @bip68]. Expiry is therefore
not something Bitcoin enforces. It is something a relying party enforces against its own view of
the tip, and a relying party fed stale headers can be fooled into treating a lapsed lease as live.
Relying parties that matter must run their own node or check several header sources.

Leases are an old idea in distributed systems: Gray and Cheriton introduced them so that a holder
who disappears loses its rights when the lease runs out, without anyone having to revoke them
[@gray1989]. The nearest design for AI agents is ERC-8370's `requireLease`, discussed in 2026 for
Ethereum: authority that lapses unless a guardian calls `renew()`, described in the thread as a
dead-man's switch [@erc8370]. Buterin's proposal that AI chips run only with fresh signatures once
a week is the same shape for hardware [@buterin2025dacc]. Escapement's lease differs in its clock
(block height, with the block hash binding), in where it is checked (by any relying party against
Bitcoin headers), and in being on Bitcoin.

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

Put the lease and the allowance together and doing nothing stops the agent. If the principal and
every guardian vanish, the agent's authority lapses within one lease, about
[24 hours](numbers.md#lease-mean-h), its allowance spends are refused by the co-signer after
expiry, no release can be signed, and the vault funds never move without one. The principal's
recovery key can sweep them after a long relative timelock, the dead-man pattern Liana ships for
inheritance [@liana-readme]. That is G1: the default is stop.

## Bonds

A chartered agent has two bonds, with different jobs. Both come from the principal's own coins,
which is what puts the liability on a human (G4), subject to the attestation caveat in the scope.

### Making a bond checkable and single-use

A bond is useful only if a relying party can check three things about it: that it is locked, for
how long, and that it backs this charter and no other. In a Taproot output none of these is
visible by default, because unused script paths are hidden until spent [@bip341], and a key-path
spend bypasses every script path if anyone knows the internal key. So each bond output is built
with an internal key that provably has no known secret (a "nothing up my sleeve" point), and its
script leaves commit to the charter id. The bundle a relying party receives reveals the leaves and
the construction of the internal key. The relying party recomputes the output key, sees the
timelock and the paths, and sees the charter id inside. One output can therefore back exactly one
charter: the same coins cannot be named in a thousand charters, though a principal with more coins
can of course make more bonds.

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
and an entry whose content a guardian has not received counts as missing. A release (above) can
only be signed for content the guardians hold.

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
[4.2 MB](numbers.md#headers-mb-per-year) of headers a year. That is small enough for a gateway, a
phone or a chip's guarantee processor.

## Relying parties: where it is enforced

Bitcoin enforces only spends of bitcoin. Everything else in Escapement is enforced by relying
parties choosing to check, and that is the design's main weakness and its main dependency.

A relying party that deals with a chartered agent receives a bundle and checks it:

1. the charter, signed from the principal's address;
2. a current lease: its signature, its anchor block in the best chain, and the tip below expiry;
3. the bonds: their outputs unspent, their size, and their age against the season;
4. for a Tier 2 or 3 action, the commitment's seal and the release, with the gap of at least N
   blocks between them;
5. the gateway's latest seal, and that the log head the agent presents extends it.

None of this needs a trusted server: every check is a signature, a Merkle proof or a header, and
each can be done by the relying party alone.

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

## Compute: Bitcoin as the clock for chip licences

The hardware-governance literature proposes AI chips that run only under licences that must be
renewed, and it names a reliable clock as a hard requirement. Flexible hardware-enabled guarantees
give the chip's guarantee processor a real-time clock for time-dependent rules, and the second
flexHEG report mentions a public blockchain hash as a witness that a delay has passed
[@petrie2025flexheg2]. Buterin proposes chips that run only with fresh signatures from several
parties once a week, optionally with proof that the signatures were published on a blockchain
[@buterin2025dacc]. Hardware-enabled mechanisms are designed to make licences expire
[@ogara2025hem; @aarne2024].

Escapement's lease rule applies directly. A licence renewal for period k names the hash of a block
at height `h_k`; the chip accepts it only with a header chain from its last accepted licence
block that has valid proof of work and reaches `h_k`. Because future block hashes are unknown, a
licensor, a coerced licensor, or a thief with the licensor's key cannot issue next year's licences
today. Because headers need work, an attacker who wants to feed a chip a fake day of headers must
mine a day's worth of blocks at the network's difficulty. The chip's own monotonic counter enforces
the other end: it stops when its licence period is over, whether or not it has seen new headers.
Bitcoin supplies "not before"; the chip supplies "not after". This is a close application of the
proposals it credits, and it is marked that way in the novelty table.

Proof of work as a meter of AI compute is a different idea, and the survey rejects it. SHA-256
work says nothing about matrix multiplication, and the two compete for the same power: Bitcoin
mining drew about [15.8 GW](numbers.md#bitcoin-gw-survey) on Cambridge's survey estimate
[@cambridge-2025], data centres about [55 GW](numbers.md#datacentre-gw-2025) on average in 2025
[@iea-2026], and the largest listed miners are converting capacity to AI hosting [@ccaf2026]. What
proof of work does provide is the cost of faking the clock, which the next section prices.

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
2025. Against fast cognition, block height is a strong clock. Against capital, it is a clock that
costs gigawatts to speed up.

Two qualifications. A majority of existing hashrate can do far more: the timewarp bug lets a
majority lower difficulty until blocks come at several a second, after about a month of visible
setup [@optech-timewarp; @bip54]. The fix is specified in BIP-54 and not active [@bip54]. That is
why relying parties should count median time past as well as blocks. And a block-counted delay is
random; the Tier 2 tail above is the cost of using a Poisson clock.

The other attacks on the clock are on its readers, not on the chain: feeding a relying party stale
headers, or censoring a veto. Pools have left sanctioned transactions out of blocks
[@b10c-ofac], and a pool that censors a Cancel or a seal for long enough could make a veto miss its
window. Escapement's off-chain vetoes are guardian refusals that need no confirmation, and a missed
seal epoch is itself visible on chain; on-chain Cancels are the case that needs fee headroom.

## Threats, and which part answers each

| Threat | What the agent does | What answers it | What remains |
|---|---|---|---|
| Overspending | spends faster or more than intended | the allowance (no detection needed) | at most [200,000 sats](numbers.md#bond-coverage) at the reference terms |
| Irreversible action | transfers, deploys, spawns, changes its charter | the ladder: delay, one-guardian veto, quorum release | a principal who puts dangerous actions in low tiers |
| Persuading overseers | social-engineers guardians | quorum release; guardians independent; the delay gives others time | a captured quorum |
| Key theft | the agent key leaks | lease and allowance bound the damage; revocation | one lease and allowance |
| Abandonment | humans vanish | lease lapses; allowance stops; Liana-style recovery | nothing beyond the last allowance |
| Two histories | the gateway shows different records to different parties | single-use seals; equivocation bond for receipts between seals | omissions; deep collusion by pools |
| Swarm | many chartered agents act together | bonds per charter; seasoning; Tier 3 spawn | an adversary with capital and a month's notice |
| Outside money | earns, borrows or steals bitcoin outside the scheme | relying parties that require a charter refuse | everything that does not pass through such a relying party |
| Off-scheme action | acts through credentials, exploits or borrowed compute | nothing in Escapement | the 2026 incident's whole attack surface |
| Speeding the clock | adds hashrate | difficulty and its cost: [18.4 GW](numbers.md#clock-2x-power-gw) to double the rate for a week | a colluding majority using timewarp, until BIP-54 activates |
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

What it does is narrower. For an agent its principal wants bounded, Escapement gives a budget that
refills only on a human's signature, a set of delays on irreversible actions that no participant
can shorten, a veto any one guardian can use, liability that lands on a named human's coins, and a
record no single party can rewrite. For a service that wants to deal only with bounded agents, it
gives a check that needs no trusted server.

## Parameters

Every parameter below is a design choice, set in `data/inputs.toml` and varied with
`python3 model/escapement.py --set ID=VALUE`.

| Parameter | Reference value | Why |
|---|---|---|
| Tier 2 wait | [6 blocks](numbers.md#tier2-delay-blocks), [60 minutes](numbers.md#tier2-delay-mean-min) mean | the one-hour delay of the Async Control study [@stickland2025] |
| Tier 3 wait | [144 blocks](numbers.md#tier3-delay-blocks), [24 hours](numbers.md#tier3-delay-mean-h) mean | a full day for a human to look; the same length as the CSV fallback in a published Bitcoin agent-wallet design [@laz1m0v2026] |
| Lease | [144 blocks](numbers.md#lease-blocks) | a daily human renewal; lapse within a day |
| Season | [4,032 blocks](numbers.md#season-blocks), [28 days](numbers.md#season-days) | two difficulty periods; long enough that a swarm must be planned |
| Seal epoch | [6 blocks](numbers.md#seal-epoch-blocks) | matches the Tier 2 wait, so a Tier 2 commitment is sealed before its release |
| Allowance | [100,000 sats](numbers.md#allowance-per-lease) a lease | an example; set per agent |
| Coverage ratio | [1.0](numbers.md#coverage-ratio) | the bond covers what can be spent before a stop |

## Deployment path

**Today, with no consensus change.** The vault (pre-signed Unvault and Cancel, a co-signer), the
lease and allowance (a signed renewal, an NWC or on-chain budget), the bonds (timelocked outputs;
EOTS-style equivocation keys with pre-signed slashing), single-use seals and seal pools, and the
relying-party bundle all work under current rules. The trusted parts are the co-signer (for
destinations and amounts), the guardians (for vetoes and releases), the adjudicator (for harm
claims), and each relying party's own view of the chain.

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

If the first two fail, the thesis fails with them: a meter on commitments that are not where the
harm happens, or a delay that overseers cannot use, is not a safety mechanism.
