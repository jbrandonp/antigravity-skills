#!/usr/bin/env python3
"""
scaffold_agy_customization.py — Automated generator for Google Antigravity (AGY) customizations.
Generates fully compliant skills, plugins, rules, lifecycle hooks, and MCP server templates.

Usage:
  python scaffold_agy_customization.py --type skill --name my-skill --desc "Skill description" --output ./skills
  python scaffold_agy_customization.py --type plugin --name my-plugin --output ./plugins
  python scaffold_agy_customization.py --type hook --name audit-hook --event PreToolUse --matcher run_command --command "python audit.py" --output ./
  python scaffold_agy_customization.py --type rule --name coding-standards --output ./rules
  python scaffold_agy_customization.py --type mcp --name sqlite-mcp --command "uv run mcp-server-sqlite" --output ./

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional

VALID_TYPES = ["skill", "plugin", "hook", "rule", "mcp"]
VALID_HOOK_EVENTS = ["SessionStart", "SessionEnd", "PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation", "Stop"]


def scaffold_skill(name: str, desc: str, output_dir: Path, force: bool = False) -> Path:
    """Scaffold a compliant Antigravity Skill."""
    target_dir = output_dir / name
    target_dir.mkdir(parents=True, exist_ok=True)
    
    skill_md = target_dir / "SKILL.md"
    if skill_md.exists() and not force:
        raise FileExistsError(f"SKILL.md already exists at {skill_md}. Use --force to overwrite.")

    content = f"""---
name: {name}
description: {desc or f"Comprehensive guide and automated toolchain for {name}."}
---

# {name}

## 🎯 Overview
{desc or f"This skill provides deterministic workflows and production standards for {name}."}

## 🚀 Workflows & CLI Tools
This skill adheres to the WAT (Workflows, Agents, Tools) paradigm. Deterministic operations are executed via Python CLI tools located in `scripts/`.

### Available Scripts
- `scripts/run_{name.replace('-', '_')}.py`: Main deterministic execution entrypoint.

## 📋 Best Practices
1. **Deterministic Execution**: Always run CLI tools with explicit arguments.
2. **Context Efficiency**: Keep inputs and logs concise to preserve context limits.
3. **Safety & Verification**: Validate outputs against acceptance gates before concluding.

## 🔗 References
- See `references/` for detailed architectural guidelines.
"""
    skill_md.write_text(content, encoding="utf-8")
    
    # Create companion directories
    scripts_dir = target_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    starter_script = scripts_dir / f"run_{name.replace('-', '_')}.py"
    if not starter_script.exists():
        script_content = f"""#!/usr/bin/env python3
\"\"\"
run_{name.replace('-', '_')}.py — Deterministic CLI utility for {name}.
\"\"\"

