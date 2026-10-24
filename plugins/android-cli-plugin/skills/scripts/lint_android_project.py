#!/usr/bin/env python3
"""
lint_android_project.py — Deterministic linter for Android manifests and Gradle configurations.
Enforces Android 12+ exported component rules, Google Play targetSdk requirements,
Java 17 compatibility, and security best practices.

Usage:
  python lint_android_project.py <path/to/android/project_or_manifest> [--json]

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import re
import json
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional

ANDROID_NAMESPACE = "{http://schemas.android.com/apk/res/android}"


def audit_manifest(manifest_path: Path) -> List[Dict[str, str]]:
    """Audit AndroidManifest.xml for security, Android 12+ compliance, and attributes."""
    findings = []
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
    except Exception as e:
        return [{"severity": "CRITICAL", "message": f"XML parsing error in manifest: {e}"}]

    # 1. Package or namespace
    package = root.attrib.get("package")
    if not package:
        findings.append({
            "severity": "WARNING",
            "message": "Missing 'package' attribute in <manifest>. Ensure 'namespace' is defined in build.gradle."
        })

    app_elem = root.find("application")
    if app_elem is None:
        findings.append({
            "severity": "CRITICAL",
            "message": "Manifest is missing <application> tag."
        })
        return findings

    # Check allowBackup
    allow_backup = app_elem.attrib.get(f"{ANDROID_NAMESPACE}allowBackup")
    if allow_backup is None:
        findings.append({
            "severity": "WARNING",
            "message": "<application> does not explicitly set android:allowBackup. Defaults to true; recommend explicit declaration."
        })

    # 2. Check Android 12+ android:exported requirement on components with intent-filters
    component_tags = ["activity", "service", "receiver"]
    for tag in component_tags:
        for comp in app_elem.findall(tag):
            comp_name = comp.attrib.get(f"{ANDROID_NAMESPACE}name", "Unnamed")
            intent_filters = comp.findall("intent-filter")
            exported_attr = comp.attrib.get(f"{ANDROID_NAMESPACE}exported")

            if intent_filters and exported_attr is None:
                findings.append({
                    "severity": "CRITICAL",
                    "message": f"<{tag} android:name='{comp_name}'> has <intent-filter> but is missing 'android:exported'. Mandatory on Android 12+ (API 31+)."
                })

    return findings


def audit_gradle(gradle_path: Path) -> List[Dict[str, str]]:
    """Audit build.gradle or build.gradle.kts for SDK compliance and Java versions."""
    findings = []
    try:
        content = gradle_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{"severity": "CRITICAL", "message": f"Read error on {gradle_path.name}: {e}"}]

    # Min / Target / Compile SDK checks
    compile_sdk_match = re.search(r"compileSdk(?:Version)?\s*=?\s*(\d+)", content)
    target_sdk_match = re.search(r"targetSdk(?:Version)?\s*=?\s*(\d+)", content)
    min_sdk_match = re.search(r"minSdk(?:Version)?\s*=?\s*(\d+)", content)

    compile_sdk = int(compile_sdk_match.group(1)) if compile_sdk_match else None
    target_sdk = int(target_sdk_match.group(1)) if target_sdk_match else None
    min_sdk = int(min_sdk_match.group(1)) if min_sdk_match else None

    if target_sdk is not None:
        if target_sdk < 34:
            findings.append({
                "severity": "WARNING",
                "message": f"targetSdk ({target_sdk}) is below API 34. Google Play requires targetSdk >= 34 for new app and update submissions."
            })

    if compile_sdk is not None and target_sdk is not None:
        if compile_sdk < target_sdk:
            findings.append({
                "severity": "CRITICAL",
                "message": f"compileSdk ({compile_sdk}) is lower than targetSdk ({target_sdk}). compileSdk must be >= targetSdk."
            })

    if min_sdk is not None and target_sdk is not None:
        if min_sdk > target_sdk:
            findings.append({
                "severity": "CRITICAL",
                "message": f"minSdk ({min_sdk}) is greater than targetSdk ({target_sdk})."
            })

    # Java 17 check for Android Gradle Plugin 8+
    if "JavaVersion.VERSION_1_" in content:
        old_java = re.search(r"JavaVersion\.VERSION_1_([0-8])", content)
        if old_java:
            findings.append({
                "severity": "WARNING",
                "message": f"Legacy Java target detected (Java 1.{old_java.group(1)}). Android Gradle Plugin 8.0+ requires Java 17."
            })

    return findings


def audit_project(target: Path) -> Dict[str, Any]:
    """Audit project directory or specific file."""
    all_findings: List[Dict[str, str]] = []
    files_audited: List[str] = []

    if target.is_file():
        if target.name == "AndroidManifest.xml":
            all_findings.extend(audit_manifest(target))
            files_audited.append(str(target))
        elif "build.gradle" in target.name:
            all_findings.extend(audit_gradle(target))
            files_audited.append(str(target))
        else:
            all_findings.append({"severity": "WARNING", "message": f"Unsupported file type: {target.name}"})
    elif target.is_dir():
        # Search for manifests
        for mf in target.glob("**/AndroidManifest.xml"):
            if "build/" not in str(mf).replace("\\", "/"):
                all_findings.extend(audit_manifest(mf))
                files_audited.append(str(mf))

        # Search for build.gradle files
        for bg in list(target.glob("**/build.gradle")) + list(target.glob("**/build.gradle.kts")):
            if "build/" not in str(bg).replace("\\", "/"):
                all_findings.extend(audit_gradle(bg))
                files_audited.append(str(bg))

    critical_count = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
    warning_count = sum(1 for f in all_findings if f["severity"] == "WARNING")

    if critical_count > 0:
        score = max(0, 100 - (critical_count * 30 + warning_count * 10))
        status = "FAIL"
    elif warning_count > 0:
        score = max(70, 100 - (warning_count * 10))
        status = "WARN"
    else:
        score = 100
        status = "PASS"

    return {
        "target": str(target),
        "files_audited": files_audited,
        "status": status,
        "score": score,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "findings": all_findings
    }


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Lint Android manifests and Gradle configs.")
    parser.add_argument("path", help="Path to project directory or file.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    report = audit_project(target_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=" * 64)
        print("          ANDROID PROJECT & MANIFEST QUALITY AUDIT           ")
        print("=" * 64)
        print(f"Target Path    : {report['target']}")
        print(f"Files Audited  : {len(report['files_audited'])}")
        print(f"Audit Score    : {report['score']} / 100")
        print(f"Status         : {report['status']}")
        print(f"Issues         : {len(report['findings'])} ({report['critical_count']} critical, {report['warning_count']} warning)")
        print("-" * 64)
        if not report["findings"]:
            print("  [✓] All manifest and Gradle quality checks passed cleanly.")
        else:
            for f in report["findings"]:
                badge = "[CRITICAL]" if f["severity"] == "CRITICAL" else "[WARNING] "
                print(f"  {badge} {f['message']}")
        print("=" * 64)

    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
