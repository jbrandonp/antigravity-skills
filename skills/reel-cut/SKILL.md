---
name: reel-cut
description: End-to-end automated face-cam video production pipeline (derush, kinetic typography, camera moves, and SFX). Transcribes words via Whisper, detects silences with FFmpeg, curates best takes, cuts precisely at silence midpoints, and generates interactive HyperFrames DOM compositions with 0.12s lead verbatim subtitles, camera drifts/punch-ins, and synchronized zero-royalty audio SFX. Use when asked to "derush", "coupe les blancs", "monte mon reel", "ajoute des sous-titres", or "reel-cut".
---

# Reel-Cut: Complete Autonomous Video Editing & Motion Pipeline

Reel-Cut orchestrates the complete production lifecycle for vertical short-form video (Reels, TikTok, Shorts, YouTube) from raw camera rushes to final rendered video.

## Philosophy: Separation of Signal Processing and Semantic Curation

> **A Language Model NEVER invents or guesses cut timestamps.**
> - **Where to cut**: Deterministic signal processing via word-by-word Whisper transcription and `ffmpeg silencedetect`. Every cut is guaranteed to fall in the exact midpoint of measured silence, never cutting off a syllable or word.
> - **What to keep**: LLM reasoning. The agent reads the verbatim transcript of each speech island, identifies false starts, filler words, mistakes, and coughs, and preserves the single best take for each sentence.
> - **Graphic styling**: Never burned into the video file during editing. Everything lives in an interactive HTML/DOM composition inside **HyperFrames** powered by GSAP.

---

## 🛠️ Complete Workflow & Tool Execution

All scripts and audio assets are located directly in `tools/` and `assets/sfx/`:

### Phase 1: Derushage (Audio & Silence Cutting)
```bash
# 1. Environment diagnostic
python tools/check_env.py

# 2. Local word-by-word Whisper transcription
python tools/transcribe.py rushes/<video>.mp4 --lang fr

# 3. Generate cut plan (speech islands & silence midpoints)
python tools/cut_plan.py <slug> --min-silence 0.45 --noise -32

# 4. Agent Curation: Inspect work/<slug>_plan.json
#    Mark "keep": false on mistakes, hesitations, and false starts

# 5. Deterministic video cut assembly with 40ms micro-fades
python tools/build_cut.py <slug> --fade 0.04 --crf 18
# Outputs: assets/<slug>_cut.mp4 and work/<slug>_map.json
```

### Phase 2: Montage & Dressing (HyperFrames & GSAP)
```bash
# 1. Extract candidate verbatim overlays (~5 per minute target)
python tools/build_overlays.py <slug> --per-minute 5

# 2. Agent Curation: Inspect work/<slug>_overlays.json
#    Decide "keep": true/false and flag "punch": true on 1-2 climax moments/min

# 3. Generate / verify zero-royalty audio sound bank
python tools/make_sfx.py

# 4. Generate the DOM composition (index.html)
python tools/build_composition.py <slug> --width 1080 --height 1920

# 5. Preview & Render
npx hyperframes preview                       # Real-time studio preview
npx hyperframes render -o renders/<slug>.mp4  # Render master MP4
```

---

## 🎨 Doctrines Intégrées
1. **Typographie cinétique mot-à-mot** : Rareté volontaire (~5/min), texte strictement verbatim, avance de `0.12s` sur la voix, triple ombre portée sans bandeau noir.
2. **Mouvements de caméra** : Drifts continus et subtils (3% d'amplitude, loop 10s) + Punch-ins (+7.5% de zoom, retombée 3s) sur les révélations clés.
3. **Sound Design local** : Whoosh `0.06s` avant chaque punch, tick sur chaque raccord de plan, riser et thump.