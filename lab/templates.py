"""The published templates: what a relying party and a builder both agree on.

Everything here is a pure function of public data (charter id, public keys, block counts), so the
builder (chain.py) and the relying-party verifier (verify.py) compute identical scripts, keys and
commitments from it. Taproot construction, tagged hashes and secp256k1 arithmetic come from
Bitcoin Core's functional test framework (MIT), pinned in lab/bitcoin-core.txt.

Serialisation, fixed here so that anyone can recompute every commitment:
  charter id   32 bytes
  index n, k   8 bytes little-endian
  height       4 bytes little-endian
  amount, sum  8 bytes little-endian, unsigned (a verifier rejects negative values before hashing)
"""

from __future__ import annotations

import sys
from collections import namedtuple

import fetch

sys.path.insert(0, str(fetch.framework_root()))

from test_framework.key import H_POINT, TaggedHash, tweak_add_pubkey  # noqa: E402
from test_framework.messages import sha256  # noqa: E402
from test_framework.script import (  # noqa: E402
    OP_CHECKLOCKTIMEVERIFY,
    OP_CHECKSEQUENCEVERIFY,
    OP_CHECKSIG,
    OP_CHECKSIGADD,
    OP_CHECKSIGVERIFY,
    OP_DROP,
    OP_NUMEQUAL,
    OP_RETURN,
    CScript,
    taproot_construct,
)

H = bytes.fromhex(H_POINT)  # BIP341's NUMS point: lift_x(SHA256(G)), nobody knows its discrete log

TAG_TICK = "Escapement/tick"
TAG_HALT = "Escapement/halt"
TAG_BOND = "Escapement/bond"
TAG_COSIGN = "Escapement/cosign"
TAG_LEASE = "Escapement/lease"
TAG_ANCHOR = "Escapement/anchor"
TAG_LOG_LEAF = "Escapement/log-leaf"
TAG_LOG_NODE = "Escapement/log-node"
TAG_SUM_LEAF = "Escapement/sum-leaf"
TAG_SUM_NODE = "Escapement/sum-node"
TAG_SUM_ROOT = "Escapement/sum-root"

P2A_SCRIPT = bytes([0x51, 0x02, 0x4E, 0x73])  # pay-to-anchor: OP_1 <0x4e73>
MAX_AMOUNT = (1 << 63) - 1


def u64(v: int) -> bytes:
    return v.to_bytes(8, "little")


def u32(v: int) -> bytes:
    return v.to_bytes(4, "little")


def nums_key(tag: str, data: bytes) -> tuple[bytes, bytes]:
    """(x-only key H + r*G, r) with r = TaggedHash(tag, data). Anyone given data can recompute it,
    and nobody knows its secret unless they know the discrete log of H."""
    r = TaggedHash(tag, data)
    point = tweak_add_pubkey(H, r)
    if point is None:
        raise ValueError("tweak out of range")
    return point[0], r


# ----------------------------------------------------------------------------------------------
# K1 bond

def bond_info(cid: bytes, principal: bytes, locktime: int, variant: str = "tweak"):
    """The bond output.

    variant "tweak": internal key H + r*G with r = TaggedHash("Escapement/bond", cid), one leaf
      `<locktime> OP_CHECKLOCKTIMEVERIFY OP_DROP <principal> OP_CHECKSIG`. The charter id is
      committed by the internal key alone.
    variant "leaf": the same internal key plus a second, unspendable leaf `OP_RETURN <cid>`, the
      form the claims file describes (a script leaf that commits to the charter id).
    """
    internal, _ = nums_key(TAG_BOND, cid)
    leaves = [("cltv", bond_cltv_script(locktime, principal))]
    if variant == "leaf":
        leaves.append(("charter", CScript([OP_RETURN, cid])))
    elif variant != "tweak":
        raise ValueError(variant)
    return taproot_construct(internal, leaves)


def bond_cltv_script(locktime: int, principal: bytes) -> CScript:
    return CScript([locktime, OP_CHECKLOCKTIMEVERIFY, OP_DROP, principal, OP_CHECKSIG])


# ----------------------------------------------------------------------------------------------
# K7 tick chain

