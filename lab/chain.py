"""The builder's side of the lab: keys, funding, signing, broadcasting, measuring, and the proof
packages a prover hands a relying party.

Everything here talks to bitcoind through RPC, because the builder runs a full node. The relying
party's side, verify.py, never does.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import templates  # noqa: F401  (puts the pinned test framework on sys.path)
from node import RPCError
from test_framework.key import compute_xonly_pubkey, sign_schnorr, tweak_add_privkey
from test_framework.messages import CBlock, COutPoint, CTransaction, CTxIn, CTxInWitness, CTxOut, from_hex, hash256, sha256
from test_framework.script import SIGHASH_DEFAULT, TaprootSignatureHash
from test_framework.segwit_addr import encode_segwit_address

ROOT = Path(__file__).resolve().parent.parent
SEQ_FINAL_RBF = 0xFFFFFFFD  # no relative lock time, nLockTime enforced, replaceable


def model_value(name: str):
    """A number from the model's ledger (data/numbers.json), so the lab's parameters are the
    model's, not new numbers. Block counts and amounts come back as ints."""
    value = json.loads((ROOT / "data" / "numbers.json").read_text())[name]["value"]
    return int(value) if float(value).is_integer() else value


class Key:
    """A deterministic test key. Lab keys are derived from their names so runs are comparable;
    they protect nothing and must never hold real coins."""

    def __init__(self, name: str):
        self.name = name
        self.priv = sha256(b"escapement-lab/" + name.encode())
        self.x = compute_xonly_pubkey(self.priv)[0]


@dataclass
class Coin:
    txid: str  # display order hex
    vout: int
    out: CTxOut
    height: int | None = None  # confirmation height, None while unconfirmed

    @property
    def outpoint(self) -> COutPoint:
        return COutPoint(int(self.txid, 16), self.vout)


def p2tr(xonly: bytes) -> bytes:
    return bytes([0x51, 0x20]) + xonly


def control_block(info, leaf: str) -> bytes:
    lf = info.leaves[leaf]
    return bytes([lf.version | info.negflag]) + info.internal_pubkey + lf.merklebranch


def leaf_sig(tx: CTransaction, idx: int, spent: list[CTxOut], script: bytes, key: Key) -> bytes:
    # 0xffffffff is BIP342's "no OP_CODESEPARATOR executed". The framework's default, -1, no longer
    # serialises since its switch to int.to_bytes(signed=False), so it is passed explicitly.
    msg = TaprootSignatureHash(tx, spent, SIGHASH_DEFAULT, idx, scriptpath=True, leaf_script=script,
                               codeseparator_pos=0xFFFFFFFF)
    return sign_schnorr(key.priv, msg)


def keypath_sig(tx: CTransaction, idx: int, spent: list[CTxOut], priv: bytes) -> bytes:
    return sign_schnorr(priv, TaprootSignatureHash(tx, spent, SIGHASH_DEFAULT, idx))


def set_witness(tx: CTransaction, stacks: list[list[bytes]]) -> None:
    tx.wit.vtxinwit = []
    for stack in stacks:
        w = CTxInWitness()
        w.scriptWitness.stack = list(stack)
        tx.wit.vtxinwit.append(w)


