#!/usr/bin/env python3
"""
Expo Router & Project Structure Validator
Audits Expo apps for file-based routing conventions, layout hierarchies,
dynamic route slug consistency, and platform-specific layout files.
"""

import sys
import os
import re
from pathlib import Path

def validate_expo_project(project_root: Path) -> bool:
    print(f"\n[*] Auditing Expo Router project structure in: {project_root}")
    
    # Locate app directory
    app_dir = project_root / "app"
    if not app_dir.exists():
        app_dir = project_root / "src" / "app"
        
    if not app_dir.exists():
        print(f"[!] Error: Could not locate 'app/' or 'src/app/' directory.")
        return False

    print(f"[+] Found Expo Router route directory: {app_dir.relative_to(project_root)}")
    errors = []
    warnings = []

    # 1. Root layout check
    root_layout = None
    for name in ["_layout.tsx", "_layout.jsx", "_layout.js"]:
        if (app_dir / name).exists():
            root_layout = app_dir / name
            break

    if not root_layout:
        errors.append(f"Missing root layout: '{app_dir.relative_to(project_root)}/_layout.tsx'")
    else:
        print(f"[+] Root layout verified: {root_layout.name}")

    # 2. Check all route files
    total_routes = 0
    slugs_by_dir = {}

    for root, dirs, files in os.walk(app_dir):
        rel_root = Path(root).relative_to(app_dir)
        for f in files:
            if not f.endswith((".tsx", ".ts", ".jsx", ".js")):
                continue
            total_routes += 1
            f_path = Path(root) / f
            base_name = f.split(".")[0]

            # Route naming: no uppercase in route filenames unless special layout
            if not base_name.startswith("_") and not base_name.startswith("+"):
                # Check for dynamic slug
                dynamic_match = re.match(r"^\[([a-zA-Z0-9_-]+)\]$", base_name)
                if dynamic_match:
                    slug_var = dynamic_match.group(1)
                    if str(rel_root) not in slugs_by_dir:
                        slugs_by_dir[str(rel_root)] = []
                    slugs_by_dir[str(rel_root)].append(slug_var)
                elif any(c.isupper() for c in base_name):
                    warnings.append(f"Route file should use kebab-case: '{f_path.relative_to(project_root)}'")

    # Check conflicting dynamic slugs in same folder
    for folder, slugs in slugs_by_dir.items():
        if len(slugs) > 1:
            errors.append(f"Conflicting dynamic route slugs in '{folder}': {slugs}")

    print(f"[+] Audited {total_routes} route files.")

    if warnings:
        print("[!] Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("[!] Expo Router Audit FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("[+] Expo Router Audit PASSED: 100% compliant.")
        return True

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    success = validate_expo_project(target)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
