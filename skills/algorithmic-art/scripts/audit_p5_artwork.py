#!/usr/bin/env python3
"""
audit_p5_artwork.py — Linter and Quality Gate for p5.js generative art artifacts.
Verifies seeded randomness compliance (Art Blocks / fxhash standard), UI controls,
reproducibility contracts, and potential performance / memory traps.

Usage:
  python audit_p5_artwork.py <path/to/artwork.html> [--json]

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Union


def audit_artwork(html_path: Path) -> Dict[str, Union[str, int, List[Dict[str, str]]]]:
    """Audit a p5.js HTML artwork file against production generative art standards."""
    if not html_path.exists():
        return {
            "file": str(html_path),
            "status": "FAIL",
            "score": 0,
            "issues": [{"severity": "CRITICAL", "message": f"File not found: {html_path}"}]
        }

    try:
        content = html_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {
            "file": str(html_path),
            "status": "FAIL",
            "score": 0,
            "issues": [{"severity": "CRITICAL", "message": f"Read error: {e}"}]
        }

    issues: List[Dict[str, str]] = []

    # 1. CDN Dependency Check
    if "p5" not in content.lower():
        issues.append({
            "severity": "CRITICAL",
            "message": "Missing p5.js library script inclusion in HTML."
        })

    # 2. Seeded Randomness & Determinism
    has_seed_init = bool(re.search(r"randomSeed\s*\(", content) or re.search(r"noiseSeed\s*\(", content))
    if not has_seed_init:
        issues.append({
            "severity": "CRITICAL",
            "message": "Seeded randomness not initialized: missing randomSeed() or noiseSeed()."
        })

    # Forbidden: Math.random() in reproducible generative art rendering logic
    # Exception: Allowed ONLY when picking a random seed value in UI handler (e.g. params.seed = Math.floor(Math.random() ...))
    lines = content.splitlines()
    forbidden_random_lines = []
    for line_idx, line in enumerate(lines, 1):
        if "Math.random" in line:
            stripped = line.strip()
            # Check if it's purely seed generation
            if re.search(r"seed\s*=\s*.*Math\.random", stripped, re.IGNORECASE) or "randomseedandupdate" in stripped.lower():
                continue
            forbidden_random_lines.append((line_idx, stripped))

    if forbidden_random_lines:
        issues.append({
            "severity": "CRITICAL",
            "message": f"Forbidden Math.random() detected in generative logic ({len(forbidden_random_lines)} occurrences, e.g. line {forbidden_random_lines[0][0]}: '{forbidden_random_lines[0][1][:60]}'). Must use seeded p5 random() to guarantee deterministic reproduction."
        })

    # 3. Canvas Creation
    if not re.search(r"createCanvas\s*\(", content):
        issues.append({
            "severity": "CRITICAL",
            "message": "Missing createCanvas() call in setup function."
        })

    # 4. Interactive UI Controls
    required_ui_elements = [
        ("Seed Display", r"id=[\"']seed-value[\"']|class=[\"'].*seed.*[\"']|seed-display"),
        ("Regenerate Button", r"Regenerate|generateNew|redraw\s*\("),
        ("Reset Button", r"Reset|resetDefaults|resetParams"),
        ("Download / Export", r"Download|saveCanvas|exportImage|\.save\s*\(")
    ]

    for label, pattern in required_ui_elements:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append({
                "severity": "WARNING",
                "message": f"Missing or unidentifiable UI control: {label}."
            })

    # 5. Performance & Memory Traps
    # Check for unbounded particle growth: particles.push without splice/filter
    if "particles.push" in content or "elements.push" in content:
        has_pruning = any(p in content for p in ["splice", "filter", "pop", "length >", "length >="])
        if not has_pruning:
            issues.append({
                "severity": "WARNING",
                "message": "Unbounded array growth detected: elements are pushed to an array without clear pruning (splice/filter), which may cause memory leaks during prolonged animation."
            })

    # Check for graphics buffer recreation inside draw loop
    if re.search(r"function\s+draw\s*\([^\)]*\)[\s\S]*createGraphics\s*\(", content):
        issues.append({
            "severity": "WARNING",
            "message": "createGraphics() detected inside draw() loop: creating offscreen buffers every frame causes significant memory allocation spikes."
        })

    critical_count = sum(1 for i in issues if i["severity"] == "CRITICAL")
    warning_count = sum(1 for i in issues if i["severity"] == "WARNING")

    if critical_count > 0:
        score = max(0, 100 - (critical_count * 35 + warning_count * 10))
        status = "FAIL"
    elif warning_count > 0:
        score = max(70, 100 - (warning_count * 10))
        status = "WARN"
    else:
        score = 100
        status = "PASS"

    return {
        "file": str(html_path),
        "status": status,
        "score": score,
        "critical_issues": critical_count,
        "warning_issues": warning_count,
        "issues": issues
    }


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Audit p5.js generative art artifacts for determinism, performance, and UI standards."
    )
    parser.add_argument("file", help="Path to the HTML artwork file.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")

    args = parser.parse_args()
    target_path = Path(args.file).resolve()
    report = audit_artwork(target_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=" * 64)
        print("         P5.JS GENERATIVE ART QUALITY GATE AUDIT         ")
        print("=" * 64)
        print(f"Target File  : {report['file']}")
        print(f"Audit Score  : {report['score']} / 100")
        print(f"Status       : {report['status']}")
        print(f"Issues Found : {len(report['issues'])} ({report['critical_issues']} critical, {report['warning_issues']} warning)")
        print("-" * 64)
        if not report["issues"]:
            print("  [✓] All generative art quality checks passed cleanly.")
        else:
            for issue in report["issues"]:
                badge = "[CRITICAL]" if issue["severity"] == "CRITICAL" else "[WARNING] "
                print(f"  {badge} {issue['message']}")
        print("=" * 64)

    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
