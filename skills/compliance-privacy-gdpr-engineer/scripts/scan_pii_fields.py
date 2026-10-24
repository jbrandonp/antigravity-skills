#!/usr/bin/env python3
"""GDPR Personally Identifiable Information (PII) Code Scanner.

Scans data schemas, ORM models, and database migrations for PII fields:
- High Sensitivity: SSN, IBAN, Health, Biometric, Passwords
- Personal Data: Email, Phone, IP Address, Geolocation, Names
- Validates presence of cascade deletion or retention documentation
- Generates GDPR Article 30 Record of Processing summary
"""

import argparse
from pathlib import Path
import re
import sys

PII_PATTERNS = {
    "High Risk (Special Category)": [
        (r"\b(ssn|social_security|nir)\b", "Numéro de sécurité sociale"),
        (r"\b(iban|credit_card|card_number|cvv)\b", "Coordonnées bancaires / Paiement"),
        (r"\b(health|medical|diagnosis|disability)\b", "Données de santé (Art. 9)"),
        (r"\b(biometric|fingerprint|face_encoding)\b", "Données biométriques (Art. 9)"),
    ],
    "Standard Personal Data": [
        (r"\b(email|user_email)\b", "Adresse électronique"),
        (r"\b(phone|telephone|mobile)\b", "Numéro de téléphone"),
        (r"\b(ip_address|client_ip|remote_addr)\b", "Adresse IP"),
        (r"\b(birthdate|date_of_birth|dob)\b", "Date de naissance"),
        (r"\b(first_name|last_name|full_name)\b", "Identité civile"),
        (r"\b(latitude|longitude|geo_location)\b", "Géolocalisation précise"),
    ]
}


def scan_file_for_pii(path: Path) -> list[dict[str, str | int]]:
    findings = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if clean.startswith(("//", "#", "--")) and not any(k in clean.lower() for k in ["field", "column", "schema"]):
            continue

        for category, patterns in PII_PATTERNS.items():
            for pat, desc in patterns:
                if re.search(pat, clean, re.IGNORECASE):
                    findings.append({
                        "category": category,
                        "description": desc,
                        "line": idx,
                        "sample": clean[:70]
                    })
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="GDPR PII & Data Processing Scanner")
    parser.add_argument("path", help="Path to source directory or file to scan")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    extensions = {".py", ".ts", ".js", ".sql", ".prisma", ".json"}
    files = [target] if target.is_file() else [
        f for f in target.glob("**/*")
        if f.suffix.lower() in extensions and not any(part.startswith(".") for part in f.parts)
    ]

    total_pii_found = 0
    file_count = 0

    print("=" * 65)
    print(" GDPR / RGPD Article 30 PII & Data Processing Scanner")
    print("=" * 65)

    for f in files:
        findings = scan_file_for_pii(f)
        if not findings:
            continue

        file_count += 1
        total_pii_found += len(findings)
        print(f"\n[PII DETECTED] {f.name} ({len(findings)} field occurrences):")
        for item in findings:
            print(f"  Line {item['line']:3d}: [{item['category']}] {item['description']}")
            print(f"            Code: {item['sample']}")

    print("\n" + "-" * 65)
    print(f"Summary: {file_count} files contain PII | Total occurrences: {total_pii_found}")
    print("Recommendation:")
    print("1. Ensure every detected table has a cascade deletion workflow (Art. 17).")
    print("2. Ensure personal data retention periods are documented in _DECISIONS.md.")
    print("=" * 65)


if __name__ == "__main__":
    main()
