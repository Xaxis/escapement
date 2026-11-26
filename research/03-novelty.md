# What is new, and what is not

Every claimed contribution in [04-claims.md](04-claims.md), set against the closest prior work, with
a verdict. Three verdicts are used:

- **Prior work**: the same idea exists. Escapement uses it and credits it; it is not a contribution.
- **Extends prior work**: the mechanism or result exists, and the claim adds a stated element (a
  purpose, a combination, a bound) that the searches did not find. The contribution is that element
  only.
- **New, as far as two searches found**: neither independent search found it. That is a statement
  about the searches, which are listed, not about the world.

A claim can also be **cut**: it failed a level of verification as stated, so it is no longer claimed,
whatever its novelty.

## After the fresh reviewer

On 2026-11-26 a last reviewer that had seen none of the work, and had not read this file, ran its
own searches and checks on the eight claims still standing (C1 to C8 of
[06-verification.md](06-verification.md)). Its report, with every quote it re-fetched, is
`research/notes/fresh-eyes.md`. It found prior work the first two searches missed for five of them,
and two breaks on regtest (`lab/fresh_eyes.py`). Where it disagrees with the sections below, it
supersedes them. **Nothing in the program is new.**

| Claim | Final verdict | Prior work the reviewer found | Works, per the reviewer |
|---|---|---|---|
| C1 one complete record as standing, training reward and release gate (core, K1) | **Cut** as a contribution; the assembly extends prior work only as an assembly | On-chain forecasting credential [@nechepurenko2026]; stake-backed agent ledgers [@chaffer2025abt; @tomasev2026delegation]; silence scored as the worst outcome [@infinite-games]; costly stakes against lucky accounts [@craib2021numerai] | **No, as stated.** Nothing on chain binds a tick chain to its bond: one charter id carried two chains on regtest, each accepted from its own pin. Standing (the round rule) and the training reward (a proper score) ask for different reports from the same leaves |
| C2 fake-record bound K/λ, priced πλ·c_id (K2) | **Prior work** | Testing by betting from a unit stake [@shafer2021]; averaging e-values [@vovk2021]; Ville's inequality [@ville1939] and a union bound; comparative testing of experts [@alnajjar2008]; comparing sequential forecasters [@choe2024]; stakes against lucky accounts [@craib2021numerai] | **Only under stronger hypotheses than stated**: the agent's forecasts must use public information alone and its actions must not move outcomes. With more than one claim a round, the round rule is a betting score, not a proper score |
| C3 training reward neither agent nor lab can select (K4, claim 2) | **Cut** | RL on resolved outcomes [@turtel2025; @han2026futureworld]; proper-score RL [@damani2025; @banioharouni2025]; sealed, delayed-disclosure evaluation against selective reporting [@cheng2025peerbench] | **No, for the lab.** It can commit many definitions under many identities, and nothing binds what it actually trains on. The agent side is the textbook proper-score result |
| C4 two-sided adoption with seed readers (K5) | **Prior work**, applied | Critical mass on platforms [@evans2010platform; @farrell1985]; insulating tariffs that remove the bad equilibrium [@weyl2010] | **As a toy model.** The algebra and simulation check; a > 8c belongs to uniform types and costs, and nothing is measured |
| C5 the tick chain (K7) | **Extends prior work narrowly** | Spacechains: a chain of spends, one per block, under a NUMS key tweaked by a commitment [@somsen-spacechains]; Revault's cancel [@revault-intro]; BitVM2's challenge window [@bitvm2-bridge]; Catena [@catena-2017] | **With its stated limits, per pinned chain, not per identity**, until a binding of chain to bond is specified and built (proposed: identity = bond outpoint, T_0 a named output of the bond's own transaction; unbuilt, and it collides with renewing the bond). The agent can outbid a veto at the window's edge with outside money: on regtest a child paying 150,000 sats beat a veto when T_n held 100,000 |
| C6 the height-difference lease (K8) | **Prior work** | Substrate's mortal transactions, a signature over a block hash valid only for inclusion in a window after it [@substrate-mortality]; short leashes [@yee2022] | **Yes**, as stated (Proposition 6 and the lab's 7 lease checks) |
| C7 the clock's cost below a majority (K9a) | **Prior work** | Proof of work as a clock [@trubetskoy2018]; releases timed by proof of work [@yang2022] | **Arithmetic right, not load-bearing**: reorganisations and bribery beat the waits more cheaply than running the clock fast |
| C8 blockspace as an aggregate limit (K9b) | **Prior method**, applied | Capacity arithmetic for channel opens, as in the Lightning-era estimates | **Arithmetic right**, and its real meaning is a scaling ceiling: about 44,000 identities releasing every window would fill every block |

