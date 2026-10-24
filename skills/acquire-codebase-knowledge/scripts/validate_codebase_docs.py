#!/usr/bin/env python3
"""
validate_codebase_docs.py — Mandatory Phase 4 validation engine for acquire-codebase-knowledge.
Verifies the existence, section completeness, placeholder resolution, and evidence traceability
for all 7 codebase documentation files in docs/codebase/.

Usage:
  python validate_codebase_docs.py [--docs-dir DIR] [--root DIR] [--json]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

MANDATORY_DOCS = [
    "STACK.md",
    "STRUCTURE.md",
    "ARCHITECTURE.md",
    "CONVENTIONS.md",
    "INTEGRATIONS.md",
    "TESTING.md",
    "CONCERNS.md"
]

REQUIRED_SECTIONS: Dict[str, List[str]] = {
    "STACK.md": [
        "Core Stack",
        "Dependencies",
        "Dev Tooling",
        "Build and Runtime Scripts",
        "Evidence"
    ],
    "STRUCTURE.md": [
        "Directory Layout",
        "Entry Points",
        "Directory Responsibilities",
        "Evidence"
    ],
    "ARCHITECTURE.md": [
        "Architectural Style",
        "System Flow",
        "Layer/Module Responsibilities",
        "Reused Patterns",
        "Evidence"
    ],
    "CONVENTIONS.md": [
        "File and Symbol Naming",
        "Formatting and Linting",
        "Error Handling",
        "Evidence"
    ],
    "INTEGRATIONS.md": [
        "External APIs",
        "Databases",
        "Authentication",
        "Evidence"
    ],
    "TESTING.md": [
        "Test Frameworks",
        "Test Directory Structure",
        "Mocking Strategy",
        "Evidence"
    ],
    "CONCERNS.md": [
        "Top Risks",
        "Technical Debt",
        "Security Concerns",
        "Fragile/High-Churn Areas",
        "Evidence"
    ]
}

# Generic unreplaced placeholders from templates
PLACEHOLDER_REGEX = re.compile(r'\[(item|path|high/med/low|issue|reason|impact|next action|fix|risk|what exists|what is missing|name|responsibility)\]', re.IGNORECASE)
EVIDENCE_PATH_REGEX = re.compile(r'[-*]\s+\[?`?([a-zA-Z0-9_\-/\.\\]+\.[a-zA-Z0-9]+)`?\]?')


def validate_document(
    doc_path: Path,
    doc_name: str,
    root_dir: Path
) -> dict:
    """Validate a single documentation file against required sections and evidence."""
    result = {
        "doc": doc_name,
        "exists": doc_path.is_file(),
        "missing_sections": [],
        "unfilled_placeholders": [],
        "todos": [],
        "ask_users": [],
        "verified_evidence": [],
        "missing_evidence": [],
        "is_valid": False
    }

    if not result["exists"]:
        return result

    try:
        content = doc_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result["missing_sections"].append(f"Could not read file: {e}")
        return result

    # Check required sections
    required = REQUIRED_SECTIONS.get(doc_name, [])
    for sec in required:
        if not re.search(rf'#{{1,4}}\s+.*{re.escape(sec)}', content, re.IGNORECASE):
            result["missing_sections"].append(sec)

    # Check for unaddressed template placeholders
    for match in PLACEHOLDER_REGEX.finditer(content):
        result["unfilled_placeholders"].append(match.group(0))

    # Extract TODO and ASK USER items
    for line in content.splitlines():
        line_s = line.strip()
        if "[TODO]" in line_s:
            result["todos"].append(line_s)
        if "[ASK USER]" in line_s:
            result["ask_users"].append(line_s)

    # Extract evidence filepaths in Evidence section
    evidence_match = re.search(r'#{1,4}\s+.*Evidence(.*?)(?=\n#{1,4}|\Z)', content, re.DOTALL | re.IGNORECASE)
    if evidence_match:
        ev_text = evidence_match.group(1)
        for line in ev_text.splitlines():
            line_str = line.strip()
            path_matches = EVIDENCE_PATH_REGEX.findall(line_str)
            for p in path_matches:
                # Normalize path and check existence
                p_norm = p.replace('\\', '/')
                # Ignore url or generic placeholders
                if p_norm.startswith(('http://', 'https://', 'path/to')):
                    continue
                file_candidate = root_dir / p_norm
                if file_candidate.exists():
                    result["verified_evidence"].append(p_norm)
                else:
                    result["missing_evidence"].append(p_norm)

    result["is_valid"] = (
        len(result["missing_sections"]) == 0 and
        len(result["unfilled_placeholders"]) == 0
    )

    return result


def audit_codebase_docs(docs_dir: Path, root_dir: Path) -> dict:
    """Run full validation suite on docs/codebase/."""
    results = {}
    all_valid = True
    total_docs = len(MANDATORY_DOCS)
    valid_count = 0

    for doc_name in MANDATORY_DOCS:
        doc_path = docs_dir / doc_name
        doc_res = validate_document(doc_path, doc_name, root_dir)
        results[doc_name] = doc_res
        if doc_res["is_valid"]:
            valid_count += 1
        else:
            all_valid = False

    completion_score = round((valid_count / total_docs) * 100, 1)

    return {
        "status": "PASS" if all_valid else "FAIL",
        "docs_dir": str(docs_dir),
        "completion_score": completion_score,
        "valid_docs_count": valid_count,
        "total_docs_count": total_docs,
        "documents": results
    }


def format_report(summary: dict) -> str:
    """Generate human-readable console report."""
    lines = [
        "==================================================================",
        "      CODEBASE KNOWLEDGE DOCUMENTATION VALIDATION ENGINE         ",
        "==================================================================",
        f"Status: {summary['status']} | Score: {summary['completion_score']}% ({summary['valid_docs_count']}/{summary['total_docs_count']} valid)",
        f"Directory: {summary['docs_dir']}",
        "------------------------------------------------------------------"
    ]

    for doc_name, res in summary["documents"].items():
        icon = "✓" if res["is_valid"] else "✗"
        status_str = "VALID" if res["is_valid"] else ("MISSING FILE" if not res["exists"] else "INCOMPLETE")
        lines.append(f"{icon} {doc_name:<18} [{status_str}]")

        if res["missing_sections"]:
            lines.append(f"    Missing Sections: {', '.join(res['missing_sections'])}")
        if res["unfilled_placeholders"]:
            lines.append(f"    Unfilled Placeholders: {', '.join(set(res['unfilled_placeholders']))}")
        if res["missing_evidence"]:
            lines.append(f"    Missing Evidence Paths: {', '.join(res['missing_evidence'])}")
        if res["todos"]:
            lines.append(f"    Open [TODO]s: {len(res['todos'])}")
        if res["ask_users"]:
            lines.append(f"    Pending [ASK USER] items: {len(res['ask_users'])}")

    lines.append("==================================================================")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Phase 4 documentation contract for acquire-codebase-knowledge."
    )
    parser.add_argument("--docs-dir", type=str, default="docs/codebase", help="Path to docs/codebase folder")
    parser.add_argument("--root", type=str, default=".", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    docs_dir = (root_dir / args.docs_dir).resolve() if not Path(args.docs_dir).is_absolute() else Path(args.docs_dir)

    summary = audit_codebase_docs(docs_dir, root_dir)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_report(summary))

    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
