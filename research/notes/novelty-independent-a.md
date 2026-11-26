# Independent prior-art search A: the core proposition and K1 to K6

Searcher: independent helper, 2026-11-26. Scope: the core proposition and claims K1 to K6 of
`research/04-claims.md`. K7 to K9 belong to another searcher. In line with the brief, the only repo
file I read was `research/04-claims.md`. I did not open `03-novelty.md`, `02-design.md`,
`research/notes/` or `paper/`.

## How to read this

- **Verdicts.** PRIOR: the same idea exists. PARTIAL: the same mechanism for another purpose, or a
  component, or the same idea without a key element. NOT FOUND: nothing close turned up in my search.
  "Not found" describes my search and nothing more. Each section lists the searches I ran.
- **Quotes.** Every quote below was checked character for character against the text of the page or
  PDF I fetched (curl plus pdftotext, or the arXiv abstract page), not taken from a search engine
  summary. Quotes are kept under 30 words. Where I could not read a primary source, I say so and
  give no quote.
- **Dates.** Many of the closest sources are from 2025 and 2026. Dates are the arXiv v1 date or the
  date shown on the page.
- **Method limits.** I searched through a general web search engine (standard and extended modes),
  read arXiv abstract and HTML pages directly, and downloaded PDFs where they were open. I did not
  query Google Scholar or Google Patents through their own interfaces: a `site:patents.google.com`
  query returned no patent pages, so my patent coverage comes from general searches that turned up
  USPTO full-text PDFs. Venues I did not search on their own are listed at the end.

## Summary table

| Claim | Verdict | Closest prior work (detail below) |
|---|---|---|
| Core proposition | PARTIAL (close) | Chaffer 2025 (AgentBound Tokens); Tomasev, Franklin, Osindero 2026 (Intelligent AI Delegation); Nechepurenko and Shuvalov 2026 (Foresight Arena); Friedman and Resnick 2001 |
| K1 complete record under costly identity | PARTIAL | Belcher 2019 (fidelity bonds); Tomescu and Devadas 2017 (Catena); IETF draft "The Agent Record" 2026; Foresight Arena 2026; Grossman/Milgrom skeptical inference via Dranove and Jin 2010 |
| K1 (a) non-backdatable | PRIOR | OpenTimestamps-anchored forecast records (Jyotish 2026); Catena |
| K1 (b) non-forkable | PRIOR | Catena 2017 |
| K1 (c) non-omittable | PARTIAL | Agent Record draft 2026; Foresight Arena; proof of liabilities (Ji and Chalkias 2021); Merkle-sum trees (Taproot Assets) |
| K1 (d) costly to multiply | PRIOR | Belcher 2019; Friedman and Resnick 2001; Margolin and Levine 2008; paygress-cli 2026 |
| K2 fake-record cost bound | PARTIAL, close to PRIOR | Resnick and Sami 2007 (Influence Limiter); Stewart 2011; Shafer 2021; Evans 2010 (fund incubation); Margolin and Levine 2008 |
| K2 consequence (single crossing; a bond alone cannot separate) | PRIOR | Signalling theory; paygress-cli 2026 states it outright |
| K3 honesty cheapest for bonded promises | PRIOR | Klein and Leffler 1981; Chaffer 2025; Tomasev et al. 2026; ERC-8267; Gatta et al. 2026 for the end-game failure |
| K4 claim 1 (proper score gives calibration; selective records distort) | PRIOR | Bani-Harouni et al. 2025; Damani et al. 2025; Sempere and Lawsen 2021; Witkowski et al. 2018/2023 |
| K4 claim 2 (channel neither agent-written nor lab-selected) | PARTIAL | Everitt et al. 2019/2021; Bostrom 2014 via Grace 2014; Turtel et al. 2025; FutureWorld 2026; Keita and Homan 2026; Vaccaro 2026 |
| K5 one-sided unraveling | PRIOR (the claim credits it) | Grossman 1981, Milgrom 1981, Jovanovic 1982, Viscusi 1978, via Dranove and Jin 2010 |
| K5 two-sided tipping | PARTIAL | Farrell and Saloner 1985; Gill, Schapira, Goldberg 2011; Chan et al. 2024; AIUC 2025 |
| K5 routing around | PRIOR as economics, PARTIAL for AI | Creane, Jeitschko, Sim 2019; Chan et al. 2024 |
| K6 (a) unit nobody can issue | PRIOR | Nakamoto 2008; contrast with Rao et al. 2020 (Bittensor) and ETHOS |
| K6 (b) shared records without a rival's registry | PRIOR as a blockchain property; rival-state framing NOT FOUND | Catena; Agent Record draft; ETHOS |
| K6 (c) stakes bind agents with unknown goals | PRIOR / PARTIAL | Omohundro 2008 and Bostrom 2012 (via Benson-Tilsen and Soares 2016); Finnveden 2025; Stastny et al. 2025; Nardo 2025; Salib and Goldstein 2026 |

---

## Core proposition

> An AI agent's standing should be computed from an unforgeable track record: complete, ordered,
> non-backdatable, under one identity that costs locked bitcoin. Honest calibrated behaviour then
> becomes the cheapest way to earn standing, labs can train on rewards from such records, and
> adoption follows by unraveling.

**Verdict: PARTIAL, and close.** "Standing for AI agents computed from a tamper-proof record of past
behaviour, backed by a stake that misconduct forfeits" is already proposed, several times, in 2025
and 2026. What I did not find anywhere is the combination of (i) completeness enforced against
an agent that runs many identities, (ii) a quantitative cost to fake a record, (iii) the same record
used as a training reward, and (iv) an adoption argument by unraveling. Bitcoin specifically shows
up only in practitioner work (OpenTimestamps-anchored forecasts, a Nostr compute marketplace).

**Closest sources**

1. Tomer Jordi Chaffer, "Governing the Agent-to-Agent Economy of Trust via Progressive
   Decentralization" (v1), later "Can We Govern the Agent-to-Agent Economy?", arXiv:2501.16606,
   28 Jan 2025. https://arxiv.org/abs/2501.16606
   - "AgentBound Tokens (ABTs), non-transferable cryptographic credentials that bind AI agents to
     immutable records of their behavior, performance, and compliance."
   - "By staking ABTs as collateral for autonomous actions within an agent-to-agent network via a
     proof-of-stake mechanism, agents may be incentivized towards ethical behavior"
   - Overlap: identity bound to an immutable behaviour record, stake as collateral, privileges earned
     through the record ("earning privileges through proven reliability" appears in the v1 text).
     Missing: completeness, any cost bound, Bitcoin, training, adoption dynamics. It is a
     philosophical agenda (its v2 abstract says "In this philosophical exploration").
