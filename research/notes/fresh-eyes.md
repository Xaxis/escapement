# Fresh-eyes review of the eight claims

Reviewer: a last, independent reviewer that had seen none of the work. Date: 2026-11-26.

**What I read.** `research/04-claims.md`, `research/05-formal.md`, `paper/00` to `paper/13`,
`model/sim.py`, `model/escapement.py`, `research/numbers.md` (by id), `lab/README.md` and
`lab/*.py`. I did not read `research/03-novelty.md`, `research/06-verification.md` or anything
else in `research/notes/`.

**What I ran.**

- `python3 model/escapement.py --only ID` for 31 ledger ids (identity cost, fake-record figures,
  correlated-claims and round-rule results, skilled-identity rounds, adoption, clock, reorg, chain
  proof, training). Every value matched the paper.
- The whole lab, as `heavy python3 lab/run.py --only 1 ... --only 8`. This runs the same eight
  scenarios as `make lab` but does not rewrite `lab/results.json`, since I was asked to edit no
  other file. Result: **104 of 104 checks pass**, final height 4,871, the same sizes as the README.
  The node was stopped and its datadir deleted.
- Two checks of my own on a fresh regtest node, built only from the lab's own modules
  (`TickChain`, `Lab`, `verify.verify_release`). They are described under C1 and C5.
- Exact calculations of the round rule (below, C2), using `sim.record_skilled_rounds` and a
  binomial calculation of expected log growth.

**Searches.** I ran my own searches for C2 and C6, and two helper searches for C1, C3, C4 and
C5, C7, C8. I re-fetched every quote marked "verified" below. Quotes split with "..." were cut by
the fetch tool's length limit.

## Summary

