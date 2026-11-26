#!/usr/bin/env python3
"""Build the paper for Paperwright: build/escapement-paper.md and build/escapement.bib.

The paper's sources (paper/*.md, in name order) cite numbers as ledger links and sources as
[@key]. Paperwright holds its own numbers and its own library, so this flattens every ledger link
to its text and writes a BibTeX file of the cited sources, with each one's DOI, arXiv ID or URL.

  python3 tools/paper.py                     build both files
  python3 tools/paper.py --keys MAP.json     rename citation keys to the ones Paperwright gave
  python3 tools/paper.py --ids               print the identifiers to add, one per line
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[([^\]]*)\]\((?:\.\./research/)?numbers\.md#[a-z0-9-]+\)")
CITE_GROUP = re.compile(r"\[([^\[\]]*@[^\[\]]*)\]")
CITE_KEY = re.compile(r"(?<![\w.])@([A-Za-z][\w:-]*[\w])")


def sources() -> dict:
    return tomllib.loads((ROOT / "research" / "sources.toml").read_text()).get("source", {})


def paper_text() -> str:
    parts = [p.read_text().rstrip() + "\n" for p in sorted((ROOT / "paper").glob("*.md"))]
    return "\n".join(parts)


def cited(text: str) -> list[str]:
    seen: list[str] = []
    for group in CITE_GROUP.findall(text):
        for key in CITE_KEY.findall(group):
            if key not in seen:
                seen.append(key)
    return seen


def identifier(s: dict) -> str:
    if s.get("doi"):
        return s["doi"]
    if s.get("arxiv"):
        return f"arXiv:{s['arxiv']}"
    if s.get("isbn"):
        return s["isbn"]
    return s.get("url", "")


def bibtex(key: str, s: dict) -> str:
    kind = {"peer-reviewed": "article", "book": "book", "preprint": "misc"}.get(s["type"], "misc")
    fields = {
        "title": "{" + s["title"] + "}",
        "author": " and ".join(s.get("authors", [])) or None,
        "year": str(s["year"]) if s.get("year") else "n.d.",
        "journal": s.get("venue") if kind == "article" else None,
        "howpublished": s.get("venue") if kind == "misc" else None,
        "doi": s.get("doi"),
        "eprint": s.get("arxiv"),
        "archiveprefix": "arXiv" if s.get("arxiv") else None,
        "isbn": s.get("isbn"),
        "url": s.get("url") if not s.get("doi") else None,
    }
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@{kind}{{{key},\n{body}\n}}\n"


def main(argv: list[str]) -> int:
    srcs = sources()
    text = paper_text()
    keys = cited(text)
    missing = [k for k in keys if k not in srcs]
    if missing:
        print(f"paper: cited keys with no source: {', '.join(missing)}", file=sys.stderr)
        return 1
    if "--ids" in argv:
        for k in keys:
            print(identifier(srcs[k]))
        return 0
    rename = {}
    if "--keys" in argv:
        rename = json.loads(Path(argv[argv.index("--keys") + 1]).read_text())
    flat = LINK.sub(lambda m: m.group(1), text)
    if rename:
        flat = CITE_KEY.sub(lambda m: "@" + rename.get(m.group(1), m.group(1)), flat)
    out = ROOT / "build"
    out.mkdir(exist_ok=True)
    (out / "escapement-paper.md").write_text(flat)
    (out / "escapement.bib").write_text("\n".join(bibtex(rename.get(k, k), srcs[k]) for k in keys))
    words = len(re.findall(r"\b\w+\b", flat))
    print(f"wrote build/escapement-paper.md ({words} words) and build/escapement.bib ({len(keys)} sources)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
