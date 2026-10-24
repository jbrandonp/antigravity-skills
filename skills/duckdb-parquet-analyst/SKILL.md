---
name: duckdb-parquet-analyst
description: >-
  Perform high-performance columnar analytics, query Parquet datasets, and benchmark data pipelines using DuckDB, while enforcing dataset quality based on Andrew Ng Data-Centric AI standards (detecting duplicate records, missing fields, distribution skew, corrupted types, and statistical anomalies in scraped supermarket datasets).
---

# DuckDB Parquet Analyst (Columnar Analytics Standard)

High-performance in-process analytics engine inspired by modern data engineering best practices. Enables instantaneous SQL querying and aggregations across SQLite, Parquet, and CSV datasets without memory bloat.

---

## 🦆 The 4 Columnar Capabilities

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Zero-Copy Querying (Directly query SQLite & Parquet)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Statistical Outlier & Anomaly Detection (IQR, Quantiles) │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Fast Columnar Storage (Parquet with Snappy compression)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Window Functions & Cross-Brand Price Comparisons         │
 └─────────────────────────────────────────────────────────────┘
```

### Capability 1: Multi-Format Queries
- Query SQLite tables directly without dumping:
  ```sql
  INSTALL sqlite; LOAD sqlite;
  SELECT * FROM sqlite_scan('supermarkets.sqlite', 'products');
  ```
- Seamlessly export millions of rows into compressed Parquet in seconds.

### Capability 2: Statistical Anomaly Detection
- Compute 25th, 50th (median), and 75th percentiles to calculate Interquartile Range ($IQR = Q_3 - Q_1$).
- Flag pricing errors ($P < Q_1 - 1.5 \times IQR$ or $P > Q_3 + 1.5 \times IQR$) from scraper glitches.

### Capability 3: Window Functions
- Track brand price differences:
  ```sql
  SELECT article, brand, price,
         RANK() OVER (PARTITION BY article ORDER BY price ASC) as price_rank
  FROM products;
  ```

---

## 🛠️ Tooling 1 : Analyse Statistique Parquet DuckDB

```bash
# Run statistical outlier check on sample pricing dataset
python scripts/analyze_parquet_data.py --demo

# Run analytics report on an existing SQLite/Parquet file
python scripts/analyze_parquet_data.py --source prices.sqlite --table products
```

---

## 🛡️ Module Complémentaire : Sentinelle Qualité de Données (Standards Data-Centric AI)

# Data Quality Sentinel (Andrew Ng Data-Centric AI Standard)

Dataset auditing and sanitization methodology championed by **Andrew Ng** (*Data-Centric AI movement*).

Core Philosophy: **"Instead of endlessly tweaking hyperparameters or blaming model hallucinations, systematically elevate the quality, completeness, and consistency of your data."**

---

## 🔍 The 4 Data Quality Tests

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Completeness Audit (Null values & missing attributes)    │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Uniqueness & Deduplication Check (Exact & Fuzzy dupes)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Type Purity & Format Validity (Strings in float columns) │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Value Distribution & Boundary Verification               │
 └─────────────────────────────────────────────────────────────┘
```

### Test 1: Completeness ($C$)
- Measure null or empty string rates across required columns:
  $$C = \left(1 - \frac{N_{\text{null}}}{N_{\text{total}}}\right) \times 100$$
- Reject datasets with critical columns (e.g., price, product name) falling below 99% completeness.

### Test 2: Uniqueness ($U$)
- Detect accidental duplicate scraping caused by pagination loops or retry glitches.

### Test 3: Type Purity
- Ensure price columns contain strictly positive numbers (`price > 0.0`), without text contamination like `"N/A"`, `"Gratuit"`, or negative amounts.

---

## 🛠️ Tooling 2 : Audit Qualité Data-Centric AI (Andrew Ng)

```bash
# Audit an SQLite database table for data-centric quality metrics
python scripts/audit_dataset_quality.py --db supermarkets.sqlite --table products

# Run self-test on simulated pricing dataset
python scripts/audit_dataset_quality.py --demo
```
