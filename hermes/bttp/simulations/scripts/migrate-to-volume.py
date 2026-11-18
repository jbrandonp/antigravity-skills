#!/usr/bin/env python3
"""Migration des données clients vers le volume /srv/data :
1) Backup pg_dumpall AVANT toute manipulation
2) Migration du data_directory PostgreSQL vers /srv/data/postgresql
3) Vault Obsidian déplacé + symlink
Vérification à chaque étape, rollback possible."""
import os, subprocess, sys

def run(cmd, timeout=600, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        print(f"ÉCHEC: {cmd}\n{r.stderr[:400]}")
        sys.exit(1)
    return r

print("=== 1. BACKUP PRÉALABLE (pg_dumpall complet) ===")
r = run("sudo -n -u postgres pg_dumpall > /srv/data/backups/pg_dumpall-pre-migration-20261118.sql")
print("  pg_dumpall:", os.path.getsize("/srv/data/backups/pg_dumpall-pre-migration-20261118.sql") // 1024, "Ko ✓")

print("=== 2. ARRÊT PostgreSQL ===")
run("sudo -n systemctl stop postgresql")
print("  arrêté")

print("=== 3. COPIE data_directory vers le volume ===")
run("sudo -n mkdir -p /srv/data/postgresql")
run("sudo -n rsync -a /var/lib/postgresql/16/main /srv/data/postgresql/16/")
run("sudo -n chown -R postgres:postgres /srv/data/postgresql")
print("  copié:", os.popen("sudo -n du -sh /srv/data/postgresql/16/main").read().strip())

print("=== 4. Bascule data_directory ===")
conf = "/etc/postgresql/16/main/postgresql.conf"
src = open(conf).read()
if "data_directory = '/srv/data/postgresql/16/main'" not in src:
    import re
    src = re.sub(r"data_directory = '[^']*'", "data_directory = '/srv/data/postgresql/16/main'", src)
    open(conf, "w").write(src)
print("  postgresql.conf → /srv/data/postgresql/16/main")

print("=== 5. DÉMARRAGE + VÉRIFICATION ===")
run("sudo -n systemctl start postgresql")
r = run("sudo -n -u postgres psql -tAc \"SELECT count(*) FROM crm.contacts;\"")
print("  crm.contacts accessible:", r.stdout.strip(), "lignes ✓")
r = run("sudo -n -u postgres psql -tAc \"SHOW data_directory;\"")
print("  data_directory actif:", r.stdout.strip())

# 6. Vault → volume + symlink
print("=== 6. VAULT vers le volume ===")
VOLD = "/srv/data/obsidian-vault"
if not os.path.exists(VOLD):
    shutil_done = run("mv /srv/brandon-ai/workspaces/obsidian-vault /srv/data/obsidian-vault", check=True)
os.symlink(VOLD, "/srv/brandon-ai/workspaces/obsidian-vault") if not os.path.islink("/srv/brandon-ai/workspaces/obsidian-vault") else None
print("  vault déplacé + symlink en place")
print("=== MIGRATION TERMINÉE ===")