import sys

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("Executing {name} task deterministically...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        starter_script.write_text(script_content, encoding="utf-8")

    references_dir = target_dir / "references"
    references_dir.mkdir(exist_ok=True)
    ref_md = references_dir / f"{name}_standards.md"
    if not ref_md.exists():
        ref_md.write_text(f"# {name} Architectural Standards\n\nDocument core contracts and technical constraints here.\n", encoding="utf-8")

    return target_dir


def scaffold_plugin(name: str, desc: str, output_dir: Path, force: bool = False) -> Path:
    """Scaffold a full Antigravity Plugin bundle."""
    target_dir = output_dir / name
    target_dir.mkdir(parents=True, exist_ok=True)

    plugin_json = target_dir / "plugin.json"
    if plugin_json.exists() and not force:
        raise FileExistsError(f"plugin.json already exists at {plugin_json}. Use --force to overwrite.")

    manifest = {
        "name": name,
        "version": "1.0.0",
        "description": desc or f"Antigravity plugin bundle for {name}."
    }
    plugin_json.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Subdirectories
    rules_dir = target_dir / "rules"
    rules_dir.mkdir(exist_ok=True)
    agents_rule = rules_dir / "AGENTS.md"
    if not agents_rule.exists():
        agents_rule.write_text(f"# {name} Rules\n\nGuidelines applied whenever this plugin is active.\n", encoding="utf-8")

    skills_dir = target_dir / "skills"
    skills_dir.mkdir(exist_ok=True)
    starter_skill = skills_dir / f"{name}-core"
    starter_skill.mkdir(exist_ok=True)
    starter_skill_md = starter_skill / "SKILL.md"
    if not starter_skill_md.exists():
        starter_skill_md.write_text(f"""---
name: {name}-core
description: Core operations for the {name} plugin.
---

# {name} Core Skill
""", encoding="utf-8")

    # Optional mcp_config.json
    mcp_config = target_dir / "mcp_config.json"
    if not mcp_config.exists():
        mcp_data = {
            "mcpServers": {
                f"{name}-service": {
                    "command": "python",
                    "args": ["-m", f"{name}.server"]
                }
            }
        }
        mcp_config.write_text(json.dumps(mcp_data, indent=2) + "\n", encoding="utf-8")

    return target_dir


def scaffold_hook(name: str, event: str, matcher: str, command: str, output_dir: Path, force: bool = False) -> Path:
    """Scaffold or append a lifecycle hook in hooks.json."""
    if event not in VALID_HOOK_EVENTS:
        raise ValueError(f"Invalid hook event '{event}'. Valid choices: {', '.join(VALID_HOOK_EVENTS)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    hooks_file = output_dir if output_dir.suffix == ".json" else output_dir / "hooks.json"
    
    hooks_data: Dict[str, Any] = {}
    if hooks_file.exists():
        try:
            hooks_data = json.loads(hooks_file.read_text(encoding="utf-8"))
        except Exception:
            hooks_data = {}

    hook_entry: Dict[str, Any] = hooks_data.get(name, {})
    cmd = command or "echo 'Hook triggered'"

    if event in ["PreToolUse", "PostToolUse"]:
        match_pattern = matcher or "*"
        handler_group = {
            "matcher": match_pattern,
            "hooks": [
                {
                    "type": "command",
                    "command": cmd,
                    "timeout": 30
                }
            ]
        }
        if event not in hook_entry:
            hook_entry[event] = []
        hook_entry[event].append(handler_group)
    else:
        # Flat structure
        handler = {
            "type": "command",
            "command": cmd,
            "timeout": 30
        }
        if event not in hook_entry:
            hook_entry[event] = []
        hook_entry[event].append(handler)

    hooks_data[name] = hook_entry
    hooks_file.write_text(json.dumps(hooks_data, indent=2) + "\n", encoding="utf-8")
    return hooks_file


def scaffold_rule(name: str, desc: str, output_dir: Path, force: bool = False) -> Path:
    """Scaffold a rule markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{name}.md" if not name.endswith(".md") else name
    rule_file = output_dir / filename

    if rule_file.exists() and not force:
        raise FileExistsError(f"Rule file already exists at {rule_file}. Use --force to overwrite.")

    rule_title = name.replace(".md", "").replace("-", " ").replace("_", " ").title()
    content = f"""# {rule_title} Rules

{desc or "Mandatory behavioral guidelines and constraints for the AI agent."}

## 📌 Core Requirements
1. Follow architectural standards and keep code DRY.
2. Enforce strict typing (no untyped any).
3. Validate changes with automated tests before completing.
"""
    rule_file.write_text(content, encoding="utf-8")
    return rule_file


def scaffold_mcp(name: str, command: str, output_dir: Path, force: bool = False) -> Path:
    """Scaffold an MCP server configuration entry or mcp_config.json."""
    output_dir.mkdir(parents=True, exist_ok=True)
    config_file = output_dir if output_dir.suffix == ".json" else output_dir / "mcp_config.json"

    data: Dict[str, Any] = {"mcpServers": {}}
    if config_file.exists():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
        except Exception:
            data = {"mcpServers": {}}

    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        data["mcpServers"] = {}

    cmd_parts = command.split() if command else ["python", "-m", f"{name}_mcp"]
    data["mcpServers"][name] = {
        "command": cmd_parts[0],
        "args": cmd_parts[1:] if len(cmd_parts) > 1 else []
    }

    config_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return config_file


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Scaffold fully compliant Google Antigravity (AGY) customizations.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--type", "-t", required=True, choices=VALID_TYPES, help="Customization type to scaffold.")
    parser.add_argument("--name", "-n", required=True, help="Name of the customization asset.")
    parser.add_argument("--output", "-o", default=".", help="Target output directory (defaults to current dir).")
    parser.add_argument("--desc", "-d", default="", help="Description of the asset.")
    parser.add_argument("--event", default="PreToolUse", choices=VALID_HOOK_EVENTS, help="Hook event type (for --type hook).")
    parser.add_argument("--matcher", default="*", help="Tool matcher regex (for PreToolUse/PostToolUse hooks).")
    parser.add_argument("--command", "-c", default="", help="Command to execute (for hook or mcp).")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing files.")

    args = parser.parse_args()
    output_path = Path(args.output).resolve()

    try:
        if args.type == "skill":
            result = scaffold_skill(args.name, args.desc, output_path, args.force)
            print(f"[OK] Skill '{args.name}' scaffolded at: {result}")
        elif args.type == "plugin":
            result = scaffold_plugin(args.name, args.desc, output_path, args.force)
            print(f"[OK] Plugin '{args.name}' scaffolded at: {result}")
        elif args.type == "hook":
            result = scaffold_hook(args.name, args.event, args.matcher, args.command, output_path, args.force)
            print(f"[OK] Hook '{args.name}' scaffolded at: {result}")
        elif args.type == "rule":
            result = scaffold_rule(args.name, args.desc, output_path, args.force)
            print(f"[OK] Rule '{args.name}' scaffolded at: {result}")
        elif args.type == "mcp":
            result = scaffold_mcp(args.name, args.command, output_path, args.force)
            print(f"[OK] MCP config for '{args.name}' scaffolded at: {result}")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to scaffold {args.type}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
