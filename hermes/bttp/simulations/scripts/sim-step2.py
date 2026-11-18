#!/usr/bin/env python3
"""SIM étape 2 : facture Peppol UBL + rapport patron + avenant WhatsApp."""
import json, os, subprocess

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
SIM = "/srv/brandon-ai/workspaces/bttp/simulation-client"

# 1. Facture Peppol UBL 2.1 (client SPRL fictif)
r = subprocess.run(["python3", os.path.join(BASE, "generate_peppol_invoice.py"),
                    "--output-xml", os.path.join(SIM, "FACT-SIMU-001.xml"),
                    "--invoice-number", "FACT-SIMU-001",
                    "--client-name", "SIMU-CHAUFFAGE SPRL",
                    "--client-cbe", "0123456789",
                    "--amount-htva", "4850"],
                   capture_output=True, text=True, timeout=120, cwd=BASE)
print("peppol:", r.returncode, (r.stdout or r.stderr).strip()[:400])
xml = os.path.join(SIM, "FACT-SIMU-001.xml")
if os.path.exists(xml):
    content = open(xml).read()
    print("XML généré:", len(content), "caractères | contient 'SIMU-CHAUFFAGE':", "SIMU-CHAUFFAGE" in content)

# 2. Rapport patron — inspecter l'interface d'abord
r = subprocess.run(["python3", os.path.join(BASE, "generate_patron_report.py"), "--help"],
                   capture_output=True, text=True, timeout=60, cwd=BASE)
print("\npatron_report --help:", (r.stdout or r.stderr).strip()[:500])

# 3. Avenant WhatsApp (interface depuis main.py : AmendmentSpec)
r = subprocess.run(["python3", os.path.join(BASE, "generate_site_work_amendment.py"), "--help"],
                   capture_output=True, text=True, timeout=60, cwd=BASE)
print("\namendment --help:", (r.stdout or r.stderr).strip()[:400])