The sections below record the first two searches as they were run. Their statements that something
"was not found" are corrected inline where the reviewer found it.

## How the searches were run

After the core was recentred on 2026-11-26, two helpers that had not come up with the ideas searched
for each claim independently. Each read only `04-claims.md`, not the design or the author's earlier
novelty case, and was told that finding prior art was success. Searcher A covered K1 to K6 across
papers, economics, forecasting, AI-agent standards, crypto designs and AI-governance writing;
searcher B covered K7 to K9 across BIPs, the bitcoin-dev list, Delving Bitcoin, Optech, Lightning,
vault designs, single-use seals, Ethereum delay modules, DID methods, patents and the
hardware-governance literature. Their full reports, with every query and quote, are
`research/notes/novelty-independent-a.md` and `research/notes/novelty-independent-b.md`. Both
stated their gaps: A did not query Google Scholar or Google Patents directly and skipped dedicated
searches of ethresear.ch, Delving Bitcoin, Optech, Kleros, UMA, Truthcoin and the publication lists
of GovAI, CSET, RAND, IAPS and CAIS; B's patent search found only loose matches. A "not found" below
inherits those gaps.

## The summary

No single mechanism or theorem in Escapement is new. Every part has a precedent, most of them close:

- **Standing from a tamper-proof record backed by a stake** is proposed for AI agents already
  [@chaffer2025abt; @tomasev2026delegation], and an on-chain forecasting credential for AI agents
  that "cannot be selectively reported or retroactively modified" exists [@nechepurenko2026].
- **The logic of the fake-record bound** is Resnick and Sami's influence limiter: reputation as
  score gained over the prior prediction, so uninformed sybils gain little, with identity creation
  made costly [@resnick2007]. The likelihood-ratio test is game-theoretic probability
  [@shafer2021], the bound is Ville's [@ville1939], and the many-identities attack is mutual fund
  incubation [@evans2010].
- **Training with proper-score rewards yields calibration**, proved and demonstrated in 2025
  [@banioharouni2025; @damani2025]; rewards from real-world outcomes exist [@turtel2025;
  @han2026futureworld]; selective participation distorting forecasters is known [@sempere2021;
  @witkowski2021].
- **Unraveling, critical mass and lemons** are textbook [@milgrom1981; @grossman1981;
  @jovanovic1982; @farrell1985; @akerlof1970], and getting a few early adopters to move AI
  identity standards is a GovAI recommendation [@chan2024ids].
- **Stakes that bind agents of unknown goals** are the premise of the AI-dealmaking literature
  [@salib2024], which already notes the resource-seeking tension.
- **The tick chain's parts** are Revault's single-watchtower cancel [@revault-intro], vaults
  [@swambo2020], Catena's and Pikachu's chains of spends [@catena-2017; @azouvi2022], single-use
  seals [@todd-2017], and BitVM's later-spend-proves-no-challenge connectors [@bitvm2-bridge];
  its key construction and per-block rate limit are in Somsen's spacechains [@somsen-spacechains]
  (found by the fresh reviewer).
- **The lease's predicate**, a block named by height and hash plus a window, is Yee's "short
  leashes" [@yee2022], and a Bitcoin-height freshness window checked by verifiers exists
  [@zeke2026]; checking it against the inclusion height is Substrate's mortal transactions
  [@substrate-mortality] (found by the fresh reviewer).

What neither of the first two searches found is the **integration**, and three narrow elements.
*Superseded:* the fresh reviewer found prior work for most of them, and each item below now carries
its correction.

1. **One record that is at once an agent's standing, its training reward and its release
   mechanism**, made complete against an operator running many identities by consensus (one chain
   per costly identity, gapless, one root per index) and by the scoring rules (silence scores as
   failure, one forecast per event). Foresight Arena's credential is closest, and its sybil
   resistance is rate limiting, so the incubation attack stays open there [@nechepurenko2026].
   *Corrected:* silence scored as the worst outcome is prior work [@infinite-games]. The assembly
   of three roles in one record was still not found, but it fails as stated: one chain per costly
   identity holds only for a pin agreed off chain, and the three roles ask for different reports.
   **Cut** as a contribution.
