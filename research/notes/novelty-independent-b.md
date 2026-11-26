# Independent prior-art search B: claims K7, K8, K9

Searcher B, 2026-11-26. Scope: K7 (tick chain), K8 (height-difference lease), K9 (block clock).
Read only `research/04-claims.md` from the repository; did not read `03-novelty.md`,
`02-design.md`, other notes or `paper/`. Every quotation below was read by me on the page named
(raw text via curl or pdftotext unless marked otherwise) and is copied verbatim, apart from PDF
line-break hyphens being joined. "Not found" means not found in the searches listed, nothing more.

## Summary of verdicts

| Item | Verdict | Closest sources |
| --- | --- | --- |
| K7(a) consensus rate limit on releases | PARTIAL | Sanders 2023 (rate-limited unvaulting via CSV, needs covenant opcodes); Chia RL wallet 2021; ZmnSCPxj 2021 (presigned nLockTime chain); RLN (per-identity message rate limit) |
| K7(b) veto window, any single guardian | PARTIAL (mechanism is prior; purpose differs) | Revault; Lightning `to_local`; vaults (Optech, Swambo et al. 2020, BIP-345); BitVM2 challenge; OpenZeppelin canceller; Argent guardians; NIP-41 draft |
| K7(c) non-equivocating gapless chain, one root per index in the key | PRIOR (chain); PARTIAL (NUMS plus data tweak encoding) | Catena 2017; Pikachu 2022; Todd single-use seals 2016; did:btcr2 beacons; Chia singletons; BIP-341 H + rG; Delving 2023 "r is the hash of the taptree" |
| K7(d) release certificate checked with headers and Merkle proofs (light client, chip) | PRIOR (mechanism); claim adds release semantics | Catena thin clients; Tesseract enclave 2019; Taproot Assets proof file; BitVM2 light client |
| Later spend through delayed path proves no veto | PRIOR | BitVM2 connector outputs; Revault transaction graph; Todd single-use seals |
| K8 height-difference lease | PARTIAL (strong: the predicate is prior) | Yee "Short Leashes" 2022; Zeke "Chaintip freshness cert" 2026; Solana recent-blockhash expiry; OP_Expire thread 2023; Zodiac Delay expiration; Argent window |
| K9(a) block clock an AI cannot speed up, cost quantified | PARTIAL | Gigi 2021; Trubetskoy 2018; Gilliam 2025 ("first form of AI time"); Zeke 2026; Budish 2018 (attack cost). Counter-evidence: BIP-54 timewarp, time-dilation attacks |
| K9(b) blockspace as aggregate rate limit on AI agents' commitments | NOT FOUND | Nearest: capacity worries (Smith, Sept 2026), RLN |
| K9(c) Bitcoin headers with difficulty floor as AI-chip licence clock | PARTIAL | Tesseract 2019 (enclave, hardcoded difficulty); BitVM2 PowPV (hard-coded difficulty floor); flexHEG Part II 2025 (public blockchain to enforce delay); Buterin d/acc 2025; Diode patent US11146545B2 |

Three closest sources overall:

1. **Catena** (Tomescu, Devadas, IEEE S&P 2017): a chain of Bitcoin transactions, each spending the
   previous one's output and committing one statement, non-equivocating because forking needs a
   double spend, verified by thin clients from headers plus a 600-byte proof. Covers K7(c) and K7(d).
2. **Short Leashes** (Bennet Yee, Oasis Labs, 2022): a transaction carries (block number, block hash,
   length) and is void unless executed in the causal future of the anchor block and within the
   length. This is K8's predicate. Runner-up for K8: Zeke's "Chaintip freshness cert" (2026), the same
   window on Bitcoin, enforced by the verifier, argued explicitly against wall clocks.
3. **Tesseract** (Bentov, Ji, Zhang, Breidenbach, Daian, Juels, CCS 2019): an SGX enclave verifies
   Bitcoin headers against a hardcoded difficulty and deposits by Merkle path, and needs a trusted
   relative timer to resist block withholding. Covers the mechanism of K7(d) in hardware and K9(c).

Also close: Revault and BitVM2 (K7(b) and the "later spend proves no veto" idea).

---

## K7(a): rate limit, at most one release per N2 blocks per identity

**Verdict: PARTIAL.** CSV-based rate limits on spending exist (some need covenants, some use presigned
chains), and per-identity rate limits on messages exist off-chain. Rate-limiting the release of an
identity's off-chain commitments with a CSV chain on today's Bitcoin was not found.

Closest sources:

