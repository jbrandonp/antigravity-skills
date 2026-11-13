---
name: context-mode
description: >-
  Terminal execution sandbox with local SQLite FTS5 full-text indexing. Captures verbose tool, test, and scraper outputs into an indexed local database and returns only concise summaries to the agent, eliminating 90-99% of context window pollution.
version: 1.0.0
tags:
  - context-optimization
  - token-economy
  - sqlite-fts5
  - terminal-sandbox
---

# 🧠 Context-Mode: SQLite FTS5 Terminal Output Reducer

> **Inspiration :** `mksglu/context-mode`  
> **Axiome Central :** Ne jamais laisser 5 000 lignes de logs bruts, de traces de tests ou de dumps de scrapers saturer la fenêtre de contexte de l'agent. Isoler la sortie dans une base SQLite FTS5 locale et requêter chirurgicalement avec BM25.

---

## 🎯 Pourquoi ce Skill ?

Les sorties de terminal volumineuses (`pytest -v`, `npm test`, `git log`, scrapers HTTP) font exploser le coût en tokens et provoquent le "context drift" (dérive cognitive de l'agent). En interceptant les commandes lourdes :
1. **L'agent ne reçoit que 3 à 5 lignes** : code de retour, nombre de lignes capturées, durée, et aperçu compact.
2. **La donnée brute reste accessible** sur disque (`~/.antigravity/context_buffer.db`).
3. **L'agent interroge par mots-clés** : `search` extrait les snippets exacts via l'algorithme BM25 de SQLite.

---

## 💻 Commandes d'Utilisation

### 1. Exécuter une commande lourde dans le bac à sable
```bash
python skills/context-mode/scripts/ctx_buffer.py run -- pytest tests/
python skills/context-mode/scripts/ctx_buffer.py run -- npm test
python skills/context-mode/scripts/ctx_buffer.py run -s scraper-run -- python scraper.py
```

### 2. Rechercher chirurgicalement dans les logs (FTS5 / BM25)
```bash
python skills/context-mode/scripts/ctx_buffer.py search "AssertionError"
python skills/context-mode/scripts/ctx_buffer.py search -s scraper-run "403 Forbidden"
```

### 3. Afficher les N dernières lignes d'une session
```bash
python skills/context-mode/scripts/ctx_buffer.py tail <session_id> -n 50
```

### 4. Vider le tampon de contexte
```bash
python skills/context-mode/scripts/ctx_buffer.py clear
```

---

## 🛡️ Règles Comportementales pour l'Agent
- Dès qu'une commande risque de générer plus de 50 lignes, passer systématiquement par `ctx_buffer.py run`.
- En cas d'échec (`exit code != 0`), inspecter d'abord les 10 lignes de tail fournies avant de lancer un `search` ciblé sur l'erreur.
- Ne jamais ré-exécuter une commande aveuglément sans avoir diagnostiqué la cause via FTS5.
