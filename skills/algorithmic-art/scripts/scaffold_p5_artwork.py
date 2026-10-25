#!/usr/bin/env python3
"""
scaffold_p5_artwork.py — Deterministic scaffolder for interactive p5.js generative art artifacts.
Generates production-grade, gallery-quality HTML artifacts with Art Blocks seeded reproducibility,
interactive parameter sliders, seed cycling (prev/next/random/jump), palette selection, and PNG export.

Topologies supported:
  - flow-field        : Multi-octave Perlin / curl noise flow field with organic particle trails
  - strange-attractor : High-density Clifford / De Jong attractor in chaotic phase space
  - phyllotaxis       : Fermat spiral golden ratio botanical harmonics with wave pulsing
  - minimal           : Clean boilerplate with seeded loop, controls, and parameter wiring

Usage:
  python scaffold_p5_artwork.py --name "cosmic-turbulence" --topology flow-field --palette cyber-neon --output ./art
  python scaffold_p5_artwork.py --name "clifford-harmonics" --topology strange-attractor --with-philosophy

Author: Antigravity Agentic Super Suite
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import List, Dict

# Import palette generator if present
try:
    from generate_art_palette import build_palette, PRESET_THEMES
except ImportError:
    SCRIPTS_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(SCRIPTS_DIR))
    from generate_art_palette import build_palette, PRESET_THEMES

TOPOLOGIES = ["flow-field", "strange-attractor", "phyllotaxis", "minimal"]


def get_topology_code(topology: str, palette_colors: List[str]) -> Dict[str, str]:
    """Return parameters, controls HTML, and p5.js code for the given topology."""
    c1 = palette_colors[0] if len(palette_colors) > 0 else "#2e3440"
    c2 = palette_colors[1] if len(palette_colors) > 1 else "#88c0d0"
    c3 = palette_colors[2] if len(palette_colors) > 2 else "#d97757"

    if topology == "strange-attractor":
        params_js = f"""    seed: 42,
    numPoints: 80000,
    paramA: -1.4,
    paramB: 1.6,
    paramC: 1.0,
    paramD: 0.7,
    scale: 180,
    colorPalette: {json.dumps(palette_colors)}"""

        controls_html = """                <!-- Topology Parameters -->
                <div class="control-group">
                    <label>Point Density</label>
                    <input type="range" id="numPoints" min="20000" max="150000" step="5000" value="80000" oninput="updateParam('numPoints', this.value)">
                    <span class="value-display" id="numPoints-value">80000</span>
                </div>
                <div class="control-group">
                    <label>Parameter A (Curvature)</label>
                    <input type="range" id="paramA" min="-3.0" max="3.0" step="0.05" value="-1.4" oninput="updateParam('paramA', this.value)">
                    <span class="value-display" id="paramA-value">-1.4</span>
                </div>
                <div class="control-group">
                    <label>Parameter B (Folding)</label>
                    <input type="range" id="paramB" min="-3.0" max="3.0" step="0.05" value="1.6" oninput="updateParam('paramB', this.value)">
                    <span class="value-display" id="paramB-value">1.6</span>
                </div>
                <div class="control-group">
                    <label>Zoom Scale</label>
                    <input type="range" id="scale" min="80" max="350" step="10" value="180" oninput="updateParam('scale', this.value)">
                    <span class="value-display" id="scale-value">180</span>
                </div>"""

        algo_js = """        function setup() {
            let canvas = createCanvas(800, 800);
            canvas.parent('canvas-container');
            pixelDensity(2);
            initializeSystem();
            noLoop();
        }

        function initializeSystem() {
            randomSeed(params.seed);
            noiseSeed(params.seed);
            background(15, 15, 20);

            let x = 0.1;
            let y = 0.1;
            let cx = width / 2;
            let cy = height / 2;

            strokeWeight(0.6);
            loadPixels();

            for (let i = 0; i < params.numPoints; i++) {
                // Clifford Strange Attractor equations:
                // x_{n+1} = sin(a * y_n) + c * cos(a * x_n)
                // y_{n+1} = sin(b * x_n) + d * cos(b * y_n)
                let xNext = Math.sin(params.paramA * y) + params.paramC * Math.cos(params.paramA * x);
                let yNext = Math.sin(params.paramB * x) + params.paramD * Math.cos(params.paramB * y);
                x = xNext;
                y = yNext;

                let px = Math.floor(cx + x * params.scale);
                let py = Math.floor(cy + y * params.scale);

                if (px >= 0 && px < width && py >= 0 && py < height) {
                    let colIdx = (i % (params.colorPalette.length - 1)) + 1;
                    let c = color(params.colorPalette[colIdx]);
                    stroke(red(c), green(c), blue(c), 38);
                    point(px, py);
                }
            }
        }

        function draw() {
            // Static rendering for Clifford attractor
        }"""

    elif topology == "phyllotaxis":
        params_js = f"""    seed: 137,
    nodeCount: 1800,
    divergenceAngle: 137.508,
    spacing: 7.5,
    waveSpeed: 0.04,
    colorPalette: {json.dumps(palette_colors)}"""

        controls_html = """                <!-- Topology Parameters -->
                <div class="control-group">
                    <label>Node Count</label>
                    <input type="range" id="nodeCount" min="300" max="3500" step="50" value="1800" oninput="updateParam('nodeCount', this.value)">
                    <span class="value-display" id="nodeCount-value">1800</span>
                </div>
                <div class="control-group">
                    <label>Divergence Angle (°)</label>
                    <input type="range" id="divergenceAngle" min="137.0" max="138.0" step="0.005" value="137.508" oninput="updateParam('divergenceAngle', this.value)">
                    <span class="value-display" id="divergenceAngle-value">137.508</span>
                </div>
                <div class="control-group">
                    <label>Radial Spacing</label>
                    <input type="range" id="spacing" min="2.0" max="15.0" step="0.5" value="7.5" oninput="updateParam('spacing', this.value)">
                    <span class="value-display" id="spacing-value">7.5</span>
                </div>"""

        algo_js = """        let tOffset = 0;

        function setup() {
            let canvas = createCanvas(800, 800);
            canvas.parent('canvas-container');
            angleMode(DEGREES);
            initializeSystem();
        }

        function initializeSystem() {
            randomSeed(params.seed);
            noiseSeed(params.seed);
            tOffset = 0;
            loop();
        }

        function draw() {
            background(18, 19, 22, 45);
            translate(width / 2, height / 2);
            tOffset += params.waveSpeed;

            for (let n = 0; n < params.nodeCount; n++) {
                let phi = n * params.divergenceAngle;
                let r = params.spacing * Math.sqrt(n);
                let wave = Math.sin(n * 0.05 - tOffset) * 4.0;
                let x = (r + wave) * Math.cos(phi * Math.PI / 180);
                let y = (r + wave) * Math.sin(phi * Math.PI / 180);

                let palIdx = n % params.colorPalette.length;
                let c = color(params.colorPalette[palIdx]);
                let nodeSize = map(n, 0, params.nodeCount, 2, 7) + Math.cos(tOffset + n * 0.02) * 1.5;

                noStroke();
                fill(red(c), green(c), blue(c), 180);
                circle(x, y, Math.max(1, nodeSize));
            }
        }"""

    elif topology == "minimal":
        params_js = f"""    seed: 1234,
    complexity: 50,
    elementSize: 20,
    colorPalette: {json.dumps(palette_colors)}"""

        controls_html = """                <!-- Topology Parameters -->
                <div class="control-group">
                    <label>Complexity</label>
                    <input type="range" id="complexity" min="10" max="100" step="5" value="50" oninput="updateParam('complexity', this.value)">
                    <span class="value-display" id="complexity-value">50</span>
                </div>
                <div class="control-group">
                    <label>Element Size</label>
                    <input type="range" id="elementSize" min="5" max="80" step="2" value="20" oninput="updateParam('elementSize', this.value)">
                    <span class="value-display" id="elementSize-value">20</span>
                </div>"""

        algo_js = """        function setup() {
            let canvas = createCanvas(800, 800);
            canvas.parent('canvas-container');
            initializeSystem();
            noLoop();
        }

        function initializeSystem() {
            randomSeed(params.seed);
            noiseSeed(params.seed);
            background(245, 243, 238);

            for (let i = 0; i < params.complexity; i++) {
                let x = random(width * 0.1, width * 0.9);
                let y = random(height * 0.1, height * 0.9);
                let s = random(params.elementSize * 0.5, params.elementSize * 1.8);
                let col = color(params.colorPalette[i % params.colorPalette.length]);
                fill(red(col), green(col), blue(col), 160);
                stroke(20, 20, 20, 80);
                strokeWeight(1.5);
                circle(x, y, s);
            }
        }

        function draw() {
            // Custom algorithm rendering
        }"""

    else:
        # Default: Flow Field
        params_js = f"""    seed: 12345,
    particleCount: 2200,
    flowSpeed: 2.2,
    noiseScale: 0.0045,
    trailLength: 28,
    colorPalette: {json.dumps(palette_colors)}"""

        controls_html = """                <!-- Topology Parameters -->
                <div class="control-group">
                    <label>Particle Count</label>
                    <input type="range" id="particleCount" min="500" max="5000" step="100" value="2200" oninput="updateParam('particleCount', this.value)">
                    <span class="value-display" id="particleCount-value">2200</span>
                </div>
                <div class="control-group">
                    <label>Flow Speed</label>
                    <input type="range" id="flowSpeed" min="0.5" max="6.0" step="0.1" value="2.2" oninput="updateParam('flowSpeed', this.value)">
                    <span class="value-display" id="flowSpeed-value">2.2</span>
                </div>
                <div class="control-group">
                    <label>Noise Scale</label>
                    <input type="range" id="noiseScale" min="0.001" max="0.02" step="0.0005" value="0.0045" oninput="updateParam('noiseScale', this.value)">
                    <span class="value-display" id="noiseScale-value">0.0045</span>
                </div>
                <div class="control-group">
                    <label>Trail Longevity</label>
                    <input type="range" id="trailLength" min="5" max="60" step="2" value="28" oninput="updateParam('trailLength', this.value)">
                    <span class="value-display" id="trailLength-value">28</span>
                </div>"""

        algo_js = """        let particles = [];

        class Particle {
            constructor() {
                this.reset();
            }

            reset() {
                this.pos = createVector(random(width), random(height));
                this.prev = this.pos.copy();
                this.color = color(params.colorPalette[Math.floor(random(params.colorPalette.length))]);
                this.speed = params.flowSpeed * random(0.8, 1.3);
                this.life = random(params.trailLength * 0.8, params.trailLength * 1.5);
                this.maxLife = this.life;
            }

            update() {
                this.prev = this.pos.copy();
                let angle = noise(this.pos.x * params.noiseScale, this.pos.y * params.noiseScale) * TWO_PI * 4.0;
                let v = p5.Vector.fromAngle(angle).mult(this.speed);
                this.pos.add(v);
                this.life--;

                if (this.life <= 0 || this.pos.x < 0 || this.pos.x > width || this.pos.y < 0 || this.pos.y > height) {
                    this.reset();
                }
            }

            draw() {
                let alpha = map(this.life, 0, this.maxLife, 10, 180);
                stroke(red(this.color), green(this.color), blue(this.color), alpha);
                strokeWeight(1.2);
                line(this.prev.x, this.prev.y, this.pos.x, this.pos.y);
            }
        }

        function setup() {
            let canvas = createCanvas(800, 800);
            canvas.parent('canvas-container');
            initializeSystem();
        }

        function initializeSystem() {
            randomSeed(params.seed);
            noiseSeed(params.seed);
            background(20, 20, 24);
            particles = [];
            for (let i = 0; i < params.particleCount; i++) {
                particles.push(new Particle());
            }
            loop();
        }

        function draw() {
            // Subtle semi-transparent overlay to create fading trails
            background(20, 20, 24, 12);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
        }"""

    return {
        "params_js": params_js,
        "controls_html": controls_html,
        "algo_js": algo_js
    }


def generate_html_artwork(name: str, topology: str, palette_colors: List[str]) -> str:
    """Generate self-contained HTML artifact code."""
    topo = get_topology_code(topology, palette_colors)
    title = name.replace("-", " ").replace("_", " ").title()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Algorithmic Art</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Lora:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --anthropic-dark: #141413;
            --anthropic-light: #faf9f5;
            --anthropic-mid-gray: #b0aea5;
            --anthropic-light-gray: #e8e6dc;
            --anthropic-orange: #d97757;
            --anthropic-blue: #6a9bcc;
            --anthropic-green: #788c5d;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, var(--anthropic-light) 0%, #f5f3ee 100%);
            min-height: 100vh;
            color: var(--anthropic-dark);
        }}

        .container {{
            display: flex;
            min-height: 100vh;
            padding: 20px;
            gap: 20px;
        }}

        .sidebar {{
            width: 320px;
            flex-shrink: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(20, 20, 19, 0.1);
            overflow-y: auto;
            max-height: calc(100vh - 40px);
        }}

        .sidebar h1 {{
            font-family: 'Lora', serif;
            font-size: 24px;
            font-weight: 500;
            color: var(--anthropic-dark);
            margin-bottom: 6px;
        }}

        .sidebar .subtitle {{
            color: var(--anthropic-mid-gray);
            font-size: 13px;
            margin-bottom: 24px;
            line-height: 1.4;
        }}

        .control-section {{
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--anthropic-light-gray);
        }}

        .control-section:last-child {{
            border-bottom: none;
        }}

        .control-section h3 {{
            font-size: 15px;
            font-weight: 600;
            color: var(--anthropic-dark);
            margin-bottom: 14px;
        }}

        .seed-display {{
            background: var(--anthropic-light);
            border: 2px solid var(--anthropic-light-gray);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            font-family: monospace;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 12px;
        }}

        .button-row {{
            display: flex;
            gap: 8px;
            margin-bottom: 8px;
        }}

        .button {{
            flex: 1;
            padding: 8px 12px;
            background: var(--anthropic-orange);
            color: white;
            border: none;
            border-radius: 6px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        .button.secondary {{
            background: var(--anthropic-light-gray);
            color: var(--anthropic-dark);
        }}

        .button.secondary:hover {{
            background: var(--anthropic-mid-gray);
            color: white;
        }}

        .control-group {{
            margin-bottom: 14px;
        }}

        .control-group label {{
            display: block;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 6px;
        }}

        .control-group input[type="range"] {{
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: var(--anthropic-light-gray);
            outline: none;
            -webkit-appearance: none;
        }}

        .control-group input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: var(--anthropic-orange);
            cursor: pointer;
        }}

        .value-display {{
            display: inline-block;
            font-size: 12px;
            color: var(--anthropic-mid-gray);
            margin-top: 4px;
            font-family: monospace;
        }}

        .canvas-area {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: calc(100vh - 40px);
        }}

        #canvas-container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 15px 40px rgba(20, 20, 19, 0.15);
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        #canvas-container canvas {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar Controls -->
        <div class="sidebar">
            <h1>{title}</h1>
            <div class="subtitle">Autonomous Computational Aesthetics • Topology: {topology}</div>

            <!-- Seed Section (Reproducibility) -->
            <div class="control-section">
                <h3>Seed Navigation</h3>
                <div class="seed-display" id="seed-value">12345</div>
                <div class="button-row">
                    <button class="button secondary" onclick="previousSeed()">← Prev</button>
                    <button class="button secondary" onclick="nextSeed()">Next →</button>
                </div>
                <button class="button secondary" onclick="randomSeedAndUpdate()" style="width: 100%; margin-top: 4px;">↻ Random Seed</button>
            </div>

            <!-- Parameters Section -->
            <div class="control-section">
                <h3>Parameters</h3>
{topo['controls_html']}
            </div>

            <!-- Actions Section -->
            <div class="control-section">
                <h3>Actions</h3>
                <div class="button-row">
                    <button class="button" onclick="initializeSystem()">Regenerate</button>
                    <button class="button secondary" onclick="resetParameters()">Reset</button>
                </div>
                <div style="margin-top: 8px;">
                    <button class="button" onclick="downloadArtwork()" style="width: 100%; background: var(--anthropic-dark); color: white;">Download PNG</button>
                </div>
            </div>
        </div>

        <!-- Canvas Container -->
        <div class="canvas-area">
            <div id="canvas-container"></div>
        </div>
    </div>

    <script>
        // System Parameters
        let params = {{
{topo['params_js']}
        }};

        let defaultParams = JSON.parse(JSON.stringify(params));

        function updateParam(name, value) {{
            params[name] = parseFloat(value);
            let display = document.getElementById(name + '-value');
            if (display) display.textContent = value;
            initializeSystem();
        }}

        function updateSeedDisplay() {{
            let el = document.getElementById('seed-value');
            if (el) el.textContent = params.seed;
        }}

        function previousSeed() {{
            params.seed = Math.max(1, params.seed - 1);
            updateSeedDisplay();
            initializeSystem();
        }}

        function nextSeed() {{
            params.seed = params.seed + 1;
            updateSeedDisplay();
            initializeSystem();
        }}

        function randomSeedAndUpdate() {{
            params.seed = Math.floor(Math.random() * 999999) + 1;
            updateSeedDisplay();
            initializeSystem();
        }}

        function resetParameters() {{
            params = JSON.parse(JSON.stringify(defaultParams));
            for (let key in params) {{
                let input = document.getElementById(key);
                let display = document.getElementById(key + '-value');
                if (input) input.value = params[key];
                if (display) display.textContent = params[key];
            }}
            updateSeedDisplay();
            initializeSystem();
        }}

        function downloadArtwork() {{
            saveCanvas('{name}_seed_' + params.seed, 'png');
        }}

        // p5.js Core Generative Logic
{topo['algo_js']}

        window.addEventListener('load', function() {{
            updateSeedDisplay();
        }});
    </script>
</body>
</html>"""
    return html


