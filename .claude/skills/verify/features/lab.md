# Bitcoin regtest lab

Real transactions on a real bitcoind (the Bitcoin Core release pinned in `lab/bitcoin-core.txt`)
in regtest, one scenario per mechanism in `research/04-claims.md`: the bond (K1), the tick chain
(K7), the release verifier, the height lease (K8), co-signing, anchoring, TRUC fee bumping of a
veto and the Merkle-sum tree. `lab/fetch.py` downloads and verifies the binary and Bitcoin Core's
test framework files into `~/.cache/escapement/`; `lab/run.py` starts a throwaway node, runs every
scenario, writes `lab/results.json` and exits 1 on any failed check.

<!-- covers: cli:lab -->

## Sub-features

- fetch: `lab/fetch.py` (pins in `lab/bitcoin-core.txt`).
- node: `lab/node.py` (fresh datadir under mktemp, `-listen=0`, RPC port 28100 to 28999, stopped
  and deleted on exit or SIGTERM).
- templates: `lab/templates.py` (scripts, NUMS keys, lease message, log and sum trees).
- builder: `lab/chain.py`; verifier: `lab/verify.py` (no RPC); scenarios: `lab/scenarios.py`.

## How to check it

```sh
make lab
python3 lab/run.py --only 3      # one scenario; 3 needs 2's chains, so run --only 2 --only 3
ps -eo pid,args | grep '[e]scapement-regtest' || echo "no lab node left"
```

Expect: `make lab` prints every check as PASS, then the size table, then "N of N checks passed"
and "wrote lab/results.json", in about 30 s after the first fetch (about 90 MB), and exits 0; a
failed check prints FAIL with the expected and observed outcome and exits 1. Afterwards no
bitcoind with an `escapement-regtest` datadir is left running and no such datadir is left in the
temp directory.
