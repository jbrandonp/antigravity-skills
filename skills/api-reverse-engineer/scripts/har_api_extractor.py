import os
# -*- coding: utf-8 -*-
"""
har_api_extractor.py - API Reverse Engineer & HAR Parser
Extrait les requetes JSON/GraphQL pertinentes depuis une archive HAR.
"""

import json
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class ExtractedEndpoint(TypedDict):
    method: str
    url: str
    status: int
    content_type: str
    query_params: List[str]
    has_auth: bool

def parse_har_file(har_path: pathlib.Path) -> List[ExtractedEndpoint]:
    endpoints: List[ExtractedEndpoint] = []
    try:
        data = json.loads(har_path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as e:
        print(f"[X] Erreur lecture HAR : {e}")
        return endpoints

    entries = data.get("log", {}).get("entries", [])
    ignored_exts = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".css", ".js", ".woff", ".woff2", ".ico"}

    for entry in entries:
        req = entry.get("request", {})
        resp = entry.get("response", {})
        url = req.get("url", "")
        method = req.get("method", "GET")
        status = resp.get("status", 0)

        # Filtrer les ressources statiques
        if any(url.lower().endswith(ext) for ext in ignored_exts):
            continue

        headers = {h.get("name", "").lower(): h.get("value", "") for h in req.get("headers", [])}
        resp_mime = resp.get("content", {}).get("mimeType", "")

        is_json = "json" in resp_mime.lower() or "graphql" in url.lower() or "api" in url.lower()
        if not is_json:
            continue

        q_params = [q.get("name", "") for q in req.get("queryString", [])]
        has_auth = "authorization" in headers or "x-api-key" in headers

        endpoints.append({
            "method": method,
            "url": url,
            "status": status,
            "content_type": resp_mime,
            "query_params": q_params,
            "has_auth": has_auth,
        })

    return endpoints

def create_demo_har(har_path: str) -> None:
    demo_data = {
        "log": {
            "entries": [
                {
                    "request": {
                        "method": "GET",
                        "url": "https://api.delhaize.be/v1/supermarket/products/search?query=lait&limit=20",
                        "headers": [{"name": "Authorization", "value": "Bearer demo_token_xyz"}],
                        "queryString": [{"name": "query", "value": "lait"}, {"name": "limit", "value": "20"}],
                    },
                    "response": {"status": 200, "content": {"mimeType": "application/json"}},
                },
                {
                    "request": {
                        "method": "POST",
                        "url": "https://api.colruyt.be/graphql",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "queryString": [],
                    },
                    "response": {"status": 200, "content": {"mimeType": "application/json"}},
                },
                {
                    "request": {
                        "method": "GET",
                        "url": "https://www.delhaize.be/assets/logo.png",
                        "headers": [],
                        "queryString": [],
                    },
                    "response": {"status": 200, "content": {"mimeType": "image/png"}},
                },
            ]
        }
    }
    with open(har_path, "w", encoding="utf-8") as f:
        json.dump(demo_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="HAR API Extractor - Reverse Engineering d APIs")
    parser.add_argument("--har", type=str, help="Fichier .har a analyser")
    parser.add_argument("--demo", action="store_true", help="Generer et analyser une capture de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      API REVERSE ENGINEER (EXTRACTEUR D ARCHIVES HAR)      ")
    print("=" * 65)

    target_har = args.har
    if args.demo or not target_har:
        target_har = "demo_capture.har"
        create_demo_har(target_har)

    p = pathlib.Path(target_har)
    endpoints = parse_har_file(p)

    print(f"Archive analysee : {p.resolve()}")
    print(f"APIs JSON/GraphQL identifiees : {len(endpoints)}")
    print("-" * 65)

    for ep in endpoints:
        auth_tag = "[AUTH]" if ep["has_auth"] else "[PUBLIC]"
        print(f"{ep['method']:<6} {ep['status']:<4} {auth_tag:<8} {ep['url']}")
        if ep["query_params"]:
            print(f"       Parametres: {', '.join(ep['query_params'])}")

    print("=" * 65)
    if args.demo and os.path.exists(target_har):
        try:
            os.remove(target_har)
        except Exception:
            pass

if __name__ == "__main__":
    main()