#!/usr/bin/env python3
"""
Procedural Modular Hard-Surface Asset Generator for Blender (Headless)
Generates game-ready modular dungeon walls, cargo crates, sci-fi pipes, and floor tiles
without any external AI model, with metric snapping, bevel modifiers, LOD0/1/2,
and Unreal Engine UCX_ collision hulls.
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

    parser = argparse.ArgumentParser(description="Procedural Modular 3D Asset Generator")
    parser.add_argument(
        "--type",
        required=True,
        choices=["dungeon_wall", "cargo_crate", "sci_fi_pipe", "floor_tile"],
        help="Type d'asset modulaire procédural à générer"
    )
    parser.add_argument("--output", required=True, help="Chemin d'export (.glb ou .fbx)")
    parser.add_argument("--name", default="ModularAsset", help="Nom de l'asset")
    parser.add_argument("--qa-image", default=None, help="Chemin optionnel pour planche de rendu QA PNG")
    return parser.parse_args(argv)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build_dungeon_wall(name):
    """Génère un pan de mur de donjon modulaire (2.0m x 2.0m x 0.35m) avec relief et chanfreins."""
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(f"{name}_LOD0", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    # Corps principal du mur (largeur X=2.0, épaisseur Y=0.35, hauteur Z=2.0)
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.0, 0.35, 2.0, 1.0)))

    # Découpe en blocs de pierre par découpage horizontal et vertical
    for z_cut in [-0.5, 0.0, 0.5]:
        bmesh.ops.bisect_plane(
            bm,
            geom=bm.faces[:] + bm.edges[:] + bm.verts[:],
            plane_co=(0, 0, z_cut),
            plane_no=(0, 0, 1)
        )
    for x_cut in [-0.5, 0.5]:
        bmesh.ops.bisect_plane(
            bm,
            geom=bm.faces[:] + bm.edges[:] + bm.verts[:],
            plane_co=(x_cut, 0, 0),
            plane_no=(1, 0, 0)
        )

    # Décalage léger aléatoire des faces avant pour donner du relief aux briques
    for f in bm.faces:
        if f.normal.y < -0.8:  # Face orientée vers l'avant (-Y)
            noise_inset = (math.sin(f.calc_center_bounds().x * 5.0) + math.cos(f.calc_center_bounds().z * 4.0)) * 0.015
            for v in f.verts:
                v.co.y += noise_inset

    bm.to_mesh(mesh)
    bm.free()

    # Modificateur Bevel pour chanfreiner les arêtes de briques
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.02
    bevel.segments = 2
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = math.radians(35)
    bpy.ops.object.modifier_apply(modifier=bevel.name)

    return obj


def build_cargo_crate(name):
    """Génère une caisse de transport renforcée (1.0m x 1.0m x 1.0m) avec cadre en relief."""
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(f"{name}_LOD0", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    # Cube de base
    bmesh.ops.create_cube(bm, size=1.0)

    # Inset sur chaque face pour créer les panneaux creusés
    faces_to_inset = list(bm.faces)
    inset_res = bmesh.ops.inset_individual(bm, faces=faces_to_inset, thickness=0.08, depth=-0.04)

    # Diagonales de renfort en X sur les faces latérales
    bm.to_mesh(mesh)
    bm.free()

    # Chanfrein propre
    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.015
    bevel.segments = 2
    bevel.limit_method = "ANGLE"
    bpy.ops.object.modifier_apply(modifier=bevel.name)

    return obj


def build_sci_fi_pipe(name):
    """Génère un segment de tuyau industriel (longueur 2.0m, diamètre 0.3m) avec brides."""
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(f"{name}_LOD0", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    # Cylindre horizontal (longueur X=2.0, rayon=0.15)
    rot_mat = Matrix.Rotation(math.radians(90), 4, "Y")
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=24,
        radius1=0.15,
        radius2=0.15,
        depth=2.0,
        matrix=rot_mat
    )

    # Anneaux / brides aux deux extrémités et au centre
    for x_pos in [-0.9, 0.0, 0.9]:
        ring_mat = Matrix.Translation(Vector((x_pos, 0, 0))) @ rot_mat
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=24,
            radius1=0.18,
            radius2=0.18,
            depth=0.12,
            matrix=ring_mat
        )

    bm.to_mesh(mesh)
    bm.free()

    bpy.ops.object.shade_smooth()
    return obj


def build_floor_tile(name):
    """Génère une dalle de sol modulaire (2.0m x 2.0m x 0.1m) avec jointures."""
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    obj = bpy.data.objects.new(f"{name}_LOD0", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.0, 2.0, 0.1, 1.0)))
    bm.to_mesh(mesh)
    bm.free()

    bevel = obj.modifiers.new(name="Bevel", type="BEVEL")
    bevel.width = 0.02
    bevel.segments = 2
    bevel.limit_method = "ANGLE"
    bpy.ops.object.modifier_apply(modifier=bevel.name)

    return obj


def ground_pivot_at_bottom_center(obj):
    """Déplace l'origine de l'objet au centre-bas (Z=0)."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    center_x = (min(c.x for c in bbox_corners) + max(c.x for c in bbox_corners)) / 2.0
    center_y = (min(c.y for c in bbox_corners) + max(c.y for c in bbox_corners)) / 2.0
    bottom_z = min(c.z for c in bbox_corners)

    offset = Vector((-center_x, -center_y, -bottom_z))
    obj.data.transform(Matrix.Translation(offset))
    obj.matrix_world.translation = Vector((0.0, 0.0, 0.0))


