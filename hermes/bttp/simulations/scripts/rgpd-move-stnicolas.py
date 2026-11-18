#!/usr/bin/env python3
"""Déplace les derniers fichiers St-Nicolas (données réelles) hors de l'arbre projet."""
import os, shutil

BASE = "/srv/brandon-ai/workspaces/bttp/bttp"
CONF = "/srv/data/bttp-confidentiel"
os.makedirs(CONF, exist_ok=True)

moved = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if ("ST_NICOLAS" in f.upper() or "st_nicolas" in f.lower()) and "EXCLUSIONS" not in f:
            src = os.path.join(root, f)
            dst = os.path.join(CONF, f)
            if os.path.exists(dst):
                dst = dst.replace(".xlsx", "_2.xlsx").replace(".py", "_2.py")
            shutil.move(src, dst)
            moved.append(f"{src} → {dst}")

# vérification
rest = [f for r, d, fs in os.walk(BASE) for f in fs if "ST_NICOLAS" in f.upper()]
print(f"{len(moved)} fichier(s) déplacé(s) vers {CONF}")
for m in moved:
    print(" ·", m)
print("restants dans l'arbre:", rest if rest else "AUCUN")
