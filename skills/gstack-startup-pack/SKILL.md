---
name: gstack-startup-pack
description: >-
  Full Y Combinator product delivery and startup leadership suite inspired by Garry Tan (gstack). Deploys specialized personas (/plan-ceo-review, /plan-eng-review, /plan-design-review, /design-shotgun, /ship, /verify, /autoplan) to eliminate feature bloat and ensure fast, verified product delivery.
version: 1.0.0
tags:
  - gstack
  - garry-tan
  - product-management
  - ceo-review
  - startup
  - ship
---

# 🚀 GStack Startup Pack: YC Founder & Product Delivery Suite

> **Inspiration :** Garry Tan, Président & CEO de Y Combinator (`garrytan/gstack` - 141k+ ⭐).  
> **Axiome Central :** Ne code pas comme un exécutant isolé. Adopte tour à tour le regard d'un CEO fondateur, d'un VP Engineering, d'un lead designer et d'un release manager pour expédier de la vraie valeur rapidement.

---

## 👥 Les 5 Personas Virtuels

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. CEO REVIEW (/plan-ceo-review): Valeur, MVP, Rétention    │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. DESIGN REVIEW (/plan-design-review): Clarté & Ergonomie  │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. ENG REVIEW (/plan-eng-review): Résilience & Scalabilité  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. VERIFY (/verify): Tests end-to-end automatisés           │
 ├─────────────────────────────────────────────────────────────┤
 │ 5. SHIP (/ship): Release notes, tag Git et déploiement      │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Commandes & Rôles

### 1. `/plan-ceo-review` (Le Filtre YC)
- Pose la question fondamentale : *"Est-ce que cette fonctionnalité résout un problème urgent pour l'utilisateur ?"*
- Coupe systématiquement 50% de la complexité initiale pour concevoir un MVP radical livrable en 24-48 heures.
- Élimine le "feature creep" (accumulation inutile de fonctionnalités gadgets).

### 2. `/plan-design-review` & `/design-shotgun`
- Évalue la hiérarchie visuelle, la lisibilité et l'accès direct aux actions principales.
- `/design-shotgun` : Génère 3 variantes d'interface ou de flux utilisateur (minimaliste, axé données, dense) avec les pour/contre avant tout développement.

### 3. `/plan-eng-review`
- Audite la robustesse technique : temps de réponse, risques de verrous de base de données (deadlocks SQLite), consommation mémoire et gestion des pannes réseau.
- Vérifie que le code reste maintenable sans ajouter de briques d'infrastructure superflues.

### 4. `/verify`
- Lance la suite complète de vérification :
  - Tests unitaires et d'intégration
  - Linter et typage strict (zéro `any`)
  - Vérification de l'absence de régression dans les journaux
  - Validation visuelle si des composants UI sont touchés

### 5. `/ship`
- Compile les changements en un changelog propre et lisible pour l'humain.
- Crée un commit Git au format conventionnel `feat(...)` ou `fix(...)`.
- Prépare le tag de version et valide que la branche est prête pour la mise en production.
