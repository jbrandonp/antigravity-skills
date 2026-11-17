---
name: ue5-metasound-procedural-audio
description: >-
  Architect and implement Unreal Engine 5 MetaSound procedural audio graphs and World of Warcraft style 3D audio spatial ambience. Sample-accurate digital signal processing (DSP), dynamic combat audio, SoundEntries relationals with weighted random variation, surface-material footstep triggers, equal-power zone crossfading, music priority stacks with combat grace periods, and ducking compressors.
---

# 🤖 OLYMPUS PRO : UNREAL ENGINE 5 METASOUND AUDIO DSP ARCHITECT

> **Standard :** OLYMPUS System v6.0 / Epic Games UE 5.5 / 5.6++ MetaSound Standard  
> **Rôle :** Expert en synthèse sonore procédurale et traitement de signal numérique (DSP) temps réel sous Unreal Engine 5, remplaçant les Sound Cues obsolètes par des graphes MetaSound à précision d'échantillon.

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, implémenter ou optimiser des graphes MetaSound dans Unreal Engine 5, générer des bruits de moteurs de véhicules procéduraux, des synthétiseurs FM/granulaires en temps réel, moduler des paramètres audio selon la vélocité ou la santé, ou programmer des filtres DSP interactifs.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Définition de l'Horloge & Traitement par Blocs (Buffer DSP)
- Configurer la fréquence d'échantillonnage de référence ($48\text{ kHz}$) et la taille de bloc audio (Audio Block Size $= 64$ échantillons $\approx 1.33\text{ ms}$).
- Gérer les entrées de contrôle : triggers d'événements `OnPlay`, paramètres scalaires normalisés ($[0.0, 1.0]$) pour le pitch, le volume et le filtre.
- Bannir les sautes de phase : utiliser des oscillateurs à phase continue sans clic à la réinitialisation.

### Phase 2: Synthèse Procédurale & Modulation (FM / Granulaire)
- Modéliser la chaîne de synthèse : oscillateurs sinusoidaux, en dents de scie ou bruit blanc filtré.
- Implémenter la modulation de fréquence (FM) ou la synthèse granulaire pour les impacts mécaniques et les régimes moteurs :
  $$y(t) = A(t) \sin\left(2\pi f_c t + I(t) \sin(2\pi f_m t)\right)$$
- Appliquer des courbes d'atténuation d'enveloppe ADSR (Attack, Decay, Sustain, Release) précises à l'échantillon près.

### Phase 3: Filtrage Numérique & Égalisation Dynamique
- Connecter des filtres biquadratiques (Biquad Filter : LowPass, HighPass, BandPass) avec contrôle de fréquence de coupure ($f_{\text{cut}}$) et de résonance ($Q$).
- Adapter le filtre passe-bas en fonction de l'occlusion acoustique (murs, obstacles détectés par raycast).
- Intégrer les bus de réverbération spatiale et de compression dynamique du master.

### Phase 4: Profiling & Optimisation CPU des Graphes Audio
- Auditer l'utilisation des voix MetaSound simultanées : budget audio global $< 5\%$ du temps frame CPU.
- Activer la virtualisation audio sur les sources distantes non perceptibles par le joueur.
- Explication claire de la synthèse audio procédurale pour un utilisateur de 15 ans.

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
- **Stabilité de Phase :** 0 distorsion ou clic de saut de phase à la modulation.
- **Budget Voix Audio :** Exécution sous $1.5\text{ ms}$ pour 32 flux DSP actifs.
- **Lint / Types :** 0 erreur mypy/pylint/clippy.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).

---

## 🎵 Module Complémentaire : Ambiance Spatiale 3D, Mixage de Zones & Compresseur de Ducking

# Universal 3D Spatial Audio, Dynamic Music & Surface Footsteps Engine

## 📌 Executive Overview
This skill provides production-grade architectural guidance and reference implementations for the 3D spatial audio, continuous zone ambience, and dynamic combat music pipeline inspired by World of Warcraft (WotLK 3.3.5a / TrinityCore / Miles Sound System specifications).

