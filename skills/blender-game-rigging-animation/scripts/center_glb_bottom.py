"""Re-origin GLB files to the BOTTOM-CENTER of their bounding box, via Blender (bpy).

For each .glb/.gltf in the input dir:
  - import into a clean scene
  - compute the combined world-space bounding box over all meshes
  - shift the whole asset so the bbox bottom-center (centre X/Y, min Z) sits at the
    file origin (0,0,0) -> in Unreal the pivot lands at the bottom-center, so the
    asset drops straight onto the ground
  - export back to GLB into the output dir (originals are left untouched)

Run (headless):
  blender --background --python center_glb_bottom.py -- <in_dir> <out_dir>
"""
import bpy
import sys
import os
import glob
from mathutils import Vector

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []
if len(argv) < 2:
    print("USAGE: blender --background --python center_glb_bottom.py -- <in_dir> <out_dir>")
    sys.exit(1)

in_dir, out_dir = argv[0], argv[1]
os.makedirs(out_dir, exist_ok=True)


def process(path_in, path_out):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=path_in)
    except Exception as e:
        print("  IMPORT FAIL:", e)
        return "fail"

    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        return "nomesh"

    mins = [1e18, 1e18, 1e18]
    maxs = [-1e18, -1e18, -1e18]
    for o in meshes:
        mw = o.matrix_world
        for corner in o.bound_box:
            w = mw @ Vector(corner)
            for i in range(3):
                if w[i] < mins[i]:
                    mins[i] = w[i]
                if w[i] > maxs[i]:
                    maxs[i] = w[i]

    bottom_center = Vector(((mins[0] + maxs[0]) / 2.0,
                            (mins[1] + maxs[1]) / 2.0,
                            mins[2]))

    # Shift every root object by -bottom_center (children follow their parents),
    # so the whole asset moves as one and the bbox bottom-center lands at (0,0,0).
    for o in bpy.context.scene.objects:
        if o.parent is None:
            m = o.matrix_world.copy()
            m.translation = m.translation - bottom_center
            o.matrix_world = m
    bpy.context.view_layer.update()

    bpy.ops.export_scene.gltf(filepath=path_out, export_format="GLB", use_selection=False)
    return "ok"


files = sorted(glob.glob(os.path.join(in_dir, "*.glb")) +
               glob.glob(os.path.join(in_dir, "*.gltf")))
print("FOUND", len(files), "files")
ok = 0
for f in files:
    base = os.path.basename(f)
    if base.lower().endswith(".gltf"):
        base = base[:-5] + ".glb"
    out = os.path.join(out_dir, base)
    r = process(f, out)
    print(f"[{r}] {os.path.basename(f)}")
    if r == "ok":
        ok += 1
print(f"DONE {ok}/{len(files)} re-origined -> {out_dir}")
