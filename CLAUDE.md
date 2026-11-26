# CLAUDE.md: Escapement

Escapement: an open research program on whether Bitcoin can help AI safety, and a design that
tests the idea. The thesis under test (recentred 2026-11-26): an AI agent's standing should be an
unforgeable track record, complete and non-backdatable under an identity that costs locked bitcoin,
so that honesty is the cheapest way to earn standing and training rewards cannot be faked; and
verifiable records should make adoption pay for each party that joins. Caps, delays, leases, bonds
and anchored logs are the enforcement layer. Result after six levels of checking: no claim survived as new.
The fake-record bound and adoption model are prior work applied, the tick chain extends prior work
narrowly (per pinned chain), and the single-record, training and routing-around claims are cut;
`research/06-verification.md` has each claim at each level. The research files are the source of truth. README.md
has the layout and how to reproduce.

## Rules that shape every change

- **Nothing invented.** Every number comes from `data/inputs.toml` (each input says whether it is
  measured, a vendor claim, a spec value, a design choice or an assumption, and names its source)
  or is derived in `model/escapement.py`. Documents cite a number as a ledger link,
  `[any text](numbers.md#id)` in research/ or `[any text](../research/numbers.md#id)` in paper/, and
  `make docs` rewrites the link text to the model's value. Never type a model number by hand.
- **Every citation resolves.** Cite as `[@key]`; the key must be in `research/sources.toml` with a
  type and an identifier (DOI, arXiv ID, ISBN or URL). Prefer DOIs and arXiv IDs: Paperwright adds
  sources only by identifier. A source nobody opened is not cited.
- **Credit what exists.** Each idea in the design is marked as prior work, an application of prior
  work, or new, in `research/03-novelty.md`, with the closest prior work and the searches tried.
  "Not found" is a claim about our search, not about the world; say so.
- **Status is honest.** The design is a design. Nothing in it has been deployed or tested against a
  real adversary, and the documents say so wherever it matters.
- **Every contribution passes every level or is cut.** Each claimed contribution in
  `research/04-claims.md` has its result recorded in `research/06-verification.md` for each level:
  an independent prior-art search, a proof, a working build or simulation, a red team, Paperwright's
  desks and a fresh reviewer. A claim that fails a level is cut or downgraded, never argued around.
- **Simulation numbers go through the model.** `model/sim.py` is deterministic; its results enter the
  ledger through `model/escapement.py`, so they are cited as ledger links like any other number.
- **No em dashes** anywhere: research text, code, comments, commit messages. `make check` fails on one.
- **research/notes/ is raw research** from the survey tracks, kept as written. The design and the
  paper cite sources through `research/sources.toml`, not through the notes.

## Commands

```sh
make model     # data/numbers.json and research/numbers.md from inputs and model
make docs      # rewrite every ledger link to the model's value
make check     # em dashes, model reproduces, docs synced, citations and sources identified
make paper     # build/escapement-paper.md, the paper flattened for Paperwright
python3 model/escapement.py --only ID        # one number, its formula and inputs
python3 model/escapement.py --set ID=VALUE   # a variant
```

Gate before committing: `make model docs check` all exit 0.

## Working here

- This repo is **public**. Commit as `Xaxis <396863+Xaxis@users.noreply.github.com>`; the local
  pre-commit and pre-push hooks refuse any other address and block private project names, local
  paths and personal addresses in staged text.
- Python 3.11 or later, standard library only. No site, no deploy: the paper lives in Paperwright
  and the essay on randoblog.
- `.claude/skills/verify/` says how to check each feature; update it in the same commit as a
  feature change.
- License: MIT for code (model/, tools/, root config), CC BY 4.0 for research/, paper/ and data/.
