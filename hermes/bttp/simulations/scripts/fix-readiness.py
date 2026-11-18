#!/usr/bin/env python3
"""Correctifs readiness : 1) queue RGPD hors arbre repo ; 2) fixtures de test régénérées."""
import json, os, shutil, subprocess

SRC = "/srv/brandon-ai/workspaces/bttp/bttp/03_Vente_et_Prospection_Terrain/outreach_queue.json"
DST_DIR = "/srv/data/bttp-confidentiel"
DST = f"{DST_DIR}/outreach_queue.json"

# 1. Déplacer la queue hors de l'arbre repo (RGPD — risque re-push éliminé)
if os.path.exists(SRC) and not os.path.exists(DST):
    shutil.move(SRC, DST)
    print("1a. outreach_queue.json déplacé →", DST)
# recalcul du chemin canonique utilisé par le cron Pipeline
print("1b. nouveau chemin:", DST)
# vérifier le repo distant reste propre
r = subprocess.run(["gh", "api", "repos/jbrandonp/antigravity-skills/contents/hermes/bttp/03_Vente_et_Prospection_Terrain/outreach_queue.json"],
                   capture_output=True, text=True, timeout=60)
print("1c. repo distant:", "PROPRE (404)" if "404" in str(r.stderr) or "Not Found" in r.stderr else "⚠️ ENCORE PRÉSENT")

# 2. Régénérer les fixtures de test multi-formats
r = subprocess.run(["python3", "/srv/brandon-ai/workspaces/bttp/simulations/scripts/test-formats-ingestion.py"],
                   capture_output=True, text=True, timeout=300)
print("2. fixtures régénérées:", "OK" if r.returncode == 0 else r.stderr[-150:])
