#!/usr/bin/env python3
"""Resolve citation keys: print each key's primary key in research/sources.toml and its title.

A note's key can be merged into another source's entry (listed in that entry's `also`). Run this
before citing: python3 tools/keys.py KEY [KEY ...]. With --fix FILE, rewrite merged keys in FILE
to their primary key.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def table() -> tuple[dict, dict]:
    srcs = tomllib.loads((ROOT / "research" / "sources.toml").read_text())["source"]
    alias = {}
    for key, s in srcs.items():
        for other in s.get("also", []):
            alias.setdefault(other, key)
    return srcs, alias


def main(argv: list[str]) -> int:
    srcs, alias = table()
    if argv[:1] == ["--fix"]:
        path = Path(argv[1])
        text = path.read_text()
        cite = re.compile(r"(?<![\w.])@([A-Za-z][\w:-]*[\w])")
        unknown = set()

        def swap(m: re.Match) -> str:
            k = m.group(1)
            if k in srcs:
                return m.group(0)
            if k in alias:
                return "@" + alias[k]
            unknown.add(k)
            return m.group(0)

        text = re.sub(r"\[[^\[\]]*@[^\[\]]*\]", lambda g: cite.sub(swap, g.group(0)), text)
        path.write_text(text)
        for k in sorted(unknown):
            print(f"unknown: {k}")
        return 1 if unknown else 0
    bad = 0
    for k in argv:
        if k in srcs:
            print(f"{k:28} ok      {srcs[k]['title'][:70]}")
        elif k in alias:
            print(f"{k:28} -> {alias[k]:20} {srcs[alias[k]]['title'][:60]}")
        else:
            hits = [s for s in srcs if k.lower()[:6] in s.lower()]
            print(f"{k:28} MISSING  near: {' '.join(hits[:5])}")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
