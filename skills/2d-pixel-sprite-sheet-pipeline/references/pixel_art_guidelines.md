# 2D Pixel Art Craftsmanship & Production Guidelines

This reference defines the core principles, palettes, outline strategies, and animation timing standards required to produce professional, mixel-free 2D pixel art.

---

## 1. The Golden Rules of Pixel Art

1. **Strict Grid Pitch**: Every visual element in the frame must share the exact same pixel grid resolution. A character with $1\text{px}$ edges standing next to a tree with $2\text{px}$ edges is an instant stylistic mismatch.
2. **1-Bit Binary Alpha**: Transparent pixels have $\alpha = 0$, opaque pixels have $\alpha = 255$. Never use fractional alpha channels ($0 < \alpha < 255$) in retro pixel art sprites — semi-transparent pixels create smeared halos in game engines.
3. **Cluster Shading over Pillow Shading**:
   - **Cluster Shading (Correct)**: Group pixels into intentional, solid lighting masses with clean directional light sources (top-left or top-down).
   - **Pillow Shading (Anti-Pattern)**: Shading dark on the outer edges and light in the exact center like a puffed pillow, ignoring directional light.
4. **No "Jaggies"**: Avoid awkward staircases where pixel segments jump erratically (e.g., $1-3-1-4$). Curves should follow smooth arithmetic progressions (e.g., $1-2-3-4$ or $3-2-1-1$).

---

## 2. Standard Retro Palettes

Using curated palettes restricts chromatic noise and gives games a coherent visual identity.

### Pico-8 (16 Colors)
Classic fantasy console palette:
```text
#000000 (Black)      #1D2B53 (Dark Blue)   #7E2553 (Dark Purple) #008751 (Dark Green)
#AB5236 (Brown)      #5F574F (Dark Gray)   #C2C3C7 (Light Gray)  #FFF1E8 (White)
#FF004D (Red)        #FFA300 (Orange)      #FFEC27 (Yellow)      #00E436 (Green)
#29ADFF (Blue)       #83769C (Indigo)      #FF77A8 (Pink)        #FFCCAA (Peach)
```

### Endesga 32 (EDG 32)
The industry standard 32-color palette for rich indie RPGs and platformers:
```text
#BE4A2F #D77643 #EAD4AA #E4A672 #B86F50 #733E39 #3E2731 #A22633
#E43B44 #F77622 #FEE761 #63C74D #3E8948 #265C42 #193C3E #124E89
#0099DB #2CE8F5 #FFFFFF #C0CBDC #8B9BB4 #5A6988 #3A4466 #262B44
#181425 #FF0044 #68386C #B55088 #F6757A #E8B796 #C28569 #000000
```

### Game Boy (4 Shades)
Classic monochromatic olive tones:
```text
#0F380F (Blackish Green)  #306230 (Dark Green)  #8BAC0F (Light Green)  #9BBC0F (Yellow Green)
```

---

## 3. Outline Strategies

| Strategy | Description | Best For |
|---|---|---|
| **Black Outline** | Single-pixel solid black outline around the outer silhouette. Internal features use colored boundaries. | Readability against high-contrast backgrounds (action games, brawlers, arcade). |
| **Selective Outlining (Sel-Out)** | Outer outline color matches adjacent shaded colors (e.g., dark navy for blue armor, dark crimson for red cloth). Highlights on top edges have lighter outlines. | Modern high-end indie pixel art (Celeste, Hyper Light Drifter). |
| **No Outline** | Pure silhouette defined solely by color contrast against background tiles. | Realistic, atmospheric, or isometric games (Chrono Trigger, Tactics Ogre). |

---

## 4. Animation Frame Rates & Cadences

| Cycle | Recommended Frames | FPS | Timing / Feel Notes |
|---|---|---|---|
| **Idle** | 4 – 6 frames | 6 – 8 FPS | Subtle 1px vertical chest breathing or cape sway. Never over-animate idle. |
| **Walk** | 8 – 12 frames | 10 – 12 FPS | Contact $\to$ Down $\to$ Passing $\to$ Up cycle. Feet must stay locked to baseline. |
| **Run** | 6 – 8 frames | 12 – 15 FPS | Forward lean ($15^\circ$), aggressive airborne recoil frame. |
| **Melee Attack** | 4 – 7 frames | 14 – 18 FPS | 2 frames anticipation (slow) $\to$ 1 frame explosive strike snap $\to$ 2 frames follow-through/recovery. |
| **Hurt / Recoil** | 2 – 4 frames | 12 FPS | 1 frame extreme recoil compression + white flash palette shift $\to$ 2 recovery frames. |
| **Death** | 6 – 10 frames | 10 – 12 FPS | Impact $\to$ tumble $\to$ settle on ground plane. Final frame remains static. |

---

## 5. Directional Symmetry & East/West Flipping

- When generating character sheets, **always generate the West facing pose** and flip horizontally (`flip_x`) to create East.
- **Asymmetric Elements Guard**:
  - If a character has a shield in their left hand, flipping will swap the shield to the right hand.
  - *Fix*: In 16-bit retro production, this is standard convention (e.g. Link in SNES Zelda flips shield side). If strict asymmetry is required (e.g., one-eyed pirate, mechanical arm), create an explicit separate East sheet after snapping West.
