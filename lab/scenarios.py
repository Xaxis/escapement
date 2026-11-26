"""The lab's scenarios. Each builds, signs and broadcasts real transactions on the regtest node and
records what the node (or the relying-party verifier) did against what the claims file expects.

Keys, charter ids and log contents are test data. Block counts, the fee rate, the bond size and
the cap come from the model's ledger (data/numbers.json) through chain.model_value.
"""

from __future__ import annotations

import datetime
import math
import re

import templates as T
import verify as V
from chain import SEQ_FINAL_RBF, Coin, Key, Lab, control_block, keypath_sig, leaf_sig, p2tr, tweaked_priv
from node import RPCError
from test_framework.messages import CTransaction, CTxOut, sha256

AGENT = Key("agent")
GUARDIANS = [Key(f"guardian-{i}") for i in (1, 2, 3)]
COSIGNER = Key("cosigner")
PRINCIPAL = Key("principal")
TICK_VALUE = 100_000  # sats held by each tick output; it only has to carry the chain's fees
BAD_SIG = bytes(64)   # 64 bytes that are not a valid signature for any message


def charter_id(label: str) -> bytes:
    return sha256(b"escapement-lab charter: " + label.encode())


class TickChain:
    """A prover's tick chain: the charter template, the disclosed roots, the current output, and
    the txids of every link from the genesis transaction on."""

    def __init__(self, lab: Lab, label: str):
        self.lab = lab
        self.cid = charter_id(label)
        self.tpl = T.TickTemplate(self.cid, AGENT.x, [g.x for g in GUARDIANS], lab.n2, lab.n3)
        self.roots: dict[int, bytes] = {}
        self.links: list[str] = []
        self.n = 0
        self.state = "tick"
        self.coin: Coin | None = None

    def root(self, n: int) -> bytes:
        if n not in self.roots:
            self.roots[n] = sha256(self.cid + n.to_bytes(8, "little") + b"entry root placeholder")
        return self.roots[n]

    def info(self):
        return self.tpl.tick(self.n, self.root(self.n)) if self.state == "tick" else self.tpl.halt(self.n)

    def genesis(self, root0: bytes | None = None) -> int:
        if root0 is not None:
            self.roots[0] = root0
        self.coin = self.lab.fund(self.tpl.tick(0, self.root(0)).scriptPubKey, TICK_VALUE,
                                  kind="tick genesis: fund T_0 (1 in, T_0 + change)")
        self.links.append(self.coin.txid)
        self.lab.mine()
        self.coin.height = self.lab.confirmed_height(self.coin.txid)
        return self.coin.height

    def next_spk(self, n: int | None = None) -> bytes:
        n = self.n + 1 if n is None else n
        return self.tpl.tick(n, self.root(n)).scriptPubKey

    def spend(self, leaf: str, signers: list, *, sequence: int = SEQ_FINAL_RBF,
              outputs: list[CTxOut] | None = None, version: int = 2, fee: int | None = None,
              fee_output: int | None = 0, coin: Coin | None = None, info=None) -> tuple[CTransaction, int]:
        """Spend the current output through `leaf`. signers lists, in the order the script checks
        them, a Key, None (an empty signature) or raw bytes (a given signature)."""
        info = info or self.info()
        coin = coin or self.coin
        script = info.leaves[leaf].script
        cb = control_block(info, leaf)
        outputs = outputs if outputs is not None else [CTxOut(0, self.next_spk())]

        def witness(tx, spent):
            sigs = []
            for s in signers:
                if s is None:
                    sigs.append(b"")
                elif isinstance(s, bytes):
                    sigs.append(s)
                else:
                    sigs.append(leaf_sig(tx, 0, spent, script, s))
            return [list(reversed(sigs)) + [bytes(script), cb]]

        return self.lab.build([(coin, sequence)], outputs, witness, version=version,
                              fee=fee, fee_output=fee_output)

    def advance(self, tier: int, signers=None, sequence=None, **kw):
        leaf = f"advance{tier}"
        signers = signers if signers is not None else ([AGENT] if tier == 2 else [AGENT] + GUARDIANS)
        seq = sequence if sequence is not None else (self.tpl.n2 if tier == 2 else self.tpl.n3)
        return self.spend(leaf, signers, sequence=seq, **kw)

    def veto(self, i: int, to_halt: bool = True, outputs: list[CTxOut] | None = None, **kw):
        if outputs is None:
            out = self.tpl.halt(self.n).scriptPubKey if to_halt else p2tr(GUARDIANS[i - 1].x)
            outputs = [CTxOut(0, out)]
        return self.spend(f"veto_{i}", [GUARDIANS[i - 1]], outputs=outputs, **kw)

    def renew(self, **kw):
        return self.spend("renew", GUARDIANS, **kw)

    def confirmed(self, tx: CTransaction, leaf: str) -> None:
        """Record that tx, spending the current output through leaf, is confirmed."""
        self.links.append(tx.txid_hex)
        self.coin = Coin(tx.txid_hex, 0, tx.vout[0], self.lab.confirmed_height(tx.txid_hex))
        if leaf.startswith("veto"):
            self.state = "halt" if tx.vout[0].scriptPubKey == self.tpl.halt(self.n).scriptPubKey else "ended"
        else:
            self.n += 1
            self.state = "tick"

    @property
    def t0(self) -> tuple[str, int]:
        """The charter's genesis outpoint, which a relying party pins (here the funding output)."""
        return (self.links[0], 0)

    def package(self) -> list[dict]:
        return [self.lab.link(txid) for txid in self.links]


# ----------------------------------------------------------------------------------------------
# 1. Bond (K1)

