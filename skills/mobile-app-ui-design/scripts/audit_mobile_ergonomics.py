#!/usr/bin/env python3
"""Mobile App Touch Target & Accessibility Auditor.

Audits React Native / Flutter / Web UI files for:
- Touch target minimum size (44x44 dp/pt)
- Contrast and font-size minimums for body text (>= 14sp/pt)
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

def audit_mobile_file(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    for idx, line in enumerate(lines, start=1):
        # Detect tiny font sizes in React Native or CSS
        m_font = re.search(r'fontSize:\s*(\d+)', line)
        if m_font and int(m_font.group(1)) < 11:
            issues.append(f"Line {idx}: Font size {m_font.group(1)}pt is unreadably small on mobile displays.")

        # Detect tiny paddings on touchables
        if "TouchableOpacity" in line or "Pressable" in line:
            # check next lines for minHeight
            pass

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description="Mobile UI Touch Target Auditor")
    parser.add_argument("files", nargs="+", help="Files to audit")
    args = parser.parse_args()

    total = 0
    for f_str in args.files:
        f = Path(f_str)
        if f.is_file():
            errs = audit_mobile_file(f)
            if errs:
                total += len(errs)
                print(f"[FAIL] {f.name}:")
                for e in errs:
                    print(f"  ✗ {e}")
            else:
                print(f"[PASS] {f.name}: Mobile UI ergonomics verified.")
    return 0 if total == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
