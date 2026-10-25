---
name: bim-ifc-cad-architect
description: >-
  Architect and implement Building Information Modeling (BIM) pipelines, ISO 16739 IFC4 / IFC2X3 schemas, IfcOpenShell automation, spatial decomposition trees (IfcProject to IfcSpace), geometric representation (IfcExtrudedAreaSolid, CSG booleans), material associations, and IDS data validation. Use when the user asks about BIM modeling, IFC architecture, IfcOpenShell, building spatial hierarchy, architectural drawings, or BIM property sets.
---

# 🏛️ BIM & IFC Architecture Engine (ISO 16739 / IfcOpenShell)

> **Standard :** ISO 16739-1:2024 (Industry Foundation Classes - IFC4.3 / IFC4 ADD2)  
> **Noyau :** IfcOpenShell Python 0.9.x, OpenCASCADE BRep integration, buildingSMART IDS  
> **Rôle :** Spécialiste du Building Information Modeling (BIM), de la décomposition spatiale, des profils paramétriques d'extrusion, des propriétés normées (Psets) et des nomenclatures architecturales.

---

## 🎯 Déclenchement & Cas d'Usage
Active ce skill pour :
- **Décomposition Spatiale Normée** : Création et manipulation de la hiérarchie stricte `IfcProject` → `IfcSite` → `IfcBuilding` → `IfcBuildingStorey` → `IfcSpace`.
- **Modélisation d'Éléments Constructifs** : Murs (`IfcWall`, `IfcWallStandardCase`), dalles (`IfcSlab`), poteaux (`IfcColumn`), poutres (`IfcBeam`), portes (`IfcDoor`) et fenêtres (`IfcWindow`).
- **Représentations Géométriques Paramétriques** : Solides extrudés (`IfcExtrudedAreaSolid`), profils arbitraires (`IfcArbitraryClosedProfileDef`), et opérations booléennes d'ouverture (`IfcOpeningElement`, `IfcRelVoidsElement`).
- **Gestion des Données Sémantiques** : Jeux de propriétés normés (`Pset_WallCommon`, `Pset_SlabCommon`), quantités de base (`Qto_WallBaseQuantities`) et associations de matériaux (`IfcMaterialLayerSet`).
- **Validation & Conformité** : Audit de conformité IDS (Information Delivery Specification), contrôle de validité des GUIDs (chaînes de 22 caractères base64 compressées) et détection des éléments physiques flottants.

---

## 🏗️ 1. Architecture Spatiale & Contrat de Données

Tout fichier IFC valide respecte l'arbre d'agrégation défini par `IfcRelAggregates` et la relation de confinement spatial `IfcRelContainedInSpatialStructure` :

```
IfcProject (Racine du projet avec unités de mesure SI et contexte géométrique)
  └── IfcSite (Emplacement géographique, coordonnées WGS84 / Lambert, élévation)
        └── IfcBuilding (Bâtiment avec classification et niveau de référence)
              └── IfcBuildingStorey (Niveau / Étage avec élévation relative Z)
                    ├── IfcSpace (Pièce / Volume habitable délimité)
                    └── Éléments physiques (IfcWall, IfcSlab, IfcColumn...)
```

### Règle d'Or de Confinement
Aucun élément physique constructif (`IfcProduct`) ne doit flotter sans rattachement spatial. Chaque élément de structure doit être explicitement relié à son étage (`IfcBuildingStorey`) via `IfcRelContainedInSpatialStructure`.

---

## 📐 2. Pipeline IfcOpenShell Typique

```python
import ifcopenshell
import ifcopenshell.api

# 1. Initialisation d'un fichier IFC4 vierge
model = ifcopenshell.api.run("project.create_file", version="IFC4")

# 2. Création de la racine du projet
project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject", name="Mono Architecture")
ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "METRE"})

# 3. Contexte de modélisation 3D
context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
body_context = ifcopenshell.api.run(
    "context.add_context", model,
    context_type="Model", context_identifier="Body",
    target_view="MODEL_VIEW", parent=context
)

# 4. Hiérarchie Spatiale
site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite", name="Terrain Principal")
building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="Bâtiment A")
storey = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Rez-de-chaussée")

ifcopenshell.api.run("aggregate.assign_object", model, relating_object=project, product=site)
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=site, product=building)
ifcopenshell.api.run("aggregate.assign_object", model, relating_object=building, product=storey)

# 5. Création d'un Mur Porteur avec Propriétés
wall = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcWall", name="Mur_Extérieur_01")
ifcopenshell.api.run("spatial.assign_container", model, relating_structure=storey, product=wall)

# Ajout du Property Set Pset_WallCommon
pset = ifcopenshell.api.run("pset.add_pset", model, product=wall, name="Pset_WallCommon")
ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties={
    "LoadBearing": True,
    "IsExternal": True,
    "FireRating": "REI 60"
})

# Sauvegarde
model.write("modele_architecture.ifc")
```

---

## 🔍 3. Outil Compagnon Déterministe

Le script compagnon [`validate_ifc_spatial_tree.py`](scripts/validate_ifc_spatial_tree.py) analyse n'importe quel fichier `.ifc` et contrôle :
1. La présence obligatoire de la racine `IfcProject` et d'au moins un `IfcBuildingStorey`.
2. L'absence d'éléments constructifs orphelins (déconnectés de tout contenant spatial).
3. L'unicité absolue de tous les GUIDs (GlobalId 22 caractères).
4. Le respect de la casse et des types de données pour les `Pset` standards.