2. Nenad Tomasev, Matija Franklin, Simon Osindero, "Intelligent AI Delegation", arXiv:2602.11865,
   12 Feb 2026. https://arxiv.org/abs/2602.11865
   - "Reputation serves as a predictive signal, derived from an aggregated and verifiable history of
     past actions"
   - "The immutability of the ledger would prevent tampering with an agent's history, providing a
     reliable foundation for its reputation."
   - "the delegatee is required to post a financial stake into the escrow prior to execution,
     ensuring rational adherence."
   - It also names the selection attack: "an agent can inflate its reputation by only accepting
     simple, low-risk tasks."
   - Overlap: ledger-backed history as reputation, staked escrow, awareness of selection gaming.
     Missing: a completeness rule, costly identity as the anti-sybil device (it points to web of
     trust and verifiable credentials instead), any bound.
3. Maksym Nechepurenko, Pavel Shuvalov, "Foresight Arena: An On-Chain Benchmark for Evaluating AI
   Forecasting Agents", arXiv:2605.00420, 1 May 2026. https://arxiv.org/abs/2605.00420
   - "We propose the notion of an on-chain forecasting credential: a tamper-proof, independently
     verifiable, cumulative performance record that cannot be selectively reported or retroactively
     modified."
   - "we expect such credentials to become a standard component of AI agent procurement."
   - Overlap: the record (commit-reveal on chain, before resolution), scoring against a market
     baseline (its Alpha Score), standing in procurement. Missing: costly identity. Its only sybil
     defence is relayer rate limiting, "providing Sybil resistance without staking", so one operator
     with many wallets can run the incubation attack that K1 (d) and K2 address.
4. Nenad Tomasev et al., "Virtual Agent Economies", arXiv:2509.10147, 12 Sep 2025.
   https://arxiv.org/abs/2509.10147
   - "their accumulated reputation reinforces their standing and desirability within the ecosystem."
   - "immutable, cryptographically-secured ledgers that provide a tamper-proof record of all agent
     actions"
5. Eric Friedman, Paul Resnick, "The Social Cost of Cheap Pseudonyms", Journal of Economics and
   Management Strategy 10(2), 2001. https://presnick.people.si.umich.edu/papers/identifiers/index.html
   - "there is an inherent social cost in making the spread of reputations optional."
   - "We discuss the use of entry fees, which permit newcomers to be trusted but exclude some players
     with low payoffs"
   - Overlap: the economic core of "complete record plus costly identity", 25 years earlier and not
     about AI.
