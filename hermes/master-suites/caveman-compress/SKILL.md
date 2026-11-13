---
name: caveman-compress
description: >-
  Extreme token economy engine and telegraphic communication suite. Strips conversational filler, cuts output tokens by up to 65%, and includes automated prompt/rule compression (/caveman-compress) to shrink CLAUDE.md, .cursorrules, and system instructions by ~46% without semantic loss.
version: 1.0.0
tags:
  - token-economy
  - compression
  - concision
  - prompt-engineering
---

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
