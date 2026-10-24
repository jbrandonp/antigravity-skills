---
name: mmo-tab-target-combat-pipeline
description: World of Warcraft style MMORPG Engine. Covers Tab-Targeting combat, single-roll attack tables (Miss/Dodge/Parry/Block/Crit), Threat & Hate List (110% melee / 130% ranged), Quest DAG prerequisite engines, NPC Gossip dialogue trees, 8-tier faction reputation matrices, and MMORPG Head-Up Display (portrait frames, radial cooldown action bars, dynamic threat nameplates, floating combat text).
---



# ⚔️ Universal Combat Pipeline: Tab-Targeting, Threat & Frame-Precision (SOTA 2026)

> **Inspirations & Provenance :** World of Warcraft Combat Standard (TrinityCore / Mangos), Street Fighter 6 Frame-Data Standards, Unreal Engine 5 Gameplay Ability System & Motion Matching.  
> **Core Axiom :** *"A single physical or spell strike must resolve deterministically through an ordered single-roll table, respect strict frame data windows, and update multi-agent threat matrices with hysteresis."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine un combat épique dans World of Warcraft entre un Guerrier, un Mage et un Boss dragon :
1. **Le Cône de Vision et le Tab-Target** :
   Quand tu appuies sur Tab, le jeu ne choisit pas un monstre au hasard dans ton dos. Il trace un cône de vision devant toi ($120^\circ$) et sélectionne l'ennemi le plus dangereux à portée.
2. **Le Tirage Unique (The Single-Roll Attack Table)** :
   Quand tu donnes un coup d'épée, le jeu ne lance pas 10 dés différents. Il lance un seul dé à 10 000 faces (de 0 à 100.00%). Les tranches sont disposées sur une ligne : d'abord le Raté, puis l'Esquive du monstre, sa Parade, son Blocage, ton Coup Critique, et enfin le Coup Normal. Si le monstre a 30% d'esquive et que ton dé tombe dans sa tranche, ton coup est esquivé en un seul calcul ultra-rapide.
3. **Le Refoulement de Sort (Spell Pushback)** :
   Pendant qu'un Mage incante une boule de feu de 3 secondes, chaque baffe reçue repousse sa barre de 0.5 seconde. Pour éviter qu'un joueur ne reste coincé à l'infini, le jeu bloque à 2 pushbacks maximum : le sort partira coûte que coûte !
4. **La Menace et l'Aggro (Hate List)** :
   Le boss attaque le joueur qu'il déteste le plus (celui avec le plus de "Threat"). Pour lui voler l'aggro au corps-à-corps, tu dois dépasser la menace du Tank de **110%**. Si tu tires à l'arc à distance, tu dois atteindre **130%** avant que le boss ne se retourne contre toi.
5. **La Provocation du Tank (Taunt)** :
   Quand le Tank crie sur le boss (Taunt), sa menace saute instantanément pour égaler celle du premier joueur, et le boss est forcé de le frapper pendant 3 secondes.