def merkle_branch(hashes: list[bytes], index: int) -> list[bytes]:
    """Sibling hashes from leaf to root in Bitcoin's Merkle tree (last node paired with itself)."""
    branch = []
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        branch.append(level[index ^ 1])
        level = [hash256(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        index //= 2
    return branch


class Lab:
    def __init__(self, node):
        self.node = node
        self.rpc = node.rpc
        self.feerate = model_value("feerate-2026")  # sat/vB, the model's 2026 median
        self.n2 = model_value("tier2-delay-blocks")
        self.n3 = model_value("tier3-delay-blocks")
        self.lease = model_value("lease-blocks")
        self.season = model_value("season-blocks")
        self.d = model_value("confirmations-standard")
        self.bond_min = model_value("bond-coverage")
        self.cap = model_value("allowance-per-lease")
        self.clock = int(time.time())  # the node's simulated clock: 600 s per block, see mine()
        self._headers: list[bytes] = []
        self.funder = Key("funder")
        self.funder_spk = p2tr(self.funder.x)
        self.funder_addr = encode_segwit_address("bcrt", 1, self.funder.x)
        self.pool: list[Coin] = []
        self.checks: list[dict] = []
        self.sizes: list[dict] = []
        self.scenario = ""
        self.state: dict = {}  # what one scenario leaves for a later one
        self.extra: dict = {}  # measurements that are not transactions, for results.json

    # chain -------------------------------------------------------------------------------------

    def setup(self, coins: int = 30) -> None:
        """Mine coinbases to the funder's key until `coins` of them are mature."""
        self.mine(100 + coins)
        for h in range(1, coins + 1):
            block = self.rpc("getblock", self.rpc("getblockhash", h), 2)
            cb = block["tx"][0]
            value = round(cb["vout"][0]["value"] * 100_000_000)
            self.pool.append(Coin(cb["txid"], 0, CTxOut(value, self.funder_spk), h))

    def height(self) -> int:
        return self.rpc("getblockcount")

    def mine(self, n: int = 1) -> list[str]:
        """Mine n blocks to the funder. The node's clock (setmocktime) moves 600 s per block, so
        block times look like a real chain and never run more than 2 h ahead of the node's clock,
        however fast regtest mines. Nothing in the lab depends on block times."""
        hashes: list[str] = []
        while n > 0:
            step = min(n, 500)
            self.rpc("setmocktime", self.clock)
            hashes += self.rpc("generatetoaddress", step, self.funder_addr)
            self.clock += 600 * step
            n -= step
        self._refresh_pool()
        return hashes

    def generate_block(self, txs: list[CTransaction]) -> str:
        """Mine one block holding exactly these transactions (a miner's choice), bypassing the
        mempool."""
        self.rpc("setmocktime", self.clock)
        block = self.rpc("generateblock", self.funder_addr, [t.serialize().hex() for t in txs])["hash"]
        self.clock += 600
        self._refresh_pool()
        return block

    def mine_to(self, height: int) -> None:
        self.mine(height - self.height())

    def _refresh_pool(self) -> None:
        for coin in self.pool:
            if coin.height is None:
                info = self.rpc("getrawtransaction", coin.txid, True)
                if info.get("confirmations"):
                    coin.height = self.rpc("getblockheader", info["blockhash"])["height"]

    def confirmed_height(self, txid: str) -> int:
        info = self.rpc("getrawtransaction", txid, True)
        return self.rpc("getblockheader", info["blockhash"])["height"]

    # building ----------------------------------------------------------------------------------

    def take_coin(self) -> Coin:
        for i, coin in enumerate(self.pool):
            if coin.height is not None:
                return self.pool.pop(i)
        raise RuntimeError("no confirmed funder coin; mine a block first")

    def build(self, inputs: list[tuple[Coin, int]], outputs: list[CTxOut], witness, *,
              version: int = 2, locktime: int = 0, fee_output: int | None = 0,
              feerate: float | None = None, fee: int | None = None) -> tuple[CTransaction, int]:
        """A signed transaction. `witness(tx, spent)` returns one witness stack per input and is
        called twice: once to size the transaction, once to sign it with the final amounts.
        With fee_output set, that output pays the fee (fee_rate times vsize, or `fee`); with
        fee_output None, the outputs are taken as given and the fee is what is left."""
        tx = CTransaction()
        tx.version = version
        tx.nLockTime = locktime
        tx.vin = [CTxIn(coin.outpoint, b"", seq) for coin, seq in inputs]
        tx.vout = outputs
        spent = [coin.out for coin, _ in inputs]
        total = sum(c.out.nValue for c, _ in inputs)
        if fee_output is not None:
            others = sum(o.nValue for i, o in enumerate(outputs) if i != fee_output)
            outputs[fee_output].nValue = total - others
            set_witness(tx, witness(tx, spent))
            fee = fee if fee is not None else math.ceil(tx.get_vsize() * (feerate or self.feerate))
            outputs[fee_output].nValue -= fee
        set_witness(tx, witness(tx, spent))
        return tx, total - sum(o.nValue for o in tx.vout)

    def fund(self, spk: bytes, amount: int, kind: str | None = None) -> Coin:
        """Pay `amount` to `spk` from the funder's coins and confirm nothing yet."""
        coin = self.take_coin()
        tx, fee = self.build(
            [(coin, SEQ_FINAL_RBF)], [CTxOut(amount, spk), CTxOut(0, self.funder_spk)],
            lambda tx, spent: [[keypath_sig(tx, 0, spent, self.funder.priv)]], fee_output=1)
        txid = self.send(tx)
        self.pool.append(Coin(txid, 1, tx.vout[1]))
        if kind:
            self.size(kind, tx, fee)
        return Coin(txid, 0, tx.vout[0])

    def send(self, tx: CTransaction) -> str:
        return self.rpc("sendrawtransaction", tx.serialize().hex(), 0)

    def submit(self, tx: CTransaction) -> dict:
        """Test, then broadcast. Returns accepted, txid, the broadcast's reject message and the
        mempool test's reject reason."""
        hexed = tx.serialize().hex()
        tma = self.rpc("testmempoolaccept", [hexed], 0)[0]
        try:
            txid = self.rpc("sendrawtransaction", hexed, 0)
            return {"accepted": True, "txid": txid, "reason": None, "tma": None}
        except RPCError as e:
            return {"accepted": False, "txid": tx.txid_hex, "reason": e.message,
                    "tma": tma.get("reject-reason")}

    # recording ---------------------------------------------------------------------------------

    def size(self, kind: str, tx: CTransaction, fee: int, note: str = "") -> dict:
        row = {"kind": kind, "vbytes": tx.get_vsize(), "weight": tx.get_weight(), "fee_sat": fee,
               "feerate_sat_vb": round(fee / tx.get_vsize(), 3), "txid": tx.txid_hex,
               "inputs": len(tx.vin), "outputs": len(tx.vout), "version": tx.version}
        if note:
            row["note"] = note
        self.sizes.append(row)
        return row

    def record(self, check: str, expectation: str, ok: bool, observed: str, *,
               reason: str | None = None, txids: list[str] | None = None,
               vbytes: int | None = None) -> bool:
        row = {"scenario": self.scenario, "check": check, "expectation": expectation,
               "observed": observed, "reject_reason": reason, "pass": bool(ok),
               "txids": txids or [], "vbytes": vbytes}
        self.checks.append(row)
        mark = "PASS" if ok else "FAIL"
        print(f"  {mark} {check}: {observed}", flush=True)
        return ok

    def expect(self, check: str, tx: CTransaction, reject: str | None = None, *,
               kind: str | None = None, fee: int | None = None, note: str = "") -> dict:
        """Broadcast tx and assert the node accepts it (reject None) or rejects it with a reason
        containing `reject`."""
        r = self.submit(tx)
        if reject is None:
            ok = r["accepted"]
            expectation = "accepted"
        else:
            reasons = " | ".join(x for x in (r["reason"], r["tma"]) if x)
            ok = (not r["accepted"]) and reject in reasons
            expectation = f"rejected: {reject}"
        if r["accepted"]:
            observed = "accepted"
        else:
            observed = f"rejected: {r['reason'].split(', input ')[0]}"
            if r["tma"] and r["tma"] not in r["reason"]:
                observed += f" (testmempoolaccept: {r['tma']})"
        self.record(check, expectation, ok, observed, reason=r["reason"], txids=[r["txid"]],
                    vbytes=tx.get_vsize())
        if r["accepted"] and kind:
            self.size(kind, tx, fee if fee is not None else 0, note)
        return r

    def vcheck(self, check: str, fn, reject: str | None = None) -> object:
        """Run a verifier call and assert it accepts (reject None) or raises Reject with a message
        containing `reject`."""
        from verify import Reject
        try:
            value = fn()
        except Reject as e:
            ok = reject is not None and reject in str(e)
            self.record(check, "verifier rejects: " + reject if reject else "verifier accepts", ok,
                        f"verifier rejected: {e}", reason=str(e))
            return None
        observed = "verifier accepted" + (f": {value}" if isinstance(value, str) else "")
        self.record(check, "verifier rejects: " + reject if reject else "verifier accepts",
                    reject is None, observed)
        return value

    # proofs for a relying party ----------------------------------------------------------------

    def headers(self) -> list[bytes]:
        """Every header of the node's best chain, genesis first (cached; reorgs are handled)."""
        tip = self.height()
        hdr = self._headers
        while hdr and (len(hdr) - 1 > tip or
                       self.rpc("getblockhash", len(hdr) - 1) != hash256(hdr[-1])[::-1].hex()):
            hdr.pop()
        for h in range(len(hdr), tip + 1):
            hdr.append(bytes.fromhex(self.rpc("getblockheader", self.rpc("getblockhash", h), False)))
        return list(hdr)

    def link(self, txid: str, blockhash: str | None = None) -> dict:
        """What a prover hands over for one confirmed transaction: the raw transaction, its txid
        Merkle proof, and the proof that its witness is committed (coinbase, coinbase proof, wtxid
        branch)."""
        if blockhash is None:
            blockhash = self.rpc("getrawtransaction", txid, True)["blockhash"]
        block = from_hex(CBlock(), self.rpc("getblock", blockhash, 0))
        txids = [t.txid_hex for t in block.vtx]
        index = txids.index(txid)
        wtxids = [bytes(32)] + [t.wtxid for t in block.vtx[1:]]
        return {
            "tx": block.vtx[index].serialize(),
            "proof": bytes.fromhex(self.rpc("gettxoutproof", [txid], blockhash)),
            "coinbase": block.vtx[0].serialize(),
            "coinbase_proof": bytes.fromhex(self.rpc("gettxoutproof", [txids[0]], blockhash)),
            "wtxid_branch": merkle_branch(wtxids, index),
            "index": index,
        }

    def raw_blocks(self, start: int, end: int) -> list[bytes]:
        return [bytes.fromhex(self.rpc("getblock", self.rpc("getblockhash", h), 0))
                for h in range(start, end + 1)]


def tweaked_priv(priv: bytes, tweak: bytes) -> bytes:
    return tweak_add_privkey(priv, tweak)
