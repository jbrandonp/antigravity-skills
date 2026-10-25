---
name: typeui-design-systems
description: Curated registry of 67 distinct design system themes (bento, brutalism, neobrutalism, claymorphism, glassmorphism, neumorphism, editorial, retro, corporate, matrix, etc.) with pre-defined color palettes, typography scales, spacing tokens, and component guidelines. Use when styling a new web application, choosing a visual identity, or generating themed UI components.
license: MIT
metadata:
  author: typeui.sh & bergside
---

# TypeUI Design Systems Registry (67 Themes)

Universal catalog of 67 pre-compiled, implementation-ready design system blueprints. Each theme defines strict color tokens, typography scales, border radii, spacing rhythm, and component behavior.

## How to Apply a Theme

When the user asks for a specific visual style or when designing an interface:
1. **Identify the Theme**: Match the subject matter or user request against the 67 themes listed below.
2. **Load Theme Tokens**: Read `./references/themes/<theme>/DESIGN.md` for exact hex colors, typography scale, spacing tokens, and radius rules.
3. **Execute CLI (Optional)**: In projects using `typeui`, pull the tokens directly via:
   ```bash
   npx typeui.sh pull <theme-name>
   ```
4. **Enforce Foundations**: Pair with `typeui-fundamentals` for WCAG 2.2 AA accessibility, contrast ratios, and interaction laws.

---

## The 67 Design System Themes

### 🍱 Modern, Minimal & Grid-Based
- **`bento`** : Modular grid layout with card-like blocks, clear hierarchy, and soft spacing.
- **`clean`** : Simplicity-focused design with generous whitespace and restrained palette.
- **`minimal`** : Stripped-back design emphasizing whitespace, clean typography, and zero clutter.
- **`spacious`** : Generous padding and consistent breathing room for readable interfaces.
- **`contemporary`** : Current-era minimalist design with bento grids, dark mode, and high performance.
- **`sleek`** : Polished modern minimalist aesthetic with refined lines and subtle interactions.
- **`square`** : Delicate typography, sharp edges, and minimal high-end layouts.

### 🏛️ Editorial & Print-Inspired
- **`editorial`** : Magazine-inspired layout with refined serif typography and structured columns.
- **`basic`** : Print-inspired visual language for books, magazines, and technical reports.
- **`modern`** : Contemporary editorial style with high-contrast serif headlines.
- **`paper`** : Tactile paper-textured design with warm off-white surfaces and ink tones.
- **`refined`** : Sophisticated, understated minimal luxury with classic typography.
- **`terracotta`** : Sun-baked clay-toned editorial interface on warm cream surfaces.
- **`claude`** : Research-journal aesthetic on warm stone, authoritative and almost achromatic.

### ⚡ Bold, Brutalist & Utilitarian
- **`brutalism`** : Raw, concrete-inspired anti-design with unadorned elements and jarring layouts.
- **`neobrutalism`** : Modern brutalism with heavy black borders, vivid accent colors, and high contrast.
- **`bold`** : Heavyweight typography, high-contrast colors, and commanding visual presence.
- **`dramatic`** : High-contrast, theatrical design with unconventional composition.
- **`power`** : High-end dark aesthetic with bold typography for commanding brands.
- **`mono`** : Monospace-driven, high-density matrix interface for developer and terminal tools.

### 🔮 Futuristic, Cyber & Sci-Fi
- **`matrix`** : Cyber-slick, dark-only green digital terminal interface.
- **`cosmic`** : Sci-fi aesthetic with deep dark themes, neon accents, and spatial depth.
- **`futuristic`** : Forward-looking design with tech typography and sleek innovation cues.
- **`neon`** : Electric glow effects and high-contrast vibrant pairings.
- **`codex`** : Radically minimal, edge-to-edge blank canvas with near-zero chrome.

### 🕹️ Retro, Nostalgic & Pixel Art
- **`retro`** : 1970s-1980s throwback typography with warm nostalgic palettes.
- **`vintage`** : 1950s-1990s nostalgia with skeuomorphic touches and grainy textures.
- **`dithered`** : Dot-pattern retro rendering simulating shades with a restricted palette.
- **`riso`** : Two-color risograph print aesthetic on warm off-white paper.
- **`pacman`** : 8-bit retro arcade design with pixel fonts and dotted borders.
- **`sega`** : 16-bit arcade-inspired interface with hard 0px borders and VT323 pixel type.
- **`tetris`** : Classic block-game design with high-energy colorful modules.

### 🫧 Materiality, Depth & Skeuomorphism
- **`glassmorphism`** : Frosted glass effects with translucent blur layers and luminous borders.
- **`claymorphism`** : Soft, rounded 3D clay shapes with puffy, friendly elements.
- **`neumorphism`** : Soft extruded monochromatic surfaces with tactile inner/outer shadows.
- **`skeuomorphism`** : Real-world physical textures, metallic bevels, and tactile depth.
- **`perspective`** : Isometric views and layered spatial depth with vanishing points.

