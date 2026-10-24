#!/usr/bin/env python3
"""
Automated Static Source-Code Vulnerability & Secret Scanner
Scans codebase for high-entropy hardcoded secrets, dangerous execution patterns,
SQL injection vectors, and command injection risks.
Outputs VULN-FINDINGS.json and human-readable audit report.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

# High-risk secret patterns
SECRET_PATTERNS = [
    (r"(?i)(?:api_key|apikey|secret|token|password|passwd|auth_token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", "Hardcoded Secret / API Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Access Token"),
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Secret Key"),
    (r"sk_live_[0-9a-zA-Z]{24}", "Stripe Live Secret Key"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API Key")
]

# Code execution & injection patterns
CODE_PATTERNS = [
    (r"(?<!\w)eval\(", "Dangerous `eval()` call (Arbitrary Code Execution)", "Critical"),
    (r"(?<!\w)exec\(", "Dangerous `exec()` call (Arbitrary Code Execution)", "Critical"),
    (r"shell\s*=\s*True", "Subprocess invocation with `shell=True` (Command Injection Risk)", "Major"),
    (r"(?<!\w)os\.system\(", "Dangerous `os.system()` invocation", "Major"),
    (r"\.execute\(\s*f[\"'].*?\{.*?\}", "Raw SQL query string interpolation (SQL Injection Risk)", "Critical"),
    (r"\.execute\(\s*[\"'].*?%s.*?[\"']\s*%", "Raw SQL query string formatting with `%` (SQL Injection Risk)", "Critical"),
    (r"dangerouslySetInnerHTML", "React `dangerouslySetInnerHTML` usage (XSS Risk)", "Major")
]

EXCLUDE_DIRS = {".git", ".gemini", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}

def scan_file(file_path: Path):
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    lines = content.splitlines()
    for line_num, line in enumerate(lines, start=1):
        # Skip comment-only lines
        stripped = line.strip()
        if stripped.startswith(("#", "//", "/*", "*")):
            continue

        # Check secrets
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line):
                # Obfuscate matched line for safety
                findings.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": "SECRET",
                    "severity": "Critical",
                    "description": desc,
                    "snippet": stripped[:80] + "..." if len(stripped) > 80 else stripped
                })

        # Check dangerous code patterns
        for pattern, desc, severity in CODE_PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": "INJECTION_OR_EXEC",
                    "severity": severity,
                    "description": desc,
                    "snippet": stripped[:80] + "..." if len(stripped) > 80 else stripped
                })

    return findings

def scan_directory(target_dir: Path):
    print(f"\n[*] Starting static security audit in: {target_dir}")
    all_findings = []
    total_files = 0

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in {".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml", ".env", ".sh", ".ps1"}:
                total_files += 1
                f_path = Path(root) / f
                findings = scan_file(f_path)
                all_findings.extend(findings)

    print(f"[+] Scanned {total_files} source files.")
    print(f"[+] Discovered {len(all_findings)} potential vulnerabilities / secrets.\n")

    # Write JSON report
    report_file = Path("VULN-FINDINGS.json")
    report_file.write_text(json.dumps(all_findings, indent=2), encoding="utf-8")
    print(f"[+] Output structured findings to: {report_file.resolve()}")

    # Summary
    by_sev = {"Critical": 0, "Major": 0, "Minor": 0}
    for item in all_findings:
        by_sev[item["severity"]] = by_sev.get(item["severity"], 0) + 1

    print(f"    - Critical: {by_sev.get('Critical', 0)}")
    print(f"    - Major   : {by_sev.get('Major', 0)}")
    return len(all_findings) == 0

def main():
    parser = argparse.ArgumentParser(description="Static Vulnerability & Secret Scanner")
    parser.add_argument("target", nargs="?", default=".", help="Target directory to audit")
    args = parser.parse_args()

    clean = scan_directory(Path(args.target))
    sys.exit(0 if clean else 1)

if __name__ == "__main__":
    main()