- Greg Sanders, "Re: [bitcoin-dev] BIP for OP_VAULT", 2023-03-09,
  bitcoindev archive at mailing-list.bitcoindevs.xyz, thread of that date (message-id link omitted from this public copy)
  - "Using these extended primitives, you can do rate-limiting of the two step unvaulting, or just a
    single step vault by committing to the partial values."
  - Script fragment: `<deposit-delay> OP_CSV OP_DROP <pubkey> OP_CHECKSIG ... OP_FORWARD_SELF`, with
    "deposit-delay" described as "the required gap in withdrawals".
  - Follow-up: instagibbs (Greg Sanders' handle; my attribution, not stated on the page), "OP_VAULT fanfiction for rate-limited and collateralized
    unvaulting", Delving Bitcoin, 2023-08-22, https://delvingbitcoin.org/t/55 : "per-utxo-rate-limited
    unvaults(by committing to the unvaulting amount)".
- ZmnSCPxj, quoted in Zac Greenwood, "Re: [bitcoin-dev] Exploring: limiting transaction output amount
  as a function of total input value", 2021-08-13 (ZmnSCPxj's message dated 2021-08-10),
  https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2021-August/019335.html
  - "If you need to have some estimated amount of usable funds for every future unit of time, just
    create a chain of transactions with future `nLockTime`."
  - Greenwood's request: "the restrictive key may allow a maximum of 100k sats per any window of 144
    blocks."
- Chia Network, rate-limited wallet puzzle, `src/wallet/rl_wallet/rl_wallet_puzzles.py` at tag
  1.0beta27 (commits 2021-01-30 to 2021-02-04),
  https://raw.githubusercontent.com/Chia-Network/chia-blockchain/1.0beta27/src/wallet/rl_wallet/rl_wallet_puzzles.py
  - "MIN_BLOCK_AGE = V / (M / N)" and "ASSERT_COIN_BLOCK_AGE_EXCEEDS min_block_age", with a
    `clawback_pk` admin key.
- Rate-Limiting Nullifier docs, "What is RLN", https://rate-limiting-nullifier.github.io/rln-docs/what_is_rln.html
  - "users must not make more than X interactions per epoch"; "Based on the stake amount apps can
    derive what's the messageLimit".

Overlap: consensus-enforced minimum gap between spends of a chained output (Sanders, Chia), presigned
chains on today's Bitcoin (ZmnSCPxj), and stake-backed per-identity message limits (RLN).

What the claim adds: the rate-limited object is the release of an identity's committed batch of
off-chain commitments, not funds or messages; no new opcodes. Note that consensus enforces only the
CSV delay on each output. That T_{n+1} follows the template, and that no parallel chain is counted, is
enforced by relying parties (see limitation L6). In Sanders' and Chia's designs the continuation is
itself enforced by covenant.

Queries and venues: WebSearch "bitcoin rate-limited withdrawals vault chain of outputs
OP_CHECKSEQUENCEVERIFY rate limit covenant delving" (extended); "Chia rate limited wallet chialisp";
"Rate-Limiting Nullifier RLN spec messages per epoch"; Delving search API: "rate limit CSV", "veto
timelock", "chain of commitments timelock", "heartbeat timelock", "proof of non-spend"; BIP-345 text;
Optech vaults topic; bitcoin-dev OP_VAULT thread.

## K7(b): veto window, any single guardian prevents release by spending first

**Verdict: PARTIAL (the mechanism is prior; the purpose differs).** A delayed path for one party plus an
immediate path for others, with one honest watcher sufficient to block, is the standard vault,
revocation and challenge-period pattern. Its use to stop the release of an AI agent's off-chain
commitments or authority was not found.

Closest sources:

- Revault, "practical-revault" `introduction.md` (last changed 2022-02-01),
  https://github.com/revault/practical-revault/blob/master/introduction.md
  - "During this time, only a single honest watchtower is required to cancel given a breach of the
    unvault policy."
  - "During that delay period, a Cancel or Unvault Emergency TX can be broadcasted which will revoke
    the spend attempt."
- BOLT #3, `to_local` output, https://github.com/lightning/bolts/blob/master/03-transactions.md
  - "It can be claimed, without delay, by the other party if they know the revocation private key."
  - Script: `OP_IF <revocationpubkey> OP_ELSE to_self_delay OP_CHECKSEQUENCEVERIFY OP_DROP
    <local_delayedpubkey> OP_ENDIF OP_CHECKSIG`.
- Bitcoin Optech, "Vaults" topic, https://bitcoinops.org/en/topics/vaults/
  - "The first transaction signals that someone is attempting to spend the money and gives the user a
    chance to block the second transaction that completes the spend."
- Swambo, Hommel, McElrath, Bishop, "Custody Protocols Using Bitcoin Vaults", arXiv 2005.11776, May 2020
  - A vault "enforces a time-lock on the transfer of control of funds to a hot wallet, but enables an
    immediate transfer of funds into a deep cold recovery wallet."
- O'Beirne, Sanders, BIP-345 OP_VAULT, https://github.com/bitcoin/bips/blob/master/bip-0345.mediawiki
  - recovery "can be done at any point before the withdrawal transaction confirms."
- Linus, Aumayr, Zamyatin, Pelosi, Avarikioti, Maffei, "BitVM2: Bridging Bitcoin to Second Layers",
  2024, https://bitvm.org/bitvm_bridge.pdf
  - "Any challenger can dispute the claim by publishing a Challenge transaction".
- OpenZeppelin `TimelockController.sol`,
  https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/TimelockController.sol
  - "This gives time for users of the controlled contract to exit before a potentially dangerous
    maintenance operation is applied." `function cancel(bytes32 id) public virtual onlyRole(CANCELLER_ROLE)`.
- Gnosis Guild, Zodiac Delay Modifier README, https://github.com/gnosisguild/zodiac-modifier-delay
  - "The owner of the `owner` can skip transactions by advancing the transaction nonce."
- Argent Smart Wallet Specification v2.5, 2021-04-23,
  https://github.com/argentlabs/argent-contracts/blob/develop/specifications/specifications.pdf
  - "he can ask any of his guardians to lock the wallet for a security period of 5 days."
- pablof7z, fiatjaf, nvk, NIP-41 "Key migration" draft, PR #829 opened 2023-10-18 (still open),
  https://github.com/nostr-protocol/nips/pull/829
  - "When a migration event is published, a 60-day period starts in which a user can publish a
    competing migration event pointing to an earlier `kind:1776` event."
- Jentzsch, Jentzsch, Kux (Blockchains Inc), US12045805B2, priority 2020-10-14,
  https://patents.google.com/patent/US12045805B2/en
  - A veto key may "cancel a transaction, for example, by signing the transaction within a selected
    period of time relative to when an initiation key signed the transaction".
- Babylon, "Bitcoin Staking Transactions Specification", https://github.com/babylonlabs-io/babylon/blob/main/docs/staking-script.md
  (template relative): NUMS internal key, a CSV timelock leaf for the staker, multi-party leaves.
  "The key spending path is disabled by using the "Nothing Up My Sleeve" (NUMS) point as the internal key."

Overlap: the script shape of `advance2` plus `veto_i` (delayed path for one party, immediate path for
others) is Lightning's `to_local` and the vault pattern; 1-of-n blocking is Revault's watchtower model
and BitVM2's permissionless challenge; "any guardian can lock" is Argent; a dispute window before a
key or identity change takes effect is NIP-41.

What the claim adds: the protected object is an identity's off-chain commitment batch (or authority),
not coins; the veto is a plain `<Gi> OP_CHECKSIG` leaf, so no presigned cancel transaction is needed
(this avoids the presigned-fee problem Revault reports); veto halts the chain and only unanimous
`renew` restarts it.

Queries and venues: WebSearch "AI agent bitcoin taproot relative timelock guardian veto kill switch
agent commitments OP_CHECKSEQUENCEVERIFY" (extended); Google Patents via WebSearch "relative timelock
authorization veto delay output spend guardian cancel blockchain block height lease renewal"; Revault
repository; BOLT 3; BIP-345; Optech vaults; Swambo et al.; BitVM2; OpenZeppelin; Zodiac; Argent
specification; NIP-41 PR; Babylon spec; Delving "veto timelock". Möser, Eyal, Sirer (FC 2016) was
not opened (the PDF URL returned HTML); it is covered here only through Optech's primary-source list.

## K7(c): no equivocation, gapless, one Merkle root per index committed in the internal key

**Verdict: PRIOR for the non-equivocating chain of outputs; PARTIAL for the NUMS plus tagged-hash
encoding.**

Closest sources:

- Alin Tomescu, Srinivas Devadas, "Catena: Efficient Non-equivocation via Bitcoin", IEEE S&P 2017,
  https://people.csail.mit.edu/alinush/papers/catena-sp2017.pdf
  - "Catena implements a log as an OP_RETURN transaction chain and prevents forks in the log by
    leveraging Bitcoin's security against double spends."
  - "Specifically, if a log server wants to equivocate it has to double spend a Bitcoin transaction output."
- Sarah Azouvi, Marko Vukolić, "Pikachu: Securing PoS Blockchains from Long-Range Attacks by
  Checkpointing into Bitcoin PoW using Taproot", arXiv 2208.05408, 2022
  - "This key is then tweaked using a commitment ckpt to the PoS chain (i.e., the hash of the PoS
    chain at that time)."
  - Users "can follow the chain of transactions from Q0 to the newest public key Qi" (subscripts flattened).
