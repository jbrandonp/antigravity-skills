---
name: bm-reflect
description: "Scan de session. Extraire et router les learnings."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [brainmaxxing, learning, memory]
    related_skills: [bm-meditate, bm-ruminate, continual-learning]
---

# bm-reflect — Scan de session

## When to Use

À la fin d'une session significative, ou immédiatement après une correction de Brandon.

Adapté de brainmaxxing (poteto/brainmaxxing). À lancer en fin de session significative, ou après une correction de Brandon.

## Workflow

1. **Scanner la conversation** pour :
   - Erreurs + corrections reçues de Brandon
   - Préférences exprimées (ton, format, approche)
   - Décisions prises + rationales
   - Frictions d'outils (ce qui a marché / raté)
   - Étapes manuelles automatisables

2. **Router chaque trouvaille** (dans cet ordre) :
   - **Encodable structurellement** (config.yaml, script, cron) → faire le changement, PAS de note
   - **Connaissable procéduralement** → `skill_manage` (créer/patch un skill)
   - **Durable et universel** → `memory` (add)
   - **Spécifique à un projet** → note dans `05-Contexte/`
   - **Suivi requis** → todo

3. **Ne jamais capturer** : le trivial, le déjà-capturé, le one-off sans leçon.

4. **Durability test** : « Est-ce que je l'inclurais dans un prompt pour une AUTRE tâche ? » Non → ne pas noter.

## Sortie

Résumé en 4 lignes : Brain / Skills / Structural / Todos — avec ce qui a été routé où.

## Règle d'or

Si une même instruction s'écrit deux fois → chercher si elle peut devenir un mécanisme (script, config, lint). Si oui : encoder et supprimer l'instruction.