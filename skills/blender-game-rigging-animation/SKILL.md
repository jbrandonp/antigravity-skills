---
name: blender-game-rigging-animation
description: >-
  Automate Blender headless rigging, skinning, bone roll stabilization, animation baking, and FBX export for Unreal Engine 5 and Unity. Solves generative 3D pivot misalignment (center_glb_bottom.py), Mixamo rest-pose lean back (25-30°), walk cycle skating (20-37° drift), foot sliding (reducing 6.9cm slide to 0.02cm), quadruped two-bone IK rigging, and certified engine export standards.
---

# 🦴 Blender Game Rigging & Animation Pipeline (SOTA 2026)

> **Inspirations & Provenance :** World of Oldcraft 36h Autonomous MMO Slice, Overlord 3D Engine Production Pipeline, Blender bpy Automation Standards.  
> **Core Axiom :** *"Rig failures frequently masquerade as weight failures. Fix bone rolls, rest pose T-pose alignment, and pivot origins before painting weights."*

---

## 🎯 Purpose & Production Bottlenecks Solved

Generative AI 3D meshes (Tripo, Hunyuan, Rodin, Meshy) and public animation archives (Mixamo) suffer from critical pipeline flaws when imported into game engines:
1. **Floating / Misaligned Pivots**: Mesh origins sit at the bounding box centroid or in empty space, causing props and characters to float or bury into terrain.
2. **Rest Pose Lean Back (25°–30°)**: Mixamo clips store an arbitrary animation keyframe as their rest pose rather than a true T-pose, causing characters to lean back and float when running.
3. **Walk Skate Drift (20°–37°)**: Raw locomotion clips drift laterally during forward movement, breaking character headings.
4. **Foot Sliding (6.9 cm down to 0.02 cm)**: Standing and idle loops slide across the floor due to unbaked root weight shifts.
5. **Opposite-Limb Weight Bleed**: Automatic heat weighting causes left leg bones to influence right leg vertices and jaw bones to stretch chests.

This skill provides headless Blender scripts, skinning rules, and export configurations to eliminate these flaws deterministically.

---

## 📐 1. Pivot Grounding: Bounding Box Bottom-Center

Raw GLB/glTF exports must have their origin shifted to **Bottom-Center** $(X_{\text{mid}}, Y_{\text{mid}}, Z_{\text{min}})$ so they snap cleanly to terrain and physics colliders.

### Headless CLI Execution
```powershell
blender --background --factory-startup --python scripts/center_glb_bottom.py -- <input_folder> <output_folder>
```

### Core Transformation Logic (`scripts/center_glb_bottom.py`)
```python
import bpy
from mathutils import Vector

# 1. Compute combined world-space bounding box
mins = [1e18, 1e18, 1e18]
maxs = [-1e18, -1e18, -1e18]
for o in [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]:
    mw = o.matrix_world
    for corner in o.bound_box:
        w = mw @ Vector(corner)
        for i in range(3):
            mins[i] = min(mins[i], w[i])
            maxs[i] = max(maxs[i], w[i])

# 2. Vector to bottom-center
bottom_center = Vector(((mins[0] + maxs[0]) / 2.0, (mins[1] + maxs[1]) / 2.0, mins[2]))

# 3. Shift root objects so bottom-center lands at (0, 0, 0)
for o in bpy.context.scene.objects:
    if o.parent is None:
        m = o.matrix_world.copy()
        m.translation = m.translation - bottom_center
        o.matrix_world = m

bpy.context.view_layer.update()
bpy.ops.export_scene.gltf(filepath=path_out, export_format="GLB", use_selection=False)
```

---

## 🦴 2. Skeletons, Skinning & Weight Pruning

### Standard `mixamorig:` Hierarchy
Maintain identical bone names and hierarchy across all character races (Human, Dwarf, Orc, Elf) to share animation clips:
- `mixamorig:Hips` (Root Motion anchor, key neutral defaults)
- `mixamorig:Spine` -> `Spine1` -> `Spine2` -> `Neck` -> `Head`
- `mixamorig:LeftShoulder` -> `LeftArm` -> `LeftForeArm` -> `LeftHand`
- `mixamorig:LeftUpLeg` -> `LeftLeg` -> `LeftFoot` -> `LeftToeBase`

### Weighting Best Practices
1. **Automatic Weights are Initial Only**: Always clean loose geometry islands (teeth, pauldrons, belt buckles, eyeballs) by parenting them as rigid bone children or painting 100% weight to their dedicated bone.
2. **Prevent Opposite-Limb Leakage**: Box-select left limbs and explicitly zero out all `mixamorig:Right*` vertex groups before smoothing.
3. **Prune & Normalize Influences**:
   - Game engines (UE5 and Unity) strictly enforce **maximum 4 bone influences per vertex**.
   - In Blender: `Mesh -> Weights -> Limit Total (limit=4)` followed by `Mesh -> Weights -> Normalize All`.