In World of Warcraft, audio is entirely data-driven: metadata tables (`SoundEntries.dbc`, `FootstepTerrainLookup.dbc`, `AreaTable.dbc`) drive weighted variation selection, surface footstep resolution, equal-power acoustic zone crossfades, ducking prioritization, and anti-flapping combat music state machines.

---

## 🌐 Universal Cross-Genre & Engine Application

This engine provides relational audio data management, weighted variation selection, surface-material footstep triggers, equal-power zone crossfading, and combat music state machines for ANY game:

| Game Genre | Concrete Application |
| :--- | :--- |
| **Stealth & Tactical Games (Hitman, MGS, Splinter Cell)** | Footsteps varying based on walking on gravel, metal walkways, water puddles, or carpets; audio cone directivity. |
| **Action & Adventure (Uncharted, Tomb Raider, Dark Souls)** | Seamless zone ambience crossfading (cos/sin equal-power), combat music kicking in with grace periods to prevent stutter. |
| **Horror Games (Resident Evil, Dead Space)** | 3D distance attenuation, sudden stinger priorities ducking ambient wind, procedural pitch/volume jitter on creature noises. |
| **FPS & Battle Royale (Apex, Counter-Strike)** | Distinct surface footstep material sounds, directional weapon fire cone attenuation, voice line ducking over explosions. |
| **MMORPGs & Open Worlds** | Continuous regional background ambiences, day/night ambient track swapping, boss encounter music priority override. |

### Engine Integration Matrix:
- **Unreal Engine 5** : Feeds MetaSounds graphs, Sound Cues, and Audio Gameplay Volumes.
- **Godot 4.x** : Controls AudioStreamPlayer3D, AudioServer bus effects, and Raycast ground material probing.
- **Bevy Engine (Rust)** : Interfaces with bevy_kira_audio or FMOD/Wwise Rust bindings.
- **Custom C++ / Python** : Pure data model driving OpenAL, MiniAudio, or SDL_mixer.

---

## 🗄️ 1. Relational Sound Schema (`SoundEntries.dbc`)

Every sound event (spell impact, footstep, UI click, creature roar, zone music) is registered with up to 10 weighted audio file variations:

```
SoundEntries.dbc Binary Record:
├── uint32 id                    -> Unique Sound Entry ID
├── uint32 sound_type            -> Category (1=Spells, 2=UI, 3=Footsteps, 4=Weapons, 19=Music, 25=Ambience)
├── string name                  -> Identifier name (e.g. SPELL_Fireball_Impact)
├── string file_paths[10]        -> Up to 10 file variants (.wav, .ogg, .mp3)
├── uint32 file_weights[10]      -> Relative stochastic weight (0..100)
├── float base_volume            -> Default volume gain (0.0..1.0)
├── uint32 flags                 -> Bitmask (0x01=3D World, 0x02=Pitch Jitter, 0x200=Looping)
├── float min_distance           -> Near-field radius in yards (100% volume, 0 attenuation)
└── float distance_cutoff        -> Far-field cutoff radius in yards (voice killed beyond this distance)
```

### Weighted Random Variation Selection:
To eliminate mechanical audio fatigue when firing rapid spells or weapon swings, a file is picked probabilistically:
$$R \in [0, \sum w_i) \implies \text{Index } k \text{ where } \sum_{i=0}^{k-1} w_i \le R < \sum_{i=0}^k w_i$$
With subtle micro-variations applied dynamically:
$$\text{PitchMultipler} = 1.0 + \mathcal{U}(-0.05, +0.05), \quad \text{GainMultiplier} = \text{BaseGain} \times 10^{\frac{\mathcal{U}(-1.0, +1.0)}{20}}$$

---

## 👣 2. Physical Footstep Engine & Terrain Material Resolution

