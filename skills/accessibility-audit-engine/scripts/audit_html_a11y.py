#!/usr/bin/env python3
"""HTML Offline Accessibility (a11y) Scanner.

Validates HTML markup against core WCAG 2.2 Level AA requirements:
- WCAG 1.1.1: Missing 'alt' on <img> or image inputs
- WCAG 1.3.1 / 4.1.2: Form controls without labels or ARIA labels
- WCAG 2.4.2: Missing page <title>
- WCAG 2.4.3: Focus order violations (positive tabindex)
- WCAG 2.4.4 / 4.1.2: Empty interactive elements (<button>, <a>)
- WCAG 2.5.8: Target size violations (< 24px)
- WCAG 3.1.1: Missing 'lang' attribute on <html>
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


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

        # 3. Check <img> alt
        if tag == "img":
            if "alt" not in attr_dict:
                self.issues.append({
                    "severity": "FAIL",
                    "wcag": "1.1.1 (Level A)",
                    "line": line,
                    "msg": "<img> tag is missing an 'alt' attribute. Use alt='' for decorative images."
                })

        # 4. Check form controls
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

        # 5. Check positive tabindex
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

        # 6. Check interactive buttons/links
        if tag in ("button", "a"):
            self.in_interactive = True
            self.current_interactive_tag = tag
            self.current_interactive_line = line
            self.interactive_has_text = False
            self.interactive_has_aria = bool(attr_dict.get("aria-label") or attr_dict.get("aria-labelledby"))

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


def main() -> None:
    parser = argparse.ArgumentParser(description="HTML Accessibility (a11y) Scanner")
    parser.add_argument("path", help="Path to HTML file or directory to scan")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    files = [target] if target.is_file() else sorted(target.glob("**/*.html"))
    if not files:
        print(f"No HTML files found in '{target}'.")
        sys.exit(0)

    total_fails = 0
    total_warns = 0

    print("=" * 70)
    print(" WCAG 2.2 Level AA Offline HTML Accessibility Audit")
    print("=" * 70)

    for f in files:
        issues = audit_html_file(f)
        if not issues:
            print(f"[PASS] {f.name}")
            continue

        fails = [i for i in issues if i["severity"] == "FAIL"]
        warns = [i for i in issues if i["severity"] == "WARN"]
        total_fails += len(fails)
        total_warns += len(warns)

        status = "[FAIL]" if fails else "[WARN]"
        print(f"{status} {f.name} ({len(fails)} errors, {len(warns)} warnings):")
        for i in issues:
            print(f"  Line {i['line']}: [{i['severity']}] [{i['wcag']}] {i['msg']}")

    print("-" * 70)
    print(f"Summary: {len(files)} files scanned | Errors: {total_fails} | Warnings: {total_warns}")
    if total_fails > 0:
        print("Verdict: REJECTED (Accessibility violations must be resolved)")
        sys.exit(1)
    else:
        print("Verdict: APPROVED (Compliant with core WCAG 2.2 rules)")
        sys.exit(0)


if __name__ == "__main__":
    main()
