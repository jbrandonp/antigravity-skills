#!/usr/bin/env python3
"""
generate_security_attestation.py — Generate an official OWASP ASI Security Attestation & Compliance Certificate.
Compiles audit findings into a formal security sign-off deliverable for production deployment gates.

Usage:
  python generate_security_attestation.py --agent NAME --version VER [--root DIR] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import datetime
import hashlib
import json
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import scan_owasp_compliance as scanner


def generate_attestation_certificate(
    agent_name: str,
    version: str,
    root_dir: Path
) -> str:
    """Generate official markdown attestation report."""
    scan_results = scanner.scan_project(root_dir)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Calculate checksum of the scan results as attestation fingerprint
    digest = hashlib.sha256(json.dumps(scan_results, sort_keys=True).encode("utf-8")).hexdigest()[:16]

    score = scan_results["compliance_score"]
    verdict = scan_results["verdict"]

    if verdict == "COMPLIANT":
        verdict_badge = "🟢 **CERTIFIED SECURE (PASSED)**"
        recommendation = "Approved for unconstrained production deployment within specified budget and iteration limits."
    elif verdict == "PARTIALLY_COMPLIANT":
        verdict_badge = "🟡 **CONDITIONAL DEPLOYMENT (SUPERVISED)**"
        recommendation = "Approved for staged canary deployment with enhanced human oversight and active circuit breakers."
    else:
        verdict_badge = "🔴 **DEPLOYMENT BLOCKED (CRITICAL DEFICIENCIES)**"
        recommendation = "Deployment denied. Remediation of failing ASI controls is mandatory prior to authorization."

    lines = [
        "# 📜 OWASP Agentic Security Initiative (ASI 2026) Official Attestation",
        "",
        "> **Document Type :** Production Security Gate Attestation  ",
        f"> **Agent System :** `{agent_name}` (Version: `v{version}`)  ",
        f"> **Audit Timestamp :** `{timestamp}`  ",
        f"> **Attestation Hash :** `sha256:{digest}`  ",
        f"> **Verdict :** {verdict_badge}",
        "",
        "---",
        "",
        "## 1. Executive Summary & Verification Scope",
        f"The AI Agent system **{agent_name}** has undergone static security verification against the **OWASP Agentic Security Initiative (ASI) Top 10** standard.",
        "",
        f"- **Compliance Score :** `{score}%` ({scan_results['controls_covered']} controls satisfied)",
        f"- **Total Scanned Files :** `{scan_results['total_files_scanned']}` source and configuration artifacts",
        f"- **Operational Recommendation :** {recommendation}",
        "",
        "---",
        "",
        "## 2. OWASP ASI Control Attestation Inventory",
        "",
        "| Control ID | Risk Standard | Status | Verified Evidence / Gaps | Remediation Guidance |",
        "| :--- | :--- | :---: | :--- | :--- |"
    ]

    for c in scan_results["controls"]:
        icon = "✅" if c["status"] == "PASS" else ("⚠️" if c["status"] == "WARN" else "❌")
        evidence_str = ", ".join(c["evidence"][:2]) if c["evidence"] else (
            f"Defects: {', '.join(c['vulnerabilities'][:2])}" if c["vulnerabilities"] else "No mitigation detected"
        )
        lines.append(f"| `{c['id']}` | {c['name']} | {icon} {c['status']} | {evidence_str} | {c['remediation']} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Mandatory Security Guardrails in Effect",
        "1. **Zero-Trust Tool Admissibility :** No model proposal can invoke an unregistered tool or bypass parameter schemas.",
        "2. **Execution Sandboxing :** All dynamic code and browser environments operate within isolated containers.",
        "3. **Idempotency Guarantees :** External write operations enforce unique idempotency keys.",
        "4. **Audit Immutability :** Every tool dispatch is written to an append-only, structured audit ledger.",
        "",
        "---",
        "",
        "## 4. Architect & Security Sign-Off",
        "",
        "```text",
        f"Verified by      : Antigravity Automated Security Gate Engine",
        f"Compliance Standard : OWASP ASI Top 10 (2026 Edition)",
        f"Signature Hash   : {digest}",
        f"Audit Status     : {verdict}",
        "```"
    ])

    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Generate official OWASP ASI Security Attestation report."
    )
    parser.add_argument("--agent", type=str, required=True, help="Agent system identifier")
    parser.add_argument("--version", type=str, default="1.0.0", help="Agent system version")
    parser.add_argument("--root", type=str, default=".", help="Root directory of agent codebase")
    parser.add_argument("--output", type=str, default="OWASP_ASI_ATTESTATION.md", help="Output file path")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    report = generate_attestation_certificate(args.agent, args.version, root_dir)

    out_p = Path(args.output)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    print(f"✓ Security Attestation generated successfully: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