def s1_bond(lab: Lab) -> None:
    cid = charter_id("bond")
    other = charter_id("another charter")
    tweak = T.TaggedHash(T.TAG_BOND, cid)
    start = lab.height()
    locktime = start + lab.season + 10  # lab choice: just past the season, so both ends are tested
    cltv = T.bond_cltv_script(locktime, PRINCIPAL.x)
    main = T.bond_info(cid, PRINCIPAL.x, locktime, "tweak")
    with_leaf = T.bond_info(cid, PRINCIPAL.x, locktime, "leaf")
    internal = T.nums_key(T.TAG_BOND, cid)[0]
    hidden = T.taproot_construct(internal, [("cltv", cltv), ("now", T.CScript([PRINCIPAL.x, T.OP_CHECKSIG]))])
    keypath = T.taproot_construct(PRINCIPAL.x, [("cltv", cltv)])

    bond = lab.fund(main.scriptPubKey, lab.bond_min, kind="bond: fund the bond output (1 in, bond + change)")
    bond_leaf = lab.fund(with_leaf.scriptPubKey, lab.bond_min)
    bond_hidden = lab.fund(hidden.scriptPubKey, lab.bond_min)
    bond_keypath = lab.fund(keypath.scriptPubKey, lab.bond_min)
    lab.mine()

    def check(coin, leaves, c=cid, tw=tweak):
        return lambda: V.verify_bond(V.Headers(lab.headers()), lab.link(coin.txid), coin.vout, c, tw,
                                     leaves, PRINCIPAL.x, locktime, lab.bond_min, lab.season)

    lab.vcheck("bond younger than the season S is not yet counted", check(bond, [cltv]),
               reject="fewer than the season")
    lab.mine(lab.season)
    lab.vcheck("verifier recomputes the bond (tweak commits the charter id, one CLTV leaf)",
               check(bond, [cltv]))
    lab.vcheck("verifier recomputes the variant with an OP_RETURN charter-id leaf",
               check(bond_leaf, [cltv, T.CScript([T.OP_RETURN, cid])]))
    lab.vcheck("the same bond presented for a second charter id",
               check(bond, [cltv], c=other, tw=T.TaggedHash(T.TAG_BOND, other)), reject="do not produce")
    lab.vcheck("a tweak that does not match the charter id",
               check(bond, [cltv], tw=T.TaggedHash(T.TAG_BOND, other)), reject="does not commit")
    lab.vcheck("bond with a hidden immediate leaf, only the CLTV leaf revealed",
               check(bond_hidden, [cltv]), reject="do not produce")
    lab.vcheck("bond with a hidden immediate leaf, all leaves revealed",
               check(bond_hidden, [cltv, T.CScript([PRINCIPAL.x, T.OP_CHECKSIG])]), reject="spendable")
    lab.vcheck("bond whose internal key is the principal's own key (a key path)",
               check(bond_keypath, [cltv]), reject="do not produce")

    def spend(coin, info, locktime_field):
        out = [CTxOut(0, p2tr(PRINCIPAL.x))]

        def witness(tx, spent):
            return [[leaf_sig(tx, 0, spent, cltv, PRINCIPAL), bytes(cltv), control_block(info, "cltv")]]
        return lab.build([(coin, SEQ_FINAL_RBF)], out, witness, locktime=locktime_field)

    lab.mine_to(locktime - 1)
    tx, _ = spend(bond, main, lab.height())
    lab.expect(f"principal spends at tip {lab.height()} with nLockTime {lab.height()} < locktime {locktime}",
               tx, reject="Locktime requirement not satisfied")
    tx, _ = spend(bond, main, locktime)
    lab.expect(f"principal spends at tip {lab.height()} with nLockTime = locktime {locktime}", tx,
               reject="non-final")
    lab.mine()
    tx, fee = spend(bond, main, locktime)
    lab.expect(f"principal spends at tip {lab.height()} (next block {locktime + 1}) with nLockTime = locktime",
               tx, kind="bond: spend through the CLTV leaf (tweak form, 1 leaf)", fee=fee)
    tx, fee = spend(bond_leaf, with_leaf, locktime)
    lab.expect("principal spends the OP_RETURN-leaf variant after the locktime", tx,
               kind="bond: spend through the CLTV leaf (leaf form, 2 leaves)", fee=fee)
    lab.mine()
    lab.vcheck("the bond once the tip is past its locktime (it has in fact been spent)",
               check(bond, [cltv]), reject="past its locktime")


# ----------------------------------------------------------------------------------------------
# 2. Tick chain (K7)

