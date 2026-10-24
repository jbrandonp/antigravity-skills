---
name: humanoid-robotics-architect
description: >-
  Use this skill when the user asks to design, evaluate, or document humanoid robot architectures, actuator sizing, degrees of freedom (DoF), URDF modeling, or Sim-to-Real pipelines.
---

# 🤖 OLYMPUS PRO : HUMANOID ROBOTICS HARDWARE ARCHITECT

> **Standard :** OLYMPUS System v6.0  
> **Projet Référence :** awesome-humanoid-hardware-guide (Guide open-source d'architecture robotique)  
> **Rôle :** Spécialiste des chaînes cinématiques humanoïdes, dimensionnement d'actionneurs (QDD/Harmonic), dynamique bépède et modélisation physique (URDF/MuJoCo).

---

## 🎯 Déclenchement & Cas d'Usage
Use this skill when the user asks to design, evaluate, or document humanoid robot architectures, actuator sizing, degrees of freedom (DoF), URDF modeling, or Sim-to-Real pipelines.

---

## 🛠️ Outillage Déterministe Intégré
Ce skill embarque un calculateur de couple dynamique pour dimensionner les articulations et vérifier les marges thermiques :
- **Calculateur de Couple Articulaire :** [scripts/calculate_joint_torque.py](scripts/calculate_joint_torque.py)
  ```bash
  python scripts/calculate_joint_torque.py --mass 5.0 --length 0.4 --accel 15.0
  ```
- **Guide de Sélection des Actionneurs :** [references/humanoid_actuation_guide.md](references/humanoid_actuation_guide.md)

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Définition de la Chaîne Cinématique & Degrés de Liberté (DoF)
- Définir la répartition des degrés de liberté :
  - Jambes (Bipédie) : 6 DoF par jambe (3 hanche, 1 genou, 2 cheville).
  - Bras / Manipulateurs : 4 à 7 DoF par bras (3 épaule, 1 coude, 3 poignet).
  - Torse / Nuque : 2 à 3 DoF.
- Cartographier les limites articulaires et les singularités cinématiques.

### Phase 2: Dimensionnement des Actionneurs & Transmission
- Consulter [references/humanoid_actuation_guide.md](references/humanoid_actuation_guide.md).
- Utiliser `python scripts/calculate_joint_torque.py` pour évaluer les couples continus et de crête requis.
- Choisir la technologie adaptée :
  - **Quasi-Direct Drive (QDD, ratio 6:1 à 10:1) :** Idéal pour les membres inférieurs (haute transparence, absorption des chocs au sol, compliance passive).
  - **Réducteurs cycloïdaux ou harmoniques (ratio 50:1 à 100:1) :** Réservés aux hanches de lacet ou articulations nécessitant un maintien statique élevé.

### Phase 3: Modélisation URDF & Propriétés Inertielles
- Spécifier scrupuleusement les tenseurs d'inertie ($I_{xx}, I_{yy}, I_{zz}, I_{xy}, I_{xz}, I_{yz}$) pour chaque lien (Link).
- Définir les centres de masse (CoM) réels basés sur les composants CAO réels.
- Préparer les maillages de collision simplifiés (boîtes, cylindres, capsules) pour la simulation physique (MuJoCo, Isaac Gym).

### Phase 4: Validation Déterministe (Gate Obligatoire)
- Valider la syntaxe URDF (`check_urdf model.urdf`).
- Vérifier que le ratio puissance/poids total permet au robot de se relever en autonomie.
- Documenter les spécifications dans la note Obsidian sous `🤖 Robotics/`.

---

## 🔬 Fondements Scientifiques de la Dynamique Humanoïde (2024-2026)

### 1. Algorithmes Récursifs de Dynamique Multi-Corps (Featherstone)
- **Dynamique Inverse $O(n)$ - RNEA (Recursive Newton-Euler Algorithm)** : Calcule les couples articulaires $\boldsymbol{\tau}$ requis à partir des trajectoires souhaitées :
  $$\boldsymbol{\tau} = \mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{g}(\mathbf{q})$$
  par deux passes récursives linéaires (cinématique vers l'avant, dynamique des forces vers l'arrière).
- **Dynamique Directe $O(n)$ - ABA (Articulated Body Algorithm)** : Calcule les accélérations articulaires $\ddot{\mathbf{q}}$ sans former ni inverser explicitement la matrice de masse $\mathbf{M}(\mathbf{q})$, garantissant une fréquence de rafraîchissement $>1000\text{ Hz}$ en simulation physique (MuJoCo / Pinocchio).

### 2. Stabilité Bipède & Point de Capture (DCM - Divergent Component of Motion)
- La composante divergente du mouvement isole la dynamique divergente du centre de masse ($\mathbf{x}_{\text{CoM}}$) :
  $$\mathbf{x}_{\text{DCM}} = \mathbf{x}_{\text{CoM}} + \frac{\dot{\mathbf{x}}_{\text{CoM}}}{\omega_0}, \quad \omega_0 = \sqrt{\frac{g}{z_0}}$$
- Pour stabiliser la marche face à des perturbations externes, le prochain point d'impact du pied doit être placé sur le point de capture instantané, empêchant le basculement sans saturer les réducteurs de cheville.

### 3. Cinématique Différentielle par Produit d'Exponentielles (PoE) sur SE(3)
- Modélise la chaîne cinématique des membres sans singularités d'alignement d'axes (évitant Denavit-Hartenberg) :
  $$T(\boldsymbol{\theta}) = e^{[\mathcal{S}_1]\theta_1} e^{[\mathcal{S}_2]\theta_2} \dots e^{[\mathcal{S}_n]\theta_n} M$$
- Le jacobien spatial $\mathbf{J}_s(\mathbf{q})$ et le jacobien du corps $\mathbf{J}_b(\mathbf{q})$ sont calculés analytiquement par les opérations adjointes $\mathrm{Ad}_T$, facilitant l'optimisation des mouvements d'évitement d'obstacles et la projection dans l'espace nul $\mathbf{P} = \mathbf{I} - \mathbf{J}^\dagger \mathbf{J}$.
