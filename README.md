# Escapement

An open research program on one question: can Bitcoin, the one scarce and unforgeable thing we
know, act as a safety limit on AI?

In a mechanical clock the escapement lets a mainspring's energy out one counted tick at a time,
and keeps the time. Escapement asks two things of Bitcoin. For alignment: can its scarcity, its
clock and its unforgeable costs shape what AI agents are trained and rewarded to do, by making an
agent's standing an **unforgeable track record** (complete, non-backdatable, under an identity that
costs locked bitcoin) that is cheap to earn honestly and expensive to fake? For adoption: would
labs, companies, agents and governments choose it because it pays them, with staying out coming to
cost more than joining? The earlier mechanisms (caps, delays, leases, bonds, anchored logs) are the
enforcement layer under that record.

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

You need Python 3.11 or later; nothing else.

```sh
make model                                   # every number, from inputs and model
make docs                                    # write those numbers into the documents
make check                                   # em dashes, reproducibility, sync, every citation
python3 model/escapement.py --only season-days
python3 model/escapement.py --set tier3-delay-blocks=288
```

## Licence

Code is MIT; text and data are CC BY 4.0. See [LICENSE](LICENSE).
