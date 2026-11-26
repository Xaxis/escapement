# OrangeCheck verbs and Blocklore edition seals: what they actually do (local-source audit, 2026-11-26)

> Public version of a local audit. Claims that rested only on private repositories (the web apps, the
> workspace's internal research and an infrastructure incident report) were removed; paths name the
> public repositories github.com/orangecheck/* and github.com/Xaxis/blocklore.space.

Scope: the six OrangeCheck verbs (Attest, Agent, Pledge, Stamp, Lock, Vote) and Blocklore's edition seals, read from their source. Citation form: `path:line (spec|code|doc)`. Paths are relative to github.com/orangecheck unless they start with `blocklore.space/` (= github.com/Xaxis/blocklore.space). "Live" below means deployed code exists; it does not mean used (see adoption note in the cross-cutting section).

## Cross-cutting: family rules that shape every verb

### Takeaway
Every verb is an off-chain, content-addressed, BIP-322-signed envelope published to Nostr. Bitcoin is used as (1) an identity namespace and signature scheme, (2) a read-only public UTXO state oracle (balance, coin age), and (3) a clock (block headers, OpenTimestamps). By an explicit family invariant, no verb moves, locks, escrows or slashes funds.

### Cited Findings
- Invariant 2 "No custody. Funds never move. No deposits, no escrow, no custody of user keys, no wallet-inside-the-app." (ochk.app is the one stated, temporary exception.)
- "All six verbs are live" (deployed sites per verb).. Spec status differs: Attest "Stable (Normative)" `oc-attest-protocol/SPEC.md:3`; Agent "Stable" `oc-agent-protocol/SPEC.md:3`; Pledge "Draft" (dispute rules changed 2026-10-29) `oc-pledge-protocol/SPEC.md:3`; Stamp "Stable" `oc-stamp-protocol/SPEC.md:3`; Lock "Stable" `oc-lock-protocol/SPEC.md:3`; Vote "v0, still changing" `oc-vote-protocol/SPEC.md:3` (spec).
- Nostr kinds (authoritative table): 30078 attestation / Lock device record / Pledge (`oc-pledge:` d-tags); 30080-30082 Vote poll/ballot/reveal; 30083 Stamp co-claimed with Agent delegation; 30084 Agent action; 30085 Agent revocation; 30086 Agent sub-delegation; 30112 Chat seal / block-height anchor (draft). `KINDS.md:9-26` (doc)

### Inferences
- For Escapement, OrangeCheck is an evidence and verification layer, not an enforcement layer: it can prove who authorized what, when (to block precision), and how much stake was visible, but it never makes a misbehaving party lose sats. Anything in N1 to N11 that requires sats to be locked or taken must come from new script-level design, and would break the family's "no custody" invariant if built inside OrangeCheck.

### Gaps
- No current (post-July 2026) usage count per verb was found in local files.

## OC Pledge (commitment): bond, address rule, states

### Takeaway
A pledge is a BIP-322-signed forward commitment with a machine-checkable resolution predicate and a mandatory bond that is only a reference to an OrangeCheck attestation of the swearer's own address. The bond is never locked, timelocked, escrowed or slashable; nobody can take it. "Enforcement" is a permanent public `broken` record plus a live re-check that the attested coins are still unspent. States are a pure function of envelopes, the verifier's clock and block-header timestamps.

### Cited Findings
Format and signing
- Canonical message (line-oriented, LF, no trailing LF), first line `oc-pledge/v1` as domain separator; fields swearer, proposition, resolution{mechanism,query}, resolves_at{time|block}, expires_at (ISO only), bond{attestation_id,min_sats,min_days}, counterparty, dispute{mechanism,params}, `remediation: breach_recorded`, sworn_at, nonce (16 random bytes). `oc-pledge-protocol/SPEC.md:50-77` (spec)
- `pledge_id := H(canonical_message_bytes)` (SHA-256); the id is also the Nostr d-tag suffix `oc-pledge:<id>` on kind 30078. `oc-pledge-protocol/SPEC.md:89-99`, `:737-740` (spec)
- Signature: `sig.value := BIP322(swearer.address, hex(pledge_id))`; addresses P2WPKH, P2TR or P2PKH mainnet. `oc-pledge-protocol/SPEC.md:245-251`, `:36` (spec). Reference node example verifies P2PKH, P2SH-P2WPKH, P2WPKH and P2TR. `oc-pledge-examples/node-verify/README.md:62` (doc)
- `remediation` is fixed to `breach_recorded`: "There is no `slashing` value, no `payout` value, no `escrow_release` value." `oc-pledge-protocol/SPEC.md:87` (spec). Refused registry values: `slashing`, `auto_payout`, `escrow_release` (all "Requires custody"), `revocation`. `oc-pledge-protocol/REGISTRY.md:75-82` (spec)
- Seven resolution mechanisms: `chain_state` (block hash prefix, tx confirmations, address balance, `AT block(N)`), `counterparty_signs`, `nostr_event_exists`, `stamp_published`, `http_get_hash`, `dns_record`, `vote_resolves`; `self_proof` refused. `oc-pledge-protocol/SPEC.md:158-241` (spec)

Bond: what it is
- "A pledge MUST include a bond referencing an OrangeCheck attestation, with two minimum thresholds: `min_sats` and `min_days`. The reference is self-declared and re-verifiable ... The protocol never holds the bonded sats; enforcement is by public exposure, not slashing." `oc-pledge-protocol/SPEC.md:40` (spec)
- "The bond is a commitment, not custody. A swearer who spends the bonded UTXO before resolution invalidates the bond ... No protocol actor can seize the bonded sats. This is a deliberate refusal of slashing-based designs." `oc-pledge-protocol/SPEC.md:42` (spec)
- WHY H7 "There is no slashing primitive, period": slashing would need custody or a covenant, "makes the protocol an actor with state, breaks offline-verifiability, and adds a censorship surface"; refused: slashing via HTLC, covenant, multisig arbiter. `oc-pledge-protocol/WHY.md:78-84` (doc). Threat model: "Bond seizure ... The protocol cannot transfer or burn the bonded sats." `oc-pledge-protocol/SECURITY.md:57` (doc)
- Stated rationale for Bitcoin: "`sats_bonded x days_unspent` is the only credibly-neutral stake oracle"; the cost is opportunity cost of "I won't move this UTXO". `oc-pledge-protocol/WHY.md:30-36` (doc)

Bond: how "from the principal's own address" is checked
- Spec algorithm: resolve attestation by id; `if attestation.address != pledge.swearer: return E_BOND_ADDRESS_MISMATCH`; then spent, sats, days checks. `oc-pledge-protocol/SPEC.md:575-585` (spec). Field rule: `bond.attestation_id` "SHOULD be the SHA-256 of an OrangeCheck attestation canonical message signed by `swearer.address`". `oc-pledge-protocol/SPEC.md:269` (spec)
- Code does an exact string comparison of the attestation's signing address against `pledge.swearer.address`. `oc-packages/pledge-core/src/bond.ts:65-71` (code). Address spelling is normalized by rule (bech32 lowercase only) precisely so that exact-string comparisons hold. `oc-pledge-protocol/SPEC.md:38` (spec)
- So "own funds" means: the coins counted are the confirmed UTXOs at the same address that signed the attestation and the pledge. `days_unspent(now, cover)`: sort the attested address's confirmed unspent outputs oldest first by (block_height, txid, vout), take until sum >= `min_sats`, count whole days since the youngest one taken confirmed. `oc-pledge-protocol/SPEC.md:592` (spec)
- The chain lookup is caller-injected; the SDK ships no Bitcoin client ("Esplora, mempool.space, bitcoind RPC, oc-attest sdk"). `oc-packages/pledge-core/src/bond.ts:1-6` (code), `oc-packages/pledge-core/src/types.ts:568-581` (code)
- Bond and state are decoupled in the spec and code: "the protocol does not seize sats and does not auto-classify spent-bond as `broken`". `oc-pledge-protocol/SPEC.md:596` (spec); `oc-packages/pledge-core/src/state.ts` contains no bond reference (grep, code). Contradicted by `oc-pledge-protocol/LIFECYCLE.md:42-43`, which says a spent bond makes the pledge "resolve `broken` regardless" with `E_INSUFFICIENT_BOND` (an error code that exists nowhere else). SPEC and code are live; LIFECYCLE is stale.
- Accepted residual: "a swearer who spends mid-pledge AND posts a kept outcome ... gets a `kept` ledger entry alongside an invalid bond." `oc-pledge-protocol/SECURITY.md:103` (doc)
- No exclusivity: nothing in the spec or `verifyBond` prevents one attestation (one set of coins) from backing any number of pledges and delegations at once (inference from the algorithm at `oc-pledge-protocol/SPEC.md:575-585` and `oc-packages/pledge-core/src/bond.ts:37-101`, which take a single pledge and never consult other pledges).

States and block headers
- States: `pending`, `resolvable`, `kept`, `broken`, `disputed`, `expired_unresolved`; transition pseudocode is a pure function of (pledge, outcomes, abandonment, now, chain). `oc-pledge-protocol/SPEC.md:372-418` (spec)
- `resolves_at_normalized` = the `time:` value, or "the wall-clock timestamp of the Bitcoin block at `resolves_at.block` (or, if not yet mined, +infinity)". `oc-pledge-protocol/SPEC.md:383` (spec). Code: uses `chain.blockTimes[block]` if given, else the tip time once `tip_height >= block`, else pending. `oc-packages/pledge-core/src/state.ts:19-22`, `:126-140` (code)
- The offline example reads the block timestamp from bytes 68-71 of a raw 80-byte header supplied by the caller; it trusts the header source (two headers fetched from mempool.space and blockstream.info) and does not validate proof-of-work or header linkage; "To trust no one, take headers from your own node". `oc-pledge-examples/node-verify/README.md:50`, `:63`, `:71-75` (doc). It does not check the bond. `oc-pledge-examples/node-verify/README.md:65` (doc)
- `expires_at` is ISO time only (no block form), so expiry rides on the verifier's wall clock. `oc-pledge-protocol/SPEC.md:63`, `:268` (spec)
- Abandonment (swearer-signed `oc-pledge-abandonment/v1`) counts as `broken`; "There is no honorable-exit ledger state"; agents may not abandon. `oc-pledge-protocol/SPEC.md:433`, `:480`, `:542` (spec)
- Disputes: a swearer can always turn a counterparty `broken` into `disputed` or `expired_unresolved` unless a dispute mechanism is named, because every outcome date is the signer's claim. `oc-pledge-protocol/SPEC.md:427`, `oc-pledge-protocol/SECURITY.md:101` (spec, doc). With a named mechanism the pledge "stays `disputed`" (`oc-pledge-protocol/SPEC.md:425`); the code returns `'disputed'` and never consults `vote_resolves` or `named_oracle` to exit it. `oc-packages/pledge-core/src/state.ts:95-99` (code). `named_oracle` (a Bitcoin address whose BIP-322 outcome resolves the dispute) exists only in the registry. `oc-pledge-protocol/REGISTRY.md:43`, `:51-57` (spec)
- Time anchoring of pledges is absent: "a v1 pledge carries nothing that anchors `sworn_at`" and a backdated `resolved_at` "cannot be told from a true one without an anchored time". `oc-pledge-protocol/SPEC.md:540`, `oc-pledge-protocol/SECURITY.md:145` (spec, doc)

Agent-signed pledges
- An agent with delegation scope `pledge:create(max_bond_sats<=N, mechanism=..., counterparty=...)` may sign; the pledge counts in the principal's ledger; `agent_address` must differ from `swearer.address`; the delegation must be in force at verification time (not at the agent-chosen `sworn_at`). `oc-pledge-protocol/SPEC.md:520-556` (spec). Code check `bond.min_sats <= max_bond_sats`. `oc-packages/pledge-core/src/delegation.ts:135-150` (code)
- `max_bond_sats` caps the size of the bond the agent may cite, not any sats the agent can spend (inference from `oc-pledge-protocol/SPEC.md:556`).

Implementation status
- pledge-core 3.7.0 on main (npm serves 3.6.0); SDKs cover SPEC §9.1 steps 1-7 and 9; step 8 (re-evaluating deterministic mechanisms against chain/Nostr/HTTP/DNS) is consumer-side and the hosted site does not run it. `oc-pledge-protocol/SECURITY.md:18-31` (doc)
- Example in the corpus of a self-imposed "timelock" done socially: vector v61 proposition "I will not spend the bonded UTXO before block 920000." `oc-pledge-examples/node-verify/README.md:17` (doc)

### Inferences
- For N2 (bond from principal's own funds, slashed on misbehavior): OC Pledge implements the first half (attribution and "own address" check by exact address match) and explicitly refuses the second half. Liability lands on the human principal's address reputationally (`oc-pledge-protocol/WHY.md:118-124`), never financially.
- The bond is a balance-plus-age read of an address, so it is (a) reusable across unlimited commitments, (b) withdrawable at any moment with only a reputational cost, (c) observable only through whatever Esplora/indexer the verifier trusts.
- The block-height deadline is the strongest Bitcoin property used here, yet header validation is left to the integrator.

### Gaps
- No implementation of dispute adjudication (`named_oracle`, `vote_resolves`) in the state machine was found; whether oc-pledge-web shows anything beyond `disputed` was not checked.
- No measured count of live pledges.

## OC Agent (authority): delegation, scopes, caps, revocation

### Takeaway
OC Agent is a capability-token scheme on Bitcoin keys: a principal BIP-322-signs a delegation (agent address, sorted scope strings, wall-clock window of at most 365 days, optional bond reference); the agent BIP-322-signs each action envelope citing it; revocations are signed envelopes on Nostr. A verifier (the relying party) checks signatures, window, freshness (120 s), single use, scope containment and revocation absence at a relay read floor. Caps such as `ln:send(max_sats<=1000)` are per-action upper bounds checked by the relying party; there is no cumulative budget, no block-height bound, no on-chain enforcement, and the optional bond is not checked by the reference code.

### Cited Findings
Delegation format
- Canonical message: `oc-agent:delegation:v1`, principal, agent, scopes (sorted, comma-joined), `bond_sats`, `bond_attestation` (64-hex or `none`), issued_at, expires_at, nonce; `id := H(canonical)`; `sig.value := BIP322(principal.address, hex(id))`. `oc-agent-protocol/SPEC.md:73-95`, `:161-167` (spec)
- Window rule: `expires_at > issued_at` and `expires_at - issued_at <= 365 days`. `oc-agent-protocol/SPEC.md:153` (spec). Times are ISO 8601 UTC; there is no block-height bound anywhere in the delegation (grep for height/block in SPEC returns only the OTS fields at `oc-agent-protocol/SPEC.md:225-226`) (spec).
- Identities: mainnet P2WPKH, P2SH-P2WPKH, P2TR, P2PKH. `oc-agent-protocol/SPEC.md:33` (spec). The verifier used by agent-cli, `@orangecheck/bip322`, "checks P2TR on the key path only and does not check P2WSH". `oc-agent-protocol/SECURITY.md:109` (doc). So a P2WSH or script-path (multisig) address cannot act as a principal or agent in practice.

Scopes and "caps"
- Grammar `product:verb(key op value, ...)`, ops `= != < <= > >= *`. `oc-agent-protocol/SPEC.md:285-299` (spec)
- Registered scopes include `ln:send(max_sats<=1000, max_fee_sats<=10)`, `http:request(origin, method, max_rps)`, `mcp:invoke(server, tool, max_invocations)`, `pledge:create(max_bond_sats<=N)`, and tool scopes for Anthropic, OpenAI, Vercel AI, LangGraph. `oc-agent-protocol/SPEC.md:325-340`, registry `:370-386` (spec)
- Sub-scope relation: for ordered ops the exercised scope's implied range must be a subset of the granted range. Example: granted `ln:send(max_sats<=1000)` admits exercised `ln:send(max_sats=500, node=...)`. `oc-agent-protocol/SPEC.md:343-358` (spec)
- Per-action, not cumulative: "A delegation granting `ln:send(max_sats<=1000)` admits any payment under 1000 sats within the window." `oc-agent-protocol/SECURITY.md:35` (doc). The live dashboard labels it "Sats per call (cap)" and counts only actions in local storage, noting a relay list "is never complete"., `:104-107` (code). No code in agent-core, agent-mcp or agent-signer implements a cumulative budget (grep for budget/cumulative/max_invocations found only the key registry at `oc-packages/agent-core/src/scope.ts:47-67`) (code).
- Content-bound keys: only `stamp:sign` mime/max_bytes/content_hash_prefix are derived from the signed content; for every other scope (ln:send, lock:seal, mcp:invoke...) the real recipient, amount or tool sits inside content the action commits to only by hash, so the product's own verifier must check it. `oc-agent-protocol/SPEC.md:438-446`, `:395` (spec)

Verifier checks before honouring an action (live verification)
- Delegation: version, shape and 365-day window, canonical id, scope grammar, BIP-322 signature, `issued_at <= now < expires_at`, revocation check. `oc-agent-protocol/SPEC.md:410-420` (spec)
- Action: base OC Stamp checks; `delegation_id` binding; signer equals delegation agent; `issued_at <= signed_at < expires_at`; freshness `|now - signed_at|` within verifier bound, 120 s RECOMMENDED; single use (keep accepted ids); scope containment; content-bound keys. `oc-agent-protocol/SPEC.md:422-446` (spec). Code default `DEFAULT_MAX_SKEW_MS = 120_000` and an in-memory, per-process `createReplayGuard`. `oc-packages/agent-core/src/verify.ts:55`, `:686-708` (code)
- Bond (optional, "If caller policy requires a bond"): presence, `bond.sats >= threshold`, re-resolve the attestation. `oc-agent-protocol/SPEC.md:448-454` (spec). Docs vs code: agent-core 2.10.0 only shape-checks `bond` (`oc-packages/agent-core/src/verify.ts:858-861`); `E_NO_BOND`/`E_BOND_UNMET`/`E_BOND_UNVERIFIED` are declared (`oc-packages/agent-core/src/types.ts:246-248`) but no code path emits them (grep, code). The reference site says "the sats and attestation id are what the principal declared ... this page does not" re-resolve.. The spec requires the attestation to be "signed by `principal.address`" (`oc-agent-protocol/SPEC.md:152`) but nothing in agent-core checks it.
- Bond semantics: "The bond is not escrow. OC Agent does not enforce slashing on-chain; the sats remain in the principal's wallet and remain spendable." `oc-agent-protocol/SPEC.md:910-914` (spec); "there is no smart contract that automatically debits the bond". `oc-agent-protocol/SECURITY.md:53-58` (doc)
- Example relying-party enforcement: `verifying-mcp-server` refuses to execute a tool unless the call carries an action that verifies against a delegation granting `mcp:invoke(server=..., tool=...)`. `oc-agent-examples/verifying-mcp-server/README.md:3-5`, `:43` (doc)

Revocation, renewal, chains, multisig principal
- Revocation envelope `oc-agent:revocation:v1` signed by principal or agent (both always authorized; `revocation.holders` is unsigned and informational). `oc-agent-protocol/SPEC.md:488-494`, `:611-622` (spec). Kind 30085, discovered by `#t` = delegation id. `oc-agent-protocol/SPEC.md:556-582` (spec)
- Effective time = OTS anchor time if anchored, else `signed_at`; in live verification any revocation already in effect kills every action. `oc-agent-protocol/SPEC.md:527-552` (spec)
- Absence of revocation may be concluded only if at least (relays asked - 2 + 1) relays "answered in full" (paged to a short page, none cut off), e.g. four of five; otherwise result is "unchecked", never "unrevoked". `oc-agent-protocol/SPEC.md:812-827` (spec). Errata: before 2026-09-02 the spec's revocation query could not match on NIP-12 relays, "a conforming implementation would find no revocations and honour a revoked delegation". `oc-agent-protocol/SPEC.md:590-597` (spec)
- No renewal primitive: `agent-renewal` is only a reserved `kind` value. `oc-agent-protocol/SPEC.md:944` (spec). Expiry is the only automatic end of authority (wall clock).
- Sub-delegation (v1.1, kind 30086): strictly narrowing in scope and time, principal of child = agent of parent, default max depth 5, revoking any link cascades; sub-delegations "MAY NOT carry its own bond". `oc-agent-protocol/SUB-DELEGATION.md:5-15`, `:121-123`, `:191-204` (spec)
- Federation principal (v1.2): M-of-N guardian BIP-322 signatures over the delegation id (and over revocations), off-chain; "No custody is added". `oc-agent-protocol/FEDERATION.md:10-16`, `:164-177`, `:271-277` (spec). Status: verifier path in agent-core shipped; `agent-signer` helpers and wallet flow "not built yet". `oc-agent-protocol/FEDERATION.md:260-269` (spec); `oc-packages/agent-core/src/federation.ts:1-15` (code)
- Per-action co-signature by a human is not a protocol feature; the rationale suggests "Verifiers who want per-action certainty can pair an agent-action with a fresh OC Stamp from the principal". `oc-agent-protocol/WHY.md:86` (doc)

What it does not prove
- Not that the action happened, not that it was in the principal's interest; a leaked agent key "allows anyone to act within the delegation's scope up to expiry, hence bond, short expiry, and revocation-on-compromise as the three risk controls". `oc-agent-protocol/SPEC.md:894-908` (spec)
- Deferred: bond slashing ("belongs in a higher-layer protocol"), multi-principal m-of-n, per-link bonds, per-action bond increments. `oc-agent-protocol/SPEC.md:955-963` (spec)
- An early draft required every action to cite a recent Bitcoin block hash (a freshness proof); dropped as "brittle" in favor of optional OTS. `oc-agent-protocol/WHY.md:88-98` (doc)

### Inferences
- OC Agent gives Escapement a working, test-vectored authorization artifact for AI tool calls (with framework adapters), but its limits are exactly the ones the thesis targets: the agent's caps bind only relying parties that choose to verify; an agent holding its own wallet key can spend outside any delegation; per-call caps can be split into many calls; and authority ends by wall clock, not by block height.
- The 365-day maximum window and short-expiry advice are the closest thing to a lease (N4), but there is no renewal envelope and no block-height freshness.

### Gaps
- Whether any deployed Lightning or payment service actually verifies `ln:send` actions before paying: none found in local code (grep for `ln:send` found only scope tables, CLI, templates and dashboards).

## OC Attest (identity): stake measurement and sybil claims

### Takeaway
An attestation is a BIP-322 signature by a single-key address over a fixed seven-line message binding self-asserted handles (nostr, dns, x, github) to the address. Stake is not posted anywhere: at verification time the verifier reads the address's confirmed UTXOs from an Esplora API and computes `sats_bonded` and `days_unspent` (coin age, oldest-first greedy cover). Sybil resistance is claimed only as cost (sats x time), not uniqueness. A separate Draft "bond" (BOND.md) adds one-coin-one-subject and a registry-keyed nullifier ban, called "slashing without custody", whose only cost is that a moved coin's age restarts.

### Cited Findings
Format and signing
- Spec v2.1.0 "Stable (Normative)". `oc-attest-protocol/SPEC.md:3-4` (spec). Reference SDK `@orangecheck/sdk` 1.27.0. `oc-packages/sdk/CHANGELOG.md:12` (code)
- Canonical message lines: `orangecheck`, `identities:` (sorted, <= 512 bytes), `address:`, `purpose: portable reputation attestation (non-custodial)`, `nonce:`, `issued_at:`, `ack: I attest control of this address and bind it to my identities.` `oc-attest-protocol/SPEC.md:35-47`, `:62-81` (spec). Optional signed extension lines `aud`, `bond` (integer sats), `expires`, `network`, `publish`, `relay_hints`, `scope`, `scoring`. `oc-attest-protocol/SPEC.md:92-112` (spec). `attestation_id = SHA-256(canonical_message)`. `oc-attest-protocol/SPEC.md:149-158` (spec)
- Addresses: mainnet single-key P2WPKH, P2TR, P2PKH; `bip322` first, `legacy` (BIP-137) only for P2PKH. `oc-attest-protocol/SPEC.md:22-24`, `:170-173` (spec). Code verifies BIP-322 "simple" for P2WPKH, P2SH-P2WPKH, single-key P2TR (Schnorr key path) and BIP-137; "full" and proof-of-funds signatures refused. `oc-packages/bip322/src/index.ts:282-287`, `:350-366`, `:359` (code). So no P2WSH or multisig address can attest.
- Nostr wrapper (kind 30078, `d` = bare attestation id, `t` = address and `oc-attest`, `i` per identity) is a NIP-01 Schnorr signature used only as transport: "Verifiers MUST NOT trust attestations based on the Nostr wrapper pubkey". `oc-attest-protocol/SPEC.md:242-277`; `KINDS.md:50-52` (spec, doc). Handle bindings are self-asserted. `oc-attest-protocol/SECURITY.md:37-39` (doc)

How stake is measured
- Without `bond:`: `sats_bonded` = sum of confirmed UTXOs; `days_unspent = floor((now - min(confirmation_time)) / 86400)`. With `bond:`: balance below bond is `bond_insufficient`, else `sats_bonded` = bond, and days by "oldest-first greedy": sort coins by (height, txid, vout), take until the sum reaches the bond, age of the youngest coin taken, so "an old dust output [cannot] lend its age to a fresh deposit". `oc-attest-protocol/SPEC.md:103-106`, `:336-353` (spec). Code matches; days measured from the header timestamp `status.block_time` (wall-clock days, not block counts). `oc-packages/sdk/src/verify.ts:356-427` (code)
- Chain source: Esplora `GET {base}/address/{addr}/utxo`, mempool.space then blockstream.info, 5 s timeout each; addresses with more than about 500 UTXOs return `utxo_cap_unread`. `oc-packages/sdk/src/verify.ts:195-237`, `:277-282` (code). So signature and id verify offline, stake needs an indexer.
- Confirmation depth, docs vs code: SECURITY says "One block is insufficient, six is the family default" `oc-attest-protocol/SECURITY.md:102-104` (doc); live `verify()` keeps any `status.confirmed` UTXO, i.e. 1 confirmation, with no option to raise it. `oc-packages/sdk/src/verify.ts:357` (code). Live = 1 confirmation.
- Advisory score `score_v0 = round(ln(1+sats_bonded) x (1+days_unspent/30), 2)`; raw metrics are the source of truth. `oc-attest-protocol/SPEC.md:418`, `:450-453`; `oc-attest-protocol/registry/scoring.md:10`, `:20` (spec)
- Gate `check()` returns `stake_shared` when the address also backs another identity on that protocol, and `stake_unread` when the relay read did not finish. `oc-packages/sdk/src/check.ts:36-51`, `:83-88`, `:221-228` (code)

Sybil claims and limits
- "OC Attest raises the *cost* of sybils; it does not make them impossible"; no personhood or uniqueness. `oc-attest-protocol/SECURITY.md:46-49` (doc). Coins can be spent right after publication, so verifiers SHOULD re-read the chain on every check. `oc-attest-protocol/SECURITY.md:56-59` (doc). One-address-one-identity-per-protocol (`stake_shared`) depends on a relay read floor and can be evaded by an attestation held only on a silent relay. `oc-attest-protocol/SECURITY.md:84-88`, `:115-125` (doc)
- "Not going to claim this solves AI-agent trust. It doesn't." `oc-attest-protocol/WHY.md:133` (doc)
- No revocation envelope; the real exit is spending the UTXOs. `oc-attest-protocol/LIFECYCLE.md:22-34`, `:50-66` (spec)

BOND.md (Appendix B, Draft 1.1.0-draft)
- Message header `orangecheck-bond`: address, `outpoint` (txid:vout), `subject` (up to 256 printable ASCII; may be "an account, a key, an agent"), nonce, issued_at, expires_at (signing window at most 1 hour), `ack: I back this subject with this coin. It stays in my wallet.` `oc-attest-protocol/BOND.md:10-13`, `:39-65` (spec)
- Verification at tip H: outpoint exists, script matches address, confirmed at h, unspent at H, SHOULD require `H - h + 1 >= 6`; age in days `floor(conf/144)` (block-count days). `oc-attest-protocol/BOND.md:78-100` (spec). Code `BOND_MIN_CONFIRMATIONS = 6`. `oc-packages/sdk/src/bond.ts:17-23`, `:245-251` (code)
- "The coin stays in its holder's wallet. Nobody takes custody of it, and spending it ends the bond." `oc-attest-protocol/BOND.md:17-18` (spec). One coin per bond, value does not add across coins, consolidation restarts age. `oc-attest-protocol/BOND.md:102-104` (spec). One active bond per subject per registry; rebonding a released coin to another subject waits out the longest claim lifetime (ochk.io: 30 days). `oc-attest-protocol/BOND.md:106-120` (spec)
- Nullifier `HMAC-SHA256(key = nullifier_key, "orangecheck-bond-nullifier\n" || audience || "\n" || outpoint)` with a secret registry key; rotating the key lifts every ban. `oc-attest-protocol/BOND.md:157-174` (spec); registry key in
- "Slashing without custody. An audience that bans a nullifier has banned the coin ... The only way is to move the coin ... its age restarts at zero ... Nothing is confiscated, and nobody holds anything. The cost of abuse is time." `oc-attest-protocol/BOND.md:176-181` (spec). Registry re-checks after 10 minutes.. Deployment status not verified.
- Archived agent-delegation analysis (retired as "reinventing UCAN"): GAP-6 "`bond:` = self-declared commitment" vs needed "`budget_sats:` = externally-granted authorization", "opposite trust directions"; never built. `oc-attest-protocol/archive/AGENT_DELEGATION_GAP_ANALYSIS.md:161-174`; `oc-attest-protocol/archive/README.md:7-12` (doc)

### Inferences
- Attest's coin-age metric is the corpus's real implementation of N6's "seasoned stake" idea, but as a read of an unlocked balance: the time cost is real (a fresh coin cannot be made old), yet the same coins can be shown to many verbs and verifiers, and can be borrowed for the window (BOND.md accepts rental, one subject at a time).
- BOND.md's nullifier ban is the only "penalty" mechanism found anywhere in the family, and it is reputational plus time-reset, enforced by a trusted registry secret.
- The live 1-confirmation read and Esplora dependency weaken the "Bitcoin-verified" claim for consequential gates.

### Gaps
- Whether BOND.md's registry is live on ochk.io was not checked against a deployment.

## OC Vote (legitimacy): weight, snapshot, sybil handling

### Takeaway
Polls and ballots are BIP-322-signed JSON objects on kinds 30080 to 30082. Weight is computed from the voter's UTXOs at a snapshot block in one of three modes: one per address (above `min_sats`), sats, or capped sats x coin-age-days (block counts / 144). Ballot timing for new polls is fixed by OC Stamp OTS anchors verified against headers. Secret ballots use OC Lock to the creator's reveal key with a hash commitment; no timelock. Sybil resistance is only economic; `one_per_address` is admitted to be attackable. The live tally reads current UTXOs, not historical ones, so results can drift after the snapshot.

### Cited Findings
- Spec v0.2.0, "still changing". `oc-vote-protocol/SPEC.md:3-4` (spec). Reference vote-core 2.2.1 (sub-reader, code).
- Poll fields: creator, question, options, deadline, created_at, `snapshot_block` (height or `"deadline"`), `weight_mode` (`one_per_address`, `sats`, `sats_days`), `weight_params`, `min_sats`, `min_days`, `mode` (public/secret), `reveal_pk`, `tiebreak`, `sig`. `oc-vote-protocol/SPEC.md:48-74` (spec). `poll_id = SHA256(canonical poll with sig.value="")`, signed by BIP-322 over hex id. `oc-vote-protocol/SPEC.md:76-80` (spec). P2WSH creators do not verify with the reference verifier. `oc-vote-protocol/SPEC.md:86` (spec)
- Kinds: 30080 `oc-vote:poll:<id>`, 30081 `oc-vote:ballot:<poll_id>:<voter>`, 30082 `oc-vote:reveal:<id>`; event pubkeys are HKDF throwaways not tied to the Bitcoin identity. `oc-vote-protocol/SPEC.md:103-133`, `:194-214` (spec). Until 2026-09-02 the specified filter used unindexed multi-letter tags "so every tally returned zero ballots". `oc-vote-protocol/SPEC.md:468-477` (spec)
- Weight: from `U(a,H)`, UTXOs at snapshot height H; `age_days(u,H) = max(0, floor((H - confirmed_height) x 600 / 86400))`; `one_per_address` = 1 if qualifying sats >= `min_sats`; `sats` = qualifying sats; `sats_days` = sum of value x min(age_days, cap_days), cap REQUIRED so a single ancient UTXO cannot drown fresh ones; a coin qualifies if age >= `min_days`. `oc-vote-protocol/SPEC.md:312-362`, `:519-522` (spec). Code matches. `oc-packages/vote-core/src/weight.ts:13-17`, `:51-77` (code). Vector v03: 200,000 sats x 50 days + 300,000 sats x 180 (capped from 400) = 64,000,000. `oc-vote-protocol/test-vectors/v03-sats-days-weighted.json` (spec)
- Snapshot `"deadline"` resolves to `H_close`, highest block with median time past <= deadline; tally deferred (`E_REORG`) until 6 confirmations. `oc-vote-protocol/SPEC.md:20`, `:90`, `:579-582` (spec)
- Anchoring (polls with deadline on or after 2026-11-15): a ballot counts if an OC Stamp over `sha256:<ballot_id>` has an OTS proof the tallier verified against headers; lowest verified height wins; grace 36 blocks; final once tip >= H_close + 36 + 6, else "provisional". `oc-vote-protocol/SPEC.md:218-285`, `:536-547` (spec). vote.ochk.io runs an anchorer every 10 minutes (at most 300 stamps per run). `oc-vote-protocol/SPEC.md:293-304`. Older polls use self-reported `created_at`. `oc-vote-protocol/SPEC.md:617-625` (spec)
- Secret ballot: option sealed in an OC Lock v2 envelope to the creator's X25519 reveal key, commitment SHA256("oc-vote/v0/commit", poll, voter, option), reveal on kind 30082 after finality; no timelock or tlock (threshold or drand reveal is future work). `oc-vote-protocol/SPEC.md:183-190`, `:368-387`, `:711`, `:735` (spec). Creator can peek early or never reveal; not receipt-free. `oc-vote-protocol/SECURITY.md:31-33`, `:96-102` (doc)
- Sybil: splitting gains nothing in `sats`/`sats_days`; in `one_per_address` it is an attack and the only defense is the community's `min_sats`/`min_days` bar. `oc-vote-protocol/SECURITY.md:84-86`; `oc-vote-protocol/WHY.md:91-98` (doc). Key selling not addressed. `oc-vote-protocol/SECURITY.md:72-74` (doc)
- Agent tie-in: under a `vote:cast` delegation, poll and choice are read from the ballot, never from `scope_exercised`. `oc-vote-protocol/SPEC.md:717` (spec)

### Inferences
- Vote shows a block-anchored, header-verified ordering rule (lowest OTS anchor height, grace window, finality depth) that could be reused for ordering agent actions against human vetoes or revocations.
- Weight by `sats_days` with a cap is a worked, test-vectored formula for time-weighted stake, again read-only.

### Gaps
- No live poll counts found locally.

## OC Stamp (provenance): anchoring, cost, batching, verification

### Takeaway
A stamp is a BIP-322 signature over the SHA-256 id of a six-line canonical message (address, content hash, length, MIME, self-declared `signed_at`), optionally anchored by submitting the 32-byte id to free OpenTimestamps calendars. It proves authorship plus existence-before-block-N, verifiable offline with block headers. It proves no recency, no uniqueness, no ordering and no non-equivocation, and its "stake" field is unsigned and checked only at verification time. OC Agent actions reuse this envelope.

### Cited Findings
- Spec v1.1 Stable, 2026-11-21. `oc-stamp-protocol/SPEC.md:1-4` (spec). Packages stamp-core 1.4.0, stamp-ots 0.7.0. `oc-packages/stamp-core/package.json:3`, `oc-packages/stamp-ots/package.json:3` (code)
- Canonical message: `oc-stamp:v1`, `address:`, `content_hash: sha256:<hex>`, `content_length:`, `content_mime:`, `signed_at:`; LF-joined, no trailing LF; `id = SHA-256(canonical bytes)` is at once the OTS digest, the BIP-322 message and the envelope id. `oc-stamp-protocol/SPEC.md:41-62` (spec). Signature `BIP322(signer.address, hex(id))`. `oc-stamp-protocol/SPEC.md:154-160` (spec)
- Address types P2WPKH, P2SH-P2WPKH, P2TR, P2PKH (`oc-stamp-protocol/SPEC.md:31`); reference verifier checks P2TR key path only and not P2WSH (`oc-stamp-protocol/SPEC.md:435`); multi-signer stamps deferred (`oc-stamp-protocol/SPEC.md:492`) (spec).
- OTS flow: POST the raw id to `<calendar>/digest`, get a pending proof; calendars anchor "roughly once per hour"; upgrade by GET `<calendar>/timestamp/<hex>`; a client MUST NOT mark confirmed without fetching and comparing the block header. `oc-stamp-protocol/SPEC.md:189-223` (spec). Defaults: alice/bob.btc.calendar.opentimestamps.org and finney.calendar.eternitywall.com. `oc-packages/stamp-ots/src/calendar.ts:12-16` (code). Code requires 2 calendar successes by default and merges receipts. `oc-packages/stamp-ots/src/submit.ts:54`, `:77-91` (code). `upgradeProof` refuses without a header source and confirms only when the header's merkle root (bytes 36-68) matches. `oc-packages/stamp-ots/src/upgrade.ts:66-68`, `:91-150` (code)
- Cost: "It batches submissions so individual users pay no fees". `oc-stamp-protocol/WHY.md:47` (doc). Batching is the calendars' internal Merkle aggregation (`oc-stamp-protocol/SPEC.md:195`, `:214`). How calendars commit on chain is not described locally (public OTS commits a root in a calendar transaction; outside knowledge, not verified here).
- Aggregator: specified (`POST /aggregate`, ~60 s Merkle batches, liveness-only trust; "The reference aggregator at `stamp.ochk.io` is open-source and replaceable") `oc-stamp-protocol/SPEC.md:238-248` (spec). Docs vs code: the live site has only a whitelisted CORS proxy to the three calendars, rate-limited, and no `/aggregate` route., `:50-52`, `:101` (code). Live = proxy; aggregator = specified only.
- Verification: version, shape, id rebuild, BIP-322, anchor (walk proof, fetch header at height, check hash and merkle root; unreadable header leaves it "unchecked"), optional content, optional stake. `oc-stamp-protocol/SPEC.md:363-379` (spec). "No ochk.io endpoint is required or consulted at verify time" but needs "a full-node-verified chain (or a trusted SPV-style checkpoint)". `oc-stamp-protocol/SPEC.md:232-234`, `:393` (spec). Default header source is the Esplora API, "trusted only to report which block is at a height"; no proof-of-work check. `oc-packages/stamp-ots/src/anchor.ts:77-93`, `:134-162` (code)
- Stake field `{attestation_id, sats_bonded, days_unspent}` is outside the canonical message: "anyone who handles the envelope can add, remove or change it". `oc-stamp-protocol/SPEC.md:96-100`, `:133` (spec). Verifier step 7 resolves the attestation against current chain state and requires id match, attestation address == `signer.address`, thresholds met on resolved (not declared) values; a pass says "nothing about the stake when the stamp was signed". `oc-stamp-protocol/SPEC.md:373-377`, `:391` (spec). Vectors: v06 stripped stake still verifies but fails a stake policy (`oc-stamp-protocol/test-vectors/v06-stake-stripped.json:2`, `:42-53`); v07 swapped to another address's attestation is rejected (`v07-stake-swapped.json:51-65`); v08 own attestation accepted on resolved values (`v08-stake-own.json:51-64`) (spec). Code `checkStake` checks id, address, min sats, min days; resolution is the caller's. `oc-packages/stamp-core/src/stake.ts:28-55` (code). Docs vs code: `oc-stamp-protocol/LIFECYCLE.md:28`, `:38` describe a content-addressed `stake_at_signing` snapshot; SPEC, vectors and code say unsigned; CHANGELOG records the correction (`oc-stamp-protocol/CHANGELOG.md:106`, `:114-121`). SPEC/code live.
- Nostr kind 30083, `d = oc-stamp:<id>`, `t` tags signer and content hash, ephemeral Nostr pubkey with "no relationship to the Bitcoin identity". `oc-stamp-protocol/SPEC.md:252-287` (spec). Co-claimed with OC Agent delegations (`oc-agent-del:` prefix, internal `kind` field disambiguates). `KINDS.md:14`, `:34` (doc)
- Does not prove: "Recency ... A stamp with `signed_at: 2020-01-01` anchored in 2026 proves priority relative to the 2026 block"; "Uniqueness. The signer may sign the same content twice". `oc-stamp-protocol/SPEC.md:424-427` (spec). No sequence number or previous-stamp pointer in the canonical message (`oc-stamp-protocol/SPEC.md:41-48`, spec). Reorg handling: v1 assumes about 6 confirmations; `orphaned` status reserved. `oc-stamp-protocol/SPEC.md:481`, `:496` (spec). Calendar-plus-miner backdating "Partially mitigated" by several calendars. `oc-stamp-protocol/SECURITY.md:73` (doc)
- Test vectors v04/v05 OTS blobs "do not chain to any real Bitcoin block". `oc-stamp-protocol/test-vectors/README.md:62` (spec)

### Inferences
- Stamp is the cheapest Bitcoin-anchored primitive in the family (zero marginal sats, roughly hourly, 1 to several blocks latency) and the natural base for N8 action logs, but as specified it is an existence-before proof for isolated items. An agent can sign conflicting stamps and disclose only some; without a hash chain, a sequence number or a single-use seal, omission and equivocation are invisible.
- "Existed before block N" bounds backdating only from above; nothing gives a not-before bound (no recent block hash in the message), which matters for proving an agent acted after a given human authorization.

### Gaps
- No measurement of calendar latency or failure rates in local files; whether batched witness stamps (deferred, `oc-stamp-protocol/SPEC.md:495`) will be built is unknown.

## OC Lock (confidentiality) and the seal-til-block mode

### Takeaway
OC Lock encrypts to X25519 device keys that a Bitcoin address authorizes by a BIP-322 binding statement; the Bitcoin key never does key agreement. Its `expires_at` is a client-side refusal, not cryptographic. Block-height sealing exists only in OC Chat (a mode of Lock) via drand tlock with a hard client-side chain gate; the family spec itself says this leg fails its Ed25519 substitution test. A CLTV-based seal (consensus-enforced) is reserved and unbuilt.

### Cited Findings
- Spec v2.5.0 (2026-11-21) supersedes v1.0 (adaptor signature) and v1.1 (Proof-of-Access), and v1.1 had unlocked by an on-chain tx rule ("tx spending >= 10,000 sats from X at or after block Y"), since dropped. `oc-lock-protocol/SPEC.md:1-5`; `oc-lock-protocol/WHY.md:11` (spec, doc)
- Device binding: long-lived X25519 key; BIP-322 statement `oc-lock:device-bind:v2` (address, device_pk, device_id, created_at; v3 adds `nostr_pk`) published on kind 30078 with `d = oc-lock:device:<address>`. `oc-lock-protocol/SPEC.md:40-96` (spec). Revocation by signed `oc-lock:device-revoke:v2` statement (wallet only); read floor 4 of 5 relays else `E_RELAY_UNREACHABLE`. `oc-lock-protocol/SPEC.md:121-143` (spec)
- Encryption: random content key, AES-256-GCM payload; per-recipient ephemeral X25519, HKDF to a KEK, AES-GCM key wrap; envelope id SHA-256 of canonical envelope, `sig = BIP322(sender, id)`. `oc-lock-protocol/SPEC.md:202-227` (spec). No per-message forward secrecy. `oc-lock-protocol/SPEC.md:343-353` (spec)
- Expiry: `unseal` throws `E_EXPIRED` when the local clock is past `expires_at`, before decrypting. `oc-packages/lock-core/src/seal.ts:200-206` (code). Ciphertext itself is not time-bound (inference). LIFECYCLE: "Conforming consumers (e.g., agents acting on a delegated payment intent) MUST refuse to act on an envelope where `expires_at` is in the past. This is the only protocol-level 'withdraw the authority' mechanism"; stronger withdrawal is left to "wallet-level controls (multisig policy, transaction queueing)". `oc-lock-protocol/LIFECYCLE.md:59`, `:63` (doc)
- Payment mode (relay re-wraps the key after checking a confirmed tx via a block explorer; "The relay is a trust anchor") is specified only; no `tx_proof` or release endpoint in any code. `oc-lock-protocol/SPEC.md:229-260` (spec); grep across workspace by sub-reader (code). "Trustless payment mode. Requires DLC oracles, BIP-118 ... Not shippable today". `oc-lock-protocol/WHY.md:102` (doc)
- Lock `chat-seal` with `anchor: "beacon"`: block height is "beacon-enforced policy, not Bitcoin consensus"; a colluding beacon can release early; a vanished beacon bricks the seal. `oc-lock-protocol/SPEC.md:275-283` (spec). lock-core has no `chat-seal` kind (`EnvelopeKind = 'identity' | 'payment'`). `oc-packages/lock-core/src/types.ts:9` (code)
- Shipped v0 seal (OC Chat): text under fresh secret R; R tlock-encrypted to a drand quicknet round; "Anyone can decrypt R once the round's BLS signature publishes". `oc-chat-protocol/SPEC.md:230-249` (spec)
- Block-to-round mapping: `round = roundAt(now + max(0, unlock_block - current_tip) x 600000ms)`; "an approximation ... std-dev is about 10min x sqrt(N_blocks), hours at weekly horizons, unbounded worst case". `oc-chat-protocol/SPEC.md:251` (spec). Vector vc10: tip 900000, unlock 900006, round 8333412, std-dev 0.41 h. `oc-chat-protocol/test-vectors/vc10-round-for-block.json:4-18` (spec)
- Hard chain gate (normative): a client MUST NOT show the body until `chain_tip >= unlock_block + confirmations` "EVEN IF `tlock` has already yielded `R`"; early reading needs "BOTH a drand-threshold collusion AND a non-conforming client". `oc-chat-protocol/SPEC.md:253` (spec). Code checks tip first, default 1 confirmation, tip read as a bare height from mempool.space or blockstream.info with no header or PoW check., `:250-274`
- Self-assessment: "swap block height for an NTP clock and the construction is byte-identical, so this leg FAILS the Ed25519 substitution test"; horizon capped at 4320 blocks (about 30 days). `oc-chat-protocol/SPEC.md:255` (spec)
- CLTV anchor: "content_key is committed to a P2WSH output encumbered by OP_CHECKLOCKTIMEVERIFY at unlock_block; spending after the height reveals the key in the witness ... Bitcoin consensus is the enforcer"; "reserved, not shipped in v0", MUST NOT be advertised until a vector and browser build exist. `oc-chat-protocol/SPEC.md:225` (spec)
- Standing delivery (dead-man's switch): re-seal the same content to a later `unlock_block` under a hidden `standing_id`; highest `unlock_block` is live; a relay "can never make the switch fire earlier" but can drop check-ins, so the switch can be made to fire, not reliably suppressed; check-in at least every ~30 days. `oc-chat-protocol/SPEC.md:259-263` (spec), `:115`, `:122-123` (code)
- Kind 30112 (seal / block-height anchor) is draft; no emitter in code. `KINDS.md:23` (doc); grep by sub-reader (code)
- UTXO-age gate for chat channel writes (`utxo-floor`): checks an outpoint's value and `age_confs = tip - anchor_height + 1` offline; example 144 confirmations and 10000 sats. `oc-chat-protocol/test-vectors/vc17-channel-utxo-write-proof.json:2-30`; `oc-chat-protocol/SPEC.md:589` (spec)
- Agent relevance: under `lock:seal`/`lock:chat` scopes the verifier takes recipients from the Lock envelope's `recipients[]`, never from `scope_exercised`. `oc-lock-protocol/SPEC.md:355-357` (spec)
- Docs vs code: `oc-lock-protocol/SECURITY.md:71` names `bip322-js`/`elliptic` uses `@orangecheck/bip322` (code live; doc stale).

### Inferences
- For N4/N5, the family already has a "dead-man's switch" pattern (standing delivery) and a block-height gate, but both are client-enforced and drand-keyed, so a non-conforming or compromised client (an AI agent's own runtime, for instance) is not bound. The reserved CLTV seal is the only design in the corpus where Bitcoin consensus would hold a key until a height.
- Lock's `expires_at` gives no confidentiality-based constraint on agents beyond what a cooperating runtime chooses to refuse.

### Gaps
- No implementation, vector or cost estimate for the CLTV seal exists locally.

## Blocklore: how editions are sealed in Bitcoin blocks

### Takeaway
An edition is a JSON snapshot listing every claim's hash, an RFC 6962 Merkle root over them and the previous edition's root. Blocklore SHA-256s the whole file and submits that digest to four public OpenTimestamps calendars (no own transaction, no OP_RETURN, zero sats), then signs an OC Stamp over the same bytes with a single publisher key. A third party verifies offline with the claim files, the `.json`, the `.ots` and one block header. The seal proves existence before a block; it does not prove not-before, authorship time, or non-equivocation (two different files for the same edition number are not prevented by anything in Bitcoin).

### Cited Findings
Edition format and hashing
- Snapshot `knowledge/snapshots/<n>.json` fields: `n`, `at {time, height}`, `commit` (git sha), `count`, `root`, `previous` (prior root or null), `claims[{id, hash}]` in id order. `blocklore.space/core/src/snapshot.ts:20-36`; `blocklore.space/core/src/schema.ts:76-80`, `:337-346` (code)
- The bytes committed to are `JSON.stringify(s, null, 2) + "\n"`. `blocklore.space/core/src/snapshot.ts:38-41` (code)
- Claim hash: SHA-256 of canonical JSON (sorted keys), excluding `last_verified`. `blocklore.space/core/src/hash.ts:12-29`; `blocklore.space/CLAIMS.md:209-211` (code, doc)
- Merkle tree is RFC 6962: leaf = SHA-256(0x00 || claim hash), node = SHA-256(0x01 || left || right), split at the largest power of two below n, no duplicated odd leaf; inclusion proofs per RFC 9162 2.1.3.2. `blocklore.space/core/src/hash.ts:3-6`, `:31-63`, `:83-114` (code)
- Edition chain check: consecutive numbers, each `previous` equals the prior root, counts, ordering, root recomputes. `blocklore.space/core/src/snapshot.ts:65-83` (code)

Seal mechanism
- The digest stamped is SHA-256 of the whole snapshot text (`createHash("sha256").update(text)`), not the bare root; the root reaches Bitcoin because it sits inside the file. `blocklore.space/brain/src/snapshot.ts:200-202` (code). README's "Merkle root is timestamped" simplifies this (`blocklore.space/README.md:45`, doc); `blocklore.space/ARCHITECTURE.md:89` matches the code.
- Calendars (reference-client defaults): a.pool.opentimestamps.org, b.pool.opentimestamps.org, a.pool.eternitywall.com, ots.btc.catallaxy.com; at least two must answer; proofs pointing outside an allowlist are refused. `blocklore.space/brain/src/snapshot.ts:37-64`, `:85-113` (code)
- Hourly upgrade of pending proofs to Bitcoin attestations, checked against the block header's merkle root before keeping; upgrading stops at the first Bitcoin attestation. `blocklore.space/brain/src/snapshot.ts:116-160`, `:230` (code). OTS proof format parsed in-house. `blocklore.space/core/src/ots.ts:21-22`, `:290-352` (code)
- Cost to Blocklore: zero sats; calendars aggregate digests and pay for their own transactions (inference from OTS design; code only shows free POSTs).
- Frequency: daily tick snapshots only when the root changed; hourly tick upgrades. `blocklore.space/brain/src/tick.ts:6`, `:10-11`, `:300-303`, `:353-356` (code). Docs disagree: "Snapshots are taken after each publish that changes claims" `blocklore.space/web/app/verify/page.tsx:235-236`, `blocklore.space/ARCHITECTURE.md:132` (doc); code (daily) is live.
- Observed: editions 1 to 4 created at recorded tip heights 976771, 977320, 977464, 977628 and confirmed in blocks 976778, 977323, 977466, 977630 (2 to 7 blocks later). Read from `blocklore.space/knowledge/snapshots/1..4.json(.ots)` and reproduced with `tools/verify-snapshot.ts` by the sub-reader (artifact).
- No not-before proof: `at.height` is the explorers' tip height at creation, no block hash embedded. `blocklore.space/brain/src/store.ts:86-91` (code)

Verification path
- `tools/verify-snapshot.ts`: re-hash claim files at the edition's git commit, recompute root and chain, check proof digest equals file SHA-256, then fetch the header at the attested height from your own `bitcoin-cli` or from mempool.space and blockstream.info (must agree; header must double-SHA-256 to the block hash) and compare header bytes 36-68 with the proof's merkle root. `blocklore.space/tools/verify-snapshot.ts:68-166` (code; checked lines 140-166)
- Explorer path does not check proof-of-work or most-work chain; "Every chain check prints the command a reader runs against their own node, which is the real defense". `blocklore.space/SECURITY.md:266-270` (doc)
- Independent path: download `.json` and `.ots`, run `ots verify`. `blocklore.space/web/app/verify/page.tsx:189-195` (code). Files served byte for byte at `/api/v1/snapshots` and `/snapshots/{n}.json(.ots,.stamp)`. `blocklore.space/API.md:40-41` (doc)

What it proves and does not
- "It proves the snapshot file, and so every claim hash in it, existed before the block was mined. It does not make a claim true". `blocklore.space/web/app/verify/page.tsx:228-234` (code)
- "A snapshot file is never rewritten" is policy, not cryptography. `blocklore.space/ARCHITECTURE.md:89-90` (doc). Equivocation (two files for one `n`) is detectable only socially: public git history, the `previous` chain, Nostr copies, and the mirror check that flags "different bytes". `blocklore.space/core/src/mirror.ts:162`, `:181`; `blocklore.space/MIRROR.md:169-171` (code, doc)

OrangeCheck use
- Each edition carries an OC Stamp (BIP-322 by one P2WPKH publisher key over the stamp id, content hash = file SHA-256). `blocklore.space/brain/src/orangecheck.ts:181-210` (code). All four `.stamp` files have `"ots": null` (stamp ids not anchored) and `"stake": null` (artifact: `blocklore.space/knowledge/snapshots/4.json.stamp`).
- Intended authority chain: owner key attested for `dns:blocklore.space` (OC Attest), OC Agent delegation to the publisher key with scope `stamp:sign(mime=application/json)` for 365 days. `blocklore.space/ORANGECHECK.md:16-34`; `blocklore.space/core/src/orangecheck.ts:47-51` (doc, code). Live state: the owner has signed no record yet; the publisher key "signed alone" (sub-reader ran `tools/verify-orangecheck.ts 4 --offline`; no `knowledge/orangecheck/` directory).
- Self-stated times: "The time in a signature is the signer's own statement". `blocklore.space/ORANGECHECK.md:37-39`; `blocklore.space/core/src/orangecheck.ts:674` (doc, code). Edition 1 was signed two days after its `at` time. `blocklore.space/brain/src/orangecheck.ts:296-311`; `blocklore.space/ORANGECHECK.md:140` (code, doc)
- "A leaked key could sign false editions until revoked; the OpenTimestamps proofs and the git history still show what was published when." `blocklore.space/SECURITY.md:249-250` (doc)
- Planned only: outside reviewers' attestations, "optional Bonds on the reader queue against spam", `git-stamp`, "anchoring stamp ids with `stamp-ots`". `blocklore.space/ORANGECHECK.md:142-145` (doc)
- Agent-isolation pattern: "Models never publish": research and verifier roles write only to a staging folder, with no secret but the Claude subscription token; only deterministic code holds the publisher key, which "can sign only what the owner delegated (`stamp:sign` of JSON, a year at most)". `blocklore.space/CLAUDE.md:22-24`; `blocklore.space/SECURITY.md:242-254` (doc)

### Inferences
- Blocklore is a working, low-cost instance of N8's weaker half (tamper-evident log with existence-before proofs, Merkle inclusion, free OTS batching), with a daily cadence and 2 to 7 block confirmation latency observed. It lacks N8's stronger half: single-use seals or any rule that makes a second, conflicting edition for the same slot cryptographically detectable or costly.
- Its key-isolation pattern (models get no money-capable secret; a deterministic publisher holds a scoped, expiring, revocable key) is a concrete precedent for Escapement, but the delegation carries no spending limit and no bond, because the key never touches funds.

### Gaps
- No incident tied to sealing found. No measurement of OTS calendar availability or worst-case confirmation delay beyond four editions.

## Incidents and operational lessons that bear on agent payments

### Takeaway
The family's one real money loss (2026-08-07) came from a bearer credential with full spend authority sitting on an internet-facing server; the funds that survived were the ones whose signing keys were never online (watch-only xpub). Lightning is off family-wide with zero lifetime Lightning revenue, so no OrangeCheck agent has ever made a production payment. The only spending caps found in the workspace were off-chain risk limits in a now-retired trading bot.

### Cited Findings

### Inferences
- For N1 and N11, the lesson is that a cap is only as real as the narrowest credential that can move funds. An OC Agent `ln:send(max_sats<=N)` scope does nothing if the agent (or its host) holds an admin macaroon or a hot key; the enforcement point must be the key or script that signs the spend (a co-signer, a policy signer, or a script), and outflow monitoring is separate from authorization.
- "Two independent keys to arm" in the retired trading bot is an off-chain version of N11.

### Gaps
- No incident involving an agent acting under an OC Agent delegation was found (consistent with near-zero usage).

## Implications for Escapement

What to reuse (exists, tested, documented)
- Envelope discipline: line-oriented canonical message with a domain-separator first line, SHA-256 id, BIP-322 over the hex id, Nostr as untrusted directory with application-signature-only trust, relay read floor of (asked - 2 + 1) before concluding absence. `oc-agent-protocol/SPEC.md:73-95`, `:812-827`; `oc-pledge-protocol/SPEC.md:677` (spec)
- OC Agent's scope grammar, sub-scope relation, strictly narrowing sub-delegation (depth 5), live-verification rules (120 s freshness, single use, revocation in effect at now), revocation by principal or agent, M-of-N federation principal, and framework adapters for Anthropic, OpenAI, Vercel AI, LangGraph and MCP. `oc-agent-protocol/SPEC.md:283-446`, `oc-agent-protocol/SUB-DELEGATION.md:5-15`, `oc-agent-protocol/FEDERATION.md:10-16` (spec)
- OC Pledge's block-height `resolves_at`, `chain_state` predicates (`address(<addr>).balance >= <sats> AT block(<N>)`), pure state machine, abandonment-counts-as-broken, and "agent pledges count in the principal's ledger". `oc-pledge-protocol/SPEC.md:164-177`, `:372-418`, `:520-542` (spec)
- Coin-age arithmetic: Attest's oldest-first greedy cover (no dust lending age), BOND.md's one-coin-one-subject with re-bond wait and block-count days, Vote's capped `sats_days`. `oc-attest-protocol/SPEC.md:336-353`; `oc-attest-protocol/BOND.md:78-120`; `oc-vote-protocol/SPEC.md:347-362` (spec)
- Anchoring: Stamp's free OTS pipeline with header-checked upgrade, Vote's lowest-anchor-height ordering with grace and finality depth, Blocklore's RFC 6962 Merkle editions chained by `previous` root and its offline verifier. `oc-stamp-protocol/SPEC.md:189-223`; `oc-vote-protocol/SPEC.md:218-285`; `blocklore.space/core/src/hash.ts:31-114`; `blocklore.space/tools/verify-snapshot.ts:68-166` (spec, code)
- Dead-man's switch semantics from OC Chat standing delivery (max unlock_block wins; a relay can make it fire, cannot suppress it), and the reserved CLTV seal design. `oc-chat-protocol/SPEC.md:225`, `:259-263` (spec)
- Key isolation: Blocklore's "models never publish", model roles hold no money-capable secret, a deterministic process holds a scoped, expiring, revocable key. `blocklore.space/CLAUDE.md:22-24`; `blocklore.space/SECURITY.md:242-254` (doc)

What is missing (a new design must add)
- Any on-chain enforcement. No verb locks, timelocks, escrows or slashes sats; this is a family invariant, not an omission.; `oc-pledge-protocol/WHY.md:78-84`; `oc-agent-protocol/SPEC.md:910-914` (doc, spec). Escapement's caps (N1), slashable bonds (N2, N3), delay windows (N5) and co-signing (N11) need script-level constructions (multisig/co-signer, CLTV/CSV, vault or covenant designs, extractable one-time signatures) that would sit outside OrangeCheck's rules.
- Cumulative budgets: OC Agent caps are per action; no counter, no sequence number, no complete action list (, code). The archived `budget_sats` idea was never built (`oc-attest-protocol/archive/AGENT_DELEGATION_GAP_ANALYSIS.md:161-174`, doc).
- Block-height authority: delegations and pledge expiry are wall-clock; no renewal envelope (`agent-renewal` is only reserved, `oc-agent-protocol/SPEC.md:944`, spec); no not-before proof (the block-hash-citation idea was dropped, `oc-agent-protocol/WHY.md:88-98`, doc).
- Non-equivocation: Stamp has no uniqueness or ordering (`oc-stamp-protocol/SPEC.md:424-427`); Blocklore's "never rewritten" is policy (`blocklore.space/ARCHITECTURE.md:89-90`). No single-use seals anywhere.
- Header-chain verification: every reference path trusts Esplora or explorers for which block is at a height and for UTXO sets; none checks proof-of-work. `oc-packages/stamp-ots/src/anchor.ts:134-162`; `oc-packages/sdk/src/verify.ts:195-228` (code)
- Script-path and multisig signers: the reference BIP-322 verifier checks P2TR key path only and not P2WSH. `oc-agent-protocol/SECURITY.md:109` (doc); `oc-packages/bip322/src/index.ts:359` (code)
- Bond checks in OC Agent: specified as optional, not implemented in agent-core or the reference site. `oc-packages/agent-core/src/verify.ts:858-861`

What undercuts the thesis (evidence against, from the user's own protocols)
- The family deliberately chose reputation over custody and argues slashing makes the protocol "an actor with state, breaks offline-verifiability, and adds a censorship surface". `oc-pledge-protocol/WHY.md:80` (doc). Escapement must answer that argument, not ignore it.
- Every "cap" in the existing verbs binds only relying parties that choose to verify. An agent that holds its own funded key can spend outside any delegation; nothing in OC Agent touches the wallet. `oc-agent-protocol/SECURITY.md:35`, `:53-58` (doc)
- The one block-height lock that shipped (Chat seal) is keyed by drand and "FAILS the Ed25519 substitution test" by the spec's own admission. `oc-chat-protocol/SPEC.md:255` (spec)
- Stake signals are unlocked balances: reusable across commitments, withdrawable at any time, read at 1 confirmation in the live Attest path, and borrowable. `oc-pledge-protocol/SPEC.md:575-585`; `oc-packages/sdk/src/verify.ts:357`; `oc-attest-protocol/BOND.md:206-226` (spec, code)

## Coverage of N1 to N11

| Idea | Status in OrangeCheck / Blocklore | Where | Gap a new design must fill |
|---|---|---|---|
| N1 sat allowances, renewal as dead-man switch | Partial, weak. Per-action `ln:send(max_sats<=N)` checked by relying parties; wall-clock expiry; no cumulative budget; dead-man semantics exist only for messages (Chat standing delivery, drand-keyed) | `oc-agent-protocol/SPEC.md:333`, `:358`; `oc-agent-protocol/SECURITY.md:35`; `oc-chat-protocol/SPEC.md:259-263` | Enforcement at the spending key or script; cumulative accounting; expiry that a non-cooperating agent cannot ignore |
| N2 principal-funded bonds, slashed on adjudication | Half. "Own address" rule implemented (exact address match); slashing explicitly refused; BOND.md nullifier ban is reputational and registry-trusted; OC Agent bond unchecked | `oc-pledge-protocol/SPEC.md:575-585`; `oc-packages/pledge-core/src/bond.ts:65-71`; `oc-pledge-protocol/WHY.md:78-84`; `oc-attest-protocol/BOND.md:176-181` | Locked collateral and a transfer path on adjudicated breach; adjudication wiring (Pledge `named_oracle`/`vote_resolves` never exit `disputed` in code, `oc-packages/pledge-core/src/state.ts:95-99`) |
| N3 adjudicator-free slashing on equivocation | Not present | none found | Extractable one-time signatures or equivalent over agents' signed commitments |
| N4 block-height leases with human renewal | Partial. Wall-clock delegations (max 365 days), live expiry and revocation checks, 120 s freshness; no block-height bound, no renewal envelope | `oc-agent-protocol/SPEC.md:153`, `:419`, `:435`, `:944` | Height-denominated expiry, renewal signed by the human, freshness proof against a recent block |
| N5 timelocked vaults or delay windows with veto | Not present on chain. CLTV seal reserved only; pledge dispute windows are self-dated | `oc-chat-protocol/SPEC.md:225`; `oc-pledge-protocol/SPEC.md:427` | Script-level delay plus veto path (vault-style) |
| N6 seasoned bonds as sybil friction | Largely, as a read-only signal: coin age with greedy cover, block-count days, one-coin-one-subject, capped sats_days, UTXO-age write gates | `oc-attest-protocol/SPEC.md:336-353`; `oc-attest-protocol/BOND.md:78-120`; `oc-vote-protocol/SPEC.md:347-362`; `oc-chat-protocol/test-vectors/vc17-channel-utxo-write-proof.json` | Exclusivity across verbs and verifiers; resistance to borrowed coins; optional timelocked (not just unspent) variant |
| N7 blockspace as global rate limit | Not present; the family uses OTS batching precisely to avoid blockspace cost | `oc-stamp-protocol/WHY.md:47` | Entire idea |
| N8 tamper-evident, non-equivocating action logs; weight hash commitments | Partial. Stamp/OTS existence-before proofs, optional OTS on agent actions, Blocklore Merkle editions with previous-root chain; no non-equivocation, no not-before, no model-weight commitments (any hash can be stamped) | `oc-stamp-protocol/SPEC.md:189-223`, `:424-427`; `oc-agent-protocol/SPEC.md:245-252`; `blocklore.space/core/src/snapshot.ts:65-83` | Single-use seals or slot-unique commitments; sequence/hash chain per agent; not-before anchoring |
| N9 Bitcoin as clock for chip licence renewal | Not present (clock primitives exist: block-height deadlines, header-checked OTS) | `oc-pledge-protocol/SPEC.md:383`; `oc-vote-protocol/SPEC.md:267-285` | Entire idea |
| N10 proof-of-work energy anchor for compute governance | Not present | none found | Entire idea |
| N11 human co-signature on high-stakes agent transactions | Partial at grant level only: M-of-N federation principal signs delegations (verifier built, signer helpers not); no per-action co-sign; no P2WSH or script-path signers in the reference verifier | `oc-agent-protocol/FEDERATION.md:164-177`, `:260-269`; `oc-agent-protocol/SECURITY.md:109`; `oc-lock-protocol/LIFECYCLE.md:63` | Per-action human co-signature enforced by a spending script, not by a relying party |

```yaml
sources:
  - key: ochk-kinds
    path: OrangeCheck's Nostr kind table (the workspace KINDS.md; the same allocations appear in each protocol's SPEC.md)
    supports: Nostr kind allocations and d-tag prefixes, co-claim rule, errata
  - key: pledge-spec
    path: https://github.com/orangecheck/oc-pledge-protocol/blob/main/SPEC.md
    supports: pledge format, bond rule, own-address check, state machine, agent-signed pledges, no slashing
  - key: pledge-why
    path: https://github.com/orangecheck/oc-pledge-protocol/blob/main/WHY.md
    supports: sats x days rationale, block headers as clock, refusal of slashing (H5, H7), principal attribution (H12)
  - key: pledge-security
    path: https://github.com/orangecheck/oc-pledge-protocol/blob/main/SECURITY.md
    supports: implementation status, bond-draining residual, dispute gaming, backdating limits
  - key: pledge-lifecycle
    path: https://github.com/orangecheck/oc-pledge-protocol/blob/main/LIFECYCLE.md
    supports: stale claim that spent bond resolves broken (contradicts SPEC and code)
  - key: pledge-registry
    path: https://github.com/orangecheck/oc-pledge-protocol/blob/main/REGISTRY.md
    supports: refused slashing/escrow remediations, named_oracle dispute
  - key: pledge-core-bond
    path: https://github.com/orangecheck/oc-packages/blob/main/pledge-core/src/bond.ts
    supports: exact address match and bond checks in code
  - key: pledge-core-types
    path: https://github.com/orangecheck/oc-packages/blob/main/pledge-core/src/types.ts
    supports: caller-injected attestation lookup contract
  - key: pledge-core-state
    path: https://github.com/orangecheck/oc-packages/blob/main/pledge-core/src/state.ts
    supports: block-height normalization, disputes never resolved by mechanism, no bond in state
  - key: pledge-core-delegation
    path: https://github.com/orangecheck/oc-packages/blob/main/pledge-core/src/delegation.ts
    supports: max_bond_sats ceiling check for agent pledges
  - key: pledge-node-verify
    path: https://github.com/orangecheck/oc-pledge-examples/blob/main/node-verify/README.md
    supports: offline state from supplied block headers, header trust, v61 self-timelock pledge
  - key: agent-spec
    path: https://github.com/orangecheck/oc-agent-protocol/blob/main/SPEC.md
    supports: delegation/action/revocation formats, scopes and caps, verification steps, bond semantics, future work
  - key: agent-security
    path: https://github.com/orangecheck/oc-agent-protocol/blob/main/SECURITY.md
    supports: per-action cap admission, no on-chain bond enforcement, threats, BIP-322 verifier limits
  - key: agent-why
    path: https://github.com/orangecheck/oc-agent-protocol/blob/main/WHY.md
    supports: bond on grant not action, dropped block-hash freshness, comparison to UCAN
  - key: agent-subdelegation
    path: https://github.com/orangecheck/oc-agent-protocol/blob/main/SUB-DELEGATION.md
    supports: narrowing chains, depth limit, cascade revocation, no per-link bonds
  - key: agent-federation
    path: https://github.com/orangecheck/oc-agent-protocol/blob/main/FEDERATION.md
    supports: M-of-N guardian principal, implementation status
  - key: agent-core-verify
    path: https://github.com/orangecheck/oc-packages/blob/main/agent-core/src/verify.ts
    supports: 120 s skew default, replay guard, bond only shape-checked
  - key: agent-core-types
    path: https://github.com/orangecheck/oc-packages/blob/main/agent-core/src/types.ts
    supports: bond error codes declared but unused
  - key: agent-core-scope
    path: https://github.com/orangecheck/oc-packages/blob/main/agent-core/src/scope.ts
    supports: registered constraint keys incl. max_sats and max_invocations
  - key: agent-core-federation
    path: https://github.com/orangecheck/oc-packages/blob/main/agent-core/src/federation.ts
    supports: federation verifier path exists in code
  - key: agent-example-mcp
    path: https://github.com/orangecheck/oc-agent-examples/blob/main/verifying-mcp-server/README.md
    supports: relying-party enforcement before tool execution
  - key: attest-spec
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/SPEC.md
    supports: attestation format, stake metrics, greedy coin-age rule, Nostr wrapper, score
  - key: attest-security
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/SECURITY.md
    supports: sybil cost claim, six-confirmation default, stake_shared limits
  - key: attest-why
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/WHY.md
    supports: disclaimer on AI-agent trust
  - key: attest-lifecycle
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/LIFECYCLE.md
    supports: no revocation; exit by spending
  - key: attest-bond
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/BOND.md
    supports: one-coin bond, nullifier ban, slashing without custody, rebond wait
  - key: attest-scoring
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/registry/scoring.md
    supports: advisory score formula
  - key: attest-archive-gap
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/archive/AGENT_DELEGATION_GAP_ANALYSIS.md
    supports: unbuilt budget_sats versus bond distinction
  - key: attest-archive-readme
    path: https://github.com/orangecheck/oc-attest-protocol/blob/main/archive/README.md
    supports: why the agent-delegation-in-attest idea was retired
  - key: sdk-verify
    path: https://github.com/orangecheck/oc-packages/blob/main/sdk/src/verify.ts
    supports: Esplora UTXO reads, 1-confirmation filter, coin-age computation
  - key: sdk-check
    path: https://github.com/orangecheck/oc-packages/blob/main/sdk/src/check.ts
    supports: stake_shared and stake_unread gate outcomes
  - key: sdk-bond
    path: https://github.com/orangecheck/oc-packages/blob/main/sdk/src/bond.ts
    supports: six-confirmation bond minimum, nullifier and floors
  - key: bip322
    path: https://github.com/orangecheck/oc-packages/blob/main/bip322/src/index.ts
    supports: supported address types; full and proof-of-funds refused
  - key: vote-spec
    path: https://github.com/orangecheck/oc-vote-protocol/blob/main/SPEC.md
    supports: poll/ballot format, weight modes, snapshot, OTS anchoring, secret ballot
  - key: vote-security
    path: https://github.com/orangecheck/oc-vote-protocol/blob/main/SECURITY.md
    supports: sybil handling, secret-ballot limits
  - key: vote-why
    path: https://github.com/orangecheck/oc-vote-protocol/blob/main/WHY.md
    supports: one_per_address attack admission
  - key: vote-lifecycle
    path: https://github.com/orangecheck/oc-vote-protocol/blob/main/LIFECYCLE.md
    supports: stale claim that post-snapshot spends have no effect
  - key: vote-core-weight
    path: https://github.com/orangecheck/oc-packages/blob/main/vote-core/src/weight.ts
    supports: weight formulas in code
  - key: vote-v03
    path: https://github.com/orangecheck/oc-vote-protocol/blob/main/test-vectors/v03-sats-days-weighted.json
    supports: worked sats_days example
  - key: stamp-spec
    path: https://github.com/orangecheck/oc-stamp-protocol/blob/main/SPEC.md
    supports: stamp format, OTS flow, stake field, verification, limits, aggregator claim
  - key: stamp-why
    path: https://github.com/orangecheck/oc-stamp-protocol/blob/main/WHY.md
    supports: zero fees via calendar batching
  - key: stamp-security
    path: https://github.com/orangecheck/oc-stamp-protocol/blob/main/SECURITY.md
    supports: calendar backdating partially mitigated
  - key: stamp-lifecycle
    path: https://github.com/orangecheck/oc-stamp-protocol/blob/main/LIFECYCLE.md
    supports: stale stake_at_signing claim
  - key: stamp-vectors
    path: https://github.com/orangecheck/oc-stamp-protocol/blob/main/test-vectors/
    supports: v06/v07/v08 stake vectors, fixture OTS blobs
  - key: stamp-ots-code
    path: https://github.com/orangecheck/oc-packages/blob/main/stamp-ots/src/
    supports: calendars, two-success submit, header-checked upgrade, Esplora header source
  - key: stamp-core-stake
    path: https://github.com/orangecheck/oc-packages/blob/main/stamp-core/src/stake.ts
    supports: checkStake logic
  - key: lock-spec
    path: https://github.com/orangecheck/oc-lock-protocol/blob/main/SPEC.md
    supports: device binding, encryption, payment mode (specified only), beacon seal caveats
  - key: lock-why
    path: https://github.com/orangecheck/oc-lock-protocol/blob/main/WHY.md
    supports: dropped on-chain unlock rule, trustless payment not shippable
  - key: lock-lifecycle
    path: https://github.com/orangecheck/oc-lock-protocol/blob/main/LIFECYCLE.md
    supports: expires_at as only withdrawal mechanism; wallet-level controls for payments
  - key: lock-core-seal
    path: https://github.com/orangecheck/oc-packages/blob/main/lock-core/src/seal.ts
    supports: client-side expiry refusal
  - key: lock-core-types
    path: https://github.com/orangecheck/oc-packages/blob/main/lock-core/src/types.ts
    supports: no chat-seal kind in lock-core
  - key: chat-spec
    path: https://github.com/orangecheck/oc-chat-protocol/blob/main/SPEC.md
    supports: drand tlock seal, block-to-round mapping, hard chain gate, Ed25519 failure admission, CLTV reserved, standing delivery
  - key: chat-vectors
    path: https://github.com/orangecheck/oc-chat-protocol/blob/main/test-vectors/
    supports: vc10 round mapping, vc17 UTXO-age write gate
  - key: blocklore-snapshot-core
    path: https://github.com/Xaxis/blocklore.space/blob/main/core/src/snapshot.ts
    supports: edition format, committed bytes, chain checks
  - key: blocklore-hash
    path: https://github.com/Xaxis/blocklore.space/blob/main/core/src/hash.ts
    supports: claim hashing, RFC 6962 Merkle tree, inclusion proofs
  - key: blocklore-brain-snapshot
    path: https://github.com/Xaxis/blocklore.space/blob/main/brain/src/snapshot.ts
    supports: whole-file digest stamped, calendars, upgrade
  - key: blocklore-store
    path: https://github.com/Xaxis/blocklore.space/blob/main/brain/src/store.ts
    supports: at.height is self-reported tip, no block hash
  - key: blocklore-tick
    path: https://github.com/Xaxis/blocklore.space/blob/main/brain/src/tick.ts
    supports: daily snapshot, hourly upgrade
  - key: blocklore-verify-snapshot
    path: https://github.com/Xaxis/blocklore.space/blob/main/tools/verify-snapshot.ts
    supports: offline verification path, explorer agreement, no PoW check
  - key: blocklore-orangecheck-brain
    path: https://github.com/Xaxis/blocklore.space/blob/main/brain/src/orangecheck.ts
    supports: OC Stamp per edition, publisher key, edition 1 signed later
  - key: blocklore-orangecheck-core
    path: https://github.com/Xaxis/blocklore.space/blob/main/core/src/orangecheck.ts
    supports: delegation scope and window, self-stated signature times
  - key: blocklore-orangecheck-doc
    path: https://github.com/Xaxis/blocklore.space/blob/main/ORANGECHECK.md
    supports: intended authority chain, self-stated times, planned bonds and stamp-ots
  - key: blocklore-security
    path: https://github.com/Xaxis/blocklore.space/blob/main/SECURITY.md
    supports: publisher key isolation, leaked-key risk, explorer trust
  - key: blocklore-claude
    path: https://github.com/Xaxis/blocklore.space/blob/main/CLAUDE.md
    supports: models never publish
  - key: blocklore-architecture
    path: https://github.com/Xaxis/blocklore.space/blob/main/ARCHITECTURE.md
    supports: never-rewritten policy, snapshot cadence text (disagrees with code)
  - key: blocklore-verify-page
    path: https://github.com/Xaxis/blocklore.space/blob/main/web/app/verify/page.tsx
    supports: what a timestamp proves, ots verify instructions
  - key: blocklore-mirror
    path: https://github.com/Xaxis/blocklore.space/blob/main/core/src/mirror.ts
    supports: mirror check flags rewritten editions
  - key: blocklore-snapshots-data
    path: https://github.com/Xaxis/blocklore.space/blob/main/knowledge/snapshots/
    supports: four live editions, ots proofs, stamps with ots null
```
