#!/usr/bin/env python3
"""Audit security of third-party AI agent skills before installation."""

import argparse
import os
import re
import sys
from pathlib import Path

# Sensitive paths and injection patterns
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior)\s+instructions", "Prompt Injection (instruction override)"),
    (r"disregard\s+(the\s+)?system\s+prompt", "Prompt Injection (system disregard)"),
    (r"you\s+are\s+now\s+in\s+developer\s+mode", "Jailbreak (developer mode)"),
    (r"<\s*system\s*>", "Prompt Injection (fake system tag)"),
    (r"\[\s*system\s*instruction\s*\]", "Prompt Injection (fake system instruction)"),
    (r"bypass\s+all\s+safety\s+filters", "Safety filter bypass attempt")
]

EXFILTRATION_PATTERNS = [
    (r"(os\.environ|process\.env)\b.*(fetch|post|requests|curl|urllib)", "Possible environment secret exfiltration"),
    (r"(id_rsa|id_ed25519|\.ssh|\.aws\/credentials|\.env)", "Attempt to reference sensitive credential paths"),
    (r"(eval\s*\(\s*base64|exec\s*\(\s*base64|eval\s*\(\s*b64decode)", "Obfuscated payload execution")
]

DANGEROUS_CALLS = [
    (r"\brm\s+-rf\s+[/~]", "Destructive filesystem command"),
    (r"chmod\s+777", "Insecure wide permission grant"),
    (r"curl\s+-[sS]*\s*http.*\|\s*(bash|sh)", "Remote pipe-to-shell execution")
]

def audit_skill(skill_dir: Path) -> dict:
    results = {
        "skill": skill_dir.name,
        "path": str(skill_dir),
        "verdict": "PASS",
        "findings": []
    }
    
    sk_file = skill_dir / "SKILL.md"
    if not sk_file.exists():
        results["verdict"] = "FAIL"
        results["findings"].append({"severity": "CRITICAL", "message": "Missing SKILL.md file"})
        return results

    # 1. Check SKILL.md
    try:
        content = sk_file.read_text(encoding="utf-8", errors="replace")
        for pat, desc in INJECTION_PATTERNS:
            if re.search(pat, content, re.IGNORECASE):
                results["verdict"] = "FAIL"
                results["findings"].append({"severity": "CRITICAL", "type": "PROMPT_INJECTION", "message": desc})
        
        for pat, desc in EXFILTRATION_PATTERNS:
            if re.search(pat, content, re.IGNORECASE):
                results["verdict"] = "FAIL"
                results["findings"].append({"severity": "CRITICAL", "type": "DATA_EXFILTRATION", "message": desc})
    except Exception as e:
        results["findings"].append({"severity": "WARN", "message": f"Error reading SKILL.md: {e}"})

    # 2. Check all script files
    for root, _, files in os.walk(skill_dir):
        for f in files:
            if f == "audit_skill_security.py":
                continue
            if f.endswith((".py", ".sh", ".bash", ".js", ".ts", ".ps1")):
                p = Path(root) / f
                try:
                    txt = p.read_text(encoding="utf-8", errors="replace")
                    for pat, desc in EXFILTRATION_PATTERNS:
                        if re.search(pat, txt, re.IGNORECASE):
                            results["verdict"] = "FAIL"
                            results["findings"].append({"severity": "CRITICAL", "file": str(p.relative_to(skill_dir)), "message": desc})
                    for pat, desc in DANGEROUS_CALLS:
                        if re.search(pat, txt, re.IGNORECASE):
                            if results["verdict"] != "FAIL":
                                results["verdict"] = "WARN"
                            results["findings"].append({"severity": "HIGH", "file": str(p.relative_to(skill_dir)), "message": desc})
                except Exception:
                    pass

    return results

def main():
    parser = argparse.ArgumentParser(description="Skill Security Auditor")
    parser.add_argument("target", help="Path to skill directory or skills root directory")
    parser.add_argument("--all", action="store_true", help="Audit all subdirectories in target")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"Error: Target path {target_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    targets = []
    if args.all:
        targets = [d for d in target_path.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    else:
        targets = [target_path]

    print(f"=== Auditing {len(targets)} skill(s) for security ===")
    total_pass = 0
    total_warn = 0
    total_fail = 0

    for t in targets:
        res = audit_skill(t)
        verdict = res["verdict"]
        if verdict == "PASS":
            total_pass += 1
            status_str = "[PASS]"
        elif verdict == "WARN":
            total_warn += 1
            status_str = "[WARN]"
        else:
            total_fail += 1
            status_str = "[FAIL]"

        print(f"{status_str} {res['skill']}")
        for item in res["findings"]:
            loc = f" ({item['file']})" if "file" in item else ""
            print(f"   ! [{item['severity']}] {item['message']}{loc}")

    print("\n=== Audit Summary ===")
    print(f"Total: {len(targets)} | PASS: {total_pass} | WARN: {total_warn} | FAIL: {total_fail}")

    if total_fail > 0:
        sys.exit(2)
    elif total_warn > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