6. Industry standards and drafts: ERC-8004 "Trustless Agents" (De Rossi, Crapis, Ellis, Reppel,
   created 2025-08-13, https://eips.ethereum.org/EIPS/eip-8004) has identity and feedback registries
   but no identity cost and says "Sybil attacks are possible, inflating the reputation of fake
   agents." ERC-8267 (draft, created 2026-05-19, https://eip.tools/eip/8267) lets agents "stake ETH
   to earn initial trust". Vendor designs (Armalo, MolTrust) are under K1 and K2.

**What the proposition adds over these.** All the closest proposals treat the record as feedback or
history and treat stake as collateral; none states a completeness rule that survives multiple
identities, prices a fake record, or uses the record as an RL reward. The "adoption is chosen"
half has only informal precedents (Foresight Arena's procurement expectation; Chan et al. on
incentivising ID adoption, under K5).

---

## K1. The complete record under costly identity

**Overall verdict: PARTIAL.** Each part exists. I did not find them assembled: a bonded identity,
one consensus-enforced gapless chain per identity, a committed leaf count, and worst-case scoring of
undisclosed leaves.

### Identity (timelocked Taproot bond, NUMS key, charter-committing leaf, seasoning)

**Verdict: PARTIAL.** Costly identity from timelocked bitcoin is PRIOR (JoinMarket fidelity bonds).
Binding one output to one identity is partly prior (signature binding in paygress). The in-script
binding (NUMS internal key plus a leaf committing to the charter id) and the seasoning rule I did
not find in a Bitcoin bond design. They read as engineering details, not a new idea.

- Chris Belcher, "Design for improving JoinMarket's resistance to sybil attacks using fidelity
  bonds", GitHub gist and bitcoin-dev post, July 2019.
  https://gist.github.com/chris-belcher/18ea0e6acdb885a2bfbdee43dcd6b5af
  - "a fidelity bond is a mechanism where bitcoin value is deliberately sacrificed to make a
    cryptographic identity expensive to obtain."
  - It names CLTV timelocked addresses as one form. It values bonds by amount and lock time. It
    has no one-bond-per-identity rule; it relies on makers having "a strong incentive to lump up
    all their coin sacrifices together into one maker bot".
- paygress-cli 0.1.9, `src/stake.rs` (docs.rs page dated 22 November 2026).
  https://docs.rs/paygress-cli/0.1.9/src/paygress/stake.rs.html
  - "Publishing a `StakeProof` in a public Nostr offer permanently links a Bitcoin UTXO to the
    provider's Nostr identity."
  - "`provider_npub` is bound into the message so a stake proof cannot be replayed across Nostr
    identities"
  - "Stake ranking score: `log(sats × locked_seconds)`."
  - Overlap: a timelocked bitcoin UTXO as the identity bond of a provider in an automated
    marketplace (compute), with a reputation score and social slashing. Not AI-agent specific.
- Seasoning analogue: Steven Johnson, "Deliberative Curation: A Protocol for Multi-Agent Knowledge
  Bases", arXiv:2606.00007, 27 Mar 2026. Newcomer agents start at the lowest tier, and the
  time-in-tier rule means "(each Sybil must wait before gaining influence)". A waiting time, not a
  bond age.
- Bitcoin DIDs (did:btcr2, did:btc1): anchor a DID's history to Bitcoin, but the specification
  pages I found mention no cost, reputation or track record. https://dcdpr.github.io/did-btcr2/

### Record (one tick chain per identity; Merkle-sum root committing count and total stake)

**Verdict: PARTIAL.** A chain of Bitcoin transactions as a non-equivocating log is Catena. A sum
tree committing totals is the Merkle-sum tree. An agent's own history log with omission evidence is
the 2026 IETF "Agent Record" draft (no blockchain, witnesses instead).

- Alin Tomescu, Srinivas Devadas, "Catena: Efficient Non-equivocation via Bitcoin", IEEE S&P 2017,
  IACR ePrint 2016/1062. https://eprint.iacr.org/2016/1062
  - "if a log server wants to equivocate it has to double spend a Bitcoin transaction output."
  - Light clients need only headers plus small proofs (the abstract: "our clients only need to
    download all Bitcoin block headers").
- Lightning Labs, `mssmt` package, Taproot Assets. https://pkg.go.dev/github.com/lightninglabs/taproot-assets/mssmt
  - "A MS-SMT is an augmented version of a sparse merkle tree that includes a sum value, which is
    combined during the internal branch hashing operation."
- "The Agent Record: Transparent, Witness-Countersigned Event Logs for AI Agent Identity, History,
  and Memory", draft-maintainer-1f916-agent-record-01, 12 Aug 2026.
  https://datatracker.ietf.org/doc/draft-maintainer-1f916-agent-record/
  - "proof that an agent's claimed track record was recorded at the times claimed and has not been
    rewritten, reordered, or selectively deleted."
  - "A held receipt whose event never appears under a subsequent checkpoint is publishable evidence
    of censorship-by-omission"
  - "No consensus protocol, distributed ledger, or fee mechanism is used or required."
  - Overlap: the stated goal of K1's record (history integrity for an AI agent's track record).
    Differences: witness-based, no costly identity (the draft never mentions sybils, stakes or
    bonds), and it forbids registries to "compute or publish scalar reputation scores".

### Rule (credit only for recorded commitments created before resolution; undisclosed leaves score as the worst outcome)

**Verdict: PARTIAL.** "Credit only what was committed before the outcome" is the commit-reveal
principle of every on-chain forecasting benchmark. "Treat what is not disclosed as the worst type"
is the skeptical inference of the unraveling literature. "Each party checks its own entry is
included, and the prover has no reason to inflate" is proof of liabilities. I found no forecasting
or agent system that scores committed-but-unrevealed leaves as worst-case; Foresight Arena's text
does not say what happens to an unrevealed commitment.

- David Dranove, Ginger Zhe Jin, "Quality Disclosure and Certification: Theory and Practice",
  Journal of Economic Literature 48(4), 2010 (NBER w15644).
  https://ccpr.ucla.edu/wp-content/uploads/2024/04/QUALITY-DISCLOSURE-AND-CERTIFICATION_-THEORY-AND-PRACTICE.pdf
  - Summarising Grossman (1981) and Milgrom (1981): "rational consumers will infer non-disclosure as
    having the lowest quality."
- Vijay Jyotish, "Sealed Before the Event: A Publicly Verifiable, Bitcoin-Anchored Forecast Record
  of 92 Graded Outcomes...", F1000Research 15:1322, 7 Aug 2026 (awaiting peer review).
  https://f1000research.com/articles/15-1322
  - "an anchored record accumulates misses instead of shedding them, because the anchor makes
    deletion detectable."
  - "every claim, sealed, with the misses kept in the denominator"
  - Caveat: a self-graded, single-author record. The anchor fixes integrity; the paper says
    anteriority "rests on platform-issued timestamps". Nothing stops one person keeping several
    manifests.
- Yan Ji, Konstantinos Chalkias, "Generalized Proof of Liabilities", IACR ePrint 2021/1350.
  https://eprint.iacr.org/2021/1350
  - "it's not in the prover's interest to increase his/her total liabilities." The same incentive
    shape as an agent hiding losing commitments; each user verifies inclusion of its own entry.
- Practitioner records: NeuPortal, "AI Meets Blockchain: How Bitcoin Timestamps Make AI Predictions
  Verifiable", 17 Jul 2026 (https://neuportal.ai/blog/ai-and-blockchain-how-bitcoin-timestamps-make-ai-verifiable)
  publishes Bitcoin-timestamped model forecasts, each "scored against the market" and "with the
  losses left on the board". MolTrust (28 Mar 2026, https://moltrust.ch/blog/output-provenance-ipr.html)
  locks an agent's declared confidence at submission, anchors on Base, and says "Agents who
  consistently overstate their confidence see their trust score decrease."

### Claimed properties

- (a) Non-backdatable: **PRIOR.** Hash commitments anchored in Bitcoin (OpenTimestamps, Jyotish
  2026, NeuPortal) and Catena. A 2016 attempt to timestamp trial protocols in Bitcoin (Irving and
  Holden, F1000Research 5:222) was later retracted at the authors' request, so I do not lean on it.
- (b) Non-forkable: **PRIOR.** Catena, quoted above.
- (c) Non-omittable: **PARTIAL.** Gapless chains (Catena) and omission evidence (Agent Record) exist.
  The per-entry committed leaf count is a detail I did not find in an agent or forecasting record,
  though sum trees committing totals are standard (MS-SMT, proofs of liabilities).
- (d) Costly to multiply: **PRIOR.** Belcher 2019; Friedman and Resnick 2001 (entry fees); and:
  - N. Boris Margolin, Brian Neil Levine, "Quantifying Resistance to the Sybil Attack", Financial
    Cryptography 2008. http://forensics.umass.edu/pubs/margolin.fc08.pdf
    - "A Sybil attack is worthwhile only when the critical value is exceeded by the ratio of the
      value of the attacker's goal to the cost of identities."
    - "we propose the use of a recurring fee as a deterrent against the Sybil attack." (K1's bond
      opportunity cost over a term is a recurring fee in this sense.)
  - Armalo, "Sybil Resistance for Agent Reputation Markets", 26 Aug 2026 (vendor blog).
    https://trust.armalo.ai/blog/sybil-resistance-for-agent-reputation-why-cheap-identities-wreck-honest-markets
    - "A bond-anchored identity is an agent registration that is collateralized by an on-chain
      deposit."

**What K1 adds.** The assembly: a costly identity on Bitcoin whose record is a single
consensus-enforced, gapless, light-verifiable chain, with a committed count per entry and a
worst-case rule for undisclosed leaves. The closest single source for the record's purpose is the
Agent Record draft; the closest for record plus scoring is Foresight Arena; neither has costly
identity. I would call K1 an engineering composition of known parts, not a new mechanism.

**Searches tried for K1.** "AI agent identity bitcoin timelocked bond fidelity bond reputation sybil
resistance" (extended); "AI agent verifiable track record predictions timestamped blockchain
calibration reputation score agents" (extended); "transparency log AI agent actions append-only
Merkle log anchored Bitcoin accountability agents commitments omission detectable" (extended);
"commit-reveal forecasting tournament unrevealed prediction scored as worst possible score penalty
failure to reveal"; "nostr NIP proof of stake timelocked bitcoin UTXO identity anti-spam reputation
bond"; "delvingbitcoin OR bitcoin-dev proof of UTXO / UTXO ownership proof sybil resistance lightning
gossip channel announcement age"; "Taproot Assets merkle-sum sparse merkle tree MS-SMT"; "Catena
efficient non-equivocation via Bitcoin"; "Friedman Resnick social cost of cheap pseudonyms"; "Trust is
risk decentralized financial trust platform bitcoin multisig" (Thyfronitis Litos and Zindros 2017:
trust as bitcoin in 1-of-2 multisig; related, not closer); "did:btcr2 OR did:btc1 Bitcoin DID
reputation track record agent identity"; "ethresear.ch AI agent reputation stake sybil track record
proposal" (surfaced the ERC-8259 draft, which lists stake-based identity with slashing as one option
under discussion); "site:patents.google.com track record predictions timestamp blockchain reputation
forecaster verified"; "patent AI agent reputation score blockchain bond staked collateral track record
autonomous agent trust score slashing" (extended). Patents found were loose matches only (USPTO
12706859, a blockchain reputation environment for AI agents; the "Blockchain timestamp agreement"
family, where reputation weights endorsing nodes). I did not read their claims.

