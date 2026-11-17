---
name: how
description: "Explique comment fonctionne X. Fan-out puis synthèse."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [architecture, analysis, brainmaxxing]
    related_skills: [poteto-playbooks, verify-brandon]
---

# how — Explication d'architecture

## When to Use

Quand Brandon (ou un agent) demande « comment fonctionne X ? » — codebase, workflow, système.

Portage Hermes de poteto/how (Lauren Tan, MIT). Répond aux questions « comment fonctionne X ? » niveau onboarding senior.

## Deux modes

1. **Explain** (défaut) — explorer et expliquer
2. **Critique** — expliquer d'abord, puis critiques parallèles sur modèles différents

## Mode Explain

### 1. Évaluer la complexité

- **Simple** (un module, question étroite) → PAS de subagents : expliquer en un passage.
- **Complexe** (sous-système multi-fichiers) → explorers parallèles puis synthèse.

En cas de doute : chemin simple. On peut toujours ajouter des explorers.

### 2a. Explorer (complexe)

Décomposer en 2-4 angles parallèles distincts via `delegate_task` en UN appel, explorers read-only (collecte de faits, pas de prose). Chaque explorer :
- Start broad → suivre le fil (call chain, flux) → lire le réel, jamais deviner
- S'arrêter quand le chemin input→output est descriptible sans hand-waving
- Sortie structurée : Components / Flow / Files Read / Boundaries / Non-Obvious / Open Questions
- **Dire « je n'ai pas pu tracer X » plutôt que d'inventer**

### 2b. Explain direct (simple)

Un seul subagent explore + explique en un passage.

### 3. Synthétiser (complexe)

Un SEUL synthétiseur : réconcilie les chevauchements, résout les contradictions, tableau unifié.

### 4. Présenter

La communication du synthétiseur EST le produit — ne pas réécrire substantiellement.

### Format (adapter au besoin)

- **Overview** — c'est quoi, pourquoi ça existe (1-2 ¶)
- **Key Concepts** — abstractions clés, brefs
- **How It Works** — flux pas à pas en prose, fichiers nommés, pas de pseudocode
- **Where Things Live** — carte des fichiers nécessaires
- **Gotchas** — pièges, non-évident, contexte historique

## Mode Critique

1. **Explain d'abord**
2. **3 critiques en parallèle sur 3 modèles différents** (diversité = signal) via delegate_task, rubrique partagée
3. **Le lead TRIE** au lieu d'agréger : Act on / Consider / Noted / Dismissed

### Rubrique (6 lentilles)

Abstraction Fit · Data Model · Boundary Discipline · Evolution Readiness · Complexity vs. Value · Consistency

### Règles critique

- Sévérité structural/concern/observation avec preuve (fichier/ligne) + impact
- Interdits : review ligne-à-ligne, rewrites sans preuve
- **Une critique vide est un résultat valide**

## Rappel Hermes

- Sauver les explications produites dans `05-Contexte/` (format d'onboarding vault).