#!/usr/bin/env python3
"""
diagnose_android_env.py — Deterministic environment diagnostic and readiness checker for Android development.
Audits Android SDK, JDK, ADB, Android CLI, connected physical/virtual devices, and environment paths.

Usage:
  python diagnose_android_env.py [--json]

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import shutil
import subprocess
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional


def check_executable(cmd: str) -> Optional[str]:
    """Find absolute path of an executable in system PATH."""
    return shutil.which(cmd)


def run_cmd(args: List[str], timeout: int = 5) -> Optional[str]:
    """Run a shell command and return trimmed stdout, or None on failure."""
    try:
        res = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return res.stdout.strip()
        return (res.stdout + "\n" + res.stderr).strip()
    except Exception:
        return None


def get_android_sdk_path() -> Optional[Path]:
    """Locate Android SDK path from env vars or standard OS paths."""
    candidates = [
        os.environ.get("ANDROID_HOME"),
        os.environ.get("ANDROID_SDK_ROOT"),
    ]

    # Standard OS fallbacks
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            candidates.append(str(Path(local_app_data) / "Android" / "Sdk"))
    elif sys.platform == "darwin":
        candidates.append(str(Path.home() / "Library" / "Android" / "sdk"))
    else:
        candidates.append(str(Path.home() / "Android" / "Sdk"))

    for c in candidates:
        if c and Path(c).is_dir():
            return Path(c).resolve()
    return None


def get_java_home() -> Optional[Path]:
    """Locate JAVA_HOME from environment or standard paths."""
    jh = os.environ.get("JAVA_HOME")
    if jh and Path(jh).is_dir():
        return Path(jh).resolve()
    return None


def diagnose_environment() -> Dict[str, Union[str, Dict[str, Union[str, bool, int, List[str]]], List[str], List[Dict[str, str]]]] :
    """Perform comprehensive audit of Android development environment."""
    report: Dict[str, Union[str, Dict[str, Union[str, bool, int, List[str]]], List[str], List[Dict[str, str]]]] = {
        "platform": sys.platform,
        "sdk": {},
        "java": {},
        "tools": {},
        "devices": [],
        "avds": [],
        "recommendations": []
    }

    # 1. SDK Audit
    sdk_path = get_android_sdk_path()
    if sdk_path:
        report["sdk"]["path"] = str(sdk_path)
        report["sdk"]["valid"] = True
        # Check platforms and build-tools
        platforms_dir = sdk_path / "platforms"
        build_tools_dir = sdk_path / "build-tools"
        report["sdk"]["installed_platforms"] = [p.name for p in platforms_dir.iterdir() if p.is_dir()] if platforms_dir.is_dir() else []
        report["sdk"]["installed_build_tools"] = [b.name for b in build_tools_dir.iterdir() if b.is_dir()] if build_tools_dir.is_dir() else []
    else:
        report["sdk"]["valid"] = False
        report["recommendations"].append("Android SDK not found. Set ANDROID_HOME or install via Android Studio / Android CLI.")

    # 2. Java Audit
    java_home = get_java_home()
    java_exe = check_executable("java")
    report["java"]["java_home"] = str(java_home) if java_home else None
    report["java"]["java_in_path"] = bool(java_exe)

    if java_exe:
        ver_output = run_cmd(["java", "-version"])
        report["java"]["version_info"] = ver_output.splitlines()[0] if ver_output else "Available"
    else:
        report["recommendations"].append("Java runtime (JDK 17+) not found in PATH. Install OpenJDK 17 and configure JAVA_HOME.")

    # 3. Executable Tools Check
    tool_binaries = ["android", "adb", "emulator", "sdkmanager", "avdmanager", "gradle"]
    for tool in tool_binaries:
        exe_path = check_executable(tool)
        if not exe_path and sdk_path:
            # Check within SDK subdirectories
            sdk_candidates = [
                sdk_path / "platform-tools" / (f"{tool}.exe" if sys.platform == "win32" else tool),
                sdk_path / "cmdline-tools" / "latest" / "bin" / (f"{tool}.bat" if sys.platform == "win32" else tool),
                sdk_path / "emulator" / (f"{tool}.exe" if sys.platform == "win32" else tool)
            ]
            for cand in sdk_candidates:
                if cand.is_file():
                    exe_path = str(cand)
                    break

        report["tools"][tool] = {
            "found": bool(exe_path),
            "path": exe_path
        }

    # 4. Connected Devices (via adb)
    adb_found = report["tools"]["adb"]["found"]
    if adb_found:
        adb_cmd = report["tools"]["adb"]["path"] or "adb"
        dev_out = run_cmd([adb_cmd, "devices", "-l"])
        if dev_out:
            for line in dev_out.splitlines()[1:]:
                line = line.strip()
                if line and not line.startswith("*"):
                    report["devices"].append(line)

    # 5. Emulators (AVDs)
    emu_found = report["tools"]["emulator"]["found"]
    if emu_found:
        emu_cmd = report["tools"]["emulator"]["path"] or "emulator"
        avd_out = run_cmd([emu_cmd, "-list-avds"])
        if avd_out:
            report["avds"] = [a.strip() for a in avd_out.splitlines() if a.strip()]

    # Global readiness calculation
    ready_for_cli = report["tools"]["android"]["found"]
    ready_for_adb = report["tools"]["adb"]["found"] and bool(sdk_path)
    report["ready_for_development"] = bool(sdk_path and (ready_for_cli or ready_for_adb) and report["java"]["java_in_path"])

    return report


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Audit Android development environment readiness.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    args = parser.parse_args()

    report = diagnose_environment()

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("=" * 64)
    print("      ANDROID DEVELOPMENT ENVIRONMENT DIAGNOSTIC REPORT      ")
    print("=" * 64)
    print(f"Host OS Platform     : {report['platform']}")
    print(f"Android SDK Found    : {'YES' if report['sdk'].get('valid') else 'NO'}")
    if report['sdk'].get('valid'):
        print(f"  SDK Path           : {report['sdk']['path']}")
        print(f"  Platforms Installed: {', '.join(report['sdk']['installed_platforms']) or 'None'}")
        print(f"  Build Tools        : {', '.join(report['sdk']['installed_build_tools']) or 'None'}")

    print(f"JDK / Java Found     : {'YES' if report['java']['java_in_path'] else 'NO'}")
    if report['java']['java_in_path']:
        print(f"  Version            : {report['java'].get('version_info', 'Unknown')}")
        print(f"  JAVA_HOME          : {report['java']['java_home'] or 'Not set'}")

    print("-" * 64)
    print("Tool Availability:")
    for tool, info in report["tools"].items():
        status = "INSTALLED" if info["found"] else "MISSING"
        path_str = f" ({info['path']})" if info["found"] else ""
        print(f"  - {tool:12}: [{status}]{path_str}")

    print("-" * 64)
    print(f"Connected Devices    : {len(report['devices'])}")
    for dev in report['devices']:
        print(f"  • {dev}")

    print(f"Configured AVDs      : {len(report['avds'])}")
    for avd in report['avds']:
        print(f"  • {avd}")

    print("=" * 64)
    if report["recommendations"]:
        print("Actionable Recommendations:")
        for rec in report["recommendations"]:
            print(f"  [!] {rec}")
        print("=" * 64)

    return 0 if report["ready_for_development"] else 1


if __name__ == "__main__":
    sys.exit(main())