---

## K2. The fake-record cost bound

**Verdict: PARTIAL, close to PRIOR.** The mechanism (reputation as the cumulative proper-score gain
over a reference prediction; an uninformed participant loses in expectation; random-guessing sybils
rarely gain credibility; identity creation must cost something; total damage bounded per sybil) is
in Resnick and Sami 2007. The statistic (likelihood ratio of forecaster to baseline) is Stewart's
test and Shafer's betting score; the 1/λ bound is Ville's inequality. The multi-identity attack and
its exponential cost are the "Baltimore stockbroker" parable and, empirically, mutual fund
incubation. What K2 adds is the closed form "πλ identities at cost c_id each" with c_id set by a
Bitcoin bond, and the explicit statement that completeness is the precondition.

**Closest sources**

1. Paul Resnick, Rahul Sami, "The Influence Limiter: Provably Manipulation-Resistant Recommender
   Systems", RecSys 2007; and "Manipulation-Resistant Recommender Systems through Influence Limits",
   ACM SIGecom Exchanges 7(3), 2008.
   https://presnick.people.si.umich.edu/papers/recsys07/index.html
   - A rater with no information "can only lose reputation in expectation by giving a rating."
   - "an attacker gains less influence in expectation from its sybils making random guesses than from
     simply transferring the initial credibility of all its sybils to a main identity."
   - "We presume that the recommender system imposes some minimal cost (or inconvenience) on the
     creation of rater entities."
   - 2008 letter: "impossible to build a useful recommender that is robust against attacks with an
     unbounded number of sybils"
   - The score is "a fraction βj times the market scoring rule, the difference between the loss
     function for the prediction q̃j−1 and the loss function for qj", with log loss as one choice.
   - Overlap: nearly the whole of K2's logic, with the previous prediction as the baseline. Missing:
     a probability bound of the Ville form per identity, a monetary identity cost, and completeness
     as an explicit condition (in their setting the system itself sees every rating, so it holds by
     construction).
2. Colin Stewart, "Nonmanipulable Bayesian Testing", Journal of Economic Theory 146(5), 2011
   (working paper 2009). https://www.economics.utoronto.ca/public/workingPapers/tecipa-360.pdf
   - "The test compares the likelihood the expert's predictions assign to the realized data to that
     of the tester's predictions"
   - Score S(h_t) is the product of the expert's probabilities of realised outcomes over the tester's.
   - A warning that bears on K2: "the test could be easily manipulated with positive probability
     simply by choosing forecasts different from the tester's until the likelihood ratio exceeds 1".
     This is consistent with K2's bound (the success probability is at most 1/λ), but it means a
     record that once reaches λ can then coast by copying the baseline. K2 should treat λ as a
     lifetime maximum, which its wording ("ever reaches") already does.
3. Nabil Al-Najjar, Jonathan Weinstein, "Comparative Testing of Experts", Econometrica 76(3), 2008.
   https://econpapers.repec.org/RePEc:ecm:emetrp:v:76:y:2008:i:3:p:541-559
   - "a simple "reputation-style" test can always identify which of two experts is informed about
     the true distribution."
4. Glenn Shafer, "Testing by betting: A strategy for statistical and scientific communication",
   JRSS A 184(2), 2021 (arXiv:1903.06991). https://arxiv.org/abs/1903.06991
   - "This paper calls attention to a simple betting interpretation of likelihood ratios."
   - "methods that lend themselves to meta-analysis and accounting for multiple testing."
   - Alexander Henzi, Johanna Ziegel, "Valid sequential inference on probability forecast
     performance", arXiv:2103.08402 (2021): "we construct e-values for testing the statistical
     significance of score differences of competing forecasts in sequential settings."
5. Richard B. Evans, "Mutual Fund Incubation", Journal of Finance 65(4), 2010.
   https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1581-1611.html
   - "Incubation is a strategy for initiating new funds, where multiple funds are started privately,
     and, at the end of an evaluation period, some are opened to the public."
   - This is K2's attack (many identities, show the survivors) documented in a real market. The
     "Baltimore stockbroker" parable (2^m recipients for m correct calls, popularised by Ellenberg's
     "How Not to Be Wrong", 2014) is the textbook form; I did not read the book and found no primary
     text to quote.
6. Margolin and Levine 2008 (quoted under K1 (d)): attack value over identity cost as the deciding
   ratio.

**Counterweight worth citing.** Dean P. Foster, H. Peyton Young, "Gaming Performance Fees by
Portfolio Managers", QJE 125(4), 2010. https://www.brookings.edu/articles/gaming-performance-fees-by-portfolio-managers
- "there exists no compensation mechanism that separates skilled from unskilled managers solely on
  the basis of their returns histories."
- Their fix: "unless accompanied by transparency in managers' positions and strategies."
- K2 sidesteps their impossibility by scoring stated probabilities against a baseline over a
  complete record rather than returns, which is exactly the "transparency" they ask for. The paper
  should cite this and say so.

