# Escapement. Python 3.11 or later, standard library only.
PY ?= python3

.PHONY: all model docs check paper sources

all: sources model docs check

model:  ## write data/numbers.json and research/numbers.md from data/inputs.toml
	$(PY) model/escapement.py --write

docs:   ## rewrite every ledger link to the model's value
	$(PY) tools/sync.py

check:  ## em dashes, model reproduces, docs synced, every citation and source identified
	$(PY) tools/check.py

paper:  ## build/escapement-paper.md, the paper with ledger links flattened, for Paperwright
	$(PY) tools/paper.py

sources:  ## research/sources.toml from the notes' YAML, the manual sources and the Crossref DOIs (needs PyYAML)
	$(PY) tools/sources.py