- Peter Todd, "Preventing Consensus Fraud with Commitments and Single-Use-Seals", 2016-12-07,
  https://petertodd.org/2016/commitments-and-single-use-seals
  - "A single-use-seal is secure if it's infeasible to produce two apparently valid proofs that the
    same seal has been closed over two different messages."
- Salvatore Ingala (salvatoshi), "Unspendable keys in descriptors", Delving Bitcoin, 2023-12-19,
  https://delvingbitcoin.org/t/unspendable-keys-in-descriptors/304
  - "define a new fragment ... where the keypath is computed as a NUMS point with the previous
    approach, where `r` is the hash of the taptree." (idea credited there to Antoine Poinsot)
- BIP-341, https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
  - "It is possible to prove that this internal key does not have a known discrete logarithm with
    respect to G by revealing r to a verifier".
- Alex Schoof, "Re: [Lightning-dev] [bitcoin-dev] Taro", 2022-04-07,
  mail-archive.com, lightning-dev list, msg02793 (link omitted from this public copy)
  - "mainstay[1] uses a pay-to-contract/bip175[2]-like scheme to commit sidechain merkle roots to
    p2pkh/p2sh addresses with signature tweaks." (The Mainstay whitepaper itself could not be fetched.)
- DCD, "did:btcr2 DID Method", https://dcdpr.github.io/did-btcr2/print.html
  - "Late Publishing is the ability for DID updates to be revealed at a later point in time".
  - "a Singleton Beacon ... only allows for one BTCR2 Update per Bitcoin transaction".
