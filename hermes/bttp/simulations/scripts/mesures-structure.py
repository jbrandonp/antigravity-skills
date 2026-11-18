#!/usr/bin/env python3
"""Mesures structurelles du projet BTTP pour l'analyse round 3."""
import os

BASE = "/srv/brandon-ai/workspaces/bttp/bttp"

print("=== inventaire par pôle ===")
for d in sorted(os.listdir(BASE)):
    full = os.path.join(BASE, d)
    if os.path.isdir(full) and d[0].isdigit():
        n = sum(len(f) for _, _, f in os.walk(full))
        size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(full) for f in fs)
        print(f"{d}: {n} fichiers, {size // 1024} Ko")

print("\n=== lignes de code (outils + orchestrateur) ===")
total = 0
for f in sorted(os.listdir(f"{BASE}/05_Outils_et_Modeles_Excel")):
    if f.endswith(".py"):
        n = sum(1 for _ in open(os.path.join(f"{BASE}/05_Outils_et_Modeles_Excel", f), encoding="utf-8", errors="replace"))
        total += n
        print(f"  {f}: {n} lignes")
for f in ("main.py", "run_all_tests.py", "bttp.py"):
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        n = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
        total += n
        print(f"  {f}: {n} lignes")
print(f"  TOTAL: {total} lignes Python")

print("\n=== docs racine ===")
for f in ("README.md", "CHANGELOG.md", "DATA-ARCHITECTURE.md", "pyproject.toml"):
    p = os.path.join(BASE, f)
    print(f"  {f}: {'OK ' + str(os.path.getsize(p) // 1024) + ' Ko' if os.path.exists(p) else 'ABSENT'}")

print("\n=== RGPD / confidentiel ===")
print("  /srv/data/bttp-confidentiel/:", os.listdir("/srv/data/bttp-confidentiel") if os.path.isdir("/srv/data/bttp-confidentiel") else "ABSENT")
suspects = [f for root, _, fs in os.walk(BASE) for f in fs if "ST_NICOLAS" in f.upper() or "outreach_queue" in f or f.endswith(".db")]
print("  données sensibles dans l'arbre projet:", suspects if suspects else "AUCUNE")

print("\n=== git local vs distant ===")
r = os.popen("gh api repos/jbrandonp/antigravity-skills/commits/main --jq .sha[:8] 2>/dev/null").read().strip()
print("  HEAD distant:", r)