2. **The explicit cost bound for faking a record under costly identities**, πλ·c_id, priced with a
   Bitcoin bond. Its logic is Resnick and Sami's; the closed form and its pricing are the addition.
   *Corrected:* the closed form is a union bound on Ville's inequality, the round rule is Shafer's
   betting from a unit stake [@shafer2021] with Vovk and Wang's averaging [@vovk2021], and stakes
   priced against lucky accounts are Numerai's [@craib2021numerai]. **Prior work.**
3. **Blockspace as an aggregate limit on the release rate of AI agents' commitments**. Searcher B
   found only capacity worries. Its value as a safety limit is weak (section "The table").
   *Corrected:* the method is the old capacity arithmetic, applied; what it shows is a scaling
   ceiling for the design. **Prior method.**
4. **Two narrow mechanism elements**: the tick chain's purpose, rate-limiting and vetoing releases of
   off-chain commitments, and the lease's renewal signed by every guardian and checked against the
   release's confirmation height rather than the verifier's tip. *Corrected:* the tick chain's key
   construction and per-block rate limit are in Somsen's spacechains, there enforced by a covenant
   [@somsen-spacechains]; its covenant-free version with a Revault-style cancel, applied to
   off-chain commitments, still extends prior work narrowly. A signature over a block hash, checked
   against the inclusion height, is Substrate's mortal transactions [@substrate-mortality], so the
   lease is **prior work**; a renewal signed by every guardian is an n-of-n signer.

## The table, after the first two searches

Superseded where the reviewer disagreed; the final verdicts are in "After the fresh reviewer".

| Claim | Closest prior work | Verdict |
|---|---|---|
| **Core proposition**: standing from an unforgeable record under costly identity; honesty cheapest; adoption by choice | Agent standing from immutable records and stakes [@chaffer2025abt; @tomasev2026delegation]; on-chain forecasting credential [@nechepurenko2026]; agent reputation registries [@erc8004] | **Extends prior work.** The integration in item 1 above was not found. *Superseded: cut (C1)* |
| **K1** the complete record: non-backdatable, non-forkable, non-omittable, costly to multiply | Anchoring and non-equivocation [@todd-ots-2016; @catena-2017]; Merkle-sum trees in Taproot Assets; costly identities [@belcher-2019; @friedman2001] | **Extends prior work.** Each property is prior; the assembly, and silence scored as failure for the charter's maximum leaves, were not found. *Superseded: silence scored as the worst outcome is prior work [@infinite-games]; non-forkable and costly to multiply hold only per pinned chain* |
| **K2** fake-record cost bound πλ·c_id | Influence limiter [@resnick2007]; testing by betting [@shafer2021]; Ville [@ville1939]; incubation [@evans2010]; record gaming by hidden tail risk [@foster2010] | **Extends prior work**, close to prior. The closed form with a costly identity is the addition. *Superseded: prior work (C2)* |
| **K3** bonded promises, honesty cheapest with complete records | Reputation enforcement [@klein1981; @shapiro1983]; cheap pseudonyms [@friedman2001]; exit scams by AI agents [@gatta2026] | **Prior work.** Cut as a contribution; kept as a building block |
| **K4** training on complete records | Proper-score RL yields calibration [@banioharouni2025; @damani2025]; outcome rewards [@turtel2025; @han2026futureworld]; reward tampering [@everitt2019]; selective participation [@sempere2021] | **Claim 1 prior work. Claim 2 extends prior work**: a reward channel that neither agent nor lab can select was not found. *Superseded: claim 2 cut (C3); the lab can select* |
| **K5** adoption: unraveling, tipping point, routing around | [@milgrom1981; @grossman1981; @jovanovic1982; @farrell1985; @akerlof1970; @chan2024ids] | **Prior work** (one-sided), **extends prior work** (two-sided and routing around applied to AI agents), and **downgraded** by the simulation: routing around becomes costly only where business can move. *Superseded: routing around cut; two-sided adoption is prior work applied [@evans2010platform; @weyl2010] (C4)* |
| **K6** a neutral unit and clock | Fixed supply [@nakamoto2008]; emission-paid AI networks [@rao2020bittensor]; AI dealmaking and property rights [@salib2024] | **Prior work** for (a) and (c); (b) is a general blockchain property, its rival-labs framing not found. An argument, not a contribution |
| **K7** the tick chain | Single-watchtower cancel [@revault-intro]; vaults [@swambo2020]; chains of spends [@catena-2017; @azouvi2022]; single-use seals [@todd-2017]; connectors [@bitvm2-bridge]; consensus rate limits on money [@chia-rl-wallet]; per-identity message limits [@rln-docs] | **Extends prior work.** Its use to rate-limit and veto releases of off-chain commitments was not found. *Superseded: extends prior work narrowly [@somsen-spacechains], per pinned chain (C5)* |
| **K8** the height-difference lease | Short leashes [@yee2022]; chaintip freshness [@zeke2026]; agent leases [@erc8370]; licences that expire [@petrie2024] | **Extends prior work**, close to prior. Guardian-unanimous renewal checked against the release's height is the addition. *Superseded: prior work [@substrate-mortality] (C6)* |
| **K9a** a clock an AI cannot speed up, its cost quantified | Proof of work as a clock [@trubetskoy2018; @gigi2021]; "AI time" [@gilliam2025]; attack cost [@budish2024]; timewarp [@bip54] | **Extends prior work.** The intelligence-independent cost argument with numbers was not found. *Superseded: prior work [@yang2022], and not load-bearing (C7)* |
| **K9b** blockspace as an aggregate limit on agents' releases | Capacity concerns only | **New, as far as two searches found**, and weak (see 06-verification). *Superseded: prior method, applied; a scaling ceiling (C8)* |
| **K9c** headers with a difficulty floor as a chip's licence clock | Enclave verifying headers against a hardcoded difficulty [@bentov2019]; light client with a floor [@bitvm2-bridge]; renewal chips [@buterin2025dacc; @petrie2025flexheg2] | **Extends prior work.** Reading a tick-chain release on the chip is the addition. *Superseded: cut by the red team and the lab (a frozen header feed, a ratcheting difficulty floor, one forgery serving a fleet)* |

