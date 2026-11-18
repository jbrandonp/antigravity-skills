#!/usr/bin/env python3
"""Rapport Patron mensuel automatique — Pack 3 BTTP.
Scanne /srv/brandon-ai/workspaces/bttp/clients/<client>/ pour chaque classeur devis,
génère le rapport patron, sync les statuts vers la fiche Obsidian du client.
Sortie : résumé textuel pour le cron (ou [SILENT] si aucun client).
Usage : python3 rapport_patron_mensuel.py [--clients-dir DIR]"""
import json, os, re, shutil, subprocess, sys, glob

sys.path.insert(0, "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel")

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"
CLIENTS_DIR = "/srv/brandon-ai/workspaces/bttp/clients"
TIMEOUT_PAR_CLIENT = int(os.environ.get("BTTP_RAPPORT_TIMEOUT", "120"))  # secondes, ajustable
VAULT_CLIENTS = "/srv/brandon-ai/workspaces/obsidian-vault/08-Clients"

def get_arg(name, default=None):
    argv = sys.argv
    if name in argv:
        return argv[argv.index(name) + 1]
    return default

clients_dir = get_arg("--clients-dir", CLIENTS_DIR)
if not os.path.isdir(clients_dir):
    print("[SILENT]")
    sys.exit(0)

def _nom_client_sure(nom: str) -> bool:
    """Anti path-traversal : refuse les noms manipulant des chemins."""
    return not any(bad in nom for bad in ("/", "\\", "..", "\x00")) and nom not in (".", "")


clients = sorted(d for d in os.listdir(clients_dir)
                 if os.path.isdir(os.path.join(clients_dir, d)) and _nom_client_sure(d))
if not clients:
    print("[SILENT]")
    sys.exit(0)

lines = ["# 📊 RAPPORT PATRON MENSUEL AUTO — " + os.environ.get("SIM_DATE", "")[:10] or "2026-11-18",
         ""]
total_pipeline = 0.0
alerts = []

for client in clients:
    cdir = os.path.join(clients_dir, client)
    wb = glob.glob(os.path.join(cdir, "DEVIS*.xlsx"))
    if not wb:
        alerts.append(f"⚠️ {client}: aucun classeur devis trouvé")
        continue
    if len(wb) > 1:
        alerts.append(f"⚠️ {client}: {len(wb)} classeurs trouvés — seul {os.path.basename(wb[0])} est traité, les autres sont ignorés")
    wb = wb[0]
    out = os.path.join(cdir, "rapport_patron_" + __import__("datetime").date.today().strftime("%Y-%m") + ".txt")
    try:
        r = subprocess.run(["python3", os.path.join(BASE, "generate_patron_report.py"),
                            "-e", wb, "-c", client, "-o", out],
                           capture_output=True, text=True, timeout=TIMEOUT_PAR_CLIENT, cwd=BASE)
    except (subprocess.TimeoutExpired, OSError) as exc:
        alerts.append(f"⚠️ {client}: échec génération rapport ({type(exc).__name__}: {exc})")
        continue
    if r.returncode != 0 or not os.path.exists(out):
        alerts.append(f"⚠️ {client}: échec génération rapport ({(r.stderr or r.stdout).strip()[:120]})")
        continue
    txt = open(out, encoding="utf-8").read()
    m = re.search(r"Pipeline EN COURS\s*: ([\d\s.,]+) €", txt)
    if m:
        # format "1,234,567.89" (virgules = séparateurs de milliers, point = décimal)
        total_pipeline += float(m.group(1).replace(" ", "").replace(",", "") or 0)
    alerts_found = "ALERTES" in txt
    lines.append(f"## {client}")
    lines.append(f"- Rapport : `{out}`")
    lines.append(f"- Alertes en souffrance : {'OUI — action requise' if alerts_found else 'non'}")
    # sync statut fiche vault — matching tolérant : le slug du dossier (tirets)
    # ne correspond pas au nom de fiche (espaces, suffixes type "(SIMULATION)").
    # Recherche : correspondance insensible à la casse/tirets/espaces/suffixes.
    def _norm(s: str) -> str:
        # casse d'abord, puis suffixes (sinon "sim" casse "simulation"), puis séparateurs + chiffres isolés
        s = s.lower()
        for tok in ("simulation2", "simulation", "sim", "(", ")", "-", "_"):
            s = s.replace(tok, " ")
        mots = [m for m in s.split() if not m.isdigit()]
        return " ".join(mots)

    fiche = None
    for cand in os.listdir(VAULT_CLIENTS):
        if not cand.endswith(".md") or cand.startswith("_"):
            continue
        if _norm(cand[:-3]) == _norm(client):
            fiche = os.path.join(VAULT_CLIENTS, cand)
            break
    if fiche:
        note = open(fiche, encoding="utf-8").read()
        stamp = __import__("datetime").date.today().strftime("%Y-%m-%d")
        block = f"\n### {stamp} — Rapport patron auto\n- Pipeline rapporté, rapport: `{os.path.basename(out)}`\n"
        if "Rapport patron auto" not in note:
            note = note.rstrip() + "\n## Notes d'échange" if "## Notes d'échange" not in note else note
            note = note.rstrip() + block
            try:
                # écriture atomique : backup + tmp + rename (jamais d'écrasement sec)
                shutil.copy2(fiche, fiche + ".bak")
                tmp = fiche + ".tmp"
                with open(tmp, "w", encoding="utf-8") as fh:
                    fh.write(note)
                os.replace(tmp, fiche)
                lines.append("- Fiche vault synchronisée ✔")
            except OSError as exc:
                alerts.append(f"⚠️ {client}: échec sync fiche vault ({exc})")
    else:
        lines.append("- ⚠️ pas de fiche vault — à créer")
    lines.append("")

# détection de conflits de synchro cloud (OneDrive/Drive) — scaling 5-25 clients
conflits = []
for root2, dirs2, files2 in os.walk(clients_dir):
    for f2 in files2:
        low = f2.lower()
        if ("conflit" in low or "conflict" in low) and not f2.startswith("."):
            conflits.append(os.path.join(root2, f2).replace(clients_dir + os.sep, ""))
if conflits:
    alerts.append(f"⚠️ {len(conflits)} fichier(s) de conflit cloud détecté(s): " + ", ".join(conflits[:3]))

if alerts:
    lines.append("## ⚠️ Alertes techniques")
    lines.extend("- " + a for a in alerts)

print("\n".join(lines) if len(lines) > 2 else "[SILENT]")
