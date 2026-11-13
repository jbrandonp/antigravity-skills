#!/usr/bin/env python3
"""ECC AgentShield & Continuous Learning Instinct Engine.

1. audit-cmd: Intercepts destructive shell commands before execution.
2. learn-instinct: Compiles debugging lessons into persistent Markdown instinct rules.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DESTRUCTIVE_PATTERNS = [
    (r'\brm\s+-(?:r|f|rf|fr)\s+(?:/|~|\$HOME|\.\.)', "Destructive recursive deletion of root or home directory"),
    (r'\b(?:drop\s+database|truncate\s+table)\b', "Direct destructive SQL database drop/truncate"),
    (r'\bchmod\s+-R\s+777\s+/', "Unsafe permissive permissions on system root"),
    (r'\bcurl\b.*\|\s*(?:bash|sh)\b', "Unverified piping of remote web curl output directly into shell"),
    (r'\bgit\s+push\s+.*--force\b', "Destructive force-push overwriting remote git history"),
    (r'>\s*/dev/sd[a-z]', "Direct disk block overwriting"),
]

def audit_command(cmd_str: str) -> dict:
    for pat, desc in DESTRUCTIVE_PATTERNS:
        if re.search(pat, cmd_str, re.IGNORECASE):
            return {
                "safe": False,
                "reason": desc,
                "pattern": pat
            }
    return {"safe": True, "reason": "Command passed safety verification"}

def learn_instinct(title: str, trigger: str, rule: str, vault_dir: Path = None):
    instinct_dir = (vault_dir or Path(".agent/instincts"))
    instinct_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r'[^a-zA-Z0-9_\-]', '_', title.lower()).strip('_')
    file_path = instinct_dir / f"instinct_{slug}.md"

    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""---
title: "{title}"
type: agent-instinct
trigger: "{trigger}"
created_at: "{now_iso}"
status: active
---

# 🧠 Instinct: {title}

## ⚡ Trigger / Symptôme
> `{trigger}`

## 🛡️ Règle Déterministe Apprise
{rule}

## 🔍 Validation Déterministe
1. Vérifier si ce symptôme est présent avant d'exécuter la tâche.
2. Appliquer immédiatement la règle sans passer par un cycle d'essai-erreur.
"""
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"✓ Persistent instinct saved: {file_path.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="ECC AgentShield & Continuous Learning Engine")
    subparsers = parser.add_subparsers(dest="action", help="Action mode")

    audit_p = subparsers.add_parser("audit-cmd", help="Audit shell command for destructive patterns")
    audit_p.add_argument("--cmd", required=True, help="Shell command string to verify")

    learn_p = subparsers.add_parser("learn-instinct", help="Compile lesson into persistent instinct rule")
    learn_p.add_argument("--title", required=True, help="Short descriptive title of the learned behavior")
    learn_p.add_argument("--trigger", required=True, help="Error message, symptom, or scenario trigger")
    learn_p.add_argument("--rule", required=True, help="Actionable rule to apply permanently")

    args = parser.parse_args()

    if args.action == "audit-cmd":
        res = audit_command(args.cmd)
        if not res["safe"]:
            print(f"[BLOCKED] Destructive command detected!")
            print(f"Reason: {res['reason']}")
            sys.exit(1)
        else:
            print("✓ PASS: Command passed safety gate.")
    elif args.action == "learn-instinct":
        learn_instinct(args.title, args.trigger, args.rule)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
