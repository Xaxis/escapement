#!/usr/bin/env python3
"""Two breaks the fresh reviewer found in the tick chain, rerun on a throwaway regtest node.

  python3 lab/fresh_eyes.py       (or: make lab-fresh-eyes)

1. The agent's bid at the window's edge is not bounded by T_n's value. An advance may carry a
   pay-to-anchor output beside T_{n+1}, and a child spending it can pay from a coin outside the
   chain, so the agent outbids the watchtower's veto package with outside money.
2. Nothing on chain binds a tick chain to its identity. Two chains under one charter id, with
   different roots at entry 1, are each accepted by the release verifier from their own pin.

Each finding prints as a "BREAK:" line when the attack succeeds, or "HELD:" when it fails. The
script exits non-zero only if it crashes. It uses only the lab's own modules, and the node is
stopped and its datadir deleted when it ends.
"""

from __future__ import annotations

import sys

import fetch

BINARY, _ = fetch.ensure()

from chain import SEQ_FINAL_RBF, Coin, Lab, keypath_sig  # noqa: E402
from node import Node, RPCError  # noqa: E402
import scenarios as S  # noqa: E402
import templates as T  # noqa: E402
import verify as V  # noqa: E402
from test_framework.messages import CTxOut, sha256  # noqa: E402

OUTSIDE_FEE = 150_000
WATCHTOWER_FEE = 20_000


def main() -> int:
    with Node(BINARY) as node:
        lab = Lab(node)
        lab.setup()

        def child(parent, coin, fee):
            """A v3 child spending the parent's anchor (output 1) and a funder coin, paying fee."""
            anchor = Coin(parent.txid_hex, 1, CTxOut(0, T.P2A_SCRIPT))
            return lab.build([(anchor, SEQ_FINAL_RBF), (coin, SEQ_FINAL_RBF)],
                             [CTxOut(0, lab.funder_spk)],
                             lambda tx, spent: [[], [keypath_sig(tx, 1, spent, lab.funder.priv)]],
                             version=3, fee=fee)

        def package(parent, kid) -> str:
            try:
                res = lab.rpc("submitpackage", [parent.serialize().hex(), kid.serialize().hex()])
            except RPCError as e:
                return "error " + e.message
            errs = " | ".join(str(v["error"]) for v in res.get("tx-results", {}).values() if v.get("error"))
            return (res.get("package_msg", "") + " " + errs).strip()

        # 1. The agent outbids a veto at the window's edge with money from outside T_n.
        e = S.TickChain(lab, "fresh-eyes cpfp")
        he = e.genesis()
        lab.mine_to(he + e.tpl.n2 - 1)
        tick_value = e.coin.out.nValue
        veto = e.veto(1, outputs=[CTxOut(tick_value, e.tpl.halt(e.n).scriptPubKey),
                                  CTxOut(0, T.P2A_SCRIPT)], version=3, fee_output=None)[0]
        wkid, wfee = child(veto, lab.take_coin(), fee=WATCHTOWER_FEE)
        print(f"watchtower veto package (child fee {wfee} sats): {package(veto, wkid)}")
        adv = e.advance(2, outputs=[CTxOut(tick_value, e.next_spk()), CTxOut(0, T.P2A_SCRIPT)],
                        version=3, fee_output=None)[0]
        akid, afee = child(adv, lab.take_coin(), fee=OUTSIDE_FEE)
        print(f"agent advance2 with anchor, child paying {afee} sats from outside the chain "
              f"(T_n holds {tick_value}): {package(adv, akid)}")
        pool = lab.rpc("getrawmempool")
        print(f"mempool: advance in {adv.txid_hex in pool}, veto in {veto.txid_hex in pool}")
        lab.mine()
        released = None
        if adv.txid_hex in pool:
            e.confirmed(adv, "advance2")
            lab.mine(lab.d)
            try:
                released = V.verify_release(V.Headers(lab.headers()), e.tpl, e.t0, e.package(), e.roots, 0, lab.d)
            except Exception as ex:  # noqa: BLE001
                print("relying-party verifier rejected:", ex)
        if released:
            print(f"BREAK: outside-money bid of {afee} sats (T_n held {tick_value}) evicted the veto; "
                  f"verifier: {released}")
        else:
            print("HELD: the veto was not evicted by an outside-money bid")

        # 2. Two chains under one charter id, each accepted from its own pin.
        a = S.TickChain(lab, "fresh-eyes same charter")
        b = S.TickChain(lab, "fresh-eyes same charter")
        assert a.cid == b.cid
        a.roots[1] = sha256(b"entry 1 shown to scorer A")
        b.roots[1] = sha256(b"entry 1 shown to scorer B")
        ha, hb = a.genesis(), b.genesis()
        lab.mine_to(max(ha, hb) + a.tpl.n2 - 1)
        txs = [(c, c.advance(2)[0]) for c in (a, b)]
        for _, tx in txs:
            lab.send(tx)
        lab.mine()
        for c, tx in txs:
            c.confirmed(tx, "advance2")
        lab.mine(lab.d)
        hdr = V.Headers(lab.headers())
        accepted = []
        for c, who in ((a, "A"), (b, "B")):
            try:
                v = V.verify_release(hdr, c.tpl, c.t0, c.package(), c.roots, 0, lab.d)
                print(f"chain {who}, pinned at its own T_0 {c.t0[0][:16]}: {v}; root_1 = {c.roots[1].hex()[:16]}")
                accepted.append(who)
            except Exception as ex:  # noqa: BLE001
                print(f"chain {who} rejected:", ex)
        if len(accepted) == 2:
            print("BREAK: one charter id carried two chains with different roots at entry 1, "
                  "each accepted from its own pin")
        else:
            print("HELD: only one chain per charter id was accepted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
