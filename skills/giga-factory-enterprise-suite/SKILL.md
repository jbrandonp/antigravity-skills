---
name: giga-factory-enterprise-suite
description: >-
  Hermes Giga-Factory Enterprise Delivery Suite: High-conversion landing page design, brand identity systems, legal contracts & corporate governance, and end-to-end game production pipelines.
version: 2.0.0
tags:
  - gigafactory
  - enterprise
  - legal
  - branding
  - landing-page
  - production
merged_member_skills:
  - giga-brand-toolkit (08_Hermes_GigaFactory_Skills\giga-brand-toolkit\SKILL.md)
  - giga-game-pipeline (08_Hermes_GigaFactory_Skills\giga-game-pipeline\SKILL.md)
  - giga-landing-page (08_Hermes_GigaFactory_Skills\giga-landing-page\SKILL.md)
  - giga-legal-contracts (08_Hermes_GigaFactory_Skills\giga-legal-contracts\SKILL.md)
  - giga-legal-corporate (08_Hermes_GigaFactory_Skills\giga-legal-corporate\SKILL.md)
---

# Giga Factory Enterprise Suite

> **Master Suite Consolidée :** Regroupe et unifie **5 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[giga-brand-toolkit](#module-1-giga-brand-toolkit)** : Suite complète de développement de marque — 15 phases couvrant positionnement, identité, voix, visuel, contenu, stratégie. v2.1 ajoute design tokens CSS/JSON, dark mode palette, MVP Brand mode, trademark disclaimer légal, revision cascade protocol, format de sortie Brand Book HTML.
2. **[giga-game-pipeline](#module-2-giga-game-pipeline)** : Pipeline complet de développement de jeux vidéo Godot 4 — de la conception (GDD) au déploiement (Steam/itch.io). Architecture solo-dev, 8 phases, assets CC0.
3. **[giga-landing-page](#module-3-giga-landing-page)** : Landing page complète — hero, features, pricing, FAQ, analytics, SEO, waitlist et déploiement
4. **[giga-legal-contracts](#module-4-giga-legal-contracts)** : >-
5. **[giga-legal-corporate](#module-5-giga-legal-corporate)** : >-

---

## Module 1: `giga-brand-toolkit`

- **Origine :** `08_Hermes_GigaFactory_Skills\giga-brand-toolkit\SKILL.md`
- **Rôle / Objectif :** Suite complète de développement de marque — 15 phases couvrant positionnement, identité, voix, visuel, contenu, stratégie. v2.1 ajoute design tokens CSS/JSON, dark mode palette, MVP Brand mode, trademark disclaimer légal, revision cascade protocol, format de sortie Brand Book HTML.

## giga-brand-toolkit — Brand Development Suite v2.1.0

### Core Principle
NEVER from scratch — always use existing boilerplate (Platforms Starter Kit, Makerkit) and configure via giga-configure.

---

### Phase 0: Orchestration Layer *(NEW in v2.0)*

#### Dependency Graph
```
Phase 1 (Naming)
   └─► Phase 2 (Positioning)
         ├─► Phase 3 (Values)
         │      └─► Phase 4 (Story)
         │             └─► Phase 5 (Tagline) ◄── [2, 4]
         ├─► Phase 6 (Tone of Voice) ◄── [2, 3]
         │      ├─► Phase 7 (Messaging Matrix) ◄── [2, 6]
         │      │      └─► Phase 8 (Pitch) ◄── [2, 3, 4, 5, 6, 7]
         │      ├─► Phase 13 (Content Strategy) ◄── [2, 6, 7]
         │      └─► Phase 15 (Social Media) ◄── [6, 13]
         ├─► Phase 9 (Visual Identity)
         │      └─► Phase 10 (Color Palette)
         │             └─► Phase 11 (Logo) ◄── [9, 10]
         │                    └─► Phase 12 (Brand Book) ◄── [ALL 1–11]
         └─► Phase 14 (SEO) ◄── [2, external site context]
```

#### Execution Modes

| Mode | Phases incluses | Usage |
|------|----------------|-------|
| **Full Brand Build** | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15 | Lancement de marque complet |
| **MVP Brand** *(NEW v2.1)* | 2 → 5 → 6 → 9 → 10 | Lancement rapide — l'essentiel uniquement. Skip naming (utilise nom provisoire), skip valeurs/story/pitch/book/content/SEO/social. Output : positioning + tagline + tone + design tokens livrables |
| **Foundation Only** | 1 → 2 → 3 → 4 → 5 → 6 | Socle narratif avant design |
| **Visual Track** | 9 → 10 → 11 (nécessite Phase 2 en input) | Identité visuelle seulement |
| **Go-to-Market** | 7 → 8 → 13 → 14 → 15 (nécessite Phase 2 + 6 en input) | Activation marché |

#### Règle d'exécution
**Ne jamais lancer une phase sans que ses dépendances soient en statut PASS.**
Si une phase upstream est en FAIL → bloquer et signaler avant de continuer.

---

### Phase 1: Brand Name Generation

**Purpose** — Generate distinctive brand names by combining linguistic roots, semantics, and phonetics from specified language pairs or style combinations.

**Agent hint:** temperature 0.7 — phase créative.

**Inputs:**
- industry
- brand_attributes (list, e.g. ["trust", "speed", "global"])
- linguistic_combination (e.g. "Greek + Modern English")
- target_audience

**Fallback:**
- Si `brand_attributes` vide → défaut : ["trust", "quality", "innovation"]
- Si `linguistic_combination` non spécifié → défaut : "Latin + Modern English"

**Outputs:**
- 10 brand names avec étymologie, phonétique, rationale stratégique

**Steps:**
1. **Root Mining** — Extract 5–10 morphemes from each language in the specified combination
2. **Blending** — Combine roots following phonetic euphonics (avoid hard consonant clusters)
3. **Trademark Pre-Check** — Flag names likely to collide with existing marks based on obvious conflicts (same industry, phonetic similarity to major brands).
   **⚠️ DISCLAIMER LÉGAL — LIRE OBLIGATOIREMENT :** Cette étape est un heuristique créatif uniquement. Elle **NE remplace PAS** une recherche dans les bases officielles (EUIPO, USPTO, WIPO, INPI, BOPI). **Ne jamais affirmer qu'un nom est « libre », « disponible » ou « non protégé ».** L'IA n'a pas accès à ces bases et peut halluciner une marque comme libre alors qu'elle est déposée. Risque juridique direct en cas de contrefaçon. **Toujours inclure dans l'output la mention : « Vérification trademark par un avocat spécialisé requise avant tout dépôt. »**
4. **Audience Test Fit** — Score each name against target audience associations and pronunciation ease
5. **Top 10 Selection** — Rank by distinctiveness + meaning + ease of pronunciation

**Example output format:**
| # | Name | Linguistic Origin | Meaning | Why It Works |
|---|------|-------------------|---------|--------------|
| 1 | Veridium | Latin "veritas" + "-ium" | "Truth + Element" | Trust implied, scientific sound suits fintech |

**✅ Quality Gate**
- [ ] Exactement 10 noms générés
- [ ] Chaque nom a : origine linguistique, signification, rationale
- [ ] Au moins 1 risque trademark flaggé si pertinent
- [ ] Colonne "Why It Works" présente pour chaque nom
- [ ] ⚠️ **Disclaimer légal présent dans l'output** — « Vérification trademark par un avocat spécialisé requise avant tout dépôt »

→ FAIL → re-run Steps 3–5 avec inputs corrigés.

---

### Phase 2: Brand Positioning (What / For Whom / Why)

**Purpose** — Define the brand's unique space in the market using the **What / For Whom / Why** framework.

**Agent hint:** temperature 0.3 — phase analytique.

**Inputs:**
- brand_name
- product_or_service_description
- target_customer_segments
- competitive_landscape (list of competitors)
- key_differentiators

**Fallback:**
- Si `competitive_landscape` vide → exécuter positionnement générique par catégorie + noter la lacune dans l'output

**Outputs:**
- 1-paragraph Positioning Statement
- Positioning Matrix (What / For Whom / Why)
- Competitive Differentiation Map

**Steps:**
1. **Define What** — Articulate the brand's core competency in one sentence
2. **Define For Whom** — Primary target audience with demographic and psychographic detail
3. **Define Why** — Emotional + functional reasons customers choose this brand
4. **Build Positioning Statement** — Brand X is [category] for [audience] who want [benefit]. Unlike [competitors], brand provides [differentiators].
5. **Create Differentiation Map** — Feature comparison matrix against 2–3 key competitors

**✅ Quality Gate**
- [ ] Positioning Statement est exactement 1–2 phrases
- [ ] Contient les 4 éléments : [category], [audience], [benefit], [differentiator]
- [ ] Matrice de différenciation a ≥ 2 concurrents comparés

→ FAIL → re-run Steps 4–5.

---

### Phase 3: Brand Values

**Purpose** — Codify the brand's 3–5 core values with behavioural anchors, cultural manifestations, and hiring/partnership implications.

**Inputs:**
- brand_name
- brand_origin_story
- founder_beliefs
- team_culture_description
- industry_norms_to_challenge

**Fallback:**
- Si `founder_beliefs` non disponibles → extraire les valeurs implicites depuis `product_or_service_description` (Phase 2)

**Outputs:**
- 3–5 core values with name + one-line definition
- Behavioural anchors per value ("In action" vs "Not this")
- Anti-values (what we are NOT)
- Culture code impact

**Steps:**
1. **Extract Values** — From founder beliefs and origin story, distill 3–5 fundamental principles
2. **Define Each Value** — Name, one-line essence, 1-sentence elaboration
3. **Add Behavioural Anchors** — What each value looks like in action vs what it explicitly is NOT
4. **Define Anti-Values** — 3 items the brand explicitly rejects
5. **Create Culture Code Manifestations** — How values show up in onboarding, evaluations, decision frameworks

**✅ Quality Gate**
- [ ] Entre 3 et 5 valeurs (pas moins, pas plus)
- [ ] Chaque valeur a : nom + définition + Do + Don't
- [ ] Section Anti-Values présente avec ≥ 3 items
- [ ] Culture code manifestations présentes

→ FAIL → re-run Step 3 pour les valeurs sans ancres comportementales.

---

### Phase 4: Brand Story (5-Act Narrative)

**Purpose** — Build the foundational narrative: origin story, mission, vision, manifesto.

**Agent hint:** temperature 0.7 — phase narrative créative.

**Inputs:**
- brand_name
- founder_background
- founding_moment_or_anecdote
- mission_core
- vision_for_the_future
- brand_personality_adjectives

**Fallback:**
- Si `founding_moment_or_anecdote` absent → construire le récit autour du pain point client principal (extraire depuis Phase 2)
- Si `founder_background` absent → centrer l'origin story sur le problème de marché, pas sur la personne

**Outputs:**
- Origin Story (~300 words)
- Mission Statement (1 sentence)
- Vision Statement (1 sentence)
- Brand Manifesto (~150 words)

**Steps:**
1. **Write Origin Story** — Start with the founder's personal frustration or discovery. Use concrete, specific detail (names, places, numbers).
2. **Articulate Mission** — One sentence, present tense, action-oriented
3. **Articulate Vision** — One sentence, future tense
4. **Draft Manifesto** — 3–5 declarative statements (each prefixed "We believe…") ending with the brand's core call
5. **Review for Narrative Arc** — Ensure origin → mission → vision → manifesto tells one coherent story

**✅ Quality Gate**
- [ ] Origin Story contient au moins 1 détail concret (nom, lieu, ou chiffre)
- [ ] Mission est au présent, Vision est au futur
- [ ] Manifeste contient ≥ 3 "We believe…" (ou équivalent dans la langue cible)
- [ ] Arc narratif cohérent testé en lecture linéaire

→ FAIL → re-run Step 5 pour corriger l'arc.

---

### Phase 5: Brand Tagline & Slogans

**Purpose** — Craft 3 memorable taglines (5–8 words each) capturing brand essence and target emotion.

**Agent hint:** temperature 0.7 — phase créative haute.

**Inputs:**
- brand_name
- brand_essence (single sentence, depuis Phase 2 + 4)
- target_emotion (e.g. "trust", "excitement", "belonging")
- industry

**Outputs:**
- 3 taglines with word count, rhythmic scan, emotional hook, rationale

**Steps:**
1. **Extract Brand Essence** — Single most important thing the brand stands for (from Phase 2 + 4)
2. **Brainstorm 15–20 Candidates** — Short phrases, free-form, targeting the desired emotion
3. **Apply Constraints** — Filter to 5–8 words strictly; remove jargon; prefer active voice
4. **Rhythmic Scan** — Read each candidate aloud. Check dactylic/iambic/anapest flow
5. **Select Top 3** — Rank by memorability + emotional resonance + semantic clarity

**Tagline Principles:**
- 5–8 words — HARD LIMIT (< 5 = incomplet, > 8 = dilué)
- Active voice preferred
- Read-aloud test mandatory

**✅ Quality Gate**
- [ ] Exactement 3 taglines livrés
- [ ] Chaque tagline est entre 5 et 8 mots (compter explicitement)
- [ ] Chaque tagline a : word count, scan rythmique, emotional hook, rationale

→ FAIL sur word count → re-run Steps 3–5 sans exception.

---

### Phase 6: Brand Tone of Voice (5-Axis)

**Purpose** — Define the brand's voice across five dimensions: formality, warmth, energy, complexity, humour.

**Inputs:**
- brand_name
- brand_personality
- target_audience_description
- industry
- communication_channels

**Outputs:**
- Tone spectrum (5-axis, each 1–10)
- Voice principles (4–6 rules)
- Do/Don't examples per channel
- Vocabulary: words to use / words to avoid

**Steps:**
1. **Set Each Axis** — Formality, Warmth, Energy, Complexity, Humour — score 1–10 each, avec justification
2. **Define Voice Principles** — 4–6 rules (e.g. "Precision over hype")
3. **Create Channel Examples** — Per channel: ✅ Do and ❌ Don't example
4. **Build Vocabulary List** — "Use" vs "Avoid" two-column table
5. **Review for Consistency** — Tone spectrum aligned with values (Phase 3) and target audience

**✅ Quality Gate**
- [ ] 5 axes scorés (pas un seul manquant) avec justification
- [ ] ≥ 4 voice principles
- [ ] Do/Don't pour chaque channel listé
- [ ] Vocabulary table : ≥ 8 entries par colonne

→ FAIL → re-run Step 1 pour les axes manquants.

---

### Phase 7: Brand Messaging Matrix

**Purpose** — Structured messaging framework adapting the core narrative to each audience segment.

**Agent hint:** temperature 0.3 — phase analytique/structurelle.

**Inputs:**
- brand_name
- positioning_statement (Phase 2)
- target_audience_segments (list)
- key_differentiators
- proof_points (data, endorsements, metrics)

**Fallback:**
- Si `proof_points` vides → utiliser "pending validation" comme placeholder, noter dans l'output

**Outputs:**
- Messaging hierarchy (master message → segment messages)
- 3 key messages per segment
- Elevator pitches per segment (30s each)
- Proof point bank

**Steps:**
1. **Draft Master Message** — One sentence capturing the entire value proposition
2. **Identify Segments** — 3–5 distinct audience segments
3. **Per Segment: Write 3 Key Messages** — Each with priority label, message sentence, supporting proof point
4. **Write Elevator Pitches** — One 30-second pitch per segment
5. **Compile Proof Point Bank** — All data, endorsements, metrics in one reference table

**✅ Quality Gate**
- [ ] Master message présent (1 phrase)
- [ ] ≥ 3 segments définis
- [ ] Exactement 3 key messages par segment
- [ ] Un pitch de 30s par segment
- [ ] Proof point bank compile TOUS les points de preuve utilisés

→ FAIL → re-run Step 3 pour les segments incomplets.

---

### Phase 8: Brand Pitch (15s / 30s / 60s / 2min)

**Purpose** — 10-slide pitch deck with slide-by-slide content, visual recommendations, speaker notes, and condensed pitches.

**Agent hint:** température 0.3 pour usage investisseurs, 0.5 pour usage interne.

**Inputs:**
- brand_name
- one_liner
- problem_statement
- solution_description
- market_size (TAM/SAM/SOM)
- business_model
- traction_metrics
- team_backgrounds
- funding_ask

**Fallback:**
- Si `traction_metrics` absent → remplacer Slide 6 par "Pipeline & Early Signals", noter gap

**Outputs:**
- 10-slide structure (headline + content + visual treatment + speaker notes per slide)
- Condensed pitches: 15s, 30s, 60s, 2min

**Steps:**
1. **Slide 1: Hook** — Cover slide, brand mark, one-liner
2. **Slide 2: Problem** — Concrete statistic + human story
3. **Slides 3–5: Solution** — Three pillars; market sizing (TAM/SAM/SOM); product overview
4. **Slide 6: Traction** — Growth metrics, revenue, partner logos, key credibility signal
5. **Slide 7: Team** — Headshots descriptions, credentials, past employer logos
6. **Slide 8: Competition** — Comparison matrix showing advantages
7. **Slide 9: Financials** — Use of funds + revenue projection
8. **Slide 10: Ask** — Funding details, CTA, contact
9. **Condense** — Write 15s / 30s / 60s / 2min versions

**✅ Quality Gate**
- [ ] Exactement 10 slides avec headline + content + speaker notes chacune
- [ ] 4 formats condensés livrés (15s, 30s, 60s, 2min)
- [ ] Arc narratif : Hook → Problem → Solution → Traction → Team → Competition → Financials → Ask

→ FAIL → re-run slides manquantes + condensés manquants.

---

### Phase 9: Brand Visual Identity

**Purpose** — Define the complete visual language: art direction, photography, illustration, typography, iconography, motion. **Cette phase est la source de vérité visuelle et produit des design tokens livrables pour le frontend.**

**Inputs:**
- brand_name
- brand_personality
- industry
- competitor_visual_landscape
- primary_use_cases (web, print, social, pitch deck)

**Note :** Cette phase est la **source de vérité visuelle**. La Phase 10 (Color Palette) DOIT être cohérente avec l'art direction définie ici. Toute couleur introduite en Phase 10 doit être justifiée par les principes de Phase 9.

**Outputs:**
- Art direction principles (4–5 rules)
- Visual style: photography, illustration, typography, iconography, motion
- Mood board description (text-based)
- Photography & illustration brief
- **🎨 Design Tokens — Typography & Spacing** *(NEW v2.1)* : CSS custom properties + JSON export pour handoff frontend

**Steps:**
1. **Define Art Direction Principles** — 4–5 high-level rules
2. **Set Photography Style** — Documentary ou studio? Natural light? Real people ou stock?
3. **Set Illustration Style** — Isometric? Flat? Line-art? Selective colour?
4. **Define Typography Hierarchy** — Headline, body, monospace/data fonts; weights per role
5. **Define Iconography System** — Outline ou filled? Stroke width? Consistent perspective?
6. **Define Motion Principles** — Micro-interactions? Data transitions? What to avoid?
7. **Describe Mood Board** — Paragraph evoking the visual world: colours, textures, atmosphere
8. **🎨 Generate Design Tokens — Typography & Spacing** *(NEW v2.1)*:
   - **CSS Custom Properties** pour `:root` :
     ```css
     :root {
       --font-headline: 'Familjen Grotesk', sans-serif;
       --font-body: 'Inter', sans-serif;
       --font-mono: 'JetBrains Mono', monospace;
       --font-size-display: clamp(3rem, 5vw, 5rem);
       --font-size-h1: 2.5rem;
       --font-size-h2: 2rem;
       --font-size-body: 1rem;
       --font-size-small: 0.875rem;
       --font-weight-headline: 700;
       --font-weight-body: 400;
       --line-height-body: 1.6;
       --spacing-unit: 0.25rem;
       --spacing-xs: calc(var(--spacing-unit) * 1);
       --spacing-sm: calc(var(--spacing-unit) * 2);
       --spacing-md: calc(var(--spacing-unit) * 4);
       --spacing-lg: calc(var(--spacing-unit) * 8);
       --spacing-xl: calc(var(--spacing-unit) * 16);
       --border-radius-sm: 4px;
       --border-radius-md: 8px;
       --border-radius-lg: 16px;
       --border-radius-full: 9999px;
     }
     ```
   - **JSON tokens** (même données, format portable) :
     ```json
     {
       "typography": {
         "headline": {"family": "Familjen Grotesk", "fallback": "sans-serif", "weight": 700},
         "body": {"family": "Inter", "fallback": "sans-serif", "weight": 400}
       },
       "fontSize": {
         "display": "clamp(3rem, 5vw, 5rem)",
         "h1": "2.5rem",
         "body": "1rem"
       },
       "spacing": {"unit": "0.25rem", "xs": "0.25rem", "sm": "0.5rem", "md": "1rem", "lg": "2rem", "xl": "4rem"},
       "borderRadius": {"sm": "4px", "md": "8px", "lg": "16px", "full": "9999px"}
     }
     ```

**✅ Quality Gate**
- [ ] ≥ 4 art direction principles
- [ ] 7 dimensions couvertes (photo, illustration, typo, icono, motion, mood board, art direction)
- [ ] Mention explicite des teintes/tons prévus pour cohérence avec Phase 10
- [ ] 🎨 **Design tokens CSS + JSON livrés** (typo + spacing) *(NEW v2.1)*

→ FAIL → re-run dimensions manquantes.

---

### Phase 10: Brand Color Palette

**Purpose** — Psychologically grounded color palette with WCAG 2.1 AA accessibility, dark mode variant, and production-ready hex/RGB/HSL values + CSS/JSON design tokens.

**Dépendance critique :** Vérifier que la palette est **cohérente avec le mood board Phase 9** avant de finaliser.

**Inputs:**
- brand_name
- industry
- brand_personality_adjectives
- target_audience_demographics
- light_or_dark_primary (preference)
- art_direction_principles (Phase 9 output)

**Outputs:**
- Primary palette (3–5 colors) with hex codes + psychology justification
- Secondary palette (3–4 functional colors)
- Neutral palette (5 shades)
- **🌙 Dark mode palette** *(NEW v2.1)* — variantes de chaque couleur pour fond sombre
- WCAG compliance table with contrast ratios (light + dark)
- **🎨 Design Tokens — Colors** *(NEW v2.1)* : CSS custom properties light + dark + JSON export

**Steps:**
1. **Select Primary Colors** — 3–5 colors rooted in brand personality, psychological justification
2. **Select Secondary Colors** — Functional colors for interactive states, alerts, data highlights
3. **Build Neutral Palette** — 5 shades from near-white to rich black
4. **Create WCAG Compliance Table** — Contrast ratio per key combination, AA/AAA pass/fail
5. **Document Usage Rules** — Headings, body, CTAs, backgrounds, borders, errors
6. **🌙 Generate Dark Mode Palette** *(NEW v2.1)* :
   - Pour chaque couleur primaire/secondaire/neutre, fournir une variante dark mode
   - Règles : les couleurs claires s'inversent mais ne doivent PAS être du blanc pur (#FFFFFF sur #000000 = contraste trop agressif)
   - Le fond dark n'est jamais du noir pur — préférer un gris très foncé (#0D1117, #1A1A2E, ou selon l'identité)
   - Recalculer les ratios WCAG pour le mode sombre (les règles changent — un texte clair sur fond sombre a des seuils différents)
   - Table dark mode : Primary (light bg → dark bg), Secondary, Neutral, Status colors
7. **🎨 Generate Design Tokens — Colors** *(NEW v2.1)* :
   - **CSS Custom Properties** — bloc `:root` pour light mode + bloc `[data-theme="dark"]` pour dark mode :
     ```css
     :root {
       --color-primary: #2563EB;
       --color-primary-hover: #1D4ED8;
       --color-secondary: #7C3AED;
       --color-bg: #FFFFFF;
       --color-bg-secondary: #F8FAFC;
       --color-text: #0F172A;
       --color-text-muted: #64748B;
       --color-border: #E2E8F0;
       --color-success: #16A34A;
       --color-error: #DC2626;
       --color-warning: #F59E0B;
     }
     [data-theme="dark"] {
       --color-primary: #3B82F6;
       --color-primary-hover: #60A5FA;
       --color-bg: #0D1117;
       --color-bg-secondary: #161B22;
       --color-text: #E6EDF3;
       --color-text-muted: #8B949E;
       --color-border: #30363D;
     }
     ```
   - **JSON tokens** — un objet unique avec sections `light` et `dark` pour consommation programmatique

**✅ Quality Gate**
- [ ] ≥ 3 primary colors avec hex codes
- [ ] Secondary palette (≥ 3 couleurs fonctionnelles)
- [ ] Neutral palette (exactement 5 shades)
- [ ] WCAG table complète avec ratios de contraste pour chaque combo clé
- [ ] 🌙 **Dark mode palette présente** — variantes pour toutes les couleurs primaires/secondaires/neutres *(NEW v2.1)*
- [ ] 🌙 **WCAG dark mode vérifié** — ratios recalculés pour fond sombre *(NEW v2.1)*
- [ ] 🎨 **Design tokens CSS + JSON livrés** (light + dark) *(NEW v2.1)*
- [ ] Cohérence confirmée avec art direction Phase 9 (cross-check explicite)

→ FAIL sur WCAG → ajuster luminosité jusqu'à passer AA minimum.

---

### Phase 11: Brand Logo

**Purpose** — 3 logo concept directions (wordmark, emblem, abstract) with descriptions, rationale, usage constraints.

**Agent hint:** temperature 0.7 — phase créative descriptive.

**Inputs:**
- brand_name
- brand_essence
- industry
- brand_personality
- color_palette_reference (Phase 10)

**Outputs:**
- 3 logo concept descriptions
- Concept rationale per direction
- Clear space & minimum size guidelines
- Do/Don't usage examples

**Steps:**
1. **Concept A — Wordmark** — Custom/modified font treatment, letter substitution, ligature
2. **Concept B — Emblem** — Symbol + text in unified shape
3. **Concept C — Abstract Mark** — Purely symbolic visual, can stand alone
4. **Define Variants Per Concept** — Horizontal, vertical/stacked, icon-only, monochrome, animated
5. **Set Usage Guidelines** — Clear space (minimum = height of first letter), min size digital/print
6. **Document Prohibited Uses** — No stretching, recolouring, outlining, drop shadows, low-contrast

**Post-execution → giga-configure handoff:**
Après Phase 11, appeler `giga-configure` pour injecter les brand assets dans les templates boilerplate.

**✅ Quality Gate**
- [ ] 3 concepts livrés (Wordmark + Emblem + Abstract)
- [ ] Variants définis pour chaque concept
- [ ] Usage guidelines présentes (clear space + min size)
- [ ] Prohibited uses listés (≥ 4 items)

→ FAIL → re-run concepts manquants.

---

### Phase 12: Brand Book / Guidelines

**Purpose** — Consolidate all brand identity into a single authoritative Brand Guidelines document.

**Dépendance :** Nécessite les outputs de TOUTES les phases 1–11 en statut PASS.

**📄 Format de sortie** *(NEW v2.1)* :
- **Primaire : HTML dark-themed, self-contained single-file.** Un seul fichier `.html` autonome (CSS inline, pas de dépendances externes sauf Google Fonts). Thème sombre par défaut (background #0D1117, texte #E6EDF3) avec toggle light mode. Design éditorial — navigation par sections, table des matières sticky, palette de couleurs interactive, code blocks pour design tokens.
- **Fallback : Markdown** — Version texte brut pour Vault Obsidian, PR descriptions, ou environnements sans navigateur.
- Les deux formats sont livrés. Le HTML est le livrable principal.

**Inputs:**
- brand_name
- all_previous_phases_outputs (Phases 1–11)
- applications (digital, print, environmental, swag)
- governance_rules

**Outputs:**
- **`brand-book.html`** — Brand Book HTML dark-themed interactif
- **`brand-book.md`** — Version Markdown pour archivage/Vault
- 5 sections : Foundation, Story+Voice, Visual, Applications, Governance
- Application examples per channel
- Asset delivery checklist
- Version history

**Steps:**
1. **Section 1: Brand Foundation** — Positioning statement, mission, vision, values
2. **Section 2: Brand Story & Voice** — Origin narrative, tone spectrum (5-axis), voice principles, vocabulary
3. **Section 3: Visual Identity** — 3 logo concepts, color palette (light + dark) avec swatches CSS, typography, photography/illustration, **design tokens CSS/JSON intégrés**
4. **Section 4: Applications** — Per-channel guidelines (Web, Mobile, Social, Print, Merchandise, Presentations)
5. **Section 5: Governance** — File naming, asset storage, approval matrix, do/don't checklist
6. **Add Version History** — Version number, date, change log
7. **Render HTML** — Générer le fichier HTML self-contained avec :
   - Dark theme par défaut (#0D1117 background)
   - Table des matières sticky sidebar
   - Swatches de couleurs interactifs (hover → copier hex)
   - Code blocks pour CSS/JSON design tokens
   - Toggle ☀️/🌙 light/dark mode
   - Print stylesheet pour export PDF propre
8. **Render Markdown** — Version texte brut du même contenu

**Post-execution → hermes-agent:**
Stocker les deux fichiers dans Obsidian Vault sous `~/OneDrive/Documents/Obsidian Vault/Brands/[brand_name]/`.

**✅ Quality Gate**
- [ ] 5 sections présentes (Foundation, Story+Voice, Visual, Applications, Governance)
- [ ] Version history présente
- [ ] Asset delivery checklist présente
- [ ] 🎨 Design tokens CSS + JSON inclus dans Section 3 *(NEW v2.1)*
- [ ] 📄 **`brand-book.html` livré** — HTML dark-themed self-contained *(NEW v2.1)*
- [ ] 📄 **`brand-book.md` livré** — Markdown fallback *(NEW v2.1)*

→ FAIL → identifier la/les section(s) manquante(s) et re-run.

---

### Phase 13: Brand Content Strategy

**Purpose** — Editorial calendar mapping content to pillars, channels, formats, and business goals.

**Inputs:**
- brand_name
- content_pillars
- channels
- monthly_theme_or_campaign
- resources_available
- business_goals_for_month
- calendar_duration (default: 30 jours — configurable: 7, 30, 90)

**Fallback:**
- Si `calendar_duration` non spécifié → défaut 30 jours
- Si `resources_available` non spécifié → assumer : 1 designer, 1 writer, pas de vidéo

**Outputs:**
- Editorial calendar (table: day / pillar / channel / format / headline / goal)
- Content formats per piece
- Distribution plan
- Weekly theme breakdown
- KPI targets per content type

**Steps:**
1. **Define 4 Content Pillars** — With percentage mix
2. **Set Weekly Themes** — Foundation / Proof / Community / Vision (ou équivalent)
3. **Assign Daily Content** — Per day: pillar, channel, format, headline/topic, primary goal
4. **Balance Goals** — Mix: education, engagement, authority, social proof, conversion, retention, talent
5. **Set KPI Targets** — Per content type (traffic, engagement, opens, CTR, views, conversions)

**✅ Quality Gate**
- [ ] Calendrier complet pour la durée demandée (7, 30, ou 90 jours selon input)
- [ ] 4 colonnes minimum par entrée : pillar, channel, format, goal
- [ ] KPI targets définis pour chaque type de contenu
- [ ] Mix de goals équilibré (pas 100% conversion)

→ FAIL → compléter les jours ou entrées manquants.

---

### Phase 14: Brand SEO

**Purpose** — Technical and strategic SEO foundation: keyword clusters, site architecture, on-page optimization, content gap analysis.

**Agent hint:** temperature 0.3 — phase analytique.

**Inputs:**
- brand_name
- industry
- core_products_or_services
- primary_and_secondary_audiences
- competitor_domains
- target_geo

**Outputs:**
- Keyword clusters (head, body, long-tail) with intent + volume estimates
- Site information architecture (sitemap)
- On-page SEO checklist
- Content gap opportunities table

**Steps:**
1. **Research Head Terms** — High-volume (10K+/mo), informational intent → pillar pages
2. **Research Body Terms** — Medium-volume (900–5K/mo), commercial intent → product/landing pages
3. **Research Long-Tail Terms** — Low volume, high conversion → blog + tools
4. **Design Site Architecture** — URL structure: product pages, learn hub, blog, pricing, about, resources
5. **Build On-Page Checklist** — Title tag (50–60 chars), meta description (150–160 chars), H1 unique per page, URL slug format, schema types, alt text, internal linking
6. **Analyse Content Gaps** — Topics competitors rank for that brand doesn't; tag as opportunities
7. **Set Core Web Vitals Targets:**
   - LCP (Largest Contentful Paint) < 2.5s
   - **INP (Interaction to Next Paint) < 200ms** *(FID déprécié par Google en mars 2024)*
   - CLS (Cumulative Layout Shift) < 0.1

**✅ Quality Gate**
- [ ] 3 clusters présents (head, body, long-tail)
- [ ] Sitemap avec structure d'URLs
- [ ] On-page checklist avec TOUS les items listés
- [ ] Content gaps : ≥ 5 opportunités identifiées
- [ ] Core Web Vitals utilisent **INP** (pas FID) — vérification obligatoire

→ FAIL sur INP/FID → corriger immédiatement, ce bug invalide la crédibilité SEO.

---

### Phase 15: Brand Social Media

**Purpose** — Social media content strategy: platform selection, content pillars, posting cadence, format guidelines, engagement playbook.

**Inputs:**
- brand_name
- brand_personality
- tone_of_voice (Phase 6)
- target_audience_by_platform
- business_goals
- content_mojo

**Outputs:**
- Platform strategy (3–5 platforms with role, cadence, primary goal)
- Content pillars (4 themes with percentage mix)
- Posting cadence per platform
- Content format guidelines
- Engagement playbook

**Steps:**
1. **Select Platforms** — 3–5 platforms based on audience location; assign role + primary goal
2. **Define Content Pillars** — 4 pillars with percentage allocation
3. **Set Posting Cadence** — Per-platform schedule
4. **Define Format Guidelines** — Preferred formats per platform
5. **Write Engagement Playbook** — Comment reply rules (do/don't), DM routing, crisis protocol (pause → acknowledge → investigate → follow-up within 48h)

**✅ Quality Gate**
- [ ] ≥ 3 plateformes avec rôle + objectif définis
- [ ] 4 content pillars avec pourcentages (total = 100%)
- [ ] Cadence définie par plateforme
- [ ] Engagement playbook avec crisis protocol

→ FAIL → re-run sections manquantes.

---

### Revision Cascade Protocol *(NEW in v2.1)*

**Quand le client change un livrable upstream, quelles phases doivent être re-run ?**

Ce protocole définit la cascade de révision : si une phase est modifiée, toutes les phases downstream qui en dépendent doivent être re-validées ou re-générées.

| Phase modifiée | Phases à re-run | Justification |
|---------------|-----------------|---------------|
| **Phase 1** (Naming) | 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Le nom impacte tout : positionnement, tagline, SEO, visuel |
| **Phase 2** (Positioning) | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Le positionnement est la fondation — tout en dépend |
| **Phase 3** (Values) | 4, 6, 7, 8, 12, 13, 15 | Les valeurs influencent le ton, le messaging, le contenu |
| **Phase 4** (Story) | 5, 7, 8, 12, 13 | L'histoire impacte tagline, messaging, pitch |
| **Phase 5** (Tagline) | 7, 8, 12, 13, 15 | Tagline → messaging, pitch, contenu |
| **Phase 6** (Tone of Voice) | 7, 8, 12, 13, 15 | Le ton façonne tout le contenu écrit |
| **Phase 7** (Messaging) | 8, 12, 13, 15 | Messaging → pitch, content strategy, social |
| **Phase 8** (Pitch) | 12 | Pitch → Brand Book uniquement |
| **Phase 9** (Visual Identity) | 10, 11, 12 | Visuel → palette, logo, Brand Book |
| **Phase 10** (Color Palette) | 9 (re-validation), 11, 12 | Palette → logo, Brand Book. Si les couleurs changent, vérifier que l'art direction Phase 9 les supporte |
| **Phase 11** (Logo) | 12 | Logo → Brand Book uniquement |
| **Phase 12** (Brand Book) | — | Phase terminale, pas de downstream |
| **Phase 13** (Content Strategy) | 15 | Content → social media |
| **Phase 14** (SEO) | — | Phase indépendante (référence le positionnement mais pas de downstream direct) |
| **Phase 15** (Social Media) | — | Phase terminale |

**Procédure de révision :**
1. Identifier la phase modifiée dans la table ci-dessus
2. Marquer toutes les phases downstream comme `STALE`
3. Re-run les phases dans l'ordre du dependency graph (Phase 0)
4. Pour chaque phase re-run, exécuter le Cross-Phase Consistency Protocol
5. Si une phase downstream est déjà en `PASS` et que le changement upstream est mineur → évaluer si une simple re-validation suffit (pas de re-génération complète)

**Règle du "changement mineur" :**
Un changement est **mineur** si :
- Il ne modifie pas le sens ou la structure du livrable (ex: correction orthographique, ajustement de wording sans changement sémantique)
- Il n'affecte pas une décision binaire (ex: un choix de couleur)
- Il est documenté comme "patch" dans le versioning

Un changement est **majeur** (re-run obligatoire) si :
- Il change le positionnement, le ton, les valeurs, ou la direction créative
- Il modifie un livrable que d'autres phases référencent directement
- Le client le qualifie de "refonte" ou "pivot"

---

### Cross-Phase Consistency Protocol *(NEW in v2.0)*

Exécuter ce check **après Phase 12** avant de livrer le Brand Book final.

| Check | Source | Target | Règle |
|-------|--------|--------|-------|
| Ton vs Messaging | Phase 6 (Tone spectrum) | Phase 7 (Messaging examples) | Les exemples de messaging doivent refléter le ton défini |
| Couleurs vs Art Direction | Phase 9 (Mood board) | Phase 10 (Color palette) | Chaque couleur primaire doit être justifiable par l'art direction |
| Tagline vs Essence | Phase 2 (Positioning) | Phase 5 (Taglines) | Les taglines doivent refléter l'essence de positionnement |
| Voix vs Valeurs | Phase 3 (Values) | Phase 6 (Voice principles) | Les voice principles doivent incarner les valeurs |
| Pilliers contenu vs Messaging | Phase 7 (Messaging matrix) | Phase 13 (Content strategy) | Les content pillars doivent mapper les segments messaging |
| Tone vs Social | Phase 6 (Tone) | Phase 15 (Social playbook) | Le ton du social doit respecter le 5-axis spectrum |
| 🎨 Design Tokens vs Palette *(NEW v2.1)* | Phase 10 (CSS/JSON tokens) | Phase 12 (Brand Book) | Les tokens dans le Brand Book doivent matcher la palette livrée |
| 🌙 Dark vs Light *(NEW v2.1)* | Phase 10 (Dark palette) | Phase 12 (Brand Book) | Le Brand Book HTML doit utiliser la dark palette comme thème par défaut |

**Procédure :** Pour chaque check, valider manuellement. Si incohérence → retourner à la phase source, corriger, re-run la phase dépendante.

---

### Fallback Strategy Master Table *(NEW in v2.0)*

| Phase | Input manquant | Fallback |
|-------|---------------|---------|
| 1 | brand_attributes | Défaut : ["trust", "quality", "innovation"] |
| 1 | linguistic_combination | Défaut : "Latin + Modern English" |
| 2 | competitive_landscape | Positionnement générique + gap noté dans l'output |
| 3 | founder_beliefs | Extraire valeurs implicites depuis description produit (Phase 2) |
| 4 | founding_moment | Construire récit autour du pain point client (Phase 2) |
| 4 | founder_background | Centrer sur le problème marché, pas sur la personne |
| 7 | proof_points | Placeholder "pending validation" + gap noté |
| 8 | traction_metrics | Remplacer Slide 6 par "Pipeline & Early Signals" |
| 10 | light_or_dark_primary | Défaut : light. Mais la dark palette est TOUJOURS générée *(NEW v2.1)* |
| 13 | calendar_duration | Défaut : 30 jours |
| 13 | resources_available | Défaut : 1 designer, 1 writer, pas de vidéo |

---

### AI Execution Hints *(NEW in v2.0)*

```yaml
execution_protocol:
  before_each_phase:
    - Load all upstream phase outputs into context
    - Check dependency graph (Phase 0) before proceeding
    - Check Revision Cascade Protocol — si une phase upstream a changé, marquer les downstream STALE
  
  temperature_by_phase:
    creative_0.7: [1, 4, 5, 9, 11]
    analytical_0.3: [2, 7, 8, 14]
    default_0.5: [3, 6, 10, 12, 13, 15]
  
  on_quality_gate_fail:
    - Identify failing criteria
    - Re-run only failing steps (not entire phase)
    - Max 1 retry per phase
    - If retry fails → flag for human review, continue with next phase

  context_management:
    - Always carry: brand_name, positioning_statement, tone_spectrum, design_tokens (once Phase 9+10 done)
    - Phase 12 requires all Phase 1-11 outputs simultaneously
    - Summarize long phase outputs before carrying into next phase
  
  design_tokens_handoff:  # NEW v2.1
    - After Phase 10: tokens are ready for frontend handoff
    - Pass to OLYMPUS:frontend-developer as: {css: "...", json: {...}, darkMode: true}
    - Brand Book HTML MUST consume the same tokens (single source of truth)
```

---

### Integration Hooks *(NEW in v2.0)*

| Moment | Skill/Agent | Action |
|--------|------------|--------|
| Après Phase 10 | `OLYMPUS:frontend-developer` | Transmettre design tokens CSS + JSON (typo, spacing, colors light+dark) comme variables --brand-* |
| Après Phase 11 | `giga-configure` | Injecter brand assets (couleurs, typo, logo) dans templates boilerplate |
| Après Phase 12 | `hermes-agent` | Stocker `brand-book.html` + `brand-book.md` dans Obsidian Vault |
| Avant toute UI build | `OLYMPUS:frontend-developer` | Vérifier que les design tokens Phase 9+10 sont chargés — NE PAS commencer sans |
| Phase 14 | `giga-seo` (optionnel) | Enrichir keyword research avec données en temps réel |


---

## Module 2: `giga-game-pipeline`

- **Origine :** `08_Hermes_GigaFactory_Skills\giga-game-pipeline\SKILL.md`
- **Rôle / Objectif :** Pipeline complet de développement de jeux vidéo Godot 4 — de la conception (GDD) au déploiement (Steam/itch.io). Architecture solo-dev, 8 phases, assets CC0.

## giga-game-pipeline — Godot 4 Game Development Pipeline

### Core Principle
NEVER generate code from scratch — always use the Godot 4 template as boilerplate. Assets: préférer les packs CC0 (Quaternius, Kenney). Architecture : solo-dev approach par défaut.

### Phase 1 — Game Design Document (GDD)

**Objectif :** Définir le concept, le gameplay, l'univers et la structure complète du jeu avant toute ligne de code.

**Inputs :** Genre, inspiration, plateforme cible, public visé
**Outputs :** GDD structuré (5-15 pages)

1. Définir le concept central (elevator pitch : 1 phrase)
2. Décrire les mécaniques principales (3-5 core loops)
3. Définir le système de progression (niveaux, compétences, équipement)
4. Esquisser l'histoire et le lore (personnages, worldbuilding)
5. Lister les features par priorité (MVP → V1 → V2)
6. Estimer la scope solo-dev (éviter feature creep)

**Template GDD :**
```markdown
## [Titre du Jeu] — GDD

### Concept
> [Elevator pitch]

### Mécaniques
- [Core loop 1]
- [Core loop 2]

### Univers
- Style visuel :
- Univers sonore :
- Histoire :

### Progression
- [Système de niveau/récompense]

### Features
- MVP (mois 1-2) : [features essentielles]
- V1 (mois 3-4) : [features supplémentaires]
- V2+ : [features de polish]
```

### Phase 2 — Architecture Godot 4

**Objectif :** Mettre en place l'architecture du projet Godot 4 (scenes, autoloads, signals, resources).

**Inputs :** GDD, genre
**Outputs :** Structure de projet Godot 4

1. Créer l'arborescence de scenes (Menu → Game → UI → World)
2. Configurer les autoloads (GameManager, SaveManager, AudioManager)
3. Définir les scènes réutilisables (Player, Enemy, Item, Projectile)
4. Mettre en place le système de signaux (event bus pattern)
5. Structurer les Resources personnalisées (Stats, ItemData, QuestData)
6. Configurer les Input Maps (clavier, manette, tactile)

**Arborescence standard :**
```
res://
├── scenes/
│   ├── main/
│   ├── game/
│   ├── ui/
│   └── menu/
├── scripts/
│   ├── autoload/
│   ├── entities/
│   └── systems/
├── assets/
│   ├── models/
│   ├── textures/
│   ├── audio/
│   └── fonts/
├── resources/
│   ├── stats/
│   ├── items/
│   └── levels/
└── export/
```

### Phase 3 — Player Controller & Mouvement

**Objectif :** Implémenter le personnage joueur avec contrôles fluides (CharacterBody2D/3D).

**Inputs :** Type de jeu, contrôles
**Outputs :** Player scene + script

1. Créer le Player scene avec CharacterBody2D/3D
2. Configurer le mouvement (run, jump, dash, wall-slide selon genre)
3. Ajouter les animations (Idle, Walk, Jump, Attack — via AnimationTree)
4. Connecter les Input Actions
5. Ajouter les effets (particules de pas, trails)

### Phase 4 — Enemies & Combat

**Objectif :** Mettre en place le système d'ennemis et de combat.

**Inputs :** GDD, genre
**Outputs :** Enemy scenes, combat system

1. Créer le template Enemy (Health, Damage, Drop)
2. Implémenter l'IA (State Machine : Idle → Patrol → Chase → Attack → Hurt → Death)
3. Créer le système de combat (weapon, damage calculation, hitbox/hurtbox)
4. Configurer les drops (loots, XP, or)
5. Créer les patterns d'attaque pour différents types d'ennemis

**State Machine template :**
```gdscript
enum State { IDLE, PATROL, CHASE, ATTACK, HURT, DEATH }
var current_state = State.IDLE

func _process(delta):
    match current_state:
        State.IDLE:
            # Attendre + transition vers PATROL
        State.PATROL:
            # Se déplacer entre waypoints
        State.CHASE:
            # Poursuivre le joueur
        State.ATTACK:
            # Infliger des dégâts
        State.HURT:
            # Animation de dégâts
        State.DEATH:
            # Animation de mort + drop
```

### Phase 5 — Audio & Sound Design

**Objectif :** Intégrer la musique et les effets sonores.

**Inputs :** Univers du jeu, assets audio (CC0/self-made)
**Outputs :** AudioManager, bus audio, SFX intégrés

1. Configurer les bus audio (Master, Music, SFX, Voice)
2. Implémenter l'AudioManager (crossfade, ducking, random pitch)
3. Intégrer les SFX (footsteps, UI clicks, weapon sounds, ambient)
4. Composer/integrer la musique (par zone/biome — transition fluide)
5. Créer les AudioStreamPlayer pour chaque type de son

### Phase 6 — UI & HUD

**Objectif :** Créer l'interface utilisateur (menus, HUD, inventaire, dialogues).

**Inputs :** GDD, style graphique
**Outputs :** UI scenes, HUD, menus

1. Créer le Main Menu (Play, Options, Credits, Quit)
2. Développer le HUD (health bar, score, minimap, ammo)
3. Créer l'inventaire / equipment screen
4. Implémenter les dialogues (DialogueNode avec branches)
5. Ajouter les effets de transition (fade, screen shake, hit flash)
6. Créer le Pause Menu

### Phase 7 — Levels & World Design

**Objectif :** Construire les niveaux ou le monde ouvert (tilemaps / scenes instanciables).

**Inputs :** GDD, game design
**Outputs :** Level scenes, world/overworld

1. Créer le template de niveau (WorldEnvironment, GridMap/TileMap)
2. Placer les spawn points (Player, Enemies, Items, Checkpoints)
3. Ajouter les triggers (zones de dialogue, events, cutscenes)
4. Intégrer le système de sauvegarde (ResourceSaver / JSON)
5. Tester le level design (flow, difficulté, exploration)
6. Configurer le système de chargement de niveau (scène séparée)

### Phase 8 — Build, Export & Deploy

**Objectif :** Builder le jeu pour la/les plateformes cibles et le déployer.

**Inputs :** Projet Godot complet
**Outputs :** Build exécutable, page de déploiement

1. Configurer les Export Presets (Windows, Linux, Web, Android)
2. Optimiser les performances (LOD, occlusion culling, texture compression)
3. Builder et tester sur chaque plateforme cible
4. Créer la page de déploiement (itch.io, Steam)
5. Configurer les achievements / leaderboards (si applicable)

**Boilerplate / Templates recommandés :**
- Godot 4 template : `giga-scaffold` > godot-game
- Assets CC0 : Quaternius (personnages, monstres, nature, buildings), Kenney (UI, SFX)
- Outils : Audacity (audio), Aseprite (pixel art), Blender (3D)

### Quality Gates
1. NE PAS coder from scratch — utiliser le template Godot 4
2. Assets CC0 par défaut (sauf besoin spécifique)
3. Architecture solo-dev (éviter le sur-engineering)
4. Build testé sur au moins 1 plateforme cible avant déploiement


---

## Module 3: `giga-landing-page`

- **Origine :** `08_Hermes_GigaFactory_Skills\giga-landing-page\SKILL.md`
- **Rôle / Objectif :** Landing page complète — hero, features, pricing, FAQ, analytics, SEO, waitlist et déploiement

## giga-landing-page

Skill Giga Factory unifié pour créer une landing page complète de A à Z : hero → features → pricing → FAQ → SEO → analytics → waitlist → déploiement.

**NEVER from scratch** — toujours utiliser Platforms Starter Kit (Vercel) comme boilerplate ou scaffolding existant via giga-scaffold.

### Phases

#### Phase 1 — Hero & Hook

Génère la section hero : titre accrocheur, sous-titre, CTA primaire/secondaire, éléments de crédibilité.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `project` | string | oui | Nom du projet |
| `tagline` | string | non | Accroche principale |
| `subtitle` | string | non | Sous-titre |
| `cta` | string | non | Texte du bouton principal |
| `style` | string | non | dark, light, gradient, minimal |
| `visual` | string | non | illustration, mockup, video, abstract |

**Principes :**
- Hook en < 3 secondes (problème + solution)
- Sous-titre = bénéfice concret, pas fonctionnalités
- CTA = verbe d'action + promesse de valeur
- Social proof : chiffres, logos clients, notes
- Mobile-first : CTA cliquable sans zoom

#### Phase 2 — Features Grid

Génère la section fonctionnalités : grille organisée, icônes, descriptions, cas d'usage.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `count` | number | non | 3, 6 ou 9 features |
| `layout` | string | non | grid, alternating, list, tabs, masonry |
| `use-cases` | boolean | non | Ajouter des cas d'usage |

**Principes :**
- 6 features = optimal (assez pour convaincre, pas trop pour noyer)
- Un bénéfice par feature, pas une liste technique
- Icônes cohérentes (même famille, même style)
- Grouper par thème (3-4 max par groupe)

#### Phase 3 — Pricing Table

Génère le tableau de tarifs : 3 plans, features, CTA, mise en avant du plan recommandé.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `plans` | string | non | "Starter:9€,Pro:29€,Enterprise:99€" |
| `currency` | string | non | EUR, USD, GBP |
| `toggle` | boolean | non | Toggle mensuel/annuel |
| `highlight` | string | non | Plan à mettre en avant |

**Principes :**
- 3 plans max (le choix optimal pour conversion)
- Plan du milieu mis en avant ("Populaire")
- 5-7 lignes de features par plan max
- Prix annuel avec réduction visible

#### Phase 4 — FAQ Section

Génère la section FAQ : 10 questions/réponses optimisées conversion + SEO.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `categories` | string | non | general, pricing, technical, security |
| `count` | number | non | Nombre de questions (défaut: 10) |

**Principes :**
- Vraies questions utilisateurs, pas du marketing
- Réponses concises (2-3 phrases max)
- Inclure les mots-clés SEO naturellement
- JSON-LD FAQ schema pour rich results Google
- Questions sur pricing et sécurité = critiques pour conversion

#### Phase 5 — SEO & Meta

Optimisation SEO complète : meta tags, OG, Twitter Cards, JSON-LD, sitemap, robots.txt.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `keywords` | string | oui | Mots-clés principaux |
| `audit` | boolean | non | Audit SEO on-page |
| `schema` | boolean | non | Générer JSON-LD |

**Génère :**
- Meta title (50-60 chars) + meta description (150-160 chars)
- Open Graph (og:title, og:description, og:image, og:url)
- Twitter Cards (summary_large_image)
- JSON-LD (SoftwareApplication pour SaaS, Organization, Product)
- Structure HTML sémantique (H1 → H2 → H3)
- Canonical URL, robots.txt, sitemap.xml, hreflang

#### Phase 6 — Analytics & Tracking

Configuration du tracking : GA4/Plausible/Umami, événements conversion, tests A/B.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `provider` | string | non | ga4, plausible, umami, mixpanel |
| `events` | string | non | Événements à tracker |
| `ab-test` | string | non | Élément à tester en A/B |

**Événements standards :** page_view, cta_click, signup_start, signup_complete, scroll_depth (25/50/75/100%), pricing_view, faq_toggle, video_play, outbound_click

**Providers :**
| Provider | Gratuit | Auto-hébergé | RGPD compliant |
|----------|---------|--------------|----------------|
| GA4 | 10M events/mois | ✗ | Partiellement (cookie consent) |
| Plausible | 30 jours | ✓ | ✓ (pas de cookies) |
| Umami | ✓ | ✓ | ✓ |
| Mixpanel | 20M events/mois | ✗ | Partiellement |

#### Phase 7 — Waitlist & Pre-launch

Page de pré-lancement avec capture d'email, compteur, preuve sociale, parrainage.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `launch-date` | string | non | Date de lancement (YYYY-MM-DD) |
| `referral` | boolean | non | Système de parrainage |
| `minimal` | boolean | non | Version minimaliste |

**Services email supportés :** Mailchimp, ConvertKit, SendGrid, Brevo (Sendinblue)

#### Phase 8 — Deploy

Déploiement automatisé sur Vercel / Netlify / Cloudflare Pages.

**Entrées :**
| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `provider` | string | oui | vercel, netlify, cloudflare, github |
| `source` | string | oui | Chemin du dossier de build |
| `domain` | string | non | Domaine personnalisé |
| `framework` | string | non | next, astro, hugo, vanilla |

**Étapes :** Build → Preview → DNS (CNAME) → SSL → Domaine → Headers sécurité → Redirects → Test

**Boilerplate recommandé :** Platforms Starter Kit (Vercel) — jamais from scratch.

### Utilisation

```bash
## Landing page complète
hermes skill run giga-landing-page --project "MonProjet" --full

## Phase spécifique
hermes skill run giga-landing-page --project "MonProjet" --phase "hero" --tagline "L'IA qui simplifie vos revenus"

## Avec déploiement
hermes skill run giga-landing-page --project "MonProjet" --full --deploy --provider "vercel"
```

### Post-exécution Obligatoire

1. **calculate_confidence** — Évaluer la landing générée (0-10) :
   - Score < 5 → améliorer la section faible (phase concernée)
   - Score ≥ 5 et < 7 → flag HUMAN GATE (relecture recommandée)
   - Score ≥ 7 → validé pour déploiement

2. **register_decision** — Enregistrer dans lessons.jsonl :
   ```json
   {"entry_id": <auto>, "timestamp": "<today>", "type": "landing", "task": "<project>",
    "pattern": "LANDING_GENERATED", "phases": ["hero","features","pricing","faq","seo","analytics","waitlist","deploy"],
    "provider": "<deploy_provider>", "confidence": <score>}
   ```

3. **version_file** — Versionner dans vault/runs/ :
   ```
   vault/runs/landing-<project>-<YYYYMMDD>.json
   ```

### Configuration

```yaml
## config.yaml
default_cta: "Commencer"
default_currency: "EUR"
discount_annual: 20
highlight_plan: "pro"
free_trial_days: 14
analytics_provider: "ga4"
cookie_consent: true
deploy_provider: "vercel"
auto_deploy: false
preview_deployments: true
locale: "fr_FR"
social_proof: true
double_optin: true
```

### Notes

- Le hero et le pricing sont les sections les plus critiques pour la conversion
- Toujours commencer par le boilerplate Platform Starter Kit (Vercel)
- La FAQ est souvent la dernière section lue avant décision d'achat
- Plausible/Umami sont recommandés pour la conformité RGPD (pas de cookies)
- Un test A/B nécessite ≥1000 visiteurs par variante pour être significatif
- Le déploiement automatique sur push Git est recommandé
- Configurer les en-têtes de sécurité (CSP, HSTS, CORS) dès le départ


---

## Module 4: `giga-legal-contracts`

- **Origine :** `08_Hermes_GigaFactory_Skills\giga-legal-contracts\SKILL.md`
- **Rôle / Objectif :** >-

## ⚖️ Giga Legal Contracts — Contrats & Accords Juridiques

### Description

Skill consolidé couvrant l'ensemble des **contrats et accords juridiques** nécessaires au fonctionnement d'une startup ou PME : accords de confidentialité, conditions générales de vente et d'utilisation, contrats de travail, contrats de partenariat, politique de confidentialité RGPD, et analyse des risques de responsabilité avec programme d'assurances. Conçu pour les entrepreneurs français et belges francophones.

---

### ⚠️ AVERTISSEMENT JURIDIQUE GÉNÉRAL

**Ce contenu est généré par une intelligence artificielle et est fourni à titre informatif uniquement. Il ne constitue pas un conseil juridique.** Les documents contractuels générés engagent votre responsabilité. Chaque document doit être adapté à votre activité spécifique et validé par un avocat spécialisé avant toute signature ou publication. Des documents non conformes peuvent entraîner des sanctions civiles, administratives et pénales. L'auteur et l'éditeur déclinent toute responsabilité quant aux conséquences de l'utilisation de ces informations.

---

### Modules

Le skill est organisé en **6 modules interconnectés**, chacun pouvant être utilisé indépendamment.

---

### Module 1 — 🤫 Accord de Confidentialité (NDA)

#### Versions disponibles

| Type | Usage |
|---|---|
| **Unilatéral** | Présentation à un investisseur, recrutement d'un prestataire, due diligence |
| **Bilatéral** | Partenariat, co-développement, JV, négociation bilatérale |
| **Multilatéral** | Projets impliquant 3+ parties (consortium, groupement) |

#### Structure du NDA complet

| Section | Contenu |
|---|---|
| **1. Préambule** | Identité des parties, contexte de la divulgation |
| **2. Définitions** | Informations confidentielles, représentants, support |
| **3. Obligations de la partie réceptrice** | Utilisation limitée au but défini, non-divulgation, mesures de protection |
| **4. Exclusions** | Infos publiques, connues antérieurement, obtenues d'un tiers, développées indépendamment, divulgation légale requise |
| **5. Absence de licence IP** | Aucun transfert implicite de droits de propriété intellectuelle |
| **6. Retour des informations** | Restitution ou destruction sur demande |
| **7. Durée** | Période de divulgation (12 mois) + obligation de confidentialité (2-5 ans) |
| **8. Responsabilité** | Plafond, exceptions (secret d'affaires, PI, fraude) |
| **9. Loi applicable** | Droit français, tribunal de commerce |

#### Erreurs fréquentes à éviter

| Erreur | Conséquence |
|---|---|
| NDA signé après la divulgation | Infos divulguées avant non couvertes |
| Pas de marquage « Confidentiel » | Preuve difficile qu'une info était confidentielle |
| NDA trop large (« toutes les infos ») | Risque de nullité pour absence d'objet déterminé |
| Pas de clause de retour/destruction | L'autre partie conserve vos informations indéfiniment |
| NDA réciproque non nécessaire | Obligations réciproques inutiles et complexité |

#### Checklist de négociation NDA
- [ ] Définition des informations confidentielles : équilibrée ?
- [ ] Durée de confidentialité : 2-3 ans standard
- [ ] Exclusions : vérifier l'équilibre
- [ ] Plafond de responsabilité : acceptable ?
- [ ] Clause de non-licence IP présente ?
- [ ] Sous-traitants et conseils inclus ?
- [ ] Notification préalable en cas de divulgation légale ?
- [ ] Délai de destruction raisonnable (14-30 jours) ?

---

### Module 2 — 📋 Conditions Générales de Vente et d'Utilisation (CGV/CGU)

#### Structure des CGV (13 articles)

| Article | Contenu |
|---|---|
| Préambule | Identité du vendeur, champ d'application |
| 1 | Définitions |
| 2 | Documents contractuels et commandes |
| 3 | Prix et conditions tarifaires |
| 4 | Modalités de paiement |
| 5 | Délais de livraison / fourniture |
| 6 | Réception et vérification |
| 7 | Droit de rétractation (B2C uniquement) |
| 8 | Garanties (légale de conformité, vices cachés) |
| 9 | Propriété intellectuelle |
| 10 | Responsabilité et force majeure |
| 11 | Données personnelles (RGPD) |
| 12 | Résolution des litiges et médiation |
| 13 | Loi applicable et juridiction |

##### Clauses spécifiques B2B
- Réserve de propriété (rétention de titre jusqu'au paiement complet)
- Délais de paiement et pénalités de retard (LME)
- Plafond de responsabilité
- Renonciation au droit de rétractation

##### Clauses spécifiques B2C
- Informations précontractuelles (L221-5 C. conso.)
- Droit de rétractation de 14 jours (L221-18)
- Formulaire type de rétractation
- Garantie légale de conformité (2 ans)
- Médiation de la consommation

#### Structure des CGU (13 articles)

| Article | Contenu |
|---|---|
| Préambule | Identité de l'éditeur, services concernés |
| 1 | Définitions |
| 2 | Accès et création de compte |
| 3 | Obligations de l'utilisateur |
| 4 | Obligations de l'éditeur |
| 5 | Propriété intellectuelle (contenus, licences) |
| 6 | Données personnelles (renvoi politique confidentialité) |
| 7 | Conditions financières (abonnement, gratuit, freemium) |
| 8 | Garanties et responsabilité |
| 9 | Suspension et résiliation |
| 10 | Force majeure |
| 11 | Évolution du service et des CGU |
| 12 | Propriété des contenus générés par l'utilisateur |
| 13 | Loi applicable et litiges |

##### Clauses spécifiques SaaS
- Disponibilité (uptime SLA si applicable)
- Sauvegarde et sécurité des données
- Portabilité des données (art. 20 RGPD)
- Période d'essai gratuite
- Résiliation pour non-paiement

#### Mentions légales obligatoires (art. 6 LCEN)
- Dénomination sociale, forme juridique, capital social
- Adresse du siège social
- Numéro RCS et SIRET
- Numéro de TVA intracommunautaire
- Directeur de la publication
- Hébergeur du site (nom, adresse, téléphone)
- Email de contact

#### Recommandations de mise en œuvre
1. **Affichage** : les CGV/CGU accessibles à chaque étape de la commande/inscription
2. **Acceptation** : case à cocher obligatoire (double clic pour contrats à distance)
3. **Archivage** : conservation de la version acceptée par le client
4. **Mise à jour** : clause de modification avec notification et préavis
5. **Langue** : obligation de rédaction en français
6. **Cookies** : renvoi vers la politique de cookies conforme RGPD

---

### Module 3 — 👔 Contrats de Travail

#### Contrats disponibles

##### 1. CDI (Contrat à Durée Indéterminée)

**Clauses obligatoires :**
- Identité des parties
- Date d'embauche et période d'essai
- Intitulé du poste, classification et coefficient (convention collective)
- Lieu de travail et mobilité éventuelle
- Durée du travail (35h, 39h, forfait-jours)
- Rémunération brute mensuelle
- Congés payés (2,5 jours ouvrables/mois = 5 semaines/an)
- Mutuelle et prévoyance
- Convention collective applicable

**Période d'essai légale :**
| Catégorie | Durée initiale | Renouvellement |
|---|---|---|
| Ouvrier / Employé | 2 mois | 1 mois |
| Agent de maîtrise / Technicien | 3 mois | 2 mois |
| Cadre | 4 mois | 4 mois |

##### 2. CDD (Contrat à Durée Déterminée)

**Conditions de validité :**
- Motif précis (remplacement, accroissement temporaire, saisonnier, contrat à objet défini)
- Durée max : 18 mois (sauf exceptions : 24-36 mois)
- Indemnité de fin de contrat : 10% de la rémunération brute totale (sauf exceptions)
- Pas de CDD pour remplacer un gréviste ou un emploi dangereux

##### 3. Convention de stage

- Durée max : 6 mois (924 heures) par année d'enseignement
- Gratification obligatoire ≥ 4,35 €/h (2026) si stage > 2 mois
- Convention tripartite obligatoire
- Tuteur obligatoire
- Congés : 1 jour par mois

##### 4. Contrat de freelance / prestation de services (B2B)

**⚠️ Risque de requalification (faux freelance) — art. L8221-6 Code du travail**

Pour être un véritable contrat de freelance, l'URSSAF vérifie :
- Absence de lien de subordination
- Liberté (choix des moyens, méthodes, possibilité de se faire remplacer)
- Propre organisation (plusieurs clients, propre matériel)
- Facturation au TJM ou au forfait avec TVA

**Clauses clés du contrat de freelance :**
- Description de la mission et des livrables
- TJM / forfait et modalités de facturation
- Durée et conditions de renouvellement
- Propriété intellectuelle (cession des droits sur les livrables)
- Confidentialité (NDA)
- Assurances (RC Pro du freelance)
- Clause de non-sollicitation de personnel

#### Formalités obligatoires à l'embauche

| Formalité | Délai | Organisme |
|---|---|---|
| DPAE (Déclaration Préalable à l'Embauche) | Avant embauche | URSSAF |
| Visite médicale d'information et prévention | Dans les 3 mois | Médecine du travail |
| Affiliation mutuelle | 1er jour du contrat | Mutuelle entreprise |
| Registre Unique du Personnel | Jour d'embauche | Inspection du travail |
| Remise du contrat signé | 2 jours ouvrables | Employeur → salarié |
| DSN (Déclaration Sociale Nominative) | Mensuelle | URSSAF |

#### Clauses importantes pour les startups
- **Clause de télétravail** : modalités, nombre de jours, prise en charge des frais
- **Clause de propriété intellectuelle** : obligatoire pour salariés créateurs (cession automatique art. L611-7 CPI)
- **Clause de non-concurrence** : limitée (temps, espace, objet) avec contrepartie financière (20-30% du brut)
- **Clause de mobilité** : préciser le périmètre géographique
- **Forfait-jours** (cadres autonomes) : 218 jours/an, avec suivi de charge et droit à la déconnexion
- **Période d'essai** : à adapter selon la convention collective

#### Documents associés à générer
- Lettre de mission / d'engagement
- Avenant au contrat
- Reçu pour solde de tout compte
- Certificat de travail
- Attestation France Travail
- Convention de stage tripartite

---

### Module 4 — 🤝 Contrat de Partenariat

#### Types de partenariat disponibles

| Type | Structure recommandée |
|---|---|
| **Commercial / Distribution** | Clause d'efforts, exclusivité, minimum de vente, reporting trimestriel |
| **Co-développement (R&D)** | PI conjointe 50/50, partage frais dépôt, licences croisées |
| **Technologique (API)** | Licence non exclusive d'API, défimitation d'usage et territoire |
| **Joint Venture** | Gouvernance paritaire, conseil d'administration, décisions stratégiques unanimes |
| **Co-marketing** | Partage des coûts, visibilité réciproque, KPIs communs |
| **Sous-traitance** | Cahier des charges, livrables, délais, prix forfaitaires |

#### Structure générale (14 sections)

| Section | Contenu |
|---|---|
| 1 | Préambule (activités, complémentarité) |
| 2 | Définitions (Territoire, Produits, PI, Revenus Nets) |
| 3 | Objet du partenariat (prestations, périmètre géographique) |
| 4 | Exclusivité (périmètre, exceptions) |
| 5 | Obligations des parties (A : fourniture/support, B : commercialisation/reporting) |
| 6 | Conditions financières (commissions, royalties, minimum de vente) |
| 7 | Propriété intellectuelle (préexistante, développée, licences) |
| 8 | Confidentialité (NDA intégré ou en annexe) |
| 9 | Durée et résiliation (initiale, reconduction, préavis) |
| 10 | Non-concurrence et non-sollicitation |
| 11 | Responsabilité et assurances (RC Pro obligatoire) |
| 12 | Force majeure |
| 13 | Résolution des litiges (médiation préalable, tribunal compétent) |
| 14 | Dispositions générales |

#### Points de négociation clés

| Point | Position standard | À vérifier |
|---|---|---|
| **Exclusivité** | Contrepartie d'efforts | Justifiée par des engagements réciproques |
| **PI** | Chacun conserve sa PI | Sort de la PI développée ensemble |
| **Durée** | 1-3 ans avec reconduction tacite | Durée minimale pour rentabiliser l'investissement |
| **Résiliation** | Sans préavis pour manquement grave | Définition précise du « manquement grave » |
| **Non-concurrence** | Durée + 12 mois post-contrat | Géographiquement limitée, justifiée |
| **Responsabilité** | Plafond 1x montant annuel | Exclure violation de PI et secret d'affaires |

---

### Module 5 — 🔒 Politique de Confidentialité RGPD

#### Structure (12 sections)

| Section | Contenu |
|---|---|
| 1 | Identité du responsable de traitement |
| 2 | Données collectées (catégories, origine, caractère obligatoire) |
| 3 | Finalités et bases légales (tableau par traitement) |
| 4 | Destinataires des données (internes, sous-traitants) |
| 5 | Transferts hors UE (CCT, DPF, BCR) |
| 6 | Durée de conservation |
| 7 | Droits des personnes (art. 15-22 RGPD) |
| 8 | Modalités d'exercice des droits |
| 9 | Sécurité des données |
| 10 | Cookies et traceurs |
| 11 | Réclamation auprès de la CNIL |
| 12 | Évolution de la politique |

#### Droits des personnes (art. 15-22 RGPD)
- **Accès** (art. 15) : obtenir confirmation et copie
- **Rectification** (art. 16) : corriger des données inexactes
- **Effacement** (art. 17) : « droit à l'oubli »
- **Limitation** (art. 18) : figer temporairement le traitement
- **Portabilité** (art. 20) : recevoir ses données dans un format structuré
- **Opposition** (art. 21) : s'opposer au traitement (prospection, profilage)
- **Décision automatisée** (art. 22) : ne pas faire l'objet d'une décision exclusivement automatisée

#### Bandeau cookies obligatoire
Le bandeau doit comporter :
- ✅ Bouton « Tout accepter »
- ❌ Bouton « Tout refuser »
- ⚙️ Bouton « Personnaliser » (paramétrage granulaire)
- 🔗 Lien vers la politique de confidentialité

#### Registre des activités de traitement (art. 30 RGPD)

| Champ | Description |
|---|---|
| Nom du traitement | Ex : « Gestion des prospects » |
| Responsable de traitement | Nom et coordonnées |
| Finalité | Marketing, prospection |
| Base légale | Intérêt légitime (art. 6.1.f) / Consentement (art. 6.1.a) |
| Catégories de personnes | Prospects, clients, visiteurs |
| Catégories de données | Nom, email, téléphone, cookies |
| Destinataires | Service commercial, CRM, sous-traitants |
| Transferts hors UE | Oui/Non, garanties |
| Durée de conservation | 3 ans après dernier contact |
| Mesures de sécurité | Chiffrement TLS, accès restreint, logs |

#### Checklist de conformité CNIL
- [ ] Registre des traitements tenu et à jour
- [ ] Politique de confidentialité accessible en 2 clics max
- [ ] Formulaire de recueil de consentement valide (case non pré-cochée)
- [ ] Bandeau cookies conforme (refus aussi facile qu'acceptation)
- [ ] Mentions d'information aux formulaires de collecte
- [ ] DPO désigné (si données sensibles ou grande échelle)
- [ ] AIPD réalisée pour les traitements à risque
- [ ] Procédure de notification des violations de données
- [ ] Contrats sous-traitance conformes (art. 28 RGPD)
- [ ] Procédure d'exercice des droits opérationnelle

---

### Module 6 — ⚖️ Responsabilité & Assurances

#### Les 4 régimes de responsabilité

| Régime | Fondement | Dommages |
|---|---|---|
| **Responsabilité civile contractuelle** | Art. 1231-1 C. civ. — inexécution d'une obligation | Directs et prévisibles |
| **Responsabilité civile délictuelle** | Art. 1240 C. civ. — fait causant un dommage | Intégralité du préjudice |
| **Responsabilité pénale personne morale** | Art. 121-2 C. pén. — infraction pour le compte de la société | Amende jusqu'à 1 M€, dissolution |
| **Responsabilité des dirigeants** | Faute de gestion, violation statuts, infraction | Action ut singuli/universi, interdiction de gérer |

#### Analyse des risques par secteur

| Secteur | Risque principal | Assurance recommandée |
|---|---|---|
| **Conseil / Expertise** | Erreur professionnelle → préjudice financier | RC Pro (obligatoire pour professions réglementées) |
| **Développement logiciel** | Défaut logiciel, perte de données | RC Pro + Cyber |
| **E-commerce** | Produit défectueux, non-conformité | RC Exploitation + RC Produits |
| **Fintech** | Erreur de calcul, fraude, non-conformité | RC Pro (obligatoire ORIAS) + Cyber |
| **Healthtech** | Préjudice corporel, violation données santé | RC Pro + Cyber + RC Exploitation |
| **Industrie** | Produit défectueux, dommage environnemental | RC Produits + RC Exploitation |

#### Programme d'assurances recommandé

| Assurance | Couverture | Montant | Budget/an |
|---|---|---|---|
| **RC Pro** | Dommages à des tiers (erreur, omission, négligence) | 1-5 M€ par sinistre | 1 000–5 000 € |
| **RC Exploitation** | Dommages dans les locaux ou par les biens | 1-3 M€ par sinistre | 500–2 000 € |
| **Cyber** | Fuite de données, ransomware, DDoS, fraude | 500 K€–5 M€ | 2 000–20 000 € |
| **RC Mandataires Sociaux** | Défense pénale et civile des dirigeants | 500 K€–5 M€ | 1 500–5 000 € |
| **Protection Juridique** | Frais d'avocat en cas de litige | — | 300–1 000 € |
| **Perte d'Exploitation** | Perte de CA pendant interruption | — | 1 000–5 000 € |

#### Budget annuel estimatif par profil

| Profil | Assurances | Budget/an |
|---|---|---|
| Micro-startup (< 5 pers., CA < 500K€) | RC Pro + RC Exploitation + Cyber | 3 000–6 000 € |
| Startup croissance (5-20 pers., CA 500K-5M€) | RC Pro + RC Exploitation + Cyber + RCMS | 8 000–20 000 € |
| Scale-up (20-100 pers., CA 5-50M€) | Tout + Protection Juridique + Perte exploitation | 20 000–60 000 € |
| Fintech / Healthtech | Tout + Assurance spécifique secteur | 30 000–100 000 € |

#### Mesures de prévention des risques

| Risque | Mesure préventive |
|---|---|
| Responsabilité contractuelle | CGV/CGU solides, limitation de responsabilité |
| Responsabilité délictuelle | Politique de confidentialité, sécurité des données, NDA |
| Responsabilité pénale | Code de conduite, compliance, cartographie des risques |
| Responsabilité des dirigeants | Pacte d'actionnaires, PV réguliers, délégations de pouvoirs |
| Cyber | MFA, EDR, backups, plan de réponse aux incidents, formation |
| Produits défectueux | Tests qualité, traçabilité, conformité CE/Normes |

---

### Références réglementaires
- Code civil (art. 1101 et s., art. 1231-1, art. 1240) — droit des contrats et responsabilité
- Code de commerce (L.441-1 à L.441-16) — CGV B2B, pénalités de retard
- Code de la consommation (L.221-1 à L.221-28, L.217-1 à L.217-15) — droit de rétractation, garanties
- Code du travail (L.1221-1 et s., L.8221-6) — contrats de travail, requalification
- RGPD — Règlement UE 2016/679
- Loi Informatique et Libertés modifiée (loi n°78-17)
- LCEN (loi n°2004-575) — mentions légales
- Code des assurances — RC Pro, obligations d'assurance
- Loi pour une République numérique (n°2016-1321)


---

## Module 5: `giga-legal-corporate`

- **Origine :** `08_Hermes_GigaFactory_Skills\giga-legal-corporate\SKILL.md`
- **Rôle / Objectif :** >-

## 🏢 Giga Legal Corporate — Vie Sociale & Structuration Juridique

### Description

Skill consolidé couvrant l'intégralité de la **vie sociale et corporate** d'une startup ou PME : du choix de la structure juridique à l'optimisation fiscale, en passant par les statuts, le pacte d'actionnaires, la levée de fonds, la cap table, la propriété intellectuelle, l'audit pré-levée et la conformité réglementaire. Conçu pour les entrepreneurs français et belges francophones.

---

### ⚠️ AVERTISSEMENT JURIDIQUE GÉNÉRAL

**Ce contenu est généré par une intelligence artificielle et est fourni à titre informatif uniquement. Il ne constitue pas un conseil juridique, fiscal ou comptable.** Les documents et analyses produits doivent être impérativement validés par un avocat spécialisé, un expert-comptable ou un conseil en propriété industrielle avant toute utilisation. L'auteur et l'éditeur déclinent toute responsabilité quant aux conséquences de l'utilisation de ces informations.

---

### Modules

Le skill est organisé en **9 modules interconnectés**, chacun pouvant être utilisé indépendamment ou en séquence.

---

### Module 1 — 🏛️ Choix de la Structure Juridique

#### Formes disponibles

| Critère | SAS / SASU | SARL / EURL |
|---|---|---|
| **Nombre d'associés** | 1 (SASU) ou plusieurs (SAS) | 1 (EURL) ou 2-50 (SARL) |
| **Capital minimum** | Pas de minimum légal | Pas de minimum légal |
| **Régime social dirigeant** | Assimilé salarié | TNS (sauf gérant minoritaire = assimilé salarié) |
| **Protection sociale** | Meilleure (Sécurité sociale, chômage ss conditions) | Moins bonne (cotisations réduites mais couverture moindre) |
| **Flexibilité statutaire** | Très élevée (statuts libres) | Faible (statuts très encadrés) |
| **Levée de fonds** | Très adaptée (BSA, actions de préférence) | Peu adaptée |
| **Cession de titres** | Libre sauf clause d'agrément | Agrément obligatoire pour les tiers |

#### Logique de recommandation

- **Seul fondateur + levée de fonds prévue** → SASU
- **Seul fondateur, pas de levée, CA < 100K€** → EURL ou EI
- **Plusieurs associés + levée < 24 mois** → SAS
- **2-5 associés, pas de VC** → SARL possible
- **Protection sociale renforcée souhaitée** → SAS / SASU

#### Actions concrètes post-décision
1. Valider avec un avocat spécialisé
2. Rédiger les statuts (cf. Module 2)
3. Préparer le pacte d'actionnaires (cf. Module 3)
4. Ouvrir un compte bancaire professionnel
5. Déposer le capital (banque / Caisse des Dépôts / notaire)
6. Publier un avis de constitution (JAL)
7. Immatriculer au RCS via guichet unique (formalites.gouv.fr)

---

### Module 2 — 📜 Statuts Complets (22 sections)

#### Structure des statuts

| Section | Contenu |
|---|---|
| 1 | Forme juridique |
| 2 | Dénomination sociale |
| 3 | Objet social (code NAF / APE) |
| 4 | Siège social et transfert |
| 5 | Durée (99 ans max) |
| 6 | Apports (numéraire, nature, industrie) |
| 7 | Capital social (montant, valeur nominale) |
| 8 | Libération des apports |
| 9 | Comptes courants d'associés |
| 10 | Cession de titres / agrément |
| 11 | Droits et obligations des associés |
| 12 | Organes de direction (Président / Gérant) |
| 13 | Organes de contrôle (CAC) |
| 14 | Décisions collectives (AG, consultation écrite) |
| 15 | Exercice social |
| 16 | Affectation du résultat |
| 17 | Avantages particuliers |
| 18 | Transformation de la société |
| 19 | Dissolution et liquidation |
| 20 | Contestations (médiation, arbitrage) |
| 21 | Notifications |
| 22 | Formalités de publicité |

#### Options statutaires disponibles
- Clause d'agrément
- Actions de préférence
- Droits de veto
- Clause de non-concurrence
- Convention de portage
- Clauses de sortie conjointe (drag-along, tag-along)
- Clause de médiation / arbitrage
- Procédure de consultation écrite

#### Annexes générées
- Annexe des apports en nature (évaluation et rapport)
- Feuille de présence des associés fondateurs
- État des actes à accomplir (checklist formalités)
- Modèle de déclaration de souscription et de versement
- Projet de nomination du 1er dirigeant

---

### Module 3 — 🤝 Pacte d'Actionnaires (9 clauses)

Le pacte d'actionnaires est un **document extra-statutaire** (confidentiel, non déposé au greffe) qui régit les relations entre actionnaires fondateurs et investisseurs.

#### Les 9 clauses

| Clause | Description | Usage |
|---|---|---|
| **1 — Agrément** | Tout cession à un tiers nécessite l'accord préalable des actionnaires existants | Protection contre l'entrée d'actionnaires indésirables |
| **2 — Préemption** | Droit de premier refus pour les actionnaires existants avant cession à un tiers | Maintien de la répartition du capital |
| **3 — Non-concurrence** | Interdiction pour les fondateurs de participer à une activité concurrente (24 mois post-sortie) | Protection de la société |
| **4 — Drag-along** | Les majoritaires (≥ 80%) peuvent entraîner les minoritaires dans une cession | Facilite l'exit |
| **5 — Tag-along** | Les minoritaires ont le droit de vendre aux mêmes conditions que les majoritaires | Protection des minoritaires |
| **6 — Pre-emption** | Droit de souscription prioritaire lors d'augmentations de capital | Anti-dilution des actionnaires existants |
| **7 — Anti-dilution** | Protection des investisseurs en cas de down round (weighted average broad-based standard) | Protection investisseurs |
| **8 — Sortie (IPO / cession)** | Modalités de sortie collective | Planification de l'exit |
| **9 — Médiation / Arbitrage** | Médiation préalable obligatoire avant action judiciaire | Évitement des litiges coûteux |

#### ⚠️ Rappels importants
- Le pacte est **distinct des statuts** et peut rester confidentiel
- Il est **exécutoire uniquement entre signataires** (ne lie pas la société)
- En cas de contradiction, les **statuts prévalent** sur le pacte vis-à-vis des tiers
- Le pacte doit être **signé par tous les actionnaires** actuels et futurs (clause d'adhésion)

---

### Module 4 — 💰 Levée de Fonds

#### Term Sheet (lettre d'intention)

Le term sheet résume les principaux termes de l'investissement (non contraignant sauf clauses d'exclusivité, confidentialité, frais).

| Section | Standard de marché |
|---|---|
| **Valorisation** | Pré-money / post-money |
| **Liquidation Preference** | 1x non-participating |
| **Anti-dilution** | Weighted average (broad-based) |
| **Board** | Fondateurs + investisseurs + indépendant(s) |
| **Vesting fondateurs** | 4 ans, cliff 1 an |
| **Drag-along / Tag-along** | Seuil 80% / 50% |
| **Protective provisions** | Droit de veto limité aux décisions fondamentales |
| **Exclusivité** | 30-60 jours |

#### Information Memorandum / Teaser

1. Executive Summary
2. Problème & Solution
3. Marché (TAM/SAM/SOM)
4. Produit / Technologie / PI
5. Traction (MRR, ARR, croissance, rétention, CAC, LTV)
6. Équipe
7. Concurrence
8. Business Model
9. Plan financier (3-5 ans)
10. Utilisation des fonds

#### Chronologie d'une levée (Série A)

| Étape | Durée |
|---|---|
| Préparation (data room, IM) | 1-2 mois |
| Prospection investisseurs | 2-3 mois |
| Term Sheet | 2-4 semaines |
| Due Diligence | 4-8 semaines |
| Documentation définitive | 2-4 semaines |
| Signature / Closing | 1-2 semaines |
| **Total** | **6-12 mois** |

#### Conseils aux fondateurs
- Valorisation réaliste pour éviter un down round
- Préférence de liquidation 1x non-participating
- Garder le contrôle du board
- Accepter le weighted average, refuser le full ratchet
- Budget frais juridiques : 15 000–50 000 €

---

### Module 5 — 📊 Cap Table & Dilution

#### Types de titres et instruments

| Instrument | Description |
|---|---|
| **Actions ordinaires** | Standard, droit de vote + dividende |
| **Actions de préférence** | Droits spécifiques (dividende prioritaire, préférence de liquidation, anti-dilution) |
| **BSPCE** | Stock-options pour fondateurs et salariés (régime fiscal favorable) |
| **BSA** | Options pour investisseurs |
| **Convertible Notes** | Prêt convertible en actions au prochain tour |
| **SAFE** | Simple Agreement for Future Equity |

#### Plan de vesting standard (recommandé)

| Période | Actions acquises |
|---|---|
| Jour 1 – Mois 12 (cliff) | 0% |
| Mois 12 (cliff atteint) | 25% |
| Mois 24 | 50% |
| Mois 36 | 75% |
| Mois 48 | 100% |

#### Simulation de dilution par tour

| Tour | % Cédé aux investisseurs | Capital restant fondateurs |
|---|---|---|
| Amorçage (Seed) | ~16,7% | 83,3% |
| Série A | ~23% | 64% |
| Série B | ~21% | 50,5% |
| Série C | ~20% | 40,4% |
| IPO | ~13% | 35,2% |

#### Recommandations
- Pool BSPCE de 10-15% dès la création
- Vesting 4 ans / cliff 1 an
- Pas d'anti-dilution pour les fondateurs
- Cap table claire et registre précis
- Préférence de liquidation 1x non-participante

---

### Module 6 — 🧠 Propriété Intellectuelle

#### Les 7 catégories de droits IP

| Actif | Protection | Durée | Coût (France) |
|---|---|---|---|
| **Brevet** (INPI/OEB/PCT) | Invention technique | 20 ans | 3 000–8 000 € |
| **Marque** (INPI/EUIPO) | Signe distinctif | 10 ans renouvelable | 200 € (1 classe) |
| **Droit d'auteur** | Œuvre originale | 70 ans post-mortem | Gratuit (dépôt Soleau : 15 €) |
| **Dessin & modèle** | Apparence d'un produit | 5-25 ans | 40-100 € |
| **Secret d'affaires** | Savoir-faire, algorithme | Indéfini (si secret) | Mesures de protection |
| **Base de données** | Investissement substantiel | 15 ans renouvelable | —
| **Nom de domaine** | Adresse web | 1-10 ans | 10 €/an |

#### Priorités par secteur

| Secteur | Priorité IP |
|---|---|
| Tech / Logiciel | Droit d'auteur (code source), brevet (si technique), marque |
| Biotech / Pharma | Brevet (priorité absolue), secret d'affaires |
| Mode / Luxe | Marque, dessin & modèle, droit d'auteur |
| Services / SaaS | Marque, droit d'auteur (code), secret d'affaires (algorithme) |
| Industrie | Brevet, secret d'affaires, dessin & modèle |

#### Checklist pré-dépôt
- [ ] Recherche d'antériorité (brevet / marque)
- [ ] Rédaction du mémoire descriptif / classes de Nice
- [ ] Vérification : pas de divulgation publique préalable
- [ ] Contrat de cession de droits d'auteur (freelances, salariés)
- [ ] Dépôt du code source (Soleau, APP, horodatage)
- [ ] Licences open source compatibles avec le modèle commercial

---

### Module 7 — 🔍 Audit Juridique Pré-Levée

#### 9 domaines audités

| Domaine | Points critiques |
|---|---|
| **Corporate** | Statuts à jour, registre des mouvements, cap table, PV AG, conventions réglementées, bénéficiaires effectifs |
| **Propriété Intellectuelle** | Marques, brevets, cessions droits d'auteur, licences open source, secrets d'affaires |
| **Social / RH** | Contrats de travail, registre personnel, BSPCE, risque requalification freelance → CDI |
| **Fiscal** | Déclarations IS/TVA, CIR/CII, JEI, reports déficits |
| **Contrats commerciaux** | CGV/CGU, contrats clients (top 10), NDA, clauses de responsabilité et PI |
| **Conformité** | RGPD (politique, registre, cookies), AI Act, DSA, NIS 2 |
| **Assurances** | RC Pro, cyber, mandataires sociaux |
| **Contentieux** | Litiges en cours ou potentiels |
| **Finance / Comptabilité** | Comptes annuels, prévisionnel, data room |

#### Data Room Checklist

**Dossier Corporate :** statuts consolidés, pacte signé, cap table, registre titres, PV AG, Kbis, bénéficiaires effectifs
**Dossier IP :** certificats dépôt, contrats cession, licences open source, noms de domaine
**Dossier Social :** organigramme, contrats de travail, plan BSPCE, conventions collectives
**Dossier Fiscal :** liasses fiscales (3 ans), déclarations CIR/CII, attestation JEI
**Dossier Conformité :** politique confidentialité, registre traitements, CGV/CGU

#### Budget de remédiation estimé
- Régularisation cessions droits d'auteur : 5 000–15 000 €
- Mise à jour CGV/CGU : 2 000–5 000 €
- Mise en conformité RGPD : 3 000–10 000 €
- Sécurisation cap table : 1 000–3 000 €
- Mise à jour statuts et pacte : 5 000–15 000 €
- **Total estimation : ~20 000–70 000 €**

---

### Module 8 — ✅ Conformité Réglementaire

#### 1. RGPD (Règlement UE 2016/679)

| Obligation | Priorité | Sanction |
|---|---|---|
| Registre des activités de traitement (art. 30) | 🔴 | 10 M€ / 2% CA |
| Politique de confidentialité conforme (art. 12-14) | 🔴 | 20 M€ / 4% CA |
| Consentement valide (case non pré-cochée) | 🔴 | 20 M€ / 4% CA |
| Procédure d'exercice des droits (art. 15-22) | 🔴 | 20 M€ / 4% CA |
| Bandeau cookies conforme | 🔴 | 10 M€ / 2% CA |
| Contrats sous-traitance (art. 28) | 🔴 | 10 M€ / 2% CA |
| Notification violations (art. 33-34) | 🔴 | 10 M€ / 2% CA |
| Transferts hors UE encadrés | 🔴 | 20 M€ / 4% CA |

#### 2. AI Act (Règlement UE 2024/1689)

| Niveau de risque | Obligations | Sanction |
|---|---|---|
| **Inacceptable** (interdit) | Aucune mise sur le marché | 35 M€ / 7% CA |
| **Haut risque** | Gestion des risques, documentation technique, contrôle humain | 15 M€ / 3% CA |
| **Risque limité** | Transparence (informer l'utilisateur) | 7,5 M€ / 1,5% CA |
| **GPAI (Foundation models)** | Copyright, résumés données, red teaming, reporting énergétique | 15 M€ / 3% CA |

#### 3. NIS 2 (Directive UE 2022/2555)
Applicable aux entreprises de taille moyenne/grande dans des secteurs critiques.
- Mesures de cybersécurité (chiffrement, accès, logs)
- Signalement des incidents (24h alerte, 72h notification)
- Continuité d'activité (BCP/DRP)
- Sécurité chaîne d'approvisionnement
- Tests de pénétration réguliers

#### 4. DSA (Règlement UE 2022/2065)
Applicable aux plateformes en ligne, intermédiaires, hébergeurs, marketplaces.
- Transparence des algorithmes de recommandation
- Point de contact unique
- Procédure de signalement de contenus illicites
- Vérification des identités des vendeurs tiers

#### Plan d'action priorisé
🔴 **Immédiat (0-3 mois)** : Registre RGPD, politique confidentialité, classification IA, notification violations, contrats sous-traitance
🟡 **Court terme (3-6 mois)** : AIPD, documentation technique IA, procédure droits RGPD, politique sécurité NIS 2
🟢 **Moyen terme (6-12 mois)** : Tests robustesse, certification ISO 27001, due diligence fournisseurs

---

### Module 9 — 💶 Optimisation Fiscale

#### Les 7 dispositifs clés

| Dispositif | Principe | Économie type |
|---|---|---|
| **CIR** (Crédit d'Impôt Recherche) | 30% des dépenses R&D | ~75 K€ pour 300 K€ salaires R&D |
| **CII** (Crédit d'Impôt Innovation) | 20% des dépenses innovation (plafond 400 K€) | ~80 K€/an |
| **JEI** (Jeune Entreprise Innovante) | Exonérations charges sociales et fiscales (< 8 ans) | ~50 K€/an |
| **IS taux réduit** | 15% jusqu'à 42 500 € de bénéfice | ~4 250 € |
| **Report en avant déficits** | Imputation des pertes sur bénéfices futurs | Variable |
| **TVA** | Option pour le réel si achats importants | ~20 K€ |
| **PFU (Flat Tax)** | 30% sur dividendes (vs barème progressif) | Variable |

#### Conditions JEI
- Moins de 8 ans depuis l'immatriculation
- PME (< 250 salariés, CA ≤ 50 M€)
- Dépenses R&D ≥ 15% des charges
- Indépendance capitalistique
- Création véritable (pas de reprise/fusion)

#### Calendrier fiscal
| Date | Démarche |
|---|---|
| 15 janvier | Déclaration TVA décembre |
| 31 mars | Déclaration de résultats |
| 15 avril | TVA + CVAE |
| 15 mai | Acompte IS |
| 31 mai | Déclaration CIR / CII |
| 30 juin | Option JEI |
| 15 septembre | Acompte IS + TVA |
| 15 décembre | Acompte IS + TVA |
| Novembre | Paiement CFE |

#### Régimes TVA
| Régime | Seuil (2026) |
|---|---|
| Franchise en base | CA < 91 900 € (prestations) |
| Réel simplifié | CA < 818 000 € (prestations) |
| Réel normal | Au-delà |

---

### Références réglementaires
- Code de commerce (L.210-1 et s.) — droit des sociétés
- Code de la propriété intellectuelle (L.112-2, L.611-1 et s.)
- RGPD — Règlement UE 2016/679
- AI Act — Règlement UE 2024/1689
- NIS 2 — Directive UE 2022/2555
- DSA — Règlement UE 2022/2065
- Code général des impôts (CIR art. 244 quater B, CII art. 244 quater T, JEI art. 44 sexies-0 A)


---