6. **La Précision des Frames (Hitbox & Hurtbox)** :
   Un coup d'épée n'est pas un bloc magique. Il a 3 temps :
   - *Startup* (la préparation du geste où tu es vulnérable),
   - *Active* (la lame est en l'air et blesse si elle touche la Hurtbox ennemie),
   - *Recovery* (le temps de remettre l'arme en garde, où tu peux être puni).

---

## 🎯 2. Déclenchement & Cas d'Usage
Active ce skill pour :
- Concevoir et équilibrer un système de combat RPG / MMO (résolution de coups en mêlée ou à distance).
- Implémenter la table d'attaque probabiliste classique de WoW (Single-Roll Table).
- Programmer la mécanique d'aggro, les multiplicateurs de posture de tank (+450%), les seuils 110%/130% et le reset d'évasion (*Leash/Evade*).
- Calibrer la frame data d'attaques d'action (Startup, Active, Recovery, HitStun, BlockStun, Frame Advantage).

---

## 🎲 3. Module 1 : Résolution de la Table d'Attaque & Incantations

### Cône de Vision (FOV) & Sélection Tab-Target
Calcul du score de priorité lors de l'appui sur Tab :
$$\text{Score} = \frac{\cos(\theta) + 1.0}{2.0} \times \left(1.0 - \frac{d}{d_{\text{max}}}\right)$$
Où $\theta$ est l'angle entre le vecteur avant du joueur $\mathbf{F}$ et le vecteur vers la cible $\mathbf{T}$, avec $\cos(\theta) \ge \cos(60^\circ) = 0.5$ (cône de $120^\circ$).

### Table d'Attaque Probabiliste (Single-Roll Resolution)
Chaque résultat physique occupe une tranche continue de l'intervalle $[0, 100]\%$. Un seul tirage aléatoire $r \in [0, 100)$ résout l'issue :

```
[0% ── Miss ──> Dodge ──> Parry ──> Glancing ──> Block ──> Crit ──> Crushing ──> Normal Hit ── 100%]
```

Ordre strict d'évaluation cumulative :
1. $\text{Miss} = \max(0, 5.0\% + \Delta\text{Def})$
2. $\text{Dodge} = \max(0, \text{Dodge}_{\text{target}} - \text{Expertise}_{\text{attacker}})$
3. $\text{Parry} = \max(0, \text{Parry}_{\text{target}} - \text{Expertise}_{\text{attacker}})$ (uniquement si attaquant de face, cône $180^\circ$)
4. $\text{Glancing Blow} = 24.0\%$ (uniquement sur cible de niveau supérieur $\Delta L \ge 3$)
5. $\text{Block} = \text{BlockChance}_{\text{target}}$ (réduit les dégâts du montant de blocage du bouclier)
6. $\text{Critical Strike} = \text{CritChance}_{\text{attacker}} + \Delta\text{Crit}$
7. $\text{Normal Hit} = \text{Reste de l'intervalle jusqu'à 100%}$

### Pipeline de Sorts : Global Cooldown (GCD) & Pushback
- **GCD** : Verrouillage de 1.5 s (réductible jusqu'à 1.0 s avec la Hâte) sur toutes les aptitudes instantanées.
- **Spell Pushback** : Chaque coup reçu pendant l'incantation ajoute $+0.5\text{ s}$ au temps restant.
  - Limite stricte : **Maximum 2 refoulements** par tentative d'incantation. Tout coup ultérieur n'ajoute aucun délai.

---

## 👹 4. Module 2 : Gestion de la Menace, Aggro (Hate List) & Taunt/Leash

### Accumulation de Menace
- $1\text{ Dégât direct} = 1.0\text{ Point de Menace (Threat)}$.
- $1\text{ Point de Soin effectif} = 0.5\text{ Threat}$ réparti équitablement sur tous les ennemis en combat.
- Multiplicateur Tank (Posture défensive / Forme d'ours) : $\times 4.5$ ($+350\%$ à $+450\%$).

### Hystérésis d'Aggro (Seuils 110% Mêlée / 130% Distance)
Pour éviter qu'un monstre oscille de façon erratique entre deux joueurs :
- **En mêlée** ($d \le 5\text{ m}$) : Le joueur doit accumuler $\ge 110\%$ de la menace de la cible actuelle pour prendre l'aggro :
  $$\text{Seuil}_{\text{mêlée}} = 1.10 \times \text{Threat}_{\text{current}}$$
- **À distance** ($d > 5\text{ m}$) : Le joueur doit accumuler $\ge 130\%$ de la menace :
  $$\text{Seuil}_{\text{distance}} = 1.30 \times \text{Threat}_{\text{current}}$$

### Mécanique de Provocation (Taunt)
À l'activation du sort de Provocation :
1. **Égalisation immédiate** : La menace du Tank est alignée sur la plus haute valeur de la Hate List :
   $$\text{Threat}_{\text{Tank}} = \max(\text{Threat}_{\text{all}})$$
2. **Fixation temporaire** : La cible est forcée d'attaquer le Tank pendant **3.0 secondes**, ignorant tout changement de menace durant cette fenêtre.

### Zone de Laisse & Évasion (Leash & Evade Reset)
- Si le monstre s'éloigne au-delà de son rayon de laisse ($R_{\text{leash}} = 45\text{ m}$) de son point de spawn :
  - Passage immédiat en état `Evade` (immunité totale aux dégâts et aux sorts).
  - Retour en ligne directe à son point d'origine à vitesse doublée ($\times 2.0$).
  - Régénération instantanée de 100% de ses points de vie.
  - Réinitialisation complète de sa Hate List (tous les compteurs de menace tombent à 0).

---

## 🥊 5. Module 3 : Précision Frame Data & Boîtes de Collision (Hitbox/Hurtbox)

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Startup Frames (Telegraph / Wind-up, Hurtbox vulnerable) │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Active Frames (Hitbox spawns, Deals damage & hit-stop)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Recovery Frames (Cooldown / Weapon reset, Whiff punish)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Frame Advantage (HitStun - Recovery vs BlockStun - Recov)│
 └─────────────────────────────────────────────────────────────┘
```

### Calcul de l'Avantage de Frame (Frame Advantage)
À $60\text{ FPS}$ :
- **Sur Touché (Hit)** :
  $$\text{Advantage}_{\text{hit}} = \text{HitStun} - \text{Recovery}_{\text{attacker}}$$
  *Exemple :* $18\text{ frames de HitStun} - 12\text{ frames de Recovery} = +6\text{ frames d'avantage}$. L'attaquant peut agir 6 frames avant l'adversaire (lien de combo garanti).
- **Sur Blocage (Block)** :
  $$\text{Advantage}_{\text{block}} = \text{BlockStun} - \text{Recovery}_{\text{attacker}}$$
  Si $\text{Advantage}_{\text{block}} \le -10$, l'attaque est **punissable au blocage** (l'adversaire a le temps d'amorcer une riposte rapide de 8 frames).

### Ségrégation Stricte des Calques de Collision
- **Hurtbox (Calque Vert)** : Volume corporel vulnérable du joueur ou du monstre.
- **Hitbox (Calque Rouge)** : Volume géométrique damagant instancié pendant les frames actives de l'arme ou du projectile.
- *Règle absolue* : Une Hitbox ne teste de collision qu'avec les Hurtboxes ennemies (jamais Hitbox vs Hitbox, sauf lors d'un système explicite de choc d'armes ou de parade).

---

## 🌐 6. Matrice d'Intégration Moteurs

| Moteur | Intégration Recommandée |
|---|---|
| **Unreal Engine 5** | Résolution via `UGameplayAbility` (GAS), `FGameplayEffectContext`, et animation via `Motion Matching` / `AnimNotifies` pour borner les fenêtres Startup/Active/Recovery. Menace branchée sur `UAIPerceptionComponent` et Blackboards. |
| **Unity** | Calculateur de combat C# pur, `PlayableGraph` / `Animator` avec événements d'animation pour fenêtres de Hitbox. |
| **Bevy Engine (Rust)** | Systèmes ECS dédiés (`combat_table_system`, `threat_update_system`, `frame_advance_system`). |

---

## 🛠️ 7. Outils Déterministes

Les scripts de validation et démonstration se trouvent dans `scripts/` :
```bash
# Vérifier et équilibrer la frame data et l'avantage d'une animation de combat
python scripts/calculate_frame_advantage.py --demo
```




# Universal Quest DAG, Branching Dialogue & Faction Reputation Engine

> **Standard :** OLYMPUS System v6.0 / MMORPG Narrative & Progression Engine  
> **Rôle :** Architecte du moteur de quêtes, des dialogues PNJ (Gossip) et de la progression de factions selon les règles canoniques de World of Warcraft, garantissant l'intégrité des chaînes narratives, des embranchements exclusifs et des paliers de réputation.

---

## 🌐 Universal Cross-Genre & Engine Application

This engine provides quest dependency graphs (DAG), branching dialogue trees, and multi-tier faction matrices for ANY narrative or RPG game:

| Modern System | Architecture & Workflow | Exemples de Jeux |
| :--- | :--- | :--- |
| **Yarn Spinner / Ink (Moderne 2026+)** | Scripts narratifs à embranchements avec variables de monde dynamiques et balises i18n. | *Disco Elysium, Sable, Outer Wilds* |
| **Quest State Machine DAG** | Graphe acyclique orienté validant prérequis, quêtes complétées, inventaire et réputation de faction. | *The Witcher, Cyberpunk 2077, Mass Effect* |
| **Legacy Gossip Menus (WoW 3.3.5a)** | Arbres de dialogue textuels discrets avec vérification de réputation par paliers (Haineux à Exalté). | *World of Warcraft, Runescape, MMORPGs classiques* |

---

## 🧭 1. Graphe de Dépendance de Quêtes (Quest DAG & ExclusiveGroup)

Les quêtes ne sont pas des entrées isolées, mais un graphe orienté acyclique (DAG) :
1. **Chaînes de Prérequis (`PrevQuestId`)** :
   - Une quête n'apparaît sur la carte (point d'exclamation jaune) que si toutes ses quêtes parentes sont complétées et validées.
2. **Embranchements Exclusifs (`ExclusiveGroup`)** :
   - Si deux quêtes partagent un `ExclusiveGroup < 0` (ex: allégeance Aldor vs Clairvoyants), accepter ou valider l'une annule et verrouille définitivement l'autre.
3. **Objectifs Multiples** :
   - `KILL_CREDIT` : Tuer $N$ monstres d'un `entry_id` donné.
   - `LOOT_CREDIT` : Collecter $N$ objets dans l'inventaire (avec probabilité de drop par créature).
   - `EXPLORE_AREA` : Déclencher un `AreaTrigger` dans le monde 3D.
   - `INTERACT_GAMEOBJECT` : Clic droit sur un coffre, un autel ou un drapeau.

---

## 💬 2. Moteur de Dialogue PNJ (Gossip Menu Service)

Lorsqu'un joueur clique sur un PNJ neutre ou allié :
- Le serveur évalue le contexte : classe, race, quêtes actives et palier de réputation.
- Arborescence de sous-menus :
  - Parler $\to$ Récit d'histoire (*Lore*).
  - Ouvrir la boutique du marchand (*Vendor*).
  - Afficher les trajectoires de vol (*Flight Master*).
  - Réinitialiser les talents (*Class Trainer*).
  - Proposer une quête éligible.

---

## ⭐ 3. Matrice Canonique des 8 Paliers de Réputation

World of Warcraft structure les factions en **8 paliers stricts** de points d'estime :

| Palier de Réputation | Plage de Points | Statut Vis-à-vis du Joueur | Avantage Commercial |
|---|---|---|---|
| **Hated (Haï)** | $[-42000, -6000[$ | Attaque à vue immédiate | Accès interdit |
| **Hostile** | $[-6000, -3000[$ | Attaque à vue si approche | Accès interdit |
| **Unfriendly (Inamical)** | $[-3000, 0[$ | Ne parle pas, n'attaque pas | Accès interdit |
| **Neutral (Neutre)** | $[0, 3000[$ | Quêtes de base accessibles | Prix standard (100%) |
| **Friendly (Amical)** | $[3000, 9000[$ | Débloque la plupart des quêtes | **-5% de réduction** |
| **Honored (Honoré)** | $[9000, 21000[$ | Débloque objets d'équipement | **-10% de réduction** |
| **Revered (Révéré)** | $[21000, 42000[$ | Clés de donjons héroïques | **-15% de réduction** |
| **Exalted (Exalté)** | $[42000, 43000]$ | Montures de faction & titres | **-20% de réduction** |

---

## 🛠️ 4. Script Compagnon & Démonstrateur

Le script compagnon implémente la validation du DAG de quêtes avec ExclusiveGroup, l'évaluation de menus Gossip conditionnels, et le calcul de réputation avec remises commerciales :
```bash
python scripts/benchmark_quest_gossip_engine.py
```

---

## 🎲 Module Complémentaire : Tables de Loot, Tirages Need/Greed/Pass & Récompenses

# Loot Rolling Engine & Quest DAG Architecture — Universal Multi-Genre Specification

## 🌐 Architecture Universelle (Tous Moteurs & Genres)
Ce skill régit les tables de butin et la progression des quêtes pour **tout RPG et jeu d'aventure** :
- **Action RPG & Looter Shooters** (Borderlands, Monster Hunter, Destiny 2, Path of Exile)
- **MMORPGs** (World of Warcraft, Final Fantasy XIV, The Elder Scrolls Online)
- **Jeux Narratifs & Mondes Ouverts** (The Witcher 3, Cyberpunk 2077, Baldur's Gate 3)

### 🚀 Équivalents & Standards Modernes de l'Industrie
1. **Graphe de Dépendance de Quêtes (DAG)** : Modélisation des prérequis de quêtes par un graphe orienté acyclique garantissant l'absence de boucles infinies.
2. **Distribution de Butin Pseudo-Aléatoire (PRD)** : Algorithme avec protection contre la malchance (Bad-Luck Protection) pour éviter les séries de drops frustrantes.
3. **Système de Jet de Dés Équitable** : Machine à états Need / Greed / Pass avec gestion déterministe des égalités (Roll 1-100 avec timestamp tie-breaker).
4. **Séparation Données / Moteur** : Définition des quêtes et tables de loot en JSON/YAML ou bases SQLite/PostgreSQL découplées du moteur graphique.


> **Standard :** OLYMPUS System v6.0 / World of Warcraft Loot & Quest Architecture  
> **Rôle :** Architecte du moteur d'attribution des butins de donjon/raid (Besoin / Avidité / Passer) et de la progression narrative par graphes de quêtes orientés (Quest DAG).

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, équilibrer ou implémenter les tables de drop d'objets d'un MMORPG, programmer le système de tirage au sort de groupe (Need / Greed / Pass avec dés 1-100), structurer les arbres de quêtes (objectifs de monstres tués, objets collectés, escortes), ou attribuer des récompenses d'expérience et d'inventaire.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Tables de Butin Probabilistes (Loot Tables)
- Modéliser les conteneurs de butin de monstres et boss :
  - Chaque entrée possède un taux de drop ($P \in ]0.0, 1.0]$), une quantité minimale/maximale, et des conditions d'éligibilité (ex: Quête active requise pour les objets de quête).
  - Gestion du drop garanti pour certains objets de progression de raid.

### Phase 2: Système de Tirage au Sort de Groupe (Need vs Greed)
- Ouvrir une fenêtre de tirage temporisée ($60\text{ s}$) pour chaque objet de qualité Supérieure ou Épique.
- Priorités de tirage strictes :
  $$\text{Besoin (Need)} > \text{Avidité (Greed)} > \text{Passer (Pass)}$$
- En cas d'égalité sur la priorité (ex: deux joueurs choisissent Besoin) : tirage pseudo-aléatoire déterministe d'un dé $1-100$. Le score le plus élevé remporte l'objet.

### Phase 3: Graphe d'États de Quêtes (Quest DAG)
- Modéliser les quêtes comme un graphe orienté sans cycle (DAG) : conditions de niveau, quêtes préalables requises, réputation de faction minimale.
- Gérer les objectifs multiples : `KillMonsterObjective`, `CollectItemObjective`, `DiscoverAreaObjective`.
- Transitions d'état : `Available` $\rightarrow$ `Active` $\rightarrow$ `Complete` $\rightarrow$ `Rewarded`.

### Phase 4: Attribution Atomique & Sauvegarde
- Transférer atomiquement le butin remporté dans le sac d'inventaire du joueur sans risque de duplication.
- Explication claire du système de butin et de quêtes pour un utilisateur de 15 ans.

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
- **Priorité Need > Greed :** 100% de respect des priorités de tirage.
- **DAG Quêtes :** 0 quête débloquée sans validation des prérequis.
- **Lint / Types :** 0 erreur mypy/pylint/clippy.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).




# 🖥️ Classic MMO & Action-RPG HUD and Front-End System (SOTA 2026)

> **Inspirations & Provenance :** World of Oldcraft 36h Autonomous MMO Build (September 2026, uGUI/UMG retained architecture), World of Warcraft Classic UI/HUD standard, Unreal Engine 5 CommonUI, Riot Games UI Performance Standards.  
> **Core Axiom :** *"Never rebuild scenes to swap UI. Never use IMGUI. Never update UI text on every 60 FPS tick. A great RPG UI is event-driven, pooled, packed in SpriteAtlases, and updates its dirty state at 10 Hz."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine que tu joues à World of Warcraft ou à un grand RPG d'action :
1. **Le Cadre de ton Héros (Player Frame)** :
   En haut à gauche, tu as le visage de ton personnage dans un médaillon rond, sa barre de vie verte et sa barre de mana bleue. Quand tu prends un coup, la barre ne saute pas d'un coup sec : elle glisse doucement avec une petite traînée rouge pour que tes yeux comprennent instantanément la violence du choc.
2. **La Barre d'Action (Action Bar)** :
   En bas, tu as tes 12 sorts préférés (touches 1 à 12). Quand tu lances une boule de feu, une ombre tourne en rond sur l'icône comme l'aiguille d'une horloge (*Cooldown Swipe*). Si tu es trop loin du monstre, le chiffre de la touche devient rouge vif ; et si tu n'as plus assez de mana, toute l'icône devient grisée.
3. **Le Cadre de la Cible (Target Frame)** :
   Dès que tu cliques sur un monstre, son cadre apparaît à côté du tien. Si c'est un boss terrifiant, un magnifique dragon doré entoure son portrait (*Cadre Élite*), et une barre de canalisation montre le sort qu'il prépare en temps réel.
4. **Les Chiffres qui Volent (Floating Combat Text)** :
   Quand tu frappes, les dégâts s'affichent au-dessus de la tête du monstre. Un coup normal affiche un petit chiffre blanc, mais si tu sors un **Coup Critique**, le chiffre grossit, devient jaune flamboyant et fait un petit bond rebondissant avant de disparaître !
5. **Le Menu d'Accueil Fluide (Front-End Flow)** :
   Avant de jouer, tu passes par un écran de connexion stylé (la Porte des Ténèbres qui s'anime), puis tu choisis ton personnage sur un piédestal 3D, ou tu en crées un nouveau en changeant sa race, sa classe et sa coiffure en direct, avant qu'un bel écran de chargement avec barre de progression ne te téléporte dans le monde.

---

## 🏗️ 2. Architectural Structure of the UI System

```
UI_Manager (Root Canvas / Viewport Layer)
  ├── 1. FrontEnd Layer (Z-Order: 100, toggled before game world)
  │    ├── LoginScreenWidget (Credentials, realm status, video backdrop)
  │    ├── CharacterSelectWidget (Hero carousel, 3D pedestal camera, play button)
  │    ├── CharacterCreationWidget (Race/class buttons, hair/skin sliders, live 3D preview)
  │    └── LoadingScreenWidget (Async level progress bar, zone lore splash art)
  │
  ├── 2. HUD Layer (Z-Order: 50, active during gameplay)
  │    ├── PlayerFrame (Portrait RT, Health bar, Resource bar, Level, Combat flash)
  │    ├── TargetFrame (Target Health, Buff/Debuff trays, CastBar, Elite dragon border)
  │    ├── ActionBarWidget (12 ActionSlotButtons with cooldown sweep, range tint)
  │    ├── MinimapWidget (Circular mask, player arrow, zone text, static 4096² texture)
  │    ├── QuestTrackerWidget (Active objectives, progress counters)
  │    └── ChatBoxWidget (Tabs: General, Combat, System log, input field)
  │
  └── 3. World-Space UI Layer (Z-Order: 20, projected in 3D camera view)
       ├── NameplatePool (Floating overhead bars with dynamic threat/aggro colors)
       └── FloatingCombatTextPool (Damage numbers, crit bounce, heals, dodge/parry)
```

---

## ⚔️ 3. Core Component Specifications

### A. Player & Target Unit Frames
- **Portrait Generation**:
  - *Option 1 (Static/Fast)*: Pre-rendered 2D headshot icons generated during character creation.
  - *Option 2 (Live 3D)*: Dedicated portrait camera rendering a miniature 3D head onto a $128 \times 128$ `RenderTexture`.
- **Health & Resource Interpolation**:
  - Two overlapping fill bars: immediate fill (instant feedback) + delayed ghost fill (catches up at $200\%/\text{s}$ to highlight damage taken).
  - Resource types dynamically update bar color:
    - `Mana`: Blue (`#1E88E5`)
    - `Rage`: Red (`#E53935`)
    - `Energy`: Yellow (`#FDD835`)
    - `Focus`: Orange (`#FB8C00`)
- **Elite Dragon Decoration**:
  - Ornamental golden dragon border dynamically attached when target classification is `Elite` or `Boss`.

### B. Action Bar & Cooldown Radial Sweep
Each `ActionSlot` contains:
1. **Background & Border Frame** (standard fantasy brass/stone border).
2. **Spell Icon Image** (loaded from a single shared `SpriteAtlas`).
3. **Radial Sweep Overlay**:
   - Material / Shader driven by a normalized `CooldownProgress` float ($0.0 \to 1.0$).
   - Computes radial wipe using polar coordinates: $\theta = \text{atan2}(UV_y - 0.5, UV_x - 0.5)$.
4. **Range & Resource State Evaluator**:
   - Out of range ($d > d_{\text{max}}$) $\to$ Keybind text turns red (`#FF3333`).
   - Insufficient resource $\to$ Icon material desaturated and tinted blue/grey (`#557799`).
   - On Global Cooldown (GCD) $\to$ Light clockwise shadow overlay.

### C. Overhead Nameplates & Dynamic Threat Borders
- **Projection**: Screen-space anchored above actor bounding box:
  $$\mathbf{P}_{\text{screen}} = \text{WorldToScreenPoint}(\mathbf{P}_{\text{actor}} + (0, 0, Z_{\text{head}} + 0.3))$$
- **Distance Culling**: Hidden beyond 40 meters.
- **Dynamic Threat / Aggro Colors**:
  - `Red`: Mob is targeting player / tank lost aggro.
  - `Yellow`: Threat transition ($80\% - 100\%$ threat threshold).
  - `Green`: Tank has solid aggro / safe.
  - `Grey`: Tapped by another player (no loot/XP eligibility).

### D. Pooled Floating Combat Text (FCT)
Never instantiate `GameObject` or UMG widgets per damage tick (causes GC spikes). Use an object pool of 50 reusable text elements:
- **Trajectory Physics**:
  - Normal Hit: Rises vertically at $+1.2\text{ m/s}$ and fades out over $1.0\text{s}$.
  - Critical Hit: Spawns at $1.5\times$ scale, bounces along a parabolic arc ($v_y = 3\text{ m/s}, a_y = -9.8\text{ m/s}^2$), with bright golden text.
  - Healing: Drifts slowly upward in green (`#00FF66`).
  - Miss / Dodge / Parry: Scrolls horizontally in silver-grey (`#CCCCCC`).

---

## ⚡ 4. SOTA Performance Rules (From World of Oldcraft Post-Mortem)

### 1. The Zero-IMGUI Rule
- **Never use IMGUI (`OnGUI`)**: IMGUI allocations create tens of megabytes of garbage per minute and **never appear in game camera captures or timelapse recordings**.
- Always use Retained UI: **CommonUI / UMG** in Unreal Engine 5 or **uGUI** in Unity.

### 2. 10 Hz UI Update Throttling
- Do **NOT** update strings, health texts, and cooldown counters inside per-frame `Tick()` / `Update()` (60–144 times per second).
- UI elements subscribe to gameplay events (`OnHealthChanged`, `OnResourceChanged`) or poll dirty states on a fixed timer at **10 Hz** (every 100 ms). Eliminates $90\%$ of UI CPU overhead.

### 3. SpriteAtlas Packing
- In an MMO HUD with 48 spell icons, 12 bag slots, 10 inventory slots, and portrait frames, loose individual PNGs force 150+ separate draw calls.
- Pack all UI sprites into unified $2048 \times 2048$ **SpriteAtlases** with 2px padding. Reduces HUD draw calls to **3–5 calls total**.

### 4. Static Minimap Baking (Saving 35 FPS)
- **The Disaster**: Placing a secondary 3D camera above the player rendering into a RenderTexture caused city FPS to plummet from 84 to 35.
- **The Solution**: Render the entire terrain once into a static high-res $4096 \times 4096$ texture map. In the HUD, simply offset and scale the 2D texture UV coordinates based on normalized player world position:
  $$UV_x = \frac{X_{\text{player}} - X_{\text{min}}}{X_{\text{max}} - X_{\text{min}}}, \quad UV_y = \frac{Y_{\text{player}} - Y_{\text{min}}}{Y_{\text{max}} - Y_{\text{min}}}$$

---

## 🔄 5. Complete Front-End Flow Implementation

```csharp
// Example Clean Front-End Scene Transition Controller
public class FrontEndFlowManager : MonoBehaviour
{
    public enum ScreenState { Login, CharacterSelect, CharacterCreate, Loading }

    [SerializeField] private GameObject loginPanel;
    [SerializeField] private GameObject charSelectPanel;
    [SerializeField] private GameObject charCreatePanel;
    [SerializeField] private GameObject loadingPanel;
    [SerializeField] private Slider loadingProgressBar;

    public void SwitchState(ScreenState newState)
    {
        loginPanel.SetActive(newState == ScreenState.Login);
        charSelectPanel.SetActive(newState == ScreenState.CharacterSelect);
        charCreatePanel.SetActive(newState == ScreenState.CharacterCreate);
        loadingPanel.SetActive(newState == ScreenState.Loading);
    }

    public IEnumerator LoadGameWorldAsync(string targetSceneName)
    {
        SwitchState(ScreenState.Loading);
        AsyncOperation asyncLoad = SceneManager.LoadSceneAsync(targetSceneName);
        asyncLoad.allowSceneActivation = false;

        while (!asyncLoad.isDone)
        {
            float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);
            if (loadingProgressBar != null)
                loadingProgressBar.value = progress;

            if (asyncLoad.progress >= 0.9f)
            {
                // Smooth transition, then activate scene
                yield return new WaitForSeconds(0.5f);
                asyncLoad.allowSceneActivation = true;
            }
            yield return null;
        }
    }
}
```

---

## 🔗 Related Skills in Antigravity
- [gameplay-ability-system](../gameplay-ability-system/SKILL.md): Drives spell icons, cooldown durations, and resource expenditures.
- [game-ai-behavior-tree](../game-ai-behavior-tree/SKILL.md): Drives creature patrol states, threat targets, and tactical kiting.
- [utonomous-game-slice-director](../autonomous-game-slice-director/SKILL.md): Oversees the entire autonomous integration and testing loop.
