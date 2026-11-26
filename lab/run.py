#!/usr/bin/env python3
"""Run every lab scenario on a throwaway regtest bitcoind and write lab/results.json.

  python3 lab/run.py              everything (what `make lab` runs); exits 1 on any failed check
  python3 lab/run.py --only 3     scenarios whose name starts with 3 (results.json is not written)
  python3 lab/run.py --keep       keep the node's datadir for inspection

The node is stopped and its datadir deleted when the run ends, whether it passed or not.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

import fetch

BINARY, _ = fetch.ensure()

from chain import Lab  # noqa: E402
from node import Node  # noqa: E402
import scenarios  # noqa: E402

HERE = Path(__file__).resolve().parent


def size_table(sizes: list[dict]) -> list[dict]:
    """One row per kind of transaction: its sizes are deterministic, so the first is the row."""
    seen: dict[str, dict] = {}
    for row in sizes:
        seen.setdefault(row["kind"], row)
    return list(seen.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[], help="run scenarios whose name starts with this")
    ap.add_argument("--keep", action="store_true", help="keep the node's datadir")
    args = ap.parse_args()
    pins = fetch.pins()
    with Node(BINARY, keep=args.keep) as node:
        lab = Lab(node)
        print(f"bitcoind {node.rpc('getnetworkinfo')['subversion']} regtest, RPC on 127.0.0.1:{node.port}")
        lab.setup()
        for name, fn in scenarios.ALL:
            if args.only and not any(name.startswith(o) for o in args.only):
                continue
            lab.scenario = name
            print(f"== {name}", flush=True)
            try:
                fn(lab)
            except Exception as e:
                traceback.print_exc()
                lab.record("scenario ran to completion", "no exception", False, f"exception: {e!r}")
        tip = lab.height()
        if args.keep:
            print(f"datadir kept at {node.tmp}")

    failed = [c for c in lab.checks if not c["pass"]]
    sizes = size_table(lab.sizes)
    print()
    print(f"{'vB':>5} {'WU':>5} {'fee':>6}  transaction")
    for row in sizes:
        print(f"{row['vbytes']:>5} {row['weight']:>5} {row['fee_sat']:>6}  {row['kind']}")
    print()
    print(f"{len(lab.checks) - len(failed)} of {len(lab.checks)} checks passed, final height {tip}")
    for c in failed:
        print(f"FAIL [{c['scenario']}] {c['check']}: expected {c['expectation']}; observed {c['observed']}")
    if not args.only:
        results = {
            "bitcoin_core": {"version": pins["version"], "tarball": pins["tarball"],
                             "tarball_sha256": pins["tarball_sha256"], "framework_tag": pins["tag"]},
            "parameters": {
                "n2_blocks": lab.n2, "n3_blocks": lab.n3, "lease_blocks": lab.lease,
                "season_blocks": lab.season, "d_confirmations": lab.d, "bond_min_sats": lab.bond_min,
                "entry_cap_sats": lab.cap, "feerate_sat_vb": lab.feerate, "guardians": 3,
                "source": "data/numbers.json (the model's ledger)",
            },
            "summary": {"checks": len(lab.checks), "passed": len(lab.checks) - len(failed),
                        "failed": len(failed), "final_height": tip},
            "checks": lab.checks,
            "sizes": sizes,
            **lab.extra,
        }
        (HERE / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print("wrote lab/results.json")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
