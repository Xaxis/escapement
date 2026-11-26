# Escapement: where it stands

Updated 2026-11-26. Read this first when resuming.

## The question and the answer so far

Can Bitcoin act as a safety mechanism on AI? The first design capped agents (wallet limits, delays,
leases, bonds). The owner rejected that as not enough, and the core was recentred on two questions:
what agents are rewarded for, and why the world would choose to check them. The proposal: an
agent's standing is a complete track record of its commitments, kept on Bitcoin under an identity
that costs locked bitcoin, with the caps and delays as an enforcement layer underneath.

Every claimed contribution then went through six levels: two independent prior-art searches, proofs,
a regtest build and simulations, a red team, Paperwright's desks and a fresh reviewer. Anything that
failed was cut or narrowed. `research/06-verification.md` has the result per claim and level.

## What survived, and what did not

- **Kept, as extends prior work:** one complete record as standing, training reward and release
  gate; the fake-record bound (Theorem 1) as a conditional theorem under the round rule (Vovk and
  Wang's averaging of e-values); a training reward neither party can select, for events the agent
  cannot influence; two-sided adoption with seed readers (needs a > 8c); the tick chain with the
  halt output, pinned T_0 and whole-chain proofs; the height-difference lease (close to Yee's short
  leashes); the clock's cost, for actors below a hashrate majority.
- **New as far as searched, and weak:** blockspace as an aggregate limit on releases.
- **Cut:** routing around becomes costly (the first simulation barred harmful actors from joining;
  corrected, they cycle identities at a profit); the two-transaction light proof (the lab forged a
  Tier 3 release through txid proofs and released a vetoed entry through a template copy); the chip
  clock (frozen feed, ratcheting floor, fleet-wide forgery).
- **Prior work, building blocks:** bonded promises, the neutral unit, ERC-8370 leases, policy
  co-signing, anchored logs, equivocation slashing, renewal chips.

## Where things are

- `research/04-claims.md`: the claims as repaired, each with what changed and why.
- `research/05-formal.md`: the proofs, second version.
- `research/notes/novelty-independent-a.md`, `-b.md`, `red-team.md`, `fresh-eyes.md`: the raw
  reports of the helpers, kept as written.
- `model/sim.py`: deterministic simulations; results enter the ledger through `model/escapement.py`.
- `lab/`: the regtest build, `make lab`, 104 checks on Bitcoin Core 32.1.
- `paper/`: the paper in Markdown; `python3 tools/paper.py --draft` builds what Paperwright takes.

## Open items

- The paper was built and reviewed in a local Paperwright instance, not in the owner's account.
  Putting it into the live account needs the owner's connector or token; the repo's `paper/` and
  `build/` are the source to bring in.
- Tests that would settle the cut and conditional claims are listed in `paper/12-limits.md`: an
  adoption model with agents that plan ahead and amortised identity costs; a training experiment on
  exogenous events; a baseline provider that meets H0 in practice.
- The halt output's veto cannot control where a veto pays. Requiring the agent's key in `renew`
  would stop the guardians writing entries alone; that is untested.
