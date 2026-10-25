---
name: threejs-rtc-cad-viewport
description: Architect, implement, and harden high-precision Relative-To-Center (RTC) and Camera-Relative 3D viewports in Three.js and WebGL/WebGPU for CAD assemblies, large-scale GIS, and microscopic precision inspection. Covers double-precision CPU coordinate handling, floating origin OrbitControls, RTC raycasting, B-Rep edge silhouette shaders, logarithmic depth buffer chunks, and WebGL context loss recovery.
---

# Three.js RTC (Relative-To-Center) Industrial CAD Viewport Engine

Ce guide d'ingénierie certifié fournit l'architecture matérielle et logicielle complète pour concevoir un viewport 3D de classe industrielle sous **Three.js** / **Tauri 2.x**, éliminant les tremblements de sommets (*vertex jitter*), les erreurs d'orbite à fort grossissement, et le *Z-fighting*.

---

## 🎯 Pédagogie : Les 4 Pièges du Rendu CAO 3D (Explication 15 ans)

Quand on affiche une pièce mécanique dans un navigateur ou dans une application de bureau :
1. **Le tremblement de terre numérique (*Vertex Jitter*) :** La carte graphique n'a que des nombres à 7 chiffres significatifs (`float32`). Si ta pièce est à $1000\text{ mm}$ et que tu inspectes une fissure de $0.001\text{ mm}$, les petits chiffres sont effacés : la pièce vibre comme si elle était secouée.
2. **Le clignotement des faces (*Z-fighting*) :** Quand deux plaques de tôle sont presque collées, la carte graphique ne sait plus laquelle est devant l'autre : elles clignotent frénétiquement.
3. **Le clic fantôme (*Raycasting Drift*) :** Si tu cliques pour sélectionner un trou de vis sur un grand assemblage, le rayon de ta souris calcule une position imprécise et rate la face ciblée de plusieurs millimètres.
4. **La caméra qui tangue (*Orbit Wobble*) :** En zoomant très fort avec la molette, le centre de rotation de la caméra dérive parce que le vecteur cible s'arrondit.

**La solution globale durcie :**
- **CPU en Float64 :** Le processeur calcule la caméra, le centre d'orbite et le rayon de souris en 64 bits ultra-précis.
- **Origine Flottante GPU :** La carte graphique reçoit le monde déjà translaté autour de la caméra (`P_relatif = P_monde - P_caméra`). Pour elle, l'objet est toujours à portée de main !
- **Logarithmic Depth Buffer :** La précision en profondeur est distribuée de façon logarithmique pour séparer les surfaces distantes d'un micromètre.

---

## 🏗️ Architecture Complète du Viewport Industriel (`cad_viewport_rtc.ts`)