def s2_tick_chain(lab: Lab) -> None:
    c = TickChain(lab, "tick chain A")
    lab.state["chain_a"] = c
    h0 = c.genesis()
    tx, _ = c.advance(2)
    lab.expect(f"agent advance2 at tip {lab.height()}, {lab.height() - h0} blocks after T_0", tx,
               reject="non-BIP68-final")
    lab.mine_to(h0 + c.tpl.n2 - 2)
    tx, _ = c.advance(2)
    lab.expect(f"agent advance2 at tip {lab.height()} (next block {lab.height() + 1} = h(T_0) + N2 - 1)",
               tx, reject="non-BIP68-final")
    lab.mine()
    tx, _ = c.advance(2, sequence=c.tpl.n2 - 1)
    lab.expect("agent advance2 with nSequence N2 - 1 (BIP68 satisfied, CSV in script not)", tx,
               reject="Locktime requirement not satisfied")
    tx, _ = c.advance(2, sequence=SEQ_FINAL_RBF)
    lab.expect("agent advance2 with relative lock time disabled in nSequence", tx,
               reject="Locktime requirement not satisfied")
    tx, fee = c.advance(2)
    r = lab.expect(f"agent advance2 at tip {lab.height()} (next block = h(T_0) + N2)", tx,
                   kind="tick advance2: T_n to T_n+1 (agent, script path, depth 1)", fee=fee)
    if not r["accepted"]:
        return
    lab.mine()
    c.confirmed(tx, "advance2")
    h1 = c.coin.height
    lab.record("release confirmed exactly N2 blocks after T_0", f"height {h0 + c.tpl.n2}",
               h1 == h0 + c.tpl.n2, f"T_0 at {h0}, T_1 at {h1}")

    tx, _ = c.advance(3)
    lab.expect("advance3 with every signature, before N3", tx, reject="non-BIP68-final")
    lab.mine_to(h1 + c.tpl.n3 - 1)
    tx, _ = c.advance(3, signers=[AGENT, GUARDIANS[0], None, GUARDIANS[2]])
    lab.expect("advance3 after N3 without guardian 2's signature", tx,
               reject="Script failed an OP_CHECKSIGVERIFY operation")
    tx, _ = c.advance(3, signers=[AGENT, GUARDIANS[0], GUARDIANS[1], BAD_SIG])
    lab.expect("advance3 after N3 with an invalid signature for guardian 3", tx,
               reject="Invalid Schnorr signature")
    tx, _ = c.advance(3, signers=[AGENT, GUARDIANS[0], GUARDIANS[1], GUARDIANS[1]])
    lab.expect("advance3 after N3 with guardian 2 signing in guardian 3's place", tx,
               reject="Invalid Schnorr signature")
    tx, fee = c.advance(3)
    lab.expect("advance3 after N3 with the agent and every guardian", tx,
               kind="tick advance3: T_n to T_n+1 (agent + 3 guardians, depth 3)", fee=fee)
    lab.mine()
    c.confirmed(tx, "advance3")
    h2 = c.coin.height

    vtx, fee = c.veto(2)
    lab.expect("guardian 2 vetoes T_2 at once, paying to the halt output", vtx,
               kind="veto: T_n to halt output (one guardian, plain v2, depth 4)", fee=fee)
    lab.mine()
    blocked = c.advance(2)[0]
    stale_renew = c.renew()[0]
    c.confirmed(vtx, "veto_2")
    lab.mine_to(h2 + c.tpl.n2 + 1)
    lab.expect("agent advance2 of the vetoed T_2 after N2", blocked, reject="bad-txns-inputs-missingorspent")
    lab.expect("renew through T_2's own renew leaf after the veto", stale_renew,
               reject="bad-txns-inputs-missingorspent")
    tx, fee = c.renew()
    lab.expect("every guardian renews from the halt output, creating T_3", tx,
               kind="renew: halt output to T_n+1 (3 guardians, single-leaf tree)", fee=fee)
    lab.mine()
    c.confirmed(tx, "renew")
    h3 = c.coin.height
    lab.mine_to(h3 + c.tpl.n2 - 1)
    tx, fee = c.advance(2)
    lab.expect("agent advance2 of T_3 after N2: the renewed chain releases again", tx)
    lab.mine()
    c.confirmed(tx, "advance2")
    tx, fee = c.renew()
    lab.expect("every guardian renews an unspent T_4 at once (no wait)", tx,
               kind="renew: T_n to T_n+1 (3 guardians, depth 3)", fee=fee)
    lab.mine()
    c.confirmed(tx, "renew")
    lab.mine(lab.d)

    # A veto that does not pay to the halt output: the chain cannot be restarted on template.
    b = TickChain(lab, "tick chain B")
    b.genesis()
    vtx, fee = b.veto(1, to_halt=False)
    lab.expect("guardian 1 vetoes chain B's T_0, paying to its own key", vtx,
               kind="veto: T_n to one P2TR output (one guardian, plain v2, depth 3)", fee=fee)
    lab.mine()
    stale = b.renew()[0]
    b.confirmed(vtx, "veto_1")
    lab.expect("renew of chain B's T_0 after that veto", stale, reject="bad-txns-inputs-missingorspent")
    headers = V.Headers(lab.headers())
    entries = V.walk_chain(headers, b.tpl, b.t0, b.package(), b.roots)
    lab.record("verifier on chain B: a veto not paid to the halt template ends the chain",
               "entry 0 vetoed, chain ended", entries[-1].status == "vetoed, chain ended",
               "; ".join(str(e) for e in entries))

    # The race at the window edge: both spends valid; whichever a miner confirms first wins.
    r = TickChain(lab, "tick chain race")
    lab.state["chain_race"] = r
    hr = r.genesis()
    lab.mine_to(hr + r.tpl.n2 - 1)
    adv, _ = r.advance(2)
    veto, _ = r.veto(1)
    tma = lab.rpc("testmempoolaccept", [adv.serialize().hex()], 0)[0]
    tmv = lab.rpc("testmempoolaccept", [veto.serialize().hex()], 0)[0]
    lab.record(f"at tip {lab.height()} both the agent's advance2 and guardian 1's veto are valid",
               "both accepted by testmempoolaccept", tma["allowed"] and tmv["allowed"],
               f"advance2 allowed={tma['allowed']}, veto allowed={tmv['allowed']}")
    block_a = lab.generate_block([adv])
    lab.expect("guardian 1's veto after a miner confirmed the advance first", veto,
               reject="bad-txns-inputs-missingorspent")
    stale_links = [lab.link(r.links[0]), lab.link(adv.txid_hex)]
    hdr = V.Headers(lab.headers())
    lab.vcheck("release with 1 confirmation, checked with d = 1",
               lambda: V.verify_release(hdr, r.tpl, r.t0, stale_links, r.roots, 0, 1))
    lab.vcheck(f"the same release checked with d = {lab.d}",
               lambda: V.verify_release(hdr, r.tpl, r.t0, stale_links, r.roots, 0, lab.d),
               reject="fewer than d")
    lab.rpc("invalidateblock", block_a)
    lab.generate_block([veto])
    lab.mine(lab.d)
    lab.expect("the agent's advance2 after a one-block reorg confirmed the veto instead", adv,
               reject="bad-txns-inputs-missingorspent")
    r.confirmed(veto, "veto_1")
    lab.state["race_stale_links"] = stale_links


