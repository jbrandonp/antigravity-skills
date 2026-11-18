#!/usr/bin/env python3
"""Probes de sécurité/comportement : 1) injection CSV/Excel, 2) numérotation devis edge cases."""
import csv, datetime, os, shutil, subprocess, openpyxl

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
TMP = "/home/arthur/.hermes/cache/scratch/probe-bttp"
os.makedirs(TMP, exist_ok=True)

# ---- 1. Injection CSV/Excel : nom client malveillant dans l'export ----
wb = openpyxl.load_workbook(os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"))
ws = wb.active
ws.insert_rows(5)
ws.cell(row=5, column=1, value="PROBE-INJ")
ws.cell(row=5, column=2, value=datetime.date(2026, 11, 18))
ws.cell(row=5, column=3, value="=cmd|' /C calc'!A0")  # payload DDE classique
ws.cell(row=5, column=4, value="0470000000")
ws.cell(row=5, column=5, value="@SUM(1+1)*cmd|' /C calc'!A0")
ws.cell(row=5, column=6, value=1234.56)
inj_wb = os.path.join(TMP, "inj.xlsx")
wb.save(inj_wb)
r = subprocess.run(["python3", os.path.join(BASE, "export_devis_to_csv.py"),
                    "-e", inj_wb, "-o", os.path.join(TMP, "inj.csv")],
                   capture_output=True, text=True, timeout=120, cwd=BASE)
rows = list(csv.reader(open(os.path.join(TMP, "inj.csv"), encoding="utf-8-sig"), delimiter=";"))
mal = [c for row in rows[1:] for c in row if c.strip().startswith(("=", "@", "+", "-"))]
print("INJECTION CSV:", "VULNÉRABLE — payloads passés sans neutralisation:" if mal else "protégé", mal[:3])

# ---- 2. Numérotation devis : edge cases ----
wb2 = openpyxl.load_workbook(os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"))
ws2 = wb2.active
# scénario A : classeur contenant DEV-2026-088 → attendu DEV-2026-089
ws2.cell(row=5, column=1, value="DEV-2026-088")
ws2.cell(row=5, column=2, value=datetime.date(2026, 11, 1))
ws2.cell(row=5, column=3, value="Client Edge A")
ws2.cell(row=5, column=6, value=100)
a_wb = os.path.join(TMP, "edge_a.xlsx"); wb2.save(a_wb)
r = subprocess.run(["python3", os.path.join(BASE, "append_new_devis.py"),
                    "--excel-path", a_wb, "--client", "Client Edge A", "--montant", "100",
                    "--objet", "Probe A"], capture_output=True, text=True, timeout=120, cwd=BASE)
import re
m = re.search(r"Numéro généré : (DEV-\d+-\d+)", r.stdout or "")
print("EDGE A (après DEV-2026-088):", m.group(1) if m else "INCONNU", "→ attendu DEV-2026-089")

# scénario B : classeur contenant uniquement DEV-2025-050 (année passée) → attendu DEV-2026-001 (reset annuel)
wb3 = openpyxl.load_workbook(os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"))
ws3 = wb3.active
ws3.cell(row=5, column=1, value="DEV-2025-050")
ws3.cell(row=5, column=2, value=datetime.date(2025, 6, 1))
ws3.cell(row=5, column=3, value="Client Edge B")
ws3.cell(row=5, column=6, value=100)
b_wb = os.path.join(TMP, "edge_b.xlsx"); wb3.save(b_wb)
r = subprocess.run(["python3", os.path.join(BASE, "append_new_devis.py"),
                    "--excel-path", b_wb, "--client", "Client Edge B", "--montant", "100",
                    "--objet", "Probe B"], capture_output=True, text=True, timeout=120, cwd=BASE)
m = re.search(r"Numéro généré : (DEV-\d+-\d+)", r.stdout or "")
print("EDGE B (classeur 2025 seul):", m.group(1) if m else "INCONNU", "→ attendu DEV-2026-001")
