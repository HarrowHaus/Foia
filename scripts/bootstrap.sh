#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,analysis]"
python scripts/verify_repo.py
python -m pytest -q
printf '\nBootstrap complete. Activate with: source .venv/bin/activate\n'
