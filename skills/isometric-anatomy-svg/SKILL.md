---
name: isometric-anatomy-svg
description: >-
  Generates interactive, standalone isometric SVG technical illustrations and mechanical system cutaways inspired by wheresryan22/anatomy. Visualizes complex architectures, data pipelines, hardware components, and state machines as isometric exploded diagrams with zero external dependencies.
version: 1.0.0
tags:
  - isometric
  - anatomy
  - svg-illustrations
  - system-architecture
  - exploded-view
---

# 📐 Isometric Anatomy SVG: Exploded Technical Illustrations

> **Inspiration :** Ryan Dahl / `wheresryan22/anatomy`  
> **Axiome Central :** Les architectures complexes méritent des représentations visuelles éclatées, techniques et mécaniques plutôt que de simples boîtes plates reliées par des flèches en 2D.

---

## 🎨 Capacités Visuelles

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. ISOMETRIC PROJECTION (30° Angle): Vraie perspective 3D   │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. EXPLODED LAYERS: Niveaux étagés (Data, App, Infra, Net)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. MECHANICAL CUTAWAYS: Pistons, engrenages, bus de données │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. STANDALONE SVG: Zéro dépendance, CSS vectoriel intégré   │
 └─────────────────────────────────────────────────────────────┘
```

---

## 💻 Utilisation du Compilateur Isométrique

Le skill fournit un générateur Python autonome :

```bash
# Générer un diagramme isométrique à 3 couches (Database, Backend, Client)
python skills/isometric-anatomy-svg/scripts/isometric_compiler.py \
  --title "Scraper Pipeline Architecture" \
  --layers "Raw Scrapers,SQLite FTS5 Buffer,Agentic Core" \
  --output scraper-anatomy.svg

# Mode vue éclatée (Exploded View) avec espacement vertical accentué
python skills/isometric-anatomy-svg/scripts/isometric_compiler.py \
  --title "Autonomous Robot Controller" \
  --layers "Sensors & IMU,Sim-to-Real Policy,Motor Actuators" \
  --exploded \
  --output robot-anatomy.svg
```
