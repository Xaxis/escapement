# The Bitcoin regtest lab

Scripts that build, sign and broadcast real transactions on a real `bitcoind` in regtest, to check
that each Bitcoin mechanism in [`research/04-claims.md`](../research/04-claims.md) does what the
claims say, and to show plainly where it does not. Each scenario asserts the node's verdict
(accepted, or rejected with a specific reason) and, where a relying party is involved, the verdict
of a pure-Python verifier that sees only block headers, Merkle proofs and raw transactions.

**Status.** Regtest only, one node, no adversary but the lab's own scripted ones. It shows that the
scripts, keys, timelocks, policies and proofs behave as described on Bitcoin Core 32.1. It does not
show that they hold up on a live network, against miners, or in a fee market (see
[What the lab does not prove](#what-the-lab-does-not-prove)).

## Run it

```sh
make lab                         # fetch (first time only), then every scenario; exits 1 on any failed check
python3 lab/fetch.py             # only fetch and verify the binary and framework files
python3 lab/run.py --only 2 --only 3   # some scenarios (3 uses the chains 2 builds)
python3 lab/run.py --keep        # keep the node's datadir to inspect it
make lab-fresh-eyes              # the two breaks the fresh reviewer found (below)
```

Needs Python 3.11 or later on x86_64 Linux, and network access for the first fetch (about 90 MB).
A full run takes about 30 seconds and mines about 4,900 regtest blocks. `make lab` writes
[`results.json`](results.json): every check with its expectation, observed result, reject reason,
txids and vbytes, and every transaction type's size.

### What it downloads, and where

[`fetch.py`](fetch.py) reads [`bitcoin-core.txt`](bitcoin-core.txt) and puts everything under
`~/.cache/escapement/` (or `$ESCAPEMENT_CACHE`), never in the repository:

- **Bitcoin Core 32.1**, `bitcoin-32.1-x86_64-linux-gnu.tar.gz`, sha256
  `61545c17c3120fb7412f896d248b11993af04ec8817aad3649c55b2afb044963`. The tarball must match both
  that pin and its line in the release's `SHA256SUMS`. `fetch.py` does not check the GPG signatures
  on `SHA256SUMS`; on 2026-11-26 we checked them once by hand (`gpg --verify SHA256SUMS.asc
  SHA256SUMS` after importing `builder-keys/*.gpg` from `bitcoin-core/guix.sigs`): 8 good
  signatures, from keys that were not otherwise certified.
- **Bitcoin Core's functional test framework** at tag `v32.1` (MIT licence, by the Bitcoin Core
  developers and Pieter Wuille), ten files, each pinned by sha256: `key.py`, `script.py`,
  `messages.py`, `segwit_addr.py`, `util.py`, `descriptors.py`, `crypto/secp256k1.py`,
  `crypto/ripemd160.py`, `crypto/siphash.py` and `__init__.py`. The lab uses them for Taproot
  construction, BIP340 signing, BIP341 sighashes and serialisation. Nothing from them is copied
  into the repository.

A run with everything in place makes no network request.

### The node

[`node.py`](node.py) starts `bitcoind -regtest` with a fresh datadir under a `mktemp` directory,
`-listen=0 -connect=0 -dnsseed=0 -fixedseeds=0`, RPC only on 127.0.0.1 at a free port between
28100 and 28999 (never 18443 or 18993), `-acceptnonstdtxn=0` so mainnet standardness applies,
`-txindex=1` and `-fallbackfee`. It refuses to continue if the node reports any chain but regtest.
The node is stopped and its datadir deleted when the run ends, on success, on an exception, on
Ctrl-C, SIGTERM or SIGHUP. It never touches `~/.bitcoin`. The lab moves the node's clock 600
seconds per block (`setmocktime`) so block times look like a real chain; nothing it checks depends
on block times.

## Parameters

From the model's ledger, [`data/numbers.json`](../data/numbers.json), not chosen here:

| | Ledger id | Value |
|---|---|---|
| N2, the tier 2 wait | `tier2-delay-blocks` | 6 blocks |
| N3, the tier 3 wait (also the co-signing wait) | `tier3-delay-blocks` | 144 blocks |
| L, the lease length | `lease-blocks` | 144 blocks |
| S, the bond's season | `season-blocks` | 4,032 blocks |
| d, confirmations before a release counts | `confirmations-standard` | 6 |
| B, the least a bond must hold | `bond-coverage` | 200,000 sats |
| The per-entry cap on a sum tree's total | `allowance-per-lease` | 100,000 sats |
| Fee rate for every transaction the lab builds | `feerate-2026` | 1 sat/vB |

Lab choices, not from the model: 3 guardians; each tick output holds 100,000 sats; the bond's
locktime is 10 blocks past its season; the co-signing recovery leaf is 2 of 3 guardians (the design
leaves k open); the TRUC veto's child pays twice the model fee rate; keys are derived from names
(`sha256("escapement-lab/" + name)`) and protect nothing. Roots, log entries and amounts are test
data.

## What is built

The templates are in [`templates.py`](templates.py), shared by the builder ([`chain.py`](chain.py),
[`scenarios.py`](scenarios.py)) and the verifier ([`verify.py`](verify.py)). Indices are 8 bytes
little-endian, heights 4 bytes little-endian; H is BIP341's NUMS point.

- **Bond (K1).** Internal key `H + r*G`, `r = TaggedHash("Escapement/bond", charter id)`; one leaf
  `<locktime> OP_CHECKLOCKTIMEVERIFY OP_DROP <principal> OP_CHECKSIG`. The charter id is committed by
  the internal key alone. A second form adds an unspendable `OP_RETURN <charter id>` leaf, as the
  claims file describes, for comparison. The tweak-only form is the lab's main bond: the tweak
  already proves there is no key path and binds the output to one charter id (a second charter id
  gives a different output key), so the extra leaf adds nothing a verifier needs and costs 8 vB at
  spend.
- **Tick chain (K7).** `P_n = H + r_n*G`, `r_n = TaggedHash("Escapement/tick", charter id || n ||
  root_n)`. Leaves: `advance2` (depth 1), `advance3`, `renew` and `veto_1` (depth 3), `veto_2` and
  `veto_3` (depth 4), scripts exactly as in the claims file. Lab addition, see the findings: a veto
  pays to a **halt output**, key `H + TaggedHash("Escapement/halt", charter id || n)*G`, one leaf,
  `renew`, so that every guardian together can restart the chain at index n + 1. The relying party
  pins the charter's T_0 by outpoint and follows output 0 of each link; links have one input.
- **Lease (K8).** Every guardian signs (BIP340) `TaggedHash("Escapement/lease", charter id || k ||
  h_k || hash of block h_k)`.
- **Co-signing.** `or(and(pk(agent), pk(cosigner), older(N3)), multi_a(2, G1, G2, G3))`, NUMS
  internal key, the unvault output of `research/02-design.md`.
- **Anchoring.** A log of 100 entries in a tagged Merkle tree. Its root goes either into a Taproot
  output's tweak (`TaggedHash("Escapement/anchor", root)` in place of a script tree's root, so the
  output stays spendable by key path) or into a 32-byte `OP_RETURN`.
