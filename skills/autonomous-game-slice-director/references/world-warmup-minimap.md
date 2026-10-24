# World Warmup, Static Minimap Baking & Zero-Stutter Performance Architecture

Derived from the 36-hour autonomous *World of Oldcraft* marathon (reducing a 218.6ms loading hitch to 15.3ms and recovering +33 FPS).

## 🚀 1. The WorldWarmup Protocol (Zero Micro-Saccade)

### The Shader Compilation Hitch Problem
Engines delay GPU pipeline state object (PSO) compilation until an asset is visible on screen. Entering a new dense zone triggers a massive stutter (>200ms) as dozens of shaders compile simultaneously.

### The Solution: Phantom Warmup Camera
During the loading screen (`LoadingScreen`):
1. Spawn a hidden camera and translate it through pre-placed waypoints (`WarmupWaypoints`) across all key vistas.
2. Force-render 1 frame at each waypoint with culling disabled to upload all PSOs and high-res mipmaps to GPU VRAM.
3. Fade to game once all waypoints are warmed.

```csharp
// WorldWarmupDriver.cs (Unity C# / Godot C# / Unreal C++ Bridge)
using System;
using System.Collections;
using UnityEngine;

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

## 🗺️ 2. Static Orthographic Minimap Baking (+33 FPS Recovered)

> [!CAUTION]
> **Never use real-time overhead cameras for minimaps.**
> Rendering a secondary camera every frame cuts FPS in half (e.g., 84 FPS down to 35 FPS).

### The Static Baking Pipeline
1. **Zenith Capture**: Position an orthographic camera at $Z = +500	ext{m}$ pointing directly down.
2. **High-Res Export**: Bake the zone once into a $4096 \times 4096$ PNG texture.
3. **Runtime Projection**: Map player world coordinates $(X, Z)$ to texture UVs:
   $$U = \frac{X - X_{\min}}{X_{\max} - X_{\min}}, \quad V = \frac{Z - Z_{\min}}{Z_{\max} - Z_{\min}}$$

---

## 🛡️ 3. Shader Keep-Alive Stripping Guards

When building standalone packages, game engines strip shaders that appear unreferenced in scenes.
- **Guard**: Maintain an explicit `KeepAliveMaterials` asset in a `Resources/` or preload folder with serialized references to all materials used by procedural or dynamically loaded assets.

---

## 🧹 4. Marathon Disk & VRAM Storage Watchdog

During multi-hour autonomous runs, intermediate decimation caches and temporary assets inflate disk space.
- Run an automated check removing intermediate GLB mesh takes and build caches when free space drops below 15 GB.
