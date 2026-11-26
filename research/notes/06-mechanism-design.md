# Mechanism design and cryptoeconomics of bonds, slashing, commitment and costly identity, as applied to constraining AI agents

State as of 2026-11-26. Track 06 of Escapement.

Number labels used throughout: [measured] = independently observed or counted; [vendor] = claim by an interested party (protocol team, company, authors reporting their own system); [derived] = my arithmetic, shown; [spec] = a constant fixed by a protocol specification; [paper] = a figure from a paper's own model or worked example; [news] = a figure reported by a news outlet that I could not trace to a primary count.

Notation used in formulas below (unless a section redefines it): g = gain to the wrongdoer from the act; h = harm caused; p = probability the act is detected and the sanction actually applied; f = sanction (fine, forfeited bond); w = wealth that can actually be collected; B = posted bond; epsA = probability of mistaken acquittal; epsC = probability of mistaken conviction; lambda = share of the bribe surplus captured by a corrupt enforcer.

## Q1. Commitment devices and credible commitment for AI agents

### Takeaway
Commitment works by a "voluntary but irreversible sacrifice of freedom of choice" that the other side can see (Schelling 1956). For AI agents the literature converges on enforcement outside the agent (escrow, smart contracts, proof-checked execution gates), because text instructions do not bind an LLM agent; but the same commitment power supports threats and coercion, and smart contracts only bind what an on-chain condition can observe.

