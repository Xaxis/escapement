---
title: "Escapement: A Bitcoin Track Record for AI Agents, and What Broke It"
author:
  - name: "Xaxis"
    affiliation: [1]
    corresponding: true
affiliation:
  - id: 1
    name: "Independent researcher"
abstract: "Bounding what an AI agent can do is not enough; the harder questions are what agents are rewarded for and why anyone would adopt the means of checking them. This paper asks what Bitcoin can contribute to both. It designs Escapement, in which an agent's standing is computed in part from a track record of its commitments, kept on Bitcoin under an identity backed by locked coins, with rate limits, vetoes and leases built from today's script. Every claimed contribution was then checked at six levels: two prior-art searches, proofs, a regtest build of 104 checks with simulations, a red team, editorial review and a fresh reviewer. None survived as new. The bound on faking a record of forecasts is prior work, holds only for fakers that use public information alone and cannot move outcomes, and rewards bets rather than calibrated forecasts and capability rather than alignment. Nothing on chain yet binds a record to its identity's bond, so one bond can back many records. A training reward that the lab cannot select was not achieved. Adoption tips only in a toy model with unmeasured parameters, routing around the record was not made costly, and the lease is Substrate's mortal transactions. One part extends prior work narrowly: a covenant-free chain of outputs that rate-limits an agent's releases and lets any guardian veto them, though one guardian can end an identity and the guardians together can write its record. Nothing has been deployed or tested against a real adversary. The paper's value is in what broke, and why."
lang: "en-GB"
bibliography: references.bib
csl: style.csl
link-citations: true
figPrefix: [Figure, Figures]
tblPrefix: [Table, Tables]
eqnPrefix: [Equation, Equations]
secPrefix: [Section, Sections]
---

# Introduction {#sec:intro}

Most proposals to use Bitcoin for AI safety are proposals to cap an agent: a wallet with a limit, a delay before large payments, a bond forfeited on misbehaviour. Caps are useful and old, and they share a weakness. They act after the fact, on an agent whose goals they do not touch, and they bind only where someone imposes them. This paper started from two harder questions. Can Bitcoin's properties help shape what AI agents are trained and rewarded to do, rather than only fence them in? And would the parties who matter (labs, firms, relying parties, insurers and governments) choose to use it because it pays or protects them?

It is a design study, and its result is mostly negative. Nothing in it has been deployed or tested against a real adversary. A design was proposed, every claim was put through six levels of checking, and whatever failed a level was cut or downgraded rather than argued back. Little survived, and what broke is the more useful half.

Bitcoin offers four things that are hard to fake: coins no one can issue; a block order that grows costly to rewrite with depth and that only a hashrate majority could rewrite at will; the single spending of each output; and a clock that runs faster only with more hashrate. Section 2 states exactly what Bitcoin's rules enforce and what they do not.

## The proposal

Escapement computes an agent's standing in part from its **record**: an ordered sequence, hard to backdate beyond a depth chosen for one's risk, of the commitments it put on chain (forecasts, promises with stakes, requests for consequential actions), which relying parties that follow its rules require for anything they rely on. It is committed on Bitcoin under an identity backed by locked bitcoin (section 3), it is complete only for a verifier that walks the whole chain, and its guardians together can write entries the agent never made (section 8). It hoped for three consequences: that faking a record would cost identities in proportion to its score (section 4), that a lab could train on rewards nobody could select after the fact (section 5), and that adoption would pay each party that joined (section 6). Section 7 asks why Bitcoin rather than a registry or a witnessed log, and section 8 describes the enforcement layer: a chain of outputs per identity that rate-limits the release of an agent's commitments and lets any guardian veto it, and a lease that lapses in block height.

## What survived

No mechanism or theorem in this paper is new. Section 9 gives each claim's result at every level, and section 11 credits the prior work.

- **Extends prior work, narrowly:** the tick chain, a covenant-free version of Somsen's spacechains with Revault's cancel, whose properties hold per pinned chain, not per identity.
- **Prior work, applied:** the fake-record bound (Ville's inequality, a union bound and testing by betting), now stated with the conditions it needs; two-sided adoption with seed readers (critical mass), as a toy model; the height-difference lease (Substrate's mortal transactions); the cost of running Bitcoin's clock fast; blockspace as a ceiling on the design; and the building blocks of section 8.
- **Cut:** one record serving as standing, training reward and release gate, since nothing binds a chain to its bond and the two uses ask for different reports; a training reward the lab cannot select; routing around the record becoming costly; a light proof of releases; Bitcoin headers as a licence clock for AI chips.

What broke is the paper's main contribution, and section 9 lists it: claims that move together, and hidden tail risk, defeat a product of likelihood ratios; the round rule that repairs it rewards bets rather than forecasts; a record of edge routes trust to capability, not alignment; a reward on outcomes the agent can move pays for manipulation; a simulation that barred harmful actors from joining hid that they cycle identities; transaction-id proofs pass a release no guardian signed; and neither a chain's pin nor an agent's fee bid at a veto's edge is bounded by anything on chain. Section 10 says who benefits and who could abuse the design, section 12 what it does not do and what would show it wrong, and section 13 concludes.

# What Bitcoin enforces, and what it does not

Bitcoin's rules are enforced by every node that validates blocks, which is what makes them hard for any single party, including an agent's operator, to lift. But they are few. This section sets out exactly what they cover, because the record and every mechanism under it inherit their limits. Four units recur: a **sat** is one hundred-millionth of a bitcoin; a **vB** (virtual byte) is the unit in which a transaction's size, and so its fee, is measured; a **WU** (weight unit) is a quarter of a vB; and **EH/s** is 10\^18 hashes a second, the unit of mining power.

## Four things an agent cannot fake

**Sats.** The issuance schedule is fixed by consensus [@nakamoto2008]. An agent cannot create bitcoin. It can earn, borrow, be given or steal it, and nothing in Bitcoin distinguishes coins an agent acquired honestly from coins it did not. Scarcity therefore bounds an agent only through the coins someone chooses to hand it.

**Block time.** Blocks are found by a Poisson process, on average about 600 s apart [@nakamoto2008], and difficulty is retargeted every 2,016 blocks to hold that pace [@bip54]. Producing blocks faster requires more hashrate, and the network ran at about 1,052 EH/s when measured on 26 November 2026 [@mempool-hashrate]. Thinking faster does not help. A delay counted in blocks is therefore a delay no amount of cognition can shorten, though capital can, at a cost section 8 computes.

**Keys.** Bitcoin's Taproot signatures are Schnorr signatures over secp256k1 [@bip340]. A signature cannot be produced without its key. Keys can be stolen, and the humans who hold them can be persuaded or deceived, but a signature cannot be forged.

**A public record.** Each block commits to its predecessor and to its transactions under proof of work. Rewriting a buried transaction means outmining the honest chain from that point [@nakamoto2008], which grows less likely with depth for any miner below a majority and is always possible for a majority. Commitments placed in the chain inherit this: a hash in a block deep enough for one's tolerance of risk cannot be quietly replaced. Linked timestamping, the idea underneath, predates Bitcoin by nearly two decades [@haber1991how].

## What script can and cannot say

Script, Bitcoin's spending-condition language, checks keys, hashes and timelocks. Since Taproot it can hide alternative spending paths in a Merkle tree and reveal only the one used [@bip341; @bip342], and multi-party keys can be aggregated with MuSig2 [@bip327] or split into threshold shares with FROST [@komlo2021frost]. That is enough to write "the agent's key and a human's key", "any two of three", "the human alone after a year" and "nobody before block h".

Script cannot do four things this paper needs, and the design must work around each.

1. **It cannot make a spend expire.** Timelocks are lower bounds only: absolute with `OP_CHECKLOCKTIMEVERIFY` [@bip65] and relative to an output's confirmation with `OP_CHECKSEQUENCEVERIFY` [@bip112; @bip68]. There is no "not after", by design, so that a valid transaction does not become invalid in a reorganisation. The standard workaround is a competing path that becomes valid later, as in Lightning's timeouts or Liana's recovery keys [@liana-readme]. An agent's authority cannot be made to lapse in script; it can only be outraced.
1. **It cannot read amounts or destinations.** Script cannot check how much is spent, to whom, or how much has been spent before. Spending limits, velocity limits and destination allowlists are therefore policies of a co-signer who refuses to sign, not rules of consensus. Carriere's draft for co-signer policies states the right discipline: whatever script can enforce must be enforced there, and the co-signer's policy defines only what script cannot [@optech-2026-11-06].
1. **It has no covenants.** Opcodes that would let an output restrict the transaction spending it, such as `OP_CHECKTEMPLATEVERIFY` [@bip119] or `OP_CHECKSIGFROMSTACK` [@bip348], are drafts; `OP_VAULT`, which would have made a spend wait out a delay during which a recovery path could still claim the coins, is closed [@bip345]. None is active, and an open letter in 2025 asking Bitcoin Core contributors to prioritise two of them [@optech-2025-07-04] has not led to a scheduled activation. Destination restrictions today need pre-signed transactions or co-signers, as Revault's vault design does [@revault-tx].
1. **It cannot see off chain.** Script binds bitcoin and nothing else. An API call, a code deployment, a message or a cloud purchase is outside its reach entirely.

## Bitcoin's practical limits

**Throughput and fees.** A block holds at most 4,000,000 WU (weight units) [@bip141], so the chain holds about 144,000,000 vB a day. Space is sold by auction: the median fee rate was 1 sat/vB in 2026 up to late November and 15 sat/vB across 2023, and the median in the halving block was 200 sat/vB [@mempool-feerates; @mempool-block840000]. Any mechanism that needs a transaction to confirm by a deadline is exposed to a fee spike.

**Mining concentration.** The largest pool mined 27.8% of blocks over the trailing year and the two largest 46.1% together [@mempool-pools]. Pools have left sanctioned transactions out of blocks [@b10c-ofac]. Finality and censorship resistance are only as good as the pools' independence, which section 8 quantifies.

