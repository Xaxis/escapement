# The enforcement layer

The record decides who is trusted to act; the enforcement layer limits what an agent can do in the
moment, including an agent whose record is good until the day it is not. One part extends prior
work, narrowly: the tick chain. The lease is prior work applied to an agent's authority, and the rest
are building blocks, used and credited. Every Bitcoin piece below was built and checked on regtest,
against Bitcoin Core 32.1, in [104 checks](../research/numbers.md#lab-checks) that anyone can rerun
[@escapement-lab]. The checks show that the scripts, timelocks and proofs behave as described on one
node, with no adversary but the lab's own scripts and no fee market; they do not show that the
design withstands a live adversary. Where the build, or a later reviewer's check on it, broke what
the first design claimed, this section says so.

## The tick chain

Each identity has a chain of Taproot outputs T_0, T_1, ..., each spent by the next, pinned by the
outpoint of T_0 that its charter names. Output T_n's internal key is a nothing-up-my-sleeve point
tweaked by a hash of the charter identifier, the index n and the root committed in entry n, so the
output commits to one root and provably has no key path [@bip341]. Its script tree has four kinds
of leaf: `advance2`, which lets the agent alone spend after N2 blocks; `advance3`, which needs the
agent and every guardian after N3 blocks; one `veto_i` per guardian, which spends at once; and `renew`, which needs every guardian's signature. A veto pays to a halt output for index n whose only leaf is
`renew`, from which the guardians can restart the chain. The relative waits are enforced by BIP68
and BIP112 [@bip68; @bip112]. The construction follows Somsen's spacechains, a chain of spends one
per block from a key with no known secret tweaked by a commitment, enforced there by a covenant
[@somsen-spacechains]; the tick chain does without the covenant, putting relying parties' template
rules in its place.

To release a batch of commitments, the agent commits their Merkle-sum root in T_n by spending
T_{n-1}. For the next [6 blocks](../research/numbers.md#tier2-delay-blocks) (or
[144 blocks](../research/numbers.md#tier3-delay-blocks) for a batch with any Tier 3 commitment) the
only valid spend of T_n is a veto: any one guardian who objects, or who has not received the batch's
contents in full, spends T_n. Afterwards the agent spends T_n through an advance leaf, and the batch
is released once that spend is confirmed deeply enough. In the lab an early advance was rejected as non-final until N2 blocks after T_n, an `advance3` missing one guardian failed its signature
check, and after a veto every other spend of T_n failed as a double spend.

Consensus enforces the waits, the signatures and single spending, which gives three properties
(Propositions 1 to 4 of the formal statements [@escapement-formal]):

- **Rate.** Releases of one pinned chain are at least N2 blocks apart. The limit is per chain: an
  operator can split an action across identities, entries and relying parties.
- **One root per index.** The pinned chain has one T_n for each n, committing one root.
- **Completeness.** Entries run without gaps from T_0, for a verifier that walks the chain.

The rest are relying parties' rules, checked by recomputing keys from the template: that each
advance's output 0 is T_{n+1} built to the template, that a veto pays to the halt output, that only
links descending from the pinned T_0 count, that a commitment names its relying party, its action
and a deadline, that the root's sum does not exceed the charter's cap per entry, and that Tier 3
commitments came through `advance3`. The cap holds only if the guardians check the whole tree
inside the window: the lab found that a subtree which under-reports its sum passes for a relying
party whose leaf lies outside it, and a leaf that names no counterparty can be honoured by
several.

## What the build broke

The first design claimed that a release could be proved with two transactions and their Merkle
proofs, light enough for a phone or a chip. The lab broke that twice. Merkle proofs of transaction
ids leave out the witness, so the agent swapped in the `advance3` leaf with junk signatures, kept
the same id, and the verifier accepted a Tier 3 release that no guardian had signed. And two
transactions cannot show that T_n is the identity's own: anyone can fund a copy of the template for
any index, and guardians cannot spot one, because the root is hidden in the tweak. The agent funded
a copy of an entry that had been vetoed, advanced it, and the two-transaction proof was accepted.
The fix is a proof of the whole chain from the pinned T_0, with each link's witness proved under its
block's witness commitment (Proposition 5). It works, and it grows with the chain: [901 bytes](../research/numbers.md#chain-proof-bytes-per-link) a link on regtest, where Merkle
branches are short, and more on mainnet. Even then it proves that entries exist, not that none has
been added since: in the lab a truncated chain passed, and finding the hidden release took a scan
of full blocks.

The first design also had `renew` restart a chain halted by a veto, but a veto spends T_n, leaving
T_n's own `renew` leaf nothing to spend. The halt output fixes that, and exposes something worse: a
veto leaf cannot control where the veto pays, so one guardian that vetoes to its own key ends the
identity's chain for good and keeps its value, and the guardians together can renew and write an
entry the agent never made. An identity's record is hostage to any one of its guardians.

A fresh reviewer's checks on the same lab found two more faults [@escapement-redteam]. The pin is a
trusted input: one charter identifier carried two chains with different roots at entry 1, each
accepted from its own pin (section 3). And the agent's bid at the window's edge is not bounded by
what T_n holds: an advance can carry a pay-to-anchor output, and a child paying
[150,000 sats](../research/numbers.md#lab-bid-child-sats) from outside the chain, more than T_n's
[100,000 sats](../research/numbers.md#lab-bid-tick-sats), evicted a watchtower's veto, after which the verifier counted
the release.

## How final a veto is

A veto ends a batch in every chain that contains it. It does not end it in a chain that leaves it
out, and a miner who forks below the veto and overtakes the honest chain once the advance is valid
releases the batch. That is Nakamoto's catch-up problem [@nakamoto2008], with the depth equal to how
many blocks before the window's edge the veto confirmed. A Tier 2 window of six blocks can never
give a veto the [19 blocks](../research/numbers.md#depth-for-target-largest) that this design treats
as final against the largest pool: at six blocks that pool overtakes with probability up to
[8.9%](../research/numbers.md#reorg-p-largest-6), and the two largest together up to
[82%](../research/numbers.md#reorg-p-top2-6). Even a Tier 3 veto confirmed at once leaves the two largest together a chance of up to [12.79%](../research/numbers.md#reorg-p-top2-144). These treat a pool as one
miner and ignore the rewards it forfeits on a failed attempt, and no deliberate deep reorganisation
has been seen on Bitcoin, but a veto is only as final as a payment of the same depth.

Censorship is the other way to beat a veto. If half of all hashrate simply refused to mine it, a
six-block window would miss it [1.6%](../research/numbers.md#veto-miss-tier2-half) of the time,
against [4e-44](../research/numbers.md#veto-miss-tier3-half) for 144 blocks, but those figures
assume refusal, not bribery, and bribery is cheap [@winzer2019; @tsabary2021; @nadahalli2021;
@avarikioti2024]. At the window's edge the veto and the advance are both valid, so the edge is a fee
auction: in the lab, under full replace-by-fee, the agent's advance evicted the veto and the
watchtower won the slot back only by outbidding it. Vetoes are therefore built as TRUC (topologically restricted until confirmation) transactions with a pay-to-anchor output, so that any watchtower can raise their fee [@bip431; @core-28]. They must confirm well before the edge and carry fees in proportion to what the batch is worth; a veto
package measured [319 vB](../research/numbers.md#lab-veto-package-vbytes), about
[63,800 sats](../research/numbers.md#veto-cost-halving) at the halving block's fee rate. Because the
agent can bid with money from outside the chain, a veto is safe only if it confirms well before the
edge. A flood of transactions can still delay many vetoes at once [@harris2020]. A Tier 2 veto can
be reversed by a large pool with the probabilities above, and contested at the edge by a briber or a
well-funded agent; what Tier 2 offers is a cap on what a Tier 2 batch can be worth.

## The height-difference lease

Bitcoin script has no "not after" [@bip65; @bip68], so an agent's authority cannot be made to lapse
in script. The lease supplies the bound outside script without trusting anyone's clock. A renewal is
a signature by every guardian over the charter identifier, a counter, a block height h_k and the
hash of block h_k. A relying party counts a release only if it holds a renewal whose block is in its
best chain and the release was confirmed at a height between h_k and h_k + L.

**Proposition 6.** If the guardians sign no renewal after the chain's tip reaches h*, no release
confirmed above h* + L is counted by any relying party that follows the honest chain. The guardians
cannot sign over the hash of a block that does not yet exist, and the release's height is fixed by
its confirmation, so the agent cannot place it lower.

The check compares two heights in the same chain and never reads the relying party's clock. In the
lab it held as claimed: a renewal signed over a guessed future block hash was rejected, and the
verdicts did not change when block times jumped a year or when every clock function was disabled.
What it bounds is when a release is made, not when the released action is carried out, which needs
a fresh view of the tip; a relying party that is eclipsed sees an old one [@riard2020], and a
reorganisation near h_k + L can move a release across the boundary. Any one guardian can stop
renewals, so the lease ends an agent's authority within L blocks of the first guardian's
disappearance, which is the intended way for it to fail.

The lease is prior work. Substrate's mortal transactions sign the hash of a block and are valid only
for inclusion in a window after it, checked against the inclusion height [@substrate-mortality];
Yee states the same short leash for transactions in general, also checked at the including block
[@yee2022]; and a freshness window in Bitcoin height already exists for signed scores [@zeke2026].
Escapement applies the predicate to an agent's authority, with every guardian signing each
renewal.

## Building blocks

The remaining parts are prior work, and Escapement uses them as published: the allowance follows
wallet budgets and agent spending caps [@nwc-08; @lightninglabs2026], and the coverage bond follows
verifiable agent insurance [@hua2026vai]. @tab:blocks lists each with what it needs from
outside Bitcoin.

Table: Building blocks of the enforcement layer, what each needs from outside Bitcoin, and whose work it is. {#tab:blocks}

| Building block | What Bitcoin enforces | What it needs from outside | Prior work |
|---|---|---|---|
| Allowance per lease | a capped output, swept at each renewal | a co-signer that refuses after expiry | wallet budgets [@nwc-08]; agent caps [@lightninglabs2026] |
| Vault with cancel | a relative timelock and pre-signed cancels | watchtowers; a co-signer for destinations | Revault [@revault-tx]; vaults [@swambo2020] |
| Policy co-signing | a second key on every spend | an honest co-signer | Nunchuk's co-signer [@nunchuk-blog] |
| Lease-gated authority | (on Ethereum, a contract) | a guardian who renews | ERC-8370 [@erc8370] |
| Coverage bond | a timelocked output with an arbiter's path | an adjudicator | agent insurance [@hua2026vai] |
| Equivocation bond | key extraction on two signatures with one nonce | a place where receipts meet | accountable assertions [@ruffing2015]; Babylon [@babylon2023] |
| Anchored logs | existence by a block; one chain of seals | a logger; watchers who follow seals | OpenTimestamps [@todd-ots-2016]; a transparency profile [@fassbender2026]; Catena [@catena-2017]; Pikachu [@azouvi2022] |
| Costly identity | locked coins and their age | attestations that a human stands behind the keys | fidelity bonds [@belcher-2019] |
| Rate-limited spending | a minimum gap between spends | (in Chia, the coin's puzzle) | Chia's rate-limited wallet [@chia-rl-wallet]; rate-limiting nullifiers [@rln-docs] |

The lab built the co-signing and anchoring blocks as well: a co-signed spend was refused before its
wait and without the co-signer, and an entry anchored in a log verified through both the key-tweak
and the data-output forms.

Costly identity changes role now that the record is the core. It no longer has to sort honest agents from
dishonest ones, which it cannot do; it only has to make identities cost something, so that the
record can do the sorting (section 4). The first version also made the chip licence a reader of the
tick chain, with Bitcoin headers and a difficulty floor as the chip's clock. That is withdrawn. An
operator who stops feeding a chip headers freezes its view, so its lease never lapses; a floor set
relative to the last difficulty the chip accepted ratchets down one header at a time, so forging a
release costs a fraction of one block's work, not the dozens claimed; and one forged fork serves
every chip in a fleet. A chip clock would need full retarget validation that is safe against
timewarp, a local clock with a stated drift, and a cost per fleet. Renewal chips remain prior work
[@buterin2025dacc; @petrie2025flexheg2], and stockpiled licences their known weakness [@petrie2024].

## How final the record is

A record is as final as the chain under it. Using the measured pool shares [@mempool-pools] in
Nakamoto's formula [@nakamoto2008], the chance that the largest pool, at
[27.8%](../research/numbers.md#pool-largest-share) of blocks, ever rewrites an entry six deep is
[8.9%](../research/numbers.md#reorg-p-largest-6), and it falls under
[0.1%](../research/numbers.md#reorg-risk-target) only at
[19 blocks](../research/numbers.md#depth-for-target-largest). For the two largest pools colluding, at
[46.1%](../research/numbers.md#pool-top2-share), it takes
[552 blocks](../research/numbers.md#depth-for-target-top2), about
[3.8 days](../research/numbers.md#depth-for-target-top2-days). The formula treats a pool as one miner
and ignores what an attack would cost the pools, so these are upper bounds under collusion, not
forecasts. A reorganisation cannot shorten a wait, but a deep one could replace an entry, so scorers
treat entries as final only at the depth their risk tolerance names, and credit a forecast only if
its entry was that deep before the event resolved.
