#!/usr/bin/env python3
"""
test_codebase_knowledge.py — Automated test suite for the acquire-codebase-knowledge WAT toolkit.
Tests scan.py, generate_architecture_diagram.py, audit_codebase_debt.py, and validate_codebase_docs.py.

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

import scan
import generate_architecture_diagram as arch_diag
import audit_codebase_debt as debt_audit
import validate_codebase_docs as val_docs


class TestScanEngine(unittest.TestCase):
    """Test scan.py functionality."""

    def test_exclude_directories(self):
        """Ensure build, cache, and intermediate folders are strictly excluded."""
        self.assertTrue(scan.should_exclude(Path("node_modules/foo/bar.js")))
        self.assertTrue(scan.should_exclude(Path(".git/HEAD")))
        self.assertTrue(scan.should_exclude(Path("Intermediate/Build/foo.obj")))
        self.assertTrue(scan.should_exclude(Path("Saved/Logs/game.log")))
        self.assertFalse(scan.should_exclude(Path("src/controllers/user.ts")))

    def test_collect_code_metrics(self):
        """Test code metrics collection returns expected keys."""
        metrics = scan.collect_code_metrics()
        self.assertIn("total_files", metrics)
        self.assertIn("total_lines", metrics)
        self.assertIn("by_language", metrics)
        self.assertIsInstance(metrics["total_files"], int)


class TestArchitectureDiagramGenerator(unittest.TestCase):
    """Test Mermaid diagram generation."""

    def test_sanitize_id(self):
        """Ensure node IDs are safe for Mermaid syntax."""
        self.assertEqual(arch_diag.sanitize_id("my-service.core"), "my_service_core")
        self.assertEqual(arch_diag.sanitize_id("123service"), "node_123service")

    def test_mermaid_flowchart_generation(self):
        """Test Mermaid flowchart syntax."""
        modules = [Path("auth"), Path("billing")]
        deps = {"auth": {"billing"}, "billing": set()}
        externals = {"Database": ["postgres"]}

        flowchart = arch_diag.generate_mermaid_diagram(Path("."), modules, deps, externals)
        self.assertTrue(flowchart.startswith("```mermaid\nflowchart TD"))
        self.assertIn("subgraph CoreApplication", flowchart)
        self.assertIn("auth --> billing", flowchart)
        self.assertIn("subgraph ExternalServices", flowchart)
        self.assertTrue(flowchart.endswith("```"))

    def test_mermaid_sequence_generation(self):
        """Test Mermaid sequence diagram syntax."""
        modules = [Path("Gateway"), Path("Service")]
        externals = {"Database": ["postgres"]}

        sequence = arch_diag.generate_sequence_diagram(modules, externals)
        self.assertTrue(sequence.startswith("```mermaid\nsequenceDiagram"))
        self.assertIn("autonumber", sequence)
        self.assertIn("Client->>Gateway: Issue Command / Request", sequence)
        self.assertTrue(sequence.endswith("```"))


class TestCodebaseDebtAuditor(unittest.TestCase):
    """Test technical debt and code health metrics."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_god_file_and_debt_audit(self):
        """Test detection of god files exceeding LOC threshold."""
        small_file = Path(self.test_dir) / "small.py"
        small_file.write_text("print('hello')\n" * 50, encoding="utf-8")

        god_file = Path(self.test_dir) / "god.py"
        god_file.write_text("x = 1\n" * 600, encoding="utf-8")

        audit_res = debt_audit.audit_codebase(Path(self.test_dir), max_lines_threshold=500)
        self.assertEqual(len(audit_res["god_files"]), 1)
        self.assertEqual(audit_res["god_files"][0]["path"], "god.py")
        self.assertGreaterEqual(audit_res["god_files"][0]["loc"], 600)
        self.assertIn("health_score", audit_res["summary"])

    def test_circular_dependency_detection(self):
        """Test detection of cyclic imports."""
        mod_a = Path(self.test_dir) / "module_a.py"
        mod_b = Path(self.test_dir) / "module_b.py"

        mod_a.write_text("import module_b\n", encoding="utf-8")
        mod_b.write_text("import module_a\n", encoding="utf-8")

        cycles = debt_audit.detect_circular_dependencies(Path(self.test_dir), [mod_a, mod_b])
        self.assertEqual(len(cycles), 1)
        self.assertIn("module_a.py", cycles[0])
        self.assertIn("module_b.py", cycles[0])


class TestCodebaseDocsValidator(unittest.TestCase):
    """Test validate_codebase_docs.py contract validation."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.docs_dir = Path(self.test_dir) / "docs" / "codebase"
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_missing_mandatory_docs_fail(self):
        """Test failure when docs are missing."""
        summary = val_docs.audit_codebase_docs(self.docs_dir, Path(self.test_dir))
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["valid_docs_count"], 0)

    def test_complete_docs_pass(self):
        """Test pass when all 7 docs exist with required headers and zero unfilled placeholders."""
        # Create an existing evidence file
        evidence_file = Path(self.test_dir) / "src" / "index.ts"
        evidence_file.parent.mkdir(parents=True, exist_ok=True)
        evidence_file.write_text("export const x = 1;", encoding="utf-8")

        for doc_name, sections in val_docs.REQUIRED_SECTIONS.items():
            content = f"# {doc_name}\n\n"
            for s in sections:
                content += f"## {s}\n- Documented verified facts.\n\n"
            content += f"## Evidence\n- `src/index.ts`\n"

            (self.docs_dir / doc_name).write_text(content, encoding="utf-8")

        summary = val_docs.audit_codebase_docs(self.docs_dir, Path(self.test_dir))
        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary["valid_docs_count"], 7)
        self.assertEqual(summary["completion_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
