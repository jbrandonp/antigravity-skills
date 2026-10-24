#!/usr/bin/env python3
"""
test_agy_customizations.py — Unit test suite for AGY customization validator and scaffolder.
Verifies full compliance, error detection, and deterministic scaffolding.
"""

import unittest
import tempfile
import shutil
import json
import sys
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import validate_agy_environment as validator
import scaffold_agy_customization as scaffolder


class TestValidateAgyEnvironment(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="agy_val_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_skills_valid(self):
        skills_dir = self.root / "skills"
        skills_dir.mkdir()
        my_skill = skills_dir / "valid-skill"
        my_skill.mkdir()
        (my_skill / "SKILL.md").write_text(
            "---\nname: valid-skill\ndescription: Test description\n---\n# Valid Skill\n",
            encoding="utf-8"
        )
        findings = validator.audit_skills(skills_dir)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "PASS")

    def test_audit_skills_missing_frontmatter(self):
        skills_dir = self.root / "skills"
        skills_dir.mkdir()
        bad_skill = skills_dir / "bad-skill"
        bad_skill.mkdir()
        (bad_skill / "SKILL.md").write_text("# Missing frontmatter\n", encoding="utf-8")
        
        findings = validator.audit_skills(skills_dir)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "FAIL")
        self.assertIn("frontmatter", findings[0]["issue"].lower())

    def test_audit_plugins_valid(self):
        plugins_dir = self.root / "plugins"
        plugins_dir.mkdir()
        p_dir = plugins_dir / "my-plugin"
        p_dir.mkdir()
        (p_dir / "plugin.json").write_text(
            json.dumps({"name": "my-plugin", "version": "1.0.0"}),
            encoding="utf-8"
        )
        findings = validator.audit_plugins(plugins_dir)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "PASS")

    def test_audit_hooks_grouped_and_flat(self):
        hooks_data = {
            "my-guard": {
                "PreToolUse": [
                    {
                        "matcher": "run_command",
                        "hooks": [{"command": "echo check"}]
                    }
                ],
                "SessionStart": [
                    {"command": "echo start"}
                ]
            }
        }
        hooks_file = self.root / "hooks.json"
        hooks_file.write_text(json.dumps(hooks_data), encoding="utf-8")
        
        findings = validator.audit_hooks_file(hooks_file)
        self.assertEqual(len(findings), 2)
        self.assertTrue(all(f["status"] == "PASS" for f in findings))

    def test_audit_hooks_invalid_event(self):
        hooks_data = {
            "bad-hook": {
                "UnknownEvent": [{"command": "echo test"}]
            }
        }
        hooks_file = self.root / "hooks.json"
        hooks_file.write_text(json.dumps(hooks_data), encoding="utf-8")
        
        findings = validator.audit_hooks_file(hooks_file)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "FAIL")
        self.assertIn("Invalid lifecycle event", findings[0]["issue"])

    def test_audit_mcp_valid(self):
        mcp_data = {
            "mcpServers": {
                "sqlite-srv": {
                    "command": "python",
                    "args": ["-m", "sqlite_srv"]
                }
            }
        }
        mcp_file = self.root / "mcp_config.json"
        mcp_file.write_text(json.dumps(mcp_data), encoding="utf-8")
        
        findings = validator.audit_mcp_config(mcp_file)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["status"], "PASS")


class TestScaffoldAgyCustomization(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="agy_scaf_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scaffold_skill(self):
        target = scaffolder.scaffold_skill(
            name="demo-skill",
            desc="Demo skill description",
            output_dir=self.root
        )
        self.assertTrue((target / "SKILL.md").exists())
        self.assertTrue((target / "scripts" / "run_demo_skill.py").exists())
        self.assertTrue((target / "references" / "demo-skill_standards.md").exists())

        content = (target / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: demo-skill", content)
        self.assertIn("description: Demo skill description", content)

    def test_scaffold_plugin(self):
        target = scaffolder.scaffold_plugin(
            name="demo-plugin",
            desc="Plugin description",
            output_dir=self.root
        )
        self.assertTrue((target / "plugin.json").exists())
        self.assertTrue((target / "rules" / "AGENTS.md").exists())
        self.assertTrue((target / "skills" / "demo-plugin-core" / "SKILL.md").exists())
        self.assertTrue((target / "mcp_config.json").exists())

    def test_scaffold_hook_grouped(self):
        hook_file = scaffolder.scaffold_hook(
            name="security-gate",
            event="PreToolUse",
            matcher="run_command",
            command="python check.py",
            output_dir=self.root
        )
        self.assertTrue(hook_file.exists())
        data = json.loads(hook_file.read_text(encoding="utf-8"))
        self.assertIn("security-gate", data)
        self.assertIn("PreToolUse", data["security-gate"])
        entry = data["security-gate"]["PreToolUse"][0]
        self.assertEqual(entry["matcher"], "run_command")
        self.assertEqual(entry["hooks"][0]["command"], "python check.py")

    def test_scaffold_rule(self):
        rule_file = scaffolder.scaffold_rule(
            name="safety-rules",
            desc="Safety protocol constraints",
            output_dir=self.root
        )
        self.assertTrue(rule_file.exists())
        content = rule_file.read_text(encoding="utf-8")
        self.assertIn("# Safety Rules Rules", content)
        self.assertIn("Safety protocol constraints", content)

    def test_scaffold_mcp(self):
        mcp_file = scaffolder.scaffold_mcp(
            name="test-server",
            command="uv run my-server --port 8000",
            output_dir=self.root
        )
        self.assertTrue(mcp_file.exists())
        data = json.loads(mcp_file.read_text(encoding="utf-8"))
        self.assertIn("test-server", data["mcpServers"])
        self.assertEqual(data["mcpServers"]["test-server"]["command"], "uv")
        self.assertEqual(data["mcpServers"]["test-server"]["args"], ["run", "my-server", "--port", "8000"])


if __name__ == "__main__":
    unittest.main()
