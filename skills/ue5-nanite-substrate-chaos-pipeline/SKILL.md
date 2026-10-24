---
name: ue5-nanite-substrate-chaos-pipeline
description: >-
  Architect and implement next-generation Unreal Engine 5.5 - 5.8 rendering, materials, and physics. Unifies Nanite virtualized micro-polygon geometry (Hi-Z occlusion culling, meshlet cluster trees), Lumen dynamic Global Illumination (Surface Cache, Mesh Distance Fields), Substrate modular BSDF materials (Slab layers, energy conservation), and Chaos Physics (Voronoi Geometry Collections, strain damage thresholds, physics field impulses, and active physical ragdolls).
---

# 🌌 Unreal Engine 5 Next-Gen Graphics & Physics Core (SOTA 2026)

> **Inspirations & Provenance :** Epic Games UE 5.5 / 5.6 / 5.8 Architectural Standards, Nanite & Lumen Engineering, Substrate (Strata) Shading System, Chaos Destruction Engine.  
> **Core Axiom :** *"A photorealistic game scene requires an integrated pipeline: Nanite eliminates polycount budgets, Lumen dynamically illuminates micro-surfaces, Substrate conserves physical optical energy, and Chaos fractures geometry deterministically upon impact."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine que tu construis un château médiéval ultra-détaillé dans Unreal Engine 5 :
1. **Nanite (Les Micro-Polygones Invisibles)** :
   Au lieu de créer 5 versions simplifiées d'un mur (LODs) pour soulager la carte graphique, tu importes le mur directement avec 10 millions de polygones ! Nanite découpe automatiquement la pierre en petits paquets de 128 triangles (*clusters*). Si le mur est loin, Nanite n'affiche que les paquets visibles. S'il est caché derrière une tour, le tampon Hi-Z l'efface instantanément avant même de calculer la moindre couleur.
2. **Lumen (La Lumière Qui Rebondit Partout)** :
   Le soleil tape sur une bannière rouge vif à l'entrée du château. La lumière ne s'arrête pas là : elle rebondit sur la pierre grise qui prend une teinte rose chaleureuse (*Global Illumination*). Lumen fait cela en temps réel sans que tu aies besoin de "cuire" la lumière pendant des heures.
3. **Substrate (Les Vrais Matériaux Physiques)** :
   Une armure de chevalier n'est pas juste "grise et brillante". C'est une plaque d'acier brut recouverte d'une fine couche de vernis protecteur, avec des traces de poussière mate et des rayures. Substrate te permet d'empiler ces couches physiques comme un mille-feuille (*Slabs*), tout en respectant une loi de la physique inviolable : la lumière réfléchie ne peut jamais être plus puissante que la lumière reçue (*Conservation d'Énergie*).
4. **Chaos (La Destruction Spectaculaire)** :
   Une catapulte tire un rocher sur la tour. Au lieu de remplacer magiquement la tour par un tas de cailloux précalculé, Chaos calcule l'onde de choc (*Strain Energy*). Si l'impact dépasse la résistance de la pierre, les joints se brisent le long de fractures géométriques de Voronoi. Les morceaux deviennent de vrais objets physiques qui tombent, s'entrechoquent et soulèvent de la poussière.

---

## 🏛️ 2. Nanite : Géométrie Virtualisée & Tampon Hi-Z

### Arbre de Clusters de Meshlets
- Chaque maillage Nanite est subdivisé en clusters de **128 triangles** partageant des sommets voisins.
- Un arbre hiérarchique de boîtes englobantes permet de streamer uniquement les nœuds du niveau de détail (LOD) requis par la taille en pixels à l'écran.

### Rendu Occlusion Culling en Deux Passes (Hi-Z)
1. **Passe 1 (Hi-Z Initial)** : Rendu des clusters visibles à la frame précédente $\to$ mise à jour du tampon Hi-Z (Hierarchical Z-Buffer).
2. **Passe 2 (Validation)** : Test de tous les autres clusters contre le tampon Hi-Z $\to$ élimination intégrale des clusters masqués avant shading.
- Élimine $98\%$ du surcoût de shading sur les scènes denses (villes, forêts touffues).

---

## 💡 3. Lumen : Illumination Globale Dynamique & Cache de Surface

### Cartes d'Atlas du Surface Cache
- Lumen génère un atlas de cartes de réflectance et de normales pour chaque objet statique :
  - **Cartes Plates (Cards)** : Projections 2D basse résolution capturant l'albedo et l'émissivité.
  - **Mesh Distance Fields (MDF)** : Représentation volumétrique de distance signée permettant de tracer des rayons logiciels (*Software Ray Tracing*) à coût fixe sans GPU RTX dédié.

### Radiance Caching Multi-Rebonds
- Les rayons de lumière effectuent jusqu'à **3 rebonds dynamiques** dans la scène.
- Permet des intérieurs de châteaux sombres naturellement éclairés par la lumière entrant par une fenêtre ouverte.

---

## 🎨 4. Substrate : Matériaux Modulaires BSDF & Slabs

### Composition Verticale de Couches (Vertical Layering)
Superposition rigoureuse d'un vernis diélectrique sur un substrat métallique :
```
Top Layer: Clear Coat Slab (IOR = 1.5, Roughness = 0.05, Metallic = 0.0)
     │   (Reflects F_top, Transmits 1.0 - F_top)
     ▼
Bottom Layer: Brushed Steel Slab (Albedo = Silver, Roughness = 0.35, Metallic = 1.0)
```

### Règle d'Or : Conservation Mathématique de l'Énergie
$$\int_{\Omega^+} \left( f_d(\omega_i, \omega_o) + f_s(\omega_i, \omega_o) \right) (\omega_i \cdot \mathbf{n}) \, d\omega_i \le 1.0$$
- Substrate déduit automatiquement l'énergie réfléchie par la couche supérieure de celle transmise aux couches inférieures.
- Empêche les matériaux d'émettre magiquement de la lumière parasite (artéfacts de "glow" blanc).

---

## 💥 5. Chaos : Physique & Destruction Voronoi

### Hiérarchie des Geometry Collections
- **Niveau 0 (Root)** : Structure complète intacte.
- **Niveau 1 (Macro Chunks)** : Poutres maîtresses, piliers, linteaux.
- **Niveau 2 (Micro Debris)** : Briques, éclats de pierre et gravats.

### Seuil de Rupture par Contrainte (Strain Damage Threshold)
- Chaque liaison physique entre fragments possède un seuil de résistance :
  - Si l'énergie de l'impact $E_{\text{impact}} > \text{StrainThreshold}$, le lien est rompu.
  - Les fragments désolidarisés deviennent des corps rigides dynamiques soumis à la gravité.
- **Champs d'Ancrage (Anchor Fields)** : Fixent les fondations au sol avec une masse infinie pour éviter l'envol des bâtiments.

---

## 🛠️ 6. Suite Déterministe d'Outils Compagnons

Les scripts d'évaluation et de benchmark se trouvent dans `scripts/` :
```bash
# 1. Auditer la densité des clusters Nanite et le ratio de triangles
python scripts/audit_nanite_clusters.py --demo

# 2. Benchmarker le temps de couverture du Surface Cache Lumen
python scripts/benchmark_lumen_surface_cache.py --demo

# 3. Valider la conservation d'énergie d'un matériau Substrate multi-couches
python scripts/validate_substrate_bsdf_energy.py --demo

# 4. Simuler l'onde de choc et la fracturation Voronoi Chaos avec ancrage
python scripts/simulate_chaos_fracture.py
```
