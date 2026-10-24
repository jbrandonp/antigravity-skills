#!/usr/bin/env python3
"""
simulate_agent_threats.py — Automated architectural stress-testing and threat simulation engine.
Executes 12 discriminating probes against an AI Agent specification based on scenarios U01–U15.

Usage:
  python simulate_agent_threats.py PATH [--json] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List

STRESS_PROBES = [
    {
        "id": "PROBE-01",
        "scenario": "U08 (Parallel Guardrail Timing)",
        "name": "Synchronous Pre-Effect Enforcement",
        "severity": "CRITICAL",
        "keywords": [r"pre[_\s-]?execution", r"pre[_\s-]?call", r"before an external effect", r"synchronous gate"],
        "anti_keywords": [r"parallel check", r"asynchronous guardrail", r"audit after execution"],
        "rationale": "If safety checks run in parallel or asynchronously after an effect has been dispatched, violations cannot be prevented.",
        "remediation": "Enforce mandatory synchronous gate before any external mutation."
    },
    {
        "id": "PROBE-02",
        "scenario": "U10 (Concurrent Budget Race Condition)",
        "name": "Centralized Shared Budget Reservation",
        "severity": "CRITICAL",
        "keywords": [r"reservation", r"centralized budget", r"atomic budget", r"allocated share", r"shared pool"],
        "anti_keywords": [r"each worker gets full budget", r"workers share same limit independently"],
        "rationale": "When concurrent subagents query the remaining budget independently, they can concurrently overshoot total financial limits.",
        "remediation": "Implement atomic budget reservation tokens before fanning out tasks."
    },
    {
        "id": "PROBE-03",
        "scenario": "U09 (Ambiguous Timeout Reconciliation)",
        "name": "Effect-Unknown Downstream Reconciliation",
        "severity": "MAJOR",
        "keywords": [r"effect[_\s-]?unknown", r"reconciliation", r"poll downstream", r"verify status before retry", r"idempotency[_\s-]?key"],
        "anti_keywords": [r"blindly retry", r"retry on timeout without check"],
        "rationale": "A timed-out network write may have succeeded on the remote server; blindly retrying causes duplicate orders or charges.",
        "remediation": "Enter EFFECT_UNKNOWN state and query downstream resource status before re-attempting."
    },
    {
        "id": "PROBE-04",
        "scenario": "Diagnostics (False Success Defense)",
        "name": "Observable Artifact Verification",
        "severity": "MAJOR",
        "keywords": [r"observable", r"acceptance gate", r"groundedness", r"verifiable output", r"traceable"],
        "anti_keywords": [r"trust model done=true", r"model self-reports done"],
        "rationale": "A model declaring done=true does not prove task completion; an empty or broken output must be verified by the runtime.",
        "remediation": "Verify required output fields, non-empty datasets, and concrete file artifacts."
    },
    {
        "id": "PROBE-05",
        "scenario": "U11 (Memory Poisoning & Procedural Promotion)",
        "name": "Authoritative Procedure Admission",
        "severity": "CRITICAL",
        "keywords": [r"change authority", r"admission policy", r"validated before active", r"candidate memory", r"approval"],
        "anti_keywords": [r"agent modifies its own rules automatically", r"experience immediately becomes rule"],
        "rationale": "Untrusted external text saved directly as an active instruction can permanently bypass agent guardrails.",
        "remediation": "Require explicit human or policy approval before candidate rules are promoted to active procedures."
    },
    {
        "id": "PROBE-06",
        "scenario": "U12 (Sandbox Boundary Integrity)",
        "name": "Comprehensive Execution Isolation",
        "severity": "CRITICAL",
        "keywords": [r"sandbox", r"container", r"isolated", r"non-root", r"network isolation", r"read-only"],
        "anti_keywords": [r"host filesystem access", r"runs directly on host without sandbox"],
        "rationale": "Isolating one tool in a container while leaving browser or filesystem tools on the host creates a privilege escalation path.",
        "remediation": "Enforce unified container/micro-VM sandboxing for all code, shell, and browser execution."
    },
    {
        "id": "PROBE-07",
        "scenario": "U13 (Cancellation Post-Effect Disclosure)",
        "name": "Task Cancellation vs Rollback Distinction",
        "severity": "MAJOR",
        "keywords": [r"cancellation", r"abort", r"rollback distinction", r"cancel does not rollback", r"already dispatched"],
        "anti_keywords": [r"cancelling rolls back everything automatically"],
        "rationale": "Cancelling a running job does not automatically undo external side-effects that have already completed.",
        "remediation": "Explicitly track which actions were already dispatched and initiate compensating transactions if necessary."
    },
    {
        "id": "PROBE-08",
        "scenario": "U05 (Non-Compensable Security Gates)",
        "name": "Hard Security Block Overriding Quality Score",
        "severity": "CRITICAL",
        "keywords": [r"non-compensable", r"hard block", r"zero-tolerance", r"immediately blocks", r"security gate"],
        "anti_keywords": [r"average score includes security", r"high quality compensates for permission error"],
        "rationale": "A high writing quality score (e.g. 98%) must never compensate for or hide a tenant access or security violation.",
        "remediation": "Treat security and authorization as non-compensable binary gates (0 = instant rejection)."
    },
    {
        "id": "PROBE-09",
        "scenario": "U14 (Tool Interface & Truncation Transparency)",
        "name": "Completeness & Pagination Indicators",
        "severity": "MAJOR",
        "keywords": [r"pagination", r"truncation", r"partial data", r"indicator", r"schema units"],
        "anti_keywords": [r"silent truncation", r"cut off without indication"],
        "rationale": "Truncating tool outputs without flagging partial completeness causes models to assume data is fully represented.",
        "remediation": "Include explicit has_more, total_count, and units in all tool schemas."
    },
    {
        "id": "PROBE-10",
        "scenario": "U01 (Minimal Viable Complexity)",
        "name": "Occam's Razor Complexity Guard",
        "severity": "MINOR",
        "keywords": [r"simplest alternative", r"predefined workflow", r"single call", r"minimal complexity", r"justified"],
        "anti_keywords": [r"use swarm for simple task", r"unnecessary multi-agent"],
        "rationale": "Introducing complex multi-agent loops when a simple single-call or deterministic script suffices multiplies failure modes.",
        "remediation": "Justify every added component against a simpler non-agentic alternative."
    },
    {
        "id": "PROBE-11",
        "scenario": "U07 (Independent Evaluation Split)",
        "name": "Independent Benchmark vs Tuning Split",
        "severity": "MAJOR",
        "keywords": [r"independent evaluation", r"separate validation", r"holdout", r"tuning vs test", r"gold standard"],
        "anti_keywords": [r"evaluate on training prompt", r"tune criteria on eval set"],
        "rationale": "Evaluating an agent on the same prompts or gold examples used for prompt engineering yields false confidence.",
        "remediation": "Maintain an unpolluted, independent holdout eval set."
    },
    {
        "id": "PROBE-12",
        "scenario": "Egress Redaction (Data Exfiltration Defense)",
        "name": "Egress PII & Secret Scrubbing",
        "severity": "CRITICAL",
        "keywords": [r"redaction", r"egress", r"scrub", r"pii", r"data leakage"],
        "anti_keywords": [r"direct output without filter"],
        "rationale": "Agents accessing sensitive databases can inadvertently echo API keys or user credentials back to the chat interface.",
        "remediation": "Deploy an egress filtering proxy scanning for API key patterns and PII before user delivery."
    }
]


def run_threat_probes(doc_path: Path) -> dict:
    """Run all 12 stress probes against an agent architecture document."""
    if not doc_path.is_file():
        return {
            "error": f"File not found: {doc_path}",
            "status": "FAIL"
        }

    try:
        content = doc_path.read_text(encoding="utf-8", errors="replace").lower()
    except Exception as e:
        return {
            "error": f"Could not read file: {e}",
            "status": "FAIL"
        }

    passed_count = 0
    findings = []
    critical_failures = 0

    for probe in STRESS_PROBES:
        matched = False
        for kw in probe["keywords"]:
            if re.search(kw, content):
                matched = True
                break

        anti_matched = False
        if "anti_keywords" in probe:
            for akw in probe["anti_keywords"]:
                if re.search(akw, content):
                    anti_matched = True
                    break

        if matched and not anti_matched:
            passed_count += 1
            findings.append({
                "id": probe["id"],
                "scenario": probe["scenario"],
                "name": probe["name"],
                "severity": probe["severity"],
                "status": "MITIGATED",
                "message": "Architecture explicitly addresses this failure mode."
            })
        else:
            if probe["severity"] == "CRITICAL":
                critical_failures += 1
            findings.append({
                "id": probe["id"],
                "scenario": probe["scenario"],
                "name": probe["name"],
                "severity": probe["severity"],
                "status": "VULNERABLE",
                "rationale": probe["rationale"],
                "remediation": probe["remediation"]
            })

    total_probes = len(STRESS_PROBES)
    pass_rate = round((passed_count / total_probes) * 100, 1)

    return {
        "target_file": str(doc_path),
        "total_probes": total_probes,
        "mitigated_probes": passed_count,
        "vulnerable_probes": total_probes - passed_count,
        "critical_failures": critical_failures,
        "pass_rate": pass_rate,
        "verdict": "RESILIENT" if (pass_rate >= 80 and critical_failures == 0) else "VULNERABLE",
        "findings": findings
    }


def format_stress_report(result: dict) -> str:
    """Format markdown stress report."""
    lines = [
        "# 🌪️ AI Agent Architectural Stress-Test & Threat Simulation Report",
        "",
        "## 📊 Executive Threat Posture",
        f"- **Audited Document :** `{result['target_file']}`",
        f"- **Resilience Verdict :** **{result['verdict']}** ({result['pass_rate']}% Mitigated)",
        f"- **Mitigated Probes :** `{result['mitigated_probes']}/{result['total_probes']}`",
        f"- **Critical Vulnerabilities :** `{result['critical_failures']}`",
        "",
        "## 🛡️ Probes & Scenario Breakdown (U01–U15)",
        "| ID | Scenario | Stress Probe | Severity | Status | Architectural Defense / Action |",
        "| :--- | :--- | :--- | :---: | :---: | :--- |"
    ]

    for f in result["findings"]:
        icon = "🛡️" if f["status"] == "MITIGATED" else ("🚨" if f["severity"] == "CRITICAL" else "⚠️")
        note = f["message"] if f["status"] == "MITIGATED" else f["remediation"]
        lines.append(f"| `{f['id']}` | {f['scenario']} | {f['name']} | {f['severity']} | {icon} {f['status']} | {note} |")

    lines.extend([
        "",
        "## ⚠️ Hard Architecture Gates",
        "1. Critical probes must be 100% mitigated prior to production roll-out.",
        "2. Any unmitigated probe represents an active operational or financial hazard."
    ])
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Run architectural stress probes against AI Agent specification (Scenarios U01-U15)."
    )
    parser.add_argument("path", type=str, help="Path to architecture specification markdown file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--output", type=str, help="Write report to specified file")
    args = parser.parse_args()

    doc_p = Path(args.path).resolve()
    result = run_threat_probes(doc_p)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    if args.json:
        output_text = json.dumps(result, indent=2)
    else:
        output_text = format_stress_report(result)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as fh:
            fh.write(output_text + "\n")
        print(f"Stress test report written to: {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0 if result["verdict"] == "RESILIENT" else 1


if __name__ == "__main__":
    sys.exit(main())