- Chia, "Singletons", https://chialisp.com/singletons/
  - "It proves that the puzzle is unique and cannot be duplicated."

Overlap: a chain of outputs where each index's commitment can exist only once because a second one
would be a double spend (Catena, Todd, Pikachu, Mainstay, did:btcr2); commitment carried in a Taproot
key tweak rather than OP_RETURN (Pikachu, Mainstay via P2C); NUMS internal key with a tweak derived
by hashing public data (BIP-341 H + rG, Delving 2023 with r as a hash).

What the claim adds: committing (charter id, n, root_n) in r of a NUMS key, which keeps the key path
provably dead while carrying the index and root, and binds the index into each output. This is a
small encoding step from the cited work. "Gapless" follows from the chain structure in all of the
above; did:btcr2 calls its failure mode "late publishing".

Queries and venues: WebSearch "Mainstay staychain proof of publication pay-to-contract", "commerceblock
mainstay whitepaper pdf staychain pay-to-contract tweaked public key" (extended), "deterministic
unspendable taproot internal key NUMS H + rG", "taproot NUMS internal key tweaked with hash of data
commitment", "did:btcr2 specification singleton beacon late publishing"; Delving topic 304; BIP-341;
Catena; Pikachu; Todd; Chia docs; Taproot Assets BIPs.

## K7(d): release certificate verified with headers and Merkle inclusion proofs only

**Verdict: PRIOR for the mechanism.** Light verification of a Bitcoin-anchored chain entry by headers
plus Merkle proofs, including inside trusted hardware, is published.

Closest sources:

- Catena (above): "our clients only need to download all Bitcoin block headers (currently less than
  35 MB) and a small, 600-byte proof for each statement in a block."
- Bentov, Ji, Zhang, Breidenbach, Daian, Juels, "Tesseract: Real-Time Cryptocurrency Exchange Using
  Trusted Hardware", CCS 2019, doi:10.1145/3319535.3363221, PDF at https://par.nsf.gov/servlets/purl/10153194
  - "Each header is validated according to the protocol rule of the underlying cryptocurrency,
    specifically for Bitcoin the proof-of-work (PoW) in the header is validated against the current
    difficulty level."
  - Evidence of a deposit is "the transaction that spends the coins into a deposit address of
    Tesseract, as well as an authentication path".
- Olaoluwa Osuntokun, "Taproot Asset Flat File Proof Format" (draft BIP, created 2021-12-10),
  https://github.com/Roasbeef/bips/blob/bip-tap/bip-tap-proof-file.mediawiki
  - "A proof of a single Taproot Asset state transition includes a Bitcoin merkle proof, a Taproot
    Asset merkle-sum sparse merkle tree (MS-SMT) inclusion proof".
  - "Proofs are anchored at the initial "genesis output" for a given asset."
- BitVM2 (above): a Bitcoin light client checked inside a SNARK-verified program.
- Vitalik Buterin, "d/acc: one year later", 2025-01-05, https://vitalik.eth.limo/general/2025/01/05/dacc2.html
  - Chip signatures: "if desired, we could even require a zero-knowledge proof that they were
    published on a blockchain".

What the claim adds: the checked statement is "output T_n was spent through leaf `advance2`/`advance3`
after its CSV and created T_{n+1} to template", checked by an AI-governance chip. But see limitations
L6 (lineage) and L7 (64-byte Merkle ambiguity): Catena and Taproot Assets both verify from a genesis
output onward, not from two transactions.

Queries and venues: Catena; Tesseract (ePrint 2017/1153 blocked automated download; read the NSF PAR
copy); Taproot Assets BIPs; BitVM2; Buterin d/acc; WebSearch "secure element hardware wallet uses
bitcoin block headers as trusted time source" (extended); Google Patents "device license expiration
verified using blockchain block headers proof of work difficulty".

## Later spend through the delayed path proves no veto happened

