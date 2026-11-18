#!/usr/bin/env python3
"""TEST FORMATS D'INGESTION — un client apporte ses données en 6 formats différents.
Phase 1 : sonder ce que le pipeline actuel accepte (probablement XLSX uniquement).
Phase 2 : à compléter avec l'outil d'import universel."""
import csv, datetime, json, os, subprocess

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
TMP = "/home/arthur/.hermes/cache/scratch/test-formats"
os.makedirs(TMP, exist_ok=True)

DONNEES = [  # (date, client, objet, montant, statut)
    ("2026-09-01", "Client Format Test", "Chaudière condensation", 4850.0, "Validé"),
    ("05/10/2026", "Client Format Test", "Salle de bain complète", 6200.0, "Envoyé"),
    ("2026-11-01", "Client Format Test", "Radiateurs ×6", 1980.0, "En attente"),
]

# --- Générer les fichiers de test ---
# 1. CSV standard (virgule)
p1 = f"{TMP}/standard.csv"
with open(p1, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Client", "Objet", "Montant HTVA", "Statut"])
    for row in DONNEES: w.writerow(row)

# 2. CSV français (point-virgule, décimales à virgule)
p2 = f"{TMP}/francais.csv"
with open(p2, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["Date d'émission", "Client", "Description", "Montant", "Statut"])
    for d, c, o, m, s in DONNEES:
        w.writerow([d, c, o, f"{m:.2f}".replace(".", ","), s])

# 3. JSON structuré
p3 = f"{TMP}/donnees.json"
json.dump({"devis": [{"date": d, "client": c, "objet": o, "montant": m, "statut": s}
                     for d, c, o, m, s in DONNEES]}, open(p3, "w"), ensure_ascii=False)

# 4. Texte libre (log artisan)
p4 = f"{TMP}/notes.txt"
lines = [f"{d} | {c} | {o} | {m} EUR | {s}" for d, c, o, m, s in DONNEES]
open(p4, "w", encoding="utf-8").write("\n".join(lines))

# 5. ODS (via odfpy)
try:
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    doc = OpenDocumentSpreadsheet()
    table = Table(name="Devis")
    for row in [["Date", "Client", "Objet", "Montant", "Statut"]] + [list(r) for r in DONNEES]:
        tr = TableRow()
        for v in row:
            tc = TableCell(valuetype="string")
            tc.addElement(P(text=str(v)))
            tr.addElement(tc)
        table.addElement(tr)
    doc.spreadsheet.addElement(table)
    p5 = f"{TMP}/classeur.ods"
    doc.save(p5)
except Exception as e:
    p5 = None
    print("ODS non généré:", e)

# 6. XLSX layout différent (en-tête ligne 1, colonnes dans un autre ordre)
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Nos interventions"
ws.append(["Statut", "Montant HTVA (€)", "Description travaux", "Client", "Date émission"])
for d, c, o, m, s in DONNEES:
    ws.append([s, m, o, c, d])
p6 = f"{TMP}/layout-different.xlsx"
wb.save(p6)

# --- Sonde : le pipeline actuel accepte-t-il ces formats ? ---
print("=" * 60)
for label, path in [("CSV standard", p1), ("CSV français ;", p2), ("JSON", p3),
                    ("Texte libre", p4), ("ODS", p5), ("XLSX autre layout", p6)]:
    if path is None:
        continue
    ext = os.path.splitext(path)[1]
    r = subprocess.run(["python3", os.path.join(BASE, "export_devis_to_csv.py"),
                        "-e", path, "-o", f"{TMP}/out-{label.replace(' ', '_')}.csv"],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    status = "ACCEPTÉ" if r.returncode == 0 else f"REJETÉ ({(r.stderr or r.stdout).strip().splitlines()[-1][:80] if (r.stderr or r.stdout).strip() else 'silence'})"
    print(f"{label:20} → {status}")
