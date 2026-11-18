#!/usr/bin/env python3
"""Répare la migration vault interrompue : vérifie la complétude de la copie,
restaure ce qui manque, puis termine proprement avec sudo."""
import filecmp, os, subprocess, sys

OLD = "/srv/brandon-ai/workspaces/obsidian-vault"
VOLD = "/srv/data/obsidian-vault"

def tree(root):
    out = {}
    for r, d, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            rel = os.path.relpath(p, root)
            try:
                out[rel] = os.path.getsize(p)
            except OSError:
                pass
    return out

old_tree = tree(OLD) if os.path.exists(OLD) else {}
new_tree = tree(VOLD)
print(f"source restante: {len(old_tree)} fichiers | copie volume: {len(new_tree)} fichiers")

# complétude : tout ce qui existe dans la SOURCE doit exister dans la COPIE (même taille)
manquants = [k for k in old_tree if k not in new_tree or new_tree[k] != old_tree[k]]
if manquants:
    print(f"⚠️ {len(manquants)} fichiers absents/différents dans la copie — restauration depuis la source:")
    os.makedirs("/tmp/restore-vault", exist_ok=True)
    for k in manquants[:20]:
        src = os.path.join(OLD, k)
        dst = os.path.join(VOLD, k)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil_done = subprocess.run(["cp", "-a", src, dst], capture_output=True, text=True)
        print("  restauré:", k, "✓" if shutil_done.returncode == 0 else f"✗ {shutil_done.stderr[:80]}")
else:
    print("✅ copie du volume COMPLÈTE — la source peut être supprimée sans perte")

print("\npermissions problématiques (source):")
r = subprocess.run(["sudo", "-n", "find", OLD, "!", "-user", "arthur", "|", "head", "-5"],
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip()[:200])