**Verdict: PRIOR.** That a spend of an output excludes every competing spend, and that an optimistic
payout after a timeout therefore certifies no challenge occurred, is explicit in BitVM2 and Revault and
general in single-use seals.

- BitVM2 (above):
  - The connector output "must remain be unspent for the operator use PayoutOptimistic to withdraw
    funds from BitVM2 unchallenged." (sic)
  - "As soon as one of these transactions is included in the Bitcoin blockchain, spending the
    connector output, the other transactions become invalid."
- Revault introduction (above), figure caption: "only one of the Cancel, Unvault Emergency or Spend
  TXs can consume a specific UTXO".
- Todd 2016 (above): the single-use-seal definition.

What the claim adds: nothing substantive beyond applying it to releases; the leaf reveal identifies
which path was used, which is standard Taproot.

Queries and venues: BitVM2, Revault, Todd, BOLT 3, Optech; Delving "proof of non-spend" (no hits).

## K8: the height-difference lease

**Verdict: PARTIAL (strong).** The predicate "valid only if included at height h with h_k ≤ h ≤ h_k + L,
where the authorisation names block h_k by height and hash" is published (Yee 2022), as is a
Bitcoin-specific, verifier-enforced freshness window on signed statements that names tip height and
hash and argues against wall clocks (Zeke 2026). Not found: a guardian-unanimous renewal used as a
lease on a Bitcoin agent's releases, checked against the release transaction's confirmation height.

Closest sources:

- Bennet Yee (Oasis Labs), "Keep Your Transactions On Short Leashes", arXiv 2206.11974, 2022-06-02
  - "the leash asserts that the transaction is null and void unless the current block is in the
    causal future of the anchor block"
  - "and further, that anchor is not too far in the past of the current block, as specified by the
    length or range of the leash."
  - Signature: "leash ∈ (Txn, BlockNumber, Blockhash, Z2256 ) → Txn".
- Zeke (dev.to/zekebuilds), "Chaintip freshness cert: signed identity scores that age with the
  chain", 2026-04-28, https://dev.to/zekebuilds/chaintip-freshness-cert-signed-identity-scores-that-age-with-the-chain-59o8
  - "The verifier rejects scores where current_tip_height - bitcoin_tip.height > freshness_blocks."
  - "A chaintip-block window says "expires 6 blocks past height N." You can't fake that."
- Solana docs, "Confirmation & finality" (source file in solana-foundation/solana-com),
  https://github.com/solana-foundation/solana-com/blob/main/apps/docs/content/docs/en/core/transactions/confirmation.mdx
  - "If the transaction has not landed in a block before that blockhash is more than 150 blocks old,
    about 30 seconds at 200ms slots, the network drops it".
- Peter Todd, "[bitcoin-dev] OP_Expire and Coinbase-Like Behavior", 2023-10-21,
  mirror.b10c.me bitcoindev archive, message of that date (message-id link omitted from this public copy)
  - "Traditionally, we've tried to ensure that transactions - once valid - remain valid forever."
  - "This is conceptually an AntiCheckLockTimeVerify".
- Luke Dashjr, BIP-115 OP_CHECKBLOCKATHEIGHT (closed), https://github.com/bitcoin/bips/blob/master/bip-0115.mediawiki
  - "allows construction of transactions which are valid only on specific blockchains."
- Zodiac Delay Modifier README (above): "an approved address can execute transactions only after a
  cooldown period and, optionally, before an expiration time."
- Argent specification (above): additions "must be confirmed after 36 hours and no later than 48
  hours after the addition was requested."
- Liana README (2.0.0), https://docs.rs/crate/liana/2.0.0/source/README.md
  - "each coin must be spent at least once every `N` blocks." (an on-chain keep-alive lease)
- Bitcoin Optech, "Ark" topic, https://bitcoinops.org/en/topics/ark/
  - "users must ensure their VTXOs are spent into a new transaction tree before expiry."
- On stockpiling (relevant to "cannot be pre-signed in bulk"):
  - James Petrie, "Near-term enforcement of AI chip export controls using a firmware-based design for
    offline licensing", arXiv 2404.18308, 2024: "Chip owners could save licenses instead of using
    them, which would allow them to use AI chips for a longer time in a situation where license
    approvals are halted."
  - O'Gara, Kulp, Hodgkins, Petrie et al., "Hardware-Enabled Mechanisms for Verifying Responsible AI
    Development", arXiv 2505.03742, 2025: RTCs "could ensure license expiration after a specific
    period of time, to prevent people from stockpiling licenses and then using them all at once".

Overlap: the window predicate with a named block hash (Yee); verifier-side, Bitcoin-height freshness
with an explicit no-wall-clock argument (Zeke); consensus-level blockhash expiry (Solana); Bitcoin
script's lack of "not after" and the reason (OP_Expire thread); expiry windows in delay modules and
guardian wallets (Zodiac, Argent, timestamp-based).

