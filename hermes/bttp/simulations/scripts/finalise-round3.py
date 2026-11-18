#!/usr/bin/env python3
"""Finalisation round 3 : README 138, re-test import, banc complet, push."""
import subprocess

p = "/srv/brandon-ai/workspaces/bttp/bttp/README.md"
src = open(p, encoding="utf-8").read()
if "(118 tests)" in src:
    src = src.replace("(118 tests)", "(138 tests)")
    open(p, "w", encoding="utf-8").write(src)
print("README: 138 tests ✓" if "(138 tests)" in src else "README: déjà à jour")

r = subprocess.run(["python3", "/srv/brandon-ai/workspaces/bttp/simulations/scripts/test-import-universel.py"],
                   capture_output=True, text=True, timeout=580)
print("import universel:", [l for l in r.stdout.splitlines() if "VERDICT" in l])

r = subprocess.run(["python3", "run_all_tests.py"], capture_output=True, text=True,
                   timeout=300, cwd="/srv/brandon-ai/workspaces/bttp/bttp")
for l in r.stdout.splitlines():
    if "Réussites" in l or "VERDICT" in l:
        print("banc:", l.strip())

r = subprocess.run(["python3", "/srv/brandon-ai/workspaces/scripts/push-bttp-v2.py"],
                   capture_output=True, text=True, timeout=580)
for l in r.stdout.splitlines():
    if "commit" in l or "poussés" in l:
        print("push:", l)
