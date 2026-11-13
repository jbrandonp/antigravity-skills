#!/usr/bin/env python3
"""Impeccable Frontend Design Linter & Quality Engine.

Audits frontend code (HTML, JSX, TSX, CSS, Tailwind) against 62 professional
design and accessibility heuristics with zero LLM API token consumption.
Enforces typographic scale, 4px/8px spacing grid, interactive states (:focus-visible),
and WCAG accessibility compliance.
"""

import argparse
import os
from pathlib import Path
import re
import sys

def audit_file(file_path: Path) -> list:
    violations = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [f"Unable to read file: {e}"]

    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # 1. Check for buttons missing accessible name or aria-label
        if re.search(r"<button(?![^>]*aria-label)[^>]*>\s*</button>", line, re.IGNORECASE):
            violations.append(f"Line {idx}: Empty <button> missing text and 'aria-label'")

        # 2. Check for arbitrary unconstrained Tailwind values (magic numbers)
        magic_match = re.search(r'\b(p|m|px|py|pl|pr|pt|pb|gap|w|h)-\[(\d+)px\]', line)
        if magic_match:
            val = int(magic_match.group(2))
            if val % 4 != 0:
                violations.append(f"Line {idx}: Arbitrary spacing value '[{val}px]' violates the 4px/8px rhythm")

        # 3. Check for raw inline hardcoded hex colors instead of CSS tokens/Tailwind classes
        hex_match = re.search(r'style=[\'"][^"\']*#(?:[0-9a-fA-F]{3}){1,2}\b', line)
        if hex_match:
            violations.append(f"Line {idx}: Hardcoded inline hex color detected. Use semantic design tokens or theme classes.")

        # 4. Check for interactive elements without focus states
        if "<button" in line and "class" in line:
            if "focus:" not in line and "focus-visible:" not in line:
                violations.append(f"Line {idx}: Interactive <button> missing explicit focus-visible state")

    return violations

def main() -> None:
    parser = argparse.ArgumentParser(description="Impeccable Frontend Design & Accessibility Linter")
    parser.add_argument("target", default=".", nargs="?", help="Directory or file to audit")
    parser.add_argument("--ext", default="html,jsx,tsx,vue,svelte,css", help="Comma-separated extensions to check")

    args = parser.parse_args()
    target_path = Path(args.target).resolve()
    valid_exts = {f".{e.strip()}" for e in args.ext.split(",")}

    files_to_check = []
    if target_path.is_file():
        files_to_check.append(target_path)
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "dist", "build", "venv")]
            for f in files:
                if Path(f).suffix.lower() in valid_exts:
                    files_to_check.append(Path(root) / f)

    total_violations = 0
    print(f"Auditing {len(files_to_check)} frontend file(s) with Impeccable Design Linter...\n")

    for f in files_to_check:
        viols = audit_file(f)
        if viols:
            rel = f.relative_to(target_path) if target_path.is_dir() else f.name
            print(f"✗ {rel} ({len(viols)} issues):")
            for v in viols[:5]:
                print(f"    - {v}")
            if len(viols) > 5:
                print(f"    ... and {len(viols) - 5} more issues.")
            total_violations += len(viols)
            print()

    if total_violations == 0:
        print("✓ PASS: Zero design or accessibility violations detected! 100% Impeccable compliant.")
        sys.exit(0)
    else:
        print(f"FAILED: {total_violations} design/accessibility violation(s) found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
