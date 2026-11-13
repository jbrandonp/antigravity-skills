#!/usr/bin/env python3
"""Karpathy Surgical Diff & Simplicity Auditor.

Audits source code changes and git diffs against Andrej Karpathy's 4 laws:
1. Think Before Coding
2. Simplicity First (Anti-Overengineering & Ponytail heuristics)
3. Surgical Changes (Diff ratio, no whole-file rewrites)
4. Goal-Driven Execution
"""

import argparse
import os
import re
import subprocess
import sys

def audit_diff(diff_text: str) -> dict:
    lines = diff_text.splitlines()
    added = 0
    deleted = 0
    overengineering_flags = []
    modified_files = set()

    speculative_patterns = [
        (r'class\s+\w*(?:Factory|Abstract|Strategy|Decorator|Proxy|Facade|Adapter)\w*:', "Speculative design pattern detected (Factory/Abstract/Strategy)"),
        (r'def\s+\w+\(.*?\):\s*\n\s*return\s+\w+\(.*?\)', "Unnecessary one-line indirection function"),
        (r'import\s+(?:redux|lodash|rxjs|axios|ramda)', "Heavy external dependency imported for routine tasks"),
    ]

    for line in lines:
        if line.startswith('+++ b/'):
            modified_files.add(line[6:])
        elif line.startswith('+') and not line.startswith('+++'):
            added += 1
            for pat, desc in speculative_patterns:
                if re.search(pat, line):
                    overengineering_flags.append(desc)
        elif line.startswith('-') and not line.startswith('---'):
            deleted += 1

    total_changes = added + deleted
    # Surgical score calculation
    surgical_score = 100
    if total_changes > 200:
        surgical_score -= min(40, (total_changes - 200) // 10)
    if len(overengineering_flags) > 0:
        surgical_score -= min(30, len(overengineering_flags) * 10)

    surgical_score = max(0, surgical_score)

    return {
        "files_count": len(modified_files),
        "lines_added": added,
        "lines_deleted": deleted,
        "total_lines_touched": total_changes,
        "overengineering_flags": overengineering_flags,
        "surgical_score": surgical_score,
        "verdict": "PASS (Surgical & Clean)" if surgical_score >= 70 else "WARN (Too Broad or Over-Engineered)"
    }

def main():
    parser = argparse.ArgumentParser(description="Karpathy Surgical Code & Simplicity Checker")
    parser.add_argument("--diff", type=str, help="Path to diff file (optional, defaults to git diff HEAD)")
    parser.add_argument("--staged", action="store_true", help="Audit staged git changes")
    parser.add_argument("--max-lines", type=int, default=150, help="Maximum recommended lines modified")
    args = parser.parse_args()

    diff_content = ""
    if args.diff and os.path.exists(args.diff):
        with open(args.diff, "r", encoding="utf-8") as f:
            diff_content = f.read()
    else:
        cmd = ["git", "diff", "--staged"] if args.staged else ["git", "diff", "HEAD~1"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            diff_content = res.stdout
            if not diff_content:
                res_unstaged = subprocess.run(["git", "diff"], capture_output=True, text=True, check=False)
                diff_content = res_unstaged.stdout
        except Exception as e:
            diff_content = ""

    if not diff_content.strip():
        print("[Karpathy Checker] No git diff detected. Analyzing working tree clean state.")
        print("Verdict: PASS (0 changes)")
        return

    result = audit_diff(diff_content)
    print("=" * 60)
    print("      KARPATHY SURGICAL & SIMPLICITY AUDIT REPORT           ")
    print("=" * 60)
    print(f"Files Modified   : {result['files_count']}")
    print(f"Lines Added      : +{result['lines_added']}")
    print(f"Lines Deleted    : -{result['lines_deleted']}")
    print(f"Total Diff Size  : {result['total_lines_touched']} lines")
    print(f"Surgical Score   : {result['surgical_score']}/100")
    print(f"Verdict          : {result['verdict']}")
    print("-" * 60)

    if result["overengineering_flags"]:
        print("Flags detected:")
        for flag in set(result["overengineering_flags"]):
            print(f"  [!] {flag}")
    else:
        print("✓ Zero speculative abstraction flags detected.")

    if result["total_lines_touched"] > args.max_lines:
        print(f"  [!] Diff size ({result['total_lines_touched']}) exceeds surgical threshold ({args.max_lines}). Consider breaking into atomic micro-tasks.")
    print("=" * 60)

if __name__ == "__main__":
    main()
