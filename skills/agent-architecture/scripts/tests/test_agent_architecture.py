#!/usr/bin/env python3
"""
test_agent_architecture.py — Automated unit test suite for the agent-architecture WAT toolkit.
Tests scaffold_agent_architecture.py, audit_agent_design.py, and validate_agent_architecture.py.

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import unittest
import tempfile
import shutil
import json
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import scaffold_agent_architecture as scaffolder
import audit_agent_design as auditor
import validate_agent_architecture as validator
import simulate_agent_threats as threat_sim


class TestAgentArchitectureToolkit(unittest.TestCase):
    """Test suite for AI Agent Architecture engineering tools."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scaffold_all_topologies(self):
        """Ensure all 3 primary topologies scaffold valid Markdown and Mermaid diagrams."""
        topologies = ["single_agent_loop", "router_worker", "orchestrator_subagents"]
        for top in topologies:
            content = scaffolder.build_specification(
                name=f"Agent_{top}",
                role="Perform automated task orchestration",
                topology=top,
                model="claude-3-5-sonnet",
                tools=["tool_a", "tool_b"],
                max_steps=12,
                timeout_sec=90,
                budget_usd=1.00
            )
            self.assertIn("```mermaid\nflowchart TD", content)
            self.assertIn("```mermaid\nsequenceDiagram", content)
            self.assertIn("## 1. Task and Requirements Criteria", content)
            self.assertIn("## 3. Execution, State, and Stopping Invariants", content)
            self.assertIn("## 7. Quality Verification, Economics & Evaluation Gates", content)

    def test_scaffold_and_audit_soundness(self):
        """Scaffolded architectures must score 100/100 on the 10 Golden Invariants audit."""
        spec_path = Path(self.test_dir) / "AGENT_ARCHITECTURE.md"
        content = scaffolder.build_specification(
            name="ComplianceAgent",
            role="Audit regulatory records",
            topology="router_worker",
            model="gpt-4o",
            tools=["db_query", "generate_pdf"],
            max_steps=10,
            timeout_sec=60,
            budget_usd=0.50
        )
        spec_path.write_text(content, encoding="utf-8")

        audit_res = auditor.audit_agent_document(spec_path)
        self.assertEqual(audit_res["score"], 100)
        self.assertEqual(audit_res["verdict"], "ARCHITECTURALLY_SOUND")
        self.assertEqual(audit_res["passed_invariants"], 10)

    def test_audit_detects_unbounded_vulnerabilities(self):
        """Auditor must detect missing loop bounds and prompt-only security."""
        bad_spec = Path(self.test_dir) / "VULNERABLE_AGENT.md"
        bad_content = """# Insecure Bot
This bot runs forever until user says quit.
The model decides if allowed to delete files.
Prompt only controls access.
"""
        bad_spec.write_text(bad_content, encoding="utf-8")

        audit_res = auditor.audit_agent_document(bad_spec)
        self.assertLess(audit_res["score"], 65)
        self.assertEqual(audit_res["verdict"], "CRITICAL_DEFICIENCIES")
        # Check failed invariants
        failed_ids = [f["id"] for f in audit_res["findings"] if f["status"] == "FAIL"]
        self.assertIn("INV-01", failed_ids)  # Unbounded loop
        self.assertIn("INV-04", failed_ids)  # Deterministic policy enforcement

    def test_validate_architecture_contract(self):
        """Validator must approve complete 7-view deliverable and reject incomplete specs."""
        complete_spec = Path(self.test_dir) / "COMPLETE_SPEC.md"
        content = scaffolder.build_specification(
            name="OpsAgent",
            role="Perform cluster health recovery",
            topology="single_agent_loop",
            model="gemini-1.5-pro",
            tools=["restart_pod", "check_logs"],
            max_steps=5,
            timeout_sec=30,
            budget_usd=0.20
        )
        complete_spec.write_text(content, encoding="utf-8")

        val_res = validator.validate_architecture_contract(complete_spec)
        self.assertEqual(val_res["status"], "PASS")
        self.assertEqual(val_res["contract_score"], 100.0)
        self.assertTrue(val_res["has_mermaid_diagrams"])
        self.assertTrue(val_res["has_limits_table"])

        # Test incomplete spec
        partial_spec = Path(self.test_dir) / "PARTIAL_SPEC.md"
        partial_spec.write_text("# My Bot\nJust a simple prompt.\n", encoding="utf-8")
        partial_res = validator.validate_architecture_contract(partial_spec)
        self.assertEqual(partial_res["status"], "FAIL")
        self.assertLess(partial_res["contract_score"], 50.0)

    def test_threat_simulator(self):
        """Threat simulator must verify 12 stress probes on resilient vs vulnerable architectures."""
        spec_path = Path(self.test_dir) / "STRESS_SPEC.md"
        content = scaffolder.build_specification(
            name="ResilientAgent",
            role="Perform high-assurance trading operations",
            topology="router_worker",
            model="claude-3-5-sonnet",
            tools=["execute_order", "check_risk"],
            max_steps=8,
            timeout_sec=45,
            budget_usd=0.25
        )
        spec_path.write_text(content, encoding="utf-8")

        res = threat_sim.run_threat_probes(spec_path)
        self.assertEqual(res["verdict"], "RESILIENT")
        self.assertEqual(res["critical_failures"], 0)
        self.assertEqual(res["mitigated_probes"], 12)
        self.assertEqual(res["pass_rate"], 100.0)


if __name__ == "__main__":
    unittest.main()
