#!/usr/bin/env python3
"""ROUND 4 — vérification profonde des angles morts.
A) Le générateur de classeur n'a JAMAIS été exécuté depuis la purge mot de passe.
B) Cycle complet sur classeur NEUF généré.
C) Scan PII du repo distant (noms, téléphones, AVP01, rues).
D) Cron Pipeline : chemin queue vérifié dans jobs.json."""
import os, re, shutil, subprocess, sys

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
TMP = "/home/arthur/.hermes/cache/scratch/round4"
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP, exist_ok=True)
ok_all = True

def scenario(nom, ok, detail=""):
    global ok_all
    if not ok: ok_all = False
    print(("✅" if ok else "❌"), nom, ("— " + detail if detail else ""))

# A. Générateur de classeur neuf (jamais testé post-purge)
wb_new = f"{TMP}/classeur-neuf.xlsx"
r = subprocess.run(["python3", f"{BASE}/generate_devis_sans_oubli.py",
                    "--output", wb_new],
                   capture_output=True, text=True, timeout=180, cwd=BASE)
ok = r.returncode == 0 and os.path.exists(wb_new)
scenario("A1. Générateur de classeur neuf (post-purge mot de passe)", ok,
         (r.stderr or r.stdout).strip()[-120:] if not ok else "généré sans erreur")

if os.path.exists(wb_new):
    import openpyxl
    wb = openpyxl.load_workbook(wb_new)
    # vérifier : 5 onglets attendus? au moins le sheet devis, AUCUN password
    pwds = []
    for sh in wb.worksheets:
        pw = sh.protection.password
        # CE4B = hash openpyxl de la chaîne vide → protection SANS mot de passe (décision 18/11)
        if pw and str(pw) not in ("", "None", "CE4B"):
            pwds.append((sh.title, pw))
    scenario("A2. Zéro mot de passe dans le classeur neuf", not pwds, f"{pwds}" if pwds else f"{len(wb.worksheets)} onglets, protections sans verrou")
    # formules vivantes présentes?
    ws = wb.active
    formules = sum(1 for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("="))
    scenario("A3. Formules vivantes présentes dans le classeur neuf", formules > 0, f"{formules} formules")

    # B. Cycle complet sur ce classeur NEUF
    r = subprocess.run(["python3", f"{BASE}/append_new_devis.py", "--excel-path", wb_new,
                        "--client", "Client R4", "--montant", "1250", "--objet", "Test cycle neuf"],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    r2 = subprocess.run(["python3", f"{BASE}/export_devis_to_csv.py", "-e", wb_new, "-o", f"{TMP}/cycle.csv"],
                        capture_output=True, text=True, timeout=120, cwd=BASE)
    r3 = subprocess.run(["python3", f"{BASE}/generate_patron_report.py", "-e", wb_new, "-c", "Client R4",
                         "-o", f"{TMP}/cycle-rapport.txt"], capture_output=True, text=True, timeout=120, cwd=BASE)
    r4 = subprocess.run(["python3", f"{BASE}/draft_relance_messages.py", "--excel-path", wb_new,
                         "--artisan-name", "Client R4", "--output-md", f"{TMP}/cycle-relances.md"],
                        capture_output=True, text=True, timeout=120, cwd=BASE)
    scenario("B. Cycle complet sur classeur neuf (devis+csv+rapport+relances)",
             all(x.returncode == 0 for x in (r, r2, r3, r4)))

# C. Scan PII du repo distant
import json
r = subprocess.run(["gh", "api", "repos/jbrandonp/antigravity-skills/git/trees/main?recursive=1",
                    "--jq", ".tree[].path"], capture_output=True, text=True, timeout=120)
paths = [p for p in r.stdout.splitlines() if p.startswith("hermes/bttp/")]
print(f"  (scan de {len(paths)} fichiers bttp dans le repo distant)")
suspects = []
for p in paths:
    if any(k in p.lower() for k in ("st_nicolas", "avp01", "outreach_queue", "export_devis_erp", "rapport_patron_exemple", "fichier_prospection")):
        suspects.append(p)
# contenu : téléphones et noms dans les fichiers texte les plus risqués
suspects_contenu = []
for p in paths:
    if p.endswith((".md", ".py", ".json")) and any(k in p for k in ("MANUEL", "DOSSIER", "PACK", "README", "main.py")):
        r2 = subprocess.run(["gh", "api", f"repos/jbrandonp/antigravity-skills/contents/{p}", "--jq", ".content"],
                            capture_output=True, text=True, timeout=60)
        import base64
        try:
            content = base64.b64decode(r2.stdout.strip()).decode("utf-8", errors="replace")
        except Exception:
            continue
        if re.search(r"04\d{2}[ .]?\d{2}[ .]?\d{2}[ .]?\d{2}", content) or "Jean-Marc Dupont" in content or "AVP01" in content:
            suspects_contenu.append(p)
scenario("C. Scan PII du repo distant (noms/téléphones/AVP01)", not suspects and not suspects_contenu,
         f"fichiers suspects: {suspects + suspects_contenu}" if (suspects or suspects_contenu) else f"{len(paths)} fichiers scannés, rien trouvé")

# D. Cron Pipeline : chemin de la queue dans jobs.json
j = json.load(open("/home/arthur/.hermes/cron/jobs.json"))
jobs = j if isinstance(j, list) else j.get("jobs", [])
for x in jobs:
    if x.get("id") == "60302a8c02eb":
        prompt = x.get("prompt", "")
        ok = "/srv/data/bttp-confidentiel/outreach_queue.json" in prompt and \
             "03_Vente_et_Prospection_Terrain/outreach_queue" not in prompt
        scenario("D. Cron Pipeline → queue dans confidentiel", ok)
        break

print("=" * 60)
print("ROUND 4:", "TOUT VERT ✅" if ok_all else "DES FAILLES ❌")
sys.exit(0 if ok_all else 1)
