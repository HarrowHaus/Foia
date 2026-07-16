.PHONY: install test lint verify package

install:
	python -m pip install -e ".[dev,analysis]"

test:
	python -m pytest -q

lint:
	python -m ruff check src tests scripts

verify:
	python scripts/verify_repo.py
	python -m pytest -q

package: verify
	python scripts/export_bundle.py
