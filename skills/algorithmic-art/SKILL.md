---
name: algorithmic-art
description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.
license: Complete terms in LICENSE.txt
---

# Algorithmic & Generative Art Guide

Algorithmic art is the expression of computational aesthetic movements through code. This skill guides the creation of gallery-grade generative art via **p5.js**, incorporating the **WAT (Workflows, Agents, Tools)** paradigm with deterministic Python utilities for palette generation, scaffolding, and quality gate auditing.

---

## 💡 Comprendre l'Art Algorithmique (Explication Simple pour un ado de 15 ans)

L'art algorithmique, c'est peindre avec des **mathématiques en mouvement** plutôt qu'avec un pinceau classique :
1. **Le Peintre Virtuel (L'Algorithme)** : Au lieu de dessiner chaque point à la main, tu inventes un ensemble de règles physiques (la gravité, des tourbillons de vent, des vagues sonores, des équations chaotiques).
2. **La Graine (`Seed`)** : C'est comme le **numéro d'un univers parallèle**. Si tu donnes la graine `12345`, l'ordinateur recréera exactement le même tableau au pixel près, à chaque fois. Si tu changes la graine à `12346`, l'univers change complètement.
3. **Le Chaos Contrôlé** : Ce n'est pas du bruit au hasard (le hasard pur donne un brouillard moche). C'est de l'émergence : des milliers de particules invisibles qui suivent un champ de vecteurs harmonieux pour former des soies, des galaxies ou des cristaux.
4. **Les Manettes (`Sliders`)** : L'œuvre n'est pas figée dans un musée : l'observateur peut faire varier la vitesse d'écoulement, le nombre de particules ou la courbure pour explorer l'univers de l'œuvre en direct.

---

## 🛠️ Outils Déterministes Inclus (WAT Toolkit)

Ce skill intègre une suite d'outils CLI déterministes situés dans `scripts/` :

### 1. Générateur de Palettes Harmoniques (`scripts/generate_art_palette.py`)
Calcule des palettes basées sur le Nombre d'Or ($H_{n+1} = (H_n + 0.618 \times 360) \pmod{360}$) et des harmonies de couleur :
```bash
# Générer une palette Cyber Neon au format JS
python scripts/generate_art_palette.py --scheme cyber-neon --count 6 --format js

# Générer une harmonie basée sur le nombre d'or avec teinte de base
python scripts/generate_art_palette.py --scheme golden-ratio --base-hue 210 --count 8 --format css
```

### 2. Échafaudeur d'Œuvres Interactives (`scripts/scaffold_p5_artwork.py`)
Génère instantanément un artefact HTML autonome complet (avec contrôles, navigation de graines et export PNG) :
```bash
# Topologies disponibles: flow-field, strange-attractor, phyllotaxis, minimal
python scripts/scaffold_p5_artwork.py --name "cosmic-drift" --topology flow-field --palette nordic-mist --output ./art

# Générer également le manifeste philosophique d'art algorithmique (.md)
python scripts/scaffold_p5_artwork.py --name "clifford-caustics" --topology strange-attractor --with-philosophy
```

### 3. Auditeur de Qualité & Conformité (`scripts/audit_p5_artwork.py`)
Vérifie la conformité aux standards de reproductibilité Art Blocks / fxhash :
```bash
python scripts/audit_p5_artwork.py path/to/artwork.html
# Audite : randomSeed(), détection de Math.random() interdit dans draw(), contrôles UI, fuites mémoires
```

### 4. Suite de Tests Automatisée (`scripts/tests/test_algorithmic_art.py`)
Exécute 10 tests unitaires complets en moins de 100ms :
```bash
python scripts/tests/test_algorithmic_art.py
```

---

## 🏛️ ALGORITHMIC PHILOSOPHY CREATION

To begin, create an ALGORITHMIC PHILOSOPHY (not static images or templates) that will be interpreted through:
- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation and controlled chaos

### THE CRITICAL UNDERSTANDING
- What is received: Subtle input or instructions by the user to take into account as a foundation without constraining creative freedom.
- What is created: An algorithmic philosophy / generative aesthetic movement (.md).
- What happens next: Express it in code—creating p5.js sketches that are 90% algorithmic generation, 10% essential parameters.

### HOW TO GENERATE AN ALGORITHMIC PHILOSOPHY
- **Name the movement** (1-2 words): "Organic Turbulence", "Quantum Harmonics", "Emergent Stillness", "Clifford Caustics".
- **Articulate the philosophy** (4-6 paragraphs): Describe computational processes, mathematical relationships, noise functions, particle behaviors, and emergent complexity.
- **Craftsmanship**: Emphasize meticulous optimization, mathematical calibration, and mastery of computational aesthetics.

---

## 🎨 P5.JS IMPLEMENTATION CONTRACT

### STEP 0: Read the Template First
- The template [`templates/viewer.html`](./templates/viewer.html) is the literal foundation.
- Keep all FIXED sections: Anthropic branding, sidebar layout, seed navigation (prev/next/random/jump), reset, regenerate, download PNG.
- Replace only the VARIABLE sections: p5.js algorithm, parameters object, and UI parameter sliders.

### Technical Requirements:
1. **Seeded Randomness (Art Blocks Pattern)**:
   ```javascript
   function initializeSystem() {
       randomSeed(params.seed);
       noiseSeed(params.seed);
   }
   ```
2. **Ban `Math.random()` in Generative Logic**: Never use `Math.random()` inside `draw()`, `setup()`, or particle loops. Only use seeded `random()`.
3. **Single Self-Contained HTML File**: All styles, scripts, and p5.js CDN links must be embedded in a single file that runs immediately in any browser or artifact viewer.
4. **Performance & Memory**: Prune dead particles, avoid recreating offscreen graphics buffers inside `draw()`, and scale canvas with `pixelDensity(2)` for high-DPI clarity.

---

## 📖 In-Depth Mathematical Reference
For advanced formulations on Curl Noise, Clifford Strange Attractors, Fibonacci Phyllotaxis, and Gray-Scott Reaction-Diffusion models, consult the [Master Computational Art Playbook](./references/computational_art_playbook.md).
