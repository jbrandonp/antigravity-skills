# Engine Integration: Flawless Pixel Art Setup

When importing pixel art spritesheets into modern game engines, engines default to bilinear filtering, texture compression, and sub-pixel camera smoothing that blur pixel art. Follow these exact settings for each target engine.

---

## 1. Godot 4.x

In Godot 4, pixel art requires project-wide and per-texture configuration:

### Project Settings
- **Rendering $\to$ Textures $\to$ Canvas Textures $\to$ Default Texture Filter**: Set to `Nearest`.
- **Display $\to$ Window $\to$ Stretch $\to$ Mode**: Set to `viewport`.
- **Display $\to$ Window $\to$ Stretch $\to$ Aspect**: Set to `keep`.
- **Rendering $\to$ 2D $\to$ Snap 2D Transforms to Pixel**: Set to `On` (prevents sub-pixel jitter during camera panning).
- **Rendering $\to$ 2D $\to$ Snap 2D Vertices to Pixel**: Set to `On`.

### SpriteFrames Setup
```gdscript
# Attach generated JSON spritesheet coordinates
var sprite_frames = SpriteFrames.new()
# Add animation with target FPS from metadata
sprite_frames.add_animation("walk")
sprite_frames.set_animation_speed("walk", 10.0)
sprite_frames.set_animation_loop("walk", true)
```

---

## 2. Unity (2022+ / 6.x)

In Unity, select the exported `.png` spritesheet in the Project Window and configure the Inspector:

| Property | Required Setting | Why |
|---|---|---|
| **Texture Type** | `Sprite (2D and UI)` | Enables 2D sprite renderer pipeline |
| **Sprite Mode** | `Multiple` | Slices sheet into individual animation frames |
| **Pixels Per Unit (PPU)** | Matches grid size (e.g. `16`, `32`, or `64`) | 1 world unit = 1 tile or 1 character height |
| **Generate Physics Shape** | Disabled (or custom polygon) | Prevents expensive auto-physics calculation |
| **Filter Mode** | `Point (no filter)` | **Crucial:** Prevents blurry bilinear anti-aliasing |
| **Compression** | `None` | **Crucial:** Lossy DXTC/ETC compression creates color noise/mixels |

### Slicing with Sprite Editor
1. Click **Sprite Editor**.
2. Select **Slice $\to$ Type: Grid By Cell Size** (enter the `cell_size` from our `spritesheet.json`).
3. Set **Pivot** to `Bottom` or `Custom` (using the normalized anchor from our JSON, e.g. `X: 0.5`, `Y: 0.1`).

---

## 3. Unreal Engine 5 (Paper2D / PaperZD)

1. **Texture Settings**:
   - Right-click texture $\to$ **Sprite Actions $\to$ Apply Paper2D Texture Settings**.
   - This automatically configures:
     - **Texture Group**: `2D Pixels (unfiltered)`.
     - **Compression Settings**: `UserInterface2D (RGBA)`.
     - **Filter**: `Nearest`.
2. **Sprite Extraction**:
   - Right-click $\to$ **Create Flipbook** or **Extract Sprites** using grid mode.
3. **PaperZD Character Blueprint**:
   - Set Character Movement component **Orient Rotation to Movement** to `False`.
   - Control flipbook facing using:
     ```text
     Velocity.X < 0 -> SetRelativeScale3D(X = -1)  // Mirror East/West
     Velocity.X > 0 -> SetRelativeScale3D(X = 1)
     ```

---

## 4. HTML5 Canvas / Phaser 3

### CSS Rendering Rule
```css
canvas {
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
```

### 2D Canvas Context
```javascript
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
// Disable bilinear image smoothing
ctx.imageSmoothingEnabled = false;
```

### Phaser 3 Configuration
```javascript
const config = {
  type: Phaser.AUTO,
  width: 320,
  height: 180,
  pixelArt: true, // Enables Nearest Neighbor filtering across all textures
  zoom: 3,
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 0 } }
  },
  scene: GameScene
};
```
