# Why Bitcoin, and not a registry

The record needs two properties, completeness and costly identity, and section 4's bound needs
nothing else. A registry run by a lab, a consortium or a government could supply both. The case for
Bitcoin is therefore not that it is the only possible substrate but that it is the one the parties
who must adopt the record can share. That case rests on three arguments, none of which is a theorem.

## Nobody issues the unit

Stakes, standing and training rewards in Escapement are denominated in a unit that no participant
issues. That matters because of an elementary accounting fact (Proposition 14 in the formal
appendix): in a scheme where every reward is a transfer from an identifiable payer, a coalition of
rewarded agents can gain only what outsiders pay in, whereas in a scheme that pays agents in newly
issued units according to a score they can influence, a coalition that captures the score captures
the issuance, with no outside payer at all. The second is reward tampering at the level of an
economy. Any fixed-supply asset issued outside the scheme avoids it; what Bitcoin adds is that its
issuance is outside the control of every lab, every state and every AI, and is enforced by the same
nodes that enforce the record.

## Rivals can share it

The parties whose adoption matters most distrust each other. Competing labs will not score their
agents on a rival's registry, and states that regard AI as strategic will not rely on a registry
another state can edit or switch off. A record kept on a chain that none of them controls, under
rules none of them can change alone, is one they can all read without trusting each other. This is
the ordinary logic of shared standards, where the standard that survives is often the one no
competitor owns; it is an argument about coordination, and it could be wrong if a dominant platform
or a group of states prefers a registry it controls and can make others use it.

## The clock cannot be run fast

Every height in the record, every wait in the tick chain and every lease is measured in blocks.
Running that clock faster means outpacing the network's hashrate: doubling the block rate needs new
hardware drawing about [18.4 GW](../research/numbers.md#clock-2x-power-gw), costing about
[7.4 billion USD](../research/numbers.md#clock-2x-hardware-busd), and gains only
[7 days](../research/numbers.md#clock-2x-days-gained) before the next difficulty adjustment cancels
it. Shrinking a day-long Tier 3 wait to an hour needs
[24 x](../research/numbers.md#tier3-compress-factor) the network's hashrate, hardware drawing about
[423 GW](../research/numbers.md#tier3-compress-power-gw), about
[8 x](../research/numbers.md#tier3-compress-vs-datacentres) the power of every data centre in the
world in 2025. These costs do not fall as an agent becomes faster or more capable; they fall only as
hashrate becomes cheaper. That is the precise sense of the claim that Bitcoin is a clock an AI
cannot speed up. A registry's clock is whatever its operator's server reports.

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
[144,000,000 vB](../research/numbers.md#vbytes-per-day) a day, which bounds how many identities can
tick often (section 8), and fee spikes fall hardest on the smallest identities. Bitcoin is slow by
design, which is the point for delays and a cost for everything else.
