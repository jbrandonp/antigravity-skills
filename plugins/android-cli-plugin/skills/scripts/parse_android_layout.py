#!/usr/bin/env python3
"""
parse_android_layout.py — Deterministic parser and action resolver for Android layout hierarchies.
Parses JSON dumps from `android layout`, computes tap/swipe coordinates for `adb shell input`,
diffs layout snapshots, and audits accessibility / touch target sizes.

Usage:
  python parse_android_layout.py layout.json --find-text "Submit" --action tap
  python parse_android_layout.py layout.json --find-id "com.example:id/login_btn"
  python parse_android_layout.py --diff prev_layout.json current_layout.json
  python parse_android_layout.py layout.json --audit-a11y

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


def parse_bounds(bounds_str: str) -> Optional[Tuple[int, int, int, int]]:
    """Parse bounds formatted as '[minX,minY][maxX,maxY]' into (minX, minY, maxX, maxY)."""
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_str.strip())
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    return None


def parse_center(center_str: str) -> Optional[Tuple[int, int]]:
    """Parse center formatted as '[x,y]' into (x, y)."""
    m = re.match(r"\[(\d+),(\d+)\]", center_str.strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def calculate_center(bounds: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Calculate center coordinates from bounds."""
    min_x, min_y, max_x, max_y = bounds
    return (min_x + max_x) // 2, (min_y + max_y) // 2


def flatten_layout(data: Any) -> List[Dict[str, Any]]:
    """Normalize hierarchical or flat layout JSON into a list of element dicts."""
    elements = []
    if isinstance(data, list):
        for item in data:
            elements.extend(flatten_layout(item))
    elif isinstance(data, dict):
        elements.append(data)
        children = data.get("children", [])
        if isinstance(children, list):
            elements.extend(flatten_layout(children))
    return elements


def find_elements(
    elements: List[Dict[str, Any]],
    text_query: Optional[str] = None,
    id_query: Optional[str] = None,
    desc_query: Optional[str] = None,
    clickable_only: bool = False
) -> List[Dict[str, Any]]:
    """Filter layout elements matching criteria."""
    matches = []
    for el in elements:
        if clickable_only:
            interactions = el.get("interactions", [])
            if "clickable" not in interactions and not el.get("clickable"):
                continue

        if text_query is not None:
            el_text = str(el.get("text", "")).lower()
            if text_query.lower() not in el_text:
                continue

        if id_query is not None:
            el_id = str(el.get("resourceId", "")).lower()
            if id_query.lower() not in el_id:
                continue

        if desc_query is not None:
            el_desc = str(el.get("contentDesc", "")).lower()
            if desc_query.lower() not in el_desc:
                continue

        matches.append(el)
    return matches


