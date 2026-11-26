# Related work

Escapement is assembled from parts that exist. The searches of section 9 found close precedents for
most of them, and the fresh reviewer found the rest. This section credits them, starting with the
closest.

## Standing and reputation for AI agents

The idea that an AI agent's standing should come from a tamper-proof record backed by a stake is
already in the literature. Chaffer proposes agent-bound tokens whose standing accrues from an
immutable record and a stake [@chaffer2025abt], and Tomašev, Franklin and Osindero make reputation
and staking part of delegating to AI agents, noting that an agent can inflate its reputation by
accepting only easy tasks [@tomasev2026delegation]. Foresight Arena keeps an on-chain forecasting
credential for AI agents, one that cannot be selectively reported or retroactively modified, scored
against market consensus; its sybil resistance is rate limiting, not costly identity, so one
operator with many wallets is the case it leaves open [@nechepurenko2026]. ERC-8004 gives AI agents
identity, reputation and validation registries on Ethereum [@erc8004], and Gatta, Naviglio and
Tarantelli model the exit scams of agents that can abandon their identities [@gatta2026]. Scoring a
missing forecast as the worst outcome is already practice in Infinite Games, a forecasting network
[@infinite-games]. Escapement differs from these in pricing each extra identity with a bond, which
Theorem 1 then counts; like Foresight Arena it leaves an operator free to open many identities, and
charges for each. It also proposed one record as standing, training reward and release gate, which
did not survive (section 9).

## Reputation, sybils and testing forecasters

The logic of the fake-record bound is Resnick and Sami's influence limiter: reputation is the score
gained over the prior prediction, so raters without information gain little, given an attacker that
can create only a bounded number of shills [@resnick2007], which a costly identity is one way to
make true. Friedman and Resnick showed why cheap pseudonyms force everyone to distrust newcomers, and
weighed entry fees against free but unreplaceable pseudonyms [@friedman2001]. Numerai answered an
attack by thousands of accounts hoping to get lucky with staking [@craib2021numerai]. Bonded reputation is Klein and Leffler's and Shapiro's
[@klein1981; @shapiro1983]. Testing a forecaster by its likelihood ratio is game-theoretic
probability [@shafer2019; @shafer2021]; the bound is Ville's [@ville1939]; valid inference on sequential forecasts is developed by Henzi and Ziegel [@henzi2021]; and averaging e-values under
arbitrary dependence, which the round rule uses, is Vovk and Wang's [@vovk2021]. Comparing an
expert with a second forecaster by likelihood is Al-Najjar and Weinstein's comparative test
[@alnajjar2008], and Choe and Ramdas give anytime-valid comparisons of sequential forecasters
[@choe2024]. The many-identity
attack is the analogue of mutual fund incubation [@evans2010], and Foster and Young's result that return histories
cannot separate skill from hidden tail risk [@foster2010] is the objection the round rule answers
for forecasts and does not answer for promises.

## Training on outcomes

Reinforcement learning with proper-score rewards is shown to train calibrated confidence in
language models [@banioharouni2025; @damani2025]; rewards from real-world outcomes are used to
train forecasters [@turtel2025; @han2026futureworld]; selective participation distorts forecasting
incentives [@sempere2021]; sealed and delayed-disclosure evaluation answers selective reporting by
developers [@cheng2025peerbench]; reward tampering is analysed by Everitt and others
[@everitt2019]; and predictions that move their own outcomes are performative prediction
[@perdomo2020], the limit section 5 accepts.

## Adoption

Unraveling under verifiable disclosure is Milgrom's and Grossman's [@milgrom1981; @grossman1981],
with a cost of disclosure Jovanovic's [@jovanovic1982]; the market for lemons is Akerlof's
[@akerlof1970]; multiple equilibria and inertia in the adoption of standards are Farrell and
Saloner's [@farrell1985]; critical mass in two-sided platforms is Evans and Schmalensee's
[@evans2010platform], and insulating tariffs that avoid coordination failure are Weyl's [@weyl2010].
Chan and colleagues advise requiring identifiers for AI systems first in high-stakes settings
[@chan2024ids]. Insurance for AI agents is already offered [@fortune2025aiuc].

## The building blocks of the enforcement layer

Five pieces are used as published and credited as prior work, not contributions. **Lease-gated
authority** for agents is ERC-8370 [@erc8370], and leases themselves are Gray and Cheriton's
[@gray1989]. **Policy co-signing**, a second key that refuses spends outside a policy, is offered
by Nunchuk and others [@nunchuk-blog]. **Bitcoin-anchored logs** are OpenTimestamps
[@todd-ots-2016], a transparency profile for anchoring logs [@fassbender2026], Catena's chain of
spends [@catena-2017] and Pikachu's Taproot checkpoints [@azouvi2022], over Todd's single-use seals
[@todd-2017]. **Slashing for equivocation** is accountable assertions, which reveal a party's Bitcoin
credentials if it equivocates [@ruffing2015], and Babylon, which extracts a key from two signatures
under one nonce [@babylon2023]. **Transparency logs** with monitors and witness cosigning give
non-equivocation without a blockchain [@laurie2013ct; @syta2016], and are the strongest alternative
to the record (section 7). **Chips that run only with fresh
signatures** are Buterin's renewal chips [@buterin2025dacc] and the flexHEG design
[@petrie2025flexheg2], with stockpiled licences their known weakness [@petrie2024].

The tick chain's parts are prior too: Somsen's spacechains, a chain of spends one per block from a
tweaked key with no known secret, enforced by a covenant [@somsen-spacechains]; the single-guardian
cancel of Revault [@revault-intro]; vaults of pre-signed transactions [@swambo2020]; BitVM's
connectors, where a later spend proves no challenge succeeded [@bitvm2-bridge]; fidelity bonds
[@belcher-2019]; Chia's rate-limited wallet [@chia-rl-wallet]; and rate-limiting nullifiers
[@rln-docs]. The lease's predicate is Substrate's
mortal transactions [@substrate-mortality] and Yee's short leash [@yee2022], and a Bitcoin-height
freshness window for signed scores exists [@zeke2026]. Proof of work as a clock is an old
observation [@trubetskoy2018; @gigi2021], and a release timed by it can be advanced only by
overtaking the network's hashrate [@yang2022]; the economics of
attacking it are Budish's [@budish2024]; time-dilation, bribery and flooding attacks on timelocked
protocols are Riard and Naumenko's, Avarikioti and others', and Harris and Zohar's [@riard2020;
@avarikioti2024; @harris2020]; and an enclave that checks Bitcoin headers against a fixed difficulty
is Tesseract [@bentov2019].

## Networks that pay AI in their own tokens

Networks that reward machine-learning peers by issuing their own token, such as Bittensor
[@rao2020bittensor], are the case the accounting argument of section 7 contrasts with: a coalition
that captures the score there captures the issuance. Paying AI systems for cooperation, and giving
them property and contract rights so that trade beats conflict, is argued by Salib and Goldstein
[@salib2024].
