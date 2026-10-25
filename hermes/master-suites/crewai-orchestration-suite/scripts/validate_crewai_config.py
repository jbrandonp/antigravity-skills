#!/usr/bin/env python3
"""CrewAI YAML Configuration Validator.

Audits agents.yaml and tasks.yaml for mandatory fields and anti-patterns.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import yaml

def validate_crewai_config(dir_path: Path) -> list[str]:
    issues = []
    agents_file = dir_path / "config" / "agents.yaml"
    if not agents_file.exists():
        agents_file = dir_path / "agents.yaml"
    
    tasks_file = dir_path / "config" / "tasks.yaml"
    if not tasks_file.exists():
        tasks_file = dir_path / "tasks.yaml"

    if agents_file.exists():
        try:
            agents = yaml.safe_load(agents_file.read_text(encoding="utf-8")) or {}
            for name, cfg in agents.items():
                for req in ["role", "goal", "backstory"]:
                    if not cfg.get(req):
                        issues.append(f"Agent '{name}' missing required field: '{req}'.")
        except Exception as e:
            issues.append(f"agents.yaml parse error: {e}")
    else:
        issues.append("agents.yaml not found.")

    if tasks_file.exists():
        try:
            tasks = yaml.safe_load(tasks_file.read_text(encoding="utf-8")) or {}
            for name, cfg in tasks.items():
                for req in ["description", "expected_output"]:
                    if not cfg.get(req):
                        issues.append(f"Task '{name}' missing required field: '{req}'.")
        except Exception as e:
            issues.append(f"tasks.yaml parse error: {e}")
    else:
        issues.append("tasks.yaml not found.")

    return issues

def main() -> int:
    parser = argparse.ArgumentParser(description="CrewAI Config Validator")
    parser.add_argument("project_dir", nargs="?", default=".", help="Path to CrewAI project root")
    args = parser.parse_args()

    p = Path(args.project_dir)
    print(f"=== Validating CrewAI configuration in: {p.resolve()} ===")
    issues = validate_crewai_config(p)
    if issues:
        print(f"[FAIL] {len(issues)} issue(s) detected:")
        for iss in issues:
            print(f"  ✗ {iss}")
        return 1
    print("[PASS] CrewAI agents and tasks configurations are compliant.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
