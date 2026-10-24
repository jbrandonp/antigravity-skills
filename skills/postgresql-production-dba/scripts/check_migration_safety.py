#!/usr/bin/env python3
"""PostgreSQL Production Migration Safety Linter.

Audits SQL migration files for dangerous DDL operations:
- CREATE INDEX without CONCURRENTLY (table locking)
- ADD COLUMN NOT NULL without DEFAULT
- Missing lock_timeout setting
- Non-SARGable LOWER/DATE wrapping in WHERE clauses
- Irreversible DROP operations
"""

import argparse
import re
import sys
from pathlib import Path


class MigrationSafetyAuditor:
    def __init__(self) -> None:
        self.violations: list[dict[str, str | int]] = []

    def audit_file(self, file_path: Path) -> list[dict[str, str | int]]:
        self.violations = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return [{"severity": "FAIL", "line": 0, "msg": f"Cannot read file: {e}"}]

        lines = content.splitlines()

        # Check for lock_timeout
        has_lock_timeout = any("lock_timeout" in line.lower() for line in lines)
        if not has_lock_timeout and len(lines) > 2:
            self.violations.append({
                "severity": "WARN",
                "line": 1,
                "msg": "Missing 'SET lock_timeout' setting at transaction start. Risks long lock queues."
            })

        for idx, line in enumerate(lines, 1):
            clean_line = line.strip()
            if clean_line.startswith("--") or not clean_line:
                continue

            # 1. Non-concurrent index creation
            if re.search(r"\bCREATE\s+(?:UNIQUE\s+)?INDEX\s+(?!CONCURRENTLY\b)", clean_line, re.IGNORECASE):
                self.violations.append({
                    "severity": "FAIL",
                    "line": idx,
                    "msg": "CREATE INDEX without CONCURRENTLY locks the table for writes. Use 'CREATE INDEX CONCURRENTLY'."
                })

            # 2. Add column NOT NULL without DEFAULT
            if re.search(r"\bADD\s+COLUMN\s+.*\bNOT\s+NULL\b", clean_line, re.IGNORECASE):
                if not re.search(r"\bDEFAULT\b", clean_line, re.IGNORECASE):
                    self.violations.append({
                        "severity": "FAIL",
                        "line": idx,
                        "msg": "ADD COLUMN NOT NULL without DEFAULT will fail if table has existing rows."
                    })

            # 3. Irreversible DROPs
            if re.search(r"\bDROP\s+(?:TABLE|COLUMN)\b", clean_line, re.IGNORECASE):
                self.violations.append({
                    "severity": "WARN",
                    "line": idx,
                    "msg": "Destructive DROP operation. Verify backward-compatibility and data migration first."
                })

            # 4. Non-SARGable WHERE clause
            if re.search(r"\bWHERE\s+LOWER\s*\(", clean_line, re.IGNORECASE):
                self.violations.append({
                    "severity": "WARN",
                    "line": idx,
                    "msg": "Non-SARGable 'WHERE LOWER(...)' call. Negates B-Tree index unless functional index exists."
                })

        return self.violations


def main() -> None:
    parser = argparse.ArgumentParser(description="PostgreSQL Migration Safety Auditor")
    parser.add_argument("path", help="Path to SQL file or directory of migrations")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    files = [target] if target.is_file() else sorted(target.glob("**/*.sql"))
    if not files:
        print(f"No SQL files found in '{target}'.")
        sys.exit(0)

    auditor = MigrationSafetyAuditor()
    total_fails = 0
    total_warns = 0

    print("=" * 65)
    print(" PostgreSQL Zero-Downtime Migration Safety Audit")
    print("=" * 65)

    for f in files:
        issues = auditor.audit_file(f)
        if not issues:
            print(f"[PASS] {f.name}")
            continue

        fails = [i for i in issues if i["severity"] == "FAIL"]
        warns = [i for i in issues if i["severity"] == "WARN"]
        total_fails += len(fails)
        total_warns += len(warns)

        status = "[FAIL]" if fails else "[WARN]"
        print(f"{status} {f.name} ({len(fails)} errors, {len(warns)} warnings):")
        for i in issues:
            print(f"  Line {i['line']}: [{i['severity']}] {i['msg']}")

    print("-" * 65)
    print(f"Summary: {len(files)} files checked | Errors: {total_fails} | Warnings: {total_warns}")
    if total_fails > 0:
        print("Verdict: REJECTED (Unsafe migration patterns detected)")
        sys.exit(1)
    else:
        print("Verdict: APPROVED (Migration patterns compliant with zero-downtime)")
        sys.exit(0)


if __name__ == "__main__":
    main()
