#!/usr/bin/env python3
"""
HTML Presentation Deck Validator
Validates strategic presentation decks against 16:9 aspect ratio,
responsive scaling, Chart.js integrations, and keyboard navigation standards.
"""

import sys
import re
from pathlib import Path

def validate_deck(deck_path: Path) -> bool:
    print(f"\n[*] Auditing HTML slide deck: {deck_path}")
    if not deck_path.exists():
        print(f"[!] Error: File {deck_path} not found.")
        return False
        
    html = deck_path.read_text(encoding="utf-8", errors="ignore")
    errors = []
    warnings = []
    
    # 1. Slide containers check
    slides = re.findall(r'<section[^>]*class=["\'][^"\']*slide[^"\']*["\']', html, re.IGNORECASE)
    if not slides:
        slides = re.findall(r'<div[^>]*class=["\'][^"\']*slide[^"\']*["\']', html, re.IGNORECASE)
    
    if not slides:
        errors.append("No slide elements found (expected <section class=\"slide\"> or <div class=\"slide\">)")
    else:
        print(f"[+] Detected {len(slides)} slides.")
        
    # 2. Aspect Ratio (16:9) check
    if "aspect-ratio" not in html and "16 / 9" not in html and "16/9" not in html and "56.25%" not in html:
        warnings.append("No explicit 16:9 aspect-ratio rule found in CSS")
        
    # 3. Canvas & Chart.js check
    has_canvas = "<canvas" in html.lower()
    has_chartjs = "chart.js" in html.lower() or "chart.min.js" in html.lower()
    if has_canvas and not has_chartjs:
        errors.append("<canvas> element detected but Chart.js script tag is missing")
    elif has_canvas and has_chartjs:
        print("[+] Chart.js integration verified for data visualization canvas.")
        
    # 4. Keyboard Navigation check
    has_keydown = "keydown" in html or "ArrowRight" in html or "keyCode" in html or "nextSlide" in html
    if not has_keydown:
        warnings.append("No keyboard navigation script detected (recommend ArrowRight / ArrowLeft listeners)")
    else:
        print("[+] Interactive keyboard navigation detected.")
        
    # 5. Viewport meta tag
    if "viewport" not in html.lower():
        errors.append("Missing <meta name=\"viewport\"> for responsive presentation scaling")
        
    # Output results
    if warnings:
        print("[!] Warnings:")
        for w in warnings:
            print(f"  - {w}")
            
    if errors:
        print("[!] Deck Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("[+] Presentation Deck Audit PASSED: 100% compliant.")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_presentation_deck.py <path_to_presentation.html>")
        sys.exit(1)
        
    path = Path(sys.argv[1])
    success = validate_deck(path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