# ----------------------------------------------------------------------------------------------
# 3. Release verifier

def s3_verifier(lab: Lab) -> None:
    a: TickChain = lab.state["chain_a"]
    race: TickChain = lab.state["chain_race"]
    hdr = V.Headers(lab.headers())
    links = a.package()
    roots = dict(a.roots)
    rel = lambda n, ls=links, rs=roots, strict=True, tier=2, d=lab.d: (  # noqa: E731
        lambda: V.verify_release(hdr, a.tpl, a.t0, ls, rs, n, d, strict, tier))

    entries = V.walk_chain(hdr, a.tpl, a.t0, links, roots)
    lab.record("verifier walks chain A from T_0", "entries 0, 1, 3 released; 2 vetoed; 4 renewed",
               [e.status for e in entries] == ["released", "released", "vetoed", "released", "renewed", "open"],
               "; ".join(str(e) for e in entries))
    lab.vcheck("genuine release of entry 0 (advance2)", rel(0))
    lab.vcheck("genuine release of entry 1 at tier 3 (advance3)", rel(1, tier=3))
    lab.vcheck("genuine release of entry 3, after the halt and renew", rel(3))
    lab.vcheck("entry 1 claimed with a different root_1", rel(1, rs={**roots, 1: sha256(b"other root")}),
               reject="root_1")
    lab.vcheck("chain with a gap (the link that created T_2 left out)", rel(3, ls=links[:2] + links[3:]),
               reject="gap")
    lab.vcheck("release whose revealed leaf is veto (entry 2 of chain A)", rel(2), reject="through veto_2")
    lab.vcheck("tier 3 claimed for entry 0, which was released at tier 2", rel(0, tier=3), reject="below tier 3")
    stale = lab.state["race_stale_links"]
    lab.vcheck("vetoed entry: the agent's release proof from the block a reorg replaced",
               lambda: V.verify_release(hdr, race.tpl, race.t0, stale, race.roots, 0, 1), reject="not in the best header chain")
    lab.vcheck("vetoed entry: the race chain as the best chain has it",
               lambda: V.verify_release(hdr, race.tpl, race.t0, race.package(), race.roots, 0, lab.d),
               reject="through veto_1")
    # K7(e)'s shortcut: the transaction that created T_n plus its release, without the walk.
    two = [lab.link(a.links[1]), lab.link(a.links[2])]
    lab.vcheck("two-transaction proof of entry 1 (K7(e)): creating tx of T_1 and its release",
               lambda: V.verify_release(hdr, a.tpl, None, two, roots, 1, lab.d, True, 3, start=1))
    r3x = sha256(b"the agent's own root for entry 3")
    fake = lab.fund(a.tpl.tick(2, a.root(2)).scriptPubKey, TICK_VALUE)
    fake0 = lab.fund(a.tpl.tick(0, a.root(0)).scriptPubKey, TICK_VALUE)
    lab.mine()
    lab.mine(a.tpl.n2 - 1)
    ftx, _ = a.spend("advance2", [AGENT], sequence=a.tpl.n2, coin=fake,
                     info=a.tpl.tick(2, a.root(2)), outputs=[CTxOut(0, a.tpl.tick(3, r3x).scriptPubKey)])
    lab.expect("agent funds its own copy of T_2 (same template and root) and advances it after N2", ftx)
    f0tx, _ = a.spend("advance2", [AGENT], sequence=a.tpl.n2, coin=fake0,
                      info=a.tpl.tick(0, a.root(0)), outputs=[CTxOut(0, a.next_spk(1))])
    lab.expect("agent funds its own copy of T_0 and advances it after N2 (a parallel chain)", f0tx)
    lab.mine(lab.d)
    hdr = V.Headers(lab.headers())
    fake_links = [lab.link(fake.txid), lab.link(ftx.txid_hex)]
    parallel = [lab.link(fake0.txid), lab.link(f0tx.txid_hex)]
    lab.vcheck("a parallel chain from the agent's own copy of T_0, genesis not pinned: the flaw",
               lambda: V.verify_release(hdr, a.tpl, None, parallel, roots, 0, lab.d))
    lab.vcheck("the same parallel chain with T_0 pinned to the charter's genesis outpoint",
               lambda: V.verify_release(hdr, a.tpl, a.t0, parallel, roots, 0, lab.d),
               reject="not the transaction that created the charter's T_0")
    lab.vcheck("two-transaction proof of the vetoed entry 2, from the agent's copy of T_2: the flaw",
               lambda: V.verify_release(hdr, a.tpl, None, fake_links, {2: roots[2], 3: r3x}, 2, lab.d, True, 2,
                                        start=2))
    lab.vcheck("the same release checked by walking the chain from T_0",
               lambda: V.verify_release(hdr, a.tpl, a.t0, links[:3] + fake_links[1:], {**roots, 3: r3x}, 2, lab.d),
               reject="gap")
    lab.extra["proof_bytes"] = {
        "headers_bytes_per_block": 80,
        "chain_a_links": len(links),
        "full_walk_with_witness_proofs": V.proof_bytes(links, True),
        "full_walk_txid_proofs_only": V.proof_bytes(links, False),
        "two_tx_with_witness_proofs": V.proof_bytes(two, True),
        "note": "regtest blocks hold a few transactions, so Merkle branches here are 1 or 2 hashes deep",
    }

    bad = [bytearray(h) for h in lab.headers()]
    bad[5][4] ^= 1
    lab.vcheck("header chain with one broken link", lambda: V.Headers([bytes(h) for h in bad]),
               reject="does not link")

    # The revealed leaf is in the witness, which txid Merkle proofs do not cover.
    f = TickChain(lab, "tick chain forgery")
    hf = f.genesis()
    lab.mine_to(hf + f.tpl.n3 - 1)
    tx, _ = f.advance(2)
    lab.send(tx)
    lab.mine()
    f.confirmed(tx, "advance2")
    flinks = f.package()
    rel_f = lambda ls, strict, tier=3: (lambda: V.verify_release(  # noqa: E731
        V.Headers(lab.headers()), f.tpl, f.t0, ls, f.roots, 0, lab.d, strict, tier))
    lab.vcheck(f"release with 1 confirmation, d = {lab.d}", rel_f(flinks, True, 2), reject="fewer than d")
    lab.mine(lab.d)
    info0 = f.tpl.tick(0, f.root(0))
    forged = V.parse_tx(flinks[1]["tx"])
    stack = forged.wit.vtxinwit[0].scriptWitness.stack
    s3 = info0.leaves["advance3"].script
    forged.wit.vtxinwit[0].scriptWitness.stack = [BAD_SIG, BAD_SIG, BAD_SIG, stack[0], bytes(s3),
                                                  control_block(info0, "advance3")]
    forged_links = [flinks[0], {**flinks[1], "tx": forged.serialize()}]
    lab.record("forged witness keeps the txid", "same txid", forged.txid_hex == f.links[1],
               f"txid {forged.txid_hex[:16]} for both")
    lab.vcheck("tier-3 claim with a forged witness, txid proofs only (K7(e) as written): the flaw",
               rel_f(forged_links, False))
    lab.vcheck("tier-3 claim with a forged witness, witness commitment checked",
               rel_f(forged_links, True), reject="not the one the block committed to")
    lab.vcheck("the genuine witness for that link, witness commitment checked, at tier 2",
               rel_f(flinks, True, 2))

    # Completeness at the tip: a prefix of the chain passes; full blocks show it continued.
    prefix = links[:5]  # up to the renew that created T_3
    hdr = V.Headers(lab.headers())
    try:
        entries = V.walk_chain(hdr, a.tpl, a.t0, prefix, roots)
        last = entries[-1]
        lab.record("a prefix of chain A that hides entries 3 and 4", "light verifier cannot tell (accepts)",
                   last.status == "open" and last.n == 3, f"verifier accepted; it reports {last} as the tip")
    except V.Reject as e:
        lab.record("a prefix of chain A that hides entries 3 and 4", "light verifier cannot tell (accepts)",
                   False, f"verifier rejected: {e}")
    t3 = V.parse_tx(prefix[-1]["tx"])
    h3 = V.tx_in_block(hdr, prefix[-1]["proof"], t3)[0]
    found = V.find_spend(hdr, lab.raw_blocks(h3 + 1, hdr.tip), h3 + 1, t3.txid, 0)
    lab.record(f"scan of full blocks {h3 + 1}..{hdr.tip} for a spend of T_3 (no UTXO query)",
               "finds the hidden release", found is not None,
               f"T_3 spent at height {found[0]} by {found[1][:16]}" if found else "no spend found")