| Claim | Novelty | Works | One-line reason |
|---|---|---|---|
| C1 one record as standing, reward and gate, complete against many identities | Extends prior work, as an assembly only | **Does not work as stated** | Nothing on chain binds a chain to its bond. On regtest, one charter id carried two chains, each accepted from its own pin, with different roots at entry 1. Standing and training reward ask for different reports from the same leaves. |
| C2 fake-record bound K/λ, priced πλ·c_id | **Prior work** in substance (Shafer's testing by betting, Vovk and Wang, Ville, union bound; Numerai's stake against lucky accounts) | Works only under hypotheses stronger than stated | The theorem needs the agent's forecasts to use only public information and its actions not to move outcomes. "A property of the baseline, not of the agent" is wrong. With more than one claim a round, the round rule is not proper. |
| C3 training reward neither agent nor lab can select | Application of prior work (sealed or pre-registered evaluation; RL on resolved outcomes; proper-score RL) | **Does not work for the lab** | The lab controls the agent's keys in training, can commit many definitions under many identities, and nothing binds what it actually trains on. The agent side is the textbook proper-score result. |
| C4 two-sided adoption, tipping point, seed readers | **Prior work** (critical mass in two-sided platforms) | Works as a toy model | The algebra checks and the simulation tips between a 5% and a 9% start. The a > 8c constant comes from uniform types and costs. Nothing is measured. |
| C5 tick chain, rate limit and guardian veto | Extends prior work narrowly (Somsen's spacechain key and CSV chain, Revault's cancel, BitVM2's challenge window, Catena) | Works with the stated limits, plus two the authors miss | The pin is a trusted input. On regtest the agent outbid a watchtower's veto with a CPFP child paying 150,000 sats, more than T_n holds, and the verifier counted the release. |
| C6 height-difference lease | **Prior work** (Substrate's mortal transactions; Solana's recent blockhash; Yee) | Works as stated | Proposition 6 holds under B2 and B3, and the lab's 7 lease checks pass. The predicate "signed block hash, valid until the inclusion height passes h_k + L" is Substrate's. |
| C7 cost of running the clock fast, below a majority | **Prior work** (proof of work as a clock; Budish; Yang and Yuan) | Arithmetic correct, not load-bearing | A pool with 27.8% of hashrate beats a Tier 2 veto up to 8.9% of the time without speeding the clock. Reorgs and bribery, not clock speed, are the binding attack. |
| C8 blockspace as an aggregate limit | Prior method (Lightning-era capacity arithmetic), applied | Correct arithmetic, weak as safety | Its real meaning is a scaling ceiling: about 44,000 identities releasing every window would fill every block. |

## C1. One complete record as standing, training reward and release gate

### Novelty

Every part has close precedent, and the authors credit most of it. What I could not find is one
record used for all three roles.

- **Foresight Arena**, Nechepurenko and Shuvalov, arXiv:2605.00420 (1 May 2026), an on-chain
  benchmark for AI forecasting agents. It uses "a commit-reveal protocol enforced by Solidity smart
  contracts" and "proper scoring rules that incentivize honest probability reporting and isolate
  predictive edge over market consensus" (verified). It has no costly identity, no training use and
  no gate.
- **Infinite Games**, a Bittensor forecasting subnet, https://github.com/Metaculus/infinite_games:
  "in case of no prediction being submitted a miner gets the worst possible score under the peer
  scoring rule" (verified). This is the worst-case scoring of silence. `04-claims.md:66-67` says
  that scoring "was not found", so that sentence is wrong.
- **Numerai**, Craib, 25 June 2021, https://foresight.org/?p=6249 (verified):
  - "Thousands of accounts were created and they swamped the signal market with random signals
    hoping they'd get lucky."
  - "In response, a cryptocurrency and staking system was introduced"
  - "users staked their NMR tokens against their models and could have their stake slashed if the
    model does not do well."

  That is the many-identities problem of C2, answered with a costly stake, and scoring against a
  meta-model is a baseline.
- **Chaffer**, AgentBound Tokens, arXiv:2501.16606, and **Tomasev, Franklin and Osindero**,
  arXiv:2602.11865. They cover a stake-backed immutable ledger and gating of authority (from the
  helper search; not re-fetched).

**Verdict: extends prior work, as an assembly.** None of the paper's results depends on the three
roles sharing one record. Each role works, or fails, the same way with three separate records.

### Works

Three problems, the first shown on regtest.

1. **The pin is not bound to anything on chain.**
   - The paper says the chain is "pinned by the outpoint of T_0 that the charter names"
     (`paper/03-record.md:13-14`, `paper/08-enforcement.md:12-13`). But T_0's internal key commits
     the charter id (r_0 = TaggedHash(id ‖ 0 ‖ root_0)). If the charter id is a hash of a charter
     that names T_0's outpoint, the definition is circular: T_0's txid depends on the charter id,
     and the charter id depends on T_0's txid.
   - In the lab the charter id is a hash of a label, and the pin is a parameter handed to the
     verifier (`lab/verify.py:245-266`; `TickChain.t0` in `lab/scenarios.py:119-121`: "which a
     relying party pins (here the funding output)"). The README says the binding (T_0 "created in
     the same transaction as the bond") was not built (`lab/README.md:186-188`).
   - **I built it.** I opened two tick chains under one charter id, with different roots for
     entry 1, and released entry 0 of each. `verify_release` accepted both, each from its own
     pin:
     - chain A: "entry 0 released at tier 2 at height 151, 7 confirmations; root_1 = b46712fb..."
     - chain B: the same verdict, with root_1 = f9e373ef...
   - So "An identity cannot show two parties two different entries" (`paper/03-record.md:55-56`)
     holds only for parties that agree on a pin from outside the chain.
   - One bond can back as many chains as its owner likes. That defeats K1(d) "costly to multiply",
     the per-identity rate limit of C5, and C2's per-identity price.
   - **A fix is cheap:** identity = bond outpoint, and T_0 = a named output of the bond's own
     transaction. But it must be specified and built. It also collides with renewing a one-year
     bond (`bond-term-years`) without losing the record, which the claims do not address.
2. **"Complete against an operator's many identities"** (`paper/01-introduction.md:45`,
   `paper/11-related.md:18`).
   - The record is complete per identity. An operator with K identities can hide whole identities
     and show the best one.
   - The bound prices that (K/λ), and `paper/10-benefit-abuse.md:51-53` says so ("run many young
     identities and present the luckiest"). Completeness does not prevent it.
3. **Standing and training reward pull the same leaves apart.**
   - Standing uses the round rule. Training uses the per-claim log score
     (`research/05-formal.md:313-315`).
   - With more than one claim a round, the round rule rewards extreme reports, not beliefs (C2,
     item 3). An agent that values its standing therefore reports q near 0 or 1. The training
     reward, computed on the same q, is then dominated by log scores of misses near ln(0.001).
   - One record cannot be both a calibrated forecast record and a growth-optimal betting record
     unless each leaf carries a forecast and a separate bet.

### Overclaims

See the list at the end: `paper/01-introduction.md:44-46`, `paper/03-record.md:49-50` and
`:55-56`, `paper/11-related.md:18-19`, `paper/13-conclusion.md:6-7`, `research/04-claims.md:66-67`.

## C2. The fake-record bound

### Novelty

The mathematics is prior, and the authors say so. The new part is a one-line corollary.

- **Shafer, "On Testing by Imaginary Betting"** (ERCIM News; glennshafer.com article117), verified
  from the PDF:
  - "If you make successive bets against a forecaster, beginning with a unit stake and never
    risking additional capital, and you obtain a large cumulative betting score, then you
    discredit the forecaster."
  - "you must bet before you see the outcomes."

  The round rule is exactly "never risking additional capital" when several bets are open at once.
  A weighted mean of q_i/b_i is the return on a unit stake split w_i across fair bets at the
  baseline's odds.
- **Vovk and Wang**, arXiv:1912.06116 (Ann. Statist. 2021): "e-values can be merged simply by
  averaging them" (verified).
- **Choe and Ramdas**, "Comparing Sequential Forecasters", arXiv:2110.00115 (Operations Research
  2024). Anytime-valid e-processes for comparing forecasters under any scoring rule.
- **Al-Najjar and Weinstein**, "Comparative Testing of Experts", Econometrica 76(3) 2008: "a simple
  "reputation-style" test can always identify which of two experts is informed" (verified). This is
  a likelihood-ratio comparison of an expert against another forecaster, which is C2 with the
  baseline as the second expert.
- **Resnick and Sami**, the influence limiter (RecSys 2007): "If an attacker can create only a
  bounded number of shills, the attacker can mislead only a small amount" (verified). The 2008
  sequel defines (n, c)-robustness against n sybils.
- **Numerai** (C1 above): staking against "thousands of accounts" that hoped to "get lucky".

**Verdict: prior work.** K ≥ πλ is a union bound on Ville's inequality, and πλ·c_id multiplies it
by a price. `04-claims.md:101-102` says "the closed form under costly identities and the round
rule were not found". The round rule is Shafer's principle with Vovk and Wang's averaging, and the
closed form is a union bound.

### Works

**The proof is correct given F_{k-1}-measurable forecasts and weights.** The steps are
E[M_k | F_{k-1}] = Σ w_i = 1, then a nonnegative martingale, then Ville, then a union bound. The
tightness example (2^m opposite predictions) is right. Four problems remain.

1. **The hypothesis is mis-stated.**
   - `research/05-formal.md:183` says "for any strategy", and the proof uses "The forecasts and
     weights of round k are fixed before it opens, so given F_{k-1}, E[M_k] = Σ_i w_i·E[...]"
     (`:188-189`). That pulls q_i and w_i out of a conditional expectation on public information.
     This is valid only if they are functions of public information (plus independent noise).
   - An agent with private information, or one that can act on the outcome, fails it. Its "edge"
     may be insider knowledge or manipulation. Under H0 as written, an agent that can cause y to
     equal its forecast gets factor 1/b every round.
   - So H0 is not "a property of the baseline, not of the agent" (`04-claims.md:77`,
     `paper/04-honesty.md:19-20`). The theorem needs, about the agent: its forecasts use only
     public information, and its actions do not move outcomes.
   - The paper states the second condition for training (section 5) but omits it from "What
     breaks the bound" (`paper/04-honesty.md:78-94`). It applies equally here: standing rewards
     manipulation exactly as Proposition 10b says training does.
   - Minor: `05-formal.md:175` defines F_{k-1} at round k-1's settlement, and `:179` calls it
     "when round k opens". By the tower property this is harmless if forecasts are measurable at
     opening.
2. **The price assumes a term nothing requires.**
   - c_id = 13,000 sats is a one-year bond (`bond-term-years`, a design value). The rules require
     only a season of S = 4,032 blocks, and the verifier stops counting a bond at its locktime.
   - A faker can set the locktime just after it presents the record. The lab's bond locks 10 blocks
     past its season. The cost per identity then falls toward the opportunity cost of about 28 days
     plus the faking time, plus fees.
   - The 70 BTC figure is therefore an upper estimate of the lower bound, unless relying parties
     require a minimum remaining term. And all of it rests on problem C1.1 (one bond, one chain)
     being fixed.
3. **The round rule is not a proper scoring rule once a round holds more than one claim.**
   - I computed the expected log growth per round exactly, for n independent yes or no claims with
     true probability p, baseline b, equal weights and the same report q on each:

     | p, b | claims a round | truthful q = p | growth-optimal q | growth at that q |
     |---|---|---|---|---|
     | 0.6, 0.5 | 1 | 0.0201 nats | 0.6 (proper) | 0.0201 |
     | 0.6, 0.5 | 10 | 0.0374 | 0.999 | 0.1431 |
     | 0.6, 0.53 | 10 | 0.0186 | 0.999 | 0.0850 |
     | 0.55, 0.5 | 100 | 0.0099 | 0.999 | 0.0910 |

   - So Proposition 7's sentence "a mean of ratios grows at most like ln(1 + χ²(p ‖ b)) per round"
     (`05-formal.md:218-219`) is true only for truthful reports. An identity that maximises its
     standing bets, it does not forecast.
   - This matters for C1 (above) and for anyone who reads the record's q as probabilities.
   - A fix: let each leaf carry a forecast (scored by a proper rule, for training) and a separate
     stake fraction (scored by the round rule, for standing). Or allow only one claim per round
     for standing, which makes it proper.
4. **Time to standing.**
   - For truthful reporting, `sim.record_skilled_rounds` gives 118, 74, 72 and 72 median rounds
     for 1, 10, 100 and 1,000 claims a round. It saturates near 72, as predicted.
   - That uses the paper's edge of 0.12 nats a claim: an agent that knows every event's probability
     when the public says 1/2. For realistic edges, truthful reporting to 2^20 needs:
     - p = 0.6 against b = 0.55: about 2,700 one-claim rounds, or about 1,400 rounds of 10 or 100
       claims;
     - p = 0.6 against b = 0.53: about 1,400 or 720.
   - Rounds are serial per identity. Each lasts at least until its slowest claim resolves, plus d
     blocks, and at most one entry fits per N2 blocks.
   - With daily events that is years, with weekly events decades. Extreme betting cuts it to about
     115 to 290 rounds, at the price of problem 3.
   - `paper/04-honesty.md:101-103` ("produces its record as a by-product of forecasting, at the
     cost of one identity") omits the time.
   - And λ must exceed the number of edgeless identities in use (`paper/04-honesty.md:92-93`).
     With a million identities, a meaningful score is out of reach for most real forecasters on
     useful horizons.

The simulations reproduce: 22.9% against 25.0%; product rule 99.8% against 1.6%; round rule 1.1%;
tail-risk record 23,000 against 1.01. They test strategies that use only public information, so
they cannot show problem 1.

## C3. A training reward neither the agent nor the lab can select after the fact

### Novelty

- **RL on resolved real-world outcomes:**
  - Turtel et al., arXiv:2505.17989;
  - FutureWorld, arXiv:2604.26733: "stores prediction-time rollouts, backfills rewards after
    real-world outcomes become available" (helper search);
  - Future-as-Label, arXiv:2601.06336.
- **Proper-score RL for calibration:** Damani et al., arXiv:2507.16806; Bani-Harouni et al.,
  arXiv:2503.02623. The paper credits both.
- **Sealed and delayed-disclosure evaluation against selective reporting:** PeerBench,
  arXiv:2510.07575. Its abstract names "selective reporting by model developers" and proposes
  "sealed execution, item banking with rolling renewal, and delayed transparency" (verified).
- **Pre-registration timestamped on a public log** is old practice, and the paper says so
  (`paper/05-training.md:71-72`).

No source found commits an RL reward on Bitcoin before training. **Verdict: application of prior
work.** What remains is putting a pre-registration and the claim log on Bitcoin.

### Works

- **Agent side.** Propositions 9, 10 and 10b are correct and textbook, and the learner simulation
  reproduces (a = 1.06 complete, 10.4 and rising under selection). But in training the agent's
  claims are produced and committed by the lab's harness under keys the lab holds. The agent
  "selecting after the fact" is not a threat the record answers. The lab's logging already
  prevents it, and the proper score handles selection before the fact.
- **Lab side.** It does not hold.
  - The text concedes the lab "can commit many reward definitions and use one"
    (`paper/05-training.md:70-71`; `04-claims.md:134-135`). That is selection after the fact.
  - A reader sees all the definitions only if the lab uses one chain. A lab can run as many
    identities as it likes at 13,000 sats each, and the pin problem (C1.1) lets it run several
    chains even under one bond.
  - Nothing binds what the lab actually trains on to what it committed. The commitment binds a
    report, not a computation.
- **Table @tab:verification** (`paper/09-verification.md:40`) lists "Proved (Props 9, 10, 10b)"
  for this claim. Those propositions prove properties of proper scores. None proves that either
  party cannot select.

## C4. Two-sided adoption with seed readers and a tipping point

### Novelty

- **Evans and Schmalensee**, "Failure to launch: critical mass in platform businesses", Review of
  Network Economics 9(4) 2010, doi:10.2202/1446-9022.1256: "the initial critical mass hurdle"
  (helper search).
- **Weyl**, AER 2010, doi:10.1257/aer.100.4.1642: "Platforms use insulating tariffs to avoid
  coordination failure" (helper search). That is the standard way to remove the bad equilibrium,
  of which seed readers are a special case.
- **Farrell and Saloner** 1985, cited by the authors. **Caillaud and Jullien** 2003; **Rochet and
  Tirole** 2003.

**Verdict: prior work, applied.** The a > 8c constant is specific to uniform types and uniform
reading costs.

### Works

**The algebra checks:**
- t = 2c/z;
- a·x² − a·x + 2c = 0;
- slope (1 − x)/x at a fixed point, so x_high is stable and x_low is not;
- with z ≥ z_0 > 2c, x ≥ 1 − 2c/z_0 > 0.

**The analytic numbers reproduce** (8.8% and 91%).

**The agent-based simulation**, which I reran, collapses from a 2% or 5% start and reaches 100%
from 9%, 12% or 20%. That is consistent with a tipping point near 8.8%. Three things to note:
- It reaches the high state within one or two periods, because every agent best-responds at once.
- Its harmful actors alternate between joining and leaving every period (the path reads 0.95,
  1.0, 1.0, 0.95, ...).
- Their payoff falls from 0.45 with no adoption to 0.25 with adoption. "Earn more than by staying
  out" is a comparison within the adopted world.

**Verdict: works as a toy model.**

## C5. The tick chain

### Novelty

The closest is **Somsen's spacechain**, bitcoin-dev, 26 Dec 2019, "Blind Merged Mining with
covenants". Verified quotes:
- "A long string of sighash_anyprevout transactions, each only spendable by the next"
- an internal key T = H + hash(H||bmm_hash)*G with "a NUMS such as hashToCurve(G) = H"
- "A relative locktime of one block, ensuring only one transaction gets mined per block"

That is the tick chain's key construction and its CSV rate limit, enforced there by a covenant.
Other close work:
- **Revault**: an unvault output spendable by managers after `older(X)` or by stakeholders at once,
  and a Cancel that "pays back to a deposit output". That is the veto, and renew.
- **BOLT 3 `to_local`**: a CSV wait for the owner and an immediate path for the other party.
- **BitVM2**: a claimed value released after a timelock unless "anyone" spends a connector. That
  is a veto window on a commitment that others act on.
- **Catena** and **Mainstay**: a chain of spends committing a log root by OP_RETURN or a key tweak,
  for non-equivocation.

**Verdict: extends prior work narrowly.** What is added is the covenant-free version: relying-party
template rules stand in for the spacechain's covenant, combined with a Revault-style cancel and
applied to off-chain commitments. I found no prior design with all four parts.

### Works

**Propositions 1 to 5 hold as written, for a pinned chain.**
- Proposition 1: the CSV wait.
- Proposition 2: single spending.
- Proposition 3: a hash collision is needed for two roots.
- Proposition 4: walking the chain with full blocks.
- Proposition 5: each link's wtxid proved under the coinbase's witness commitment.

**The lab confirms all of them** (25 + 25 checks, rerun). Two problems are not in the claims.

1. **The pin** (C1.1, built on regtest). Without an on-chain binding, the rate limit, "one root
   per index" and completeness hold only per chain, and one identity can have any number of
   chains.
2. **The agent's bid at the window edge is not bounded by T_n's value.**
   - The README says: "The agent can bid only out of T_n's value (extra inputs break the one-input
     link rule, and T_n+1 cannot be spent early to bump it), so a watchtower whose fee reserve
     exceeds the tick output's value can outbid it" (`lab/README.md:204-206`).
   - But the verifier checks one input and output 0 only (`lab/verify.py:274-293`). An advance may
     carry a second output.
   - **On regtest**, at the edge of a window:
     1. A watchtower's veto package (zero-fee v3 veto with a P2A anchor, plus a child paying
        20,000 sats) was accepted: `submitpackage` returned "success".
     2. The agent then submitted a zero-fee v3 advance2 with outputs [T_1, P2A], plus a v3 child
        paying **150,000 sats** from a coin outside the chain. T_0 held 100,000.
     3. `submitpackage` returned "success" and the veto left the mempool ("advance in True | veto
        in False").
     4. After one block and d more, `verify_release` returned "entry 0 released at tier 2 at height
        137, 7 confirmations".
   - The paper itself only says a veto "must confirm well before the edge", which stays true. The
     README's bound is false.
   - The one-input rule buys nothing unless the verifier also forbids any output beyond T_{n+1}.
     But that rule would then also forbid the agent from topping up fees, so a chain's life would
     be bounded by T_0's value divided by the fee per release.

**Smaller points:**
- The claims never fix d. The lab uses d = 6 (`confirmations-standard`), and B2 says 19 blocks are
  needed for a 0.1% risk against the largest pool. Rule 1's backdating margin and the release depth
  both inherit whichever is chosen. At 6 the largest pool rewrites with up to 8.9%.
- The Merkle-sum cap is checkable only by owners of leaves under a misreported node (lab item 9),
  so "the cap per entry" is weak even with honest guardians.

## C6. The height-difference lease

### Novelty

- **Substrate's mortal transactions.**
  - `CheckMortality` "contributes to the signed data, by including the hash of the block at
    [`Era::birth`]" and "affects `longevity` of the transaction according to the [`Era`]
    definition".
  - `sp_runtime::generic::era`: "The period of validity from the block hash found in the signing
    material", and `death` is "the block number of the first block at which the era has ended".

  All verified. That is a signature over a block's hash, valid only for inclusion in the window
  after it, checked against the inclusion height by consensus. It has been in Substrate since
  about 2018.
- **Solana**: every transaction carries a recent blockhash and expires after about 150 blocks
  (search results; the docs page refused fetches).
- **Yee**, "Keep Your Transactions On Short Leashes", arXiv:2206.11974. The paper cites it.
- **Zeke's chaintip freshness certificate**. The paper cites it.

The added element named at `paper/08-enforcement.md:115-117` and `04-claims.md:228-229` is "checked
against the release's own confirmation height rather than the verifier's tip". That is what mortal
transactions do. A unanimous guardian signature is an n-of-n signer.

**Verdict: prior work, applied as a lease.**

### Works

**Proposition 6 holds under B2 and B3.** The proof is short and correct:
- the renewal needs hash(h_k), so h_k ≤ h*;
- the release height is fixed by confirmation.

**The lab's 7 checks pass**, including a guessed future hash, a timestamp jump and disabled clock
functions. The limits stated (eclipse, reorg near the edge, bounds the release and not its use)
are the right ones.

**Verdict: works as stated.**

## C7. The cost of running the clock fast

### Novelty

- **Proof of work as a clock:** Trubetskoy 2018 ("simply a distributed, decentralized clock");
  Gigi 2021.
- **Yang and Yuan**, arXiv:2205.09020: an attacker must "overtake the total hash rate of the whole
  blockchain network" to advance a PoW-timed release.
- **Budish**, NBER w24717: the economics of attacks.
- **BIP-54**: Status Complete, not active on mainnet.

All from the helper search. **Verdict: prior work.**

### Works

**The arithmetic is right.** 1,052 EH/s × 17.5 J/TH = 18.4 GW. Doubling gains 2,016 × 600 / 2 s
= 7 days. 144 blocks in an hour needs 24×. The 18.4 GW is new current-generation hardware, so it
sits below the fleet's measured draw, as it should.

**But it is not the binding constraint.** The design's waits are 6 and 144 blocks. Against them,
a 27.8% pool reorganises a 6-block-deep veto with up to 8.9% (`reorg-p-largest-6`), and a briber
can buy the window's edge. Neither needs the clock to run fast.

"These costs do not fall as an agent becomes faster or more capable" (`paper/07-why-bitcoin.md:47`)
is true of this one attack, which no capable attacker would choose.

**Verdict: works as arithmetic, matters little.**

## C8. Blockspace as an aggregate limit

### Novelty

**The method is old.**
- Poon and Dryja's estimate of chain capacity for channel opens. The paper estimates "it would
  require 133 MB blocks" (via Lopp, not re-fetched).
- Delving Bitcoin's "3M channels a day" arithmetic (helper search).

Its application to releases was not found, and is trivial.

### Works

**The arithmetic is right:** 144,000,000 vB / 137 vB = 1.05 million a day, and 44,000 identities
releasing every 6 blocks.

**The authors already call it weak as a safety limit.** What they do not draw out is that it is a
scaling ceiling for the design itself:
- If every block were filled with releases, only about 44,000 identities could release every
  window, or about a million once a day.
- C2's own faking example (520,000 identities) and any economy of millions of agents run into it.
- Fees fall hardest on small identities. The paper notes this, but it is the opposite of a safety
  property.

## Overclaims

Each quote says more than the evidence supports.

1. `paper/00-abstract.md:12-13`: "a record of forecasts scored in rounds cannot be faked except by
   running a number of identities that grows with the score". It can be faked with probability up
   to K/λ, only for strategies that use public information and do not move outcomes. And as built,
   one bond can carry many chains.
2. `paper/00-abstract.md:13-14`: "it gives a training reward that neither agent nor lab can select
   after the fact". The lab can commit many definitions under many identities, and its actual
   training is not bound (C3).
3. `paper/01-introduction.md:44-46`: "one complete record serving as standing, training reward and
   release gate, complete against an operator's many identities". The record is complete per
   chain, not per operator (C1.2), and per pin, not per bond (C1.1).
4. `paper/03-record.md:49-50`: "each is a consequence of Bitcoin's rules rather than of anyone's
   honesty". Non-forkability and costly multiplication depend on a pin that relying parties must
   agree on off chain.
5. `paper/03-record.md:55-56`: "An identity cannot show two parties two different entries." This
   is refuted on regtest for two parties that hold different pins (C1.1).
6. `paper/04-honesty.md:19-20` and `research/04-claims.md:77`: "a property of the baseline, not of
   the agent". The theorem also needs the agent's forecasts to use only public information and its
   actions not to move outcomes (C2.1).
7. `paper/04-honesty.md:22-23` and `research/05-formal.md:183`: "whatever an identity's strategy" /
   "for any strategy". This is false for strategies with private information or influence over
   outcomes.
8. `paper/04-honesty.md:101-103`: "the identity with edge produces its record as a by-product of
   forecasting, at the cost of one identity". For realistic edges that is 700 to 2,800 serial
   rounds of truthful reports (C2.4).
9. `research/05-formal.md:217-219`: "More claims per round raise the growth per round only up to a
   limit, since a mean of ratios grows at most like ln(1 + χ²(p ‖ b))". This holds only for
   truthful reports. The round rule rewards reports near 0 or 1 (C2.3), and section 4 of the paper
   presents round-rule scores as scores of forecasts.
10. `paper/05-training.md:68-70`: "The lab cannot choose after the fact which results to report or
    which reward it meant to use, because both were committed first on its own chain". The next
    sentence (`:70-71`) concedes that it can commit many and use one.
11. `paper/05-training.md:73-74`: "what the record adds is completeness of what the agent itself
    claimed, which no pre-registration of the lab's protocol can supply". In training, the agent's
    claims are committed by the lab's harness under keys the lab holds, so this is the lab's
    pre-registration.
12. `paper/09-verification.md:40`: "Proved (Props 9, 10, 10b)" for "Training reward neither party
    can select". No proposition addresses selection by the lab.
13. `paper/06-adoption.md:5-7`: "The answers are yes for the first two". Whether "the record pays
    for itself at each step" is shown only in a model whose parameters "nobody has measured"
    (`:56`). The heading at `:24`, "Staying out comes to cost more than joining", reads as the
    claim that section cuts.
14. `paper/06-adoption.md:102-104`: "The record can pay for itself, the parties who gain alone can
    tip adoption past the point where joining pays". This is a property of the uniform toy model.
15. `paper/08-enforcement.md:4-5`: "Two of its parts extend prior work: the tick chain and the
    height-difference lease." The lease is prior work (C6).
16. `paper/08-enforcement.md:115-117` and `research/04-claims.md:228-229`: "what is added is the
    guardians' unanimous renewal, checked against the release's own confirmation height rather
    than the verifier's tip". Substrate's mortal transactions check against the inclusion height.
17. `research/04-claims.md:66-67`: "the assembly and the worst-case scoring of silence were not
    found". Infinite Games scores a missing prediction as "the worst possible score".
18. `research/04-claims.md:101-102`: "the closed form under costly identities and the round rule
    were not found". This is Shafer's "never risking additional capital", plus Vovk and Wang,
    plus a union bound. Numerai priced lucky accounts with stakes.
19. `paper/13-conclusion.md:6-7`: "such a record has properties no registry run by one party offers
    to rivals: it cannot be backdated, forked or quietly trimmed". It can be forked per pin (C1.1),
    and a light verifier cannot see a trimmed tip (lab item 5). A transparency-log registry with
    witnesses offers non-equivocation to rivals too.
20. `lab/README.md:204-206`: "The agent can bid only out of T_n's value ... so a watchtower whose
    fee reserve exceeds the tick output's value can outbid it". Refuted on regtest with an anchor
    output and CPFP (C5.2).
21. `paper/07-why-bitcoin.md:47-49`: "These costs do not fall as an agent becomes faster or more
    capable ... That is the precise sense of the claim that Bitcoin is a clock an AI cannot speed
    up". This is true, but the waits it protects fall to cheaper attacks (C7), so the sentence
    implies a protection the design does not get from it.

## Reproducing my two regtest checks

Both use only the lab's modules, on a throwaway node (`node.Node`), with `sys.path` set to `lab/`:

- **Pin.** Make `a = TickChain(lab, "x")` and `b = TickChain(lab, "x")` (same charter id), with
  different `roots[1]`. Run `genesis()` on each and mine N2 - 1 blocks. Send and confirm
  `advance(2)` for each, then mine d. Call `verify_release(headers, c.tpl, c.t0, c.package(),
  c.roots, 0, d)` on each: both accept.
- **Bid.** At h(T_0) + N2 - 1, submit the scenario-7 veto package. Then build
  `advance(2, outputs=[CTxOut(v, next_spk()), CTxOut(0, P2A)], version=3, fee_output=None)` and a
  v3 child spending output 1 plus a funder coin with `fee=150_000`, and call `submitpackage`. Then
  mine 1 + d blocks and call `verify_release`.
