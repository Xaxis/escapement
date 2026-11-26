#!/usr/bin/env python3
"""Write research/sources.toml: every source the survey tracks opened, plus the hand-added ones.

Each note in research/notes/ ends with a fenced YAML block `sources:`. This reads them all, merges
the entries that name the same work (same DOI, arXiv ID or URL), maps each type onto the repo's
types, pulls a DOI or arXiv ID out of the identifier where there is one, and adds
research/sources.manual.toml (sources the design and the paper cite that no track opened), and
the identifiers in research/sources.ids.toml (a DOI found on Crossref for a work a note gave only
by URL, matched by title). Keys
stay as the notes wrote them; a key two notes used for different works gets the note's number.

  python3 tools/sources.py          write research/sources.toml
  python3 tools/sources.py --check  exit 1 if research/sources.toml is stale
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "research" / "notes"
OUT = ROOT / "research" / "sources.toml"
MANUAL = ROOT / "research" / "sources.manual.toml"
IDS = ROOT / "research" / "sources.ids.toml"

TYPE_MAP = [
    ("peer", "peer-reviewed"),
    ("preprint", "preprint"),
    ("legislation", "legislation"),
    ("legal", "legal-scholarship"),
    ("standard", "spec"),
    ("bip", "spec"),
    ("rfc", "spec"),
    ("spec", "spec"),
    ("book", "book"),
    ("official", "official-docs"),
    ("docs", "official-docs"),
    ("vendor", "vendor"),
    ("company", "vendor"),
    ("news", "news"),
    ("essay", "essay"),
    ("blog", "essay"),
    ("code", "code"),
    ("dataset", "dataset"),
    ("report", "report"),
]
DOI_IN = re.compile(r"(10\.\d{4,9}/[^\s\"'<>]+)")
ARXIV_IN = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arXiv:\s*)(\d{4}\.\d{4,5})(v\d+)?", re.I)
KEY_OK = re.compile(r"^[A-Za-z][\w:-]*\w$")


def map_type(raw: str) -> str:
    low = (raw or "").lower()
    for needle, kind in TYPE_MAP:
        if needle in low:
            return kind
    return "essay"


def blocks(path: Path) -> list[dict]:
    text = path.read_text()
    found = []
    for m in re.finditer(r"```ya?ml\n(.*?)```", text, re.S):
        try:
            data = yaml.safe_load(m.group(1))
        except yaml.YAMLError as e:
            print(f"{path.name}: YAML does not parse: {e}", file=sys.stderr)
            continue
        if isinstance(data, dict) and isinstance(data.get("sources"), list):
            found.extend(x for x in data["sources"] if isinstance(x, dict))
    return found


def first(entry: dict, *names: str) -> str:
    for n in names:
        v = entry.get(n)
        if v not in (None, "", []):
            return str(v).strip()
    return ""


def normalize(entry: dict, note: str) -> dict | None:
    key = re.sub(r"[^\w:-]", "-", first(entry, "key")).strip("-_:")
    if not key:
        return None
    if not key[0].isalpha():
        key = "s" + key
    blob = " ".join(str(entry.get(n, "")) for n in ("doi", "arxiv", "id", "identifier", "url"))
    found_doi = DOI_IN.search(blob)
    doi = first(entry, "doi") or (found_doi.group(1) if found_doi else "")
    doi = doi.removeprefix("https://doi.org/").removeprefix("doi:").rstrip(".,;)")
    arxiv = first(entry, "arxiv")
    found_arxiv = ARXIV_IN.search(blob)
    if not arxiv and found_arxiv:
        arxiv = found_arxiv.group(1)
    arxiv = arxiv.removeprefix("arXiv:").strip()
    if arxiv and not re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", arxiv):
        arxiv = ""
    url = first(entry, "url")
    if not url:
        ident = first(entry, "id", "identifier", "path")
        url = ident if ident.startswith("http") else ""
    isbn = first(entry, "isbn")
    if not isbn:
        m = re.search(r"ISBN[:\s]*([\d-]{10,17}X?)", blob)
        isbn = m.group(1) if m else ""
    authors = entry.get("authors") or []
    if not isinstance(authors, (list, str)):
        authors = str(authors)
    if isinstance(authors, str):
        authors = [a.strip() for a in re.split(r";| and ", authors) if a.strip()]
    year = first(entry, "year")
    m = re.search(r"(19|20)\d\d", year)
    title = first(entry, "title")
    path = first(entry, "path")
    if not title and path.startswith("https://github.com/"):
        # Note 01 cites repository files by path: name them by repository and file.
        parts = path.removeprefix("https://github.com/").split("/")
        repo, file = parts[1], "/".join(parts[4:]) if len(parts) > 4 else ""
        title = f"{repo}: {file}" if file else repo
        authors = authors or [parts[0]]
        if not first(entry, "type"):
            entry = {**entry, "type": "code" if re.search(r"\.(ts|js|py|rs|json)$", file) else "spec"}
    if not (title and (doi or arxiv or url or isbn)):
        return None
    out = {
        "type": map_type(first(entry, "type")),
        "title": title,
        "authors": [str(a) for a in authors],
        "year": int(m.group(0)) if m else (2026 if path.startswith("https://github.com/") else 0),
        "venue": first(entry, "venue", "publisher"),
        "doi": doi,
        "arxiv": arxiv,
        "isbn": isbn,
        "url": url,
        "supports": first(entry, "supports"),
        "note": note,
    }
    out["key"] = key
    return out


def identity(s: dict) -> str:
    if s["doi"]:
        return "doi:" + s["doi"].lower()
    if s["arxiv"]:
        return "arxiv:" + s["arxiv"].split("v")[0]
    return "url:" + s["url"].lower().rstrip("/").removeprefix("https://").removeprefix("http://")


def toml_value(v) -> str:
    if isinstance(v, bool):  # before int: bool is a subclass of int, and TOML spells it lowercase
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(toml_value(x) for x in v) + "]"
    s = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'


def build() -> str:
    merged: dict[str, dict] = {}
    by_identity: dict[str, str] = {}
    for path in sorted(NOTES.glob("[0-9]*.md")):
        if path.name.endswith(".private.md"):
            continue
        note = path.name.split("-")[0]
        for raw in blocks(path):
            s = normalize(raw, f"research/notes/{path.name}")
            if s is None:
                continue
            ident = identity(s)
            if ident in by_identity:
                kept = merged[by_identity[ident]]
                kept.setdefault("also", []).append(s["key"])
                if s["supports"] and s["supports"] not in kept["supports"]:
                    kept["supports"] = (kept["supports"] + " | " + s["supports"])[:600]
                continue
            key = s["key"]
            if key in merged:
                key = f"{key}-n{note}"
            if not KEY_OK.match(key):
                continue
            s["key"] = key
            merged[key] = s
            by_identity[ident] = key
    manual = tomllib.loads(MANUAL.read_text()).get("source", {}) if MANUAL.exists() else {}
    ids = tomllib.loads(IDS.read_text()) if IDS.exists() else {}
    for key, extra in ids.items():
        if key in merged:
            merged[key].update({k: v for k, v in extra.items() if k in ("doi", "arxiv", "isbn")})
    lines = [
        "# Every source Escapement cites, generated by tools/sources.py from the YAML blocks in",
        "# research/notes/ and from research/sources.manual.toml. Do not edit by hand: change the note",
        "# or the manual file and run `make sources`. Cite as [@key].",
        "",
    ]
    for key, s in list(manual.items()):
        lines.append(f"[source.{key}]")
        for field, value in s.items():
            lines.append(f"{field} = {toml_value(value)}")
        lines.append("")
    for key in sorted(merged, key=str.lower):
        if key in manual:
            continue
        s = merged[key]
        lines.append(f"[source.{toml_value(key) if not re.match(r'^[A-Za-z0-9_-]+$', key) else key}]")
        if not s.get("year"):
            s["undated"] = "the page gives no date; read 2026-11-26"
        for field in ("type", "title", "authors", "year", "undated", "venue", "doi", "arxiv", "isbn", "url", "supports", "note", "also"):
            value = s.get(field)
            if value in ("", [], None, 0):
                continue
            lines.append(f"{field} = {toml_value(value)}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text = build()
    if "--check" in argv:
        if not OUT.exists() or OUT.read_text() != text:
            print("sources: research/sources.toml is stale; run make sources", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text)
    count = text.count("\n[source.")
    print(f"wrote research/sources.toml ({count} sources)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
