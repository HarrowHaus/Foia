from __future__ import annotations

import importlib.util
import os
import platform
import sqlite3
import sys


def doctor_report() -> dict:
    conn = sqlite3.connect(":memory:")
    fts5 = True
    try:
        conn.execute("CREATE VIRTUAL TABLE x USING fts5(value)")
    except sqlite3.OperationalError:
        fts5 = False
    optional = {name: importlib.util.find_spec(name) is not None for name in ["pypdf", "bs4", "networkx", "rapidfuzz", "pytesseract", "fitz"]}
    keys = {name: bool(os.getenv(name)) for name in ["NARA_API_KEY", "GOVINFO_API_KEY", "CONGRESS_API_KEY", "COURTLISTENER_TOKEN"]}
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "sqlite": sqlite3.sqlite_version,
        "fts5": fts5,
        "optional_modules": optional,
        "api_keys_present": keys,
        "user_agent_configured": "replace-me" not in os.getenv("PRIL_USER_AGENT", "replace-me"),
    }