def audit_layout_accessibility(elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Audit accessibility and touch targets for UI elements."""
    findings = []
    checked_count = 0

    for idx, el in enumerate(elements):
        interactions = el.get("interactions", [])
        is_clickable = "clickable" in interactions or bool(el.get("clickable"))
        if not is_clickable:
            continue

        checked_count += 1
        text = el.get("text", "").strip()
        content_desc = el.get("contentDesc", "").strip()
        resource_id = el.get("resourceId", f"element_{idx}")

        # Check for missing description
        if not text and not content_desc:
            findings.append({
                "severity": "CRITICAL",
                "element": resource_id,
                "issue": "Clickable element has no text label or accessibility contentDesc."
            })

        # Check touch target size (minimum 48x48)
        bounds_str = el.get("bounds")
        if bounds_str:
            b = parse_bounds(bounds_str)
            if b:
                width = b[2] - b[0]
                height = b[3] - b[1]
                if width < 48 or height < 48:
                    findings.append({
                        "severity": "WARNING",
                        "element": resource_id,
                        "issue": f"Touch target is too small ({width}x{height}px < 48x48px minimum target size)."
                    })

    return {
        "clickable_elements_audited": checked_count,
        "violations_found": len(findings),
        "score": max(0, 100 - len(findings) * 15),
        "findings": findings
    }


def diff_layouts(prev_elements: List[Dict[str, Any]], curr_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Diff two layout trees by element identifiers/signatures."""
    def elem_sig(e: Dict[str, Any]) -> str:
        return f"{e.get('resourceId', '')}|{e.get('text', '')}|{e.get('bounds', '')}"

    prev_sigs = {elem_sig(e): e for e in prev_elements}
    curr_sigs = {elem_sig(e): e for e in curr_elements}

    added = [e for sig, e in curr_sigs.items() if sig not in prev_sigs]
    removed = [e for sig, e in prev_sigs.items() if sig not in curr_sigs]

    return {
        "added_count": len(added),
        "removed_count": len(removed),
        "added_elements": added,
        "removed_elements": removed
    }


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Parse Android UI layout JSON and resolve ADB commands.")
    parser.add_argument("file", nargs="?", help="Path to the layout JSON file.")
    parser.add_argument("--find-text", help="Find elements containing this text.")
    parser.add_argument("--find-id", help="Find elements containing this resourceId.")
    parser.add_argument("--find-desc", help="Find elements containing this contentDesc.")
    parser.add_argument("--clickable-only", action="store_true", help="Match only clickable elements.")
    parser.add_argument("--action", choices=["tap", "swipe-up", "swipe-down"], help="Generate ADB input shell command.")
    parser.add_argument("--audit-a11y", action="store_true", help="Perform accessibility and touch target size audit.")
    parser.add_argument("--diff", nargs=2, metavar=("PREV", "CURR"), help="Diff two layout JSON snapshots.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")

    args = parser.parse_args()

    # Diff Mode
    if args.diff:
        p1 = Path(args.diff[0]).resolve()
        p2 = Path(args.diff[1]).resolve()
        if not p1.exists() or not p2.exists():
            print(f"Error: One or both diff files do not exist: {p1}, {p2}", file=sys.stderr)
            return 1
        d1 = flatten_layout(json.loads(p1.read_text(encoding="utf-8")))
        d2 = flatten_layout(json.loads(p2.read_text(encoding="utf-8")))
        diff_res = diff_layouts(d1, d2)
        if args.json:
            print(json.dumps(diff_res, indent=2))
        else:
            print(f"Layout Diff: +{diff_res['added_count']} added, -{diff_res['removed_count']} removed elements.")
            for el in diff_res["added_elements"]:
                print(f"  [+] {el.get('resourceId') or el.get('text') or 'Element'} (bounds: {el.get('bounds')})")
            for el in diff_res["removed_elements"]:
                print(f"  [-] {el.get('resourceId') or el.get('text') or 'Element'} (bounds: {el.get('bounds')})")
        return 0

    if not args.file:
        parser.print_help()
        return 1

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    try:
        raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error parsing JSON from {file_path}: {e}", file=sys.stderr)
        return 1

    elements = flatten_layout(raw_data)

    # Accessibility Audit Mode
    if args.audit_a11y:
        a11y_report = audit_layout_accessibility(elements)
        if args.json:
            print(json.dumps(a11y_report, indent=2))
        else:
            print("=" * 64)
            print("         ANDROID UI ACCESSIBILITY & TARGET SIZE AUDIT         ")
            print("=" * 64)
            print(f"Clickable Elements Checked : {a11y_report['clickable_elements_audited']}")
            print(f"Violations Found          : {a11y_report['violations_found']}")
            print(f"A11y Score                : {a11y_report['score']} / 100")
            print("-" * 64)
            for f in a11y_report["findings"]:
                print(f"  [{f['severity']}] {f['element']}: {f['issue']}")
            print("=" * 64)
        return 0 if a11y_report["violations_found"] == 0 else 1

    # Search & Action Mode
    matches = find_elements(
        elements,
        text_query=args.find_text,
        id_query=args.find_id,
        desc_query=args.find_desc,
        clickable_only=args.clickable_only
    )

    if args.json:
        print(json.dumps(matches, indent=2))
        return 0

    print(f"Found {len(matches)} matching UI element(s):")
    for idx, el in enumerate(matches, 1):
        center_coords = None
        if el.get("center"):
            center_coords = parse_center(el["center"])
        elif el.get("bounds"):
            b = parse_bounds(el["bounds"])
            if b:
                center_coords = calculate_center(b)

        print(f"\n[{idx}] {el.get('class', 'View')}")
        print(f"    Resource ID  : {el.get('resourceId', 'None')}")
        print(f"    Text         : {el.get('text', 'None')}")
        print(f"    ContentDesc  : {el.get('contentDesc', 'None')}")
        print(f"    Bounds       : {el.get('bounds', 'None')}")
        print(f"    Center       : {center_coords if center_coords else 'Unknown'}")

        if args.action and center_coords:
            cx, cy = center_coords
            if args.action == "tap":
                print(f"    >>> ADB Command: adb shell input tap {cx} {cy}")
            elif args.action == "swipe-up":
                print(f"    >>> ADB Command: adb shell input swipe {cx} {cy + 300} {cx} {cy - 300} 300")
            elif args.action == "swipe-down":
                print(f"    >>> ADB Command: adb shell input swipe {cx} {cy - 300} {cx} {cy + 300} 300")

    return 0


if __name__ == "__main__":
    sys.exit(main())