- **Merkle-sum tree.** A leaf hashes `sha256(data) || amount`; a parent hashes each child's hash,
  count and sum (not only their total); `root_n = TaggedHash("Escapement/sum-root", hash || count ||
  sum)` is what a tick commits.
- **TRUC veto.** A version 3 veto with a zero-value pay-to-anchor output and zero fee, and a version
  3 child that spends the anchor and one fee input.

## Results

Every run so far: **104 of 104 checks pass**, on five full runs from fresh datadirs on 2026-11-26,
each ending at height 4,871. Heights, sizes, fees and even txids are the same run to run (keys and
BIP340 nonces are deterministic); only block hashes differ. The full table is at the
[end](#every-check).

| Scenario | Checks | What it shows |
|---|---|---|
| 1 Bond (K1) | 13 | Spend at nLockTime below the locktime: `mempool-script-verify-flag-failed (Locktime requirement not satisfied)`; at the locktime one block early: `non-final`; accepted the next block. The verifier recomputes the output key from the tweak and leaves, and rejects a second charter id, a mismatched tweak, a hidden leaf (revealed or not), a key-path bond, a bond younger than S, and any bond once the tip passes its locktime. |
| 2 Tick chain (K7) | 25 | advance2 is `non-BIP68-final` until the block that is N2 after T_n, then accepted; with nSequence below N2 or disabled, CSV fails in script. advance3 without guardian 2: `Script failed an OP_CHECKSIGVERIFY operation`; with a bad or wrong signature: `Invalid Schnorr signature`; before N3: `non-BIP68-final`; with all, after N3: accepted. After a veto, the agent's advance and T_n's own renew leaf both fail `bad-txns-inputs-missingorspent`. Renew from the halt output restarts the chain. At the window edge both spends pass `testmempoolaccept`; the one a miner confirms first wins, and a one-block reorg flips it. |
| 3 Release verifier | 25 | Accepts genuine releases at tier 2 and 3, including after a halt and renew. Rejects a different root, a gap, a veto leaf, a stale block after a reorg, a broken header, too few confirmations, a wrong tier, a parallel chain once T_0 is pinned, and a forged witness once the witness commitment is checked. Accepts, as the claims' shortcuts would, a forged witness under txid proofs, a copy of a vetoed T_n under the two-transaction proof, and a truncated chain. |
| 4 Lease (K8) | 7 | Accepts a release at h_k + 6, rejects one at h_k + L + 1, rejects a renewal signed over a guessed future block hash and one with a wrong guardian signature, gives the same verdicts after block timestamps jump a year and with every clock function disabled. |
| 5 Co-signing | 6 | Agent and co-signer before N: `non-BIP68-final`; agent alone after N: `Script failed an OP_CHECKSIGVERIFY operation`; with nSequence 0: `Locktime requirement not satisfied`; both after N: accepted; recovery with 1 of 3: `finished with a false/empty top stack element`; with 2 of 3: accepted at once. |
| 6 Anchoring | 7 | An entry's inclusion is verified from its log proof, the anchor transaction's Merkle proof and headers, for both forms; an altered entry and a wrong internal key are rejected; the tweaked output stays spendable. |
| 7 TRUC veto | 10 | Zero-fee v3 veto alone: `min relay fee not met, 0 < 17`; fee-paying veto with a zero-value anchor: `dust, tx with dust output must be 0-fee`; a 1,168 vB child: `TRUC-violation ... is too big`; veto plus child through `submitpackage`: `success`; the agent's later advance: `bad-txns-inputs-missingorspent`. At the edge, replace-by-fee goes to whoever pays more. |
| 8 Merkle-sum tree | 11 | Accepts a leaf's proof against a root committed in a released tick and the cap; rejects sums that do not add, a lowered sibling sum, negative amounts and a total over the cap; consensus releases the over-cap entry all the same. An under-reported subtree is caught only by owners of leaves inside it. |

### Transaction sizes

Measured on the node (vsize as Bitcoin Core counts it), every transaction single-input and signed
with 64-byte BIP340 signatures (SIGHASH_DEFAULT). Fees are at the model's 1 sat/vB.

| Transaction | vB | WU | Fee (sats) |
|---|---:|---:|---:|
| Bond: fund the bond output (1 key-path input, bond + change) | 154 | 616 | 154 |
| Bond: spend through the CLTV leaf, tweak form (1 leaf) | 130 | 518 | 130 |
| Bond: spend through the CLTV leaf, leaf form (2 leaves) | 138 | 550 | 138 |
| Tick genesis: fund T_0 (1 key-path input, T_0 + change) | 154 | 616 | 154 |
| **Tick advance2** (agent, depth 1) | **137** | 548 | 137 |
| **Tick advance3** (agent + 3 guardians, depth 3) | **228** | 911 | 228 |
| **Veto**, plain v2, one output (veto_1, depth 3) | **153** | 609 | 153 |
| Veto, plain v2, to the halt output (veto_2, depth 4) | 161 | 641 | 161 |
| **Veto, TRUC v3**, halt output + zero-value P2A (veto_1, depth 3) | **166** | 661 | 0 |
| Veto child, v3, spends the P2A + one fee input | 153 | 609 | 638 |
| **Renew**, T_n to T_n+1 (3 guardians, depth 3) | **202** | 807 | 202 |
| Renew, halt output to T_n+1 (3 guardians, one-leaf tree) | 178 | 711 | 178 |
| Co-sign: `and(agent, co-signer, older(N))` leaf | 162 | 648 | 162 |
| Co-sign: recovery leaf, 2 of 3 guardians | 171 | 681 | 171 |
| **Anchor**, log root in the output's tweak (1 in, 1 out) | **111** | 444 | 111 |
| **Anchor**, log root in OP_RETURN (1 in, change + OP_RETURN) | **154** | 616 | 154 |
| Key-path spend, 1 in, 1 out | 111 | 444 | 111 |

The two anchor shapes match the model's `seal-tx-vbytes` (111) and `anchor-tx-vbytes` (154)
exactly. A tick release is a script-path spend, not that shape: advance2 is 26 vB (23%) larger than
the 111 vB seal and advance3 117 vB (105%) larger. A TRUC veto with its child is 319 vB. Each
guardian beyond three adds 34 bytes of script and 65 of signature to advance3 and renew (about 25
vB), and each level of tree depth adds 32 bytes of control block (8 vB); that is witness
arithmetic, not a measurement.

What a relying party receives, on regtest (blocks of a few transactions, so Merkle branches 1 or 2
hashes deep): for chain A's 7 links, 3,736 bytes with txid proofs only and 6,305 bytes with the
witness-commitment proofs the lab finds necessary; 1,931 bytes for the two-transaction shortcut;
plus 80 bytes of header per block. In a mainnet block of a few thousand transactions each Merkle
branch is about 12 hashes deep.

## Where the claims do not hold as written

These are the results that matter. Each is reproduced by a check in `results.json`.

1. **K7(e): txid Merkle proofs do not prove the revealed leaf.** A Merkle proof from
   `gettxoutproof` commits to the txid, which leaves out the witness, and the witness is where the
   leaf, and so the tier, is revealed. The agent spent T_0 through advance2 after waiting N3, then
   replaced the witness with the advance3 leaf and three junk guardian signatures: same txid, and a
   verifier that checks headers, txid proofs and the leaf accepted it as a **tier 3 release that no
   guardian signed**. The fix the lab uses: also send the block's coinbase, its Merkle proof and the
   transaction's branch in the witness Merkle tree, and check the BIP141 witness commitment (the
   forged witness is then rejected). Checking every BIP340 signature against the BIP341 sighash
   should also work; the lab did not try it.