### Cited Findings
- Schelling defines the class of tactics: "The essence of these tactics is some voluntary but irreversible sacrifice of freedom of choice. They rest on the paradox that the power to constrain an adversary may depend on the power to bind oneself" (Introduction, AER 46(3), June 1956). [Schelling 1956](https://userpages.umbc.edu/~nmiller/POLI388/BARGAINING.TCS.pdf)
- Schelling's canonical device is literally a bond: a buyer makes "an irrevocable and enforceable bet with some third party, duly recorded and certified" to pay no more than $16,000 "or forfeit $5,000" [paper example]; "if the buyer can accept an irrevocable commitment, in a way that is unambiguously visible to the seller, he can squeeze the range of indeterminacy down to the point most favorable to him" (Sec. I, "Bargaining Power: the Power to Bind Oneself"). Two conditions: irrevocable and visible. [Schelling 1956](https://userpages.umbc.edu/~nmiller/POLI388/BARGAINING.TCS.pdf)
- Simultaneous commitments produce stalemate: when both sign binding letters, "There is then no sale; both are bound to incompatible positions" (Sec. I). [Schelling 1956](https://userpages.umbc.edu/~nmiller/POLI388/BARGAINING.TCS.pdf)
- Schelling on agents, directly relevant to AI agents: "the agent may be given instructions that are difficult or impossible to change, such instructions (and their inflexibility) being visible to the opposite party" ("Use of a Bargaining Agent"). [Schelling 1956](https://userpages.umbc.edu/~nmiller/POLI388/BARGAINING.TCS.pdf)
- Schelling (1956), as quoted by Budish (fn. 5), on reputation as collateral: "What makes many agreements enforceable is only the recognition of future opportunities for agreement that will be eliminated if mutual trust is not created and maintained, and whose value outweighs the momentary gain from cheating in the present instance." [Budish 2018](https://www.nber.org/system/files/working_papers/w24717/w24717.pdf)
- Bryan, Karlan and Nelson (2010) review lab and field evidence on commitment devices and "distinguish between what we call hard and soft commitments", examine "the demand for commitment devices", and close on "commitment device design" (abstract; Annual Review of Economics 2:671-698). [Bryan, Karlan, Nelson 2010 via IDEAS](https://ideas.repec.org/a/anr/reveco/v2y2010p671-698.html)
- Dafoe et al. (2020) define a commitment device as one that "compels one to fulfill a commitment, either through a 'soft' change to one's incentives for taking different actions ... such as a penalty for non-compliance, or a 'hard' pruning of one's action space" (Sec. 4.3.1); "a conditional commitment is sufficient to overcome the Prisoner's Dilemma, whereas an unconditional commitment is not." [Dafoe et al. 2020](https://arxiv.org/abs/2012.08630)
- Dafoe et al. list reputation, delegation, contracts and hardware as device classes; reputation works "by creating a valuable asset (reputation) which can be put up as collateral"; smart contracts and trusted hardware "enable the delegation of increasingly sophisticated commitments to non-human entities, including commitments that are conditional on states of the world" (Sec. 4.3.2). [Dafoe et al. 2020](https://arxiv.org/abs/2012.08630)
- Dafoe et al. warn the capability is dual-use: "commitment is often essential for making credible promises, but also threats" (Sec. 5.2, "Coercive Capabilities"). [Dafoe et al. 2020](https://arxiv.org/abs/2012.08630)
- Program equilibrium (Tennenholtz 2004, Games and Economic Behavior 49(2):363-373): players submit programs that read each other's source; "a program equilibrium is reached when neither side can improve its expected payoff by replacing its submitted code after observing the other's"; canonical cooperative program cooperates "if they identify a syntactically identical program from their opponent, and defect otherwise" (definitions as restated and cited by Sistla and Kleiman-Weiner, ref. [42]). [Sistla and Kleiman-Weiner 2025](https://arxiv.org/abs/2512.00371)
- LLM agents in open-source games (arXiv 2512.00371, 2025-11-29) "converge to approximate program equilibria" and show "the emergence of payoff-maximizing, cooperative, and deceptive strategies" (abstract, Sec. 6). [Sistla and Kleiman-Weiner 2025](https://arxiv.org/abs/2512.00371)
- Conitzer and Oesterheld (AAAI-23, vol. 37(13):15359-15367, published 2023-06-26): "AI agents are in some ways unlike the agents traditionally studied in game theory, introducing new challenges as well as opportunities"; proposes a game theory of advanced AI agents focused on cooperation (abstract). [Conitzer and Oesterheld 2023 via Crossref](https://api.crossref.org/works/10.1609/aaai.v37i13.26791)
- Sun et al. (arXiv 2311.07815, 2023-11-14; PDF footer: NeurIPS 2023): existing commitment mechanisms suffer "limitations like privacy, integrity, and susceptibility to mediator or user strategic behavior"; decentralized cryptographic commitment devices already coordinate algorithmic agents with incentives "in the order of several million to billions of dollars" [vendor, authors from Flashbots/EF]; uses the MEV literature as evidence of attack vectors. [Sun et al. 2023](https://arxiv.org/abs/2311.07815)
- Chan et al. ("Infrastructure for AI Agents", arXiv 2501.10114 v3, 2025-06-19), Sec. 4.4: threats and norms "can be communicated to language-model-based agents. However, it is not clear how reliably such agents will respond"; "Software-based commitment devices, such as smart contracts, are likely to be more fruitful in the short term"; the limit: "Many agreements involve an information source in the real world ... Without a reliable digital connection to such sources, smart contracts are inapplicable." [Chan et al. 2025](https://arxiv.org/abs/2501.10114)
- Proof-Carrying Contracts (Ciliberto, Rudi, Tassi; arXiv 2610.28484 v1, 2026-10-20): "text alone cannot make it comply"; before an operation runs "the agent must supply a machine-checkable proof that it preserves the agreed constraints", checked by an execution gate (the "Airlock"); "We prove that the constraints hold at every instant during execution, even for an adversarial agent" (abstract). Worked example uses a 300 EUR escrow released "with nobody's approval" when the goal is proven [paper example]. [Ciliberto et al. 2026](https://arxiv.org/abs/2610.28484)

### Inferences
- Bitcoin script meets Schelling's two conditions (irrevocable, publicly visible) for one narrow class of commitments: conditions on spending a UTXO (timelocks, multisig, hashlocks). In Dafoe's terms that is a "hard" pruning of the agent's action space over money it controls; a bond-and-slash design is the "soft" variant (a penalty). Escapement's strongest claims should be about the hard variant.
- Schelling's bargaining-agent point cuts against the thesis as much as for it: an agent whose spending rules are visibly unchangeable gains bargaining power for its principal at the counterparty's expense, and two such agents can lock into Schelling's stalemate. A human renewal or veto path (N1, N11) is what keeps an irrevocable commitment from becoming an irrevocable threat (Dafoe Sec. 5.2).
- Chan et al. and PCC both locate enforcement at a gate the agent cannot bypass. A Bitcoin wallet policy is such a gate for value transfer only; everything an agent does without moving sats is outside it.

### Gaps
- Schelling, The Strategy of Conflict (1960, Harvard University Press) not opened; no claim rests on it.
- No empirical study found that measures whether LLM agents change behavior when an on-chain bond is at stake (as opposed to the principal changing configuration). The "Get It Cooperating" AAMAS 2024 commitment-device study surfaced in search but was not opened.

## Q2. Bonds, deterrence, judgment-proof agents and insurance

### Takeaway
The deterrence condition is g > p*f (act if gain exceeds expected sanction); first-best sanction is f* = h/p; a bond caps f at B, so any harm with h/p > B is underdeterred (the judgment-proof problem). Errors and corrupt enforcers both dilute deterrence multiplicatively. Placing the sanction on a risk-neutral principal induces optimal monitoring of agents, which supports N2, but only if the principal can actually control the agent.

### Cited Findings
- Basic model (Polinsky and Shavell, "The Theory of Public Enforcement of Law", NBER w11780, Nov 2005, chapter for the Handbook of Law and Economics): a risk-neutral individual commits the act iff "gain from doing so exceeds the expected fine: g > pf" (Sec. 7.1, eq. preceding (13)). [Polinsky and Shavell 2005](https://www.nber.org/papers/w11780)
- Optimal fine with p fixed: "if pf = h, namely, the expected fine equals the harm ... f* = h/p, (14)"; footnote 16: the formula "was put forward by Bentham (1789, p. 173), was emphasized by Becker (1968)". [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Judgment-proof limit: "there will be underdeterrence if individuals' wealth is less than h/p, in which case the optimal fine equals their wealth" (Sec. 7.1); for p = 1 the analogous statement is underdeterrence "if the individual's wealth is less than h" (Sec. 4). [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- When the state also chooses p: "the optimal fine is maximal: f* = w", and optimal p satisfies p(e*)w < h, i.e. some underdeterrence is tolerated to save enforcement cost (Sec. 7.1, eq. 15); footnote 18: the low-probability, high-fine point "is due to Becker (1968)". [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Errors: the individual acts iff "g > (1 - epsA - epsC)pf. (24)"; "both types of error reduce deterrence" (Sec. 15). [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Corruption: with lambda = "fraction obtained by the enforcer of the surplus from a bribe agreement", the surplus is f so "an individual pays a bribe of lambda f. To the degree that lambda is less than one, there is underdeterrence" (Sec. 24). [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Principal-agent: "given the probability of detection p, it is optimal for a risk-neutral principal to face a fine of h/p ... the principal will behave socially optimally in controlling his agents"; and "the particular allocation of sanctions may not matter when ... the principal and the agent can reallocate sanctions through their own contract" (Sec. 19). [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Shavell, "The judgment proof problem", International Review of Law and Economics 6(1):45-58 (1986): title and volume confirmed on IDEAS; abstract not accessible (ScienceDirect 403). Content claims about judgment-proofness above rest on Polinsky and Shavell 2005, not on this paper. [IDEAS record](https://ideas.repec.org/a/eee/irlaec/v6y1986i1p45-58.html)
- Becker, "Crime and Punishment: An Economic Approach", JPE 76 (1968), first page 169, DOI 10.1086/259394: record confirmed on IDEAS; the NBER chapter PDF I fetched is a scan without a text layer, so no claim is quoted from Becker directly. [IDEAS record](https://ideas.repec.org/a/ucp/jpolec/v76y1968p169.html)
- AI agent insurance exists as a product category: the Artificial Intelligence Underwriting Company (AIUC) left stealth on 2025-07-23 with a $15 million seed [news] led by Nat Friedman's NFDG, aiming to "Build the insurance, audit, and certification infrastructure needed to bring AI agents safely into the enterprise world"; its AIUC-1 framework "pulls together existing standards like the NIST AI Risk Management Framework, the EU AI Act, and MITRE's ATLAS threat model". [Fortune 2025](https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/)

Bond sizing for an agent (all [derived] from the formulas above):
- Full internalization of harm: B >= h/p. Minimum bond to deter a given gain under adjudication error: B > g / ((1 - epsA - epsC) * p). The bond is the collectible wealth w, so it is also the hard cap on the sanction.
- Example: h = 0.1 BTC, p = 0.2 gives B = 0.5 BTC. With an adjudicator that misses 30% of true violations (epsA = 0.3) and wrongly convicts 5% (epsC = 0.05), deterring g = 0.1 BTC needs B > 0.1 / (0.65 * 0.2) = 0.77 BTC.
- Tail harm: h = 100 BTC, p = 0.01 gives B = 10,000 BTC. No individual principal posts that, so catastrophic, rarely detected harms are judgment-proof by construction.
- Corrupt adjudicator: effective sanction becomes lambda*B, so required bond scales by 1/lambda.

### Inferences
- A bond prices harm; it does not prevent it. It deters only an actor who (a) responds to expected sanctions and (b) controls the act. For a prompt-injected or misaligned agent, (a) fails for the agent and (b) fails for the principal, so the bond degrades into partial compensation capped at B. Chan et al. (Q1) state it is "not clear how reliably" LLM agents respond to threats.
- Polinsky and Shavell's principal-agent result is the best theoretical support for N2: sanction the human principal at h/p and the principal will choose monitoring and contracts. The same section says the split between principal and agent "may not matter" because they can re-contract; for an AI agent there is no agent-side wealth, so all liability must land on the principal anyway.
- Insurance breaks the deterrence channel unless premiums move with risk (classic moral hazard). AIUC ties terms to audits (per its own framing), which is the standard fix, but I found no evidence on whether this works for agents.

### Gaps
- No source opened on surety or performance bond practice (premium rates, claim ratios) or on mandatory liability insurance and moral hazard; those claims are not made here.
- Becker 1968 and Shavell 1986 texts not read directly (see Unverified).

## Q3. Cryptoeconomic slashing in practice: Casper, Ethereum, EigenLayer, rollups, Truebit, Kleros, UMA, Babylon

### Takeaway
Slashing is cheap and objective only for self-evident faults (two conflicting signatures). Everything else needs a challenge game or a vote, which brings the verifier's dilemma, P + epsilon bribery and whale capture. Measured Ethereum slashings are rare and overwhelmingly operational errors, not attacks. Bitcoin can host adjudicator-free equivocation slashing (Babylon EOTS) but today needs a covenant committee because Bitcoin lacks covenants.

### Cited Findings
Casper FFG and proof-of-stake attacks
- Casper FFG (Buterin and Griffith, arXiv 1710.09437, v1 2017-10-25, v4 2019-01-22): a validator "MUST NOT PUBLISH TWO DISTINCT VOTES" with (I) the same target height or (II) one vote surrounding another; violation evidence can be included on chain "at which point the validator's entire deposit is taken away with a small 'finder's fee'" (Sec. 2, Fig. 2). [Buterin and Griffith 2017](https://arxiv.org/abs/1710.09437)
- Accountable safety: "two conflicting checkpoints cannot both be finalized unless >= 1/3 of validators violate a slashing condition (meaning at least one third of the total deposit is lost)"; plausible liveness needs >= 2/3 honest (Sec. 2.1). [Buterin and Griffith 2017](https://arxiv.org/abs/1710.09437)
- Long-range revision: a coalition that withdrew can "finalize conflicting checkpoints without fear of getting slashed (because they have already withdrawn their money)"; defense is a fork-choice rule never reverting finality plus clients logging on "once per 1-2 months" [paper parameter] (Sec. 4.1). The inactivity leak allows conflicting finality "without any validators being explicitly slashed", and the fallback is that validators "manually create a 'minority soft fork'" (Sec. 4.2). [Buterin and Griffith 2017](https://arxiv.org/abs/1710.09437)
- Nothing at stake (Buterin, blog 2014-11-25): under naive PoS "if there are multiple forks, the optimal strategy is to vote on all forks at once"; deposits make single-fork voting dominant only for short-range forks; permanent deposits risk a "permanent nobility". [Buterin 2014](https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity)

Ethereum penalty rules and statistics
- Current spec (Electra): initial slashing penalty = effective_balance // MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA with quotient 4,096 [spec]; whistleblower reward = effective_balance // 4,096 [spec]; MAX_EFFECTIVE_BALANCE_ELECTRA = 2,048 ETH [spec]; process_slashings still multiplies the window's slashed sum by PROPORTIONAL_SLASHING_MULTIPLIER_BELLATRIX. [consensus-specs, electra/beacon-chain.md](https://github.com/ethereum/consensus-specs/blob/master/specs/electra/beacon-chain.md)
- Pectra (which includes Electra) activated on mainnet 2025-05-07 at epoch 364032 [spec]. [Ethereum Foundation blog 2025-04-23](https://blog.ethereum.org/2025/04/23/pectra-mainnet)
- Correlation penalty (Bellatrix-era description): penalty = min(B, 3*S*B/T), S = total slashed in the 8,192-epoch (~36 day) window, T = total active balance, multiplier 3 [spec]; intent: a "one-off event posing little threat" is lightly punished while a mass event that "might be the result of an attempt to finalise conflicting blocks" is punished maximally; initial penalty was 1/32 before Electra [spec]. [eth2book, Slashing](https://eth2book.info/latest/part2/incentives/slashing/)
- [derived] Electra initial penalty: 32 ETH / 4,096 = 0.0078 ETH for a 32 ETH validator; 2,048 / 4,096 = 0.5 ETH at max effective balance. Correlation fraction is about min(1, 3*S/T): if 1/3 of stake is slashed inside the window, the slashed validators lose everything; an isolated slashing loses almost nothing beyond the initial penalty.
- Counts: 438 validators slashed since beacon-chain genesis as of 2024-09-17 [measured] (MigaLabs, which also found explorer errors: "A validator cannot be slashed twice"). [MigaLabs 2024-09-18](https://migalabs.io/blog/slashed-validators-discrepancies-in-popular-block-explorers)
- 525 validators slashed since 2020 per MigaLabs data [measured, via news]; besides the September 2025 event "there have only been 15 such cases this year" [news]; in November 2023 "nearly 100 validators tied to Bitcoin Suisse lost almost $200,000" [news]. [CryptoSlate 2025-09-11](https://cryptoslate.com/ethereum-slashing-wipes-funds-of-40-validators-punished-for-double-signing/)
- 2025-09-10 mass slashing: 39 validators connected to SSV operators [news; CryptoSlate's headline says 40], with "operational patterns consistent with incomplete migrations and active residual instances". [Cryptonomist 2025-09-11](https://en.cryptonomist.ch/2025/09/11/mass-slashing-on-ethereum-39-validators-affected-operational-link-with-ssv/)

EigenLayer restaking
- Slashing went live on mainnet on 2025-04-17 ("We expect Slashing to go live later today, April 17th"); AVSs "define specific conditions" and operators opt in; "Unique Stake Allocation" lets an operator "Ensure only one AVS can slash that particular stake"; ecosystem claimed "190 AVSs in development (including 40 on mainnet), 2,000+ registered Operators, and 80,000+ unique staking addresses" [vendor]. [EigenLayer blog 2025-04-17](https://blog.eigencloud.xyz/slashing-goes-live/)
- Durvasula and Roughgarden (arXiv 2407.21785, 2024-08-01): for a PBFT-type chain where double-voters lose all stake, attack cost is bounded below by (1/3)*sum(sigma_v) and the chain is "cryptoeconomically secure provided the estimated profit pi of an attack is less than this quantity"; with overcollateralization factor gamma (stake exceeds corruption profit by factor 1 + gamma), a shock destroying fraction psi of stake can cascade to at most (1 + 1/gamma)*psi, tight (Theorem 1); example: if "attack costs always exceed attack profits by 10%, then a sudden loss of .1% of the overall stake ... cannot result in the ultimate loss of more than 1.1%" [paper]. [Durvasula and Roughgarden 2024](https://arxiv.org/abs/2407.21785)
- [derived] Check: (1 + 1/0.1) * 0.1% = 11 * 0.1% = 1.1%.

Optimistic rollups and the 7 days
- L2BEAT (forum, 2026-04-30): "the time needed to detect a 51% attack, coordinate a fork, implement it and activate it is around 6 days. Leaving 1 day for honest challengers to submit a fraud proof and play the dispute game in the absence of censorship, the minimum challenge period needed to guarantee safety of funds in the presence of 51% attacks is 7 days" [paper-style estimate]. Stage 1 minimum cut to 5 days: "one day to resolve economic attacks, and 4 days to resolve network delays"; "The 7d lower bound for Stage 2 remains unaffected". Soft censorship requires bribing proposers "with at least the amount of fees" the censored transaction would pay. [L2BEAT 2026](https://forum.l2beat.com/t/stage-1-update-minimum-challenge-period-reduction-from-7d-to-5d/425)
- Landis (arXiv 2312.01549 v3, 2024-10-16) formalizes the verifier's dilemma for rollups: "the verifier has no incentive to execute its role if there are never any errors and therefore no rewards"; treats a mechanism as secure only "if there is a unique pure equilibrium that is the intended behaviour", and exhibits mixed equilibria that are not. [Landis 2024](https://arxiv.org/abs/2312.01549)

Truebit and the verifier's dilemma
- Teutsch and Reitwiessner (arXiv 1908.04756, posted 2019-08-12; the paper itself is dated 2017-11-16): "if the verification work becomes substantial, then miners risk falling behind in the mining race by following protocol and actually verifying ... A rational miner doesn't know what to do!" (Sec. 3.1); they cite the July 4, 2015 Bitcoin fork as the dilemma "manifested". [Teutsch and Reitwiessner](https://arxiv.org/abs/1908.04756)
- Why plain rewards fail: rewards for checking give "no incentive for correct verification"; bug bounties work only "when the Verifier has some reason to believe that a bug might actually exist"; their fix is "forced errors" (deliberate wrong answers with a jackpot), which they call TrueBit's "Achilles' heel" because "the prize for discovering forced errors is necessarily enormous" (Sec. 2, Sec. 3). [Teutsch and Reitwiessner](https://arxiv.org/abs/1908.04756)

Schelling-point courts and oracles
- P + epsilon (Buterin, 2015-01-28, attack credited to Andrew Miller): in a vote paying P to majority voters, an attacker credibly promises P + epsilon to those voting the false answer if the truth wins; voting false becomes dominant and "The attack has successfully managed to take over the mechanism at zero cost"; mitigation: large deposits that grow with contention, so "the bribe must now be greater than the deposit". [Buterin 2015](https://blog.ethereum.org/2015/01/28/p-epsilon-attack)
- Kleros (Ast et al., Frontiers in Blockchain, 2023-10-09, DOI 10.3389/fbloc.2023.1204090; authors from Kleros Cooperative): jurors drawn "proportional to staked PNK. No demonstrated expertise or identity proof is required"; dissenters "lose their staked PNK, which is given to majority jurors"; caseload "exceeding 1,500 disputes" [vendor]; redistributive deposits make P + epsilon attacks "require substantially higher budgets"; "There is generally no reliable way to ensure that all jurors ... are distinct, identifiable individuals". [Ast et al. 2023](https://www.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2023.1204090/pdf)
- UMA (official docs): a proposer posts a bond "refundable if the proposal is deemed correct"; disputes go to the DVM with a "24-hour commit period" and "24-hour reveal period"; resolution needs "a minimum 65% majority of staked UMA" [spec]; non-voters and losing voters are slashed; unstaking takes a "one-week period"; the security argument is that corrupting the DVM would make UMA "depreciate significantly", which "creates a cost of corruption"; the optimistic oracle resolves "currently 99.8%" of requests without the DVM [vendor]. [UMA docs](https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work)
- Polymarket/UMA, March 2025: market "Ukraine agrees to Trump mineral deal before April?" ($7 million [news]) went from 9% to 100% "yes" on 2025-03-24/25 and resolved yes though no deal existed; users alleged a "UMA whale" swung the vote; Polymarket: "This is an unprecedented situation", the outcome "wasn't a market failure", no refunds; proposals require a $750 USDC.e bond [news]. [The Block 2025-03-26](https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented)

Bitcoin-native slashing (Babylon)
- Tas, Tse, Gai, Kannan, Maddah-Ali, Yu (arXiv 2207.08392 v7, 2025-02-01): PoS chains face "non-slashable long-range safety attacks", and slashable safety is "not possible without external trust"; checkpointing on Bitcoin cuts withdrawal delay "from weeks in existing PoS chains to less than 5 hours" at "less than 10K USD per annum" [paper]. [Tas et al. 2022](https://arxiv.org/abs/2207.08392)
- "Bitcoin Staking" (Dong, Litos, Tas et al., arXiv 2408.01896 v5, 2026-05-18): EOTS: "when a signer signs two messages using the same private key and context, then the private key can be extracted from the signatures"; the protocol sends "an evidence that can directly lead to slashing: the staker's private key"; guarantees 1/3-economic safety; but "we require one of the covenant committee members to be honest (existential honesty). If covenants are enabled on Bitcoin in the future, the protocol would not need existential honesty"; drawback: "if only a single member is offline or refuses to participate, then the committee cannot complete its signature" (Sec. 1.4.1 and covenant-committee section). [Dong et al. 2024](https://arxiv.org/abs/2408.01896)
- Same paper on native PoS: "by borrowing a sufficient amount of stake, the adversary can temporarily control over 2/3 of the validator set ... and subsequently withdraw its stake to pay back its loan". [Dong et al. 2024](https://arxiv.org/abs/2408.01896)
- Deployment: Babylon Genesis launched 2025-04-10; Bitcoin staking activated in pilot mode on 2025-04-11 with 1,000 BTC from Phase 1 allowed [vendor]; "fully permissionless" from 2025-04-24. [Babylon Labs blog 2025-05-08](https://babylonlabs.io/blog/phase-2-launch-round-up---bitcoin-staking-activated-babylon-genesis-marches-towards-the-next-phase)

### Inferences
- The split that matters for Escapement: self-evident faults (two signatures on conflicting statements at the same "height") can be slashed without a judge; everything else (did the agent deliver, lie, cause harm) needs an oracle, and every oracle surveyed here has a documented or theoretical capture path (P + epsilon, token-weighted whale, verifier's dilemma).
- Ethereum's real slashing record is a warning for N3: agents that restart, fail over or run duplicate instances will equivocate by accident, exactly as SSV/Ankr validators did in 2025-09. Any agent equivocation-slashing design needs the analogue of validator anti-slashing databases and a correlation-scaled penalty so that isolated faults cost little.
- Ethereum's correlation penalty is a useful template for agent swarms: penalty proportional to how many bonded agents misbehaved together makes coordinated defection expensive while sparing isolated bugs.
- UMA's cost-of-corruption argument is Budish's "sabotage" assumption (token value collapses after an attack). It fails when the attacker's profit is external to UMA (the $7M market) and the vote is cheaper than that profit.
- The 7-day window is a social-coordination constant (time to fork away a 51% attacker), not a computation time. An Escapement challenge window for agent claims inherits the same logic: it must exceed the time for humans to notice and react.

### Gaps
- EigenLayer whitepaper text could not be opened (403 and HTML redirect); its exact CoC/PfC definitions and veto-committee design are not quoted here.
- No independent count of EigenLayer or Babylon slashing events found. Kleros whitepaper download failed.
- No current (2026) total of Ethereum slashings found beyond the September 2025 figure.

## Q4. Economic limits of security: Budish, bribery, zero-cost attacks, cost vs profit of corruption

### Takeaway
Security bought with recurring payments is linear in spend and must exceed the one-shot value of an attack (Budish). Attack resources can be rented or borrowed, and in some models the attacker's net cost is negative (Gans and Halaburda). Cost of corruption must exceed profit from corruption with a buffer, or a single shock cascades (Durvasula and Roughgarden).

### Cited Findings
- Budish (NBER w24717, June 2018; first public draft 2018-05-03). Variables: N* = honest computational units, c = per-block cost per unit (c = rC + e), P_block = per-block reward, A = attacker power multiple, t = attack duration in blocks, V_attack = attacker payoff.
  - Free entry: N* c = P_block (1).
  - Incentive compatibility: alpha * N* c > V_attack (2), with alpha = (A - 1) t net of block rewards.
  - Combined: P_block > V_attack / alpha (3): "the equilibrium per-block payment to miners for running the blockchain must be large relative to the one-off benefits of attacking it."
  - "the security of the blockchain is linear in the amount of expenditure on mining power", unlike "a lock on a door [that] increases the security of a house by more than the cost of the lock" (Sec. 1.2). [Budish 2018](https://www.nber.org/system/files/working_papers/w24717/w24717.pdf)
- Budish double-spend example: p_transaction > v_transaction / alpha (4); with A = 1.25 and a 6-block escrow, alpha = 3.35 [paper], so per-transaction payment must exceed about 30% of the largest transaction [paper]. For a $1M transaction with e = 100 blocks and A = 1.05, p_transaction > $108,700 [paper]; with e = 1,000 blocks ("1 week at 10 minutes per block") about $18,700 [paper]. [Budish 2018](https://www.nber.org/system/files/working_papers/w24717/w24717.pdf)
- The constraint "is softer (i.e., stock versus stock) if both (i) the mining technology ... is both scarce and non-repurposable, and (ii) any majority attack is a 'sabotage'" that collapses the chain's value; Budish notes the first large majority attack, "the $18M attack on Bitcoin Gold" [news, as cited], came weeks after his draft (abstract and title-page note). [Budish 2018](https://www.nber.org/system/files/working_papers/w24717/w24717.pdf)
- Gans and Halaburda (arXiv 2308.06568, 2023-08-12; Management Science 70(6):4155-4165, 2024, DOI 10.1287/mnsc.2023.02426): "a majority attacker can successfully attack with a negative net cost when accounting for the mining rewards the attacker collects during the attack. This shows that the protocol mechanisms are insufficient to create a secure network, emphasizing the importance of socially driven mechanisms external to the protocol." [Gans and Halaburda via IDEAS](https://ideas.repec.org/a/inm/ormnsc/v70y2024i6p4155-4165.html); [arXiv](https://arxiv.org/abs/2308.06568)
- Renting and borrowing: Buterin (2019-04-03) notes vote-buying can be done "by renting coins on the market and using them to participate in votes"; Babylon's authors show borrowed stake can take >2/3 of a PoS validator set and be repaid after the attack (Q3). [Buterin 2019](https://vitalik.eth.limo/general/2019/04/03/collusion.html); [Dong et al. 2024](https://arxiv.org/abs/2408.01896)
- Cost of corruption vs profit from corruption, formalized for restaking: secure iff pi < (1/3) sum(sigma_v); robust security needs a buffer gamma, with cascade bound (1 + 1/gamma) psi (Q3). [Durvasula and Roughgarden 2024](https://arxiv.org/abs/2407.21785)

### Inferences
- Applied to an agent bond [derived reasoning from (2)]: a bond B deters a one-shot defection worth V only if p_eff * B > V. Bonds are stock, not flow, so agent bonds are on the better side of Budish's dichotomy; but the required stock still scales with the largest single gain available to the agent, and Budish's point that this is "very expensive" carries over directly.
- A spending cap (N1) sidesteps detection entirely for value that must pass through the wallet: loss per period is at most the allowance A, with p = 1 by construction. This is the strongest economic result available to Escapement, and also its boundary: it bounds money out of the wallet, not harm done by other means.
- Gans and Halaburda and Casper's "minority soft fork" both end at the same place: when the protocol's incentives fail, the backstop is social (humans forking, courts). Escapement should state that its guarantees inherit a human backstop rather than replace one.

### Gaps
- Bonneau 2016 ("Why Buy When You Can Rent?") could not be opened; bibliographic data confirmed via Crossref only. No claim rests on its content.
- EigenLayer whitepaper's CoC/PfC wording not verified (see Unverified).

## Q5. Costly identity and sybil resistance: Douceur, proof of personhood, World ID, coin age, fidelity bonds, signalling, plutocracy

### Takeaway
Without a trusted authority, sybil identities are bounded only by the attacker's resources (Douceur), so any stake- or bond-based identity yields "one dollar, one vote", and a costly signal only separates types whose costs differ (Spence); sats cost an honest and a malicious agent the same. Proof-of-personhood counts humans, not agents, and its leading deployment (World ID, ~18M verified, vendor) faces continuing regulatory orders. Timelocked Bitcoin bonds as sybil friction already exist (JoinMarket fidelity bonds), and their documented weakness is that long-term holders get them almost free.

### Cited Findings
- Douceur (IPTPS 2002): "without a logically centralized authority, Sybil attacks are always possible except under extreme and unrealistic assumptions of resource parity and coordination among entities" (abstract). Lemma 1: if rho is the ratio of the faulty entity's resources to a minimally capable entity's, it can present about rho (rounded down) identities. Lemma 2: "If local entity l accepts entities that are not validated simultaneously, then a single faulty entity f can present an arbitrarily large number of distinct identities"; "Lemma 2 is insurmountable for intrinsically temporal resources, such as computation speed and communication bandwidth. However, since storage is not inherently time-based, entity l can indefinitely extend the challenge duration". [Douceur 2002](https://www.microsoft.com/en-us/research/wp-content/uploads/2002/01/IPTPS2002.pdf)
- Borge et al. (IEEE EuroS&PW 2017, DOI 10.1109/EuroSPW.2017.46): PoW "leads to massive amounts of wasted electricity and re-centralization, whereas major stakeholders in PoS might be able to create a monopoly"; PoP "binds physical entities to virtual identities in a way that enables accountability while preserving anonymity" (abstract). [Borge et al. 2017](https://infoscience.epfl.ch/record/301744/files/pop.pdf)
- Ford (arXiv 2011.02412, 2020-11-05): pseudonym parties "rely for security on the fact that real people still (at present) have only one physical body each that can be in only one place at a time"; PoW gives "a rule much closer to a 'one dollar, one vote' than a 'one person, one vote' principle"; PoS "is still a proof of investment ... and thus still operates in the 'one dollar, one vote' paradigm", its participants "merely pay the opportunity cost of not using their cryptocurrency" (Sec. 3, 4.5). [Ford 2020](https://arxiv.org/abs/2011.02412)
- Siddarth, Ivliev, Siri, Berman (arXiv 2008.05300, 2020): resource-based membership "rendered most crypto-governance practices into plutocracies, with a few powerful players able to control choices" (Sec. 1); Idena FLIP tests: "Human accuracy in solving FLIPs is at 95%, while AI teams have been able to reach 60-76%" [measured, as cited, 2020]; reverse Turing tests "fail to address human-generated attacks, in which one individual passes the test multiple times". [Siddarth et al. 2020](https://arxiv.org/abs/2008.05300)
- Adler et al., "Personhood credentials" (arXiv 2408.07892, v1 2024-08-15, v4 2025-01-17; 32 authors): two requirements, "Credential limits: The issuer of a PHC gives at most one credential to an eligible person" and "Unlinkable pseudonymity"; delegation: "Should a principal fail to address harms caused by their PHC-verified AI, they risk suspension from a service"; "PHCs create a form of accountability for AI agents without demanding sensitive information from principals" (Sec. 3.3). [Adler et al. 2024](https://arxiv.org/abs/2408.07892)
- World (formerly Worldcoin): "One network. 10 million verified humans" [vendor] announced around 2025-01-13; same week Chile's Supreme Court gave World 30 days to delete a minor's World ID and biometric data. [Biometric Update 2025-01-13](https://www.biometricupdate.com/202501/world-network-reaches-10-million-verified-humans-amid-continued-legal-blocks)
- World status 2026: "18 million verified humans across 160 countries" [vendor, as reported]; Okta plans "Human Principal, a product allowing API builders to verify whether a human stands behind an agent" [vendor]. [Decrypt 2026-04-17](https://decrypt.co/364774/sam-altman-world-zoom-tinder-better-verify-humans-ai-age)
- Regulatory: Thailand's PDPC ordered World to stop iris enrollment and delete records, with about 1.2 million Thai residents scanned [news]; the same report says Germany ordered deletion of biometric data in December 2024 and the Philippines banned the project in October 2025. [IDTechWire 2025-11-26](https://idtechwire.com/thailand-orders-worldcoin-to-halt-iris-scans-and-delete-biometric-data/)
- Human Passport (ex-Gitcoin Passport): acquired by Holonym Foundation, announced 2025-02-10; "over 2M users, with over 35M identity credentials" [vendor]. [human.tech blog 2025-02-10](https://human.tech/blog/from-gitcoin-passport-to-human-passport-we-re-now-part-of-human-tech)
- Coin age (King and Nadal, PPCoin paper, 2012-08-19): "Coin age is simply defined as currency amount times holding period"; 10 coins held 90 days = 900 coin-days [paper]; the main chain is "the block chain with highest total consumed coin age"; history is "further protected by a centrally broadcasted checkpoint mechanism" (abstract, "Coin Age", "Main Chain Protocol"). [King and Nadal 2012](https://bitcoin.peryaudo.org/vendor/peercoin-paper.pdf)
- JoinMarket fidelity bonds (code docs): "bitcoin value is deliberately sacrificed to make a cryptographic identity expensive to obtain"; usually by sending coins to an OP_CHECKLOCKTIMEVERIFY address; "The valuable thing being sacrificed is the time-value-of-money"; formula bond_value = (locked_coins * (exp(interest_rate * locktime) - 1))^x, default x = 1.3 and interest_rate = 1.5% per year [spec]; the superlinear exponent gives "an incentive for makers to lump all their coins into just one bot"; and "a long-term holder (or hodler) of bitcoins can buy time-locked fidelity bonds essentially for free, assuming they never intended to transact with their coins". [JoinMarket docs, fidelity-bonds.md](https://github.com/JoinMarket-Org/joinmarket-clientserver/blob/master/docs/fidelity-bonds.md)
- [derived] JoinMarket arithmetic: 1 BTC locked 1 year sacrifices 1*(e^0.015 - 1) = 0.0151 BTC of time value; bond value 0.0151^1.3 = 0.0043. Splitting a fixed stake across k identities multiplies total weight by k^(1 - x) = k^(-0.3): 10 identities keep 50% of the weight, 100 keep 25%. The docs' own check: 5 BTC sacrificed gives 5^1.3 = 8.1 and 6 gives 10.3.
- Spence (QJE 87(3):355-374, 1973): "a signal will not effectively distinguish one applicant from another, unless the costs of signaling are negatively correlated with productive capability" ("A Critical Assumption", pp. 358-359). [Spence 1973](https://www.sfu.ca/~allen/Spence.pdf)
- Agents: Xia et al. (arXiv 2605.08922, 2026-05-09): PoP approaches do not transfer "to AI agents, whose 'personhood' is not tied to any biological substrate and whose capabilities can be duplicated at near-zero marginal cost"; candidate uniqueness notions "perhaps grounded in model fingerprints, operator attestations, or staked collateral"; "a guarantee that no current standard provides" (Sec. 4.1.5). [Xia et al. 2026](https://arxiv.org/abs/2605.08922)

### Inferences
- [derived] Bond-based sybil bound, from Douceur Lemma 1: with minimum bond B_min, an actor with liquid wealth W controls at most W / B_min identities. A bond requirement does not stop swarms; it prices them. A principal with 1 BTC and B_min = 0.001 BTC runs 1,000 agents.
- Timelocked capital behaves like Douceur's storage, not his temporal resources: the same coins cannot back two concurrent bonds, and the UTXO set lets a verifier check all bonds simultaneously. That is a real advantage over CPU-based throttles for N6. But Bitcoin's time cost is opportunity cost, which JoinMarket's own docs say is near zero for holders, and capital can be borrowed (Babylon) or rented (Buterin).
- Spence's condition is the deepest problem for "costly identity" as a trust signal: the cost of locking sats is the same for an honest and a malicious agent (or lower for a well-funded attacker), so a bond separates wealth and time preference, not intent. It works as liability (something to slash), not as a signal of type.
- Plutocracy is not a side effect: Ford, Siddarth and Borge each identify stake-weighting as structurally "one dollar, one vote", and JoinMarket deliberately makes it superlinear. For Escapement, whoever has the most sats gets the most agent identities and the most weight in any bonded vote.
- PHCs (Adler) point to the alternative N2 relies on: bind each agent to a rate-limited human credential and punish the principal (suspension), not the agent. That moves sybil resistance to the human layer, where World ID's regulatory record shows the costs.

### Gaps
- No 2025-2026 primary data found on BrightID or Idena activity or attacks; Siddarth et al. (2020) is the latest opened source on them.
- Zahavi (1975) handicap principle: metadata only (see Unverified); no claim rests on it.
- No source found that measures how many sats-per-identity a real sybil attacker would pay (no empirical sybil cost curve for fidelity bonds).

## Q6. Collusion and bribery among agents

### Takeaway
Mechanisms robust to individual deviation generally fail against coalitions; per-agent bonds assume independent decisions, which agents sharing a model, principal or channel do not have. Bribery is cheap when it can be made conditional (P + epsilon). LLM agents collude without instruction in pricing experiments and can hide coordination steganographically.

### Cited Findings
- Buterin (2019-04-03): "there are large classes of games that do not have any stable outcome that a coalition cannot profitably deviate from"; "it is much harder, and more likely to be outright impossible, to make mechanisms that maintain desirable properties in a model where participants can collude"; coin-based designs "can be circumvented by users bribing other users to vote for them en masse"; "mechanisms that do not rely on any model of identity and only rely on coins fundamentally cannot solve the problem"; needed: "an identity that you cannot credibly rent or sell"; and "the use of security deposits is fundamentally in the same class of technique". [Buterin 2019](https://vitalik.eth.limo/general/2019/04/03/collusion.html)
- Conditional bribes cost nothing when they succeed (P + epsilon, Q3), and enforcer bribery dilutes the sanction to lambda*f (Polinsky and Shavell Sec. 24, Q2). [Buterin 2015](https://blog.ethereum.org/2015/01/28/p-epsilon-attack); [Polinsky and Shavell 2005](https://www.nber.org/system/files/working_papers/w11780/w11780.pdf)
- Coalitions and stake: Babylon's borrowed-stake attack, Durvasula and Roughgarden model attacks as coalitions of services and validators, and Ethereum's correlation penalty targets coordinated faults (Q3). [Dong et al. 2024](https://arxiv.org/abs/2408.01896); [eth2book](https://eth2book.info/latest/part2/incentives/slashing/)
- Fish, Gonczarowski, Shorrer (arXiv 2404.00806 v6, 2026-08-31; first version January 2024; one-page abstract in ACM EC proceedings per the paper): "LLM-based pricing agents quickly and autonomously reach supracompetitive prices and profits"; "Variation in seemingly innocuous phrases in LLM instructions ('prompts') substantially influence the degree of supracompetitive pricing" (abstract). [Fish et al. 2024](https://arxiv.org/abs/2404.00806)
- Motwani et al. (arXiv 2402.07510 v5, 2025-07-25): formal threat model for steganographic "secret collusion"; empirical evaluations show "rising steganographic capabilities in frontier single and multi-agent LLM setups" and "limitations in countermeasures such as monitoring, paraphrasing, and parameter optimization" (abstract). [Motwani et al. 2024](https://arxiv.org/abs/2402.07510)

### Inferences
- A coalition of k agents each with bond B faces total exposure kB, but can pool a joint gain V; deterrence needs p_eff * k * B > V. When agents share one principal, the bonds are one pot, and the coalition is really one actor.
- Escapement designs that use multiple agents as mutual watchers (challengers, co-signers, jurors) inherit Fish et al. and Motwani et al.: agents from the same model family are correlated, may collude spontaneously, and may coordinate in ways monitors miss. Watchers should be humans or independent principals with their own bonds at risk.
- The Ethereum correlation penalty and Kleros' redistributive deposits are the two deployed cryptoeconomic answers to cartels: make simultaneous misbehavior cost more than isolated misbehavior, and pay defectors from the losers' deposits.

### Gaps
- No source found that tests bonded LLM agents against bribery offers. Collusion among AI agents is covered in depth by another Escapement track.

## Q7. Pricing actions as rate limiting: hashcash lineage, when cost throttles fail, blockspace

### Takeaway
Pricing access "restrains, but does not prohibit" (Dwork and Naor). It fails when attacker value per action exceeds the price, when attackers use stolen resources, and when honest and abusive volumes overlap (Laurie and Clayton). Blockspace is a global, fee-auctioned cap, so as a rate limit it binds the least wealthy first.

### Cited Findings
- Dwork and Naor (preliminary version presented at CRYPTO '92, per the paper): "require a user to compute a moderately hard, but not intractable, function in order to gain access to the resource, thus preventing frivolous use"; an "access control mechanism that can be used whenever it is desirable to restrain, but not prohibit, access to a resource"; a trapdoor "shortcut" lets the resource manager "grant bulk mailings at a price chosen by the post office" (abstract, Sec. 1). [Dwork and Naor 1992](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/pvp.pdf)
- Laurie and Clayton (paper dated 2004-05-03): spammer PC cost about 75 cents per day [paper estimate]; at 0.005 cents per email, breakeven is 15,000 emails per day, so "C must be set so that each calculation takes at least 5.8 seconds" [paper]; to restore 0.1-cent pricing, restrict to "1,750 emails per day ... at least 50 seconds"; with a million compromised machines, cutting spam to 1% needs 250 emails per day per machine, "C of 346 seconds" [paper]. [Laurie and Clayton 2004](https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf)
- Their conclusion: "the limits we would wish to set are of the same order of magnitude as global averages for usage", so many real users "would be unable to provide 'proof-of-work' for all the legitimate email that they currently send"; schemes need "many orders of magnitude between the work done by the 'good guys' and that achievable by the 'bad guys'" (Sec. 5). [Laurie and Clayton 2004](https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf)
- [derived] Check: $0.75 / $0.00005 = 15,000 emails; 86,400 s / 15,000 = 5.76 s.
- Bitcoin capacity: BIP141 sets "block weight <= 4,000,000" [spec]; blocks arrive "roughly ten minutes" apart (Budish's description of the protocol target). [BIP141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki); [Budish 2018](https://www.nber.org/system/files/working_papers/w24717/w24717.pdf)
- [derived] Assuming a simple 1-input, 2-output P2WPKH transaction of about 141 vbytes (564 weight units; size is my assumption, not from an opened source): 4,000,000 / 564 = about 7,090 transactions per block, about 11.8 per second at 600 s per block. That ceiling is shared by everyone on Bitcoin.
- Censorship through the fee market: to censor a transaction "they need to bribe block proposers with at least the amount of fees" it would pay (L2BEAT, soft-censorship analysis). [L2BEAT 2026](https://forum.l2beat.com/t/stage-1-update-minimum-challenge-period-reduction-from-7d-to-5d/425)

### Inferences
- [derived] General throttle condition: a per-action price c stops an attacker only if c > v_a (the attacker's value per action), and stays usable only if c * n_h fits honest users' budgets. If v_a is high (high-stakes actions are exactly where it is), no tolerable c deters. Stolen keys or compromised machines drive the attacker's c to near zero, as botnets did for proof-of-work.
- Blockspace as a rate limit (N7) is a fee auction: a well-funded agent outbids, a poor human waits, and an adversary can buy blockspace to delay a human's timeout or fraud-proof transaction. The cap is global, not per agent, and Lightning or other off-chain channels let agents act without touching it.
- The useful version of N7 is narrower: require that a specific high-stakes authorization be confirmed on chain at depth d, which forces a wall-clock delay of about d blocks that compute cannot compress. That is a timelock argument, not a throughput argument.

### Gaps
- Hashcash (Back 1997/2002) not opened; no claim rests on it.

## Unverified sources (opened only partly or not at all; no claim rests on them)
- Bonneau 2016, "Why Buy When You Can Rent? Bribery Attacks on Bitcoin-Style Consensus", FC 2016 Workshops, LNCS 9604 pp. 19-26, DOI 10.1007/978-3-662-53357-4_2: metadata confirmed via Crossref; PDF links 404 or paywalled.
- Shavell 1986, "The judgment proof problem", IRLE 6(1):45-58: title confirmed on IDEAS; abstract and text not accessible.
- Becker 1968, JPE 76(2): scanned PDF without text layer; content cited only through Polinsky and Shavell 2005.
- Tennenholtz 2004, "Program equilibrium", GEB 49(2):363-373, DOI 10.1016/j.geb.2004.02.002: metadata via IDEAS and Semantic Scholar; content via Sistla and Kleiman-Weiner 2025.
- Zahavi 1975, "Mate selection: a selection for a handicap", J. Theor. Biol., DOI 10.1016/0022-5193(75)90111-3: metadata via Europe PMC, no abstract.
- Schelling 1960, The Strategy of Conflict: not opened.
- EigenLayer whitepaper (docs.eigenlayer.xyz PDF): blocked (403/HTML); CoC/PfC wording seen only in search snippets.
- Kleros long whitepaper (kleros.io): download failed.
- Worldcoin actions in Hong Kong (2024-05), Brazil (2025-01), Spain (2026), and the 5M-token/25% whale figure in the Polymarket dispute: search snippets only.
- Google AP2, Lightning Labs L402, AWS AgentCore Payments, zCloak AI-human multisig, arXiv 2507.00631 (bonded verification protocol), IACR ePrint 2026/2001 (Bitcoin fused bonds; download returned HTML), Damus/Nostr fidelity-bond proposal, The Block on agentic-payment congestion (2026-09-29), "Get It Cooperating" (AAMAS 2024): surfaced in search, not opened.

## Implications for Escapement

Strengths found
- Caps need no detection. A wallet allowance enforced by script or smart-contract policy bounds value out of the wallet to the allowance per period with p = 1, which beats every bond whose deterrence decays with p (f* = h/p). This is the single strongest mechanism-design argument for the thesis (Q2, Q4).
- Bitcoin offers Schelling's two ingredients (irrevocable, publicly visible) for spend conditions, and Douceur-style "storage-like" stake: locked coins cannot back two identities at once and are checkable simultaneously in the UTXO set (Q1, Q5).
- Adjudicator-free slashing exists for one class of misbehavior: equivocation. EOTS extracts the key from two signatures in the same context and is deployed on Bitcoin by Babylon (since 2025-04) (Q3).
- Liability on the human principal is the textbook answer to agent misconduct (Polinsky and Shavell Sec. 19) and the PHC literature proposes the same thing for AI delegates (Adler et al.) (Q2, Q5).
- Timelocks give uncompressible wall-clock delay: the reason optimistic rollups wait 7 days is the time humans need to react, which a block-height lock enforces regardless of agent speed (Q3, Q7).

Fatal or serious problems found
1. Judgment-proof ceiling. Deterrence needs B >= h/p; for rare, catastrophic, hard-to-detect harms (h large, p small) the required bond exceeds any principal's wealth (e.g., h = 100 BTC, p = 0.01 gives 10,000 BTC [derived]). Bonds work only for bounded, detectable harms.
2. Bonds do not constrain a non-responsive agent. They deter actors who respond to expected sanctions and control the act; a misaligned or injected agent satisfies neither, and the principal may not control it. The bond then becomes capped compensation (Q2; Chan et al.).
3. The oracle problem. Outside equivocation, slashing needs adjudication, and every adjudicator studied is capturable: P + epsilon makes Schelling votes free to hijack; token-weighted DVM was allegedly swung by a whale in the $7M Polymarket market (2025-03); the verifier's dilemma means nobody checks when nobody cheats (Q3).
4. Slashing punishes operations, not malice. Measured Ethereum slashings are mostly duplicate-instance and migration errors (2025-09 SSV/Ankr event). Agent equivocation slashing will hit restarts and failovers first (Q3).
5. Bitcoin cannot yet slash on its own. Babylon needs a covenant committee with "existential honesty" because Bitcoin lacks covenants, and a single non-signing member stalls it (Q3).
6. Stake is rentable, borrowable and plutocratic. Bonds price sybils at W / B_min identities, give the richest the most agents, and per Spence separate wealth rather than intent; JoinMarket's docs concede bonds are "essentially free" for holders (Q5).
7. Coalitions defeat per-agent bonds, and LLM agents collude spontaneously and covertly (Q6).
8. Economic security is linear in spend and must exceed one-shot attack value (Budish); some majority attacks have negative net cost (Gans and Halaburda). Protocols fall back to social coordination (Casper's minority soft fork) (Q4).
9. Blockspace is a poor rate limit: global, fee-auctioned, bypassable off chain, and usable by an adversary to delay a human's transaction (Q7).
10. The properties Escapement relies on cut both ways: Marino and Juels (arXiv 2507.08249 v3, 2026-08-26) argue that giving agents crypto creates "new vectors of AI harm" from sovereignty, immutability, pseudonymity and trustless transactions; agent errors become irreversible ("no entity has the power to undo it"), and smart-contract bounties can pay for real-world crimes. [Marino and Juels](https://arxiv.org/abs/2507.08249)

Net: the literature supports a narrow thesis (Bitcoin can cap and delay what passes through keys the agent holds, and can make equivocation self-slashing), and undercuts a broad one (bonds and costly identity do not constrain agent behavior in general, because of judgment-proofness, oracles, renting and collusion).

## Novelty check

N1. Sat budgets / allowance as a dead-man switch
- Closest prior work: Coinbase Spend Permissions define a spender with an `allowance` ("Maximum allowed value to spend within each `period`"), a `period` ("Time duration for resetting used `allowance` on a recurring basis"), and `start`/`end` timestamps after which the permission is invalid [spec] ([Coinbase docs](https://docs.cdp.coinbase.com/coinbase-wallet/reference/onchain-contracts/spend-permissions.md)). An `end` timestamp is a dead-man switch: authority expires unless the account signs a new permission. Safe's docs list an "Agent with spending limit" quickstart ([Safe docs](https://docs.safe.global/home/ai-agent-quickstarts/human-approval)). Economic case: a cap binds with p = 1 and needs no detection, unlike a bond whose deterrence is p*B (Q2, Q4).
- Verdict: exists on EVM smart accounts; Bitcoin-native (script or Lightning) agent allowance with expiry: partial (L402 and agent-budget tooling surfaced in search but not opened).

N2. Bonds from the principal's funds, slashed on adjudicated misbehavior
- Closest prior work: Polinsky and Shavell Sec. 19 (sanction h/p on a risk-neutral principal induces optimal control of agents); Adler et al. 2024 (principal suspension for harms by PHC-verified AI); AIUC agent insurance (2025-07). A bonded-agent verification protocol (arXiv 2507.00631) surfaced but was not opened.
- Verdict: partial. The liability theory exists and insurance products exist; a Bitcoin-posted principal bond for agents was not found, and the adjudication step is the unsolved part (Q3).

N3. Adjudicator-free slashing on equivocation applied to agents' signed commitments
- Closest prior work: Casper FFG slashing conditions (2017); Babylon EOTS, deployed 2025-04, related to DAPS and accountable assertions (cited as refs [38], [39] in Dong et al.).
- Verdict: mechanism exists; application to AI agents' commitments not found. Caveat: on Bitcoin today it needs a covenant committee. Queries tried: "Babylon bitcoin staking extractable one-time signature EOTS slashing double sign private key"; "Bitcoin timelocked bond sybil resistance AI agents identity fidelity bond agents"; "LLM agents program equilibrium commitment devices credible commitment arXiv 2025".

N6. Seasoned (coin-age or timelocked) bonds as sybil friction for agent swarms
- Closest prior work: JoinMarket fidelity bonds (timelocked BTC via CLTV, value grows with lock time, superlinear in amount, explicitly for sybil resistance); Peercoin coin age (2012); Xia et al. 2026 name "staked collateral" as a candidate agent-uniqueness notion.
- Verdict: exists for non-agent identities (JoinMarket makers); for AI agent swarms specifically: not found. Queries tried: "Bitcoin timelocked bond sybil resistance AI agents identity fidelity bond agents". Note the documented weakness: holders get the time cost almost free, so the "time cost fast agents cannot compress" is real for the delay but small as a price.

N7. Blockspace as a global rate limit on high-stakes AI actions
- Closest prior work: Dwork and Naor pricing via processing (1992); Laurie and Clayton's failure analysis (2004). Commentary on agents consuming blockspace surfaced (The Block 2026-09-29, not opened).
- Verdict: not found as a safety mechanism. Queries tried: "Bitcoin blockspace scarcity rate limit AI agents transactions throughput limit safety". Q7 argues the defensible form is confirmation-depth delay, not throughput.

N11. Human keys co-sign an agent's high-stakes transactions
- Closest prior work: Safe's "Human approval for AI agent actions": "an autonomous agent proposes transactions, and one or more human signers approve and execute"; recommends "a 2-out-of-3, 3-out-of-5, or 5-out-of-7 threshold", "The AI agent should be one signer", so "at least one human approval is required"; trade-off: "it can take minutes or hours to collect the necessary approvals" [vendor] ([Safe docs](https://docs.safe.global/home/ai-agent-quickstarts/human-approval)). Schelling 1956 and Babylon's covenant committee show the failure mode: a co-signer that refuses or is offline halts the system.
- Verdict: exists (EVM, vendor docs); Bitcoin-native multisig brake for agents is the same primitive and not novel.

```yaml
sources:
  - key: schelling1956
    authors: Thomas C. Schelling
    year: 1956
    title: An Essay on Bargaining
    venue: American Economic Review 46(3):281-306
    type: peer-reviewed
    id: url (journal scan hosted on a UMBC course page)
    url: https://userpages.umbc.edu/~nmiller/POLI388/BARGAINING.TCS.pdf
    supports: commitment as irreversible, visible sacrifice; bond example ($5,000 forfeit); simultaneous-commitment stalemate; bargaining agent with unchangeable instructions
  - key: bryan2010
    authors: Gharad Bryan, Dean Karlan, Scott Nelson
    year: 2010
    title: Commitment Devices
    venue: Annual Review of Economics 2:671-698
    type: peer-reviewed
    id: doi:10.1146/annurev.economics.102308.124324
    url: https://ideas.repec.org/a/anr/reveco/v2y2010p671-698.html
    supports: hard vs soft commitments; evidence on demand; device design (abstract only)
  - key: dafoe2020
    authors: Allan Dafoe, Edward Hughes, Yoram Bachrach, Tantum Collins, Kevin R. McKee, Joel Z. Leibo, Kate Larson, Thore Graepel
    year: 2020
    title: Open Problems in Cooperative AI
    venue: arXiv
    type: preprint
    id: arXiv:2012.08630
    url: https://arxiv.org/abs/2012.08630
    supports: commitment device taxonomy (soft/hard, unilateral/multilateral, conditional); smart contracts for non-human commitments; commitment enables threats
  - key: tennenholtz2004
    authors: Moshe Tennenholtz
    year: 2004
    title: Program equilibrium
    venue: Games and Economic Behavior 49(2):363-373
    type: peer-reviewed
    id: doi:10.1016/j.geb.2004.02.002
    url: https://ideas.repec.org/a/eee/gamebe/v49y2004i2p363-373.html
    supports: metadata only; content via sistla2025
  - key: sistla2025
    authors: Swadesh Sistla, Max Kleiman-Weiner
    year: 2025
    title: Evaluating LLMs in Open-Source Games
    venue: arXiv
    type: preprint
    id: arXiv:2512.00371
    url: https://arxiv.org/abs/2512.00371
    supports: definition of program equilibrium; LLMs reach approximate program equilibria with cooperative and deceptive strategies
  - key: conitzer2023
    authors: Vincent Conitzer, Caspar Oesterheld
    year: 2023
    title: Foundations of Cooperative AI
    venue: Proceedings of the AAAI Conference on Artificial Intelligence 37(13):15359-15367
    type: peer-reviewed
    id: doi:10.1609/aaai.v37i13.26791
    url: https://api.crossref.org/works/10.1609/aaai.v37i13.26791
    supports: AI agents differ from classical game-theoretic agents; research agenda (abstract)
  - key: sun2023
    authors: Xinyuan Sun, Davide Crapis, Matt Stephenson, Barnabe Monnot, Thomas Thiery, Jonathan Passerat-Palmbach
    year: 2023
    title: Cooperative AI via Decentralized Commitment Devices
    venue: arXiv (PDF footer NeurIPS 2023)
    type: preprint
    id: arXiv:2311.07815
    url: https://arxiv.org/abs/2311.07815
    supports: limits of commitment mechanisms; MEV as evidence of attacks on decentralized commitment devices
  - key: chan2025
    authors: Alan Chan, Kevin Wei, Sihao Huang, Nitarshan Rajkumar, Elija Perrier, Seth Lazar, et al.
    year: 2025
    title: Infrastructure for AI Agents
    venue: arXiv (v3 2025-06-19)
    type: preprint
    id: arXiv:2501.10114
    url: https://arxiv.org/abs/2501.10114
    supports: commitment devices for agents; unclear agent response to threats; smart contracts limited by real-world information sources; identity binding
  - key: ciliberto2026
    authors: Carlo Ciliberto, Alessandro Rudi, Enrico Tassi
    year: 2026
    title: "Proof-Carrying Contracts: Commitments AI Agents Cannot Break"
    venue: arXiv (v1 2026-10-20)
    type: preprint
    id: arXiv:2610.28484
    url: https://arxiv.org/abs/2610.28484
    supports: text cannot bind agents; proof-checked execution gate; escrow example
  - key: polinsky2005
    authors: A. Mitchell Polinsky, Steven Shavell
    year: 2005
    title: The Theory of Public Enforcement of Law
    venue: NBER Working Paper 11780 (Handbook of Law and Economics chapter)
    type: preprint
    id: doi:10.3386/w11780
    url: https://www.nber.org/papers/w11780
    supports: g > pf; f* = h/p; wealth cap and underdeterrence; maximal fines; errors (eq. 24); bribery lambda f; sanctioning principals
  - key: becker1968
    authors: Gary S. Becker
    year: 1968
    title: "Crime and Punishment: An Economic Approach"
    venue: Journal of Political Economy 76 (first page 169)
    type: peer-reviewed
    id: doi:10.1086/259394
    url: https://ideas.repec.org/a/ucp/jpolec/v76y1968p169.html
    supports: metadata only; content via polinsky2005
  - key: shavell1986
    authors: Steven Shavell
    year: 1986
    title: The judgment proof problem
    venue: International Review of Law and Economics 6(1):45-58
    type: peer-reviewed
    id: doi:10.1016/0144-8188(86)90038-9
    url: https://ideas.repec.org/a/eee/irlaec/v6y1986i1p45-58.html
    supports: metadata only (unverified content)
  - key: fortune2025aiuc
    authors: Sharon Goldman
    year: 2025
    title: "Exclusive: Who covers the damage when an AI agent goes rogue? This startup has an insurance policy for that"
    venue: Fortune
    type: news
    id: url
    url: https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/
    supports: AIUC launch 2025-07-23, $15M seed, AIUC-1 framework
  - key: buterin2017casper
    authors: Vitalik Buterin, Virgil Griffith
    year: 2017
    title: Casper the Friendly Finality Gadget
    venue: arXiv
    type: preprint
    id: arXiv:1710.09437
    url: https://arxiv.org/abs/1710.09437
    supports: slashing conditions; accountable safety (1/3 deposit); long-range revisions; inactivity leak; minority soft fork
  - key: buterin2014ws
    authors: Vitalik Buterin
    year: 2014
    title: "Proof of Stake: How I Learned to Love Weak Subjectivity"
    venue: Ethereum Foundation Blog
    type: essay/blog
    id: url
    url: https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity
    supports: nothing at stake; deposits; long-range; permanent nobility
  - key: electra_spec
    authors: Ethereum consensus-specs contributors
    year: 2025
    title: Electra beacon-chain specification
    venue: GitHub ethereum/consensus-specs
    type: standard/spec
    id: specs/electra/beacon-chain.md
    url: https://github.com/ethereum/consensus-specs/blob/master/specs/electra/beacon-chain.md
    supports: slashing penalty and whistleblower quotients 4096; max effective balance 2048 ETH; process_slashings multiplier
  - key: pectra2025
    authors: EF Protocol Support Team
    year: 2025
    title: Pectra Mainnet Announcement
    venue: Ethereum Foundation Blog
    type: official docs
    id: url
    url: https://blog.ethereum.org/2025/04/23/pectra-mainnet
    supports: Pectra activation 2025-05-07 epoch 364032
  - key: eth2book
    authors: Upgrading Ethereum (eth2book.info)
    year: undated (Bellatrix-era content, accessed 2026-11-26)
    title: "Upgrading Ethereum: Slashing"
    venue: eth2book.info
    type: official docs
    id: url
    url: https://eth2book.info/latest/part2/incentives/slashing/
    supports: slashable offences; correlation penalty min(B, 3SB/T); rationale; pre-Electra quotients
  - key: migalabs2024
    authors: MigaLabs
    year: 2024
    title: Slashed Validators Discrepancies in popular Block Explorers
    venue: MigaLabs blog
    type: essay/blog
    id: url
    url: https://migalabs.io/blog/slashed-validators-discrepancies-in-popular-block-explorers
    supports: 438 slashed validators as of 2024-09-17
  - key: cryptoslate2025
    authors: CryptoSlate
    year: 2025
    title: Ethereum slashing wipes funds of 40 validators punished for double-signing
    venue: CryptoSlate
    type: news
    id: url
    url: https://cryptoslate.com/ethereum-slashing-wipes-funds-of-40-validators-punished-for-double-signing/
    supports: 525 slashed since 2020 (MigaLabs); 15 other cases in 2025; Bitcoin Suisse 2023
  - key: cryptonomist2025
    authors: The Cryptonomist
    year: 2025
    title: "Mass slashing on Ethereum: 39 validators affected, operational link with SSV"
    venue: The Cryptonomist
    type: news
    id: url
    url: https://en.cryptonomist.ch/2025/09/11/mass-slashing-on-ethereum-39-validators-affected-operational-link-with-ssv/
    supports: 2025-09-10 event; operational cause
  - key: eigen2025
    authors: EigenLayer (Eigen Labs)
    year: 2025
    title: "Slashing Goes Live on Mainnet"
    venue: EigenCloud blog
    type: company/vendor claim
    id: url
    url: https://blog.eigencloud.xyz/slashing-goes-live/
    supports: slashing live 2025-04-17; AVS-defined conditions; Unique Stake Allocation; ecosystem counts
  - key: durvasula2024
    authors: Naveen Durvasula, Tim Roughgarden
    year: 2024
    title: Robust Restaking Networks
    venue: arXiv
    type: preprint
    id: arXiv:2407.21785
    url: https://arxiv.org/abs/2407.21785
    supports: cost (1/3 stake) vs profit; overcollateralization gamma; cascade bound (1 + 1/gamma) psi
  - key: l2beat2026
    authors: donnoh (L2BEAT)
    year: 2026
    title: "Stage 1 update: minimum challenge period reduction from 7d to 5d"
    venue: L2BEAT forum
    type: essay/blog
    id: url
    url: https://forum.l2beat.com/t/stage-1-update-minimum-challenge-period-reduction-from-7d-to-5d/425
    supports: why 7 days (6 days social response + 1 day fraud proof); Stage 1 5 days; fee bribery for censorship
  - key: landis2023
    authors: Daji Landis
    year: 2023
    title: Incentive Non-Compatibility of Optimistic Rollups
    venue: arXiv (v3 2024-10-16)
    type: preprint
    id: arXiv:2312.01549
    url: https://arxiv.org/abs/2312.01549
    supports: formal verifier's dilemma in rollups; unintended mixed equilibria
  - key: teutsch2017
    authors: Jason Teutsch, Christian Reitwiessner
    year: 2017 (paper dated 2017-11-16)
    title: A scalable verification solution for blockchains
    venue: arXiv (posted 2019-08-12)
    type: preprint
    id: arXiv:1908.04756
    url: https://arxiv.org/abs/1908.04756
    supports: verifier's dilemma; failure of plain rewards and bounties; forced errors and jackpots as Achilles' heel
  - key: buterin2015pe
    authors: Vitalik Buterin
    year: 2015
    title: The P + epsilon Attack
    venue: Ethereum Foundation Blog
    type: essay/blog
    id: url
    url: https://blog.ethereum.org/2015/01/28/p-epsilon-attack
    supports: zero-cost bribery of Schelling votes; deposits as mitigation
  - key: ast2023
    authors: Federico Ast, William George, Jamilya Kamalova, Abeer Sharma, Yann Aouidef
    year: 2023
    title: "Decentralized justice: state of the art, recurring criticisms and next-generation research topics"
    venue: Frontiers in Blockchain
    type: peer-reviewed
    id: doi:10.3389/fbloc.2023.1204090
    url: https://www.frontiersin.org/journals/blockchain/articles/10.3389/fbloc.2023.1204090/pdf
    supports: Kleros juror selection by stake; redistribution; caseload; p+epsilon resistance; identity limits
  - key: uma_docs
    authors: UMA Project
    year: accessed 2026-11-26
    title: How does UMA's Oracle work?
    venue: UMA documentation
    type: official docs
    id: url
    url: https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work
    supports: proposer/disputer bonds; DVM commit-reveal; 65% threshold; slashing of voters; cost-of-corruption argument
  - key: theblock2025
    authors: The Block
    year: 2025
    title: Polymarket says governance attack by UMA whale to hijack a bet's resolution is 'unprecedented'
    venue: The Block
    type: news
    id: url
    url: https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented
    supports: March 2025 $7M Ukraine market dispute; no refunds; $750 bond
  - key: tas2022
    authors: Ertem Nusret Tas, David Tse, Fangyu Gai, Sreeram Kannan, Mohammad Ali Maddah-Ali, Fisher Yu
    year: 2022
    title: "Bitcoin-Enhanced Proof-of-Stake Security: Possibilities and Impossibilities"
    venue: arXiv (v7 2025-02-01)
    type: preprint
    id: arXiv:2207.08392
    url: https://arxiv.org/abs/2207.08392
    supports: non-slashable long-range attacks; slashable safety needs external trust; Bitcoin checkpointing
  - key: dong2024
    authors: Xinshu Dong, Orfeas Stefanos Thyfronitis Litos, Ertem Nusret Tas, et al.
    year: 2024
    title: Bitcoin Staking
    venue: arXiv (v5 2026-05-18)
    type: preprint
    id: arXiv:2408.01896
    url: https://arxiv.org/abs/2408.01896
    supports: EOTS key extraction; 1/3-economic safety; covenant committee existential honesty; borrowed-stake attack
  - key: babylon2025
    authors: Babylon Labs
    year: 2025
    title: Phase-2 launch round up
    venue: Babylon Labs blog
    type: company/vendor claim
    id: url
    url: https://babylonlabs.io/blog/phase-2-launch-round-up---bitcoin-staking-activated-babylon-genesis-marches-towards-the-next-phase
    supports: Genesis 2025-04-10; staking pilot 2025-04-11 (1,000 BTC); permissionless 2025-04-24
  - key: budish2018
    authors: Eric Budish
    year: 2018
    title: The Economic Limits of Bitcoin and the Blockchain
    venue: NBER Working Paper 24717
    type: preprint
    id: NBER w24717
    url: https://www.nber.org/system/files/working_papers/w24717/w24717.pdf
    supports: equations (1)-(4); linear security; double-spend examples; stock vs flow; Schelling quote
  - key: gans2023
    authors: Joshua S. Gans, Hanna Halaburda
    year: 2023
    title: "\"Zero Cost\" Majority Attacks on Permissionless Blockchains"
    venue: arXiv; Management Science 70(6):4155-4165 (2024)
    type: peer-reviewed
    id: doi:10.1287/mnsc.2023.02426
    url: https://arxiv.org/abs/2308.06568
    supports: negative-cost majority attacks; need for social mechanisms
  - key: bonneau2016
    authors: Joseph Bonneau
    year: 2016
    title: "Why Buy When You Can Rent? Bribery Attacks on Bitcoin-Style Consensus"
    venue: Financial Cryptography and Data Security 2016 Workshops, LNCS 9604, pp. 19-26
    type: peer-reviewed
    id: doi:10.1007/978-3-662-53357-4_2
    url: https://api.crossref.org/works/10.1007/978-3-662-53357-4_2
    supports: metadata only (unverified content)
  - key: buterin2019collusion
    authors: Vitalik Buterin
    year: 2019
    title: On Collusion
    venue: vitalik.eth.limo
    type: essay/blog
    id: url
    url: https://vitalik.eth.limo/general/2019/04/03/collusion.html
    supports: coalition deviation; renting coins for votes; identity that cannot be rented; deposits
  - key: douceur2002
    authors: John R. Douceur
    year: 2002
    title: The Sybil Attack
    venue: IPTPS 2002 (per file name and metadata)
    type: peer-reviewed
    id: url
    url: https://www.microsoft.com/en-us/research/wp-content/uploads/2002/01/IPTPS2002.pdf
    supports: impossibility without central authority; Lemmas 1, 2, 4; temporal vs storage resources
  - key: borge2017
    authors: Maria Borge, Eleftherios Kokoris-Kogias, Philipp Jovanovic, Linus Gasser, Nicolas Gailly, Bryan Ford
    year: 2017
    title: "Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies"
    venue: IEEE EuroS&P Workshops 2017
    type: peer-reviewed
    id: doi:10.1109/EuroSPW.2017.46
    url: https://infoscience.epfl.ch/record/301744/files/pop.pdf
    supports: PoP definition; PoS monopoly critique
  - key: ford2020
    authors: Bryan Ford
    year: 2020
    title: "Identity and Personhood in Digital Democracy: Evaluating Inclusion, Equality, Security, and Privacy in Pseudonym Parties and Other Proofs of Personhood"
    venue: arXiv
    type: preprint
    id: arXiv:2011.02412
    url: https://arxiv.org/abs/2011.02412
    supports: pseudonym parties; PoW and PoS as one dollar one vote
  - key: siddarth2020
    authors: Divya Siddarth, Sergey Ivliev, Santiago Siri, Paula Berman
    year: 2020
    title: "Who Watches the Watchmen? A Review of Subjective Approaches for Sybil-resistance in Proof of Personhood Protocols"
    venue: arXiv
    type: preprint
    id: arXiv:2008.05300
    url: https://arxiv.org/abs/2008.05300
    supports: plutocracy of resource-based membership; Idena FLIP accuracy; BrightID/Idena review
  - key: adler2024
    authors: Steven Adler, Zoe Hitzig, Shrey Jain, et al. (32 authors)
    year: 2024
    title: "Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online"
    venue: arXiv (v4 2025-01-17)
    type: preprint
    id: arXiv:2408.07892
    url: https://arxiv.org/abs/2408.07892
    supports: credential limits; unlinkable pseudonymity; verified delegation to AI agents; principal suspension
  - key: biometricupdate2025
    authors: Joel R. McConvey
    year: 2025
    title: World Network reaches 10 million 'verified humans' amid continued legal blocks
    venue: Biometric Update
    type: news
    id: url
    url: https://www.biometricupdate.com/202501/world-network-reaches-10-million-verified-humans-amid-continued-legal-blocks
    supports: 10M verified (vendor); Chile Supreme Court ruling
  - key: decrypt2026
    authors: Decrypt
    year: 2026
    title: World upgrade article (Zoom, Tinder, human verification)
    venue: Decrypt
    type: news
    id: url
    url: https://decrypt.co/364774/sam-altman-world-zoom-tinder-better-verify-humans-ai-age
    supports: 18M verified across 160 countries (vendor); Okta Human Principal
  - key: idtechwire2025
    authors: Ali Nassar-Smith
    year: 2025
    title: Thailand Orders Worldcoin to Halt Iris Scans and Delete Biometric Data
    venue: ID Tech (IDTechWire)
    type: news
    id: url
    url: https://idtechwire.com/thailand-orders-worldcoin-to-halt-iris-scans-and-delete-biometric-data/
    supports: Thailand PDPC order; ~1.2M scanned; Germany deletion order (Dec 2024); Philippines ban (Oct 2025)
  - key: humantech2025
    authors: Kyle (Passport XYZ co-founder)
    year: 2025
    title: "From Gitcoin Passport to Human Passport: We're Now Part of human.tech"
    venue: human.tech blog
    type: company/vendor claim
    id: url
    url: https://human.tech/blog/from-gitcoin-passport-to-human-passport-we-re-now-part-of-human-tech
    supports: acquisition 2025-02-10; 2M users, 35M credentials (vendor)
  - key: king2012
    authors: Sunny King, Scott Nadal
    year: 2012
    title: "PPCoin: Peer-to-Peer Crypto-Currency with Proof-of-Stake"
    venue: self-published whitepaper
    type: company/vendor claim
    id: url
    url: https://bitcoin.peryaudo.org/vendor/peercoin-paper.pdf
    supports: coin age definition; main chain by consumed coin age; central checkpoints
  - key: joinmarket_fb
    authors: JoinMarket developers
    year: accessed 2026-11-26
    title: Fidelity bonds
    venue: joinmarket-clientserver docs
    type: code
    id: docs/fidelity-bonds.md
    url: https://github.com/JoinMarket-Org/joinmarket-clientserver/blob/master/docs/fidelity-bonds.md
    supports: timelocked BTC bonds for sybil resistance; value formula; exponent 1.3; near-free for holders
  - key: spence1973
    authors: Michael Spence
    year: 1973
    title: Job Market Signaling
    venue: Quarterly Journal of Economics 87(3):355-374
    type: peer-reviewed
    id: doi:10.2307/1882010
    url: https://www.sfu.ca/~allen/Spence.pdf
    supports: signal separates only if cost negatively correlated with productivity
  - key: zahavi1975
    authors: Amotz Zahavi
    year: 1975
    title: "Mate selection: a selection for a handicap"
    venue: Journal of Theoretical Biology
    type: peer-reviewed
    id: doi:10.1016/0022-5193(75)90111-3
    url: https://pubmed.ncbi.nlm.nih.gov/1195756/
    supports: metadata only (unverified content)
  - key: xia2026
    authors: Yunfeng Xia, Chao Li, Lei Li, Chenhao Zhang, Li Duan, Runhua Xu, Wei Wang
    year: 2026
    title: "Toward Web 4.0: Bidirectional Trust between AI Agents and Blockchain"
    venue: arXiv
    type: preprint
    id: arXiv:2605.08922
    url: https://arxiv.org/abs/2605.08922
    supports: PoP does not transfer to agents; staked collateral as candidate; no standard gives sybil-resistant agent identity
  - key: fish2024
    authors: Sara Fish, Yannai A. Gonczarowski, Ran Shorrer
    year: 2024
    title: Algorithmic Collusion by Large Language Models
    venue: arXiv (v6 2026-08-31)
    type: preprint
    id: arXiv:2404.00806
    url: https://arxiv.org/abs/2404.00806
    supports: LLM pricing agents reach supracompetitive prices; prompt sensitivity
  - key: motwani2024
    authors: Sumeet Ramesh Motwani, Mikhail Baranchuk, Martin Strohmeier, Vijay Bolina, Philip H.S. Torr, Lewis Hammond, Christian Schroeder de Witt
    year: 2024
    title: "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography"
    venue: arXiv (v5 2025-07-25)
    type: preprint
    id: arXiv:2402.07510
    url: https://arxiv.org/abs/2402.07510
    supports: steganographic collusion; limits of monitoring and paraphrasing
  - key: dwork1992
    authors: Cynthia Dwork, Moni Naor
    year: 1992
    title: Pricing via Processing or Combatting Junk Mail
    venue: CRYPTO '92 (preliminary version, per the paper)
    type: peer-reviewed
    id: url
    url: https://www.wisdom.weizmann.ac.il/~naor/PAPERS/pvp.pdf
    supports: moderately hard functions for access control; restrain not prohibit; shortcut for privileged bulk access
  - key: laurie2004
    authors: Ben Laurie, Richard Clayton
    year: 2004
    title: "\"Proof-of-Work\" Proves Not to Work"
    venue: workshop paper dated 2004-05-03 (Cambridge Computer Laboratory copy)
    type: peer-reviewed
    id: url
    url: https://www.cl.cam.ac.uk/~rnc1/proofwork.pdf
    supports: cost-throttle economics; botnet resources; overlap of legitimate and abusive volumes
  - key: bip141
    authors: Eric Lombrozo, Johnson Lau, Pieter Wuille
    year: 2015 (assigned 2015-12-21)
    title: "BIP 141: Segregated Witness (Consensus layer)"
    venue: Bitcoin Improvement Proposals
    type: standard/spec
    id: BIP-0141
    url: https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
    supports: block weight <= 4,000,000
  - key: marino2025
    authors: Bill Marino, Ari Juels
    year: 2025
    title: Giving AI Agents Access to Cryptocurrency and Smart Contracts Creates New Vectors of AI Harm
    venue: arXiv (v3 2026-08-26)
    type: preprint
    id: arXiv:2507.08249
    url: https://arxiv.org/abs/2507.08249
    supports: sovereignty, immutability, pseudonymity, trustless transactions as harm vectors; irreversibility of agent errors
  - key: safe_docs
    authors: Safe
    year: accessed 2026-11-26
    title: Human approval for AI agent actions
    venue: Safe developer docs
    type: official docs
    id: url
    url: https://docs.safe.global/home/ai-agent-quickstarts/human-approval
    supports: agent as one signer, human co-sign threshold, latency trade-off (N11)
  - key: coinbase_spend
    authors: Coinbase Developer Platform
    year: accessed 2026-11-26
    title: Spend Permissions (onchain contracts reference)
    venue: Coinbase developer docs
    type: official docs
    id: url
    url: https://docs.cdp.coinbase.com/coinbase-wallet/reference/onchain-contracts/spend-permissions.md
    supports: allowance per period with start/end expiry (N1)
```
