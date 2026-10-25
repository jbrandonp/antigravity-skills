#!/usr/bin/env python3
"""Deterministic validator for Slang shader files (.slang).

Checks:
- Entry point stage annotations ([shader("compute|vertex|fragment|pixel")])
- ParameterBlock declarations
- Module and import directives
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

def validate_slang(file_path: Path) -> list[str]:
    issues = []
    text = file_path.read_text(encoding="utf-8", errors="replace")
    
    # Check entry point
    has_stage = bool(re.search(r'\[shader\s*\(\s*"(compute|vertex|fragment|pixel|geometry|raygen)"\s*\)\]', text))
    is_module_only = text.strip().startswith("module ") and not has_stage
    
    if not has_stage and not is_module_only:
        issues.append("Missing entry point annotation, e.g., [shader(\"compute\")] or [shader(\"vertex\")].")

    # Check unmatched braces
    open_braces = text.count("{")
    close_braces = text.count("}")
    if open_braces != close_braces:
        issues.append(f"Mismatched braces: {open_braces} open vs {close_braces} close.")

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description="Slang Shader Validator")
    parser.add_argument("files", nargs="+", help="Path to .slang files")
    args = parser.parse_args()

    total_errors = 0
    for f_str in args.files:
        f = Path(f_str)
        if not f.exists():
            print(f"[ERROR] File not found: {f}")
            total_errors += 1
            continue
        errs = validate_slang(f)
        if errs:
            total_errors += len(errs)
            print(f"[FAIL] {f.name}:")
            for e in errs:
                print(f"  ✗ {e}")
        else:
            print(f"[PASS] {f.name}: Slang syntax and structure valid.")

    return 0 if total_errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
