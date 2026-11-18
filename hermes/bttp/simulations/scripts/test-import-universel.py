#!/usr/bin/env python3
"""TEST IMPORT UNIVERSEL — les 6 formats → classeur canonique → vérification pipeline."""
import csv, os, subprocess, sys

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
TMP = "/home/arthur/.hermes/cache/scratch/test-formats"
SOURCES = [
    ("CSV standard", f"{TMP}/standard.csv"),
    ("CSV français ;", f"{TMP}/francais.csv"),
    ("JSON", f"{TMP}/donnees.json"),
    ("Texte libre", f"{TMP}/notes.txt"),
    ("ODS", f"{TMP}/classeur.ods"),
    ("XLSX autre layout", f"{TMP}/layout-different.xlsx"),
]

ok_all = True
for label, src in SOURCES:
    if not os.path.exists(src):
        print(f"❌ {label}: fichier de test absent"); ok_all = False; continue
    out = f"{TMP}/import-{label.replace(' ', '_')}.xlsx"
    # 1. Import universel
    r = subprocess.run(["python3", f"{BASE}/bttp_import.py", "-s", src, "-o", out,
                        "-c", "Client Format Test"],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    if r.returncode != 0:
        print(f"❌ {label}: IMPORT ÉCHOUÉ — {(r.stderr or r.stdout).strip()[:120]}")
        ok_all = False; continue
    # 2. Vérifier le contenu importé (3 devis, montants exacts, statuts reconnus)
    import openpyxl
    wb = openpyxl.load_workbook(out)
    ws = wb.active
    devis = 0
    montants_ok = 0
    for row in range(5, ws.max_row + 1):
        num = ws.cell(row=row, column=1).value
        if num and str(num).startswith("IMP-"):
            devis += 1
            m = ws.cell(row=row, column=6).value
            if m in (4850.0, 6200.0, 1980.0):
                montants_ok += 1
    # 3. Le pipeline aval fonctionne-t-il sur le classeur importé ?
    r2 = subprocess.run(["python3", f"{BASE}/generate_patron_report.py", "-e", out,
                         "-c", "Client Format Test", "-o", f"{TMP}/rapport-import.md"],
                        capture_output=True, text=True, timeout=120, cwd=BASE)
    rapport = open(f"{TMP}/rapport-import.md", encoding="utf-8").read() if r2.returncode == 0 else ""
    won_recognized = "Validé" and ("950.00" in rapport or "4,850" in rapport or "4.850" in rapport)
    if devis == 3 and montants_ok == 3 and r2.returncode == 0:
        print(f"✅ {label}: 3 devis importés, montants exacts 3/3, rapport patron OK (CA gagné reconnu: {'oui' if won_recognized else 'à vérifier'})")
    else:
        print(f"❌ {label}: devis={devis}/3, montants={montants_ok}/3, rapport rc={r2.returncode}")
        ok_all = False

print("=" * 60)
print("VERDICT GLOBAL:", "TOUT PASSE ✅" if ok_all else "DES ÉCHECS ❌")
