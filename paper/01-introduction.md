# Introduction

Most proposals to use Bitcoin for AI safety are proposals to cap an agent: a wallet with a limit, a
delay before large payments, a bond forfeited on misbehaviour. Caps are useful and old, and they
share a weakness. They act after the fact, on an agent whose goals they do not touch, and they bind
only where someone imposes them. This paper starts from two harder questions. Can Bitcoin's
properties help shape what AI agents are trained and rewarded to do, rather than only fence them in?
And would the parties who matter, labs, firms, relying parties, insurers and governments, choose to
use it because it pays or protects them?

Bitcoin offers four things nobody can fake: its coins, which no one can issue; the order and height
of its blocks, which no one can backdate; its single spending of each output, which no one can fork;
and the work behind its clock, which no one can run faster without matching the network's hashrate.
Section 2 states exactly what those rules enforce and what they do not.

## The proposal

Escapement makes an agent's standing a function of its **record**: an ordered, gapless,
non-backdatable sequence of the commitments it asked anyone to rely on (forecasts, promises with
stakes, requests for consequential actions), committed on Bitcoin under one identity that costs
locked bitcoin (section 3). Three consequences are argued, each only under its conditions.

1. **Faking a record costs identities.** Scored in rounds against a baseline that meets a stated
   condition, a record of forecasts with score λ costs an agent without edge at least πλ identities
   for a chance π of success (section 4).
2. **A reward nobody selects.** On events whose outcomes the agent cannot influence, a lab can train
   on rewards computed from the complete record, which neither the agent nor the lab can select
   after the fact (section 5).
3. **Adoption with a tipping point.** Reading records and keeping them are strategic complements,
   and the parties who gain from records regardless of others can push adoption past the tipping
   point when the gain from reading is large enough relative to the cost of joining (section 6).

Section 7 asks why Bitcoin rather than a registry, and section 8 describes the enforcement layer: a
chain of outputs per identity that rate-limits and lets any guardian veto the release of an agent's
commitments, and a lease that lapses in block height without anyone's clock.

## Contributions, and how far each survived

No single mechanism or theorem in this paper is new; every part has a precedent, and section 11
credits them. What two independent searches did not find is the integration and a few narrow
elements. Each was then proved, built or simulated, attacked by a red team, and reviewed, and
section 9 gives the result at every level. In short:

- **Extends prior work:** one complete record serving as standing, training reward and release
  gate, complete against an operator's many identities; the fake-record bound priced with a Bitcoin
  bond, kept only as a conditional theorem after the red team broke its first form; a training
  reward neither party can select, kept only for events the agent cannot move; two-sided adoption
  with seed readers; the tick chain, without the light proof the build broke; the height-difference
  lease, which held as stated; the cost of running Bitcoin's clock fast, for actors below a hashrate
  majority.
- **New as far as the searches found, and weak:** blockspace as an aggregate limit on releases.
- **Cut:** that routing around the record becomes costly for a harmful actor; a light proof of a
  release; Bitcoin headers as the licence clock of AI chips.
- **Prior work, used as building blocks:** bonded promises, the neutrality of a fixed-supply unit,
  lease-gated agent authority, policy co-signing, anchored logs, equivocation slashing and renewal
  chips.

Section 10 says who benefits and who could abuse the design, section 12 what it does not do and what
would show it wrong, and section 13 concludes. Nothing in this paper has been deployed or tested
against a real adversary.