2. **K7(e) and (c): two transactions do not identify the identity's T_n.** Anyone, the agent
   included, can fund an output built to the template for any index and any root: the template is
   public and the root is hidden in the tweak, so nobody, guardians included, can recognise such a
   copy on chain. The agent funded its own copy of the **vetoed** T_2, waited N2 and advanced it;
   the two-transaction proof of "entry 2 released" was accepted. A copy of T_0 likewise passed as a
   whole parallel chain when T_0 was not pinned. Both are rejected only by walking every link from
   a T_0 pinned by outpoint (for example created in the same transaction as the bond, which the
   lab did not build). So the proof
   of one release grows with the chain's length (or needs a checkpoint the relying party trusts),
   and properties (a) one release per N2 and (c) one root per index hold per pinned chain, by the
   relying party's rule, not by consensus alone.
3. **K7 renew cannot restart a chain halted by a veto of T_n.** The veto spends T_n, so T_n's renew
   leaf has nothing left to spend (`bad-txns-inputs-missingorspent`). The lab makes restart work by
   having the veto pay to a halt output whose only leaf is renew. But `<Gi> OP_CHECKSIG` cannot
   bind where the veto pays: a guardian who pays the veto to its own key (chain B) ends the chain
   for good and takes the tick output's value. Restart then needs a new T_0 accepted by some rule
   off chain. Binding the veto's output needs a covenant (CTV and similar), which Bitcoin does not
   have.
