# Formal statements

Each mechanism in `04-claims.md`, stated precisely, with its key property proved or derived and
the conditions under which it fails. Where the mathematics is a known result, the source is named
and the contribution, if any, is only the application. The verification status of each
proposition (searched, proved, built, attacked, reviewed) is kept in `06-verification.md`.

## Assumptions

- **B1, consensus as deployed.** Relative timelocks (BIP68 and BIP112) count blocks from the
  confirmation of the output being spent [@bip68; @bip112]; an outpoint can be spent once in a
  valid chain; Taproot script-path spends reveal the leaf script and a control block containing
  the internal key [@bip341; @bip342].
- **B2, an honest best chain.** The relying party's best chain is the one most hashrate builds on,
  and a transaction with d confirmations stays in it except with the reorganisation probability
  the model computes for d (for example [19 blocks](numbers.md#depth-for-target-largest) for a
  [0.1%](numbers.md#reorg-risk-target) risk against the largest pool).
- **B3, cryptography.** BIP340 signatures are unforgeable [@bip340]; tagged hashes are collision
  and preimage resistant; nobody knows the discrete logarithm of the NUMS point H; a block's hash
  cannot be predicted before the block is found.

## 1. The tick chain (K7)

**Definition.** An identity's tick chain is a sequence of outputs T_0, T_1, ... where T_0 is the
genesis outpoint named in the identity's charter and, for n ≥ 0, T_{n+1} is output 0 of the
transaction that spends T_n through `advance2`, `advance3` or `renew`. Output T_n has internal key
P_n = H + r_n·G with r_n = TaggedHash("Escapement/tick", id ‖ n ‖ root_n), and the script tree of
`04-claims.md`. Write h(x) for the height of the block that confirms transaction or output x.
Entry n is **released** when T_n is spent through an advance leaf; it is **vetoed** when T_n is
spent through a `veto_i` leaf.

**Proposition 1 (rate).** If entry n is released by a spend through `advance2`, the spend's
height is at least h(T_n) + N2. Consecutive releases are therefore at least N2 blocks apart, and
an identity has at most ⌊W/N2⌋ + 1 releases in any W consecutive blocks.

*Proof.* The `advance2` leaf executes `<N2> OP_CHECKSEQUENCEVERIFY`, which requires the input's
sequence number to encode a height-based relative lock of at least N2 (BIP112), and BIP68 makes
such an input valid only in a block at height at least h(T_n) + N2. T_{n+1} is created by that
spend, so h(T_{n+1}) ≥ h(T_n) + N2, and induction gives the gap between any two releases. ∎

**Proposition 2 (veto).** If a spend of T_n through `veto_i` confirms, entry n is never released.
In each of the N2 blocks at heights h(T_n), ..., h(T_n) + N2 − 1, a veto is valid and no advance is.

*Proof.* An outpoint is spent at most once (B1), so after the veto confirms no advance spend of
T_n is valid. Before height h(T_n) + N2, an advance spend is invalid by Proposition 1, while
`veto_i` has no timelock. ∎

**When the veto fails.** The guarantee needs the veto mined inside its window. If a fraction β
of hashrate refuses to include it and each block's miner is drawn in proportion to hashrate, the
chance that none of the N2 blocks includes it is β^N2. That is
[1.6%](numbers.md#veto-miss-tier2-half) for a six-block window if half of all hashrate censors,
and [4e-44](numbers.md#veto-miss-tier3-half) for 144 blocks. Against miners that are paid to
censor, the literature on timelock bribery applies [@winzer2019; @tsabary2021; @nadahalli2021]:
a myopic miner excludes the veto only if paid at least its fee f_v, so keeping a veto out of N2
blocks costs a briber at least N2·f_v, and the guardians are safe only while N2·f_v exceeds what
the agent gains from the release. That makes veto fees proportional to the stakes of the entry,
and makes the long Tier 3 window, not the short one, the one to rely on for large stakes.

**Proposition 3 (one root per index).** In the best chain there is at most one T_n for each n,
and it commits to exactly one root_n.

*Proof.* T_{n+1} is defined as output 0 of the unique transaction spending T_n, so the chain is
linear. If H + r·G = H + r'·G then r = r', and r = r' for distinct (id, n, root) would be a
collision of the tagged hash (B3). ∎

The relying party must also check that output 0 of each advance is built to the template (it
recomputes the output key from the template keys and the claimed root). An advance that creates
an output off the template ends the identity's chain at that point, and with it the identity's
record.

**Proposition 4 (completeness).** Given the genesis outpoint, anyone with the best chain can list
every entry index 0..n and, given the claimed roots, verify each against its P_n. If each root
commits the number of its leaves (the sum tree carries a count), then a commitment that was put in
an entry cannot be hidden from a scorer without the omission being detectable.

*Proof.* By Proposition 3 the sequence is unique, and n increments by one per link, so a gap is
impossible. The internal key P_n is revealed in the control block when T_n is spent (B1); the
claimed root_n verifies against it only if it is the committed root. A root that commits a count c
cannot be opened to fewer than c leaves. ∎

What completeness does not cover: commitments never put in the chain earn no credit and are
outside the record; an identity can withhold an entry's root altogether, which is why the scoring
rule (K1) treats undisclosed entries as the worst outcome for the maximum number of leaves the
charter allows per entry.

**Proposition 5 (light verification).** A relying party can verify that entry n was released at
tier t with d confirmations from block headers, the raw transactions of the chain links and their
Merkle inclusion proofs, without querying the set of unspent outputs.

*Proof.* Inclusion proofs show each link transaction is in a block of the header chain; the raw
transactions show each link spends the previous one at output 0; the witness shows which leaf was
used and the internal key; the claimed roots verify against the keys. Under B2, a transaction in
the best chain is valid, so the advance spend's validity implies that its timelock was met and that
no veto had spent T_n first. Every fact used is a positive inclusion; none is a statement about
absence. ∎

The weak point is the step "a transaction in the best chain is valid": a light verifier trusts the
headers' proof of work for validity. A chip that sees only headers can be fed a fork whose blocks
contain an advance that the honest chain would reject because a veto came first. Forging that
needs the fork's N + d blocks mined at or above the chip's difficulty floor, which the model
prices (section 8).

## 2. The height-difference lease (K8)

**Definition.** A renewal R_k is a signature by every guardian over (id, k, h_k, hash(h_k)). A
relying party counts a release at height h only if it holds some R_k with block h_k in its best
chain and h_k ≤ h ≤ h_k + L.

**Proposition 6 (not after, without a clock).** If no guardian signs a renewal after the tip is at
height h*, then no release at a height above h* + L is counted by any relying party whose best
chain is the honest one. The rule reads only heights and hashes from the relying party's header
chain, never its clock.

*Proof.* A counted release at height h needs a renewal with h_k ≥ h − L. Signing R_k requires
hash(h_k), which cannot be known before block h_k exists (B3), and every guardian must sign
(B3), so h_k ≤ h*. Hence h ≤ h* + L. The release's height is fixed by its confirmation (B1), so
the agent cannot place it lower. ∎

**When it fails.** A relying party whose header view is stale can be shown only releases inside
that view, all of which were within their lease when made; what it cannot judge is how late it is
acting on them, which is the separate execution deadline. A reorganisation that removes block h_k
voids the renewal, which fails closed. Any one guardian can stop renewals, so the lease is also a
liveness cost: a guardian who disappears ends the agent's authority within L blocks.

## 3. The fake-record cost bound (K2)

**Setting.** An identity makes claims on distinct events. For event t, it commits a forecast q_t
(a distribution over outcomes) in an entry created before the event resolves; b_t is the public
baseline for that event, fixed before it resolves; y_t is the outcome. Order claims by resolution
and let F_t be everything known when the t-th event resolves, including every forecast of every
identity. The null hypothesis H0 for an identity is that it has no edge over the baseline: given
F_{t−1} and the forecasts, y_t has distribution b_t. The record's score is
Λ_T = Π_{t ≤ T} q_t(y_t) / b_t(y_t).

**Theorem 1.** Under H0, for any forecasting strategy, adaptive or coordinated with other
identities, P(sup_T Λ_T ≥ λ) ≤ 1/λ. An adversary controlling K identities, none with an edge,
obtains at least one record with Λ ≥ λ with probability at most K/λ. To succeed with probability
π it needs K ≥ πλ identities, and its cost is at least πλ·c_id.

*Proof.* Given F_{t−1}, E[q_t(y_t)/b_t(y_t)] = Σ_y b_t(y)·q_t(y)/b_t(y) = Σ_y q_t(y) = 1, so Λ is
a nonnegative martingale with Λ_0 = 1. Ville's inequality gives P(sup Λ_T ≥ λ) ≤ 1/λ
[@ville1939; @shafer2019]. The union bound over K identities gives K/λ. ∎

**Corollary (yes or no claims).** Against a baseline of 1/2, a record of m correct confident claims
has λ = 2^m, so faking it with probability π needs πλ = π·2^m identities. The classic scheme of
sending opposite predictions to 2^m recipients meets the bound with π = 1, so it is tight.

**Proposition 7 (the honest path is cheap).** An identity whose forecasts equal the true
conditional distributions p_t has E[ln Λ_T] = Σ_t KL(p_t ‖ b_t). With a mean per-claim edge D, it
reaches ln Λ = ln λ after about ln(λ)/D claims with one identity.

*Proof.* E[ln(p_t(y)/b_t(y))] under p_t is the Kullback-Leibler divergence; sum over t. ∎

So the cost of a record with score λ is about c_id for a skilled honest identity and at least
πλ·c_id for an identity without edge.

**In numbers.** With an identity costing [13,000 sats](numbers.md#identity-cost-sats) (the return
forgone on the reference bond for a year at [5%/yr](numbers.md#capital-cost-rate), plus two
transactions' fees), an all-correct record of [20 claims](numbers.md#fake-record-claims) has
λ = [1,000,000](numbers.md#fake-record-lambda); faking it with a
[50%](numbers.md#fake-record-success) chance needs
[520,000 identities](numbers.md#fake-record-identities) and at least
[70 BTC](numbers.md#fake-record-cost-btc). A skilled identity with a per-claim edge of
[0.12 nats](numbers.md#sim-skilled-edge) reaches the same score in a median of
[116 claims](numbers.md#sim-skilled-claims), with one identity. In simulation, a faker running
[256 identities](numbers.md#sim-identities) reached 2^10 in [22.9%](numbers.md#sim-fake-p) of
trials against a bound of [25.0%](numbers.md#sim-fake-bound); allowed to hide its misses, one
identity reached it in about [20 claims](numbers.md#sim-selective-claims). The ratio grows with λ: the record satisfies the
single-crossing condition that a separating signal needs [@spence1973], which the bond alone does
not (it costs every type the same).

**Rules the bound needs, and failure if they are broken.**

1. *Completeness and pre-resolution commitment* (Propositions 3 and 4). If an identity can drop
   claims after outcomes are known, the product over the kept claims is not a martingale and one
   identity can reach any λ by keeping only its hits.
2. *One forecast per event per identity.* Two forecasts on the same event break the martingale:
   with b = (1/2, 1/2) and both forecasts putting probability 1 on the same outcome,
   E[(q_1/b)(q_2/b)] = 2. The scorer keeps the first forecast on each event.
3. *An honest baseline.* The bound measures edge over the baseline. If the baseline is worse than
   public information, identities that merely use public information well look skilled. The
   baseline should be the best public forecast (a market price or a reference model).
4. *Costly identities.* c_id must be the cost of an identity whose record counts: bond opportunity
   cost over its term, fees, and the forgone use of the capital during seasoning. Seasoning runs in
   parallel, so it adds delay, not cost per identity.
5. *Resolution.* Outcomes must be resolved honestly. A captured resolver breaks everything above.

The bound does not depend on Bitcoin: it needs complete, pre-committed records and costly
identities. Bitcoin supplies those two properties without a registry (sections 1 and 7).

## 4. Bonded promises (K3)

An agent faces a sequence of relying parties. In each period it can keep or break a promise; breaking
gains G, forfeits stake s if the adjudicator rules against it (probability a), and, if future
partners learn of it (probability p), loses the value V of its standing, net of what a fresh
identity would be worth.

**Proposition 8.** Keeping the promise is a best response if G ≤ a·(s + p·V). Complete records
make p = 1 for every partner who checks, so the condition becomes G ≤ a·(s + V). Because a fresh
identity costs c_id plus a season and starts with no record, V is at least the value of the record
lost, which grows with the record.

*Proof.* Compare the payoff of breaking, G − a·s − a·p·V, with zero. ∎

This is the standard logic of reputation and bonds [@klein1981; @shapiro1983], and the role of a
costly identity is the cure for cheap pseudonyms that Friedman and Resnick describe
[@friedman2001]. The application here is only that the record makes p equal to one and makes the
identity costly. **Failure:** near the end of an identity's life V falls to nothing, so the last
promises need s ≥ G/a (the exit scam); gains above a·(s + V) are not deterred (the judgment-proof
case); a ≤ 1 is only as good as the adjudicator.

## 5. Training on complete records (K4)

An agent sees, for each event, its belief p about a yes or no outcome and reports q. The reward for
a counted claim is the log score relative to the baseline, S(q, y) = ln q(y) − ln b(y).

**Proposition 9 (complete records).** If every claim counts, the expected reward is maximised by
q = p for every event, so a learner maximising expected reward is driven towards calibrated
reports.

*Proof.* The log score is strictly proper: E_p[ln q(y)] is maximised uniquely at q = p
[@gneiting2007]. The baseline term does not depend on q. ∎

**Proposition 10 (selection after the outcome).** If the agent may choose which claims count after
the outcome is known, and keeps only claims on whose outcome it put more than one half, the
expected reward is increasing in confidence: it has no finite maximiser in the family
q = σ(a·logit p) as a grows, so a learner is driven towards maximal overconfidence.

*Proof.* A kept claim has y equal to the side the agent favoured, so its score is
ln max(q, 1 − q) − ln b, which increases as q moves away from 1/2, and the misses that would
penalise confidence are never counted. ∎

**Selection before the outcome is harmless here.** If the agent chooses which claims to commit
before outcomes are known, each committed claim has expected relative score KL(p ‖ b) ≥ 0 at
q = p, so committing everything truthfully stays optimal. The harmful selection is after the fact,
which the record's pre-resolution commitment prevents. Scoring relative to a baseline also stops a
learner from farming reward with many trivial claims, whose expected relative score is zero.

**In simulation.** A learner adjusting a by stochastic gradient ascent on its reward settled at
a = [1.06](numbers.md#sim-train-a-complete) under complete records (calibration error
[1.0%](numbers.md#sim-train-err-complete)); started calibrated under after-the-fact selection, it
reached a = [10.4](numbers.md#sim-train-a-selective) and was still rising (calibration error
[24%](numbers.md#sim-train-err-selective)).

What this does not show: that a large model trained this way generalises calibration to other
settings, or that it stays honest where it is not scored. It is the textbook property of proper
scores, shown to survive a learner; its only link to Bitcoin is that the record makes the complete
regime enforceable.

## 6. Adoption (K5)

### One-sided unraveling

Types θ have a continuous density on [0, 1] with mean μ; joining costs c per period. Relying parties
pay a verified agent θ and an unverified one m(t) = E[θ | θ < t], where t is the lowest type that
joins.

**Proposition 11.** If 1 − c > μ, there is an equilibrium in which exactly the types θ ≥ θ* join,
where θ* − c = m(θ*). If m′(t) < 1 for all t (true for every log-concave density
[@bagnoli2005]), it is unique. For θ uniform on [0, 1], θ* = 2c, so a fraction 1 − 2c joins.
Every type above θ* loses θ − c − m(θ*) > 0 per period by staying out.

*Proof.* Joining pays θ − c and staying out pays m(t) regardless of θ, so the joiners form an
upper set {θ ≥ t}. The marginal type is indifferent: t − c = m(t). Let g(t) = t − c − m(t). Then
g(0) = −c < 0 and g(1) = 1 − c − μ > 0, so g has a root by continuity; if m′ < 1 then g′ > 0 and
the root is unique. For the uniform density m(t) = t/2, so t − c − t/2 = 0 gives t = 2c. ∎

This is the unraveling result for verifiable disclosure [@milgrom1981; @grossman1981] with a cost
of disclosure [@jovanovic1982]. The record is what makes disclosure verifiable without a trusted
certifier.

### Two-sided adoption

Relying parties must first choose to read records, at a fixed cost k distributed uniformly on
[0, K]; a reader's gain grows with the share x of agents who have records, as g·x. Let z be the
share of transactions with readers and a = g/K. An agent of type θ gains z·(θ − m) from joining.

**Proposition 12.** With θ uniform, joiners satisfy x = 1 − 2c/z (or x = 0 if z ≤ 2c), and
readers satisfy z = min(1, a·x). If a < 8c, the only equilibrium is no adoption. If a > 8c and
a·x stays below 1, there are three: x = 0 (stable), x_low = (1 − √(1 − 8c/a))/2 (unstable, the
tipping point) and x_high = (1 + √(1 − 8c/a))/2 (stable). A share z_0 of readers who read
regardless of x (insurers pricing agent risk, relying parties with heavy fraud losses) removes the
no-adoption equilibrium when z_0 > 2c, and moves the system to x_high when 1 − 2c/z_0 > x_low.

*Proof.* The marginal joiner satisfies z·(t − t/2) = c, so t = 2c/z and x = 1 − t. Substituting
z = a·x gives a·x² − a·x + 2c = 0, with real roots exactly when a ≥ 8c. Under best-response
dynamics x′ = 1 − 2c/(a·x), the slope at a fixed point is 2c/(a·x²) = (1 − x)/x, which is below
one exactly when x > 1/2, so x_high is stable and x_low is not. With z ≥ z_0 > 2c, x ≥ 1 − 2c/z_0
> 0 from the first step, and if that exceeds x_low the iteration increases to x_high. ∎

### Routing around

**Proposition 13.** In the equilibrium of Proposition 12, an actor that will not join can deal only
with non-readers, a share 1 − z of transactions, or with readers at the price m(θ*) = c/z of the
worst pool. Both its accessible market and its terms worsen as adoption grows.

*Proof.* Readers price the unverified at m(θ*) = θ*/2 = c/z under the uniform density, which falls
as z rises; non-readers are a share 1 − z = 1 − min(1, a·x) that falls as x rises. ∎

**In numbers and in simulation.** With a joining cost of [0.02](numbers.md#sim-join-cost) of the
range of agent value and a = [0.5](numbers.md#sim-gain-over-k), uniform types give a tipping point
at [8.8%](numbers.md#adopt-x-low) of agents and a high equilibrium at
[91%](numbers.md#adopt-x-high); seed readers above [4%](numbers.md#adopt-seed-threshold) remove the
no-adoption equilibrium. The agent-based version (non-uniform types, records that reveal type
gradually, [5%](numbers.md#sim-harmful-share) harmful actors who never join) agrees: from a start
of [2%](numbers.md#sim-start-low) with no seed readers adoption collapses to
[0%](numbers.md#sim-adopt-low-noseed); from [20%](numbers.md#sim-start-high) it reaches
[95%](numbers.md#sim-adopt-high-noseed); with [10%](numbers.md#sim-seed-readers) seed readers it
reaches [95%](numbers.md#sim-adopt-low-seed) from the low start.

**Routing around fails only where business can move.** Proposition 13 is about readers. The
simulation shows what happens at non-readers. If agents cannot move their business between
relying parties, non-readers keep serving everyone at the population's mean terms
([0.45](numbers.md#sim-population-mean)), and a harmful actor that routes around gets
[0.45](numbers.md#sim-harm-terms-nosub): routing around costs it nothing. If agents can move half
their business to relying parties that offer them better terms, verified agents leave the
non-readers, whose pool worsens, and the harmful actor's best terms fall to
[0.31](numbers.md#sim-harm-terms-partial); with full substitution they fall to
[-0.50](numbers.md#sim-harm-terms-full), its own harm, which is to say it must pay in advance for
the damage it does. Claim K5's routing-around part therefore holds only where services are
substitutable, and is downgraded to that condition.

**What this does not show.** It does not stop an actor with its own resources and its own
counterparties, outside the market the model describes; it does not cover a state that mandates a
rival system or bans this one; and it assumes that relying parties' losses from unverified agents
are large enough to make reading worthwhile (a large relative to c). Section 9 lists the
simulations that relax the uniform types, the instant revelation of type, and the absence of
harmful actors.

## 7. The neutral unit (K6)

**Proposition 14 (conservation).** In a scheme where every reward is a transfer from an
identifiable payer, the total reward that any coalition of rewarded agents can obtain is at most
the total that payers outside the coalition transfer. In a scheme where rewards are newly issued
units distributed by a score that the rewarded agents influence, a coalition that captures the
score captures the issuance with no outside payer.

*Proof.* Transfers conserve the unit, so a coalition's net gain is what others paid in. Issuance is
not a transfer. ∎

This is elementary; the point is which side of it a design is on. Networks that pay AI models in
their own newly issued token are on the second side. A fixed-supply unit that no participant
issues is on the first. That is a property of any externally issued fixed-supply asset; what
Bitcoin adds is that its issuance is outside the control of every lab, state and AI, which is the
neutrality argument (K6b), and an argument, not a theorem. Claim K6c, that a stake in a general
resource has positive value to agents with almost any goal, rests on the instrumental-convergence
argument [@omohundro2008] and on the result that optimal policies tend to seek power in a formal
sense [@turner2021]; it is evidence for the claim, not a proof that a particular system values
its stake.

## 8. The clock under attack (K9)

The model computes the cost of running Bitcoin's clock fast: doubling the block rate needs new
hardware drawing [18.4 GW](numbers.md#clock-2x-power-gw), and gains only
[7 days](numbers.md#clock-2x-days-gained) before the next difficulty adjustment; shrinking a Tier 3
delay to an hour needs [24 x](numbers.md#tier3-compress-factor) the network's hashrate. A forged
release fed to a chip that checks headers against a difficulty floor of one quarter of its last
accepted difficulty costs the forger about
[38 blocks of work](numbers.md#chip-forge-blocks-tier3) for a Tier 3 release with six
confirmations, which the model prices at [120,000 MWh](numbers.md#chip-forge-mwh-tier3).
These numbers do not fall as the agent gets faster or smarter; they fall only as hashrate gets
cheaper, which is the sense in which the clock is one the agent cannot speed up.

## 9. What the simulations check

Each of these is run by `model/sim.py` with fixed seeds, and its result is in the ledger.

- **Record faking (Theorem 1).** Many identities without edge, including the opposite-prediction
  scheme, against the bound K/λ; and the claims a skilled honest identity needs to reach λ.
- **Training (Propositions 9 and 10).** A learning agent adjusting its confidence by stochastic
  gradient ascent on the reward, under complete and after-the-fact selective records.
- **Adoption (Propositions 11 to 13).** Agent-based best-response dynamics with non-uniform types,
  types revealed gradually by records rather than at once, readers with integration costs, seed
  readers, and a share of harmful actors that never join.
- **Veto censorship (Proposition 2).** Windows of N blocks against a censoring share of hashrate.
