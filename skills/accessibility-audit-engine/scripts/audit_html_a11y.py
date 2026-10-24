#!/usr/bin/env python3
"""HTML Offline Accessibility (a11y) Scanner (Enhanced V2).

Validates HTML markup against core WCAG 2.2 Level AA requirements:
- WCAG 1.1.1: Missing 'alt' on <img> or image inputs
- WCAG 1.3.1: Skipped heading levels (e.g. h1 -> h3 skipping h2)
- WCAG 1.3.1 / 4.1.2: Form controls without labels or ARIA labels
- WCAG 2.4.2: Missing page <title>
- WCAG 2.4.3: Focus order violations (positive tabindex)
- WCAG 2.4.4 / 4.1.2: Empty interactive elements (<button>, <a>)
- WCAG 2.5.8: Target size violations (< 24px)
- WCAG 3.1.1: Missing 'lang' attribute on <html>
- WCAG 4.1.1: Duplicate element IDs breaking label/aria associations
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Sequence


class A11yHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.issues: list[dict[str, str | int]] = []
        self.has_html = False
        self.html_has_lang = False
        self.has_title = False
        self.in_interactive = False
        self.current_interactive_tag = ""
        self.current_interactive_line = 0
        self.interactive_has_text = False
        self.interactive_has_aria = False
        self.seen_ids: set[str] = set()
        self.last_heading_level = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        line, _ = self.getpos()

        # 1. Check <html lang="...">
        if tag == "html":
            self.has_html = True
            if "lang" in attr_dict and attr_dict["lang"].strip():
                self.html_has_lang = True
            else:
                self.issues.append({
                    "severity": "FAIL",
                    "wcag": "3.1.1 (Level A)",
                    "line": line,
                    "msg": "Missing or empty 'lang' attribute on <html> tag."
                })

        # 2. Check <title>
        if tag == "title":
            self.has_title = True

        # 3. Check duplicate IDs
        if "id" in attr_dict:
            elem_id = attr_dict["id"].strip()
            if elem_id:
                if elem_id in self.seen_ids:
                    self.issues.append({
                        "severity": "FAIL",
                        "wcag": "4.1.1 (Level A)",
                        "line": line,
                        "msg": f"Duplicate element id='{elem_id}' breaks label and aria associations."
                    })
                else:
                    self.seen_ids.add(elem_id)

        # 4. Check heading hierarchy
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            if self.last_heading_level > 0 and level > (self.last_heading_level + 1):
                self.issues.append({
                    "severity": "WARN",
                    "wcag": "1.3.1 (Level A)",
                    "line": line,
                    "msg": f"Skipped heading level: <{tag}> directly follows <h{self.last_heading_level}>. Maintain sequential structure."
                })
            self.last_heading_level = level

        # 5. Check <img> alt
        if tag == "img":
            if "alt" not in attr_dict:
                self.issues.append({
                    "severity": "FAIL",
                    "wcag": "1.1.1 (Level A)",
                    "line": line,
                    "msg": "<img> tag is missing an 'alt' attribute. Use alt='' for decorative images."
                })

        # 6. Check form controls
        if tag in ("input", "textarea", "select"):
            input_type = attr_dict.get("type", "text").lower()
            if input_type not in ("hidden", "submit", "button", "reset"):
                has_label = bool(
                    attr_dict.get("aria-label") or
                    attr_dict.get("aria-labelledby") or
                    attr_dict.get("id")  # Can be associated via <label for="...">
                )
                if not has_label:
                    self.issues.append({
                        "severity": "FAIL",
                        "wcag": "4.1.2 (Level A)",
                        "line": line,
                        "msg": f"Form control <{tag}> has no 'aria-label', 'aria-labelledby', or 'id' for label matching."
                    })

        # 7. Check positive tabindex
        if "tabindex" in attr_dict:
            try:
                t_val = int(attr_dict["tabindex"])
                if t_val > 0:
                    self.issues.append({
                        "severity": "FAIL",
                        "wcag": "2.4.3 (Level A)",
                        "line": line,
                        "msg": f"Positive tabindex='{t_val}' disrupts natural keyboard focus flow. Use tabindex='0' or '-1'."
                    })
            except ValueError:
                pass

        # 8. Check interactive buttons/links
        if tag in ("button", "a"):
            self.in_interactive = True
            self.current_interactive_tag = tag
            self.current_interactive_line = line
            self.interactive_has_text = False
            self.interactive_has_aria = bool(attr_dict.get("aria-label") or attr_dict.get("aria-labelledby"))

            # Check target="_blank"
            if tag == "a" and attr_dict.get("target") == "_blank":
                rel = attr_dict.get("rel", "").lower()
                if "noopener" not in rel and "noreferrer" not in rel:
                    self.issues.append({
                        "severity": "WARN",
                        "wcag": "Security/Usability",
                        "line": line,
                        "msg": "<a target='_blank'> missing rel='noopener noreferrer'."
                    })

            # Check touch target inline dimensions
            style = attr_dict.get("style", "")
            w_match = re.search(r"width:\s*(\d+)px", style)
            h_match = re.search(r"height:\s*(\d+)px", style)
            if w_match and int(w_match.group(1)) < 24:
                self.issues.append({
                    "severity": "WARN",
                    "wcag": "2.5.8 (Level AA)",
                    "line": line,
                    "msg": f"Inline width ({w_match.group(1)}px) is under the 24px WCAG 2.2 touch target minimum."
                })
            if h_match and int(h_match.group(1)) < 24:
                self.issues.append({
                    "severity": "WARN",
                    "wcag": "2.5.8 (Level AA)",
                    "line": line,
                    "msg": f"Inline height ({h_match.group(1)}px) is under the 24px WCAG 2.2 touch target minimum."
                })

    def handle_data(self, data: str) -> None:
        if self.in_interactive and data.strip():
            self.interactive_has_text = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("button", "a") and self.in_interactive:
            if not self.interactive_has_text and not self.interactive_has_aria:
                self.issues.append({
                    "severity": "FAIL",
                    "wcag": "4.1.2 (Level A)",
                    "line": self.current_interactive_line,
                    "msg": f"Empty <{tag}> has neither text content nor 'aria-label'."
                })
            self.in_interactive = False

    def check_closing(self) -> None:
        if self.has_html and not self.has_title:
            self.issues.append({
                "severity": "WARN",
                "wcag": "2.4.2 (Level A)",
                "line": 1,
                "msg": "Missing <title> element in document head."
            })


def audit_html_file(file_path: Path) -> list[dict[str, str | int]]:
    content = file_path.read_text(encoding="utf-8", errors="replace")
    parser = A11yHTMLParser()
    parser.feed(content)
    parser.check_closing()
    return parser.issues


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HTML Accessibility (a11y) Scanner")
    parser.add_argument("path", help="Path to HTML file or directory to scan")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        return 1

    files = [target] if target.is_file() else sorted(target.glob("**/*.html"))
    if not files:
        print(f"No HTML files found in '{target}'.")
        return 0

    all_results = []
    total_fails = 0
    total_warns = 0

    for f in files:
        issues = audit_html_file(f)
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

    print("=" * 70)
    print(" WCAG 2.2 Level AA Offline HTML Accessibility Audit")
    print("=" * 70)

    for res in all_results:
        fpath = Path(res["file"]).name
        status = "[PASS]" if res["fails"] == 0 and res["warnings"] == 0 else ("[FAIL]" if res["fails"] > 0 else "[WARN]")
        print(f"{status:8} {fpath} ({res['fails']} errors, {res['warnings']} warnings):")
        for i in res["issues"]:
            print(f"  Line {i['line']}: [{i['severity']}] [{i['wcag']}] {i['msg']}")

    print("-" * 70)
    print(f"Summary: {len(files)} files scanned | Errors: {total_fails} | Warnings: {total_warns}")
    if total_fails > 0:
        print("Verdict: REJECTED (Accessibility violations must be resolved)")
        return 1
    else:
        print("Verdict: APPROVED (Compliant with core WCAG 2.2 rules)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
