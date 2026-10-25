# Référence d'Architecture Spatiale IFC4 (ISO 16739)

## 1. Hiérarchie d'Agrégation Normée
Selon le standard buildingSMART, la structure du bâtiment s'organise selon :
1. `IfcProject` : Unités, repère mondial, métadonnées du contrat BIM.
2. `IfcSite` : Terrain, latitude, longitude, élévation géodésique.
3. `IfcBuilding` : Corps d'état architectural et structurel.
4. `IfcBuildingStorey` : Niveaux altimétriques (Z = 0.00m, Z = +3.00m, etc.).
5. `IfcSpace` : Volumes intérieurs pour le calcul thermique et surfacique.

## 2. Jeux de Propriétés (Psets) Standards
- `Pset_WallCommon` :
  - `LoadBearing` (Boolean) : Indique si le mur reprend des charges verticales.
  - `IsExternal` (Boolean) : Indique si la paroi est en contact avec l'extérieur.
  - `FireRating` (String) : Résistance au feu (ex. REI 60, REI 120).
- `Pset_SlabCommon` :
  - `PitchAngle` (Angle) : Pente pour les toitures terrasses ou charpentes.
