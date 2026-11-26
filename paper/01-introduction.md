# Introduction

Most proposals to use Bitcoin for AI safety are proposals to cap an agent: a wallet with a limit, a
delay before large payments, a bond forfeited on misbehaviour. Caps are useful and old, and they
share a weakness. They act after the fact, on an agent whose goals they do not touch, and they bind
only where someone imposes them. This paper started from two harder questions. Can Bitcoin's
properties help shape what AI agents are trained and rewarded to do, rather than only fence them in?
And would the parties who matter (labs, firms, relying parties, insurers and governments) choose to
use it because it pays or protects them?

It is a design study, and its result is mostly negative. Nothing in it has been deployed or tested
against a real adversary. A design was proposed, every claim was put through six levels of
checking, and whatever failed a level was cut or downgraded rather than argued back. Little
survived, and what broke is the more useful half.

Bitcoin offers four things that are hard to fake: coins no one can issue; a block order that grows
costly to rewrite with depth and that only a hashrate majority could rewrite at will; the single
spending of each output; and a clock that runs faster only with more hashrate. Section 2 states
exactly what Bitcoin's rules enforce and what they do not.

## The proposal

Escapement computes an agent's standing in part from its **record**: an ordered sequence, hard to
backdate beyond a depth chosen for one's risk, of the commitments it put on chain (forecasts,
promises with stakes, requests for consequential actions), which relying parties that follow its
rules require for anything they rely on. It is committed on Bitcoin under an identity backed by
locked bitcoin (section 3), it is complete only for a verifier that walks the whole chain, and its
guardians together can write entries the agent never made (section 8). It hoped for three consequences: that faking a record would cost identities in
proportion to its score (section 4), that a lab could train on rewards nobody could select after the
fact (section 5), and that adoption would pay each party that joined (section 6). Section 7 asks why
Bitcoin rather than a registry or a witnessed log, and section 8 describes the enforcement layer: a
chain of outputs per identity that rate-limits the release of an agent's commitments and lets any
guardian veto it, and a lease that lapses in block height.

## What survived

No mechanism or theorem in this paper is new. Section 9 gives each claim's result at every level,
and section 11 credits the prior work.

- **Extends prior work, narrowly:** the tick chain, a covenant-free version of Somsen's spacechains
  with Revault's cancel, whose properties hold per pinned chain, not per identity.
- **Prior work, applied:** the fake-record bound (Ville's inequality, a union bound and testing by
  betting), now stated with the conditions it needs; two-sided adoption with seed readers (critical
  mass), as a toy model; the height-difference lease (Substrate's mortal transactions); the cost of
  running Bitcoin's clock fast; blockspace as a ceiling on the design; and the building blocks of
  section 8.
- **Cut:** one record serving as standing, training reward and release gate, since nothing binds a
  chain to its bond and the two uses ask for different reports; a training reward the lab cannot
  select; routing around the record becoming costly; a light proof of releases; Bitcoin headers as a
  licence clock for AI chips.

What broke is the paper's main contribution, and section 9 lists it: claims that move together, and
hidden tail risk, defeat a product of likelihood ratios; the round rule that repairs it rewards bets
rather than forecasts; a record of edge routes trust to capability, not alignment; a reward on
outcomes the agent can move pays for manipulation; a simulation that barred harmful actors from
joining hid that they cycle identities; transaction-id proofs pass a release no guardian signed; and
neither a chain's pin nor an agent's fee bid at a veto's edge is bounded by anything on chain.
Section 10 says who benefits and who could abuse the design, section 12 what it does not do and what
would show it wrong, and section 13 concludes.