What the claim adds: (1) the authority is a renewal signed by every guardian, not the transactor; (2)
the window is evaluated on the confirmation height of a separate on-chain release, so the verdict does
not depend on when the relying party checks (Zeke compares with the verifier's current tip; Yee
enforces inside execution); (3) the application to bound an AI agent's release authority on Bitcoin
without script support. The "cannot be pre-signed before h_k exists" property is the same freshness
argument as Yee's ("the system cannot be constructing a block for which the hash value is
known/specified") and the warrant-canary practice of signing a recent block hash.

Queries and venues: WebSearch "Solana transaction recent blockhash expiration 150 blocks", "warrant
canary signed includes latest bitcoin block hash prove freshness", "Peter Todd OP_Expire bitcoin-dev
2023", "ERC-8370 agent lease authority expiry", "Liana wallet recovery path timelock refresh", "Ark
protocol VTXO expiry refresh"; BIP-115; arXiv 2206.11974; dev.to post; Ethereum Magicians agent-mandate
map thread (no block-height lease found there); Google Patents "block height lease" (no hit).

## K9(a): Bitcoin's block clock as a clock an AI cannot speed up, with the cost quantified

**Verdict: PARTIAL.** "Proof of work is a decentralised clock" is an old framing; one 2025 essay calls
Bitcoin "the first form of AI time"; a 2026 post argues block windows cannot be faked because blocks
cost energy; attack-cost economics are standard (Budish). Not found: the specific argument, with a
computed cost, that accelerating the clock costs the same whatever the agent's speed or intelligence.

- Gigi, "Bitcoin is Time", 2021-01-14, https://nakamotoinstitute.org/mempool/bitcoin-is-time/
  - "its network is time because it is a decentralized clock."
- Gregory Trubetskoy, "Blockchain Proof-of-Work is a Decentralized Clock", 2018-01-23,
  https://grisha.org/blog/2018/01/23/explaining-proof-of-work/
  - "The Bitcoin blockchain Proof-of-Work is simply a distributed, decentralized clock."
- Byron Gilliam, "Bitcoin's arrow of time", Blockworks, 2025-10-22,
  https://mail.blockworks.com/p/bitcoin-s-arrow-of-time
  - "Bitcoin's proof-of-work, where progress is measured block by computational block, might be seen
    as an early example of such computational time."
  - "Bitcoin might be the first form of AI time."
- Zeke 2026 (above): "To advance the chain by 6 blocks past height N, the bitcoin network has to
  actually mine 6 blocks."
- Eric Budish, "The Economic Limits of Bitcoin and the Blockchain", NBER w24717, 2018,
  https://www.nber.org/papers/w24717
  - "the computational costs of such an attack must exceed the benefits."
- BitVM2 (above): "The probability of success scales with the hashrate of the operator."
- Counter-evidence that the claim should address:
  - Poinsot, Corallo, BIP-54 "Consensus Cleanup", https://github.com/bitcoin/bips/blob/master/bip-0054.md :
    "The timewarp bug makes it possible for a majority-hashrate attacker to arbitrarily lower mining
    difficulty, and therefore arbitrarily increase the block rate."
  - Riard, Naumenko, "Time-Dilation Attacks on the Lightning Network", arXiv 2006.01418, 2020:
    "time-dilation attacks neither require access to hashrate nor purchasing from a victim."

What the claim adds: the AI-specific framing (intelligence does not buy clock speed) and a computed
cost. The cost model should include timewarp (a majority coalition speeds the clock by timestamp
manipulation, not by outpacing the network, until BIP-54 is active) and the fact that a victim's view
of the clock can be slowed without any hashrate.

Queries and venues: WebSearch "bitcoin block clock artificial intelligence cannot speed up proof of
work time superintelligence clock" (extended), "AI safety bitcoin proof of work limit AI agents
physical cost energy" (extended); Gigi; Trubetskoy; Blockworks; Budish; BIP-54.

## K9(b): blockspace as an aggregate rate limit on AI agents' commitments

**Verdict: NOT FOUND.** Blockspace scarcity appears only as a capacity problem for AI agents, not as an
intended safety bound priced by fees.

- Lawrence Mondal, "AI agents could squeeze L1 block space, Avalanche CEO says", crypto.news,
  2026-09-17, https://crypto.news/ai-agents-could-squeeze-l1-block-space-avalanche-ceo/
  - Bart Smith: "There is not enough block space, and block space is no longer infinite."
- RLN (above): per-identity, stake-backed limits, not aggregate and not blockspace.

Queries and venues: WebSearch "blockspace scarcity limits AI agents rate limit AI agents bitcoin
blockspace bottleneck safety throttle" (extended); "AI safety bitcoin proof of work limit AI agents";
Delving search (PRECOP posts, below, are about agent wallets, not aggregate limits).

## K9(c): Bitcoin headers with a difficulty floor as the licence clock of AI chips