# ----------------------------------------------------------------------------------------------
# 4. Lease (K8)

def sign_renewal(cid: bytes, k: int, h_k: int, blockhash: bytes, signers=None) -> dict:
    msg = T.lease_message(cid, k, h_k, blockhash)
    from test_framework.key import sign_schnorr
    signers = signers or GUARDIANS
    return {"k": k, "h_k": h_k, "blockhash": blockhash, "sigs": [sign_schnorr(g.priv, msg) for g in signers]}


def s4_lease(lab: Lab) -> None:
    c = TickChain(lab, "tick chain lease")
    g = [x.x for x in GUARDIANS]
    L = lab.lease
    h0 = c.genesis()
    h1 = lab.height()
    hdr = V.Headers(lab.headers())
    renewals = [sign_renewal(c.cid, 1, h1, hdr.hash_at(h1))]

    def release() -> int:
        lab.mine_to(c.coin.height + c.tpl.n2 - 1)
        tx, _ = c.advance(2)
        lab.send(tx)
        lab.mine()
        c.confirmed(tx, "advance2")
        return c.coin.height

    r1 = release()
    lab.mine(lab.d)
    check = lambda h, rs=None: (lambda: V.verify_lease(  # noqa: E731
        V.Headers(lab.headers()), c.cid, g, L, rs or renewals, h))
    lab.vcheck(f"release at height {r1}, lease 1 at h_1 = {h1}, L = {L}", check(r1))
    times_before = V.Headers(lab.headers()).raw[-1][68:72]
    lab.clock += 365 * 24 * 3600
    lab.mine(1)
    times_after = V.Headers(lab.headers()).raw[-1][68:72]
    jump = int.from_bytes(times_after, "little") - int.from_bytes(times_before, "little")
    lab.vcheck(f"same release after block timestamps jump {jump // 86400} days ahead", check(r1))
    lab.mine_to(h1 + L)
    r2 = release()
    lab.mine(lab.d)
    lab.vcheck(f"release at height {r2}, after h_1 + L = {h1 + L}", check(r2), reject="outside every lease")
    guess = sha256(b"a guess at a block that does not exist yet")
    early = sign_renewal(c.cid, 2, lab.height() + 3, guess)
    lab.mine(3)
    lab.vcheck("renewal signed before its block existed (guessed hash)", check(r2, [early]),
               reject="not the best chain's block")
    h3 = lab.height()
    hdr = V.Headers(lab.headers())
    renewals.append(sign_renewal(c.cid, 3, h3, hdr.hash_at(h3)))
    partial = sign_renewal(c.cid, 4, h3, hdr.hash_at(h3), signers=GUARDIANS[:2] + [GUARDIANS[1]])
    r3 = release()
    lab.mine(lab.d)
    lab.vcheck(f"release at height {r3} under renewal 3 (h_3 = {h3})", check(r3))
    lab.vcheck("renewal with guardian 2's signature in guardian 3's place", check(r3, [partial]),
               reject="invalid guardian signature")

    # No clock: every clock function raises while the verifier runs.
    headers = lab.headers()

    def verdict(h: int) -> str:
        try:
            return "accepted: " + V.verify_lease(V.Headers(headers), c.cid, g, L, renewals, h)
        except V.Reject as e:
            return "rejected: " + str(e)

    import time as clock
    names = ("time", "time_ns", "monotonic", "perf_counter", "localtime", "gmtime")
    saved = {n: getattr(clock, n) for n in names}
    saved_dt = datetime.datetime

    def boom(*a, **k):
        raise AssertionError("the verifier read a clock")

    class NoClock(datetime.datetime):
        now = classmethod(boom)
        utcnow = classmethod(boom)
        today = classmethod(boom)

    try:
        for n in names:
            setattr(clock, n, boom)
        datetime.datetime = NoClock
        inside, outside = verdict(r3), verdict(r2)
    except AssertionError as e:
        inside = outside = str(e)
    finally:
        for n, fn in saved.items():
            setattr(clock, n, fn)
        datetime.datetime = saved_dt
    lab.record("lease verdicts with every clock function disabled", "same verdicts, no clock read",
               inside.startswith("accepted") and "outside every lease" in outside,
               f"{inside}; {outside}")


