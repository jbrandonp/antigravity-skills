---
name: kinematic-character-controller
description: >-
  Design and implement responsive 2D and 3D kinematic character controllers with premium game feel, tactile juice, and Unreal Engine 5.5 - 5.8 Motion Matching. Enforces Coyote Time (80-130ms), Jump Buffering (100-150ms), variable jump height, apex floatiness, slope projection, Two-Bone Inverse Kinematics (IK) for foot placement, trauma-based screen shake (T²), hitstop freeze-frames, audio pitch randomization, and UE5 Motion Matching (Pose Search Databases, Chooser Tables, Trajectory sampling, and Inertialization blending).
---

# 🕹️ Master Kinematic Character Controller & Next-Gen Locomotion (SOTA 2026)

> **Inspirations & Provenance :** Matt Thorson (*Celeste*), Martin Jonasson & Petri Purho (*Juice it or lose it*), Epic Games Unreal Engine 5.5 - 5.8 Motion Matching & Pose Search Architecture.  
> **Core Axiom :** *"A character controller must feel responsive in physics and fluid in animation. Combine kinematic input forgiveness (Coyote/Buffer) with UE5 Motion Matching trajectory synthesis and procedural Foot IK."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine que tu contrôles un personnage dans un jeu d'action ou de plateforme exceptionnel :
1. **Le Temps du Coyote (Coyote Time)** :
   Comme dans les dessins animés de Bip Bip et Coyote, quand le personnage quitte le bord d'une falaise, le jeu lui donne une tolérance secrète de **80 à 130 millisecondes** pour appuyer sur Saut, même s'il court déjà techniquement dans le vide. Le joueur a l'impression d'avoir des réflexes surhumains !
2. **La Mémoire Tampon (Jump Buffering)** :
   Si tu appuies sur Saut un dixième de seconde trop tôt avant d'avoir touché le sol, le jeu ne jette pas ta commande à la poubelle : il la garde en mémoire et déclenche le saut à la première frame de contact.
