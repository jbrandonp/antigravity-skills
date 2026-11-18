#!/usr/bin/env python3
"""Correctifs round 3 : purge OFFICE2026 (branche universelle), retrait dépendance
bttp_password, ODS protégé contre odfpy absent, docs alignées."""
import os, re

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8").write(s)

# 1. generate_digital_office_workbook.py : OFFICE2026 → ""
p = f"{BASE}/generate_digital_office_workbook.py"
src = read(p)
n1 = src.count('"OFFICE2026"')
src = src.replace('"OFFICE2026"', '""')
n2 = len(re.findall(r"\.set_password\(", src))
src = re.sub(r"(\w+\.protection\.)set_password\(([^)]+)\)", r"\1password = \2 if \2 else None", src)
# protection sans mot de passe : password = None si vide — simplifier : retirer les set_password
write(p, src)
print(f"✅ digital_office_workbook: {n1} OFFICE2026 → \"\", {n2} set_password neutralisés")

# 2. append_new_deal.py : défaut "" + set_password conditionnel
p = f"{BASE}/append_new_deal.py"
src = read(p)
src = src.replace('password: str = "OFFICE2026"', 'password: str = ""')
src = src.replace("ws.protection.set_password(password)",
                  "if password: ws.protection.set_password(password)")
# argparse default
src = re.sub(r'add_argument\("--password",[^)]*default="OFFICE2026"[^)]*\)',
             'add_argument("--password", type=str, default="", help="Mot de passe de la feuille (vide = aucun, décision 18/11)")', src)
write(p, src)
print("✅ append_new_deal: OFFICE2026 → \"\", set_password conditionnel")

# 3. append_new_devis.py : retirer la dépendance bttp_password (bombe)
p = f"{BASE}/append_new_devis.py"
src = read(p)
src = src.replace(
    """            password=(args.password if args.password
                      else __import__("bttp_password", fromlist=["password_for"]).password_for(args.client)),""",
    "            password=args.password,  # vide = protection SANS mot de passe (décision Brandon 18/11)")
src = src.replace(
    'help="Mot de passe de la feuille (vide = dérivé par client via bttp_password)"',
    'help="Mot de passe optionnel — vide = protection SANS mot de passe (décision Brandon 18/11)"')
write(p, src)
print("✅ append_new_devis: dépendance bttp_password retirée")

# 4. bttp_import.py : ODS sans odfpy → message propre
p = f"{BASE}/bttp_import.py"
src = read(p)
old = 'def _rows_from_ods(path: str) -> List[Dict[str, Any]]:\n    from odf.opendocument import load'
new = '''def _rows_from_ods(path: str) -> List[Dict[str, Any]]:
    try:
        from odf.opendocument import load
    except ImportError:
        raise ValueError("import ODS impossible : le paquet 'odfpy' n'est pas installé "
                         "(pip install odfpy) — ou convertissez le fichier en XLSX/CSV")'''
if old in src:
    src = src.replace(old, new)
    write(p, src)
    print("✅ bttp_import: ODS sans odfpy → message propre")

# 5. Docs : README 118→138, PROTOCOLE ligne mot de passe
for path, pairs in [
    (f"{BASE}/README.md", [("118 tests", "138 tests")]),
    ("/srv/brandon-ai/workspaces/bttp/bttp/04_Operations_et_Formation_Client/PROTOCOLE_INSTALLATION_TECHNIQUE.md",
     [("mot de passe", "aucun mot de passe (protection librement déverrouillable)")]),
]:
    if os.path.exists(path):
        src = read(path)
        n = 0
        for old, new in pairs:
            if old in src:
                src = src.replace(old, new); n += 1
        write(path, src)
        print(f"✅ doc {os.path.basename(path)}: {n} correction(s)")
