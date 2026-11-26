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

| Contribution | Two searches | Formal | Working | Adversarial | Fresh eyes | Final verdict |
|---|---|---|---|---|---|---|
| C1. One complete record as standing, training reward and release gate, under costly identity | Partial, close | Props 3, 4 | Lab passes; light verifier misses newest entries | Downgraded | Does not work as stated: chain not bound to bond (regtest); standing and reward ask for different reports | **Cut** as a contribution |
| C2. Fake-record bound under costly identity, with the round rule | Partial, close; round rule is Vovk and Wang | Theorem 1, conditional | Product rule broken; round rule within bound | Broken, then repaired | Prior work; hypothesis mis-stated; round rule not proper | **Prior work**, applied, with corrected hypotheses |
| C3. Training reward that neither agent nor lab can select | Claim 1 prior, claim 2 partial | Props 9, 10, 10b | Learner calibrates | Downgraded: manipulation | Does not work for the lab; agent side textbook | **Cut**; agent side is prior work |
| C4. Two-sided adoption with seed readers | Partial | Prop 12 | Tipping point reproduced | Downgraded: conditions | Prior work (critical mass); toy model | **Prior work**, applied |
| C4b. Routing around becomes costly | Prior / partial | Prop 13 (readers only) | Corrected simulation: false | Fatal | (cut before review) | **Cut** |
| C5. Tick chain: rate limit and veto on releases of off-chain commitments | Partial; parts prior | Props 1 to 5 | Lab passes; light proof broken | Light proof fatal | Extends prior work narrowly (spacechains); pin unbound; outside-money bid (regtest) | **Extends prior work narrowly**, per pinned chain |
| C6. Height-difference lease | Partial, close (Yee) | Prop 6 | Lab: 7 checks pass | Survives, stated limits | Prior work (Substrate's mortal transactions); works | **Prior work**, applied |
| C7. The clock's cost, below a majority | Partial | Ledger arithmetic | Model numbers | Narrowed | Prior work; not load-bearing | **Prior work** |
| C8. Blockspace as an aggregate limit | Not found | Ledger arithmetic | Measured release size | Weak | Prior method, applied; a scaling ceiling | **Prior method**, an observation |
| C9. Bitcoin headers as a chip's licence clock | Partial | (none) | Not built | Fatal | (cut before review) | **Cut** |
| K3. Bonded promises | Prior | Prop 8 | (none) | Downgraded | (not reviewed) | **Prior work**, a building block |
| K6. A neutral unit and clock | Prior | Prop 14 | (none) | Narrowed | (not reviewed) | **Prior work**, an argument |

Nothing survived as new. The one contribution that extends prior work, the covenant-free tick chain,
does so narrowly and holds per pinned chain until a binding of chain to bond is specified and built.
Paperwright's desks are recorded under "Paper review" below.

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
- **Fresh eyes.** Extends prior work as an assembly only, and does not work as stated. Nothing on
  chain binds a tick chain to its bond; on regtest one charter id carried two chains with different
  roots at entry 1, each accepted from its own pin, so non-forkability, the rate limit and the cost
  of multiplying identities hold per pin, not per bond. The record is complete per identity, not per
  operator. Standing (the round rule) and the training reward (a proper score) ask for different
  reports from the same leaves. Scoring silence as the worst outcome is prior work
  [@infinite-games]. None of the paper's results needs the three roles to share one record.
- **Final.** Cut as a contribution. A binding (identity = bond outpoint, T_0 an output of the bond's
  own transaction) and a leaf that carries a forecast and a separate stake are proposed, not built.

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
- **Fresh eyes.** Prior work: a union bound on Ville's inequality, with the round rule being
  Shafer's testing by betting with a unit stake split across open bets and Vovk and Wang's averaging
  [@shafer2021; @vovk2021]; Numerai priced lucky accounts with stakes [@craib2021numerai]; the closest
  statistical work is Al-Najjar and Weinstein's comparative test [@alnajjar2008] and Choe and
  Ramdas's sequential comparison of forecasters [@choe2024]. The proof is correct, but H0 also needs
  the agent to use only public information and not to move outcomes, so "a property of the baseline,
  not of the agent" was wrong. With more than one claim a round the round rule is not proper: a
  truthful report grows [0.037 nats](numbers.md#round-growth-truthful) a round where a report of
  [0.999](numbers.md#round-best-report) grows [0.143 nats](numbers.md#round-growth-best) (Proposition 7b, reproduced
  exactly). The price assumes a one-year bond; at the season's length an identity costs
  [4,100 sats](numbers.md#identity-cost-season-sats) and the fake [21 BTC](numbers.md#fake-record-cost-season-btc). A
  truthful identity with a small edge needs about [2,722 rounds](numbers.md#rounds-close-single) of one claim.
- **Final.** Prior work, applied, with H0 restated in 05-formal.

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
- **Fresh eyes.** Application of prior work [@turtel2025; @damani2025; @banioharouni2025;
  @cheng2025peerbench]. It does not work for the lab: in training the lab's harness commits the
  agent's claims under keys the lab holds, the lab can commit many definitions under many
  identities, and nothing binds what it actually trains on. Propositions 9, 10 and 10b do not
  address selection, so the table's earlier "proved" was wrong.
- **Final.** Claim 2 cut. The agent-side property is the textbook result for proper scores.

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
- **Fresh eyes.** Prior work: critical mass in two-sided platforms [@evans2010platform;
  @farrell1985], with seed readers a special case of insulating tariffs [@weyl2010]. The algebra and
  the simulation check out (it tips between a 5% and a 9% start); a > 8c holds for uniform types and
  costs only, and nothing is measured.
- **Final.** Prior work, applied, as a toy model.

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
- **Fresh eyes.** Extends prior work narrowly: Somsen's spacechains chain spends one per block from a
  NUMS key tweaked by a commitment, under a covenant [@somsen-spacechains]; Revault supplies the
  cancel, BitVM2 the challenge window, Catena the log. Propositions 1 to 5 hold for a pinned chain,
  and the lab's checks were rerun and pass. Two faults, both reproduced on regtest by
  `lab/fresh_eyes.py`: the pin is a trusted input, so one charter id carried two chains, each
  accepted from its own pin; and at the window's edge the agent outbid a watchtower's veto with a
  child paying [150,000 sats](numbers.md#lab-bid-child-sats) from outside the chain, more than T_n's
  [100,000 sats](numbers.md#lab-bid-tick-sats), and the verifier counted the release.
- **Final.** Extends prior work narrowly. Its properties hold per pinned chain, not per identity.

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
- **Fresh eyes.** Prior work: Substrate's mortal transactions sign a block's hash and are valid
  only in a window after it, checked at the inclusion height [@substrate-mortality]. Proposition 6
  is correct and the lab's checks pass.
- **Final.** Prior work, applied as a lease.

## C7. The clock

- **Novelty.** Searcher B: partial [@trubetskoy2018; @gigi2021; @gilliam2025; @budish2024].
- **Formal.** Arithmetic in the ledger, not a theorem.
- **Working.** Model numbers only.
- **Adversarial.** RT-23 and RT-25: the cost binds only actors below a hashrate majority (timewarp,
  until BIP-54), and borrowing existing hashrate may get cheaper with capability.
- **Change.** Narrowed to actors below a majority.
- **Fresh eyes.** Prior work [@trubetskoy2018; @yang2022]. The arithmetic is right but not
  load-bearing: a pool with [27.8%](numbers.md#pool-largest-share) of blocks beats a six-block veto with
  probability up to [8.9%](numbers.md#reorg-p-largest-6) without speeding the clock.
- **Final.** Prior work.

## C8. Blockspace

- **Novelty.** Searcher B: not found; only capacity concerns.
- **Formal.** Arithmetic: about [1,100,000 releases](numbers.md#tick-releases-per-day-max) at Tier 2 a
  day if they filled every block.
- **Working.** The release size is measured on regtest.
- **Adversarial.** Weak as a safety limit: releases batch many commitments, and the fee auction
  excludes the poor first.
- **Change.** Kept as an observation about the design's capacity, not offered as a safety limit.
- **Fresh eyes.** The method is the capacity arithmetic used for payment channels, applied; the
  arithmetic is right. Read honestly it is a ceiling on the design: about
  [44,000 identities](numbers.md#tick-identities-max) releasing every window would fill every block.
- **Final.** Prior method, an observation.

## C9. The chip clock

- **Adversarial.** RT-24: a frozen header feed, a floor that ratchets down per header, and one
  forgery serving a fleet. **Cut.**

## Paper review

Paperwright ran its three desks on the draft of the paper (before the fresh reviewer's cuts).

- **Integrity desk:** [30 notes](numbers.md#desk-notes-integrity), [5 notes](numbers.md#desk-notes-integrity-important)
  marked important. It checked each cited claim against its source. By its categories: 10
  overstatements, 5 misattributions, 3 conclusions beyond the results, 2 cases of prior work
  presented as the paper's own, 2 results the paper could not trace, 2 attributions, 3 numbers not in
  or not matching the ledger, an uncited input, an unsupported citation and a stray table placement.
  The misattributions: the whitepaper cited for the 2,016-block retarget (now BIP 54); Friedman and
  Resnick credited with proposing bonds (they discuss entry fees and prefer unreplaceable
  pseudonyms); Chan and colleagues credited with advice to seed early adopters (they advise
  high-stakes settings first); Witkowski and colleagues cited for selective participation; and Salib
  and Goldstein credited with a tension nothing held shows them noting. The important notes: the
  lease credited to the paper though Yee checks the window at the including block; a formal appendix
  the paper does not contain (now the formal statements, cited as supplementary material); a fresh
  review reported without its findings (now section 9); and a training reward said to be beyond the
  lab's selection (cut). All corrected.
- **Reviewer desk:** [73 notes](numbers.md#desk-notes-reviewer), recommending major revision. Its main
  points: the record's value over a witnessed transparency log is not shown (now section 7, "The
  stronger alternatives", and left open); H0 is stronger than stated and constrains the agent too
  (restated); standing measures capability, not alignment (now sections 4, 10 and 12); the training
  claim's lab half does not follow (cut); the adoption model's seed readers were underspecified
  (z = max(z_0, min(1, a·x)) added to Proposition 12); the identity bond cannot be forfeited, so
  "recourse" and "liability" overclaimed (withdrawn); the lab's checks show behaviour on one node
  without an adversary (now said).
- **Editor desk:** [61 notes](numbers.md#desk-notes-editor): units, dates, undefined terms (tiers, roles,
  now a table in section 3), and sentences that said more than the evidence.
- **Suggestions:** of 57 rewordings offered, [55 suggestions](numbers.md#desk-suggestions-accepted) were
  accepted as written and two dismissed as superseded by the fresh-eyes rewrite. The comments were
  answered by the major revision of every section and then dismissed.

Paperwright counts a citation inside a table cell as uncited; the three sources cited only in the
building-blocks table are now also cited in prose.

## Fresh eyes

The last reviewer read the claims, the proofs, the paper, the model and the lab, and none of the
novelty searches or this file (`notes/fresh-eyes.md`). It reran the whole lab (104 of 104 checks
pass) and 31 ledger numbers (all match), and built two regtest checks of its own from the lab's
modules, now `lab/fresh_eyes.py`. Its verdicts are in the summary table and under each claim. Every
finding it made that this program could check was reproduced before anything was changed: the
properness table by exact calculation, and both regtest breaks by rerunning them. It broke or
downgraded every claim, and nothing was argued back. It also listed 21 sentences that said more than
the evidence; each was corrected in the paper, the claims, the proofs or the lab's README.
