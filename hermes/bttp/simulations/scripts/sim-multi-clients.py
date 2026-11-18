#!/usr/bin/env python3
"""SIMULATION MULTI-CLIENTS — 3 profiles d'artisans différents + données désordonnées.
Teste tout le cycle : devis → CSV → Peppol → rapport → relances → fiche vault → cron multi-clients → backup."""
import datetime, json, os, shutil, subprocess, openpyxl

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
CLIENTS = "/srv/data/bttp-clients"
VAULT = "/srv/brandon-ai/workspaces/obsidian-vault/08-Clients"
MASTER = os.path.join(BASE, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")

CLIENTS_SIM = [
    {
        "nom": "Dubreuil & Fils <Spa>",
        "metier": "Électricien", "taille": 8,
        "particularites": "caractères spéciaux & <>, dates texte FR (05/03/2026), statut 'Signé'",
        "devis": [
            ("05/03/2026", "Tableau électrique + mise aux normes", 1450.0, "Signé", "12/03/2026"),
            ("2026-04-10", "Réfection complète appartement", 4200.0, "Envoyé", "17/04/2026"),
            ("18/11/2026", "Panneaux solaires 6 kwc", 7800.0, "En attente", "25/11/2026"),
        ],
    },
    {
        "nom": "ETS MARTIN",
        "metier": "Plombier-chauffagiste", "taille": 12,
        "particularites": "MAJUSCULES, statut 'Validé', relances très en retard",
        "devis": [
            ("01/09/2026", "Chaudière condensation + désembouage", 4850.0, "Validé", "08/09/2026"),
            ("15/09/2026", "Salle de bain complète", 6200.0, "Relancé", "22/09/2026"),
            ("01/10/2026", "Remplacement radiateurs ×6", 1980.0, "En attente", "08/10/2026"),
            ("10/10/2026", "Thermostat connecté + pose", 420.0, "Perdu", "17/10/2026"),
        ],
    },
    {
        "nom": "carrelage-dupont",
        "metier": "Carreleur", "taille": 5,
        "particularites": "minuscules + tiret, statut 'OK' (non standard), montants variés",
        "devis": [
            ("2026-10-01", "Sol carrelage 45 m² + plinthes", 2250.0, "OK", "2026-10-08"),
            ("2026-10-20", "Douche à l'italienne", 1890.0, "OK", "2026-10-27"),
            ("2026-11-10", "Terrasse extérieure 30 m²", 3400.0, "Envoyé", "2026-11-17"),
        ],
    },
]

def results(name, ok, detail=""):
    print(("✅" if ok else "❌"), name, detail)

print("=" * 60)
for c in CLIENTS_SIM:
    slug = c["nom"].replace(" ", "-")
    cdir = os.path.join(CLIENTS, slug)
    os.makedirs(cdir, exist_ok=True)
    wb_path = os.path.join(cdir, f"DEVIS_{slug}.xlsx")
    shutil.copy2(MASTER, wb_path)

    # 1. Devis via le script officiel (numérotation + formules du socle)
    devis_ok = 0
    for date_str, objet, montant, statut, relance in c["devis"]:
        r = subprocess.run(["python3", os.path.join(BASE, "append_new_devis.py"),
                            "--excel-path", wb_path, "--client", c["nom"],
                            "--montant", str(montant), "--objet", objet,
                            "--statut", statut],
                           capture_output=True, text=True, timeout=120, cwd=BASE)
        if r.returncode == 0 and "SUCCÈS" in (r.stdout or ""):
            devis_ok += 1
    results(f"[{c['nom']}] devis insérés", devis_ok == len(c["devis"]), f"{devis_ok}/{len(c['devis'])}")

    # 2. Export CSV + vérif anti-injection
    csv_out = os.path.join(cdir, "export_erp.csv")
    r = subprocess.run(["python3", os.path.join(BASE, "export_devis_to_csv.py"),
                        "-e", wb_path, "-o", csv_out],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    import csv as _csv
    rows = list(_csv.reader(open(csv_out, encoding="utf-8-sig"), delimiter=";"))
    injecte = any(cell.strip().startswith(("=", "@")) for row in rows[1:] for cell in row
                  if isinstance(cell, str))
    results(f"[{c['nom']}] export CSV", r.returncode == 0 and not injecte, f"{len(rows)-1} lignes, injection={'non' if not injecte else 'OUI'}")

    # 3. Facture Peppol (montant = 1er devis, client avec caractères spéciaux)
    xml_out = os.path.join(cdir, "facture_test.xml")
    r = subprocess.run(["python3", os.path.join(BASE, "generate_peppol_invoice.py"),
                        "--output-xml", xml_out, "--invoice-number", f"FACT-{slug[:8]}-001",
                        "--client-name", c["nom"], "--client-cbe", "0123456789",
                        "--amount-htva", str(c["devis"][0][2]),
                        "--customer-street", "Rue Test 1", "--customer-city", "Liège",
                        "--customer-zip", "4000", "--vat-rate", "0.06"],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    results(f"[{c['nom']}] facture Peppol pré-vol", r.returncode == 0 and "Pré-vol" in (r.stdout or ""))

    # 4. Rapport patron — les statuts exotiques doivent être reconnus
    r = subprocess.run(["python3", os.path.join(BASE, "generate_patron_report.py"),
                        "-e", wb_path, "-c", c["nom"], "-o", os.path.join(cdir, "rapport.txt")],
                       capture_output=True, text=True, timeout=180, cwd=BASE)
    rapport = open(os.path.join(cdir, "rapport.txt"), encoding="utf-8").read() if r.returncode == 0 else ""
    gagne = "GAGNÉ" in rapport and ("0.00 € HTVA (0 dossiers" not in rapport.split("CHIFFRE D'AFFAIRES")[1][:80] if "CHIFFRE D'AFFAIRES" in rapport else True)
    results(f"[{c['nom']}] rapport patron", r.returncode == 0 and "SYNTHÈSE" in rapport,
            f"CA gagné reconnu: {'oui' if gagne else 'à vérifier'}")

    # 5. Relances
    r = subprocess.run(["python3", os.path.join(BASE, "draft_relance_messages.py"),
                        "--excel-path", wb_path, "--artisan-name", c["nom"],
                        "--output-md", os.path.join(cdir, "relances.md")],
                       capture_output=True, text=True, timeout=120, cwd=BASE)
    results(f"[{c['nom']}] relances", r.returncode == 0)

    # 6. Fiche vault
    fiche = os.path.join(VAULT, f"{c['nom']} (SIMULATION 2).md")
    open(fiche, "w", encoding="utf-8").write(
        f"---\ntitle: \"Fiche — {c['nom']} (SIMULATION 2)\"\ntags: [client, simulation]\nstatus: prospect\n---\n\n"
        f"# {c['nom']} (SIMULATION 2 — client fictif multi-profils)\n\n"
        f"| Métier | {c['metier']} |\n| Taille | {c['taille']} pers. |\n"
        f"| Particularités testées | {c['particularites']} |\n| Devis insérés | {devis_ok} |\n\n"
        "## Notes d'échange\n\n### 2026-11-18 — Simulation multi-clients\nCycle complet exécuté.\n")

print("=" * 60)
# 7. Cron mensuel multi-clients (doit traiter TOUS les clients)
r = subprocess.run(["python3", "/home/arthur/.hermes/scripts/rapport_patron_mensuel.py"],
                   capture_output=True, text=True, timeout=600)
out = r.stdout or ""
n_rapports = out.count("## ")
print(f"{'✅' if r.returncode == 0 else '❌'} cron mensuel multi-clients: {n_rapports} clients traités, rc={r.returncode}")
alerts = [l for l in out.splitlines() if "⚠️" in l]
print(f"   alertes: {len(alerts)}")

# 8. Backup couvre les nouveaux clients
r = subprocess.run(["python3", "/home/arthur/.hermes/scripts/backup_clients.py"],
                   capture_output=True, text=True, timeout=600)
print(("✅" if r.returncode == 0 else "❌"), "backup quotidien:", (r.stdout or r.stderr).strip()[:100])
