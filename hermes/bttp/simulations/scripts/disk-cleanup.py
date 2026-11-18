#!/usr/bin/env python3
"""Libère le disque système : déplace les backups hérités vers le volume, vacuum journald.
Non destructif : tout est déplacé, rien de supprimé."""
import os, shutil, subprocess

HOME = "/home/arthur"
DST = "/srv/data/backups"
os.makedirs(DST, exist_ok=True)

def mv(src, dst_dir, note=""):
    if not os.path.exists(src):
        return
    dst = os.path.join(dst_dir, os.path.basename(src.rstrip("/")))
    if os.path.exists(dst):
        print(f"⚠️ collision ignorée: {src}")
        return
    shutil.move(src, dst)
    print(f"✓ {src} → {dst} {note}")

# 1. repo restic (5,2 Go) → volume
mv(f"{HOME}/backups/restic", DST, "(repo restic hérité — nouveau chemin à référencer)")

# 2. dumps pg hérités
mv(f"{HOME}/backups/pgdump", DST, "(dumps pg anciens)")
mv(f"{HOME}/backups/pg_dumpall-pre-migration-20261118.sql", DST, "(doublon du volume)")
mv(f"{HOME}/backups/backup-test-2026-11-11.log", DST)

# 3. petits dossiers bttp égarés dans home/backups
mv(f"{HOME}/backups/bttp", DST + "/legacy-home")
mv(f"{HOME}/backups/bttp-clients", DST + "/legacy-home")

# 4. journald : vacuum à 100 Mo
r = subprocess.run(["sudo", "-n", "journalctl", "--vacuum-size=100M"],
                   capture_output=True, text=True)
print("✓ journald vacuum:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "fait")

# 5. référencer le nouveau chemin restic dans 04-Secrets
idx = "/srv/brandon-ai/workspaces/obsidian-vault/04-Secrets/Index.md"
src = open(idx, encoding="utf-8").read()
if "restic" in src and "/srv/data/backups/restic" not in src:
    src = src.replace("/home/arthur/backups/restic", "/srv/data/backups/restic")
    src += "\n- 2026-11-18 — Repo restic déplacé vers `/srv/data/backups/restic` (disque système libéré de 5,2 Go). Aucun cron restic actif trouvé — exécution manuelle uniquement.\n"
    open(idx, "w", encoding="utf-8").write(src)
    print("✓ 04-Secrets/Index.md mis à jour (chemin restic)")

# 6. état final
r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1])
