# Master Computational Art Playbook

> **Scope**: Mathematical foundations, algorithmic topologies, seeded determinism, and performance engineering for gallery-grade p5.js generative art.

---

## 1. 🌌 The 6 Mathematical Foundations of Computational Art

True algorithmic craftsmanship goes far beyond simple random geometry. It orchestrates physical, trigonometric, and chaotic equations to produce emergent visual resonance.

### 1.1 Vector Fields & Curl Noise
Standard Perlin noise creates directional clustering with convergence and divergence points (sinks and sources). For fluid, smoke-like motion without unnatural particle clumpings, **Curl Noise** calculates the analytical curl of a 2D scalar potential field $\psi(x, y)$:

$$\vec{v} = \nabla \times \psi = \left( \frac{\partial \psi}{\partial y}, -\frac{\partial \psi}{\partial x} \right)$$

Because $\nabla \cdot (\nabla \times \psi) \equiv 0$, the resulting velocity field is **strictly incompressible** (divergence-free), creating organic eddy currents and turbulence reminiscent of natural fluid mechanics.

### 1.2 Strange Attractors in Chaotic Phase Space
Strange attractors visualize the long-term orbits of non-linear iterative systems. Even when trajectories never repeat and remain bounded, they trace intricate, fractal filaments:

#### The Clifford Attractor
Defined by two iterative trigonometric equations:
$$x_{n+1} = \sin(a \cdot y_n) + c \cdot \cos(a \cdot x_n)$$
$$y_{n+1} = \sin(b \cdot x_n) + d \cdot \cos(b \cdot y_n)$$

- **Curvature parameter $a$**: Controls the degree of orbital twisting.
- **Folding parameter $b$**: Controls topological layering.
- **Coefficients $c, d$**: Dictate the balance between circular and hyperbolic deformation.
- **Rendering**: Accumulating 100,000+ semi-transparent points (`alpha: 20-40`) onto a dark canvas produces celestial silk-like caustics.

#### The De Jong Attractor
$$x_{n+1} = \sin(a \cdot y_n) - \cos(b \cdot x_n)$$
$$y_{n+1} = \sin(c \cdot x_n) - \cos(d \cdot y_n)$$

---

### 1.3 Natural Morphogenesis & Phyllotaxis
Plant leaf arrangements, sunflower seed packing, and pinecone spirals follow the **golden ratio** $\phi \approx 1.6180339887$:

$$\theta_n = n \times 137.50776405^\circ \quad (\text{Golden Angle})$$
$$r_n = c \cdot \sqrt{n}$$

By modulating the radius $r_n$ with trigonometric phase waves ($\sin(\omega t + k n)$), the static botanical spiral transforms into dynamic pulsing ripples, breathing like living sea flora.

---