3. **Le Motion Matching (L'Animation Fluide sans Coupures)** :
   Dans les vieux jeux, le personnage passe brutalement d'une animation de marche à une animation de course avec des transitions rigides qui font glisser les pieds. Avec le **Motion Matching d'Unreal Engine 5**, le jeu prédit où tu seras dans 1 seconde en fonction de la direction de ton joystick, fouille dans une base de données de milliers de poses de capture de mouvement en moins de 0.1 ms, et choisit la pose exacte qui correspond à ta trajectoire !
4. **L'Ancrage des Pieds (Two-Bone Foot IK)** :
   Si le héros monte un escalier ou marche sur un terrain rocheux, ses jambes ne traversent pas la pierre et ne flottent pas dans le vide. Deux os (cuisse et mollet) se plient mathématiquement par la loi des cosinus pour poser la semelle à plat sur la pente.
5. **Le "Juice" Tactile (Trauma Shake & Hitstop)** :
   Quand tu frappes violemment un ennemi, le jeu se fige pendant 3 frames (40 ms de *Hitstop*) pour que ton cerveau savoure l'impact, la caméra tremble avec une secousse quadratique ($T^2$), et le son du coup change légèrement de hauteur pour éviter la fatigue auditive.

---

## 🎮 2. Les 6 Piliers du Contrôleur Kinématique

1. **Coyote Time** : Fenêtre de **80 à 130 ms** après la perte de contact au sol.
2. **Jump Buffering** : Fenêtre de **100 à 150 ms** avant atterrissage.
3. **Variable Jump Height** : Coupure de la vélocité ascendante ($\times 0.5$) si le bouton de saut est relâché avant le sommet.
4. **Apex Floatiness** : Réduction de 40% de la gravité lorsque $|\text{velocity.y}| < \text{threshold}$ au sommet de la trajectoire pour offrir un contrôle aérien précis.
5. **Corner Correction / Ledge Nudge** : Décalage horizontal automatique de quelques pixels si la tête heurte l'angle d'un plafond.
6. **Slope Projection** : Projection de la vélocité sur le plan de la pente pour éliminer les sauts parasites en descente :
   $$\vec{v}_{\text{slope}} = \vec{v} - (\vec{v} \cdot \vec{n}) \vec{n}$$

---

## 📐 3. Équations de Saut Déterministes

Calculez la gravité et la force de saut à partir de la hauteur désirée ($h$) et du temps de montée ($t_{\text{rise}}$) :
$$\text{Gravity} = \frac{2h}{t_{\text{rise}}^2}, \quad \text{JumpVelocity} = -\frac{2h}{t_{\text{rise}}}$$

*Exemple pour $h = 3.5\text{ m}$ et $t_{\text{rise}} = 0.35\text{ s}$ :*
$$\text{Gravity} = \frac{7}{0.1225} \approx 57.14\text{ m/s}^2, \quad \text{JumpVelocity} = -\frac{7}{0.35} = -20.0\text{ m/s}$$

---

## 🤖 4. Unreal Engine 5.5 - 5.8 Motion Matching & Pose Search

Éliminez les Blend Spaces et machines à états complexes au profit de la recherche de trajectoire continue :

### Échantillonnage de Trajectoire (CharacterTrajectoryComponent)
- Échantillonne l'historique récent ($-0.5\text{s}, -0.2\text{s}$) et prédit la trajectoire future ($+0.2\text{s}, +0.5\text{s}, +1.0\text{s}$).
- Évalue la fonction de coût de correspondance de pose :
  $$\text{Cost} = w_{\text{pose}} \sum_{b} \| P_b - \hat{P}_b \|^2 + w_{\text{traj}} \sum_{t} \left( \| X_t - \hat{X}_t \|^2 + \lambda \| V_t - \hat{V}_t \|^2 \right)$$

### Bases de Recherche de Poses (Pose Search Databases & Chooser Tables)
- Indexation par arbres KD-Tree / VP-Tree garantissant une recherche en sous-milliseconde ($< 0.1\text{ ms}$).
- Filtrage dynamique des démarches (Marche, Jogging, Sprint, Accroupi, Demi-tour brusque) via des **Chooser Tables**.

### Inertialization Blending & Foot IK
- Remplacement du cross-fading par le nœud **Inertialization** d'Unreal Engine 5 (préserve la continuité des vitesses et accélérations articulaires sans glissement de pied).
- Application du solveur Two-Bone IK par-dessus la pose matchée pour adapter les semelles au dénivelé.

---

## 🦵 5. Ancrage au Sol : Solveur Two-Bone IK

Loi des cosinus dans le triangle de la jambe (cuisse $L_1$, mollet $L_2$, distance sol-hanche $D$) :
$$\cos(\theta_{\text{knee}}) = \frac{L_1^2 + L_2^2 - D^2}{2 L_1 L_2}, \quad \cos(\theta_{\text{hip}}) = \frac{L_1^2 + D^2 - L_2^2}{2 L_1 D}$$

- **Décalage Dynamique du Bassin (Pelvis Offset)** :
  $$\Delta h = \min(h_{\text{pied\_gauche}}, h_{\text{pied\_droit}})$$
  Le bassin est abaissé dynamiquement de $\Delta h$ pour que les deux pieds touchent le sol sans étirement excessif.

---

## 💥 6. Game Juice : Trauma Screen Shake & Hitstop

1. **Non-Linear Trauma Shake ($T^2$)** :
   Le trauma $T \in [0.0, 1.0]$ décroît linéairement, mais l'amplitude de secousse est quadratique :
   $$\text{Angle} = \text{max\_angle} \times T^2 \times \text{noise}(t), \quad \text{Offset} = \text{max\_offset} \times T^2 \times \text{noise}(t + 100)$$
2. **Hitstop Freeze-Frames** : Pause de 30 ms à 60 ms de la boucle d'animation lors des coups lourds pour un impact viscéral.
3. **Anti-Fatigue Sonore** : Variation aléatoire du pitch audio :
   $$\text{Pitch} = \text{base\_pitch} \times \text{rand\_range}(0.92, 1.08)$$

---

## 🛠️ 7. Suite Déterministe d'Outils

```bash
# 1. Simuler le saut kinématique et valider Coyote Time / Jump Buffer
python scripts/simulate_kinematic_jump.py

# 2. Calculer les angles Two-Bone IK sur dénivelé
python scripts/calculate_two_bone_ik.py

# 3. Calculer la courbe d'amortissement du Trauma Screen Shake
python scripts/calculate_trauma_shake.py --impact 0.8 --decay 1.2

# 4. Simuler une requête de recherche de trajectoire Motion Matching
python scripts/simulate_motion_matching_query.py --demo
```