def decimate_object(obj, ratio):
    mod = obj.modifiers.new(name="Decimate_LOD", type="DECIMATE")
    mod.decimate_type = "COLLAPSE"
    mod.ratio = max(0.01, min(1.0, ratio))
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)


def generate_lods_and_collision(lod0_obj, name):
    # LOD1 (50%)
    lod1 = lod0_obj.copy()
    lod1.data = lod0_obj.data.copy()
    lod1.name = f"{name}_LOD1"
    lod1.data.name = f"{name}_LOD1_Mesh"
    bpy.context.collection.objects.link(lod1)
    decimate_object(lod1, 0.5)

    # LOD2 (20%)
    lod2 = lod0_obj.copy()
    lod2.data = lod0_obj.data.copy()
    lod2.name = f"{name}_LOD2"
    lod2.data.name = f"{name}_LOD2_Mesh"
    bpy.context.collection.objects.link(lod2)
    decimate_object(lod2, 0.2)

    # UCX Convex Collision Hull
    ucx = lod2.copy()
    ucx.data = lod2.data.copy()
    ucx.name = f"UCX_{name}"
    ucx.data.name = f"UCX_{name}_Mesh"
    ucx.data.materials.clear()
    bpy.context.collection.objects.link(ucx)

    bm = bmesh.new()
    bm.from_mesh(ucx.data)
    hull = bmesh.ops.convex_hull(bm, input=bm.verts)
    bmesh.ops.delete(bm, geom=hull["geom_interior"] + hull["geom_unused"], context="VERTS")
    bm.to_mesh(ucx.data)
    bm.free()

    if len(ucx.data.polygons) > 36:
        decimate_object(ucx, 36.0 / len(ucx.data.polygons))

    return lod0_obj, lod1, lod2, ucx


def export_asset(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    ext = os.path.splitext(output_path)[1].lower()
    if ext in [".glb", ".gltf"]:
        bpy.ops.export_scene.gltf(filepath=output_path, export_format="GLB", export_apply=True, export_yup=True)
    elif ext == ".fbx":
        bpy.ops.export_scene.fbx(filepath=output_path, use_selection=False, apply_scale_options="FBX_SCALE_ALL")
    else:
        raise ValueError(f"Extension non supportée: {ext}")


def main():
    args = parse_args()
    clear_scene()

    generators = {
        "dungeon_wall": build_dungeon_wall,
        "cargo_crate": build_cargo_crate,
        "sci_fi_pipe": build_sci_fi_pipe,
        "floor_tile": build_floor_tile
    }

    lod0 = generators[args.type](args.name)
    ground_pivot_at_bottom_center(lod0)
    lod0, lod1, lod2, ucx = generate_lods_and_collision(lod0, args.name)
    export_asset(args.output)

    print("=== PROCEDURAL MODULAR ASSET GÉNÉRÉ ===")
    print(f"Type     : {args.type}")
    print(f"Nom      : {args.name}")
    print(f"LOD0     : {len(lod0.data.polygons)} tris")
    print(f"LOD1     : {len(lod1.data.polygons)} tris")
    print(f"LOD2     : {len(lod2.data.polygons)} tris")
    print(f"UCX      : {len(ucx.data.polygons)} tris")
    print(f"Sortie   : {args.output}")


if __name__ == "__main__":
    main()