# ----------------------------------------------------------------------------------------------
# 5. Co-signing

def s5_cosign(lab: Lab) -> None:
    n = lab.n3
    k = 2
    info = T.cosign_info(sha256(b"escapement-lab vault 1"), AGENT.x, COSIGNER.x, n, [g.x for g in GUARDIANS], k)
    o1 = lab.fund(info.scriptPubKey, TICK_VALUE)
    o2 = lab.fund(info.scriptPubKey, TICK_VALUE)
    lab.mine()
    hv = lab.height()
    spend_s = info.leaves["spend"].script
    rec_s = info.leaves["recovery"].script

    def spend(coin, sigs: list, seq: int):
        def witness(tx, spent):
            out = []
            for s in sigs:
                out.append(b"" if s is None else leaf_sig(tx, 0, spent, spend_s, s))
            return [list(reversed(out)) + [bytes(spend_s), control_block(info, "spend")]]
        return lab.build([(coin, seq)], [CTxOut(0, p2tr(AGENT.x))], witness)

    def recover(coin, signers: list):
        def witness(tx, spent):
            out = [b"" if s is None else leaf_sig(tx, 0, spent, rec_s, s) for s in signers]
            return [list(reversed(out)) + [bytes(rec_s), control_block(info, "recovery")]]
        return lab.build([(coin, SEQ_FINAL_RBF)], [CTxOut(0, p2tr(GUARDIANS[0].x))], witness)

    tx, _ = spend(o1, [AGENT, COSIGNER], n)
    lab.expect(f"agent and co-signer before N = {n}", tx, reject="non-BIP68-final")
    tx, _ = recover(o2, [GUARDIANS[0], None, None])
    lab.expect("recovery with 1 of 3 guardians", tx, reject="finished with a false/empty top stack element")
    tx, fee = recover(o2, [GUARDIANS[0], None, GUARDIANS[2]])
    lab.expect(f"recovery with {k} of 3 guardians at once", tx,
               kind=f"co-sign: recovery leaf ({k} of 3 guardians, CHECKSIGADD)", fee=fee)
    lab.mine_to(hv + n - 1)
    tx, _ = spend(o1, [AGENT, None], n)
    lab.expect("agent alone after N", tx, reject="Script failed an OP_CHECKSIGVERIFY operation")
    tx, _ = spend(o1, [AGENT, COSIGNER], 0)
    lab.expect("agent and co-signer after N but with nSequence 0", tx, reject="Locktime requirement not satisfied")
    tx, fee = spend(o1, [AGENT, COSIGNER], n)
    lab.expect("agent and co-signer after N", tx, kind="co-sign: and(agent, co-signer, older(N)) leaf", fee=fee)
    lab.mine()


# ----------------------------------------------------------------------------------------------
# 6. Anchoring

def s6_anchor(lab: Lab) -> None:
    owner = Key("log-owner")
    entries = [f"log entry {i}: action committed by the agent".encode() for i in range(100)]
    root, proofs = T.log_tree(entries)
    i = 37
    c1 = lab.fund(p2tr(owner.x), TICK_VALUE)
    c2 = lab.fund(p2tr(owner.x), TICK_VALUE)
    lab.mine()
    q, _, tweak = T.anchor_output_key(owner.x, root)

    def keyspend(coin, outputs, priv):
        return lab.build([(coin, SEQ_FINAL_RBF)], outputs,
                         lambda tx, spent: [[keypath_sig(tx, 0, spent, priv)]])

    t1, fee = keyspend(c1, [CTxOut(0, p2tr(q))], owner.priv)
    lab.expect("anchor through the Taproot tweak (1 key-path input, 1 output)", t1,
               kind="anchor: log root in the output's tweak (1 in, 1 out)", fee=fee)
    t2, fee = keyspend(c2, [CTxOut(0, p2tr(owner.x)), CTxOut(0, bytes([0x6A, 0x20]) + root)], owner.priv)
    lab.expect("anchor through OP_RETURN (1 key-path input, change + OP_RETURN)", t2,
               kind="anchor: log root in OP_RETURN (1 in, change + OP_RETURN)", fee=fee)
    lab.mine(lab.d)
    hdr = lambda: V.Headers(lab.headers())  # noqa: E731
    l1, l2 = lab.link(t1.txid_hex), lab.link(t2.txid_hex)
    lab.vcheck(f"entry {i} of 100 via the tweak anchor",
               lambda: V.verify_log_inclusion(hdr(), l1, 0, "tweak", entries[i], proofs[i], root, owner.x))
    lab.vcheck(f"entry {i} of 100 via the OP_RETURN anchor",
               lambda: V.verify_log_inclusion(hdr(), l2, 1, "opreturn", entries[i], proofs[i], root))
    lab.vcheck("an altered entry", lambda: V.verify_log_inclusion(
        hdr(), l1, 0, "tweak", entries[i] + b"!", proofs[i], root, owner.x), reject="does not reach")
    lab.vcheck("the tweak anchor checked against another internal key", lambda: V.verify_log_inclusion(
        hdr(), l1, 0, "tweak", entries[i], proofs[i], root, AGENT.x), reject="output key is not")
    anchored = Coin(t1.txid_hex, 0, t1.vout[0])
    t3, fee = keyspend(anchored, [CTxOut(0, p2tr(owner.x))], tweaked_priv(owner.priv, tweak))
    lab.expect("the tweak-anchored output stays spendable by the owner's key path", t3,
               kind="key-path spend, 1 in 1 out (the model's seal transaction shape)", fee=fee)
    lab.mine()