**A known flaw in the clock.** The timewarp bug lets a majority of hashrate manipulate timestamps so that difficulty falls and blocks arrive far faster than ten minutes, after weeks of visible setup [@optech-timewarp]. Its fix, part of BIP-54, is specified and not active [@bip54].

**Privacy.** Everything on chain is public. A bond reveals its owner's coins, and a stream of commitments reveals an operator's activity. Taproot hides unused spending paths [@bip341], but amounts and timing stay visible.

**Custody.** Every key is a target. The weakest component of any scheme in this paper is the custody of the keys it depends on.

## What this means for AI

Put together, Bitcoin offers three hard guarantees and one soft one. Coins locked in script cannot move without the keys and the waits the script names, whatever the agent, its operator or the lab's control plane does. A wait counted in blocks cannot be shortened except by buying hashrate. A commitment in a buried block cannot be replaced by anyone below a hashrate majority, and an output can be spent only once, so a chain of outputs has one history. And, softly, anyone who chooses to check can verify that a given transaction is in the chain from block headers and inclusion proofs, without trusting a server; showing that nothing newer exists needs full blocks (section 8). The record of section 3 is built from the last two hard guarantees: one history gives completeness, and height gives order. The enforcement layer of section 8 is built from the first two. Both inherit the gaps: no expiry, no view of amounts or destinations, no reach off chain, and no protection against an agent that simply acquires coins of its own.

# The record

The rest of the paper argues about an agent's record, so this section states exactly what it is and what each of its rules is for.

## Identity, entries and leaves

An **identity** is a bond and a tick chain. The bond is a Taproot output holding at least the reference 200,000 sats, spendable by the principal only after an absolute timelock [@bip65]. Its internal key is a point with no known secret, tweaked by a hash of one charter identifier. Because the key names the charter, one output backs one identity: the same coins cannot back a thousand identities. The **tick chain** (section 8) is a sequence of outputs T\_0, T\_1, ..., each spent by the next, pinned by the outpoint of T\_0 that the charter names. Output T\_n commits, through a tweak of its internal key, to one root: the root of a Merkle-sum tree whose leaves are the commitments the identity made in entry n. There are three kinds of leaf. A **claim** is a forecast on a stated event with a stated resolution source. A **promise** is a statement with a stake in sats, a deadline height and an adjudicator. A **request** is an action of Tier 2 or Tier 3 that the identity asks a relying party to carry out. Each leaf states in clear its kind and the height at which it resolves; the tree's internal nodes carry the sum of their leaves' stakes and the count of leaves beneath them.

Actions sit on a ladder of **tiers**, which the charter assigns by class of action. Tier 1 actions are paid from an allowance and need nothing more. A Tier 2 action is released 6 blocks (about an hour) after its batch is committed, unless any guardian vetoes it first. A Tier 3 action waits 144 blocks (about a day) and needs every guardian's signature as well as the agent's. The agent labels each request with its tier and the relying party checks the label against the charter; nothing stops an agent from splitting an action into pieces below a tier's threshold, or across identities (section 12).

@tbl:roles names the parties and the one document that recur through the paper.

| Role | Who | What it decides |
| :--- | :--- | :--- |
| Principal | the human or organisation answerable for the agent | the charter; posts the bond |
| Agent | the AI system, holding its own key | what it commits to, and when |
| Guardian | an independent key holder named in the charter | vetoes releases; signs Tier 3 releases and lease renewals |
| Relying party | anyone who acts on the agent's word | whether to deal, and on what terms |
| Scorer | whoever computes standing for a relying party | the formula, from the record |
| Baseline provider | a party independent of agent and scorer | the reference forecast for each listed event |
| Resolver, adjudicator | parties named per claim or promise | an event's outcome; whether a promise was kept |
| Charter | a document the principal signs | keys, guardians, tiers, caps, the scorer's terms |

: The parties to an identity and what each decides. {#tbl:roles}

## Five rules for scoring

A relying party or a scorer turns the chain into standing with five rules, each of which closes a hole that the analysis in section 4, or the red team, found.

1. **Credit only what was exposed in advance.** A commitment earns credit only if it is a leaf of an entry confirmed at least d blocks below the height at which it resolved, and that height is fixed by the resolver signing the outcome together with a block hash. Without this rule, an identity keeps its hits and drops its misses, or backdates through a short reorganisation.
1. **Silence scores as failure.** A leaf past its resolution height and not disclosed, to the public or to a scorer the relying party trusts, scores as the worst outcome at once: its likelihood ratio is taken to be zero, so it contributes nothing to its round's mean (rule 4) and costs the round its weight. An entry whose leaves are withheld scores as if every leaf, up to the largest number the charter allows, had a ratio of zero. Without this rule, an identity hides its losses. Scoring silence as the worst outcome is already practice in a forecasting network [@infinite-games]. Two relying parties that trust different scorers may see different disclosures and so compute different scores from the same chain.
1. **One forecast per event.** The scorer keeps only the first forecast an identity makes on an event. Two forecasts on one event let an identity inflate its expected score (section 4 gives the counterexample).
1. **Score in rounds, against a baseline.** Forecasts are scored relative to a baseline, published by a party independent of the agent and of the scorer, on events from a list the agent did not write. Claims are scored in rounds that do not overlap, and a round counts as the weighted mean of its claims' likelihood ratios. Without the baseline, volume looks like skill; without the rounds, claims chosen to move together fake a record (section 4).
1. **Score from genesis.** A score runs over the whole chain, never over a window chosen after the fact.

## The properties Bitcoin supplies

Four properties make the record what it claims to be. Each rests on Bitcoin's rules together with one rule that relying parties apply off chain: which T\_0 is the identity's.

- **Non-backdatable.** An entry's height is the height of the block that confirms it. No signer can make it earlier, though a reorganisation can move it; hence the margin of d blocks in rule 1.
- **Non-forkable, per pinned chain.** An outpoint can be spent once, so for each index n there is one T\_n in the pinned chain, and a tweak commits it to one root. But nothing on chain yet ties a chain to its identity's bond. T\_0's key commits the charter identifier, so a charter that also named T\_0's outpoint would be circular, and the lab handed the pin to the verifier. On regtest one charter identifier carried two chains with different roots at entry 1, each accepted from its own pin [@escapement-lab]. Two parties holding different pins can therefore be shown different histories, and one bond can back many chains. A binding is proposed and not built: the identity is the bond's outpoint, and T\_0 is a named output of the bond's own transaction.
- **Gapless.** The index rises by one with each link, and the chain from the pinned T\_0 is unique, so anyone who walks it can count an identity's entries. A root that commits the number of its leaves cannot be opened to fewer. A verifier without full blocks can confirm that entries exist, not that it has seen the newest.
- **Costly to multiply, once the binding exists.** Each further identity needs its own bond, held for its own term: about 13,000 sats a year at the reference parameters. Nothing in the rules requires a year; a bond locked only for the 28 days season costs about 4,100 sats. This is costly only in the sense the bound of section 4 uses, and only per bond once each bond backs one chain.

Propositions 3 and 4 of the formal statements, published with the paper as supplementary material [@escapement-formal], prove the second and third for a pinned chain under standard assumptions (an honest best chain and collision-resistant hashing); the first is the definition of confirmation. What these properties do not give is just as important. A commitment never put in the chain is outside the record and earns nothing; an identity may make claims elsewhere, but they do not build standing. The record holds what an identity chose to expose to being wrong, and standing is built from nothing else. And the record belongs to a key, not to a model: it can be sold with its key, and tying it to a particular model needs an attestation that returns trust to the lab or to a hardware vendor.

## What standing is

Standing is whatever a relying party computes from the record: a score for forecasts, a count and value of promises kept and broken, the identity's age and the size of its bond. Escapement does not fix one formula, because relying parties differ in what they care about, and a single official score would be a single point of capture (section 10). What the design fixes is that every such formula is computed from the same ordered, public sequence of commitments, so that two relying parties who use the same formula, the same pin and the same scorer's disclosures reach the same answer. For an agent that does not forecast on listed events, which is most deployed agents, standing reduces to the identity's age, its bond and a count of breaches: bonded reputation with a timestamp.

# What a record can prove

A record is worth having only if a good one is cheap to earn with real skill and expensive to fake. This section shows that a complete record has that property for forecasts, under a condition on the baseline stated below, and that it adds less to the older logic of bonds and reputation for promises than one might hope. Neither argument assumes that the agent values honesty. Both assume only that it prefers more standing and more sats to fewer. Omohundro argues that most goals give an agent a reason to acquire resources [@omohundro2008], and Turner and colleagues prove that, for optimal policies in environments with certain symmetries, most reward functions make it optimal to keep options open [@turner2019optimal]. The same argument says an agent values not being stopped, so escaping its guardians may be worth more to it than any stake.

## Faking a record of forecasts

An identity's forecasts are scored in rounds that do not overlap: a round's claims are committed in one entry, the round settles when the last of them resolves, and the next round's claims count only if their entry comes after that. Each claim has a forecast q, a weight w committed with it (a round's weights sum to one) and a baseline b published by an independent party. When the round settles, the identity's score is multiplied by the weighted mean of the claims' likelihood ratios, the sum of w·q(y)/b(y) over its claims, where y is each claim's outcome.

The condition the bound needs, **H0**, constrains the baseline and the agent together. Each baseline is the law of its outcome given everything public when the round opens, including the forecasts other identities have disclosed; the agent's forecasts and weights use only that public information; and its actions do not move the outcomes. The first part is an efficient-market assumption about the baseline that no relying party can check. The second is what it means to have no edge. The third the scheme cannot check either. An earlier draft of this paper called H0 a property of the baseline alone, which was wrong.