def generate_philosophy_markdown(name: str, topology: str) -> str:
    """Generate Algorithmic Philosophy manifesto markdown."""
    title = name.replace("-", " ").replace("_", " ").title()
    content = f"""# Algorithmic Philosophy: {title}

## 🌌 The Computational Movement: *{title}*

In the intersection of mathematics and perception lies the aesthetic of **{title}**. Rather than depicting a static snapshot of nature or geometry, this work treats computing as an active medium of emergence—where determinism and stochastic variation dance in perpetual dialogue.

### 1. Vector Harmonics & Field Dynamics
The composition is governed by the principles of **{topology}**. At its core, the universe of this canvas is not empty space filled with objects, but an invisible manifold of vector potentials. Every coordinate point holds latent energy, guiding entities along mathematical contours that echo fluid dynamics, strange attractors, and natural growth laws.

### 2. Controlled Chaos & Seeded Reproducibility
Beauty in algorithmic art emerges not from unconstrained randomness, but from **finely tuned constraints**. Following the Art Blocks standard of generative craftsmanship, every single seed forms a deterministic parallel universe:
- The exact same seed will reproduce this harmonic state down to the individual sub-pixel.
- Minor parameter deviations introduce phase shifts, bifurcations, and cascading emergent structures.

### 3. Color Space & Chromatic Resonance
The color palette avoids arbitrary RGB randomness. Instead, it relies on calculated luminance gradients and complementary perceptual contrast. Faster entities burn with heightened luminosity, while dormant vectors settle into deep, tranquil atmospheric depths.

### 4. Expert Computational Craftsmanship
This algorithm represents the culmination of countless iterations—a master-level calibration of scale, damping, velocity, and boundary equilibrium. It invites the observer not merely to view a composition, but to explore an infinite parametric landscape where mathematics becomes living poetry.
"""
    return content


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Scaffold production-grade p5.js generative art artifacts."
    )
    parser.add_argument("--name", "-n", required=True, help="Artwork name / slug (e.g. 'organic-turbulence').")
    parser.add_argument("--topology", "-t", default="flow-field", choices=TOPOLOGIES, help="Generative mathematical topology.")
    parser.add_argument("--palette", "-p", default="cyber-neon", help="Color palette preset (or 'nordic-mist', 'japanese-woodblock', etc.).")
    parser.add_argument("--output", "-o", default=".", help="Target output directory.")
    parser.add_argument("--with-philosophy", action="store_true", help="Generate accompanying Algorithmic Philosophy markdown file.")

    args = parser.parse_args()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = args.name.lower().replace(" ", "-")
    palette_colors = build_palette(args.palette, 6, 210.0)

    html_code = generate_html_artwork(slug, args.topology, palette_colors)
    html_file = output_dir / f"{slug}.html"
    html_file.write_text(html_code, encoding="utf-8")
    print(f"[OK] Generated HTML Artwork: {html_file}")

    if args.with_philosophy:
        md_code = generate_philosophy_markdown(slug, args.topology)
        md_file = output_dir / f"{slug}_philosophy.md"
        md_file.write_text(md_code, encoding="utf-8")
        print(f"[OK] Generated Algorithmic Philosophy: {md_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
