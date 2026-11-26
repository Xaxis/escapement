# What Bitcoin enforces, and what it does not

Bitcoin's rules are enforced by every node that validates blocks, which is what makes them hard for
any single party, including an agent's operator, to lift. But they are few. This section sets out
exactly what they cover, because the record and every mechanism under it inherit their limits.

## Four things an agent cannot fake

**Sats.** The issuance schedule is fixed by consensus [@nakamoto2008]. An agent cannot create
bitcoin. It can earn, borrow, be given or steal it, and nothing in Bitcoin distinguishes coins an
agent acquired honestly from coins it did not. Scarcity therefore bounds an agent only through the
coins someone chooses to hand it.

**Block time.** Blocks are found by a Poisson process tuned by difficulty adjustment to about
[600 s](../research/numbers.md#block-interval-s) apart, retargeted every
[2,016 blocks](../research/numbers.md#blocks-per-retarget) [@nakamoto2008]. Producing blocks faster
requires more hashrate, and the network ran at about
[1,052 EH/s](../research/numbers.md#hashrate-eh) when we measured it [@mempool-hashrate]. Thinking
faster does not help. A delay counted in blocks is therefore a delay no amount of cognition can
shorten, though capital can, at a cost section 8 computes.

**Keys.** Bitcoin's signatures are Schnorr signatures over secp256k1 [@bip340]. A signature
cannot be produced without its key. Keys can be stolen, and the humans who hold them can be
persuaded or deceived, but they cannot be forged.

**A public record.** Each block commits to its predecessor and to its transactions under proof of
work. Rewriting a buried transaction means outmining the honest chain from that point
[@nakamoto2008]. Commitments placed in the chain inherit this: a hash in a block cannot be quietly
replaced. Linked timestamping, the idea underneath, predates Bitcoin by nearly two decades
[@haber1991].

## What script can and cannot say

Script, Bitcoin's spending-condition language, checks keys, hashes and timelocks. Since Taproot it
can hide alternative spending paths in a Merkle tree and reveal only the one used [@bip341;
@bip342], and multi-party keys can be aggregated with MuSig2 [@bip327] or split into threshold
shares with FROST [@komlo2021]. That is enough to write "the agent's key and a human's key", "any
two of three", "the human alone after a year" and "nobody before block h".

Script cannot do four things this paper needs, and the design must work around each.

1. **It cannot make a spend expire.** Timelocks are lower bounds only: absolute with
   `OP_CHECKLOCKTIMEVERIFY` [@bip65] and relative to an output's confirmation with
   `OP_CHECKSEQUENCEVERIFY` [@bip112; @bip68]. There is no "not after", by design, so that a valid
   transaction does not become invalid in a reorganisation. The standard workaround is a competing
   path that becomes valid later, as in Lightning's timeouts or Liana's recovery keys
   [@liana-readme]. An agent's authority cannot be made to lapse in script; it can only be
   outraced.
2. **It cannot read amounts or destinations.** Script cannot check how much is spent, to whom, or
   how much has been spent before. Spending limits, velocity limits and destination allowlists are
   therefore policies of a co-signer who refuses to sign, not rules of consensus. Carriere's draft
   for co-signer policies states the right discipline: whatever script can enforce must be
   enforced there, and the co-signer's policy defines only what script cannot
   [@optech-2026-11-06].
3. **It has no covenants.** Opcodes that would let an output restrict the transaction spending it,
   such as `OP_CHECKTEMPLATEVERIFY` [@bip119] or `OP_CHECKSIGFROMSTACK` [@bip348], are drafts;
   `OP_VAULT`, which would have enforced "wait, then spend anywhere, except a recovery path", is
   closed [@bip345]. None is active, and an open letter in 2025 asking Core contributors to
   prioritise two of them [@optech-2025-07-04] has not led to a scheduled activation. Destination
   restrictions today need pre-signed transactions or co-signers, as Revault's vault design does
   [@revault-tx].
4. **It cannot see off chain.** Script binds bitcoin and nothing else. An API call, a code
   deployment, a message or a cloud purchase is outside its reach entirely.

## Bitcoin's practical limits

**Throughput and fees.** A block holds at most
[4,000,000 WU](../research/numbers.md#block-weight-limit) [@bip141], about
[144,000,000 vB](../research/numbers.md#vbytes-per-day) a day. Space is sold by auction: the median
fee rate was [1 sat/vB](../research/numbers.md#feerate-2026) across 2026 and
[15 sat/vB](../research/numbers.md#feerate-2023) across 2023, and the median in the halving block
was [200 sat/vB](../research/numbers.md#feerate-halving) [@mempool-feerates; @mempool-block840000].
Any mechanism that needs a transaction to confirm by a deadline is exposed to a fee spike.

**Mining concentration.** The largest pool mined
[27.8%](../research/numbers.md#pool-largest-share) of blocks over the trailing year and the two
largest [46.1%](../research/numbers.md#pool-top2-share) together [@mempool-pools]. Pools have left
sanctioned transactions out of blocks [@b10c-ofac]. Finality and censorship resistance are only as
good as the pools' independence, which section 8 quantifies.

**A known flaw in the clock.** The timewarp bug lets a majority of hashrate manipulate timestamps
so that difficulty falls and blocks arrive far faster than ten minutes, after weeks of visible
setup [@optech-timewarp]. Its fix, part of BIP-54, is specified and not active [@bip54].

**Privacy.** Everything on chain is public. A bond reveals its owner's coins, and a stream of
commitments reveals an operator's activity. Taproot hides unused spending paths [@bip341], but
amounts and timing stay visible.

**Custody.** Every key is a target. The weakest component of any scheme in this paper is the
custody of the keys it depends on.

## What this means for AI

Put together, Bitcoin offers three hard guarantees and one soft one. Coins locked in script cannot
move without the keys and the waits the script names, whatever the agent, its operator or the lab's
control plane does. A wait counted in blocks cannot be shortened except by buying hashrate. A
commitment in a buried block cannot be replaced, and an output can be spent only once, so a chain of
outputs has one history. And, softly, anyone who chooses to check can verify all of this from block
headers and inclusion proofs, without trusting a server. The record of section 3 is built from the
last two: one history gives completeness, and height gives order. The enforcement layer of section 8
is built from the first two. Both inherit the gaps: no expiry, no view of amounts or destinations,
no reach off chain, and no protection against an agent that simply acquires coins of its own.
