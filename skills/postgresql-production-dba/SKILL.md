---
name: postgresql-production-dba
description: >-
  Design, optimize, and manage production PostgreSQL databases. Covers 3NF relational modeling, B-Tree/GIN/GiST index tuning, EXPLAIN (ANALYZE, BUFFERS) query optimization, zero-downtime schema migrations (CREATE INDEX CONCURRENTLY, lock timeouts), connection pooling (PgBouncer), and modern ORMs/query builders (Drizzle, Prisma, SQLAlchemy).
---

# 🐘 PostgreSQL Production DBA & Relational Architecture

> **Standard :** PostgreSQL 16+ Production Reliability & Zero-Downtime Operations  
> **Core Axiom :** *"A slow database is almost never a hardware problem—it is a missing index, an unindexed foreign key lock, or an unpooled connection flood. Design schema rigorously in 3NF and migrate with zero downtime."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Une base de données de production comme PostgreSQL, c'est comme la **bibliothèque centrale d'une métropole** :
- **Sans indexation (B-Tree)** : Si un lecteur cherche un livre par son auteur et que la bibliothèque n'a aucun fichier alphabétique, le bibliothécaire doit fouiller tous les rayons un par un (c'est le `Seq Scan`). Pour 10 millions de livres, cela prend des minutes et bloque tout le monde.
- **Avec un index B-Tree bien placé** : Le bibliothécaire consulte le catalogue et va directement au bon rayon en 2 millisecondes (c'est l'`Index Scan`).
- **Les Migrations Zéro-Downtime** : En plein milieu de la journée avec des millions d'utilisateurs connectés, tu ne peux pas fermer la bibliothèque pour ajouter une étagère (`ALTER TABLE`). Tu dois ajouter tes colonnes et tes index en arrière-plan sans jamais bloquer les lectures ni les écritures.
- **Le Connection Pooling (PgBouncer)** : Si 5 000 personnes arrivent à la porte en même temps, PostgreSQL s'écroule s'il doit créer 5 000 processus lourds. PgBouncer agit comme un portier intelligent qui réutilise 50 connexions ultra-rapides pour servir les 5 000 clients à tour de rôle.

---

## 🏛️ 2. Règles d'Or de l'Architecture PostgreSQL

### 1. Indexation Stratégique
- **Clés Étrangères (`FOREIGN KEY`)** : Toujours indexer explicitement les colonnes de clés étrangères pour éviter les verrous de table entière lors des `DELETE` ou `UPDATE` en cascade :
  ```sql
  CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);
  ```
- **Index Partiels** : Indexer uniquement les lignes pertinentes pour diviser la taille de l'index par 10 :
  ```sql
  -- Indexe uniquement les tâches non traitées
  CREATE INDEX CONCURRENTLY idx_tasks_pending ON tasks(created_at) WHERE status = 'pending';
  ```
- **Index GIN pour JSONB et Texte** :
  ```sql
  CREATE INDEX CONCURRENTLY idx_users_metadata_gin ON users USING GIN (metadata);
  ```
- **SARGability & Index Fonctionnels** : Ne JAMAIS envelopper une colonne indexée dans une fonction dans la clause `WHERE` (`WHERE LOWER(email) = ...` ou `WHERE DATE(created_at) = ...`), car cela annule l'index B-Tree et force un `Seq Scan`. Toujours écrire des requêtes SARGables (`WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`), ou créer un index fonctionnel explicite :
  ```sql
  CREATE INDEX CONCURRENTLY idx_users_lower_email ON users (LOWER(email));
  ```

### 2. Le Protocole de Migration Zéro-Downtime
Ne JAMAIS exécuter un simple `CREATE INDEX` ou un `ALTER TABLE ADD COLUMN NOT NULL` sans valeur par défaut en production :
1. **Toujours définir un `lock_timeout` court** (ex: 2 secondes) pour ne pas former de file d'attente bloquant toutes les requêtes :
   ```sql
   SET lock_timeout = '2s';
   ```
2. **Créer les index de façon concurrente** :
   ```sql
   CREATE INDEX CONCURRENTLY idx_items_sku ON items(sku);
   ```
3. **Ajout de colonne avec valeur par défaut** : En PostgreSQL 11+, `ADD COLUMN ... DEFAULT ...` est instantané (temps constant $\mathcal{O}(1)$), car il ne réécrit pas la table.

---

## 🔍 3. Analyse & Optimisation de Requêtes (`EXPLAIN ANALYZE`)

Lorsqu'une requête est lente, toujours exécuter :
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, o.total_amount, c.email
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'completed' AND o.created_at >= '2026-01-01';
```

### Grille d'Interprétation des Coûts :
- `Seq Scan` sur une table volumineuse ($\ge 10\,000$ lignes) $\rightarrow$ **Alerte : index manquant**.
- `Buffers: shared hit=... read=...` : Si `read` (lecture disque) est très supérieur à `hit` (cache RAM), la mémoire tampon (`shared_buffers`) est insuffisante ou la requête balaie trop de pages.
- `Sort Method: external merge Disk` $\rightarrow$ La mémoire `work_mem` est trop faible pour le tri, forçant un passage sur disque. Augmenter `work_mem` pour la session.

---

## ⚙️ 4. Configuration Recommandée de Production

Pour un serveur moyen (8 Go RAM, 4 vCPU) :
```ini
# postgresql.conf
max_connections = 100               # Maintenu bas, délégué à PgBouncer
shared_buffers = 2GB                # 25% de la RAM totale
effective_cache_size = 6GB          # 75% de la RAM totale
maintenance_work_mem = 512MB
checkpoint_completion_target = 0.9  # Lissage des écritures disque
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1              # Optimisé pour disques SSD NVMe
work_mem = 32MB                     # Alloué par nœud de tri
```

---

## 🛠️ 5. Linter de Migration Zéro-Downtime Déterministe

Un script Python autonome est fourni pour vérifier automatiquement la sécurité de vos fichiers SQL de migration avant exécution :
```bash
python scripts/check_migration_safety.py path/to/migration.sql
```
Vérifications effectuées : absence de `CONCURRENTLY`, colonnes `NOT NULL` sans valeur par défaut, absence de `lock_timeout`, requêtes non-SARGables (`LOWER()`) et `DROP` destructifs.
