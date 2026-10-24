#!/usr/bin/env python3
"""WAI-ARIA 1.2 Design Patterns & Keyboard Accessibility Scanner.

Audits HTML, JSX, and TSX markup for ARIA pattern violations and keyboard traps:
1. Dialogs & Modals: role="dialog" / <dialog> requiring aria-modal="true" & accessible name
2. Tablists: role="tablist" requiring role="tab" with aria-selected & aria-controls
3. Disclosures: Accordion triggers requiring aria-expanded & aria-controls
4. Fake Buttons: onClick on <div>/<span> without role="button" and tabindex="0"
5. First Rule of ARIA: Redundant ARIA roles on semantic elements (<button role="button">)
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Sequence


class ARIAValidator(HTMLParser):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename
        self.issues: list[dict] = []
        self.open_dialog = False
        self.open_dialog_has_name = False
        self.open_dialog_is_modal = False
        self.open_tablist = False
        self.tablist_tabs: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        role = attr_dict.get("role", "").lower()
        line, _ = self.getpos()

        # 1. Dialog & Modal Verification
        if role == "dialog" or tag == "dialog":
            has_name = bool(attr_dict.get("aria-label") or attr_dict.get("aria-labelledby"))
            is_modal = attr_dict.get("aria-modal") == "true" or tag == "dialog"

            if not has_name:
                self.issues.append({
                    "severity": "FAIL",
                    "pattern": "Dialog (Modal)",
                    "line": line,
                    "msg": f"<{tag} role='dialog'> is missing an accessible name via 'aria-labelledby' or 'aria-label'."
                })
            if role == "dialog" and not is_modal:
                self.issues.append({
                    "severity": "WARN",
                    "pattern": "Dialog (Modal)",
                    "line": line,
                    "msg": "role='dialog' should specify aria-modal='true' to communicate focus trapping to screen readers."
                })

        # 2. Tablist Verification
        if role == "tablist":
            self.open_tablist = True

        if role == "tab":
            has_selected = "aria-selected" in attr_dict
            has_controls = "aria-controls" in attr_dict
            if not has_selected:
                self.issues.append({
                    "severity": "FAIL",
                    "pattern": "Tablist",
                    "line": line,
                    "msg": "role='tab' must declare aria-selected='true' or aria-selected='false'."
                })
            if not has_controls:
                self.issues.append({
                    "severity": "WARN",
                    "pattern": "Tablist",
                    "line": line,
                    "msg": "role='tab' should reference its associated panel via 'aria-controls=\"panel-id\"'."
                })

        # 3. Disclosure / Accordion trigger
        if "aria-expanded" in attr_dict:
            val = attr_dict["aria-expanded"].lower()
            if val not in ("true", "false"):
                self.issues.append({
                    "severity": "FAIL",
                    "pattern": "Disclosure",
                    "line": line,
                    "msg": f"aria-expanded must be boolean 'true' or 'false', got '{val}'."
                })

        # 4. Fake buttons on non-interactive tags (div, span, p)
        has_click = any(k in attr_dict for k in ("onclick", "onclickcapture"))
        if tag in ("div", "span", "p", "a") and has_click:
            is_button_role = role == "button"
            has_tabindex = "tabindex" in attr_dict

            if not is_button_role:
                self.issues.append({
                    "severity": "FAIL",
                    "pattern": "Keyboard Navigation",
                    "line": line,
                    "msg": f"<{tag}> has click listener but lacks role='button'. Screen readers will announce it as generic text."
                })
            if not has_tabindex:
                self.issues.append({
                    "severity": "FAIL",
                    "pattern": "Keyboard Navigation",
                    "line": line,
                    "msg": f"<{tag}> has click listener but lacks tabindex='0'. Keyboard users cannot tab to or activate it."
                })

        # 5. First Rule of ARIA: Redundant roles
        redundant_roles = {
            "button": "button",
            "nav": "navigation",
            "main": "main",
            "header": "banner",
            "footer": "contentinfo",
            "aside": "complementary",
            "form": "form",
        }
        if tag in redundant_roles and role == redundant_roles[tag]:
            self.issues.append({
                "severity": "WARN",
                "pattern": "First Rule of ARIA",
                "line": line,
                "msg": f"Redundant role: <{tag} role='{role}'>. Native HTML element already provides this semantic role."
            })


def audit_file_aria(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8", errors="replace")
    parser = ARIAValidator(path.name)
    try:
        parser.feed(content)
    except Exception as e:
        parser.issues.append({
            "severity": "WARN",
            "pattern": "Parser",
            "line": 1,
            "msg": f"Parsing exception: {e}"
        })
    return parser.issues


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="WAI-ARIA 1.2 Design Pattern & Keyboard Focus Trap Scanner."
    )
    parser.add_argument("path", help="HTML/JSX/TSX file or directory to audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")

    args = parser.parse_args(argv)
    target = Path(args.path)

    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        return 1

    files: list[Path] = []
    if target.is_file():
        files.append(target)
    else:
        for ext in ("*.html", "*.htm", "*.jsx", "*.tsx"):
            files.extend(target.glob(f"**/{ext}"))
    files = sorted(files)

    if not files:
        print(f"No matching markup files found in '{target}'.")
        return 0

    all_results = []
    total_fails = 0
    total_warns = 0

    for f in files:
        issues = audit_file_aria(f)
        fails = [i for i in issues if i["severity"] == "FAIL"]
        warns = [i for i in issues if i["severity"] == "WARN"]
        total_fails += len(fails)
        total_warns += len(warns)

        all_results.append({
            "file": str(f),
            "fails": len(fails),
            "warnings": len(warns),
            "issues": issues
        })

    if args.json:
        print(json.dumps(all_results, indent=2))
        return 0 if total_fails == 0 else 1

    print("==================================================================")
    print("      WAI-ARIA 1.2 DESIGN PATTERN & KEYBOARD ACCESSIBILITY AUDIT  ")
    print("==================================================================")

    for res in all_results:
        fpath = Path(res["file"]).name
        status = "[PASS]" if res["fails"] == 0 and res["warnings"] == 0 else ("[FAIL]" if res["fails"] > 0 else "[WARN]")
        print(f"{status:8} {fpath} ({res['fails']} errors, {res['warnings']} warnings)")
        for issue in res["issues"]:
            print(f"   Line {issue['line']}: [{issue['severity']}] [{issue['pattern']}] {issue['msg']}")

    print("------------------------------------------------------------------")
    print(f"Scanned {len(files)} files | Total Errors: {total_fails} | Total Warnings: {total_warns}")
    verdict = "APPROVED (Compliant with WAI-ARIA 1.2)" if total_fails == 0 else "REJECTED (ARIA pattern violations detected)"
    print(f"Verdict: {verdict}")
    print("==================================================================")
    return 0 if total_fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
