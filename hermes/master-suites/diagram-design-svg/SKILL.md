---
name: diagram-design-svg
description: >-
  Editorial technical diagram generator producing 45+ types of standalone HTML+SVG architecture diagrams (flowcharts, sequence diagrams, ERDs, cloud topologies, 2x2 quadrants) with zero external JavaScript or CDN dependencies.
version: 1.0.0
tags:
  - diagram-design
  - svg-diagrams
  - editorial-design
  - technical-architecture
  - zero-dependency
---

# 📊 Diagram Design SVG: Zero-Dependency Editorial Diagrams

> **Inspiration :** Cathryn Lavery (`cathrynlavery/diagram-design` - 66k+ ⭐).  
> **Axiome Central :** Les schémas Mermaid sont souvent laids, difficiles à personnaliser et nécessitent des visualiseurs tiers. Ce skill génère du code HTML et SVG autonome, élégant, réactif, supportant nativement les thèmes clair/sombre via CSS, sans aucune dépendance JS externe.

---

## 🎨 Caractéristiques & Types Supportés

- **Zéro Dépendance Externe :** Aucun CDN, aucune bibliothèque JavaScript requise. Rendu instantané dans n'importe quel navigateur ou webview.
- **Support Thème Sombre & Clair Automatique :** Couleurs gérées via variables CSS `@media (prefers-color-scheme: dark)`.
- **Typographie Éditoriale :** Polices système modernes (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`), contrastes nets et marges aérées.
- **Catalogue de Types :**
  1. *Architecture Système Multi-Couches* (Client -> Passerelle -> Services -> Persistance).
  2. *Diagrammes de Séquence Temporelle* (Acteurs, lignes de vie, messages asynchrones).
  3. *Matrices 2x2 & Quadrants Stratégiques* (Effort vs Impact, Sécurité vs Vélocité).
  4. *Modèles Entité-Association (ERD)* et flux de données.

---

## 💻 Commandes d'Utilisation

```bash
# Générer un diagramme d'architecture système complet
python skills/diagram-design-svg/scripts/svg_generator.py \
  --type architecture \
  --title "Microservice Scraping & SQLite FTS5 Pipeline" \
  --output docs/architecture.html

# Générer un diagramme de séquence
python skills/diagram-design-svg/scripts/svg_generator.py \
  --type sequence \
  --title "Context-Mode Buffer Sequence" \
  --output docs/sequence.html
```
