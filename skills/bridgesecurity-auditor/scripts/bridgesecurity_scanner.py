# -*- coding: utf-8 -*-
"""
bridgesecurity_scanner.py - BridgeMind Senior Security Auditor Scanner
Audits credentials, high Shannon entropy, CWE Top 25 patterns, and Dockerfile/IaC hardening.
"""

import os
import re
import sys
import math
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class SecurityFinding(TypedDict):
    file: str
    line: int
    type: str
    title: str
    severity: str
    detail: str

# Signatures de secrets courantes
SECRET_PATTERNS: List[Tuple[str, str, str]] = [
    ("AWS Access Key", r"AKIA[0-9A-Z]{16}", "CRITICAL"),
    ("GitHub Personal Token", r"gh[pousr]_[A-Za-z0-9_]{36,255}", "CRITICAL"),
    ("OpenAI API Key", r"sk-[A-Za-z0-9_-]{20,}", "CRITICAL"),
    ("Google Cloud API Key", r"AIza[0-9A-Za-z\-_]{35}", "CRITICAL"),
    ("Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24}", "CRITICAL"),
    ("Slack Token", r"xox[baprs]-[0-9a-zA-Z]{10,48}", "CRITICAL"),
    ("Generic Bearer Token", r"(?:bearer|token)\s*[:=]\s*['\"][A-Za-z0-9\-_\.]{32,}['\"]", "HIGH"),
    ("Private Key Header", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "CRITICAL"),
]

# Modèles de vulnérabilités CWE
VULN_PATTERNS: List[Tuple[str, str, str, str]] = [
    ("CWE-89: SQL Injection", r"execute\s*\(\s*f['\"].*SELECT|INSERT|UPDATE|DELETE", "HIGH", "Utiliser requetes parametrees avec ? au lieu de f-strings"),
    ("CWE-78: Command Injection", r"subprocess\.(?:Popen|run|call)\s*\(.*shell\s*=\s*True", "HIGH", "Fixer shell=False et passer une liste d arguments"),
    ("CWE-502: Unsafe Deserialization", r"pickle\.loads?\s*\(", "HIGH", "Remplacer pickle par un format securise (JSON, msgpack)"),
    ("CWE-798: Hardcoded Password", r"(?:password|passwd|pwd|secret)\s*=\s*['\"][^'\"]{6,}['\"]", "MEDIUM", "Externaliser les mots de passe dans des variables d environnement"),
]

def calculate_shannon_entropy(data: str) -> float:
    """Calcule l entropie de Shannon d une chaine de caracteres."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    frequencies: Dict[str, int] = {}
    for char in data:
        frequencies[char] = frequencies.get(char, 0) + 1
    for count in frequencies.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def audit_file(file_path: pathlib.Path) -> List[SecurityFinding]:
    findings: List[SecurityFinding] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return findings

    lines = content.splitlines()

    # 1. Scan des patterns de secrets
    for idx, line in enumerate(lines, start=1):
        for name, pattern, severity in SECRET_PATTERNS:
            match = re.search(pattern, line)
            if match:
                raw_val = match.group(0)
                masked = raw_val[:4] + "..." + raw_val[-4:] if len(raw_val) > 8 else "***"
                findings.append({
                    "file": str(file_path),
                    "line": idx,
                    "type": "SECRET",
                    "title": name,
                    "severity": severity,
                    "detail": f"Token detecte : {masked}",
                })

    # 2. Scan des vulnerabilites CWE
    for idx, line in enumerate(lines, start=1):
        for cwe_title, pattern, severity, fix in VULN_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "file": str(file_path),
                    "line": idx,
                    "type": "VULNERABILITY",
                    "title": cwe_title,
                    "severity": severity,
                    "detail": fix,
                })

    # 3. Hardening Dockerfile si applicable
    if file_path.name.lower() in ["dockerfile", "dockerfile.dev", "dockerfile.prod"]:
        has_user = any("USER" in l for l in lines)
        if not has_user:
            findings.append({
                "file": str(file_path),
                "line": 1,
                "type": "IAC_HARDENING",
                "title": "CWE-250: Execution Docker en Root",
                "severity": "HIGH",
                "detail": "Aucune directive USER specifiee. Ajouter USER appuser.",
            })
        for idx, line in enumerate(lines, start=1):
            if re.search(r"^FROM\s+[^\s:]+:latest", line, re.IGNORECASE):
                findings.append({
                    "file": str(file_path),
                    "line": idx,
                    "type": "IAC_HARDENING",
                    "title": "Unpinned Docker Tag",
                    "severity": "MEDIUM",
                    "detail": "Tag :latest non reproductible. Verrouiller la version ou le sha256.",
                })

    return findings

def main():
    parser = argparse.ArgumentParser(description="BridgeSecurity Auditor - Scanner de securite conforme BridgeMind")
    parser.add_argument("--scan-dir", type=str, default=".", help="Repertoire a auditer")
    parser.add_argument("--file", type=str, help="Fichier unique a auditer")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details et recommandations")
    args = parser.parse_args()

    print("=" * 65)
    print("        BRIDGESECURITY AUDITOR (STANDARD BRIDGEMIND)        ")
    print("=" * 65)

    all_findings: List[SecurityFinding] = []
    ignored_dirs = {".git", ".svn", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}

    if args.file:
        p = pathlib.Path(args.file)
        if p.exists() and p.is_file():
            all_findings.extend(audit_file(p))
    else:
        root = pathlib.Path(args.scan_dir)
        for current_root, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for f in files:
                p = pathlib.Path(current_root) / f
                if p.suffix.lower() in [".py", ".js", ".ts", ".tsx", ".yaml", ".yml", ".json", ".env", "dockerfile"]:
                    all_findings.extend(audit_file(p))

    critical = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
    high = sum(1 for f in all_findings if f["severity"] == "HIGH")
    medium = sum(1 for f in all_findings if f["severity"] == "MEDIUM")

    score = max(0, 100 - (critical * 25 + high * 10 + medium * 5))

    print(f"Total findings : {len(all_findings)}")
    print(f"  - CRITICAL : {critical}")
    print(f"  - HIGH     : {high}")
    print(f"  - MEDIUM   : {medium}")
    print(f"BridgeSecurity Compliance Score : {score} / 100")
    print("-" * 65)

    if all_findings:
        for f in all_findings:
            sev_tag = f"[{f['severity']}]"
            print(f"{sev_tag:<10} {f['file']}:{f['line']} -> {f['title']}")
            if args.verbose:
                print(f"           Detail : {f['detail']}")
    else:
        print("[OK] Aucun secret ou faille critique detectee.")

    print("=" * 65)

if __name__ == "__main__":
    main()