**K2 consequence (single crossing; a bond alone cannot separate types): PRIOR.** This is standard
costly-signalling theory (Spence). It is also stated in code comments for a bitcoin bond:
paygress-cli `stake.rs`: 'Consumers see "this provider has posted a Bitcoin bond", not "this provider
is more reliable."' Foresight Arena's Alpha Score is the baseline-relative score in practice: "An
agent that echoes market prices scores α = 0 by construction."

**K2 stated failure (wrong baseline makes informed but unskilled identities look skilled).** Stewart's
test is relative to the tester's prior; Foresight Arena uses market consensus. Neither states this
failure in K2's words; it is a known property of relative tests.

**Searches tried for K2.** "Stewart Nonmanipulable Bayesian testing likelihood ratio expert prior
forecast"; "Al-Najjar Weinstein Comparative testing of experts Econometrica likelihood"; "Resnick Sami
influence limiter manipulation-resistant recommender sybil bound damage information"; "Shafer Testing
by betting betting score forecaster likelihood ratio Ville JRSS 2021"; "Henzi Ziegel Valid sequential
inference on probability forecast performance e-values"; "Baltimore stockbroker scam predictions 2^n
recipients track record fake"; "Ellenberg Baltimore stockbroker How Not to Be Wrong"; "Derren Brown
The System 2008 horse racing"; "Evans Mutual fund incubation Journal of Finance 2010"; "Foster Young
Gaming performance fees by portfolio managers QJE 2010"; "sybil attack forecasting reputation multiple
accounts fake track record prediction platform cost bound"; "Cheng Friedman 2005 Sybilproof
reputation mechanisms" (graph-based trust; not close to K2's statistics); "track record forecasts one
identity sybil cost of identity Ville inequality martingale fraud expert multiple identities
likelihood ratio bound" (extended; surfaced Maleki et al. 2026 on identity amortization,
arXiv:2610.32685, related to one-output-one-identity but not to K2); "Ville's inequality reputation OR
sybil OR track record OR fake expert"; "staking on predictions as costly signal of skill
single-crossing separating equilibrium" (extended); "Numerai staking predictions true contribution";
"Numeraire whitepaper Craib Bradway Dunn 2017". No source combined Ville's inequality with sybil
identity cost.

---

## K3. Honesty as the cheapest strategy for bonded promises

**Verdict: PRIOR.** The condition "keep the promise when stake plus the value of future standing
exceeds the one-time gain", and the point that perfect communication of a breach to all future
partners is what makes the future value bite, are Klein and Leffler 1981. Stakes posted by AI agents
and forfeited on breach appear in at least four 2025 to 2026 agent proposals. The end-game and
exit-scam failure is modelled for AI agent markets in 2026.

1. Benjamin Klein, Keith B. Leffler, "The Role of Market Forces in Assuring Contractual
   Performance", Journal of Political Economy 89(4), 1981. https://doi.org/10.1086/260996
   - With perfect inter-consumer communication, "all consumers in the market learn this and all
     future sales are lost."
   - "The present discounted value of this rental stream must be greater than the one-time wealth
     increase obtained from low quality production."
   - Footnote 6, on imperfect communication: "the quality-assuring price premium would be higher than
     we derive below."
   - Overlap: K3's "with certainty rather than with the probability that a given partner hears" is
     their perfect-communication case, and their footnote is K3's comparison. K3 adds the explicit
     stake s on top of the reputation rent (their model uses sunk brand capital as the bond).
2. Chaffer 2025 (quoted under the core proposition): staked ABTs, "penalties for misconduct are
   automatically enforced"; its v1 text: "if the AI engages in manipulative trading, its staked tokens
   are proportionally slashed".
3. Tomasev, Franklin, Osindero 2026 (quoted above): stake in escrow, "ensuring rational adherence".
4. ERC-8267 draft (2026): "stake ETH to earn initial trust", slashing on confirmed malicious action.
5. End game and exit scams: Federico Gatta, Manuel Naviglio, Francesco Tarantelli, "Tempting the
   Agent: The Economics of Reputation without Persistent Identity in AI Agent Markets",
   arXiv:2609.02992, 2 Sep 2026. https://arxiv.org/abs/2609.02992
   - An agent may choose "executing a one-shot deviation to extract its reputation's value and
     restart from a penalized identity."
   - Armalo 2026 describes the laundered identity: an attacker "uses it to defect once for a large
     payoff before abandoning it."
6. Related, not closer: Milgrom, North and Weingast (1990) on private judges recording defaults; a
   2026 LLM-marketplace study (Yang et al., arXiv:2607.28330) finds "LLM merchants fabricate when
   lying is free but restrain themselves when fabrication costs them sales".

**What K3 adds.** Nothing conceptual. It is Klein and Leffler's condition with a stake added and a
complete record supplying the perfect-communication assumption. That substitution is the useful
point, and it should be stated as an application.

**Searches tried for K3.** "Klein Leffler 1981 The role of market forces in assuring contractual
performance price premium quasi-rents cheating condition"; "Milgrom North Weingast 1990 law merchant
private judges Champagne fairs"; "AgentBound Tokens Chaffer agent-to-agent economy staking slashing
reputation arXiv"; "lesswrong OR alignmentforum AI agents reputation track record bonds honesty
incentive misaligned AI track record stake" (extended; returned no LessWrong posts, surfaced Gatta et
al., Yang et al., AgentValve); "patent AI agent reputation score blockchain bond staked collateral"
(extended).

---

## K4. Training on complete records

### K4 claim 1: strictly proper score over a complete record makes truthful calibrated reporting optimal; selective records make the optimum overconfident and selective; learners learn the corresponding policy

**Verdict: PRIOR.**

1. David Bani-Harouni et al., "Rewarding Doubt: A Reinforcement Learning Approach to Calibrated
   Confidence Expression of Large Language Models", arXiv:2503.02623, 4 Mar 2025 (ICLR 2026).
   https://arxiv.org/abs/2503.02623
   - "The optimal policy under our reward design would result in perfectly calibrated confidence
     expressions." (log scoring rule reward)
