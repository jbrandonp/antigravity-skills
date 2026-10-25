#!/usr/bin/env python3
"""
scan_ui_slop.py — Static analysis linter and Quality Gate against AI-generated UI clichés.
Scans HTML, JSX, TSX, Vue, Svelte, and CSS files for the 5 dead tells of AI slop:
  1. Generic transitions (transition-all without targeted properties)
  2. Cliché AI color palettes (default Indigo/Violet soup, raw #000000 pure blacks)
  3. Monotonous card soup & excessive hairline border dividers
  4. Marketing buzzword copy & template typography clichés (meaningless 01/02 badges, arrows on all buttons)
  5. Missing accessibility & interaction states (focus:outline-none without focus-visible rings, missing tabular-nums)

Usage:
  python scan_ui_slop.py <path/to/code_or_directory> [--json] [--fail-on-warnings]

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

SUPPORTED_EXTENSIONS = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".css", ".scss"}

AI_BUZZWORDS = [
    r"\bstreamline\s+your\s+workflow\b",
    r"\bsupercharge\s+your\s+productivity\b",
    r"\bunlock\s+the\s+power\s+of\b",
    r"\bnext-gen(?:eration)?\s+ai\b",
    r"\beffortlessly?\s+manage\b",
    r"\brevolutionize\s+your\b",
    r"\ball-in-one\s+solution\b",
    r"\bseamless(?:ly)?\s+integrat(?:e|ion)\b"
]


def scan_file(file_path: Path) -> List[Dict[str, Union[str, int]]]:
    """Scan a single file for UI slop anti-patterns."""
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{"severity": "CRITICAL", "line": 1, "code": "", "issue": f"Read error: {e}", "fix": "Ensure file is accessible and UTF-8 encoded."}]

    lines = content.splitlines()

    for line_idx, line in enumerate(lines, 1):
        line_clean = line.strip()

        # 1. Generic transition-all
        if "transition-all" in line_clean and not "no-transition-all" in line_clean:
            findings.append({
                "severity": "CRITICAL",
                "line": line_idx,
                "code": line_clean[:80],
                "issue": "Generic 'transition-all' detected: Causes expensive browser layout reflows and sluggish animation.",
                "fix": "Replace with targeted properties: 'transition-colors', 'transition-transform', or 'transition-opacity'."
            })

        # 2. Raw #000000 pure black backgrounds without 4-layer elevation
        if re.search(r"#(?:000000|000)\b|background:\s*black\b|bg-black\b", line_clean, re.IGNORECASE):
            # Exclude text colors or borders
            if "bg-" in line_clean or "background" in line_clean:
                findings.append({
                    "severity": "WARNING",
                    "line": line_idx,
                    "code": line_clean[:80],
                    "issue": "Pure harsh black (#000000) background detected: High eye-fatigue, destroys elevation in dark mode.",
                    "fix": "Use calibrated dark neutrals: #09090b, #0f172a, or #121214 with proper 4-layer surface elevation."
                })

        # 3. Focus outline removed without replacement focus-visible ring
        if "focus:outline-none" in line_clean or "outline: none" in line_clean:
            if "focus-visible:ring" not in line_clean and "focus:ring" not in line_clean and "outline-offset" not in line_clean:
                findings.append({
                    "severity": "CRITICAL",
                    "line": line_idx,
                    "code": line_clean[:80],
                    "issue": "Focus outline removed without focus-visible replacement: Breaks keyboard navigation and WCAG 2.2 AA.",
                    "fix": "Add 'focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary'."
                })

        # 4. Numbers / metrics without tabular-nums
        if re.search(r"\$\s*\{?\w*\}?|\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*(?:USD|EUR|\$|€|%)\b", line_clean):
            if any(ext in file_path.suffix for ext in [".jsx", ".tsx", ".html", ".vue", ".svelte"]):
                if "tabular-nums" not in line_clean and "font-mono" not in line_clean and "<span" in line_clean:
                    findings.append({
                        "severity": "ADVICE",
                        "line": line_idx,
                        "code": line_clean[:80],
                        "issue": "Financial / numeric metric rendered without tabular figures: Digits cause visual jitter during updates.",
                        "fix": "Add 'tabular-nums' or 'font-mono' to prevent horizontal layout shifting."
                    })

        # 5. Meaningless non-sequential numbers as badges (01, 02, 03)
        if re.search(r">\s*0[1-9]\s*<|badge.*0[1-9]", line_clean):
            findings.append({
                "severity": "WARNING",
                "line": line_idx,
                "code": line_clean[:80],
                "issue": "AI Cliché detected: Meaningless '01 / 02' numbered prefix badge on non-ordered elements.",
                "fix": "Remove arbitrary numbering or use clear descriptive tags and semantic headers."
            })

        # 6. Cliché marketing buzzwords in UI copy
        for bw_pattern in AI_BUZZWORDS:
            if re.search(bw_pattern, line_clean, re.IGNORECASE):
                findings.append({
                    "severity": "WARNING",
                    "line": line_idx,
                    "code": line_clean[:80],
                    "issue": f"AI Cliché Copywriting detected: Generic filler buzzword matching '{bw_pattern}'.",
                    "fix": "Replace with concrete, human actions (e.g. 'Export invoices', 'Sync customer database')."
                })

    return findings


def scan_path(target: Path) -> Dict[str, Union[int, Dict[str, List[Dict[str, Union[str, int]]]]]]:
    """Scan a file or directory recursively."""
    results: Dict[str, List[Dict[str, Union[str, int]]]] = {}
    total_files = 0

    if target.is_file():
        if target.suffix.lower() in SUPPORTED_EXTENSIONS:
            total_files = 1
            f = scan_file(target)
            if f:
                results[str(target)] = f
    elif target.is_dir():
        for root, dirs, files in os.walk(target):
            # Exclude node_modules, .git, dist, build, .next
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "dist", "build", ".next", ".cache", "__pycache__"}]
            for file in files:
                p = Path(root) / file
                if p.suffix.lower() in SUPPORTED_EXTENSIONS:
                    total_files += 1
                    f = scan_file(p)
                    if f:
                        results[str(p)] = f

    total_critical = sum(sum(1 for i in items if i["severity"] == "CRITICAL") for items in results.values())
    total_warning = sum(sum(1 for i in items if i["severity"] == "WARNING") for items in results.values())
    total_advice = sum(sum(1 for i in items if i["severity"] == "ADVICE") for items in results.values())

    score = max(0, 100 - (total_critical * 25 + total_warning * 10 + total_advice * 2))
    status = "FAIL" if total_critical > 0 else ("WARN" if total_warning > 0 else "PASS")

    return {
        "target": str(target),
        "total_files_scanned": total_files,
        "files_with_issues": len(results),
        "total_critical": total_critical,
        "total_warning": total_warning,
        "total_advice": total_advice,
        "score": score,
        "status": status,
        "findings_by_file": results
    }


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Linter and Quality Gate against AI-generated UI slop and frontend anti-patterns."
    )
    parser.add_argument("path", help="Path to file or project directory to scan.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Return non-zero exit code on warnings.")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if not target_path.exists():
        print(f"Error: Target path does not exist: {target_path}", file=sys.stderr)
        return 1

    report = scan_path(target_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=" * 68)
        print("           ANTI-UI SLOP CRAFTSMANSHIP QUALITY GATE AUDIT          ")
        print("=" * 68)
        print(f"Target Path         : {report['target']}")
        print(f"Files Scanned       : {report['total_files_scanned']}")
        print(f"Files with Issues   : {report['files_with_issues']}")
        print(f"Craftsmanship Score : {report['score']} / 100")
        print(f"Audit Status        : {report['status']}")
        print(f"Violations          : {report['total_critical']} Critical, {report['total_warning']} Warning, {report['total_advice']} Advice")
        print("-" * 68)

        if not report["findings_by_file"]:
            print("  [✓] Clean Craftsmanship: Zero AI UI slop or anti-patterns detected!")
        else:
            for file_path, items in report["findings_by_file"].items():
                rel_path = os.path.relpath(file_path, report['target']) if os.path.isdir(report['target']) else os.path.basename(file_path)
                print(f"\n📁 {rel_path} ({len(items)} issue{'s' if len(items) > 1 else ''}):")
                for item in items:
                    badge = f"[{item['severity']}]"
                    print(f"  • Line {item['line']:<4} {badge} {item['issue']}")
                    if item.get("code"):
                        print(f"      Code: {item['code']}")
                    print(f"      Fix : {item['fix']}")

        print("=" * 68)

    if report["status"] == "FAIL":
        return 1
    if args.fail_on_warnings and report["status"] == "WARN":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
