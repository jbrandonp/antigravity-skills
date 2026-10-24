#!/usr/bin/env python3
"""
WAT Pipeline Scaffolder & Architecture Validator
Enforces the 3-layer WAT paradigm (Workflows, Agents, Tools) for autonomous AI systems.
"""

import sys
import os
import json
import argparse
from pathlib import Path

def scaffold_wat(target_dir: Path, pipeline_name: str) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Create canonical directories
    (target_dir / "workflows").mkdir(exist_ok=True)
    (target_dir / "tools").mkdir(exist_ok=True)
    (target_dir / "work").mkdir(exist_ok=True)
    (target_dir / "assets").mkdir(exist_ok=True)
    
    # Create .gitignore ensuring secrets and work artifacts are ignored
    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(".env\nwork/\n__pycache__/\n*.pyc\n", encoding="utf-8")
        print("[+] Created .gitignore (protecting secrets and intermediate work)")
        
    # Create .env.example
    env_example = target_dir / ".env.example"
    if not env_example.exists():
        env_example.write_text("# WAT Environment Secrets\nAPI_KEY=your_key_here\nLOG_LEVEL=INFO\n", encoding="utf-8")
        print("[+] Created .env.example")
        
    # Create Workflow SOP
    sop_path = target_dir / "workflows" / f"{pipeline_name}.md"
    if not sop_path.exists():
        sop_content = f"""# SOP: {pipeline_name.replace('_', ' ').title()} Pipeline

## 🎯 Objective
Execute the {pipeline_name} workflow deterministically with <1% error rate.

## 📥 Inputs
- Primary source data: `assets/input_data.json`

## 🛠️ Deterministic Execution Tools
1. `python tools/validate_input.py` -> validates schema and ranges.
2. `python tools/process_{pipeline_name}.py` -> generates `work/{pipeline_name}_plan.json`.

## 🤖 Agent Semantic Curation Gate
- Agent inspects `work/{pipeline_name}_plan.json`.
- Agent verifies flags, approves steps, and marks `"approved": true`.

## 📤 Output Artifacts
- Final output: `assets/{pipeline_name}_output.json`

## 🚨 Edge Cases & Fallbacks
- If input missing: raise explicit `FileNotFoundError`.
- If schema invalid: do not guess; log error and halt turn.
"""
        sop_path.write_text(sop_content, encoding="utf-8")
        print(f"[+] Created workflow SOP: {sop_path.relative_to(target_dir)}")
        
    # Create Starter Tool
    tool_path = target_dir / "tools" / f"process_{pipeline_name}.py"
    if not tool_path.exists():
        tool_code = f'''#!/usr/bin/env python3
"""Deterministic processing tool for {pipeline_name}."""
import json
import sys
from pathlib import Path

def run():
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)
    plan_file = work_dir / "{pipeline_name}_plan.json"
    
    plan_data = {{
        "status": "ready_for_curation",
        "steps": [
            {{"id": 1, "action": "extract", "approved": False}},
            {{"id": 2, "action": "transform", "approved": False}}
        ]
    }}
    plan_file.write_text(json.dumps(plan_data, indent=2), encoding="utf-8")
    print(f"[+] Generated plan artifact: {{plan_file}}")

if __name__ == "__main__":
    run()
'''
        tool_path.write_text(tool_code, encoding="utf-8")
        print(f"[+] Created starter deterministic tool: {tool_path.relative_to(target_dir)}")

def validate_wat(target_dir: Path) -> bool:
    print(f"\n[*] Auditing WAT architecture compliance in: {target_dir}")
    errors = []
    
    # Check directory structure
    for folder in ["workflows", "tools"]:
        if not (target_dir / folder).exists():
            errors.append(f"Missing mandatory layer directory: {folder}/")
            
    # Check gitignore
    gi = target_dir / ".gitignore"
    if not gi.exists():
        errors.append("Missing .gitignore file")
    else:
        text = gi.read_text(encoding="utf-8", errors="ignore")
        if ".env" not in text:
            errors.append(".gitignore must ignore .env to prevent secret leaks")
            
    # Check tools are python scripts
    tools_dir = target_dir / "tools"
    if tools_dir.exists():
        py_tools = list(tools_dir.glob("*.py"))
        if not py_tools:
            errors.append("No executable Python tools found in tools/ directory")
            
    if errors:
        print("[!] WAT Architecture Audit FAILED:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("[+] WAT Architecture Audit PASSED: 100% compliant.")
        return True

def main():
    parser = argparse.ArgumentParser(description="WAT Framework Scaffolder & Validator")
    subparsers = parser.add_subparsers(dest="command")
    
    scaffold_p = subparsers.add_parser("scaffold", help="Scaffold a new WAT project")
    scaffold_p.add_argument("--dir", default=".", help="Target project directory")
    scaffold_p.add_argument("--pipeline", default="data_pipeline", help="Pipeline name")
    
    validate_p = subparsers.add_parser("validate", help="Validate an existing WAT project")
    validate_p.add_argument("--dir", default=".", help="Project directory to validate")
    
    args = parser.parse_args()
    
    if args.command == "scaffold":
        scaffold_wat(Path(args.dir), args.pipeline)
    elif args.command == "validate":
        success = validate_wat(Path(args.dir))
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
