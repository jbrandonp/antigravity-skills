import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

root = Path(__file__).resolve().parent.parent
skills_dir = root / "skills"
plugins_dir = root / "plugins"

errors = []
total_skills = 0

print("=== Verifying Skills Frontmatters ===")
for d in sorted(skills_dir.iterdir()):
    if not d.is_dir():
        continue
    total_skills += 1
    sk = d / "SKILL.md"
    if not sk.exists():
        errors.append(f"{d.name}: Missing SKILL.md")
        continue
    lines = sk.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{d.name}: Missing opening frontmatter '---'")
        continue
    has_name = any(l.startswith("name:") for l in lines[1:25])
    has_desc = any(l.startswith("description:") for l in lines[1:25])
    if not has_name or not has_desc:
        errors.append(f"{d.name}: Missing 'name' or 'description' in YAML frontmatter")

print(f"Total skills audited: {total_skills}")
if errors:
    print(f"Errors found ({len(errors)}):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("[OK] All skills have valid YAML frontmatters!")
