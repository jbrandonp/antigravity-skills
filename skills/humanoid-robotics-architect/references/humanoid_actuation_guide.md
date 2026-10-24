# Guide de Sélection des Actionneurs pour Robots Humanoïdes

Ce guide résume les compromis technologiques pour concevoir des membres bépèdes robustes.

---

## 1. Comparatif des Technologies d'Actionnement

| Technologie | Ratio Réduction | Transparence / Backdrivability | Résistance aux Chocs | Usage Humanoïde Idéal |
| :--- | :---: | :---: | :---: | :--- |
| **Quasi-Direct Drive (QDD)** | 6:1 à 10:1 | **Excellente** (95%) | **Très haute** | Genoux, chevilles, hanches (absorption d'impacts) |
| **Planetary Gearbox** | 15:1 à 30:1 | Bonne (75%) | Moyenne | Épaules, coudes |
| **Harmonic Drive** | 50:1 à 160:1 | Faible / Nulle | Fragile aux à-coups | Bras de manipulation fine, cou, buste |

---

## 2. Règle Fondamentale : Minimiser l'Inertie Distale

Pour maximiser la dynamique de marche et réduire la dépense énergétique :
- **Placer les moteurs lourds au plus près du tronc.**
- Relier les articulations distales (chevilles) par des tringleries légères (Push-rods en fibre de carbone) ou des courroies crantées plutôt que de mettre le moteur directement dans le pied.
