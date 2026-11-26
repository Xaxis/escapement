# Model

Every derived number, computed from `data/inputs.toml` by `model/escapement.py` through
`model/ledger.py`, with its formula, inputs, basis and the line that defines it.

<!-- covers: cli:model, job:make-model -->

## Sub-features

- all: `python3 model/escapement.py` prints every number with its basis.
- only: `--only ID` prints one number, its formula, each input's value and where it is defined.
- set: `--set ID=VALUE` (repeatable) reruns with an input changed; an unknown ID is an error.
- json: `--json` prints the ledger as JSON.
- write: `--write` (= `make model`) writes `data/numbers.json` and `research/numbers.md`.

## How to check it

```sh
python3 model/escapement.py --only tier2-delay-p-under-half; echo "exit $?"
python3 model/escapement.py --set tier2-delay-blocks=12 | grep tier2-delay-mean-min
python3 model/escapement.py --set no-such-input=1; echo "exit $? (expect a KeyError)"
make model && git diff --stat data/numbers.json research/numbers.md
```

Expect: the first prints the value with its two inputs and exits 0; the second shows 120 minutes;
the third fails naming the unknown input; the last shows no diff when inputs did not change.
