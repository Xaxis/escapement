# Sources

`tools/sources.py` builds `research/sources.toml`, the one catalogue every `[@key]` resolves
against, from the YAML `sources:` blocks in `research/notes/[0-9]*.md` (never `*.private.md`), the
hand-written `research/sources.manual.toml`, and the Crossref-checked DOIs in
`research/sources.ids.toml`. It merges duplicates by DOI, arXiv ID or URL and lists the merged keys
in `also`. `tools/keys.py` resolves a key to its primary entry, and `--fix FILE` rewrites merged
keys in a document to their primary key.

<!-- covers: cli:sources, cli:keys -->

## How to check it

```sh
make sources && python3 tools/sources.py --check; echo "exit $?"     # expect exit 0
python3 tools/keys.py ruffing2015 precop2026 no-such-key; echo "exit $?"
```

Expect `ruffing2015 ok`, `precop2026 -> laz1m0v2026`, `no-such-key MISSING` and exit 1.
`make check` also fails if `research/sources.toml` is stale. To prove it bites, in a scratch copy
add a source to `research/sources.manual.toml` without running `make sources`, then run
`make check` (expect a FAIL saying the catalogue is stale).
