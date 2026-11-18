#!/usr/bin/env python3
"""Analyse des 2 disques + diff avec le clone du repo antigravity-skills.
Objectif : identifier tout ce qui est NOUVEAU/MODIFIÉ depuis le dernier push (HEAD 29d578bf),
et classer : poussable / exclu (RGPD, secrets, données clients)."""
import os, subprocess

CLONE = "/srv/brandon-ai/workspaces/antigravity-sync"

print("=== 1. ÉTAT DES DEUX DISQUES ===")
r = subprocess.run(["df", "-h", "/", "/srv/data"], capture_output=True, text=True)
print(r.stdout)

print("=== 2. ZONES SOURCE CANDIDATES AU PUSH ===")
zones = [
    ("/home/arthur/.hermes/scripts", ".hermes/scripts (jev, bttp, backup, drift)"),
    ("/srv/brandon-ai/workspaces/bttp/bttp", "bttp canonique"),
    ("/srv/brandon-ai/workspaces/*.py", "scripts de travail racine"),
]
for z, desc in zones:
    if os.path.isdir(z):
        n = sum(len(fs) for _, _, fs in os.walk(z))
        print(f"  {z}: {n} fichiers — {desc}")
    else:
        import glob
        print(f"  {z}: {len(glob.glob(z))} fichiers — {desc}")

print("\n=== 3. ÉTAT DU CLONE GIT ===")
r = subprocess.run(["bash", "-c", f"cd {CLONE} && git log --oneline -3 && git status --porcelain | head -20 && git status --porcelain | wc -l"],
                   capture_output=True, text=True)
print(r.stdout or r.stderr)

print("=== 4. DIFF LOCAL vs CLONE (scripts hermes) ===")
r = subprocess.run(["bash", "-c",
    "diff -rq /home/arthur/.hermes/scripts " + CLONE + "/hermes/scripts 2>/dev/null | grep -v __pycache__ | head -25; echo ---; "
    "diff -rq /srv/brandon-ai/workspaces/bttp/bttp " + CLONE + "/hermes/bttp 2>/dev/null | head -25"],
    capture_output=True, text=True)
print(r.stdout or "(aucune différence)")
