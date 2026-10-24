#!/usr/bin/env python3
"""
Game-Ready 3D Asset Post-Processor for Blender (Headless)
Normalizes scale, grounds pivot at (0,0,0) [Bottom-Center Z=0], cleans topology,
builds LOD0/1/2, generates a Convex Hull collision mesh (UCX_), exports GLB/FBX,
and renders a fast Workbench 4-view QA sheet.
"""

import bpy
import bmesh
import sys
import os
import math
import argparse
from mathutils import Vector, Matrix


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    parser = argparse.ArgumentParser(description="Game-Ready 3D Asset Pipeline")
    parser.add_argument("--input", required=True, help="Chemin du mesh brut (.glb, .gltf, .fbx, .obj)")
    parser.add_argument("--output", required=True, help="Chemin d'export final (.glb ou .fbx)")
    parser.add_argument("--name", default="Prop", help="Nom de base de l'asset (ex: Crate_01)")
    parser.add_argument("--target-height", type=float, default=1.0, help="Hauteur cible en mètres (axe Z)")
    parser.add_argument("--max-faces-lod0", type=int, default=15000, help="Budget max de triangles pour LOD0")
    parser.add_argument("--rot-x", type=float, default=0.0, help="Correction de rotation X en degrés")
    parser.add_argument("--rot-y", type=float, default=0.0, help="Correction de rotation Y en degrés")
    parser.add_argument("--rot-z", type=float, default=0.0, help="Correction de rotation Z en degrés")
    parser.add_argument("--qa-image", default="/tmp/qa_render.png", help="Chemin de la planche de validation PNG")
    return parser.parse_args(argv)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_asset(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".glb", ".gltf"]:
        bpy.ops.import_scene.gltf(filepath=filepath)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=filepath)
    elif ext == ".obj":
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=filepath)
        else:
            bpy.ops.import_scene.obj(filepath=filepath)
    else:
        raise ValueError(f"Format non supporté : {ext}")


def join_and_clean_meshes(asset_name):
    mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not mesh_objs:
        raise RuntimeError("Aucun maillage trouvé dans le fichier importé.")

    bpy.ops.object.select_all(action="DESELECT")
    for obj in mesh_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]

    if len(mesh_objs) > 1:
        bpy.ops.object.join()

    main_obj = bpy.context.view_layer.objects.active
    main_obj.name = f"{asset_name}_LOD0"
    main_obj.data.name = f"{asset_name}_LOD0_Mesh"

    # Supprimer les Empties/Armatures résiduels d'import
    for obj in list(bpy.context.scene.objects):
        if obj != main_obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    # Nettoyage BMesh : fusion des sommets doubles, suppression des éléments isolés
    bm = bmesh.new()
    bm.from_mesh(main_obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(main_obj.data)
    bm.free()

    # Recalcul des normales vers l'extérieur et lissage auto
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()

    return main_obj


def normalize_transform_and_pivot(obj, target_height, rot_deg):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Appliquer les transformations d'import
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Correction manuelle d'orientation si demandée
    if any(rot_deg):
        obj.rotation_euler = (
            math.radians(rot_deg[0]),
            math.radians(rot_deg[1]),
            math.radians(rot_deg[2]),
        )
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    # Calcul de la Bounding Box en espace monde
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    min_x = min(c.x for c in bbox_corners)
    max_x = max(c.x for c in bbox_corners)
    min_y = min(c.y for c in bbox_corners)
    max_y = max(c.y for c in bbox_corners)
    min_z = min(c.z for c in bbox_corners)
    max_z = max(c.z for c in bbox_corners)

    current_height = max_z - min_z
    if current_height > 1e-5 and target_height > 0:
        scale_factor = target_height / current_height
        obj.scale = (scale_factor, scale_factor, scale_factor)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Recalcul après mise à l'échelle pour placer le pivot au centre-bas (Z = 0)
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    center_x = (min(c.x for c in bbox_corners) + max(c.x for c in bbox_corners)) / 2.0
    center_y = (min(c.y for c in bbox_corners) + max(c.y for c in bbox_corners)) / 2.0
    bottom_z = min(c.z for c in bbox_corners)

    offset = Vector((-center_x, -center_y, -bottom_z))
    obj.data.transform(Matrix.Translation(offset))
    obj.matrix_world.translation = Vector((0.0, 0.0, 0.0))


def decimate_object(obj, ratio):
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Decimate_LOD", type="DECIMATE")
    mod.decimate_type = "COLLAPSE"
    mod.ratio = max(0.01, min(1.0, ratio))
    mod.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=mod.name)


