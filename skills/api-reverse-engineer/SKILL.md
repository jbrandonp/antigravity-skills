---
name: api-reverse-engineer
description: >-
  Reverse-engineer private mobile and web APIs by analyzing HTTP Archive (.har) files, network captures, or decompiled Android application source trees (APKs/JADX). Extracts endpoints, headers, authentication tokens, GraphQL operations, Retrofit interfaces, and generates executable Python curl_cffi / httpx snippets (JA4 TLS fingerprinting & HTTP/2).
---

# API Reverse Engineer (Network Capture & HAR Standard)

Specialized methodology for reverse-engineering modern single-page applications (SPAs) and mobile apps (e.g., supermarket product catalogs, dynamic pricing, inventory check APIs) via HTTP Archive (`.har`) files.

---

## 🔍 The 4-Step Reverse Engineering Pipeline

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Ingest & Filter HAR (Strip images, fonts, styles)        │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Identify High-Value JSON & GraphQL Endpoints             │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Isolate Dynamic State (Bearer tokens, Session cookies)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Synthesize Reproducible Python / curl_cffi Client        │
 └─────────────────────────────────────────────────────────────┘
```

### Step 1: HAR Ingestion & Filtering
- Browser network captures contain 80% noise (`.png`, `.svg`, `.css`, analytics trackers).
- Filter strictly for `content-type: application/json` or `application/graphql`.

### Step 2: Endpoint Classification
- Map URL structure: path variables vs query parameters.
- Detect pagination mechanisms (`page`, `offset`, `limit`, cursor tokens).
- Inspect request payload schemas for GraphQL queries and mutations.

### Step 3: Auth & Session Isolation
- Extract `Authorization: Bearer ...` or session cookies.
- Identify token refresh lifecycles to ensure long-running scrapers don't fail silently after 1 hour.

### Step 4: Python Client Generation
- Generate clean, strictly-typed Python code using `curl_cffi` (with `impersonate='chrome131'` for JA4 TLS fingerprinting) or `httpx` (HTTP/2), banning deprecated plain `requests` to prevent WAF bot-detection.

---

## 🛠️ Tooling 1 : Extracteur d'APIs Réseau (HAR)

```bash
# Analyze a HAR file and extract private API endpoints
python scripts/har_api_extractor.py --har network_capture.har

# Run demonstration on synthetic HAR capture
python scripts/har_api_extractor.py --demo
```

---

## 📱 Module Complémentaire : Extraction Mobile APK & JADX

# Mobile API Extractor (Android APK & JADX Reverse Engineering)

Methodology for discovering and extracting private REST, GraphQL, and WebSocket endpoints directly from decompiled Android applications (e.g. Delhaize, Colruyt, and smart retail apps) using JADX / APKTool outputs.

---

## 📱 The 4 Extraction Vectors

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Retrofit & Ktor Interface Parsing (@GET, @POST, @Headers) │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Base URL & API Host Discovery in BuildConfig / Strings   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. OkHttp Interceptors & Header Signatures (HMAC, Tokens)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Network Security Config (Certificate Pinning bypasses)   │
 └─────────────────────────────────────────────────────────────┘
```

### Vector 1: Retrofit Interfaces
- Scans decompiled Java/Kotlin classes for Retrofit declarations:
  ```kotlin
  @GET("api/v2/products/{id}/price")
  fun getProductPrice(@Path("id") id: String): Call<ProductResponse>
  ```

### Vector 2: Base URLs
- Extracts constants: `https://api.delhaize.be/mobile/`, `https://colruyt.be/gateway/`.

### Vector 3: Auth Interceptors
- Locates custom `Interceptor` classes adding dynamic signing headers (e.g. `X-Signature`, `X-Timestamp`, API keys).

---

## 🛠️ Tooling 2 : Scanner de Code Mobile JADX

```bash
# Scan a directory of decompiled Java/Kotlin sources for API endpoints
python scripts/scan_mobile_endpoints.py --source-dir jadx_out/

# Run demonstration on synthetic mobile source tree
python scripts/scan_mobile_endpoints.py --demo
```
