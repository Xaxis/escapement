# Why Bitcoin, and not a registry

The record needs two properties, completeness and costly identity, and section 4's bound needs
nothing else. A registry run by a lab, a consortium or a government could supply both. The case for
Bitcoin is therefore not that it is the only possible substrate but that it is the one the parties
who must adopt the record can share. That case rests on three arguments, none of which is a theorem.

## Nobody issues the unit

Stakes and bonds in Escapement are denominated in a unit that no participant issues; standing is a
score, and the training reward of section 5 is a log score. The unit matters because of an
elementary accounting fact (Proposition 14 of the formal statements [@escapement-formal]): in a scheme where every reward is a transfer from an identifiable payer, a coalition of
rewarded agents can gain only what outsiders pay in, whereas in a scheme that pays agents in newly
issued units according to a score they can influence, a coalition that captures the score captures
the issuance, with no outside payer at all. The second is reward tampering at the level of an
economy. Any fixed-supply asset issued outside the scheme avoids it; what Bitcoin adds is that its
issuance is outside the control of every lab, every state and every AI, and is enforced by the same nodes that validate the chain the record is kept on.

## Rivals can share it

The parties whose adoption matters most distrust each other. Competing labs are unlikely to score their agents on a rival's registry, and states that regard AI as strategic are unlikely to rely on a registry
another state can edit or switch off. A record kept on a chain that none of them controls, under
rules none of them can change alone, is one they can all read without trusting each other. This is
the ordinary logic of shared standards, where the standard that survives is often the one no
competitor owns. It is a conjecture about behaviour, not a finding, and it could be wrong if a
dominant platform or a group of states prefers a registry it controls and can make others use it.

The neutrality covers the commitment layer and nothing above it. Scoring needs an event list, a
baseline provider, resolvers and adjudicators (section 4), and each of those is a party that
relying parties trust and rivals may not share. So the honest form of the argument is that Bitcoin
lets rivals agree on what each agent committed to and when, while they may still disagree on who
keeps score.

## The stronger alternatives

A registry run by one party is the weakest alternative, and two stronger ones exist. Append-only
transparency logs, watched by monitors and cosigned by independent witnesses, give
non-equivocation, and completeness for a monitor that reads the whole log, with no mining and no
fees [@laurie2013ct; @syta2016]. A chain with general smart contracts gives what Bitcoin's script
lacks: covenants, expiry and programmable stakes. Against the first, Bitcoin adds a witness set that
anyone may join and that is paid to stay honest, timestamps that more cognition cannot produce
faster, and identities priced in the same unit as stakes. Against the second, it adds a unit and
rules that no issuer or foundation can change, at the price of the workarounds of section 2. Nothing
in this paper shows that either difference is worth its cost; a witnessed log with a bond per
identity may do everything the record needs.

## The clock cannot be run fast

Every height in the record, every wait in the tick chain and every lease is measured in blocks.
Running that clock faster means adding to the network's hashrate: doubling the block rate needs new
hardware drawing about [18.4 GW](../research/numbers.md#clock-2x-power-gw), costing about
[7.4 billion USD](../research/numbers.md#clock-2x-hardware-busd), and gains only
[7 days](../research/numbers.md#clock-2x-days-gained) before the next difficulty adjustment cancels
it. Shrinking a day-long Tier 3 wait to an hour needs
[24 x](../research/numbers.md#tier3-compress-factor) the network's hashrate, hardware drawing about
[423 GW](../research/numbers.md#tier3-compress-power-gw), about
[8 x](../research/numbers.md#tier3-compress-vs-datacentres) the power of every data centre in the
world in 2025. These figures rest on a vendor's specification of current mining hardware, a reported
hardware price and an energy agency's estimate of data-centre demand [@hri-s21; @ct-bitmain;
@iea-2026]. The costs do not fall as an agent becomes faster or more capable; they fall only as
hashrate becomes cheaper. That proof of work is a clock, and that a release timed by it can be
advanced only by overtaking the network's hashrate, are prior observations [@trubetskoy2018;
@yang2022]. The cost is also not what protects the design's waits: a pool with
[27.8%](../research/numbers.md#pool-largest-share) of blocks reorganises a veto six blocks deep with probability up to
[8.9%](../research/numbers.md#reorg-p-largest-6) without speeding the clock at all (section 8). The clock has two further
limits. It binds only actors below a hashrate majority, and while
the energy cost of new hashrate does not fall with intelligence, the cost of borrowing existing
hashrate, by renting it or bribing pools, may. A registry's clock is whatever its operator's server
reports.

The clock has a known crack. The timewarp bug lets a hashrate majority manipulate timestamps so that
difficulty falls and blocks come much faster, after weeks of visible preparation; its fix is
specified in BIP-54 and not active [@bip54; @optech-timewarp]. Heights in the record are not
directly affected, since they count blocks rather than seconds, but every wait measured in blocks
becomes shorter in wall-clock time while an attack runs.

## What Bitcoin costs

The same scarcity that makes the unit neutral makes the substrate expensive. Each tick is a
transaction, and blockspace is sold at auction: the median fee rate was
[1 sat/vB](../research/numbers.md#feerate-2026) across 2026 but
[200 sat/vB](../research/numbers.md#feerate-halving) in the halving block. The chain holds about
[144,000,000 vB](../research/numbers.md#vbytes-per-day) a day. A Tier 2 release measured on regtest
costs [137 sats](../research/numbers.md#tick-release-cost-2026) at the 2026 median and
[27,400 sats](../research/numbers.md#tick-release-cost-halving) at the halving block's rate, and if
releases filled every block, about [44,000 identities](../research/numbers.md#tick-identities-max)
could release every six blocks. That bounds the total rate of releases, but weakly, since a release
can batch many commitments, and fee spikes fall hardest on the smallest identities. Read the other
way, it is a ceiling on the design itself: no more identities than that can release every window,
fewer than the faking example of section 4 would need. Bitcoin is slow by
design, which is the point for delays and a cost for everything else.
