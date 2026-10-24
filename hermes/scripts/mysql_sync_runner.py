#!/usr/bin/env python3
"""Wrapper no_agent pour MySQL sync — sortie compacte, 0 token LLM."""
import subprocess, sys, os

try:
    r = subprocess.run(
        [sys.executable, "C:/Users/brand/.hermes/scripts/kate_mysql_sync.py", "--full"],
        capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace"
    )
    out = (r.stdout or "").strip()
    if r.returncode == 0 and out:
        print(out)
    else:
        print(f"⚠️ MySQL sync échec (exit {r.returncode}): {out[:300]} {r.stderr[:200]}")
except Exception as e:
    print(f"⚠️ MySQL sync erreur: {e}")
