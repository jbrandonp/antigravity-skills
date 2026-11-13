---
name: impeccable-design-engine
description: >-
  62-rule local frontend design linter and polish engine (zero API token cost) inspired by Paul Bakaus. Enforces strict typographic scale, 4px/8px rhythm, WCAG contrast compliance, interactive states (:hover, :focus-visible, disabled), and layout responsiveness.
version: 1.0.0
tags:
  - impeccable
  - frontend-design
  - design-linter
  - accessibility
  - anti-slop
---

# 🎨 Impeccable Design Engine: 62-Rule Frontend Linter & Polisher

> **Inspiration :** Paul Bakaus (`pbakaus/impeccable`).  
> **Axiome Central :** L'AI Slop frontend (contrastes illisibles, boutons sans états de focus, valeurs arbitraires `text-[13px]`, mise en page bancale) doit être intercepté en local par des règles heuristiques déterministes sans dépenser de tokens d'API.

---

## 📐 Les 5 Fondations du Design Impeccable

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Rythme Vertical & Espacements: Grille stricte 4px / 8px  │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Échelle Typographique: Tailles proportionnées (12/16/24) │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. États Interactifs: :hover, :active, :focus-visible       │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Accessibilité WCAG: Contrastes 4.5:1 & aria-label        │
 ├─────────────────────────────────────────────────────────────┤
 │ 5. Thème Cohérent: Tokens CSS sémantiques vs hexadécimal    │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Commandes & Outils

### 1. `/impeccable audit` (Linter Local)
Exécute le moteur de scan statique sur l'ensemble des fichiers HTML, JSX, TSX, CSS ou Vue :
```bash
python skills/impeccable-design-engine/scripts/design_audit.py src/
```

### 2. `/impeccable polish`
Règles de correction automatique appliquées par l'agent :
- Remplacer les espacements arbitraires (`p-[7px]`) par les équivalents de la grille Tailwind (`p-2`).
- Ajouter les états d'accessibilité manquants (`focus-visible:ring-2 focus-visible:ring-offset-2`).
- Assurer un fallback propre des polices système pour éviter les sursauts visuels (CLS).

### 3. `/impeccable critique`
Revue critique d'interface :
- Vérifier que la hiérarchie visuelle guide le regard vers l'appel à l'action (CTA) principal en moins de 3 secondes.
- Éliminer les dégradés et ombres plates génériques ("AI purple slop") au profit d'une palette typée et contrastée.