# ----------------------------------------------------------------------------------------------
# 7. Fee bumping of a veto (TRUC v3 + pay-to-anchor)

def s7_truc_veto(lab: Lab) -> None:
    c = TickChain(lab, "tick chain truc")
    h0 = c.genesis()

    def veto_parent(chain: TickChain, fee: int = 0) -> CTransaction:
        outs = [CTxOut(chain.coin.out.nValue - fee, chain.tpl.halt(chain.n).scriptPubKey),
                CTxOut(0, T.P2A_SCRIPT)]
        return chain.veto(1, outputs=outs, version=3, fee_output=None)[0]

    def child(parent: CTransaction, coin: Coin, *, feerate: float = 0, fee: int | None = None,
              pad: int = 0) -> tuple[CTransaction, int]:
        """A v3 child spending the parent's P2A output and one funder coin for the fee."""
        anchor = Coin(parent.txid_hex, 1, CTxOut(0, T.P2A_SCRIPT))
        extra = [CTxOut(0, bytes([0x6A, 0x4D]) + pad.to_bytes(2, "little") + bytes(pad))] if pad else []

        def build(f):
            return lab.build([(anchor, SEQ_FINAL_RBF), (coin, SEQ_FINAL_RBF)],
                             [CTxOut(0, lab.funder_spk)] + extra,
                             lambda tx, spent: [[], [keypath_sig(tx, 1, spent, lab.funder.priv)]],
                             version=3, fee=f)
        if fee is None:
            probe, _ = build(0)
            fee = math.ceil(feerate * (parent.get_vsize() + probe.get_vsize()))
        return build(fee)

    def package(parent, kid) -> tuple[str, str]:
        try:
            res = lab.rpc("submitpackage", [parent.serialize().hex(), kid.serialize().hex()])
        except RPCError as e:
            return "error", e.message
        errs = " | ".join(str(v["error"]) for v in res.get("tx-results", {}).values() if v.get("error"))
        return res.get("package_msg", ""), errs

    parent = veto_parent(c)
    lab.expect("v3 veto with a zero-value P2A output and zero fee, alone", parent,
               reject="min relay fee not met")
    low = veto_parent(c, fee=math.ceil(parent.get_vsize() * lab.feerate))
    lab.expect(f"v3 veto paying {lab.feerate} sat/vB with a zero-value P2A output, alone", low, reject="dust")
    coin = lab.take_coin()
    big, _ = child(parent, coin, feerate=2 * lab.feerate, pad=1000)
    msg, errs = package(parent, big)
    short = re.sub(r" \(wtxid=[0-9a-f]{64}\)| [0-9a-f]{64}", "", msg)
    lab.record(f"package whose child is {big.get_vsize()} vB (TRUC allows a child at most 1000 vB)",
               "rejected: TRUC-violation", "TRUC-violation" in msg + errs, f"rejected: {short}",
               reason=f"{msg}: {errs}", vbytes=big.get_vsize())
    kid, kid_fee = child(parent, coin, feerate=2 * lab.feerate)
    msg, errs = package(parent, kid)
    ok = msg == "success"
    lab.record("submitpackage: zero-fee v3 veto + v3 child spending its P2A output", "package accepted", ok,
               f"package_msg={msg} {errs}".strip(), txids=[parent.txid_hex, kid.txid_hex],
               vbytes=parent.get_vsize() + kid.get_vsize())
    if ok:
        lab.size("veto: v3 TRUC, T_n to halt + zero-value P2A, zero fee", parent, 0)
        lab.size("veto child: v3, spends the P2A + one fee input (CPFP)", kid, kid_fee,
                 note="pays for parent and child at twice the model fee rate")
    blocked = c.advance(2)[0]
    lab.mine()
    c.confirmed(parent, "veto_1")
    lab.mine_to(h0 + c.tpl.n2)
    lab.expect("agent advance2 after the veto package confirmed", blocked, reject="bad-txns-inputs-missingorspent")

    # At the window edge both spends are valid, and the mempool keeps whichever pays more.
    e = TickChain(lab, "tick chain auction")
    he = e.genesis()
    lab.mine_to(he + e.tpl.n2 - 1)
    p = veto_parent(e)
    coin = lab.take_coin()
    kid, kid_fee = child(p, coin, feerate=2 * lab.feerate)
    msg, errs = package(p, kid)
    lab.record("at the edge: a watchtower submits the veto package", "package accepted", msg == "success",
               f"package_msg={msg}, child fee {kid_fee} sats {errs}".strip())
    adv, adv_fee = e.advance(2, fee=5 * kid_fee + 1_000)
    lab.expect(f"at the edge: the agent's advance2 paying {adv_fee} sats replaces the veto package", adv)
    pool = lab.rpc("getrawmempool")
    lab.record("mempool after the agent's bid", "advance in, veto package out",
               adv.txid_hex in pool and p.txid_hex not in pool and kid.txid_hex not in pool,
               f"advance in mempool: {adv.txid_hex in pool}; veto in mempool: {p.txid_hex in pool}")
    kid2, kid2_fee = child(p, coin, fee=3 * adv_fee)
    msg, errs = package(p, kid2)
    lab.record(f"at the edge: the watchtower re-bids with a child paying {kid2_fee} sats",
               "package replaces the agent's advance", msg == "success", f"package_msg={msg} {errs}".strip())
    lab.mine()
    winner = [name for name, t in (("veto", p), ("advance2", adv)) if _in_chain(lab, t.txid_hex)]
    lab.record("at the edge: the next block confirms the higher bidder", "veto confirmed",
               winner == ["veto"], f"{', '.join(winner) or 'neither'} confirmed")


