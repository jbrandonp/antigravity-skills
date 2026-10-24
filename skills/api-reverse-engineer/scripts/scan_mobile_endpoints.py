# -*- coding: utf-8 -*-
"""
scan_mobile_endpoints.py - Mobile API Extractor (JADX / Android Source)
Scanne les classes Java/Kotlin decompilees pour detecter les endpoints Retrofit et URLs d API.
"""

import re
import os
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class MobileEndpoint(TypedDict):
    file_name: str
    line_num: int
    http_method: str
    endpoint_path: str
    signature: str

RETROFIT_REGEX = re.compile(r"""@(GET|POST|PUT|DELETE|PATCH)\s*\(\s*["']([^"'\)]+)["']\s*\)""", re.IGNORECASE)
BASE_URL_REGEX = re.compile(r"""["'](https?://[a-zA-Z0-9_\-\.]+(?:/api|/v[0-9]|/graphql)[^"'\s]*)["']""", re.IGNORECASE)

def scan_file_for_endpoints(file_path: pathlib.Path) -> List[MobileEndpoint]:
    results: List[MobileEndpoint] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return results

    lines = content.splitlines()
    for idx, line in enumerate(lines, start=1):
        match = RETROFIT_REGEX.search(line)
        if match:
            method, path = match.groups()
            results.append({
                "file_name": file_path.name,
                "line_num": idx,
                "http_method": method.upper(),
                "endpoint_path": path,
                "signature": line.strip(),
            })

    return results

def create_demo_mobile_source(out_dir: pathlib.Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    sample_kt = """package be.delhaize.mobile.api

import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface SupermarketApiService {
    @GET("v1/products/search")
    fun searchProducts(@Query("q") query: String): Call<ProductListResponse>

    @GET("v2/stores/{storeId}/promotions")
    fun getStorePromotions(@Path("storeId") storeId: String): Call<PromotionsResponse>

    @POST("v1/cart/estimate")
    fun estimateCart(): Call<CartEstimateResponse>
}
"""
    (out_dir / "SupermarketApiService.kt").write_text(sample_kt, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Mobile API Extractor - Scanner d endpoints Android/JADX")
    parser.add_argument("--source-dir", type=str, help="Dossier des sources decompilees a analyser")
    parser.add_argument("--demo", action="store_true", help="Creer et analyser une source mobile de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      MOBILE API EXTRACTOR (EXTRACTION JADX / RETROFIT)        ")
    print("=" * 65)

    target_dir = pathlib.Path(args.source_dir) if args.source_dir else pathlib.Path("demo_mobile_src")
    is_demo = False
    if args.demo or not args.source_dir:
        create_demo_mobile_source(target_dir)
        is_demo = True

    all_endpoints: List[MobileEndpoint] = []
    for cur, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith((".java", ".kt", ".xml")):
                all_endpoints.extend(scan_file_for_endpoints(pathlib.Path(cur) / f))

    print(f"Dossier inspecte : {target_dir.resolve()}")
    print(f"Endpoints Retrofit detectes : {len(all_endpoints)}")
    print("-" * 65)

    for ep in all_endpoints:
        print(f"{ep['http_method']:<6} {ep['endpoint_path']:<35} ({ep['file_name']}:{ep['line_num']})")

    print("=" * 65)
    print("[OK] Extraction des routes mobiles terminee avec succes.")

    if is_demo and target_dir.exists():
        try:
            for f in target_dir.iterdir():
                f.unlink()
            target_dir.rmdir()
        except Exception:
            pass

if __name__ == "__main__":
    main()
