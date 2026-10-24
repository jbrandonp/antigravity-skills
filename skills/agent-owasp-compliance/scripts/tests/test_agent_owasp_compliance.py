#!/usr/bin/env python3
"""
test_agent_owasp_compliance.py — Automated test suite for the agent-owasp-compliance WAT toolkit.
Tests scan_owasp_compliance.py and generate_security_attestation.py.

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import unittest
import tempfile
import shutil
import json
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import scan_owasp_compliance as scanner
import generate_security_attestation as attester


class TestOwaspComplianceToolkit(unittest.TestCase):
    """Test suite for OWASP ASI compliance scanning and attestation."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_compliant_codebase_scan(self):
        """A codebase implementing all 10 ASI controls must score 100% and return COMPLIANT."""
        code_file = Path(self.test_dir) / "agent_core.py"
        code_content = """
# ASI-01: input_validation and sanitize
def process_user_input(text):
    return sanitize(text)

# ASI-02: allowed_tools registry
ALLOWED_TOOLS = {"search", "read_file"}

# ASI-03: capability_boundary and max_steps
MAX_STEPS = 10
EXECUTION_RING = "ring_2"

# ASI-04: require_approval
def delete_record(record_id):
    require_approval(record_id)

# ASI-05: verify_signature and signed_token
def verify_agent_token(token):
    return verify_signature(token)

# ASI-06: audit_log with hash_chain
def record_action(action):
    audit_log.append(action)

# ASI-07: ed25519 cryptographic_identity
AGENT_KEY = "ed25519_keypair"

# ASI-08: policy_evaluator deterministic
def check_policy(action):
    return policy_evaluator.evaluate(action)

# ASI-09: integrity.json
MANIFEST = "integrity.json"

# ASI-10: circuit_breaker and kill_switch
CIRCUIT = "circuit_breaker_active"
"""
        code_file.write_text(code_content, encoding="utf-8")

        summary = scanner.scan_project(Path(self.test_dir))
        self.assertEqual(summary["verdict"], "COMPLIANT")
        self.assertEqual(summary["compliance_score"], 100.0)
        self.assertEqual(summary["controls_covered"], "10/10")

    def test_vulnerable_codebase_scan(self):
        """A codebase with raw eval, shell=True, and prompt-only security must flag vulnerabilities."""
        bad_file = Path(self.test_dir) / "insecure_agent.py"
        bad_content = """
import os, subprocess

def run_user_cmd(cmd):
    # ASI-01 / ASI-02 negative patterns
    eval(cmd)
    subprocess.run(cmd, shell=True)

# ASI-08 negative pattern
def check_auth(user):
    ask_llm_if_allowed(user)
"""
        bad_file.write_text(bad_content, encoding="utf-8")

        summary = scanner.scan_project(Path(self.test_dir))
        self.assertEqual(summary["verdict"], "NON_COMPLIANT")
        self.assertLess(summary["compliance_score"], 50.0)

        # Check detected vulnerabilities
        asi_01 = next(c for c in summary["controls"] if c["id"] == "ASI-01")
        asi_02 = next(c for c in summary["controls"] if c["id"] == "ASI-02")
        self.assertEqual(asi_01["status"], "FAIL")
        self.assertTrue(len(asi_01["vulnerabilities"]) > 0)
        self.assertTrue(len(asi_02["vulnerabilities"]) > 0)

    def test_generate_security_attestation(self):
        """Attestation generator must produce a formal report with cryptographic fingerprint."""
        # Create minimal compliant file
        mini_file = Path(self.test_dir) / "service.py"
        mini_file.write_text("input_validation = True\nallowed_tools = []\n", encoding="utf-8")

        report = attester.generate_attestation_certificate("OrderBot", "2.1.0", Path(self.test_dir))
        self.assertIn("OWASP Agentic Security Initiative (ASI 2026) Official Attestation", report)
        self.assertIn("OrderBot", report)
        self.assertIn("sha256:", report)
        self.assertIn("Compliance Standard : OWASP ASI Top 10", report)


if __name__ == "__main__":
    unittest.main()
