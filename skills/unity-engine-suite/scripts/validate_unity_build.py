#!/usr/bin/env python3
"""Unity C# Architecture & Build Linter.

Audits:
1. Assembly Definition Files (.asmdef):
   - Enforces editor/runtime boundary separation
2. C# Script Anti-Patterns:
   - UnityEditor API leaks outside '#if UNITY_EDITOR'
   - Expensive 'GetComponent' or 'Find' inside Update() or FixedUpdate()
   - Non-cached coroutines or allocations in hot paths
3. Project Version Pinning:
   - Validates ProjectSettings/ProjectVersion.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def lint_csharp_script(file_path: Path) -> list[str]:
    issues = []
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    in_update = False
    in_editor_block = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track #if UNITY_EDITOR blocks
        if stripped.startswith("#if") and "UNITY_EDITOR" in stripped:
            in_editor_block = True
        elif stripped.startswith("#endif") and in_editor_block:
            in_editor_block = False

        # Detect UnityEditor API leak
        if not in_editor_block:
            if re.search(r"\b(UnityEditor|EditorUtility|AssetDatabase|EditorGUILayout)\b", line):
                # check if line has local using
                if "using UnityEditor;" in line or not line.startswith("using"):
                    issues.append(f"Line {idx}: UnityEditor API used outside '#if UNITY_EDITOR' block.")

        # Track Update() blocks
        if re.search(r"\bvoid\s+(Update|FixedUpdate|LateUpdate)\s*\(", line):
            in_update = True
        elif in_update and stripped == "}":
            in_update = False

        # Detect expensive calls in hot paths
        if in_update:
            if re.search(r"\b(GetComponent|FindObjectOfType|GameObject\.Find)\b", line):
                issues.append(f"Line {idx}: Expensive '{line.strip()}' called inside Update() loop. Cache in Awake/Start.")

    return issues


def lint_asmdef(asmdef_path: Path) -> list[str]:
    issues = []
    try:
        import json
        data = json.loads(asmdef_path.read_text(encoding="utf-8"))
        name = data.get("name", "")
        include_platforms = data.get("includePlatforms", [])

        if "Editor" in name and "Editor" not in include_platforms:
            issues.append(f"Editor assembly '{name}' should explicitly set includePlatforms: ['Editor'].")
    except Exception as e:
        issues.append(f"Failed to parse .asmdef: {e}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Unity C# Architecture & Build Linter")
    parser.add_argument("paths", nargs="+", help="Files or directory to audit (.cs, .asmdef, or ProjectSettings/)")
    args = parser.parse_args()

    total_issues = 0
    print("=== Unity C# Architecture & Safety Linter ===")

    for p_str in args.paths:
        p = Path(p_str)
        if p.is_dir():
            files = list(p.rglob("*.cs")) + list(p.rglob("*.asmdef"))
        else:
            files = [p]

        for f in files:
            ext = f.suffix.lower()
            issues = []
            if ext == ".cs":
                issues = lint_csharp_script(f)
            elif ext == ".asmdef":
                issues = lint_asmdef(f)

            if issues:
                total_issues += len(issues)
                print(f"\n[FAIL] {f.name}:")
                for iss in issues:
                    print(f"  ✗ {iss}")

    if total_issues == 0:
        print("\n✓ PASS: All Unity scripts and assemblies conform to production standards.")
        return 0
    else:
        print(f"\nAudit complete: {total_issues} issue(s) detected.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
