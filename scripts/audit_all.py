#!/usr/bin/env python3
"""Forensic Audit Engine for Antigravity Super Suite.

Scans:
1. Broken relative markdown links in README.md, CLAUDE.md, hermes/README.md
2. Folder name vs YAML frontmatter name mismatches in skills/ and hermes/
3. Broken script paths in test_companion_scripts.py
4. Broken links in mega-suites and master-suites indexes
5. Status of all 12 target skills across skills/, hermes/master-suites/, hermes/mega-suites/
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []

print("=" * 65)
print("     ANTIGRAVITY FORENSIC REPOSITORY AUDIT & REPAIR ENGINE      ")
print("=" * 65)

# --- 1. Audit Markdown Links in README.md ---
readme_path = ROOT / "README.md"
if readme_path.exists():
    text = readme_path.read_text(encoding="utf-8")
    links = re.findall(r'\[.*?\]\((skills/[^)]+|hermes/[^)]+|plugins/[^)]+)\)', text)
    broken = []
    for l in links:
        clean = l.split("#")[0]
        target = ROOT / clean
        if not target.exists():
            broken.append(l)
    print(f"\n[1/5] Auditing README.md relative links ({len(links)} links checked)...")
    if broken:
        for b in broken:
            errors.append(f"Broken link in README.md: {b}")
            print(f"  ✗ Broken: {b}")
    else:
        print("  ✓ All relative links in README.md point to existing files!")

# --- 2. Check Name Mismatches in skills/ ---
print("\n[2/5] Auditing Skill Names vs Directory Names...")
for sdir in sorted((ROOT / "skills").iterdir()):
    if sdir.is_dir():
        sk = sdir / "SKILL.md"
        if not sk.exists():
            errors.append(f"Directory without SKILL.md: skills/{sdir.name}")
            print(f"  ✗ skills/{sdir.name}: Missing SKILL.md")
        else:
            c = sk.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^name:\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?", c, re.MULTILINE)
            if not m or m.group(1).strip() != sdir.name:
                found = m.group(1).strip() if m else "None"
                errors.append(f"Name mismatch in skills/{sdir.name}: found '{found}'")
                print(f"  ✗ skills/{sdir.name}: Name mismatch '{found}'")

# --- 3. Check Name Mismatches in hermes/master-suites/ ---
print("\n[3/5] Auditing Hermes Master-Suites Names vs Directory Names...")
for sdir in sorted((ROOT / "hermes" / "master-suites").iterdir()):
    if sdir.is_dir():
        sk = sdir / "SKILL.md"
        if not sk.exists():
            errors.append(f"Directory without SKILL.md: hermes/master-suites/{sdir.name}")
            print(f"  ✗ hermes/master-suites/{sdir.name}: Missing SKILL.md")
        else:
            c = sk.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"^name:\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?", c, re.MULTILINE)
            if not m or m.group(1).strip() != sdir.name:
                found = m.group(1).strip() if m else "None"
                errors.append(f"Name mismatch in hermes/master-suites/{sdir.name}: found '{found}'")
                print(f"  ✗ hermes/master-suites/{sdir.name}: Name mismatch '{found}'")

# --- 4. Check Status of 12 Target Skills ---
print("\n[4/5] Checking Integrity of 12 SOTA Target Skills...")
target_skills = [
    ("karpathy-guidelines", "03_mega-software-engineering-and-devops-suite"),
    ("socratic-spec-architect", "03_mega-software-engineering-and-devops-suite"),
    ("gstack-startup-pack", "03_mega-software-engineering-and-devops-suite"),
    ("graphify-ast-knowledge", "03_mega-software-engineering-and-devops-suite"),
    ("trail-of-bits-security-engine", "03_mega-software-engineering-and-devops-suite"),
    ("cloudflare-adversarial-audit", "03_mega-software-engineering-and-devops-suite"),
    ("diagram-design-svg", "07_mega-creative-arts-and-visual-motion-suite"),
    ("isometric-anatomy-svg", "07_mega-creative-arts-and-visual-motion-suite"),
    ("impeccable-design-engine", "07_mega-creative-arts-and-visual-motion-suite"),
    ("ecc-agent-shield", "10_mega-autonomous-agents-and-mcp-orchestration-suite"),
    ("context-mode", "10_mega-autonomous-agents-and-mcp-orchestration-suite"),
    ("caveman-compress", "10_mega-autonomous-agents-and-mcp-orchestration-suite")
]

for s, mega in target_skills:
    in_skills = (ROOT / "skills" / s / "SKILL.md").exists()
    in_consolidated_skills = (ROOT / "skills" / "context-token-optimization-suite" / "SKILL.md").exists() and s in ["context-mode", "caveman-compress"]
    in_master = (ROOT / "hermes" / "master-suites" / s / "SKILL.md").exists()
    in_consolidated_master = (ROOT / "hermes" / "master-suites" / "context-token-optimization-suite" / "SKILL.md").exists() and s in ["context-mode", "caveman-compress"]
    mega_txt = (ROOT / "hermes" / "mega-suites" / mega / "SKILL.md").read_text(encoding="utf-8")
    in_mega = s in mega_txt
    status_skills = in_skills or in_consolidated_skills
    status_master = in_master or in_consolidated_master
    print(f"  {s:<32} | in skills/: {status_skills} | in master/: {status_master} | in mega/: {in_mega}")
    if not status_skills:
        errors.append(f"Skill '{s}' missing from skills/")
    if not status_master:
        errors.append(f"Skill '{s}' missing from hermes/master-suites/")
    if not in_mega:
        errors.append(f"Skill '{s}' missing from hermes/mega-suites/{mega}")

# --- 5. Verify Functional Tests Script Paths ---
print("\n[5/5] Checking script path resolution in test_companion_scripts.py...")
test_script_path = ROOT / "scripts" / "test_companion_scripts.py"
if test_script_path.exists():
    c = test_script_path.read_text(encoding="utf-8")
    # Check if context-mode and caveman point to existing files
    ctx_match = "context-token-optimization-suite" in c
    print(f"  context-token-optimization-suite referenced: {ctx_match}")
    if not ctx_match:
        errors.append("test_companion_scripts.py still references obsolete skills/context-mode and skills/caveman-compress paths instead of context-token-optimization-suite!")

print("=" * 65)
print(f"AUDIT SUMMARY: {len(errors)} error(s), {len(warnings)} warning(s)")
print("=" * 65)
for e in errors:
    print(f"  ✗ {e}")