### 1.4 Spatial Partitioning & Circle Packing
Organic cellular structures rely on collision detection and relaxation:
- **Poisson Disk Sampling** (Bridson's algorithm): Produces tightly packed points with a guaranteed minimum distance $r$, eliminating the visual clustering of pure uniform randomness.
- **Iterative Circle Packing**: Circles grow until touching neighbors or canvas boundaries, generating natural skin, sponge, or cobblestone textures.

---

### 1.5 Reaction-Diffusion (Gray-Scott Model)
Simulates two virtual chemical substances ($U$ and $V$) diffusing across a 2D grid and reacting:
$$\frac{\partial U}{\partial t} = D_u \nabla^2 U - UV^2 + F(1 - U)$$
$$\frac{\partial V}{\partial t} = D_v \nabla^2 V + UV^2 - (F + k)V$$

- Varying the feed rate $F$ and kill rate $k$ produces leopard spots, zebra stripes, coral branches, and dividing cellular colonies.

---

### 1.6 Harmonic Interference & Wave Resonance
- **Chladni Plate Nodes**: Standing wave nodal lines produced by two-dimensional vibrational modes:
$$w(x, y) = a \sin\left(\frac{n \pi x}{L}\right) \sin\left(\frac{m \pi y}{L}\right) - b \sin\left(\frac{m \pi x}{L}\right) \sin\left(\frac{n \pi y}{L}\right) = 0$$
- Visualizing particles settling exclusively onto nodal lines creates sacred acoustic mandalas.

---

## 2. 🎲 The Reproducibility Contract (Art Blocks / fxhash Standard)

In commercial generative art platforms (Art Blocks, fxhash, Verse), **a single seed must always reproduce the exact same artwork byte-for-byte**.

```
┌────────────────────────────────────────────────────────┐
│             SEED INPUT (e.g. 12345 or Hash)            │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
   randomSeed(params.seed)      noiseSeed(params.seed)
             │                           │
             ▼                           ▼
    Deterministic Vectors       Deterministic Noise
             │                           │
             └─────────────┬─────────────┘
                           ▼
          Pixel-Identical Output Across Browsers
```

### ⚠️ Strict Rules for Seeded Determinism
1. **Never use `Math.random()` in drawing loops**: Using `Math.random()` inside `setup()`, `draw()`, or particle constructors ruins reproducibility. Only use p5's `random()`, which obeys `randomSeed()`.
   *(Exception: `Math.random()` is only permissible in UI event handlers to pick a new integer seed for the user).*
2. **Deterministic Arrays**: Initialize arrays in deterministic order; never rely on non-deterministic asynchronous callbacks during generation.
3. **Floating Point Precision**: Keep coordinate math within standard IEEE 754 precision; avoid accumulating unchecked rounding drifts in iterative loops.

---

## 3. 🎨 Perceptual Color Theory & Luminance Ramps

Garish, randomly chosen RGB colors are the hallmark of amateur code art. Gallery-quality generative art uses mathematically calibrated color spaces.

### 3.1 Golden Ratio Hue Distribution
To generate $N$ colors that feel distinct yet naturally balanced, increment the hue by the golden ratio conjugate:
$$H_{n+1} = (H_n + 0.618033988749895 \times 360^\circ) \pmod{360^\circ}$$

### 3.2 Luminance Ramps & Depth
Flat colors make complex generative structures look like 2D stickers. Instead, modulate lightness and alpha:
- **Fast vs Slow Particles**: Fast entities burn with higher lightness ($L = 0.85$) and lower alpha; slow particles settle with deeper saturation and higher opacity.
- **Additive Blending**: Use `blendMode(ADD)` or `blendMode(SCREEN)` against pure black backgrounds (`background(10, 10, 14)`) to achieve ethereal glowing energy fields.

---

## 4. ⚡ Performance & Memory Engineering

Generative art frequently computes tens of thousands of particles in real time. Poor memory habits cause frame rate drops and browser tab crashes:

### 4.1 Particle Array Pruning
Never execute `particles.push(new Particle())` in `draw()` without strict lifespans and bounds checking:
```javascript
// DO: In-place recycling or strict filtering
for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    if (particles[i].isDead()) {
        particles.splice(i, 1); // Or better: particle.reset() in-place!
    }
}
```

### 4.2 Avoid Dynamic Buffer Allocations
Never call `createGraphics()` inside the `draw()` loop. Allocate offscreen buffers once in `setup()` and reuse them.

### 4.3 High-DPI Display Scaling
For ultra-sharp gallery viewing on 4K / Retina screens:
```javascript
function setup() {
    let canvas = createCanvas(1080, 1080);
    pixelDensity(2); // Sharp 2x rendering
}
```

---

## 5. 🛠️ Deterministic Tooling Reference (WAT Framework)

This skill provides 3 production CLI scripts:

```bash
# 1. Generate harmonious color palettes
python scripts/generate_art_palette.py --scheme cyber-neon --count 6 --format js

# 2. Scaffold gallery-ready interactive p5.js artwork
python scripts/scaffold_p5_artwork.py --name "curl-vortices" --topology flow-field --palette nordic-mist --with-philosophy

# 3. Audit compliance, seeded determinism, and performance
python scripts/audit_p5_artwork.py path/to/artwork.html
```
