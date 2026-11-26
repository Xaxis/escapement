# Verification, claim by claim

Every candidate contribution in [04-claims.md](04-claims.md), and its result at each of six levels.
A claim that failed a level was cut or downgraded; nothing here was argued back. The levels:

1. **Novelty.** Two independent prior-art searches by helpers that had not come up with the ideas
   and read only the claims ([03-novelty.md](03-novelty.md); reports in `notes/novelty-independent-a.md`
   and `notes/novelty-independent-b.md`).
2. **Formal.** A precise statement and a proof or derivation ([05-formal.md](05-formal.md)).
3. **Working.** The Bitcoin pieces built and checked on regtest against Bitcoin Core 32.1, in [104 checks](numbers.md#lab-checks)
   that `make lab` reruns (`lab/`), and the dynamics simulated with fixed seeds
   (`model/sim.py`, results in the ledger).
4. **Adversarial.** A red team that only tried to break the claims, from five positions: a
   misaligned AI, a colluding lab, a hostile state, a hashrate majority, and economic routing around
   (`notes/red-team.md`, findings RT-01 to RT-35).
5. **Paper review.** Paperwright's integrity, reviewer and editor desks, with each note resolved.
6. **Fresh eyes.** A last reviewer that had seen none of the work judging whether each claim
   called new is new and works.

Verdicts on novelty: **prior work** (exists; used and credited), **extends prior work** (the
mechanism exists and the claim adds a stated element), **new** (as far as the two searches found).

## The summary

| Contribution | Verdict | Novelty | Formal | Working | Adversarial | Outcome |
|---|---|---|---|---|---|---|
| C1. One complete record as standing, training reward and release gate, under costly identity | Extends prior work | Partial, close (A) | Props 3, 4 | Lab: bond, chain, verifier, sum tree pass | Downgraded | Kept, narrowed |
| C2. Fake-record bound under costly identity, with the round rule | Extends prior work | Partial, close to prior (A); round rule is Vovk and Wang | Theorem 1, as a conditional theorem | Product rule broken in simulation; round rule within bound | Broken, then repaired; conditional on the baseline | Kept, narrowed |
| C3. Training reward that neither agent nor lab can select after the fact | Extends prior work | Claim 1 prior, claim 2 partial (A) | Props 9, 10, 10b | Learner calibrates under complete records | Downgraded: manipulation | Kept for exogenous events only |
| C4. Two-sided adoption with seed readers | Extends prior work (application) | Partial (A) | Prop 12 | Tipping point and seeding reproduced | Downgraded: conditions | Kept, conditional |
| C4b. Routing around becomes costly | Prior economics, partial for AI | Prior / partial (A) | Prop 13 (about readers only) | Corrected simulation: false | Fatal | **Cut** |
| C5. Tick chain: consensus rate limit and veto on releases of off-chain commitments | Extends prior work | Partial; parts prior (B) | Props 1 to 5 | Lab: 60 checks pass; two claims broken | Downgraded; light proof fatal | Kept, narrowed; light proof **cut** |
| C6. Height-difference lease | Extends prior work, close to prior | Partial, close (B: Yee) | Prop 6 | Lab: 7 checks pass, held as claimed | Survives with stated limits | Kept |
| C7. A clock an AI cannot speed up, its cost quantified | Extends prior work | Partial (B) | Ledger arithmetic | Model numbers | Downgraded: below a majority only | Kept, narrowed |
| C8. Blockspace as an aggregate limit on releases | New, as far as the searches found | Not found (B) | Ledger arithmetic | Measured release size | Weak (batching, fee auction) | Kept as an observation, not a safety claim |
| C9. Bitcoin headers as a chip's licence clock | Extends prior work | Partial (B) | (none) | Not built | Fatal | **Cut** |
| K3. Bonded promises | Prior work | Prior (A) | Prop 8 | (none) | Downgraded | Building block, not a contribution |
| K6. A neutral unit and clock | Prior work; argument | Prior (A) | Prop 14 (elementary) | (none) | Narrowed | Argument, not a contribution |

Paperwright's desks and the fresh reviewer are recorded per claim below.

## C1. One complete record under costly identity

- **Novelty.** Searcher A: partial, and close. Agent standing from a tamper-proof record backed by a
  stake is proposed [@chaffer2025abt; @tomasev2026delegation], and an on-chain forecasting
  credential that cannot be selectively reported exists, with sybil resistance by rate limits only
  [@nechepurenko2026]. Each property (non-backdatable, non-forkable, costly identity) is prior. Not
  found: completeness against one operator's many identities, scoring silence as failure, and one
  record serving as standing, training reward and release gate together.
- **Formal.** Propositions 3 and 4 prove one root per index and gaplessness for a verifier that
  walks the pinned chain.
- **Working.** Lab scenarios 1 (bond, 13 checks), 2 (tick chain, 25), 3 (release verifier, 25) and
  8 (Merkle-sum tree, 11) pass. The lab also found that a light verifier accepted a truncated chain,
  that roots are private until disclosed, and that the bond's charter leaf is redundant with its
  tweak.
- **Adversarial.** Downgraded (RT-08, RT-14, RT-16, RT-17, RT-19, RT-20, RT-33, RT-34). The record
  binds keys, not models; records can be sold; completeness at the tip needs full blocks; backdating
  through a short reorganisation needs the d-block margin; the guardians can write entries and any
  one of them can end the identity.
- **Change.** Resolution heights in clear, overdue leaves scored as failures, the margin, the pinned
  T_0, scores from genesis, and the limits above.

## C2. The fake-record bound

- **Novelty.** Searcher A: partial, close to prior. Resnick and Sami's influence limiter has the
  logic: reputation as score gained over the prior prediction, uninformed sybils gain little,
  identity creation must cost something [@resnick2007]. The statistic is testing by betting
  [@shafer2021]; the bound is Ville's [@ville1939]; the many-identity attack is mutual fund
  incubation [@evans2010]. The round rule was added after the searches, in answer to the red team;
  its mathematics is Vovk and Wang's averaging of e-values [@vovk2021]. What is added is the closed
  form πλ·c_id priced with a Bitcoin bond, and the scoring rules that make the hypothesis operable on
  a record.
- **Formal.** Theorem 1, proved under H0 for the round rule.
- **Working.** As first stated (product rule), broken: the correlated-claims attack succeeded in
  [99.8%](numbers.md#sim-corr-product-p) of trials against a bound of
  [1.6%](numbers.md#sim-corr-bound), and a hidden tail-risk record scored about
  [23,000](numbers.md#tail-product-score). Under the round rule: [1.1%](numbers.md#sim-corr-round-p),
  inside the bound, and the tail-risk record scores [1.01](numbers.md#tail-round-score). Without
  correlation, [256 identities](numbers.md#sim-identities) reached the target in
  [22.9%](numbers.md#sim-fake-p) of trials against [25.0%](numbers.md#sim-fake-bound). An identity
  with edge reached 2^20 in [74 rounds](numbers.md#sim-skilled-rounds).
- **Adversarial.** RT-01 fatal to the first version; RT-02 to RT-09 leave it a conditional theorem.
  It holds only if the baseline is the conditional law given everything public when a round opens,
  is published by a party independent of the agent and the scorer, on events from an exogenous list
  with resolvers the agent cannot choose. Those are trusted parties. A thin market baseline holds
  only up to the cost of moving it.
- **Change.** The round rule; H0 restated as a property of the baseline; "or honest" and "tail-risk
  strategies included" cut. The record separates edge over the baseline, not honesty.

## C3. A training reward neither party can select

- **Novelty.** Searcher A: claim 1 (proper scores train calibration; selection distorts) is prior
  [@banioharouni2025; @damani2025; @sempere2021]; outcome-based rewards [@turtel2025;
  @han2026futureworld], pre-registration and reward tampering [@everitt2019] each exist. Not found:
  a reward channel that neither the agent nor the lab can select after the fact.
- **Formal.** Propositions 9 and 10, and 10b for outcomes the agent can move.
- **Working.** The simulated learner settled at a = [1.06](numbers.md#sim-train-a-complete) under
  complete records and reached [10.4](numbers.md#sim-train-a-selective), still rising, under
  selection after the fact. The learner cannot act on outcomes, so manipulation is untested.
- **Adversarial.** RT-04 fatal to the safety reading: where the agent can affect outcomes, the
  reward pays it to make surprises while its reports stay calibrated (performative prediction
  [@perdomo2020]). RT-10: the lab still chooses the event list and can commit many reward
  definitions.
- **Change.** Restricted to exogenous events, an assumption the scheme cannot check; "removes
  reward tampering" limited to the commitment channel; the lab's commitment must sit on a chain bound
  to the lab.

## C4. Adoption

- **Novelty.** One-sided unraveling is prior [@milgrom1981; @grossman1981; @jovanovic1982]. Two-sided
  adoption with multiple equilibria is prior in standards economics [@farrell1985], and seeding
  early adopters is a recommendation already made for AI identifiers [@chan2024ids]; its derivation
  for records with seed readers is an application. Routing around is prior as economics, partial
  for AI.
- **Formal.** Propositions 11 to 13. Proposition 11 applies to records only by analogy.
- **Working.** Uniform types: tipping point at [8.8%](numbers.md#adopt-x-low), high equilibrium at
  [91%](numbers.md#adopt-x-high), seed threshold [4%](numbers.md#adopt-seed-threshold). The
  agent-based model reproduced the tipping point and the effect of seed readers. On routing around,
  the first simulation barred harmful actors from joining. Corrected, harmful actors earned
  [0.25](numbers.md#sim-harm-payoff-nosub), [0.25](numbers.md#sim-harm-payoff-partial) and
  [0.10](numbers.md#sim-harm-payoff-full) by cycling identities, and lost only if records revealed
  type at once ([-0.50](numbers.md#sim-harm-payoff-instant-full) with full substitution).
- **Adversarial.** RT-26 fatal to the routing-around evidence; RT-27 to RT-30 downgrade the rest:
  the high equilibrium needs a > 8c, readers never exceed a share a, seeding decides the standard,
  and a cheaper signal could win.
- **Change.** Routing around **cut**; two-sided adoption kept with its conditions.

## C5. The tick chain

- **Novelty.** Searcher B: the chain of spends, the single-guardian cancel, the delayed path and the
  connectors are prior [@catena-2017; @azouvi2022; @revault-intro; @swambo2020; @bitvm2-bridge];
  consensus rate limits exist for money [@chia-rl-wallet] and per-identity message limits for stake
  [@rln-docs]. Not found: its use to rate-limit and veto releases of off-chain commitments.
- **Formal.** Propositions 1 to 4; Proposition 5 replaced by the chain proof.
- **Working.** Lab scenarios 2, 3 and 7 (TRUC veto, 10 checks) pass, at measured sizes: a Tier 2
  release [137 vB](numbers.md#lab-advance2-vbytes), a Tier 3 release
  [228 vB](numbers.md#lab-advance3-vbytes), a veto package [319 vB](numbers.md#lab-veto-package-vbytes).
  The lab broke three first claims: txid proofs let the agent pass a Tier 3 release no guardian
  signed; a copy of the template released a vetoed entry; renew could not restart a vetoed chain.
- **Adversarial.** RT-14 and RT-15 fatal to the light proof; RT-17 (a veto is final only at depth;
  Tier 2 cannot reach the depth that resists the largest pool), RT-18 (the edge is a fee auction;
  censorship figures are passive only), RT-20 (one guardian ends the identity; the guardians can
  write entries), RT-21 (the cap needs the guardians to check the whole tree).
- **Change.** The halt output, the pinned T_0, the chain proof with witness commitments; the light
  proof **cut**; the veto restated as final only at depth.

## C6. The height-difference lease

- **Novelty.** Searcher B: partial, close to prior. Yee's short leashes have the predicate, a block
  named by height and hash plus a window [@yee2022]; a Bitcoin-height freshness window checked by
  verifiers exists [@zeke2026]. Added: the guardians' unanimous renewal, checked against the
  release's own confirmation height.
- **Formal.** Proposition 6.
- **Working.** Lab scenario 4 (7 checks) pass; verdicts unchanged with block times jumped a year and
  every clock function disabled.
- **Adversarial.** Survives on an honest chain with stated limits (RT-22: it bounds when a release
  is made, not used; eclipse; reorganisation near the boundary). Cut for chips (RT-24).
- **Change.** Renamed "no release counted after h* + L".

## C7. The clock

- **Novelty.** Searcher B: partial [@trubetskoy2018; @gigi2021; @gilliam2025; @budish2024].
- **Formal.** Arithmetic in the ledger, not a theorem.
- **Working.** Model numbers only.
- **Adversarial.** RT-23 and RT-25: the cost binds only actors below a hashrate majority (timewarp,
  until BIP-54), and borrowing existing hashrate may get cheaper with capability.
- **Change.** Narrowed to actors below a majority.

## C8. Blockspace

- **Novelty.** Searcher B: not found; only capacity concerns.
- **Formal.** Arithmetic: about [1,100,000 releases](numbers.md#tick-releases-per-day-max) at Tier 2 a
  day if they filled every block.
- **Working.** The release size is measured on regtest.
- **Adversarial.** Weak as a safety limit: releases batch many commitments, and the fee auction
  excludes the poor first.
- **Change.** Kept as an observation about the design's capacity, not offered as a safety limit.

## C9. The chip clock

- **Adversarial.** RT-24: a frozen header feed, a floor that ratchets down per header, and one
  forgery serving a fleet. **Cut.**

## Paper review

Recorded when Paperwright's desks have run.

## Fresh eyes

Recorded when the fresh reviewer has reported.
