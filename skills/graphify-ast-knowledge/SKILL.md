---
name: graphify-ast-knowledge
description: >-
  Deterministic Tree-Sitter and AST codebase knowledge graph builder. Maps symbols, dependencies, API routes, SQL schemas, and markdown docs into a queryable graph.json and interactive graph.html, reducing codebase exploration token consumption by 80%.
version: 1.0.0
tags:
  - graphify
  - ast-parsing
  - knowledge-graph
  - code-exploration
  - token-economy
---

# 🕸️ Graphify AST: Deterministic Codebase Knowledge Graph

> **Inspiration :** `Graphify-Labs/graphify`  
> **Axiome Central :** Les recherches textuelles `grep` sont aveugles aux relations fonctionnelles. Construire un graphe AST déterministe en local permet à l'agent de traverser instantanément les dépendances réelles sans gaspiller des dizaines de milliers de tokens en lectures répétées.

---

## 🎯 Avantages Clés
1. **100% Local & Déterministe :** S'exécute directement sur l'AST Python sans aucun appel de modèle LLM ni base vectorielle externe.
2. **Double Export :**
   - `graph.json` : Structure normalisée des nœuds (fichiers, classes, fonctions, tables) et des arêtes (contient, importe, appelle).
   - `graph.html` : Interface visuelle moderne, autonome (zéro CDN, zéro dépendance JS externe) explorable dans tout navigateur.
3. **Réduction Drastique de Tokens :** L'agent interroge le graphe avec `--query` pour savoir immédiatement qui appelle une méthode ou quel fichier importe un module.

---

## 💻 Commandes d'Utilisation

### 1. Construire le graphe de la base de code
```bash
python skills/graphify-ast-knowledge/scripts/graph_builder.py --root . --json graph.json --html graph.html
```

### 2. Interroger directement un symbole depuis le terminal
```bash
python skills/graphify-ast-knowledge/scripts/graph_builder.py --query "parse_product"
python skills/graphify-ast-knowledge/scripts/graph_builder.py --query "SQLiteManager"
```

### 3. Explorer visuellement
Ouvrir le fichier `graph.html` généré dans un navigateur pour naviguer dans l'arborescence des appels et des dépendances.
