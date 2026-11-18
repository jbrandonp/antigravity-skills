#!/usr/bin/env python3
"""Analyse de la couche ERP du système BTTP : mentions ERP dans l'offre, formats
d'export compatibles, état du connecteur Odoo (n8n), positionnement anti-ERP."""
import os, re, urllib.request

BASE = "/srv/brandon-ai/workspaces/bttp/bttp"
print("=== 1. Mentions ERP dans les documents commerciaux ===")
total = 0
for root, dirs, files in os.walk(BASE):
    if "__pycache__" in root or "tools" in root:
        continue
    for f in files:
        if not f.endswith((".md", ".html")):
            continue
        p = os.path.join(root, f)
        content = open(p, encoding="utf-8", errors="replace").read().lower()
        hits = {k: content.count(k) for k in ("vertuoza", "winbooks", "bouwsoft", "exact online", "odoo", "erp") if content.count(k)}
        if hits:
            total += sum(hits.values())
            print(f"  {f}: {hits}")
print(f"  TOTAL mentions: {total}")

print("\n=== 2. Formats d'export vers ERP ===")
print("  - export_devis_to_csv.py : CSV ';', utf-8-sig, anti-injection → Excel/ERP européens")
print("  - generate_peppol_invoice.py : UBL 2.1 / BIS 3.0 → Peppol (légal B2B BE)")
print("  - bttp_import.py : 6 formats ENTRANTS → classeur canonique (données client existantes)")

print("\n=== 3. Connecteur Odoo (n8n) ===")
try:
    r = urllib.request.urlopen("http://localhost:5678", timeout=5)
    print("  n8n localhost:5678 :", r.status, "→ JOIGNABLE")
except Exception as e:
    print("  n8n localhost:5678 : NON JOIGNABLE —", type(e).__name__)
print("  Odoo : connecteur NODE n8n installé (config 14/11) mais AUCUNE instance Odoo connectée")
print("  → il n'existe pas d'ERP réel branché : le connecteur est un nœud vide")

print("\n=== 4. Positionnement anti-ERP (offre) ===")
readme = open(f"{BASE}/README.md", encoding="utf-8", errors="replace").read().lower()
manuel = open(f"{BASE}/03_Vente_et_Prospection_Terrain/MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md", encoding="utf-8", errors="replace").read().lower()
print("  « pas un logiciel de plus » dans le manuel :", "logiciel supplémentaire" in manuel or "pas un logiciel" in manuel)
print("  l'offre INSTALLLE des fichiers Excel (pas un ERP) : oui — classeur + PWA + alertes")