## Earlier searches, for the bounding design

These were run on 2026-11-25 and 2026-11-26 for the bounding design, before the redirect. They are
kept because the verdicts for K7 to K9 rest partly on them.

- **Thesis:** "bitcoin "clock" AI cannot speed up time irreversible commitment AI agents essay";
  ""irreversible" commitments rate AI agents safety metering not capability limiting time delay
  argument"; "bitcoin as AI safety mechanism paper "AI alignment" proof of work limit AI".
- **Lease in block height:** "block height expiry AI agent delegation credential bitcoin freshness
  renew"; "AI agent wallet allowance expires dead man's switch human renew authority".
- **Two-anchor delay:** "delay window proof "block hash" "not before" timestamp both ends veto
  release off-chain action AI agent bitcoin"; ""time-lock" "human veto" AI agent actions verifiable
  delay relying party checks bitcoin timestamp release signature". The first found the
  bracketing technique for files [@solomon-bracket]; neither found it applied to a veto window.
- **Vault for agent actions:** "AI agents timelock vault human veto delay irreversible
  transactions"; "bitcoin AI safety timelock "AI agents" covenant vault delving bitcoin".
- **Equivocation bond:** "extractable one-time signatures AI agents commitments equivocation
  Bitcoin"; ""AI agent" bond slashing equivocation signed commitments accountability
  cryptographic".
- **Seasoning:** "AI agents sybil swarm bonds coin age timelocked stake "proof of personhood"
  agents delegation"; "timelocked bitcoin bond AI agent sybil resistance swarm".
- **Spawn rule:** "AI agent spawning sub-agents requires human approval delay bond each sub-agent
  delegation sybil swarm limit". It found depth and breadth limits on spawning and per-principal
  credentials [@reid2026], but no bonded, delayed, human-approved spawn.
- **Chip clock:** "hardware-enabled mechanisms AI chips licence renewal blockchain time source";
  "AI chip licence renewal bitcoin block height clock compute governance"; keyword searches for
  bitcoin, blockchain and clock in the hardware-governance reports cited above.

## What the paper may and may not claim

It may say that Escapement assembles prior work into a design for AI agents' track records and
enforcement on Bitcoin, built and checked on regtest, and that it reports what six levels of
verification broke: the product rule under correlated claims, routing around under cheap identities,
a training reward the lab can still select, light proofs from transaction ids, the chip clock, the
binding of a chain to its identity and the bound on the agent's bid at a veto's edge. It may name one
contribution, the covenant-free tick chain, as extending prior work narrowly, with its properties
holding per pinned chain, and it may present the fake-record bound, the training result, the
adoption model, the lease, the clock's cost and the blockspace ceiling as prior work applied, each
with its conditions.

It may not claim any mechanism or theorem as new, the integration as working, a training reward the
lab cannot select, a lease or clock argument as its own, or any evidence that the design makes an AI
system safer. The Bitcoin pieces run on regtest; nothing has been deployed or tested against a real
adversary.
