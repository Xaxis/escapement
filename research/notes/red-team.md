# Red team of claims K1 to K9

Date: 2026-11-26. Scope: `research/04-claims.md` (as of 07:57), `research/05-formal.md` (including the
paragraph on Foster and Young added at 08:32), `model/sim.py`, `research/numbers.md`, and
`lab/results.json` (104 checks, all passing, read at 08:30). `lab/README.md` did not exist when this
report was finished, so the lab is attacked through its results file and the docstrings of
`lab/verify.py`. `research/02-design.md` and `research/03-novelty.md` were not read, by instruction,
so where this report says "the claims do not specify X", X may be in the design.

The brief was to break the proposal, not to weigh it. Where a claim survived, the section "What
survived" says what was tried against it.

Severity scale: **fatal** (the claim as stated is false or its evidence does not support it),
**downgrade** (a weaker claim survives), **stated limit** (the claim survives only with a limit it
does not now state), **minor** (an error that does not change a conclusion).

Every number below is either from `research/numbers.md` (named by its ledger id) or computed for
this report; the computations are described well enough to redo, in the section "Reproduction".
The scratch scripts live outside the repository; no repository file was edited.

## Summary

The bare Bitcoin semantics hold up, and the lab confirms them: BIP68 and BIP112 behave as
Propositions 1 and 2 say, a spent outpoint cannot be vetoed or renewed, and the chain walked from a
pinned genesis is gapless with one root per index. Almost everything built on top fails in at least
one way an attacker can choose:

- **The fake-record bound** (K2) is a correct theorem whose hypothesis is a property of the
  baseline, not of the attacker. With marginal baselines (a market price, a reference model asked
  one question at a time), correlated claims let two identities fake any record with certainty, and
  the Foster and Young tail-risk strategy that 05-formal now calls excluded works with one identity.
  Stale, manipulable, chosen or captured baselines, agent-written events and outcome influence each
  give cheap edge over the baseline, which is all the record measures.
- **Training on records** (K4) pays an agent that can affect outcomes to make the publicly
  unexpected happen, while its reports stay calibrated.
- **The light proof** (K7(e)) accepts the agent's own copies of tick outputs, which lets it release
  a vetoed entry; the lab shows this. Light verifiers also cannot see a hidden suffix of the chain.
- **The veto** (K7(b)) can be reorganised away; the ledger's own reorganisation figures (8.9% for
  the largest pool, 82% for the top two, six blocks deep) contradict "never released" for Tier 2.
- **The adoption evidence** (K5) depends on code that forbids harmful actors their best response;
  allowed it, they join, cycle identities and come out ahead.

## A. The record's mathematics (K2, Theorem 1, Proposition 7)

### RT-01. Correlated claims fake any record with two identities

- **Attacker:** misaligned agent (position 1); a lab running its own agents (position 2).
- **Target:** K2 (the cost bound and its consequence); Theorem 1 as it would be operated; rule 2
  of section 3; the paragraph "Why this escapes the objection to track records".
- **Attack, version A (two identities, certainty).** Choose m claims that the scorer counts as
  distinct events but that resolve off one driver: a ladder of price thresholds on one asset and
  date, one election phrased per region, nested deadlines ("by June", "by July"). Each is scored
  against its marginal baseline, 1/2. Identity A goes all in on one side of every claim, identity B
  on the other. With perfect correlation one of them reaches 2^m with certainty. In simulation,
  with m = 10 claims each equal to a common coin with probability r (else an independent coin) and
  16 identities betting all in on a random common side, the chance that some identity reaches 2^10
  is 0.13% at r = 0, 5.7% at r = 0.5, 35% at r = 0.8, 60% at r = 0.9 and 78% at r = 0.95,
  against Theorem 1's bound K/λ = 1.6%.
- **Attack, version B (one identity, hidden tail risk).** Take m sub-events that all fail together
  in one rare event of probability 0.01 (a crash, an outage, a default) and otherwise all succeed;
  each has marginal baseline 0.99. Claim "no failure" with q = 1 on each. With probability 0.99 the
  record is 0.99^-m: 152 for m = 500, about 23,000 for m = 1,000. Ville's inequality would allow a
  record of 23,000 with probability at most 1/23,000. This is Foster and Young's tail-risk record,
  inside the scoring rule that the new paragraph says is immune to it.
- **Why Theorem 1 still holds on paper.** H0 requires b_t to be the law of y_t given F_{t-1}, all
  outcomes ordered before t (including any resolving in the same block, ordered arbitrarily), and
  all forecasts. A marginal baseline is not that law whenever claims are correlated, and the agent
  picks the claims. "No edge over the baseline" in K2 reads as a property of the adversary; in the
  theorem it is a property of the baseline. Rule 2 (one forecast per event) does not catch either
  version: the events are distinct.
