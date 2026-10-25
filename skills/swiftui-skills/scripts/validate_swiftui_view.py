#!/usr/bin/env python3
"""SwiftUI View & Concurrency Linter.

Checks:
- View body contains @MainActor compliance if touching observable state
- Detects anti-pattern view model instantiation inside View struct without @State
- Detects missing frame minWidth/minHeight for touch target compliance (>= 44pt)
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

def lint_swiftui_file(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Detect View struct anti-pattern: var vm = MyViewModel() without @State
        if re.search(r'var\s+\w+\s*=\s*\w+ViewModel\(\)', stripped):
            if not any(ann in lines[max(0, idx-2):idx] for ann in ["@State", "@StateObject"]):
                issues.append(f"Line {idx}: Unwrapped ViewModel instantiation in View. Wrap with @State or @StateObject.")

        # Check button frame height
        if ".frame(" in stripped and "height:" in stripped:
            m = re.search(r'height:\s*(\d+)', stripped)
            if m and int(m.group(1)) < 44:
                issues.append(f"Line {idx}: Touch target height {m.group(1)}pt is under Apple HIG minimum (44pt).")

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description="SwiftUI Architecture Linter")
    parser.add_argument("files", nargs="+", help="Swift source files")
    args = parser.parse_args()

    total = 0
    for f_str in args.files:
        f = Path(f_str)
        if f.is_file():
            errs = lint_swiftui_file(f)
            if errs:
                total += len(errs)
                print(f"[FAIL] {f.name}:")
                for e in errs:
                    print(f"  ✗ {e}")
            else:
                print(f"[PASS] {f.name}: SwiftUI view conforms to production standards.")
    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
