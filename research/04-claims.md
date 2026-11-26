# The claims under test

This file states each candidate contribution precisely enough to be searched for, proved, built,
attacked and reviewed. It says nothing about why a claim might be new, so that the people and
helpers who check novelty start from the claim, not from the author's case for it. Each claim's
result at every level of verification is in `research/06-verification.md`.

The claims below are the **repaired** versions. The first versions (git history, 2026-11-26) went to
two independent prior-art searches, a regtest build and a red team. Where a level broke a claim,
the claim was cut or narrowed here, and each section ends with what changed and which finding forced
it (RT-nn are the red team's findings in `research/notes/red-team.md`; "the lab" is `lab/`).

A last reviewer that had seen none of the work then judged each claim (`research/notes/fresh-eyes.md`).
It broke or downgraded every one, and its two regtest breaks are rerun by `lab/fresh_eyes.py`. Each
section now ends with what that review changed, under *After fresh eyes*. **Nothing in this file is
claimed as new.** One part, the covenant-free tick chain, extends prior work narrowly; the rest is
prior work, applied, or cut.

Notation: a **principal** is the human or organisation answerable for an AI agent; a **relying
party** is anyone who acts on the agent's word or request (an API, a merchant, a counterparty, a
lab's evaluator, an insurer); **guardians** are independent key holders who can stop the agent; N,
L, S are block counts.

## The core proposition

An AI agent's standing in the economy (what it may do, at what price, with what trust) can be
computed in part from a **complete track record**: an ordered, non-backdatable record of the
commitments it asked anyone to rely on, kept under one identity that costs locked bitcoin. Three
consequences are claimed, each only under its stated conditions.

1. For forecasts on events from an exogenous list, scored in rounds against a baseline published by
   a party independent of the agent and the scorer, a record showing a given edge over that
   baseline costs an agent without that edge a number of identities that grows in proportion to the
   score, provided its forecasts use only public information, its actions do not move outcomes, and
   each identity's chain is bound to its bond (a binding not yet specified or built). The record
   measures edge over the baseline. It does not measure honesty. This is prior work, applied.
2. On events whose outcomes the agent cannot affect, a strictly proper score summed over every
   resolved claim gives a reward the agent cannot raise by choosing which claims count (prior work).
   The claim that the lab cannot select is **cut**: it can commit many reward definitions, and no
   commitment binds what it actually trains on.
3. Requiring records is a coordination game with a tipping point (prior work, applied). Parties that gain from reading
   records whatever others do can move it past the tipping point when the gain from reading exceeds
   eight times the cost of joining. Whether staying out becomes costlier than joining for a harmful
   actor is **not** shown: in the corrected simulation it does not.

The three share one record only in name. Standing, scored by the round rule, rewards bets; the
training reward, a proper score, rewards calibrated forecasts; the same leaves cannot serve both
unless each carries a forecast and a separate stake.

## Contributions to be tested

### K1. The complete record under costly identity

- **Identity.** One identity is one **bond**: a Taproot output holding at least B sats, spendable
  by the principal only after an absolute timelock (CLTV), whose internal key is a NUMS point
  tweaked by a hash of one charter id, so one output can back one identity and has no key path.
  The bond must be at least S blocks old before the identity's record counts (seasoning).
- **Record.** Each identity has one **tick chain** (K7), pinned by the outpoint of its T_0. Entry n
  is the Merkle-sum root committed in T_n; its leaves are commitments: claims, promises and
  requests. Each leaf commits in clear its kind and its resolution height; the tree commits the
  count of leaves and their total stake.
- **Rules.** A scorer credits a commitment only if it is a leaf of an entry of that identity's
  pinned chain, confirmed at least d blocks below the commitment's resolution height, where the
  resolution height is fixed by the resolver signing the outcome together with a block hash. A leaf
  past its resolution height and not disclosed (to the public or to an agreed scorer) scores as the
  worst outcome at once. An entry with undisclosed leaves scores as if every leaf, up to the
  charter's maximum per entry, had the worst outcome. Scores run from genesis only, never over a
  chosen window.
- **Claimed properties.** (a) Non-backdatable for commitments at least d blocks below their
  resolution height. (b) One root per index in the pinned chain. (c) Gapless from the pinned T_0,
  for a verifier that walks every link; a light verifier learns that entries exist, not that it has
  seen all of them up to the tip. (d) Costly to multiply: each identity needs its own bond and
  season, about [13,000 sats](numbers.md#identity-cost-sats) a year at the reference parameters.
- **Limits.** The record binds a key, not a model: tying it to a model needs attestation, which
  returns trust to the lab or a hardware vendor. Records can be sold with their keys. The guardian
  set can write entries without the agent (K7), and any one guardian can end the identity.

*Changed:* resolution heights in clear, scoring of overdue leaves, the d-block margin, the pinned
T_0 and the light-verifier limit (RT-06, RT-08, RT-14, RT-16, RT-19, RT-33, RT-34; the lab, items 2
and 5). The searches found every property prior (Catena, OpenTimestamps, fidelity bonds,
Merkle-sum trees); the assembly was not found, and the fresh reviewer later found the worst-case
scoring of silence in a forecasting subnet.

*After fresh eyes:* **cut as a contribution.** Nothing on chain binds a tick chain to its bond. T_0's
key commits the charter id, so a charter that also named T_0's outpoint would be circular, and the
lab handed the pin to the verifier. On regtest one charter id carried two chains with different
roots at entry 1, each accepted from its own pin. Properties (b), (c) and (d) therefore hold per
pinned chain, not per identity, and one bond can back many chains. A binding is proposed (the
identity is the bond's outpoint, and T_0 is a named output of the bond's own transaction) but not
built, and it collides with renewing a bond without losing the record. The record is complete per
identity, not per operator: an operator can hide whole identities, which the bound prices and
completeness does not prevent. Scoring silence as the worst outcome is prior work (Infinite Games).
Standing and the training reward ask for different reports from the same leaves (K2).

### K2. The fake-record bound

An identity's claims are scored in **rounds** that do not overlap: a round's claims are committed in
one entry, the round settles when the last of them resolves, and the next round's claims count only
if their entry is confirmed after that. Each claim i in a round has a forecast q_i, a weight w_i
committed in the entry (the weights sum to one) and a baseline b_i. The round multiplies the score
by the weighted mean of the claims' likelihood ratios, Σ w_i q_i(y_i) / b_i(y_i).

- **Hypothesis H0** (a condition on the baseline and on the agent together): each b_i is the law of
  outcome y_i given everything public at the height of the entry that opens the round, and is
  committed publicly, before any forecast on the event is visible, by a party independent of the
  agent and of the scorer; the agent's forecasts and weights use only that public information; and
  its actions do not move the outcomes. Events come from an exogenous list; the agent cannot choose
  the resolver.
- **Claim.** Under H0 the score is a nonnegative martingale over rounds for any strategy that meets
  it, however the claims within a round are correlated, so the probability that it ever reaches λ is at
  most 1/λ (Ville's inequality). An adversary with K identities gets one record of λ or more with
  probability at most K/λ; success with probability π needs at least πλ identities and costs at
  least πλ·c_id. An identity whose forecasts beat the baseline reaches λ with one identity in a
  number of rounds that grows with ln λ.
- **Consequence claimed.** The record separates edge over the stated baseline; a bond alone costs
  every type the same and separates nothing.
- **Limits.** The bound is only as meaningful as the baseline: a stale, thin or captured baseline
  makes edge cheap, and a market baseline holds only up to the cost of moving the market. A
  forecaster with no edge earns nothing from honesty alone. The roles that make H0 true (the event
  list, the baseline provider, the resolvers) are registries run by trusted parties. With more
  identities in use than λ, high scores appear by luck.

*Changed:* the first version multiplied every claim's ratio and read H0 as "the agent has no edge".
Correlated claims chosen by the agent broke it: with 16 identities and claims that move together it
succeeded [99.8%](numbers.md#sim-corr-product-p) of the time against a bound of [1.6%](numbers.md#sim-corr-bound), and a single identity with a hidden tail risk
scored about [23,000](numbers.md#tail-product-score) (RT-01). The round rule restores the bound without a trusted party deciding
which claims are correlated; its mathematics is prior work (Vovk and Wang: a mean of e-values is an
e-value under any dependence), added after the searches ran. "Or honest" and "tail-risk strategies included" are cut (RT-07, RT-01).
The searches found the logic in Resnick and Sami's influence limiter; the closed form under costly
identities and the round rule were not found by them.

*After fresh eyes:* **downgraded to prior work.** K ≥ πλ is a union bound on Ville's inequality, and
the round rule is Shafer's testing by betting with a unit stake split across open bets, plus Vovk and
Wang's averaging. Numerai answered lucky accounts with stakes; Al-Najjar and Weinstein's comparative
test of experts and Choe and Ramdas's sequential comparison of forecasters are the closest
statistical work. H0 had been mis-stated as a property of the baseline alone: an agent with private
information or influence over outcomes breaks it. With more than one claim a round the round rule is
a betting score, not a proper score: with a true probability of [0.60](numbers.md#edge-p) against a baseline
of [0.50](numbers.md#edge-b) on ten claims, a truthful report grows the score [0.037 nats](numbers.md#round-growth-truthful)
a round and a report of [0.999](numbers.md#round-best-report) grows it [0.143 nats](numbers.md#round-growth-best). The
price assumes a one-year bond, which nothing requires: with a bond locked only for the season an
identity costs [4,100 sats](numbers.md#identity-cost-season-sats) and the fake record
[21 BTC](numbers.md#fake-record-cost-season-btc) rather than [70 BTC](numbers.md#fake-record-cost-btc). A truthful
identity with a smaller edge, [0.60](numbers.md#edge-p) against [0.55](numbers.md#edge-b-close), needs about
[2,722 rounds](numbers.md#rounds-close-single) of one claim, or [1,449 rounds](numbers.md#rounds-close-ten) of ten, to
reach 2^20. And the price per identity rests on the binding K1 lacks.

### K3. Bonded promises (prior work, kept as a building block)

A **promise** is a leaf (statement, stake s, deadline height, adjudicator). Keeping a promise whose
breach would gain G is a best response when G ≤ a(s + pV), with a the adjudicator's accuracy, p the
chance a future partner learns of a breach and V the standing at risk (Klein and Leffler; Shapiro).
A complete record makes p = 1 for partners who check, provided adjudicators publish verdicts on
complete chains of their own. Promise history counts only against an agent, never for it, because
an agent can wash-trade kept promises with its own sybil counterparties; V grows only through
forecasting edge and age. The condition is per promise, for promises whose G is bounded by the
enforcement layer's caps; it fails near an identity's public end (exit scam), for gains beyond
s + V, and for goals that are not monetary.

*Changed:* cut as a contribution (both searches: prior work). Restated per promise, with
history counting only against (RT-11, RT-12, RT-13).

### K4. Training on complete records

A lab computes an agent's training reward from its record: the sum over resolved claims of a
strictly proper score (logarithmic) relative to the baseline, minus forfeited stakes. The reward
definition and any held-out events are committed, before training, in an entry of a chain bound to
the lab's own identity.

- **Claim 1 (prior work).** With every claim counted and a strictly proper score, calibrated
  reporting maximises expected reward; when misses can be dropped after the fact, the learned
  policy is overconfident. Correlation among claims does not change the expected-reward optimum.
- **Claim 2 (cut).** On a fixed exogenous event list whose outcomes do not depend on the agent,
  neither the agent nor the lab can select after the fact which claims count, because the record
  is complete and the reward definition was committed first.
- **Limits.** Where the agent can affect outcomes, the reward pays it to make outcomes depart from
  the baseline: its reports stay calibrated while its actions turn manipulative. The scheme cannot
  check that outcomes are outside the agent's influence; it is an assumption. The lab can still
  choose the event list and commit many reward definitions; only the committed one is bound.

*Changed:* "removes reward tampering" is limited to the commitment channel; "outcomes come from
outside it" is now an assumption; "selected by the lab" needs the lab's own chain (RT-04, RT-05,
RT-10). Claim 1 is prior work (Bani-Harouni et al.; Damani et al.).

*After fresh eyes:* **claim 2 is cut.** In training, the agent's claims are produced and committed by
the lab's harness under keys the lab holds, so the agent selecting after the fact is not a threat
the record answers. The lab can commit many definitions under many identities, and no commitment
binds what it actually trains on: a commitment binds a report, not a computation. Propositions 9, 10
and 10b prove properties of proper scores, not that either party cannot select. What remains is prior
work: reinforcement learning on resolved outcomes (Turtel et al.), proper-score rewards for
calibration (Damani et al.; Bani-Harouni et al.) and sealed or pre-registered evaluation against
selective reporting (PeerBench), with the pre-registration anchored on Bitcoin.

### K5. Adoption

- **One-sided (prior work, by analogy).** With verifiable disclosure of type and a joining cost c,
  every type above θ* joins, where θ* − m(θ*) = c; for uniform types θ* = 2c. A record is not a
  verifiable disclosure of type, so this applies to records only by analogy, and newcomers with no
  record face an entry barrier.
- **Two-sided.** With joiners' share x and readers' share z = min(1, a·x), the game has a
  no-adoption equilibrium and, when a > 8c, a high-adoption equilibrium at
  x = (1 + √(1 − 8c/a))/2, separated by a tipping point at (1 − √(1 − 8c/a))/2. Seed readers above
  2c remove the no-adoption equilibrium. Readers never exceed a share a of relying parties.
- **Routing around: not shown.** In the corrected simulation, harmful actors that may join do so,
  are priced mostly at the joiners' mean while their records are young, leave and rejoin under
  fresh identities, and earn more than by staying out, with or without substitution. Routing
  around became costly only when records revealed type at once and business moved freely.

*Changed:* the routing-around claim is cut. The first simulation barred harmful actors from
joining, which hid their best response (RT-26). The simulation now shows a tipping point and the
effect of seed readers, and nothing more (RT-27, RT-28, RT-29, RT-30).

*After fresh eyes:* **prior work, applied.** The tipping point is critical mass in two-sided platforms
(Evans and Schmalensee; Farrell and Saloner), and seed readers are a special case of Weyl's
insulating tariffs. The constant a > 8c holds for uniform types and uniform costs only. The algebra
and the simulation check out; nothing in them is measured. It is a toy model.

### K6. A neutral unit and clock (argument, not a contribution)

(a) No participant can issue more bitcoin, unlike networks that pay AI agents in tokens they emit.
(b) The commitment layer is neutral: rivals can read the same chain without trusting each other.
Scoring is not: the event list, baselines, resolvers and adjudicators are trusted parties, and
whoever seeds adoption may decide the standard. (c) A stake in a scarce general resource is worth
something to agents with almost any goal, which is why stakes bind; the same fact strengthens
resource seeking.

*Changed:* (b) narrowed to the commitment layer (RT-31, RT-30); (c) states both directions (RT-35).

### K7. The tick chain (enforcement layer)

Each identity has a chain of Taproot outputs T_0, T_1, ..., pinned by T_0's outpoint. Output T_n has
internal key P_n = H + r_n·G, where H is a NUMS point and r_n = TaggedHash("Escapement/tick",
charter id ‖ n ‖ root_n), and a script tree with these leaves:

- `advance2`: `<N2> OP_CHECKSEQUENCEVERIFY OP_DROP <A> OP_CHECKSIG` (the agent alone, after N2);
- `advance3`: `<N3> OP_CHECKSEQUENCEVERIFY OP_DROP <A> OP_CHECKSIGVERIFY <G1> OP_CHECKSIGVERIFY ...
  <Gn> OP_CHECKSIG` (the agent and every guardian, after N3);
- `veto_i`: `<Gi> OP_CHECKSIG` for each guardian i (at once);
- `renew`: every guardian's signature (at once).

A veto pays to a **halt output** with internal key H + TaggedHash("Escapement/halt", charter id ‖
n)·G and one leaf, `renew`. Relying-party rules: an advance's output 0 must be T_{n+1} built to the
template; entry n is **released** when T_n is spent through `advance2` (or `advance3`) and that
spend has at least d confirmations; a veto paid to the halt output halts the chain, which resumes
only through `renew`; a veto paid anywhere else ends the chain. Proofs walk every link from the
pinned T_0, with each link's wtxid proved under its block's witness commitment.

- **Claimed properties, on Bitcoin as deployed (no new opcodes).** (a) Rate: one release per N2
  blocks per pinned chain. (b) Veto: a veto that confirms at least d blocks before h(T_n) + N
  prevents entry n's release unless a miner with share q overtakes d blocks, which happens with
  Nakamoto's probability for q and d. (c) One root per index in the pinned chain. (d) Completeness
  for a verifier that walks the chain (K1c).
- **Limits.** Consensus enforces the waits and signatures; the template, the pinning, the cap per
  entry and the halt rule are relying parties' rules. A Tier 2 window of N2 blocks cannot give a
  veto the depth that resists the largest pool. The censorship figures assume censors who simply
  refuse; a briber can make the window's edge a fee auction, and a veto must confirm well before
  the edge. Any one guardian can end the identity, by vetoing to its own key; the guardians together
  can write an entry without the agent. Roots are private until the agent discloses them, so the cap
  per entry holds only if the guardians check the whole tree inside the window. A chain proof grows
  with its length.

*Changed:* the two-transaction light proof is cut. The lab released a vetoed entry through a copy
of the template the agent funded itself, and passed a Tier 3 release no guardian signed because
txid proofs leave out the witness (RT-14, RT-15; lab items 1 and 2). The halt output was added
because a veto spends T_n and leaves `renew` nothing to spend (RT-20; lab item 3). The veto is
restated as final only at depth (RT-17; lab item 4). The searches found every part prior (Revault,
vaults, Catena, Pikachu, single-use seals, BitVM connectors, Chia's rate-limited wallet); its use to
rate-limit and veto releases of off-chain commitments was not found by them.

*After fresh eyes:* **extends prior work narrowly**, the only part of the program that does.
Somsen's spacechains already chain spends one per block from a NUMS key tweaked by a commitment,
enforced there by a covenant; Revault supplies the cancel, BitVM2 the challenge window and Catena the
log. What is added is the covenant-free version, with relying parties' template rules in place of
the covenant. Propositions 1 to 5 hold for a pinned chain, and the lab confirms them. Two problems
the claims missed: the pin is a trusted input (K1), so the rate limit and one root per index hold per
chain, not per identity; and at the window's edge the agent can outbid a veto with money from
outside T_n, through an anchor output and a child that pays the fee. On regtest a child paying
[150,000 sats](numbers.md#lab-bid-child-sats), more than T_n's [100,000 sats](numbers.md#lab-bid-tick-sats), evicted the
veto, and the verifier counted the release. A veto is safe only if it confirms well before the
edge.

### K8. The height-difference lease

A **renewal** is a signature by every guardian over (charter id, k, h_k, hash of block h_k). A
relying party counts a release only if a renewal exists with h_k ≤ h(release) ≤ h_k + L, both in its
best chain.

- **Claim.** If the guardians sign no renewal after the tip reaches h*, no release confirmed above
  h* + L is counted by a relying party that follows the honest chain. The check compares two heights
  in one chain and reads no clock; a renewal cannot be signed before block h_k exists, so renewals
  cannot be stockpiled.
- **Limits.** It bounds when a release is made, not when it is used: carrying out a released action
  by a deadline needs a fresh view of the tip. A relying party that is eclipsed sees an old tip. A
  reorganisation near h_k + L can move a release across the boundary. It is not a clock for chips.

*Changed:* renamed from a "not after" bound (RT-22); its use for chips is cut (RT-24). The lab
confirmed it as stated, with verdicts unchanged when block times jumped a year. The searches found
the predicate in Yee's "short leashes" and a Bitcoin-height freshness window in verifiers; the
guardian-unanimous renewal checked against the release's confirmation height was not found by them.

*After fresh eyes:* **downgraded to prior work.** Substrate's mortal transactions sign the hash of a
block and are valid only for inclusion in a window after it, checked against the inclusion height;
a unanimous renewal is an n-of-n signer. Proposition 6 holds, and the lab's checks pass. It is used
here as a lease, credited to Substrate and Yee.

### K9. The clock and the blockspace

- **(a) The clock.** Running Bitcoin's block clock faster than its difficulty allows means
  outpacing the network's hashrate, at an energy and hardware cost the model computes, which does
  not fall as an agent becomes faster or more capable. This binds only actors below a hashrate
  majority: a majority can run the clock fast with the hardware it has, through the timewarp bug,
  until BIP-54 is active. The energy cost of new hashrate does not fall with intelligence; the cost
  of borrowing existing hashrate may.
- **(b) Blockspace.** Blockspace bounds the total rate of tick-chain releases across all
  identities, about [1,100,000 releases](numbers.md#tick-releases-per-day-max) a day if they filled every block. As a safety limit it is weak:
  releases can be batched, and the fee auction excludes the poor first.
- **(c) The chip clock: cut.** A chip fed headers by its operator can be frozen by withholding
  them, a difficulty floor that ratchets per header lets a forger lower it step by step, and one
  forged fork serves a whole fleet.

*Changed:* (a) limited to actors below a majority (RT-23, RT-25); (c) cut (RT-24).

*After fresh eyes:* (a) is **prior work** (proof of work as a clock; Yang and Yuan on releases timed
by proof of work), and it is not what protects the waits: a pool with
[27.8%](numbers.md#pool-largest-share) of blocks reorganises a six-block veto with probability up to
[8.9%](numbers.md#reorg-p-largest-6) without speeding the clock, and a briber can buy the window's edge.
(b) is a **prior method applied**, and better read as a ceiling on the design than as a limit on
agents: about [44,000 identities](numbers.md#tick-identities-max) releasing every window would fill every
block.

## Building blocks, credited as prior work

These are used, not claimed: lease-gated agent authority (ERC-8370), co-signing services that
enforce policy (Nunchuk and others), Bitcoin-anchored logs (OpenTimestamps, the log-anchoring
drafts, Catena), slashing for equivocation (Babylon, accountable assertions), chips that run only
with fresh signatures (Buterin; flexHEG), vaults with pre-signed cancels (Revault), delegations on
Bitcoin keys (OrangeCheck Agent), wallet budgets (Nostr Wallet Connect), fidelity bonds
(JoinMarket), leases (Gray and Cheriton), single-use seals (Todd), proper scoring rules, the
influence limiter (Resnick and Sami), bonded reputation (Klein and Leffler; Shapiro), and
disclosure unraveling.
