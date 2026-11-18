#!/usr/bin/env python3
"""Backup chiffré quotidien des données clients BTTP (AES-256-CBC + PBKDF2).
Source : /srv/data/bttp-clients → Destination : /srv/data/backups/bttp-clients/
Rétention 7 jours. Idempotent. Silencieux en succès ; échec = exit non-zéro
= alerte cron automatique. Vérifie le chiffré en lecture après écriture.
"""
import datetime, glob, os, subprocess, sys

SRC = "/srv/data/bttp-clients"
DST = "/srv/data/backups/bttp-clients"
KEYFILE = "/home/arthur/.hermes/secrets/bttp-backup.key"
KEEP = 7

def main() -> int:
    stamp = datetime.date.today().isoformat()
    today = os.path.join(DST, f"{stamp}.tar.gz.enc")
    if not os.path.isdir(SRC):
        print(f"ERREUR: source {SRC} absente"); return 1
    if not os.path.isfile(KEYFILE):
        print(f"ERREUR: keyfile {KEYFILE} absente"); return 1
    if os.path.exists(today):
        return 0  # idempotent
    os.makedirs(DST, exist_ok=True)

    tmp_tar = f"/tmp/bttp-backup-{stamp}.tar.gz"

    # pg_dump du schéma CRM (PostgreSQL) — les données CRM ne sont nulle part ailleurs.
    # DATABASE_URL lu depuis l'environnement du processus crm_server en cours (jamais
    # depuis un fichier d'identifiants).
    dump_crm = None
    env = dict(os.environ)
    try:
        for pid_dir in os.listdir("/proc"):
            if not pid_dir.isdigit():
                continue
            try:
                with open(f"/proc/{pid_dir}/cmdline", "rb") as f:
                    cmdline = f.read().decode("utf-8", errors="replace")
                if "crm_server.py" not in cmdline:
                    continue
                with open(f"/proc/{pid_dir}/environ", "rb") as f:
                    for entry in f.read().decode("utf-8", errors="replace").split("\0"):
                        if entry.startswith("DATABASE_URL="):
                            env["DATABASE_URL"] = entry.split("=", 1)[1]
                            break
                if "DATABASE_URL" in env:
                    break
            except (PermissionError, FileNotFoundError, ProcessLookupError):
                continue
    except OSError as exc:
        print("Avertissement: scan /proc impossible:", exc)
    if "DATABASE_URL" in env:
        import gzip as gz
        r_pg = subprocess.run(["pg_dump", "--schema=crm", "-d", env["DATABASE_URL"]],
                              capture_output=True, text=True, timeout=120, env=env)
        if r_pg.returncode == 0 and "CREATE TABLE" in r_pg.stdout:
            dump_crm = f"/tmp/bttp-crm-{stamp}.sql.gz"
            with gz.open(dump_crm, "wt") as f:
                f.write(r_pg.stdout)
            print(f"pg_dump crm OK ({len(r_pg.stdout) // 1024} Ko SQL)")
        else:
            print("Avertissement: pg_dump crm a echoue - backup fichiers quand meme:",
                  (r_pg.stderr or "")[:120])
    else:
        print("Avertissement: processus crm_server introuvable - pg_dump crm ignore")

    try:
        tar_cmd = ["tar", "-czf", tmp_tar, "-C", os.path.dirname(SRC), os.path.basename(SRC)]
        if dump_crm:
            tar_cmd += ["-C", "/tmp", os.path.basename(dump_crm)]
        subprocess.run(tar_cmd, check=True, timeout=600)
        subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000",
                        "-salt", "-in", tmp_tar, "-out", today, "-pass", f"file:{KEYFILE}"],
                       check=True, timeout=600)
        # Manifeste d'intégrité
        sha = subprocess.run(["sha256sum", today], capture_output=True, text=True, check=True)
        with open(os.path.join(DST, f"{stamp}.sha256"), "w") as f:
            f.write(sha.stdout)

        # Vérification lecture : déchiffrer + lister, le classeur doit être présent
        test_out = f"/tmp/bttp-backup-test-{stamp}.tar.gz"
        subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "200000",
                        "-in", today, "-out", test_out, "-pass", f"file:{KEYFILE}"],
                       check=True, timeout=600)
        listing = subprocess.run(["tar", "-tzf", test_out], capture_output=True, text=True)
        if "DEVIS" not in listing.stdout:
            print("ERREUR: backup illisible/incomplet — archive rejetée")
            os.remove(today)
            sidecar = os.path.join(DST, f"{stamp}.sha256")
            if os.path.exists(sidecar):
                os.remove(sidecar)
            return 1
        os.remove(test_out)

        # Rétention 7 jours
        archives = sorted(glob.glob(os.path.join(DST, "*.tar.gz.enc")), reverse=True)
        for old in archives[KEEP:]:
            os.remove(old)
            sidecar = old.replace(".tar.gz.enc", ".sha256")
            if os.path.exists(sidecar):
                os.remove(sidecar)
        print(f"backup {stamp} OK ({os.path.getsize(today) // 1024} Ko) — vérifié en lecture")
        return 0
    finally:
        if os.path.exists(tmp_tar):
            os.remove(tmp_tar)

if __name__ == "__main__":
    sys.exit(main())
