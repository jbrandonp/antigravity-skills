#!/usr/bin/env python3
"""
test_algorithmic_art.py — Unit test suite for algorithmic art CLI tools.
Verifies palette generation, p5.js artwork scaffolding, and quality gate auditing.
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

import generate_art_palette as palette_gen
import scaffold_p5_artwork as scaffolder
import audit_p5_artwork as auditor


class TestGenerateArtPalette(unittest.TestCase):
    def test_hsl_to_rgb_primaries(self):
        # Red
        r, g, b = palette_gen.hsl_to_rgb(0, 1.0, 0.5)
        self.assertEqual((r, g, b), (255, 0, 0))
        # Green
        r, g, b = palette_gen.hsl_to_rgb(120, 1.0, 0.5)
        self.assertEqual((r, g, b), (0, 255, 0))
        # Blue
        r, g, b = palette_gen.hsl_to_rgb(240, 1.0, 0.5)
        self.assertEqual((r, g, b), (0, 0, 255))

    def test_golden_ratio_palette_count(self):
        pal = palette_gen.build_palette("golden-ratio", 8, 180.0)
        self.assertEqual(len(pal), 8)
        for color in pal:
            self.assertTrue(color.startswith("#"))
            self.assertEqual(len(color), 7)

    def test_analogous_and_triadic(self):
        analogous = palette_gen.build_palette("analogous", 5, 45.0)
        self.assertEqual(len(analogous), 5)
        triadic = palette_gen.build_palette("triadic", 6, 90.0)
        self.assertEqual(len(triadic), 6)

    def test_preset_themes(self):
        cyber = palette_gen.build_palette("cyber-neon", 4, 0.0)
        self.assertEqual(len(cyber), 4)
        self.assertEqual(cyber[0], palette_gen.PRESET_THEMES["cyber-neon"][0])


class TestScaffoldP5Artwork(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="art_scaf_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scaffold_all_topologies(self):
        for topo in scaffolder.TOPOLOGIES:
            name = f"test-{topo}"
            html_code = scaffolder.generate_html_artwork(name, topo, ["#111111", "#222222", "#333333"])
            self.assertIn("p5.min.js", html_code)
            self.assertIn("createCanvas", html_code)
            self.assertIn("randomSeed", html_code)
            self.assertIn("noiseSeed", html_code)
            self.assertIn("downloadArtwork", html_code)
            self.assertIn("resetParameters", html_code)

    def test_scaffold_with_philosophy_markdown(self):
        md = scaffolder.generate_philosophy_markdown("stellar-flow", "flow-field")
        self.assertIn("# Algorithmic Philosophy: Stellar Flow", md)
        self.assertIn("Vector Harmonics", md)
        self.assertIn("Controlled Chaos", md)


class TestAuditP5Artwork(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="art_audit_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_scaffolded_passing(self):
        html_code = scaffolder.generate_html_artwork("pass-art", "strange-attractor", ["#111111", "#222222"])
        target = self.root / "pass-art.html"
        target.write_text(html_code, encoding="utf-8")

        report = auditor.audit_artwork(target)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["score"], 100)
        self.assertEqual(len(report["issues"]), 0)

    def test_audit_missing_create_canvas(self):
        bad_html = "<html><script src='p5.js'></script><body><script>randomSeed(1);</script></body></html>"
        target = self.root / "bad-canvas.html"
        target.write_text(bad_html, encoding="utf-8")

        report = auditor.audit_artwork(target)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("createCanvas" in i["message"] for i in report["issues"]))

    def test_audit_forbidden_math_random_in_drawing(self):
        bad_html = """<html>
        <script src='p5.js'></script>
        <body>
        <div id='seed-value'>1</div>
        <script>
        function setup() { createCanvas(400, 400); randomSeed(1); }
        function draw() {
            let x = Math.random() * 400; // Forbidden in draw!
            point(x, 100);
        }
        function resetDefaults() {}
        function generateNew() {}
        function exportImage() {}
        </script>
        </body>
        </html>"""
        target = self.root / "bad-random.html"
        target.write_text(bad_html, encoding="utf-8")

        report = auditor.audit_artwork(target)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Forbidden Math.random" in i["message"] for i in report["issues"]))

    def test_audit_unbounded_array_warning(self):
        warn_html = """<html>
        <script src='p5.js'></script>
        <body>
        <div id='seed-value'>1</div>
        <script>
        function setup() { createCanvas(400, 400); randomSeed(1); }
        let particles = [];
        function draw() {
            particles.push(1); // Leaking array!
        }
        function resetDefaults() {}
        function generateNew() {}
        function exportImage() {}
        </script>
        </body>
        </html>"""
        target = self.root / "warn-array.html"
        target.write_text(warn_html, encoding="utf-8")

        report = auditor.audit_artwork(target)
        self.assertEqual(report["status"], "WARN")
        self.assertTrue(any("Unbounded array growth" in i["message"] for i in report["issues"]))


if __name__ == "__main__":
    unittest.main()
