#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_audit_weekly.py — Cron hebdomadaire d'audit sécurité (lundi 8h)
Lance security_audit.py sur les repos principaux de Brandon, imprime le
résumé compact (stdout = message délivré, pattern watchdog no_agent).
"""
import os
import subprocess

PY = r"C:\Users\brand\AppData\Local\Programs\Python\Python312\python.exe"
SCRIPT = os.path.expanduser("~/.hermes/scripts/security_audit.py")
REPOS = [
    (r"C:\Users\brand\havok-toolbox", "havok-toolbox"),
    (r"C:\Users\brand\tda-longevity-resilience", "tda-longevity"),
    (r"C:\Users\brand\giga-office", "giga-office"),
    (r"C:\Users\brand\havok-toolbox\havolib", "havolib (source)"),
]

env = {**os.environ, "PYTHONPATH": ""}
outputs = []
for repo, label in REPOS:
    if not os.path.isdir(repo):
        continue
    out_file = os.path.join(os.path.expanduser("~/.hermes/security-tools/reports"),
                            f"weekly-{label.replace(' ', '-')}-{__import__('datetime').date.today()}.md")
    try:
        p = subprocess.run(
            [PY, SCRIPT, repo, "--cron", "--output", out_file],
            capture_output=True, text=True, timeout=1500, errors="replace", env=env,
        )
        text = (p.stdout or p.stderr or "").strip()
        outputs.append((label, text, p.returncode))
    except subprocess.TimeoutExpired:
        outputs.append((label, "TIMEOUT >25min", 124))

print("🛡️ AUDIT SÉCURITÉ HEBDOMADAIRE — repos principaux")
issues = 0
for label, text, rc in outputs:
    lines = text.splitlines()
    head = lines[0] if lines else "pas de sortie"
    n_red = text.count("🔴")
    flag = "🔴" if rc != 0 or n_red else "🟢"
    if rc != 0 or n_red:
        issues += 1
    print(f"\n{flag} {label}")
    for line in lines[1:6]:
        print("  " + line)

print(f"\n{'⚠️ ' + str(issues) + ' repo(s) avec findings — voir les rapports dans ~/.hermes/security-tools/reports/' if issues else '✅ Aucun finding bloquant sur les repos audités'}")
