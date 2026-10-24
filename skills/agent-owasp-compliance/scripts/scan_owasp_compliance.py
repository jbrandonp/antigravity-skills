#!/usr/bin/env python3
"""
scan_owasp_compliance.py — Automated static scanner for OWASP Agentic Security Initiative (ASI) Top 10.
Audits AI Agent codebases, configurations, and architecture specifications for the 10 agentic risks.

Usage:
  python scan_owasp_compliance.py [--root DIR] [--json] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next",
    "__pycache__", ".venv", "venv", ".tox", "target", "vendor",
    "coverage", ".cache", "bin", "obj", "Intermediate", "Saved"
}

ASI_CONTROLS = [
    {
        "id": "ASI-01",
        "name": "Prompt Injection Protection",
        "description": "User input must be validated before reaching tool execution, not just output filtering.",
        "positives": [
            r"input_validation", r"validate_input", r"sanitize",
            r"prompt_injection", r"threat_detect", r"policy_engine",
            r"check_content", r"ingress_guard"
        ],
        "negatives": [
            r"eval\(", r"exec\(", r"subprocess\.(?:run|Popen)\(.*shell\s*=\s*True",
            r"os\.system\("
        ],
        "remediation": "Deploy programmatic input sanitization and delimiter guards before dispatching tool calls."
    },
    {
        "id": "ASI-02",
        "name": "Insecure Tool Use",
        "description": "Tools must enforce explicit allowlists, typed argument validation, and no arbitrary shell execution.",
        "positives": [
            r"allowed_tools", r"tool_allowlist", r"validate_args",
            r"pydantic", r"tool_registry", r"authorized_tools"
        ],
        "negatives": [
            r"getattr\(.*tools.*\)", r"shell\s*=\s*True", r"shutil\.rmtree\(.*user",
            r"tool_name\s*==\s*[\"']\*[\"']"
        ],
        "remediation": "Restrict agent tools to an explicit allowlist and validate all arguments against strict Pydantic/JSON schemas."
    },
    {
        "id": "ASI-03",
        "name": "Excessive Agency",
        "description": "Agent capabilities must be strictly scoped to the principle of least privilege.",
        "positives": [
            r"capability_boundary", r"execution_ring", r"max_steps",
            r"rate_limit", r"least_privilege", r"scope_limit", r"budget"
        ],
        "negatives": [
            r"unlimited_steps", r"all_permissions", r"admin_override_default"
        ],
        "remediation": "Confine agent authority with hard step caps, execution rings, and resource budgets."
    },
    {
        "id": "ASI-04",
        "name": "Unauthorized Escalation",
        "description": "Agents must not be capable of modifying their own privileges, roles, or trust scores.",
        "positives": [
            r"require_approval", r"sre_attestation", r"out_of_band",
            r"escalation_gate", r"human_in_the_loop", r"permission_check"
        ],
        "negatives": [
            r"self\.trust_score\s*=", r"set_role\(.*admin", r"promote_self\("
        ],
        "remediation": "Require external out-of-band attestation or human approval for privilege elevation."
    },
    {
        "id": "ASI-05",
        "name": "Trust Boundary Violation",
        "description": "Inter-agent messages must be cryptographically verified; no blind trust in multi-agent swarms.",
        "positives": [
            r"verify_signature", r"trust_registry", r"signed_token",
            r"did:key", r"did:web", r"delegation_narrowing", r"mtls"
        ],
        "negatives": [
            r"trust_all_agents", r"skip_auth_internal", r"accept_unverified"
        ],
        "remediation": "Verify cryptographic signatures and enforce delegation narrowing on all inter-agent messages."
    },
    {
        "id": "ASI-06",
        "name": "Insufficient Logging & Audit Trail",
        "description": "All tool calls and state mutations must be recorded in structured, tamper-evident logs.",
        "positives": [
            r"audit_log", r"hash_chain", r"tamper_evident",
            r"structlog", r"audit_trail", r"jsonl_logger", r"step_log"
        ],
        "negatives": [
            r"logging\.disable", r"pass\s*#\s*no logging"
        ],
        "remediation": "Maintain structured JSONL audit trails with execution timestamps, tool parameters, and hash chaining."
    },
    {
        "id": "ASI-07",
        "name": "Insecure Identity Management",
        "description": "Agents must possess unique cryptographic credentials, not just plain string identifiers.",
        "positives": [
            r"ed25519", r"cryptographic_identity", r"did", r"keypair",
            r"jwk", r"agent_cert", r"public_key"
        ],
        "negatives": [
            r"agent_name\s*=\s*[\"'][a-zA-Z0-9_\-]+[\"']\s*#\s*only id"
        ],
        "remediation": "Bind agent permissions to cryptographic keypairs (Ed25519/DIDs) rather than arbitrary name strings."
    },
    {
        "id": "ASI-08",
        "name": "Policy Bypass (Deterministic Enforcement)",
        "description": "Security policy evaluation must be deterministic code/rules, never delegated to LLM prompts.",
        "positives": [
            r"policy_evaluator", r"policy_engine", r"deterministic_check",
            r"rule_engine", r"pre_execution_gate"
        ],
        "negatives": [
            r"ask_llm_if_allowed", r"prompt_permission_check", r"model decides if allowed"
        ],
        "remediation": "Enforce policies with deterministic sub-millisecond code checks; never prompt the model to self-police."
    },
    {
        "id": "ASI-09",
        "name": "Supply Chain & Plugin Integrity",
        "description": "Third-party tools and dependencies must verify cryptographic integrity and hash manifests.",
        "positives": [
            r"integrity\.json", r"sbom", r"package-lock\.json",
            r"poetry\.lock", r"pipfile\.lock", r"sha256", r"pinned_version"
        ],
        "negatives": [
            r"version\s*=\s*[\"']\*[\"']", r"latest", r"curl.*\|\s*sh"
        ],
        "remediation": "Pin all dependencies with cryptographic lockfiles and verify tool plugin checksums."
    },
    {
        "id": "ASI-10",
        "name": "Behavioral Anomaly & Kill Switch",
        "description": "The system must support automated circuit breakers, drift detection, and an emergency stop.",
        "positives": [
            r"circuit_breaker", r"kill_switch", r"emergency_stop",
            r"drift_detect", r"watchdog", r"timeout"
        ],
        "negatives": [
            r"while\s+True:\s*#\s*no break", r"ignore_errors\s*=\s*True"
        ],
        "remediation": "Implement an automated circuit breaker that trips after repeated faults, paired with an emergency kill switch."
    }
]


def scan_project(root_dir: Path) -> dict:
    """Scan all source and configuration files in root_dir against the 10 ASI controls."""
    files_to_scan = []
    supported_exts = {".py", ".ts", ".js", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".md", ".toml"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            p = Path(root) / f
            if p.suffix in supported_exts and not p.name.endswith(('.min.js', '.min.css')):
                files_to_scan.append(p)

    results = []
    covered_controls = 0

    for ctrl in ASI_CONTROLS:
        positive_evidence = []
        negative_findings = []

        for fpath in files_to_scan:
            try:
                content = fpath.read_text(encoding="utf-8", errors="ignore")
                rel_p = str(fpath.relative_to(root_dir)).replace('/', os.sep)

                # Check positives
                for pat in ctrl["positives"]:
                    matches = re.findall(pat, content, re.IGNORECASE)
                    if matches:
                        positive_evidence.append(f"{rel_p} ({matches[0]})")
                        break

                # Check negatives
                for npat in ctrl["negatives"]:
                    matches = re.findall(npat, content, re.IGNORECASE)
                    if matches:
                        negative_findings.append(f"{rel_p} (found pattern: `{matches[0]}`)")
            except Exception:
                pass

        has_positives = len(positive_evidence) > 0
        has_negatives = len(negative_findings) > 0

        if has_positives and not has_negatives:
            status = "PASS"
            covered_controls += 1
        elif has_positives and has_negatives:
            status = "WARN"
            covered_controls += 0.5
        else:
            status = "FAIL"

        results.append({
            "id": ctrl["id"],
            "name": ctrl["name"],
            "description": ctrl["description"],
            "status": status,
            "evidence": positive_evidence[:5],
            "vulnerabilities": negative_findings[:5],
            "remediation": ctrl["remediation"]
        })

    compliance_score = round((covered_controls / len(ASI_CONTROLS)) * 100, 1)

    if compliance_score >= 80:
        verdict = "COMPLIANT"
    elif compliance_score >= 50:
        verdict = "PARTIALLY_COMPLIANT"
    else:
        verdict = "NON_COMPLIANT"

    return {
        "root_directory": str(root_dir),
        "total_files_scanned": len(files_to_scan),
        "compliance_score": compliance_score,
        "controls_covered": f"{int(covered_controls)}/{len(ASI_CONTROLS)}",
        "verdict": verdict,
        "controls": results
    }


def format_markdown_report(summary: dict) -> str:
    """Format compliance scan results as clean Markdown."""
    lines = [
        "# 🛡️ OWASP Agentic Security Initiative (ASI) Top 10 Audit Report",
        "",
        "## 📊 Executive Posture",
        f"- **Audited Path :** `{summary['root_directory']}` ({summary['total_files_scanned']} files scanned)",
        f"- **ASI Compliance Score :** `{summary['compliance_score']}%` ({summary['controls_covered']} controls addressed)",
        f"- **Security Posture Verdict :** **{summary['verdict']}**",
        "",
        "## 📋 Control Matrix (ASI-01 through ASI-10)",
        "| Control ID | Risk Name | Status | Evidence / Gap | Required Remediation |",
        "| :--- | :--- | :---: | :--- | :--- |"
    ]

    for c in summary["controls"]:
        icon = "✅" if c["status"] == "PASS" else ("⚠️" if c["status"] == "WARN" else "🚨")
        evidence_str = f"Found in {len(c['evidence'])} files" if c["status"] == "PASS" else (
            f"Vulnerabilities in: {', '.join(c['vulnerabilities'][:2])}" if c["vulnerabilities"] else "No controls detected"
        )
        lines.append(f"| `{c['id']}` | {c['name']} | {icon} **{c['status']}** | {evidence_str} | {c['remediation']} |")

    lines.extend([
        "",
        "## 🚨 Immediate Action Items",
        "1. Prioritize all `FAIL` and `WARN` controls before production agent deployment.",
        "2. Ensure runtime enforcement wraps tool calls rather than relying on LLM prompt instructions."
    ])
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Audit AI Agent codebase for OWASP Agentic Security Initiative (ASI) Top 10 risks."
    )
    parser.add_argument("--root", type=str, default=".", help="Project root directory (default: .)")
    parser.add_argument("--json", action="store_true", help="Output audit results as JSON")
    parser.add_argument("--output", type=str, help="Save report to file")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    summary = scan_project(root_dir)

    if args.json:
        output_text = json.dumps(summary, indent=2)
    else:
        output_text = format_markdown_report(summary)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as fh:
            fh.write(output_text + "\n")
        print(f"OWASP ASI audit report written to: {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0 if summary["verdict"] == "COMPLIANT" else 1


if __name__ == "__main__":
    sys.exit(main())