class TickTemplate:
    """The script tree every tick output T_n of one charter shares. Only the internal key changes
    from one tick to the next: P_n = H + r_n*G, r_n = TaggedHash("Escapement/tick",
    cid || n || root_n).

    Tree shape (fixed, so the control blocks are predictable): advance2 at depth 1, because it is
    the spend a healthy chain uses most; advance3, renew and veto_1 at depth 3; veto_2 and veto_3
    at depth 4.
    """

    def __init__(self, cid: bytes, agent: bytes, guardians: list[bytes], n2: int, n3: int):
        assert len(cid) == 32 and len(agent) == 32 and all(len(g) == 32 for g in guardians)
        self.cid, self.agent, self.guardians, self.n2, self.n3 = cid, agent, list(guardians), n2, n3

    def scripts(self) -> dict[str, CScript]:
        g = self.guardians
        out = {
            "advance2": CScript([self.n2, OP_CHECKSEQUENCEVERIFY, OP_DROP, self.agent, OP_CHECKSIG]),
            "advance3": CScript([self.n3, OP_CHECKSEQUENCEVERIFY, OP_DROP, self.agent, OP_CHECKSIGVERIFY]
                                + [x for k in g[:-1] for x in (k, OP_CHECKSIGVERIFY)] + [g[-1], OP_CHECKSIG]),
            "renew": all_of(g),
        }
        for i, k in enumerate(g, 1):
            out[f"veto_{i}"] = CScript([k, OP_CHECKSIG])
        return out

    def tree(self) -> list:
        s = self.scripts()
        vetoes = [(f"veto_{i}", s[f"veto_{i}"]) for i in range(1, len(self.guardians) + 1)]
        return [("advance2", s["advance2"]),
                [("advance3", s["advance3"]), ("renew", s["renew"])] + vetoes]

    def tick_key(self, n: int, root: bytes) -> tuple[bytes, bytes]:
        assert len(root) == 32
        return nums_key(TAG_TICK, self.cid + u64(n) + root)

    def tick(self, n: int, root: bytes):
        return taproot_construct(self.tick_key(n, root)[0], self.tree())

    def halt_key(self, n: int) -> tuple[bytes, bytes]:
        return nums_key(TAG_HALT, self.cid + u64(n))

    def halt(self, n: int):
        """The output a veto of T_n pays to, so that the chain can be restarted: one leaf, renew."""
        return taproot_construct(self.halt_key(n)[0], [("renew", all_of(self.guardians))])


def all_of(keys: list[bytes]) -> CScript:
    """Every key must sign: <k1> CHECKSIGVERIFY ... <kn> CHECKSIG."""
    return CScript([x for k in keys[:-1] for x in (k, OP_CHECKSIGVERIFY)] + [keys[-1], OP_CHECKSIG])


def multi_a(k: int, keys: list[bytes]) -> CScript:
    """k of n: <k1> CHECKSIG <k2> CHECKSIGADD ... <kn> CHECKSIGADD <k> NUMEQUAL."""
    items = [keys[0], OP_CHECKSIG]
    for key in keys[1:]:
        items += [key, OP_CHECKSIGADD]
    return CScript(items + [k, OP_NUMEQUAL])


# ----------------------------------------------------------------------------------------------
# Co-signing (02-design's unvault output)

def cosign_info(vault_id: bytes, agent: bytes, cosigner: bytes, n: int, guardians: list[bytes], k: int):
    """or(and(pk(agent), pk(cosigner), older(n)), thresh(k, guardians)), no key path."""
    internal, _ = nums_key(TAG_COSIGN, vault_id)
    spend = CScript([agent, OP_CHECKSIGVERIFY, cosigner, OP_CHECKSIGVERIFY, n, OP_CHECKSEQUENCEVERIFY])
    return taproot_construct(internal, [("spend", spend), ("recovery", multi_a(k, guardians))])


# ----------------------------------------------------------------------------------------------
# K8 lease

def lease_message(cid: bytes, k: int, h_k: int, blockhash: bytes) -> bytes:
    """What every guardian signs (BIP340). blockhash is the 32-byte internal byte order hash."""
    assert len(blockhash) == 32
    return TaggedHash(TAG_LEASE, cid + u64(k) + u32(h_k) + blockhash)


# ----------------------------------------------------------------------------------------------
# Anchoring a log

