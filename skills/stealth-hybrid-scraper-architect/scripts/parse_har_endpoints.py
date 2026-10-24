#!/usr/bin/env python3
"""
HAR to Python curl_cffi Synthesizer
Parses HTTP Archive (.har) files, filters out static web assets,
and generates executable Python curl_cffi requests with JA4 browser impersonation.
"""

import sys
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse

STATIC_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".css", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3"
}

def parse_har(har_path: Path, output_file: Path = None):
    print(f"\n[*] Ingesting and filtering HAR file: {har_path}")
    if not har_path.exists():
        print(f"[!] File not found: {har_path}")
        return False

    try:
        data = json.loads(har_path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as e:
        print(f"[!] JSON parsing error: {e}")
        return False

    entries = data.get("log", {}).get("entries", [])
    print(f"[+] Total raw network entries: {len(entries)}")

    api_endpoints = []
    for entry in entries:
        req = entry.get("request", {})
        res = entry.get("response", {})
        url = req.get("url", "")
        method = req.get("method", "GET")

        # Skip static assets
        path = urlparse(url).path.lower()
        if any(path.endswith(ext) for ext in STATIC_EXTENSIONS):
            continue

        mime_type = res.get("content", {}).get("mimeType", "").lower()
        if "json" in mime_type or "graphql" in mime_type or "api" in path:
            headers = {h["name"]: h["value"] for h in req.get("headers", []) if not h["name"].startswith(":")}
            post_data = req.get("postData", {}).get("text", "")
            status = res.get("status", 0)

            api_endpoints.append({
                "url": url,
                "method": method,
                "status": status,
                "headers": headers,
                "payload": post_data
            })

    print(f"[+] Identified {len(api_endpoints)} high-value API endpoints.")

    # Generate Python snippet for top endpoints
    if api_endpoints:
        first = api_endpoints[0]
        py_snippet = f'''# Generated curl_cffi client for {urlparse(first["url"]).netloc}
from curl_cffi import requests
import json

headers = {json.dumps({k: v for k, v in list(first["headers"].items())[:6]}, indent=4)}

# JA4 Fingerprint Spoofing with Chrome 120+ impersonation
session = requests.Session(impersonate="chrome")
response = session.{first["method"].lower()}(
    "{first["url"]}",
    headers=headers,
    timeout=15
)

print(f"Status: {{response.status_code}}")
print(response.json())
'''
        if output_file:
            output_file.write_text(py_snippet, encoding="utf-8")
            print(f"[+] Exported executable Python script: {output_file}")
        else:
            print("\n--- Sample Generated Client ---")
            print(py_snippet)

    return True

def main():
    parser = argparse.ArgumentParser(description="HAR to curl_cffi API Synthesizer")
    parser.add_argument("har_file", help="Path to .har file")
    parser.add_argument("-o", "--output", help="Output python file path")
    args = parser.parse_args()

    out_p = Path(args.output) if args.output else None
    parse_har(Path(args.har_file), out_p)

if __name__ == "__main__":
    main()
