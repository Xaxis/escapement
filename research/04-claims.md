# The claims under test

This file states each candidate contribution precisely enough to be searched for, proved, built,
attacked and reviewed. It says nothing about why a claim might be new, so that the people and
helpers who check novelty start from the claim, not from the author's case for it. Every claim
here is provisional until it has passed each level in `research/06-verification.md`; anything that
fails a level is cut or downgraded there, not argued around here.

Notation: a **principal** is the human or organisation answerable for an AI agent; a **relying
party** is anyone who acts on the agent's word or request (an API, a merchant, a counterparty, a
lab's evaluator, an insurer); **guardians** are independent key holders who can stop the agent; N,
L, S are block counts.

## The core proposition

An AI agent's standing in the economy (what it may do, at what price, with what trust) should be
computed from an **unforgeable track record**: a complete, ordered, non-backdatable record of
every commitment it asked anyone to rely on, kept under one identity that costs locked bitcoin.
Two consequences are claimed. First, honest and calibrated behaviour becomes the cheapest way to
acquire standing, for agents whose goals are unknown, and labs can train on rewards computed from
such records that neither the agent nor the lab can fabricate or select. Second, once some agents
can show such records, relying parties discount agents that cannot, and the terms for staying out
worsen until joining is cheaper: adoption is chosen, not imposed.

## Contributions to be tested

### K1. The complete record under costly identity

- **Identity.** One identity is one **bond**: a Taproot output holding at least B sats, spendable
  by the principal only after an absolute timelock (CLTV), with an internal key that provably has
  no known secret (NUMS point plus a revealed tweak) and a script leaf that commits to one charter
  id, so one output can back one identity. The bond must be at least S blocks old before the
  identity's record counts (seasoning).
- **Record.** Each identity has one **tick chain** (K7). Entry n of the record is the Merkle-sum
  root committed in tick output T_n; its leaves are the identity's commitments made in that entry:
  claims with a stated resolution source, promises with a stake and deadline, and requests for
  Tier 2 and Tier 3 actions. The sum tree commits the count of leaves and their total stake.
- **Rule.** A relying party or scorer gives an identity credit for a commitment only if it is a
  leaf of some entry of that identity's chain, created before the commitment's resolution height.
  Entries whose leaves are not disclosed (to the public or to an agreed scorer) are scored as if
  every undisclosed leaf had the worst outcome.
- **Claimed properties.** (a) Non-backdatable: an entry's creation height is fixed by
  confirmation. (b) Non-forkable: exactly one entry per index exists in the best chain. (c)
  Non-omittable: the sequence of entry indices is gapless and visible to anyone, and each entry
  commits the count of its leaves, so hiding a commitment is detectable. (d) Costly to multiply:
  each additional identity needs its own bond and season.

### K2. The fake-record cost bound

Claims are scored against a public **baseline** forecaster b (for example a market price or a
reference model). For an identity whose claims q_1..q_T resolve to outcomes y_1..y_T, the record's
score is the likelihood ratio Λ_T = Π q_t(y_t) / b_t(y_t), which is a nonnegative martingale with
mean 1 when outcomes follow the baseline.

