#!/usr/bin/env python3
"""SIM « client vient de payer, beaucoup de data » : migration d'un historique complet.
Client fictif : SIMU-CHAUFFAGE SPRL, 3 ans d'historique (400 devis, 8 ans d'activité).
Pipeline testé : ingestion workbook → export CSV ERP → rapport patron → relances."""
import datetime, json, os, random, shutil, subprocess, time

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
CDIR = "/srv/brandon-ai/workspaces/bttp/clients/SIMU-CHAUFFAGE-SPRL"
os.makedirs(CDIR, exist_ok=True)

random.seed(42)
import openpyxl

# 1. Construire un classeur réaliste à grande échelle sur une copie du modèle
wb_path = os.path.join(CDIR, "DEVIS_SIMU-CHAUFFAGE.xlsx")
src = os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
shutil.copy2(src, wb_path)
wb = openpyxl.load_workbook(wb_path)
ws = wb.active
# détecter la ligne d'en-tête (1re ligne contenant "Client")
header_row = next(i for i in range(1, 6) if any("client" in str(c.value).lower() for c in ws[i]))
header = [c.value for c in ws[header_row]]
idx = {str(v).strip(): i for i, v in enumerate(header) if v}
print("en-tête détecté ligne", header_row, "| colonnes:", len(header))

noms = [f"Client SIM {i:03d}" for i in range(1, 121)]
objets = ["Chaudière condensation", "Pompe à chaleur air/eau", "Chauffe-eau thermodynamique",
          "Rénovation électrique complète", "Tableau électrique + mise aux normes",
          "Salle de bain complète", "Panneau solaire + onduleur", "Vannes thermostatiques"]
stats = ["Envoyé", "Relancé", "En attente", "Validé", "Validé", "Validé", "Perdu"]  # ~40% gagnés
t0 = time.time()
row = header_row + 1
devis_rows = 400
for i in range(devis_rows):
    nom = random.choice(noms)
    date = datetime.date(2023, 1, 2) + datetime.timedelta(days=random.randint(0, 1420))
    montant = round(random.uniform(450, 14500), 2)
    st = random.choice(stats)
    relance = date + datetime.timedelta(days=random.choice([4, 7, 10, 12, 14]))
    vals = {k: "" for k in idx}
    def setcol(pattern, value):
        for k in idx:
            if pattern.lower() in str(k).lower():
                vals[k] = value; return
    setcol("Devis", f"SIM-2026-{i+1:04d}")
    setcol("Date", date.strftime("%Y-%m-%d"))
    setcol("Client", nom)
    setcol("Télé", f"047{random.randint(0,9)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}")
    setcol("Objet", random.choice(objets))
    setcol("Montant", montant)
    setcol("Statut", st)
    setcol("Relance", relance.strftime("%Y-%m-%d"))
    for k, v in vals.items():
        col = idx[k] + 1
        ws.cell(row=row, column=col, value=v)
    row += 1
wb.save(wb_path)
t_ing = time.time() - t0
print(f"INGESTION: {devis_rows} devis insérés en {t_ing:.1f}s")

# 2. Export CSV ERP
t0 = time.time()
r = subprocess.run(["python3", os.path.join(BASE, "export_devis_to_csv.py"),
                    "--excel-path", wb_path, "--output", os.path.join(CDIR, "export_erp_sim.csv")],
                   capture_output=True, text=True, timeout=300, cwd=BASE)
t_csv = time.time() - t0
print(f"EXPORT CSV: rc={r.returncode} en {t_csv:.1f}s | {(r.stdout or r.stderr).strip()[:120]}")

# 3. Rapport patron à l'échelle
t0 = time.time()
r = subprocess.run(["python3", os.path.join(BASE, "generate_patron_report.py"),
                    "-e", wb_path, "-c", "SIMU-CHAUFFAGE SPRL",
                    "-o", os.path.join(CDIR, "rapport_patron_migration.txt")],
                   capture_output=True, text=True, timeout=300, cwd=BASE)
t_rep = time.time() - t0
print(f"RAPPORT PATRON: rc={r.returncode} en {t_rep:.1f}s")
if os.path.exists(os.path.join(CDIR, "rapport_patron_migration.txt")):
    print(open(os.path.join(CDIR, "rapport_patron_migration.txt")).read()[:900])

# 4. Relances à l'échelle
t0 = time.time()
r = subprocess.run(["python3", os.path.join(BASE, "draft_relance_messages.py"),
                    "--excel-path", wb_path, "--artisan-name", "SIMU-CHAUFFAGE SPRL",
                    "--output-md", os.path.join(CDIR, "relances_migration.md")],
                   capture_output=True, text=True, timeout=300, cwd=BASE)
t_rel = time.time() - t0
print(f"RELANCES: rc={r.returncode} en {t_rel:.1f}s | {(r.stdout or r.stderr).strip()[:150]}")

print("\n--- TIMINGS TOTAUX ---")
print(f"ingestion {t_ing:.1f}s | csv {t_csv:.1f}s | rapport {t_rep:.1f}s | relances {t_rel:.1f}s")
