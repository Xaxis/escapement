# Bitcoin regtest lab

Real transactions on a real bitcoind (the Bitcoin Core release pinned in `lab/bitcoin-core.txt`)
in regtest, one scenario per mechanism in `research/04-claims.md`: the bond (K1), the tick chain
(K7), the release verifier, the height lease (K8), co-signing, anchoring, TRUC fee bumping of a
veto and the Merkle-sum tree. `lab/fetch.py` downloads and verifies the binary and Bitcoin Core's
test framework files into `~/.cache/escapement/`; `lab/run.py` starts a throwaway node, runs every
scenario, writes `lab/results.json` and exits 1 on any failed check.

<!-- covers: cli:lab, cli:lab-fresh-eyes -->

## Sub-features

- fetch: `lab/fetch.py` (pins in `lab/bitcoin-core.txt`).
- node: `lab/node.py` (fresh datadir under mktemp, `-listen=0`, RPC port 28100 to 28999, stopped
  and deleted on exit or SIGTERM).
- templates: `lab/templates.py` (scripts, NUMS keys, lease message, log and sum trees).
- builder: `lab/chain.py`; verifier: `lab/verify.py` (no RPC); scenarios: `lab/scenarios.py`.
- fresh eyes: `lab/fresh_eyes.py` (`make lab-fresh-eyes`), the fresh reviewer's two breaks of the
  tick chain, kept outside `make lab` and its checks because it records what fails.

## How to check it

```sh
make lab
python3 lab/run.py --only 3      # one scenario; 3 needs 2's chains, so run --only 2 --only 3
ps -eo pid,args | grep '[e]scapement-regtest' || echo "no lab node left"
make lab-fresh-eyes             # the fresh reviewer's two breaks
```

Expect: `make lab` prints every check as PASS, then the size table, then "N of N checks passed"
and "wrote lab/results.json", in about 30 s after the first fetch (about 90 MB), and exits 0; a
failed check prints FAIL with the expected and observed outcome and exits 1. Afterwards no
bitcoind with an `escapement-regtest` datadir is left running and no such datadir is left in the
temp directory.

`make lab-fresh-eyes` prints two `BREAK:` lines and exits 0: an outside-money child paying
150,000 sats evicts a veto package and the release is counted, and two chains under one charter id
are each accepted from their own pin. A `HELD:` line instead means the attack failed, which would
change what research/06-verification.md records. It exits non-zero only on a crash, and leaves no
node running.
