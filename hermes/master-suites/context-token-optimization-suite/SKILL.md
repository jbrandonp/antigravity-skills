---
name: context-token-optimization-suite
description: >-
  Unified Context Window & Token Optimization Suite: Architectural context engineering, Anthropic/Gemini prompt caching, terminal output reduction via SQLite FTS5 buffer (context-mode), and semantic prompt rule compression (caveman-compress). Eliminates 65-95% context pollution.
version: 2.0.0
tags:
  - token-economy
  - context-engineering
  - prompt-caching
  - prompt-compression
  - sqlite-fts5
  - terminal-sandbox
  - context-rot
merged_member_skills:
  - context-engineering
  - context-mode
  - caveman-compress
---

# Context & Token Optimization Suite

> **Unified Agent Memory & Token Economy Suite :** Eliminates cognitive degradation (context rot), slashes token expenditure by up to 90%, stabilizes prompt cache hit rates, captures massive tool outputs into an indexed local SQLite buffer, and compresses verbose rulebooks and prompt instructions without semantic loss.

---

## 🎯 When to Trigger this Master Suite

Activate this master suite whenever a task involves:
- **Context Budgeting & Cache Optimization** : Managing token quotas across long agentic sessions, configuring Anthropic or Gemini prompt caching breakpoints, avoiding cache churn.
- **Verbose Tool Output Interception** : Running test suites (`pytest`, `jest`), build outputs, or web scrapers that generate hundreds or thousands of output lines that would otherwise pollute the context window.
- **Prompt & Rulebook Compression** : Compressing instruction files (`CLAUDE.md`, `.cursorrules`, `SKILL.md`, `GEMINI.md`) into high-density tokens, or switching to telegraphic communication mode (`/caveman`).

---

## 📋 Module Summary & Navigation

1. **[Module 1: Context Engineering & Prompt Caching Architecture](#module-1-context-engineering--prompt-caching-architecture)**: Token budgeting, grep-first discovery, static prompt caching prefixes, and context rot prevention.
2. **[Module 2: Context-Mode SQLite FTS5 Buffer](#module-2-context-mode-sqlite-fts5-buffer)**: Intercepting verbose CLI outputs, local BM25 full-text indexing, and surgical retrieval.
3. **[Module 3: Caveman Concision & Prompt Compressor](#module-3-caveman-concision--prompt-compressor)**: Telegraphic machine-to-machine concision modes and automated markdown prompt compression.
4. **[Module 4: Companion Diagnostic & Optimization Tools](#module-4-companion-diagnostic--optimization-tools)**: CLI scripts in `scripts/`.

---

## Module 1: Context Engineering & Prompt Caching Architecture

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

---

## Module 2: Context-Mode SQLite FTS5 Buffer

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

---

## Module 3: Caveman Concision & Prompt Compressor

# 🪓 Caveman: Telegraphic Token Economy & Prompt Compressor

> **Inspiration :** `JuliusBrussee/caveman` (100k+ ⭐)  
> **Axiome Central :** Les politesses, flatteries et périphrases gaspillent la mémoire de l'agent. Communiquer en style télégraphique machine-to-machine réduit de 65% les tokens de sortie et de 46% les tokens de contexte système.

---

## 🎯 Les 3 Niveaux de Concision

### 1. Mode `/caveman lite`
- Supprime les salutations ("Bonjour", "Avec plaisir", "Certainement").
- Supprime les résumés redondants en début de réponse.
- Conserve les explications techniques normales en français direct.

### 2. Mode `/caveman full`
- Style télégraphique strict.
- Phrases courtes sans fioritures.
- Listes à puces denses au lieu de paragraphes narratifs.
- Diffs de code minimaux uniquement.

### 3. Mode `/caveman ultra` (Machine-to-Machine)
- Sortie purement technique : syntaxe, commandes shell, chemins de fichiers, diffs unifiés.
- Zéro phrase d'accompagnement.

---

## 🛠️ Outil d'Automatisation : `/caveman-compress`

Le script compagnon `compressor.py` nettoie automatiquement les fichiers de configuration système (`CLAUDE.md`, `.cursorrules`, `SKILL.md`, prompts système) pour diviser par deux leur coût d'ingestion permanent :

```bash
# Mesurer le gain potentiel sur un fichier d'instructions
python skills/caveman-compress/scripts/compressor.py CLAUDE.md --stats-only

# Compresser le fichier sur place
python skills/caveman-compress/scripts/compressor.py CLAUDE.md --in-place

# Mode agressif
python skills/caveman-compress/scripts/compressor.py rules.md -i --aggressive
```

---

## 📋 Directives Comportementales
- En mode révision de PR ou commit review, produire un compte rendu en une seule ligne : `type(scope): exact fix`.
- Bannir les transitions d'excuses ("Je m'excuse pour cette erreur, voici le correctif"). Diagnostiquer directement la cause et appliquer le patch.
---

## Module 4: Companion Diagnostic & Optimization Tools

The suite includes 4 standalone Python tools in `scripts/`:

1. `profile_context_budget.py` : Analyzes token distribution across system instructions, tool definitions, scratchpads, and user turns.
2. `simulate_prompt_cache_hit_rate.py` : Evaluates prompt caching efficacy and recommends optimal breakpoint placements to avoid cache misses.
3. `ctx_buffer.py` : Local SQLite FTS5 engine that buffers verbose command outputs and exposes keyword search via BM25.
4. `compressor.py` : Automated lossless prompt and rule compressor reducing file tokens by up to 46%.

### Quick Run Examples:
```bash
# 1. Profile current context consumption
python scripts/profile_context_budget.py --path .

# 2. Simulate prompt cache hit rate
python scripts/simulate_prompt_cache_hit_rate.py --session session.jsonl

# 3. Buffer a verbose command into SQLite
python scripts/ctx_buffer.py run "pytest -v tests/"

# 4. Search within buffered terminal outputs
python scripts/ctx_buffer.py search "AssertionError"

# 5. Compress a prompt or rules file
python scripts/compressor.py CLAUDE.md --out CLAUDE.min.md
```
