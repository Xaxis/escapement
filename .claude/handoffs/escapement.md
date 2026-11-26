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

Final verdicts, after the fresh reviewer (nothing is new):

- **Extends prior work, narrowly:** the tick chain (covenant-free spacechains with Revault's cancel),
  per pinned chain only.
- **Prior work, applied:** the fake-record bound (Ville, union bound, testing by betting; H0 now
  constrains the baseline, the agent's information and its influence); two-sided adoption with seed
  readers (critical mass; a toy model); the height-difference lease (Substrate's mortal
  transactions); the clock's cost (not load-bearing); blockspace (a ceiling on the design, about
  44,000 identities); the building blocks.
- **Cut:** one record as standing, training reward and release gate (chain not bound to bond; the
  round rule is not proper with more than one claim, so standing rewards bets); a training reward
  the lab cannot select; routing around becomes costly; the two-transaction light proof; the chip
  clock.
- **Two regtest breaks by the fresh reviewer, reproduced** (`make lab-fresh-eyes`): one charter id
  carried two tick chains, each accepted from its own pin; the agent evicted a veto at the window's
  edge with a pay-to-anchor child paid from outside the chain.

## Where things are

- `research/04-claims.md`: the claims as repaired, each with what changed and why.
- `research/05-formal.md`: the proofs, second version.
- `research/notes/novelty-independent-a.md`, `-b.md`, `red-team.md`, `fresh-eyes.md`, `paperwright-desks.md`:
  the raw reports of the helpers and the desks, kept as written.
- `model/sim.py`: deterministic simulations; results enter the ledger through `model/escapement.py`.
- `lab/`: the regtest build, `make lab`, 104 checks on Bitcoin Core 32.1; `make lab-fresh-eyes`
  reproduces the two breaks.
- `paper/`: the paper in Markdown; `python3 tools/paper.py --draft` builds what Paperwright takes.

## Open items

- The paper was built and reviewed in a local Paperwright instance that does not persist, so it is
  gone; the owner's live account does not have it. To bring it in: `python3 tools/paper.py --draft`
  gives the sections and tables, `--ids` the identifiers for `add_sources`, and the URL-only sources
  go in as BibTeX. `paper/exports/` holds the final PDF and Markdown.
- Tests that would settle the cut and conditional claims are listed in `paper/12-limits.md`: an
  adoption model with agents that plan ahead and amortised identity costs; a training experiment on
  exogenous events; a baseline provider that meets H0 in practice.
- Binding a chain to its bond (identity = bond outpoint, T_0 an output of the bond's transaction)
  is proposed in `research/02-design.md` and not built.
- Paperwright counts a citation inside a table cell as uncited; sources cited only in a table are
  also cited in prose to work around it.
- The halt output's veto cannot control where a veto pays. Requiring the agent's key in `renew`
  would stop the guardians writing entries alone; that is untested.
