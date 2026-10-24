#!/usr/bin/env python3
"""Automated Test Suite for Accessibility Audit Engine Tools."""

from pathlib import Path
import tempfile
import unittest

sys_path = Path(__file__).resolve().parent.parent
import sys
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

from audit_aria_patterns import audit_file_aria
from audit_html_a11y import audit_html_file
from calc_color_contrast import contrast_ratio, evaluate_contrast, parse_color


class TestA11yEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_contrast_ratio_calculations(self):
        """Tests relative luminance and contrast ratio calculations."""
        # 1. Black on White = 21:1
        black = parse_color("#000000")
        white = parse_color("#FFFFFF")
        ratio = contrast_ratio(black, white)
        self.assertAlmostEqual(ratio, 21.0, places=1)

        rep_bw = evaluate_contrast("#000000", "#FFFFFF")
        self.assertEqual(rep_bw["verdict"], "PASS")
        self.assertTrue(rep_bw["wcag_compliance"]["AA_normal_text_4_5"])
        self.assertTrue(rep_bw["wcag_compliance"]["AAA_normal_text_7_0"])

        # 2. Borderline grey (#777777 = 4.48:1) -> WARN (passes large text 3:1, fails normal 4.5:1)
        rep_warn = evaluate_contrast("#777777", "#FFFFFF")
        self.assertEqual(rep_warn["verdict"], "WARN")
        self.assertTrue(rep_warn["wcag_compliance"]["AA_large_text_3_0"])
        self.assertFalse(rep_warn["wcag_compliance"]["AA_normal_text_4_5"])

        # 3. Failing light grey (#999999 = 2.85:1) -> FAIL (fails both 4.5:1 and 3:1)
        rep_fail = evaluate_contrast("#999999", "#FFFFFF")
        self.assertEqual(rep_fail["verdict"], "FAIL")
        self.assertFalse(rep_fail["wcag_compliance"]["AA_normal_text_4_5"])
        self.assertIsNotNone(rep_fail["suggested_fg"])

        # Verify suggestion passes AA normal text
        sugg_fg = parse_color(rep_fail["suggested_fg"])
        self.assertGreaterEqual(contrast_ratio(sugg_fg, white), 4.5)

    def test_html_parser_wcag_validations(self):
        """Tests HTML accessibility auditor on compliant and flawed documents."""
        # 1. Compliant document
        good_html = """<!DOCTYPE html>
        <html lang="en">
        <head><title>Accessible Dashboard</title></head>
        <body>
            <h1>Main Title</h1>
            <h2>Section Subtitle</h2>
            <img src="logo.png" alt="Company Logo">
            <label for="username">Username</label>
            <input id="username" type="text">
            <button type="button">Submit Form</button>
        </body>
        </html>
        """
        good_file = self.work_dir / "good.html"
        good_file.write_text(good_html, encoding="utf-8")

        issues_good = audit_html_file(good_file)
        fails_good = [i for i in issues_good if i["severity"] == "FAIL"]
        self.assertEqual(len(fails_good), 0, "Compliant HTML must have zero FAIL errors")

        # 2. Flawed document (missing lang, missing alt, duplicate id, positive tabindex, skipped heading)
        bad_html = """<!DOCTYPE html>
        <html>
        <head></head>
        <body>
            <h1>Main Title</h1>
            <h3>Skipped Subtitle</h3>
            <img src="banner.png">
            <input type="text">
            <button tabindex="2"></button>
            <div id="duplicate-card">A</div>
            <div id="duplicate-card">B</div>
        </body>
        </html>
        """
        bad_file = self.work_dir / "bad.html"
        bad_file.write_text(bad_html, encoding="utf-8")

        issues_bad = audit_html_file(bad_file)
        fails_bad = [i for i in issues_bad if i["severity"] == "FAIL"]
        warns_bad = [i for i in issues_bad if i["severity"] == "WARN"]

        self.assertGreaterEqual(len(fails_bad), 4)  # lang, alt, form label, empty button, duplicate id
        fail_msgs = " ".join(i["msg"] for i in fails_bad)
        self.assertIn("lang", fail_msgs)
        self.assertIn("alt", fail_msgs)
        self.assertIn("Duplicate", fail_msgs)

    def test_aria_pattern_auditing(self):
        """Tests WAI-ARIA 1.2 modal dialog and tablist scanner."""
        # 1. Broken Modal & Fake button
        broken_aria = """
        <div>
            <!-- Broken dialog without name or modal -->
            <div role="dialog">
                <p>Delete account?</p>
            </div>

            <!-- Fake button with click but no role or tabindex -->
            <div onclick="doSomething()">Click Me</div>

            <!-- Tab without aria-selected -->
            <div role="tablist">
                <div role="tab">Tab 1</div>
            </div>
        </div>
        """
        f = self.work_dir / "broken.html"
        f.write_text(broken_aria, encoding="utf-8")

        issues = audit_file_aria(f)
        fails = [i for i in issues if i["severity"] == "FAIL"]
        self.assertGreaterEqual(len(fails), 3)

        patterns = [i["pattern"] for i in fails]
        self.assertIn("Dialog (Modal)", patterns)
        self.assertIn("Keyboard Navigation", patterns)
        self.assertIn("Tablist", patterns)


if __name__ == "__main__":
    unittest.main()
