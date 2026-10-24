# Three.js PBR & WebGL Lighting Master Cheat Sheet

This reference details the production settings, lighting ratios, tone mapping calibrations, and visual artifact remedies required for high-end WebGL 3D scenes.

---

## 1. Renderer Baseline Setup

```javascript
import * as THREE from 'three';

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  powerPreference: 'high-performance'
});

// 1. Output Color Space (r152+ standard)
renderer.outputColorSpace = THREE.SRGBColorSpace;

// 2. High-DPI Clamping (CRITICAL: prevents GPU fillrate choke on 3x/4x mobile screens)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

// 3. Cinematic Tone Mapping (prevents blown-out white specular highlights)
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

// 4. Physical Shadow Maps
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
```

---

## 2. Tone Mapping Comparisons

| Tone Mapping | Visual Characteristic | Best For |
|---|---|---|
| `THREE.ACESFilmicToneMapping` | High contrast, saturated filmic curve, smooth shoulder roll-off on highlights. | Photorealistic environments, cinematic lighting, outdoor sun. |
| `THREE.AgXToneMapping` | Broad dynamic range, gentle desaturation on extreme highlights (Blender 4.0+ default). | Scientific models, architectural interiors, high-emission scenes. |
| `THREE.NeutralToneMapping` | Preserves exact albedo colors without contrast tinting. | Product showcase, e-commerce, accurate brand color reproduction. |
| `THREE.NoToneMapping` | Direct linear output (highlights clip harshly at 1.0). | Pure diagrammatic / flat shaded UI only. |

---

## 3. Top 5 WebGL Visual Artifacts & Remedies

### 1. Shadow Acne vs Peter Panning
- **Symptom**: Dark zebra stripes across curved surfaces (acne), or shadows detaching and floating away from feet (peter panning).
- **Remedy**:
  ```javascript
  directionalLight.shadow.bias = -0.0001;        // Eliminates shadow detachment
  directionalLight.shadow.normalBias = 0.05;     // Offsets depth along surface normal (cures acne)
  directionalLight.shadow.mapSize.set(2048, 2048);
  ```

### 2. Z-Fighting (Flickering Co-planar Surfaces)
- **Symptom**: Surfaces flicker violently when viewed at distance or shallow angles.
- **Remedy**:
  - Keep `camera.near` as large as possible ($\ge 0.1$, never $0.001$).
  - Keep `far / near` ratio under $50,000$.
  - Enable `logarithmicDepthBuffer: true` in `WebGLRenderer` only when massive open-world scales are unavoidable.

### 3. Washed-Out / Milky Textures
- **Symptom**: Albedo textures look pale or overexposed compared to their Photoshop/PNG source.
- **Remedy**:
  ```javascript
  const textureLoader = new THREE.TextureLoader();
  const diffuseMap = textureLoader.load('diffuse.png');
  diffuseMap.colorSpace = THREE.SRGBColorSpace; // Diffuse/Albedo MUST be sRGB!

  const normalMap = textureLoader.load('normal.png');
  normalMap.colorSpace = THREE.NoColorSpace;   // Data maps (Normal, Roughness, Metalness) MUST be Linear!
  ```

### 4. Physics & Animation Explosion on Tab Backgrounding
- **Symptom**: When the user switches browser tabs and returns, particles shoot into deep space or animations jump uncontrollably.
- **Remedy**:
  ```javascript
  function animate() {
    requestAnimationFrame(animate);
    const rawDelta = clock.getDelta();
    const dt = Math.min(rawDelta, 0.1); // Clamp delta time to maximum 100ms
    updatePhysics(dt);
    renderer.render(scene, camera);
  }
  ```

### 5. Memory Leaks on Component Unmount
- **Symptom**: Tab RAM grows indefinitely on route navigation or scene reload until browser tab crashes (`WebGL context lost`).
- **Remedy**:
  ```javascript
  function disposeHierarchy(node) {
    if (node.geometry) node.geometry.dispose();
    if (node.material) {
      if (Array.isArray(node.material)) node.material.forEach(disposeMaterial);
      else disposeMaterial(node.material);
    }
  }

  function disposeMaterial(mat) {
    mat.dispose();
    for (const key of Object.keys(mat)) {
      const val = mat[key];
      if (val && typeof val.dispose === 'function') val.dispose();
    }
  }
  ```
