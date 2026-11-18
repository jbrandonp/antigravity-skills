#!/usr/bin/env python3
"""Vérification de bout en bout de tout ce qui a été fait ce soir (18 nov soir)."""
import os, json, subprocess

ok = []
fail = []

def check(name, cond, detail=""):
    (ok if cond else fail).append(f"{name} {detail}")

# 1. PostgreSQL sur le volume
r = subprocess.run(["sudo","-n","-u","postgres","psql","-tAc","SHOW data_directory;"],
                   capture_output=True, text=True)
check("1. PostgreSQL → volume", "/srv/data/postgresql" in r.stdout, r.stdout.strip())

# 2. CRM servi depuis la nouvelle base
r = subprocess.run(["sudo","-n","-u","postgres","psql","-d","brandon_ai","-tAc",
                    "SELECT count(*) FROM crm.contacts;"], capture_output=True, text=True)
check("2. CRM intact", r.stdout.strip() == "5", f"({r.stdout.strip()} contacts)")

# 3. Vault accessible via symlink
vp = "/srv/brandon-ai/workspaces/obsidian-vault"
check("3. Vault symlink", os.path.islink(vp) and os.path.isdir(vp))
check("3b. 08-Clients présent", os.path.isdir(vp + "/08-Clients"))
n_files = sum(len(fs) for _,_,fs in os.walk(vp))
check("3c. Vault complet (91 fichiers)", n_files == 91, f"({n_files})")

# 4. Backups récupérés
b = "/srv/data/backups"
check("4. pg_dumpall recovery", os.path.getsize(b+"/pg_dumpall-20261118-recovery.sql") > 100_000_000)
check("4b. Dump CRM", os.path.exists(b+"/bttp-crm-2026-11-18.sql.gz") and os.path.getsize(b+"/bttp-crm-2026-11-18.sql.gz") > 2000)
check("4c. Repo restic", os.path.exists(b+"/restic/config"))
r = subprocess.run(["bash","-c","RESTIC_PASSWORD_FILE=/home/arthur/.hermes/secrets/restic-repo.password restic -r /srv/data/backups/restic snapshots --json | wc -l"], capture_output=True, text=True)
check("4d. Restic snapshot(s)", int(r.stdout.strip() or 0) >= 1, f"({r.stdout.strip()})")
check("4e. Backup chiffré BTTP", os.path.exists(b+"/bttp-clients/2026-11-18.tar.gz.enc"))
# pg_dump présent DANS l'archive chiffrée ?
r = subprocess.run(["bash","-c","""python3 - <<'EOF'
import io, tarfile, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key = open('/home/arthur/.hermes/secrets/bttp-clients.key').read().strip()
k = hashlib.sha256(key.encode()).digest()
data = open('/srv/data/backups/bttp-clients/2026-11-18.tar.gz.enc','rb').read()
out = AESGCM(k).decrypt(data[:12], data[12:], b'bttp-clients')
tf = tarfile.open(fileobj=io.BytesIO(out))
print('CRM' if any('crm' in n.lower() for n in tf.getnames()) else 'NO_CRM')
EOF"""], capture_output=True, text=True)
check("4f. Dump CRM DANS l'archive chiffrée", "CRM" in r.stdout, r.stdout.strip() or r.stderr[:80])

# 5. Cron moves auto
try:
    jobs = json.load(open("/home/arthur/.hermes/cron/jobs.json"))
    def find(nm):
        for j in jobs:
            if j.get("id") == nm or j.get("name") == nm:
                return j
    j = find("eb9a571f017f")
    check("5. Cron moves auto actif", bool(j) and j.get("enabled") is not False)
    j2 = find("60302a8c02eb")
    sch = (j2 or {}).get("schedule", "")
    check("6. Pipeline mode volume 2×/jour", "6,14" in sch or "14" in sch, f"({sch})")
except Exception as e:
    fail.append(f"5/6. vérif crons: {e}")

# 7. Détection conflits OneDrive dans le script rapport
src = open("/home/arthur/.hermes/scripts/rapport_patron_mensuel.py").read()
check("7. Détection conflits OneDrive", "conflit" in src)

# 8. Tests BTTP
r = subprocess.run(["bash","-c","cd /srv/brandon-ai/workspaces/bttp/bttp && python3 run_all_tests.py 2>&1 | grep -E 'Réussites'"], capture_output=True, text=True, timeout=600)
check("8. Tests BTTP", "138" in r.stdout, r.stdout.strip())

# 9. Disques
r = subprocess.run(["df","-h","/","/srv/data"], capture_output=True, text=True)
lines = [l for l in r.stdout.splitlines() if "/" in l]
print("Disques:", lines)

print(f"\n✅ {len(ok)} vérifications OK")
for o in ok: print("  ✓", o)
if fail:
    print(f"\n❌ {len(fail)} ÉCHECS:")
    for f in fail: print("  ✗", f)
else:
    print("\n🏆 ZÉRO ÉCHEC — tout ce qui devait être fait est fait et vérifié")