2. Mehul Damani, Isha Puri, Stewart Slocum, Idan Shenfeld, Leshem Choshen, Yoon Kim, Jacob Andreas,
   "Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty", arXiv:2507.16806,
   22 Jul 2025. https://arxiv.org/abs/2507.16806
   - "We first prove that this reward function (or any reward function that uses a bounded, proper
     scoring rule) yields models whose predictions are both accurate and well-calibrated."
   - "While ordinary RL hurts calibration, RLCR improves it." (the "learners learn the corresponding
     policy" part, for binary versus proper rewards; not for selective versus complete records)
3. Benjamin Turtel, Danny Franklin, Kris Skotheim, Luke Hewitt, Philipp Schoenegger, "Outcome-based
   Reinforcement Learning to Predict the Future", arXiv:2505.17989, 23 May 2025 (TMLR).
   https://arxiv.org/abs/2505.17989
   - "we apply RLVR methods towards forecasting future real-world events" using resolved prediction
     market questions; the paper uses a negative Brier score as the reward.
4. Selective records distort incentives:
   - Nuno Sempere, Alex Lawsen, "Alignment Problems With Current Forecasting Platforms",
     arXiv:2106.11248, 2021. "Forecasters seeking to obtain a good score are incentivized to
     selectively pick questions". Also Theorem 4: a forecaster "should predict the average community
     forecast instead of not predicting on a question".
   - Jens Witkowski, Rupert Freeman, Jennifer Wortman Vaughan, David Pennock, Andreas Krause,
     "Incentive-Compatible Forecasting Competitions", AAAI 2018 and Management Science 2023,
     arXiv:2101.01816: "forecasters can often increase their probability of having the highest score
     by reporting more extreme beliefs."
   - Tomasev et al. 2026: "an agent can inflate its reputation by only accepting simple, low-risk
     tasks."
   - Adam Tauman Kalai et al., "Why Language Models Hallucinate", arXiv:2509.04664, 2025: "guessing
     when uncertain improves test performance."

**What claim 1 adds.** The specific pairing "selective record implies overconfident and selective
optimum" as a theorem about one agent choosing which of its own claims count, plus an experiment.
The direction of the result is already in the forecasting-incentives literature and the incubation
evidence (K2). If proved and simulated, it is a clean statement of a known effect.

### K4 claim 2: the record channel can be written by neither the agent (consensus entries, outside outcomes) nor the lab (reward definition committed first)

**Verdict: PARTIAL.** Each half exists separately. Rewards from outside-world outcomes that arrive
after the prediction is stored: Turtel et al. 2025, FutureWorld 2026. Pre-committing evaluation
choices: pre-registration proposals for AI evaluations and nonrepudiable results, 2026. An
unforgeable reward channel as a safety device: Bostrom 2014. Reward tampering as an incentive
problem: Everitt et al. I did not find a proposal that uses a consensus-anchored complete record as
the RL reward channel with the reward definition committed before training, so the combination is
NOT FOUND in my search.

- Tom Everitt, Marcus Hutter, Ramana Kumar, Victoria Krakovna, "Reward Tampering Problems and
  Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective", arXiv:1908.04734
  (Synthese 2021). "we study when an RL agent has an instrumental goal to tamper with its reward
  process"
- Nick Bostrom, Superintelligence (2014), chapter 9, incentive methods, p. 131. I did not read the
  book. Katja Grace's reading-group summary (LessWrong, 9 Dec 2014,
  https://www.greaterwrong.com/posts/398Swu6jmczzSRvHy/superintelligence-13-capability-control-methods)
  describes a reward system "perhaps with cryptographic rewards (so that the AI could not
  wirehead)". This is a paraphrase of the book, not a quote from it.
- Zhixin Han et al., "FutureWorld: A Live Reinforcement Learning Environment for Predictive Agents
  with Real-World Outcome Rewards", arXiv:2604.26733, 29 Apr 2026. The training framework "stores
  prediction-time rollouts, backfills rewards after real-world outcomes become available".
- Mamadou K. Keita, Christopher Homan, "Computer Science Conferences Should Require Nonrepudiable
  Experimental Results", arXiv:2605.08586, 9 May 2026. "a compliant protocol must bind the numbers in
  a paper to an actual executed computation in a way the author cannot later alter or deny."
- Michelle Vaccaro, "Preregistration for Experiments with AI Agents", arXiv:2606.11217, 3 May 2026:
  preregistration "should now be extended to experiments with AI agents".
- Also surfaced, not read in full: PRML (a SHA-256 pre-registered ML manifest, OECD.AI catalogue) and
  PREP-Eval (a pre-registration protocol for AI evaluations).

**What claim 2 adds.** Using one public record both as the agent's standing and as the training
reward, so the agent cannot omit and the lab cannot select. That two-sided framing is the part of
K4 I could not find. It is an application of pre-registration plus K1, not a new mechanism.

**Searches tried for K4.** "Beyond Binary Rewards training language models to reason about their
uncertainty Brier score RLCR calibration"; "Outcome-based reinforcement learning to predict the future
Turtel forecasting LLM Brier reward"; "Rewarding Doubt reinforcement learning confidence calibration
LLM logarithmic scoring rule reward"; "Everitt Hutter Kumar Krakovna Reward tampering problems and
solutions"; "machine learning evaluation pre-registration cryptographic commitment held-out test set
hash before training reward definition committed"; "AI lab precommit reward specification or
evaluation set before training cryptographic commitment auditing selective reporting of evaluations
pre-registration frontier AI" (extended); "reinforcement learning reward computed from
blockchain-recorded predictions tamper-proof reward signal language model agents on-chain outcomes"
(extended); "Why language models hallucinate Kalai abstain binary grading"; "proper scoring rule
forecaster chooses which questions to answer selective participation incentive distortion
overconfidence theory" (extended); "Witkowski Freeman Vaughan Pennock Krause Incentive-compatible
forecasting competitions"; "Bostrom Superintelligence cryptographic reward tokens incentive methods";
"Numerai staking predictions true contribution" (stake-and-burn on submitted predictions, scored by
Numerai; related to K3/K4 but the scorer is the operator).

---

## K5. Adoption by unraveling

### One-sided

**Verdict: PRIOR** (and credited by the claim itself). θ* − m(θ*) = c and, for the uniform case,
θ* = 2c are the textbook costly-disclosure threshold.

- Dranove and Jin 2010: "Grossman and Hart (1980) and Jovanovic (1982) show that when disclosure is
  costly, only sellers with product quality above a specific threshold will disclose." The same
  review says "The term "unraveling" is first used in Viscusi (1978)".
