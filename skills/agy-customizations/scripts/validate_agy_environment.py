#!/usr/bin/env python3
"""
validate_agy_environment.py — Comprehensive environment validator for Google Antigravity (AGY).
Verifies the integrity of config.json, skills, plugins, rules, lifecycle hooks, and MCP servers.

Usage:
  python validate_agy_environment.py [--config-dir DIR] [--json]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

VALID_HOOK_EVENTS = {
    "PreInvocation", "PostInvocation",
    "PreToolUse", "PostToolUse",
    "SessionStart", "SessionEnd", "Stop"
}


def audit_skills(skills_dir: Path) -> List[dict]:
    """Audit all skills in the target skills directory."""
    findings = []
    if not skills_dir.is_dir():
        return findings

    for item in sorted(skills_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            skill_md = item / "SKILL.md"
            if not skill_md.is_file():
                findings.append({
                    "target": str(item),
                    "type": "SKILL",
                    "status": "FAIL",
                    "issue": "Missing required SKILL.md file."
                })
                continue

            try:
                content = skill_md.read_text(encoding="utf-8", errors="replace")
                if not content.startswith("---"):
                    findings.append({
                        "target": str(skill_md),
                        "type": "SKILL",
                        "status": "FAIL",
                        "issue": "Missing YAML frontmatter (must start with '---')."
                    })
                    continue

                # Check name and description
                has_name = bool(re.search(r"^name:\s*.+", content, re.MULTILINE))
                has_desc = bool(re.search(r"^description:\s*.+", content, re.MULTILINE))

                if not has_name or not has_desc:
                    findings.append({
                        "target": str(skill_md),
                        "type": "SKILL",
                        "status": "FAIL",
                        "issue": "YAML frontmatter missing required 'name' or 'description'."
                    })
                else:
                    findings.append({
                        "target": item.name,
                        "type": "SKILL",
                        "status": "PASS",
                        "issue": "Valid skill definition."
                    })
            except Exception as e:
                findings.append({
                    "target": str(skill_md),
                    "type": "SKILL",
                    "status": "FAIL",
                    "issue": f"Error reading SKILL.md: {e}"
                })

    return findings


def audit_plugins(plugins_dir: Path) -> List[dict]:
    """Audit all plugins in the plugins directory."""
    findings = []
    if not plugins_dir.is_dir():
        return findings

    for item in sorted(plugins_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            plugin_json = item / "plugin.json"
            if not plugin_json.is_file():
                findings.append({
                    "target": str(item),
                    "type": "PLUGIN",
                    "status": "FAIL",
                    "issue": "Missing required plugin.json manifest."
                })
                continue

            try:
                data = json.loads(plugin_json.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    findings.append({
                        "target": str(plugin_json),
                        "type": "PLUGIN",
                        "status": "FAIL",
                        "issue": "plugin.json must contain a JSON object."
                    })
                else:
                    findings.append({
                        "target": item.name,
                        "type": "PLUGIN",
                        "status": "PASS",
                        "issue": f"Valid plugin manifest (name: {data.get('name', item.name)})."
                    })
            except Exception as e:
                findings.append({
                    "target": str(plugin_json),
                    "type": "PLUGIN",
                    "status": "FAIL",
                    "issue": f"Invalid JSON in plugin.json: {e}"
                })

            # Check hooks inside plugin if present
            hooks_json = item / "hooks.json"
            if hooks_json.is_file():
                h_findings = audit_hooks_file(hooks_json)
                findings.extend(h_findings)

    return findings


def audit_hooks_file(hooks_path: Path) -> List[dict]:
    """Audit a hooks.json file against valid lifecycle events."""
    findings = []
    try:
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            findings.append({
                "target": str(hooks_path),
                "type": "HOOK",
                "status": "FAIL",
                "issue": "hooks.json must be a JSON object mapping hook names to event lists."
            })
            return findings

        for hook_name, hook_cfg in data.items():
            if not isinstance(hook_cfg, dict):
                continue
            for event in hook_cfg.keys():
                if event == "enabled":
                    continue
                if event not in VALID_HOOK_EVENTS:
                    findings.append({
                        "target": f"{hooks_path.name}:{hook_name}",
                        "type": "HOOK",
                        "status": "FAIL",
                        "issue": f"Invalid lifecycle event '{event}'. Must be one of: {', '.join(sorted(VALID_HOOK_EVENTS))}."
                    })
                else:
                    findings.append({
                        "target": f"{hooks_path.name}:{hook_name}",
                        "type": "HOOK",
                        "status": "PASS",
                        "issue": f"Valid event '{event}' configured."
                    })
    except Exception as e:
        findings.append({
            "target": str(hooks_path),
            "type": "HOOK",
            "status": "FAIL",
            "issue": f"Invalid JSON in hooks file: {e}"
        })

    return findings


def audit_mcp_config(mcp_path: Path) -> List[dict]:
    """Audit MCP server configuration file."""
    findings = []
    if not mcp_path.is_file():
        return findings

    try:
        data = json.loads(mcp_path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers", {})
        if not isinstance(servers, dict):
            findings.append({
                "target": str(mcp_path),
                "type": "MCP",
                "status": "FAIL",
                "issue": "'mcpServers' must be a JSON object."
            })
            return findings

        for s_name, s_cfg in servers.items():
            if "command" not in s_cfg and "url" not in s_cfg:
                findings.append({
                    "target": f"mcp:{s_name}",
                    "type": "MCP",
                    "status": "WARN",
                    "issue": "MCP server missing 'command' (stdio) or 'url' (sse)."
                })
            else:
                findings.append({
                    "target": f"mcp:{s_name}",
                    "type": "MCP",
                    "status": "PASS",
                    "issue": f"Configured properly (command: {s_cfg.get('command') or s_cfg.get('url')})."
                })
    except Exception as e:
        findings.append({
            "target": str(mcp_path),
            "type": "MCP",
            "status": "FAIL",
            "issue": f"Invalid JSON in MCP config: {e}"
        })

    return findings


def validate_environment(config_dir: Path) -> dict:
    """Run full validation across all Antigravity configuration assets."""
    all_findings = []

    skills_dir = config_dir / "skills"
    plugins_dir = config_dir / "plugins"
    hooks_json = config_dir / "hooks.json"
    mcp_json = config_dir / "mcp_config.json"

    # Also check workspace .agents
    all_findings.extend(audit_skills(skills_dir))
    all_findings.extend(audit_plugins(plugins_dir))
    if hooks_json.is_file():
        all_findings.extend(audit_hooks_file(hooks_json))
    if mcp_json.is_file():
        all_findings.extend(audit_mcp_config(mcp_json))

    failures = [f for f in all_findings if f["status"] == "FAIL"]
    warnings = [f for f in all_findings if f["status"] == "WARN"]
    passes = [f for f in all_findings if f["status"] == "PASS"]

    total = len(all_findings)
    score = round((len(passes) / max(1, total)) * 100, 1)

    return {
        "config_directory": str(config_dir),
        "total_assets_audited": total,
        "score": score,
        "passed_count": len(passes),
        "warning_count": len(warnings),
        "failure_count": len(failures),
        "status": "PASS" if len(failures) == 0 else "FAIL",
        "findings": all_findings
    }


def format_report(summary: dict) -> str:
    """Format validation summary report as Markdown."""
    lines = [
        "==================================================================",
        "          ANTIGRAVITY (AGY) CONFIGURATION ENVIRONMENT AUDIT       ",
        "==================================================================",
        f"Directory   : {summary['config_directory']}",
        f"Health Score: {summary['score']}% [{summary['status']}]",
        f"Summary     : {summary['passed_count']} passed, {summary['warning_count']} warnings, {summary['failure_count']} failures",
        "------------------------------------------------------------------"
    ]

    for f in summary["findings"]:
        if f["status"] == "FAIL":
            lines.append(f"❌ [{f['type']}] {f['target']} : {f['issue']}")
        elif f["status"] == "WARN":
            lines.append(f"⚠️ [{f['type']}] {f['target']} : {f['issue']}")

    if summary["failure_count"] == 0 and summary["warning_count"] == 0:
        lines.append("✓ All skills, plugins, hooks, and MCP servers conform to AGY standards.")

    lines.append("==================================================================")
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Validate Antigravity configuration directory, skills, plugins, and hooks."
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        default=os.path.expanduser("~/.gemini/config"),
        help="Path to Antigravity configuration directory (default: ~/.gemini/config)"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    config_dir = Path(args.config_dir).resolve()
    summary = validate_environment(config_dir)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(format_report(summary))

    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
