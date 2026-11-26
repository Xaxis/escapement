# Paper build

`tools/paper.py` joins `paper/*.md` in name order, flattens ledger links to their text, and writes
`build/escapement-paper.md` and `build/escapement.bib` for Paperwright.

<!-- covers: cli:paper -->

## Sub-features

- build: `make paper` writes both files and prints the word count and source count.
- ids: `--ids` prints the identifier of every cited source (DOI, `arXiv:ID`, ISBN or URL), the list
  Paperwright's `add_sources` takes (URLs are not accepted there; those stay as links).
- keys: `--keys MAP.json` renames citation keys to the keys Paperwright gave each source.
- draft: `--draft` also writes `build/escapement-draft.json`, the sections and tables as
  Paperwright's `write_section` and `set_table` take them. It joins each wrapped list item onto one
  line (Paperwright ends an item at its first line break, so a wrapped numbered list restarts at 1)
  and lifts each subsection heading one level (Paperwright numbers `#` inside a section as 3.1 and
  `##` as 3.0.1). Tables become `![](tb_label)` lines, to be swapped for Paperwright's table ids.
- exports: `paper/exports/` holds Paperwright's PDF and Markdown exports, which cite Paperwright's
  own keys against their own `references.bib`; `make check` skips the folder.

## How to check it

```sh
make paper && grep -c 'numbers.md#' build/escapement-paper.md   # expect 0
python3 tools/paper.py --ids | head
python3 tools/paper.py --draft && python3 -c "import json,re; d=json.load(open('build/escapement-draft.json')); \
  print(sum(1 for s in d['sections'] for l in s['text'].split(chr(10)) if l.startswith('  ') and l.strip()), \
        sum(1 for s in d['sections'] for l in s['text'].split(chr(10)) if l.startswith('##')))"   # expect 0 0
```

After an export, render its pages (`pdftoppm -png -r 60`) and look: numbered lists count 1, 2, 3;
subsections read 3.1; a table reference reads "Table 1", not "Table Table 1" (write `@tab:x`, not
`Table @tab:x`).
