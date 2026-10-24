---
name: game-ai-behavior-tree
description: >-
  Design and implement hierarchical Game AI Behavior Trees, Unreal Engine 5 StateTree state machines, Utility AI, and creature spawning/patrol engines. Enforces composite nodes (Selectors, Sequences), Decorators, Blackboard shared state memory, Catmull-Rom spline patrol motion with dwell times, delta-level aggro radiuses (5m to 40m), tactical kiting/retreat state machines for ranged enemies, and UE5 StateTree evaluators, tasks, and state transitions.
---

# Game AI Behavior Tree (Behavior Tree & Utility AI Standard)

Hierarchical Game AI architecture framework used by AAA and indie studios. Replaces sprawling, unmaintainable state machines with modular, reactive **Behavior Trees** (BT).

---

## 🧠 The 4 Structural Nodes of Behavior Trees

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Composite Nodes: Selectors (?) & Sequences (->)          │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Decorators: Inverters, Repeaters, Condition Gates        │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Leaf Tasks: Actions (NavigateTo, Attack, Patrol, Flee)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Blackboard State Memory (Shared variables: target, alert)│
 └─────────────────────────────────────────────────────────────┘
```

### Node 1: Selector (?) — "Fallback / OR"
- Runs children left to right.
- **Succeeds immediately** when any child returns `SUCCESS`.
- Fails only if *all* children return `FAILURE`.
- Perfect for prioritizing actions: Combat $\rightarrow$ Investigate $\rightarrow$ Patrol.

### Node 2: Sequence (->) — "Plan / AND"
- Runs children left to right.
- **Fails immediately** if any child returns `FAILURE`.
- Succeeds only if *all* children return `SUCCESS`.
- Perfect for execution steps: FindPath $\rightarrow$ MoveTo $\rightarrow$ PerformStrike.

### Node 3: The Blackboard Pattern
- A shared dictionary decoupling AI logic from game engines.
- Stores: `target_player: Node3D`, `last_heard_noise: Vector3`, `health_ratio: float`.

---

## 🛠️ Deterministic Tooling

```bash
# Validate behavior tree structure for dangling nodes and infinite loops
python scripts/validate_behavior_tree.py --demo
```

---

## 🐾 Module Complémentaire : Moteur de Spawning, Patrouille par Spline de Catmull-Rom & Kiting Tactique

# Universal Dynamic Spawning, Spline Patrol & AI Aggro / Leash Engine

## 1. Executive Overview & Pedagogical Analogy (Style 15 ans)

Imagine que le monde de World of Warcraft est peuplé de millions de créatures vivantes : des loups dans les bois, des gardes qui patrouillent sur les remparts d'Hurlevent, et de redoutables dragons dans leurs cavernes :
1. **Le Modèle de Base vs le Monstre dans le Monde** :
   Le serveur ne crée pas 10 000 fois la fiche d'un loup. Il y a un seul modèle d'origine (`creature_template` : ses PV, sa morsure, son pelage), et des milliers de petits points de spawn (`creature`) qui disent où chaque loup apparaît sur la carte.
2. **Le Respawn Dynamique (Quand le serveur accélère le temps)** :
   Si tu es seul dans la forêt, un monstre tué met 5 minutes à réapparaître. Mais si 50 joueurs débarquent en même temps le jour de la sortie du jeu pour faire la même quête, le serveur le détecte et accélère les réapparitions : le monstre réapparaît toutes les 30 secondes pour que personne ne reste coincé à attendre !
3. **La Patrouille Fluide (Courbes Splines)** :
   Les gardes ne marchent pas en faisant des angles droits comme des robots cassés. Le moteur lisse leur chemin avec des courbes harmonieuses (*Splines de Catmull-Rom*). Quand un garde arrive à un poste d'observation, il s'arrête, se tourne vers la vallée et attend 10 secondes avant de reprendre sa ronde.
4. **Le Rayon d'Aggro selon la Différence de Niveau ($\Delta L$)** :
   - Si tu as le même niveau que le loup (niveau 20 contre 20), il t'attaque dès que tu passes à moins de **20 mètres**.
   - Si tu es niveau 10 face à un monstre de niveau 30 (*Tête de mort*), il a une vue d'aigle et te charge de super loin (**40 mètres**) !
   - Mais si tu es niveau 60 face à un petit sanglier niveau 5, il a tellement peur qu'il ne bouge pas, sauf si tu lui marches littéralement sur la queue (**5 mètres**) !
5. **La Laisse et le Mode Évasion (Leash & Evade à Vitesse x2)** :
   Si tu tires sur un boss et que tu t'enfuis à l'autre bout de la carte pour essayer de l'arnaquer (*kiting infini*), le monstre s'arrête net dès qu'il franchit sa distance de laisse (**40 mètres** de son point de départ). Il devient invulnérable, se soigne à 100% et rentre chez lui en courant à **deux fois sa vitesse normale** !

---

## 🌐 Universal Cross-Genre & Engine Application

This engine provides player-density dynamic respawn scaling, Catmull-Rom spline patrol motion, and delta-level aggro/leash mechanics applicable to ANY game with NPC behaviors:

| Game Genre | Concrete Application |
| :--- | :--- |
| **Open-World Action & Stealth (Far Cry, Assassin\'s Creed, MGS)** | Enemy base patrols along splines with realistic dwell times, vision cones (180 deg) and proximity alerts, returning to post if player evades. |
| **Souls-like & Action RPGs (Elden Ring, Dark Souls)** | Monster patrol paths, strict leash reset zones preventing cheese pulling of difficult enemies across the map. |
| **Survival & Crafting (Rust, Valheim, 7 Days to Die)** | Wildlife and mutant spawning that scales up dynamically when multiple players group in the same territory. |
| **Multiplayer Shooters (The Division, Destiny, Payday)** | Co-op mission reinforcement spawning, waves patrolling along waypoints, disengaging when players flee beyond encounter radius. |
| **MMORPGs & Virtual Worlds** | World mob spawning, dynamic anti-camp respawn scaling, leash boundaries resetting creature HP at 200% movement speed. |

### Engine Integration Matrix:
- **Unreal Engine 5** : Integrates with AIController, StateTree, and Spline Components.
- **Godot 4.x** : Integrates with Path3D / PathFollow3D nodes and custom NPC finite state machines.
- **Bevy Engine (Rust)** : Evaluated as PatrolSpline and AggroRadius ECS components.
- **Custom C++ / Python** : Clean standalone state machine evaluated at fixed simulation ticks.

---

## 2. Délais de Réapparition Dynamiques (Dynamic Respawn Scaling)

Pour éviter la pénurie de monstres lors des pics d'affluence :
$$T_{\text{respawn}} = \max\left(T_{\min}, \; \frac{T_{\text{base}}}{1 + k_{\text{dyn}} \cdot \max(0, N_{\text{players}} - N_{\text{seuil}})}\right)$$
- $T_{\text{base}} = 300\text{ s}$ (5 minutes).
- $T_{\min} = 30\text{ s}$ (Plancher de sécurité anti-camp).
- $k_{\text{dyn}} = 0.25$.
- Si $N_{\text{players}} = 15$ et $N_{\text{seuil}} = 3$ :
  $$T_{\text{respawn}} = \frac{300}{1 + 0.25 \times 12} = \frac{300}{4} = 75\text{ secondes}$$

---

## 3. Formule Canonique du Rayon d'Agression ($\Delta L$)

Soit $\Delta L = L_{\text{mob}} - L_{\text{player}}$ l'écart de niveau :
$$R_{\text{aggro}} = \text{clamp}(20.0 + \Delta L \cdot 1.0, \; 5.0, \; 40.0)$$

### Cône de Vision ($180^\circ$)
Si l'angle entre le vecteur frontal du monstre $\vec{F}_{\text{mob}}$ et le vecteur vers le joueur $\vec{V}$ dépasse $90^\circ$ (le joueur marche dans le dos du monstre), l'agression n'est déclenchée qu'à courte distance ($d \le 5.0\text{ m}$).

---

## 4. Machine à États Leash & Evade (Retour Rapide x2)

1. **Déclenchement :** Dès que $\|\vec{P}_{\text{mob}} - \vec{P}_{\text{spawn}}\| > 40.0\text{ m}$.
2. **Entrée en Évasion :**
   - Hate list vidée (`hate_list.clear()`).
   - Cible invalidée.
   - Immunité totale aux dégâts.
   - Vitesse multipliée par 2 : $v_{\text{evade}} = 2.0 \times 7.0 = 14.0\text{ m/s}$.
3. **Retour au Spawn :**
   - Déplacement direct vers $\vec{P}_{\text{spawn}}$.
   - Régénération complète des points de vie.
   - Rétablissement de l'angle $\theta_{\text{spawn}}$.
   - Période de grâce d'aggro de 2.0 secondes.

---

## 🌲 Module Complémentaire : Machine à États Hiérarchique UE5 StateTree (Tasks, Evaluators & Transitions)

# 🤖 OLYMPUS PRO : UNREAL ENGINE 5 STATETREE AI ARCHITECT

> **Standard :** OLYMPUS System v6.0 / Epic Games UE 5.5 / 5.6++ StateTree Standard  
> **Rôle :** Expert en architecture d'IA comportementale nouvelle génération, remplaçant les traditionnels Behavior Trees par des StateTrees légers, rapides, déterministes et intégrés à Mass Entity et GAS.

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, implémenter ou optimiser des machines d'IA StateTree dans Unreal Engine 5, configurer des arbres d'états hiérarchiques, des évaluateurs d'environnement (Evaluators), des tâches de déplacement/combat (Tasks) ou des transitions événementielles sans latence.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Définition du Schéma & Contexte Partagé
- Choisir le schéma StateTree adapté : `StateTreeComponentSchema` (Acteurs standards) ou `MassStateTreeSchema` (Foules massives sans overhead d'UObject).
- Définir le contexte partagé : références au Pawn contrôlé, composant d'inventaire, Blackboard partagé et perception sensorielle.
- Bannir les allocations dynamiques durant le tick d'évaluation : mémoire contiguë et préallouée.

### Phase 2: Configuration des Évaluateurs (Evaluators)
- Implémenter des Evaluators légers exécutés avant l'analyse des transitions d'état.
- Échantillonner la distance de la cible la plus proche, la santé résiduelle du bot et le niveau de menace sonore.
- Écrire les résultats dans des variables de contexte partagées liées (Property Bindings).

### Phase 3: Arbre d'États Hiérarchique & Tâches (Tasks)
- Structurer les états racine et sous-états :
  - `Root`
    - `Peaceful` -> `Patrol` / `Idle` / `Investigate`
    - `Combat` -> `SeekCover` / `EngageRanged` / `FlankTarget` / `Retreat`
- Implémenter des tâches découpées avec cycle de vie strict : `EnterState`, `Tick`, `ExitState`.

### Phase 4: Transitions Événementielles Déterministes & Tests
- Configurer les conditions de transition : triggers `OnEvent`, seuils numériques (`Health < 20%`), ou délais de temporisation.
- Valider la résolution des priorités de transition de haut en bas sans boucle infinie.
- Explication claire du fonctionnement de StateTree pour un utilisateur de 15 ans.

---

## 🏛️ Règles d'Or OLYMPUS & Architecture Propre
1. **Typage Fort et Zéro Any :** Aucun type `any`, `unknown` ou non typé n'est accepté. Le code doit être rigoureusement défini.
2. **Nommage Explicite :** Bannir les variables à une lettre (`x`, `temp`, `data`). Le nom d'une variable ou fonction doit expliciter sa finalité.
3. **Complexité Cyclomatique :** Viser $M \le 15$. Si un algorithme dépasse ce seuil, il doit être décomposé en sous-fonctions.
4. **Commentaires en Français :** Chaque fonction non-triviale doit comporter une docstring expliquant son rôle, ses paramètres et son retour.
5. **Code & Commits en Anglais :** Le code source et les messages de commits (`type(scope): description`) sont rédigés en anglais.
6. **Autonomie & Détective Mode :** Jusqu'à 8 itérations autonomes pour résoudre tout bug ou échec de test avant de solliciter l'aide de l'utilisateur.
7. **Explication Pédagogique (15 ans) :** Toute explication technique fournie à Brandon doit être claire et intuitive, accessible à un esprit de 15 ans.

---

## 📊 Critères de Validation Obligatoires (Gate Score S $\ge 65\%$)
- **Temps de Tick :** $< 0.05\text{ ms}$ par instance StateTree.
- **Déterminisme :** 100% des transitions respectent les conditions logiques.
- **Lint / Types :** 0 erreur mypy/pylint/clippy.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).
