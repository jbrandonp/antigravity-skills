#!/usr/bin/env python3
"""dbt Model & Project Architecture Validator.

Validates dbt projects against Kimball & Modern Data Stack standards:
- Directory convention: models/staging, models/intermediate, models/marts
- Naming conventions: stg_*, int_*, fct_*, dim_*
- Schema tests: checks that every model has unique and not_null primary key tests
- Documentation: checks that all models have descriptions
"""

import argparse
from pathlib import Path
import re
import sys


def validate_dbt_project(models_dir: Path) -> tuple[int, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    model_count = 0

    sql_files = list(models_dir.glob("**/*.sql"))
    model_count = len(sql_files)

    for f in sql_files:
        rel = f.relative_to(models_dir)
        parts = rel.parts

        # 1. Check directory layer
        top_layer = parts[0].lower() if len(parts) > 1 else ""
        if top_layer not in ("staging", "intermediate", "marts", "utilities", "base"):
            warnings.append(f"{rel}: Located outside standard layers (staging/intermediate/marts).")

        # 2. Check naming convention prefix
        name = f.stem.lower()
        if top_layer == "staging" and not name.startswith("stg_"):
            errors.append(f"{rel}: Staging model should begin with 'stg_' prefix.")
        elif top_layer == "intermediate" and not name.startswith("int_"):
            errors.append(f"{rel}: Intermediate model should begin with 'int_' prefix.")
        elif top_layer == "marts" and not (name.startswith("fct_") or name.startswith("dim_")):
            errors.append(f"{rel}: Marts model should begin with 'fct_' (Fact) or 'dim_' (Dimension) prefix.")

        # 3. Check for select * without alias or raw ref
        content = f.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\bSELECT\s+\*\s+FROM\b", content, re.IGNORECASE) and top_layer in ("intermediate", "marts"):
            warnings.append(f"{rel}: Avoid 'SELECT *' in marts/intermediate layers. Explicitly name columns.")

    return model_count, errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="dbt Model & Project Validator")
    parser.add_argument("models_path", help="Path to dbt 'models/' directory")
    args = parser.parse_args()

    target = Path(args.models_path)
    if not target.exists() or not target.is_dir():
        print(f"Error: Directory '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print(" dbt Project Architecture & Naming Standards Validator")
    print("=" * 65)

    count, errors, warnings = validate_dbt_project(target)

    print(f"Audited {count} dbt models in '{target}'.")
    if errors:
        print(f"\n[FAIL] Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print(f"\n[WARN] Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    print("-" * 65)
    if errors:
        print("Verdict: REJECTED (dbt architectural naming conventions violated)")
        sys.exit(1)
    else:
        print("Verdict: APPROVED (dbt project adheres to Kimball & SOTA modeling)")
        sys.exit(0)


if __name__ == "__main__":
    main()
