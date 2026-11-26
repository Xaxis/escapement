# What it does not do, and what would show it wrong

Escapement is a design. Its Bitcoin pieces run on regtest, its dynamics in simulation; nothing has
been deployed or tested against a real adversary. Its limits are of three kinds.

## What it does not do

It does not align an agent's goals. It records what an agent committed to and prices the record;
an agent that behaves well where it is recorded and otherwise elsewhere is the failure a record of
recorded behaviour cannot see. It does not bind a model: the record belongs to a key, which can be
sold, and tying it to a model needs attestation from a lab or a hardware vendor. It does not make the
scorers neutral: the event list, the baselines, the resolvers and the adjudicators are trusted
parties, and capturing one of them captures standing. It does not stop an actor with its own
resources and counterparties, and on present evidence it does not stop a harmful agent from
re-entering under a fresh identity. It does not deter gains larger than an identity's stake and
standing, or aims that are not monetary. It does not make the guardians safe to have: any one can
end an identity, and together they can write its record. And it does not give a clock for chips.

## Where its guarantees are conditional

The fake-record bound holds only for a baseline that is the conditional law of each outcome given
everything public when a round opens, published by an independent party; a market baseline holds
only up to the cost of moving the market. The training claim holds only for events the agent cannot
influence, which nothing in the scheme can check. Adoption tips only when the gain from reading
records is more than eight times the cost of joining, and some relying parties may never read. A
veto is as final as a payment of the same depth, so Tier 2 vetoes do not hold against a bribed large
pool. The cost of running the clock fast binds only actors below a hashrate majority, until the
timewarp fix is active. And the poor and the new start behind, because bonds cost money and records
take time.

## What would show it wrong

Each claim names a test. If identities without edge, run at scale against a baseline that meets
the condition, produce high round-rule scores more often than K/λ, Theorem 1's application is wrong.
If an agent trained on complete records of exogenous events is no better calibrated, or no harder to
game, than one trained on records a lab curated, the training claim adds nothing. If relying parties
offered agent records with insurers reading them do not price them, the adoption argument fails at
its first step; if harmful actors under an amortised identity cost still profit by cycling
identities in a model where agents plan ahead, the withdrawn routing-around claim stays withdrawn.
And if a tick-chain release can be counted by a relying party that follows its rules after a veto
confirmed at depth, or a lease release counted beyond h* + L on the honest chain, the enforcement
layer is broken where the lab found it sound.
