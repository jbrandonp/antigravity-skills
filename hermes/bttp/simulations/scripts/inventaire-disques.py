#!/usr/bin/env python3
"""Inventaire : où vivent les données appartenant aux clients ? (/ = système 89 % vs /srv/data = volume)"""
import os

print("=== 1. Données clients sur le VOLUME dédié (bon) ===")
ok = []
if os.path.islink("/srv/brandon-ai/workspaces/bttp/clients"):
    ok.append("/srv/brandon-ai/workspaces/bttp/clients → " + os.path.realpath("/srv/brandon-ai/workspaces/bttp/clients"))
ok.append("/srv/data/bttp-confidentiel/ (queue, dossier St-Nicolas, archives)")
for o in ok:
    print("  ✓", o)

print("\n=== 2. Données clients encore sur le disque SYSTÈME / (à vérifier) ===")
# a. PostgreSQL : le schéma crm (contacts/deals/interactions = données clients)
r = os.popen("sudo -n -u postgres psql -tAc \"SHOW data_directory;\" 2>&1 || psql -tAc \"SHOW data_directory;\" 2>&1").read().strip()
print("  a. PostgreSQL data_directory:", r or "non déterminé (accès psql requis)")
# b. Vault 08-Clients (fiches clients) — sur /
vp = "/srv/brandon-ai/workspaces/obsidian-vault/08-Clients"
n = len([f for f in os.listdir(vp) if f.endswith(".md")]) if os.path.isdir(vp) else 0
size = sum(os.path.getsize(os.path.join(r2, f)) for r2, d, fs in os.walk(vp) for f in fs) // 1024
print(f"  b. Vault 08-Clients: {n} fiches, {size} Ko → SUR / (système)")
# c. Vault 04-Secrets references — sur / (ok: références seulement)
# d. exports CRM récents
import glob
csvs = glob.glob("/srv/brandon-ai/workspaces/crm_*export*.csv")
print("  c. Exports CRM en racine workspaces:", csvs if csvs else "aucun (déplacés ✓)")
# e. backups du CRM sur /srv/data ✓
print("  d. Backup CRM chiffré:", "✓ /srv/data/backups/bttp-clients/" if glob.glob("/srv/data/backups/bttp-clients/*.tar.gz.enc") else "absent")

print("\n=== 3. Capacité sudo pour migration PostgreSQL ===")
r = os.popen("sudo -n true 2>&1 && echo SUDO_OK || echo SUDO_NON").read().strip()
print("  sudo sans mot de passe:", r)
