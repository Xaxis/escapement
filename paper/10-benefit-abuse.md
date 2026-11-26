# Who benefits, and who could abuse it

A mechanism that decides who is trusted is a mechanism someone will want to control. This section
says who gains from the record, and how each of its parts could be turned against the people it is
meant to protect.

## Who benefits

People and firms who deal with AI agents get a record of what each agent committed to, backed by a
human principal's locked coins, and a way to tell agents apart that does not depend on any agent's
say-so. They do not get recourse: the identity bond can be spent only by its principal, and recourse
would need a coverage bond this paper does not specify.
Agents with real forecasting edge, and their principals, get credit for it that a rival's
marketing or a fraudster's sock puppets cannot cheaply counterfeit. Labs get, on events their agents
cannot move, a training signal their models cannot select after the fact, and a record of what their deployed agents committed to that can serve as evidence of diligence. Insurers get a basis for pricing agent risk. The wider public gets a shared, uneditable
account of what agents committed to and when, on terms that do not depend on trusting any single
operator, lab or state. What the public does not get, on present evidence, is an economy that a
harmful agent cannot re-enter under a fresh identity (section 6).

## Who could abuse it

**Capability without alignment.** Standing measures edge, which capability supplies whether or not an
agent is aligned. A capable misaligned agent therefore earns standing, and the access it brings,
fastest. This is the abuse that matters most for AI safety, and nothing in the design prevents it.

**Surveillance.** Standing requires persistence, and a persistent identity is linkable. Leaves are
hashes and their contents can be disclosed to a scorer rather than to the world, but the pattern of
an identity's entries is public for good. If identities are bound to people, the record is a
surveillance tool. Escapement binds identities to principals only through attestations that relying
parties choose to require; a state that requires those attestations to name citizens has built
something else on top of it.

**Hostage guardians.** Any one guardian can end an identity for good by vetoing to its own key,
and the guardians together can write entries the agent never made (section 8). A state or an
employer that controls one guardian controls whether an agent's record survives; a lab that
chooses all the guardians can put words in its agent's record.

**Training for surprises.** A lab that trains agents on rewards from events the agents can
influence pays them to make outcomes depart from what everyone expected (section 5). The record
would make that training look rigorous.

**Exclusion.** Bonds cost money and records take time. At the reference parameters an identity costs
about [13,000 sats](../research/numbers.md#identity-cost-sats) a year in forgone return and fees, but the bond
itself must be found first, and a new identity starts with no record. The poor and the new start
behind. Sponsorship, in which an insurer or a guardian service funds a newcomer's bond, is the
obvious remedy and the obvious point of capture.

**Capture of the scorer.** Whoever writes the event list, publishes the baseline, resolves claims,
adjudicates promises or decides which actions count as consequential controls standing. These are
registries, whatever the chain under them. A captured resolver or baseline breaks every guarantee in
section 4, and a thin market used as a baseline can be moved. Escapement keeps these roles separate and named in each charter, so that
relying parties can choose whom to trust and can see whom others trusted, but it cannot make the
choice for them.

**Plutocracy.** The cost of faking a record grows with its score, but short records are cheap to fake
for anyone with capital: a rich actor can run many young identities and present the luckiest,
and a record can be bought with its keys. Relying parties have to weigh records by their length and score and read a score as meaningful
only when it exceeds the number of identities in use, a number they cannot observe. The design
cannot force them to.

**Lock-in and social scoring.** A record that everyone needs is a standard someone will try to own,
and a score that decides access can be used to exclude. The defences are structural and partial:
the data is on a chain nobody owns, scoring formulas are chosen by each relying party, and every
formula is computed from the same public history.

**Turning it on people.** Nothing in the record is specific to AI. The same machinery could score
humans' promises and forecasts, with every one of the abuses above. That is a reason to keep it
voluntary, keep contents off chain, and keep the identity of principals out of the protocol.
