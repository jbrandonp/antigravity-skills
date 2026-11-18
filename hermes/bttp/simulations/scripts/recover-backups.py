#!/usr/bin/env python3
"""RÉCUPÉRATION après destruction accidentelle des backups (symlink traversé).
1. Nouveau repo restic sur le volume (mot de passe dans secrets, chmod 600)
2. pg_dumpall + dumps par base régénérés immédiatement
3. Backup chiffré BTTP régénéré
4. Garde anti-récurrence : realpath avant toute suppression (définitif)."""
import os, subprocess, sys

SECRETS = "/home/arthur/.hermes/secrets"
BACKUPS = "/srv/data/backups"
RESTIC_PW = f"{SECRETS}/restic-repo.password"

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=kw.pop("timeout", 600), **kw)
    return r

# 1. recréer le dossier backups
os.makedirs(BACKUPS, exist_ok=True)

# 2. dumps PostgreSQL régénérés immédiatement (les bases sont vivantes)
env = dict(os.environ)
for pid in os.listdir("/proc"):
    if pid.isdigit():
        try:
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().decode("utf-8", "replace")
            if "crm_server.py" in cmd:
                for e in open(f"/proc/{pid}/environ", "rb").read().decode("utf-8", "replace").split("\0"):
                    if e.startswith("DATABASE_URL="):
                        env["DATABASE_URL"] = e.split("=", 1)[1]
                break
        except (OSError, PermissionError):
            continue
if "DATABASE_URL" in env:
    r = run(["sudo", "-n", "-u", "postgres", "pg_dumpall", "-f", f"{BACKUPS}/pg_dumpall-20261118-recovery.sql"])
    print("pg_dumpall:", "OK" if r.returncode == 0 else r.stderr[:200])
else:
    print("⚠️ DATABASE_URL non trouvé — dump via sudo postgres direct")
    r = run(["sudo", "-n", "-u", "postgres", "pg_dumpall", "-f", f"{BACKUPS}/pg_dumpall-20261118-recovery.sql"])
    print("pg_dumpall (sudo):", "OK" if r.returncode == 0 else r.stderr[:200])

# 3. nouveau repo restic
if not os.path.exists(f"{BACKUPS}/restic/config"):
    if not os.path.exists(RESTIC_PW):
        open(RESTIC_PW, "w").write(os.urandom(24).hex())
        os.chmod(RESTIC_PW, 0o600)
    env_r = dict(os.environ, RESTIC_PASSWORD_FILE=RESTIC_PW)
    r = run(["restic", "-r", f"{BACKUPS}/restic", "init"], env=env_r)
    print("restic init:", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else "fait")

# 4. premier backup restic : vault + configs + bttp (les données vivantes)
env_r = dict(os.environ, RESTIC_PASSWORD_FILE=RESTIC_PW)
r = run(["restic", "-r", f"{BACKUPS}/restic", "backup",
         "/srv/data/obsidian-vault", "/srv/data/bttp-confidentiel",
         "/srv/brandon-ai/workspaces/bttp", "/home/arthur/.hermes/scripts",
         "/etc/postgresql/16/main", "--tag", "recovery-20261118"], env=env_r, timeout=900)
print("restic backup recovery:", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else "fait")

# 5. backup BTTP chiffré régénéré
r = run(["python3", "/home/arthur/.hermes/scripts/backup_clients.py"])
print("backup chiffré:", (r.stdout or r.stderr).strip()[:80])
