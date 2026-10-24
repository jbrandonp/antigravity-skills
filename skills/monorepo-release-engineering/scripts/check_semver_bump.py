#!/usr/bin/env python3
"""Conventional Commits & Semantic Versioning (SemVer) Bump Calculator.

Analyzes git commit messages to determine the next Semantic Version:
- BREAKING CHANGE or 'type!:' -> MAJOR bump (X.0.0)
- 'feat:'                     -> MINOR bump (x.Y.0)
- 'fix:' / 'perf:' / 'refactor:' -> PATCH bump (x.y.Z)
- Generates automated categorized changelogs
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys


def parse_commits(commit_messages: list[str]) -> tuple[str, dict[str, list[str]]]:
    bump = "PATCH"
    categories = {
        "Breaking Changes": [],
        "Features": [],
        "Bug Fixes": [],
        "Performance & Refactoring": [],
        "Other": []
    }

    for msg in commit_messages:
        clean = msg.strip()
        if not clean:
            continue

        # Check for Breaking Change
        if "BREAKING CHANGE:" in clean or re.search(r"^[a-z]+(\([^)]+\))?!:", clean):
            bump = "MAJOR"
            categories["Breaking Changes"].append(clean)
            continue

        # Check for Feat
        if re.search(r"^feat(\([^)]+\))?:", clean):
            if bump != "MAJOR":
                bump = "MINOR"
            categories["Features"].append(clean)
            continue

        # Check for Fix
        if re.search(r"^fix(\([^)]+\))?:", clean):
            categories["Bug Fixes"].append(clean)
            continue

        # Check for Perf / Refactor
        if re.search(r"^(perf|refactor)(\([^)]+\))?:", clean):
            categories["Performance & Refactoring"].append(clean)
            continue

        categories["Other"].append(clean)

    return bump, categories


def bump_version(current_version: str, bump_type: str) -> str:
    v_clean = current_version.lstrip("v")
    parts = [int(p) for p in v_clean.split(".")]
    while len(parts) < 3:
        parts.append(0)

    major, minor, patch = parts[0], parts[1], parts[2]

    if bump_type == "MAJOR":
        return f"{major + 1}.0.0"
    elif bump_type == "MINOR":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def get_git_commits(from_tag: str | None = None) -> list[str]:
    cmd = ["git", "log", "--pretty=format:%s"]
    if from_tag:
        cmd.append(f"{from_tag}..HEAD")
    else:
        cmd.extend(["-n", "30"])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.splitlines()
    except Exception as e:
        print(f"Warning: git command failed: {e}", file=sys.stderr)
        return []


def main() -> None:
    parser = argparse.ArgumentParser(description="SemVer Bump Calculator & Changelog Generator")
    parser.add_argument("--current", default="1.0.0", help="Current version string (e.g. 1.2.3)")
    parser.add_argument("--tag", help="Git tag to read commits from (e.g. v1.2.3..HEAD)")
    parser.add_argument("--file", help="Path to text file containing commit messages (one per line)")
    args = parser.parse_args()

    if args.file:
        commits = Path(args.file).read_text(encoding="utf-8").splitlines()
    else:
        commits = get_git_commits(args.tag)

    if not commits:
        print("No commits found to analyze.")
        sys.exit(0)

    bump_type, categories = parse_commits(commits)
    next_ver = bump_version(args.current, bump_type)

    print("=" * 65)
    print(" Semantic Versioning (SemVer) Analysis")
    print("=" * 65)
    print(f"Current Version  : {args.current}")
    print(f"Detected Bump    : {bump_type}")
    print(f"Next Version     : {next_ver}")
    print("-" * 65)
    print(" Categorized Changelog Preview:")
    print("-" * 65)

    for cat_name, items in categories.items():
        if items:
            print(f"\n### {cat_name}")
            for it in items:
                print(f"- {it}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
