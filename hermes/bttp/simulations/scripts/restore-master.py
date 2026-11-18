#!/usr/bin/env python3
"""Restaure le classeur maître (écrasé par le test round 4 — le générateur ignore argv)
+ ajoute un CLI --output au générateur pour que ça ne reproduise plus jamais."""
import os, subprocess, sys

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
GEN = f"{BASE}/generate_devis_sans_oubli.py"
MASTER = f"{BASE}/DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"

# 1. CLI : respecter un argument de sortie (sinon le défaut écrase le master)
src = open(GEN, encoding="utf-8").read()
old = '''if __name__ == "__main__":
    create_devis_sans_oubli_workbook(DEFAULT_WORKBOOK_PATH)'''
new = '''if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Génère le classeur maître DEVIS_SANS_OUBLI")
    parser.add_argument("--output", "-o", default=DEFAULT_WORKBOOK_PATH,
                        help="Chemin de sortie (DÉFAUT = écrase le classeur maître — prudence)")
    args = parser.parse_args()
    create_devis_sans_oubli_workbook(args.output)'''
if old in src and "--output" not in src:
    src = src.replace(old, new)
    open(GEN, "w", encoding="utf-8").write(src)
    print("✅ générateur : CLI --output ajouté")

# 2. Régénérer le classeur maître (le master est la sortie du générateur par définition)
r = subprocess.run(["python3", GEN], capture_output=True, text=True, timeout=180, cwd=BASE)
print("régénération master:", r.returncode, (r.stdout or r.stderr).strip()[-90:])

# 3. Vérifier le master restauré : 5 onglets, zéro mot de passe, formules
import openpyxl
wb = openpyxl.load_workbook(MASTER)
pwds = [(s.title, s.protection.password) for s in wb.worksheets
        if s.protection.password and str(s.protection.password) not in ("", "None")]
formules = sum(1 for sh in wb.worksheets for row in sh.iter_rows()
               for c in row if isinstance(c.value, str) and c.value.startswith("="))
print(f"master restauré: {len(wb.worksheets)} onglets | mot de passe: {'⚠️ ' + str(pwds) if pwds else 'aucun ✓'} | formules: {formules}")
