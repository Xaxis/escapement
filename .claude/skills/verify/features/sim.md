# Simulations

The simulations behind `research/05-formal.md`: record faking against Ville's bound, correlated
claims under the product rule and the round rule, a learner under complete and selective records,
two-sided adoption with harmful actors (who may join, like everyone) and business substitution,
and veto censorship. `model/sim.py` is deterministic for a given seed; its results
enter the ledger through `model/escapement.py`.

<!-- covers: cli:sim -->

## Sub-features

- record faking: `record_faking`, `record_selective`, `record_skilled`, `record_correlated`,
  `record_skilled_rounds`.
- training: `training("complete" | "selective", ...)`.
- adoption: `adoption(...)` (agent-based) and `adoption_analytic(...)` (Proposition 12).
- veto censorship: `veto_censorship(...)`.

## How to check it

```sh
python3 model/sim.py
python3 model/escapement.py --only sim-fake-p
python3 model/escapement.py --only sim-corr-round-p
python3 model/escapement.py --set sim-tenure-tau=0 | grep sim-harm-payoff-full
make model && git diff --stat data/numbers.json
```

Expect: the first prints each result in a few seconds, with the record-faking share close to its
exact value and below its bound, the correlated attack near 100% under the product rule and below
its 1.6% bound under the round rule, the complete-record learner near a = 1, the selective learner
far above it, adoption at 0% from the low start without seed readers and 100% with them, and the
harmful payoff negative only when type is revealed at once; the second shows the simulated share
with its formula; the third shows the round-rule share under the bound; the fourth shows the
harmful actor's payoff with full substitution falling to about -0.5 when records reveal type at
once; the last shows no diff when nothing changed.
