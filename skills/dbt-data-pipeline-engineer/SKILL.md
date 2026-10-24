---
name: dbt-data-pipeline-engineer
description: >-
  Design, orchestrate, and test scalable data transformation pipelines using dbt (data build tool), modern orchestrators (Dagster, Prefect, Airflow), and cloud data warehouses (BigQuery, Snowflake). Covers staging/intermediate/marts modeling, lineage graphs, incremental models, and automated data quality tests.
---

# 🔄 dbt Data Pipeline Engineering & Modern Data Stack

> **Standard :** Analytics Engineering SOTA 2026 (dbt Core + Dagster/Prefect + Cloud DW)  
> **Core Axiom :** *"Raw data is never queried directly by business applications. Transform raw tables through structured layers (staging -> intermediate -> marts) with deterministic lineage, version control, and automated schema tests."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Faire de la Data Engineering moderne, c'est comme **cuisiner dans un restaurant étoilé** :
1. **La Couche Staging (Les Ingrédients Bruts au Marché)** : Les données arrivent en vrac depuis Stripe, les bases de production et les scrapers. La couche Staging nettoie juste les noms des colonnes, convertit les dates et supprime les doublons évidents. Elle ne fait aucun calcul complexe.
2. **La Couche Intermediate (La Préparation des Ingrédients)** : On épluche les légumes, on prépare les sauces (on joint les tables clients et commandes, on calcule les paniers moyens).
3. **La Couche Marts (Le Plat Fini et Présenté au Client)** : Ce sont les tables finales, ultra-propres et faciles à comprendre (ex: `fct_daily_revenue`, `dim_customers`), directement prêtes pour les tableaux de bord PowerBI / Metabase ou les modèles de Machine Learning.
4. **dbt (La Recette de Cuisine Reproductible)** : Au lieu d'écrire des scripts Python de 2 000 lignes avec des requêtes SQL emmêlées, tu écris de simples fichiers `SELECT` en SQL. dbt gère automatiquement les dépendances, crée les tables dans Snowflake ou BigQuery et lance des tests pour vérifier que les chiffres ne sont jamais négatifs ou vides.

---

## 🏛️ 2. Architecture des Dossiers dbt

```text
models/
├── staging/                # Nettoyage 1:1 des sources brutes (vues)
│   └── stripe/
│       ├── src_stripe.yml
│       ├── stg_stripe__charges.sql
│       └── stg_stripe__customers.sql
├── intermediate/           # Jointures et logique métier intermédiaire
│   └── finance/
│       └── int_payments_unioned.sql
└── marts/                  # Tables analytiques finales (dimension & fact)
    ├── core/
    │   ├── dim_customers.sql
    │   └── fct_orders.sql
    └── finance/
        └── fct_monthly_mrr.sql
```

---

## 💻 3. Modèles Types & Conventions SQL

### Exemple de Modèle Staging (`stg_stripe__charges.sql`)
```sql
with source as (
    select * from {{ source('stripe', 'charges') }}
),

renamed as (
    select
        id as charge_id,
        customer as customer_id,
        amount / 100.0 as amount_usd,
        status,
        created as created_at,
        paid as is_paid
    from source
)

select * from renamed
```

### Modèle Incrémental pour Données Massives (`fct_events.sql`)
Pour traiter des millions d'événements sans recalculer l'historique complet chaque nuit :
```sql
{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='fail'
    )
}}

with new_events as (
    select * from {{ ref('stg_app__events') }}
    {% if is_incremental() %}
        where event_timestamp >= (select max(event_timestamp) from {{ this }}) - interval '3 hours'
    {% endif %}
)

select * from new_events
```

---

## 🧪 4. Tests Automatiques de Qualité des Données

Définis dans les fichiers YAML dbt pour bloquer les données corrompues :
```yaml
version: 2

models:
  - name: fct_orders
    description: "Table de faits des commandes confirmées"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'refunded']
      - name: total_amount
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
```

---

## ⚡ Commandes Fréquentes dbt CLI

```bash
# Compiler et exécuter tous les modèles
dbt run

# Exécuter uniquement un modèle et tous ses descendants
dbt run --select dim_customers+

# Lancer la batterie de tests d'intégrité
dbt test

# Générer et visualiser la documentation et le graphe de lignage (Lineage DAG)
dbt docs generate
dbt docs serve
```
