#!/usr/bin/env python3
"""SIMULATION client fictif BTTP — dry-run complet du workflow.
Client : SIMU-CHAUFFAGE SPRL (fictif, jamais envoyé à personne)."""
import json, shutil, os, subprocess

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
SIM = "/srv/brandon-ai/workspaces/bttp/simulation-client"
os.makedirs(SIM, exist_ok=True)

CLIENT = {
    "nom": "Jean Simul (SIMULATION — client fictif)",
    "entreprise": "SIMU-CHAUFFAGE SPRL",
    "bce": "0123456789",
    "tel": "+32 470 00 00 00",
    "email": "contact@simu-chauffage.example",
    "adresse": "Rue de la Simulation 1, 4000 Liège",
    "travaux": "Remplacement chaudière condensation gaz + régulation",
    "montant_htva": 4850.0,
    "pack": "Pack 1 (290 €) + Pack 3 récurrent (195 €/trim)",
}
json.dump(CLIENT, open(os.path.join(SIM, "client_simule.json"), "w"), ensure_ascii=False, indent=2)
print("client de simulation créé:", json.dumps(CLIENT, ensure_ascii=False))

# openpyxl dispo ?
try:
    import openpyxl
    print("openpyxl:", openpyxl.__version__)
except ImportError:
    print("⚠️ openpyxl MANQUANT — les scripts Excel ne tourneront pas")

# 1. Copier le classeur maître (ne jamais modifier le template)
src = os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
dst = os.path.join(SIM, "DEVIS_SIMULATION.xlsx")
if os.path.exists(src):
    shutil.copy2(src, dst)
    print("classeur copié:", dst, os.path.getsize(dst), "o")
else:
    print("⚠️ classeur maître introuvable:", src)

# 2. Ajouter le devis du client simulé
r = subprocess.run(["python3", os.path.join(BASE, "append_new_devis.py"),
                    "--excel-path", dst,
                    "--client", "SIMU-CHAUFFAGE SPRL (SIMULATION)",
                    "--montant", "4850",
                    "--objet", "Remplacement chaudière condensation gaz",
                    "--tel", "+32 470 00 00 00",
                    "--statut", "Envoyé — simulation"],
                   capture_output=True, text=True, timeout=120, cwd=BASE)
print("append_new_devis:", r.returncode, (r.stdout or r.stderr).strip()[:300])

# 3. Export CSV
r = subprocess.run(["python3", os.path.join(BASE, "export_devis_to_csv.py"),
                    "--excel-path", dst, "--output", os.path.join(SIM, "devis_sim.csv")],
                   capture_output=True, text=True, timeout=120, cwd=BASE)
print("export_csv:", r.returncode, (r.stdout or r.stderr).strip()[:200])
if os.path.exists(os.path.join(SIM, "devis_sim.csv")):
    print("CSV:", open(os.path.join(SIM, "devis_sim.csv")).read()[:300])
