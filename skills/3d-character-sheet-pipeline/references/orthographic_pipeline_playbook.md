# 🎨 Orthographic 3D Character Reference Playbook

This reference provides the mechanical standards, joint angles, seam discipline, and model routing parameters required to turn 2D character concept art into game-ready 3D modular assets.

---

## 1. Anatomy of the Strict-Front A-Pose

To allow automated skeletal rigging (Mixamo, Unreal Engine Control Rig, Unity Humanoid Avatar), the reference character must strictly adhere to the following spatial posture:

```
          [Head: Neutral, No Tilt]
                     |
       /----[Shoulders: Level]----\
      /                            \
     / (Arms at 45° angle)          \
    /                                \
  [Hands: Palms Forward]          [Hands]
         \                  /
          \----[Hips]------/
           |              |
           | (Legs straight)
           |              |
       [Feet: Shoulder Width, Pointing Dead-Front]
```

### Critical Angles
1. **Shoulder/Arm Angle**: $45^\circ$ down from horizontal. Never a T-pose (T-poses stretch shoulder deltoid textures during generation) and never resting at sides (arms clip through hips).
2. **Elbow Hinge**: $5^\circ$ subtle forward bend. This defines the pole-vector direction for two-bone Inverse Kinematic (IK) solvers.
3. **Leg Stance**: Parallel, vertical, separated by exactly shoulder width. Feet flat on the ground plane, toes pointing dead-on to camera.
4. **Facial Expression**: Completely neutral mouth closed, eyes level. No smirk, wink, or head tilt.

---

## 2. Modular Seam Alignment Discipline

When extracting modular equipment (armor, boots, gauntlets, pauldrons, helmets), seams must align to predefined anatomical anchor planes:

| Modular Part | Primary Seam Anchor Plane | Extraction Rule |
|---|---|---|
| **Head & Face** | Neck Base ($C_7$ vertebra level) | Extract with neck collar intact. No hair flowing over chest. |
| **Hair** | Scalp hairline | Isolated front silhouette with soft alpha edges. Generated floating above empty skull volume. |
| **Torso Armor** | Clavicle (top), Iliac crest (bottom) | Sleeveless or short-capped. Pauldrons and cape extracted separately. |
| **Gauntlets / Hands** | Wrist joint ($2\text{cm}$ above styloid process) | Generated as close-crop pair, palms facing camera. |
| **Boots / Footwear** | Mid-calf or knee joint | Both boots side-by-side, dead front, sole flat to baseline. |
| **Weapons / Shields** | Floating isolated, blade-on | Never held in hands. Weapon handles aligned vertically. |

---

## 3. Downstream 3D Engine Routing & Decimation Matrix

| Target Platform | Polygon Budget (Character + Gear) | Recommended Model | Generation Flags |
|---|---|---|---|
| **Unreal Engine 5 (Nanite Desktop)** | 40,000 – 60,000 tris | `tripo_h3_1_image_to_3d` | `geometry_quality: detailed`, `texture_quality: detailed`, `texture_alignment: original_image` |
| **Unity (Mobile / WebGL / VR)** | 12,000 – 20,000 tris | `tripo_h3_1_image_to_3d` + Blender Decimate | `face_limit: 15000`, `texture_quality: standard` |
| **Modular Props & Weapons** | 4,000 – 8,000 tris | `tripo3d/p1/image-to-3d` | `texture: true`, `face_limit: 8000` |
| **Tiling PBR Terrain & Surfaces** | N/A (Texture Maps) | `fal-ai/patina/material` | `maps: [basecolor, normal, roughness, metalness, height]` |

---

## 4. Blender Pre-Rigging Post-Processing

Before passing raw GLB meshes to Mixamo or Unreal Engine:
1. **Re-center Pivot to Floor**: Run `center_glb_bottom.py` so the root origin $(0, 0, 0)$ sits on the floor between the heels.
2. **Remove Non-Manifold Geometry**: Clean zero-area faces and internal floating loose vertices.
3. **Rest Pose Lean Stabilization**: AI-generated characters often exhibit a $25^\circ - 30^\circ$ backward lean in the spine. Apply an inverse rotational offset on the root bone before baking animation cycles.
