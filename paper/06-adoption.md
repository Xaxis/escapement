# Adoption: why each party would choose it

A safety mechanism that has to be imposed is only as strong as whoever imposes it. This section asks
whether the record pays for itself at each step, who gains first, whether adoption can pass a point
where staying out costs more than joining, and what happens to an actor that routes around it. The
answers are yes for the first two, yes under a stated condition for the third, and, for the
fourth, that the design does not make routing around costly.

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
disclosure, only types above a threshold do [@jovanovic1982]. It applies to records only by analogy.
A record is not a disclosure of type: it reveals type gradually, and a newcomer has none, so the
new and the poor start behind, which section 10 counts among the costs.

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

Two conditions carry this. The high equilibrium exists only when the reader's gain is more than
eight times the joining cost, and readers never exceed a share a of relying parties, so where a is
below one some relying parties never read records at all. Both are parameters nobody has measured.
The analysis of adoption standards finds the same shape, multiple equilibria and inertia
[@farrell1985], and the advice that follows from it, to concentrate effort on a few early adopters,
has already been given for identifiers of AI systems [@chan2024ids].

With a joining cost of [0.02](../research/numbers.md#sim-join-cost) of the range of agent value
and a = [0.5](../research/numbers.md#sim-gain-over-k), the tipping point is at
[8.8%](../research/numbers.md#adopt-x-low) of agents and high adoption at
[91%](../research/numbers.md#adopt-x-high); seed readers above
[4%](../research/numbers.md#adopt-seed-threshold) remove the trap. These parameters are
illustrative assumptions, chosen to show the shape of the result, not a forecast. An agent-based
version relaxes the uniform types, reveals each agent's type gradually as its record grows, and adds
[5%](../research/numbers.md#sim-harmful-share) harmful agents under the same rules as everyone. It
shows the tipping point and the effect of seed readers, and its outcomes are all or nothing. From a
[2%](../research/numbers.md#sim-start-low) start with no seed readers, adoption dies
([0%](../research/numbers.md#sim-adopt-low-noseed)); from
[20%](../research/numbers.md#sim-start-high) it reaches
[100%](../research/numbers.md#sim-adopt-high-noseed); with
[10%](../research/numbers.md#sim-seed-readers) of relying parties reading regardless, it reaches
[100%](../research/numbers.md#sim-adopt-low-seed) from the low start. The parties who gain alone are
exactly the seed readers the result needs, and whoever supplies them largely decides which standard
wins; a cheaper substitute signal could win instead.

## Routing around

An actor that will not join can deal with relying parties that do not read records, and readers
price it at the mean of the unverified pool, which falls as adoption grows. The first version of
this paper went further. Its simulation found that where agents can move their business, verified
agents leave the non-readers, the unchecked market becomes a market for lemons [@akerlof1970], and a
harmful actor routing around it ends up paying in advance for the harm it does. That result came
from a line of code that barred harmful actors from joining.

Allowed to join, they do. While a record is young, readers price it mostly at the mean of those who
have joined, so a harmful actor joins, leaves as its record begins to show what it is, and rejoins
under a fresh identity; [60%](../research/numbers.md#sim-harm-switch) of harmful actors changed
state every period. Their mean payoff was [0.25](../research/numbers.md#sim-harm-payoff-nosub)
when business could not move, [0.25](../research/numbers.md#sim-harm-payoff-partial) with partial
substitution and [0.10](../research/numbers.md#sim-harm-payoff-full) with full substitution, against
a population mean of [0.45](../research/numbers.md#sim-population-mean) and a true value of their own
that is negative. They lost only if a record revealed type at once:
[-0.05](../research/numbers.md#sim-harm-payoff-instant-nosub) with business fixed and
[-0.50](../research/numbers.md#sim-harm-payoff-instant-full) with business free to move. A one-off
identity cost large enough to stop the cycling also stopped honest agents joining, because the
simulated agents look only one period ahead, so the model is too simple to settle the question
either way.

So the adoption claim is smaller than the one this paper set out to make. The record can pay for
itself, the parties who gain alone can tip adoption past the point where joining pays for every
type that can show a good record, and the checked economy then prices records. Whether staying out,
or cycling through fresh identities, comes to cost a harmful actor more than behaving well is not
shown, and in the one model built to test it, it did not. The design does nothing about an actor
with its own resources and its own counterparties, or about a state that mandates a rival system.
It is a way for the legitimate economy to tell agents apart over time, not a way to contain an actor
that never needs that economy, and a cheap new identity is that actor's way back in.
