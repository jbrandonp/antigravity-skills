#!/usr/bin/env python3
"""Diagnostic détaillé des échecs stress round 1."""
import subprocess

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
S = "/home/arthur/.hermes/cache/scratch/stress-bttp"

r = subprocess.run(["python3", f"{BASE}/export_devis_to_csv.py", "-e", f"{S}/volume2000.xlsx",
                    "-o", "/tmp/v.csv"], capture_output=True, text=True, timeout=120, cwd=BASE)
print("VOLUME CSV rc:", r.returncode, "|", (r.stderr or r.stdout).strip()[-160:])

r = subprocess.run(["python3", f"{BASE}/generate_patron_report.py", "-e", f"{S}/volume2000.xlsx",
                    "-c", "VOL", "-o", f"{S}/vol-rapport.txt"], capture_output=True, text=True,
                   timeout=120, cwd=BASE)
print("VOLUME RAPPORT rc:", r.returncode, "|", (r.stderr or r.stdout).strip()[-200:])

r = subprocess.run(["python3", f"{BASE}/generate_patron_report.py", "-e", f"{S}/vide.xlsx",
                    "-c", "V", "-o", "/tmp/v.txt"], capture_output=True, text=True, timeout=60, cwd=BASE)
print("VIDE rc:", r.returncode, "|", (r.stderr or "").strip()[-220:])

r = subprocess.run(["python3", f"{BASE}/bttp_import.py", "-s", f"{S}/malforme.csv", "-o", "/tmp/m.xlsx"],
                   capture_output=True, text=True, timeout=60, cwd=BASE)
print("MALFORME rc:", r.returncode, "| err:", (r.stderr or "").strip()[-140:], "| out:", (r.stdout or "").strip()[:90])

for label, extra in [("BCE12345", ["--client-cbe", "12345"]),
                     ("negatif", ["--amount-htva", "-1000"]),
                     ("zero", ["--amount-htva", "0"])]:
    r = subprocess.run(["python3", f"{BASE}/generate_peppol_invoice.py", "--output-xml", "/tmp/p.xml",
                        "--invoice-number", "T", "--client-name", "X", "--client-cbe", "0123456789",
                        "--amount-htva", "1000", "--customer-street", "R", "--customer-city", "L",
                        "--customer-zip", "4000", *extra], capture_output=True, text=True,
                       timeout=60, cwd=BASE)
    line = ((r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else "")
    print(f"PEPPOL {label}: rc={r.returncode} | {line[:110]}")

# numérotation : vérifier le vrai contenu du classeur 999
import openpyxl
wb = openpyxl.load_workbook(f"{S}/num999.xlsx")
nums = [str(wb.active.cell(row=rr, column=1).value) for rr in range(5, wb.active.max_row + 1)
        if wb.active.cell(row=rr, column=1).value]
print("NUM999: tous les numéros DEV:", [n for n in nums if n.startswith("DEV-")][-4:])
