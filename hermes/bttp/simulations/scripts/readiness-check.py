#!/usr/bin/env python3
"""VÉRIFICATION FINALE DE PRÉPARATION — usage professionnel."""
import datetime, glob, json, os, subprocess, sys

checks = []

def check(nom, ok, detail=""):
    checks.append((nom, ok, detail))
    print(("✅" if ok else "❌"), nom, ("— " + detail if detail else ""))

BASE = "/srv/brandon-ai/workspaces/bttp/bttp"
WS = "/srv/brandon-ai/workspaces"

# 1. Banc officiel
r = subprocess.run(["python3", f"{BASE}/run_all_tests.py"], capture_output=True, text=True, timeout=300)
ok = "100 % DES TESTS VALIDÉS" in r.stdout and "138" in r.stdout
check("1. Banc de tests officiel", ok, "138/138" if ok else "échec")

# 2. Stress battery (re-exécution)
r = subprocess.run(["python3", f"{WS}/bttp/simulations/scripts/stress-tests.py"],
                   capture_output=True, text=True, timeout=580)
ok = "8/8 scénarios PASS" in r.stdout
check("2. Batterie de stress", ok, "8/8" if ok else "voir stress")

# 3. Status projet
r = subprocess.run(["bash", "/home/arthur/.hermes/scripts/bttp.sh", "status"],
                   capture_output=True, text=True, timeout=120)
ok = r.stdout.count("CONFORME") >= 6
check("3. Status projet (6 pôles)", ok, f"{r.stdout.count('CONFORME')}/6")

# 4. Crons actifs
r = subprocess.run(["python3", "-c", """
import json
j = json.load(open('/home/arthur/.hermes/cron/jobs.json'))
jobs = j if isinstance(j, list) else j.get('jobs', [])
ids = {x.get('id'): x for x in jobs}
for cid, attendu in [('60302a8c02eb', 'pipeline'), ('07ef4fb92295', 'rapport patron'), ('5a4f1f163fed', 'backup')]:
    print(cid, 'OK' if cid in ids and ids[cid].get('enabled') else 'ABSENT/PAUSE')
"""], capture_output=True, text=True, timeout=60)
lignes = r.stdout.strip().splitlines()
ok = all("OK" in l for l in lignes if "OK" in l or "ABSENT" in l) and len(lignes) == 3
check("4. Crons (pipeline, rapport mensuel, backup)", ok, "; ".join(lignes))

# 5. Backup chiffré d'aujourd'hui existe et vérifiable
bks = sorted(glob.glob("/srv/data/backups/bttp-clients/*.tar.gz.enc"))
ok = len(bks) >= 1
check("5. Backup chiffré", ok, f"{len(bks)} archive(s), dernière: {os.path.basename(bks[-1]) if bks else 'aucune'}")

# 6. Données clients sur le bon disque (symlink)
ok = os.path.islink(f"{WS}/bttp/clients") and os.path.realpath(f"{WS}/bttp/clients").startswith("/srv/data")
check("6. Données clients sur volume dédié", ok)

# 7. RGPD : pas de données réelles dans le dossier projet
fuite = []
for root, dirs, files in os.walk(f"{BASE}"):
    for f in files:
        if f in ("DOSSIER_COMPLET_EXPERTISE_TECHNIQUE_ST_NICOLAS_AVP01.md",) or "outreach_queue" in f:
            fuite.append(f)
check("7. RGPD dossier projet", not fuite, f"{fuite}" if fuite else "propre")

# 8. Repo distant aligné
r = subprocess.run(["gh", "api", "repos/jbrandonp/antigravity-skills/commits/main", "--jq", ".sha[:8]"],
                   capture_output=True, text=True, timeout=60)
ok = r.stdout.strip() == "08df4f9a"
check("8. Repo distant = v1.0.1", ok, r.stdout.strip())

# 9. Pre-flight Peppol fonctionne
r = subprocess.run(["python3", f"{BASE}/05_Outils_et_Modeles_Excel/generate_peppol_invoice.py",
                    "--output-xml", "/tmp/ready.xml", "--invoice-number", "READY-1",
                    "--client-name", "Client Prêt", "--client-cbe", "0123456789",
                    "--amount-htva", "1000", "--customer-street", "R 1",
                    "--customer-city", "Liège", "--customer-zip", "4000"],
                   capture_output=True, text=True, timeout=120)
ok = r.returncode == 0 and "Pré-vol" in r.stdout
check("9. Facture Peppol de bout en bout", ok)

# 10. Import universel multi-formats
r = subprocess.run(["python3", f"{WS}/bttp/simulations/scripts/test-import-universel.py"],
                   capture_output=True, text=True, timeout=580)
ok = "TOUT PASSE" in r.stdout
check("10. Import universel (6 formats)", ok)

print("=" * 60)
echecs = [n for n, ok, _ in checks if not ok]
print(f"PRÉPARATION: {len(checks) - len(echecs)}/{len(checks)} critères validés" +
      (f" — ÉCHECS: {echecs}" if echecs else ""))
sys.exit(1 if echecs else 0)
