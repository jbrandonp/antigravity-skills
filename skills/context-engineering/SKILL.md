---
name: context-engineering
description: >-
  Optimize agent token budgets, context quality, prevent context rot, and architect LLM prompt caching strategies for Anthropic Claude, Google Gemini, and OpenAI. Prunes redundant files, generates high-density scratchpad summaries, enforces selective reading, deterministic tool schema ordering, static cache prefix structuring, cache hit telemetry, and 80%+ API cost reductions.
---

# Context Engineering

Authored by **Addy Osmani** and synthesized with **Anthropic agent engineering standards**, *Context Engineering* governs how an AI coding assistant budgets, compresses, and structures its context window to prevent "context rot" (degradation of model reasoning over long sessions).

---

## 🧠 The 4 Pillars of Context Engineering

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Token Budget Allocation (Target < 60% saturation)        │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Grep-First Discovery (Never read whole files blindly)    │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Context Distillation (Compress logs into executive state)│
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Active Pruning (Exclude node_modules, .git, venv)        │
 └─────────────────────────────────────────────────────────────┘
```

### Pillar 1: The Context Budget Rule
- Keep active working context lean:
  - 10% System prompt & core instructions
  - 15% Architectural specs & active PRD
  - 25% Active files under modification
  - 50% Reserve for multi-turn thinking, tool outputs, and diffs

### Pillar 2: Selective Reading over Ingestion
- **Forbidden**: Loading an entire 2,000-line file to check a single function signature.
- **Required**:
  1. `Select-String` / `grep` to locate the target line range.
  2. View only the relevant slice (e.g. lines 40 to 90).
  3. Extract AST outlines or docstrings.

### Pillar 3: Distillation & Scratchpads
- Every 10 iterations or upon completing a milestone, produce a structured Markdown summary artifact.
- The summary replaces raw conversation transcripts and tool dumps, freeing cognitive bandwidth.

### Pillar 4: Token Waste Elimination
- Run `python scripts/profile_context_budget.py` to identify context bloaters (oversized test fixtures, verbose logs, minified bundles, vendored libraries).

---

## 🛠️ Deterministic Tooling

```bash
# Profile directory token consumption
python scripts/profile_context_budget.py --dir .

# Inspect top 10 heaviest files
python scripts/profile_context_budget.py --dir src/ --top 10
```

---

## ⚡ Module Complémentaire : Stratégies d'Optimisation de Cache de Prompts & Économie de Jetons (-80% Coûts)

# 🤖 OLYMPUS PRO : PROMPT CACHING & TOKEN ECONOMY ARCHITECT

> **Standard :** OLYMPUS System v6.0 / Prompt Caching SOTA 2026 (Anthropic & Gemini Standard)  
> **Rôle :** Architecte d'optimisation économique et de latence pour agents IA, concevant des prompts ordonnancés pour maximiser le taux de succès du cache mémoire (Prompt Caching), divisant les coûts d'API par 5 à 10 et réduisant la latence de 80%.

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, auditer ou optimiser des prompts d'agents IA à long contexte (ex: `FoundryOS`, `Kit_Vibe_Coder`), structurer des préfixes de cache statiques (`cache_control`), éliminer les invalidations de cache imprévues, ou analyser le taux de cache hits/misses.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Structuration Hiérarchique en Préfixe Statique
- Organiser les requêtes LLM selon la règle d'or de stabilité temporelle (du plus statique au plus dynamique) :
  $$\text{Ordre : } \underbrace{\text{Instructions Système & Règles Globales}}_{\text{100\% Statique (Point de rupture cache)}} \longrightarrow \underbrace{\text{Schémas d'Outils & MCP}}_{\text{Statique}} \longrightarrow \underbrace{\text{Contexte Projet / RAG}}_{\text{Semi-statique}} \longrightarrow \underbrace{\text{Historique & Requête Utilisateur}}_{\text{Dynamique}}$$
- Interdire formellement l'insertion de variables dynamiques (ex: horodatage courant, compteur de tours) en tête de prompt : toute variation au début invalide l'intégralité du cache aval.

### Phase 2: Ordonnancement Déterministe des Outils & Schémas
- Garantir que la liste des définitions d'outils (tools) et leurs schémas JSON Schema sont triés par ordre alphabétique strict.
- Un dictionnaire Python non ordonné modifiant l'ordre des clés JSON provoque une invalidation immédiate du cache tokenisateur.

### Phase 3: Gestion des Points de Rupture de Cache (`cache_control`)
- Positionner les balises `cache_control: { type: "ephemeral" }` (Anthropic) ou context caching TTL (Gemini) au seuil de fin des instructions système et à la fin de la base documentaire partagée.
- Maintenir une taille de préfixe supérieure au seuil minimal de déclenchement du fournisseur (ex: $\ge 1024$ tokens pour Claude 3.5 / 3.7 Sonnet).

### Phase 4: Mesure Télémétrique & Ratios d'Économie
- Calculer le ratio d'efficacité du cache :
  $$\text{Économie (\$)} = \left(1 - \frac{C_{\text{hit}}}{C_{\text{write}}}\right) \times \text{Tokens Cachés}$$
- Viser un taux de cache hit $\ge 85\%$ sur les sessions multi-tours d'agents.
- Explication claire du fonctionnement du cache mémoire pour un utilisateur de 15 ans.

---

## 🏛️ Règles d'Or OLYMPUS & Architecture Propre
1. **Typage Fort et Zéro Any :** Aucun type `any`, `unknown` ou non typé n'est accepté. Le code doit être rigoureusement défini.
2. **Nommage Explicite :** Bannir les variables à une lettre (`x`, `temp`, `data`). Le nom d'une variable ou fonction doit expliciter sa finalité.
3. **Complexité Cyclomatique :** Viser $M \le 15$. Si un algorithme dépasse ce seuil, il doit être décomposé en sous-fonctions.
4. **Commentaires en Français :** Chaque fonction non-triviale doit comporter une docstring expliquant son rôle, ses paramètres et son retour.
5. **Code & Commits en Anglais :** Le code source et les messages de commits (`type(scope): description`) sont rédigés en anglais.
6. **Autonomie & Détective Mode :** Jusqu'à 8 itérations autonomes pour résoudre tout bug ou échec de test avant de solliciter l'aide de l'utilisateur.
7. **Explication Pédagogique (15 ans) :** Toute explication technique fournie à Brandon doit être claire et intuitive, accessible à un esprit de 15 ans.

---

## 📊 Critères de Validation Obligatoires (Gate Score S $\ge 65\%$)
- **Stabilité Préfixe :** 100% du bloc système invariant sur la session.
- **Taux de Cache Hit :** $\ge 85\%$ après le premier tour d'initialisation.
- **Lint / Types :** 0 erreur mypy/pylint/clippy.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).
