# Paper build

`tools/paper.py` joins `paper/*.md` in name order, flattens ledger links to their text, and writes
`build/escapement-paper.md` and `build/escapement.bib` for Paperwright.

<!-- covers: cli:paper -->

## Sub-features

- build: `make paper` writes both files and prints the word count and source count.
- ids: `--ids` prints the identifier of every cited source (DOI, `arXiv:ID`, ISBN or URL), the list
  Paperwright's `add_sources` takes (URLs are not accepted there; those stay as links).
- keys: `--keys MAP.json` renames citation keys to the keys Paperwright gave each source.

## How to check it

```sh
make paper && grep -c 'numbers.md#' build/escapement-paper.md   # expect 0
python3 tools/paper.py --ids | head
```
