# Escapement

An open research program on one question: can Bitcoin, the one scarce and unforgeable thing we
know, act as a safety limit on AI?

In a mechanical clock the escapement lets a mainspring's energy out one counted tick at a time,
and keeps the time. Escapement asks two things of Bitcoin. For alignment: can its scarcity, its
clock and its unforgeable costs shape what AI agents are trained and rewarded to do, by making an
agent's standing a **complete track record** (ordered, non-backdatable, under an identity that costs
locked bitcoin)? For adoption: would labs, companies, agents and governments choose it because it
pays them? The earlier mechanisms (caps, delays, leases, bonds, anchored logs) are the enforcement
layer under that record.

What survived checking is narrower than what was proposed. Under a stated condition on the baseline,
a record of forecasts scored in rounds costs an agent without edge a number of identities that grows
with the score; on events the agent cannot influence, it gives a training reward nobody can select
after the fact; and adoption has a tipping point that parties who gain alone can push past. The
claim that staying out comes to cost a harmful actor more than joining was cut, as were a light
proof of releases and Bitcoin as a clock for AI chips. `research/06-verification.md` has each claim's
result at every level.

## Status

**A design, not a result.** Nothing here has been deployed or tested against a real adversary. The
economic claims are proved in `research/05-formal.md` and checked by simulation, the Bitcoin pieces
run on regtest in `lab/`, and each claim's result at every level of checking (an independent
prior-art search, proof, build, red team, paper review, a fresh reviewer) is in
`research/06-verification.md`. Anything that failed a level was cut or downgraded. The model
computes what the design's parameters cost and allow; it does not show that the design makes any AI
safer.

## Layout

```
research/notes/     the survey tracks, raw, with their sources
research/01-survey.md      what exists: the mechanisms, tested against an adversary and against Bitcoin's limits
research/02-design.md      the design: charters, bonds, leases, the ladder, seals, seasoning, adjudication
research/03-novelty.md     each idea against the literature
research/04-claims.md      the claims under test, stated precisely
research/05-formal.md      the formal statements and proofs
research/06-verification.md  each claim's result at every level of checking
research/numbers.md        the ledger: every number, generated, never edited by hand
research/sources.toml      every source, with its identifier
data/inputs.toml           every input, with its basis (measured, vendor, spec, design, assumption)
model/                     the model that derives every other number, and model/sim.py, the simulations
lab/                       the Bitcoin pieces on regtest, with real scripts and transactions
paper/                     the paper, in Markdown, built for Paperwright by tools/paper.py
tools/                     docs sync, the repository check, the paper build
```

## Reproduce

You need Python 3.11 or later; nothing else for the model. `make lab` also downloads Bitcoin Core
32.1 (checked against a pinned hash) into `~/.cache/escapement/` and runs a throwaway regtest node.

```sh
make model                                   # every number, from inputs and model
make docs                                    # write those numbers into the documents
make check                                   # em dashes, reproducibility, sync, every citation
make lab                                     # the Bitcoin pieces on regtest: 104 checks
python3 model/sim.py                         # the simulations
python3 model/escapement.py --only season-days
python3 model/escapement.py --set tier3-delay-blocks=288
```

## Licence

Code is MIT; text and data are CC BY 4.0. See [LICENSE](LICENSE).