**Verdict: PARTIAL.** Trusted hardware verifying Bitcoin headers against a hardcoded difficulty exists
(Tesseract); a hard-coded difficulty floor and its safety/liveness trade-off is analysed (BitVM2); the
chip-governance literature names secure time as an open problem and mentions public blockchains for
delays (flexHEG) and publication proofs (Buterin). Not found: Bitcoin headers as the licence clock of
AI chips, with a computed forgery cost.

- Tesseract (above):
  - "We note that the enclave is hardcoded with the current difficulty parameter of each PoW-based
    blockchain."
  - "This prevents an adversary (who has physical control of the Tesseract server) from feeding a
    low-difficulty fake chain to the enclave."
  - "Assuming that the TEE has a trusted clock, the enclave can impose a rule that requires waiting
    for additional confirmations if the blocks arrive too slowly." (footnote marker removed)
- BitVM2 (above), PowPV light client: "Choosing it higher or lower is always a trade-off between safety
  (a lower difficulty makes it easier for operators to fake a proof) and liveness".
- Petrie, Aarne, "Flexible Hardware-Enabled Guarantees, Part II", April 2025, https://www.flexheg.com/report-2.pdf
  - To enforce a delay: "(or instead of an auditor, the presence of that hash in the history of a
    public blockchain could be used)".
  - Licences elsewhere use "a secure real-time clock or cycle counter".
- Aarne, Fist, Withers, "Secure, Governable Chips", CNAS, January 2024,
  https://s3.us-east-1.amazonaws.com/files.cnas.org/documents/CNAS-Report-Tech-Secure-Chips-Jan-24-finalb.pdf
  - "Accurate, hack-proof, and tamper-proof tracking of time generally is considered very difficult."
  - "The authors expect that a timed license is the only way to implement a robust mechanism for
    remotely disabling chips".
- O'Gara, Kulp et al. 2025 (above): "Research should explore how such a component could be secured
  against attempts to slow down or speed up the rate at which it is incremented".
- Buterin 2025 (above): weekly 3-of-3 signatures, optionally with a ZK proof of blockchain publication.
- Letz, Webster, Rempel (Exosite, now Diode), US11146545B2, priority 2018-03-27,
  https://patents.google.com/patent/US11146545B2/en
  - "without the actual current time, the IoT device cannot validate PKI certificates, and without PKI
    certificate validation, the IoT device lacks of a trusted source of time." (It derives time from an
    authoritative chain via trusted peers and signed headers, not a difficulty floor.)

What the claim adds: the pairing of AI-chip licensing with Bitcoin headers as the clock, a difficulty
floor, and a computed forgery cost. Tesseract shows the limitation (it needed a trusted relative timer
against slow, withheld block feeds), see L2.

Queries and venues: WebSearch "hardware-enabled governance AI chips license expiry trusted time source
blockchain block headers proof of work clock" (extended), "lesswrong AI chip blockchain timestamp
clock compute governance" (extended), "bitcoin AI chips license renewal block height hardware kill
switch" (extended), "RAND Hardware-Enabled Governance Mechanisms Kulp 2024"; Google Patents "device
license expiration verified using blockchain block headers proof of work difficulty"; flexHEG reports
1 to 3 (grep for blockchain, clock); CNAS; arXiv 2505.03742, 2404.18308, 2506.20530 (the last mentions
blockchain only for chip serialisation). The RAND WR-A3056-1 PDF could not be downloaded.

---

## Attacks and limitations in the literature not stated in the claims file

The claims file states miner or bribed-miner censorship of vetoes, a vanished guardian set, and the
per-entry cap being relying-party enforced. These are additional:

