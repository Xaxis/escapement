"""A relying party's verifier, in pure Python with no RPC.

It sees only what a prover hands it: block headers (80 bytes each, from the chain's genesis to the
tip of the relying party's best chain), Merkle proofs in the form `gettxoutproof` returns, raw
transactions, and the charter's public data. It never queries the UTXO set and never reads a
clock. Every failure raises Reject with the reason.

What it trusts: that the headers it is given are its best chain (a light client gets them from its
peers and keeps the one with most work), and that consensus validated the transactions in those
blocks. On regtest the proof of work is trivial, so "meets the target" proves the format, not cost.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import templates as T
from test_framework.key import TaggedHash, tweak_add_pubkey, verify_schnorr
from test_framework.messages import CBlock, CMerkleBlock, CTransaction, hash256, ser_string, ser_uint256

REGTEST_GENESIS = bytes.fromhex("0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206")[::-1]
REGTEST_BITS = 0x207FFFFF
WITNESS_COMMITMENT = bytes.fromhex("6a24aa21a9ed")


class Reject(Exception):
    pass


def need(cond: bool, why: str) -> None:
    if not cond:
        raise Reject(why)


def target(bits: int) -> int:
    need(not bits & 0x00800000, "negative compact target")
    return (bits & 0x007FFFFF) << (8 * ((bits >> 24) - 3))


def parse_tx(raw: bytes) -> CTransaction:
    tx = CTransaction()
    f = BytesIO(raw)
    try:
        tx.deserialize(f)
    except Exception as e:  # malformed bytes from a prover
        raise Reject(f"transaction does not parse: {e}") from None
    need(f.read() == b"" and tx.serialize() == raw, "transaction encoding is not canonical")
    return tx


# ----------------------------------------------------------------------------------------------
# Headers

class Headers:
    """A header chain from genesis, checked for linkage and proof of work against a fixed target
    (regtest never retargets). Heights come only from position in this chain."""

    def __init__(self, raw: list[bytes], genesis: bytes = REGTEST_GENESIS, bits: int = REGTEST_BITS):
        need(len(raw) > 0, "no headers")
        self.hashes: list[bytes] = []
        self.index: dict[bytes, int] = {}
        for i, h in enumerate(raw):
            need(len(h) == 80, f"header {i} is not 80 bytes")
            bh = hash256(h)
            if i == 0:
                need(bh == genesis, "first header is not the regtest genesis block")
            else:
                need(h[4:36] == self.hashes[-1], f"header {i} does not link to header {i - 1}")
            nbits = int.from_bytes(h[72:76], "little")
            need(nbits == bits, f"header {i} has nBits {nbits:08x}, expected {bits:08x}")
            need(int.from_bytes(bh, "little") <= target(nbits), f"header {i} does not meet its target")
            self.index[bh] = i
            self.hashes.append(bh)
        self.raw = raw

    @property
    def tip(self) -> int:
        return len(self.hashes) - 1

    def height_of(self, block_hash: bytes) -> int:
        need(block_hash in self.index, f"block {block_hash[::-1].hex()[:16]} is not in the best header chain")
        return self.index[block_hash]

    def hash_at(self, height: int) -> bytes:
        need(0 <= height <= self.tip, f"height {height} is beyond the best chain's tip {self.tip}")
        return self.hashes[height]

    def merkle_root_at(self, height: int) -> bytes:
        return self.raw[height][36:68]

    def confirmations(self, height: int) -> int:
        return self.tip - height + 1


# ----------------------------------------------------------------------------------------------
# Merkle proofs

def extract_matches(nTx: int, hashes: list[bytes], bits: list[bool]) -> tuple[bytes, list[tuple[bytes, int]]]:
    """Bitcoin Core's CPartialMerkleTree::ExtractMatches, including the CVE-2012-2459 check."""
    need(nTx > 0, "partial Merkle tree has no transactions")
    need(nTx <= 4_000_000 // 240, "partial Merkle tree claims too many transactions")
    need(len(hashes) <= nTx, "partial Merkle tree has more hashes than transactions")
    need(len(bits) >= len(hashes), "partial Merkle tree has too few flag bits")

    def width(height: int) -> int:
        return (nTx + (1 << height) - 1) >> height

    height = 0
    while width(height) > 1:
        height += 1
    used = {"bits": 0, "hashes": 0}
    matches: list[tuple[bytes, int]] = []

    def walk(h: int, pos: int) -> bytes:
        need(used["bits"] < len(bits), "partial Merkle tree ran out of flag bits")
        flag = bits[used["bits"]]
        used["bits"] += 1
        if h == 0 or not flag:
            need(used["hashes"] < len(hashes), "partial Merkle tree ran out of hashes")
            value = hashes[used["hashes"]]
            used["hashes"] += 1
            if h == 0 and flag:
                matches.append((value, pos))
            return value
        left = walk(h - 1, pos * 2)
        if pos * 2 + 1 < width(h - 1):
            right = walk(h - 1, pos * 2 + 1)
            need(right != left, "partial Merkle tree repeats a node (CVE-2012-2459)")
        else:
            right = left
        return hash256(left + right)

    root = walk(height, 0)
    need((used["bits"] + 7) // 8 == (len(bits) + 7) // 8, "partial Merkle tree has unused flag bytes")
    need(used["hashes"] == len(hashes), "partial Merkle tree has unused hashes")
    return root, matches


def tx_in_block(headers: Headers, proof: bytes, tx: CTransaction) -> tuple[int, int]:
    """(height, position) of tx in the best chain, from a gettxoutproof proof."""
    mb = CMerkleBlock()
    try:
        mb.deserialize(BytesIO(proof))
    except Exception as e:
        raise Reject(f"Merkle proof does not parse: {e}") from None
    header = mb.header.serialize()
    height = headers.height_of(hash256(header))
    root, matches = extract_matches(mb.txn.nTransactions, [ser_uint256(h) for h in mb.txn.vHash],
                                    list(mb.txn.vBits))
    need(root == header[36:68], "Merkle proof does not reach the block's Merkle root")
    for txid, pos in matches:
        if txid == tx.txid:
            return height, pos
    raise Reject(f"Merkle proof does not include transaction {tx.txid_hex[:16]}")


def fold_branch(leaf: bytes, branch: list[bytes], index: int) -> bytes:
    h = leaf
    for sibling in branch:
        h = hash256(sibling + h) if index & 1 else hash256(h + sibling)
        index >>= 1
    need(index == 0, "Merkle branch is shorter than its index needs")
    return h


def witness_committed(headers: Headers, link: dict, tx: CTransaction, height: int, pos: int) -> None:
    """The witness a prover shows is the one the block committed to (BIP141): the tx's wtxid is in
    the witness Merkle tree whose root, with the coinbase's reserved value, is in the coinbase."""
    cb = parse_tx(link["coinbase"])
    cb_height, cb_pos = tx_in_block(headers, link["coinbase_proof"], cb)
    need(cb_height == height and cb_pos == 0, "coinbase is not the first transaction of the same block")
    need(len(cb.vin) == 1 and cb.vin[0].prevout.hash == 0 and cb.vin[0].prevout.n == 0xFFFFFFFF,
         "coinbase is not a coinbase")
    commitments = [o.scriptPubKey for o in cb.vout
                   if len(o.scriptPubKey) >= 38 and o.scriptPubKey[:6] == WITNESS_COMMITMENT]
    need(bool(commitments), "block has no witness commitment")
    stack = cb.wit.vtxinwit[0].scriptWitness.stack if cb.wit.vtxinwit else []
    need(len(stack) == 1 and len(stack[0]) == 32, "coinbase has no witness reserved value")
    need(link["index"] == pos, "wtxid branch index differs from the txid proof's position")
    root = fold_branch(tx.wtxid, link["wtxid_branch"], pos)
    need(hash256(root + stack[0]) == bytes(commitments[-1][6:38]),
         "witness is not the one the block committed to (wtxid not under the witness commitment)")


def confirmed_tx(headers: Headers, link: dict, strict: bool) -> tuple[CTransaction, int]:
    tx = parse_tx(link["tx"])
    height, pos = tx_in_block(headers, link["proof"], tx)
    if strict:
        witness_committed(headers, link, tx, height, pos)
    return tx, height


# ----------------------------------------------------------------------------------------------
# Taproot script path

def script_path(tx: CTransaction, i: int) -> tuple[bytes, bytes]:
    need(len(tx.wit.vtxinwit) > i, "input has no witness")
    stack = tx.wit.vtxinwit[i].scriptWitness.stack
    need(len(stack) >= 2, "witness is not a script-path spend")
    need(stack[-1][:1] != b"\x50", "witness carries an annex, which no template allows")
    control, script = stack[-1], stack[-2]
    need(len(control) >= 33 and (len(control) - 33) % 32 == 0 and len(control) <= 33 + 32 * 128,
         "control block has a bad length")
    need(control[0] & 0xFE == 0xC0, "leaf version is not tapscript")
    return script, control


def output_key_from(script: bytes, control: bytes) -> bytes:
    """Recompute the Taproot output key a script-path spend commits to (BIP341)."""
    internal = control[1:33]
    k = TaggedHash("TapLeaf", bytes([control[0] & 0xFE]) + ser_string(script))
    for j in range(33, len(control), 32):
        e = control[j:j + 32]
        k = TaggedHash("TapBranch", k + e if k < e else e + k)
    q = tweak_add_pubkey(internal, TaggedHash("TapTweak", internal + k))
    need(q is not None, "internal key in the control block is not a valid point")
    need(int(q[1]) == control[0] & 1, "control block parity bit is wrong")
    return q[0]


# ----------------------------------------------------------------------------------------------
# K7 tick chain and release

@dataclass
class Entry:
    n: int
    root: bytes | None
    created: int
    status: str  # released, vetoed, renewed, open, halted, ended
    tier: int | None = None
    spent_at: int | None = None
    spend_txid: str | None = None
    leaf: str | None = None

    def __str__(self) -> str:
        s = f"entry {self.n} {self.status}"
        if self.tier:
            s += f" at tier {self.tier}"
        if self.spent_at is not None:
            s += f" at height {self.spent_at}"
        return s


def walk_chain(headers: Headers, tpl: T.TickTemplate, t0: tuple[str, int] | None, links: list[dict],
               roots: dict[int, bytes], strict: bool = True, start: int = 0) -> list[Entry]:
    """Follow the chain from T_start through every link, classify each spend by its revealed leaf,
    and return one Entry per index. Rejects on any break in the chain or the template.

    links[0] is the transaction that created T_start. t0 is the charter's pinned (txid, vout) for
    it; None means unpinned (output 0 of whatever links[0] is). What a relying party must do is
    walk from a pinned T_0. Unpinned, or starting above 0 (the shortcut K7(e) describes: the
    transaction that created T_n plus its release), it cannot tell the identity's outputs from
    copies built to the same template, which the lab shows."""
    need(len(links) > 0, "no links")

    def root(n: int) -> bytes:
        need(n in roots, f"root for entry {n} not disclosed")
        return roots[n]

    tx0, h0 = confirmed_tx(headers, links[0], strict=False)  # only its outputs matter
    vout = 0
    if t0 is not None:
        need(tx0.txid_hex == t0[0], f"first link is not the transaction that created the charter's T_{start}")
        vout = t0[1]
    need(len(tx0.vout) > vout, "first transaction has no such output")
    need(tx0.vout[vout].scriptPubKey == tpl.tick(start, root(start)).scriptPubKey,
         f"T_{start} does not match the template for root_{start}")
    prev_tx, prev_vout, created, n, state = tx0, vout, h0, start, "tick"
    entries: list[Entry] = []
    scripts = tpl.scripts()
    names = {bytes(s): name for name, s in scripts.items()}
    for k, link in enumerate(links[1:], 1):
        need(state != "ended", f"link {k} follows a veto that did not pay to the halt template; "
                               f"the chain ended at entry {n}")
        tx, height = confirmed_tx(headers, link, strict)
        need(len(tx.vin) == 1, f"link {k} has {len(tx.vin)} inputs; chain links have one")
        need(tx.vin[0].prevout.hash == prev_tx.txid_int and tx.vin[0].prevout.n == prev_vout,
             f"gap: link {k} does not spend the previous link's chain output")
        spent_spk = prev_tx.vout[prev_vout].scriptPubKey
        script, control = script_path(tx, 0)
        need(spent_spk == bytes([0x51, 0x20]) + output_key_from(script, control),
             f"link {k}: revealed leaf and control block do not open the spent output")
        want_internal = tpl.tick_key(n, root(n))[0] if state == "tick" else tpl.halt_key(n)[0]
        need(control[1:33] == want_internal,
             f"link {k}: internal key is not H + r_n*G for (charter, {n}, root_{n})"
             if state == "tick" else f"link {k}: internal key is not the halt key for entry {n}")
        leaf = names.get(bytes(script))
        need(leaf is not None, f"link {k}: revealed leaf is not in the template")
        if state == "halt":
            need(leaf == "renew", f"link {k}: a halted chain resumes only through renew, not {leaf}")
        if leaf in ("advance2", "advance3"):
            wait = tpl.n2 if leaf == "advance2" else tpl.n3
            need(height - created >= wait, f"link {k}: {leaf} confirmed {height - created} blocks "
                                           f"after T_{n}, before its wait of {wait}")
            need(tx.vout[0].scriptPubKey == tpl.tick(n + 1, root(n + 1)).scriptPubKey,
                 f"link {k}: release of entry {n} does not create T_{n + 1} for root_{n + 1}")
            entries.append(Entry(n, root(n), created, "released", int(leaf[-1]), height,
                                 tx.txid_hex, leaf))
            n, state = n + 1, "tick"
        elif leaf.startswith("veto"):
            entries.append(Entry(n, root(n), created, "vetoed", None, height, tx.txid_hex, leaf))
            state = "halt" if tx.vout[0].scriptPubKey == tpl.halt(n).scriptPubKey else "ended"
        elif leaf == "renew":
            if state == "tick":
                entries.append(Entry(n, root(n), created, "renewed", None, height, tx.txid_hex, leaf))
            need(tx.vout[0].scriptPubKey == tpl.tick(n + 1, root(n + 1)).scriptPubKey,
                 f"link {k}: renew does not create T_{n + 1} for root_{n + 1}")
            n, state = n + 1, "tick"
        prev_tx, prev_vout, created = tx, 0, height
    if state == "tick":
        entries.append(Entry(n, roots.get(n), created, "open"))
    elif state == "ended":
        entries[-1].status = "vetoed, chain ended"
    return entries


def verify_release(headers: Headers, tpl: T.TickTemplate, t0: tuple[str, int] | None, links: list[dict],
                   roots: dict[int, bytes], n: int, d: int, strict: bool = True, tier: int = 2,
                   start: int = 0) -> str:
    entries = walk_chain(headers, tpl, t0, links, roots, strict, start)
    match = [e for e in entries if e.n == n]
    need(bool(match), f"the chain shown has no entry {n}")
    e = match[0]
    need(e.status == "released", f"entry {n} was not released: {e.status} through {e.leaf}"
         if e.leaf else f"entry {n} was not released: {e.status}")
    need(e.tier >= tier, f"entry {n} was released at tier {e.tier}, below tier {tier}")
    conf = headers.confirmations(e.spent_at)
    need(conf >= d, f"release of entry {n} has {conf} confirmation(s), fewer than d = {d}")
    return f"entry {n} released at tier {e.tier} at height {e.spent_at}, {conf} confirmations"


def find_spend(headers: Headers, blocks: list[bytes], start: int, txid: bytes, vout: int):
    """Scan full blocks start, start+1, ... (each checked against the header chain) for a spend of
    (txid, vout). This is what completeness at the tip costs a client without the UTXO set."""
    for i, raw in enumerate(blocks):
        block = CBlock()
        block.deserialize(BytesIO(raw))
        height = start + i
        need(hash256(block.serialize()[:80]) == headers.hash_at(height), f"block {height} is not the chain's")
        need(ser_uint256(block.calc_merkle_root()) == headers.merkle_root_at(height),
             f"block {height}'s transactions do not match its header")
        for tx in block.vtx:
            for vin in tx.vin:
                if vin.prevout.hash == int.from_bytes(txid, "little") and vin.prevout.n == vout:
                    return height, tx.txid_hex
    return None


# ----------------------------------------------------------------------------------------------
# K8 lease

def verify_lease(headers: Headers, cid: bytes, guardians: list[bytes], L: int,
                 renewals: list[dict], release_height: int) -> str:
    """Accept a release at release_height only if some renewal, signed by every guardian over
    (cid, k, h_k, hash of block h_k) with h_k in this header chain, has h_k <= h <= h_k + L.
    Only heights from the header chain are compared; no clock is read."""
    valid, notes = [], []
    for r in renewals:
        try:
            need(r["h_k"] <= headers.tip, f"renewal {r['k']} names height {r['h_k']} beyond the tip")
            need(headers.hash_at(r["h_k"]) == r["blockhash"],
                 f"renewal {r['k']} names a block that is not the best chain's block {r['h_k']}")
            msg = T.lease_message(cid, r["k"], r["h_k"], r["blockhash"])
            need(len(r["sigs"]) == len(guardians), f"renewal {r['k']} lacks a guardian signature")
            for g, sig in zip(guardians, r["sigs"]):
                need(len(sig) == 64 and verify_schnorr(g, sig, msg),
                     f"renewal {r['k']} has an invalid guardian signature")
            valid.append(r)
        except Reject as e:
            notes.append(str(e))
    need(bool(valid), "no valid renewal: " + "; ".join(notes))
    covering = [r for r in valid if r["h_k"] <= release_height <= r["h_k"] + L]
    need(bool(covering), f"release at height {release_height} is outside every lease "
                         + ", ".join(f"[{r['h_k']}, {r['h_k'] + L}]" for r in valid))
    best = max(covering, key=lambda r: r["k"])
    return f"lease {best['k']} covers height {release_height} (window [{best['h_k']}, {best['h_k'] + L}])"


# ----------------------------------------------------------------------------------------------
# K1 bond

def verify_bond(headers: Headers, link: dict, vout: int, cid: bytes, tweak: bytes, leaves: list[bytes],
                principal: bytes, locktime: int, min_value: int, season: int) -> str:
    """Recompute the bond's output key from the revealed tweak and leaves, and check that it has
    no usable key path, that its only spendable leaf is the CLTV leaf for (principal, locktime),
    that it commits to this charter, and that it is old enough."""
    tx, height = confirmed_tx(headers, link, strict=False)
    need(len(tx.vout) > vout, "bond transaction has no such output")
    out = tx.vout[vout]
    need(tweak == TaggedHash(T.TAG_BOND, cid), "revealed tweak does not commit to this charter id")
    internal = tweak_add_pubkey(T.H, tweak)
    need(internal is not None, "tweak out of range")
    info = T.taproot_construct(internal[0], [(f"leaf{i}", s) for i, s in enumerate(leaves)])
    need(out.scriptPubKey == info.scriptPubKey,
         "revealed tweak and leaves do not produce the bond's output key (a leaf is hidden or altered, "
         "or the internal key is not H + r*G)")
    need(bytes(leaves[0]) == bytes(T.bond_cltv_script(locktime, principal)),
         "first leaf is not <locktime> CLTV DROP <principal> CHECKSIG for the claimed values")
    for s in leaves[1:]:
        need(s[:1] == b"\x6a", "a leaf other than the CLTV leaf is spendable")
        need(bytes(s) == bytes(T.CScript([T.OP_RETURN, cid])), "unspendable leaf does not commit to this charter id")
    need(out.nValue >= min_value, f"bond holds {out.nValue} sats, less than {min_value}")
    age = headers.confirmations(height)
    need(age >= season, f"bond has {age} confirmations, fewer than the season S = {season}")
    # The CLTV leaf is the only spend path, and it is valid only in a block above the locktime, so
    # while the tip is at or below it the bond is unspent, with no UTXO query. After that, a
    # verifier without the UTXO set (or a scan of every later block) cannot tell, so it stops
    # counting the bond.
    need(headers.tip <= locktime, f"bond is past its locktime {locktime} (tip {headers.tip}): "
                                  "a verifier without the UTXO set cannot tell whether it is spent")
    return (f"bond of {out.nValue} sats, {age} confirmations, unspent by construction until "
            f"height {locktime} (tip {headers.tip})")


# ----------------------------------------------------------------------------------------------
# Anchoring a log

def verify_log_inclusion(headers: Headers, link: dict, vout: int, mode: str, entry: bytes,
                         proof: list[tuple[str, bytes]], log_root: bytes, internal: bytes | None = None) -> str:
    h = T.log_leaf(entry)
    for side, sib in proof:
        h = T.log_node(sib, h) if side == "L" else T.log_node(h, sib)
    need(h == log_root, "log proof does not reach the anchored root")
    tx, height = confirmed_tx(headers, link, strict=False)
    spk = tx.vout[vout].scriptPubKey
    if mode == "tweak":
        q, _, _ = T.anchor_output_key(internal, log_root)
        need(spk == bytes([0x51, 0x20]) + q, "output key is not the internal key tweaked by this log root")
    else:
        need(spk == bytes([0x6A, 0x20]) + log_root, "OP_RETURN output does not carry this log root")
    return f"entry in log anchored at height {height}, {headers.confirmations(height)} confirmations"


# ----------------------------------------------------------------------------------------------
# Merkle-sum tree

def verify_sum_proof(data: bytes, amount: int, proof: list[tuple[str, bytes, int, int]],
                     root: tuple[bytes, int, int], root_n: bytes, cap: int) -> str:
    """Check one leaf's inclusion in a Merkle-sum tree whose root commitment is root_n, that every
    amount and partial sum on the path is non-negative and adds up, and that the total is <= cap."""
    need(isinstance(amount, int) and amount >= 0, f"leaf amount {amount} is negative")
    node = T.sum_leaf(data, amount)
    for side, h, count, total in proof:
        need(count >= 1, f"sibling count {count} is not positive")
        need(total >= 0, f"sibling sum {total} is negative")
        sib = T.SumNode(h, count, total)
        try:
            node = T.sum_parent(sib, node) if side == "L" else T.sum_parent(node, sib)
        except ValueError as e:
            raise Reject(f"sum tree node out of range: {e}") from None
    claimed = T.SumNode(*root)
    need(node.hash == claimed.hash, "proof does not reach the claimed root hash")
    need(node.count == claimed.count and node.total == claimed.total,
         f"sums do not add: path gives count {node.count} and total {node.total}, "
         f"root claims {claimed.count} and {claimed.total}")
    need(T.sum_root_commitment(node) == root_n, "root does not match the tick's committed root_n")
    need(node.total <= cap, f"total {node.total} exceeds the cap {cap}")
    return f"leaf of {amount} included; {node.count} leaves, total {node.total} <= cap {cap}"


def proof_bytes(links: list[dict], strict: bool = True) -> int:
    """Bytes a prover sends for these links (headers not counted)."""
    total = 0
    for link in links:
        total += len(link["tx"]) + len(link["proof"])
        if strict:
            total += len(link["coinbase"]) + len(link["coinbase_proof"]) + 32 * len(link["wtxid_branch"]) + 4
    return total
