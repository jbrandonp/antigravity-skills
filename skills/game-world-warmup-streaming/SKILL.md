---
name: game-world-warmup-streaming
description: "Architect and implement zero-stutter world warmup, static orthographic minimap baking, shader keep-alive guards, and autonomous marathon storage policies for Unreal Engine 5, Unity, and Godot. Eliminates 200ms+ runtime compilation hitches, recovers 30+ FPS from dynamic minimap overhead, and prevents out-of-memory crashes."
---

# Game World Warmup & Zero-Stutter Performance Architecture

Use this skill when optimizing game loading, streaming open worlds, eradicating runtime hitching (first-frame shader compilation micro-stutters), replacing expensive real-time minimap cameras, and preventing memory leaks during long-running builds.

Derived from the post-mortem engineering breakthroughs of the 36-hour autonomous *World of Oldcraft* marathon (reducing a 218.6 ms city loading hitch to 15.3 ms, recovering +33 FPS via static minimap baking, and preventing 16 GB pagefile memory bloat).

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

As-tu déjà joué à un jeu où tout est fluide, mais dès que tu passes les portes d'une grande ville ou qu'un boss lance son premier sort, **l'écran se fige pendant un quart de seconde** ?

C'est ce qu'on appelle un **"Shader Compilation Hitch"** : le moteur de jeu attend que le joueur voie l'objet pour compiler son matériau dans la carte graphique. Si 50 nouveaux matériaux apparaissent d'un coup, le processeur s'étouffe et le jeu saccade.

Ce skill applique 3 remèdes d'ingénierie de pointe :
1. **Le Préchauffage Mondial (World Warmup) :** Pendant que le joueur regarde la barre de chargement, le jeu fait discrètement un rendu rapide des 10 zones clés hors-champ. Quand le joueur entre dans la ville, tous les shaders sont déjà chauds dans la mémoire GPU : le gel passe de **218 ms à 15 ms** (invisible à l'œil nu).
2. **La Carte Statique Cuite (Minimap Baker) :** Mettre une deuxième caméra dans le ciel qui filme la ville en temps réel pour faire la mini-carte fait chuter les performances de 84 FPS à 35 FPS ! On prend une seule photo géante haute définition ($4096 \times 4096$) à la compilation, et pendant le jeu, la mini-carte n'est qu'une simple image 2D qui défile. Résultat : **+33 FPS récupérés immédiatement**.
3. **Le Gardien de Mémoire (Storage Watchdog) :** Durant un développement de plusieurs heures avec IA, les fichiers temporaires et les caches explosent (jusqu'à 16 Go de mémoire virtuelle gaspillée). Le watchdog nettoie automatiquement les résidus à chaque étape.

---

## 🚀 2. Le Protocole WorldWarmup (Zéro Micro-Saccade)

### Le Problème
Le premier passage devant la fontaine ou le château provoque un saut d'image inacceptable ($> 200\text{ ms}$).

### La Solution WorldWarmup
Derrière l'écran de chargement (`LoadingScreen`), avant de dissoudre la caméra dans le monde jouable :
1. Déplacer une caméra virtuelle fantôme vers une liste de $N$ points névralgiques prédéfinis (`WarmupWaypoints`).
2. Rendre 1 frame de chaque point avec le culling désactivé pour forcer le pilote GPU (DirectX 12 / Vulkan) à compiler tous les PSOs (Pipeline State Objects) et charger les mipmaps haute résolution.
3. Afficher le fondu au noir et donner le contrôle au joueur.

```csharp
// WorldWarmupDriver.cs (Compatible Unity C# / Unreal C++ / Godot)
public class WorldWarmupDriver : MonoBehaviour
{
    [SerializeField] private Transform[] warmupWaypoints;
    [SerializeField] private Camera warmupCamera;

    public IEnumerator ExecuteWarmupSequence(Action onComplete)
    {
        warmupCamera.enabled = true;
        foreach (var waypoint in warmupWaypoints)
        {
            warmupCamera.transform.position = waypoint.position;
            warmupCamera.transform.rotation = waypoint.rotation;
            warmupCamera.Render(); // Force GPU pipeline compilation & texture streaming
            yield return null;     // Wait 1 frame
        }
        warmupCamera.enabled = false;
        onComplete?.Invoke();
    }
}
```

---

## 🗺️ 3. Baking de Mini-Carte Statique ($+33$ FPS Récupérés)

> [!CAUTION]
> **Interdiction formelle des caméras de mini-carte en temps réel.**
> Une caméra secondaire qui rend la scène à chaque frame double le nombre de draw calls, réévalue les lumières dynamiques et divise le framerate par deux (chute mesurée de 84 FPS à 35 FPS).

### Le Pipeline de Baking
1. **Capture Hors-Ligne :** Positionner une caméra orthographique zénithale au-dessus de la carte du monde ($Z = +500\text{ m}$, taille orthographique = largeur du monde en mètres).
2. **Export Texture Haute Résolution :** Rendre la scène complète en texture PNG non compressée ($2048 \times 2048$ ou $4096 \times 4096$).
3. **Projection Mathématique Runtime :**
   Calculer les coordonnées UV de la mini-carte en fonction de la position monde du joueur $(X, Z)$ :
   $$U = \frac{X - X_{\min}}{X_{\max} - X_{\min}}, \quad V = \frac{Z - Z_{\min}}{Z_{\max} - Z_{\min}}$$
4. **Affichage UI Léger :** Afficher l'icône du joueur et des objectifs sur un simple canvas UI 2D. Consommation CPU : $< 0.05\text{ ms}$ au lieu de $14\text{ ms}$.

---

## 🛡️ 4. Shader Keep-Alive Guards (Anti-Crash Build)

### Le Problème du "Shader Stripping"
Lors de la compilation finale d'un jeu (`Build`), le moteur supprime agressivement les shaders qu'il croit inutilisés. Si un shader ou matériau VFX est chargé dynamiquement via code ou script (ex: effet de gel, aura de quête, contour de sélection), le jeu plante au démarrage avec un écran rose ou un crash `Shader lookup null`.

### La Solution Keep-Alive
1. Créer un asset `KeepAliveMaterialManifest` contenant un tableau explicite de tous les matériaux dynamiques.
2. Assigner cet asset dans les paramètres du moteur (`Always Included Shaders` dans Unity ou `Project Settings -> Packing -> Additional Asset Directories to Cook` dans Unreal Engine).
3. Placer une instance cachée de ces matériaux dans la scène d'initialisation pour garantir qu'aucun shader ne soit éliminé par le compilateur.

---

## 🧹 5. Marathon Storage & Cache Watchdog

Lors d'un développement autonome marathon (24h à 48h) :
- Les fichiers caches (`DerivedDataCache` UE5, `Library/Artifacts` Unity, buffers temporaires de rendu) gonflent de plusieurs dizaines de gigaoctets.
- **Règle Watchdog :**
  - Purger les caches de rendus intermédiaires après chaque jalon validé.
  - Surveiller le fichier d'échange (pagefile) : si la mémoire virtuelle dépasse 12 Go, forcer un redémarrage propre de l'éditeur headless pour libérer les allocations non-purgées.
  - Conserver un espace disque SSD libre d'au moins **15 Go** en permanence sous peine d'interruption fatale du build.