- **L1. Eclipse and time-dilation of guardians.** Riard and Naumenko (arXiv 2006.01418): victims are
  kept unaware of new blocks "by eclipsing (isolating) victims from the network and delaying block
  delivery", with no hashrate. A guardian that does not see T_n's creation until its CSV has matured
  misses the veto window. Light-client guardians are the easiest targets ("running just 500 Sybil
  nodes allows an attacker to Eclipse 47% of newly deployed light clients").
- **L2. Frozen clock for light verifiers and chips (K8, K9(c)).** The lease bound holds only in the
  verifier's best chain. A verifier fed no new headers never sees h_k + L pass, so a stale renewal
  stays valid. Tesseract needed a trusted relative timer for exactly this; Catena notes a compromised
  log server can "hide away transactions" so that "Catena clients would lose freshness"; CNAS notes timers can be
  compromised "by manipulating the power supply to the chip". The claim that K8 does not depend on
  the verifier's clock is true for forgery but not for withholding.
- **L3. Bribery is cheap.** Avarikioti, Kędzior, Lizurej, Michalak, "Bribe & Fork" (arXiv 2402.01363,
  2024): "an adversary incentivizes blockchain miners to deliberately ignore a specific transaction
  to undermine the punishment mechanism of PCNs", with cost "dramatically reduced (to approximately
  \$125)". Tsabary et al., MAD-HTLC (arXiv 2006.12031): "An attacker can incentivize miners to prefer
  her transactions by offering high transaction fees." Khabbazian, Nadahalli, Wattenhofer, "Timelocked
  Bribing" (FC 2021, ePrint 2020/774; abstract read through a fetch tool, PDF blocked): a bribery attack
  in which a hash-protected transaction "is censored" by the counterparty's timelocked one. Winzer,
  Herd, Faust, "Temporary Censorship Attacks in the Presence of Rational Miners" (EuroS&P Workshops
  2019, ePrint 2019/748; only a tool summary of the abstract was available, not quoted). The agent's
  `advance2` spend is exactly the timelocked transaction that benefits from censoring `veto_i`.
- **L4. Targeted censorship is easy.** Todd 2016: "Miners who learn the txout associated with the seal
  can censor transactions spending that txout." T_n's outpoint is public, and before maturity the only
  valid spends of it are vetoes, so a censor needs no further information.
- **L5. Congestion and systemic flooding.** Harris, Zohar, "Flood & Loot" (arXiv 2006.08513): "The
  resulting high volume of transactions in the blockchain will not allow for the proper settlement of
  all debts". Many identities' veto windows share blockspace; a fee spike or a deliberate flood can
  push vetoes past h(T_n) + N. This also interacts with K9(b): releases and vetoes compete for the
  same blockspace.
- **L6. Lineage, not two transactions.** Catena requires that before verifying statement s_i,
  "VerifyStmt must first be called on s1, s2, ..., si−1, in that order" (spacing normalised); the Taproot Assets proof file
  is "an append-only log of the prior lineage" anchored at a genesis output; Chia singletons enforce
  uniqueness by covenant. Without lineage back to T_0 (or a trusted checkpoint), a two-transaction
  proof does not show that T_n belongs to the identity's chain. (Inference, to be checked: the agent
  can fund a fresh output with the template's keys and a different root, wait N2, and spend it through
  `advance2`; Taproot hides the scripts, so guardians cannot find it to veto.)
- **L7. Forged Merkle inclusion proofs.** BIP-54: a 64-byte transaction "makes it possible to trick an
  SPV verifier into accepting an inclusion proof for a transaction that is not part of a block". Until
  BIP-54 is active, a light or chip verifier must apply a workaround.
- **L8. Timewarp speeds the clock without outpacing the network.** BIP-54 (quoted under K9(a)); it also
  states the worst case: "an attacker can bring down the difficulty to its minimum within 38 days".
- **L9. Reorgs near the lease boundary.** The OP_Expire thread gives the reason Bitcoin avoids expiry:
  "transactions - once valid - remain valid forever" for reorg safety. A release confirmed near
  h_k + L can move past the bound after a reorg, so K8's verdict can flip; relying parties need a
  margin or a depth rule.
- **L10. Griefing by one guardian.** Revault lists "unjustified Cancel TX push" among its risks. With
  K7, one guardian can veto and then withhold its signature from the unanimous `renew`, halting the
  identity indefinitely.
- **L11. Fees and pinning for the veto transaction.** Revault: pinning can be used for "pinning a
  Cancel TX for longer than the Unvault TX's time-lock, and stealing funds", and "we are not aware of
  a method to dynamically allocate fees to these transactions without the risk of pinning attacks".
  Because `veto_i` is a fresh single-key spend, the guardian can attach its own fee inputs, which
  avoids Revault's presigned-fee problem; but who funds vetoes, and whether T_n's value covers a
  veto at high fee rates, is not stated.

## Venues searched with nothing closer than the above

- Delving Bitcoin search API: "veto timelock", "rate limit CSV", "chain of commitments timelock",
  "proof of non-spend", "heartbeat timelock". Hits read: topics 55, 304, 2377 and 2410. Topics 2377
  and 2410 (Laz1m0v, "PRECOP", April 2026) describe TEE guardians for AI-agent Bitcoin wallets with a
  144-block CSV fallback, about spending constraints, not release chains, vetoes or leases.
- Ethereum Magicians "A map of the agent-mandate ERCs" (topic 29421): taxonomy of delegation, cap,
  revocation and expiry; no block-height lease or guardian veto chain found in it. ERC-8370 itself is
  credited in the claims file and was not re-examined.
- Statechains, spacechains: searched by name only; not opened, since their timelocks govern fund
  exits. Ark: Optech topic read (quoted under K8).
- Google Patents (via WebSearch with domain filter): two queries, hits US11146545B2, US12045805B2,
  US20190156301A1 (Tesseract), WO2019049022A1 (time lock technique, not opened).
- Not reachable: IACR ePrint PDFs (Cloudflare), Mainstay whitepaper (IPFS gateway), RAND PDF, the
  Möser, Eyal, Sirer FC 2016 PDF, solana.com pages (used the docs' GitHub source instead).