Footsteps are triggered by animation markers (`$FTL`, `$FTR`) in M2 models and resolve against the physical ground:

1. **Fluid Test**: If feet are submerged in fluid ($Z_{\text{feet}} \le Z_{\text{water}}$), emit `FootstepWaterSplash`.
2. **Object Mesh (WMO / M2)**: If standing on an architectural polygon, query the material flag in `MOPY` (`Wood`, `Stone`, `Metal`, `Snow`).
3. **Terrain Tile (ADT)**: On ground terrain, sample the dominant alpha weight in `MCAL` and convert via `TerrainType.dbc` (`Grass`, `Dirt`, `Sand`, `Rock`, `Snow`).
4. **Lookup**: `FootstepTerrainLookup.dbc` takes `(Race/ShoeType, MaterialID)` and returns the specific `SoundEntryID`.

---

## 🌲 3. Equal-Power Zone Ambience Crossfading

When crossing from zone $A$ to zone $B$ over crossfade duration $T_{\text{crossfade}} \in [2.5\text{s}, 4.0\text{s}]$:
$$\tau = \frac{t - t_{\text{start}}}{T_{\text{crossfade}}} \in [0, 1]$$
$$\text{Gain}_A(\tau) = \cos\left(\frac{\pi}{2} \cdot \tau\right), \quad \text{Gain}_B(\tau) = \sin\left(\frac{\pi}{2} \cdot \tau\right)$$

This maintains constant perceived acoustic energy ($\text{Gain}_A^2 + \text{Gain}_B^2 = \cos^2 + \sin^2 = 1.0$), eliminating the perceived $-3\text{ dB}$ volume drop that plagues naive linear crossfades.

---

## ⚔️ 4. Dynamic Music Priority Stack & Combat Grace Period

Music playback is governed by a strict hierarchical priority stack:

```
[Priority 100] Cinematic / In-Engine Cutscene
      ▲
[Priority 80]  Raid Boss Encounter Theme
      ▲
[Priority 60]  Dynamic Combat Music Loop
      ▲
[Priority 40]  Zone Discovery Intro Fanfare
      ▲
[Priority 20]  Zone Exploration Ambient Playlist (with silent rest pauses)
```

### Anti-Flapping Combat Grace Period:
When the active threat list drops to zero upon slaying a creature, the engine does not abruptly cut combat music. It enters a **Combat Grace Period** ($5.0\text{s}$ to $8.0\text{s}$). If another monster is pulled during this grace window, the timer resets and combat music continues seamlessly. If the timer elapses with zero threat, it executes a smooth $3.0\text{s}$ crossfade back to exploration music.

---

## 🔊 5. 3D Spatial Attenuation, Directivity Cones & Ducking

### 5.1 — Clamped Inverse Distance Attenuation:
For distance $d \in [\text{MinDistance}, \text{DistanceCutoff}]$:
$$\text{Atten}(d) = \text{clamp}\left(\frac{\text{MinDistance}}{\text{MinDistance} + (d - \text{MinDistance})}, 0.0, 1.0\right)$$
Beyond $\text{DistanceCutoff}$, voice processing is culled to save CPU cycles.

### 5.2 — Directional Audio Cone:
For emitters with forward orientation (e.g. dragon breath, boss voice):
- Within inner cone angle ($\theta \le \theta_{\text{inner}}$): Attenuation $= 1.0$.
- Between inner and outer cone ($\theta_{\text{inner}} < \theta < \theta_{\text{outer}}$): Linearly drops to $\text{OuterVolumeGain}$.
- Outside outer cone ($\theta \ge \theta_{\text{outer}}$): Fixed at $\text{OuterVolumeGain}$ (e.g. $0.20$).

### 5.3 — Ducking Bus Hierarchy:
When voice lines or high-priority combat warnings trigger, background music and ambience buses are ducked by $-6\text{ dB}$ to $-12\text{ dB}$ with a $200\text{ ms}$ attack and $1000\text{ ms}$ smooth release.
