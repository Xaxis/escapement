# Abstract

Bounding what an AI agent can do is not enough; the harder questions are what agents are rewarded
for and why anyone would adopt the means of checking them. This paper asks what Bitcoin can
contribute to both. It designs Escapement, in which an agent's standing is computed in part from a
track record of its commitments, kept on Bitcoin under an identity backed by locked coins, with rate
limits, vetoes and leases built from today's script. Every claimed contribution was then checked at
six levels: two prior-art searches, proofs, a regtest build of [104 checks](../research/numbers.md#lab-checks) with
simulations, a red team, editorial review and a fresh reviewer. None survived as new. The bound on
faking a record of forecasts is prior work, holds only for fakers that use public information alone
and cannot move outcomes, and rewards bets rather than calibrated forecasts and capability rather
than alignment. Nothing on chain yet binds a record to its identity's bond, so one bond can back many
records. A training reward that the lab cannot select was not achieved. Adoption tips only in a toy
model with unmeasured parameters, routing around the record was not made costly, and the lease is
Substrate's mortal transactions. One part extends prior work narrowly: a covenant-free chain of
outputs that rate-limits an agent's releases and lets any guardian veto them, though one guardian can
end an identity and the guardians together can write its record. Nothing has been deployed or tested
against a real adversary. The paper's value is in what broke, and why.
