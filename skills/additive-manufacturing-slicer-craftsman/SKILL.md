---
name: additive-manufacturing-slicer-craftsman
description: >-
  Architect and implement additive manufacturing pipelines, 3D printing DFM rules (overhangs >45°, bridging limits, minimum wall thicknesses), G-code generation, slicer automation (OrcaSlicer CLI, PrusaSlicer, Bambu Studio), support structure strategies (tree vs organic), infill geometry (gyroid, cubic), and extrusion temperature audits. Use when the user asks about 3D printing, slicers, OrcaSlicer, PrusaSlicer, G-code parsing, layer height, or FDM/SLA additive manufacturing.
---

# 🖨️ Additive Manufacturing & Slicing Craftsman (FDM / SLA / SLS)

> **Moteurs de Tranchage :** OrcaSlicer CLI, PrusaSlicer CLI, Bambu Studio, CuraEngine  
> **Standards :** ISO/ASTM 52900 (Terminologie Fabrication Additive), ISO/ASTM 52910 (Conception DfAM)  
> **Rôle :** Spécialiste de la fabrication additive, de l'optimisation d'orientation sur plateau, de la génération de supports arborescents, des profils d'extrusion volumétrique et de l'audit de G-code.

---

## 🎯 Déclenchement & Cas d'Usage
Active ce skill pour :
- **Règles DfAM (Design for Additive Manufacturing)** : Détection des surplombs critiques (> 45° sans support), limites de pontage (*bridging*), épaisseurs minimales de parois (selon diamètre de buse 0.4mm / 0.6mm).
- **Stratégies de Tranchage & Remplissage** : Sélection optimale des motifs d'infill (Gyroid pour isotropie mécanique, Cubic pour résistance en compression), hauteurs de couches adaptatives.
- **Supportage Intelligent** : Choix entre supports arborescents (*tree/organic supports*) pour réduire la consommation matière et l'effort de post-traitement, et supports linéaires.
- **Automatisation CLI des Slicers** : Exécution headless d'OrcaSlicer ou PrusaSlicer en ligne de commande pour trancher des assemblages en lots automatisés.
- **Contrôle & Audit de G-code** : Vérification des températures de buse/plateau (M104, M109, M140, M190), de la cohérence d'extrusion, des vitesses de déplacement et du temps d'impression estimé.

---

## ⚙️ 1. Règles Géométriques DfAM Fondamentales

| Paramètre | Limite Recommandée (Buse 0.4 mm) | Risque en Cas de Non-Respect |
| :--- | :--- | :--- |
| **Angle de surplomb (Overhang)** | $\le 45^\circ$ par rapport à la verticale | Affaissement des filaments, cordage, perte de tolérance |
| **Longueur de pont (Bridge)** | $\le 15\text{ mm}$ sans support | Rupture de continuité, effondrement sous gravité |
| **Épaisseur de paroi minimale** | $\ge 1.2\text{ mm}$ (3 périmètres) | Paroi poreuse, délamination entre couches |
| **Tolérance d'ajustement (Clearance)** | $\ge 0.35\text{ mm}$ (assemblages mobiles) | Fusion par collage thermique des pièces articulées |
| **Orientation sur plateau** | Alignement des contraintes maximales dans le plan XY | Les liaisons inter-couches (Z) ont une résistance à la traction réduite de 30 à 50% |

---

## 💻 2. Automatisation OrcaSlicer / PrusaSlicer CLI

```bash
# Tranchage déterministe headless via OrcaSlicer CLI
orca-slicer --slice \
  --output "build/part_slice.gcode" \
  --load-settings "profiles/pla_fdm_020.json" \
  --export-3mf "build/plate_layout.3mf" \
  "models/piece_mecanique.stl"
```

---

## 🔍 3. Outil Compagnon Déterministe

Le script compagnon [`verify_slicing_gcode.py`](scripts/verify_slicing_gcode.py) analyse les fichiers `.gcode` et valide :
1. La présence et la conformité des commandes de chauffe buse/plateau.
2. La monotonie stricte des coordonnées Z (hauteur de couche croissante).
3. La quantité totale de filament extrudé (coordonnées E).
4. La cohérence des vitesses d'avance (flux volumétrique $mm^3/s \le 15$ pour du PLA standard).