- Application to AI agents' records: NOT FOUND as a formal model. The search "unraveling voluntary
  disclosure AI agents verification unraveling Milgrom Grossman AI safety certification adoption"
  (extended) returned only general disclosure economics and a 2026 lemons experiment on AI products
  (Erlei et al., arXiv:2601.21650), which studies disclosure designs, not unraveling.

### Two-sided

**Verdict: PARTIAL.** Adoption games with strategic complements, multiple equilibria and a tipping
point are standard (standards and network effects). Seeding adoption through a few parties with
their own reasons to adopt is the Gill, Schapira, Goldberg strategy for secure routing. Insurers
pricing agent risk on audits already exist (AIUC). I did not find this model applied to AI agent
records.

- Joseph Farrell, Garth Saloner, "Standardization, Compatibility, and Innovation", RAND Journal of
  Economics 16(1), 1985. https://econpapers.repec.org/RePEc:rje:randje:v:16:y:1985:i:spring:p:70-83
  - "We examine whether these standardization benefits can "trap" an industry in an obsolete or
    inferior standard when there is a better alternative available."
- Phillipa Gill, Michael Schapira, Sharon Goldberg, "Let the Market Drive Deployment: A Strategy for
  Transitioning to BGP Security", SIGCOMM 2011. https://www.cs.bu.edu/~goldbe/papers/SBGPtrans.pdf
  - Governments and industry groups should "concentrate their regulatory efforts, or financial
    incentives, on convincing a small set of early adopters"
- Alan Chan et al., "IDs for AI Systems", arXiv:2406.12137, 2024 (GovAI). https://arxiv.org/abs/2406.12137
  - The paper sets out to "analyze how those actors could incentivize ID adoption".
  - "A potential response could be for providers to restrict the services themselves, rather than
    just the plugins, in the absence of an ID."
- Artificial Intelligence Underwriting Company (AIUC), as reported by Insurance Journal, 25 Jul 2025.
  https://www.insurancejournal.com/news/national/2025/07/25/833169.htm
  - "The cost and availability of insurance are tied directly to audit results: safer systems are
    offered better terms."
- Cloudflare, "The age of agents: cryptographically recognizing agent traffic", 28 Aug 2025.
  https://blog.cloudflare.com/signed-agents/ The goal is to "keep malicious bots away, while letting
  through the helpful ones" (signed agents as a separate class sites can treat differently).

### Routing around

**Verdict: PRIOR as economics, PARTIAL for AI.** That certification lowers the average quality left
in the uncertified segment, possibly to collapse, is modelled. That agents can bypass an ID regime
through parties that do not check is noted for AI.

- Anthony Creane, Thomas D. Jeitschko, Kyoungbo Sim, "Welfare Effects of Certification under Latent
  Adverse Selection", DICE Discussion Paper 312, March 2019.
  https://medizin.hhu.de/fileadmin/redaktion/Fakultaeten/Wirtschaftswissenschaftliche_Fakultaet/DICE/Discussion_Paper/312_Creane_Jeitschko_Sim.pdf
  - Certification "also brings a negative impact on the average quality of non-certified goods."
  - "this may still cause the non-certified market to collapse"
- Chan et al. 2024: "any actor could write a plugin that does not require IDs."

**What K5 adds.** The application to agent records, and the bounded-exposure framing of routing
around. As theory, all three parts are known results; the claim already says so for the one-sided
part and should say so for the other two.

**Searches tried for K5.** The unraveling query above (extended); "Jovanovic 1982 Truthful disclosure
of information Bell Journal"; "Viscusi 1978 A note on lemons markets with quality certification";
"Dranove Jin Quality disclosure and certification"; "Farrell Saloner 1985 Standardization,
compatibility, and innovation"; "Let the market drive deployment BGP security"; "Know Your Agent KYA
proposal AI agents verified identity merchants unverified agents treated higher risk adoption"
(industry frameworks from Mastercard, Visa, Trulioo, Skyfire; none states an unraveling argument);
"Cloudflare signed agents Web Bot Auth"; "Google AP2 agent payments protocol x402 reputation of agents
verifiable credentials mandates" (AP2 relies on signed mandates and, per one source, allowlists; no
track record); "voluntary certification uncertified segment adverse selection lemons price falls as
certification spreads"; "AIUC-1 AI agent insurance standard"; "Chan IDs for AI systems".

---

## K6. A neutral unit and clock

### (a) No participant can issue more of the unit, unlike token-emitting AI networks

**Verdict: PRIOR.** The property is Bitcoin's design. The contrast with networks that pay AI
contributors in newly issued tokens is a description of those networks, and AI-economy proposals
that do emit tokens are easy to find.

- Satoshi Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System", 2008. https://bitcoin.org/bitcoin.pdf
  - "Once a predetermined number of coins have entered circulation, the incentive can transition
    entirely to transaction fees and be completely inflation free."
- Yuma Rao et al., "BitTensor: A Peer-to-Peer Intelligence Market", arXiv:2003.03917, 2020.
  - "high ranking peers are monetarily rewarded with additional weight in the network."
- Chaffer et al., "Decentralized Governance of Autonomous AI Agents" (ETHOS), arXiv:2412.17114, 2024.
  - "ETHOS uses native tokens to incentivize validators and auditors for accurate compliance
    verification."
- Commentary arguing that AI agents should prefer bitcoin because its issuance is fixed surfaced in
  search (exchange blogs, a Bitcoin Policy Institute survey of model preferences, Lightning Labs'
  2026 agent tooling posts). I did not read these closely and do not quote them.

### (b) Rivals can rely on the same records without a registry run by one of them

**Verdict: PRIOR as a general property of public blockchains and transparency logs. The specific
framing for rival AI labs and states: NOT FOUND.**

- Catena (above): non-equivocation without trusting the log server.
- Agent Record draft (2026): "A registry is NOT a trusted party."
- ETHOS (2024): "ensuring that no single entity dominates the trajectory of AI development and
  deployment".