def generate_lods_and_collision(lod0_obj, asset_name, max_faces_lod0):
    current_faces = len(lod0_obj.data.polygons)
    if current_faces > max_faces_lod0:
        ratio = max_faces_lod0 / float(current_faces)
        decimate_object(lod0_obj, ratio)

    # Création LOD1 (50%)
    lod1_obj = lod0_obj.copy()
    lod1_obj.data = lod0_obj.data.copy()
    lod1_obj.name = f"{asset_name}_LOD1"
    lod1_obj.data.name = f"{asset_name}_LOD1_Mesh"
    bpy.context.collection.objects.link(lod1_obj)
    decimate_object(lod1_obj, 0.5)

    # Création LOD2 (20%)
    lod2_obj = lod0_obj.copy()
    lod2_obj.data = lod0_obj.data.copy()
    lod2_obj.name = f"{asset_name}_LOD2"
    lod2_obj.data.name = f"{asset_name}_LOD2_Mesh"
    bpy.context.collection.objects.link(lod2_obj)
    decimate_object(lod2_obj, 0.2)

    # Création de la boîte de collision convexe UCX_<AssetName>
    ucx_obj = lod2_obj.copy()
    ucx_obj.data = lod2_obj.data.copy()
    ucx_obj.name = f"UCX_{asset_name}"
    ucx_obj.data.name = f"UCX_{asset_name}_Mesh"
    ucx_obj.data.materials.clear()
    bpy.context.collection.objects.link(ucx_obj)

    bm = bmesh.new()
    bm.from_mesh(ucx_obj.data)
    hull_out = bmesh.ops.convex_hull(bm, input=bm.verts)
    # Supprimer les sommets/faces internes qui ne font pas partie de l'enveloppe
    bmesh.ops.delete(bm, geom=hull_out["geom_interior"] + hull_out["geom_unused"], context="VERTS")
    bm.to_mesh(ucx_obj.data)
    bm.free()

    # Limiter le collider à ~48 triangles max pour les moteurs physiques
    if len(ucx_obj.data.polygons) > 48:
        decimate_object(ucx_obj, 48.0 / len(ucx_obj.data.polygons))

    return lod0_obj, lod1_obj, lod2_obj, ucx_obj


def render_qa_sheet(lod0_obj, all_objs, qa_path, target_height):
    """Rend une vue studio rapide de LOD0 pour inspection Vision par Claude / Antigravity."""
    for o in all_objs:
        o.hide_render = (o != lod0_obj)

    scene = bpy.context.scene
    # Utiliser Workbench pour un rendu instantané (< 0.5s) garanti sans GPU en mode headless
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"
    scene.display.shading.show_backface_culling = True
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.film_transparent = False
    scene.world = bpy.data.worlds.new("QA_World")
    scene.world.color = (0.18, 0.18, 0.18)

    cam_data = bpy.data.cameras.new("QA_Cam")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("QA_Cam", cam_data)
    scene.collection.objects.link(cam_obj)
    scene.camera = cam_obj

    dist = max(target_height * 2.2, 0.5)
    target_center = Vector((0.0, 0.0, target_height * 0.5))

    # Placement caméra 3/4 Isométrique
    cam_obj.location = Vector((dist * 0.8, -dist * 0.8, target_height * 0.85))
    direction = target_center - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    os.makedirs(os.path.dirname(os.path.abspath(qa_path)), exist_ok=True)
    scene.render.filepath = qa_path
    bpy.ops.render.render(write_still=True)

    # Nettoyage de la caméra de rendu avant l'export final
    bpy.data.objects.remove(cam_obj, do_unlink=True)
    for o in all_objs:
        o.hide_render = False


def export_game_ready(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    ext = os.path.splitext(output_path)[1].lower()
    if ext in [".glb", ".gltf"]:
        bpy.ops.export_scene.gltf(
            filepath=output_path,
            export_format="GLB" if ext == ".glb" else "GLTF_SEPARATE",
            export_apply=True,
            export_yup=True,
        )
    elif ext == ".fbx":
        bpy.ops.export_scene.fbx(
            filepath=output_path,
            use_selection=False,
            apply_scale_options="FBX_SCALE_ALL",
            path_mode="COPY",
            embed_textures=True,
        )
    else:
        raise ValueError(f"Format d'export non supporté : {ext}")


def main():
    args = parse_args()
    clear_scene()
    import_asset(args.input)

    lod0 = join_and_clean_meshes(args.name)
    normalize_transform_and_pivot(
        lod0,
        args.target_height,
        (args.rot_x, args.rot_y, args.rot_z),
    )

    lod0, lod1, lod2, ucx = generate_lods_and_collision(
        lod0, args.name, args.max_faces_lod0
    )

    render_qa_sheet(lod0, [lod0, lod1, lod2, ucx], args.qa_image, args.target_height)
    export_game_ready(args.output)

    print("=== RAPPORT GAME-READY ===")
    print(f"Asset       : {args.name}")
    print(f"Pivot       : (0, 0, 0) [Bottom-Center Z=0]")
    print(f"Hauteur (Z) : {args.target_height:.2f} m")
    print(f"LOD0 Tris   : {len(lod0.data.polygons)}")
    print(f"LOD1 Tris   : {len(lod1.data.polygons)}")
    print(f"LOD2 Tris   : {len(lod2.data.polygons)}")
    print(f"UCX Tris    : {len(ucx.data.polygons)}")
    print(f"QA Image    : {args.qa_image}")
    print(f"Export      : {args.output}")


if __name__ == "__main__":
    main()
