# Adoption: why each party would choose it

A safety mechanism that has to be imposed is only as strong as whoever imposes it. This section asks
whether the record pays for itself at each step, who gains first, how adoption passes the point
where staying out costs more than joining, and what happens to an actor that routes around it.

## Who gains alone

Four kinds of party gain from the record whether or not anyone else adopts it. **Insurers** pricing
agent risk can underwrite an agent with a record more cheaply than one without, and insurance for AI
agents is already sold [@fortune2025aiuc]. **Relying parties with heavy losses from agents** (abused
APIs, payment services, compute sellers) gain at once from pricing or refusing agents without
records. **Agents with good records**, and their principals, get better terms wherever records are
read. **Labs** get a liability defence in their deployed agents' complete records, a training and
evaluation signal that nobody can accuse them of selecting (section 5), and a way to show a
regulator what their agents committed to without showing their weights. Governments gain
enforcement they did not have to build: liability that lands on a principal's own coins, and
evidence for incident investigations that nobody could have edited. They also have reasons to
refuse it, from a preference for registries they control to a wish to identify citizens, and
nothing below assumes they join.

## Staying out comes to cost more than joining

Let an agent's type θ, the value it delivers to relying parties per period, have a continuous
density on the unit interval with mean μ, and let joining cost c per period. Relying parties pay a
verified agent θ and an unverified one the mean type of those who stay out.

**Proposition 11.** If 1 − c exceeds μ, there is an equilibrium in which exactly the types above a
threshold θ* join, where θ* − c equals the mean of the types below θ*. It is unique for every
log-concave density [@bagnoli2005]; for the uniform density θ* = 2c. Every type above θ* loses by
staying out.

This is the unraveling result for verifiable disclosure: when quality can be shown, silence is read
as bad news and everyone but the worst discloses [@milgrom1981; @grossman1981]; with a cost of
disclosure, only types above a threshold do [@jovanovic1982]. The record's role is to make
disclosure verifiable without a certifier anyone has to trust.

## The tipping point

Unraveling assumes relying parties read records, but reading costs them something, and agents gain
from records only where they are read. Let reading cost each relying party a fixed amount drawn
uniformly up to K, let a reader's gain grow with the share x of agents who have records as g·x, and
write a = g/K.

**Proposition 12.** With uniform types, agents join up to the share x = 1 − 2c/z, where z is the
share of transactions with readers, and relying parties read up to z = min(1, a·x). If a < 8c, the
only equilibrium is no adoption. If a > 8c, there are three: no adoption (stable), a tipping point
at x = (1 − √(1 − 8c/a))/2 (unstable) and high adoption at x = (1 + √(1 − 8c/a))/2 (stable). Readers
who read regardless of others remove the no-adoption equilibrium once their share exceeds 2c.

With a joining cost of [0.02](../research/numbers.md#sim-join-cost) of the range of agent value
and a = [0.5](../research/numbers.md#sim-gain-over-k), the tipping point is at
[8.8%](../research/numbers.md#adopt-x-low) of agents and high adoption at
[91%](../research/numbers.md#adopt-x-high); seed readers above
[4%](../research/numbers.md#adopt-seed-threshold) remove the trap. These parameters are
illustrative assumptions, chosen to show the shape of the result, not a forecast. An agent-based
version relaxes the uniform types, reveals each agent's type gradually as its record grows, and adds
[5%](../research/numbers.md#sim-harmful-share) harmful agents who never join. From a
[2%](../research/numbers.md#sim-start-low) start with no seed readers, adoption dies
([0%](../research/numbers.md#sim-adopt-low-noseed)); from
[20%](../research/numbers.md#sim-start-high) it reaches
[95%](../research/numbers.md#sim-adopt-high-noseed); with
[10%](../research/numbers.md#sim-seed-readers) of relying parties reading regardless, it reaches
[95%](../research/numbers.md#sim-adopt-low-seed) from the low start. The parties who gain alone are
exactly the seed readers the result needs.

## Routing around

An actor that will not join can deal with relying parties that do not read records. Proposition 12
says only that readers price such an actor at the mean of the unverified pool, which falls as
adoption grows. Whether routing around becomes costly depends on what happens at the non-readers,
and the simulation shows that it depends on one thing: whether agents can move their business.

Where they cannot, non-readers keep serving every agent at the population's mean terms
([0.45](../research/numbers.md#sim-population-mean)), and a harmful actor routing around them gets
the same ([0.45](../research/numbers.md#sim-harm-terms-nosub)). Routing around then costs nothing,
and the non-readers carry the harm. Where agents can move half their business to whichever relying
party offers them better terms, verified agents leave the non-readers, whose pool worsens, and the
harmful actor's best terms fall to [0.31](../research/numbers.md#sim-harm-terms-partial); with full
substitution, to [-0.50](../research/numbers.md#sim-harm-terms-full), the harm it does, which is to
say it must pay in advance for the damage it causes. The unchecked market becomes a market for
lemons [@akerlof1970] only where business can move.

So the honest statement of the adoption claim is conditional. The record makes the checked economy
safer, makes joining pay once enough parties read records, and makes routing around expensive in
markets where agents can take their business elsewhere. It does nothing about an actor with its own
resources and its own counterparties, about a market with no substitutes, or about a state that
mandates a rival system. It is a way for the legitimate economy to protect itself, not a way to
contain an actor that never needs it.
