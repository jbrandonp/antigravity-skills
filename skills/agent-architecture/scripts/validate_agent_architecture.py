#!/usr/bin/env python3
"""
validate_agent_architecture.py — Verifies that an AI Agent architecture document conforms
to the 7 Mandatory Deliverable Views of the Antigravity Agent Architecture Contract.

Usage:
  python validate_agent_architecture.py PATH [--json]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List

MANDATORY_VIEWS = [
    {
        "id": "VIEW-01",
        "title": "Task and Requirements Criteria",
        "patterns": [r"task and (requirements )?criteria", r"mission & value", r"requirements traceability"]
    },
    {
        "id": "VIEW-02",
        "title": "Structure and Boundaries",
        "patterns": [r"structure and boundaries", r"component topology", r"component responsibilities"]
    },
    {
        "id": "VIEW-03",
        "title": "Execution, State, and Stopping",
        "patterns": [r"execution, state,? and stopping", r"operational limits", r"sequence flow", r"four environment functions"]
    },
    {
        "id": "VIEW-04",
        "title": "Context, Knowledge, and Memory",
        "patterns": [r"context, knowledge,? and memory", r"token budget", r"compaction & memory"]
    },
    {
        "id": "VIEW-05",
        "title": "Tool Contracts and Authority",
        "patterns": [r"tool contracts and authority", r"registered capabilities", r"idempotency and write"]
    },
    {
        "id": "VIEW-06",
        "title": "Threats and Failures",
        "patterns": [r"threat(s| model)? and failures?", r"threat mitigation"]
    },
    {
        "id": "VIEW-07",
        "title": "Quality Verification, Economics & Evaluation Gates",
        "patterns": [r"quality verification", r"evaluation gates?", r"quality gate criteria"]
    }
]


def validate_architecture_contract(doc_path: Path) -> dict:
    """Validate document against the 7 contract views."""
    if not doc_path.is_file():
        return {
            "error": f"File not found: {doc_path}",
            "status": "FAIL"
        }

    try:
        content = doc_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {
            "error": f"Could not read file: {e}",
            "status": "FAIL"
        }

    view_results = []
    missing_views = []

    for view in MANDATORY_VIEWS:
        matched = False
        for pat in view["patterns"]:
            if re.search(pat, content, re.IGNORECASE):
                matched = True
                break
        if matched:
            view_results.append({
                "id": view["id"],
                "title": view["title"],
                "status": "PASS"
            })
        else:
            missing_views.append(view["title"])
            view_results.append({
                "id": view["id"],
                "title": view["title"],
                "status": "FAIL"
            })

    # Diagram check
    has_mermaid = "```mermaid" in content

    # Limits table check
    has_limits_table = bool(re.search(r"iterations|steps|timeout|budget", content, re.IGNORECASE))

    # Placeholder check
    placeholders = re.findall(r"\[(TODO|TBD|FIXME)\]", content, re.IGNORECASE)

    is_valid = (len(missing_views) == 0 and has_mermaid and has_limits_table)
    score = round((len(MANDATORY_VIEWS) - len(missing_views)) / len(MANDATORY_VIEWS) * 100, 1)

    return {
        "file": str(doc_path),
        "status": "PASS" if is_valid else "FAIL",
        "contract_score": score,
        "views_audited": len(MANDATORY_VIEWS),
        "missing_views": missing_views,
        "has_mermaid_diagrams": has_mermaid,
        "has_limits_table": has_limits_table,
        "unresolved_placeholders_count": len(placeholders),
        "details": view_results
    }


def format_report(result: dict) -> str:
    """Format human-readable CLI report."""
    lines = [
        "==================================================================",
        "          AI AGENT ARCHITECTURE CONTRACT VALIDATION ENGINE        ",
        "==================================================================",
        f"Target Document : {result['file']}",
        f"Contract Status : {result['status']} ({result['contract_score']}% coverage)",
        f"Mermaid Diagrams: {'✓ Present' if result['has_mermaid_diagrams'] else '✗ Missing'}",
        f"Limits Table    : {'✓ Present' if result['has_limits_table'] else '✗ Missing'}",
        f"Unresolved [TODO] / [TBD]: {result['unresolved_placeholders_count']}",
        "------------------------------------------------------------------"
    ]

    for v in result["details"]:
        icon = "✓" if v["status"] == "PASS" else "✗"
        lines.append(f"{icon} {v['id']} — {v['title']:<50} [{v['status']}]")

    lines.append("==================================================================")
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Validate AI Agent Architecture document against the 7 Contract Views."
    )
    parser.add_argument("path", type=str, help="Path to architecture specification markdown file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    doc_p = Path(args.path).resolve()
    result = validate_architecture_contract(doc_p)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
