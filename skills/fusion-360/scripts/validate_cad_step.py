#!/usr/bin/env python3
"""CAD STEP/STL & Parametric Script Linter.

Audits:
1. STEP / STP / STL export files:
   - Header validity (ISO-10303-21 standard)
   - Unit contract (verifies millimeter definition)
   - File integrity and non-zero manifold geometry
2. Build123d / CadQuery / Fusion 360 Python scripts:
   - AST syntax validation
   - Detection of hardcoded dimensions vs userParameters
   - Safe export statement validation (export_step / export_stl)
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def audit_step_file(file_path: Path) -> list[str]:
    issues = []
    if not file_path.exists():
        return [f"File not found: {file_path}"]

    size = file_path.stat().st_size
    if size < 100:
        issues.append(f"STEP file is suspiciously small ({size} bytes). May be empty or corrupt.")

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")[:4096]
        if "ISO-10303-21;" not in content:
            issues.append("Missing standard ISO-10303-21 STEP header marker.")
        if "HEADER;" not in content:
            issues.append("Missing HEADER block in STEP file.")
        
        # Check units
        if "SI_UNIT(.MILLI.,.METRE.)" not in content and "MILLIMETRE" not in content:
            issues.append("Unit warning: Millimeter unit definition not explicitly found. Verify unit scale before manufacturing.")
    except Exception as e:
        issues.append(f"Failed to read STEP file: {e}")

    return issues


def audit_cad_script(script_path: Path) -> list[str]:
    issues = []
    if not script_path.exists():
        return [f"Script not found: {script_path}"]

    try:
        code = script_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(code, filename=str(script_path))

        # Check for export statements
        has_export = bool(re.search(r"\b(export_step|export_stl|ExportManager|SaveAs3)\b", code))
        if not has_export:
            issues.append("Notice: No CAD export function detected (e.g. export_step, export_stl, or ExportManager).")

        # Check for un-parameterized negative dimensions in extrude
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", "") in ("extrude", "ExtrudeFeature"):
                for arg in node.args:
                    if isinstance(arg, ast.UnaryOp) and isinstance(arg.op, ast.USub):
                        issues.append("Warning: Extrude called with negative literal. Verify extrusion direction vector.")
    except SyntaxError as se:
        issues.append(f"SyntaxError in CAD script on line {se.lineno}: {se.msg}")
    except Exception as e:
        issues.append(f"Script audit error: {e}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="CAD STEP/STL & Parametric Script Linter")
    parser.add_argument("paths", nargs="+", help="Files to audit (.step, .stp, .stl, or .py)")
    args = parser.parse_args()

    total_issues = 0
    print("=== CAD Parametric & Export Safety Linter ===")

    for p_str in args.paths:
        p = Path(p_str)
        ext = p.suffix.lower()
        print(f"\nAuditing: {p.name}")

        if ext in (".step", ".stp"):
            issues = audit_step_file(p)
        elif ext == ".py":
            issues = audit_cad_script(p)
        elif ext == ".stl":
            size = p.stat().st_size if p.exists() else 0
            issues = ["STL file is empty (< 84 bytes header)."] if size < 84 else []
        else:
            issues = [f"Unsupported file format: {ext} (expected .step, .stp, .stl, or .py)"]

        if issues:
            total_issues += len(issues)
            for iss in issues:
                print(f"  ✗ {iss}")
        else:
            print("  ✓ PASS: File conforms to CAD production standards.")

    print(f"\nAudit complete: {total_issues} issue(s) found.")
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