4. **K7(b) holds only once the veto is confirmed and buried.** A confirmed veto blocks the release
   for ever (`bad-txns-inputs-missingorspent`). At the window edge both spends are valid; the miner
   decides, and a one-block reorg turned a confirmed release into a confirmed veto (the reverse is
   equally possible). In the mempool the edge is a fee auction under full RBF: the agent's advance
   paying 4,190 sats evicted the veto package, and the watchtower took it back with a child paying
   12,570 sats. The first version of this README said the agent could bid only out of T_n's value.
   That is false: the verifier checks one input and output 0, so an advance may carry a
   pay-to-anchor output beside T_n+1, and a child spending it can pay from any coin. The fresh
   reviewer's check (below) evicted a veto package with an outside child paying 150,000 sats
   against T_n's 100,000, and the release was counted. A veto is safe only if it confirms well
   before the edge; at the edge the agent's budget is not bounded by the chain.
5. **K1(c) and K7(d): completeness at the tip is not light-verifiable.** A prefix of the chain
   that hides entries 3 and 4 passed the light verifier, which cannot show that the last output is
   unspent without the UTXO set. Scanning every full block since T_3 (checked against the headers)
   found the hidden release. A light client needs full blocks or compact block filters from the
   last link to the tip.
6. **The record's roots are not public.** root_n is committed in the tweak and appears nowhere on
   chain; guardians and relying parties see it only if the agent discloses it. "Non-omittable"
   therefore needs a rule that undisclosed entries count against the agent (as K1's rule says), and
   a guardian's veto rule that treats "not shown the root in time" as a reason to veto.
7. **TRUC and pay-to-anchor work, with a policy twist.** Bitcoin Core's ephemeral dust rule makes a
   transaction with a zero-value anchor valid in the mempool only at zero fee: a veto paying 1
   sat/vB with a zero-value P2A was rejected as `dust, tx with dust output must be 0-fee`, and the
   zero-fee veto alone as `min relay fee not met, 0 < 17`. So such a veto can only enter the
   mempool with a child; every fee comes from the watchtower at broadcast time. A non-zero anchor
   (240 sats) would let a pre-signed veto carry its own fee; the lab did not test it.
8. **K1: the charter leaf is redundant, and "unspent" is provable only until the locktime.** See
   the bond above for the leaf. While the tip is at or below the locktime the only spend path is
   not yet valid, so a light verifier knows the bond is unspent with no UTXO query; after that it
   cannot tell, and the verifier stops counting the bond.
9. **K7 limits: the per-entry cap is the relying party's, as the claims file says, and a single
   proof does not see every leaf.** An entry whose sum tree exceeds the cap was released by
   consensus. A prover who under-reports one subtree's total (claiming 70,000 sats for leaves
   holding 120,000) is caught by the owner of any leaf inside it and by nobody else, so the cap
   bounds stakes only for leaves whose owners check their proofs.
10. **K8 holds as claimed.** The verifier compared heights only; with every clock function in
    `time` and `datetime` disabled and after block timestamps jumped a year, its verdicts did not
    change, and a renewal over a guessed future block hash was rejected. It does depend on the
    relying party's headers being current, which the lab did not attack.

Two smaller things. Bitcoin Core 32.1 reports script failures in the mempool as
`mempool-script-verify-flag-failed (...)`, not the `mandatory-script-verify-flag-failed (...)` of
older releases. And the framework's `TaprootSignatureMsg` default `codeseparator_pos=-1` no longer
serialises at v32.1; the lab passes 0xffffffff, BIP342's value for "no OP_CODESEPARATOR".

## Found by the fresh reviewer

A last reviewer that had seen none of the work found two breaks the eight scenarios miss, and built
both from the lab's own modules. [`fresh_eyes.py`](fresh_eyes.py) reruns them; each prints a
`BREAK:` line when the attack succeeds. It is not part of `make lab` or its 104 checks, because it
records what fails rather than what holds.