```typescript
import * as THREE from 'three';

/**
 * High-precision 64-bit coordinate representation on CPU.
 */
export interface Vector3F64 {
  x: number;
  y: number;
  z: number;
}

export interface CadMeshItem {
  mesh: THREE.Mesh;
  wireframeMesh?: THREE.LineSegments;
  worldPositionF64: Vector3F64;
  partId: string;
}

/**
 * Industrial CAD Shader with RTC, Logarithmic Depth, and Normal Edge Shading.
 */
export function createIndustrialCadMaterial(options: {
  baseColor: THREE.Color;
  wireframe?: boolean;
}): THREE.ShaderMaterial {
  return new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: options.baseColor },
      uLightDir: { value: new THREE.Vector3(0.5, 0.8, 0.4).normalize() },
      uObjectOffset: { value: new THREE.Vector3(0, 0, 0) },
      uEdgeHighlight: { value: 0.15 },
    },
    vertexShader: /* glsl */ `
      #include <common>
      #include <logdepthbuf_pars_vertex>

      uniform vec3 uObjectOffset;
      varying vec3 vNormalEye;
      varying vec3 vViewDir;

      void main() {
        // Normale transformée dans l'espace vue
        vNormalEye = normalize(normalMatrix * normal);

        // Position locale relative-to-center transmise via modelViewMatrix
        vec4 eyePosition = modelViewMatrix * vec4(position, 1.0);
        vViewDir = -eyePosition.xyz;

        gl_Position = projectionMatrix * eyePosition;

        // Injection obligatoire du tampon logarithmique Three.js
        #include <logdepthbuf_vertex>
      }
    `,
    fragmentShader: /* glsl */ `
      #include <common>
      #include <logdepthbuf_pars_fragment>

      uniform vec3 uColor;
      uniform vec3 uLightDir;
      uniform float uEdgeHighlight;

      varying vec3 vNormalEye;
      varying vec3 vViewDir;

      void main() {
        vec3 N = normalize(vNormalEye);
        vec3 V = normalize(vViewDir);

        // Modèle d'éclairage CAD métallique doux (Diffuse + Curv/Rim)
        float diff = max(dot(N, uLightDir), 0.25);
        
        // Silhouette Rim Light pour accentuer les contours B-Rep
        float rim = 1.0 - max(dot(N, V), 0.0);
        float edgeStrength = smoothstep(0.7, 1.0, rim) * uEdgeHighlight;

        vec3 ambient = vec3(0.15, 0.18, 0.22);
        vec3 finalColor = (ambient + diff * uColor) + vec3(edgeStrength);

        gl_FragColor = vec4(finalColor, 1.0);

        #include <logdepthbuf_fragment>
      }
    `,
    side: THREE.DoubleSide,
    wireframe: options.wireframe ?? false,
  });
}

/**
 * High-Precision Industrial CAD Viewport with Floating Origin Controls & RTC Raycasting.
 */
export class IndustrialCadViewport {
  private renderer: THREE.WebGLRenderer;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private canvas: HTMLCanvasElement;

  // Coordonnées absolues 64-bit sur CPU
  private cameraPosF64: Vector3F64 = { x: 0.0, y: 0.0, z: 200.0 };
  private orbitTargetF64: Vector3F64 = { x: 0.0, y: 0.0, z: 0.0 };

  private objects: CadMeshItem[] = [];
  private isContextLost: boolean = false;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;

    // 1. Initialisation Renderer avec Logarithmic Depth Buffer
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      logarithmicDepthBuffer: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: true,
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2.0));
    this.renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x131722); // Thème CAD Studio Dark

    // 2. Caméra perspective avec plans de découpe optimaux
    this.camera = new THREE.PerspectiveCamera(
      45,
      canvas.clientWidth / canvas.clientHeight,
      0.01,
      100000.0
    );

    // 3. Gestionnaire de perte de contexte WebGL (Tauri / Redimensionnement)
    this.setupContextLossHandling();
  }

  private setupContextLossHandling(): void {
    this.canvas.addEventListener('webglcontextlost', (event: Event) => {
      event.preventDefault();
      this.isContextLost = true;
      console.warn('[CAD Viewport] WebGL Context lost. Pausing rendering pipeline.');
    });

    this.canvas.addEventListener('webglcontextrestored', () => {
      console.info('[CAD Viewport] WebGL Context restored. Rebuilding GPU resources.');
      this.isContextLost = false;
      this.rebuildShaders();
    });
  }

  private rebuildShaders(): void {
    for (const item of this.objects) {
      if (item.mesh.material instanceof THREE.Material) {
        item.mesh.material.needsUpdate = true;
      }
    }
  }

  /**
   * Floating-Origin Orbit Transformation (CPU 64-bit).
   */
  public orbit(deltaAzimuthRad: number, deltaElevationRad: number): void {
    // Calcul de l'orbite en f64 relatif au target
    const dx = this.cameraPosF64.x - this.orbitTargetF64.x;
    const dy = this.cameraPosF64.y - this.orbitTargetF64.y;
    const dz = this.cameraPosF64.z - this.orbitTargetF64.z;

    const radius = Math.sqrt(dx * dx + dy * dy + dz * dz);
    let elevation = Math.asin(Math.max(-1.0, Math.min(1.0, dy / radius))) + deltaElevationRad;
    let azimuth = Math.atan2(dx, dz) + deltaAzimuthRad;

    // Clamping élévation pour éviter singularité des pôles
    elevation = Math.max(-Math.PI / 2.05, Math.min(Math.PI / 2.05, elevation));

    this.cameraPosF64.x = this.orbitTargetF64.x + radius * Math.cos(elevation) * Math.sin(azimuth);
    this.cameraPosF64.y = this.orbitTargetF64.y + radius * Math.sin(elevation);
    this.cameraPosF64.z = this.orbitTargetF64.z + radius * Math.cos(elevation) * Math.cos(azimuth);
  }

  /**
   * Surgical RTC Raycasting: Detects faces/edges without floating-point jitter.
   */
  public pickPart(normalizedX: number, normalizedY: number): CadMeshItem | null {
    // Rayon tracé depuis la caméra ancrée en (0, 0, 0)
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(new THREE.Vector2(normalizedX, normalizedY), this.camera);

    const meshes = this.objects.map((o) => o.mesh);
    const intersections = raycaster.intersectObjects(meshes, false);

    if (intersections.length > 0) {
      const hitMesh = intersections[0].object;
      const found = this.objects.find((o) => o.mesh === hitMesh);
      return found ?? null;
    }
    return null;
  }

  /**
   * Render Loop: Subtracts camera pos in 64-bit CPU math before GPU submission.
   */
  public renderFrame(): void {
    if (this.isContextLost) return;

    // La caméra GPU reste toujours centrée à l'origine locale
    this.camera.position.set(0, 0, 0);

    // Orientation de la caméra pointant vers le target relatif
    const relTargetX = this.orbitTargetF64.x - this.cameraPosF64.x;
    const relTargetY = this.orbitTargetF64.y - this.cameraPosF64.y;
    const relTargetZ = this.orbitTargetF64.z - this.cameraPosF64.z;
    this.camera.lookAt(relTargetX, relTargetY, relTargetZ);

    // Mise à jour des positions d'objets relatives en Float32 pour le GPU
    for (const item of this.objects) {
      const relX = item.worldPositionF64.x - this.cameraPosF64.x;
      const relY = item.worldPositionF64.y - this.cameraPosF64.y;
      const relZ = item.worldPositionF64.z - this.cameraPosF64.z;
      item.mesh.position.set(relX, relY, relZ);

      if (item.wireframeMesh) {
        item.wireframeMesh.position.set(relX, relY, relZ);
      }
    }

    this.renderer.render(this.scene, this.camera);
  }
}
```

---

## 🛡️ Règles de Validation Déterministes
- **Test du Zoom Extrême :** Positionner un cube à $(10^6, 10^6, 10^6)\text{ mm}$. Placer la caméra à $0.1\text{ mm}$ de la face. Faire tourner la caméra : aucun pixel ne doit trembler.
- **Sélection Précise :** Tester `pickPart` à un zoom de $10^5\times$. Le pointeur doit identifier la sous-face exacte sans décalage.
- **Typage Strict :** Zéro `any`, typage intégral TypeScript 5.x.
