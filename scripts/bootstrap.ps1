$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev,analysis]"
& .\.venv\Scripts\python.exe scripts\verify_repo.py
& .\.venv\Scripts\python.exe -m pytest -q
Write-Host "Bootstrap complete. Activate with: .\.venv\Scripts\Activate.ps1"
