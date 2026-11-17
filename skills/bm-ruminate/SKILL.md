---
name: bm-ruminate
description: "Minage de l'historique des sessions. Extraire les patterns."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [brainmaxxing, history, mining]
    related_skills: [bm-reflect, continual-learning]
---

# bm-ruminate — Minage de l'historique

## When to Use

Occasionnellement (hebdo/mensuel) pour bootstraper ou compléter le brain depuis l'historique de sessions.

Adapté de brainmaxxing. À lancer occasionnellement (hebdo/mensuel) pour bootstraper ou compléter le brain depuis l'historique de sessions.

## Workflow

1. **Utiliser `session_search`** sur les sessions passées avec des requêtes ciblées :
   - Corrections de Brandon ("non", "pas ça", "t'es sûr", corrections orthographiques)
   - Préférences répétées ("fait comme ça", "j'aime pas")
   - Frustrations ("ça marche pas", "pourquoi tu fais ça")
   - Learnings techniques (erreurs résolues, workarounds découverts)

2. **Filtrer par fréquence + impact** : mieux vaut 3 findings à haut signal que 9 avec du bruit.

3. **Dédupliquer** avec ce qui existe déjà dans memory + 05-Contexte.

4. **Router** (même logique que bm-reflect) :
   - Structurel → config/script
   - Skill → skill_manage
   - Durable → memory
   - Projet → 05-Contexte

5. **Présenter à Brandon** : liste des findings avec citations exactes des sessions. Appliquer seulement ce qu'il approuve.

## Citer, toujours

Pour chaque correction directe de Brandon : citer ses mots exacts + la date de session. Pas de paraphrase.