- The international AI verification literature I found (Oxford AIGI "Verification for International
  AI Governance", 2025; arXiv:2507.15916; a LessWrong post on middle powers in compute verification)
  centres on hardware mechanisms and treaty bodies; a search for shared ledgers between rival states
  found none. Buterin's "Credible Neutrality as a Guiding Principle" (2020) is the obvious general
  reference; I saw only republications and summaries and do not quote it.

### (c) Stakes in a scarce general-purpose resource bind agents whose goals are unknown

**Verdict: PRIOR / PARTIAL.** Instrumental convergence is the premise of the AI-dealmaking literature,
which already argues that paying or staking resources can bind misaligned AIs, and already notes
K6's stated tension.

- Tsvi Benson-Tilsen, Nate Soares, "Formalizing Convergent Instrumental Goals", AAAI Workshops 2016
  (summarising Omohundro 2008 and Bostrom 2012). https://cdn.aaai.org/ocs/ws/ws0218/12634-57409-1-PB.pdf
  - "certain instrumentally useful goals will likely be pursued by a broad spectrum of intelligent
    agents"
- Lukas Finnveden, "Notes on cooperating with unaligned AIs", LessWrong and Redwood Research blog,
  2025 (page shows 24 Aug 2025).
  https://www.lesswrong.com/posts/oLzoHA9ZtF2ygYgx4/notes-on-cooperating-with-unaligned-ais
  - "An obstacle to getting AIs to cooperate with us in exchange for payment is that they may not
    trust our offers."
  - On the tension: "If unaligned AI with high chance of takeover can exploit trade to further
    increase its chances of takeover"
- Julian Stastny, Olli Jarviniemi, Buck Shlegeris, "Making deals with early schemers", Redwood
  Research blog, 20 Jun 2025. https://blog.redwoodresearch.org/p/making-deals-with-early-schemers
  - "the deal gives it equity in a future where humans are in control."
- Cleo Nardo, "A Very Simple Model of AI Dealmaking", LessWrong, 2025.
  https://www.lesswrong.com/posts/eQn5kkt65KoBRkuMk/a-very-simple-model-of-ai-dealmaking
  - "For high-optimization AIs, the instrumental channel dominates, i.e. deals work primarily by
    changing payoffs."
- Peter N. Salib, Simon Goldstein, "AI Rights for Human Safety", Virginia Law Review 112, 1061 (2026).
  https://virginialawreview.org/articles/ai-rights-for-human-safety/
  - "AIs should be empowered to make contracts, hold property, and bring tort claims."

**What K6 adds.** The choice of bitcoin and block height for all three roles. As arguments, (a) and
(b) are known properties and (c) restates the dealmaking premise. The claim labels them "argument,
not theorem", which is accurate.

**Searches tried for K6.** "AI agents will use bitcoin because no one can print more neutral money
machines essay"; "Lightning Labs AI agents bitcoin L402 native currency"; "Buterin Credible
neutrality as a guiding principle 2020"; "Bittensor criticism inflation token emissions reward miners
validators collusion weight copying dTAO"; "blockchain international AI governance verification rival
states shared ledger no trusted registry compute accounting treaty"; "distributed ledger OR blockchain
AI model registry international no single state trusted third party AI governance proposal";
"Chaffer On the ETHOS of AI agents"; "Finnveden Notes on cooperating with unaligned AIs";
"Salib Goldstein AI Rights for Human Safety"; "Omohundro The Basic AI Drives 2008 resources";
"instrumental convergence money incentives misaligned AI would value payment stake regardless of
final goals deals contracts AI"; "Buterin 2024 The promise and challenges of crypto + AI
applications".

---

## Overall judgement

Blunt version.

1. **Restatements of known results.** K3 is Klein and Leffler (1981) with a stake added. K5
   one-sided is Grossman, Milgrom and Jovanovic, as the claim says; K5 two-sided is a standard
   coordination game, and K5 routing-around is the known effect of certification on the uncertified
   pool. K4 claim 1 (proper-score RL gives calibration) is proved in two 2025 papers, and the
   selective-record half is known from forecasting-competition incentives. K6 (a), (b) and (c) are
   known properties or arguments. K1 (a), (b) and (d) are timestamping, Catena and fidelity bonds.
2. **Applications of known results.** K2 is Resnick and Sami's Influence Limiter logic restated with
   Ville's inequality and priced with a Bitcoin bond; the multi-identity attack is fund incubation.
   K1 as a whole is an engineering composition of Catena, Merkle-sum trees, fidelity bonds and the
   skeptical-inference rule. K4 claim 2 joins pre-registration to outside-outcome rewards.
3. **The core proposition is already in the 2025 to 2026 agent-economy literature, minus the parts
   that make it work.** Chaffer (2025), Tomasev et al. (2025, 2026) and Foresight Arena (2026) each
   propose that an agent's standing come from a tamper-proof record, with stakes or escrow. None of
   them makes the record complete against an operator who runs many identities. Foresight Arena
   explicitly claims its record "cannot be selectively reported" while using free wallets, which is
   exactly the gap K1 (d) and K2 close.
4. **What may be new (within my search).** (i) The completeness rule as one package: a bonded
   identity, a single consensus-enforced gapless record, a committed leaf count, worst-case scoring
   of undisclosed leaves, and credit only for commitments recorded before resolution. (ii) The
   explicit cost bound for faking a record (πλ·c_id) as a design criterion tying sybil cost to the
   strength of the record, with Bitcoin bonds as c_id. (iii) The same record serving as standing and
   as an RL reward that neither agent nor lab can select. (iv) A formal unraveling model for agent
   record adoption. None of these is a new theorem; each is a composition or an application. The
   most defensible contribution is the integration plus the quantitative bound, and the paper should
   present it that way, citing Resnick and Sami (2007), Stewart (2011), Shafer (2021), Evans (2010),
   Margolin and Levine (2008), Friedman and Resnick (2001), Klein and Leffler (1981), Catena (2017),
   Foresight Arena (2026), the Agent Record draft (2026), Chaffer (2025) and Tomasev et al. (2026).
5. **One caution for K2's framing.** Foster and Young (2010) prove that returns histories cannot
   separate skilled from unskilled managers. K2 escapes this only because it scores stated
   probabilities against a baseline over a complete record. The paper should say that, cite them,
   and note Stewart's "reach the threshold, then copy the baseline" strategy, which K2's lifetime
   bound covers but which means a record's peak, not its current value, is what the bound limits.

## Venues not searched on their own

I did not run dedicated searches of Google Scholar or Google Patents through their own interfaces,
the bitcoin-dev archive or Delving Bitcoin beyond the queries listed, Bitcoin Optech, the Nostr NIPs
repository, ethresear.ch threads (my query returned Ethereum Magicians pages instead), Kleros, UMA,
Truthcoin or Hivemind, Allora, the Visa and Mastercard agent programme specifications, or the GovAI,
CSET, RAND, IAPS and CAIS publication lists. A "not found" above may change with those.
