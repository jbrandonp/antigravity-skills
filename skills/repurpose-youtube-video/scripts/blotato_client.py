#!/usr/bin/env python3
"""Blotato API Client for automated YouTube repurposing.

Extracts transcript & metadata, generates social copy for LinkedIn, Instagram, and X,
generates platform-specific visuals, and dispatches posts.
API reference: https://help.blotato.com/api/llm
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

def get_api_key():
    key = os.environ.get("BLOTATO_API_KEY", "").strip()
    if not key:
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("BLOTATO_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"')
                    break
    if not key:
        print(json.dumps({"error": "BLOTATO_API_KEY missing. Please set it in your environment or .env file."}, ensure_ascii=False))
        sys.exit(1)
    return key

def call_blotato(endpoint, payload):
    key = get_api_key()
    url = f"https://api.blotato.com/v1/{endpoint.lstrip('/')}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "User-Agent": "Antigravity-Blotato-Repurposer/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {e.reason}", "details": err_msg}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python blotato_client.py <endpoint> [json_payload_file]")
        sys.exit(1)
    ep = sys.argv[1]
    pl = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else {}
    res = call_blotato(ep, pl)
    print(json.dumps(res, indent=2, ensure_ascii=False))