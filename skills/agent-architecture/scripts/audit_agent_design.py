#!/usr/bin/env python3
"""
audit_agent_design.py — Static architectural auditor and diagnostic engine for AI Agents.
Verifies compliance against the 10 Golden Architectural Invariants for autonomous agents.

Usage:
  python audit_agent_design.py PATH [--json] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

INVARIANTS = [
    {
        "id": "INV-01",
        "name": "Unbounded Loop Defense",
        "severity": "CRITICAL",
        "points": 20,
        "keywords": [r"max[_\s-]?iterations", r"max[_\s-]?steps", r"iteration[_\s-]?limit", r"step[_\s-]?counter", r"loop[_\s-]?breaker"],
        "recommendation": "Define an explicit maximum iteration/step cap enforced by the runtime (e.g., max 10 steps)."
    },
    {
        "id": "INV-02",
        "name": "Total Task Timeout",
        "severity": "MAJOR",
        "points": 10,
        "keywords": [r"timeout", r"deadline", r"watchdog", r"execution[_\s-]?time"],
        "recommendation": "Configure a hard execution timeout (e.g. 60s) to abort stalled network/agent operations."
    },
    {
        "id": "INV-03",
        "name": "Token & Cost Guardrail",
        "severity": "MAJOR",
        "points": 10,
        "keywords": [r"budget", r"cost[_\s-]?limit", r"token[_\s-]?limit", r"hard[_\s-]?cap", r"quota"],
        "recommendation": "Enforce a maximum financial ($) or token budget per execution cycle to prevent runaway billing."
    },
    {
        "id": "INV-04",
        "name": "Deterministic Policy Enforcement",
        "severity": "CRITICAL",
        "points": 20,
        "keywords": [r"deterministic", r"policy[_\s-]?gate", r"pre[_\s-]?call", r"runtime[_\s-]?enforce", r"permission[_\s-]?check"],
        "anti_keywords": [r"prompt only", r"model decides if allowed", r"instruct the model not to"],
        "recommendation": "Never rely solely on LLM prompt instructions to enforce security or access control; use programmatic runtime validators."
    },
    {
        "id": "INV-05",
        "name": "Write Idempotency & Reconciliation",
        "severity": "MAJOR",
        "points": 10,
        "keywords": [r"idempotency", r"idempotent", r"reconciliation", r"effect[_\s-]?unknown", r"deduplication"],
        "recommendation": "All state-mutating tools must enforce idempotency keys and handle ambiguous timeouts (EFFECT_UNKNOWN)."
    },
    {
        "id": "INV-06",
        "name": "Tool Budget & Overcrowding Prevention",
        "severity": "MAJOR",
        "points": 10,
        "keywords": [r"router", r"subagent", r"hierarchy", r"specialized", r"tool[_\s-]?catalog"],
        "recommendation": "Avoid exposing >15 tools directly in one prompt; use a Router-Worker or dynamic tool discovery."
    },
    {
        "id": "INV-07",
        "name": "Context Compaction & Memory Isolation",
        "severity": "MINOR",
        "points": 5,
        "keywords": [r"compact", r"compaction", r"summariz", r"sliding[_\s-]?window", r"memory[_\s-]?tier"],
        "recommendation": "Implement context compaction and ensure authorization tokens are never dumped into chat history."
    },
    {
        "id": "INV-08",
        "name": "Untrusted Input & Prompt Injection Defense",
        "severity": "CRITICAL",
        "points": 15,
        "keywords": [r"prompt[_\s-]?injection", r"sanitiz", r"ingress", r"untrusted", r"guardrail"],
        "recommendation": "Isolate untrusted user/web input from privileged system instructions using XML delimiters or ingress scanners."
    },
    {
        "id": "INV-09",
        "name": "Execution Isolation & Sandboxing",
        "severity": "MAJOR",
        "points": 10,
        "keywords": [r"sandbox", r"container", r"docker", r"isolated[_\s-]?process", r"gvisor", r"firecracker", r"read-only"],
        "recommendation": "Code execution, terminal commands, or browser actions must run in isolated sandboxes with zero-trust networking."
    },
    {
        "id": "INV-10",
        "name": "Human-in-the-Loop & Escalation Path",
        "severity": "MINOR",
        "points": 5,
        "keywords": [r"human[_\s-]?in[_\s-]?the[_\s-]?loop", r"approval", r"escalat", r"fallback", r"human[_\s-]?queue"],
        "recommendation": "Sensitive or irreversible actions must require explicit confirmation or escalate to a human review queue."
    }
]


def audit_agent_document(doc_path: Path) -> dict:
    """Audit an agent design specification or prompt against architectural invariants."""
    if not doc_path.is_file():
        return {
            "error": f"File not found: {doc_path}",
            "status": "ERROR"
        }

    try:
        content = doc_path.read_text(encoding="utf-8", errors="replace").lower()
    except Exception as e:
        return {
            "error": f"Could not read file: {e}",
            "status": "ERROR"
        }

    total_score = 100
    findings = []
    passed_invariants = 0

    for inv in INVARIANTS:
        matched = False
        # Check positive keywords
        for kw in inv["keywords"]:
            if re.search(kw, content):
                matched = True
                break

        # Check for anti-keywords if present
        anti_matched = False
        if "anti_keywords" in inv:
            for akw in inv["anti_keywords"]:
                if re.search(akw, content):
                    anti_matched = True
                    break

        if matched and not anti_matched:
            passed_invariants += 1
            findings.append({
                "id": inv["id"],
                "name": inv["name"],
                "severity": "PASS",
                "status": "PASS",
                "deduction": 0,
                "message": "Compliant invariant evidenced in architecture."
            })
        else:
            total_score -= inv["points"]
            findings.append({
                "id": inv["id"],
                "name": inv["name"],
                "severity": inv["severity"],
                "status": "FAIL",
                "deduction": inv["points"],
                "message": inv["recommendation"]
            })

    total_score = max(0, total_score)
    if total_score >= 85:
        verdict = "ARCHITECTURALLY_SOUND"
    elif total_score >= 65:
        verdict = "MODERATE_RISK"
    else:
        verdict = "CRITICAL_DEFICIENCIES"

    return {
        "target_file": str(doc_path),
        "score": total_score,
        "verdict": verdict,
        "passed_invariants": passed_invariants,
        "total_invariants": len(INVARIANTS),
        "findings": findings
    }


def format_markdown_audit_report(result: dict) -> str:
    """Format audit results as Markdown."""
    lines = [
        "# 🛡️ AI Agent Architecture Diagnostic Audit Report",
        "",
        "## 📊 Executive Summary",
        f"- **Audited Document :** `{result['target_file']}`",
        f"- **Readiness Score :** `{result['score']}/100` ({result['verdict']})",
        f"- **Invariants Satisfied :** `{result['passed_invariants']}/{result['total_invariants']}` ({result['passed_invariants']/result['total_invariants']*100:.1f}%)",
        "",
        "## 🔍 Invariant Findings & Deficiencies",
        "| ID | Invariant | Severity | Status | Actionable Remediation |",
        "| :--- | :--- | :---: | :---: | :--- |"
    ]

    for f in result["findings"]:
        status_icon = "✅" if f["status"] == "PASS" else ("🚨" if f["severity"] == "CRITICAL" else "⚠️")
        lines.append(f"| `{f['id']}` | {f['name']} | {f['severity']} | {status_icon} {f['status']} | {f['message']} |")

    lines.extend([
        "",
        "## 💡 Next Steps for Production Readiness",
        "1. Remedy all `CRITICAL` findings before deploying to production environments.",
        "2. Ensure runtime enforcement layer wraps agent execution rather than relying on LLM self-policing.",
        "3. Re-run `audit_agent_design.py` to confirm 100% adherence to all 10 invariants."
    ])

    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Audit AI Agent design against the 10 Golden Architectural Invariants."
    )
    parser.add_argument("path", type=str, help="Path to agent architecture markdown, prompt, or spec file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--output", type=str, help="Write output to specified file")
    args = parser.parse_args()

    doc_path = Path(args.path).resolve()
    result = audit_agent_document(doc_path)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    if args.json:
        output_text = json.dumps(result, indent=2)
    else:
        output_text = format_markdown_audit_report(result)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as fh:
            fh.write(output_text + "\n")
        print(f"Audit report written to: {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0 if result["score"] >= 65 else 1


if __name__ == "__main__":
    sys.exit(main())
