# Bitcoin protocol primitives for AI-agent safety: exact semantics and deployment status (as of 2026-11-26)

Scope: what Bitcoin (L1 and the main off-chain layers) can enforce today for budgets, bonds, slashing, leases, delays and audit anchors; what needs a trusted party; what needs a soft fork that has not happened. All statuses were checked on 2026-11-25/26 unless a different date is given. The BIP index (README.mediawiki) was read at commit date 2026-11-25. Number labels: **measured** (independent or chain data), **vendor** (claim by an interested party, including protocol authors about their own system), **derived** (my arithmetic, shown), **estimate** (a named person's estimate).

Status legend used below (BIP-3 statuses, [bip3]): Draft, Complete ("authors have concluded all planned work"), Deployed (settled, evidence of adoption), Closed (historical interest only). "Complete" does **not** mean activated.

## 1. Timelocks: nLockTime, CLTV (BIP-65), CSV (BIP-112) with BIP-68, MTP (BIP-113), expiry, block-time bounds, timewarp, BIP-54

### Takeaway
Bitcoin script enforces only lower bounds on time ("not before"): absolute via nLockTime/CLTV and relative via nSequence/CSV, measured in block height or median-time-past. There is no consensus way to make a valid spend become invalid later ("not after"), by deliberate design for reorg safety; every expiry on Bitcoin is emulated with a competing path that becomes valid later, pre-signed transactions, or a co-signer that refuses. Block height is a decent but attackable clock: the timewarp bug still lets a hashrate majority speed up blocks, and its fix (BIP-54) is specified but not activated, with one developer suggesting activation discussion could start in the second half of 2027.

### Cited Findings
- **nLockTime (consensus)**: a transaction is final if `nLockTime == 0`, or if `nLockTime < (height or time)` where values below `LOCKTIME_THRESHOLD` are heights and values at or above are times; a transaction is also final, ignoring nLockTime, if all inputs have `nSequence == 0xffffffff`. So a height lock L is first valid in block L+1 (strict `<`). [core-tx-verify]
- `LOCKTIME_THRESHOLD{500'000'000}; // Tue Nov 5 00:53:20 1985 UTC`. [core-script-h]
- **BIP-65 CLTV** (Status: Deployed, per BIP index): redefines NOP2; script fails if the stack is empty, top item < 0, the lock type (height vs timestamp) of the top item differs from the tx nLockTime type, "the top stack item is greater than the transaction's nLockTime field", or the input's nSequence is 0xffffffff. CLTV therefore only checks "argument <= nLockTime"; nLockTime finality then makes the spend wait. [bip65]
- BIP-65 motivation: nLockTime alone "can't prove that it is impossible to spend a transaction output until some time in the future, as there is no way to know if a valid signature for a different transaction spending that output has been created." [bip65] (This is why a pre-signed nLockTime transaction is not a lock: the key holder can sign a different, unlocked spend.)
- CLTV accepts up to 5-byte numbers, "good until 2**32-1, the same limit as the nLockTime field itself" (time locks meaningful until 2106). [bip65]
- **BIP-68 relative locktime** (Deployed): applies to transactions with nVersion >= 2; if bit 31 of nSequence is set, no consensus meaning; bit 22 selects time (units of 512 s) vs blocks; only the low 16 bits (mask 0x0000ffff) are used: "The 16-bit specification allows for a year of relative lock-time". Time-based locks count from "the median-time-past of the previous block which mined it" (the output's confirmation). [bip68]
- Derived: maximum height-based relative lock = 65,535 blocks; at the 600 s target that is 65,535 x 600 s = 39,321,000 s = about 455 days. Maximum time-based = 65,535 x 512 s = 33,553,920 s = about 388.4 days. (derived)
- Optech (2025-08-01 entry on its timelocks topic) lists a "Proposal to allow longer relative timelocks"; not adopted. [optech-timelocks-topic]
- **BIP-112 CSV** (Deployed): redefines NOP3; fails if the stack is empty, top item < 0, or (when the top item's disable flag is unset) the tx version < 2, the input's disable flag is set, the lock types differ, or "the top stack item is greater than the transaction input sequence (when masked according to the BIP68)". [bip112]
- **BIP-113 MTP** (Deployed): "The median of the last 11 blocks is used instead of the block's timestamp, ensuring that it increases monotonically with each block." [bip113]
- Miniscript encodes these as `older(n)` = `<n> CHECKSEQUENCEVERIFY` and `after(n)` = `<n> CHECKLOCKTIMEVERIFY`, with 1 <= n < 2^31; it forbids mixing height-based and time-based locks of the same kind (absolute or relative) inside `and` or `thresh(k>=2)` because a single transaction cannot satisfy both. [bip379]
- **No expiry, with the reason**: Peter Todd, bitcoin-dev, 2023-10-21: "Traditionally, we've tried to ensure that transactions - once valid - remain valid forever. We do this because we don't want transactions to become impossible to mine in the event of a large reorganization." His OP_Expire proposal ("conceptually an AntiCheckLockTimeVerify") would need a "Coinbase Bit" soft fork so expiring transactions have coinbase-like 100-block reorg safety. Not adopted. [todd-opexpire-2023]
- Optech 2026-08-07: "Absolute expiry proposals such as Peter Todd's OP_EXPIRE make a valid transaction later invalid, enabling cheap relay spam unless policy demands near-next-block fees." Josh Doman's "input-triggered transaction expiry" (a new nSequence bit 21 rule plus optional "tapscript OP_LOCKTIME introspection opcode so scripts can require a maximum locktime") is a proposal only. The need for a new opcode to "require a maximum locktime" confirms scripts cannot do it today. [optech-2026-08-07]
- **Block-time bounds today**: block timestamps may be at most `MAX_FUTURE_BLOCK_TIME = 2 * 60 * 60` seconds ahead of node time [core-chain-h]; difficulty retargets every 2016 blocks with the measured timespan clamped to between `nPowTargetTimespan/4` and `nPowTargetTimespan*4` [core-pow]; BIP-68 rationale: "bitcoin blocks are generated every 600 seconds" (a target average). [bip68]
- **Timewarp**: BIP-54: "The timewarp bug makes it possible for a majority-hashrate attacker to arbitrarily lower mining difficulty, and therefore arbitrarily increase the block rate. In the worst case, an attacker can bring down the difficulty to its minimum within 38 days of starting the attack." (BIP authors' analysis) [bip54]
- **BIP-54 Consensus Cleanup** (Status: Complete, assigned 2025-04-11; authors Poinsot, Corallo): new rules include, for height N with N % 2016 == 0, T_N >= T_(N-1) - 7200 s; with N % 2016 == 2015, T_N >= T_(N-2015); a 2500 sigops limit per legacy transaction; invalid 64-byte transactions; coinbase nLockTime = height - 1. [bip54] Optech's topic page lists 2026 work: Bitcoin Inquisition implements BIP-54, and a draft testnet5 BIP would activate it from block 1. [optech-cleanup-topic]
- BIP-54 activation status: Optech 2026-11-06 summarizes Antoine Riard: the Bitcoin Core implementation (#35793) "enables the new rules on regtest with no mainnet activation"; remaining work is review, testing, documentation, "and, only later, activation logic"; speaking for himself, "it could be realistic to start considering activation in the second half of 2027". Riard estimated the residual 7,200 s window "could lower difficulty by roughly 0.60% per retarget period" (estimate). Pieter Wuille has a Lean-checked proof that the two timestamp rules bound chain length for a given amount of work (reported by Optech; proof not opened). [optech-2026-11-06]
- Optech 2024-12-06: Zawy noted a per-block timestamp rule "would also make timestamps more accurate for other uses, such as timelocks." [optech-2024-12-06]
- Optech 2026-11-20 and 2026-11-13 newsletters report no soft-fork activation; 2026-11-20 still describes designs that work "until a soft fork enables rebindable signatures, such as those proposed in BIP448". [optech-2026-11-20], [optech-2026-11-13]

### Inferences
- Standard workarounds for "not after" (all exist today): (1) a competing spend path that becomes valid later (Lightning HTLC timeout, Liana recovery path, Ark operator sweep after VTXO expiry, Cashu refund keys); (2) pre-signed transactions held by a watcher (Revault Cancel/Emergency, Babylon slashing tx, DLC refund tx); (3) a co-signer or service that refuses after a deadline (NWC `expires_at`, L402 `valid_until`, policy co-signers). Each converts "expiry" into a race or into trust: the original path stays valid until someone actually spends the competing path on-chain.
- Height vs MTP under attack (my reasoning, not from a source): in a classic timewarp, timestamps are held low while blocks arrive faster, so height-based locks would mature early in wall-clock terms while MTP-based locks would mature late. A design that wants "at least X real time" should consider requiring both a height and a time condition on separate paths or in separate transactions (miniscript forbids mixing them in one `and`).
- MTP lags the tip: the median of 11 blocks sits about 5 to 6 blocks back, so roughly 50 to 60 minutes behind at 10-minute spacing (derived, approximate).
- For Escapement: block height is an "uncompressible" clock only against minority actors. Against a hashrate majority (today, without BIP-54) it is compressible. That caveat belongs next to every "time cost" claim.

### Gaps
- No primary measurement of block-interval variance was opened (the Poisson-arrival model is standard, but I did not open a source for it).
- Wuille's Delving Bitcoin proof on BIP-54 chain-length bounds was seen only via Optech.

## 2. Taproot, miniscript, MuSig2, FROST, PSBT; inheritance wallets; policy co-signers

### Takeaway
Taproot (BIP-340/341/342), miniscript (BIP-379), descriptors, MuSig2 (BIP-327) and PSBT v0/v2 (BIP-174/370) are all Deployed and enough to express "agent key AND human key", "k-of-n", "human alone after N blocks", and hidden alternatives. FROST has no BIP yet: BIP-445 is still an open pull request (opened 2026-01-03, open on 2026-11-26). Script cannot see amounts or destinations, so any per-period spending cap, destination whitelist or velocity limit is enforced by a co-signer service (trusted), not by Bitcoin. Liana proves the dead-man-switch pattern on-chain; BitGo, Bitkey and Nunchuk show policy co-signers, including one product marketed for AI agents (Nunchuk, 2026-04-08).

### Cited Findings
- Status (BIP index, 2026-11-25): BIP-340 Schnorr Deployed; BIP-341 Taproot Deployed; BIP-342 Tapscript Deployed; BIP-327 MuSig2 Deployed (Informational); BIP-174 PSBT Deployed; BIP-370 PSBTv2 Deployed; BIP-379 Miniscript Deployed; BIP-380/386 descriptors Deployed; BIP-388 Wallet Policies Complete; BIP-390 `musig()` descriptor Draft. [bips-index]
- BIP-341: to disable the key path, use a NUMS internal key `H = lift_x(0x50929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0)`, optionally `H + rG` to hide that the key path is disabled; and when an output key is an aggregate, always commit to a script tree because "a malicious party [could] add a script path without being noticed". [bip341]
- BIP-342: `OP_SUCCESSx` opcodes (80, 98, 126-129, ...) make validation succeed and are the upgrade hook for new opcodes (OP_CAT would redefine OP_SUCCESS126). [bip342], [bip347]
- Miniscript `multi_a(k,key_1,...,key_n)` compiles to `<key_1> CHECKSIG <key_2> CHECKSIGADD ... <k> NUMEQUAL` (tapscript only). [bip379]
- BIP-340 signature: `sig = bytes(R) || bytes((k + ed) mod n)`; the nonce "must be a fresh uniformly random 32-byte string"; reuse "can leak the secret key". [bip340]
- MuSig2 (BIP-327) "is a n-of-n multi-signature scheme and not a t-of-n threshold-signature scheme"; outputs "are indistinguishable for a blockchain observer from regular, single-signer Taproot outputs"; requires secure handling of signing state (no deterministic nonces). [bip327]
- FROST: BIP-445 "FROST Signing Protocol for BIP340 Signatures", PR #2070 by siv2r, created 2026-01-03, state "open", last updated 2026-11-26. PR body: RFC 9591 standardizes two-round FROST "but it is incompatible with Bitcoin's BIP340 X-only public keys"; the BIP standardizes the FROST3 variant from the ROAST paper and follows BIP-327 design. Not in the BIP index. [bip445-pr], [bips-index]
- FROST ecosystem (Optech threshold-signature topic): ChillDKG distributed key generation draft (2024-07-19, updated 2025-01-03), FROST BIP proposal announced 2024-08-09, FROSTR library for k-of-n signing on nostr (2025-03-21), Frostsnap signing devices with k-of-n threshold signing (2025-07-18). [optech-threshold-topic], [optech-2024-08-09]
- PSBT (BIP-174): lets "offline signers such as air-gapped wallets and hardware wallets" sign, with per-output data so "signers [can] verify that the outputs are going to the intended recipient". [bip174] PSBTv2 (BIP-370) adds `PSBT_IN_REQUIRED_TIME_LOCKTIME` (0x11) and `PSBT_IN_REQUIRED_HEIGHT_LOCKTIME` (0x12) per input. [bip370] Optech 2026: BIPs #2277 retains required locktimes after PSBTv2 finalization. [optech-timelocks-topic]
- BIP-388 wallet policies: the host "is considered untrusted"; hardware signers must let the user "completely validate on-screen the kind of script used (and each of the involved keys)". [bip388]
- **Liana** (Wizardsardine): "one key which can spend the funds in the wallet immediately" plus "one key which can only spend the coins after the wallet has been inactive for some time"; example: manager key always, "Any 2 keys from the owner's spouse and two kids (after 1 year)", a third party "(after 1 year and 3 months)"; "The lockup period is enforced onchain by the Bitcoin network." Latest release v16.0 published 2026-11-03. [liana-readme]
- **BitGo** (vendor docs): policy rule types Destination, Initiator, Percentage of Wallet Balance, Threshold, Velocity Limit, Webhook; "Policy rules for withdrawals apply only to transactions that involve BitGo. Recovery transactions that use the user key and the backup key bypass any policies"; "new whitelist policies for self-custody wallets lock 48 hours after creation and only BitGo support can unlock them" (vendor). [bitgo-policies], [bitgo-whitelists]
- **Bitkey** (Block, vendor): 2-of-3 (phone, hardware, server); "Bitkey can't move your money without you"; opt-in "Transfer without hardware" lets app+server co-sign "up to a set daily limit of your choosing"; recovery after lost hardware has a "7-day security waiting period"; inheritance "A 6-month security waiting period starts" and can be cancelled (vendor). [bitkey-how]
- **Nunchuk** "Open-source Bitcoin agents with bounded authority" (2026-04-08, vendor): components "Your key", "Agent key", "Policy co-signer", "Shared Bitcoin wallet"; policies named are spending limits, signing delays, dummy-transaction approvals; Miniscript wallets supported. The post does not say whether policies are enforced by script or by Nunchuk's server, or what happens if the co-signer is offline. [nunchuk-blog]
- Optech 2026-11-06: Luke Carriere's draft (no BIP number requested) standardizing co-signer policies when emulating covenants: "Anything that can be enforced by Bitcoin script must be enforced there, with co-signer policies only defining what script cannot"; "At least one spending path that needs no co-signer must always be available"; co-signers accept DLC-format oracle attestations; open question "whether the fallback path must be timelocked". [optech-2026-11-06]

### Inferences
- Script can check keys, hashes and timelocks, not amounts, destinations or cumulative spend; therefore per-day caps, velocity limits and destination whitelists are co-signer policy (trust the co-signer to refuse) unless covenants activate. The only script-native "budget" is the value of the UTXOs the agent can reach.
- MuSig2 and FROST hide which keys signed; script multisig (`multi_a`) reveals which keys signed. For audit and liability, the privacy feature is an accountability bug: an Escapement "human brake" should likely use script-path `multi_a` or separate leaves per signer set if attribution matters.
- Liana's relative-timelock recovery is a working dead-man switch whose clock restarts whenever coins are moved (CSV counts from the spent output's confirmation, [bip68]); "inactivity" in practice means "no coin refresh".
- Template sketches (derived from BIP-379/386 grammar; not tested):
  - Dead-man switch: `tr(PRIMARY,{and_v(v:pk(RECOVERY),older(52560))})` (52,560 blocks = 365 days at 10 min, derived).
  - Agent with human brake and human escape hatch: `tr(HUMAN,{and_v(v:pk(AGENT),pk(COSIGNER))})`: agent spends only with the policy co-signer; human alone via key path.
  - Human co-sign on every agent spend, attributable: `tr(NUMS,{multi_a(2,AGENT,HUMAN,COSIGNER)})`.

### Gaps
- Casa documentation was not opened (see Unverified). libsecp256k1 MuSig2/FROST module status not checked.
- Nunchuk's enforcement point (server vs script) is unstated in the source.

## 3. Covenants and vaults: CTV, OP_CAT, CSFS, OP_VAULT, LNHANCE, INTERNALKEY; status November 2026; pre-signed vaults

### Takeaway
No covenant opcode is active on Bitcoin mainnet as of 2026-11-26. CTV (BIP-119), CSFS (BIP-348), INTERNALKEY (BIP-349), TEMPLATEHASH (BIP-446) and the BIP-448 bundle are Draft; OP_CAT (BIP-347) is Complete but not activated; OP_VAULT (BIP-345) is Closed with BIP-443 (CCV) as its proposed replacement. A CTV activation meeting (reported 2026-01-02) favored BIP9 with conservative parameters, but no activation client has shipped. Without covenants, destination restrictions exist only as pre-signed transactions (with key deletion or n-of-n committees) or co-signer policy.

### Cited Findings
- Status (BIP index, 2026-11-25): BIP-119 CTV Draft; BIP-345 OP_VAULT Closed ("Proposed-Replacement: 443"); BIP-346 OP_TXHASH Draft; BIP-347 OP_CAT Complete; BIP-348 CSFS Draft; BIP-349 OP_INTERNALKEY Draft; BIP-442 OP_PAIRCOMMIT Draft; BIP-443 OP_CHECKCONTRACTVERIFY Draft; BIP-446 OP_TEMPLATEHASH Draft; BIP-448 "Taproot-native (Re)bindable Transactions" Draft; BIP-449 OP_TWEAKADD Draft. [bips-index], [bip345]
- BIP-119: CTV redefines OP_NOP4; fails unless the 32-byte stack element equals the DefaultCheckTemplateVerifyHash, which "commits to the serialized version, locktime, scriptSigs hash..., number of inputs, sequences hash, number of outputs, outputs hash, and currently executing input index"; "Activation logic is elided from this BIP". [bip119]
- BIP-347: OP_CAT in tapscript, redefining OP_SUCCESS126; fails if the result exceeds 520 bytes. [bip347]
- BIP-348: CSFS replaces OP_SUCCESS204; pops pubkey, message, signature; verifies a BIP-340 signature over arbitrary stack data. [bip348] BIP-349: OP_INTERNALKEY replaces OP_SUCCESS203 and pushes the taproot internal key. [bip349]
- BIP-345 (Closed): OP_VAULT/OP_VAULT_RECOVER with CTV "allow users to enforce a delay period before designated coins may be spent to an arbitrary destination, with the exception of a prespecified 'recovery' path." [bip345]
- LNHANCE: Optech 2025-12-05: Moonsettler proposes a soft fork for LNHANCE = BIP-119 + BIP-348 + BIP-349 + OP_PAIRCOMMIT; a "similar tapscript-only opcode package including OP_TEMPLATEHASH" is newer. [optech-2025-12-05]
- Open letter: Optech 2025-07-04: an open letter signed by 66 individuals (at time of writing) "asks Bitcoin Core contributors to prioritize the review and integration of OP_CHECKTEMPLATEVERIFY (CTV) and OP_CHECKSIGFROMSTACK (CSFS) within the next six months." [optech-2025-07-04]
- Optech 2026-01-02: at a CTV activation meeting, attendees "agreed that a CTV activation client should use conservative parameters (i.e. long signaling and activation periods) and BIP9"; other developers had not weighed in. [optech-2026-01-02] Optech's CTV topic lists no 2026 activation event after that meeting (only reports, demos and a proof-of-concept vault). [optech-ctv-topic]
- Optech 2026-09-04: BIP-448 (TEMPLATEHASH + CSFS + INTERNALKEY) implementations include Bitcoin Inquisition and "a Bitcoin Core patch without activation"; the bundle would be usable on default signet with the next Inquisition release. [optech-2026-09-04]
- Optech 2026-10-02: Lillian Wang's vault comparison "concludes that CTV fits simple vaults with precomputed outputs, CCV best supports partial withdrawals and choosing a withdrawal address at trigger time"; APOAS vault addresses must never be reused (half-spend). [optech-2026-10-02]
- Optech definitions: covenants are "proposed changes to Bitcoin's consensus rules that would allow a script to prevent an authorized spender from spending to certain other scripts" [optech-covenants-topic]; vaults "require two separate transactions to appear in two different blocks", giving the owner time to block the second. [optech-vaults-topic]
- **Moser, Eyal, Sirer 2016** (FC 2016 Workshops, LNCS, pp. 126-141): propose `CheckOutputVerify(index, value, pattern)`; vaults "disincentivize key theft by preventing an attacker from gaining full access to stolen funds"; "vault transactions cannot be implemented with existing timing mechanisms such as the CheckLockTimeVerify opcode or transaction locktime"; also "poison transactions" for "penalizing double-spending attacks". [moser2016]
- **Revault** (pre-signed vault, multi-party custody): N-of-N stakeholders; delegated K-of-M managers; after each deposit stakeholders exchange signatures for 4 pre-signed, not broadcast, transactions (Emergency, Unvault, Cancel, Unvault Emergency). Unvault descriptor: `or(1@thresh(len(stakeholders), stakeholders), 9@and(thresh(len(managers), managers), and(thresh(len(cosigners), cosigners), older(X))))`. Managers "are forced to wait for the unvault time-lock to expire before they can broadcast a Spend TX"; watchtowers broadcast Cancel unless the spend "adheres to a pre-configured spend policy"; a co-signing server signs any Spend TX "but only once" to stop replacement. Risk: anyone holding one Emergency TX can force all funds into the emergency path (blackmail / business-continuity risk). [revault-intro], [revault-tx]

### Inferences
- Destination restrictions possible today without covenants: (a) pre-signed transactions from an output whose other spend paths require keys that are deleted or held by an n-of-n committee (Revault, Babylon, BitVM2/Clementine); (b) co-signers that refuse non-policy spends (BitGo, Bitkey, Nunchuk; trust in the co-signer); (c) hash or timelock gating only, which says nothing about destination. Pre-signing costs interactivity per deposit and breaks if amounts or fees must change later.
- Revault maps almost one-to-one onto N5/N11: "managers" = agents, "stakeholders" = humans, watchtower = automated veto. It is a 2020-era working design, so N5 is not novel.
- A soft fork that would make agent vaults native (CTV, CCV, TEMPLATEHASH) is not scheduled. Escapement should design for pre-signed or co-signed vaults and treat covenant versions as upside.

### Gaps
- Optech 2026-06-05 "CTV-only vault proof of concept" not opened.
- I did not find a definitive list of which Bitcoin Core releases (31.x, 32.x) contain any covenant code; Optech says only an unactivated patch exists for BIP-448.

## 4. Slashing on Bitcoin without smart contracts: Babylon, JoinMarket fidelity bonds, Lightning penalty

### Takeaway
Bitcoin-native slashing exists today only where the slashing transaction is pre-signed and the last missing signature is released by the cheater's own misbehavior (Babylon's EOTS, Lightning revocation keys), or where a committee co-signs. Babylon burns a fixed fraction of the staker's BTC when the delegated finality provider double-signs, and relies on an M-of-N covenant committee to emulate the missing covenant. JoinMarket fidelity bonds are pure time-value sacrifice (no slashing) priced superlinearly to punish sybil splitting. The user-suggested paper (Tas et al., IEEE S&P 2023) is about Bitcoin timestamping/checkpointing of PoS chains, not about EOTS staking.

### Cited Findings
- Babylon staking output (Taproot, NUMS internal key) has three script paths: timelock `<StakerPK> OP_CHECKSIGVERIFY <TimelockBlocks> OP_CHECKSEQUENCEVERIFY` (timelock "must be lower than 65535"); unbonding `<StakerPk> OP_CHECKSIGVERIFY <CovenantPk1> OP_CHECKSIG ... OP_CHECKSIGADD <CovenantThreshold> OP_NUMEQUAL`; slashing `<StakerPk> OP_CHECKSIGVERIFY <FinalityProviderPk> OP_CHECKSIGVERIFY <CovenantPk1> OP_CHECKSIG ... <CovenantThreshold> OP_NUMEQUAL`. [babylon-staking-script]
- "The staker is required to submit a pre-signature for spending the slashing path in order for their stake to be accepted"; the slashing path "requires a pre-signed slashing transaction by both the staker and a CovenantThreshold of the covenant emulation committee... This ensures that the finality provider's cooperation is needed to prevent slashing, but not to execute it. If a finality provider misbehaves, their key is exposed and can be used to execute the slashing." [babylon-staking-script]
- Slashed coins: the slashing transaction has exactly two outputs: "the first sending the slashed fraction of the funds to a burn address specified in the Babylon Genesis chain's parameters", the second to a slashing refund output timelocked before the staker can redeem it. The unbonding output also carries a slashing path so a staker "can still be slashed during the unbonding period". [babylon-staking-script]
- Parameters (`covenant_pks`, `covenant_quorum`, `slashing_pk_script`, `slashing_rate`, `min_slashing_tx_fee_sat`, `unbonding_time_blocks`, min/max staking value and time) are set by the Babylon chain. [babylon-register]
- Covenant committee: "an M-out-of-N multi-signature that co-signs BTC transactions with the BTC staker... There's no way the covenant committee can act against the stakers, except rejecting their staking requests" (vendor claim). "Currently, only a single finality provider securing the Babylon Genesis chain can be selected." [babylon-staking-script]
- EOTS: "If a finality provider re-uses the same committed randomness to sign two conflicting blocks on the same height, their EOTS private key is exposed, leading to the slashing of their delegations." [fp-slashing-protection] Finality providers commit public randomness per height via a Merkle root before voting. [fp-commit-pub-rand]
- Derived (from the BIP-340 equation s = k + e·d mod n [bip340]): two valid signatures (R, s1) and (R, s2) with the same R on different messages give d = (s1 - s2) / (e1 - e2) mod n. Pre-committing R per slot makes any second signature for the slot either invalid (different R) or key-revealing (same R).
- **Tas, Tse, Gai, Kannan, Maddah-Ali, Yu** (arXiv 2207.08392; "In IEEE Symposium on Security and Privacy 2023"): Babylon "checkpoints onto Bitcoin" to fix non-slashable long-range attacks; withdrawal delay reduced "from weeks... to less than 5 hours" at "less than 10K USD per annum" for checkpoints (authors' experiment). Full-text search: 0 occurrences of "extractable" or "one-time sig". [tas2023]
- **JoinMarket fidelity bonds**: coins sent to a CLTV-timelocked address; "The valuable thing being sacrificed is the time-value-of-money"; "a long-term holder (or hodler) of bitcoins can buy time-locked fidelity bonds essentially for free"; simplified value `bond_value = (locked_coins * (exp(interest_rate * locktime) - 1))^x`, default x = 1.3 and interest_rate = 1.5% per annum; sacrificed value capped at the value of burned coins; after expiry value "will exponentially drop". [jm-fidelity] BIP-46 (Draft) standardizes HD derivation for timelocked fidelity bond addresses and signing certificates so bond keys can stay in cold storage. [bip46]
- Derived check of the JoinMarket docs: 5^1.3 = 8.10 and 6^1.3 = 10.27 (docs say ~8.1 and ~10.3). Splitting 6 units into six bonds of 1 yields 6 x 1^1.3 = 6 vs 10.27 for one bond: about 42% less total weight, which is the anti-sybil effect. (derived)
- **Lightning penalty**: BOLT 3 `to_local` witness script: `OP_IF <revocationpubkey> OP_ELSE to_self_delay OP_CHECKSEQUENCEVERIFY OP_DROP <local_delayedpubkey> OP_ENDIF OP_CHECKSIG` [bolt03]; BOLT 5: if a node broadcasts an outdated commitment, "the other node in the channel can use its revocation private key to claim all the funds from the channel's original funding transaction"; this is safe only "provided that the situation is properly handled" (someone must watch within to_self_delay). [bolt05]

### Inferences
- Pattern for N3 (adjudicator-free slashing): bond output where the slashing leaf needs (principal pre-signature) + (agent EOTS key) + (committee quorum pre-signature), with a fixed burn or victim output. The committee is needed only because Bitcoin lacks a covenant to force the slashing destination and to stop early withdrawal; with CTV-like opcodes the committee could disappear (BitVM2 authors say the same about their committee, see section 5).
- Babylon already puts the delegator's own coins at risk for a delegate's equivocation. That is structurally N2 (liability on the principal for the agent's act), though Babylon's "misbehavior" is a narrow, objectively checkable equivocation, not adjudicated harm.
- EOTS only catches provable equivocation (two signatures for one slot). Most AI misbehavior is not equivocation; it needs an adjudicator (oracle, committee, court), which brings back trust.
- Fidelity bonds cost capital times time, not time alone: a wealthy principal can mint many bonds at once, and hodlers pay almost nothing. This undercuts N6's "time cost fast agents cannot compress": the time cannot be compressed, but it can be pre-bought in parallel.

### Gaps
- The Babylon Bitcoin Staking whitepaper (where EOTS staking is formalized) was not opened; current mainnet values of `covenant_quorum`, committee size and `slashing_rate` were not retrieved.
- Chris Belcher's "Financial mathematics of fidelity bonds" gist was not opened.

## 5. Oracles and adjudication: DLCs, BitVM/BitVM2, fraud proofs, bridges

### Takeaway
DLCs let parties settle on an oracle's attestation with the oracle learning nothing, and an oracle that publicly attests two outcomes leaks its private key (another equivocation-to-key primitive). BitVM (2023) and BitVM2 (2024/2025) give optimistic fraud proofs on today's Bitcoin, with BitVM2 needing 1-of-n honest signers at setup (because there are no covenants) and permissionless challengers; Citrea's Clementine bridge is live on mainnet with a 1-of-N claim. All of these move trust to oracles, committees or liveness assumptions rather than removing it.

### Cited Findings
- Dryja 2017 (MIT DCI): if the oracle "attempts to publicly report two different prices... she will reveal her permanent private key"; an oracle who is herself a counterparty can cheat once without revealing her key, which is "detectable" and provable; multiple oracles can be combined by adding their points; contracts should include "a refund transaction which can be broadcast by either party a few days after" the expected attestation in case the oracle disappears. [dlc-dryja2017]
- DLC specs repository: "currently a work-in-progress"; implementations listed include bitcoin-s, cfd-dlc, rust-dlc, node-dlc (fetched 2026-11-26). [dlcspecs-readme]
- BitVM (Linus, 2023-12-12): "requires no changes to the network's consensus rules"; computations "are merely verified, similarly to optimistic rollups"; "The main drawback... is that it is limited to the two-party setting with a prover and a verifier"; prover and verifier "pre-sign a sequence of challenge-and-response transactions". [bitvm2023]
- BitVM2 bridge paper (Linus, Aumayr, Zamyatin, Pelosi, Avarikioti, Maffei): reduces trust "from an honest majority (t-of-n) to existential honesty (1-of-n) during setup"; "only one active rational operator"; "any user with a Bitcoin full node can challenge"; disproof in "only 3 on-chain transactions that can be executed within 1-2 weeks" (authors' claim); signers: "One of the n signers is assumed to be honest... this... assumption is not necessary if the underlying blockchain supports covenants." [bitvm2-bridge]
- ePrint 2025/1158 "Bridging Bitcoin to Second Layers via BitVM2" (9 authors incl. Tse, Zamyatin; received 2025-06-18, revised 2026-03-04): "a full challenge verification has been executed on the Bitcoin mainnet" (authors' claim). [bitvm2-eprint]
- Citrea docs (vendor): Clementine "has a 1-of-N trust assumption"; "deployed on Citrea mainnet"; Signers "pre-sign the allowed spend rules... emulate covenant-like restrictions"; Watchtowers publish a "Bitcoin header-chain proof with total work"; "Operators ⊆ Signers ⊆ Watchtowers ⊆ Challenger ⊆ Users (permissionless)"; the bridge path is "spendable only with all Signers' signatures". [citrea-docs]

### Inferences
- For N2 (adjudicated slashing), a DLC-style oracle is the cleanest Bitcoin-native adjudicator: the bond's slash and refund transactions are pre-signed as adaptor-signature CETs, the oracle's attestation completes one, and a timelocked refund handles oracle disappearance. Trust lands on the oracle's honesty; equivocation is punishable by key leak, but a single lie is not.
- BitVM2-style fraud proofs could, in principle, adjudicate "agent did X" claims if X is a checkable computation; the cost (multi-week challenge windows, heavy setup) suits large, rare disputes, not routine agent oversight.
- Bridges and BitVM2 emulate covenants via n-of-n pre-signing with key deletion: the same trick Escapement would use for bonded agents today.

### Gaps
- BOB's bridge was not researched (no source opened).
- USENIX Security 2026 acceptance of the BitVM2 paper appeared only in search results (Unverified).

## 6. Commitments and timestamping: OpenTimestamps, Haber-Stornetta, single-use seals, RGB, Taproot Assets, OP_RETURN and the v30 policy change

### Takeaway
OpenTimestamps gives cheap, aggregated proofs that data existed before a Bitcoin block, verifiable with a node and without trusting calendars once complete; but a timestamp proves existence, not uniqueness, so it does not stop equivocation. Single-use seals (a UTXO spent exactly once, committing to a message) add non-equivocation, and RGB/Taproot Assets use that model for assets. Bitcoin Core v30 (2025-10-13) raised the default OP_RETURN relay limit from 83 bytes to 100,000; the consensus counter-proposal BIP-110 caused a short chain split on 2026-08-08 at block 961,632, stalled, and was Closed on 2026-08-09.

### Cited Findings
- Haber, Stornetta, "How to time-stamp a digital document", Journal of Cryptology 3, pp. 99-111, 1991 (bibliographic metadata only, via Crossref). [haber1991]
- Todd 2016 (OpenTimestamps announcement, 2016-09-15): aggregation servers combine pending digests "into a single merkle tree, and then the tip of that tree is timestamped with Bitcoin"; "allowing timestamps to be created for free by combining an unlimited number of timestamps into one Bitcoin transaction" (project claim); public calendars "are a central point of failure", so a timestamp that still needs a calendar is "incomplete", and `--wait` avoids calendars; Bitcoin's nTime is "very likely... accurate to within two or three hours... and almost certainly within a day"; "A timestamp only proves a message existed, not the message... you could have timestamped two conflicting IRC logs." [todd-ots-2016]
- OpenTimestamps client README: "to verify timestamps you need a local Bitcoin Core node (a pruned node is fine)"; "It takes a few hours for the timestamp to get confirmed... we're not doing one transaction per timestamp" (project docs). [ots-client-readme]
- Todd 2016-12-07, single-use seals: a seal "can be closed over a message after the fact, producing a proof that the seal has been irrevocably bound to the message. A single-use-seal is secure if it's infeasible to produce two apparently valid proofs that the same seal has been closed over two different messages." Bitcoin implementation: the seal is a txout; closing = spending it in a transaction whose last output is an OP_RETURN with the message digest, and each message commits to the next seal (a chain of solvency proofs, demonstrated with mainnet transactions). [todd-seals-2016]
- Taproot Assets (Lightning Labs docs, vendor): the asset tree root "is added to a taproot tapscript"; once confirmed the issuer "can no longer change or amend it"; a Universe "has no privileges" and can only withhold data; an asset becomes invalid once its output is spent without committing to a new tree, which "is not obvious for a third party observer". [taproot-assets-docs]
- RGB docs: RGB enforces "contracts and assets... leveraging Bitcoin consensus rules"; RGB v0.12 is labeled an "unfinished proposal [to] rewrite the protocol" (site banner). [rgb-docs]
- **Bitcoin Core v30.0** (GitHub release published 2025-10-13): "`-datacarriersize` is increased to 100,000 by default, which effectively uncaps the limit"; it "can be overridden with `-datacarriersize=83` to revert"; "Multiple data carrier (OP_RETURN) outputs in a transaction are now permitted for relay and mining", the limit applying to their aggregate size; default `-minrelaytxfee` and `-incrementalrelayfee` lowered to 0.1 sat/vB. [core-rn30], [core-releases]
- Current source: `MAX_OP_RETURN_RELAY = MAX_STANDARD_TX_WEIGHT / WITNESS_SCALE_FACTOR` with `MAX_STANDARD_TX_WEIGHT{400'000}`, i.e. 400,000 / 4 = 100,000 bytes (derived). `DEFAULT_ACCEPT_DATACARRIER = true`. [core-policy-h]
- Latest Bitcoin Core releases: v32.1 (2026-10-28), v31.3 and v30.5 (2026-11-20). [core-releases]
- **BIP-110** "Reduced Data Temporary Softfork" (Dathon Ohm; assigned 2025-12-03): one-year rules capping new scriptPubKeys at 34 bytes except OP_RETURN up to 83 bytes, pushes and witness items at 256 bytes, banning OP_SUCCESSx and executed OP_IF in tapscript, etc.; modified BIP9 with 55% threshold, mandatory signaling blocks 961632 to 963647, `max_activation_height` 965664, `active_duration` 52416 blocks. Changelog: "1.0.1 (2026-08-09): Mark as Closed, following a chain split with stalled mining". [bip110]
- The Block (news, 2026-08-08): split at block 961,632; AntPool mined the first non-signaling block; BIP-110 nodes followed a Roughnecks/Ocean block; by 6 p.m. ET main chain at 961,640 vs BIP-110 chain at 961,633 ("only two new blocks"); in the last period 51 blocks signaled (2.53%) vs 1,109 of 2,016 needed (measured, as reported); background: v30 "effectively removing the longstanding 83-byte limit", the dispute produced BIP-444 (October 2025) which became BIP-110. [theblock-bip110]
- IETF draft-fassbender-scitt-time-anchor-07 (Informational, 2026-09-24, expires 2027-03-28): anchors SCITT transparency-log artifacts to Bitcoin via OpenTimestamps; motivating example: "An AI research laboratory produces model weights and safety evaluations"... regulators ask how "the lab did not register these weights after the safety evaluation was already public"; the guarantee is "these model weights existed no later than block height H"; "calendar aggregation typically adds hours"; log-root anchoring "strengthens equivocation detection" by providing "a reference point outside the log". [ietf-fassbender-07]

### Inferences
- OTS answers "existed no later than block H"; including a recent block hash inside the committed data answers "created no earlier than block H'". Together they bracket a log entry in time. Neither stops an agent from anchoring two different logs; only a single-use seal chain (or a publicly known single anchoring key whose spends are watched) makes a fork of the log detectable as a double-close.
- Cost: direct OP_RETURN anchoring costs fee rate x vsize per anchor (derived formula); OTS amortizes one transaction over arbitrarily many digests, so per-entry cost is near zero but latency is hours (project docs, IETF draft).
- The v30 change and the BIP-110 failure show that OP_RETURN size is policy, not consensus, and that the community rejected a consensus data cap in 2026; small commitments (32-byte hashes) are unaffected either way.
- For N8, model-weight hash commitments anchored with OTS are already specified (IETF draft, 2026); Escapement's contribution would have to be non-equivocation (seals) or agent action logs, not anchoring itself.

### Gaps
- No independent measurement of current OTS calendar operators, uptime or batch interval was found.
- RGB's exact current version and mainnet status were not established from an opened primary source.

## 7. Off-chain layers: Lightning/BOLT12, NWC (NIP-47), L402, Cashu, Fedimint, Ark, Spark

### Takeaway
Spending caps, expiry and revocation for agents exist today almost only in off-chain layers, and there they are enforced by a trusted party: the NWC wallet service (`max_amount`, `renewal_period`, `expires_at`), the L402 server (`valid_until` caveats), the Cashu mint (locktime by the mint's clock), the Ark operator or Spark operators. Lightning itself is trust-minimized but has no protocol-level spending caps; node-level macaroons and client flags provide them (vendor tooling for agents shipped 2026-02-11).

### Cited Findings
- **NIP-47 (NWC)**, `draft optional`; core spec simplified on 2026-08-01 (commit "NIP-47: simplify core spec and introduce extensions (#2419)"); extensions live in github.com/nostr-wallet-connect/nwc. Connection secrets: "Keys can be revoked and created at will and have arbitrary constraints (eg. budgets)"; error `QUOTA_EXCEEDED`; requests may carry an `expiration` tag. [nip47]
- **NWC-08** (client-initiated connection creation): `expires_at` "The connection cannot be used after this date"; `max_amount` "limiting the cumulative outgoing amount, including fees, in millisatoshis per renewal_period"; `renewal_period` one of `never|daily|weekly|monthly|yearly` (`never` is default); `isolated` sub-wallet; "If max_amount is present, the wallet service MUST enforce it... or decline"; "MUST ensure concurrent payments cannot collectively exceed max_amount". [nwc-08]
- **NWC-13** `get_budget` returns `used_budget`, `total_budget` (msat), `renews_at`, `renewal_period`; "The budget is a spending limit, not the wallet balance". [nwc-13]
- **Alby** AI page (dated 2026-11-20, vendor): "Create sub-wallets for your agents, with their funds isolated from your main wallet"; "You're in full control of agent's budget and its wallet permissions"; agent can use the wallet "as long as it's online". [alby-ai]
- **L402** (Lightning Labs): server returns `402` with macaroon + BOLT11 invoice; the macaroon "commits to the payment hash", so verification needs no database; caveats chain by HMAC so holders can add but "cannot remove existing caveats"; each repeated caveat "MUST restrict further (never widen)"; `<service>_valid_until` (unix timestamp) gives expiry; capability caveats scope operations; revocation is by the issuer (e.g. "revoke and re-mint"). [l402-readme], [l402-macaroon], [l402-agent]
- **Lightning agent tools** (Lightning Labs post, 2026-02-11, vendor): seven skills including "remote-signer key isolation"; "The signer machine holds the private keys and never routes payments"; macaroon bakery with "five preset roles" (pay-only, invoice-only, read-only, channel-admin, signer-only); "lnget's --max-cost flag sets a per-request spending ceiling"; bakery can "cap total spending at the Lightning node level". [ll-agent-tools]
- **BOLT12** offers: `offer_amount`, `offer_absolute_expiry` (seconds from epoch), `offer_quantity_max`; "Payer proofs are proofs of invoice payment" (prefix `lnp`). [bolt12] Eclair v0.11.0 "adds official support for BOLT12 offers" (Optech 2024-12-06). [optech-2024-12-06]
- **Cashu NUT-10/11/14**: NUT-10 defines structured `Secret` spending conditions checked by the mint; NUT-11 P2PK tags `sigflag` (`SIG_INPUTS` default, `SIG_ALL`), `pubkeys`, `n_sigs`, `locktime` ("the Unix timestamp of when the lock expires"), `refund`, `n_sigs_refund`; the lock is "active" if "the mint's local clock is less than or equal to locktime"; after expiry Locktime Multisig "continue[s] to apply" and refund keys can additionally spend; if no refund tag, an expired proof is "spendable without a witness signature". NUT-14 HTLC: hash lock plus NUT-11 tags; receiver path "ALWAYS available" with the preimage; sender refund after locktime. [nut10], [nut11], [nut14]
- **Ark** (Optech topic): users share UTXOs via trees of pre-signed transactions; "VTXOs 'expire' according to an absolute timelock. After this timelock expires, both the Ark operator and users can unilaterally spend"; users must move VTXOs into a new tree before expiry; out-of-round payments need sender + operator co-signatures, so "receivers must trust that the sender will not collude with the operator to double-spend". [optech-ark-topic] Lightning Labs' Ark-like Wavelength is on mainnet as an alpha "with accounts limited to 300,000 sats" (Optech 2026-11-20, vendor limit). [optech-2026-11-20]
- **Arkade** (Ark Labs docs, vendor): single operator; "As cosigner, it refuses to sign spends of virtual outputs that are already spent"; it runs Arkade Script in an emulator and "signs a spend of a path written in it only if the script passes"; unilateral exit is the emergency path; renewal needed to keep exit rights. [arkade-docs]
- **Spark** (vendor docs): "moment-in-time" trust; "As long as at least one (or a configurable threshold) of the Spark operators behaves honestly during a transfer, the system ensures perfect forward security", achieved by operators "forgetting the operator key after a transfer". [spark-trust]

| Layer | Enforces | Must trust | Spending cap | Expiry | Revocation |
|---|---|---|---|---|---|
| Bitcoin L1 script | keys, hashes, min time (abs/rel) | nobody beyond consensus; hashrate majority for time | UTXO value only | no (emulate by race) | no (spend it away) |
| Lightning (BOLTs) | channel balances, HTLC timeouts, penalty | watchers online within to_self_delay | not in protocol; node macaroons, client flags | invoices/offers expire (BOLT12) | revocation keys for old states |
| NWC (NIP-47 + NWC-08/13) | per-connection methods, budgets | wallet service (holds keys or node access) | yes, `max_amount` per period | yes, `expires_at` | yes, delete connection key |
| L402 | paid, scoped API access | the server (and its root key) | per caveat semantics; client `--max-cost` | `valid_until` caveat | issuer-side |
| Cashu (NUT-11/14) | P2PK, multisig, HTLC, refund at locktime | the mint (custody and clock) | no protocol cap (bearer amounts) | lock expiry by mint clock | no (bearer) |
| Fedimint | federated ecash | guardian threshold (not verified here) | not verified | not verified | not verified |
| Ark / Arkade | VTXO trees; operator sweep after expiry | operator for out-of-round and liveness; exit is trustless | no | VTXO expiry (forces renewal) | no |
| Spark | statechain-style transfers | 1-of-n (or threshold) operators deleting keys | no | exit timelocks (not verified) | no |

### Inferences
- NWC-08 already implements N1 almost exactly: a capped, optionally non-renewing allowance with a hard expiry and revocation, enforced by the wallet service. What Bitcoin adds is only that the wallet service cannot exceed the sats it holds.
- Ark's VTXO expiry is the closest production instance of a Bitcoin-enforced lease: if the holder does not renew before the absolute timelock, a competing party (the operator) gains a spend path. N4 could reuse this shape with the human in the operator's role.
- Cashu locktimes are wall-clock and mint-enforced; they are not Bitcoin timelocks.

### Gaps
- Fedimint docs could not be loaded (empty response); no claim rests on them.
- Spark's exit timelock lengths were not read from a primary page.
- BOLT11 invoice expiry semantics were not opened.

## Unverified sources

Opened nothing, or only search snippets, for these; no claim above rests on them.
- Casa (casa.io) co-signer and key-recovery docs: not opened.
- Chris Belcher, "Design for improving JoinMarket's resistance to sybil attacks using fidelity bonds" and "Financial mathematics of fidelity bonds" (GitHub gists): not opened.
- Babylon "Bitcoin Staking" whitepaper (EOTS formalization): not opened; docs.babylonchain.io failed DNS.
- fedimint.org Trust Trade-Offs page: fetch returned empty.
- USENIX Security 2026 program listing for "Bridging Bitcoin to Second Layers via BitVM2": seen in search results only.
- Bitkey support article on daily-limit reset times: blocked by Cloudflare.
- Spark research article on key deletion and ~2-week CSV exits; spark.money glossary pages: search snippets only.
- Optech 2026-06-05 "CTV-only vault proof of concept"; Pieter Wuille's Delving Bitcoin BIP-54 proof: not opened.
- KuCoin, crypto.news, Forklog, CryptoSlate coverage of BIP-110: not opened (The Block was).
- IETF draft-thaha-scitt-agent-execution-evidence-01 (Oct 2026): seen in search results only; may be closer prior work for agent action logs.
- Proof-of-useful-work papers (arXiv 2610.26713, 2001.09244, 1903.09800) and EA Forum "Proof of useful work for verifying AI treaties": search snippets only.
- arXiv 2609.02992 ("Tempting the Agent", staking/slashing for agent markets), 2512.08737 (insured agents), 2507.00631 (bonded verification): search snippets only.
- RFC 9591 (FROST): cited only through the BIP-445 PR body.
- Nunchuk developers page; Alby MCP README; PolicyLayer and dev.to agent-wallet posts: not opened.

## Implications for Escapement

**Buildable today on Bitcoin L1, trust-minimized**
- Hard caps by funding granularity: the agent can lose at most the value of UTXOs its key paths reach. An allowance is "a UTXO the human funded"; renewal is the human funding another one. This is the only budget Bitcoin itself enforces.
- Human brake (N11): every agent spend needs a human or human-controlled key: `tr(NUMS,{multi_a(2,AGENT,HUMAN,COSIGNER)})` or `and_v(v:pk(AGENT),pk(HUMAN))`. Use script paths, not MuSig2/FROST, if you need on-chain attribution of who signed.
- Delays with human veto (N5) via pre-signed vaults (Revault pattern): agent can trigger an Unvault, must wait `older(X)`, humans or their watchtower can broadcast a pre-signed Cancel to a safer descriptor.
- Dead-man switches (Liana pattern) and "not before" gates of up to ~455 days relative (derived) or any absolute height/time.
- Equivocation-triggered slashing (N3) for objectively checkable double-signing, using EOTS plus a pre-signed slashing transaction (Babylon pattern), with burn or victim outputs fixed in advance.
- Timelocked fidelity bonds (N6) with JoinMarket's superlinear valuation to discourage splitting.
- Audit anchors (N8): OTS for "existed before block H"; block hash inside the record for "created after block H'"; a single-use-seal chain for non-equivocation.

**Needs a trusted party (works today, but someone can cheat or censor)**
- Per-period spending caps, velocity limits, destination whitelists, expiry and revocation of authority: NWC wallet services, L402 issuers, Cashu mints, Lightning node macaroons, policy co-signers (BitGo, Bitkey, Nunchuk). Bitcoin script cannot read amounts or destinations.
- Babylon-style slashing needs a covenant-emulation committee; BitVM2/Clementine need 1-of-n honest setup signers; DLC adjudication needs an honest oracle (equivocation is punishable, a single lie is not).
- Any "expiry" of agent authority on L1 is a race: a human or watchtower must actually spend a competing path or broadcast a pre-signed transaction in time. Liveness of the watcher is a trust assumption.
- Adjudicated misbehavior (most AI harms) is not mechanically detectable; slashing for it always needs an oracle, committee or court.

**Needs a soft fork that has not happened (as of 2026-11-26)**
- True expiry ("not after"): OP_EXPIRE (2023) or input-triggered expiry (2026) proposals; none has a BIP number or activation plan.
- Native vaults and destination-restricted agent wallets: CTV (BIP-119, Draft), CCV (BIP-443, Draft), TEMPLATEHASH/BIP-448 (Draft), OP_CAT (BIP-347, Complete, not activated). OP_VAULT (BIP-345) is Closed.
- Committee-free slashing destinations and committee-free bridges: need covenants (BitVM2 authors say their committee "is not necessary if the underlying blockchain supports covenants").
- A non-compressible block clock against a hashrate majority: BIP-54 timewarp fix (Complete, regtest-only implementation; activation discussion perhaps 2H 2027 per Riard).

**Where the evidence undercuts the thesis**
- "Unforgeable authority" caps only what keys can sign; caps on amounts per period and on destinations are not Bitcoin-enforced today, so most of the "spend cap" story is a trusted-service story with Bitcoin underneath.
- "Uncompressible time" is uncompressible for minorities only; a hashrate majority can accelerate blocks until BIP-54 activates; and time-cost sybil friction (bonds) is cheap for whoever already holds idle coins ("essentially for free", JoinMarket docs).
- Timestamps do not prevent equivocation; non-equivocation needs seals plus watchers who check the chain.
- Blockspace is a global auctioned resource, not a per-actor limit: a funded agent can outbid everyone, and off-chain layers bypass it.

## Novelty check

- **N1 Sat allowances as dead-man switch.** Closest: NWC-08 `max_amount` + `renewal_period` (`never` = non-renewing) + `expires_at` [nwc-08]; Lightning Labs agent tools (2026-02-11) with scoped macaroons and `--max-cost` [ll-agent-tools]; Alby agent sub-wallets (2026-11-20) [alby-ai]; Nunchuk agent spending limits (2026-04-08) [nunchuk-blog]; HBHC heartbeat-bound agent credentials (no Bitcoin) [hbhc-2026]. Verdict: **exists** (off-chain, trusted service); an on-chain, script-enforced periodic allowance is impossible without covenants.
- **N2 Principal-funded bonds slashed on adjudicated misbehavior.** Closest: Babylon (delegator BTC burned for its finality provider's equivocation) [babylon-staking-script]; AgentCity (EVM L2: "humans adjudicate through a complete ownership chain binding every agent to a responsible principal") [agentcity-2026]; DLC oracles as adjudicators [dlc-dryja2017]. Verdict: **partial** (mechanisms exist; a Bitcoin-native, principal-funded agent bond with adjudication was not found).
- **N3 Adjudicator-free slashing on equivocation for agents' signed commitments.** Closest: Babylon EOTS [fp-slashing-protection]; DLC oracle key leak on double attestation [dlc-dryja2017]; Moser et al. poison transactions [moser2016]; Lightning revocation [bolt05]. Verdict: **partial** (the primitive exists for PoS votes and oracles; applied to AI-agent commitments: not found). Queries tried: "Babylon extractable one-time signature EOTS..."; "AI agents staking bonds slashing accountability paper arXiv 2025 2026 agent collateral".
- **N4 Block-height leases on agent authority.** Closest: Ark VTXO expiry (absolute timelock after which the operator can spend; forces renewal) [optech-ark-topic]; "chaintip freshness" signed scores rejected after N blocks (self-published blog, default 6 blocks) [chaintip-devto]; HBHC (wall-clock heartbeats for agent swarms) [hbhc-2026]; NWC `expires_at` [nwc-08]. Verdict: **partial**. Bitcoin-timelock agent leases renewed by human signature: not found. Queries: "AI agent authority expires block height renewal timelock lease bitcoin agent credential".
- **N5 Timelocked vaults with human veto for irreversible agent actions.** Closest: Revault (managers delayed by `older(X)`, stakeholder/watchtower Cancel) [revault-intro]; Moser et al. vaults [moser2016]; Bitkey 7-day and 6-month delays (vendor) [bitkey-how]; Nunchuk "signing delays" for agents [nunchuk-blog]. Verdict: **exists** (pre-signed vaults with delegated spenders); AI-specific framing exists in vendor form.
- **N6 Seasoned or timelocked bonds as sybil friction for agent swarms.** Closest: JoinMarket fidelity bonds and BIP-46 [jm-fidelity], [bip46]. Verdict: **partial** (mechanism exists for coinjoin makers; agent-swarm application not found in opened sources). Queries: "AI agents staking bonds slashing accountability...". Caveat: capital can buy time in parallel.
- **N7 Blockspace as a global rate limit on high-stakes AI actions.** Closest: none as a safety mechanism; only news that agents may "crunch" blockspace (search results, not opened). Arithmetic: `MAX_BLOCK_WEIGHT` 4,000,000 WU = 1,000,000 vB per block [core-consensus-h]; if one action needs about 150 vB (assumption), about 6,666 actions per block and about 960,000 per day at 144 blocks/day (derived). Verdict: **not found**. Queries: "blockspace scarcity rate limit AI agents Bitcoin transactions throughput limit agents". Note: the limit is global and price-allocated, so it rate-limits the world, not a given agent.
- **N8 Tamper-evident, non-equivocating agent logs; model weight hash commitments.** Closest: IETF draft-fassbender-scitt-time-anchor-07 (model weights and safety evaluations anchored via OTS; equivocation detection via log-root anchoring) [ietf-fassbender-07]; single-use seals [todd-seals-2016]; OTS [todd-ots-2016]. Verdict: **exists** for weight-hash anchoring; **partial** for seal-based non-equivocating agent action logs (an IETF agent-execution-evidence draft exists but was not opened).
- **N9 Bitcoin as the clock for hardware-enabled compute governance.** Closest: Petrie 2024 firmware offline licensing (full text has no mention of blockchain or Bitcoin) [petrie2024]; FlexHEG 2025 (no mention of blockchain or Bitcoin in full text) [flexheg2025]. Verdict: **not found**. Queries: "hardware-enabled governance mechanisms AI chips license renewal offline licensing paper"; "Bitcoin block height as trusted clock for AI chip licensing compute governance". Inference: headers are a one-way clock (they prove at least so much work, hence time, has passed; they cannot prove that no more has passed), so a chip that is denied new headers sees time stand still; a licence-expiry design still needs a local tamper-resistant timer, the same "not before vs not after" asymmetry as script.
- **N10 Proof-of-work as an energy anchor for AI compute governance.** Closest: proof-of-useful-work proposals (search only, unverified). Verdict: **not found** in opened sources. Queries: "proof of work AI compute governance energy anchor bitcoin mining AI safety".
- **N11 Human keys co-sign high-stakes agent transactions.** Closest: Nunchuk agent key + user key + policy co-signer (2026-04-08) [nunchuk-blog]; Lightning Labs remote signer and scoped macaroons (2026-02-11) [ll-agent-tools]; BitGo policy co-signing [bitgo-policies]; Revault [revault-intro]; AESP (human-in-the-loop tiers for agent payments, EIP-712, not Bitcoin) [aesp-2026]. Verdict: **exists**.

```yaml
sources:
  - key: bips-index
    authors: Bitcoin BIPs editors
    year: 2026
    title: "BIP index (README.mediawiki), read at commit 2026-11-25"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/README.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/README.mediawiki
    supports: Status of every BIP cited (Deployed, Complete, Draft, Closed); FROST absent from index.
  - key: bip3
    authors: Murch
    year: 2025
    title: "BIP 3: Updated BIP Process"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0003.md
    url: https://github.com/bitcoin/bips/blob/master/bip-0003.md
    supports: Definitions of Draft, Complete, Deployed, Closed.
  - key: bip65
    authors: Peter Todd
    year: 2014
    title: "BIP 65: OP_CHECKLOCKTIMEVERIFY"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
    supports: CLTV failure conditions; nLockTime cannot prove impossibility of spending; 5-byte argument.
  - key: bip68
    authors: Mark Friedenbach, BtcDrak, Nicolas Dorier, kinoshitajona
    year: 2015
    title: "BIP 68: Relative lock-time using consensus-enforced sequence numbers"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0068.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0068.mediawiki
    supports: nSequence encoding, 512 s granularity, 16-bit mask, "a year of relative lock-time", 600 s rationale.
  - key: bip112
    authors: BtcDrak, Mark Friedenbach, Eric Lombrozo
    year: 2015
    title: "BIP 112: CHECKSEQUENCEVERIFY"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki
    supports: CSV failure conditions.
  - key: bip113
    authors: Thomas Kerin, Mark Friedenbach
    year: 2015
    title: "BIP 113: Median time-past as endpoint for lock-time calculations"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0113.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0113.mediawiki
    supports: MTP = median of last 11 blocks.
  - key: bip54
    authors: Antoine Poinsot, Matt Corallo
    year: 2025
    title: "BIP 54: Consensus Cleanup"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0054.md
    url: https://github.com/bitcoin/bips/blob/master/bip-0054.md
    supports: Timewarp description (minimum difficulty within 38 days); new timestamp, sigops, 64-byte and coinbase rules; status Complete.
  - key: bip119
    authors: Jeremy Rubin
    year: 2020
    title: "BIP 119: CHECKTEMPLATEVERIFY"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0119.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0119.mediawiki
    supports: CTV semantics; activation logic elided; Draft.
  - key: bip345
    authors: James O'Beirne, Greg Sanders
    year: 2023
    title: "BIP 345: OP_VAULT"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0345.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0345.mediawiki
    supports: OP_VAULT purpose; Status Closed; Proposed-Replacement 443.
  - key: bip347
    authors: Ethan Heilman, Armin Sabouri
    year: 2023
    title: "BIP 347: OP_CAT in Tapscript"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0347.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0347.mediawiki
    supports: OP_CAT semantics, OP_SUCCESS126, 520-byte limit; Complete.
  - key: bip348
    authors: Brandon Black, Jeremy Rubin
    year: 2024
    title: "BIP 348: CHECKSIGFROMSTACK"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0348.md
    url: https://github.com/bitcoin/bips/blob/master/bip-0348.md
    supports: CSFS semantics; Draft.
  - key: bip349
    authors: Brandon Black, Jeremy Rubin
    year: 2024
    title: "BIP 349: OP_INTERNALKEY"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0349.md
    url: https://github.com/bitcoin/bips/blob/master/bip-0349.md
    supports: OP_INTERNALKEY semantics; Draft.
  - key: bip110
    authors: Dathon Ohm
    year: 2025
    title: "BIP 110: Reduced Data Temporary Softfork"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0110.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0110.mediawiki
    supports: Data caps proposed; deployment parameters; Closed 2026-08-09 after chain split with stalled mining.
  - key: bip46
    authors: Chris Belcher, Thebora Kompanioni
    year: 2022
    title: "BIP 46: Address Scheme for Timelocked Fidelity Bonds"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0046.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0046.mediawiki
    supports: Fidelity bonds via CLTV; cold-storage certificates; Draft.
  - key: bip340
    authors: Pieter Wuille, Jonas Nick, Tim Ruffing
    year: 2020
    title: "BIP 340: Schnorr Signatures for secp256k1"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
    supports: Signing equation s = k + ed; nonce freshness and reuse leaks key.
  - key: bip341
    authors: Pieter Wuille, Jonas Nick, Anthony Towns
    year: 2020
    title: "BIP 341: Taproot: SegWit version 1 spending rules"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
    supports: NUMS internal key; always commit to a script tree for aggregate keys.
  - key: bip342
    authors: Pieter Wuille, Jonas Nick, Anthony Towns
    year: 2020
    title: "BIP 342: Validation of Taproot Scripts"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki
    supports: OP_SUCCESSx upgrade mechanism; leaf version 0xc0.
  - key: bip327
    authors: Jonas Nick, Tim Ruffing, Elliott Jin
    year: 2022
    title: "BIP 327: MuSig2 for BIP340-compatible Multi-Signatures"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
    supports: n-of-n only; outputs indistinguishable from single-sig; signing-state handling.
  - key: bip174
    authors: Ava Chow
    year: 2017
    title: "BIP 174: Partially Signed Bitcoin Transaction Format"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
    supports: Offline/hardware signers; per-output data for signer verification.
  - key: bip370
    authors: Ava Chow
    year: 2021
    title: "BIP 370: PSBT Version 2"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0370.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0370.mediawiki
    supports: Per-input required height/time locktime fields.
  - key: bip379
    authors: Pieter Wuille, Andrew Poelstra, Sanket Kanjalkar, Antoine Poinsot, Ava Chow
    year: 2023
    title: "BIP 379: Miniscript"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0379.md
    url: https://github.com/bitcoin/bips/blob/master/bip-0379.md
    supports: older/after/multi_a fragments; timelock type mixing rule.
  - key: bip388
    authors: Salvatore Ingala
    year: 2022
    title: "BIP 388: Wallet Policies for Descriptor Wallets"
    venue: github.com/bitcoin/bips
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0388.mediawiki
    url: https://github.com/bitcoin/bips/blob/master/bip-0388.mediawiki
    supports: Hardware signers must let users validate scripts and keys on-screen; host untrusted.
  - key: bip445-pr
    authors: Sivaram Dhakshinamoorthy (siv2r)
    year: 2026
    title: "BIP445: FROST Signing Protocol for BIP340 Signatures (PR #2070)"
    venue: github.com/bitcoin/bips pull request
    type: standard/BIP/RFC/spec
    id: https://github.com/bitcoin/bips/pull/2070
    url: https://github.com/bitcoin/bips/pull/2070
    supports: FROST BIP is an open PR (created 2026-01-03, open 2026-11-26); RFC 9591 incompatible with x-only keys.
  - key: core-rn30
    authors: Bitcoin Core contributors
    year: 2025
    title: "Bitcoin Core v30.0 Release Notes"
    venue: github.com/bitcoin/bitcoin
    type: official docs
    id: https://github.com/bitcoin/bitcoin/blob/master/doc/release-notes/release-notes-30.0.md
    url: https://github.com/bitcoin/bitcoin/blob/master/doc/release-notes/release-notes-30.0.md
    supports: datacarriersize default 100,000; multiple OP_RETURN outputs; 0.1 sat/vB relay floor.
  - key: core-releases
    authors: Bitcoin Core contributors
    year: 2026
    title: "Bitcoin Core GitHub releases (API listing)"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/releases
    url: https://github.com/bitcoin/bitcoin/releases
    supports: v30.0 published 2025-10-13; v32.1 2026-10-28; v31.3 and v30.5 2026-11-20.
  - key: core-tx-verify
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/consensus/tx_verify.cpp (IsFinalTx)"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/consensus/tx_verify.cpp
    url: https://github.com/bitcoin/bitcoin/blob/master/src/consensus/tx_verify.cpp
    supports: Exact nLockTime finality rule.
  - key: core-script-h
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/script/script.h"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/script/script.h
    url: https://github.com/bitcoin/bitcoin/blob/master/src/script/script.h
    supports: LOCKTIME_THRESHOLD = 500,000,000; MAX_SCRIPT_ELEMENT_SIZE 520.
  - key: core-chain-h
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/chain.h"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/chain.h
    url: https://github.com/bitcoin/bitcoin/blob/master/src/chain.h
    supports: MAX_FUTURE_BLOCK_TIME = 2 hours.
  - key: core-pow
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/pow.cpp"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/pow.cpp
    url: https://github.com/bitcoin/bitcoin/blob/master/src/pow.cpp
    supports: Retarget timespan clamp to 1/4 and 4x.
  - key: core-policy-h
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/policy/policy.h"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/policy/policy.h
    url: https://github.com/bitcoin/bitcoin/blob/master/src/policy/policy.h
    supports: MAX_OP_RETURN_RELAY = 400,000/4; DEFAULT_ACCEPT_DATACARRIER true.
  - key: core-consensus-h
    authors: Bitcoin Core contributors
    year: 2026
    title: "src/consensus/consensus.h"
    venue: github.com/bitcoin/bitcoin
    type: code
    id: https://github.com/bitcoin/bitcoin/blob/master/src/consensus/consensus.h
    url: https://github.com/bitcoin/bitcoin/blob/master/src/consensus/consensus.h
    supports: MAX_BLOCK_WEIGHT 4,000,000; COINBASE_MATURITY 100.
  - key: todd-opexpire-2023
    authors: Peter Todd
    year: 2023
    title: "OP_Expire and Coinbase-Like Behavior: Making HTLCs Safer by Letting Transactions Expire Safely"
    venue: bitcoin-dev mailing list (mirror.b10c.me archive), 2023-10-21
    type: essay/blog
    id: https://mirror.b10c.me/lists/bitcoindev/ZTMWrJ6DjxtslJBn@petertodd.org/raw
    url: https://mirror.b10c.me/lists/bitcoindev/ZTMWrJ6DjxtslJBn@petertodd.org/raw
    supports: Once-valid-always-valid design for reorg safety; expiry needs a soft fork.
  - key: optech-2026-08-07
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-08-07 (Input-triggered transaction expiry)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/08/07/
    url: https://bitcoinops.org/en/newsletters/2026/08/07/
    supports: OP_EXPIRE free-relay problem; proposed max-locktime introspection opcode.
  - key: optech-2026-11-06
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-11-06"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/11/06/
    url: https://bitcoinops.org/en/newsletters/2026/11/06/
    supports: BIP-54 status (regtest only, activation maybe 2H 2027 per Riard); co-signer policy draft BIP.
  - key: optech-2026-11-13
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-11-13"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/11/13/
    url: https://bitcoinops.org/en/newsletters/2026/11/13/
    supports: No activation news in mid-November 2026.
  - key: optech-2026-11-20
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-11-20"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/11/20/
    url: https://bitcoinops.org/en/newsletters/2026/11/20/
    supports: Rebindable signatures still need a soft fork; Wavelength mainnet alpha limited to 300,000 sats.
  - key: optech-2024-12-06
    authors: Bitcoin Optech
    year: 2024
    title: "Bitcoin Optech Newsletter, 2024-12-06"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2024/12/06/
    url: https://bitcoinops.org/en/newsletters/2024/12/06/
    supports: Timewarp fixes and timelock accuracy; Eclair BOLT12 support.
  - key: optech-2026-01-02
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-01-02 (CTV activation meeting)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/01/02/
    url: https://bitcoinops.org/en/newsletters/2026/01/02/
    supports: CTV activation meeting favored BIP9 conservative parameters.
  - key: optech-2026-10-02
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-10-02 (Comparing covenant proposals for vaults)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/10/02/
    url: https://bitcoinops.org/en/newsletters/2026/10/02/
    supports: Vault construction comparison conclusions.
  - key: optech-2025-07-04
    authors: Bitcoin Optech
    year: 2025
    title: "Bitcoin Optech Newsletter, 2025-07-04 (Open letter about CTV and CSFS)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2025/07/04/
    url: https://bitcoinops.org/en/newsletters/2025/07/04/
    supports: Open letter with 66 signatories asking for CTV+CSFS review.
  - key: optech-2025-12-05
    authors: Bitcoin Optech
    year: 2025
    title: "Bitcoin Optech Newsletter, 2025-12-05 (LNHANCE soft fork)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2025/12/05/
    url: https://bitcoinops.org/en/newsletters/2025/12/05/
    supports: LNHANCE composition.
  - key: optech-2026-09-04
    authors: Bitcoin Optech
    year: 2026
    title: "Bitcoin Optech Newsletter, 2026-09-04 (BIP448 and CSFS/CTV demos)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2026/09/04/
    url: https://bitcoinops.org/en/newsletters/2026/09/04/
    supports: BIP-448 implementations; Core patch without activation.
  - key: optech-2024-08-09
    authors: Bitcoin Optech
    year: 2024
    title: "Bitcoin Optech Newsletter, 2024-08-09 (Proposed BIP for scriptless threshold signatures)"
    venue: bitcoinops.org
    type: news
    id: https://bitcoinops.org/en/newsletters/2024/08/09/
    url: https://bitcoinops.org/en/newsletters/2024/08/09/
    supports: FROST BIP proposal announcement.
  - key: optech-timelocks-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Timelocks"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/timelocks/
    url: https://bitcoinops.org/en/topics/timelocks/
    supports: Index of timelock developments incl. longer relative timelock proposal and BIPs #2277.
  - key: optech-cleanup-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Consensus cleanup soft fork"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/consensus-cleanup-soft-fork/
    url: https://bitcoinops.org/en/topics/consensus-cleanup-soft-fork/
    supports: BIP-54 issue list and 2025-2026 history.
  - key: optech-covenants-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Covenants"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/covenants/
    url: https://bitcoinops.org/en/topics/covenants/
    supports: Covenant definition; 2026 items.
  - key: optech-vaults-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Vaults"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/vaults/
    url: https://bitcoinops.org/en/topics/vaults/
    supports: Vault definition.
  - key: optech-ctv-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: OP_CHECKTEMPLATEVERIFY"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/op_checktemplateverify/
    url: https://bitcoinops.org/en/topics/op_checktemplateverify/
    supports: 2025-2026 CTV history index.
  - key: optech-threshold-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Threshold signature"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/threshold-signature/
    url: https://bitcoinops.org/en/topics/threshold-signature/
    supports: ChillDKG, FROSTR, Frostsnap dates.
  - key: optech-ark-topic
    authors: Bitcoin Optech
    year: 2026
    title: "Topic: Ark protocol"
    venue: bitcoinops.org
    type: official docs
    id: https://bitcoinops.org/en/topics/ark/
    url: https://bitcoinops.org/en/topics/ark/
    supports: VTXO expiry semantics; operator co-signing trust.
  - key: liana-readme
    authors: Wizardsardine
    year: 2026
    title: "Liana README; GitHub releases"
    venue: github.com/wizardsardine/liana
    type: code
    id: https://github.com/wizardsardine/liana
    url: https://github.com/wizardsardine/liana
    supports: Primary and recovery paths after inactivity; v16.0 released 2026-11-03.
  - key: bitgo-policies
    authors: BitGo
    year: 2026
    title: "Policies Overview"
    venue: developers.bitgo.com
    type: company/vendor claim
    id: https://developers.bitgo.com/docs/policies-overview
    url: https://developers.bitgo.com/docs/policies-overview
    supports: Policy rule types; user+backup key bypass policies.
  - key: bitgo-whitelists
    authors: BitGo
    year: 2026
    title: "Create Whitelists"
    venue: developers.bitgo.com
    type: company/vendor claim
    id: https://developers.bitgo.com/docs/wallets-whitelists-create
    url: https://developers.bitgo.com/docs/wallets-whitelists-create
    supports: Whitelists lock 48 hours after creation; policies apply only with BitGo key.
  - key: bitkey-how
    authors: Bitkey (Block)
    year: 2026
    title: "How Bitkey works"
    venue: bitkey.world
    type: company/vendor claim
    id: https://bitkey.world/learning-hub/how-bitkey-works
    url: https://bitkey.world/learning-hub/how-bitkey-works
    supports: 2-of-3 with server key; daily limit feature; 7-day and 6-month delays.
  - key: nunchuk-blog
    authors: Nunchuk
    year: 2026
    title: "Open-source Bitcoin agents with bounded authority"
    venue: nunchuk.io
    type: company/vendor claim
    id: https://nunchuk.io/blog/bitcoin-agents
    url: https://nunchuk.io/blog/bitcoin-agents
    supports: Agent key + user key + policy co-signer; spending limits and signing delays (2026-04-08).
  - key: ll-agent-tools
    authors: Lightning Labs
    year: 2026
    title: "The Agents Are Here and They Want to Transact: Powering the AI Economy with Lightning"
    venue: lightning.engineering
    type: company/vendor claim
    id: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    url: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    supports: Remote signer isolation; five macaroon roles; --max-cost; node-level caps (2026-02-11).
  - key: alby-ai
    authors: Alby
    year: 2026
    title: "Alby for AI agents"
    venue: getalby.com
    type: company/vendor claim
    id: https://getalby.com/ai
    url: https://getalby.com/ai
    supports: Agent sub-wallets, budgets via NWC (page dated 2026-11-20).
  - key: babylon-staking-script
    authors: Babylon Labs
    year: 2026
    title: "Bitcoin Staking script (docs/staking-script.md)"
    venue: github.com/babylonlabs-io/babylon
    type: official docs
    id: https://github.com/babylonlabs-io/babylon/blob/main/docs/staking-script.md
    url: https://github.com/babylonlabs-io/babylon/blob/main/docs/staking-script.md
    supports: Staking/unbonding/slashing scripts; covenant committee; burn output; pre-signed slashing.
  - key: babylon-register
    authors: Babylon Labs
    year: 2026
    title: "Registering Bitcoin stakes (docs/register-bitcoin-stake.md)"
    venue: github.com/babylonlabs-io/babylon
    type: official docs
    id: https://github.com/babylonlabs-io/babylon/blob/main/docs/register-bitcoin-stake.md
    url: https://github.com/babylonlabs-io/babylon/blob/main/docs/register-bitcoin-stake.md
    supports: Staking parameter list.
  - key: fp-slashing-protection
    authors: Babylon Labs
    year: 2026
    title: "Slashing Protection on Finality Provider"
    venue: github.com/babylonlabs-io/finality-provider
    type: official docs
    id: https://github.com/babylonlabs-io/finality-provider/blob/main/docs/slashing-protection.md
    url: https://github.com/babylonlabs-io/finality-provider/blob/main/docs/slashing-protection.md
    supports: Reusing committed randomness on conflicting blocks exposes the EOTS private key.
  - key: fp-commit-pub-rand
    authors: Babylon Labs
    year: 2026
    title: "Public Randomness Commit Specification"
    venue: github.com/babylonlabs-io/finality-provider
    type: official docs
    id: https://github.com/babylonlabs-io/finality-provider/blob/main/docs/commit-pub-rand.md
    url: https://github.com/babylonlabs-io/finality-provider/blob/main/docs/commit-pub-rand.md
    supports: Per-height public randomness committed via Merkle root.
  - key: tas2023
    authors: Ertem Nusret Tas, David Tse, Fangyu Gai, Sreeram Kannan, Mohammad Ali Maddah-Ali, Fisher Yu
    year: 2023
    title: "Bitcoin-Enhanced Proof-of-Stake Security: Possibilities and Impossibilities"
    venue: IEEE Symposium on Security and Privacy 2023 (per arXiv comments)
    type: peer-reviewed
    id: arXiv:2207.08392
    url: https://arxiv.org/abs/2207.08392
    supports: Babylon checkpointing; <5 hour withdrawal delay, <10K USD per annum; no EOTS content.
  - key: jm-fidelity
    authors: JoinMarket developers
    year: 2026
    title: "Fidelity bonds (docs/fidelity-bonds.md)"
    venue: github.com/JoinMarket-Org/joinmarket-clientserver
    type: official docs
    id: https://github.com/JoinMarket-Org/joinmarket-clientserver/blob/master/docs/fidelity-bonds.md
    url: https://github.com/JoinMarket-Org/joinmarket-clientserver/blob/master/docs/fidelity-bonds.md
    supports: Bond value formula, exponent 1.3, 1.5% rate, hodlers buy bonds nearly free.
  - key: bolt03
    authors: Lightning BOLT contributors
    year: 2026
    title: "BOLT #3: Bitcoin Transaction and Script Formats"
    venue: github.com/lightning/bolts
    type: standard/BIP/RFC/spec
    id: https://github.com/lightning/bolts/blob/master/03-transactions.md
    url: https://github.com/lightning/bolts/blob/master/03-transactions.md
    supports: to_local script with revocation key and CSV delay.
  - key: bolt05
    authors: Lightning BOLT contributors
    year: 2026
    title: "BOLT #5: Recommendations for On-chain Transaction Handling"
    venue: github.com/lightning/bolts
    type: standard/BIP/RFC/spec
    id: https://github.com/lightning/bolts/blob/master/05-onchain.md
    url: https://github.com/lightning/bolts/blob/master/05-onchain.md
    supports: Revoked close lets counterparty claim all funds; trustless if properly handled.
  - key: bolt12
    authors: Lightning BOLT contributors
    year: 2026
    title: "BOLT #12: Negotiation Protocol for Lightning Payments"
    venue: github.com/lightning/bolts
    type: standard/BIP/RFC/spec
    id: https://github.com/lightning/bolts/blob/master/12-offer-encoding.md
    url: https://github.com/lightning/bolts/blob/master/12-offer-encoding.md
    supports: offer_absolute_expiry, offer_quantity_max, payer proofs.
  - key: dlc-dryja2017
    authors: Thaddeus Dryja
    year: 2017
    title: "Discreet Log Contracts"
    venue: MIT Digital Currency Initiative (self-published PDF)
    type: preprint
    id: https://adiabat.github.io/dlc.pdf
    url: https://adiabat.github.io/dlc.pdf
    supports: Oracle equivocation reveals key; one-time cheat as counterparty; refund transaction.
  - key: dlcspecs-readme
    authors: DLC spec contributors
    year: 2026
    title: "Discreet Log Contract specification README"
    venue: github.com/discreetlogcontracts/dlcspecs
    type: standard/BIP/RFC/spec
    id: https://github.com/discreetlogcontracts/dlcspecs
    url: https://github.com/discreetlogcontracts/dlcspecs
    supports: Specs work-in-progress; implementation list.
  - key: bitvm2023
    authors: Robin Linus
    year: 2023
    title: "BitVM: Compute Anything on Bitcoin"
    venue: bitvm.org
    type: preprint
    id: https://bitvm.org/bitvm.pdf
    url: https://bitvm.org/bitvm.pdf
    supports: No consensus change; optimistic verification; two-party limitation; pre-signed challenge transactions.
  - key: bitvm2-bridge
    authors: Robin Linus, Lukas Aumayr, Alexei Zamyatin, Andrea Pelosi, Zeta Avarikioti, Matteo Maffei
    year: 2024
    title: "BitVM2: Bridging Bitcoin to Second Layers"
    venue: bitvm.org
    type: preprint
    id: https://bitvm.org/bitvm_bridge.pdf
    url: https://bitvm.org/bitvm_bridge.pdf
    supports: 1-of-n setup honesty; rational operator; permissionless challenge; committee unnecessary with covenants.
  - key: bitvm2-eprint
    authors: Robin Linus, Lukas Aumayr, Zeta Avarikioti, Matteo Maffei, Andrea Pelosi, Orfeas Thyfronitis Litos, Christos Stefo, David Tse, Alexei Zamyatin
    year: 2025
    title: "Bridging Bitcoin to Second Layers via BitVM2"
    venue: Cryptology ePrint Archive 2025/1158
    type: preprint
    id: https://eprint.iacr.org/2025/1158
    url: https://eprint.iacr.org/2025/1158
    supports: Mainnet challenge verification executed (authors' claim); revised 2026-03-04.
  - key: citrea-docs
    authors: Citrea (Chainway Labs)
    year: 2026
    title: "Citrea documentation (llms-full export): Clementine"
    venue: docs.citrea.xyz
    type: company/vendor claim
    id: https://docs.citrea.xyz/llms-full.txt
    url: https://docs.citrea.xyz/llms-full.txt
    supports: Clementine 1-of-N claim, mainnet deployment, signers pre-sign spend rules, watchtowers.
  - key: moser2016
    authors: Malte Moser, Ittay Eyal, Emin Gun Sirer
    year: 2016
    title: "Bitcoin Covenants"
    venue: Financial Cryptography and Data Security 2016 Workshops, LNCS, pp. 126-141
    type: peer-reviewed
    id: "doi:10.1007/978-3-662-53357-4_9"
    url: https://maltemoeser.de/paper/covenants.pdf
    supports: CheckOutputVerify; vaults with recovery key; vaults not implementable with CLTV/locktime; poison transactions.
  - key: revault-intro
    authors: Revault developers
    year: 2021
    title: "Practical Revault: Introduction"
    venue: github.com/revault/practical-revault
    type: standard/BIP/RFC/spec
    id: https://github.com/revault/practical-revault/blob/master/introduction.md
    url: https://github.com/revault/practical-revault/blob/master/introduction.md
    supports: Pre-signed Emergency/Unvault/Cancel; managers delayed; watchtowers; once-only co-signer.
  - key: revault-tx
    authors: Revault developers
    year: 2021
    title: "Practical Revault: Transactions"
    venue: github.com/revault/practical-revault
    type: standard/BIP/RFC/spec
    id: https://github.com/revault/practical-revault/blob/master/transactions.md
    url: https://github.com/revault/practical-revault/blob/master/transactions.md
    supports: Deposit and unvault descriptors.
  - key: haber1991
    authors: Stuart Haber, W. Scott Stornetta
    year: 1991
    title: "How to time-stamp a digital document"
    venue: Journal of Cryptology 3, 99-111
    type: peer-reviewed
    id: "doi:10.1007/BF00196791"
    url: https://doi.org/10.1007/BF00196791
    supports: Bibliographic facts only (opened Crossref metadata, not full text).
  - key: todd-ots-2016
    authors: Peter Todd
    year: 2016
    title: "OpenTimestamps: Scalable, Trust-Minimized, Distributed Timestamping with Bitcoin"
    venue: petertodd.org
    type: essay/blog
    id: https://petertodd.org/2016/opentimestamps-announcement
    url: https://petertodd.org/2016/opentimestamps-announcement
    supports: Aggregation; calendars as point of failure; nTime accuracy; timestamps do not prove uniqueness.
  - key: ots-client-readme
    authors: OpenTimestamps developers
    year: 2026
    title: "opentimestamps-client README"
    venue: github.com/opentimestamps/opentimestamps-client
    type: code
    id: https://github.com/opentimestamps/opentimestamps-client
    url: https://github.com/opentimestamps/opentimestamps-client
    supports: Verification needs a Bitcoin node; confirmation takes a few hours.
  - key: todd-seals-2016
    authors: Peter Todd
    year: 2016
    title: "Preventing Consensus Fraud with Commitments and Single-Use-Seals"
    venue: petertodd.org
    type: essay/blog
    id: https://petertodd.org/2016/commitments-and-single-use-seals
    url: https://petertodd.org/2016/commitments-and-single-use-seals
    supports: Single-use seal definition; txout-based seals with OP_RETURN close; chained seals.
  - key: taproot-assets-docs
    authors: Lightning Labs
    year: 2026
    title: "Taproot Assets Protocol"
    venue: docs.lightning.engineering
    type: official docs
    id: https://docs.lightning.engineering/the-lightning-network/taproot-assets/taproot-assets-protocol
    url: https://docs.lightning.engineering/the-lightning-network/taproot-assets/taproot-assets-protocol
    supports: Asset tree root in tapscript; Universes unprivileged; invalidation on uncommitted spend.
  - key: rgb-docs
    authors: RGB documentation maintainers
    year: 2026
    title: "RGB documentation (introduction)"
    venue: docs.rgb.info
    type: official docs
    id: https://docs.rgb.info/
    url: https://docs.rgb.info/
    supports: RGB purpose; v0.12 labeled unfinished rewrite proposal.
  - key: theblock-bip110
    authors: The Block
    year: 2026
    title: "Bitcoin's BIP-110 supporters split onto minority chain as main network pulls ahead"
    venue: The Block
    type: news
    id: https://www.theblock.co/news/ecosystems/2026-08-08-bitcoins-bip-110-supporters-split-onto-minority-chain-as-main-network-pulls-ahead-411213
    url: https://www.theblock.co/news/ecosystems/2026-08-08-bitcoins-bip-110-supporters-split-onto-minority-chain-as-main-network-pulls-ahead-411213
    supports: Split at 961,632; block counts; 2.53% signaling; v30 background; BIP-444 to BIP-110.
  - key: nip47
    authors: Nostr NIP contributors
    year: 2026
    title: "NIP-47: Nostr Wallet Connect"
    venue: github.com/nostr-protocol/nips
    type: standard/BIP/RFC/spec
    id: https://github.com/nostr-protocol/nips/blob/master/47.md
    url: https://github.com/nostr-protocol/nips/blob/master/47.md
    supports: Revocable per-connection keys with budgets; QUOTA_EXCEEDED; simplification 2026-08-01.
  - key: nwc-08
    authors: NWC contributors
    year: 2026
    title: "NWC-08: Client-Initiated Connection Creation"
    venue: github.com/nostr-wallet-connect/nwc
    type: standard/BIP/RFC/spec
    id: https://github.com/nostr-wallet-connect/nwc/blob/main/08.md
    url: https://github.com/nostr-wallet-connect/nwc/blob/main/08.md
    supports: expires_at, max_amount, renewal_period, isolated; MUST enforce caps.
  - key: nwc-13
    authors: NWC contributors
    year: 2026
    title: "NWC-13: Connection Budgets"
    venue: github.com/nostr-wallet-connect/nwc
    type: standard/BIP/RFC/spec
    id: https://github.com/nostr-wallet-connect/nwc/blob/main/13.md
    url: https://github.com/nostr-wallet-connect/nwc/blob/main/13.md
    supports: get_budget fields and semantics.
  - key: l402-readme
    authors: Lightning Labs
    year: 2026
    title: "L402: Lightning HTTP 402 Protocol (README)"
    venue: github.com/lightninglabs/L402
    type: standard/BIP/RFC/spec
    id: https://github.com/lightninglabs/L402
    url: https://github.com/lightninglabs/L402
    supports: 402 flow; macaroon commits to payment hash.
  - key: l402-macaroon
    authors: Lightning Labs
    year: 2026
    title: "L402 macaroon specification"
    venue: github.com/lightninglabs/L402
    type: standard/BIP/RFC/spec
    id: https://github.com/lightninglabs/L402/blob/master/macaroon-spec.md
    url: https://github.com/lightninglabs/L402/blob/master/macaroon-spec.md
    supports: HMAC caveat chaining; attenuation only; valid_until; revoke and re-mint.
  - key: l402-agent
    authors: Lightning Labs
    year: 2026
    title: "L402 Agent Specification"
    venue: github.com/lightninglabs/L402
    type: standard/BIP/RFC/spec
    id: https://github.com/lightninglabs/L402/blob/master/agent-spec.md
    url: https://github.com/lightninglabs/L402/blob/master/agent-spec.md
    supports: Caveats MUST restrict further, never widen.
  - key: nut10
    authors: Cashu contributors
    year: 2026
    title: "NUT-10: Spending conditions"
    venue: github.com/cashubtc/nuts
    type: standard/BIP/RFC/spec
    id: https://github.com/cashubtc/nuts/blob/main/10.md
    url: https://github.com/cashubtc/nuts/blob/main/10.md
    supports: Structured secret format checked by mint.
  - key: nut11
    authors: Cashu contributors
    year: 2026
    title: "NUT-11: Pay-to-Pubkey (P2PK)"
    venue: github.com/cashubtc/nuts
    type: standard/BIP/RFC/spec
    id: https://github.com/cashubtc/nuts/blob/main/11.md
    url: https://github.com/cashubtc/nuts/blob/main/11.md
    supports: sigflag, multisig, locktime by mint clock, refund keys, expiry behavior.
  - key: nut14
    authors: Cashu contributors
    year: 2026
    title: "NUT-14: Hashed Timelock Contracts"
    venue: github.com/cashubtc/nuts
    type: standard/BIP/RFC/spec
    id: https://github.com/cashubtc/nuts/blob/main/14.md
    url: https://github.com/cashubtc/nuts/blob/main/14.md
    supports: HTLC hash lock with receiver and timelocked sender refund paths.
  - key: arkade-docs
    authors: Ark Labs
    year: 2026
    title: "VTXO lifecycle and liveness (Arkade docs)"
    venue: docs.arkadeos.com
    type: company/vendor claim
    id: https://docs.arkadeos.com/learn/core-concepts/vtxo-lifecycle-and-liveness.md
    url: https://docs.arkadeos.com/learn/core-concepts/vtxo-lifecycle-and-liveness.md
    supports: Single operator as cosigner and script emulator; renewal and unilateral exit.
  - key: spark-trust
    authors: Spark (Lightspark)
    year: 2026
    title: "Trust Model"
    venue: docs.spark.money
    type: company/vendor claim
    id: https://docs.spark.money/learn/trust-model
    url: https://docs.spark.money/learn/trust-model
    supports: Moment-in-time 1-of-n trust via operator key deletion.
  - key: ietf-fassbender-07
    authors: J. Fassbender
    year: 2026
    title: "Bitcoin-Anchored Temporal Proof for Transparency Services (draft-fassbender-scitt-time-anchor-07)"
    venue: IETF Internet-Draft (Informational), 2026-09-24
    type: standard/BIP/RFC/spec
    id: https://datatracker.ietf.org/doc/draft-fassbender-scitt-time-anchor/07/
    url: https://www.ietf.org/archive/id/draft-fassbender-scitt-time-anchor-07.txt
    supports: AI model weights anchoring via OTS; existed-no-later-than height H; equivocation detection.
  - key: aesp-2026
    authors: Jian Sheng Wang
    year: 2026
    title: "AESP: A Human-Sovereign Economic Protocol for AI Agents with Privacy-Preserving Settlement"
    venue: arXiv
    type: preprint
    id: arXiv:2603.00318
    url: https://arxiv.org/abs/2603.00318
    supports: Policy engine with human-in-the-loop tiers for agent payments (EIP-712, not Bitcoin).
  - key: agentcity-2026
    authors: Anbang Ruan, Xing Zhang
    year: 2026
    title: "AgentCity: Constitutional Governance for Autonomous Agent Economies via Separation of Power"
    venue: arXiv
    type: preprint
    id: arXiv:2604.07007
    url: https://arxiv.org/abs/2604.07007
    supports: Ownership chain binding every agent to a responsible human principal (EVM L2).
  - key: hbhc-2026
    authors: Saurabh Deochake
    year: 2026
    title: "Heartbeat-Bound Hierarchical Credentials: Cryptographic Revocation for AI Agent Swarms"
    venue: arXiv
    type: preprint
    id: arXiv:2605.20704
    url: https://arxiv.org/abs/2605.20704
    supports: Agent credentials that lapse without parent heartbeats (wall clock, no Bitcoin).
  - key: chaintip-devto
    authors: Zeke (zekebuilds)
    year: 2026
    title: "Chaintip freshness: cert-signed identity scores that age with the chain"
    venue: dev.to
    type: essay/blog
    id: https://dev.to/zekebuilds/chaintip-freshness-cert-signed-identity-scores-that-age-with-the-chain-1m2h
    url: https://dev.to/zekebuilds/chaintip-freshness-cert-signed-identity-scores-that-age-with-the-chain-1m2h
    supports: Signed scores rejected after N blocks past the signed tip (default 6); year not shown on page.
  - key: petrie2024
    authors: James Petrie
    year: 2024
    title: "Near-Term Enforcement of AI Chip Export Controls Using A Firmware-Based Design for Offline Licensing"
    venue: arXiv
    type: preprint
    id: arXiv:2404.18308
    url: https://arxiv.org/abs/2404.18308
    supports: Offline licensing prior work for N9; full text has no blockchain or Bitcoin mention.
  - key: flexheg2025
    authors: James Petrie, Onni Aarne, Nora Ammann, David Dalrymple
    year: 2025
    title: "Flexible Hardware-Enabled Guarantees for AI Compute"
    venue: arXiv
    type: preprint
    id: arXiv:2506.15093
    url: https://arxiv.org/abs/2506.15093
    supports: Hardware-enabled guarantees prior work; full text has no blockchain or Bitcoin mention.
```
