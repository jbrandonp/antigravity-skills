---
name: autonomous-game-slice-director
description: >-
  Architect and orchestrate long-running autonomous game development marathons (24h-48h). Enforces greybox-first MVP in <2.5h, disk-backed compaction survival (PLAN/PROGRESS/REPORT), world-space outcome probes vs naive logs, compile race prevention, ACES camera grading, minimap static baking, shader keep-alive guards, and automated asset storage cleanup based on the World of Oldcraft 36h autonomous MMO post-mortem.
---

# 🎮 Autonomous Game Slice Director & Long-Run Marathon Harness (SOTA 2026)

> **Inspirations & Provenance :** World of Oldcraft 36h Autonomous MMO Build (September 2026, 7.85B tokens, full 3D playable slice in Unity/Blender), Boris Cherny (*Claude Code Long-Run Harness*), Overlord 3D Engine Architecture.  
> **Core Axiom :** *"Art is cheap; tokens and context compactions are expensive. A game that does not play as a greybox in 2 hours will not play as a finished world in 36 hours."*

---

## 🎯 Purpose & Scope

Building a playable 3D game slice autonomously (MMO, Action RPG, Shooter) is fundamentally different from building a web app or CLI tool. 
An agent running for 12, 24, or 48 hours faces catastrophic failure modes:
1. **Context Compaction Amnesia**: As context limits compact over millions of tokens, memory of unfinished features and architecture vanishes unless pinned to disk.
2. **Compile Race Desync**: Editing engine scripts while Play Mode runs forces domain reloads, erasing singletons and freezing bridge sockets.
3. **The False-Success Trap**: A green test suite and clean console log can hide broken games (towers that never acquire targets, characters hovering 2m in the air, or ships floating above water).
4. **Performance Collapse**: Minimap cameras re-rendering scenes, unbaked lighting, and texture memory leaks can degrade framerates from 90 FPS down to 15 FPS.
5. **Disk Exhaustion**: Generating hundreds of intermediate 3D meshes and raw textures fills SSDs, triggering silent editor crashes.

This skill codifies the hard-won architecture and rules to run autonomous game-building marathons successfully.

---

## 🏗️ 1. The 5-Phase Marathon Roadmap

```
[Phase 1: Greybox Loop] ──> [Phase 2: Roster & Rigs] ──> [Phase 3: World & Environment]
     (<2h 30m, Primitives)       (Mixamo + Blender)           (Terrain, Town, Props)
                                                                       │
                                                                       ▼
[Phase 5: Release Build] ◄── [Phase 4: Combat & Quests] ◄──────────────┘
  (Shader Keep-Alives,         (Threat, Attack Tables,
   WorldWarmup, 60+ FPS)        Bag Loot, Quest DAG)
```

### Phase 1: Greybox First (Mandatory <2h 30m)
Never generate art, sculpt terrain, or download animations until the core loop is playable with primitive shapes (capsules, cubes):
- Player spawn & basic movement.
- Target selection & dummy enemy.
- 1 functional quest with pickup / kill counter.
- Basic uGUI HUD (health bar, target frame, action button).
- If the game loop is fun with capsules, it will be exceptional with art.

### Phase 2: Roster & Skeleton Standardization
- Deploy a unified `mixamorig:` skeleton hierarchy across all character races.
- Ground pivots via `center_glb_bottom.py`.
- Acquire core clips via `download_mixamo.py` and enforce T-pose reference avatars to prevent the 25°–30° lean back flaw.

### Phase 3: World Dressing & NavMesh Integrity
- Carve terrain and roads.
- **Tree Collider Rule**: Give trees *no* physical capsule colliders if they punch jagged holes in the NavMesh; use obstacle volumes or kinematic triggers.
- Re-bake NavMesh after any terrain or static geometry modification.

### Phase 4: Combat Systems & MMO Logic
- Tab-targeting raycasts, threat (hate list), 8-tier faction matrix.
- Offline bot state machines (never call live LLMs for background NPC banter during gameplay; use an offline pre-generated phrase bank).

### Phase 5: Polish & Build Resilience
- Run `WorldWarmup` routines to pre-render key vistas behind loading screens.
- Keep-alive materials to prevent shader stripping in final builds.

---

## 💾 2. Compaction Survival: The Tri-File Disk Anchor

During a 24h-48h marathon, the agent will experience dozens of context compactions. **Never rely on conversation context for project state.**

Maintain three disk-anchored files updated atomically:

### `PLAN.md` (Strategic Milestones)
High-level roadmap with strict checkboxes and status tiers:
- `[PROPOSED]`
- `[IMPLEMENTED_NOT_VERIFIED]`
- `[AGENT_VERIFIED]`
- `[OWNER_CONFIRMED]` (Only the human user can advance a task to this status).

### `PROGRESS.md` (Append-Only Chronological Ledger)
Every action, tool call result, and git commit is appended with ISO UTC timestamps:
```markdown
### 2026-10-24T12:00:00Z | M2 Character Roster Completed
- Fitted mixamorig skeleton to Dwarf and Orc meshes.
- Executed center_glb_bottom.py on 14 weapon GLBs.
- Verified gait probe: lateral walk skate measured at 1.8 deg (PASS <= 6 deg).
- Git checkpoint: commit 4e2f89a 'feat(roster): standardize dwarf and orc rigs'
```