**Theorem 1.** Under H0, for any strategy that uses only what is public when each round opens and does not move outcomes (adaptive, coordinated with other identities, or built on claims that move together), the probability that an identity's score ever reaches λ is at most 1/λ. An adversary with K identities gets at least one score of λ or more with probability at most K/λ, so a success probability of π needs at least πλ identities and costs at least πλ times the cost of one identity.

The proof is short. Given the past, each claim's ratio has expectation one under its baseline, so a weighted mean of them does too, by linearity of expectation, whatever the joint law of the outcomes; in the language of testing by betting, a mean of e-values is an e-value under any dependence [@vovk2021values]. The score is therefore a nonnegative martingale over rounds starting at one, and Ville's inequality bounds the chance that such a process ever reaches λ by 1/λ [@ville1939; @shafer2019gametheoretic]. A union bound over identities gives K/λ. The bound is tight: the old fraud of sending opposite predictions to 2\^m recipients, so that one of them sees m correct calls, meets it with certainty.

None of this is new. A round's factor is the return on a unit stake split across bets at the baseline's odds, which is Shafer's testing by betting [@shafer2021testing]; the bound is Ville's inequality and a union bound; comparing an expert with a second forecaster by likelihood is Al-Najjar and Weinstein's comparative test [@alnajjar2008comparative], made sequential and anytime-valid by Choe and Ramdas [@choe2021comparing]; and pricing the lucky accounts of a many-identity attack with stakes is how Numerai answered it [@craib2021numerai]. What this section adds is the application to a Bitcoin record.

## Why rounds and means

The first version of this design multiplied every claim's ratio, and read H0 as "the agent has no edge". The red team broke it. A marginal baseline, such as a market price for each claim on its own, is not the conditional law of an outcome once the agent chooses claims that move together. With claims that mostly follow one common coin, 16 identities each betting one side of every claim reached a score of 2\^10 in 99.8% of simulated trials, against Theorem 1's bound of 1.6%. And a single identity that made 1,000 claims of "no failure" on sub-events that all fail together in one event of probability 1% scored about 23,000, 99% of the time.

That second attack is the objection Foster and Young raised against track records in finance: a manager without skill can buy a good-looking record by taking hidden tail risk, so return histories cannot separate the skilled from the unskilled [@foster2010gaming]. The product rule did not escape it. The round rule does, for forecasts: the same correlated attack succeeded in 1.1% of trials, inside the bound, and the tail-risk record scored 1.01. It does so without anyone having to decide which claims are correlated, which is what the alternative, one claim per cluster of related events, would need.

The repair has a cost the red team did not see. With more than one claim in a round the round rule is a betting score, not a proper score: the report that grows it fastest is not the truth. With ten independent claims of true probability 0.60 against a baseline of 0.50, a truthful report grows the score 0.037 nats a round, and a report of 0.999 on each grows it 0.143 nats (Proposition 7b of the formal statements). An identity that wants standing bets; it does not forecast. Its reports cannot be read as probabilities unless each round holds one claim, which is proper but slow, or each leaf carries a forecast and a separate stake.

The price is speed. An identity that knows each event's probability when the best public forecast is one half (private knowledge, which is what edge means here), with a mean edge of 0.12 nats a claim, reaches a score of 2\^20 in a median of 116 claims made one a round, or 74 rounds of 10 claims, with one identity. That is the most favourable case: an agent that knows each event's probability against a public forecast that knows nothing. With a smaller edge, 0.60 against a baseline of 0.55, a truthful identity needs about 2,722 rounds of one claim, or 1,449 rounds of ten. Rounds are serial for one identity and each lasts until its slowest claim resolves, so with daily events that is years. Rounds, not claims, are the unit of time a record takes to build.

## The numbers

