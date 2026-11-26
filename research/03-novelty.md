# What is new, and what is not

Every claimed contribution in [04-claims.md](04-claims.md), set against the closest prior work, with
a verdict. Three verdicts are used:

- **Prior work**: the same idea exists. Escapement uses it and credits it; it is not a contribution.
- **Extends prior work**: the mechanism or result exists, and the claim adds a stated element (a
  purpose, a combination, a bound) that the searches did not find. The contribution is that element
  only.
- **New, as far as two searches found**: neither independent search found it. That is a statement
  about the searches, which are listed, not about the world.

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
  seals [@todd-2017], and BitVM's later-spend-proves-no-challenge connectors [@bitvm2-bridge].
- **The lease's predicate**, a block named by height and hash plus a window, is Yee's "short
  leashes" [@yee2022], and a Bitcoin-height freshness window checked by verifiers exists
  [@zeke2026].

What neither search found is the **integration**, and three narrow elements:

1. **One record that is at once an agent's standing, its training reward and its release
   mechanism**, made complete against an operator running many identities by consensus (one chain
   per costly identity, gapless, one root per index) and by the scoring rules (silence scores as
   failure, one forecast per event). Foresight Arena's credential is closest, and its sybil
   resistance is rate limiting, so the incubation attack stays open there [@nechepurenko2026].
2. **The explicit cost bound for faking a record under costly identities**, πλ·c_id, priced with a
   Bitcoin bond. Its logic is Resnick and Sami's; the closed form and its pricing are the addition.
3. **Blockspace as an aggregate limit on the release rate of AI agents' commitments**. Searcher B
   found only capacity worries. Its value as a safety limit is weak (section "The table").
4. **Two narrow mechanism elements**: the tick chain's purpose, rate-limiting and vetoing releases of
   off-chain commitments, and the lease's renewal signed by every guardian and checked against the
   release's confirmation height rather than the verifier's tip.

## The table

| Claim | Closest prior work | Verdict |
|---|---|---|
| **Core proposition**: standing from an unforgeable record under costly identity; honesty cheapest; adoption by choice | Agent standing from immutable records and stakes [@chaffer2025abt; @tomasev2026delegation]; on-chain forecasting credential [@nechepurenko2026]; agent reputation registries [@erc8004] | **Extends prior work.** The integration in item 1 above was not found |
| **K1** the complete record: non-backdatable, non-forkable, non-omittable, costly to multiply | Anchoring and non-equivocation [@todd-ots-2016; @catena-2017]; Merkle-sum trees in Taproot Assets; costly identities [@belcher-2019; @friedman2001] | **Extends prior work.** Each property is prior; the assembly, and silence scored as failure for the charter's maximum leaves, were not found |
| **K2** fake-record cost bound πλ·c_id | Influence limiter [@resnick2007]; testing by betting [@shafer2021]; Ville [@ville1939]; incubation [@evans2010]; record gaming by hidden tail risk [@foster2010] | **Extends prior work**, close to prior. The closed form with a costly identity is the addition |
| **K3** bonded promises, honesty cheapest with complete records | Reputation enforcement [@klein1981; @shapiro1983]; cheap pseudonyms [@friedman2001]; exit scams by AI agents [@gatta2026] | **Prior work.** Cut as a contribution; kept as a building block |
| **K4** training on complete records | Proper-score RL yields calibration [@banioharouni2025; @damani2025]; outcome rewards [@turtel2025; @han2026futureworld]; reward tampering [@everitt2019]; selective participation [@sempere2021] | **Claim 1 prior work. Claim 2 extends prior work**: a reward channel that neither agent nor lab can select was not found |
| **K5** adoption: unraveling, tipping point, routing around | [@milgrom1981; @grossman1981; @jovanovic1982; @farrell1985; @akerlof1970; @chan2024ids] | **Prior work** (one-sided), **extends prior work** (two-sided and routing around applied to AI agents), and **downgraded** by the simulation: routing around becomes costly only where business can move |
| **K6** a neutral unit and clock | Fixed supply [@nakamoto2008]; emission-paid AI networks [@rao2020bittensor]; AI dealmaking and property rights [@salib2024] | **Prior work** for (a) and (c); (b) is a general blockchain property, its rival-labs framing not found. An argument, not a contribution |
| **K7** the tick chain | Single-watchtower cancel [@revault-intro]; vaults [@swambo2020]; chains of spends [@catena-2017; @azouvi2022]; single-use seals [@todd-2017]; connectors [@bitvm2-bridge]; consensus rate limits on money [@chia-rl-wallet]; per-identity message limits [@rln-docs] | **Extends prior work.** Its use to rate-limit and veto releases of off-chain commitments was not found |
| **K8** the height-difference lease | Short leashes [@yee2022]; chaintip freshness [@zeke2026]; agent leases [@erc8370]; licences that expire [@petrie2024] | **Extends prior work**, close to prior. Guardian-unanimous renewal checked against the release's height is the addition |
| **K9a** a clock an AI cannot speed up, its cost quantified | Proof of work as a clock [@trubetskoy2018; @gigi2021]; "AI time" [@gilliam2025]; attack cost [@budish2024]; timewarp [@bip54] | **Extends prior work.** The intelligence-independent cost argument with numbers was not found |
| **K9b** blockspace as an aggregate limit on agents' releases | Capacity concerns only | **New, as far as two searches found**, and weak (see 06-verification) |
| **K9c** headers with a difficulty floor as a chip's licence clock | Enclave verifying headers against a hardcoded difficulty [@bentov2019]; light client with a floor [@bitvm2-bridge]; renewal chips [@buterin2025dacc; @petrie2025flexheg2] | **Extends prior work.** Reading a tick-chain release on the chip is the addition |

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

It may say that Escapement integrates known parts into one design in which a single record, complete
against many identities by Bitcoin's consensus and by four scoring rules, serves as an AI agent's
standing, as a training reward neither the agent nor the lab can select, and as the gate on its
consequential actions; that it derives the cost of faking such a record; and that it gives the
conditions under which adopting it pays. It may name the items in "What neither search found" as its
contributions, each with its closest prior work beside it and its result at every level of
verification in [06-verification.md](06-verification.md).

It may not claim any mechanism or theorem as new, any part marked prior work, or any evidence that
the design makes an AI system safer. The Bitcoin pieces run on regtest; nothing has been deployed
or tested against a real adversary.