### `REPORT.md` (Defect Matrix & Active Metrics)
Living document listing active bugs, performance FPS benchmarks, memory usage, and outstanding verifications.

---

## 👁️ 3. World-Space Outcome Probes (Beyond Naive Assertions)

In 3D games, local transforms and clean logs deceive. Implement a `VerificationDriver` that executes real world-space probes:

```csharp
// Example Unity/Unreal World-Space Probe Rule
public void AssertActorGrounded(GameObject actor)
{
    RaycastHit hit;
    if (Physics.Raycast(actor.transform.position + Vector3.up * 1f, Vector3.down, out hit, 5f))
    {
        float delta = Mathf.Abs(actor.transform.position.y - hit.point.y);
        // Assert actor is not hovering (>0.05m) or subterranean (<-0.05m)
        if (delta > 0.05f) {
            RecordProbeFailure($"Actor {actor.name} is floating {delta:F2}m above terrain!");
        }
    }
}
```

### Mandatory Verification Fixtures
1. **Grounding Probe**: Raycast down from actor pivots to confirm contact with terrain (detects bridge hover bugs).
2. **Gait Angle Probe**: Measure true translation vector vs actor forward vector (detects walk skating $>6^\circ$).
3. **Foot Sliding Clamp**: Track foot bone world translation during stance phase ($v_{\text{foot}} < 0.02\text{ m/s}$).
4. **Combat Resolution Probe**: Verify enemy HP decreases and loot drops into player bag upon death.
5. **End-to-End Bot Run**: Scripted bot plays through character selection, accepts a quest, travels to a marker, kills a mob, and turns in the quest.

---

## ⚡ 4. Preventing Engine Compile Races

Editing scripts while an engine editor is executing is the #1 cause of lost agent progress:
1. **Always Stop Play Mode**: Stop Play mode before editing scripts, updating prefabs, or modifying scene files.
2. **Trigger Compilation Explicitly**: Call project refresh / compile.
3. **Poll Until Idle**: Poll `isCompiling == false` and check compilation errors before re-entering Play mode.
4. **Non-Serialized Transient State**: Mark runtime debug lists and cached references `[System.NonSerialized]` so domain reloads do not serialize corrupted null references.

---

## 🎨 5. Camera Visual Grading & Color Cohesion

To prevent generative 3D assets from looking disconnected, apply a unified post-processing color grade:
- **Tonemapper**: ACES with $+1.05\text{ EV}$ exposure compensation.
- **Color Balance**: Cool blue/cyan shadows, warm amber highlights.
- **Contrast & Saturation**: Moderate contrast (6–8), subtle saturation boost (10–12). Never oversaturate.
- **Ambient Lighting**: Trilight ambient setup (Sky: `0.55, 0.59, 0.66`, Equator: `0.40, 0.43, 0.44`, Ground: `0.25, 0.28, 0.26`).
- **Fog Layering**: Exponential-squared ($\text{Exp}^2$) distance fog with atmospheric perspective tint (`0.40, 0.48, 0.58`).
- **SSAO**: Screen-Space Ambient Occlusion sampled from Depth buffer (avoids normal artifacts on low-poly meshes).
- **Bloom**: Keep disabled or clamped to low intensity to avoid blinding specular halos.
- **Verification Rule**: Always judge visual balance in **Game View** through the gameplay camera at standard player distance—never in Blender or orthographic scene view.

---

## 🚀 6. Performance & Build Hardening

### Minimap 2D Texture Baking
- **The Trap**: Placing a real-time overhead camera rendering the entire world into a RenderTexture cuts FPS in half (e.g. 84 FPS $\to$ 35 FPS).
- **The Solution**: Render the entire zone once from top-down into a static $4096 \times 4096$ PNG texture map, and pan/crop this 2D sprite inside the UI HUD. Restores 60+ FPS immediately.

### WorldWarmup Pre-Rendering
- **The Trap**: First-time camera entry into a densely dressed town causes 200ms+ stutter as meshes and shaders upload to GPU memory.
- **The Solution**: Execute a `WorldWarmup` script during the loading screen that cycles the camera through 8–12 key world vista positions for 1 frame each before unlocking player controls.

### Shader Keep-Alive Stripping Guards
- **The Trap**: Standalone game builds crash on startup with missing shader errors because engines strip shaders that are only referenced dynamically in code.
- **The Solution**: Maintain an explicit `KeepAliveMaterials` asset in a preload folder holding direct serialized references to all materials and shaders used by generative assets.

### Asset Cleanup & Disk Watchdog
- Set up an automated check removing intermediate GLB decimation files, failed generation takes, and old LFS history when disk space drops below 15 GB.

---

## 🔗 Related Skills in Antigravity
- [`3d-character-sheet-pipeline`](../3d-character-sheet-pipeline/SKILL.md): Supplies 2D-to-3D reference assets.
- [`blender-game-rigging-animation`](../blender-game-rigging-animation/SKILL.md): Headless Blender pipeline and pivot grounding.
- [`mixamo-animation-library-engine`](../mixamo-animation-library-engine/SKILL.md): Supplies verified locomotion and combat animations.
- [`loopcraft-harness-engineer`](../loopcraft-harness-engineer/SKILL.md): Governs general code self-healing loops and ISO 25010 Quality Gates.
- **Zero-Stutter Performance Architecture**: See `./references/world-warmup-minimap.md` for WorldWarmup C# driver, static minimap UV projections, and shader keep-alive stripping guards.
