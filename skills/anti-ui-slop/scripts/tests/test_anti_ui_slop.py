#!/usr/bin/env python3
"""
test_anti_ui_slop.py — Unit test suite for Anti-UI Slop scanner and token generator.
Verifies detection of AI clichés, transition-all traps, accessibility violations,
and 4-layer design token generation.
"""

import unittest
import tempfile
import shutil
import sys
import json
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import scan_ui_slop as scanner
import generate_ui_tokens as token_gen


class TestScanUiSlop(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="slop_scan_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_detect_transition_all(self):
        code = "<button className='p-4 transition-all duration-300'>Click</button>"
        f = self.root / "bad_button.tsx"
        f.write_text(code, encoding="utf-8")

        findings = scanner.scan_file(f)
        self.assertTrue(any(item["severity"] == "CRITICAL" and "transition-all" in item["issue"] for item in findings))

    def test_detect_bare_focus_outline_none(self):
        code = "<input className='border p-2 focus:outline-none' />"
        f = self.root / "bad_input.jsx"
        f.write_text(code, encoding="utf-8")

        findings = scanner.scan_file(f)
        self.assertTrue(any(item["severity"] == "CRITICAL" and "Focus outline removed" in item["issue"] for item in findings))

    def test_allow_focus_visible_ring(self):
        code = "<input className='border p-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500' />"
        f = self.root / "good_input.jsx"
        f.write_text(code, encoding="utf-8")

        findings = scanner.scan_file(f)
        self.assertFalse(any("Focus outline removed" in item["issue"] for item in findings))

    def test_detect_ai_buzzwords(self):
        code = "<h1>Streamline your workflow with our smart app</h1>"
        f = self.root / "hero.html"
        f.write_text(code, encoding="utf-8")

        findings = scanner.scan_file(f)
        self.assertTrue(any(item["severity"] == "WARNING" and "AI Cliché Copywriting" in item["issue"] for item in findings))

    def test_detect_pure_black_background(self):
        code = "<div className='bg-black text-white p-8'>Dashboard</div>"
        f = self.root / "dark_panel.tsx"
        f.write_text(code, encoding="utf-8")

        findings = scanner.scan_file(f)
        self.assertTrue(any(item["severity"] == "WARNING" and "Pure harsh black" in item["issue"] for item in findings))

    def test_scan_path_clean_craftsmanship(self):
        clean_code = """
        export function Card({ title, price }: { title: string; price: number }) {
            return (
                <div className="bg-surface border border-subtle rounded-lg p-6 hover:border-strong transition-colors duration-150">
                    <h3 className="text-foreground font-semibold">{title}</h3>
                    <span className="text-foreground-secondary tabular-nums font-mono">${price.toFixed(2)}</span>
                    <button className="mt-4 px-4 py-2 bg-accent text-accent-contrast rounded-md hover:bg-accent-hover active:scale-[0.98] transition-transform duration-150 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-accent">
                        Purchase License
                    </button>
                </div>
            );
        }
        """
        f = self.root / "CleanCard.tsx"
        f.write_text(clean_code, encoding="utf-8")

        report = scanner.scan_path(self.root)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["total_critical"], 0)
        self.assertEqual(report["total_warning"], 0)
        self.assertEqual(report["score"], 100)


class TestGenerateUiTokens(unittest.TestCase):
    def test_generate_css_variables(self):
        css = token_gen.render_css_variables("zinc-craft")
        self.assertIn(":root {", css)
        self.assertIn(".dark, [data-theme='dark'] {", css)
        self.assertIn("--bg-canvas: #fafafa;", css)
        self.assertIn("--bg-canvas: #09090b;", css)
        self.assertIn("--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);", css)

    def test_generate_tailwind_config(self):
        tw = token_gen.render_tailwind_config("slate-enterprise")
        self.assertIn("tailwind.config.js", tw)
        self.assertIn("var(--bg-canvas)", tw)
        self.assertIn("var(--accent-primary)", tw)


if __name__ == "__main__":
    unittest.main()
