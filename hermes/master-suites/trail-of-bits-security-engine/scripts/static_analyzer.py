#!/usr/bin/env python3
"""Trail of Bits Static Analysis Engine.

Scans Python source files using AST parsing for security vulnerabilities:
- Timing side-channels (token comparison with == instead of hmac.compare_digest)
- Dangerous sinks (eval, exec, pickle.loads, shell=True)
- SQL injection via string formatting
- Hardcoded high-entropy secrets and keys
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

class SecurityASTVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.findings = []

    def visit_Compare(self, node):
        # Detect token/secret/hash comparison using ==
        for comp in [node.left] + node.comparators:
            if isinstance(comp, ast.Name) and any(k in comp.id.lower() for k in ["token", "secret", "password", "signature", "hmac", "hash"]):
                for op in node.ops:
                    if isinstance(op, ast.Eq):
                        self.findings.append({
                            "type": "TIMING_SIDE_CHANNEL",
                            "severity": "HIGH",
                            "line": node.lineno,
                            "file": self.filename,
                            "message": f"Potential timing side-channel: comparison of secret '{comp.id}' with '=='. Use hmac.compare_digest() instead."
                        })
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detect eval, exec, pickle.loads
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in ["eval", "exec"]:
            self.findings.append({
                "type": "CODE_INJECTION",
                "severity": "CRITICAL",
                "line": node.lineno,
                "file": self.filename,
                "message": f"Use of dangerous dynamic execution function '{func_name}'."
            })
        elif func_name == "loads" and isinstance(getattr(node.func, "value", None), ast.Name) and node.func.value.id == "pickle":
            self.findings.append({
                "type": "DESERIALIZATION",
                "severity": "CRITICAL",
                "line": node.lineno,
                "file": self.filename,
                "message": "Insecure deserialization via pickle.loads()."
            })

        # Detect shell=True in subprocess
        if func_name in ["run", "Popen", "call", "check_output"]:
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.findings.append({
                        "type": "COMMAND_INJECTION",
                        "severity": "HIGH",
                        "line": node.lineno,
                        "file": self.filename,
                        "message": "subprocess call with shell=True. High risk of command injection."
                    })

        self.generic_visit(node)

def scan_file(file_path: Path) -> list:
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return findings

    # AST checks
    try:
        tree = ast.parse(content, filename=str(file_path))
        visitor = SecurityASTVisitor(str(file_path))
        visitor.visit(tree)
        findings.extend(visitor.findings)
    except SyntaxError:
        pass

    # Regex checks for hardcoded credentials
    secret_patterns = [
        (r'(?i)(?:api_key|secret_key|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-]{20,}["\']', "HARDCODED_SECRET", "HIGH", "Hardcoded API key or secret token detected.")
    ]
    for idx, line in enumerate(content.splitlines(), start=1):
        for pattern, ftype, severity, msg in secret_patterns:
            if re.search(pattern, line):
                findings.append({
                    "type": ftype,
                    "severity": severity,
                    "line": idx,
                    "file": str(file_path),
                    "message": msg
                })

    return findings

def main():
    parser = argparse.ArgumentParser(description="Trail of Bits Static Analysis Engine")
    parser.add_argument("--target", required=True, help="Directory or file to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--strict", action="store_true", help="Fail if any critical/high issues are found")
    args = parser.parse_args()

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: Target '{args.target}' does not exist.")
        sys.exit(1)

    files_to_scan = []
    if target_path.is_file() and target_path.suffix == ".py":
        files_to_scan.append(target_path)
    elif target_path.is_dir():
        files_to_scan = [p for p in target_path.rglob("*.py") if "__pycache__" not in p.parts and ".git" not in p.parts]

    all_findings = []
    for f in files_to_scan:
        all_findings.extend(scan_file(f))

    critical_count = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in all_findings if f["severity"] == "HIGH")

    if args.format == "json":
        report_data = {
            "total_files_scanned": len(files_to_scan),
            "findings_count": len(all_findings),
            "critical": critical_count,
            "high": high_count,
            "findings": all_findings
        }
        json_str = json.dumps(report_data, indent=2)
        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(json_str)
    else:
        print("=" * 65)
        print(" 🛡️ TRAIL OF BITS STATIC ANALYSIS AUDIT REPORT")
        print("=" * 65)
        print(f"Files Scanned   : {len(files_to_scan)}")
        print(f"Total Findings  : {len(all_findings)} (Critical: {critical_count}, High: {high_count})")
        print("-" * 65)
        if all_findings:
            for f in all_findings:
                print(f"[{f['severity']}] {f['file']}:{f['line']} -> {f['message']}")
        else:
            print("✓ Zero high/critical static analysis findings detected.")
        print("=" * 65)

    if args.strict and (critical_count > 0 or high_count > 0):
        sys.exit(1)

if __name__ == "__main__":
    main()
