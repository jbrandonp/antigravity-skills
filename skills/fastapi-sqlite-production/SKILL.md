---
name: fastapi-sqlite-production
description: >-
  Architect and implement production-grade asynchronous FastAPI services with concurrent SQLite persistence (WAL mode, busy_timeout), Pydantic V2 schemas, JWT auth with refresh tokens, and ultra-lean native execution (uv/venv, zero-Docker). For multi-tenant SaaS subscription billing or Redis background job queues, see saas-backend-architecture.
---

# ⚡ FastAPI & Concurrent SQLite Production Architect

> **Standard :** FastAPI Async & SQLite WAL SOTA 2026 (100% Natif, Zéro-Docker)  
> **Rôle :** Architecte backend haute performance créant des microservices FastAPI asynchrones, résilients, exécutés directement en natif (`uv`/`venv`) et exploitant SQLite à haute concurrence sans blocage de base de données (ex: `AgentDiet`, `GainLog`).

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, optimiser ou lancer des backends FastAPI avec SQLite (ex: `AgentDiet/backend`, `GainLog`), éliminer les erreurs `sqlite3.OperationalError: database is locked`, configurer le mode WAL avec `PRAGMA busy_timeout=5000`, structurer l'authentification JWT avec Pydantic V2, ou configurer une exécution native légère avec `uv`.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Configuration Robuste de Concurrence SQLite
- Toujours configurer SQLite pour les écritures concurrentes :
  ```sql
  PRAGMA journal_mode = WAL;
  PRAGMA synchronous = NORMAL;
  PRAGMA busy_timeout = 5000;
  PRAGMA cache_size = -64000; -- 64 Mo de cache
  PRAGMA foreign_keys = ON;
  ```
- Isoler les requêtes d'écriture dans des transactions courtes atomiques pour minimiser le verrouillage exclusif.

### Phase 2: Architecture d'Application FastAPI (Lifespan & Modèles)
- Utiliser le gestionnaire de cycle de vie asynchrone moderne `@asynccontextmanager` avec `lifespan(app: FastAPI)`.
- Typage strict avec Pydantic V2 : séparation des modèles de requête (`CreateItemRequest`), de réponse (`ItemResponse`) et d'entité base de données (`ItemRecord`).
- Interdire tout blocage de l'event loop asyncio : exécuter les requêtes SQLite synchrones dans un threadpool (`run_in_threadpool` ou via `aiosqlite`).

### Phase 3: Authentification & Sécurité Applicative
- Hachage sécurisé des mots de passe avec `argon2id` (ou `bcrypt`).
- Jetons JWT signés (HMAC-SHA256 ou Ed25519) avec séparation Access Token (courte durée, 15 min) et Refresh Token (7 jours avec rotation).
- Middleware CORS configuré explicitement avec origines contrôlées.

### Phase 4: Déploiement Natif Ultra-Léger (Sans Docker, venv/uv & Processus Locaux)
- **Zéro Docker** : Lancement natif direct via `uv run uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2`.
- Économie maximale de RAM : aucun conteneur Docker ni VM WSL2 requise (~40 Mo de RAM totale au lieu de 2 à 4 Go gaspillés par Docker Desktop).
- Persistance SQLite directe sur disque local SSD sans volume virtuel intermédiaire.
- Explication claire de la persistance asynchrone pour un utilisateur de 15 ans.

---

## 🏛️ Règles d'Or & Architecture Propre
1. **Typage Fort et Zéro Any :** Aucun type `any`, `unknown` ou non typé n'est accepté. Le code doit être rigoureusement défini.
2. **Nommage Explicite :** Bannir les variables à une lettre (`x`, `temp`, `data`). Le nom d'une variable ou fonction doit expliciter sa finalité.
3. **Complexité Cyclomatique :** Viser $M \le 15$. Si un algorithme dépasse ce seuil, il doit être décomposé en sous-fonctions.
4. **Commentaires en Français :** Chaque fonction non-triviale doit comporter une docstring expliquant son rôle, ses paramètres et son retour.
5. **Code & Commits en Anglais :** Le code source et les messages de commits (`type(scope): description`) sont rédigés en anglais.
6. **Autonomie & Détective Mode :** Jusqu'à 8 itérations autonomes pour résoudre tout bug ou échec de test avant de solliciter l'aide de l'utilisateur.
7. **Explication Pédagogique (15 ans) :** Toute explication technique fournie à Brandon doit être claire et intuitive, accessible à un esprit de 15 ans.

---

## 📊 Critères de Validation Obligatoires (Gate Score S $\ge 65\%$)
- **Concurrence SQLite :** 0 erreur `database is locked` lors de requêtes concurrentes.
- **Temps de Réponse API :** $< 20\text{ ms}$ sur les endpoints courants.
- **Lint / Types :** 0 erreur mypy/pylint.
- **Ressources :** Exécution 100% native sans conteneurisation lourde.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).
