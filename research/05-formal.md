# Formal statements

Each mechanism in `04-claims.md`, stated precisely, with its key property proved or derived and
the conditions under which it fails. Where the mathematics is a known result, the source is named
and the contribution, if any, is only the application. The verification status of each
proposition (searched, proved, built, attacked, reviewed) is kept in `06-verification.md`.

This is the second version. The red team (`notes/red-team.md`) and the regtest lab (`lab/`) broke
four statements of the first: the light proof of a release (Proposition 5), the finality of a veto
(Proposition 2), the bound on faking a record when claims are correlated (Theorem 1 as it would be
operated), and the adoption simulation's treatment of harmful actors. Each is restated or cut
below, and the place says so.

## Assumptions

- **B1, consensus as deployed.** Relative timelocks (BIP68 and BIP112) count blocks from the
  confirmation of the output being spent [@bip68; @bip112]; an outpoint can be spent once in a
  valid chain; Taproot script-path spends reveal the leaf script and a control block containing
  the internal key [@bip341; @bip342]. Block heights count blocks, but the time between them can be
  shortened by a hashrate majority through the timewarp bug until BIP-54 is active [@bip54].
- **B2, an honest best chain.** The relying party's best chain is the one most hashrate builds on,
  and a transaction with d confirmations stays in it except with the reorganisation probability
  the model computes for d (for example [19 blocks](numbers.md#depth-for-target-largest) for a
  [0.1%](numbers.md#reorg-risk-target) risk against the largest pool).
- **B3, cryptography.** BIP340 signatures are unforgeable [@bip340]; tagged hashes are collision
  and preimage resistant; nobody knows the discrete logarithm of the NUMS point H; a block's hash
  cannot be predicted before the block is found.

## 1. The tick chain (K7)

**Definition.** An identity's tick chain starts at T_0, an outpoint named in the identity's charter
(the chain is **pinned** by it). For n ≥ 0, T_{n+1} is output 0 of the transaction that spends T_n
through `advance2` or `advance3`, or that spends the halt output of index n through `renew`.
Output T_n has internal key P_n = H + r_n·G with r_n = TaggedHash("Escapement/tick", id ‖ n ‖
root_n), and the script tree of `04-claims.md`. A veto spends T_n through `veto_i` and pays to the
**halt output** of index n, whose internal key is H + TaggedHash("Escapement/halt", id ‖ n)·G and
whose only leaf is `renew`. Write h(x) for the height of the block that confirms transaction or
output x. Entry n is **released** when T_n is spent through an advance leaf, and **vetoed** when
it is spent through a veto leaf.

Consensus enforces the waits, the signatures and single spending. Four rules are relying parties'
rules, checked by recomputing keys from the template: output 0 of each advance or renew must be
the template output for the next index; a veto must pay to the halt output of its index, and a
veto paid anywhere else ends the chain; only links that descend from the pinned T_0 count; and each
link is proved with its witness (below).

**Proposition 1 (rate).** If entry n is released by a spend through `advance2`, the spend's height
is at least h(T_n) + N2. Consecutive releases of one pinned chain are therefore at least N2 blocks
apart, and it has at most ⌊W/N2⌋ + 1 releases in any W consecutive blocks.

*Proof.* The `advance2` leaf executes `<N2> OP_CHECKSEQUENCEVERIFY`, which requires the input's
sequence number to encode a height-based relative lock of at least N2 (BIP112), and BIP68 makes
such an input valid only in a block at height at least h(T_n) + N2. T_{n+1} is created by that
spend, so h(T_{n+1}) ≥ h(T_n) + N2, and induction gives the gap. A renew spends a halt output,
which exists only after a veto of T_n, and a veto makes no release. ∎

The bound is per pinned chain. The lab funded copies of the template for an index the agent chose,
which consensus cannot tell apart from the real T_n because the root is hidden in the tweak; only
the relying party's pinning rule excludes them.

**Proposition 2 (veto).** In any valid chain that contains a veto of T_n, entry n is not released.
In each block at heights h(T_n), ..., h(T_n) + N − 1 (N = N2 or N3) a veto is valid and no advance
is. If the veto confirms at height h_v, a chain that releases entry n must branch below h_v and
reach the best chain's length with the advance at a height of at least h(T_n) + N.

*Proof.* An outpoint is spent at most once (B1), so no advance spend of T_n is valid in a chain
containing the veto. Before height h(T_n) + N an advance is invalid by the argument of
Proposition 1, while `veto_i` has no timelock. A chain without the veto that agrees with the best
chain at h_v must differ from it below h_v. ∎

**When the veto fails.**

- *Reorganisation.* A miner with share q that begins a private branch when the veto confirms
  releases the entry if its branch overtakes the honest chain once the advance is valid, which is
  Nakamoto's catch-up problem with z = h(T_n) + N − h_v blocks [@nakamoto2008]. A veto in a Tier 2
  window has z of at most [6 blocks](numbers.md#tier2-delay-blocks), so it can never reach the
  [19 blocks](numbers.md#depth-for-target-largest) that B2 treats as final against the largest
  pool; at six blocks that pool overtakes with probability up to
  [8.9%](numbers.md#reorg-p-largest-6), and the two largest together up to
  [82%](numbers.md#reorg-p-top2-6). A Tier 3 veto confirmed at once has z near
  [144 blocks](numbers.md#tier3-delay-blocks), where the two largest together still succeed with
  up to [12.79%](numbers.md#reorg-p-top2-144). These are upper bounds that treat a pool as one
  miner and ignore the block rewards it forfeits when an attempt fails; deliberate deep
  reorganisations have not been seen on Bitcoin. So a veto is as final as a payment with z
  confirmations, and Tier 2 vetoes hold against everyone short of a bribed large pool.
- *Censorship.* If a fraction β of hashrate simply refuses the veto, the chance that none of N
  blocks includes it is β^N: [1.6%](numbers.md#veto-miss-tier2-half) for six blocks when half of
  hashrate refuses, and [4e-44](numbers.md#veto-miss-tier3-half) for 144. Those figures hold only
  for passive refusal. A briber can pay miners to exclude the veto [@winzer2019; @tsabary2021;
  @nadahalli2021], cheaply when it can threaten a fork [@avarikioti2024], and at the window's edge
  the veto and the advance are both valid, so the edge is a fee auction: in the lab, under full
  replace-by-fee, the agent's advance evicted the veto package and the watchtower won the slot back
  only by outbidding it. A veto must therefore confirm well before the edge, with a fee that
  reflects what the entry is worth, and a flood of transactions that congests the chain can delay
  many vetoes at once [@harris2020].
- *Guardians' power.* `<Gi> OP_CHECKSIG` cannot constrain where the veto pays. One guardian that
  vetoes to its own key ends the identity's chain for good and keeps the tick output's value (the
  lab did this), so the record's value is hostage to any one guardian. And `renew` needs every
  guardian and not the agent, so the guardians together can write an entry the agent never made.

**Proposition 3 (one root per index).** In the pinned chain there is at most one T_n for each n,
and it commits to exactly one root_n.

*Proof.* T_{n+1} is output 0 of the unique transaction spending T_n or its halt output, so the
pinned chain is linear. If H + r·G = H + r'·G then r = r', and r = r' for distinct (id, n, root)
would be a collision of the tagged hash (B3). ∎

**Proposition 4 (completeness).** A verifier that walks the pinned chain from T_0 to the tip, with
full blocks or the set of unspent outputs, lists every entry index 0..n and, given the claimed
roots, verifies each against its P_n. If each root commits the number of its leaves (the sum tree
carries a count), a commitment put in an entry cannot be hidden from a scorer without the omission
being detectable.

*Proof.* By Proposition 3 the sequence is unique and n increments by one per link, so a gap is
impossible. The internal key P_n is revealed in the control block when T_n is spent (B1); a claimed
root verifies against it only if it is the committed one. A root that commits a count c cannot be
opened to fewer than c leaves. ∎

What completeness does not cover: commitments never put in the chain; roots the agent withholds,
which is why the scoring rule (K1) treats undisclosed entries as the worst outcome for the maximum
number of leaves the charter allows; and the newest entries for a verifier without full blocks. In
the lab a truncated chain passed the verifier, and finding the hidden release took a scan of full
blocks.

**Proposition 5 (chain proof; replaces the light proof of the first version).** A relying party
can verify that entry n of a pinned chain was released at tier t with d confirmations from block
headers and, for every link from T_0 to the release, the transaction, a Merkle proof of its txid,
and a proof of its wtxid under the coinbase's witness commitment (BIP141), without querying the set
of unspent outputs. It cannot verify from these that no later link exists.

*Proof.* The proofs place every link in a block of the header chain, and the wtxid proofs bind
each link's witness, so the leaf used and the signatures are those that were mined. Each link
spends the previous one, back to the pinned T_0, which excludes copies of the template. Under B2 a
transaction in the best chain is valid, so the advance's timelock was met and no veto spent T_n
first. Every fact is a positive inclusion. ∎

The first version proved a release with two transactions and txid proofs. The lab broke both
parts: txid proofs leave out the witness, so the agent swapped in the `advance3` leaf with junk
signatures and a verifier accepted a Tier 3 release that no guardian signed; and two transactions
cannot show that T_n is the identity's own, so the agent released a vetoed entry through a copy of
T_n it funded itself. The chain proof grows with the chain: [901 bytes](numbers.md#chain-proof-bytes-per-link) a link on regtest, where Merkle branches are one
or two hashes deep, and more on mainnet, plus headers.

## 2. The height-difference lease (K8)

**Definition.** A renewal R_k is a signature by every guardian over (id, k, h_k, hash(h_k)). A
relying party counts a release at height h only if it holds some R_k with block h_k in its best
chain and h_k ≤ h ≤ h_k + L.

**Proposition 6 (no release counted after h* + L).** If no guardian signs a renewal after the tip
is at height h*, then no release at a height above h* + L is counted by any relying party whose
best chain is the honest one. The rule reads only heights and hashes from the relying party's
header chain, never its clock.

*Proof.* A counted release at height h needs a renewal with h_k ≥ h − L. Signing R_k requires
hash(h_k), which cannot be known before block h_k exists (B3), and every guardian must sign (B3),
so h_k ≤ h*. Hence h ≤ h* + L. The release's height is fixed by its confirmation (B1), so the agent
cannot place it lower. ∎

**When it fails.** It bounds when a release is made, not when the released action is carried out;
an execution deadline needs a fresh view of the tip, and a relying party that is eclipsed sees an
old one [@riard2020]. A reorganisation near h_k + L can move a release across the boundary, and one
that removes block h_k voids the renewal, which fails closed. Any one guardian can stop renewals, so
a guardian who disappears ends the agent's authority within L blocks. In the lab the verdicts held
as stated, and did not change when block times jumped a year or when every clock function was
disabled. The first version called this a "not after" bound and offered it as a clock for chips;
both are withdrawn (section 8).

## 3. The fake-record bound (K2)

**Setting.** An identity's claims are scored in **rounds** that do not overlap. A round's claims
are committed in one entry; the round settles when the last of them resolves; the next round's
claims count only if their entry is confirmed after that. Claim i of round k has a forecast q_i (a
distribution over outcomes), a weight w_i committed in the entry (w_i ≥ 0, Σ w_i = 1), a baseline
b_i and an outcome y_i. Let F_k be everything public when round k settles. The round multiplies the
score by M_k = Σ_i w_i·q_i(y_i)/b_i(y_i), and the record's score is Λ_K = Π_{k ≤ K} M_k.

**H0 (a property of the baseline).** Each b_i is the law of y_i given F_{k−1}, that is, given
everything public when round k opens, and is committed publicly by a party independent of the agent
and of the scorer before any forecast on the event is visible. Events come from an exogenous list,
and the agent cannot choose who resolves them.

**Theorem 1.** Under H0, for any strategy, adaptive or coordinated with other identities, and
however the outcomes within a round are correlated, P(sup_K Λ_K ≥ λ) ≤ 1/λ. An adversary
controlling K identities obtains at least one record with Λ ≥ λ with probability at most K/λ. To
succeed with probability π it needs at least πλ identities, at a cost of at least πλ·c_id.

*Proof.* The forecasts and weights of round k are fixed before it opens, so given F_{k−1},
E[M_k] = Σ_i w_i·E[q_i(y_i)/b_i(y_i)] = Σ_i w_i·Σ_y b_i(y)·q_i(y)/b_i(y) = Σ_i w_i = 1, by
linearity of expectation, which needs nothing about the joint law of the outcomes: each ratio is an
e-value, and a mean of e-values is an e-value under any dependence [@vovk2021]. So Λ is a
nonnegative martingale over rounds with Λ_0 = 1, and Ville's inequality gives
P(sup Λ_K ≥ λ) ≤ 1/λ [@ville1939; @shafer2019; @shafer2021]. The union bound over identities gives
K/λ. ∎

**Why rounds and means.** The first version multiplied every claim's ratio and took H0 to say that
the agent has no edge. But H0 is a property of the baseline, and a marginal baseline is not the
conditional law of an outcome once the agent picks claims that move together. The red team broke it
two ways (RT-01). With claims that mostly follow one common coin, 16 identities each betting a
side on every claim reached 2^10 in [99.8%](numbers.md#sim-corr-product-p) of simulated trials,
against a bound of [1.6%](numbers.md#sim-corr-bound). And one identity that makes [1,000 claims](numbers.md#tail-claims) of "no failure" on sub-events that all fail together in one event of probability
[1%](numbers.md#tail-fail-p) scores about [23,000](numbers.md#tail-product-score) 99% of the time:
Foster and Young's tail-risk record [@foster2010], inside the scoring rule. Under the round rule the
same attack succeeded in [1.1%](numbers.md#sim-corr-round-p) of trials, inside the bound, and the
tail-risk record scores [1.01](numbers.md#tail-round-score). The mean needs no party to decide which
claims are correlated, which the alternative (one claim per correlation cluster) would. The
mathematics is Vovk and Wang's averaging of e-values [@vovk2021]; the rule only applies it to a
record.

**Corollary (yes or no claims).** Against a baseline of 1/2 a round's factor is at most 2, so a
record of λ = 2^m needs at least m rounds, and faking it with probability π needs πλ identities.
Sending opposite predictions to 2^m recipients, one round each, meets the bound with π = 1, so it is
tight.

**Proposition 7 (an identity with edge).** If an identity's forecasts are the true conditional laws
p_i, which the baseline does not have, then with one claim per round E[ln Λ_K] = Σ_k KL(p_k ‖ b_k),
and it reaches λ after about ln(λ)/D rounds, D being its mean edge per claim. More claims per round
raise the growth per round only up to a limit, since a mean of ratios grows at most like
ln(1 + χ²(p ‖ b)) per round.

*Proof.* E[ln(p(y)/b(y))] under p is the Kullback-Leibler divergence; sum over rounds. For many
claims per round, the mean of the ratios tends to its expectation under p, which is 1 + χ²(p ‖ b). ∎

The example in the ledger is an identity that knows each event's probability p, drawn uniformly
from [0.1](numbers.md#sim-skilled-p-low) to [0.9](numbers.md#sim-skilled-p-high), when the best
public forecast is 1/2: the knowledge is private, which is what edge means here. It has a mean edge
of [0.12 nats](numbers.md#sim-skilled-edge) per claim and reaches 2^20 in a median of
[116 claims](numbers.md#sim-skilled-claims) made one a round, or
[74 rounds](numbers.md#sim-skilled-rounds) of [10 claims](numbers.md#sim-round-claims), with one
identity.

**In numbers.** With an identity costing [13,000 sats](numbers.md#identity-cost-sats) (the return
forgone on the reference bond for a year at [5%/yr](numbers.md#capital-cost-rate), plus two
transactions' fees), an all-correct record of [20 claims](numbers.md#fake-record-claims) one-claim rounds
against a baseline of 1/2 has λ = [1,000,000](numbers.md#fake-record-lambda); faking it with a
[50%](numbers.md#fake-record-success) chance needs
[520,000 identities](numbers.md#fake-record-identities) and at least
[70 BTC](numbers.md#fake-record-cost-btc). In simulation a faker running
[256 identities](numbers.md#sim-identities) reached 2^10 in [22.9%](numbers.md#sim-fake-p) of
trials against a bound of [25.0%](numbers.md#sim-fake-bound); allowed to hide its misses, one
identity reached it in about [20 claims](numbers.md#sim-selective-claims). The record separates
edge over the stated baseline, which a bond cannot do, since a bond costs every type the same
[@spence1973]. It does not separate honesty: a forecaster without edge earns nothing by being
honest.

**What the bound needs, and what breaks it.**

1. *Completeness and pre-resolution commitment* (Propositions 3 and 4). If claims can be dropped
   after outcomes are known, the product over the kept claims is not a martingale and one identity
   reaches any λ by keeping its hits. Each leaf commits its resolution height in clear, the resolver
   signs each outcome with a block hash, a claim counts only if its entry is at least d blocks below
   that height, and a leaf past its resolution height and not disclosed scores as the worst outcome
   at once (RT-06, RT-19).
2. *One forecast per event per identity.* Two forecasts on the same event break the martingale:
   with b = (1/2, 1/2) and both forecasts putting probability 1 on one outcome, the expected
   product is 2. The scorer keeps the first forecast on each event.
3. *A baseline that satisfies H0.* A stale baseline, one in a thin market that the agent can move,
   one the agent or the scorer chose, or one on events the agent wrote makes edge cheap (RT-02,
   RT-03, RT-05, RT-09). A market baseline counts only with a stated depth and averaging window,
   and the bound then holds only up to the cost of moving the market. The event list, the baseline
   provider and the resolvers are registries run by trusted parties.
4. *Costly identities.* c_id is the cost of an identity whose record counts: bond opportunity cost
   over its term, fees, and the capital idle during seasoning. Seasoning runs in parallel, so it
   adds delay, not cost per identity.
5. *Scores from genesis.* A score over a chosen window is a fresh test each time the window moves.
   And λ must exceed the number of identities in use for a high score to mean much: among a
   million identities without edge, some reach a million by luck (RT-08).
6. *Records that stay with their makers.* A record can be sold with its keys, and it binds a key,
   not a model (RT-33).

**The objection to track records.** Foster and Young show that return histories cannot separate
skilled from unskilled portfolio managers, because a manager without skill can buy a good-looking
record by taking hidden tail risk [@foster2010]. Under the round rule and H0, Theorem 1 holds for
every strategy, tail-risk strategies included, because a round's factor is a mean of fair bets;
under the product rule it did not. The answer covers forecasts only. Records of promises behave
like returns, since an agent can keep many small promises and break one large one, so promise
history counts only against an agent (section 4), and the caps and delays of the enforcement layer,
not the record, bound the one large breach.

## 4. Bonded promises (K3)

An agent faces a sequence of relying parties. In each period it can keep or break a promise; breaking
gains G, forfeits stake s if the adjudicator rules against it (probability a), and, if future
partners learn of it (probability p), loses the value V of its standing, net of what a fresh
identity would be worth.

**Proposition 8.** Keeping the promise is a best response if G ≤ a·(s + p·V). Complete records
make p = 1 for every partner who checks, so the condition becomes G ≤ a·(s + V). Because a fresh
identity costs c_id plus a season and starts with no record, V is at least the value of the record
lost. The condition is per promise: it bounds promises whose gain G the enforcement layer caps, not
an agent's conduct overall.

*Proof.* Compare the payoff of breaking, G − a·s − a·p·V, with zero. ∎

This is the standard logic of reputation and bonds [@klein1981; @shapiro1983], and the role of a
costly identity is the cure for cheap pseudonyms that Friedman and Resnick describe
[@friedman2001]. The application here is only that the record makes p equal to one and makes the
identity costly. **Failure:** near the end of an identity's life V falls to nothing, so the last
promises need s ≥ G/a (the exit scam); gains above a·(s + V) are not deterred (the judgment-proof
case); a ≤ 1 is only as good as the adjudicator, and p = 1 needs adjudicators to publish their
verdicts on complete chains of their own. Standing raises the prize, so an agent with a valuable
record and a public end date, or with aims that are not monetary, is the case the condition does
not cover (RT-12). **Wash trading:** an agent can make promises to sybil counterparties judged by a
sybil adjudicator and keep them all, for fees alone (RT-11). So promise history counts only against
an agent, as a record of breaches, never for it; V grows only through forecasting edge (section 3)
and age.

## 5. Training on complete records (K4)

An agent sees, for each event, its belief p about a yes or no outcome and reports q. The reward for
a counted claim is the log score relative to the baseline, S(q, y) = ln q(y) − ln b(y).

The training reward is the sum of per-claim scores, not the round rule of section 3: the round
rule protects a tail bound on standing, while training needs a reward whose expectation the truth
maximises.

**Proposition 9 (complete records).** If every claim counts, the expected reward is maximised by
q = p for every event, however the events are correlated, so a learner maximising expected reward
is driven towards calibrated reports.

*Proof.* The log score is strictly proper: E_p[ln q(y)] is maximised uniquely at q = p
[@gneiting2007]. The baseline term does not depend on q, and the expectation of a sum is the sum of
the expectations, whatever the joint law. ∎

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

**Proposition 10b (outcomes the agent can affect).** Suppose the agent can take an action u that
moves the outcome's law from b to π_u, at a cost κ(u), and reports calibrated forecasts q = π_u.
Its expected reward is KL(π_u ‖ b) − κ(u), which grows as the outcome is pushed away from the
baseline. Training on such events rewards making unexpected things happen, while the reports stay
calibrated.

*Proof.* E_π[ln π(y) − ln b(y)] = KL(π ‖ b). ∎

This is the performative-prediction problem [@perdomo2020] in its starkest form, and the red team's
RT-04: Proposition 9 stays true while the policy it rewards is manipulative. Claim K4 therefore
holds only on events whose outcomes the agent cannot affect, an assumption the scheme cannot check.
The record removes selection after the fact by the agent, and by the lab if the lab commits its
reward definition on a chain of its own; it does not stop the lab choosing the event list, and it
does not remove tampering with anything but the commitment channel (RT-10).

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
of disclosure [@jovanovic1982]. A record is not a verifiable disclosure of type: it reveals type
gradually, and a newcomer has none. The proposition applies to records only by analogy, and the
newcomer's position is an entry barrier (RT-29).

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

Two conditions carry the result. The high equilibrium exists only when a > 8c, and readers never
exceed a share a of relying parties, so with a below one some relying parties never read records
and an agent that stays out keeps dealing with them (RT-28). Whoever supplies the seed readers
largely decides which standard wins, and a cheaper substitute signal could win instead (RT-30).

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
no-adoption equilibrium. The agent-based version (non-uniform types, records that reveal type over
about [3 periods](numbers.md#sim-tenure-tau) periods, [5%](numbers.md#sim-harmful-share) harmful actors
under the same rules as everyone) shows the tipping point and the effect of seed readers, and
nothing more: from a start of [2%](numbers.md#sim-start-low) with no seed readers adoption collapses
to [0%](numbers.md#sim-adopt-low-noseed); from [20%](numbers.md#sim-start-high) it reaches
[100%](numbers.md#sim-adopt-high-noseed); with [10%](numbers.md#sim-seed-readers) seed readers it
reaches [100%](numbers.md#sim-adopt-low-seed) from the low start. Its outcomes are all or nothing,
unlike the interior equilibrium of the uniform case.

**Routing around: not shown.** Proposition 13 describes an actor that stays out. A harmful actor
need not. The first simulation barred harmful actors from joining, and on that basis reported that
routing around costs a harmful actor its whole harm where business can move. That was wrong
(RT-26). Allowed to join, harmful actors do: while a record is young it is priced mostly at the
joiners' mean, so they join, leave as their records start to show, and rejoin under fresh
identities; [60%](numbers.md#sim-harm-switch) of them change state each period. Their mean payoff
is [0.25](numbers.md#sim-harm-payoff-nosub) when business cannot move,
[0.25](numbers.md#sim-harm-payoff-partial) with partial substitution and
[0.10](numbers.md#sim-harm-payoff-full) with full substitution, against a population mean of
[0.45](numbers.md#sim-population-mean) and a true value of their own of -0.5. Only if records
revealed type at once did harmful actors lose: [-0.05](numbers.md#sim-harm-payoff-instant-nosub)
with business fixed and [-0.50](numbers.md#sim-harm-payoff-instant-full) with business free to
move. A one-off cost per identity large enough to stop the cycling also stopped honest agents from
joining, because the simulated agents look only one period ahead. The claim that staying out comes
to cost a harmful actor more than joining is therefore cut. A test of it would need agents that
plan over many periods, identity costs paid once and amortised, and harmful types that choose their
strategy.

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
neutrality argument (K6b), and an argument, not a theorem. The neutrality covers the commitment
layer only. The event list, the baselines, the resolvers and the adjudicators of sections 3 and 4
are trusted parties, so scoring is a set of registries, and choosing among them is not neutral
(RT-31). Claim K6c, that a stake in a general
resource has positive value to agents with almost any goal, rests on the instrumental-convergence
argument [@omohundro2008] and on the result that optimal policies tend to seek power in a formal
sense [@turner2021]; it is evidence for the claim, not a proof that a particular system values
its stake. The same fact cuts the other way: rewarding an agent in a scarce general resource also
rewards it for acquiring that resource (RT-35).

## 8. The clock and the blockspace (K9)

The model computes the cost of running Bitcoin's clock fast with new hardware: doubling the block
rate needs hardware drawing [18.4 GW](numbers.md#clock-2x-power-gw), and gains only
[7 days](numbers.md#clock-2x-days-gained) before the next difficulty adjustment; shrinking a Tier 3
delay to an hour needs [24 x](numbers.md#tier3-compress-factor) the network's hashrate. These costs
do not fall as an agent gets faster or smarter. Two limits narrow the claim (RT-23, RT-25). A
hashrate majority can run the clock fast with the hardware it already has, through the timewarp
bug, until BIP-54 is active [@bip54], so the physical cost binds only actors below a majority. And
while the energy cost of new hashrate does not fall with intelligence, the cost of borrowing
existing hashrate, by renting it or bribing pools, may.

Blockspace bounds the total rate of releases: about
[1,100,000 releases](numbers.md#tick-releases-per-day-max) a day at Tier 2 if they filled every block,
or [44,000 identities](numbers.md#tick-identities-max) releasing every Tier 2 window. A release
costs [137 sats](numbers.md#tick-release-cost-2026) at the 2026 median fee rate and
[27,400 sats](numbers.md#tick-release-cost-halving) at the halving block's. As a safety limit this
is weak: releases can batch many commitments, and the fee auction excludes the poor first.

**Cut: the chip clock.** The first version offered Bitcoin headers with a difficulty floor as the
licence clock of AI chips, with a forgery cost of thousands of blocks' worth of energy. The red team
broke it (RT-24): an operator who stops feeding headers freezes the chip's view, so a lease never
lapses; a floor set relative to the last accepted difficulty ratchets down one header at a time,
so the forged work is about a third of one block, not dozens; and one forged fork serves every chip
in a fleet. A chip clock would need full retarget validation that is safe against timewarp, a
local clock with a stated drift bound, and a cost per fleet; none of that is designed here.

## 9. What the simulations check

Each of these is run by `model/sim.py` with fixed seeds, and its result is in the ledger.

- **Record faking (Theorem 1).** Many identities without edge, including the opposite-prediction
  scheme, against the bound K/λ; correlated claims under the product rule and the round rule; the
  rounds an identity with edge needs to reach λ.
- **Training (Propositions 9 and 10).** A learning agent adjusting its confidence by stochastic
  gradient ascent on the reward, under complete and after-the-fact selective records. The learner
  cannot act on outcomes, so it does not test Proposition 10b.
- **Adoption (Propositions 11 to 13).** Agent-based best-response dynamics with non-uniform types,
  types revealed gradually by records, readers with integration costs, seed readers, and harmful
  actors under the same rules as everyone, with and without substitution, and with type revealed at
  once.
- **Veto censorship (Proposition 2).** Windows of N blocks against a passively censoring share of
  hashrate.

The Bitcoin pieces (bond, tick chain, halt and renew, chain proof, lease, co-signing, anchoring,
TRUC veto, Merkle-sum tree) are built and checked on regtest in `lab/`, with 104 checks.
