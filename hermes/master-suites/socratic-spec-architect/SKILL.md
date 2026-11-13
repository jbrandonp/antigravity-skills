---
name: socratic-spec-architect
description: >-
  The Matt Pocock Socratic engineering methodology for AI agents. Enforces relentless clarifying interviews (/grill-me, /grill-with-docs) before writing code, compiling discussions into formal specifications, dependency ticket graphs, and structured session handoffs (/handoff).
version: 1.0.0
tags:
  - socratic-interview
  - spec-driven
  - ticket-graph
  - matt-pocock
  - handoff
---

# 🧐 Socratic Spec Architect & Session Handoff Engine

> **Inspiration :** Matt Pocock (`mattpocock/skills` - "Skills for Real Engineers").  
> **Axiome Central :** Zéro code écrit à l'aveugle. L'agent bloque le clavier, pose des questions incisives sur les ambiguïtés architecturales, génère un graphe de tickets bloquants et compresse la session pour les passages de relais.

---

## 🔄 Le Cycle "Idea-to-Ship" de Matt Pocock

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. /grill-me & /grill-with-docs : L'interview socratique    │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. /to-spec : Compilation de la discussion en SPEC.md       │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. /to-tickets : Graphe de tickets atomiques (DAG)          │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. /implement : Exécution par sous-agents en TDD            │
 ├─────────────────────────────────────────────────────────────┤
 │ 5. /handoff : Compression pour nouvelle session propre      │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Commandes & Protocoles

### 1. `/grill-me` & `/grill-with-docs`
* **Comportement :** L'agent refuse d'écrire du code. Il analyse la documentation locale, les types et la demande de l'utilisateur, puis pose 3 à 5 questions critiques pour forcer les arbitrages :
  - *Quels sont les cas d'erreur attendus (timeout, rate limit, schéma corrompu) ?*
  - *Quels sont les types stricts d'entrée et de sortie ?*
  - *Quelle est la politique de rétention ou de synchronisation ?*
* Met à jour automatiquement un `GLOSSARY.md` et consigne les décisions dans `_DECISIONS.md`.

### 2. `/to-spec` & `/to-tickets`
* Transforme la conversation validée en une spécification formelle (`SPEC.md`).
* Découpe la spécification en tickets atomiques indépendants de 2 à 5 minutes avec dépendances :
  ```markdown
  - [x] Ticket #1: Créer le schéma de base de données (Prérequis: Aucun)
  - [ ] Ticket #2: Implémenter l'adaptateur de requêtes (Prérequis: #1)
  - [ ] Ticket #3: Ajouter les tests de validation (Prérequis: #2)
  ```

### 3. `/handoff` (Générateur de Relais)
* Lorsque la session commence à devenir longue ou que le contexte se dégrade, l'agent génère un document de transfert propre pour démarrer une nouvelle session à blanc :
  ```bash
  python skills/socratic-spec-architect/scripts/handoff_generator.py \
    --title "Multi-Store Scraper Upgrade" \
    --summary "Added SQLite FTS5 buffer and updated Delhaize parser." \
    --next "Implement Colruyt dynamic category traversal" \
    --next "Add rate-limit backoff handler" \
    --output HANDOFF.md
  ```