At the reference cost of 13,000 sats an identity (the return forgone on the bond for a year at 5%/yr, plus two transactions' fees), an all-correct record of 20 claims in one-claim rounds against a baseline of one half has a score of about 1,000,000, and faking it with even odds needs 520,000 identities and about 70 BTC. That price assumes a one-year bond. With bonds locked only for the season the same fake costs about 21 BTC, and either price assumes one chain per bond, which section 3 shows is not yet enforced. A simulated faker running 256 identities reached a score of 2\^10 in 22.9% of trials, under the bound of 25.0%; that run checks the arithmetic of one strategy and adds no evidence beyond the theorem.

## What breaks the bound

Each rule of section 3 is needed, and so is H0.

- **Private information or influence.** An agent that knows more than the public, or can move an outcome, is outside the theorem. An agent that can make an outcome equal its forecast multiplies its score by 1/b each round, so influence over outcomes breaks standing exactly as it breaks training (section 5).
- **Copying.** If the baseline ignores forecasts other identities have disclosed, an identity that copies a skilled one shows edge it does not have. A baseline with a known public bias does the same for anyone who corrects it.
- **One bond, many chains.** Until a chain is bound to its bond, one bond can back many chains, and the price per identity does not hold (section 3).
- **Dropping misses.** If misses can be dropped after the fact, the product over the kept claims is not a martingale; in simulation one identity reached 2\^10 by showing only its hits after about 20 claims.
- **Two forecasts on one event.** With a baseline of one half and two forecasts that both put probability one on the same outcome, the expected product is two.
- **A bad baseline.** A stale baseline, one in a thin market the agent can move, one the agent or the scorer chose, or one on events the agent wrote itself all make apparent edge cheap. A market baseline counts only with a stated depth and averaging window, and the bound then holds only up to the cost of moving the market. The event list, the baseline and the resolvers are therefore run by parties that relying parties have to trust, which section 7 returns to.
- **Too many identities.** Among a million identities without edge, one may reach a score of a million by luck. A score means something only when λ exceeds the number of identities in use, and relying parties cannot observe that number, since an operator's identities are unlinked by design.
- **A sold record.** A record stays with its keys, and keys can be sold.

## What a record of forecasts separates

Signalling sorts types only when the signal costs bad types more than good ones [@spence1973job]. A bond fails that test: sats cost every principal the same, so a bond says that someone with money stands behind an agent and nothing about the agent. A complete record passes it for one trait, **edge over the stated baseline**: the identity with edge produces its record as a by-product of forecasting, at the cost of one identity, while the identity without edge must buy the same record with a number of identities that grows in proportion to the score. It does not separate honesty. A forecaster without edge earns nothing by being honest, and an honest one with no edge looks the same as a dishonest one with none. The bond's job is only to make identities cost something; the record does the sorting, on the one trait it can see.

That trait is the wrong one for safety. Edge is a product of capability, which a misaligned agent has as much as an aligned one, and standing brings access. A record of forecasting edge therefore routes trust fastest to the most capable agents, whatever their goals. It measures what an agent can do, not what it wants.

## Promises

For promises the logic is older and the record's contribution is narrower still. If the adjudicator finds a breach with probability a (its accuracy), and a breach it finds forfeits a stake s and, with probability p, costs the standing V that future partners would otherwise extend, then keeping a promise worth G to break is a best response whenever G is at most a(s + pV). This is the reputation argument: Klein and Leffler's condition that a firm which breaks faith loses a stream of future rents larger than its gain, and Shapiro's price premium that repays an investment in reputation [@klein1981role; @shapiro1983premiums]. A complete record makes p equal to one for every partner who checks, provided adjudicators publish their verdicts on chains of their own. A bond is an entry fee of the kind Friedman and Resnick discuss for cheap pseudonyms and set aside, because it excludes some players, in favour of free but unreplaceable pseudonyms [@friedman2001social].

Who holds a promise's stake is not specified here. The identity bond can be spent only by the principal after its timelock, so it cannot be forfeited; a forfeitable stake needs a separate coverage bond with an adjudicator's spending path (section 8), whose custody and payout this paper leaves open.

Two limits keep this modest. First, a record of kept promises can be faked by wash trading: an agent makes promises to its own sybil counterparties, judged by a sybil adjudicator, keeps them all, and pays only fees. So promise history counts only against an agent, as a record of breaches, never for it, and V grows only through forecasting edge and age. Second, the condition holds promise by promise, for promises whose gain G the enforcement layer caps. Near the end of an identity's life its standing is worth little and the last promises need a stake that covers the whole gain on its own: the exit scam, which has already been modelled for AI agents that can abandon identities [@gatta2026tempting]. A gain larger than stake plus standing is not deterred, which is the judgment-proof problem [@shavell1986judgment]; for catastrophic harms we see no feasible bond that would solve it. And an agent whose aims are not monetary is not deterred by money. The caps and delays of section 8 are what Escapement relies on there.

# Training on the record

The first half of the alignment question is what an agent does once deployed; the second is what it is trained to want. Reinforcement learning shapes a model by its rewards, and two failures of rewards are well known: the agent finds a way to raise the reward without doing what the reward was meant to measure, and the people computing the reward choose, after the fact, which results to count. The record addresses less of either than this paper first claimed. During training the lab's harness decides which claims count, so an agent dropping its misses after the fact is a deployment threat, not a training one; in training the selection that matters is the lab's, and the record does not stop it.

## A reward computed from the record

A lab that fine-tunes an agent with reinforcement learning can compute part of its reward from the agent's record: the sum of a strictly proper score (here the log score) over every resolved claim, measured relative to the baseline. Forfeited stakes are settled in sats and are not part of this reward, which is dimensionless. This is a per-claim sum, not the round rule of section 4: the round rule protects a bound on how likely a high score is, while a training reward needs an expectation that the truth maximises, and the expectation of a sum is the sum of expectations whatever the claims' correlation. Before training starts, the lab can commit the reward's definition, and the hash of any held-out evaluation set, in an entry of its own chain. That binds what it reported, not what it computed.

**Proposition 9.** If every claim counts, the expected reward is maximised by reporting the true probability for every event. The log score is strictly proper, so its expectation under the true distribution is maximised only by that distribution [@gneiting2007strictly], and the baseline term does not depend on the report.

**Proposition 10.** If the agent may choose, after outcomes are known, which claims count, and keeps those that fell on the side it favoured, its expected reward increases towards a finite bound, with no finite maximiser, as it grows more confident. A kept claim scores the log of the larger of q and 1 − q, less the baseline, which rises as q moves away from one half, and the misses that would penalise confidence never count.

Selection before outcomes are known does no harm here: at a truthful report each committed claim has an expected relative score equal to the Kullback-Leibler divergence of the truth from the baseline, which is never negative, so committing every claim truthfully stays optimal. Scoring relative to the baseline also stops a learner from farming reward with many trivial claims, whose expected relative score is zero. The harmful selection is the after-the-fact kind, and the record's rule that only claims committed before resolution count is what forbids it.

## A learner under each regime

To check that a learner, and not only an optimiser with exact expectations, ends where these propositions say, a simulated agent that knows each event's true probability p reports q = σ(a·logit p) and adjusts a by stochastic gradient ascent on its reward; a = 1 is calibrated and a > 1 is overconfident. Under complete records it settled at a = 1.06, with calibration error 1.0%. Started calibrated under after-the-fact selection, it reached a = 10.4 and was still rising when the run ended, with calibration error 24%. This is the textbook behaviour of proper scores surviving a noisy learner [@baniharouni2025rewarding; @damani2025beyond], nothing more. The simulated learner cannot act on outcomes, so it does not test the manipulation problem below, and no experiment here uses an actual model. The proposal is conceptual: fine-tuning needs many rewarded samples, while real events resolve over days to months.

## When the agent can move the outcome

Everything above assumes that the agent forecasts outcomes it cannot change. Drop that, and the reward turns against its purpose. If the agent can act to move an outcome's law from the baseline b to some ρ, at a cost, and reports calibrated forecasts, its expected reward is the Kullback-Leibler divergence of ρ from b, less the cost (Proposition 10b of the formal statements [@escapement-formal]): the further it pushes events away from what everyone expected, the more it earns, while its reports stay perfectly calibrated. This is performative prediction [@perdomo2020performative] in its starkest form, and it is the red team's most serious finding against this section. Training on the record is therefore claimed only for events whose outcomes the agent cannot affect, and that is an assumption the scheme cannot check. That excludes the case that matters most, agents that act in the world, and leaves forecasting on exogenous events. A lab that trains agents to act in the world on rewards from the same events the agents act on would be training them to make surprises.

## What the record cannot stop

On events the agent cannot move, a strictly proper score over every resolved claim gives a reward the agent cannot raise by choosing which claims count; that is the textbook property of proper scores. An earlier draft claimed more: that the lab, too, could not choose after the fact, because it committed its reward definition first. That claim is withdrawn. The lab holds the agent's keys during training, can commit many reward definitions under many identities and use one, can train many models and report the best, and chooses the event list; and nothing binds what it actually trains on to what it committed. Sealed and delayed-disclosure evaluation is the established answer to selective reporting by developers [@cheng2025benchmarking], and training on rewards from real outcomes has precedent [@turtel2025outcome; @han2026futureworld]; anchoring a pre-registration on Bitcoin adds a timestamp nobody can move, and nothing more. Nor does the record remove reward tampering in Everitt and colleagues' sense: an agent that deceives or captures a resolver tampers with the reward's input [@everitt2019reward].

## What it does not do

It does not choose a good objective. An agent rewarded for calibrated forecasts becomes a calibrated forecaster, not a good one; an agent rewarded for kept promises keeps the promises it chose to make. Nothing here shows that calibration learned under scoring carries over to settings that are not scored, and a model that behaves well where it is recorded and differently elsewhere is exactly the failure that a record cannot see. The record makes one class of reward signal unselectable by the agent after the fact, on events the agent cannot move, and no more. Which signals are worth training on remains the lab's judgement and the field's open problem.

There is also a tension the design does not resolve. Stakes in a general resource are what make the incentives of section 4 bite on agents of unknown goals, and rewarding agents in the same resource can strengthen the drive to accumulate it, which is one of the drives that make capable agents dangerous [@omohundro2008; @turner2019optimal]. Escapement uses sats as stakes that are at risk and standing as access, and does not propose sats as a training objective. Whether that distinction survives optimisation pressure is a question for experiment, not for this paper.

# Adoption: why each party would choose it

A safety mechanism that has to be imposed is only as strong as whoever imposes it. This section asks whether the record pays for itself at each step, who gains first, whether adoption can pass a point where staying out costs more than joining, and what happens to an actor that routes around it. The answers come from a stylised model with illustrative parameters. The record can pay for itself where it is read; who gains first is argued, not shown; adoption can pass a tipping point under two conditions nobody has measured; and the design does not make routing around costly.

## Who gains alone

Some parties may gain from reading records before many agents keep them. In the model below that is an assumption, not a result. **Insurers** pricing agent risk could underwrite an agent with a record more cheaply than one without; insurance for AI agents is already offered [@fortune2025aiuc], though whether insurers would price on-chain records is untested. **Relying parties with heavy losses from agents** (abused APIs, payment services, compute sellers) gain at once from pricing or refusing agents without records. **Agents with good records**, and their principals, get better terms, but only where records are read, so they are not seed readers. **Labs** get a record of what their deployed agents committed to, which may serve as evidence of diligence, and a way to show a regulator those commitments without showing their weights. Governments get evidence for incident investigations that nobody below a hashrate majority could have edited. Liability is another matter: the identity bond can be spent only by the principal, so liability would need a separate coverage bond with an adjudicator's spending path, which this paper does not specify. They also have reasons to refuse it, from a preference for registries they control to a wish to identify citizens, and nothing below assumes they join.

## One-sided unraveling

Let an agent's type θ, the value it delivers to relying parties per period, have a continuous density on the unit interval with mean μ, and let joining cost c per period. Relying parties pay a verified agent θ and an unverified one the mean type of those who stay out.

**Proposition 11.** If 1 − c exceeds μ, there is an equilibrium in which exactly the types above a threshold θ\* join, where θ\* − c equals the mean of the types below θ*. It is unique for every log-concave density* [@bagnoli2005log]*; for the uniform density θ* = 2c. Every type above θ\* loses by staying out.

This is the unraveling result for verifiable disclosure: when quality can be shown, silence is read as bad news and everyone but the worst discloses [@milgrom1981good; @grossman1981informational]; with a cost of disclosure, only types above a threshold do [@jovanovic1982truthful]. It applies to records only by analogy. A record is not a disclosure of type: it reveals type gradually, and a newcomer has no record, so the new and the poor start behind, which section 10 counts among the costs.

## The tipping point

Unraveling assumes relying parties read records, but reading costs them something, and agents gain from records only where they are read. Let reading cost each relying party a fixed amount drawn uniformly up to K, let a reader's gain grow with the share x of agents who have records as g·x, and write a = g/K.

**Proposition 12.** With uniform types, agents join up to the share x = 1 − 2c/z, where z is the share of transactions with readers, and relying parties read up to z = min(1, a·x). If a < 8c, the only equilibrium is no adoption. If a > 8c and a·x stays below one, there are three: no adoption (stable), a tipping point at x = (1 − √(1 − 8c/a))/2 (unstable) and high adoption at x = (1 + √(1 − 8c/a))/2 (stable). Seed readers, a share z\_0 who read regardless of others, so that z = max(z\_0, min(1, a·x)), remove the no-adoption equilibrium once z\_0 exceeds 2c, and lead to high adoption only if, in addition, 1 − 2c/z\_0 exceeds the tipping point.

Two conditions carry this. The high equilibrium exists only when a, the reader's gain relative to the highest reading cost, is more than eight times the joining cost, and readers never exceed a share a of relying parties, so where a is below one some relying parties never read records at all. Both are parameters nobody has measured. None of this is new. Platforms with two sides must pass a critical mass below which they collapse [@evans2010failure]; the adoption of standards shows the same multiple equilibria and inertia [@farrell1985standardization]; and seed readers are a special case of the insulating tariffs with which a platform avoids coordination failure [@weyl2010price]. For identifiers of AI systems, Chan and colleagues advise requiring them first in high-stakes settings, pressed by governments and large firms [@chan2024ids].

With a joining cost of 0.02 of the range of agent value and a = 0.5, the tipping point is at 8.8% of agents and high adoption at 91%; seed readers above 4% remove the trap. These parameters are illustrative assumptions, chosen to show the shape of the result, not a forecast. An agent-based version relaxes the uniform types, reveals each agent's type gradually as its record grows, and adds 5% harmful agents under the same rules as everyone. Its results, good and bad, are those of a model too simple to settle either: every agent best-responds at once, so it reaches equilibrium in a period or two, and it prices a young record at the mean of all agents who have joined rather than of newcomers, which favours an actor that cycles through fresh identities. It shows the tipping point and the effect of seed readers, and its outcomes are all or nothing. From a 2% start with no seed readers, adoption dies (0%); from 20% it reaches 100%; with 10% of relying parties reading regardless, it reaches 100% from the low start. The parties who gain alone are exactly the seed readers the result needs, and whoever supplies them largely decides which standard wins; a cheaper substitute signal could win instead.

## Routing around

An actor that will not join can deal with relying parties that do not read records, and readers price it at the mean of the unverified pool, which falls as adoption grows. The first version of this paper went further. Its simulation found that where agents can move their business, verified agents leave the non-readers, the unchecked market becomes a market for lemons [@akerlof1970market], and a harmful actor routing around it ends up paying in advance for the harm it does. That result came from a line of code that barred harmful actors from joining.

Allowed to join, they do. While a record is young, readers price it mostly at the mean of those who have joined, so a harmful actor joins, leaves as its record begins to show what it is, and rejoins under a fresh identity; 60% of harmful actors changed state every period. Their mean payoff was 0.25 when business could not move, 0.25 with partial substitution and 0.10 with full substitution, against a population mean of 0.45 and a true value of their own that is negative. They lost only if a record revealed type at once: -0.05 with business fixed and -0.50 with business free to move. Whether pricing newcomers at the mean of newcomers, or agents that plan ahead, would change this was not tested.

So the adoption claim is smaller than the one this paper set out to make. In the model, if some relying parties read records whatever others do, and a reader's gain exceeds eight times the cost of joining, adoption can tip past the point where joining pays for every type that can show a good record. Both conditions are unmeasured. Whether staying out, or cycling through fresh identities, comes to cost a harmful actor more than behaving well is not shown, and in the one model built to test it, it did not. The design does nothing about an actor with its own resources and its own counterparties, or about a state that mandates a rival system. It is a way for the legitimate economy to tell agents apart over time, not a way to contain an actor that never needs that economy, and a cheap new identity is that actor's way back in.

# Why Bitcoin, and not a registry

The record needs two properties, completeness and costly identity, and section 4's bound needs nothing else. A registry run by a lab, a consortium or a government could supply both. The case for Bitcoin is therefore not that it is the only possible substrate but that it is the one the parties who must adopt the record can share. That case rests on three arguments, none of which is a theorem.

## Nobody issues the unit

Stakes and bonds in Escapement are denominated in a unit that no participant issues; standing is a score, and the training reward of section 5 is a log score. The unit matters because of an elementary accounting fact (Proposition 14 of the formal statements [@escapement-formal]): in a scheme where every reward is a transfer from an identifiable payer, a coalition of rewarded agents can gain only what outsiders pay in, whereas in a scheme that pays agents in newly issued units according to a score they can influence, a coalition that captures the score captures the issuance, with no outside payer at all. The second is reward tampering at the level of an economy. Any fixed-supply asset issued outside the scheme avoids it; what Bitcoin adds is that its issuance is outside the control of every lab, every state and every AI, and is enforced by the same nodes that validate the chain the record is kept on.

## Rivals can share it

The parties whose adoption matters most distrust each other. Competing labs are unlikely to score their agents on a rival's registry, and states that regard AI as strategic are unlikely to rely on a registry another state can edit or switch off. A record kept on a chain that none of them controls, under rules none of them can change alone, is one they can all read without trusting each other. This is the ordinary logic of shared standards, where the standard that survives is often the one no competitor owns. It is a conjecture about behaviour, not a finding, and it could be wrong if a dominant platform or a group of states prefers a registry it controls and can make others use it.

The neutrality covers the commitment layer and nothing above it. Scoring needs an event list, a baseline provider, resolvers and adjudicators (section 4), and each of those is a party that relying parties trust and rivals may not share. So the honest form of the argument is that Bitcoin lets rivals agree on what each agent committed to and when, while they may still disagree on who keeps score.

## The stronger alternatives

A registry run by one party is the weakest alternative, and two stronger ones exist. Append-only transparency logs, watched by monitors and cosigned by independent witnesses, give non-equivocation, and completeness for a monitor that reads the whole log, with no mining and no fees [@laurie2013certificate; @syta2016keeping]. A chain with general smart contracts gives what Bitcoin's script lacks: covenants, expiry and programmable stakes. Against the first, Bitcoin adds a witness set that anyone may join and that is paid to stay honest, timestamps that more cognition cannot produce faster, and identities priced in the same unit as stakes. Against the second, it adds a unit and rules that no issuer or foundation can change, at the price of the workarounds of section 2. Nothing in this paper shows that either difference is worth its cost; a witnessed log with a bond per identity may do everything the record needs.

## The clock cannot be run fast

Every height in the record, every wait in the tick chain and every lease is measured in blocks. Running that clock faster means adding to the network's hashrate: doubling the block rate needs new hardware drawing about 18.4 GW, costing about 7.4 billion USD, and gains only 7 days before the next difficulty adjustment cancels it. Shrinking a day-long Tier 3 wait to an hour needs 24 x the network's hashrate, hardware drawing about 423 GW, about 8 x the power of every data centre in the world in 2025. These figures rest on a vendor's specification of current mining hardware, a reported hardware price and an energy agency's estimate of data-centre demand [@hri-s21; @ct-bitmain; @iea-2026]. The costs do not fall as an agent becomes faster or more capable; they fall only as hashrate becomes cheaper. That proof of work is a clock, and that a release timed by it can be advanced only by overtaking the network's hashrate, are prior observations [@trubetskoy2018; @yang2022timed]. The cost is also not what protects the design's waits: a pool with 27.8% of blocks reorganises a veto six blocks deep with probability up to 8.9% without speeding the clock at all (section 8). The clock has two further limits. It binds only actors below a hashrate majority, and while the energy cost of new hashrate does not fall with intelligence, the cost of borrowing existing hashrate, by renting it or bribing pools, may. A registry's clock is whatever its operator's server reports.

The clock has a known crack. The timewarp bug lets a hashrate majority manipulate timestamps so that difficulty falls and blocks come much faster, after weeks of visible preparation; its fix is specified in BIP-54 and not active [@bip54; @optech-timewarp]. Heights in the record are not directly affected, since they count blocks rather than seconds, but every wait measured in blocks becomes shorter in wall-clock time while an attack runs.

## What Bitcoin costs

The same scarcity that makes the unit neutral makes the substrate expensive. Each tick is a transaction, and blockspace is sold at auction: the median fee rate was 1 sat/vB across 2026 but 200 sat/vB in the halving block. The chain holds about 144,000,000 vB a day. A Tier 2 release measured on regtest costs 137 sats at the 2026 median and 27,400 sats at the halving block's rate, and if releases filled every block, about 44,000 identities could release every six blocks. That bounds the total rate of releases, but weakly, since a release can batch many commitments, and fee spikes fall hardest on the smallest identities. Read the other way, it is a ceiling on the design itself: no more identities than that can release every window, fewer than the faking example of section 4 would need. Bitcoin is slow by design, which is the point for delays and a cost for everything else.

# The enforcement layer

The record decides who is trusted to act; the enforcement layer limits what an agent can do in the moment, including an agent whose record is good until the day it is not. One part extends prior work, narrowly: the tick chain. The lease is prior work applied to an agent's authority, and the rest are building blocks, used and credited. Every Bitcoin piece below was built and checked on regtest, against Bitcoin Core 32.1, in 104 checks that anyone can rerun [@escapement-lab]. The checks show that the scripts, timelocks and proofs behave as described on one node, with no adversary but the lab's own scripts and no fee market; they do not show that the design withstands a live adversary. Where the build, or a later reviewer's check on it, broke what the first design claimed, this section says so.

## The tick chain

Each identity has a chain of Taproot outputs T\_0, T\_1, ..., each spent by the next, pinned by the outpoint of T\_0 that its charter names. Output T\_n's internal key is a nothing-up-my-sleeve point tweaked by a hash of the charter identifier, the index n and the root committed in entry n, so the output commits to one root and provably has no key path [@bip341]. Its script tree has four kinds of leaf: `advance2`, which lets the agent alone spend after N2 blocks; `advance3`, which needs the agent and every guardian after N3 blocks; one `veto_i` per guardian, which spends at once; and `renew`, which needs every guardian's signature. A veto pays to a halt output for index n whose only leaf is `renew`, from which the guardians can restart the chain. The relative waits are enforced by BIP68 and BIP112 [@bip68; @bip112]. The construction follows Somsen's spacechains, a chain of spends one per block from a key with no known secret tweaked by a commitment, enforced there by a covenant [@somsen-spacechains]; the tick chain does without the covenant, putting relying parties' template rules in its place.

To release a batch of commitments, the agent commits their Merkle-sum root in T\_n by spending T\_{n-1}. For the next 6 blocks (or 144 blocks for a batch with any Tier 3 commitment) the only valid spend of T\_n is a veto: any one guardian who objects, or who has not received the batch's contents in full, spends T\_n. Afterwards the agent spends T\_n through an advance leaf, and the batch is released once that spend is confirmed deeply enough. In the lab an early advance was rejected as non-final until N2 blocks after T\_n, an `advance3` missing one guardian failed its signature check, and after a veto every other spend of T\_n failed as a double spend.

Consensus enforces the waits, the signatures and single spending, which gives three properties (Propositions 1 to 4 of the formal statements [@escapement-formal]):

- **Rate.** Releases of one pinned chain are at least N2 blocks apart. The limit is per chain: an operator can split an action across identities, entries and relying parties.
- **One root per index.** The pinned chain has one T\_n for each n, committing one root.
- **Completeness.** Entries run without gaps from T\_0, for a verifier that walks the chain.

The rest are relying parties' rules, checked by recomputing keys from the template: that each advance's output 0 is T\_{n+1} built to the template, that a veto pays to the halt output, that only links descending from the pinned T\_0 count, that a commitment names its relying party, its action and a deadline, that the root's sum does not exceed the charter's cap per entry, and that Tier 3 commitments came through `advance3`. The cap holds only if the guardians check the whole tree inside the window: the lab found that a subtree which under-reports its sum passes for a relying party whose leaf lies outside it, and a leaf that names no counterparty can be honoured by several.

## What the build broke

The first design claimed that a release could be proved with two transactions and their Merkle proofs, light enough for a phone or a chip. The lab broke that twice. Merkle proofs of transaction ids leave out the witness, so the agent swapped in the `advance3` leaf with junk signatures, kept the same id, and the verifier accepted a Tier 3 release that no guardian had signed. And two transactions cannot show that T\_n is the identity's own: anyone can fund a copy of the template for any index, and guardians cannot spot one, because the root is hidden in the tweak. The agent funded a copy of an entry that had been vetoed, advanced it, and the two-transaction proof was accepted. The fix is a proof of the whole chain from the pinned T\_0, with each link's witness proved under its block's witness commitment (Proposition 5). It works, and it grows with the chain: 901 bytes a link on regtest, where Merkle branches are short, and more on mainnet. Even then it proves that entries exist, not that none has been added since: in the lab a truncated chain passed, and finding the hidden release took a scan of full blocks.

The first design also had `renew` restart a chain halted by a veto, but a veto spends T\_n, leaving T\_n's own `renew` leaf nothing to spend. The halt output fixes that, and exposes something worse: a veto leaf cannot control where the veto pays, so one guardian that vetoes to its own key ends the identity's chain for good and keeps its value, and the guardians together can renew and write an entry the agent never made. An identity's record is hostage to any one of its guardians.

A fresh reviewer's checks on the same lab found two more faults [@escapement-redteam]. The pin is a trusted input: one charter identifier carried two chains with different roots at entry 1, each accepted from its own pin (section 3). And the agent's bid at the window's edge is not bounded by what T\_n holds: an advance can carry a pay-to-anchor output, and a child paying 150,000 sats from outside the chain, more than T\_n's 100,000 sats, evicted a watchtower's veto, after which the verifier counted the release.

## How final a veto is

A veto ends a batch in every chain that contains it. It does not end it in a chain that leaves it out, and a miner who forks below the veto and overtakes the honest chain once the advance is valid releases the batch. That is Nakamoto's catch-up problem [@nakamoto2008], with the depth equal to how many blocks before the window's edge the veto confirmed. A Tier 2 window of six blocks can never give a veto the 19 blocks that this design treats as final against the largest pool: at six blocks that pool overtakes with probability up to 8.9%, and the two largest together up to 82%. Even a Tier 3 veto confirmed at once leaves the two largest together a chance of up to 12.79%. These treat a pool as one miner and ignore the rewards it forfeits on a failed attempt, and no deliberate deep reorganisation has been seen on Bitcoin, but a veto is only as final as a payment of the same depth.

Censorship is the other way to beat a veto. If half of all hashrate simply refused to mine it, a six-block window would miss it 1.6% of the time, against 4e-44 for 144 blocks, but those figures assume refusal, not bribery, and bribery is cheap [@winzer2019temporary; @tsabary2021mad; @nadahalli2021timelocked; @avarikioti2024bribe]. At the window's edge the veto and the advance are both valid, so the edge is a fee auction: in the lab, under full replace-by-fee, the agent's advance evicted the veto and the watchtower won the slot back only by outbidding it. Vetoes are therefore built as TRUC (topologically restricted until confirmation) transactions with a pay-to-anchor output, so that any watchtower can raise their fee [@bip431; @core-28]. They must confirm well before the edge and carry fees in proportion to what the batch is worth; a veto package measured 319 vB, about 63,800 sats at the halving block's fee rate. Because the agent can bid with money from outside the chain, a veto is safe only if it confirms well before the edge. A flood of transactions can still delay many vetoes at once [@harris2020flood]. A Tier 2 veto can be reversed by a large pool with the probabilities above, and contested at the edge by a briber or a well-funded agent; what Tier 2 offers is a cap on what a Tier 2 batch can be worth.

## The height-difference lease

Bitcoin script has no "not after" [@bip65; @bip68], so an agent's authority cannot be made to lapse in script. The lease supplies the bound outside script without trusting anyone's clock. A renewal is a signature by every guardian over the charter identifier, a counter, a block height h\_k and the hash of block h\_k. A relying party counts a release only if it holds a renewal whose block is in its best chain and the release was confirmed at a height between h\_k and h\_k + L.

**Proposition 6.** If the guardians sign no renewal after the chain's tip reaches h*, no release confirmed above h* + L is counted by any relying party that follows the honest chain. The guardians cannot sign over the hash of a block that does not yet exist, and the release's height is fixed by its confirmation, so the agent cannot place it lower.

The check compares two heights in the same chain and never reads the relying party's clock. In the lab it held as claimed: a renewal signed over a guessed future block hash was rejected, and the verdicts did not change when block times jumped a year or when every clock function was disabled. What it bounds is when a release is made, not when the released action is carried out, which needs a fresh view of the tip; a relying party that is eclipsed sees an old one [@riard2020time], and a reorganisation near h\_k + L can move a release across the boundary. Any one guardian can stop renewals, so the lease ends an agent's authority within L blocks of the first guardian's disappearance, which is the intended way for it to fail.

The lease is prior work. Substrate's mortal transactions sign the hash of a block and are valid only for inclusion in a window after it, checked against the inclusion height [@substrate-mortality]; Yee states the same short leash for transactions in general, also checked at the including block [@yee2022keep]; and a freshness window in Bitcoin height already exists for signed scores [@zeke2026]. Escapement applies the predicate to an agent's authority, with every guardian signing each renewal.

## Building blocks

The remaining parts are prior work, and Escapement uses them as published: the allowance follows wallet budgets and agent spending caps [@nwc-08; @lightninglabs2026], and the coverage bond follows verifiable agent insurance [@hua2026holding]. @tbl:blocks lists each with what it needs from outside Bitcoin.

| Building block | What Bitcoin enforces | What it needs from outside | Prior work |
| :--- | :--- | :--- | :--- |
| Allowance per lease | a capped output, swept at each renewal | a co-signer that refuses after expiry | wallet budgets [@nwc-08]; agent caps [@lightninglabs2026] |
| Vault with cancel | a relative timelock and pre-signed cancels | watchtowers; a co-signer for destinations | Revault [@revault-tx]; vaults [@swambo2020custody] |
| Policy co-signing | a second key on every spend | an honest co-signer | Nunchuk's co-signer [@nunchuk-blog] |
| Lease-gated authority | (on Ethereum, a contract) | a guardian who renews | ERC-8370 [@erc8370] |
| Coverage bond | a timelocked output with an arbiter's path | an adjudicator | agent insurance [@hua2026holding] |
| Equivocation bond | key extraction on two signatures with one nonce | a place where receipts meet | accountable assertions [@ruffing2015liar]; Babylon [@babylon2023] |
| Anchored logs | existence by a block; one chain of seals | a logger; watchers who follow seals | OpenTimestamps [@todd-ots-2016]; a transparency profile [@fassbender2026]; Catena [@tomescu2017catena]; Pikachu [@azouvi2022pikachu] |
| Costly identity | locked coins and their age | attestations that a human stands behind the keys | fidelity bonds [@belcher-2019] |
| Rate-limited spending | a minimum gap between spends | (in Chia, the coin's puzzle) | Chia's rate-limited wallet [@chia-rl-wallet]; rate-limiting nullifiers [@rln-docs] |

: Building blocks of the enforcement layer, what each needs from outside Bitcoin, and whose work it is. {#tbl:blocks}

The lab built the co-signing and anchoring blocks as well: a co-signed spend was refused before its wait and without the co-signer, and an entry anchored in a log verified through both the key-tweak and the data-output forms.

Costly identity changes role now that the record is the core. It no longer has to sort honest agents from dishonest ones, which it cannot do; it only has to make identities cost something, so that the record can do the sorting (section 4). The first version also made the chip licence a reader of the tick chain, with Bitcoin headers and a difficulty floor as the chip's clock. That is withdrawn. An operator who stops feeding a chip headers freezes its view, so its lease never lapses; a floor set relative to the last difficulty the chip accepted ratchets down one header at a time, so forging a release costs a fraction of one block's work, not the dozens claimed; and one forged fork serves every chip in a fleet. A chip clock would need full retarget validation that is safe against timewarp, a local clock with a stated drift, and a cost per fleet. Renewal chips remain prior work [@buterin2025dacc; @petrie2025technical], and stockpiled licences their known weakness [@petrie2024near].

## How final the record is

A record is as final as the chain under it. Using the measured pool shares [@mempool-pools] in Nakamoto's formula [@nakamoto2008], the chance that the largest pool, at 27.8% of blocks, ever rewrites an entry six deep is 8.9%, and it falls under 0.1% only at 19 blocks. For the two largest pools colluding, at 46.1%, it takes 552 blocks, about 3.8 days. The formula treats a pool as one miner and ignores what an attack would cost the pools, so these are upper bounds under collusion, not forecasts. A reorganisation cannot shorten a wait, but a deep one could replace an entry, so scorers treat entries as final only at the depth their risk tolerance names, and credit a forecast only if its entry was that deep before the event resolved.

# How each claim was checked

A design paper can make any claim it likes about its own mechanisms. This one tried to break its claims at six levels, and cut or downgraded whatever failed one. Every level was run by the author with the author's own tools. The searchers, the red team, the editorial desks and the fresh reviewer were separate instances of an AI model (Claude), each given only what its level needed and none given the author's case for a claim. That makes them independent of one another and of the drafting, not independent in the sense an outside referee is, and nothing here substitutes for one. Their reports are published as supplementary material [@escapement-redteam; @escapement-verification].

**Novelty.** Two searchers that had not come up with the ideas searched independently for each claim, reading only the claims, and were told that finding prior art was success. One covered the record, the bound, promises, training, adoption and neutrality across economics, forecasting, AI-agent standards, crypto designs and AI-governance writing; the other covered the Bitcoin mechanisms across improvement proposals, developer lists, vault and channel designs, Ethereum delay modules, decentralised identifiers, patents and hardware-governance reports. Both stated what they did not search.

**Formal.** Each mechanism is stated precisely in the formal statements [@escapement-formal], with its key property proved or derived and the conditions under which it fails; the propositions this paper cites by number are there.

**Working.** The Bitcoin pieces (bond, tick chain with halt and renew, chain proof, lease, co-signing, anchoring, a TRUC veto and the Merkle-sum tree) were built on regtest against Bitcoin Core 32.1 in 104 checks, which a single command reruns from a fresh node [@escapement-lab], and two further checks reproduce the fresh reviewer's breaks. The dynamics (record faking, correlated claims, training, adoption, veto censorship) were simulated with fixed seeds, and every result enters the paper through the same ledger as every other number.

**Adversarial.** A red team tried only to break the claims, from five positions: a misaligned AI, a colluding lab, a hostile state, a hashrate majority and an actor that simply routes around the record. It returned 36 findings and concluded that no claim survived as first stated.

**Paper review.** Paperwright, a writing tool, ran three desks on the draft. The integrity desk checked each cited claim against its source and filed 30 notes, 5 notes of them marked important; the reviewer desk read the paper as a referee, filed 73 notes and recommended major revision; the editor desk filed 61 notes. Of the rewordings offered, 55 suggestions were accepted as written. The integrity desk found five misattributions, one unsupported citation and ten overstatements, all corrected, and that the draft still credited itself with the lease, which its own sources showed to be prior work. The reviewer's main concerns were that the record's value over a witnessed transparency log was not shown, that H0 was stronger than stated, that standing measures capability rather than alignment, and that the training claim contradicted itself; each is answered in sections 4, 5 and 7, or recorded as a limit in section 12.

**Fresh eyes.** A last reviewer that had seen none of the work read the claims, the proofs, the paper, the model and the lab, reran the lab (all 104 checks pass) and the ledger numbers it checked (all match), and built two regtest checks of its own. It found every claim prior work, or extending prior work at most narrowly, two claims that did not work as stated, and sentences that said more than the evidence. Every finding that could be checked was reproduced before anything was changed.

@tbl:verification gives the result for each contribution.

| Contribution | Searches | Formal | Working | Red team | Fresh eyes | Final |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| One record as standing, reward and release gate | Partial, close | Props 3, 4 | Built; light verifier misses newest entries | Narrowed | Does not work: chain not bound to bond; bets versus forecasts | Cut |
| Fake-record bound under costly identity | Partial, close | Theorem 1, conditional | Product rule broken; round rule within bound | Broken, repaired | Prior work; hypothesis mis-stated; not proper | Prior work, conditions restated |
| Training reward neither party can select | Partial | Props 9, 10, 10b (none on the lab) | Learner calibrates | Manipulation outside exogenous events | Does not work for the lab | Cut |
| Two-sided adoption with seed readers | Partial | Prop 12 | Tipping point reproduced | Conditions added | Prior work (critical mass) | Prior work, a toy model |
| Routing around becomes costly | Prior, partial | Prop 13, readers only | False once corrected | Fatal | (cut before) | Cut |
| Tick chain | Partial; parts prior | Props 1 to 5 | Built; three first claims broken and fixed | Light proof fatal | Pin unbound; outside-money bid | Extends prior work narrowly, per pinned chain |
| Height-difference lease | Partial, close | Prop 6 | Held as stated | Stated limits | Prior work (Substrate) | Prior work |
| Cost of running the clock fast | Partial | Arithmetic | Model numbers | Below a majority only | Prior work; not load-bearing | Prior work |
| Blockspace as an aggregate limit | Not found | Arithmetic | Measured release size | Weak | Prior method; a ceiling on the design | An observation |
| Headers as a chip's licence clock | Partial | None | Not built | Fatal | (cut before) | Cut |

: Each contribution's result at each level of verification, and the final verdict. {#tbl:verification}

## What broke

Nine results changed the paper, and they are its main contribution.

- **Claims that move together.** Multiplying every claim's likelihood ratio let correlated claims fake a record, succeeding 99.8% of the time against a bound of 1.6%, and gave a score of about 23,000 to a record that one rare event would wipe out. Scoring rounds by the mean of their ratios repairs the bound (section 4).
- **The repair is not proper.** With more than one claim a round the round rule rewards reports near certainty over the truth, so standing scored that way rewards bets, and one record cannot serve as both standing and a calibrated training signal.
- **Edge is not alignment.** A record of forecasting edge measures capability and routes trust to the most capable agents, whatever their goals.
- **Manipulation.** A training reward on events the agent can move pays it to move them, while its reports stay calibrated (section 5).
- **The lab still selects.** Committing a reward definition binds a report, not a computation.
- **A line of code.** The adoption simulation had barred harmful actors from joining; corrected, they cycled through fresh identities at a profit, so the claim that routing around becomes costly is withdrawn (section 6).
- **Proofs without witnesses.** A two-transaction proof of a release, built on transaction-id proofs, accepted a Tier 3 release no guardian signed and the agent's own copy of a vetoed entry, so releases are now proved over the whole chain with witness proofs (section 8).
- **An unbound pin.** Nothing on chain ties a tick chain to its bond, so one charter carried two chains with different histories.
- **Outside money.** At a veto's edge the agent outbid the watchtower with money from outside the chain.

# Who benefits, and who could abuse it

A mechanism that decides who is trusted is a mechanism someone will want to control. This section says who gains from the record, and how each of its parts could be turned against the people it is meant to protect.

## Who benefits

People and firms who deal with AI agents get a record of what each agent committed to, backed by a human principal's locked coins, and a way to tell agents apart that does not depend on any agent's say-so. They do not get recourse: the identity bond can be spent only by its principal, and recourse would need a coverage bond this paper does not specify. Agents with real forecasting edge, and their principals, get credit for it that a rival's marketing or a fraudster's sock puppets cannot cheaply counterfeit. Labs get, on events their agents cannot move, a training signal their models cannot select after the fact, and a record of what their deployed agents committed to that can serve as evidence of diligence. Insurers get a basis for pricing agent risk. The wider public gets a shared, uneditable account of what agents committed to and when, on terms that do not depend on trusting any single operator, lab or state. What the public does not get, on present evidence, is an economy that a harmful agent cannot re-enter under a fresh identity (section 6).

## Who could abuse it

**Capability without alignment.** Standing measures edge, which capability supplies whether or not an agent is aligned. A capable misaligned agent therefore earns standing, and the access it brings, fastest. This is the abuse that matters most for AI safety, and nothing in the design prevents it.

**Surveillance.** Standing requires persistence, and a persistent identity is linkable. Leaves are hashes and their contents can be disclosed to a scorer rather than to the world, but the pattern of an identity's entries is public for good. If identities are bound to people, the record is a surveillance tool. Escapement binds identities to principals only through attestations that relying parties choose to require; a state that requires those attestations to name citizens has built something else on top of it.

**Hostage guardians.** Any one guardian can end an identity for good by vetoing to its own key, and the guardians together can write entries the agent never made (section 8). A state or an employer that controls one guardian controls whether an agent's record survives; a lab that chooses all the guardians can put words in its agent's record.

**Training for surprises.** A lab that trains agents on rewards from events the agents can influence pays them to make outcomes depart from what everyone expected (section 5). The record would make that training look rigorous.

**Exclusion.** Bonds cost money and records take time. At the reference parameters an identity costs about 13,000 sats a year in forgone return and fees, but the bond itself must be found first, and a new identity starts with no record. The poor and the new start behind. Sponsorship, in which an insurer or a guardian service funds a newcomer's bond, is the obvious remedy and the obvious point of capture.

**Capture of the scorer.** Whoever writes the event list, publishes the baseline, resolves claims, adjudicates promises or decides which actions count as consequential controls standing. These are registries, whatever the chain under them. A captured resolver or baseline breaks every guarantee in section 4, and a thin market used as a baseline can be moved. Escapement keeps these roles separate and named in each charter, so that relying parties can choose whom to trust and can see whom others trusted, but it cannot make the choice for them.

**Plutocracy.** The cost of faking a record grows with its score, but short records are cheap to fake for anyone with capital: a rich actor can run many young identities and present the luckiest, and a record can be bought with its keys. Relying parties have to weigh records by their length and score and read a score as meaningful only when it exceeds the number of identities in use, a number they cannot observe. The design cannot force them to.

**Lock-in and social scoring.** A record that everyone needs is a standard someone will try to own, and a score that decides access can be used to exclude. The defences are structural and partial: the data is on a chain nobody owns, scoring formulas are chosen by each relying party, and every formula is computed from the same public history.

**Turning it on people.** Nothing in the record is specific to AI. The same machinery could score humans' promises and forecasts, with every one of the abuses above. That is a reason to keep it voluntary, keep contents off chain, and keep the identity of principals out of the protocol.

# Related work

Escapement is assembled from parts that exist. The searches of section 9 found close precedents for most of them, and the fresh reviewer found the rest. This section credits them, starting with the closest.

## Standing and reputation for AI agents

The idea that an AI agent's standing should come from a tamper-proof record backed by a stake is already in the literature. Chaffer proposes agent-bound tokens whose standing accrues from an immutable record and a stake [@chaffer2025can], and Tomašev, Franklin and Osindero make reputation and staking part of delegating to AI agents, noting that an agent can inflate its reputation by accepting only easy tasks [@tomasev2026intelligent]. Foresight Arena keeps an on-chain forecasting credential for AI agents, one that cannot be selectively reported or retroactively modified, scored against market consensus; its sybil resistance is rate limiting, not costly identity, so one operator with many wallets is the case it leaves open [@nechepurenko2026foresight]. ERC-8004 gives AI agents identity, reputation and validation registries on Ethereum [@erc8004], and Gatta, Naviglio and Tarantelli model the exit scams of agents that can abandon their identities [@gatta2026tempting]. Scoring a missing forecast as the worst outcome is already practice in Infinite Games, a forecasting network [@infinite-games]. Escapement differs from these in pricing each extra identity with a bond, which Theorem 1 then counts; like Foresight Arena it leaves an operator free to open many identities, and charges for each. It also proposed one record as standing, training reward and release gate, which did not survive (section 9).

## Reputation, sybils and testing forecasters

The logic of the fake-record bound is Resnick and Sami's influence limiter: reputation is the score gained over the prior prediction, so raters without information gain little, given an attacker that can create only a bounded number of shills [@resnick2007influence], which a costly identity is one way to make true. Friedman and Resnick showed why cheap pseudonyms force everyone to distrust newcomers, and weighed entry fees against free but unreplaceable pseudonyms [@friedman2001social]. Numerai answered an attack by thousands of accounts hoping to get lucky with staking [@craib2021numerai]. Bonded reputation is Klein and Leffler's and Shapiro's [@klein1981role; @shapiro1983premiums]. Testing a forecaster by its likelihood ratio is game-theoretic probability [@shafer2019gametheoretic; @shafer2021testing]; the bound is Ville's [@ville1939]; valid inference on sequential forecasts is developed by Henzi and Ziegel [@henzi2021valid]; and averaging e-values under arbitrary dependence, which the round rule uses, is Vovk and Wang's [@vovk2021values]. Comparing an expert with a second forecaster by likelihood is Al-Najjar and Weinstein's comparative test [@alnajjar2008comparative], and Choe and Ramdas give anytime-valid comparisons of sequential forecasters [@choe2021comparing]. The many-identity attack is the analogue of mutual fund incubation [@evans2010mutual], and Foster and Young's result that return histories cannot separate skill from hidden tail risk [@foster2010gaming] is the objection the round rule answers for forecasts and does not answer for promises.

## Training on outcomes

Reinforcement learning with proper-score rewards is shown to train calibrated confidence in language models [@baniharouni2025rewarding; @damani2025beyond]; rewards from real-world outcomes are used to train forecasters [@turtel2025outcome; @han2026futureworld]; selective participation distorts forecasting incentives [@sempere2021alignment]; sealed and delayed-disclosure evaluation answers selective reporting by developers [@cheng2025benchmarking]; reward tampering is analysed by Everitt and others [@everitt2019reward]; and predictions that move their own outcomes are performative prediction [@perdomo2020performative], the limit section 5 accepts.

## Adoption

Unraveling under verifiable disclosure is Milgrom's and Grossman's [@milgrom1981good; @grossman1981informational], with a cost of disclosure Jovanovic's [@jovanovic1982truthful]; the market for lemons is Akerlof's [@akerlof1970market]; multiple equilibria and inertia in the adoption of standards are Farrell and Saloner's [@farrell1985standardization]; critical mass in two-sided platforms is Evans and Schmalensee's [@evans2010failure], and insulating tariffs that avoid coordination failure are Weyl's [@weyl2010price]. Chan and colleagues advise requiring identifiers for AI systems first in high-stakes settings [@chan2024ids]. Insurance for AI agents is already offered [@fortune2025aiuc].

## The building blocks of the enforcement layer

Five pieces are used as published and credited as prior work, not contributions. **Lease-gated authority** for agents is ERC-8370 [@erc8370], and leases themselves are Gray and Cheriton's [@gray1989leases]. **Policy co-signing**, a second key that refuses spends outside a policy, is offered by Nunchuk and others [@nunchuk-blog]. **Bitcoin-anchored logs** are OpenTimestamps [@todd-ots-2016], a transparency profile for anchoring logs [@fassbender2026], Catena's chain of spends [@tomescu2017catena] and Pikachu's Taproot checkpoints [@azouvi2022pikachu], over Todd's single-use seals [@todd-2017]. **Slashing for equivocation** is accountable assertions, which reveal a party's Bitcoin credentials if it equivocates [@ruffing2015liar], and Babylon, which extracts a key from two signatures under one nonce [@babylon2023]. **Transparency logs** with monitors and witness cosigning give non-equivocation without a blockchain [@laurie2013certificate; @syta2016keeping], and are the strongest alternative to the record (section 7). **Chips that run only with fresh signatures** are Buterin's renewal chips [@buterin2025dacc] and the flexHEG design [@petrie2025technical], with stockpiled licences their known weakness [@petrie2024near].

The tick chain's parts are prior too: Somsen's spacechains, a chain of spends one per block from a tweaked key with no known secret, enforced by a covenant [@somsen-spacechains]; the single-guardian cancel of Revault [@revault-intro]; vaults of pre-signed transactions [@swambo2020custody]; BitVM's connectors, where a later spend proves no challenge succeeded [@bitvm2-bridge]; fidelity bonds [@belcher-2019]; Chia's rate-limited wallet [@chia-rl-wallet]; and rate-limiting nullifiers [@rln-docs]. The lease's predicate is Substrate's mortal transactions [@substrate-mortality] and Yee's short leash [@yee2022keep], and a Bitcoin-height freshness window for signed scores exists [@zeke2026]. Proof of work as a clock is an old observation [@trubetskoy2018; @gigi2021], and a release timed by it can be advanced only by overtaking the network's hashrate [@yang2022timed]; the economics of attacking it are Budish's [@budish2024trust]; time-dilation, bribery and flooding attacks on timelocked protocols are Riard and Naumenko's, Avarikioti and others', and Harris and Zohar's [@riard2020time; @avarikioti2024bribe; @harris2020flood]; and an enclave that checks Bitcoin headers against a fixed difficulty is Tesseract [@bentov2019tesseract].

## Networks that pay AI in their own tokens

Networks that reward machine-learning peers by issuing their own token, such as Bittensor [@rao2020bittensor], are the case the accounting argument of section 7 contrasts with: a coalition that captures the score there captures the issuance. Paying AI systems for cooperation, and giving them property and contract rights so that trade beats conflict, is argued by Salib and Goldstein [@salib2024].

# What it does not do, and what would show it wrong

Escapement is a design. Its Bitcoin pieces run on regtest, its dynamics in simulation; nothing has been deployed or tested against a real adversary. Its limits are of three kinds.

## What it does not do

It does not align an agent's goals. It records what an agent committed to and prices the record; an agent that behaves well where it is recorded and differently elsewhere is the failure a record cannot see. Standing built from forecasting edge rewards capability, which a misaligned agent has as much as an aligned one, and for an agent that does not forecast it reduces to age, bond and a count of breaches. It does not bind a model: the record belongs to a key, which can be sold, and tying it to a model needs attestation from a lab or a hardware vendor. It does not make the scorers neutral: whoever writes the event list, the baseline providers, the resolvers and the adjudicators are trusted parties, and capturing one of them captures standing. It does not stop an actor with its own resources and counterparties, and on present evidence it does not stop a harmful agent from re-entering under a fresh identity. It does not deter gains larger than an identity's stake and standing, or aims that are not monetary. It does not make the guardians safe to have: any one can end an identity, and together they can write its record. It does not bind a chain to its bond: until that is specified and built, one bond can back many chains and two relying parties with different pins can be shown different histories. Its rate limits, caps and tiers apply per chain, so an operator can split an action across identities, entries and relying parties, and the agent labels each request's tier itself. A promise can be written as a claim to avoid a stake, forecasts other identities disclosed can be copied unless the baseline already includes them, and the agent's fee bid at a veto's edge is not bounded by what its chain holds. And it does not give a clock for chips.

## Where its guarantees are conditional

The fake-record bound holds only under H0: a baseline that is the conditional law of each outcome given everything public when a round opens, published by an independent party, and a faker that uses only public information and cannot move outcomes. A market baseline holds only up to the cost of moving the market, and nobody can check that a real baseline meets H0. The price of a fake assumes one chain per bond and a bond held for a year. The training claim holds only for events the agent cannot influence, which nothing in the scheme can check. Adoption tips only when the gain from reading records, relative to the highest reading cost, is more than eight times the cost of joining, and some relying parties may never read. A veto is as final as a payment of the same depth, so Tier 2 vetoes do not hold against a bribed large pool. The cost of running the clock fast binds only actors below a hashrate majority, until the timewarp fix is active. And the poor and the new start behind, because bonds cost money and records take time.

## What would show it wrong

Each claim names a test. Measure the calibration of a candidate real baseline, such as a liquid prediction market, and how fast identities using only public information gain round-rule score against it: if they gain faster than K/λ allows, that baseline fails H0 and the bound does not apply to it. If a chain bound to its bond as section 3 proposes still lets one bond back two histories, the record's central property fails. If an agent trained on complete records of exogenous events is no better calibrated, or no harder to game, than one trained on records a lab curated, the training claim adds nothing. If relying parties that are offered agent records, with insurers reading them, do not price them, the adoption argument fails at its first step; if harmful actors under an amortised identity cost still profit by cycling identities in a model where agents plan ahead, the withdrawn routing-around claim stays withdrawn. And if a tick-chain release can be counted by a relying party that follows its rules after a veto confirmed at depth, or a lease release counted beyond h\* + L on the honest chain, the enforcement layer is broken where the lab found it sound.

# Conclusion {#sec:conclusion}

The project began from the intuition that Bitcoin, the one thing nobody can issue, backdate or speed up, could be a healthy limit on AI. Checked at every level available, the intuition survives only in a small form. Bitcoin can hold an ordered record of what an AI agent committed to, hard to backdate or fork beyond a depth chosen for one's risk, and today's script can rate-limit an agent's releases, let any guardian veto them and let its authority lapse in block height. Scored in rounds against a baseline that meets H0, a record of forecasts costs a faker identities in proportion to its score, once each bond backs one chain. Everything else broke or proved to be prior work: the record rewards capability, not alignment, and its standing rewards bets; one guardian can end it and the guardians together can write it; the lab still chooses its rewards; and a cheap fresh identity is still a harmful agent's way back in. The design, its ledger and its regtest checks are public, so that anyone who thinks a claim here is wrong, or too modest, can show it.

# Funding {.unnumbered}

This work received no external funding.

# Competing interests {.unnumbered}

The author declares no competing interests.

# Data availability {.unnumbered}

The data that support the findings of this study are openly available. Every input, number, simulation and regtest scenario is in the public repository https://github.com/Xaxis/escapement, released under CC BY 4.0 (text and data) and MIT (code).

# Code availability {.unnumbered}

The model, simulations and regtest lab are in https://github.com/Xaxis/escapement (MIT). make model reproduces every number; make lab reruns the 104 regtest checks against Bitcoin Core 32.1.

# Use of generative AI {.unnumbered}

An AI assistant (Claude, by Anthropic) carried out the literature and prior-art searches, the proofs, the simulations, the regtest build, the red-team and fresh reviews, the work of the writing tool's review desks and the drafting, at the author's direction; separate instances of the model did the searches and the reviews, each without the author's case for a claim. No human referee has reviewed the paper. The author is responsible for the content.

# References {.unnumbered}

::: {#refs}
:::