def _in_chain(lab: Lab, txid: str) -> bool:
    try:
        return bool(lab.rpc("getrawtransaction", txid, True).get("confirmations"))
    except RPCError:
        return False


# ----------------------------------------------------------------------------------------------
# 8. Merkle-sum tree committed in a tick

def s8_sum_tree(lab: Lab) -> None:
    cap = lab.cap
    leaves = [(f"promise {i}: stake for a commitment".encode(), 1_000 * (i + 1)) for i in range(13)]
    root, proofs = T.sum_tree(leaves)
    root_n = T.sum_root_commitment(root)
    over = [(b"promise 0", cap // 2), (b"promise 1", cap // 2 + 1)]
    over_root, over_proofs = T.sum_tree(over)
    c = TickChain(lab, "tick chain sum tree")
    c.roots[1] = T.sum_root_commitment(over_root)
    h0 = c.genesis(root_n)
    for _ in range(2):
        lab.mine_to(c.coin.height + c.tpl.n2 - 1)
        tx, _ = c.advance(2)
        lab.send(tx)
        lab.mine()
        c.confirmed(tx, "advance2")
    lab.mine(lab.d)
    hdr = V.Headers(lab.headers())
    links = c.package()
    lab.vcheck("entry 0 (the sum tree's root) is released",
               lambda: V.verify_release(hdr, c.tpl, c.t0, links, c.roots, 0, lab.d))
    i = 5
    data, amt = leaves[i]
    pr = [(s, n.hash, n.count, n.total) for s, n in proofs[i]]
    full = (root.hash, root.count, root.total)
    lab.vcheck(f"leaf {i} of {len(leaves)}: inclusion, sums and cap {cap}",
               lambda: V.verify_sum_proof(data, amt, pr, full, root_n, cap))
    lab.vcheck("root claims a smaller total than its children add to",
               lambda: V.verify_sum_proof(data, amt, pr, (root.hash, root.count, root.total - 5_000), root_n, cap),
               reject="sums do not add")
    shaved = list(pr)
    s, h, cnt, tot = shaved[-1]
    shaved[-1] = (s, h, cnt, tot - 5_000)
    lab.vcheck("a sibling's sum lowered in the proof", lambda: V.verify_sum_proof(
        data, amt, shaved, (root.hash, root.count, root.total - 5_000), root_n, cap), reject="root hash")
    neg = list(pr)
    neg[0] = (neg[0][0], neg[0][1], neg[0][2], -400)
    lab.vcheck("a sibling with a negative sum", lambda: V.verify_sum_proof(data, amt, neg, full, root_n, cap),
               reject="negative")
    lab.vcheck("a leaf with a negative amount", lambda: V.verify_sum_proof(data, -amt, pr, full, root_n, cap),
               reject="negative")
    lab.vcheck("entry 1 (a tree over the cap) is released: consensus does not enforce the cap",
               lambda: V.verify_release(hdr, c.tpl, c.t0, links, c.roots, 1, lab.d))
    opr = [(s, n.hash, n.count, n.total) for s, n in over_proofs[0]]
    lab.vcheck(f"entry 1's sum tree totals {over_root.total}, over the cap {cap}",
               lambda: V.verify_sum_proof(over[0][0], over[0][1], opr, tuple(over_root), c.roots[1], cap),
               reject="exceeds the cap")

    # A dishonest prover under-reports one subtree's total. Only owners of leaves under it can tell.
    four = [(f"stake {j}".encode(), 30_000) for j in range(4)]
    l0, l1, l2, l3 = (T.sum_leaf(d, a) for d, a in four)
    p01, p23 = T.sum_parent(l0, l1), T.sum_parent(l2, l3)
    fake01 = T.SumNode(p01.hash, p01.count, 10_000)
    fake_root = T.sum_parent(fake01, p23)
    fake_n = T.sum_root_commitment(fake_root)
    fr = tuple(fake_root)
    lab.vcheck("under-reported subtree, checked by the owner of a leaf inside it",
               lambda: V.verify_sum_proof(four[0][0], 30_000, [("R", l1.hash, 1, 30_000), ("R", p23.hash, 2, 60_000)],
                                          fr, fake_n, cap), reject="root hash")
    lab.vcheck("under-reported subtree, checked by the owner of a leaf outside it (passes: a limit)",
               lambda: V.verify_sum_proof(four[2][0], 30_000, [("R", l3.hash, 1, 30_000), ("L", fake01.hash, 2, 10_000)],
                                          fr, fake_n, cap))
    lab.record("the under-reported tree claims a total under the cap", f"total {fake_root.total} <= {cap}",
               fake_root.total <= cap < 4 * 30_000,
               f"claimed {fake_root.total}, real {4 * 30_000}, cap {cap}")


ALL = [
    ("1 bond (K1)", s1_bond),
    ("2 tick chain (K7)", s2_tick_chain),
    ("3 release verifier", s3_verifier),
    ("4 height lease (K8)", s4_lease),
    ("5 co-signing", s5_cosign),
    ("6 anchoring", s6_anchor),
    ("7 TRUC veto fee bump", s7_truc_veto),
    ("8 Merkle-sum tree", s8_sum_tree),
]
