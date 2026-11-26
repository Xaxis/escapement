# The enforcement layer

The record decides who is trusted to act; the enforcement layer limits what an agent can do in the
moment, including an agent whose record is good until the day it is not. Two of its parts are, as
far as our searches found, new: the tick chain and the height-difference lease. The rest are
building blocks from prior work, used and credited.

## The tick chain

Each identity has a chain of Taproot outputs T_0, T_1, ..., each spent by the next. Output T_n's
internal key is a nothing-up-my-sleeve point tweaked by a hash of the charter identifier, the index
n and the root committed in entry n, so the output commits to one root and provably has no key path
[@bip341]. Its script tree has four kinds of leaf: `advance2`, which lets the agent alone spend after
N2 blocks; `advance3`, which needs the agent and every guardian after N3 blocks; one `veto_i` per
guardian, which spends at once; and `renew`, every guardian's signature, which restarts a halted
chain. The relative waits are enforced by BIP68 and BIP112 [@bip68; @bip112].

To release a batch of commitments, the agent commits their Merkle-sum root in T_n by spending
T_{n-1}. For the next [6 blocks](../research/numbers.md#tier2-delay-blocks) (or
[144 blocks](../research/numbers.md#tier3-delay-blocks) for a batch with any Tier 3 commitment) the
only valid spend of T_n is a veto: any one guardian who objects, or who has not received the batch's
contents in full, spends T_n and the batch can never be released. Afterwards the agent spends T_n
through an advance leaf, and the batch is released once that spend is confirmed deeply enough.

Five properties follow from consensus rather than from any party's policy, and the formal appendix
proves each (Propositions 1 to 5):

- **Rate.** Releases of one identity are at least N2 blocks apart.
- **Veto.** A confirmed veto ends the batch for good, and during the window it is the only valid
  spend.
- **One root per index.** An identity cannot show two parties two different batches.
- **Completeness.** Entries run without gaps from the genesis outpoint, which is what makes the
  record of section 3 complete.
- **Light verification.** A release is proved by block headers, the link transactions with their
  Merkle proofs, the revealed leaf and the committed root. Every fact is a positive inclusion; none
  is a claim that something is unspent. A light client or a chip can therefore check a release.

Relying parties check what consensus cannot: that each advance's output 0 is built to the template,
that a commitment names them, their action and a deadline, that the root's sum does not exceed the
charter's cap per entry, that Tier 3 commitments came through `advance3`, and that they have not
acted on the commitment before.

The tick chain has two weaknesses. The veto must be mined inside its window, and miners can be bribed
to keep a timelocked contract's transaction out of blocks cheaply [@winzer2019; @tsabary2021;
@nadahalli2021]; if half of all hashrate refused to mine a veto, a six-block window would miss it
[1.6%](../research/numbers.md#veto-miss-tier2-half) of the time, against
[4e-44](../research/numbers.md#veto-miss-tier3-half) for 144 blocks. Vetoes therefore carry fees in
proportion to what the batch is worth, are built as TRUC transactions with a pay-to-anchor output
so that any watchtower can raise their fee [@bip431; @core-28], and large stakes go through the long
window. And at Tier 2 the chain is veto-based: if every guardian vanishes, batches keep being
released until the lease lapses, which bounds the exposure without needing a guardian online for
every release.

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

The check compares two heights in the same chain and never reads the relying party's clock. What a
clock is still needed for is the separate question of how late a released action may be carried
out. Any one guardian can stop renewals, so the lease also ends an agent's authority within L blocks
of the first guardian's disappearance, which is the intended way for it to fail.

## Building blocks

The remaining parts are prior work, and Escapement uses them as published. Table @tab:blocks lists
each with what it needs from outside Bitcoin.

Table: Building blocks of the enforcement layer, what each needs from outside Bitcoin, and whose work it is. {#tab:blocks}

| Building block | What Bitcoin enforces | What it needs from outside | Prior work |
|---|---|---|---|
| Allowance per lease | a capped output, swept at each renewal | a co-signer that refuses after expiry | wallet budgets [@nwc-08]; agent caps [@lightninglabs2026] |
| Vault with cancel | a relative timelock and pre-signed cancels | watchtowers; a co-signer for destinations | Revault [@revault-tx] |
| Policy co-signing | a second key on every spend | an honest co-signer | Nunchuk's co-signer [@nunchuk-blog] |
| Lease-gated authority | (on Ethereum, a contract) | a guardian who renews | ERC-8370 [@erc8370] |
| Coverage bond | a timelocked output with an arbiter's path | an adjudicator | agent insurance [@hua2026vai] |
| Equivocation bond | key extraction on two signatures with one nonce | a place where receipts meet | accountable assertions [@ruffing2015]; Babylon [@babylon2023] |
| Anchored logs | existence by a block; one chain of seals | a logger; watchers who follow seals | OpenTimestamps [@todd-ots-2016]; a transparency profile [@fassbender2026]; Catena [@catena-2017] |
| Costly identity | locked coins and their age | attestations that a human stands behind the keys | fidelity bonds [@belcher-2019] |
| Chips renewed by signature | headers as a lower bound on work | a chip that checks headers and enforces a floor | renewal chips [@buterin2025dacc]; flexHEG [@petrie2025flexheg2] |

Two of these change role under the new core. Costly identity no longer has to sort honest agents
from dishonest ones, which it cannot do; it only has to make identities cost something, so that the
record can do the sorting (section 4). And the chip licence becomes a reader of the tick chain: a
chip that verifies a release from headers runs a workload only once Bitcoin shows that the batch
naming it waited out its window without a veto. Forging that release for a chip that rejects headers
below a quarter of the last difficulty it accepted takes about
[38 blocks of work](../research/numbers.md#chip-forge-blocks-tier3) for a Tier 3 release with six
confirmations, roughly [120,000 MWh](../research/numbers.md#chip-forge-mwh-tier3) at today's
efficiency.

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
treat entries as final only at the depth their risk tolerance names.
