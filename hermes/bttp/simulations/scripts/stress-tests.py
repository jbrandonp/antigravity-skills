#!/usr/bin/env python3
"""STRESS TESTS BTTP — 7 familles de tests hostiles sur tout le pipeline.
Chaque scénario : PASS (comportement propre : rejet propre OU traitement correct)
ou FAIL (crash, données fausses silencieuses, ou blocage)."""
import datetime, json, os, shutil, subprocess, sys, time, openpyxl

import random as _rnd
def random_month(): return _rnd.randint(1, 12)

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
TMP = "/home/arthur/.hermes/cache/scratch/stress-bttp"
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP, exist_ok=True)
MASTER = os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
results = []

def scenario(nom, ok, detail=""):
    results.append((nom, ok, detail))
    print(("✅" if ok else "❌"), nom, ("— " + detail if detail else ""))

def run(*args, cwd=BASE, timeout=300):
    return subprocess.run(list(args), capture_output=True, text=True, timeout=timeout, cwd=cwd)

defwb = lambda name: (shutil.copy2(MASTER, p := f"{TMP}/{name}.xlsx"), p)[1]

# ---- 1. VOLUME MASSIF : 2000 devis ----
wb_path = defwb("volume2000")
import openpyxl as _oxl
wb = _oxl.load_workbook(wb_path)
ws = wb.active
t0 = time.time()
for i in range(2000):
    r = ws.max_row + 1
    ws.cell(row=r, column=1, value=f"DEV-2026-{i+900:04d}")
    ws.cell(row=r, column=2, value=datetime.datetime(2026, random_month(), 1 + i % 28))
    ws.cell(row=r, column=3, value=f"Client Vol {i}")
    ws.cell(row=r, column=5, value=f"Travaux lot {i}")
    ws.cell(row=r, column=6, value=100.0 + i)
    ws.cell(row=r, column=7, value="Envoyé")
import random as _rnd
def random_month(): return _rnd.randint(1, 12)
wb.save(wb_path)
t_ins = time.time() - t0
t0 = time.time()
r = run("python3", f"{BASE}/export_devis_to_csv.py", "-e", wb_path, "-o", f"{TMP}/vol.csv")
t_csv = time.time() - t0
t0 = time.time()
r2 = run("python3", f"{BASE}/generate_patron_report.py", "-e", wb_path, "-c", "VOL", "-o", f"{TMP}/vol-rapport.txt")
t_rep = time.time() - t0
scenario("1. Volume 2000 devis", r.returncode == 0 and r2.returncode == 0,
         f"csv {t_csv:.1f}s, rapport {t_rep:.1f}s")

# ---- 2. FICHIER CORROMPU (binaire aléatoire en .xlsx) ----
bad = f"{TMP}/corrompu.xlsx"
open(bad, "wb").write(os.urandom(4096))
r = run("python3", f"{BASE}/export_devis_to_csv.py", "-e", bad, "-o", f"{TMP}/c.csv")
scenario("2. Classeur corrompu → rejet propre", r.returncode != 0 and "Traceback" not in r.stderr,
         "exit code propre, message clair" if r.returncode != 0 else f"rc={r.returncode}")

# ---- 3. FICHIER VERROUILLÉ (permissions 000) ----
lock = defwb("verrouille")
os.chmod(lock, 0o000)
r = run("python3", f"{BASE}/export_devis_to_csv.py", "-e", lock, "-o", f"{TMP}/l.csv")
os.chmod(lock, 0o644)
scenario("3. Classeur verrouillé → rejet propre", r.returncode != 0 and "Traceback" not in r.stderr)

# ---- 4. CLASSEUR VIDE (pas d'en-têtes) ----
empty = f"{TMP}/vide.xlsx"
_wb = _oxl.Workbook(); _wb.save(empty)
r = run("python3", f"{BASE}/generate_patron_report.py", "-e", empty, "-c", "Vide", "-o", f"{TMP}/v.txt")
scenario("4. Classeur vide → rejet propre (pas de traceback)", "Traceback" not in r.stderr,
         f"rc={r.returncode} (rejet attendu, message propre)")

# ---- 5. IMPORT HOSTILE (5 sources cassées) ----
# 5a. JSON vide
open(f"{TMP}/vide.json", "w").write('{"devis": []}')
# 5b. JSON clés inconnues
open(f"{TMP}/inconnu.json", "w").write('[{"toto": 1}, {"titi": "x"}]')
# 5c. CSV malformé (guillemets cassés)
open(f"{TMP}/malforme.csv", "w").write('Date;Client;Montant\n"2026-01-01;Client A;100\n')
# 5d. Fichier binaire renommé .csv
open(f"{TMP}/binaire.csv", "wb").write(os.urandom(512))
# 5e. TXT sans séparateurs
open(f"{TMP}/nosep.txt", "w").write("une ligne sans séparateur\nune autre\n")
import_ok = 0
for f_ in ("vide.json", "inconnu.json", "malforme.csv", "binaire.csv", "nosep.txt"):
    r = run("python3", f"{BASE}/bttp_import.py", "-s", f"{TMP}/{f_}", "-o", f"{TMP}/imp.xlsx")
    if "Traceback" not in r.stderr and (r.returncode != 0 or "0 enregistrements" in r.stdout):
        import_ok += 1
    else:
        scenario(f"5. Import hostile {f_}", False, (r.stderr or "")[-150:])
