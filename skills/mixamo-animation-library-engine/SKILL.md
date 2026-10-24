---
name: mixamo-animation-library-engine
description: >-
  Programmatic, zero-credential animation acquisition of 90+ production-ready humanoid FBX clips directly from Hugging Face (Linzhan/Mixamo-Animations-Characters). Features automated SHA-256 integrity verification, categorized core animation catalog (locomotion, 1H sword & shield, 2H greatsword, archery, magic casting, hit reactions, deaths, social emotes), and seamless integration into Unreal Engine 5 and Unity animation state machines.
---

# 🎭 Mixamo Animation Library Engine & Automated Acquisition (SOTA 2026)

> **Inspirations & Provenance :** World of Oldcraft Autonomous 36h Build Kit, Hugging Face Dataset `Linzhan/Mixamo-Animations-Characters`, Overlord Production Animation Pipeline.  
> **Core Axiom :** *"Never manually download FBX animation clips one by one through a browser. Use deterministic, SHA-256 verified programmatic acquisition with exact UUIDs."*

---

## 🎯 Purpose & Capabilities

Game developers and autonomous agents building 3D action games or MMOs constantly need standard humanoid animations (walk, run, backpedal, jump, attack combos, spell casting, hit stumbles, deaths). 
Manual acquisition through Adobe Mixamo is painful, requires interactive web logins, produces arbitrary filenames, and frequently fails in automated CI/CD pipelines.

This skill provides an automated pipeline using the public Hugging Face binary archive (`Linzhan/Mixamo-Animations-Characters`):
- **Zero Credentials Required**: Downloads official Kaydara FBX binary files directly via HTTPS.
- **Atomic & Resilient**: Downloads to `.fbx.part`, verifies SHA-256 digests, and atomically writes the final FBX.
- **Deduplicated Manifest**: Maintains `downloads.json` receipts so existing clips are never re-downloaded.
- **Curated 90-Clip Core Catalog**: Pre-mapped UUIDs across 8 gameplay categories for instant game prototyping.

---

## 📦 The 90-Clip Core Animation Catalog (`scripts/mixamo_core_set.json`)

The catalog maps exact UUIDs to character archetypes and animation state machines:

| Category | Clip Count | Key Animations & Uses |
|---|---|---|
| **1. Locomotion** | 22 clips | `Breathing Idle`, `Sword & Shield Idle`, `Walk`, `Run`, `Sprint`, `Backward Walk (Backpedal)`, `Backward Run`, `Left/Right Strafe Walk & Run`, `Jump In Place`, `Jump Forward`, `Jump Land`. |
| **2. 1H Sword & Shield** | 14 clips | `1H Slash Combo 1 & 2`, `Shield Bash`, `Shield Block Idle`, `Shield Block Impact Hit`, `1H Draw/Sheathe`. |
| **3. 2H Greatsword / Heavy** | 12 clips | `2H Combat Idle`, `2H Overhead Cleave`, `2H Whirlwind Spin`, `2H Heavy Swing Left/Right`, `2H Impact Recovery`. |
| **4. Archer & Bow Combat** | 10 clips | `Bow Combat Stance`, `Bow Draw & Aim`, `Bow Arrow Release`, `Bow Rapid Fire`, `Bow Strafe Aim Left/Right`. |
| **5. Magic Casting** | 12 clips | `Spell Cast Start (Ground)`, `Spell Channeling Loop`, `Spell Fire Forward`, `Area of Effect Burst`, `Self Buff Prayer`. |
| **6. Hits & Reactions** | 8 clips | `Hit Small Chest`, `Hit Head Left/Right`, `Heavy Stumble Backward`, `Knockdown Fall`, `Getup From Floor`. |
| **7. Deaths** | 6 clips | `Death Fall Forward`, `Death Collapse Backward`, `Death Dramatic Spin`. |
| **8. Social & Emotes** | 6 clips | `Sit On Ground`, `Sitting Idle`, `Stand Up From Ground`, `Cheer`, `Wave`, `Formal Bow`. |

---

## 💻 CLI Usage & Acquisition Commands

The acquisition script is located at [`scripts/download_mixamo.py`](scripts/download_mixamo.py).

### 1. Download a Specific Animation by UUID
```powershell
python scripts/download_mixamo.py --motion-id "c9cc6f74-b96c-11e4-a802-0aaa78deedf9" --output "Content/Animations/Mixamo"
```

### 2. Batch Download Multiple Animations
```powershell
python scripts/download_mixamo.py `
  --motion-id "c9cc6f74-b96c-11e4-a802-0aaa78deedf9" `
  --motion-id "c9cc467a-b96c-11e4-a802-0aaa78deedf9" `
  --motion-id "c9cc4740-b96c-11e4-a802-0aaa78deedf9" `
  --output "Content/Animations/Mixamo"
```

### 3. Download the Full 90-Clip Core Set via Python One-Liner
```powershell
python -c "
import json, subprocess
with open('scripts/mixamo_core_set.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
ids = [c['motion_id'] for c in data['clips']]
cmd = ['python', 'scripts/download_mixamo.py', '--output', 'Content/Animations/Mixamo']
for mid in ids:
    cmd.extend(['--motion-id', mid])
subprocess.run(cmd, check=True)
"
```

---

## 🏗️ Technical Pipeline & Engine Retargeting

### Skeletons and FBX Header Check
Every downloaded clip:
- Begins with the binary magic bytes: `Kaydara FBX Binary  \x00\x1a\x00`.
- Contains the standardized `mixamorig:` joint hierarchy at 30 frames per second.
- Is accompanied by a cryptographic SHA-256 receipt in `downloads.json`.

### Engine Integration Checklist (Unreal Engine 5 & Unity)
1. **Root Motion Setting**: Keep Root Motion **DISABLED** on gameplay locomotion clips.
   - Character heading and displacement are governed by the Character Movement Component / Kinematic Controller.
   - Animation playback rate $\alpha$ scales with actual ground speed: $\alpha = \frac{v_{\text{current}}}{v_{\text{nominal}}}$.
2. **Avatar Retargeting**:
   - In **Unreal Engine 5**: Use an **IK Rig** and **IK Retargeter** mapping the source `mixamorig:` bones to the UE5 Mannequin (`SK_Mannequin`) or custom character mesh.
   - In **Unity**: Import as `Humanoid` Avatar or use a `Generic` PlayableGraph with shared bone names.
3. **Seam Matching for Loops**:
   - Ensure the first and last frames have identical bone positions and velocities to prevent twitching in Idle, Walk, and Run loops.

---

## 🔗 Related Skills in Antigravity
- [`blender-game-rigging-animation`](../blender-game-rigging-animation/SKILL.md): Cleans and fixes rest pose lean backs, walk skating, and bakes actions.
- [`3d-character-sheet-pipeline`](../3d-character-sheet-pipeline/SKILL.md): Produces the 3D humanoid character meshes driven by these animations.
- [`kinematic-character-controller`](../kinematic-character-controller/SKILL.md): Drives character locomotion physics and Motion Matching Pose Search Databases.