### 🎨 Creative, Expressive & Playful
- **`artistic`** : Expressive typography, high-contrast vibrant accents, and creative freedom.
- **`colorful`** : Vibrant, cheerful gradients and high-energy surfaces.
- **`vibrant`** : Dynamic visual energy with playful typography and bold warm accents.
- **`creative`** : Character-driven illustrations and expressive layouts for landing pages.
- **`doodle`** : Hand-drawn sketch style with imperfect lines and informal warmth.
- **`sketch`** : Pencil-drawn aesthetic on warm cream paper.
- **`lingo`** : Playful, rounded shapes with tactile 3D borders (Duolingo-inspired).
- **`fiction`** : Cartoonesque children's-book illustration aesthetic.
- **`fantasy`** : RPG-inspired fantasy aesthetic with rich palettes and thematic borders.
- **`cafe`** : Cozy coffee-shop interface with warm earthy tones and relaxed spacing.

### 💼 Enterprise, Data & Systems
- **`enterprise`** : Dark-themed cloud dashboard with modular grids and glass panels.
- **`corporate`** : Professional, structured, trustworthy enterprise layouts.
- **`professional`** : Polished business-ready UI with conservative typography.
- **`ant`** : Ant Design inspired enterprise system emphasizing data density.
- **`material`** : Google Material Design 3 with dynamic theming and layered surfaces.
- **`shadcn`** : Minimal monochrome utility-first design system with accessible components.
- **`stitch`** : High-contrast enterprise design for data workflows and node graphs.
- **`roku`** : Developer-first purple dashboard with card-based top navigation.
- **`agentic`** : Conversational AI-first interface with minimal controls and task flow cards.
- **`pulse`** : Thick borders, geometric cards, and high-contrast metrics.
- **`levels`** : Conversion-optimized landing page structure removing user friction.
- **`storytelling`** : Narrative-driven sequential layout guiding users emotionally.
- **`immersive`** : Exhibit-style interactive interface blending animation and gamification.
- **`geometric`** : Precise geometric shapes, structured grids, and clean neutral palettes.
- **`friendly`** : Approachable, pastel, rounded UI for consumer-facing apps.
- **`gradient`** : Smooth, luminous gradient transitions for modern tech products.
- **`impeccable`** : Alternating cream and black editorial poster aesthetic.

---

## Conflict Resolution & Priority Rules
1. **Tokens (`DESIGN.md`)**: Concrete values (colors, spacing, typography scales) always come from the chosen theme.
2. **Accessibility**: WCAG 2.2 AA (from `typeui-fundamentals`) always overrides purely aesthetic styling if a color contrast fails.
3. **Component Architecture**: Pair with `shadcn` or `frontend-design` for component markup.

---

## 🎨 Presentation Slide Decks & Document Themes (Theme Factory)

For presentation slide decks, PDF reports, or executive documents, reference the visual showcase in `./references/theme-showcase.pdf` or apply one of the 10 foundational presentation themes:

1. **Ocean Gradient**: Deep navy `#0f172a`, cyan `#06b6d4`, white `#ffffff` (Tech, SaaS, Data).
2. **Warm Editorial**: Cream `#fefae0`, terracotta `#bc6c25`, dark earth `#283618` (Articles, Strategy).
3. **Executive Slate**: Charcoal `#1e293b`, silver `#94a3b8`, electric blue `#3b82f6` (Board meetings).
4. **Neon Matrix**: Deep black `#09090b`, emerald `#10b981`, lime `#84cc16` (Security, Developer tools).
5. **Nordic Frost**: Snow `#f8fafc`, ice blue `#38bdf8`, midnight `#0369a1` (Healthcare, Clean tech).
6. **Crimson Authority**: White `#ffffff`, crimson `#dc2626`, charcoal `#18181b` (Finance, Legal, Urgency).
7. **Monochrome Luxury**: Pure black `#000000`, white `#ffffff`, neutral gold `#d4af37` (Fashion, High-end).
8. **Sunset Warmth**: Plum `#581c87`, amber `#f59e0b`, rose `#f43f5e` (Creative, Media, Marketing).
9. **Forest Canopy**: Deep pine `#064e3b`, sage `#10b981`, warm sand `#fef3c7` (Sustainability, Nature).
10. **Cyberpunk Violet**: Dark purple `#2e1065`, fuchsia `#d946ef`, cyan `#06b6d4` (Gaming, Web3, Creative).


---

## 🧒 Explication Pédagogique (Style 15 ans)

Un Système de Design (*Design System*), c'est la charte graphique complète d'un jeu vidéo ou d'une marque :
1. **La Cohérence Visuelle** : Si ton bouton "Valider" a des coins arrondis doux et du bleu pastel, ton bouton "Annuler" ne doit pas être un rectangle noir agressif avec des ombres dures. Tout doit parler la même langue visuelle.
2. **Les 67 Thèmes Prêts à l'Emploi** : Chaque thème a une personnalité : le style **Bento** ressemble aux cartes élégantes d'Apple, le **Neobrutalisme** ressemble à une bande dessinée punk avec des contours noirs épais et des ombres tranchées, et le **Glassmorphism** ressemble à du verre dépoli semi-transparent.

---

## 🛠️ Outil Déterministe : `export_theme_css.py`
Exporte instantanément les variables CSS d'un thème sans dépendance externe :
```bash
python scripts/export_theme_css.py --theme bento --out src/theme.css
```