def anchor_tweak(log_root: bytes) -> bytes:
    """The 32 bytes used in place of a script tree's Merkle root to commit a log root into a
    Taproot output's tweak (pay to contract). The output stays spendable by its key path."""
    return TaggedHash(TAG_ANCHOR, log_root)


def anchor_output_key(internal: bytes, log_root: bytes) -> tuple[bytes, int, bytes]:
    """(output key, parity, TapTweak) for internal key + TaggedHash("TapTweak", P || c)*G."""
    tweak = TaggedHash("TapTweak", internal + anchor_tweak(log_root))
    out = tweak_add_pubkey(internal, tweak)
    return out[0], int(out[1]), tweak


def log_leaf(entry: bytes) -> bytes:
    return TaggedHash(TAG_LOG_LEAF, entry)


def log_node(left: bytes, right: bytes) -> bytes:
    return TaggedHash(TAG_LOG_NODE, left + right)


def log_tree(entries: list[bytes]) -> tuple[bytes, list[list[tuple[str, bytes]]]]:
    """Root and, for each entry, its proof [(side of sibling, sibling hash)] from leaf to root.
    A lone last node is carried up unchanged rather than paired with itself."""
    level = [log_leaf(e) for e in entries]
    proofs: list[list[tuple[str, bytes]]] = [[] for _ in entries]
    members = [[i] for i in range(len(entries))]
    while len(level) > 1:
        nxt, nxt_members = [], []
        for j in range(0, len(level), 2):
            if j + 1 == len(level):
                nxt.append(level[j])
                nxt_members.append(members[j])
                continue
            left, right = level[j], level[j + 1]
            for i in members[j]:
                proofs[i].append(("R", right))
            for i in members[j + 1]:
                proofs[i].append(("L", left))
            nxt.append(log_node(left, right))
            nxt_members.append(members[j] + members[j + 1])
        level, members = nxt, nxt_members
    return level[0], proofs


# ----------------------------------------------------------------------------------------------
# Merkle-sum tree (record entries)

SumNode = namedtuple("SumNode", "hash count total")


def sum_leaf(data: bytes, amount: int) -> SumNode:
    if not 0 <= amount <= MAX_AMOUNT:
        raise ValueError("amount out of range")
    return SumNode(TaggedHash(TAG_SUM_LEAF, sha256(data) + u64(amount)), 1, amount)


def sum_parent(left: SumNode, right: SumNode) -> SumNode:
    """Both children's counts and sums are hashed into the parent, not only their total, which is
    the fix for the summation-tree flaw where a prover could move value between siblings."""
    for node in (left, right):
        if node.count < 1 or not 0 <= node.total <= MAX_AMOUNT:
            raise ValueError("count or sum out of range")
    total = left.total + right.total
    if total > MAX_AMOUNT:
        raise ValueError("sum overflows")
    h = TaggedHash(TAG_SUM_NODE, left.hash + u64(left.count) + u64(left.total)
                   + right.hash + u64(right.count) + u64(right.total))
    return SumNode(h, left.count + right.count, total)


def sum_root_commitment(root: SumNode) -> bytes:
    """root_n for a tick: commits the tree's hash, its leaf count and its total."""
    return TaggedHash(TAG_SUM_ROOT, root.hash + u64(root.count) + u64(root.total))


def sum_tree(leaves: list[tuple[bytes, int]]):
    """Root SumNode and, for each leaf, its proof [(side, sibling SumNode)] from leaf to root."""
    level = [sum_leaf(d, a) for d, a in leaves]
    proofs: list[list[tuple[str, SumNode]]] = [[] for _ in leaves]
    members = [[i] for i in range(len(leaves))]
    while len(level) > 1:
        nxt, nxt_members = [], []
        for j in range(0, len(level), 2):
            if j + 1 == len(level):
                nxt.append(level[j])
                nxt_members.append(members[j])
                continue
            for i in members[j]:
                proofs[i].append(("R", level[j + 1]))
            for i in members[j + 1]:
                proofs[i].append(("L", level[j]))
            nxt.append(sum_parent(level[j], level[j + 1]))
            nxt_members.append(members[j] + members[j + 1])
        level, members = nxt, nxt_members
    return level[0], proofs
