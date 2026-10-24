#!/usr/bin/env python3
"""
test_android_cli.py — Unit test suite for Android CLI companion scripts.
Verifies layout parsing, ADB coordinate resolution, accessibility checks,
environment diagnostics, and manifest/Gradle quality gates.
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

import diagnose_android_env as diag
import parse_android_layout as layout_parser
import lint_android_project as linter


class TestDiagnoseAndroidEnv(unittest.TestCase):
    def test_diagnose_structure(self):
        report = diag.diagnose_environment()
        self.assertIn("platform", report)
        self.assertIn("sdk", report)
        self.assertIn("java", report)
        self.assertIn("tools", report)
        self.assertIn("devices", report)
        self.assertIn("avds", report)
        self.assertIn("ready_for_development", report)


class TestParseAndroidLayout(unittest.TestCase):
    def test_parse_bounds_and_center(self):
        bounds = layout_parser.parse_bounds("[100,200][500,700]")
        self.assertEqual(bounds, (100, 200, 500, 700))

        center = layout_parser.calculate_center(bounds)
        self.assertEqual(center, (300, 450))

        center_parsed = layout_parser.parse_center("[300,450]")
        self.assertEqual(center_parsed, (300, 450))

    def test_find_elements(self):
        sample_elements = [
            {
                "resourceId": "com.example.app:id/submit_button",
                "text": "Submit Form",
                "contentDesc": "Submit button",
                "interactions": ["clickable"],
                "bounds": "[50,100][250,200]"
            },
            {
                "resourceId": "com.example.app:id/title_text",
                "text": "User Registration",
                "bounds": "[50,20][400,80]"
            }
        ]

        # By text
        matches = layout_parser.find_elements(sample_elements, text_query="submit")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["resourceId"], "com.example.app:id/submit_button")

        # Clickable only
        clickable = layout_parser.find_elements(sample_elements, clickable_only=True)
        self.assertEqual(len(clickable), 1)

    def test_audit_layout_accessibility(self):
        sample_elements = [
            {
                "resourceId": "com.example.app:id/bad_icon_btn",
                "text": "",
                "contentDesc": "",
                "interactions": ["clickable"],
                "bounds": "[10,10][30,30]"  # < 48x48 and no label!
            }
        ]
        report = layout_parser.audit_layout_accessibility(sample_elements)
        self.assertEqual(report["violations_found"], 2)  # Missing label + too small target
        self.assertTrue(any(f["severity"] == "CRITICAL" for f in report["findings"]))
        self.assertTrue(any("Touch target is too small" in f["issue"] for f in report["findings"]))

    def test_diff_layouts(self):
        prev = [{"resourceId": "id1", "text": "Old", "bounds": "[0,0][10,10]"}]
        curr = [
            {"resourceId": "id1", "text": "Old", "bounds": "[0,0][10,10]"},
            {"resourceId": "id2", "text": "New", "bounds": "[20,20][50,50]"}
        ]
        diff = layout_parser.diff_layouts(prev, curr)
        self.assertEqual(diff["added_count"], 1)
        self.assertEqual(diff["removed_count"], 0)


class TestLintAndroidProject(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="android_lint_test_")
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_manifest_missing_exported(self):
        bad_manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.app">
    <application android:allowBackup="true">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
        mf_path = self.root / "AndroidManifest.xml"
        mf_path.write_text(bad_manifest, encoding="utf-8")

        findings = linter.audit_manifest(mf_path)
        self.assertTrue(any(f["severity"] == "CRITICAL" and "android:exported" in f["message"] for f in findings))

    def test_audit_manifest_compliant_exported(self):
        good_manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.app">
    <application android:allowBackup="true">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
        mf_path = self.root / "AndroidManifest.xml"
        mf_path.write_text(good_manifest, encoding="utf-8")

        findings = linter.audit_manifest(mf_path)
        self.assertEqual(len(findings), 0)

    def test_audit_gradle_sdk_mismatch(self):
        bad_gradle = """
        android {
            compileSdk 33
            defaultConfig {
                minSdk 24
                targetSdk 34
            }
        }
        """
        g_path = self.root / "build.gradle"
        g_path.write_text(bad_gradle, encoding="utf-8")

        findings = linter.audit_gradle(g_path)
        self.assertTrue(any("compileSdk (33) is lower than targetSdk (34)" in f["message"] for f in findings))


if __name__ == "__main__":
    unittest.main()