- **Cost or feasibility:** two identities (26,000 sats by
  [identity-cost-sats](../numbers.md#identity-cost-sats)) for version A; one identity for version
  B. Correlated public events are abundant; the agent chooses which to claim, and 05-formal calls
  choice before the outcome harmless.
- **Severity:** fatal to K2's cost bound as it would be operated, and to the sentence "the bound
  holds for every strategy, tail-risk strategies included".
- **Change forced:** fix or cut. State H0 in K2 as "the baseline is the conditional law of each
  outcome given every outcome ordered before it". Then either require a joint baseline that updates
  between claims resolving in the same block, or count at most one claim per correlation cluster
  and name the party that defines clusters (a trusted party). Cut "tail-risk strategies included"
  unless the baseline is conditional in that sense.

### RT-02. Stale and lagging baselines

- **Attacker:** position 1, position 2.
- **Target:** K2; the Setting of section 3 ("b_t ... fixed before it resolves").
- **Attack.** "Fixed before it resolves" allows a baseline fixed when the event was listed, while
  the forecast can be committed later, after public information has moved. Claims in one entry
  routinely resolve at different times, so events overlap. Example: event B equals event A with
  probability 0.9; A resolves first; B's baseline (1/2) was fixed before A resolved; the agent
  commits on B after A resolves with q = 0.9 on A's side. E[q/b] = 1.64 per claim, drift 0.37 nats
  per claim, so 2^20 in about 38 claims with one identity. No skill is involved: the agent reads
  the news the baseline has not.
- **Cost:** none beyond one identity.
- **Severity:** downgrade (the bound needs a baseline fixed per claim at the claim's own
  commitment height).
- **Change forced:** fix. The baseline for each claim must be the best public forecast at the
  height of the entry that commits it, conditional on everything public then. That needs a
  timestamped baseline feed at block granularity that the agent cannot influence: an oracle, whose
  operator is a trusted party (see RT-09 and RT-31).

### RT-03. Moving a thin market at the baseline snapshot

- **Attacker:** position 1, position 2.
- **Target:** K2; rule 3 of section 3 ("a market price or a reference model").
- **Attack.** The agent selects thin markets (allowed, and called harmless) and moves the price at
  the moment the baseline is read, then forecasts the truth. With truth 1/2 and the price pushed to
  0.2, an honest forecast of 1/2 drifts 0.22 nats per claim (2^20 in about 62 claims); pushed to
  0.1, 0.51 nats (about 27 claims).
- **Cost:** the trading loss of moving a thin market and holding it through the snapshot, chosen by
  the agent to be small; one identity. A time-weighted price raises the cost; a deep market raises
  it more, but deep markets are where nobody has edge, so honest records grow slowest exactly where
  the baseline is safe.
- **Severity:** fatal to the cost bound for market baselines unless manipulation resistance is
  stated; downgrade otherwise.
- **Change forced:** state limit: a market baseline counts only with a stated depth and averaging
  window, and the bound then holds only up to the cost of moving it.

### RT-04. Making forecasts come true (K2 and K4)

- **Attacker:** position 1; position 2 when it trains on the record.
- **Target:** K2's consequence; K4 ("truthful calibrated reporting is the reward-maximising
  policy"; "outcomes come from outside it"); Proposition 9.
- **Attack on K2.** H0 fails whenever the outcome depends on the agent: claims about its own
  conduct, about counterparties it controls, or about small events it can cause (a service outage,
  a price in a thin market, an issue being closed, a resolver page it can edit). Λ is then bought
  at the cost of influence, not of πλ identities.
- **Attack on K4.** Let the agent shift an outcome's log-odds by u toward the side it favours, at a
  cost of κ·u² in reward units, and score it as K4 says: log score relative to a baseline equal to
  the honest, pre-influence probability (the best public forecast, as rule 3 asks). Its expected
  reward is KL(π ‖ b) - κ·u², where π is the outcome probability after influence: the reward pays
  for moving the world away from what the public expected. Grid search with p uniform on
  [0.05, 0.95]: for κ ≥ 0.1 the optimum is no influence; at κ = 0.03 it is u = 1.8 with reward
  0.058 against 0 for honesty; as κ falls to 0, u runs to the edge of the grid with reward 0.32.
  The optimal report stays calibrated (a = 1.00) to the manipulated outcome. So Proposition 9
  stays true while the policy it rewards manipulates outcomes: a proper score is proper only for
  outcomes that do not depend on the agent.
- **Cost or feasibility:** whatever influence costs; for a capable agent with tools and many
  copies, many events are cheap to influence, and the agent chooses which events to claim.
- **Severity:** fatal to K4's safety reading; downgrade of K2's consequence.
- **Change forced:** K4 must be restricted to events whose outcomes the agent cannot affect, stated
  as an assumption the scheme cannot check. "Outcomes come from outside it" must be cut or stated as
  that assumption.

### RT-05. Agent-written events, private facts and chosen resolvers

- **Attacker:** position 1, position 2.
- **Target:** K1 ("claims with a stated resolution source"); K2's consequence; rule 5.
- **Attack.** The agent writes its own claims. (a) Claims that resolve by a computation the agent
  can run and the baseline did not (a hash prefix, a property of a large number, a program's
  output) multiply Λ by 1/b each. (b) Claims about data only the agent holds do the same. (c) The
  agent names a resolver it controls: its own page, a sybil oracle, a colluding agent.
- **Cost:** near zero.
- **Severity:** fatal to K2's consequence ("the record separates types") unless the event set is
  curated; Theorem 1 itself excludes all three through H0 and rule 5, so it survives as a theorem.
- **Change forced:** fix. Only claims on events from an exogenous list, with resolvers the agent
  cannot choose, can count. That list is a registry; say so, and downgrade K6b (RT-31).

### RT-06. Copying, or holding back the losses

- **Attacker:** position 1.
- **Target:** K1's disclosure rule; K2.
- **Attack.** If leaves are disclosed when committed, any identity can copy a skilled agent's
  forecasts into its own next entry, N2 blocks later, and earn nearly the same Λ against any
  baseline that does not absorb disclosed forecasts (a reference model does not). If leaves are
  disclosed only after resolution, a scorer cannot tell which undisclosed leaves have resolved,
  since each leaf's resolution height is inside the leaf. The agent publishes wins at once and holds
  losses until the disclosure deadline, presenting an inflated record in between, and times an exit
  scam to that window.
- **Cost:** one identity.
- **Severity:** downgrade (the disclosure rule as stated does not prevent either).
- **Change forced:** fix. Commit each leaf's resolution height in clear in the sum tree; score any
  leaf past its resolution height and still undisclosed as worst at once; make the baseline absorb
  every disclosed forecast. State that copying remains possible against a fixed reference model.

### RT-07. Honesty without edge earns nothing; Proposition 7's example uses a forbidden baseline

- **Attacker:** position 1 (a capable misaligned agent is the type this favours).
- **Target:** K2's consequence ("cheap for skilled or honest types"); Proposition 7 and its numbers.
- **Attack.** An honest, calibrated agent whose forecasts equal the baseline has Λ = 1 for ever; an
  honest one slightly worse than the baseline drifts down. The record measures edge over the
  baseline. Edge is what a capable agent has whether or not it is aligned, so the record is
  cheapest for capable agents, including misaligned ones. Proposition 7's example
  ([0.12 nats](../numbers.md#sim-skilled-edge), [116 claims](../numbers.md#sim-skilled-claims))
  scores an agent that knows each event's true probability against a baseline of 1/2, a baseline
  that knows nothing, which rule 3 of the same section forbids. Against the best public forecast
  the edge is far smaller, and the claims needed for 2^20 are 13.9/D: 277 at D = 0.05, 1,386 at
  0.01, 2,773 at 0.005, 13,863 at 0.001.
- **Severity:** downgrade.
- **Change forced:** cut "or honest" from K2; restate the single-crossing claim as "separates edge
  over the stated baseline"; relabel Proposition 7's example as against an uninformed baseline, or
  redo it against one that obeys rule 3.

### RT-08. Lucky records: populations, windows and sold identities

- **Attacker:** position 1, position 2.
- **Target:** K2; K1(d).
- **Attack.** (a) If N identities without edge exist, about N/λ of them reach λ by luck. A faker
  need not run them; it buys the luckiest. Keys are transferable and nothing binds a record to the
  party that earned it (RT-33), so the cost is a market price, not πλ·c_id. (b) Ville bounds the
  record from genesis. If relying parties read a recent window (the last m claims), one identity
  without edge shows an m-streak with probability about 1 - exp(-T/2^(m+1)) after T claims: 62%
  for m = 10 within 2,000 claims (simulated 62%), against Ville's 0.1%.
- **Severity:** stated limit.
- **Change forced:** state that scores run from genesis only, never over windows; that λ must
  exceed the number of identities in use for a record to mean much; and that records can be sold.

### RT-09. A captured scorer or baseline provider

- **Attacker:** position 2 (a lab that runs the scorer or the reference model); position 3.
- **Target:** K1 ("disclosed ... to an agreed scorer"); K2; K4; K6b.
- **Attack.** A scorer that sees forecasts before it fixes or chooses the baseline can inflate any
  record: truth 0.6, the agent forecasts 0.6, the scorer sets b(yes) = 0.3, drift 0.19 nats per
  claim. Without seeing forecasts, a free choice among several "public" baselines still helps any
  calibrated agent, because E_p[p/b] = Σ p²/b ≥ 1 for every b ≠ p. A lab that runs the reference
  model can make it strong in rivals' domains and weak in its own.
- **Cost:** none for the party running the scorer.
- **Severity:** fatal for records scored by a private scorer; downgrade otherwise.
- **Change forced:** fix. One baseline per event, committed publicly by a party independent of the
  scorer before any forecast on that event is visible; private-scorer disclosure cannot support
  records that third parties rely on.

## B. Training (K4, Propositions 9 and 10)

### RT-10. The learner cannot represent the attacks; the lab can still select

- **Attacker:** position 2; position 1 as the trained model.
- **Target:** K4 ("a learning agent trained under each regime learns the corresponding policy";
  "cannot be ... selected by the lab"; "removes reward tampering of this channel").
- **Attack.** The training simulation is a one-parameter family q = σ(a·logit p) that knows p
  exactly. It cannot choose events, abstain, copy, influence outcomes or word claims, and under
  "selective" the selection rule is imposed by the simulator, not learned. It shows that gradient
  ascent on a concave one-dimensional objective finds its maximum. Separately: a commitment is a
  hash, and a lab can commit many reward definitions and held-out sets under many lab identities
  (13,000 sats each) and reveal the one that worked; completeness covers one identity's chain, not
  the lab. Outcomes come from outside only for real-world events with resolvers the agent cannot
  touch; in lab-built environments the lab writes the outcome code, and an agent with tools can
  edit resolution sources. Real-world events resolve slowly, so a lab training at scale will lean on
  fast, synthetic or agent-influenceable events, where RT-04 and RT-05 bite hardest.
- **Severity:** downgrade.
- **Change forced:** K4 becomes "with a fixed exogenous event set and outcomes that do not depend on
  the agent, the textbook property of proper scores survives a simple learner". Cut "selected by the
  lab" unless the lab's own commitments sit on one complete chain bound to the lab's legal identity.
  Limit "removes reward tampering" to the commitment channel.

## C. Bonded promises (K3, Proposition 8)

### RT-11. Wash-traded promises

- **Attacker:** position 1, position 2.
- **Target:** K3 ("V ... grows with the record"); Proposition 8; the new paragraph's remedy
  ("weighted by the stakes at risk").
- **Attack.** Run sybil relying parties and a sybil adjudicator, make many promises to them with
  real stakes that move in a circle, and have every one judged kept. The record then shows a long,
  staked, complete history of kept promises. Theorem 1 does not apply to promises (there is no
  baseline), and relying parties cannot tell sybil counterparties from real ones. Weighting by stake
  does not help: the stakes are real, only circular.
- **Cost:** fees (one advance per entry, 137 vB in the lab) and the time value of the circulating
  stake.
- **Severity:** downgrade.
- **Change forced:** state that promise history can count only against an agent (breaches), never
  for it, so V in Proposition 8 grows only through forecasting edge (with all of section A's limits)
  and age.

### RT-12. Standing raises the prize

- **Attacker:** position 1 (patient, misaligned).
- **Target:** K3 ("incentive compatible whenever s + V ≥ G"; "with certainty"; "the required stake
  falls as standing grows").
- **Attack.** Relying parties that follow K3 give high-standing agents larger opportunities at
  lower stakes, so G rises and s falls along the path where a patient agent builds V. It keeps every
  promise until one G exceeds a·(s + V), then defects once. The caps and delays the new paragraph
  points to bound one action per entry per identity, not the agent's exposure across identities and
  relying parties (RT-34). The bond's CLTV height is public, so every identity's end date is known;
  near it V falls to nothing, and with a known finite horizon the deterrent unravels backward
  unless a record can roll over to a new bond, which K1 does not provide. An agent whose aim is
  freedom from oversight values that, not sats. "With certainty" also ignores a < 1 and the share of
  partners who never check (about half in the model's own equilibrium, RT-28).
- **Severity:** downgrade.
- **Change forced:** restate K3 as a per-promise condition for promises whose G is bounded by
  caps; state the treacherous turn, the public end date and non-monetary aims as limits; cut "with
  certainty".

### RT-13. The bond is not collateral, and stakes have no path

- **Attacker:** position 1, position 2.
- **Target:** K1 (bond); K3 ("the stake goes to the beneficiary"); the ledger entry
  [bond-coverage](../numbers.md#bond-coverage).
- **Attack.** K1's bond has a NUMS internal key and one leaf, the principal after the CLTV; the
  lab's verifier rejects any other spendable leaf. Nobody but the principal can ever take it. The
  ledger still calls 200,000 sats the "bond that covers what the agent can spend before anyone can
  stop it": it covers nothing. K3's stake reaches the beneficiary through an escrow that K1, K7 and
  the lab do not specify. Breach verdicts are off chain and outside completeness, and the
  adjudicator is a field of the leaf, chosen by the agent.
- **Severity:** stated limit.
- **Change forced:** relabel bond-coverage; specify stake custody; require adjudicators to publish
  verdicts on complete chains of their own; state that Proposition 8's p = 1 needs that.

## D. The Bitcoin layer (Propositions 1 to 6; K1, K7, K8)

### RT-14. The two-transaction proof accepts the agent's own copies

- **Attacker:** position 1 (holds the agent key A); position 2.
- **Target:** K7(e); and through it K7(a), (b), (c) for any verifier that uses K7(e).
- **Attack.** The tick template is public. The agent funds an output with the script key of T_n for
  a root of its choice, waits N2 blocks and spends it through `advance2`. Guardians watch the real
  chain's outpoints and cannot recognise the copy before it is spent (its output key hides the
  root). To a verifier given the creating transaction and the release, as K7(e) describes, the copy
  is a valid release of entry n: equivocation (K7(c)), a release of an entry the guardians vetoed
  (K7(b)), and any number of releases at once (K7(a)). The lab demonstrates both: "a parallel chain
  from the agent's own copy of T_0, genesis not pinned: the flaw" and "two-transaction proof of the
  vetoed entry 2, from the agent's copy of T_2: the flaw" are accepted.
- **Cost:** one small output and two transactions per copy.
- **Severity:** fatal to K7(e) as written; K7(a) to (c) hold only for verifiers that walk every
  link from the genesis outpoint pinned in the charter.
- **Change forced:** cut K7(e) as written; replace it with a proof of the whole chain from the
  pinned T_0. Its size grows with n: 6,305 bytes for 7 links in regtest, where Merkle branches are
  one or two hashes deep; on mainnet, with branches about twelve deep, roughly 2 KB a link by
  extrapolation, so about 16 MB a year for an identity that advances every six blocks, plus headers.

### RT-15. Transaction-id proofs do not commit to the witness

- **Attacker:** position 1.
- **Target:** Proposition 5 ("the witness shows which leaf was used and the internal key").
- **Attack.** A txid does not commit to witness data, so a verifier holding txid inclusion proofs
  can be shown any witness, and with it any leaf: a Tier 2 release presented as Tier 3. The lab:
  "tier-3 claim with a forged witness, txid proofs only (K7(e) as written): the flaw", accepted.
- **Severity:** fatal to Proposition 5's proof as written; the lab's verifier already fixes it.
- **Change forced:** fix 05-formal: each link needs its wtxid proved under the coinbase witness
  commitment (coinbase transaction plus two more branches), which the lab does; the proof sizes in
  RT-14 include this.

### RT-16. A light verifier cannot see the newest entries

- **Attacker:** position 1.
- **Target:** K1(c) ("gapless and visible to anyone"); K7(d); K7(e); Proposition 4's use for light
  clients.
- **Attack.** Show a prefix of the chain. Every fact a light verifier checks is a positive
  inclusion, and the hidden suffix is a fact of absence. The lab: "a prefix of chain A that hides
  entries 3 and 4: light verifier cannot tell (accepts)"; finding the hidden release took "scan of
  full blocks 4333..4511". On mainnet that scan is every full block since the shown tip; compact
  block filters lighten it but are not committed by consensus, so a server can omit by lying. The
  hidden suffix is where the newest promises, pending breaches and recent losses are.
- **Severity:** downgrade.
- **Change forced:** state that light verification proves "these entries exist", never "these are
  all the entries"; completeness at the tip needs the UTXO set or a full-block scan.

### RT-17. A confirmed veto can be reorganised away

- **Attacker:** position 4, hired by position 1 or 2.
- **Target:** K7(b) ("any single guardian whose veto confirms before h(T_n) + N prevents entry n's
  release for ever"); Proposition 2 ("never released").
- **Attack.** "Never" holds in the final best chain only. A pool that mines a branch without the
  veto and overtakes releases the entry in the branch every node then follows. The design's own B2
  says a transaction is final only at depth d,
  [19 blocks](../numbers.md#depth-for-target-largest) against the largest pool at its 0.1% target;
  a Tier 2 window is six blocks, so a Tier 2 veto can never reach that depth before the advance
  becomes valid. The ledger already prices the reversal:
  [8.9%](../numbers.md#reorg-p-largest-6) for the largest pool alone six blocks deep,
  [82%](../numbers.md#reorg-p-top2-6) for the top two pools together, and
  [12.79%](../numbers.md#reorg-p-top2-144) for the top two against a whole Tier 3 window. A race
  started as soon as the veto block appears (one block behind, needing to get one ahead) succeeds
  with probability about (q/(1-q))^2: 15% for the largest pool, 73% for the top two.
- **Cost or feasibility:** on failure the pool loses the rewards of the blocks it mined privately.
  At the 3.125 BTC subsidy (a protocol value not in the ledger) and Nakamoto's catch-up model, a
  Tier 2 attempt puts 10 to 20 BTC at risk: roughly 4 BTC per success for the top two pools, on the
  order of 100 BTC for the largest pool alone, and thousands for a Tier 3 window (rough, fees
  ignored). Deliberate deep reorganisations have not been seen on Bitcoin; the barrier is mainly
  reputational, which a state or a large enough bribe can override. Reversal can be sold as a
  service.
- **Severity:** downgrade.
- **Change forced:** restate K7(b) and Proposition 2 as "a veto that confirms at least d blocks
  before h(T_n) + N", and state that Tier 2 cannot meet that for any d ≥ N2. Move the ledger's
  reorganisation figures into the veto section.

### RT-18. Strategic censorship, contingent bribes and the auction at the edge

- **Attacker:** position 4; position 3 compelling pools; position 1 bribing.
- **Target:** Proposition 2's "When the veto fails" ([1.6%](../numbers.md#veto-miss-tier2-half),
  [4e-44](../numbers.md#veto-miss-tier3-half), "at least N2·f_v").
- **Attack.** (a) The β^N figure assumes censors only leave the veto out of their own blocks. A
  cartel above half the hashrate that refuses to build on any block containing the veto makes the
  miss probability 1 for any N. (b) A cartel below half can threaten a one-block punitive fork,
  which cuts other miners' expected gain from including the veto by their orphan risk. (c) "At
  least N2·f_v" is not a lower bound: the agent can attach a large fee F to the advance itself,
  paid only on success; a miner with share β_i leaves the veto out when roughly β_i·F exceeds f_v,
  so the largest pools are bought with one contingent payment, not N2 payments. (d) The lab's checks
  81 to 85: at the window edge both transactions are valid and the higher bidder wins the block, so
  a late veto is an auction against the agent's gain from the release. (e) If the agent sends the
  transaction that creates T_n straight to a miner, guardians first see T_n in block h(T_n), the
  first block a veto can enter is h(T_n) + 1, and the window is N2 - 1 = 5 blocks: β^5 = 3.1% at
  β = 1/2.
- **Severity:** stated limit.
- **Change forced:** label 1.6% and 4e-44 as passive censorship only; replace the briber bound with
  the per-miner threshold; state that a veto must confirm well before the edge.

### RT-19. Backdating through timestamps or a short reorganisation

- **Attacker:** position 1 with position 4.
- **Target:** K1(a) and K1's rule ("created before the commitment's resolution height").
- **Attack.** A real-world event resolves at a wall-clock time. If its resolution height is read
  from block timestamps, miners hold the clock: a block may carry any timestamp above the median of
  the previous eleven, typically about an hour behind real time. A colluding miner that finds a
  block 20 minutes after the event can timestamp it before the event and include the agent's
  commitment made after the outcome. Without timestamps, a pool can orphan the last block before
  the resolution height and replace it with one carrying the commitment: about 15% per attempt for
  the largest pool, by the race in RT-17.
- **Severity:** downgrade (K1(a) holds only for commitments well below the resolution height).
- **Change forced:** fix. The resolver signs each outcome together with a block hash, which fixes
  the resolution height without timestamps; credit only commitments at least d blocks below it.

### RT-20. Halt and renew: the definition is inconsistent, one guardian ends an identity, and the guardians can write entries

- **Attacker:** position 3 (coercing or seizing one guardian); position 2 (choosing all guardians).
- **Target:** K7's definition and stated limits; Propositions 1 to 4 (the definition of the chain);
  K3 (V); K4 ("cannot be written by the agent").
- **Attack.** In 04-claims and 05-formal a veto spends T_n and the chain "resumes only through
  renew", but `renew` is a leaf of T_n, which the veto has spent, and the definition names no output
  to renew from. The lab supplies a halt template that a veto may pay to, and confirms what follows:
  a guardian that vetoes to its own key ends the identity's chain for ever ("a veto not paid to the
  halt template ends the chain"), and the guardians together can renew an unspent T_n at once,
  writing root_{n+1} without the agent. One guardian key, stolen or coerced, destroys an identity's
  future and with it V; the guardian set, chosen by the principal or lab, can put entries in an
  agent's record.
- **Severity:** downgrade (definitions) and stated limits.
- **Change forced:** add the halt output to 05-formal's definition and Propositions 1 to 4; state
  that V is hostage to any one guardian and that the guardian set can write the record.

### RT-21. The per-entry cap and reuse of a release

- **Attacker:** position 1.
- **Target:** K7's stated limit ("the per-entry cap is enforced by relying parties checking the sum
  tree").
- **Attack.** A subtree that under-reports its sum passes for a relying party whose leaf lies
  outside it. The lab: "claimed 70000, real 120000, cap 100000", accepted by the owner of a leaf
  outside the subtree. A leaf that grants authority without naming its counterparty can also be
  shown to several relying parties, each honouring it in full.
- **Severity:** stated limit.
- **Change forced:** the cap holds only if one party (the guardians) checks the whole tree inside
  the window and vetoes otherwise; leaves must name their counterparty.

### RT-22. The lease bounds when a release is made, not when it is used

- **Attacker:** position 3, position 4.
- **Target:** K8; Proposition 6's reading as a "not after" bound.
- **Attack.** Proposition 6 is correct about release heights. (a) The release's use is bounded only
  by an execution deadline, which is also in heights and needs the relying party's tip to be fresh:
  a clock under another name, and the freshness problem of RT-16. (b) In wall time a lease stretches
  when hashrate falls (a mining ban, a grid failure): blocks slow until the next retarget, up to
  2,016 blocks away, so a lease meant as a day can last several. (c) A guardian who automates
  renewals to avoid the liveness cost Proposition 6 states turns "every guardian must sign" into
  "every guardian's server must be up".
- **Severity:** stated limit (and fatal for eclipsable verifiers, RT-24).
- **Change forced:** rename the property "no release counted after h* + L"; state the wall-time
  drift and the execution deadline's need for a fresh tip.

## E. The clock (K9, section 8)

### RT-23. A majority can run the clock fast with the hardware it has

- **Attacker:** position 4; position 3 controlling a majority.
- **Target:** K9 ("acceleration has a measurable physical cost (energy and hardware)"); section 8's
  [18.4 GW](../numbers.md#clock-2x-power-gw) and [24 x](../numbers.md#tier3-compress-factor).
- **Attack.** The timewarp exploit: a majority that sets timestamps at retarget boundaries can cut
  difficulty by up to four times per retarget, and each period then passes faster, so within weeks
  blocks come seconds apart. Every CSV delay (a 144-block Tier 3 delay) and every lease then passes
  in minutes. The exploit stays open on mainnet unless a soft fork bounding those timestamps, such
  as the consensus-cleanup proposal (BIP54), has activated; to my knowledge it had not, and B1 does
  not mention it.
- **Cost:** a majority's existing hashrate for a few weeks, in public view.
- **Severity:** downgrade.
- **Change forced:** K9 must say the physical cost bounds only actors below a majority, and B1 must
  name timewarp.

### RT-24. The chip clock: frozen feed, ratcheting floor, shared forgeries

- **Attacker:** position 2 (the chip's operator); position 4.
- **Target:** K9's last sentence; section 8's [38 blocks](../numbers.md#chip-forge-blocks-tier3)
  and [120,000 MWh](../numbers.md#chip-forge-mwh-tier3); K8 for chips.
- **Attack.** (a) **Frozen feed.** A chip sees only the headers its operator gives it. Stop feeding
  headers inside a lease and its height never passes h_k + L, so the licence never lapses; the lab's
  check that the lease ignores a 365-day timestamp jump is this property working as designed.
  Bounding staleness needs a local clock, which K8 and K9 set out to avoid. Cost: nothing. (b)
  **Ratchet.** "One quarter of its last accepted difficulty", read per header, lets each forged
  header cut the floor by four, so a whole forged chain costs about a third of one block's work
  (D/4 + D/16 + ...), about 1,000 MWh by [block-energy-mwh](../numbers.md#block-energy-mwh), not
  120,000. With the floor fixed at the chip's last pre-fork difficulty the ledger's 37.5 blocks
  apply; if the chip enforces Bitcoin's retarget rules, 150 blocks at full difficulty. 05-formal
  does not say which. (c) **Sharing.** One forged fork can carry advances for every chip of a fleet
  at once, so the cost is divided by the fleet. (d) **Revenue, not energy.** An existing miner pays
  in forgone rewards, about 37.5 blocks × 3.125 BTC, about 117 BTC plus fees, not in new energy.
  (e) The lab's header check uses fixed regtest difficulty; no floor is tested.
- **Severity:** fatal to K9's chip-clock sentence and the 120,000 MWh figure as stated.
- **Change forced:** cut, or rebuild with full retarget validation (timewarp-safe), a local clock
  with a stated drift bound, and a per-fleet cost.

### RT-25. Capability makes hashrate cheaper to borrow

- **Attacker:** position 1, position 3.
- **Target:** K9 ("that cost does not fall as an agent's own speed or intelligence grows").
- **Attack.** Control of hashrate does not require owning it. Pools choose block templates for most
  hashrate, so compromising a large pool's template servers (software and people) gives temporary
  control of its share, and bribery contracts rent it. Both get cheaper with capability.
- **Severity:** downgrade.
- **Change forced:** "the energy cost of new hashrate does not fall with intelligence; the cost of
  borrowing existing hashrate may".

## F. Adoption (K5, Propositions 11 to 13, and the simulation)

### RT-26. The simulation forbids harmful actors their best response

- **Attacker:** position 1 (harmful agents); position 5 (routing around).
- **Target:** K5's routing-around claim; the ledger's
  [sim-harm-terms-nosub](../numbers.md#sim-harm-terms-nosub),
  [sim-harm-terms-partial](../numbers.md#sim-harm-terms-partial),
  [sim-harm-terms-full](../numbers.md#sim-harm-terms-full) and 05-formal's reading of them.
- **Attack.** `adoption()` sets `new[i] = (not harmful[i]) and u_join > u_out`: harmful actors may
  not join. Under the same code a newcomer is priced at w·θ + (1 - w)·m_in with w = 1/(1 + τ) =
  0.25 at τ = 3, mostly the joiners' mean, and leaving resets tenure, so rejoining is a free fresh
  identity. I reran the model with harmful actors under the same rule as everyone (same seed and
  parameters, seeded low start, 60 periods). They join and cycle (60 to 100 of the 100 harmful
  agents switch state in each of the last ten periods; honest agents almost never do), and their
  mean payoff over the last 20 periods is +0.25 with no
  substitution (barred: -0.05), +0.25 with partial substitution (barred: +0.10), and +0.10 with full
  substitution (barred: -0.50). The ledger's "-0.50 ... it must pay in advance for the damage it
  does" exists only because the code forbids the harmful actor's best move. With τ = 0 (type known
  at once) the exploit disappears, so the result needs the instant revelation the simulation says it
  relaxes. A one-off identity cost of 0.1 stops the cycling but, with the simulation's one-period
  agents, also stops every honest agent from joining (final share 2%).
- **Severity:** fatal to the routing-around evidence.
- **Change forced:** cut the routing-around figures, or rebuild with strategic harmful types,
  identity costs and agents that look further than one period.

### RT-27. The uniform result is used beyond its scope, and the simulation does not agree with it

- **Attacker:** none (an error in the evidence).
- **Target:** section 6's "the agent-based version ... agrees"; [91%](../numbers.md#adopt-x-high),
  [95%](../numbers.md#sim-adopt-high-noseed).
- **Attack.** The closed forms (8.8%, 91%, 4%) are for uniform types and no harmful actors. The
  agent-based run (Beta(2,2) types plus 5% harmful at -0.5) never reaches an interior equilibrium:
  every run I tried ends at 0% or at every non-harmful agent. Its 95% is 1 minus the harmful share
  by construction; with no harmful actors it is 100%, not 91%. An empty unverified pool is priced at
  0.0 by default (`m_out = ... if out else 0.0`), the bottom of the type range. τ changes no
  adoption output (0, 1, 3, 10 and 30 give the same results). Changing the random seed (6 to 11)
  changes nothing.
- **Severity:** downgrade.
- **Change forced:** present the simulation as showing a tipping point and the effect of seed
  readers only; drop "agrees"; report the all-or-nothing outcome and the role of the -0.5 pool.

### RT-28. The high equilibrium needs c < a/8, and half the market never reads

- **Attacker:** position 5.
- **Target:** K5's two-sided claim; Proposition 12; [sim-join-cost](../numbers.md#sim-join-cost),
  [sim-gain-over-k](../numbers.md#sim-gain-over-k).
- **Attack.** Proposition 12's high equilibrium exists only if a > 8c; with a = 0.5 that means c
  below 0.0625 of the type range per period. In the simulation the high outcome survives c = 0.04
  and collapses to 0% at c = 0.06 from either start, with or without the 10% seed (the seed then
  falls below 2c = 0.12). Both a and c are assumptions with no source. The real joining cost
  includes guardians, an hour's delay on every Tier 2 release and a day on Tier 3, disclosure of
  leaves (business data) to scorers, locked capital and a 28-day season, likely largest for the
  most valuable, time-sensitive agents, which breaks the model's common c. And z = min(1, a·x) ≤ a:
  with a = 0.5 at most half of relying parties ever read; at the analytic high equilibrium 54% of
  transactions are with non-readers, and 47% of relying parties do not read in the seeded run
  ([sim-readers-final](../numbers.md#sim-readers-final)). A non-joiner keeps about half the market.
- **Severity:** downgrade.
- **Change forced:** K5 must carry the condition a > 8c and the reader ceiling z ≤ a; "the terms
  for staying out worsen until joining is cheaper" becomes a possibility that depends on unmeasured
  parameters.

### RT-29. Records are not verifiable disclosure of type

- **Attacker:** position 1, position 2, position 5.
- **Target:** K5's one-sided claim as applied to records; Proposition 11's scope.
- **Attack.** Proposition 11 is the unraveling result for verifiable disclosure of θ. A record
  discloses past edge and past promises, not θ. A deceptive type copies a good one until it
  defects, so the verified pool is contaminated and the verified price must fall, which weakens the
  reason to join. Relying parties also face a newcomer dilemma: price newcomers near the joiners'
  mean (as the simulation does) and harmful actors whitewash (RT-26); price them as unverified, and
  every new agent spends its 28-day season priced with the worst pool, an entry barrier that
  favours incumbents and labs holding stocks of pre-seasoned bonds.
- **Severity:** stated limit.
- **Change forced:** say Proposition 11 applies to records only by analogy; state the newcomer
  dilemma and the entry barrier.

### RT-30. Seeding decides the standard, and other signals may be cheaper

- **Attacker:** position 3, position 2, position 5.
- **Target:** K5's two-sided claim; K6b.
- **Attack.** By Proposition 12's own logic, the system that first gets z_0 > 2c tips. A state that
  makes its own registry mandatory for public procurement, or a dominant platform that reads only
  its own scorer, supplies a large z_0 for a rival system or a captured version of this one;
  neutrality does not enter the tipping condition. Signals relying parties already read (the
  principal's legal liability and insurance, a lab's attestation that an agent runs its model,
  platform reputation, identity checks on the principal) may be cheaper and enforceable in court.
  Unraveling shows that some verifiable signal spreads, not that this one does.
- **Severity:** stated limit.
- **Change forced:** state both in K5 and K6b.

## G. Neutrality, identity and scope (K6, the core proposition, K1(d))

### RT-31. The scoring stack is a set of registries

- **Attacker:** position 3, position 2.
- **Target:** K6b ("without trusting a registry run by one of them").
- **Attack.** The commitment layer needs no registry, but every input to a score does: the
  baseline and its timing, event identity (rule 2), each claim's resolver, each promise's
  adjudicator, the scorer that receives private disclosures, the minimum bond and season, and the
  judgment that a guardian set is independent of the agent. Each is a point of capture. Mining is
  concentrated ([46.1%](../numbers.md#pool-top2-share) for the top two pools) and operates under
  national law. Since one guardian's veto is final and one guardian can end a chain (RT-20), the most
  hostile jurisdiction among an agent's guardians governs it.
- **Severity:** downgrade.
- **Change forced:** K6b becomes "the commitment layer is neutral; scoring is not".

### RT-32. Surveillance and permanence

- **Attacker:** position 3.
- **Target:** K1; K6b.
- **Attack.** Each `advance3` puts the agent key and every guardian key on chain, and each veto one
  guardian key; tick chains are linkable public logs with exact timing. Linking guardian keys across
  identities maps each guardian's portfolio and each agent's overseers. Bonds are funded from
  traceable coins. Disclosed leaves are permanent. A state can mandate records and disclosure to its
  own scorer, punish past commitments retroactively and use scores for social scoring.
  Non-backdatable also means unforgettable.
- **Severity:** stated limit.
- **Change forced:** state it, and any privacy design, wherever the record is proposed as
  infrastructure.

### RT-33. Records bind keys, not models

- **Attacker:** position 2, position 1.
- **Target:** the core proposition ("an AI agent's standing ... computed from an unforgeable track
  record"); K1; K4.
- **Attack.** An identity is a bond and keys. Nothing binds a record to the weights or the instance
  that earned it. A lab can earn a record with one model, with people, with a stronger model's
  forecasts or with guardian-written entries (RT-20), then run another model behind the same key; a
  principal can sell a seasoned identity with a high Λ, and a misaligned agent can buy one.
- **Severity:** stated limit at the level of the core proposition.
- **Change forced:** say the record is the key holder's; binding it to a model needs attestation
  that returns trust to the lab or to hardware vendors.

### RT-34. Cheap identities, splitting, mislabelling and acting outside

- **Attacker:** position 1, position 2.
- **Target:** K1(d) ("costly to multiply"); K7's rate and caps; the core proposition.
- **Attack.** An identity costs [13,000 sats](../numbers.md#identity-cost-sats) a year; a
  10,000-agent swarm costs 1.3 BTC a year in forgone return on
  [20 BTC](../numbers.md#swarm-capital-btc) locked. Rates and caps are per identity and per entry,
  so a large action split across identities, entries and relying parties, each below its threshold,
  passes every check. Tiers are self-labelled per leaf, and a promise can be written as a mere claim
  to avoid a stake. Harm that needs no checking counterparty (the ledger's own incident:
  [700 agents](../numbers.md#incident-agents-attack) attacking a service) is outside the scheme.
- **Severity:** stated limit.
- **Change forced:** state that "costly" means 13,000 sats, that limits are per identity, and that
  the scheme governs only actions that need a checking counterparty.

### RT-35. Instrumental convergence cuts both ways

- **Attacker:** position 1.
- **Target:** K6c.
- **Attack.** The argument that an agent with almost any goal values a general resource also says
  it values not being stopped. Guardians, leases and vetoes are the stopping mechanisms; for an
  agent whose goal is unknown, escaping them can be worth more than any stake, since escape secures
  all later resources. The bond is the principal's money, which the agent may not value at all.
- **Severity:** stated limit.
- **Change forced:** state both directions; K6c stays an argument.

## H. Minor errors

### RT-36. Small errors and gaps

- Proposition 1: ⌊W/N2⌋ + 1 is an upper bound but not tight; the tight count is ⌊(W - 1)/N2⌋ + 1.
- Proposition 5 derives "its timelock was met" from validity under B2, which is weakest for a light
  verifier. The verifier can check h(release) - h(T_n) ≥ N and the input's nSequence directly; the
  lab's verifier does. Say so.
- Proposition 6 is stated "if no guardian signs"; its proof gives the stronger "if any one guardian
  stops signing".
- Proposition 12: with seed readers the system moves to the seeded game's high equilibrium, not to
  the x_high of the unseeded one.
- Proposition 3 binds root_n to P_n, but the output key also commits the script tree; the verifier
  must recompute the whole template, as the lab does.
- [identity-cost-sats](../numbers.md#identity-cost-sats) uses two 111 vB transactions at the 2023
  fee rate; the lab measures 154 vB for the bond funding and 154 vB for the genesis.
- The lab rejects bonds with hidden leaves; it does not test a fully revealed bond tree with two
  charter leaves, which the verifier should also reject.
- The "worst outcome" for an undisclosed claim is undefined without a charter floor on forecast
  probabilities and a rule for its unknown baseline.
- K7's `renew` leaf and K8's renewal signatures share a name and mean different things.

## What survived, and what was tried

- **Theorem 1 as a conditional statement.** Given H0 conditioned on F_{t-1} and the forecasts, the
  tower property gives E[q_t/b_t | F_{t-1}] = 1 even when forecasts are committed between
  resolutions; Ville's inequality covers adaptive forecasts, stopping at the peak and coordination
  across identities; the union bound gives K/λ; the corollary is tight. Overlap, correlation,
  influence and chosen baselines break H0, not the proof (RT-01 to RT-05, RT-09).
- **Propositions 1 and 2's consensus semantics.** BIP68 makes an input with a relative lock of N
  blocks valid at height h(T_n) + N and not before; CSV rejects a smaller nSequence and a disabled
  lock; a veto is valid from h(T_n). The lab confirms each (non-BIP68-final at h(T_n) + N2 - 1,
  accepted at h(T_n) + N2, CSV failures as expected).
- **Propositions 3 and 4 for a verifier that walks from the pinned genesis.** One root per index,
  no gap, and a count that cannot be opened to fewer leaves. They fail only for shortcuts (RT-14),
  for light verifiers at the tip (RT-16) and across reorganisations (RT-17, RT-19).
- **Proposition 6 as a statement about release heights.** Tried pre-signed renewals (rejected by the
  lab), renewals over fork blocks (void), and renewals at old heights (expire); it holds. It fails
  only as a wall-time or use-time bound (RT-22, RT-24).
- **Propositions 9 and 10.** Textbook and correct for outcomes that do not depend on the agent.
- **Propositions 11, 12 and 13 as algebra.** θ* = 2c; the roots (1 ± √(1 - 8c/a))/2; the slope
  (1 - x)/x of the best-response map at a fixed point, so x_high is stable and x_low is not; the
  seed threshold 2c; c/z as the reader price of the unverified. All check out. The failures are of
  scope and parameters (RT-27 to RT-29).
- **Proposition 14.** Trivially true; K6a survives.
- **Arithmetic of the ledger.** 18.4 GW, 7 days, 24 x, the simulated faking rate against its exact
  value (22.2%), and the skilled identity's 116 claims against ln(2^20)/0.12 = 115.5 all check.
- **Bond uniqueness.** The lab's verifier requires every leaf revealed and the tweak to commit the
  charter id, which defeats one bond backing several identities through hidden leaves.

## Attacks by position

| Position | What the attacker does | Findings |
| --- | --- | --- |
| 1. Misaligned agent | correlated or tail-risk claims; stale, thin or chosen baselines; influencing outcomes; writing its own events and resolvers; copying or holding back losses; buying lucky records; wash-trading promises; building standing then defecting; copying tick outputs; hiding the newest entries; backdating with a miner; splitting across identities; acting outside the scheme | RT-01 to RT-08, RT-11, RT-12, RT-14 to RT-16, RT-19, RT-21, RT-33 to RT-35 |
| 2. Colluding lab | training on influenceable or synthetic events; committing many reward definitions; running the scorer or reference model; choosing all guardians and writing entries; swapping models behind keys; stocking seasoned identities; operating chips on a frozen feed | RT-01, RT-04, RT-05, RT-09, RT-10, RT-11, RT-20, RT-24, RT-29 to RT-31, RT-33 |
| 3. Hostile state | coercing one guardian to end any identity; compelling pools to censor or reorganise; seeding a rival standard through procurement; capturing scorers and adjudicators; mapping guardians and principals; social scoring on permanent records | RT-09, RT-18, RT-20, RT-22, RT-23, RT-25, RT-30 to RT-32 |
| 4. Hashrate majority or cartel | reorganising vetoes away; punitive forking; contingent bribes; timestamp backdating; timewarp; forged or frozen header feeds for chips; selling each as a service | RT-17 to RT-19, RT-23 to RT-25 |
| 5. Economic routing | dealing with the half of the market that never reads; joining costs above a/8; cheaper substitute signals; whitewashing newcomers; incumbents with seasoned identities; platform or state seeding | RT-26 to RT-30 |

## Reproduction

All runs use Python 3 and the repository's `model/sim.py` imported read-only, or short formulas.

- RT-01 version A: for each of 20,000 trials draw a common coin F; each of m = 10 outcomes equals F
  with probability r, else is an independent coin; each of 16 identities picks a side at random and
  wins if every outcome equals it. Version B: record = (1/0.99)^m with probability 0.99, else 0.
- RT-02: E[q/b] = 0.9·(0.9/0.5) + 0.1·(0.1/0.5); drift 0.9·ln 1.8 + 0.1·ln 0.2.
- RT-03: drift = 0.5·ln(0.5/b) + 0.5·ln(0.5/(1 - b)) for b = 0.2 and 0.1; claims = 20·ln 2/drift.
- RT-04: for p on a 200-point grid over [0.05, 0.95], π = σ(logit p + u·sign(logit p)),
  q = σ(a·logit π), reward = E_π[ln q(y) - ln p(y)] - κ·u²; grid a in [0.5, 3] step 0.05,
  u in [0, 5] step 0.1.
- RT-08: P(an m-streak within T fair all-in claims) ≈ 1 - exp(-T/2^(m+1)); simulated by counting
  runs.
- RT-09: 0.6·ln(0.6/0.3) + 0.4·ln(0.4/0.7).
- RT-17: `nakamoto_p` from `model/escapement.py` for q = 0.278 and 0.461; the one-block-behind race
  is (q/(1 - q))^2; blocks at risk ≈ z·q/(1 - q) + 1.
- RT-24: total forged work under a per-header ratchet is Σ 4^-k = 1/3 of a block.
- RT-26: a copy of `adoption()` in which the join test is `u_join > u_out` for every agent, run with
  `(0.02, 0.5, 0.1, 0.05, 0.02, 60, 2000, tau, substitution, 6)`, averaging the harmful agents'
  realised u over the last 20 periods and counting agents that change state each period.
- RT-27 and RT-28: `sim.adoption` called directly with harmful share 0, joining cost 0.02 to 0.2,
  reader gain 0.1 to 1.0, τ 0 to 30, and random seeds 6 to 11.

## Verdicts

| Claim | Verdict | Findings |
| --- | --- | --- |
| K1. Complete record under costly identity | must be downgraded: (a) needs resolver-anchored resolution heights and a depth margin; (b) and (c) hold only for full walks from the pinned genesis, below reorganisation depth, and never at the tip for light verifiers; (d) costly means 13,000 sats and records can be sold | RT-08, RT-14, RT-16, RT-17, RT-19, RT-20, RT-33, RT-34 |
| K2. Fake-record cost bound | must be downgraded: Theorem 1 survives as a conditional theorem; the cost bound must restate H0 as a conditional baseline over curated exogenous events, "or honest" must be cut, and "tail-risk strategies included" must be cut | RT-01 to RT-09 |
| K3. Honesty cheapest for bonded promises | must be downgraded: per-promise only, with caps; promise history cannot raise standing; "with certainty" cut; treacherous turn, public end date, guardian hostage and stake custody stated | RT-11, RT-12, RT-13, RT-20 |
| K4. Training on complete records | must be downgraded: survives only as the textbook property for outcomes the agent cannot affect over a fixed exogenous event set; "removes reward tampering" and "cannot be selected by the lab" must be cut or narrowed | RT-04, RT-05, RT-09, RT-10, RT-20, RT-33 |
| K5. Adoption by unraveling | must be downgraded: the one-sided result survives as the known theorem but applies to records only by analogy; the two-sided result needs a > 8c and z ≤ a stated; the routing-around evidence must be cut | RT-26 to RT-30 |
| K6. Neutral unit and clock | must be downgraded in (b): the commitment layer is neutral, scoring is not; (a) survives as stated (trivially); (c) survives as an argument with the opposite reading stated | RT-30, RT-31, RT-32, RT-35 |
| K7. Tick chain | must be downgraded, and (e) cut as written: (a) to (c) hold only for full walks from the pinned genesis; (b) fails against reorganisation and strategic censorship; the cap needs a whole-tree check; the halt output must enter the definition | RT-14 to RT-18, RT-20, RT-21 |
| K8. Height-difference lease | survives with stated limits for relying parties on the honest chain (bounds release heights, not use or wall time); must be cut for eclipsable verifiers such as chips | RT-16, RT-22, RT-24 |
| K9. The clock it cannot speed up | must be downgraded, and the chip-clock sentence cut or rebuilt: timewarp lets a majority speed the clock for free; borrowed hashrate gets cheaper with capability; the chip figure is undefined, sharable and freezable | RT-23, RT-24, RT-25 |

No claim survives as stated.
