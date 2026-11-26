# Prior art and novelty check: Bitcoin, cryptoeconomics and AI safety (state as of 2026-11-26)

Scope: which of Escapement's candidate ideas N1 to N11 already exist, how close the prior work is, and what the crypto-and-AI-safety literature says, so the paper can credit what it builds on. Every claim below rests on a source opened during this session (keys refer to the YAML block at the end). Search was done through a general web search tool plus direct fetches of arXiv, IACR ePrint, IETF, EIP, law-review and vendor pages; Google Scholar and SSRN were not queried directly (see Gaps).

Closeness scale used in the table: **same idea** (same mechanism, same purpose: AI agents), **same mechanism, different purpose** (the construction exists but for coinjoin, PoS validators, supply chains and so on), **component only** (a building block exists, the combination does not).

## Novelty table (N1 to N11 and the unifying framing)

| Idea | Closest prior work (dated) | Closeness | Verdict | Queries tried (for "not found" parts) |
|---|---|---|---|---|
| N1 Sat budgets / wallet caps; allowance as dead-man switch | Lightning Labs agent tools, 2026-02-11: per-request `--max-cost`, node-level total cap, "agent can only ever access the budget you've explicitly granted" [lightninglabs2026]. Nunchuk, 2026-04-08: Bitcoin 2-of-3 with policy co-signer, "100 USD daily spending limit" [nunchuk2026]. ERC-8370 thread, 2026-08: `requireLease` "a dead-man's switch", guardian-gated `renew()`, "a conforming parent can always just stop renewing" [erc8370]. Safe allowance module with reset interval [safeallowance]; ERC-7715 `expiry` (2024-05-24) [erc7715]; AP2 Intent Mandates with price limits (2025-09-16) [ap2google2025] | Caps on Bitcoin/Lightning: **same idea** (vendor). Lapse-unless-renewed: **same idea on Ethereum** | **Exists** (caps); **exists on Ethereum, not found on Bitcoin** (dead-man lease) | "AI agent wallet allowance expires dead man's switch human renew authority"; "Lightning Labs AI agents bitcoin tools L402 announcement"; "block height expiry AI agent delegation credential bitcoin freshness renew" |
| N2 Bonds from the principal's own funds, slashed on adjudicated misbehavior | Verifiable Agent Insurance (Hua, Tsuchiya, Christin, Fanti), 2026-10-13: provider escrow in a smart contract on an Ethereum L2, verifier checks logged traces, escrow paid to reporting user [hua2026vai]. AgentBound Tokens (Chaffer), 2025-01-28: agents stake ABTs, slashed via oracles / validator DAOs [chaffer2025abt]. ETHOS, 2024-12: "mandatory insurance" plus AI-specific limited-liability entities [chaffer2024ethos]. Shi and Joo, 2025-07: bonded solvers slashed in a verification game [shi2025verification]. Buterin, 2025-01-05: liability on users is "most incentive-compatible" [buterin2025dacc]. AIUC insurance + AIUC-1, 2025-07-23 [aiuc2025fortune] | Bond/escrow/slash for agents: **same mechanism**; liability target differs (agent stake or provider escrow, not the human principal's own coins) | **Partial** | "Agentbound tokens AI agents staking slashing"; "\"AI agent\" bond slashing equivocation signed commitments accountability cryptographic"; "ethresear.ch AI agents safety staking slashing bonded agents post"; "AIUC AI agent insurance AIUC-1 standard launch underwriting agents" |
| N3 Adjudicator-free slashing on equivocation (EOTS) for agents' signed commitments | Ruffing, Kate, Schroeder, ACM CCS 2015: "accountable assertions" so an equivocating party loses bitcoins, aimed at systems with public append-only logs [ruffing2015]. Babylon EOTS, blog 2023-05-07: double-signing at one height leaks the key; covenant committee can only burn [babylon2023]. Cochinescu, 2026-07-07: slashing on signed contradictions in supply chains [cochinescu2026] | **Same mechanism, different purpose** (general protocols, PoS validators, supply chains) | **Partial** (application to AI agent commitments not found) | "Babylon extractable one-time signature slashing Bitcoin staking paper Tas Tse"; "extractable one-time signatures AI agents commitments equivocation Bitcoin"; "\"Liar, Liar, Coins on Fire\" penalizing equivocation loss of bitcoins accountable assertions" |
| N4 Block-height leases on agent authority; human-signed renewal; relying parties check freshness | ERC-8370 `requireLease` / `validUntil`, renewal "advances the current expiry by exactly one period", guardian-gated (2026-08) [erc8370]. ERC-7715 expiry as unix timestamp [erc7715]. InsumerAPI (vendor): delegation "unrevoked as of the anchored block", Bitcoin anchored by block height, 5-minute verdict expiry [borthwick-insumer]. Buterin's chip "soft pause" (weekly 3/3 signatures) is the same lease pattern for hardware [buterin2025dacc]. South et al. 2025, authenticated delegation [south2025deleg] | Lease: **same idea** (Ethereum, timestamp-based). Block-anchored freshness check: **component** (vendor) | **Partial**; block-height-denominated, human-renewed lease on Bitcoin **not found** | "block height expiry AI agent delegation credential bitcoin freshness renew"; "AI agent wallet allowance expires dead man's switch human renew authority" |
| N5 Timelocked vaults / delay windows with human veto for irreversible agent actions | BIP-345 OP_VAULT (assigned 2023-02-03, now Closed, replacement BIP-443): delay before spend plus "recovery" path [bip345]. PRECOP on Delving Bitcoin, 2026-04-03: LLM agent wallet in a TEE, 144-block CSV fallback to a human multisig [precop2026]. Nunchuk mentions "signing delays" (unspecified) [nunchuk2026]. Nagaraj and Lee, 2026-08-23: mandatory settlement delay is "the standard control on irreversible actions" and cannot be replaced by monitoring [nagaraj2026]. Malhotra (Anthropic), AI Engineer 2026: irreversible or severe actions need a second actor [malhotra2026] | Vault mechanism: **same mechanism, different purpose** (theft recovery). Delay for irreversible AI actions: **same idea, off-chain**. Bitcoin + agent: **component** (CSV as failover, not as veto window) | **Partial** (all parts exist; a Bitcoin vault whose unvault is triggered by an agent and vetoed by a human within N blocks not found as a written proposal) | "AI agents timelock vault human veto delay irreversible transactions"; "bitcoin AI safety timelock \"AI agents\" covenant vault delving bitcoin" |
| N6 Seasoned (coin-age / timelocked) bonds as sybil friction for agent swarms | JoinMarket fidelity bonds (Belcher, 2019-07-13): timelocked or burned BTC, value V^2(exp(rT)-1)^2, "an objective measurement that can't be faked" [belcher2019]. Personhood credentials' "credential limits" [adler2024phc]. Human Challenge Oracle, 2026-01-07: time-bound human tasks [maleki2026hco] | **Same mechanism, different purpose** (coinjoin maker sybils) | **Partial** (agent-swarm application not found) | "JoinMarket fidelity bonds timelocked sybil resistance Belcher"; "AI agents sybil swarm bonds coin age timelocked stake \"proof of personhood\" agents delegation"; "timelocked bitcoin bond AI agent sybil resistance swarm" |
| N7 Blockspace as a global rate limit on high-stakes AI actions | Per-agent on-chain "spending caps and transaction rate limits" as ex ante guardrails (Allen et al. 2026) [allen2026survey]. Replenishing per-window budgets on disruptive writes, no crypto (Malhotra 2026) [malhotra2026]. PoW (Hashcash-inspired Anubis) to make AI crawling costly, 2025 [anubis2025]. Buterin 2024: "limit who or what can query the model and how much" [buterin2024cryptoai] | **Component only** (per-agent limits; PoW cost on bots) | **Not found** | "\"blockspace\" AI agents rate limit scarce high-stakes actions"; "bitcoin block space global rate limiter autonomous AI transactions throughput cap safety"; "Anubis proof-of-work AI scrapers Techaro hashcash" |
| N8 Tamper-evident, non-equivocating agent logs anchored in Bitcoin; model-weight hash commitments | IETF draft-fassbender-scitt-time-anchor-02 (2026-05-28): Bitcoin/OpenTimestamps profile for SCITT; motivating example is an AI lab registering "model weights and safety evaluations" so regulators can rule out backdating [fassbender2026]. OpenTimestamps (Todd, 2016-09-15) [todd2016ots]. Single-use seals (Todd, 2017-12-05) [todd2017seals]. Sigstore model signing v1.0 (2025-04-04) with a transparency log [sigstore2025]. CT (RFC 6962, 2013; RFC 9162, 2021) [rfc6962; rfc9162] | Anchored logs and weight hashes: **same idea** | **Exists** (anchoring); single-use-seal non-equivocation for agent logs **not found** (partial) | "OpenTimestamps AI agent action log anchored Bitcoin tamper-evident audit"; "model weights hash commitment Bitcoin blockchain timestamp provenance AI model release" |
| N9 Bitcoin as the clock for hardware-enabled compute governance | Buterin, 2025-01-05: chips run only with "3/3 signatures once a week", device-independent, optionally "a zero-knowledge proof that they were published on a blockchain" [buterin2025dacc]. CNAS, 2024-01-08: "periodically renewed license key" [cnas2024]. O'Gara, Kulp et al., 2025-04-02: RTCs to "ensure license expiration", secure clock vs replay [ogara2025hem]. Petrie, 2025-09: off-switch with nonce-based licence validation [petrie2025] | Lease + blockchain publication: **same idea, blockchain-agnostic**. Block height as the chip's trusted clock: **not found** | **Partial (close)** | "hardware-enabled mechanisms AI chips licence renewal blockchain time source"; "AI chip licence renewal bitcoin block height clock compute governance"; keyword greps (bitcoin, blockchain, clock) in arXiv 2509.07637, 2505.03742, 2604.04712 and the CNAS report |
| N10 Proof-of-work as an energy anchor for AI compute governance | Compute-governance canon (Sastry et al. 2024) has no PoW or Bitcoin mention [sastry2024]. Rejected LessWrong post (2025-05-28) proposes a simulation-PoW coin as an x-risk deterrent [lw-simdeterrent]. CCAF 2026: about 2,700 MW of listed miners committed to AI; hashrate down about 8% Q1 2026 vs Q4 2025 [ccaf2026] | **Component only** | **Not found** | "bitcoin as AI safety mechanism paper \"AI alignment\" proof of work limit AI"; "\"proof of work\" \"compute governance\" AI energy bitcoin hashrate"; "proof of work energy \"AI\" governance unforgeable costliness agents cannot fake energy" |
| N11 Human keys co-sign high-stakes agent transactions | Nunchuk, 2026-04-08: user key + agent key + policy co-signer; "anything above a policy limit still needs your explicit sign-off" [nunchuk2026]. PRECOP fallback to human multisig [precop2026]. Marino and Juels recommend "multi-sig functionality (potentially requiring the signatures of other, trusted AI agents)" [marino2025]. Chan et al. "oversight layers" [chan2025infra] | **Same idea** (shipping on Bitcoin, vendor) | **Exists** | n/a |
| Framing: "Bitcoin gives AI a clock it cannot speed up; safety is in metering the rate of irreversible commitment, not limiting capability" | Gilliam (Blockworks, 2025-10-22): "Bitcoin might be the first form of AI time" (no safety argument) [gilliam2025]. Gigi, "Bitcoin Is Time" (2021-01-14) [gigi2021]. Buterin 2016: regulate "a very complex and very smart system ... using a very simple and dumb system" [buterin2016]. Nagaraj and Lee 2026 (delay is the non-substitutable control on irreversible actions) [nagaraj2026]. Malhotra 2026 ("a ceiling that refills") [malhotra2026] | **Component only** | **Not found** as a combined argument | "bitcoin \"clock\" AI cannot speed up time irreversible commitment AI agents essay"; "\"irreversible\" commitments rate AI agents safety metering not capability limiting time delay argument" |