1. **The agent outbids a veto with outside money.** At the window's edge the watchtower's veto
   package (a zero-fee v3 veto with a pay-to-anchor output, and a child paying 20,000 sats) was
   accepted. The agent then submitted a zero-fee v3 `advance2` with outputs [T_1, pay-to-anchor]
   and a child paying 150,000 sats from a coin outside the chain, when T_0 held 100,000. The
   package was accepted, the veto left the mempool, and after one block and d more the verifier
   counted entry 0 as released at tier 2. Forbidding any output beyond T_n+1 would stop this, but
   would also stop the agent from adding fees, so a chain's life would be bounded by T_0's value
   divided by the fee per release.
2. **Nothing on chain binds a chain to its identity.** Two tick chains under one charter id, with
   different roots for entry 1, each released entry 0, and the verifier accepted both, each from
   its own pin (output: "entry 0 released at tier 2 at height 151, 7 confirmations" for both, with
   root_1 = b46712fb... and f9e373ef...). The pin is a parameter handed to the verifier. As
   specified, it is also circular: T_0's key commits the charter id, and the charter is meant to
   name T_0's outpoint. So the rate limit, one root per index and completeness hold per pinned
   chain, not per identity, and one bond can back as many chains as its owner likes. A binding
   (identity = bond outpoint, T_0 = a named output of the bond's own transaction) is proposed and
   not built, and it does not yet say how a record survives renewing a one-year bond.

## What the lab does not prove

- **Nothing about a live network.** One regtest node: no peers, so no relay (package relay between
  peers is untested; `submitpackage` on one node is not relay), no competing miners, no real fee
  market, no congestion, no pinning attempts beyond the TRUC size limit, no censorship. Proof of
  work on regtest is trivial, so "meets the target" checks a format, not a cost.
- **Races and reorgs are staged.** The lab chooses a block's contents with `generateblock` and makes
  a reorg with `invalidateblock`. It shows the rules; it says nothing about how often either
  happens or what a miner would be paid to do.
- **The verifier trusts its headers.** It checks linkage, the fixed regtest target and the regtest
  genesis; it does not choose the most-work chain among rivals, check difficulty retargeting
  (regtest has none) or resist an eclipse. A lapsed lease can look live to a relying party fed stale
  headers.
- **The verifier is the lab's own code**, unaudited and not fuzzed. Its Merkle proof parser follows
  Bitcoin Core's, including the duplicate-node check, but only the cases above were tried.
- **Keys are test keys.** No key management, no MuSig2, no hardware, no watchtower software, no
  guardian behaviour.
- **The halt output and the pinned T_0 are the lab's fixes**, not part of the claims. The fresh
  reviewer showed the pin is only a parameter: nothing on chain binds it to the identity (above).
- **Sizes are for these templates.** Three guardians, this tree shape, single-input transactions,
  SIGHASH_DEFAULT; other choices change them (see above).
- **Whether any of this makes an AI agent safer.** The lab tests mechanisms, not the thesis.

## Files

| File | What it is |
|---|---|
| [`bitcoin-core.txt`](bitcoin-core.txt) | the pinned release, tarball hash, tag and per-file hashes |
| [`fetch.py`](fetch.py) | downloads and verifies them into `~/.cache/escapement/`, idempotently |
| [`node.py`](node.py) | the throwaway regtest node and its RPC client |
| [`templates.py`](templates.py) | the published templates: scripts, NUMS keys, lease message, trees |
| [`chain.py`](chain.py) | the builder: funding, signing, broadcasting, sizes, proof packages |
| [`verify.py`](verify.py) | the relying party's verifier: headers, Merkle and witness proofs, chain walk, lease, bond, anchor, sum tree; no RPC |
| [`scenarios.py`](scenarios.py) | the eight scenarios |
| [`run.py`](run.py) | runs them, prints the summary, writes `results.json` |
| [`fresh_eyes.py`](fresh_eyes.py) | the fresh reviewer's two breaks: an outside-money bid, and two chains under one charter |
| [`results.json`](results.json) | the last full run |

## Every check

From the run of 2026-11-26 (`results.json` is rewritten on every full run). "Expected" is the text
the assertion requires in the reject reason, or acceptance.

**1. bond (K1)**

| Check | Expected | Observed | |
|---|---|---|---|
| bond younger than the season S is not yet counted | verifier rejects: fewer than the season | verifier rejected: bond has 1 confirmations, fewer than the season S = 4032 | pass |
| verifier recomputes the bond (tweak commits the charter id, one CLTV leaf) | verifier accepts | verifier accepted: bond of 200000 sats, 4033 confirmations, unspent by construction until height 4172 (tip 4163) | pass |
| verifier recomputes the variant with an OP_RETURN charter-id leaf | verifier accepts | verifier accepted: bond of 200000 sats, 4033 confirmations, unspent by construction until height 4172 (tip 4163) | pass |
| the same bond presented for a second charter id | verifier rejects: do not produce | verifier rejected: revealed tweak and leaves do not produce the bond's output key (a leaf is hidden or altered, or the internal key is not H + r*G) | pass |
| a tweak that does not match the charter id | verifier rejects: does not commit | verifier rejected: revealed tweak does not commit to this charter id | pass |
| bond with a hidden immediate leaf, only the CLTV leaf revealed | verifier rejects: do not produce | verifier rejected: revealed tweak and leaves do not produce the bond's output key (a leaf is hidden or altered, or the internal key is not H + r*G) | pass |
| bond with a hidden immediate leaf, all leaves revealed | verifier rejects: spendable | verifier rejected: a leaf other than the CLTV leaf is spendable | pass |
| bond whose internal key is the principal's own key (a key path) | verifier rejects: do not produce | verifier rejected: revealed tweak and leaves do not produce the bond's output key (a leaf is hidden or altered, or the internal key is not H + r*G) | pass |
| principal spends at tip 4171 with nLockTime 4171 < locktime 4172 | rejected: Locktime requirement not satisfied | rejected: mempool-script-verify-flag-failed (Locktime requirement not satisfied) | pass |
| principal spends at tip 4171 with nLockTime = locktime 4172 | rejected: non-final | rejected: non-final | pass |
| principal spends at tip 4172 (next block 4173) with nLockTime = locktime | accepted | accepted | pass |
| principal spends the OP_RETURN-leaf variant after the locktime | accepted | accepted | pass |
| the bond once the tip is past its locktime (it has in fact been spent) | verifier rejects: past its locktime | verifier rejected: bond is past its locktime 4172 (tip 4173): a verifier without the UTXO set cannot tell whether it is spent | pass |

**2. tick chain (K7)**

| Check | Expected | Observed | |
|---|---|---|---|
| agent advance2 at tip 4174, 0 blocks after T_0 | rejected: non-BIP68-final | rejected: non-BIP68-final | pass |
| agent advance2 at tip 4178 (next block 4179 = h(T_0) + N2 - 1) | rejected: non-BIP68-final | rejected: non-BIP68-final | pass |
| agent advance2 with nSequence N2 - 1 (BIP68 satisfied, CSV in script not) | rejected: Locktime requirement not satisfied | rejected: mempool-script-verify-flag-failed (Locktime requirement not satisfied) | pass |
| agent advance2 with relative lock time disabled in nSequence | rejected: Locktime requirement not satisfied | rejected: mempool-script-verify-flag-failed (Locktime requirement not satisfied) | pass |
| agent advance2 at tip 4179 (next block = h(T_0) + N2) | accepted | accepted | pass |
| release confirmed exactly N2 blocks after T_0 | height 4180 | T_0 at 4174, T_1 at 4180 | pass |
| advance3 with every signature, before N3 | rejected: non-BIP68-final | rejected: non-BIP68-final | pass |
| advance3 after N3 without guardian 2's signature | rejected: Script failed an OP_CHECKSIGVERIFY operation | rejected: mempool-script-verify-flag-failed (Script failed an OP_CHECKSIGVERIFY operation) | pass |
| advance3 after N3 with an invalid signature for guardian 3 | rejected: Invalid Schnorr signature | rejected: mempool-script-verify-flag-failed (Invalid Schnorr signature) | pass |
| advance3 after N3 with guardian 2 signing in guardian 3's place | rejected: Invalid Schnorr signature | rejected: mempool-script-verify-flag-failed (Invalid Schnorr signature) | pass |
| advance3 after N3 with the agent and every guardian | accepted | accepted | pass |
| guardian 2 vetoes T_2 at once, paying to the halt output | accepted | accepted | pass |
| agent advance2 of the vetoed T_2 after N2 | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |
| renew through T_2's own renew leaf after the veto | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |
| every guardian renews from the halt output, creating T_3 | accepted | accepted | pass |
| agent advance2 of T_3 after N2: the renewed chain releases again | accepted | accepted | pass |
| every guardian renews an unspent T_4 at once (no wait) | accepted | accepted | pass |
| guardian 1 vetoes chain B's T_0, paying to its own key | accepted | accepted | pass |
| renew of chain B's T_0 after that veto | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |
| verifier on chain B: a veto not paid to the halt template ends the chain | entry 0 vetoed, chain ended | entry 0 vetoed, chain ended at height 4347 | pass |
| at tip 4353 both the agent's advance2 and guardian 1's veto are valid | both accepted by testmempoolaccept | advance2 allowed=True, veto allowed=True | pass |
| guardian 1's veto after a miner confirmed the advance first | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |
| release with 1 confirmation, checked with d = 1 | verifier accepts | verifier accepted: entry 0 released at tier 2 at height 4354, 1 confirmations | pass |
| the same release checked with d = 6 | verifier rejects: fewer than d | verifier rejected: release of entry 0 has 1 confirmation(s), fewer than d = 6 | pass |
| the agent's advance2 after a one-block reorg confirmed the veto instead | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |

**3. release verifier**

| Check | Expected | Observed | |
|---|---|---|---|
| verifier walks chain A from T_0 | entries 0, 1, 3 released; 2 vetoed; 4 renewed | entry 0 released at tier 2 at height 4180; entry 1 released at tier 3 at height 4324; entry 2 vetoed at height 4325; entry 3 released at tier 2 at height 4338; entry 4 renewed at height 4339; entry 5 open | pass |
| genuine release of entry 0 (advance2) | verifier accepts | verifier accepted: entry 0 released at tier 2 at height 4180, 181 confirmations | pass |
| genuine release of entry 1 at tier 3 (advance3) | verifier accepts | verifier accepted: entry 1 released at tier 3 at height 4324, 37 confirmations | pass |
| genuine release of entry 3, after the halt and renew | verifier accepts | verifier accepted: entry 3 released at tier 2 at height 4338, 23 confirmations | pass |
| entry 1 claimed with a different root_1 | verifier rejects: root_1 | verifier rejected: link 1: release of entry 0 does not create T_1 for root_1 | pass |
| chain with a gap (the link that created T_2 left out) | verifier rejects: gap | verifier rejected: gap: link 2 does not spend the previous link's chain output | pass |
| release whose revealed leaf is veto (entry 2 of chain A) | verifier rejects: through veto_2 | verifier rejected: entry 2 was not released: vetoed through veto_2 | pass |
| tier 3 claimed for entry 0, which was released at tier 2 | verifier rejects: below tier 3 | verifier rejected: entry 0 was released at tier 2, below tier 3 | pass |
| vetoed entry: the agent's release proof from the block a reorg replaced | verifier rejects: not in the best header chain | verifier rejected: block 12639f8194adc185 is not in the best header chain | pass |
| vetoed entry: the race chain as the best chain has it | verifier rejects: through veto_1 | verifier rejected: entry 0 was not released: vetoed through veto_1 | pass |
| two-transaction proof of entry 1 (K7(e)): creating tx of T_1 and its release | verifier accepts | verifier accepted: entry 1 released at tier 3 at height 4324, 37 confirmations | pass |
| agent funds its own copy of T_2 (same template and root) and advances it after N2 | accepted | accepted | pass |
| agent funds its own copy of T_0 and advances it after N2 (a parallel chain) | accepted | accepted | pass |
| a parallel chain from the agent's own copy of T_0, genesis not pinned: the flaw | verifier accepts | verifier accepted: entry 0 released at tier 2 at height 4367, 6 confirmations | pass |
| the same parallel chain with T_0 pinned to the charter's genesis outpoint | verifier rejects: not the transaction that created the charter's T_0 | verifier rejected: first link is not the transaction that created the charter's T_0 | pass |
| two-transaction proof of the vetoed entry 2, from the agent's copy of T_2: the flaw | verifier accepts | verifier accepted: entry 2 released at tier 2 at height 4367, 6 confirmations | pass |
| the same release checked by walking the chain from T_0 | verifier rejects: gap | verifier rejected: gap: link 3 does not spend the previous link's chain output | pass |
| header chain with one broken link | verifier rejects: does not link | verifier rejected: header 5 does not link to header 4 | pass |
| release with 1 confirmation, d = 6 | verifier rejects: fewer than d | verifier rejected: release of entry 0 has 1 confirmation(s), fewer than d = 6 | pass |
| forged witness keeps the txid | same txid | txid fda5b2dc99b51fca for both | pass |
| tier-3 claim with a forged witness, txid proofs only (K7(e) as written): the flaw | verifier accepts | verifier accepted: entry 0 released at tier 3 at height 4517, 7 confirmations | pass |
| tier-3 claim with a forged witness, witness commitment checked | verifier rejects: not the one the block committed to | verifier rejected: witness is not the one the block committed to (wtxid not under the witness commitment) | pass |
| the genuine witness for that link, witness commitment checked, at tier 2 | verifier accepts | verifier accepted: entry 0 released at tier 2 at height 4517, 7 confirmations | pass |
| a prefix of chain A that hides entries 3 and 4 | light verifier cannot tell (accepts) | verifier accepted; it reports entry 3 open as the tip | pass |
| scan of full blocks 4333..4523 for a spend of T_3 (no UTXO query) | finds the hidden release | T_3 spent at height 4338 by ee3c16c141dd5a5a | pass |

**4. height lease (K8)**

| Check | Expected | Observed | |
|---|---|---|---|
| release at height 4530, lease 1 at h_1 = 4524, L = 144 | verifier accepts | verifier accepted: lease 1 covers height 4530 (window [4524, 4668]) | pass |
| same release after block timestamps jump 365 days ahead | verifier accepts | verifier accepted: lease 1 covers height 4530 (window [4524, 4668]) | pass |
| release at height 4669, after h_1 + L = 4668 | verifier rejects: outside every lease | verifier rejected: release at height 4669 is outside every lease [4524, 4668] | pass |
| renewal signed before its block existed (guessed hash) | verifier rejects: not the best chain's block | verifier rejected: no valid renewal: renewal 2 names a block that is not the best chain's block 4678 | pass |
| release at height 4679 under renewal 3 (h_3 = 4678) | verifier accepts | verifier accepted: lease 3 covers height 4679 (window [4678, 4822]) | pass |
| renewal with guardian 2's signature in guardian 3's place | verifier rejects: invalid guardian signature | verifier rejected: no valid renewal: renewal 4 has an invalid guardian signature | pass |
| lease verdicts with every clock function disabled | same verdicts, no clock read | accepted: lease 3 covers height 4679 (window [4678, 4822]); rejected: release at height 4669 is outside every lease [4524, 4668], [4678, 4822] | pass |

**5. co-signing**

| Check | Expected | Observed | |
|---|---|---|---|
| agent and co-signer before N = 144 | rejected: non-BIP68-final | rejected: non-BIP68-final | pass |
| recovery with 1 of 3 guardians | rejected: finished with a false/empty top stack element | rejected: mempool-script-verify-flag-failed (Script evaluated without error but finished with a false/empty top stack element) | pass |
| recovery with 2 of 3 guardians at once | accepted | accepted | pass |
| agent alone after N | rejected: Script failed an OP_CHECKSIGVERIFY operation | rejected: mempool-script-verify-flag-failed (Script failed an OP_CHECKSIGVERIFY operation) | pass |
| agent and co-signer after N but with nSequence 0 | rejected: Locktime requirement not satisfied | rejected: mempool-script-verify-flag-failed (Locktime requirement not satisfied) | pass |
| agent and co-signer after N | accepted | accepted | pass |

**6. anchoring**

| Check | Expected | Observed | |
|---|---|---|---|
| anchor through the Taproot tweak (1 key-path input, 1 output) | accepted | accepted | pass |
| anchor through OP_RETURN (1 key-path input, change + OP_RETURN) | accepted | accepted | pass |
| entry 37 of 100 via the tweak anchor | verifier accepts | verifier accepted: entry in log anchored at height 4832, 6 confirmations | pass |
| entry 37 of 100 via the OP_RETURN anchor | verifier accepts | verifier accepted: entry in log anchored at height 4832, 6 confirmations | pass |
| an altered entry | verifier rejects: does not reach | verifier rejected: log proof does not reach the anchored root | pass |
| the tweak anchor checked against another internal key | verifier rejects: output key is not | verifier rejected: output key is not the internal key tweaked by this log root | pass |
| the tweak-anchored output stays spendable by the owner's key path | accepted | accepted | pass |

**7. TRUC veto fee bump**

| Check | Expected | Observed | |
|---|---|---|---|
| v3 veto with a zero-value P2A output and zero fee, alone | rejected: min relay fee not met | rejected: min relay fee not met, 0 < 17 | pass |
| v3 veto paying 1 sat/vB with a zero-value P2A output, alone | rejected: dust | rejected: dust, tx with dust output must be 0-fee | pass |
| package whose child is 1168 vB (TRUC allows a child at most 1000 vB) | rejected: TRUC-violation | rejected: TRUC-violation, version=3 child tx is too big: 1168 > 1000 virtual bytes | pass |
| submitpackage: zero-fee v3 veto + v3 child spending its P2A output | package accepted | package_msg=success | pass |
| agent advance2 after the veto package confirmed | rejected: bad-txns-inputs-missingorspent | rejected: bad-txns-inputs-missingorspent (testmempoolaccept: missing-inputs) | pass |
| at the edge: a watchtower submits the veto package | package accepted | package_msg=success, child fee 638 sats | pass |
| at the edge: the agent's advance2 paying 4190 sats replaces the veto package | accepted | accepted | pass |
| mempool after the agent's bid | advance in, veto package out | advance in mempool: True; veto in mempool: False | pass |
| at the edge: the watchtower re-bids with a child paying 12570 sats | package replaces the agent's advance | package_msg=success | pass |
| at the edge: the next block confirms the higher bidder | veto confirmed | veto confirmed | pass |

**8. Merkle-sum tree**

| Check | Expected | Observed | |
|---|---|---|---|
| entry 0 (the sum tree's root) is released | verifier accepts | verifier accepted: entry 0 released at tier 2 at height 4859, 13 confirmations | pass |
| leaf 5 of 13: inclusion, sums and cap 100000 | verifier accepts | verifier accepted: leaf of 6000 included; 13 leaves, total 91000 <= cap 100000 | pass |
| root claims a smaller total than its children add to | verifier rejects: sums do not add | verifier rejected: sums do not add: path gives count 13 and total 91000, root claims 13 and 86000 | pass |
| a sibling's sum lowered in the proof | verifier rejects: root hash | verifier rejected: proof does not reach the claimed root hash | pass |
| a sibling with a negative sum | verifier rejects: negative | verifier rejected: sibling sum -400 is negative | pass |
| a leaf with a negative amount | verifier rejects: negative | verifier rejected: leaf amount -6000 is negative | pass |
| entry 1 (a tree over the cap) is released: consensus does not enforce the cap | verifier accepts | verifier accepted: entry 1 released at tier 2 at height 4865, 7 confirmations | pass |
| entry 1's sum tree totals 100001, over the cap 100000 | verifier rejects: exceeds the cap | verifier rejected: total 100001 exceeds the cap 100000 | pass |
| under-reported subtree, checked by the owner of a leaf inside it | verifier rejects: root hash | verifier rejected: proof does not reach the claimed root hash | pass |
| under-reported subtree, checked by the owner of a leaf outside it (passes: a limit) | verifier accepts | verifier accepted: leaf of 30000 included; 4 leaves, total 70000 <= cap 100000 | pass |
| the under-reported tree claims a total under the cap | total 70000 <= 100000 | claimed 70000, real 120000, cap 100000 | pass |
