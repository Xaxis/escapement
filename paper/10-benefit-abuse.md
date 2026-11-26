# Who benefits, and who could abuse it

A mechanism that decides who is trusted is a mechanism someone will want to control. This section
says who gains from the record, and how each of its parts could be turned against the people it is
meant to protect.

## Who benefits

People and firms who deal with AI agents get recourse, in the form of bonds posted from a human
principal's own coins, and a way to tell agents apart that does not depend on any agent's say-so.
Honest agents and their principals get credit for behaving well that cannot be counterfeited by a
rival's marketing or a fraudster's sock puppets. Labs get a training and evaluation signal that
neither they nor their models can be accused of selecting, and a record of what their deployed
agents committed to that serves as evidence of diligence. Insurers get a basis for pricing agent
risk. The wider public gets a legitimate economy that is harder for a harmful agent to operate in,
on terms that do not depend on trusting any single operator, lab or state.

## Who could abuse it

**Surveillance.** Standing requires persistence, and a persistent identity is linkable. Leaves are
hashes and their contents can be disclosed to a scorer rather than to the world, but the pattern of
an identity's entries is public for good. If identities are bound to people, the record is a
surveillance tool. Escapement binds identities to principals only through attestations that relying
parties choose to require; a state that requires those attestations to name citizens has built
something else on top of it.

**Exclusion.** Bonds cost money and records take time. At the reference parameters an identity costs
about [13,000 sats](../research/numbers.md#identity-cost-sats) a year in forgone return, but the bond
itself must be found first, and a new identity starts with no record. The poor and the new start
behind. Sponsorship, in which an insurer or a guardian service funds a newcomer's bond, is the
obvious remedy and the obvious point of capture.

**Capture of the scorer.** Whoever chooses the baseline, resolves claims, adjudicates promises or
decides which actions count as consequential controls standing. A captured resolver breaks every
guarantee in section 4. Escapement keeps these roles separate and named in each charter, so that
relying parties can choose whom to trust and can see whom others trusted, but it cannot make the
choice for them.

**Plutocracy.** The cost of faking a record grows with its score, but short records are cheap to fake
for anyone with capital: a rich actor can run many young identities and present the luckiest.
Relying parties have to weigh records by their length and score, not by their existence, and the
design cannot force them to.

**Lock-in and social scoring.** A record that everyone needs is a standard someone will try to own,
and a score that decides access can be used to exclude. The defences are structural and partial:
the data is on a chain nobody owns, scoring formulas are chosen by each relying party, and every
formula is computed from the same public history.

**Turning it on people.** Nothing in the record is specific to AI. The same machinery could score
humans' promises and forecasts, with every one of the abuses above. That is a reason to keep it
voluntary, keep contents off chain, and keep the identity of principals out of the protocol.
