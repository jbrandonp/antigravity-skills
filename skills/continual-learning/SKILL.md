---
name: continual-learning
description: "Cadence mémoire auto hebdo. Complète bm-reflect."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [brainmaxxing, learning, memory]
    related_skills: [bm-reflect, bm-ruminate, bm-meditate]
---

# continual-learning — Mémoire qui s'améliore seule

## When to Use

Déclenché par le cron hebdo (dimanche 19:30, job 4bd22702698e) ; manuellement pour un minage ad hoc.

Inspiré du plugin continual-learning de poteto/plugins (MIT). Complète `bm-reflect` (qui scanne une session) avec une cadence automatique.

## Principe

La mémoire de l'agent doit se mettre à jour depuis les transcripts de sessions, à cadence fixe, avec un index incrémental — pas de re-scan intégral à chaque fois.

## Mécanisme Hermes

1. **Cadence** : un cron hebdomadaire (dimanche, après le bilan 19:00) lance ce skill sur les sessions de la semaine.
2. **Index incrémental (mtime)** : tenir `05-Contexte/_learning-index.md` listant sessions déjà minées (date + session_id). Ne jamais re-miner une session déjà traitée.
3. **Extraction** : pour chaque session nouvelle → `session_search` ciblé (corrections Brandon, erreurs répétées, préférences, workarounds).
4. **Router** (même logique que bm-reflect) : structurel → config/script ; skill → skill_manage ; durable → memory ; projet → 05-Contexte.
5. **Rapport** : liste des items routés + items proposés mais non appliqués (décision Brandon).

## Garde-fous

- Aucune modification de config/skill à cette cadence sans validation Brandon pour les actions irréversibles.
- Signal > volume : 3 findings à haut signal valent mieux que 9 avec du bruit.
- Citer les mots exacts de Brandon pour chaque correction (pas de paraphrase).

## Distinction avec les autres skills

- `bm-reflect` = fin d'une session ponctuelle (manuel).
- `bm-ruminate` = minage ponctuel de l'historique (manuel).
- `continual-learning` = la cadence automatique qui garantit que rien n'est perdu.