---

## 🏃 3. The Big 3 Animation Fixes (World of Oldcraft Lessons)

### Problem A: Rest Pose Lean Back (25°–30°)
- **Root Cause**: Mixamo animation FBXs store frame 0 of the animation as the bind pose. When retargeted, the engine applies the difference between this pose and the target avatar, causing characters to run leaning backward.
- **Fix**: Enforce a single canonical **T-Pose Reference Avatar** for all clips. In Blender, snap arm rolls to horizontal $(0, 0, 0)$ roll, level hips, and export an explicit reference bind pose before retargeting animations.

### Problem B: Walk Cycle Skating (20°–37°)
- **Root Cause**: Many standard walk clips have subtle lateral hip motion that rotates the forward vector away from $(0, 1, 0)$.
- **Fix**: Run a **Gait Probe**:
  1. Measure root velocity heading vector over one complete stride cycle: $\theta = \text{atan2}(v_x, v_y)$.
  2. If $|\theta| > 6^\circ$, counter-rotate the root bone per frame by $-\theta \cdot \frac{t}{T_{\text{stride}}}$ in Blender NLA editor before baking.
  3. Keep foot trajectory within $\pm 6^\circ$ of the true forward axis.

### Problem C: Foot Sliding in Idle Loops (6.9 cm -> 0.02 cm)
- **Root Cause**: Breathing or shifting idle loops slightly shift the root bone position in $X/Y$, dragging planted feet along the floor.
- **Fix (Two-Tier Approach)**:
  1. *Blender Bake*: Pin the supporting foot bone translation curves to constant values during contact intervals ($v_{\text{foot}} = 0$).
  2. *Runtime Foot Lock*: In game code / engine animation blueprint, sample ground contact with a raycast. If velocity $< 0.1\text{ m/s}$, clamp foot IK target coordinates to the initial floor contact point until locomotion resumes.

---

## 🐺 4. Quadruped Rigging (Canines, Felines, Beasts)

Ground quadrupeds (wolves, boars, bears) cannot reuse humanoid skeletons:
- **Digitigrade Leg Topology**: Distinct Thigh, Shin, Hock, and Paw.
- **Two-Bone IK + Hock Helper**: Setup a two-bone IK chain from Thigh to Shin targeting a Hock helper bone, which in turn resolves to the Paw ground controller.
- **9-Clip Minimum Quadruped Set**:
  - `Idle`, `Idle Look Left/Right`, `Walk`, `Run`, `Bite/Attack1`, `Leap/Attack2`, `Hit Reaction`, `Death`.
- **Root Motion Rule**: Keep Root Motion **OFF** in action RPGs and MMOs. Game physics code owns actor translation and yaw; animation playback rate is driven dynamically by ground velocity $\nu = \frac{\Delta d}{\Delta t}$.

---

## 📤 5. Certified Engine FBX Export Standards

Always use headless Blender export with exact coordinate systems (Blender $+Z$ up, $-Y$ forward $\to$ Unreal Engine $+Z$ up, $+X$ forward / Unity $+Y$ up, $+Z$ forward).

### Character Skeletal Mesh & Animation FBX Export
```python
bpy.ops.export_scene.fbx(
    filepath=out_fbx_path,
    check_existing=False,
    use_selection=True,
    global_scale=1.0,
    apply_scale_options='FBX_SCALE_UNITS',
    axis_forward='-Z',
    axis_up='Y',
    apply_unit_scale=True,
    bake_space_transform=False,
    object_types={'ARMATURE', 'MESH'},
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    add_leaf_bones=False,               # CRITICAL: Leaf bones pollute game skeletons
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    armature_nodetype='NULL',
    bake_anim=True,
    bake_anim_use_all_actions=True,      # Export all NLA actions
    bake_anim_use_nla_strips=False,
    bake_anim_use_step=True,
    bake_anim_step=1.0,
    bake_anim_simplify_factor=0.0,       # Never simplify curves (destroys foot contacts)
    bake_anim_force_startend_keying=True,
    path_mode='RELATIVE'
)
```

### Static Prop FBX Export
```python
bpy.ops.export_scene.fbx(
    filepath=out_prop_path,
    use_selection=True,
    global_scale=1.0,
    apply_scale_options='FBX_SCALE_ALL',
    bake_space_transform=True,
    axis_forward='-Z',
    axis_up='Y',
    object_types={'MESH'},
    mesh_smooth_type='FACE',
    bake_anim=False
)
```

---

## 📚 Reference Documentation
For detailed worked examples from production, see [`references/blender-game-animation-lessons.md`](references/blender-game-animation-lessons.md).
