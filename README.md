# Escapement

An open research program on one question: can Bitcoin, the one scarce and unforgeable thing we
know, act as a safety limit on AI?

In a mechanical clock the escapement lets a mainspring's energy out one counted tick at a time.
It does not weaken the spring. Escapement asks the same of Bitcoin and AI: not to cap what a model
can think or compute, which Bitcoin cannot do, but to meter what an AI agent can spend, commit to
and bind itself to, and how fast, on a clock no machine can run faster.

## Status

**A design, not a result.** Nothing here has been deployed or tested against a real adversary. The
model computes what the design's parameters cost and allow; it does not show that the design makes
any AI safer. Every idea is marked as prior work, an application of prior work, or new, with the
closest prior work and the searches behind each verdict.

## Layout

```
research/notes/     the survey tracks, raw, with their sources
research/01-survey.md      what exists: the mechanisms, tested against an adversary and against Bitcoin's limits
research/02-design.md      the design: charters, bonds, leases, the ladder, seals, seasoning, adjudication
research/03-novelty.md     each idea against the literature
research/numbers.md        the ledger: every number, generated, never edited by hand
research/sources.toml      every source, with its identifier
data/inputs.toml           every input, with its basis (measured, vendor, spec, design, assumption)
model/                     the model that derives every other number
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
