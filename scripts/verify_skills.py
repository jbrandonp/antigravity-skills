#!/usr/bin/env python3
"""Comprehensive Quality Gate & Verification Engine for Antigravity Super Suite.

Audits:
1. Skills Integrity (SKILL.md, YAML frontmatters, name match)
2. Plugins Integrity (plugin.json, metadata)
3. Model Context Protocol (MCP) Schemas (JSON syntax & structure)
4. Companion Python Scripts (AST compilation & syntax safety)
5. Repository Cleanliness (Zero __pycache__ / .pyc bytecode pollution)
"""

import ast
import json
import os
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGINS_DIR = ROOT / "plugins"
MCP_DIR = ROOT / "mcp"

errors = []
warnings = []

print("==================================================================")
print("       ANTIGRAVITY SUPER SUITE — MASTER QUALITY GATE AUDIT        ")
print("==================================================================")

# --- 1. Audit Skills ---
total_skills = 0
skill_errors = 0
print("\n[1/5] Auditing Production Skills...")
if SKILLS_DIR.exists():
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        total_skills += 1
        sk = d / "SKILL.md"
        if not sk.exists():
            errors.append(f"Skill '{d.name}': Missing SKILL.md")
            skill_errors += 1
            continue
        txt = sk.read_text(encoding="utf-8", errors="replace")
        if not txt.startswith("---"):
            errors.append(f"Skill '{d.name}': Missing opening frontmatter '---'")
            skill_errors += 1
            continue
        name_m = re.search(
            r"^name:\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?", txt, re.MULTILINE
        )
        desc_m = re.search(r"^description:\s*(.+)", txt, re.MULTILINE)
        if not name_m or not desc_m:
            errors.append(f"Skill '{d.name}': Missing 'name' or 'description'")
            skill_errors += 1
        elif name_m.group(1).strip() != d.name:
            errors.append(
                f"Skill '{d.name}': Folder name does not match frontmatter name '{name_m.group(1).strip()}'"
            )
            skill_errors += 1
    print(f"  ✓ {total_skills} skills audited ({skill_errors} errors)")
else:
    errors.append("Missing 'skills/' directory!")

# --- 2. Audit Plugins ---
total_plugins = 0
plugin_errors = 0
print("\n[2/5] Auditing Plugins & Metadata...")
if PLUGINS_DIR.exists():
    for p in sorted(PLUGINS_DIR.iterdir()):
        if not p.is_dir():
            continue
        total_plugins += 1
        pjson = p / "plugin.json"
        if not pjson.exists():
            errors.append(f"Plugin '{p.name}': Missing plugin.json")
            plugin_errors += 1
            continue
        try:
            data = json.loads(pjson.read_text(encoding="utf-8"))
            if "name" not in data or "description" not in data:
                errors.append(
                    f"Plugin '{p.name}': plugin.json missing required 'name' or 'description'"
                )
                plugin_errors += 1
        except Exception as e:
            errors.append(
                f"Plugin '{p.name}': Invalid JSON in plugin.json ({e})"
            )
            plugin_errors += 1
    print(f"  ✓ {total_plugins} plugins audited ({plugin_errors} errors)")
else:
    warnings.append("No 'plugins/' directory found.")

# --- 3. Audit MCP Schemas ---
total_mcp_schemas = 0
mcp_errors = 0
print("\n[3/5] Auditing Model Context Protocol (MCP) Schemas...")
if MCP_DIR.exists():
    for srv in sorted(MCP_DIR.iterdir()):
        if not srv.is_dir():
            continue
        for jf in srv.glob("*.json"):
            total_mcp_schemas += 1
            try:
                json.loads(jf.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(
                    f"MCP Schema '{srv.name}/{jf.name}': Invalid JSON ({e})"
                )
                mcp_errors += 1
    print(
        f"  ✓ {total_mcp_schemas} MCP tool schemas audited ({mcp_errors} errors)"
    )
else:
    warnings.append("No 'mcp/' directory found.")

# --- 4. Audit Python Companion Scripts Syntax ---
total_py = 0
py_errors = 0
print("\n[4/5] Auditing Python Companion Scripts Syntax...")
for py_file in ROOT.rglob("*.py"):
    # skip .git or scratch
    if ".git" in py_file.parts or "scratch" in py_file.parts:
        continue
    total_py += 1
    try:
        code = py_file.read_text(encoding="utf-8", errors="replace")
        ast.parse(code, filename=str(py_file))
    except SyntaxError as se:
        errors.append(
            f"Python Script '{py_file.relative_to(ROOT)}': SyntaxError on line {se.lineno} ({se.msg})"
        )
        py_errors += 1
print(f"  ✓ {total_py} Python scripts parsed ({py_errors} errors)")

# --- 5. Cleanliness Check (No __pycache__ or .pyc) ---
print("\n[5/5] Checking Repository Cleanliness...")
pycache_dirs = [p for p in ROOT.rglob("__pycache__") if ".git" not in p.parts]
pyc_files = [p for p in ROOT.rglob("*.pyc") if ".git" not in p.parts]

if pycache_dirs or pyc_files:
    errors.append(
        f"Repository contains {len(pycache_dirs)} __pycache__ dirs and {len(pyc_files)} .pyc files. Purge before commit!"
    )
    print(
        f"  ✗ Found {len(pycache_dirs)} __pycache__ dirs and {len(pyc_files)} .pyc files"
    )
else:
    print("  ✓ Zero bytecode pollution detected (__pycache__ / .pyc clean)")

print("\n==================================================================")
if errors:
    print(f"FAILED: {len(errors)} quality gate error(s) detected:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print(
        f"SUCCESS: All {total_skills} skills, {total_plugins} plugins, {total_mcp_schemas} MCP schemas, and {total_py} scripts passed!"
    )
    sys.exit(0)