- **Claim.** If records are complete (K1c) and created before resolution (K1a), then for an
  adversary with no edge over the baseline, the probability that any one identity's record ever
  reaches Λ ≥ λ is at most 1/λ (Ville's inequality), so obtaining at least one such record with
  probability π needs at least πλ identities, at a cost of at least πλ·c_id, where c_id is the
  cost of one identity (bond opportunity cost over its term plus fees). For yes/no claims against
  a baseline of 1/2, a record of m correct claims has λ = 2^m, so faking it costs exponentially
  more as the record grows. An agent with a real per-claim edge D (expected log likelihood ratio)
  reaches the same λ with one identity after about ln(λ)/D claims.
- **Consequence claimed.** The record is a costly signal that satisfies single crossing (it is
  cheap for skilled or honest types and expensive for others), whereas a bond alone costs every
  type the same and cannot separate them.
- **Stated failure.** Without completeness, one identity can fake any Λ by hiding its losses; with
  a wrong baseline, informed but unskilled identities look skilled.

### K3. Honesty as the cheapest strategy for bonded promises

A **promise** is a leaf (statement, stake s, deadline height, adjudicator). If it is broken, the
stake goes to the beneficiary and the breach is in the record that every future relying party
sees.

- **Claim.** With complete records, a breach costs the agent s plus the full value V of the
  standing it loses with every future partner, with certainty rather than with the probability
  that a given partner hears of it, so keeping a promise of value G to break is incentive
  compatible whenever s + V ≥ G. The required stake falls as standing grows.
- **Stated failure.** End-game and exit scams (V small near the end of an identity's life), gains
  larger than s + V (the judgment-proof case), and a captured or mistaken adjudicator.

### K4. Training on complete records

A lab that trains or fine-tunes an agent with reinforcement learning computes the agent's reward
from its complete record: a strictly proper score (logarithmic or Brier) over every resolved claim,
minus forfeited stakes, with the reward definition and any held-out evaluation set committed
before training.

- **Claim.** With complete records and a strictly proper score, truthful calibrated reporting is
  the reward-maximising policy. With selective records (the agent chooses which claims count), the
  reward-maximising policy is overconfident and selective. A learning agent trained under each
  regime learns the corresponding policy.
- **Claim.** The record channel cannot be written by the agent (entries are consensus objects and
  outcomes come from outside it) or selected by the lab (the reward definition is committed first),
  which removes reward tampering of this channel and selective reporting by either party. It does
  not remove a badly chosen objective.

### K5. Adoption by unraveling

- **Claim (one-sided).** Let an agent's type θ be the expected value it delivers to relying
  parties per period, distributed with density f, and let joining cost c per period. Relying
  parties price a verified agent at θ and an unverified one at m(t) = E[θ | θ < t], the mean of
  those who stay out. In equilibrium every type above θ* joins, where θ* − m(θ*) = c. When c is
  small relative to the spread of types, almost every type joins (unraveling, as in Milgrom 1981
  and Grossman 1981 for verifiable disclosure, and Jovanovic 1982 with a disclosure cost). For θ
  uniform on [0, 1], θ* = 2c.
- **Claim (two-sided).** Relying parties choose whether to require records; agents choose whether
  to join. Requiring records is a strategic complement of joining. The game has a no-adoption
  equilibrium and a high-adoption equilibrium, separated by a tipping point, and parties who gain
  from joining or requiring regardless of others (insurers pricing agent risk, relying parties
  with high fraud losses, agents with good records) can move the system past it.
- **Claim (routing around).** An actor that refuses to join can still deal with relying parties
  that do not check, but under unraveling those parties face the worst pool of agents and price
  accordingly, so routing around remains possible but becomes more expensive as adoption grows.
  The mechanism does not stop such an actor; it bounds the checked economy's exposure to it.

### K6. A neutral unit and clock

Stakes, standing and training rewards are denominated in bitcoin and timed by Bitcoin's block
height.

- **Claims (argument, not theorem).** (a) No participant, including any lab, state or AI, can
  issue more of the unit, unlike networks that reward AI agents by emitting the network's own
  token to the agents being rewarded. (b) Parties who distrust each other (rival labs, rival
  states) can rely on the same records without trusting a registry run by one of them. (c) A stake
  in a scarce, general-purpose resource has positive value to agents with almost any goal
  (instrumental convergence), so stake-based incentives apply to agents whose goals are unknown.
- **Stated tension.** Rewarding agents in a general-purpose resource can strengthen resource
  seeking; stakes are meant to be at risk, not to be accumulated as an objective.

### K7. The tick chain (enforcement layer)

Each identity has a chain of Taproot outputs T_0, T_1, ... Output T_n has internal key
P_n = H + r_n·G, where H is a NUMS point and r_n = TaggedHash("Escapement/tick", charter id ‖ n ‖
root_n), and a script tree with these leaves:

- `advance2`: `<N2> OP_CHECKSEQUENCEVERIFY OP_DROP <A> OP_CHECKSIG` (the agent alone, after N2
  blocks);
- `advance3`: `<N3> OP_CHECKSEQUENCEVERIFY OP_DROP <A> OP_CHECKSIGVERIFY <G1> OP_CHECKSIGVERIFY ...
  <Gn> OP_CHECKSIG` (the agent and every guardian, after N3 blocks);
- `veto_i`: `<Gi> OP_CHECKSIG` for each guardian i (immediate);
- `renew`: every guardian's signature (immediate), used to restart a halted chain.

Relying-party rules: entry n is **released** at tier 2 (or 3) when T_n is spent through `advance2`
(or `advance3`) by a transaction with at least d confirmations, whose output is T_{n+1} built to
the template. A spend through `veto_i` halts the chain at n, and entry n is never released; a
halted chain resumes only through `renew`.

- **Claimed properties, on Bitcoin as deployed today (no new opcodes).** (a) Rate: at most one
  release per N2 blocks per identity, enforced by consensus. (b) Veto: any single guardian whose
  veto confirms before height h(T_n) + N prevents entry n's release for ever. (c) No
  equivocation: each index has one root. (d) Completeness: K1c. (e) Light verification: a release
  is proved by block headers and Merkle inclusion proofs of two transactions plus the revealed
  leaf, with no query of the UTXO set, so a light client or a chip can check it.
- **Stated limits.** Censorship of veto transactions by miners (or bribed miners) during the
  window; a guardian set that vanishes lets tier 2 releases continue until the lease (K8) lapses;
  the per-entry cap is enforced by relying parties checking the sum tree, not by consensus.

### K8. The height-difference lease

A **renewal** is a signature by every guardian over (charter id, k, h_k, hash of block h_k). A
relying party counts a release only if a renewal exists with h_k ≤ h(release) ≤ h_k + L, both
heights in its best chain.

- **Claim.** This gives an off-chain authority a "not after" bound although Bitcoin script cannot
  express one, and the bound does not depend on the relying party's clock: it compares two heights
  in the same chain. A renewal cannot be signed before block h_k exists, so leases cannot be
  pre-signed in bulk. The only remaining clock dependence is how late a released action may be
  carried out.

### K9. The clock it cannot speed up, quantified

- **Claim.** Bitcoin's block clock is a public clock whose acceleration has a measurable physical
  cost (energy and hardware to outpace the network's hashrate), which the model computes; that
  cost does not fall as an agent's own speed or intelligence grows. Blockspace bounds the
  aggregate rate of tick-chain releases across all identities, and the fee per release prices it.
  Bitcoin headers with a difficulty floor can serve as the licence clock of AI chips, at a
  forgery cost the model computes.

## Building blocks, credited as prior work

These are used, not claimed: lease-gated agent authority (ERC-8370), co-signing services that
enforce policy (Nunchuk and others), Bitcoin-anchored logs (OpenTimestamps, the log-anchoring
drafts, Catena), slashing for equivocation (Babylon, accountable assertions), chips that run only
with fresh signatures (Buterin; flexHEG), vaults with pre-signed cancels (Revault), delegations on
Bitcoin keys (OrangeCheck Agent), wallet budgets (Nostr Wallet Connect), fidelity bonds
(JoinMarket), leases (Gray and Cheriton), single-use seals (Todd), proper scoring rules, and
disclosure unraveling.
