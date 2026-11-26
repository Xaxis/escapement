# Simulations

The simulations behind `research/05-formal.md`: record faking against Ville's bound, a learner
under complete and selective records, two-sided adoption with harmful actors and business
substitution, and veto censorship. `model/sim.py` is deterministic for a given seed; its results
enter the ledger through `model/escapement.py`.

<!-- covers: cli:sim -->

## Sub-features

- record faking: `record_faking`, `record_selective`, `record_skilled`.
- training: `training("complete" | "selective", ...)`.
- adoption: `adoption(...)` (agent-based) and `adoption_analytic(...)` (Proposition 12).
- veto censorship: `veto_censorship(...)`.

## How to check it

```sh
python3 model/sim.py
python3 model/escapement.py --only sim-fake-p
python3 model/escapement.py --set sim-substitution-partial=0.9 | grep sim-harm-terms-partial
make model && git diff --stat data/numbers.json
```

Expect: the first prints each result in about two seconds, with the record-faking share close to
its exact value and below its bound, the complete-record learner near a = 1, the selective learner
far above it, and adoption at 0% from the low start without seed readers and about 95% with them;
the second shows the simulated share with its formula; the third shows the harmful actor's terms
falling as substitution rises; the last shows no diff when nothing changed.
