# Docs sync and check

`tools/sync.py` rewrites every ledger link (`[text](numbers.md#id)`) in research/ and paper/ to the
model's value. `tools/check.py` runs every repository check.

<!-- covers: cli:sync, cli:check -->

## How to check it

```sh
make docs check; echo "exit $?"
```

To prove the checks bite, in a scratch copy: change one ledger link's text by hand and run
`python3 tools/sync.py --check` (expect exit 1 naming the link); cite `[@no-such-key]` in a research
file and run `make check` (expect a FAIL naming it); add an em dash to any file (expect a FAIL).
