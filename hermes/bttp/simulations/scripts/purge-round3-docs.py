#!/usr/bin/env python3
"""Purge finale doc + vérifications : OFFICE2026, README 118→138, import, stress."""
import subprocess

p = "/srv/brandon-ai/workspaces/bttp/bttp/01_Strategie_et_Audits/risk_management_and_red_team_protocols.md"
src = open(p, encoding="utf-8").read()
n = 0
for old, new in [
    ("(`OFFICE2026`), sauvegardes locales", "(sans mot de passe, décision 18/11/2026), sauvegardes locales"),
    ("verrouillées par mot de passe (`OFFICE2026`)", "protégées sans mot de passe (décision 18/11/2026)"),
]:
    if old in src:
        src = src.replace(old, new); n += 1
open(p, "w", encoding="utf-8").write(src)
print(f"risk_management: {n} correction(s)")

# vérifications globales
import os
total_office = total_btp2026 = 0
for root, dirs, files in os.walk("/srv/brandon-ai/workspaces/bttp/bttp"):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for f in files:
        content = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
        total_office += content.count("OFFICE2026")
        total_btp2026 += content.count("BTP2026")
print(f"OFFICE2026 restantes: {total_office} | BTP2026 restantes: {total_btp2026}")

readme = open("/srv/brandon-ai/workspaces/bttp/bttp/README.md", encoding="utf-8").read()
print("README mention 118 tests:", readme.count("118 test"))
