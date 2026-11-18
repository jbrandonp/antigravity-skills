#!/usr/bin/env python3
"""SIM étape 3 : relance + fiche client 08-Clients + bilan des gaps."""
import json, os, subprocess

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
SIM = "/srv/brandon-ai/workspaces/bttp/simulation-client"
VAULT = "/srv/brandon-ai/workspaces/obsidian-vault/08-Clients"

# 1. Messages de relance pour le devis simulé
r = subprocess.run(["python3", os.path.join(BASE, "draft_relance_messages.py"), "--help"],
                   capture_output=True, text=True, timeout=60, cwd=BASE)
print("relance --help:", (r.stdout or r.stderr).strip()[:400])

# 2. Template fiche client dans le vault
tpl = os.path.join(VAULT, "Templates", "Fiche client.md")
print("\nfiche template existe:", os.path.exists(tpl))
if os.path.exists(tpl):
    print(open(tpl).read()[:600])