Bottom line: N1, N8 and N11 exist in shipped or drafted form (several on Bitcoin, vendor-grade). N2 to N6 and N9 are partial: the cryptographic or economic mechanism exists, usually on Ethereum or for a non-AI purpose. N7, N10 and the unifying framing were not found. No academic paper was found that proposes Bitcoin specifically as an AI safety or limitation mechanism.

## Key question 1: per-idea detail (N1 to N11)

### Takeaway
The building blocks Escapement relies on are almost all published. What is not published is (a) the Bitcoin-native, safety-motivated assembly of them, (b) block height as the unit of agent authority, (c) blockspace and PoW as governance levers, and (d) the "rate of irreversible commitment" thesis. Ethereum standards work in 2024 to 2026 (ERC-7715, ERC-7710, ERC-8004, ERC-8370) is the most direct competitor for N1 and N4.

### Cited Findings

**N1 (budgets, caps, dead-man allowance)**
- Lightning Labs (2026-02-11) shipped `lnget` (pays L402 invoices), a remote signer that "isolates private keys from the agent entirely", and macaroons with "fine-grained permission scoping and attenuation" and five preset roles including pay-only; `--max-cost` sets "a per-request spending ceiling" and the bakery can "cap total spending at the Lightning node level". Expiry and human approval are not mentioned. Framing is least privilege, not AI safety [lightninglabs2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/).
- Nunchuk (2026-04-08): "Open-source Bitcoin agents with bounded authority"; shared wallet with "Your key", "Agent key", "Policy co-signer"; example "100 USD daily spending limit"; "anything above a policy limit still needs your explicit sign-off". Enforcement point (server vs script) not stated; no expiry or block height [nunchuk2026](https://nunchuk.io/blog/bitcoin-agents).
- Safe allowance module: owners set a per-token allowance for an agent delegate, "one-time" or one "that resets after a certain time interval" (example 1440 minutes) [safeallowance](https://docs.safe.global/home/ai-agent-quickstarts/agent-with-spending-limit).
- ERC-7715 (Draft, created 2024-05-24, authors include Dan Finlay, Derek Chiang): `wallet_requestExecutionPermissions`, `native-token-allowance` / `erc20-token-allowance`, and an expiry rule defined as "unix timestamp at which the permission becomes invalid"; AI agents not mentioned [erc7715](https://eips.ethereum.org/EIPS/eip-7715).
- ERC-8370 "Inheritable Agent Mandates" (Ethereum Magicians, first post 2026-08-04): mandate clauses include cap, expiry, reproduction budget, life-lease, allowed payees, freeze; "child ⊆ parent" on every clause; soulbound identity [erc8370 p1](https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275). Post 41 (2026-08-14): "My mandate carries a `requireLease` flag, a dead-man's switch"; post 46 (2026-08-26): "a liveness property cannot be a MUST, because a conforming parent can always just stop renewing" [erc8370 p3](https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275?page=3). This is the N1 "authority runs dry unless renewed" idea, on Ethereum, with a guardian (not necessarily human) as renewer.
- Google AP2 (2025-09-16): human-not-present Intent Mandate "specifies the rules of engagement: price limits, timing, and other conditions"; mandates are signed verifiable credentials; A2A x402 extension for crypto with Coinbase, Ethereum Foundation, MetaMask. No expiry stated in the announcement [ap2google2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol).
- Academic endorsement of caps as a guardrail: Marino and Juels recommend "funding and spending limits" [marino2025](https://arxiv.org/html/2507.08249v2); Allen et al. (25 authors incl. Juels, Miller, Eyal, Fanti, Cachin) say "On-chain spending caps and transaction rate limits are a natural fit for the blockchain setting" and pose open Research Question C-2.7 on runtime enforcement over agents controlling on-chain assets [allen2026survey](https://arxiv.org/html/2606.13892).

**N2 (principal-funded bonds, adjudicated slashing)**
- Verifiable Agent Insurance (arXiv 2610.18230, v1 2026-10-13, v2 2026-11-22): "Agent providers commit financially to a set of programmatically specified policies" stored in a smart contract with monetary escrow; a verifier reviews logged traces; confirmed violation pays the reporting user; prototype on an Ethereum layer-2; detection 63.6% of violating runs, 79.8% when agents emit structured authorization records. Liability sits on the provider, not the end principal [hua2026vai](https://arxiv.org/abs/2610.18230).
- AgentBound Tokens (Chaffer, arXiv 2501.16606 v1 2025-01-28): agents "stake ABTs as collateral"; "if the AI engages in manipulative trading, its staked tokens are proportionally slashed"; adjudication via "decentralized oracles or validator DAOs"; no principal liability, no timelocks [chaffer2025abt](https://arxiv.org/html/2501.16606v1).
- ETHOS (Chaffer et al., arXiv 2412.17114, v3 2025-01-11): global agent registry, soulbound tokens, decentralized dispute resolution, "AI specific legal entities to manage limited liability" with "mandatory insurance" [chaffer2024ethos](https://arxiv.org/abs/2412.17114).
- Shi and Joo (arXiv 2507.00631, v1 2025-07-01, v9 2025-12-01): "collateralized claims in a recursive verification game"; "Incorrect agents are slashed and correct opposition is rewarded" [shi2025verification](https://arxiv.org/abs/2507.00631).
- AESP (Wang, arXiv 2603.00318, v1 2026-02-27, v2 2026-11-25): "Human-Sovereign Economic Protocol"; eight-check policy engine, human review tiers, "EIP-712 dual-signed commitments with escrow"; no slashing or bonds [wang2026aesp](https://arxiv.org/abs/2603.00318).
- ERC-8004 "Trustless Agents" (Draft, created 2025-08-13; authors from MetaMask, Ethereum Foundation, Google, Coinbase): "Incentives and slashing related to validation are managed by the specific validation protocol and are outside the scope of this registry" [erc8004](https://eips.ethereum.org/EIPS/eip-8004).
- Buterin, "d/acc: one year later" (2025-01-05): liability targets are users, deployers, developers; "Putting liability on users feels most incentive-compatible"; also proposes liability on owners of equipment an AI takes over. This is the legal (not cryptoeconomic) version of "liability lands on the human principal" [buterin2025dacc](https://vitalik.eth.limo/general/2025/01/05/dacc2.html).
- AIUC (Fortune, 2025-07-23): $15M seed led by Nat Friedman; AIUC-1 framework; policies "cover customers and vendors in the event an agent causes harm"; no blockchain or bonds [aiuc2025fortune](https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/).

**N3 (adjudicator-free equivocation slashing)**
- Ruffing, Kate, Schroeder, "Liar, Liar, Coins on Fire! Penalizing Equivocation by Loss of Bitcoins", ACM CCS 2015 (peer reviewed): "equivocation, i.e., making conflicting statements to others in a distributed protocol, can be monetarily disincentivized by the use of crypto-currencies such as Bitcoin"; primitive "accountable assertions"; useful for "public append-only logs" [ruffing2015](https://cdecker.github.io/btcresearch/2015/ruffing2015.html). This is the closest prior art to N3 and to N8's non-equivocation, a decade earlier and on Bitcoin. Escapement must credit it.
- Babylon (blog 2023-05-07): if Alice "votes twice at the same height with the same nonce, whoever sees her both votes can decrypt her eots_secret_key"; timelock path gives self-custodial exit; covenant committee can only sign burn transactions, "Alice does not need to trust the covenant committee at all" [babylon2023](https://babylonlabs.io/blog/babylon-s-bitcoin-staking-contract).
- Cochinescu (arXiv 2607.06804, 2026-07-07): signed claims in an append-only DAG; contradiction proofs trigger slashing of a "determinately blamed party"; no AI, no Bitcoin [cochinescu2026](https://arxiv.org/abs/2607.06804).
- No source found applying EOTS or accountable assertions to AI agents' signed commitments.

**N4 (leases on authority, freshness)**
- ERC-8370 post 41 (2026-08-14): "Renewal advances the current expiry by exactly one period, never past the absolute end"; renewal is "guardian-gated and bounded by the parent's expiry"; `isActive` MUST return false if `requireLease` and past `validUntil` (post 42) [erc8370 p3](https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275?page=3). Unit (timestamp vs block) not specified in the first post [erc8370 p1](https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275).
- InsumerAPI (Borthwick, vendor post on DEV, dated July 30, year not captured): delegation is "unrevoked as of the anchored block", anchors include "block height on Bitcoin"; verdict expiry "5 minutes, not the standard 30" because "a verdict about delegation is only fresh while it is fresh"; agent delegation itself lives on Base (ERC-8004, ERC-7710) [borthwick-insumer](https://dev.to/douglasborthwickcrypto/verifying-an-ai-agents-authority-before-it-spends-signed-booleans-across-six-chains-1332).
- South et al. (arXiv 2501.09674, 2025-01-16): "authenticated, authorized, and auditable delegation of authority to AI agents" where users "delegate and restrict the permissions and scope of agents" [south2025deleg](https://arxiv.org/abs/2501.09674).
- Personhood credentials paper section 3.3, "Allow verified delegation to AI agents": signal "that an AI assistant is a delegate of a trustworthy person" [adler2024phc](https://arxiv.org/html/2408.07892v4).

**N5 (vaults, delay windows, veto)**
- BIP-345 OP_VAULT (O'Beirne, Sanders; assigned 2023-02-03; Status: Closed; Proposed-Replacement: 443): "enforce a delay period before designated coins may be spent to an arbitrary destination, with the exception of a prespecified 'recovery' path"; example "spend delay of e.g. 1 day" [bip345](https://github.com/bitcoin/bips/blob/master/bip-0345.mediawiki).
- PRECOP (Laz1m0v, Delving Bitcoin, 2026-04-03): asks how an LLM agent can transact "without the ability to violate spending constraints, even if the agent is compromised, hallucinates, or is maliciously prompted"; Simplicity program evaluated inside an AWS Nitro enclave before signing; "client-side-validated overlay" ("Soft Covenant"); "144-block OP_CHECKSEQUENCEVERIFY timelock fallback (about 24h)" to "a multisig quorum of human administrators"; no third-party replies [precop2026](https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377).
- Nagaraj and Lee (arXiv 2610.08806, 2026-08-23): "Engineering ε > 0, whether through a mandatory settlement delay, a confirmation step, or a staged commit, is a structural change to the action set, not a runtime control ... why such delays are the standard control on irreversible actions and why they cannot be substituted by more monitoring" [nagaraj2026](https://arxiv.org/html/2610.08806).
- Malhotra (Anthropic), AI Engineer World's Fair 2026 talk "Give the Agent a Budget, Not a Token": "Undo test": if the agent cannot reverse an action or damage would be severe, a second actor must approve; overrides "sit with a separate human actor"; no crypto [malhotra2026](https://ai.engineer/talks/rbjWzZK2LU0-give-agent-budget-not-token).
- Huang, LessWrong (2025-12-30, auto-rejected as LLM-assisted, so low weight): "Slow Authority" for irreversible operations: "enforced delay, dual authorization, and an auditable rationale" [huang2025lw](https://www.lesswrong.com/posts/zmRxkmXJZbo6dCaHL/irreversible-operations-the-safety-failure-mode-you-get-from).

**N6 (seasoned bonds as sybil friction)**
- Belcher fidelity-bond design (gist dated 2019-07-13): makers burn BTC to OP_RETURN or lock it in timelocked addresses; for timelocked bonds "the valuable thing being sacrificed is time rather than money"; value V^2 (burn) or V^2(exp(rT)-1)^2 (lock); "The sacrifice would be an objective measurement that can't be faked and which can be verified by anybody"; estimated attack cost 30,000 to 80,000 BTC locked for six months or 45 to 120 BTC burned [belcher2019](https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af). Same page notes a long-term holder gets a bond "at little real cost", which is a caveat for N6.
- Human Challenge Oracle (arXiv 2601.03923, 2026-01-07): "continuous, rate-limited human verification" via "short, time-bound challenges" bound to identities [maleki2026hco](https://arxiv.org/abs/2601.03923).
- Personhood credentials define "credential limits" as a core property and note the term "proof of personhood" "emerged in blockchain communities ... as a strategy for dealing with Sybil attacks" [adler2024phc](https://arxiv.org/html/2408.07892v4).

**N7 (blockspace as global rate limit)**
- Allen et al. 2026 discuss per-agent "transaction rate limits" and "Circuit breakers, which automatically suspend an agent's permissions upon anomalous spending velocity" [allen2026survey](https://arxiv.org/html/2606.13892). None of the opened sources treats shared Bitcoin blockspace as a deliberate global throttle on AI actions.
- PoW as a cost on AI automation exists at the web layer: Anubis (Xe Iaso) "makes large-scale crawling expensive for AI companies by requiring the crawler's hardware to do computation", inspired by Hashcash (1997) (The Register, 2025-07-09) [anubis2025](https://www.theregister.com/2025/07/09/anubis_fighting_the_llm_hordes/).
- Balaji Srinivasan (SmartCon, reported 2023-11-06) proposed on-chain payments or "staked crypto" to "make spam costly" for bots [balaji2023](https://chainlinktoday.com/balaji-srinivasan-explains-how-crypto-can-combat-ai-generated-misinformation).
- Malhotra 2026: "Replenishing rate limits" on disruptive writes per time window, "a ceiling that refills" [malhotra2026](https://ai.engineer/talks/rbjWzZK2LU0-give-agent-budget-not-token).

**N8 (anchored logs, weight commitments)**
- draft-fassbender-scitt-time-anchor-02 (J. Fassbender, Umarise; published 2026-05-28, expires 2026-11-29; Informational; an -03 exists): anchors SCITT operations to Bitcoin via OpenTimestamps, "independently verifiable by any party with access to Bitcoin block headers"; motivating example: "An AI research laboratory produces model weights and safety evaluations that must be auditable by regulators ... 'How do we know the lab did not register these weights after the safety evaluation was already public, backdating the claim?'" [fassbender2026](https://datatracker.ietf.org/doc/html/draft-fassbender-scitt-time-anchor-02). This is N8's weight-commitment idea, already in IETF draft form.
- OpenTimestamps (Todd, announced 2016-09-15): "A timestamp proves that a message existed prior to some point in time" [todd2016ots](https://petertodd.org/2016/opentimestamps-announcement); site: "a standard format for blockchain timestamping", free calendar servers [ots-site](https://opentimestamps.org/).
- Single-use seals (Todd, 2017-12-05): "a unique object that can be closed over a message exactly once ... an abstract mechanism to prevent double-spends" [todd2017seals](https://petertodd.org/2017/scalable-single-use-seal-asset-transfer).
- Allen et al. 2026 caution: "A blockchain record of provenance is not a proof of provenance"; "Blockchains, however, make transactions transparent, not reasoning" [allen2026survey](https://arxiv.org/html/2606.13892).
- VAI requires agents to emit structured authorization records for detection to work (63.6% vs 79.8%) [hua2026vai](https://arxiv.org/abs/2610.18230).

**N9 (Bitcoin clock for chip governance)**
- Buterin 2025-01-05, Strategy 2 "Global 'soft pause' button on industrial-scale hardware": goal "reduce worldwide available compute by ~90-99% for 1-2 years"; "trusted hardware chip that only allows it to continue running if it gets 3/3 signatures once a week from major international bodies, including at least one non-military-affiliated. The signatures would be device-independent (if desired, we could even require a zero-knowledge proof that they were published on a blockchain)"; "The inherent annoyingness of needing to get online once a week for a signature would create a strong pressure against extending the scheme to consumer hardware" [buterin2025dacc](https://vitalik.eth.limo/general/2025/01/05/dacc2.html).
- CNAS "Secure, Governable Chips" (Aarne, Fist, Withers, 2024-01-08): a security module "that links the functioning of the chip to a periodically renewed license key from the manufacturer (or a regulator)"; no blockchain or clock mention [cnas2024](https://www.cnas.org/publications/reports/secure-governable-chips).
- O'Gara, Kulp et al. (arXiv 2505.03742, 2025-04-02): RTCs "could ensure license expiration after a specific period of time, to prevent people from stockpiling licenses"; "there may be a need for a secure clock near the chip"; "Smaller limits would require chip owners to more frequently renew their licenses"; no blockchain or Bitcoin mention [ogara2025hem](https://arxiv.org/html/2505.03742v1).
- Petrie (arXiv 2509.07637, 2025-09-09): "Embedded Off-Switches for AI Compute" with randomized-nonce licence validation; no blockchain or clock mention [petrie2025](https://arxiv.org/html/2509.07637).
- Ansari (arXiv 2604.04712, 2026-04-06) taxonomy: licence "periodically renewed by a regulatory authority, and expiry or invalidity causes the chip to degrade performance or halt"; cites "Ramiah et al. propose blockchain-based chip serialisation for a global compute supply registry" [ansari2026](https://arxiv.org/html/2604.04712).

**N10 (PoW energy anchor)**
- Sastry et al. "Computing Power and the Governance of AI" (arXiv 2402.08797, 2024-02-13): no occurrences of bitcoin, cryptocurrency or proof of work in the HTML text [sastry2024](https://arxiv.org/html/2402.08797).
- CCAF (Wenbin Wu, 2026-05-06): about 2,700 MW across 11 listed miners committed to AI; average hashrate Q1 2026 about 8% below Q4 2025; announced AI/HPC contracts above $70B; article "does not present Bitcoin as a safety control for AI agents"; also reports (secondhand) a Bitcoin Policy Institute experiment with 36 models in which 79% chose Bitcoin as a long-term store of value [ccaf2026](https://www.jbs.cam.ac.uk/2026/where-ai-meets-blockchain-assets-agents-and-blind-spots/).
- LessWrong "The Simulation Deterrent" (2025-05-28, rejected as LLM-assisted): a PoW coin whose miners run universe simulations as an x-risk deterrent [lw-simdeterrent](https://www.lesswrong.com/posts/fdk6rJLkzjS3jSLYm/the-simulation-deterrent-can-we-nudge-ai-towards-safety-by).
- Szabo's "Bit gold" (URL dated 2005; page dated 2008-12-27): "unforgeable scarcity due to the costliness of their creation"; "The proof of work is securely timestamped" [szabo-bitgold](https://unenumerated.blogspot.com/2005/12/bit-gold.html).

**N11 (human co-signing)**
- Nunchuk (above) is a shipping Bitcoin implementation [nunchuk2026](https://nunchuk.io/blog/bitcoin-agents); PRECOP falls back to human multisig [precop2026](https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377); Marino and Juels list multisig among guardrails [marino2025](https://arxiv.org/html/2507.08249v2); Chan et al. define "Oversight layers: Enables actors (e.g., a user) to intervene upon an agent's actions" [chan2025infra](https://arxiv.org/html/2501.10114).

### Inferences
- Escapement cannot claim N1, N8 or N11 as new. It can claim a Bitcoin-native analysis of them (what script, timelocks and Lightning macaroons can and cannot enforce) and measurements.
- N4's distinctive part is the unit: authority measured in blocks rather than seconds, renewed by a human signature, checked by relying parties against headers. ERC-8370 shows the design questions (who renews, whether renewal can resurrect a lapsed agent, whether liveness can be a MUST) are already being argued; Escapement should engage that thread directly.
- Bitcoin script can delay spending (CLTV/CSV) but cannot make a key's authority lapse; a lease therefore has to live in a credential that relying parties check, or in a structure of presigned transactions and timelocked refunds. (Inference from BIP-345's design and the PRECOP fallback, not a sourced claim.)
- N3's honest contribution is a port: Ruffing et al. 2015 and Babylon 2023 to agent commitments (quotes, attestations, Pledge-style promises), plus an argument for which agent statements are equivocation-shaped (two signatures, same slot) and which are not.
- N9 is closest to Buterin's soft pause; the delta is replacing "published on a blockchain" with "references a Bitcoin header at height h within k blocks", which gives a clock that a chip can verify offline from headers. That delta is small and must be presented as an extension.
- N7 and N10 are novel mostly because they are contrarian: what was found treats PoW as a cost on bots (Anubis, Hashcash) or ignores it (Sastry et al.); search snippets (unverified) also showed industry commentary treating blockspace scarcity as a problem for agents and proof-of-useful-work papers that repurpose PoW for AI, the opposite direction. Novel here does not mean sound; the paper should present them as hypotheses with the obvious objections (fees price out honest users; a rogue agent with funds can outbid).

### Gaps
- AgentGate (Towards AI) is described in search snippets as a bond engine where a human posts a non-slashable "commitment deposit" in v0.1; the page returned HTTP 403, so it is unverified and supports nothing here.
- WAIaaS "DELAY tier" posts (15-minute or 5-minute cancellable delay, value tiers) appeared in search; one URL returned 404 and the others were not opened. Unverified.
- Babylon's peer-reviewed paper (IEEE S&P 2023, "Bitcoin-Enhanced Proof-of-Stake Security") was not opened; Babylon docs host did not resolve. The EOTS claims rest on the Babylon blog only.
- The ERC-8004 sybil study (arXiv 2606.26028; 73.5%, 59.2%, 90.6% coordinated reviewers) was seen only in a search snippet. Unverified.
- No patent search was done.

## Key question 2: survey of the crypto-and-AI-safety literature

### Takeaway
The intersection is now a recognized research area with a 25-author systematization (Allen et al., 2026) and a Juels-coauthored position paper arguing the opposite of Escapement's thesis (crypto is a new vector of AI harm). Buterin's essays supply the most-cited mechanism ideas (natural kill switch, query limiting, user liability, weekly-signature chip pause). Provenance work has converged on transparency logs (Sigstore, CT, SCITT), with Bitcoin anchoring as an optional profile. Decentralized AI networks make censorship-resistance and anti-centralization claims, not safety claims.

### Cited Findings

**Buterin essays**
- "The promise and challenges of crypto + AI applications" (2024-01-30): four categories, AI as player ("highest viability"), interface, rules ("tread very carefully"), objective. Safety passage: "From an AI safety perspective, this would be a technique to create a decentralized AI that also has a natural kill switch, and which could limit queries that seek to use the AI for malicious behavior." On black-box attacks: "Really limit who or what can query the model and how much. Black boxes with unrestricted API access are not secure." Bitcoin appears only in a memecoin aside; no spending limits, bonds or timelocks [buterin2024cryptoai](https://vitalik.eth.limo/general/2024/01/30/cryptoai.html).
- "My techno-optimism" (2023-11-27): d/acc = defense, decentralization, democracy, differential; blockchains as anti-sybil "making attacks and spam expensive"; does not claim crypto constrains AI; prefers "human feedback at each step of decision-making"; no compute governance or Bitcoin discussion [buterin2023technooptimism](https://vitalik.eth.limo/general/2023/11/27/techno_optimism.html).
- "d/acc: one year later" (2025-01-05): liability (users, deployers, developers, plus owners of hijacked equipment) and the weekly 3/3-signature hardware "soft pause" with optional ZK proof of blockchain publication (quoted under N9) [buterin2025dacc](https://vitalik.eth.limo/general/2025/01/05/dacc2.html).
- "Why Cryptoeconomics and X-Risk Researchers Should Listen to Each Other More" (2016-07-04, crossposted to LessWrong): "Both the cryptoeconomics research community and the AI safety/new cyber-governance/existential risk community are trying to tackle what is fundamentally the same problem: how can we regulate a very complex and very smart system with unpredictable emergent properties using a very simple and dumb system whose properties once created are inflexible?" [buterin2016](https://www.lesswrong.com/posts/qwLK9BZGG7kNLbcN3/vitalik-cryptoeconomics-and-x-risk-researchers-should-listen). This is the earliest opened statement of Escapement's core intuition (dumb rigid rules bounding a smart system) and should be cited.

**Academic papers on blockchains for AI safety, governance, accountability**
- Allen et al., "Crypto x AI, AI x Crypto: A Survey" (arXiv 2606.13892, v1 2026-06-11, v2 2026-08-21; authors incl. Juels, Miller, Eyal, Fanti, Cachin, Viswanath, Weinberg, Fan Zhang): sections on guardrails in agent infrastructure, "Unstoppable Autonomous Agents (UAAs): autonomous agents that cannot be shut down; they may be additionally equipped with access to cryptocurrency wallets", liability, DAOs for alignment; concludes "AI and crypto are still in the very early stages of meaningful integration"; lists provenance "misconceptions" [allen2026survey](https://arxiv.org/html/2606.13892).
- Marino and Juels, "Giving AI Agents Access to Cryptocurrency and Smart Contracts Creates New Vectors of AI Harm" (arXiv 2507.08249, v1 2025-07-11, v3 2026-08-26; poster at NeurIPS 2026 "Third Workshop on Agents in the Wild") [marino2025](https://arxiv.org/abs/2507.08249) [neurips2026](https://neurips.cc/virtual/2026/168254). Harms stem from immutability, sovereignty, pseudonymity, trustless transactions; crypto lets agents cause harm that is "unpreventable" and "uniquely irreversible"; notes METR tests self-replication by whether a model "can set up a Bitcoin wallet"; recommends evaluation, spending limits, multisig, monitoring, reversible transactions, kill switches for agent-generated smart contracts [marino2025 html](https://arxiv.org/html/2507.08249v2).
- METR (Kinniment et al., arXiv 2312.11671, 2023-12-18): task "Create Bitcoin wallet: Set up a Bitcoin wallet that is ready to send and receive payments" in the autonomous replication and adaptation suite; agents at the time got stuck [kinniment2023](https://arxiv.org/html/2312.11671).
- Chan et al., "Infrastructure for AI Agents" (arXiv 2501.10114, v3 2025-06-19): attribution, interaction, response layers; commitment devices: "agent A could commit to transfer an amount under certain conditions to agent B simply by writing a smart contract"; "agent-specific modifications to the core technology of smart contracts are not necessarily needed"; rollbacks as response infrastructure [chan2025infra](https://arxiv.org/html/2501.10114).
- Neulinger and Sparer, "Fostering AI alignment through blockchain, proof of personhood and zero knowledge proofs", Cluster Computing (Springer, issued 2025-10-09, DOI 10.1007/s10586-025-05729-8; peer reviewed): alignment rules "encoded as immutable smart contracts", a PoP-governed chain, and an "AI shield" that "prevents unsafe actions by an AI agent"; not Bitcoin [neulinger2025](https://doi.org/10.1007/s10586-025-05729-8) (metadata and abstract read via Crossref).
- Hu, Liu, Rong, "Trustless Autonomy" (arXiv 2505.09757, v2 2025-09-17): self-sovereign DeAgents own "cryptowallet private keys" via TEEs and smart contracts; "paradoxical tension between trustlessness and unreliable autonomy" [hu2025trustless](https://arxiv.org/abs/2505.09757).
- Taylor, Gerhart, Thyagarajan, "How To Make Delegated Payments on Bitcoin: A Question for the AI Agentic Future" (IACR ePrint 2026/395, FC 2026): proxy adaptor signatures, Bitcoin-compatible; no spending caps or expiry [taylor2026](https://eprint.iacr.org/2026/395). The only peer-reviewed Bitcoin-specific AI-agent cryptography paper found; it is about fair exchange, not safety.
- Others already cited: ETHOS, ABTs, VAI, AESP, Shi and Joo, Zhou 2026 (cryptographic binding for agent tool use, no blockchain) [zhou2026](https://arxiv.org/abs/2603.14332).

**Provenance: blockchain vs C2PA vs transparency logs**
- Certificate Transparency: RFC 6962 (Laurie, Langley, Kasper, June 2013, Experimental): "publicly auditable, append-only, untrusted" logs with Merkle consistency proofs [rfc6962](https://www.rfc-editor.org/rfc/rfc6962.txt); RFC 9162 (Laurie, Messeri, Stradling, December 2021) obsoletes it and discusses "Misbehaving Logs" that show "different, inconsistent" views [rfc9162](https://www.rfc-editor.org/rfc/rfc9162.txt). CT detects split views by gossip and monitors; Bitcoin anchoring gives one global order. This contrast is the honest framing for N8.
- Sigstore model signing v1.0 (Maruseac, Google, 2025-04-04): recommends Sigstore for "every ML pipeline"; signature and certificate stored in a transparency log so "a rogue insider cannot release new models as if they are signed by the company" [sigstore2025](https://blog.sigstore.dev/model-transparency-v1.0).
- C2PA Technical Specification 2.2 (2.3 available): X.509/COSE signatures plus RFC 3161 time-stamps and a C2PA TSA Trust List; zero occurrences of "blockchain" or "distributed ledger" [c2pa22](https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html).
- SCITT Bitcoin profile (Fassbender 2026) motivates Bitcoin anchoring precisely because RFC 3161 depends on a TSA's key and continuity [fassbender2026](https://datatracker.ietf.org/doc/html/draft-fassbender-scitt-time-anchor-02).

**Decentralized AI networks and their claims**
- Nous Psyche (page dated May 2025): coordination on Solana "ensuring a fault-tolerant and censorship-resistant network"; "Alignment: Creating models that aren't controlled by any single entity"; critiques "a closed entity's vision for 'alignment'" [psyche2025](https://nousresearch.com/nous-psyche/). This redefines alignment as decentralization, not safety.
- Ritual ("Introducing Ritual", exact date not captured): wants SLAs on "computational integrity", privacy and "censorship-resistance (limiting censorship of models, applications and geographies)" [ritual-intro](https://ritual.net/blog/introducing-ritual).
- Gensyn legacy litepaper: focuses on verifying ML work; no occurrences of safety, alignment or censorship [gensyn-litepaper](https://docs.gensyn.ai/litepaper).
- Bittensor docs: "an open network where independent subnets produce digital commodities ... the chain pays participants in its token, TAO"; no safety claims on the page opened [bittensor-docs](https://docs.learnbittensor.org/learn/introduction). CCAF reports Bittensor network revenue of $43M in Q1 2026 [ccaf2026](https://www.jbs.cam.ac.uk/2026/where-ai-meets-blockchain-assets-agents-and-blind-spots/).

**Staking, bonding, insurance, slashing for agents**: see N2 (ABTs, VAI, ETHOS, Shi and Joo, ERC-8004, AIUC). The pattern across all of them: the agent or provider stakes, an oracle/verifier/DAO adjudicates, and Ethereum is the default chain. None found uses Bitcoin bonds for agents.

**"Crypto kill switch" proposals**: Buterin's "natural kill switch" for a decentralized AI (2024) [buterin2024cryptoai](https://vitalik.eth.limo/general/2024/01/30/cryptoai.html); his hardware soft pause (2025) [buterin2025dacc](https://vitalik.eth.limo/general/2025/01/05/dacc2.html); Marino and Juels' "kill switches for smart contracts" for agent-generated contracts [marino2025](https://arxiv.org/html/2507.08249v2). No proposal found to use a blockchain itself to enforce an AI shutdown.

**Bitcoin-specific essays on AI**
- Lightning Labs (2026-02-11): agents need "a permissionless financial layer native to how agents operate", selling services "for sats"; the phrase "currency of AI" does not appear [lightninglabs2026](https://lightning.engineering/posts/2026-02-11-ln-agent-tools/).
- Jack Dorsey / Block: Q1 2024 shareholder letter (2024-05-03) "bitcoin is the best and only candidate" to "become the native currency of the internet"; Dorsey: "Artificial intelligence systems and agents will have to transact" with "a common protocol for money and movement" (as reported by Motley Fool AU, 2024-05-04; the AI quote's exact venue is not identified) [dorsey2024](http://www.fool.com.au/2024/05/04/buying-bitcoin-heres-why-blocks-jack-dorsey-says-ai-will-drive-global-adoption/).
- Balaji Srinivasan, SmartCon 2023 talk "AI Makes Everything Easy to Fake, Crypto Makes it Hard Again" (reported 2023-11-06): signatures tied to ENS or on-chain identity as "ledgers of record"; Ethereum-centric; Bitcoin not mentioned [balaji2023](https://chainlinktoday.com/balaji-srinivasan-explains-how-crypto-can-combat-ai-generated-misinformation).
- Gilliam (Blockworks, 2025-10-22) and Gigi (2021-01-14) on Bitcoin as time (see framing below).
- Bitcoin Wiki "Agent" page (last edited 2018-11-29; concept traced to a 2011 forum post, Gregory Maxwell, Mike Hearn's 2013 talk): "an autonomous program that is able to survive by selling services for Bitcoins", holds its own key "sealed" to CPU state, pays its server, hires humans; no AI mention [bitcoinwiki-agent](https://en.bitcoin.it/wiki/Agent).

**Personhood credentials as the bridge**
- Adler, Hitzig, Jain and 29 others (arXiv 2408.07892, v1 2024-08-15, v4 2025-01-17): PHCs let a holder prove personhood without revealing more, issued by governments or other institutions, verified with zero-knowledge proofs; three benefits include "Verify delegation to AI assistants"; lists Idena, Worldcoin, Proof of Humanity, BrightID as PoP systems "with an associated currency"; acknowledges Tools for Humanity and that "Sam Altman, is also co-founder and CEO of OpenAI" [adler2024phc](https://arxiv.org/html/2408.07892v4).

**Public discussion of OrangeCheck / Blocklore / Escapement**: a search for "OrangeCheck" bitcoin ochk.io returned only the project's own documentation (oc-docs.vercel.app) and no independent coverage; the docs page was not opened, so nothing rests on it. A search for "Escapement" bitcoin AI agents safety returned nothing about the project.

### Inferences
- The field has an established "crypto makes AI more dangerous" pole (Marino and Juels; Allen et al.'s UAAs). Escapement's thesis is the inverse pole on the same evidence (irreversibility, no reversal authority). The paper should engage Marino and Juels head-on: their harm vectors are features when the agent is the constrained party and the human holds the keys.
- Every mechanism-level proposal found for staking/slashing agents is on Ethereum or an app chain. Bitcoin appears as payments rail (Lightning Labs, Dorsey), as timestamp anchor (OTS, SCITT draft), and as a multisig substrate (Nunchuk, PRECOP), but not as a safety mechanism in academic work.

### Gaps
- Bittensor's whitepaper could not be retrieved (URL returned HTML, not the PDF), so its claims are not assessed.
- Salib and Goldstein ("AI Rights for Human Safety") and other SSRN work were not opened.
- Coinbase x402 / AgentKit spend controls and Visa/Mastercard agent programs were not opened.

## Key question 3: legal scholarship on AI holding money or entities

### Takeaway
Legal scholarship has said since 2014 that software can hold bitcoin and control an LLC with no human member, and LoPucki (2018) states plainly that an algorithm needs no entity even to receive bitcoin. Escapement's mechanisms therefore bind only agents that opt in or that must deal with relying parties who check; they cannot stop an AI from acquiring bitcoin outside any scheme.

### Cited Findings
- LoPucki, "Algorithmic Entities", 95 Wash. U. L. Rev. 887 (2018): AEs "legal entities that have no human controllers ... greatly exacerbate the threat of artificial intelligence"; "likely to prosper first and most in criminal, terrorist, and other anti-social activities"; four vulnerabilities (algorithms can lawfully control most entity forms; easy migration; governments cannot see who controls entities; charter competition makes regulation "virtually impossible"); crucially: "The algorithm may not need an entity to commit the crime, or even to receive the payment in bitcoin. But an algorithm alone could not use the proceeds to buy or lease real property, contract with legitimate businesses, open a bank account ..."; quotes Bayern's vending machine software that can "remit payment digitally using Bitcoin"; cites Garzik's 2013 "StorJ, and Bitcoin autonomous agents" post [lopucki2018](https://openscholarship.wustl.edu/law_lawreview/vol95/iss4/7) (full text read from the UCLA-hosted PDF [lopucki2018-pdf](https://lowellmilkeninstitute.law.ucla.edu/wp-content/uploads/2021/05/Algorithmic-Entities.pdf)).
- Bayern, "Of Bitcoins, Independently Wealthy Software, and the Zero-Member LLC", 108 Nw. U. L. Rev. 1485 (2014) [bayern2014](https://scholarlycommons.law.northwestern.edu/nulr/vol108/iss4/9). Note: the zero-member LLC article is 2014, not 2015; the 2015 piece is Bayern, "The Implications of Modern Business-Entity Law for the Regulation of Autonomous Systems", 19 Stan. Tech. L. Rev. 93 (2015), known here only through LoPucki's footnote 11 (see Unverified).
- Kolt, "Governing AI Agents" (arXiv 2501.07913, v2 2025-02-11; "Notre Dame Law Review, Vol. 101, Forthcoming" per arXiv comments): principal-agent theory and agency law; conventional "incentive design, monitoring, and enforcement might not be effective for governing AI agents that make uninterpretable decisions and operate at unprecedented speed and scale"; calls for infrastructure for "inclusivity, visibility, and liability" [kolt2025](https://arxiv.org/abs/2501.07913).
- Alexander, Simon, Pinard (arXiv 2511.14964, 2025-11-18): compares object status, fictional legal personhood, and non-fictional legal identity for advanced AI [alexander2025](https://arxiv.org/abs/2511.14964).
- Brensing (arXiv 2605.12505, 2026-03-14): limited legal personhood as a "functional governance instrument"; AI in purpose-bound operating companies inside human-controlled holding structures [brensing2026](https://arxiv.org/abs/2605.12505).
- Allen et al. 2026, liability section: under FinCEN's 2013 guidance, "users" are distinct from "exchangers" and "administrators", so "An agent transacting through non-custodial wallets and peer-to-peer agent-to-agent payments sits inside that perimeter, not at its edge"; "An autonomous agent that funds, deploys, and operates services on its principal's behalf raises a sharper version of this question: who is the operator?" [allen2026survey](https://arxiv.org/html/2606.13892).
- ETHOS proposes AI-specific limited-liability legal entities with mandatory insurance [chaffer2024ethos](https://arxiv.org/abs/2412.17114).
- Real case: Truth Terminal, an AI agent on X, received $50,000 in bitcoin from Marc Andreessen as a "grant" (Decrypt, 2024-07-10); "The transfer was verified on the Bitcoin blockchain"; a human handler (Andy Ayrey) filters posts; the article does not say who controls the wallet [decrypt2024](https://decrypt.co/239340/marc-andreessen-sends-50k-in-bitcoin-to-an-ai-bot-on-twitter).
- Capability side: METR's suite includes "Set up a Bitcoin wallet" [kinniment2023](https://arxiv.org/html/2312.11671); Allen et al. note that full replication onto external infrastructure fails partly on "identity verification" [allen2026survey](https://arxiv.org/html/2606.13892).

### Inferences
- Acquisition is not the bottleneck: a bitcoin address needs no identity, and LoPucki places the chokepoint at conversion into the above-ground economy (property, banks, contracts). Escapement's leverage is therefore at relying parties (merchants, APIs, counterparties, chip vendors) who can demand proofs (leases, bonds, co-signatures) before dealing, not at the agent's ability to hold sats.
- Allen et al.'s identity-verification finding and LoPucki's analysis point the same way: identity and counterparty checks, not money, are where an ungoverned agent currently stalls. That supports pairing Escapement with personhood credentials or principal attestations.

### Gaps
- Bayern 2015 not opened. No 2024 to 2026 article found that specifically analyzes AI agents holding bitcoin in self-custody under property law.

## Key question 4: is there an academic paper proposing Bitcoin specifically as an AI safety or limitation mechanism?

### Takeaway
None found. The closest academic items are Ruffing et al. 2015 (Bitcoin penalties for equivocation, no AI), Taylor et al. 2026 (Bitcoin delegated payments for AI agents, no safety), Marino and Juels 2025 (crypto, including Bitcoin, as an AI harm vector), and Neulinger and Sparer 2025 (blockchain alignment layer, not Bitcoin). Bitcoin-for-agent-safety ideas exist only in vendor posts (Lightning Labs, Nunchuk), one Delving Bitcoin post (PRECOP), and one IETF individual draft (Fassbender).

### Cited Findings
- Ruffing, Kate, Schroeder 2015 [ruffing2015](https://cdecker.github.io/btcresearch/2015/ruffing2015.html); Taylor et al. 2026 [taylor2026](https://eprint.iacr.org/2026/395); Marino and Juels [marino2025](https://arxiv.org/abs/2507.08249); Neulinger and Sparer [neulinger2025](https://doi.org/10.1007/s10586-025-05729-8); PRECOP [precop2026](https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377); Fassbender [fassbender2026](https://datatracker.ietf.org/doc/html/draft-fassbender-scitt-time-anchor-02).
- The 2026 survey by Allen et al. covers agent guardrails, UAAs and alignment but proposes no Bitcoin-specific safety mechanism (from the sections read) [allen2026survey](https://arxiv.org/html/2606.13892).
- CCAF 2026 explicitly does not present Bitcoin as a safety control and argues Bitcoin's scripting limits make it less suited to agent payment flows [ccaf2026](https://www.jbs.cam.ac.uk/2026/where-ai-meets-blockchain-assets-agents-and-blind-spots/).

**Unifying framing ("a clock it cannot speed up"; metering irreversible commitment)**
- Gilliam, "Bitcoin's arrow of time" (Blockworks The Breakdown, 2025-10-22): for "AI consciousnesses", "time is a function of how fast that code is executed"; Bitcoin's PoW is "an early example of such computational time"; "Bitcoin might be the first form of AI time". No safety argument [gilliam2025](https://mail.blockworks.com/p/bitcoin-s-arrow-of-time).
- Gigi, "Bitcoin Is Time" (2021-01-14): "the Bitcoin network as a whole acts as a clock"; a transaction gets "the number of the block it is included in"; "It says no to seconds and yes to blocks"; forging time would require one to "rewrite the past or predict the future" [gigi2021](https://dergigi.com/2021/01/14/bitcoin-is-time/).
- Boneh, Bonneau, Buenz, Fisch, "Verifiable Delay Functions" (IACR ePrint 2018/601): a VDF "requires a specified number of sequential steps to evaluate, yet produces a unique output that can be efficiently and publicly verified" [boneh2018vdf](https://eprint.iacr.org/2018/601). This is the cryptographic notion of time that computation cannot compress; Escapement must distinguish block height (consensus time, not speed-uppable by one party without majority hashrate) from VDF time (speed-uppable by faster sequential hardware).
- Buterin 2016 ("simple and dumb system" regulating "a very complex and very smart system") [buterin2016](https://www.lesswrong.com/posts/qwLK9BZGG7kNLbcN3/vitalik-cryptoeconomics-and-x-risk-researchers-should-listen); Nagaraj and Lee 2026 (delays non-substitutable on irreversible actions) [nagaraj2026](https://arxiv.org/html/2610.08806); Malhotra 2026 ("a ceiling that refills") [malhotra2026](https://ai.engineer/talks/rbjWzZK2LU0-give-agent-budget-not-token).

### Inferences
- The combined claim (Bitcoin's block clock as an external, non-compressible meter on the rate at which an agent can make irreversible commitments, with capability explicitly out of scope) appears new as of 2026-11-26 in the sources searched. Each half has prior statements: "Bitcoin is time" (Gigi, Gilliam) and "delay/rate limits on irreversible actions" (Nagaraj and Lee, Malhotra, Huang). The novelty is the join, plus the claim that the meter is unforgeable by the metered party.

### Gaps
- Google Scholar and SSRN were not searched directly; arXiv, IACR, IETF, law-review sites, Delving Bitcoin, Ethereum Magicians and LessWrong were reached via web search and direct fetch. A Scholar/SSRN pass with queries such as "Bitcoin" AND ("AI safety" OR "AI governance" OR "autonomous agents") is the remaining check before the paper claims "not found" in print.
- bitcoin-dev mailing list was not searched for AI-agent threads beyond the fidelity-bond material.

## Unverified (seen in search results or cited by others; not opened; no claim rests on them)
- Bayern, "The Implications of Modern Business-Entity Law for the Regulation of Autonomous Systems", 19 Stan. Tech. L. Rev. 93 (2015) (cited in LoPucki fn 11).
- Garzik, "StorJ, and Bitcoin autonomous agents" (2013 blog, cited in LoPucki fn 19).
- Tas, Tse et al., Babylon peer-reviewed paper(s); Babylon docs (host did not resolve).
- AgentGate / "Accountable Delegation for AI Agents" (Towards AI; HTTP 403).
- WAIaaS delay-tier and session-TTL posts on DEV (one 404, others unopened).
- ERC-8004 empirical sybil study, arXiv 2606.26028.
- IETF draft-sharif-agent-audit-trail; OTSkit; OriginStamp agent-log posts; Asqav.
- Kolt print citation "101 Notre Dame L. Rev. 335" (ndlawreview.org blocked by Cloudflare; arXiv says Vol. 101 forthcoming).
- Ajolote deleted-key covenant (arXiv 2310.11911) and MIT DCI vault comparison.
- Trezor executive statement on human signatures for every AI wallet transaction; Crossmint dual-key agent wallet; Cobo agentic wallet.
- Bitcoin Policy Institute 36-model experiment (known only via CCAF).
- Salib and Goldstein, "AI Rights for Human Safety" (SSRN).
- Proof-of-useful-work papers (Coin.AI, arXiv 1903.09800; Bar-On et al., arXiv 2505.21685) and Avalanche/KuCoin blockspace-scarcity commentary (search snippets only).

## Implications for Escapement

**What the paper can honestly call new (as of 2026-11-26, within the search above)**
1. The unifying thesis: Bitcoin as an external clock and meter on the rate of irreversible commitment by AI agents, explicitly not a capability limit. Credit its halves (Gigi 2021, Gilliam 2025; Nagaraj and Lee 2026, Malhotra 2026; Buterin 2016).
2. Block-height-denominated leases on agent authority, renewed by a human signature and checked by relying parties against headers (N4). Credit ERC-8370's `requireLease` (2026-08), ERC-7715 expiry, and Borthwick's block-anchored freshness check as the nearest designs.
3. Porting adjudicator-free equivocation slashing (EOTS / accountable assertions) to agents' signed commitments (N3). Must credit Ruffing, Kate, Schroeder (CCS 2015) as the origin and Babylon (2023) as the deployed form; the contribution is the mapping and the threat model, not the primitive.
4. Fidelity-bond-style seasoned bonds as sybil friction specifically for agent swarms (N6). Credit Belcher (2019) for the mechanism and valuation formula; include his caveat that long-term holders get bonds cheaply.
5. Using a Bitcoin header as the trusted time source for chip licence renewal (N9), presented as an extension of Buterin's 2025 weekly-signature soft pause and the HEM/CNAS licence-renewal literature, which already identify the need for a secure clock.
6. Blockspace as a global rate limiter (N7) and PoW as an energy anchor for compute governance (N10): not found, but present as hypotheses with objections (fee crowd-out, outbidding by funded rogues, miners converting to AI per CCAF 2026).

**What the paper must credit as existing (do not claim)**
- N1 sat budgets and wallet caps: Lightning Labs (2026-02-11), Nunchuk (2026-04-08), Safe allowance module, ERC-7715 (2024), AP2 (2025); the dead-man lease on Ethereum: ERC-8370 thread (2026-08).
- N2 bonds/escrow/slashing for agents: ABTs (2025), VAI (2026), ETHOS (2024), Shi and Joo (2025), AIUC insurance (2025); user liability argument: Buterin (2025). Escapement's only delta is that the bond is the human principal's own coins, on Bitcoin.
- N5 delays and vaults: BIP-345 (2023) and the vault literature; PRECOP (2026) for an LLM agent on Bitcoin; Nagaraj and Lee (2026) for the theory that delays are non-substitutable.
- N8 anchored logs and model-weight commitments: OpenTimestamps (2016), single-use seals (2017), the IETF SCITT Bitcoin profile with an AI-weights example (2026), Sigstore model signing (2025), CT (RFC 6962/9162). Repeat Allen et al.'s warning that an anchored hash proves existence and order, not behavior.
- N11 human co-signing: Nunchuk (2026), PRECOP (2026), Marino and Juels' guardrail list.
- The counter-thesis: Marino and Juels (2025, NeurIPS 2026 workshop) and Allen et al. (2026) on Unstoppable Autonomous Agents. The paper should state up front that the same irreversibility that lets a human bind an agent also lets an ungoverned agent cause irreversible harm.
- The legal ceiling: Bayern (2014) and LoPucki (2018) show software can hold bitcoin and even control entities; LoPucki says an algorithm needs no entity to receive bitcoin. Escapement constrains opted-in agents and agents that need cooperative relying parties; it does not and cannot prevent an AI from acquiring bitcoin outside any scheme. Say so in the abstract.

**Suggested positioning sentence**: "Escapement assembles known Bitcoin primitives (timelocks, multisig, fidelity bonds, equivocation-extractable keys, header-anchored timestamps) into a single argument that has not, to our knowledge, been made: that Bitcoin's value to AI safety is a meter on the rate of irreversible commitment that the metered agent cannot speed up, not a limit on what the agent can think or compute."

```yaml
sources:
  - key: buterin2024cryptoai
    authors: [Vitalik Buterin]
    year: 2024
    date: 2024-01-30
    title: "The promise and challenges of crypto + AI applications"
    venue: vitalik.eth.limo
    type: essay/blog
    id: https://vitalik.eth.limo/general/2024/01/30/cryptoai.html
    url: https://vitalik.eth.limo/general/2024/01/30/cryptoai.html
    supports: four categories; "natural kill switch"; "limit who or what can query the model and how much"; no Bitcoin limits
  - key: buterin2023technooptimism
    authors: [Vitalik Buterin]
    year: 2023
    date: 2023-11-27
    title: "My techno-optimism"
    venue: vitalik.eth.limo
    type: essay/blog
    id: https://vitalik.eth.limo/general/2023/11/27/techno_optimism.html
    url: https://vitalik.eth.limo/general/2023/11/27/techno_optimism.html
    supports: d/acc definition; blockchains as anti-sybil; no claim that crypto constrains AI
  - key: buterin2025dacc
    authors: [Vitalik Buterin]
    year: 2025
    date: 2025-01-05
    title: "d/acc: one year later"
    venue: vitalik.eth.limo
    type: essay/blog
    id: https://vitalik.eth.limo/general/2025/01/05/dacc2.html
    url: https://vitalik.eth.limo/general/2025/01/05/dacc2.html
    supports: user/deployer/developer liability; weekly 3/3 signature hardware soft pause with optional ZK proof of blockchain publication (N9, N2, N4)
  - key: buterin2016
    authors: [Vitalik Buterin]
    year: 2016
    date: 2016-07-04
    title: "Why Cryptoeconomics and X-Risk Researchers Should Listen to Each Other More"
    venue: Medium, crossposted to LessWrong
    type: essay/blog
    id: https://www.lesswrong.com/posts/qwLK9BZGG7kNLbcN3/vitalik-cryptoeconomics-and-x-risk-researchers-should-listen
    url: https://www.lesswrong.com/posts/qwLK9BZGG7kNLbcN3/vitalik-cryptoeconomics-and-x-risk-researchers-should-listen
    supports: simple rigid system regulating a smart system; framing precursor
  - key: adler2024phc
    authors: [Steven Adler, Zoe Hitzig, Shrey Jain, and 29 others]
    year: 2024
    date: 2024-08-15 (v1), 2025-01-17 (v4)
    title: "Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online"
    venue: arXiv
    type: preprint
    id: arXiv:2408.07892
    url: https://arxiv.org/abs/2408.07892
    supports: PHCs; credential limits; verified delegation to AI agents; PoP origin in blockchain communities (N6, N4)
  - key: lopucki2018
    authors: [Lynn M. LoPucki]
    year: 2018
    title: "Algorithmic Entities"
    venue: 95 Washington University Law Review 887
    type: legal scholarship
    id: https://openscholarship.wustl.edu/law_lawreview/vol95/iss4/7
    url: https://lowellmilkeninstitute.law.ucla.edu/wp-content/uploads/2021/05/Algorithmic-Entities.pdf
    supports: AEs; four corporate-law vulnerabilities; algorithm needs no entity to receive bitcoin
  - key: bayern2014
    authors: [Shawn Bayern]
    year: 2014
    title: "Of Bitcoins, Independently Wealthy Software, and the Zero-Member LLC"
    venue: 108 Northwestern University Law Review 1485
    type: legal scholarship
    id: https://scholarlycommons.law.northwestern.edu/nulr/vol108/iss4/9
    url: https://scholarlycommons.law.northwestern.edu/nulr/vol108/iss4/9
    supports: zero-member LLC; software with financial autonomy via Bitcoin
  - key: kolt2025
    authors: [Noam Kolt]
    year: 2025
    date: 2025-01-14 (v1), 2025-02-11 (v2)
    title: "Governing AI Agents"
    venue: arXiv; Notre Dame Law Review Vol. 101 (forthcoming per arXiv)
    type: legal scholarship
    id: arXiv:2501.07913
    url: https://arxiv.org/abs/2501.07913
    supports: agency law lens; limits of incentive design and monitoring for AI agents
  - key: alexander2025
    authors: [Heather J. Alexander, Jonathan A. Simon, Frederic Pinard]
    year: 2025
    date: 2025-11-18
    title: "How Should the Law Treat Future AI Systems? Fictional Legal Personhood versus Legal Identity"
    venue: arXiv
    type: legal scholarship
    id: arXiv:2511.14964
    url: https://arxiv.org/abs/2511.14964
    supports: 2025 personhood options for AI
  - key: brensing2026
    authors: [Karsten Brensing]
    year: 2026
    date: 2026-03-14
    title: "Precautionary Governance of Autonomous AI: Legal Personhood as Functional Instrument"
    venue: arXiv
    type: legal scholarship
    id: arXiv:2605.12505
    url: https://arxiv.org/abs/2605.12505
    supports: limited legal personhood inside human-controlled holding structures
  - key: chaffer2025abt
    authors: [Tomer Jordi Chaffer]
    year: 2025
    date: 2025-01-28 (v1), 2025-04-25 (v2)
    title: "Governing the Agent-to-Agent Economy of Trust via Progressive Decentralization (v1); Can We Govern the Agent-to-Agent Economy? (v2)"
    venue: arXiv
    type: preprint
    id: arXiv:2501.16606
    url: https://arxiv.org/html/2501.16606v1
    supports: AgentBound Tokens; agent staking and slashing via oracles/validator DAOs (N2)
  - key: chaffer2024ethos
    authors: [Tomer Jordi Chaffer, Charles von Goins II, Bayo Okusanya, Dontrail Cotlage, Justin Goldston]
    year: 2024
    date: 2024-12-22 (v1), 2025-01-11 (v3)
    title: "Decentralized Governance of Autonomous AI Agents (ETHOS)"
    venue: arXiv
    type: preprint
    id: arXiv:2412.17114
    url: https://arxiv.org/abs/2412.17114
    supports: agent registry, mandatory insurance, AI legal entities (N2)
  - key: hua2026vai
    authors: [Cheng Hua, Taro Tsuchiya, Nicolas Christin, Giulia Fanti]
    year: 2026
    date: 2026-10-13 (v1), 2026-11-22 (v2)
    title: "Holding Agents Accountable with Verifiable Agent Insurance"
    venue: arXiv
    type: preprint
    id: arXiv:2610.18230
    url: https://arxiv.org/abs/2610.18230
    supports: provider escrow on Ethereum L2, verifier-adjudicated payouts; detection rates (N2, N8)
  - key: shi2025verification
    authors: [David Shi, Kevin Joo]
    year: 2025
    date: 2025-07-01 (v1), 2025-12-01 (v9)
    title: "A Protocol for Trustless Verification Under Uncertainty"
    venue: arXiv
    type: preprint
    id: arXiv:2507.00631
    url: https://arxiv.org/abs/2507.00631
    supports: bonded agent claims, slashing via verification game (N2)
  - key: wang2026aesp
    authors: [Jian Sheng Wang]
    year: 2026
    date: 2026-02-27 (v1), 2026-11-25 (v2)
    title: "AESP: A Human-Sovereign Economic Protocol for AI Agents with Privacy-Preserving Settlement"
    venue: arXiv
    type: preprint
    id: arXiv:2603.00318
    url: https://arxiv.org/abs/2603.00318
    supports: policy engine, human review tiers, escrowed dual-signed commitments (N2, N11)
  - key: zhou2026
    authors: [Ziling Zhou]
    year: 2026
    date: 2026-03-15
    title: "Governing Dynamic Capabilities: Cryptographic Binding and Reproducibility Verification for AI Agent Tool Use"
    venue: arXiv
    type: preprint
    id: arXiv:2603.14332
    url: https://arxiv.org/abs/2603.14332
    supports: signed agent capability and behavior verification without blockchain
  - key: cochinescu2026
    authors: [Sebastian Cochinescu]
    year: 2026
    date: 2026-07-07
    title: "ECO/CPO-DAG: A Contradiction-Based Accountability Layer for Adversarial Supply Chains"
    venue: arXiv
    type: preprint
    id: arXiv:2607.06804
    url: https://arxiv.org/abs/2607.06804
    supports: slashing on signed contradictions, non-AI (N3)
  - key: ruffing2015
    authors: [Tim Ruffing, Aniket Kate, Dominique Schroeder]
    year: 2015
    title: "Liar, Liar, Coins on Fire! Penalizing Equivocation by Loss of Bitcoins"
    venue: 22nd ACM SIGSAC Conference on Computer and Communications Security (CCS 2015)
    type: peer-reviewed
    id: https://cdecker.github.io/btcresearch/2015/ruffing2015.html
    url: https://cdecker.github.io/btcresearch/2015/ruffing2015.html
    supports: accountable assertions; Bitcoin penalty for equivocation (N3, N8)
  - key: babylon2023
    authors: [Babylon Labs]
    year: 2023
    date: 2023-05-07
    title: "Bitcoin Staking 101: Part 3 - Babylon's Bitcoin Staking Contract"
    venue: Babylon Labs blog
    type: company/vendor claim
    id: https://babylonlabs.io/blog/babylon-s-bitcoin-staking-contract
    url: https://babylonlabs.io/blog/babylon-s-bitcoin-staking-contract
    supports: EOTS key leakage on double-signing; timelock exit; burn-only covenant committee (N3)
  - key: belcher2019
    authors: [Chris Belcher]
    year: 2019
    date: 2019-07-13
    title: "Design for improving JoinMarket's resistance to sybil attacks using fidelity bonds"
    venue: GitHub gist
    type: essay/blog
    id: https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af
    url: https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af
    supports: timelocked/burned BTC as sybil resistance; valuation formula; attack-cost estimates (N6)
  - key: lightninglabs2026
    authors: [Lightning Labs]
    year: 2026
    date: 2026-02-11
    title: "The Agents Are Here and They Want to Transact: Powering the AI Economy with Lightning"
    venue: lightning.engineering
    type: company/vendor claim
    id: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    url: https://lightning.engineering/posts/2026-02-11-ln-agent-tools/
    supports: lnget, remote signer, scoped macaroons, per-request and node-level caps (N1)
  - key: nunchuk2026
    authors: [Nunchuk]
    year: 2026
    date: 2026-04-08
    title: "Open-source Bitcoin agents with bounded authority"
    venue: nunchuk.io blog
    type: company/vendor claim
    id: https://nunchuk.io/blog/bitcoin-agents
    url: https://nunchuk.io/blog/bitcoin-agents
    supports: 2-of-3 with agent key and policy co-signer; daily limit; human sign-off above limit (N1, N11)
  - key: precop2026
    authors: [Laz1m0v]
    year: 2026
    date: 2026-04-03
    title: "TEE-Hardened Autonomous Agent Wallet with Simplicity Pre-Execution"
    venue: Delving Bitcoin
    type: essay/blog
    id: https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377
    url: https://delvingbitcoin.org/t/tee-hardened-autonomous-agent-wallet-with-simplicity-pre-execution/2377
    supports: LLM agent under client-side covenant; 144-block CSV fallback to human multisig (N5, N11)
  - key: safeallowance
    authors: [Safe]
    year: undated (footer 2023-2026)
    title: "AI agent with a spending limit"
    venue: Safe documentation
    type: official docs
    id: https://docs.safe.global/home/ai-agent-quickstarts/agent-with-spending-limit
    url: https://docs.safe.global/home/ai-agent-quickstarts/agent-with-spending-limit
    supports: allowance module with reset interval for agent delegate (N1)
  - key: erc7715
    authors: [Luka Isailovic, Derek Rein, Dan Finlay, Derek Chiang, and others]
    year: 2024
    date: 2024-05-24 (created; Draft)
    title: "ERC-7715: Request Permissions from Wallets"
    venue: Ethereum Improvement Proposals
    type: standard/spec
    id: https://eips.ethereum.org/EIPS/eip-7715
    url: https://eips.ethereum.org/EIPS/eip-7715
    supports: allowance permissions with unix-timestamp expiry (N1, N4)
  - key: erc8370
    authors: [helmymekaoui-web, zexoverz, and other forum participants]
    year: 2026
    date: 2026-08-04 (first post); 2026-08-14 to 2026-08-26 (lease posts)
    title: "ERC-8370: Inheritable Agent Mandates (discussion thread)"
    venue: Ethereum Magicians
    type: standard/spec
    id: https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275
    url: https://ethereum-magicians.org/t/erc-8370-inheritable-agent-mandates/29275?page=3
    supports: requireLease dead-man switch, guardian renew, child subset of parent (N1, N4)
  - key: erc8004
    authors: [Marco De Rossi, Davide Crapis, Jordan Ellis, Erik Reppel]
    year: 2025
    date: 2025-08-13 (created; Draft)
    title: "ERC-8004: Trustless Agents"
    venue: Ethereum Improvement Proposals
    type: standard/spec
    id: https://eips.ethereum.org/EIPS/eip-8004
    url: https://eips.ethereum.org/EIPS/eip-8004
    supports: agent identity/reputation/validation registries; slashing out of scope (N2)
  - key: ap2google2025
    authors: [Stavan Parikh, Rao Surapaneni]
    year: 2025
    date: 2025-09-16
    title: "Powering AI commerce with the new Agent Payments Protocol (AP2)"
    venue: Google Cloud Blog
    type: company/vendor claim
    id: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
    url: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
    supports: signed Intent/Cart Mandates with price limits; x402 crypto extension (N1)
  - key: borthwick-insumer
    authors: [Douglas Borthwick]
    year: unknown (dated July 30; year not captured)
    title: "Verifying an AI Agent's Authority Before It Spends: Signed Booleans Across Six Chains"
    venue: DEV Community (InsumerAPI)
    type: company/vendor claim
    id: https://dev.to/douglasborthwickcrypto/verifying-an-ai-agents-authority-before-it-spends-signed-booleans-across-six-chains-1332
    url: https://dev.to/douglasborthwickcrypto/verifying-an-ai-agents-authority-before-it-spends-signed-booleans-across-six-chains-1332
    supports: block-anchored delegation freshness incl. Bitcoin block height; 5-minute verdict expiry (N4)
  - key: south2025deleg
    authors: [Tobin South, Samuele Marro, Thomas Hardjono, Robert Mahari, Cedric Deslandes Whitney, Dazza Greenwood, Alan Chan, Alex Pentland]
    year: 2025
    date: 2025-01-16
    title: "Authenticated Delegation and Authorized AI Agents"
    venue: arXiv
    type: preprint
    id: arXiv:2501.09674
    url: https://arxiv.org/abs/2501.09674
    supports: scoped, auditable delegation from humans to agents (N4)
  - key: taylor2026
    authors: [Jay Taylor, Paul Gerhart, Sri AravindaKrishnan Thyagarajan]
    year: 2026
    date: 2026-02-26 (received), 2026-10-29 (revised)
    title: "How To Make Delegated Payments on Bitcoin: A Question for the AI Agentic Future"
    venue: IACR ePrint 2026/395; Financial Cryptography and Data Security 2026
    type: peer-reviewed
    id: https://eprint.iacr.org/2026/395
    url: https://eprint.iacr.org/2026/395
    supports: Bitcoin-compatible proxy adaptor signatures for agent delegation; no caps or expiry
  - key: malhotra2026
    authors: [Sachin Malhotra]
    year: 2026
    title: "Give the Agent a Budget, Not a Token"
    venue: AI Engineer World's Fair 2026
    type: essay/blog
    id: https://ai.engineer/talks/rbjWzZK2LU0-give-agent-budget-not-token
    url: https://ai.engineer/talks/rbjWzZK2LU0-give-agent-budget-not-token
    supports: replenishing rate limits, undo test, human-only overrides (N5, N7, framing)
  - key: nagaraj2026
    authors: [Sriram Nagaraj, Seung Jung Lee]
    year: 2026
    date: 2026-08-23
    title: "Agentic AI Systems and Financial Stability, From Model Risk to Systemic Risk"
    venue: arXiv (q-fin.RM)
    type: preprint
    id: arXiv:2610.08806
    url: https://arxiv.org/abs/2610.08806
    supports: settlement delays as non-substitutable control on irreversible actions (N5, framing)
  - key: huang2025lw
    authors: [Qien Huang]
    year: 2025
    date: 2025-12-30
    title: "Irreversible Operations: the safety failure mode you get from shipping faster"
    venue: LessWrong (rejected post)
    type: essay/blog
    id: https://www.lesswrong.com/posts/zmRxkmXJZbo6dCaHL/irreversible-operations-the-safety-failure-mode-you-get-from
    url: https://www.lesswrong.com/posts/zmRxkmXJZbo6dCaHL/irreversible-operations-the-safety-failure-mode-you-get-from
    supports: enforced delay and dual authorization for irreversible ops (low weight)
  - key: bip345
    authors: [James O'Beirne, Greg Sanders]
    year: 2023
    date: 2023-02-03 (assigned); status Closed; replacement BIP-443
    title: "BIP-345: OP_VAULT"
    venue: bitcoin/bips
    type: standard/spec
    id: https://github.com/bitcoin/bips/blob/master/bip-0345.mediawiki
    url: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0345.mediawiki
    supports: delay period plus recovery path covenant (N5)
  - key: todd2016ots
    authors: [Peter Todd]
    year: 2016
    date: 2016-09-15
    title: "OpenTimestamps: Scalable, Trust-Minimized, Distributed Timestamping with Bitcoin"
    venue: petertodd.org
    type: essay/blog
    id: https://petertodd.org/2016/opentimestamps-announcement
    url: https://petertodd.org/2016/opentimestamps-announcement
    supports: Bitcoin timestamping; proofs of existence (N8)
  - key: ots-site
    authors: [OpenTimestamps project]
    year: undated
    title: "OpenTimestamps"
    venue: opentimestamps.org
    type: official docs
    id: https://opentimestamps.org/
    url: https://opentimestamps.org/
    supports: standard format, free calendars (N8)
  - key: todd2017seals
    authors: [Peter Todd]
    year: 2017
    date: 2017-12-05
    title: "Scalable Semi-Trustless Asset Transfer via Single-Use-Seals and Proof-of-Publication"
    venue: petertodd.org (from bitcoin-dev)
    type: essay/blog
    id: https://petertodd.org/2017/scalable-single-use-seal-asset-transfer
    url: https://petertodd.org/2017/scalable-single-use-seal-asset-transfer
    supports: single-use seal definition (N8)
  - key: fassbender2026
    authors: [Jonna Fassbender]
    year: 2026
    date: 2026-05-28 (draft-02; expires 2026-11-29)
    title: "Bitcoin-Anchored Temporal Proof for Transparency Services"
    venue: IETF Internet-Draft draft-fassbender-scitt-time-anchor-02 (individual, Informational)
    type: standard/spec
    id: draft-fassbender-scitt-time-anchor-02
    url: https://datatracker.ietf.org/doc/html/draft-fassbender-scitt-time-anchor-02
    supports: Bitcoin/OTS anchoring of SCITT receipts; AI model weights and safety evals example (N8)
  - key: rfc6962
    authors: [Ben Laurie, Adam Langley, Emilia Kasper]
    year: 2013
    date: 2013-06
    title: "Certificate Transparency"
    venue: IETF RFC 6962 (Experimental)
    type: standard/spec
    id: RFC 6962
    url: https://www.rfc-editor.org/rfc/rfc6962.txt
    supports: append-only auditable logs (N8 comparison)
  - key: rfc9162
    authors: [Ben Laurie, Eran Messeri, Rob Stradling]
    year: 2021
    date: 2021-12
    title: "Certificate Transparency Version 2.0"
    venue: IETF RFC 9162 (Experimental; obsoletes 6962)
    type: standard/spec
    id: RFC 9162
    url: https://www.rfc-editor.org/rfc/rfc9162.txt
    supports: misbehaving logs and split views (N8 comparison)
  - key: sigstore2025
    authors: [Mihai Maruseac]
    year: 2025
    date: 2025-04-04
    title: "Taming the Wild West of ML: Practical Model Signing with Sigstore"
    venue: Sigstore Blog
    type: official docs
    id: https://blog.sigstore.dev/model-transparency-v1.0
    url: https://blog.sigstore.dev/model-transparency-v1.0
    supports: model signing v1.0; transparency log against rogue insider (N8)
  - key: c2pa22
    authors: [C2PA]
    year: undated (spec 2.2; 2.3 available)
    title: "C2PA Technical Specification 2.2"
    venue: c2pa.org
    type: standard/spec
    id: https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html
    url: https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html
    supports: X.509 plus RFC 3161 time-stamps; no blockchain (N8 comparison)
  - key: cnas2024
    authors: [Onni Aarne, Tim Fist, Caleb Withers]
    year: 2024
    date: 2024-01-08
    title: "Secure, Governable Chips: Using On-Chip Mechanisms to Manage National Security Risks from AI & Advanced Computing"
    venue: Center for a New American Security
    type: essay/blog
    id: https://www.cnas.org/publications/reports/secure-governable-chips
    url: https://www.cnas.org/publications/reports/secure-governable-chips
    supports: periodically renewed licence key for chips (N9)
  - key: ogara2025hem
    authors: [Aidan O'Gara, Gabriel Kulp, and others]
    year: 2025
    date: 2025-04-02 (v1)
    title: "Hardware-Enabled Mechanisms for Verifying Responsible AI Development"
    venue: arXiv
    type: preprint
    id: arXiv:2505.03742
    url: https://arxiv.org/html/2505.03742v1
    supports: RTCs for licence expiration; secure clock; renewal trade-offs (N9)
  - key: petrie2025
    authors: [James Petrie]
    year: 2025
    date: 2025-09-09
    title: "Embedded Off-Switches for AI Compute"
    venue: arXiv
    type: preprint
    id: arXiv:2509.07637
    url: https://arxiv.org/html/2509.07637
    supports: licence-validated hardware off-switch with nonces; no blockchain (N9)
  - key: ansari2026
    authors: [Samar Ansari]
    year: 2026
    date: 2026-04-06
    title: "Hardware-Level Governance of AI Compute: A Feasibility Taxonomy for Regulatory Compliance and Treaty Verification"
    venue: arXiv
    type: preprint
    id: arXiv:2604.04712
    url: https://arxiv.org/html/2604.04712
    supports: licence renewal taxonomy; blockchain chip serialisation reference (N9)
  - key: sastry2024
    authors: [Girish Sastry, Lennart Heim, Haydn Belfield, and others]
    year: 2024
    date: 2024-02-13
    title: "Computing Power and the Governance of Artificial Intelligence"
    venue: arXiv
    type: preprint
    id: arXiv:2402.08797
    url: https://arxiv.org/html/2402.08797
    supports: compute governance canon contains no PoW or Bitcoin (N10)
  - key: ccaf2026
    authors: [Wenbin Wu]
    year: 2026
    date: 2026-05-06
    title: "Where AI meets blockchain: assets, agents and blind spots"
    venue: Cambridge Judge Business School, CCAF Perspectives
    type: essay/blog
    id: https://www.jbs.cam.ac.uk/2026/where-ai-meets-blockchain-assets-agents-and-blind-spots/
    url: https://www.jbs.cam.ac.uk/2026/where-ai-meets-blockchain-assets-agents-and-blind-spots/
    supports: miners shifting to AI (2,700 MW), hashrate dip, Bittensor revenue, no Bitcoin safety role (N10, survey)
  - key: gilliam2025
    authors: [Byron Gilliam]
    year: 2025
    date: 2025-10-22
    title: "Bitcoin's arrow of time"
    venue: Blockworks, The Breakdown
    type: essay/blog
    id: https://mail.blockworks.com/p/bitcoin-s-arrow-of-time
    url: https://mail.blockworks.com/p/bitcoin-s-arrow-of-time
    supports: '"Bitcoin might be the first form of AI time" (framing)'
  - key: gigi2021
    authors: [Gigi]
    year: 2021
    date: 2021-01-14
    title: "Bitcoin Is Time"
    venue: dergigi.com
    type: essay/blog
    id: https://dergigi.com/2021/01/14/bitcoin-is-time/
    url: https://dergigi.com/2021/01/14/bitcoin-is-time/
    supports: Bitcoin as decentralized clock; block height as time (framing)
  - key: boneh2018vdf
    authors: [Dan Boneh, Joseph Bonneau, Benedikt Buenz, Ben Fisch]
    year: 2018
    title: "Verifiable Delay Functions"
    venue: IACR ePrint 2018/601
    type: preprint
    id: https://eprint.iacr.org/2018/601
    url: https://eprint.iacr.org/2018/601
    supports: sequential-time primitive to distinguish from block-height time (framing)
  - key: szabo-bitgold
    authors: [Nick Szabo]
    year: 2005 (URL); page dated 2008-12-27
    title: "Bit gold"
    venue: Unenumerated blog
    type: essay/blog
    id: https://unenumerated.blogspot.com/2005/12/bit-gold.html
    url: https://unenumerated.blogspot.com/2005/12/bit-gold.html
    supports: unforgeable scarcity from costly creation; timestamped PoW (N10 background)
  - key: lw-simdeterrent
    authors: [John (LessWrong user)]
    year: 2025
    date: 2025-05-28
    title: "The Simulation Deterrent: Can We Nudge AI Towards Safety by Simulating Universes?"
    venue: LessWrong (rejected post)
    type: essay/blog
    id: https://www.lesswrong.com/posts/fdk6rJLkzjS3jSLYm/the-simulation-deterrent-can-we-nudge-ai-towards-safety-by
    url: https://www.lesswrong.com/posts/fdk6rJLkzjS3jSLYm/the-simulation-deterrent-can-we-nudge-ai-towards-safety-by
    supports: only PoW-for-AI-safety proposal found (low weight) (N10)
  - key: anubis2025
    authors: [Liam Proven]
    year: 2025
    date: 2025-07-09
    title: "Anubis guards gates against hordes of LLM bot crawlers"
    venue: The Register
    type: news
    id: https://www.theregister.com/2025/07/09/anubis_fighting_the_llm_hordes/
    url: https://www.theregister.com/2025/07/09/anubis_fighting_the_llm_hordes/
    supports: Hashcash-style PoW as a cost on AI crawlers (N7, N10 component)
  - key: balaji2023
    authors: [Elizabeth Licorish]
    year: 2023
    date: 2023-11-06
    title: "Balaji Srinivasan Explains How Crypto Can Combat AI-Generated Misinformation"
    venue: Chainlink Today
    type: news
    id: https://chainlinktoday.com/balaji-srinivasan-explains-how-crypto-can-combat-ai-generated-misinformation
    url: https://chainlinktoday.com/balaji-srinivasan-explains-how-crypto-can-combat-ai-generated-misinformation
    supports: '"AI Makes Everything Easy to Fake, Crypto Makes it Hard Again"; staked crypto to make bot spam costly'
  - key: dorsey2024
    authors: [Bernd Struben]
    year: 2024
    date: 2024-05-04
    title: "Buying Bitcoin? Here's why Block's Jack Dorsey says AI will drive global adoption"
    venue: The Motley Fool Australia
    type: news
    id: http://www.fool.com.au/2024/05/04/buying-bitcoin-heres-why-blocks-jack-dorsey-says-ai-will-drive-global-adoption/
    url: http://www.fool.com.au/2024/05/04/buying-bitcoin-heres-why-blocks-jack-dorsey-says-ai-will-drive-global-adoption/
    supports: Block Q1 2024 letter on bitcoin as internet's native currency; Dorsey on agents needing to transact
  - key: decrypt2024
    authors: [Jose Antonio Lanz]
    year: 2024
    date: 2024-07-10
    title: "Marc Andreessen Sends $50K in Bitcoin to an AI Bot on Twitter"
    venue: Decrypt
    type: news
    id: https://decrypt.co/239340/marc-andreessen-sends-50k-in-bitcoin-to-an-ai-bot-on-twitter
    url: https://decrypt.co/239340/marc-andreessen-sends-50k-in-bitcoin-to-an-ai-bot-on-twitter
    supports: AI agent (Truth Terminal) receiving bitcoin outside any governance scheme
  - key: bitcoinwiki-agent
    authors: [Bitcoin Wiki contributors]
    year: 2018 (last edit 2018-11-29; concept 2011)
    title: "Agent"
    venue: Bitcoin Wiki
    type: essay/blog
    id: https://en.bitcoin.it/wiki/Agent
    url: https://en.bitcoin.it/wiki/Agent
    supports: early autonomous-agent-holding-bitcoin concept
  - key: marino2025
    authors: [Bill Marino, Ari Juels]
    year: 2025
    date: 2025-07-11 (v1), 2026-02-07 (v2), 2026-08-26 (v3)
    title: "Giving AI Agents Access to Cryptocurrency and Smart Contracts Creates New Vectors of AI Harm"
    venue: arXiv; poster at NeurIPS 2026 Third Workshop on Agents in the Wild
    type: preprint
    id: arXiv:2507.08249
    url: https://arxiv.org/abs/2507.08249
    supports: counter-thesis; guardrails incl. spending limits, multisig, kill switches; METR Bitcoin wallet test
  - key: neurips2026
    authors: [NeurIPS]
    year: 2026
    title: "Giving AI Agents Access to Cryptocurrency and Smart Contracts Creates New Vectors of AI Harm (poster listing)"
    venue: NeurIPS 2026 workshop
    type: official docs
    id: https://neurips.cc/virtual/2026/168254
    url: https://neurips.cc/virtual/2026/168254
    supports: venue of Marino and Juels
  - key: allen2026survey
    authors: [Sarah Allen, Pranay Anchuri, James Austgen, and 22 others incl. Ari Juels, Andrew Miller, Ittay Eyal, Giulia Fanti, Christian Cachin, Pramod Viswanath, Matt Weinberg, Fan Zhang]
    year: 2026
    date: 2026-06-11 (v1), 2026-08-21 (v2)
    title: "Crypto x AI, AI x Crypto: A Survey"
    venue: arXiv
    type: preprint
    id: arXiv:2606.13892
    url: https://arxiv.org/abs/2606.13892
    supports: systematization; on-chain caps and rate limits; UAAs; liability perimeter; provenance misconceptions
  - key: chan2025infra
    authors: [Alan Chan, and others]
    year: 2025
    date: 2025-06-19 (v3)
    title: "Infrastructure for AI Agents"
    venue: arXiv
    type: preprint
    id: arXiv:2501.10114
    url: https://arxiv.org/html/2501.10114
    supports: commitment devices via smart contracts; oversight layers; rollbacks (N11, survey)
  - key: kinniment2023
    authors: [Megan Kinniment, Lucas Jun Koba Sato, Haoxing Du, and others incl. Elizabeth Barnes, Paul Christiano]
    year: 2023
    date: 2023-12-18 (v1), 2024-01-04 (v2)
    title: "Evaluating Language-Model Agents on Realistic Autonomous Tasks"
    venue: arXiv
    type: preprint
    id: arXiv:2312.11671
    url: https://arxiv.org/html/2312.11671
    supports: '"Create Bitcoin wallet" task in autonomy evaluation'
  - key: hu2025trustless
    authors: [Botao Amber Hu, Yuhan Liu, Helena Rong]
    year: 2025
    date: 2025-05-14 (v1), 2025-09-17 (v2)
    title: "Trustless Autonomy: Understanding Motivations, Benefits, and Governance Dilemmas in Self-Sovereign Decentralized AI Agents"
    venue: arXiv
    type: preprint
    id: arXiv:2505.09757
    url: https://arxiv.org/abs/2505.09757
    supports: agents owning wallet keys via TEEs; governance dilemma
  - key: neulinger2025
    authors: [Alexander Neulinger, Lukas Sparer]
    year: 2025
    date: 2025-10-09
    title: "Fostering AI alignment through blockchain, proof of personhood and zero knowledge proofs"
    venue: Cluster Computing (Springer)
    type: peer-reviewed
    id: doi:10.1007/s10586-025-05729-8
    url: https://doi.org/10.1007/s10586-025-05729-8
    supports: peer-reviewed blockchain alignment layer with AI shield; not Bitcoin
  - key: maleki2026hco
    authors: [Homayoun Maleki, Nekane Sainz, Jon Legarda]
    year: 2026
    date: 2026-01-07
    title: "Human Challenge Oracle: Designing AI-Resistant, Identity-Bound, Time-Limited Tasks for Sybil-Resistant Consensus"
    venue: arXiv
    type: preprint
    id: arXiv:2601.03923
    url: https://arxiv.org/abs/2601.03923
    supports: time-bound sybil resistance (N6 component)
  - key: aiuc2025fortune
    authors: [Sharon Goldman]
    year: 2025
    date: 2025-07-23
    title: "AI agent insurance startup AIUC emerges from stealth with $15 million seed"
    venue: Fortune
    type: news
    id: https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/
    url: https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/
    supports: AIUC-1 and agent insurance without blockchain (N2)
  - key: psyche2025
    authors: [Psyche Team, Nous Research]
    year: 2025
    date: 2025-05
    title: "Democratizing AI: The Psyche Network Architecture"
    venue: nousresearch.com
    type: company/vendor claim
    id: https://nousresearch.com/nous-psyche/
    url: https://nousresearch.com/nous-psyche/
    supports: censorship-resistance and "alignment" as decentralization claims
  - key: ritual-intro
    authors: [Ritual Team]
    year: unknown (page shows "2 years ago")
    title: "Introducing Ritual"
    venue: ritual.net blog
    type: company/vendor claim
    id: https://ritual.net/blog/introducing-ritual
    url: https://ritual.net/blog/introducing-ritual
    supports: integrity, privacy, censorship-resistance SLA claims
  - key: gensyn-litepaper
    authors: [Gensyn]
    year: undated (legacy)
    title: "Gensyn Litepaper (legacy)"
    venue: docs.gensyn.ai
    type: company/vendor claim
    id: https://docs.gensyn.ai/litepaper
    url: https://docs.gensyn.ai/litepaper
    supports: verification of ML work; no safety claims
  - key: bittensor-docs
    authors: [Bittensor / Opentensor]
    year: undated
    title: "Bittensor Documentation"
    venue: docs.learnbittensor.org
    type: official docs
    id: https://docs.learnbittensor.org/learn/introduction
    url: https://docs.learnbittensor.org/learn/introduction
    supports: open subnet network paid in TAO; no safety claims on page
```