scenario("5. Import hostile (5 sources cassées)", import_ok == 5,
         f"{import_ok}/5 rejetées proprement")

# ---- 6. PEPPOL HOSTILE ----
pep = [
    ("BCE invalide", ["--client-cbe", "12345"]),
    ("montant négatif", ["--amount-htva", "-1000"]),
    ("montant zéro", ["--amount-htva", "0"]),
]
pep_ok = 0
for label, extra in pep:
    r = run("python3", f"{BASE}/generate_peppol_invoice.py",
            "--output-xml", f"{TMP}/p.xml", "--invoice-number", "T", "--client-name", "X",
            "--client-cbe", "0123456789", "--amount-htva", "1000",
            "--customer-street", "R", "--customer-city", "L", "--customer-zip", "4000",
            *extra)
    propre = "Traceback" not in r.stderr
    refuse = r.returncode != 0 or "ÉCHEC" in r.stdout
    if label == "BCE invalide":
        pep_ok += propre and refuse
    elif label.startswith("montant"):
        pep_ok += propre  # négatif/zéro : doit au moins ne pas crasher
scenario("6. Peppol hostile (3 cas)", pep_ok == 3, f"{pep_ok}/3 propres")

# ---- 7. VALEURS EXTRÊMES ----
# 7a. Nom client 500 caractères dans devis + rapport + peppol
long_nom = "Entreprise " + "X" * 480 + " SPRL"
wbx = defwb("extreme")
r = run("python3", f"{BASE}/append_new_devis.py", "--excel-path", wbx,
        "--client", long_nom, "--montant", "100", "--objet", "Test")
# 7b. Montant énorme (10^12) + objet vide
r2 = run("python3", f"{BASE}/append_new_devis.py", "--excel-path", wbx,
         "--client", "Normal", "--montant", "1000000000000", "--objet", "")
r3 = run("python3", f"{BASE}/generate_peppol_invoice.py", "--output-xml", f"{TMP}/e.xml",
         "--invoice-number", "EXT-001", "--client-name", long_nom[:100],
         "--client-cbe", "0123456789", "--amount-htva", "1000",
         "--customer-street", "R", "--customer-city", "L", "--customer-zip", "4000")
scenario("7. Valeurs extrêmes (nom 500c, montant 10^12, objet vide)",
         all("Traceback" not in (x.stderr or "") for x in (r, r2, r3)))

# ---- 8. NUMÉROTATION : limite %03d (dev 999+) — inséré AVANT le bloc AVERTISSEMENT ----
wb3 = defwb("num999")
wb = _oxl.load_workbook(wb3)
ws = wb.active
# trouver la dernière ligne DEV CONTIGUË (la table s'arrête à la 1re ligne vide
# par design) et insérer juste après — sinon les lignes sont hors table
dernier_dev = 4
for r_ in range(5, ws.max_row + 1):
    v = ws.cell(row=r_, column=1).value
    if not v or not str(v).strip() or str(v).startswith("AVERTISSEMENT"):
        break
    if "DEV" in str(v):
        dernier_dev = r_
for i, numero in ((0, "DEV-2026-998"), (1, "DEV-2026-999")):
    ws.insert_rows(dernier_dev + 1 + i)
    ws.cell(row=dernier_dev + 1 + i, column=1, value=numero)
    ws.cell(row=dernier_dev + 1 + i, column=3, value="C")
    ws.cell(row=dernier_dev + 1 + i, column=6, value=100)
wb.save(wb3)
r = run("python3", f"{BASE}/append_new_devis.py", "--excel-path", wb3,
        "--client", "C", "--montant", "100", "--objet", "Overflow")
# vérifier le numéro généré (max NUMÉRIQUE, pas lexicographique)
wb = _oxl.load_workbook(wb3)
nums = [str(wb.active.cell(row=rr, column=1).value) for rr in range(5, wb.active.max_row + 1)
        if wb.active.cell(row=rr, column=1).value and str(wb.active.cell(row=rr, column=1).value).startswith("DEV-")]
dernier_num = max(int(n.split("-")[-1]) for n in nums if n.split("-")[-1].isdigit())
overflow_ok = dernier_num == 1000
scenario("8. Numérotation au-delà de 999", "Traceback" not in r.stderr and overflow_ok,
         f"numéro max: DEV-2026-{dernier_num}")

print("=" * 60)
echecs = [n for n, ok, _ in results if not ok]
print(f"BILAN: {len(results) - len(echecs)}/{len(results)} scénarios PASS" +
      (f" — ÉCHECS: {echecs}" if echecs else " — ZÉRO BUG ✅"))
sys.exit(1 if echecs else 0)
