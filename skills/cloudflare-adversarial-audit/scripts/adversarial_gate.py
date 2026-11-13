#!/usr/bin/env python3
"""Cloudflare-Style Adversarial Security Gate & False Positive Eliminator.

Enforces a 6-phase adversarial audit lifecycle where candidate vulnerabilities
MUST be challenged and verified by an independent skeptic agent before being accepted.
Validates the findings.json schema and generates clean REPORT.md documentation.
"""

import argparse
import json
from pathlib import Path
import sys
import time

REQUIRED_FIELDS = [
    "id",
    "file",
    "line",
    "severity",
    "description",
    "finder_agent",
    "adversarial_verifier",
    "falsification_attempt",
    "reproduced"
]

def validate_findings(data: list) -> tuple:
    valid = []
    rejected = []

    for item in data:
        missing = [f for f in REQUIRED_FIELDS if f not in item]
        if missing:
            rejected.append((item, f"Missing required fields: {', '.join(missing)}"))
            continue

        if not item.get("reproduced", False):
            rejected.append((item, "Finding not reproduced by adversarial verifier"))
            continue

        if item.get("finder_agent") == item.get("adversarial_verifier"):
            rejected.append((item, "Finder agent cannot be the same as adversarial verifier (violates independence rule)"))
            continue

        valid.append(item)

    return valid, rejected

def generate_report(valid_findings: list, out_path: Path) -> None:
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 🛡️ Adversarial Security Audit Report",
        f"**Generated at:** {now_str}",
        f"**Verified Vulnerabilities:** {len(valid_findings)}",
        "",
        "| ID | Severity | File & Line | Description | Verifier |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for vf in valid_findings:
        lines.append(f"| `{vf['id']}` | **{vf['severity'].upper()}** | `{vf['file']}:{vf['line']}` | {vf['description']} | `{vf['adversarial_verifier']}` |")

    lines.extend([
        "",
        "## Detailed Proof-of-Exploit & Falsification Attempts",
        ""
    ])

    for vf in valid_findings:
        lines.extend([
            f"### [{vf['id']}] {vf['description']}",
            f"- **Location:** `{vf['file']}:{vf['line']}`",
            f"- **Severity:** {vf['severity']}",
            f"- **Finder Agent:** `{vf['finder_agent']}`",
            f"- **Adversarial Verifier:** `{vf['adversarial_verifier']}`",
            f"- **Falsification Attempt:** {vf['falsification_attempt']}",
            ""
        ])

    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description="Cloudflare Adversarial Security Gate")
    parser.add_argument("--findings", "-f", default="findings.json", help="Path to input findings.json")
    parser.add_argument("--report", "-r", default="REPORT.md", help="Path to output REPORT.md")

    args = parser.parse_args()
    findings_file = Path(args.findings)

    if not findings_file.exists():
        print(f"Error: Findings file not found: {findings_file}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(findings_file.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            print("Error: findings.json must contain a JSON array of objects.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    valid, rejected = validate_findings(data)

    print(f"Adversarial Gate Audit Results:")
    print(f"  ✓ Verified findings : {len(valid)}")
    print(f"  ✗ Rejected (failed) : {len(rejected)}")

    if rejected:
        print("\n--- Rejected Candidates (Eliminated False Positives) ---")
        for item, reason in rejected:
            item_id = item.get("id", "UNKNOWN")
            print(f"  - [{item_id}]: {reason}")

    out_report = Path(args.report)
    generate_report(valid, out_report)
    print(f"\nFinal verified security report compiled to: {out_report}")

    if not valid and not rejected:
        sys.exit(0)
    elif rejected and not valid:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
